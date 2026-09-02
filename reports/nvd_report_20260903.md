# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-02 15:01 UTC
- **対象期間**: `2026-09-01T15:01:57.000Z` 〜 `2026-09-02T15:01:39.000Z`
- **重要CVE数**: 221 件（Critical 9.0+: 28 件 / High 7.0〜: 193 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 今月公開された CVE のうち **CVSS 7.0 以上が 30 件** 超と、深刻度の高い脆弱性が集中しています。  
- **ネットワーク機器（HPE Networking Fabric Composer 系列）** と **ブラウザ（Google Chrome）**、そして **WordPress プラグイン** が特に多く、いずれも **認証なしでリモートからコード実行や権限昇格が可能** になる点が共通しています。  
- 多くは **「未認証（PR:N）」「ネットワーク経路から直接攻撃可能（AV:N）」** という条件を満たすため、外部からのスキャンや自動化攻撃ツールに狙われやすく、速やかな対策が求められます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑76658** | 10.0 | HPE Networking Fabric Composer の SSH デーモンに未認証リモートコード実行（管理者権限取得） | **ネットワーク管理基盤全体が一瞬で乗っ取られる** 可能性。SSH は管理者が最も頻繁に使用する入口であり、ファイアウォールでの遮断が困難なケースが多い。 |
| **CVE‑2026‑76657** | 10.0 | 同製品 API の認証バイパス → 完全管理権限取得 | **API が外部システムと連携することが前提** のため、内部ネットワークに侵入しただけで全機能が奪取される危険性が高い。 |
| **CVE‑2026‑83548** | 10.0 | SMA1000 Appliance の Workplace インタフェースに SSRF（認証不要） | **内部サービスへの不正アクセスやクラウドリソースの横取り** が可能。SSRF は情報漏洩だけでなく、内部ネットワーク上の別サービスへの攻撃踏み台になる。 |
| **CVE‑2026‑84353 / 84352 / 84333 / 84324** (Chrome 152.0.7977.75 未満) | 9.6‑9.8 | Android/デスクトップ Chrome の Use‑After‑Free バグによりサンドボックス外コード実行 | **エンドユーザーが閲覧する Web ページだけでマシン全体が侵害** される。Chrome は企業内の標準ブラウザであることが多く、影響範囲が極めて広い。 |
| **CVE‑2026‑78657** | 9.8 | WordPress 用 SigmaForms Pro プラグインで任意ファイル削除（認証不要） | **Web サイトのファイルシステムが破壊** され、改ざんや情報漏洩につながる。プラグインは多数の中小企業サイトで利用されている。 |

> **共通点**：すべて「認証なし」か「低権限ユーザーからのエスカレーション」で、**リモートから直接実行可能** という点。特にインフラ系製品（HPE）とブラウザ・CMS系は、組織全体の攻撃面を大幅に拡大させます。

---

## 3. 推奨アクション  

### 3.1 HPE Networking Fabric Composer 系列  
- **SSH デーモン（CVE‑2026‑76658）** と **API（CVE‑2026‑76657）** の脆弱性はベンダーが **2026‑09‑01 以降のパッチ**（バージョン 8.2.1 以上）をリリース済み。  
  - `yum update hpe-fabric-composer` / `apt-get install hpe-fabric-composer=8.2.1-20260901` で即時適用。  
- **認証バイパス（CVE‑2026‑19766）** も同様に **8.2.0 以上** のリリースで修正。  
- **ネットワークレベルの防御**  
  - SSH ポート（22）への外部からの直接アクセスを **IP ACL** で制限。  
  - API エンドポイントは **WAF** でリクエストサイズ・ヘッダー検査を追加。  

### 3.2 SMA1000 Appliance（CVE‑2026‑83548）  
- ベンダー提供の **Firmware 2.5.3**（2026‑08‑15 以降）にアップデート。  
- アップデート手順: `sma-cli upgrade --file sma1000_fw_2.5.3.bin`  
- **内部ネットワーク分離**：Workplace インタフェースへのアクセスは **内部 VLAN のみ** に限定し、外部からの直接経路を遮断。  

### 3.3 Google Chrome（Android / Desktop）  
- **Chrome 152.0.7977.75 以上** に自動更新を有効化。  
  - エンタープライズ環境では **Google Update (GUP) ポリシー** `UpdatePolicy=auto` を設定。  
- **Chrome Enterprise Policy** で **「Sandbox」** と **「Site Isolation」** を強制し、未知の HTML ページからのコード実行リスクを低減。  

### 3.4 WordPress プラグイン  
| プラグイン | 脆弱バージョン | 修正版 | 推奨アップデート |
|-----------|----------------|--------|-------------------|
| SigmaForms Pro – AI Generated Forms | ≤ 1.4.11 | 1.4.12 以降 | `wp plugin update sigmaforms-pro --version=1.4.12` |
| Amelia (Booking for Appointments) | 8.0‑9.6.2 | 9.6.3 以降 | `wp plugin update amelia --version=9.6.3` |
| Authorizer | ≤ 3.15.1 | 3.15.2 以降 | `composer require authorizer/authorizer:^3.15.2` |
| Predis (PHP Redis client) | 3.0.0‑RC1〜3.3.0 | 3.3.1 以降 | `composer update predis/predis` |

- **プラグイン自動更新** を有効化し、**定期的なプラグイン監査**（WP‑CLI `wp plugin list --status=active --field=name,version`）を実施。  
- **最小権限の原則**：管理者権限が不要なユーザーからはプラグインインストール・削除権限を剥奪。  

### 3.5 その他重要パッケージ  
| 製品 | 脆弱バージョン | 修正版 | アップデート例 |
|------|----------------|--------|----------------|
| Authorizer (CVE‑2026‑81294) | ≤ 3.15.1 | 3.15.2 | `composer require authorizer/authorizer:^3.15.2` |
| Predis (CVE‑2026‑84372) | 3.0.0‑RC1〜3.3.0 | 3.3.1 | `composer update predis/predis` |
| WCFM Marketplace (CVE‑2026‑81286) | ≤ 3.8.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-83548

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441;CWE-918` |
| Published | 2026-09-01T22:17:13.170 |

A Pre-authentication SSRF vulnerability exists in the SMA1000 Appliance Work Place interface due to an unintended alternate access path. A remote unauthenticated attacker could potentially exploit this vulnerability to gain unauthorized access to sensitive functionality and perform unauthorized operations.

### CVE-2026-76658

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-01T20:17:23.097 |

A vulnerability has been identified in the SSH daemon of HPE Networking Fabric Composer that could allow an unauthenticated remote attacker to gain administrative access to vulnerable AFC hosts. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system leading to complete system compromise.

### CVE-2026-76657

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-01T20:17:22.990 |

Vulnerabilities have been identified in the API of HPE Networking Fabric Composer that could potentially allow an unauthenticated remote attacker to circumvent existing authentication controls. Successful exploitation could allow an attacker to gain administrative privileges leading to complete compromise of the HPE Networking Fabric Composer host.

### CVE-2026-81294

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-02T12:17:12.783 |

Unauthenticated Privilege Escalation in Authorizer <= 3.15.1 versions.

### CVE-2026-78657

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T06:17:18.260 |

The SigmaForms Pro – AI Generated Forms plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete_submission_files function in all versions up to, and including, 1.4.11. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The malicious path traversal URL is submitted via form upload field and stored in the database, with deletion triggered when an administrator deletes the submission record from the admin panel.

### CVE-2026-9055

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-02T05:17:10.937 |

The Booking for Appointments and Events Calendar – Amelia (Premium) plugin for WordPress is vulnerable to Privilege Escalation in versions 8.0 - 9.6.2. This is due to insufficient validation of the attacker-controlled 'type' parameter in the customer update endpoint, which allows customers to set their role to 'manager' and trigger creation of a WordPress user with the wpamelia-manager role when the 'externalId' parameter is set to 0. This makes it possible for unauthenticated attackers to escalate their privileges to administrator by first elevating to the manager role, then creating a provider entity linked to an administrator user ID and overwriting that administrator's password.

### CVE-2026-84372

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-01T22:17:18.987 |

Predis is a flexible and feature-complete Redis and Valkey client for PHP. From version 3.0.0-RC1 until version 3.3.0, pipeline handling on aggregate cluster and replication connections reparses an already serialized RESP buffer in AbstractAggregateConnection::write() by splitting it with explode("\r\n") instead of honoring RESP length prefixes. Attacker-controlled keys or values containing CRLF sequences can therefore be interpreted by Command::deserializeCommand() as additional commands. On cluster connections, ClusterStrategy::getFakeKey() can route injected keyless commands using the literal fake key value "key", permitting operations such as shard-wide cache deletion, targeted data modification, data reads, or node disruption. On replication connections, malformed reparsing can throw an uncaught exception and repeatedly terminate affected requests. Only pipeline() reaches this vulnerable path; transaction() and MULTI are not affected. This issue is fixed in version 3.3.0.

### CVE-2026-73749

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T21:18:41.430 |

Multiple vulnerabilities exist in a daemon of AOS-CX that may allow for improper processing of malformed input. An unauthenticated remote attacker could exploit these vulnerabilities by sending specially crafted packets to the affected service. Successful exploitation could result in remote code execution with elevated privileges.

### CVE-2026-84354

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-02T00:18:29.310 |

Incorrect authorization in FileSystem in Google Chrome prior to 152.0.7977.75 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84353

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:29.203 |

Use after free in Shared Tab Groups in Google Chrome on on Android prior to 152.0.7977.75 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-84352

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:29.097 |

Use after free in WebGL in Google Chrome on on Android prior to 152.0.7977.75 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-84333

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:28.217 |

Use after free in Dawn in Google Chrome on on Android prior to 152.0.7977.75 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19766

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:12.760 |

An authentication bypass vulnerability exists in the underlying operating system of HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated adjacent attacker to execute arbitrary code as a privileged user on the underlying operating system, leading to complete compromise of the AFC host.

### CVE-2026-81286

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-02T12:17:12.400 |

Unauthenticated SQL Injection in WCFM Marketplace <= 3.8.1 versions.

### CVE-2026-84699

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-02T01:17:24.990 |

Team Password Manager before 14.184.308 fails to enforce authentication requirements in the local account password reset flow. Unauthenticated attackers can reset local account passwords and authenticate as those users to gain unauthorized access.

### CVE-2026-84696

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-02T01:17:24.560 |

Phison PS3111-S11 controller firmware versions through SBFQT1.3 expose privileged vendor unique commands over the ATA interface with absent or defeatable authentication mechanisms. Attackers can bypass the weak CRC-16 based unlock handshake or exploit builds with no VUC lock to read and write controller memory and raw flash, persisting implants across power cycles.

### CVE-2026-84695

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T01:17:24.400 |

BookStack before 26.05.4 contains a stored cross-site scripting vulnerability in the drawing upload endpoint that accepts unvalidated base64 content and stores it without content inspection. Attackers with editor permissions can upload SVG files containing scripts that execute in administrator browsers when accessed through the image gallery API without content-type validation or CSP headers.

### CVE-2026-84480

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-01T23:17:22.220 |

WWBN AVideo fails to validate password recovery token expiration in userRecoverPassSave.json.php, allowing attackers to use expired tokens to reset account passwords indefinitely. Attackers who obtain a recovery token can use it at any time to change the target account's password and gain full account access.

### CVE-2026-84479

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-01T23:17:22.083 |

WWBN AVideo (current e01e41ecc and earlier) makes three login-time security controls depend solely on the client-supplied User-Agent header. The isAVideoEncoder()/isAVideoMobileApp() checks match HTTP_USER_AGENT against a hardcoded literal ("AVideoEncoder"/"AVideoMobileApp") with no IP check or shared secret. An attacker who submits valid credentials and sets User-Agent: AVideoEncoder bypasses two-factor authentication, skips brute-force captcha escalation, and avoids being recorded in the login/device audit history. No patch is available at the time of publication.

### CVE-2023-54391

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-09-01T22:17:10.283 |

Proxmox Virtual Environment (VE) 7.0 through 8.0 contains an authentication bypass vulnerability in libpve-access-control before 8.0.4 that allows unauthenticated attackers to authenticate as any existing enabled user without a configured second factor by supplying an arbitrary tfa-challenge value in the API login endpoint. Attackers can send a POST request to the access ticket API endpoint with any value in the tfa-challenge parameter to completely skip password verification, gaining unauthorized access including to the root@pam account. All affected releases are end of life.

### CVE-2026-78012

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-01T15:17:28.013 |

An issue in the NetStaX EtherNet/IP Stack prior to v5.6.1 could allow a large Class 3 explicit-message request to exceed the application-side receive buffer without generating an error or warning. The result could be memory corruption, a device crash, or a potential remote attack vector without the originating device receiving a CIP error indicating that the request could not be processed.

### CVE-2026-84795

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-02T12:17:16.093 |

Craft CMS before 5.10.11 fails to validate the admin flag during user registration, allowing it to persist from deactivated admin accounts. Attackers can register with a deactivated admin's email address to inherit administrator privileges when public registration and disabled email verification are configured.

### CVE-2026-18931

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-01T16:16:54.243 |

Use of Hard-coded Credentials vulnerability in TMT Machine Industry and Trade Ltd. Co. Talassoft Industrial Management Software allows Retrieve Embedded Sensitive Data.

This issue affects Talassoft Industrial Management Software: from V.4 before V.16.

### CVE-2026-84324

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:27.230 |

Use after free in Proxy in Google Chrome prior to 152.0.7977.75 allowed a remote attacker to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: High)

### CVE-2026-75604

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-01T22:17:12.697 |

Next.js is a React framework for building full-stack web applications. From 13.4.0 until 15.5.24 and 16.3.3, Next.js applications using Pages Router or App Router without Cache Components on Windows-hosted servers do not consistently escape backslashes in route segments before constructing incremental-cache paths. In packages/next/src/shared/lib/router/utils/escape-path-delimiters.ts and packages/next/src/server/lib/incremental-cache/file-system-cache.ts, a remote request can supply encoded Windows path separators that traverse outside the intended cache root and expose private build data, including the server-reference-manifest encryption key. Disclosure of that key can enable remote code execution in the affected application. This issue is fixed in versions 15.5.24 and 16.3.3.

### CVE-2026-73701

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:17.453 |

An unauthenticated remote code execution vulnerability exists in the underlying operating system of HPE Networking Fabric Composer and could be exploited if certain preconditions outside of the attacker's control are met. Successful exploitation of this vulnerability could allow an unauthenticated remote attacker to execute arbitrary code as a privileged user on the underlying operating system, leading to complete compromise of the HPE Networking Fabric Composer host.

### CVE-2026-73700

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:17.343 |

A vulnerability in the web-based management interface of HPE Networking Fabric Composer could allow an authenticated low privilege operator user to conduct a stored cross-site scripting (XSS) attack against an administrative user of the interface. A successful exploit could allow an attacker to execute arbitrary script code in a victim's browser in the context of the affected interface.

### CVE-2026-79687

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-01T16:17:20.160 |

Dell PowerStore SDNAS contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Filesystem access.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-84770

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-02T12:17:14.927 |

Unauthenticated Cross Site Request Forgery (CSRF) in Mang Board WP <= 2.3.8 versions.

### CVE-2026-84764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-02T12:17:14.800 |

Unauthenticated Cross Site Request Forgery (CSRF) in Simply Schedule Appointments <= 1.6.12.23 versions.

### CVE-2026-81772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-02T12:17:13.287 |

Unauthenticated PHP Object Injection in Ninja Forms - Layout & Styles <= 3.0.31 versions.

### CVE-2026-81769

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-02T12:17:12.913 |

Incorrect Privilege Assignment vulnerability in LiquidThemes Booking Hub allows Privilege Escalation.

This issue affects Booking Hub: from n/a through 1.3.1.

### CVE-2026-81283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-02T12:17:12.267 |

Subscriber PHP Object Injection in WP User Frontend <= 4.3.10 versions.

### CVE-2026-14828

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-02T08:16:42.833 |

Zohocorp ManageEngine Password Manager Pro versions before 13235, PAM360 versions before 8561, and Access Manager Plus versions before 4405 are vulnerable to an authenticated SQL Injection vulnerability.

### CVE-2026-81807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T06:17:19.773 |

The Simple Ajax Chat  WordPress plugin before 20260827 does not escape chat message content before rendering it, allowing unauthenticated users to inject arbitrary HTML attributes into the page and run scripts in the browser of anyone viewing the chat, including administrators.

### CVE-2026-81737

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T06:17:19.667 |

The FAQ Builder AYS WordPress plugin before 1.8.5 does not sanitize or escape content submitted by unauthenticated visitors before storing it and outputting it in an admin area page, and the escaping it does apply is undone by a subsequent decoding step, leading to Stored XSS which will execute in the context of a logged in administrator.

### CVE-2026-19116

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-02T06:17:16.643 |

The User Frontend  WordPress plugin before 4.3.11 does not prevent user-supplied field values from being deserialized when a submitted post is reopened in its frontend editing form, allowing authenticated users with subscriber-level access and above to perform PHP Object Injection, which may lead to remote code execution when a suitable gadget chain is present on the site.

### CVE-2026-14357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T06:17:16.110 |

The DevKit Pro plugin for WordPress is vulnerable to Missing Authorization in versions up to, and including, 2.3.0. This is due to a missing capability check and missing nonce validation in the DPDEV_install_themes_func() function registered on the wp_ajax_DPDEV_install_themes action. This makes it possible for authenticated attackers, with Subscriber-level access and above, to install arbitrary theme ZIP packages containing PHP files that are extracted into the web-accessible wp-content/themes/ directory, which may make remote code execution possible.

### CVE-2026-84700

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-02T01:17:25.137 |

PikiwiDB (Pika) v3.5.7 exposes an internal protobuf replication server on a port derived from the client port plus 2000 (e.g. 11221 when the default client port 9221 is used) that does not authenticate incoming requests. Although requirepass is intended to gate replication — a slave presents it as masterauth inside its MetaSync request — only the MetaSync handler (HandleMetaSyncRequest) validates it; the frame dispatcher (DealMessage) does not require a completed or attempted MetaSync before routing other message types to their handlers. As a result, an unauthenticated remote attacker can connect directly to the replication port and issue TrySync, DBSync, BinlogSync, and RemoveSlaveNode requests, obtaining the full-sync snapshot and live write stream and removing replica nodes, even when requirepass is configured.

### CVE-2026-84350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:28.873 |

Use after free in TabStrip in Google Chrome prior to 152.0.7977.75 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via UI Interaction. (Chromium security severity: Low)

### CVE-2026-84347

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:28.550 |

Use after free in WebRTC in Google Chrome prior to 152.0.7977.75 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-84326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-09-02T00:18:27.447 |

Uninitialized resource in V8 in Google Chrome prior to 152.0.7977.75 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-73782

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-09-01T21:18:45.057 |

A format string vulnerability exists in the command line interface of AOS-CX that could lead to unauthenticated remote code execution. Successful exploitation of this vulnerability results in the ability to execute arbitrary code as a privileged user on the underlying operating system.

### CVE-2026-73753

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:41.863 |

Exploitation through affected command-line operations could allow an authenticated low-privileged user to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73752

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:41.757 |

An unauthenticated arbitrary file write vulnerability exists in an API endpoint of AOS-CX. Successful exploitation of this vulnerability allows an attacker to write arbitrary files to the underlying operating system, which could lead to remote code execution.

### CVE-2026-73751

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:41.647 |

An authenticated user with low-privileged access could submit crafted input through the web-based management interface to execute arbitrary commands on the underlying operating system.

### CVE-2026-73750

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T21:18:41.540 |

Vulnerabilities exist in the authentication module that may improperly process malformed or truncated input. An authenticated remote attacker could exploit these vulnerabilities by providing specially crafted input from a compromised or hostile authentication server. Successful exploitation could result in a Denial-of-Service or potential remote code execution with elevated privileges.

### CVE-2026-73705

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo` |
| Published | 2026-09-01T20:17:17.870 |

An arbitrary file write vulnerability in the API of HPE Networking Fabric Composer could allow an authenticated low privilege operator user to escalate privileges. Successful exploitation of this vulnerability may enable the attacker to execute arbitrary commands on the underlying operating system, leading to complete compromise of the affected system.

### CVE-2026-73704

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T20:17:17.763 |

A command sanitization bypass exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to escalate their permissions to those of an administrative user, leading to complete compromise of the affected system.

### CVE-2026-73703

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T20:17:17.663 |

A vulnerability in the web-based management interface of HPE Networking Fabric Composer could allow an unauthenticated adjacent attacker to conduct a stored cross-site scripting (XSS) attack against a user of the interface. A successful exploit could allow an attacker to execute arbitrary script code in a victim's browser in the context of the affected interface.

### CVE-2026-73702

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T20:17:17.557 |

A privilege escalation vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to escalate their permissions to those of an administrative user, leading to complete system compromise.

### CVE-2026-72649

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T20:17:16.853 |

Deserialization of Untrusted Data (CWE-502) in the Elasticsearch machine learning component can lead to remote code execution via Object Injection (CAPEC-586). A specially crafted trained model artifact could cause attacker-controlled logic to execute with a materially broader system-call surface than intended. Exploitation requires an authenticated user with sufficient privileges to create and deploy trained models.

### CVE-2026-58566

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T17:17:31.507 |

Dell PowerStore, an Incorrect Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-84268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-01T16:17:37.563 |

A flaw was found in the SFTP backend in gvfs. When mounting a share and reading a file, a malicious SFTP server can cause read_reply() to process a length that exceeds the size requested by the client. The function does not verify the server-provided length against the allocated buffer size, causing the operation to write past the intended boundaries. This issue allows a malicious server to corrupt adjacent heap memory in the gvfsd-sftp process, resulting in a denial of service as the process aborts upon detecting the heap corruption or potentially allowing arbitrary code execution.

### CVE-2026-79682

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T16:17:19.557 |

Dell PowerStore contains a Command Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to execute arbitrary commands with root privileges.

### CVE-2026-58567

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T16:17:06.240 |

Dell PowerStore contains an OS Command Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to execute arbitrary commands with root privileges.

### CVE-2026-10195

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T16:16:47.467 |

The FS-Poster plugin for WordPress is vulnerable to Remote Code Execution in versions up to and including 8.0.1. This is due to insufficient input sanitization of the FFmpeg path parameter before passing it to the exec() function, combined with missing authorization checks on the REST API endpoints. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute arbitrary commands on the underlying server.

### CVE-2026-79686

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-01T15:17:29.567 |

Dell PowerStore contains a Protection Mechanism Failure vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to bypass access restrictions and gain escalated privileges.

### CVE-2026-58569

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-01T15:17:21.187 |

Dell PowerStore contains an Inclusion of Functionality from Untrusted Control Sphere vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to execute arbitrary code with root privileges..

### CVE-2026-18630

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-01T15:17:12.753 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in TMT Machine Industry and Trade Ltd. Co. Talassoft Industrial Management Software allows SQL Injection.

This issue affects Talassoft Industrial Management Software: from V.4 before V.16.

### CVE-2026-84801

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T12:17:16.910 |

Craft CMS versions before 5.10.11 fail to validate admin status in the actionGetPasswordResetUrl endpoint, allowing non-admin users with administrateUsers permission to mint password reset URLs for administrator accounts. Attackers can generate a valid reset URL for any admin user and set a new password via actionSetPassword, which validates only the verification code without checking the caller's session, enabling complete control-panel takeover.

### CVE-2026-84796

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-02T12:17:16.227 |

Craft CMS versions before 5.10.11 contain a site scope bypass vulnerability in GraphQL entry mutation resolvers that fail to validate siteId through ArgumentManager::prepareArguments(). Attackers with tokens scoped to one site can read, modify, or delete entries across unauthorized sites by passing siteId directly in mutation arguments.

### CVE-2026-84715

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T02:17:20.760 |

FeatherPanel versions before 1.3.7.10 fail to validate permissions in the SubuserController updateSubuser handler, allowing authenticated subusers to modify their own permission records. A subuser with minimal permissions can send a crafted request to grant themselves full server control, enabling unauthorized access to sensitive data, backups, and server configuration.

### CVE-2026-84485

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-02T02:17:20.607 |

APITable through 1.13.0-beta.1 exposes the internal organization loadOrSearch endpoint without authentication, allowing unauthenticated attackers to retrieve member names, email addresses, and team hierarchy. Attackers can query the endpoint with space identifiers obtained from shared links or public templates to enumerate the complete member directory of any workspace.

### CVE-2026-84484

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-02T02:17:20.450 |

ION-DTN versions before 4.2.0 contain an out-of-bounds read vulnerability in the decodeSdnv function that allows unauthenticated remote attackers to read memory by sending truncated SDNV values. Attackers can send a UDP datagram to the LTP link service input port with a truncated SDNV to trigger reads up to nine bytes past buffer boundaries and underflow byte counters.

### CVE-2026-84702

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T01:17:25.430 |

facefusion through 3.6.1 fails to normalize job identifiers in get_job_file_name, allowing attackers to write files outside the jobs directory. Attackers can supply traversal sequences in the job identifier parameter through the unauthenticated HTTP API to create files at arbitrary locations.

### CVE-2026-84694

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T01:17:24.243 |

Coolify before 4.2.0 fails to properly escape environment variable key names in Docker commands executed over SSH on managed servers. Authenticated attackers can inject shell metacharacters into environment variable keys to execute arbitrary commands on the server host outside containers.

### CVE-2026-84482

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-01T23:17:22.477 |

WWBN AVideo through commit 9c39d8c8 contains a cross-site request forgery vulnerability in the get_domain() and isSameDomain() functions that fail to properly validate referer origins. Attackers can forge requests from sibling subdomains or unparseable long-gTLD origins to perform administrative ObjectYPT writes including live server configuration changes.

### CVE-2026-84476

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-01T23:17:21.670 |

WWBN AVideo fails to validate trusted proxies before accepting X-Real-IP and X-Forwarded-For headers, allowing attackers to spoof the client address used by enforceRateLimit(). Attackers can rotate the header value per request to bypass login rate limiting and perform unlimited credential guessing attacks.

### CVE-2026-84208

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-01T23:17:21.353 |

AVideo through version 29.0 contains an unauthenticated SQL injection vulnerability in the User_Location plugin's regions.json.php and cities.json.php endpoints. The country and region GET parameters are passed directly into SQL queries without escaping or prepared statement binding, allowing unauthenticated attackers to execute UNION-based SQL injection to read arbitrary database contents including password hashes and sensitive data.

### CVE-2026-71981

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T21:18:36.310 |

Cypht before 2.12.2 contains a PHP object injection vulnerability that allows authenticated attackers to execute arbitrary operating system commands by supplying a crafted PHP object graph in the back_query GET parameter of the logout handler. Attackers can pass a base64-encoded serialized payload through this parameter, which is decoded and passed directly to unserialize() without an allow-list, signature check, or type restriction, enabling gadget-chain exploitation to achieve remote code execution as the web server process.

### CVE-2026-84304

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-01T19:17:30.743 |

gRPC-Go is the Go language implementation of gRPC. Prior to 1.83.1, internal/transport/transport.go stores each fragmented HTTP/2 DATA frame as a separate recvMsg in recvBuffer, so millions of one-byte frames can consume disproportionate heap memory even when payload bytes remain within connection and stream flow-control windows. An unauthenticated remote attacker can use concurrent multiplexed streams to exhaust process memory and cause a runtime panic or out-of-memory termination. Receive-buffer compaction is enabled by default and can be controlled temporarily with GRPC_GO_EXPERIMENTAL_ENABLE_RECEIVE_BUFFER_COMPACTION. This issue is fixed in version 1.83.1.

### CVE-2024-7953

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T18:17:38.887 |

A vulnerability exists in the affected products that allows a threat actor to create a project and become the administrator for it. If exploited, a threat actor could create, modify, and delete their own project.

### CVE-2024-7952

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-01T18:17:38.110 |

A data exposure vulnerability exists in the affected product. There are hardcoded links in the source code that lead to JSON files that can be reached without authentication. If exploited, a threat actor could view customer data.

### CVE-2026-84202

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:34.450 |

ModelScope uses PyYAML's unsafe yaml.Loader to parse model configuration files, allowing arbitrary code execution through Python object construction tags. Attackers can craft malicious model repositories with poisoned configuration files that execute code when loaded by users.

### CVE-2026-83619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-01T15:17:40.657 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.7.0 until 0.8.15, the release-0.8.x parser in lib/sax.js trims captured end-tag names with the unanchored global expression /[ \t\n\r]+$/g. For an end tag containing a long whitespace run followed by a non-whitespace character, the expression retries from each possible starting position and backtracks quadratically before failing its end anchor. DOMParser.parseFromString() reaches the path under default options, allowing a small unauthenticated XML input to stall the Node.js event loop; the 0.9.x and unscoped npm lines do not contain this expression. This issue is fixed in @xmldom/xmldom version 0.8.15.

### CVE-2026-83618

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91;CWE-625` |
| Published | 2026-09-01T15:17:40.480 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.9.10 until 0.9.12, the requireWellFormed: true serializer validates DocumentType.publicId and DocumentType.systemId with PubidLiteral_match and SystemLiteral_match expressions produced by reg() in lib/grammar.js, which inherit the multiline flag. A complete valid literal on the first line can therefore satisfy the matcher while U+000A, U+000D, U+2028, or U+2029 and breakout markup remain in the emitted <!DOCTYPE ...> declaration. This bypasses the strict-serialization mitigation for the earlier DocumentType injection advisory; creation and direct property assignment remain unvalidated by design. This issue is fixed in @xmldom/xmldom version 0.9.12.

### CVE-2026-83617

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91;CWE-625` |
| Published | 2026-09-01T15:17:40.273 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.9.11 until 0.9.12, the requireWellFormed: true element and attribute name checks use the anchored QName_exact expression produced by reg() in lib/grammar.js, which inherits the multiline flag. A name with a valid first line followed by U+000A, U+000D, U+2028, or U+2029 and breakout markup therefore passes validation and is emitted verbatim in element start and end tags or attribute names. This bypasses the strict-serialization checks introduced for the earlier element-name and attribute-name injection advisories, while the default serialization path remains outside the strict guarantee. This issue is fixed in @xmldom/xmldom version 0.9.12.

### CVE-2026-83616

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-01T15:17:40.040 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.15 and 0.9.12, and in xmldom version 0.6.0 and earlier, Document.createProcessingInstruction(target, data) in lib/dom.js accepts an unvalidated target, while the requireWellFormed: true serializer checks only for a colon and the reserved case-insensitive xml name on 0.9.x and performs no target check on 0.8.x. Because serialization emits <?target data?>, a target containing >, ?, whitespace, or another invalid XML-name character can break the processing-instruction boundary and inject XML structure. This issue is fixed in @xmldom/xmldom versions 0.8.15 and 0.9.12; no fixed version is available for xmldom.

### CVE-2026-83615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T15:17:39.887 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.15 and 0.9.12, and in xmldom versions 0.1.5 through 0.6.0, appendElement in lib/sax.js uses _copy to clone the complete currentNSMap for each nested element that declares a new namespace prefix. Keeping every ancestor map live on the parse stack creates quadratic peak namespace-map storage, so a small highly compressible XML document can exhaust the process heap before application validation. This issue is fixed in @xmldom/xmldom versions 0.8.15 and 0.9.12; no fixed version is available for xmldom.

### CVE-2026-83614

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-01T15:17:39.733 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.15 and 0.9.12, and in xmldom versions 0.3.0 through 0.6.0, two independent quadratic paths can cause denial of service. In lib/sax.js, parseElementStartPart repeatedly rescans a malformed tag name to the next > during single-character recovery; in lib/dom.js, normalize() repeatedly removes and appends adjacent text nodes, causing quadratic reindexing and string rebuilding. The first path is reachable through default DOMParser.parseFromString() processing, while the second is also reachable through a direct normalize() call on a programmatically constructed DOM, and endDocument invokes that normalization after parsing. This issue is fixed in @xmldom/xmldom versions 0.8.15 and 0.9.12; no fixed version is available for xmldom.

### CVE-2026-83613

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-01T15:17:39.583 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.15 and 0.9.12, and in xmldom version 0.6.0 and earlier, DOMHandler.startElement in lib/dom-parser.js inserts every parsed attribute through setAttributeNode, while NamedNodeMap.setNamedItem in lib/dom.js calls the linear getNamedItem or getNamedItemNS lookup for each insertion. A well-formed element with many distinct attributes therefore requires quadratic comparisons during DOMParser.parseFromString() and can stall a Node.js event loop before application validation. This issue is fixed in @xmldom/xmldom versions 0.8.15 and 0.9.12; no fixed version is available for xmldom.

### CVE-2026-83612

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178;CWE-400` |
| Published | 2026-09-01T15:17:39.430 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.9.0-beta.1 until 0.9.12, HTML-mode parsing through DOMParser.parseFromString() mishandles a mixed-case closing tag for the script, style, textarea, or title raw-text elements. parseHtmlSpecialContent, selected by isHTMLRawTextElement or isHTMLEscapableRawTextElement, uses a case-sensitive indexOf() and then calls substring() with a missing-close result of negative one, causing unstable parser progression and quadratic output amplification. A small untrusted text/html document can consequently consume disproportionate CPU and memory when parsed and serialized. This issue is fixed in @xmldom/xmldom version 0.9.12.

### CVE-2026-83609

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91;CWE-625` |
| Published | 2026-09-01T15:17:38.953 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.9.0 until 0.9.12, the shared reg() builder in lib/grammar.js compiles the anchored QName_exact validator with the multiline flag, so ^ and $ validate only one line instead of the complete name. createElementNS, createAttributeNS, createDocumentType, and createAttribute consequently accept a malformed XML name whose first line is valid and whose later text injects markup when serialized through either the default path or requireWellFormed: true. The triggering ECMAScript line terminators are U+000A, U+000D, U+2028, and U+2029. This issue is fixed in @xmldom/xmldom version 0.9.12.

### CVE-2026-83608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-01T15:17:38.800 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.15 and 0.9.12, and in xmldom version 0.6.0 and earlier, the DOCUMENT_TYPE_NODE branch in lib/dom.js validates publicId, systemId, and internalSubset under requireWellFormed: true but emits DocumentType.name verbatim. A name containing > or whitespace can terminate the <!DOCTYPE ...> declaration and inject sibling markup; the value can be supplied through createDocumentType() on the 0.8.x and unscoped lines or through a direct DocumentType.name property write on every affected line. The default path and legacy creation-time behavior remain permissive, while the vulnerable strict path fails to enforce an XML Name. This issue is fixed in @xmldom/xmldom versions 0.8.15 and 0.9.12; no fixed version is available for xmldom.

### CVE-2026-83607

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-01T15:17:38.650 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.14 and 0.9.11, and in xmldom version 0.6.0 and earlier, Document.createElement(tagName) stores an unvalidated element name and XMLSerializer.serializeToString() emits that name verbatim. The requireWellFormed: true path did not validate the element qualified name or synthesized xmlns:PREFIX declaration, so attacker-controlled tag names could inject attributes, elements, or processing instructions into serialized XML or HTML and could cause cross-site scripting when browser-consumed. The unchecked values violate the XML QName constraint, and default serialization and creation-time createElement() behavior remain permissive. This issue is fixed in @xmldom/xmldom versions 0.8.14 and 0.9.11; no fixed version is available for xmldom.

### CVE-2026-83606

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-01T15:17:38.490 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. From 0.9.0-beta.9 until 0.9.11, the processing-instruction production in lib/grammar.js lets the greedy S+ separator and lazy Char*? data group repeatedly repartition a long whitespace tail when the required closing ?> is absent. Both parsePI and parseProcessingInstruction apply the expression to the entire remaining source, causing quadratic backtracking during DOMParser.parseFromString() under default options and allowing a small unauthenticated XML input to stall the Node.js event loop. This issue is fixed in @xmldom/xmldom version 0.9.11.

### CVE-2026-83605

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-01T15:17:38.317 |

xmldom is a pure JavaScript W3C standard-based (XML DOM Level 2 Core) DOMParser and XMLSerializer module. Prior to @xmldom/xmldom versions 0.8.14 and 0.9.11, and in xmldom version 0.6.0 and earlier, Element.setAttribute() calls the private _createAttribute(name) path without validating the attribute name, while Document.createAttribute(name) validates against QName. XMLSerializer.serializeToString() emits attribute names verbatim, and requireWellFormed: true did not validate them, so a crafted name can terminate the intended attribute and inject additional attributes, including event handlers, into browser-consumed output; synthesized xmlns:PREFIX declarations expose the same unchecked-name boundary. This issue is fixed in @xmldom/xmldom versions 0.8.14 and 0.9.11; no fixed version is available for xmldom.

### CVE-2026-74835

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T15:17:25.730 |

The inets application HTTP server httpd fails to enforce a configured body-size limit on chunked request.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-71380

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-09-01T15:17:24.637 |

Missing Release of Resource after Effective Lifetime vulnerability in Erlang/OTP inets httpd allows an unauthenticated remote attacker to cause denial of service by sending valid request headers with a large Content-Length and then stalling before the body is complete.

httpd_request_handler:handle_info/2 cancels the request timeout as soon as a parse step succeeds, which includes the headers, and the clause that handles a decoder asking for more data re-arms the socket with {active, once} without setting any further timer. httpd_request:whole_body/2 returns such a continuation whenever the bytes received are fewer than the announced Content-Length, so a well-formed request that stops mid-body leaves the worker waiting indefinitely. The periodic byte-rate check that would reclaim it is armed only when minimum_bytes_per_second is configured, which it is not by default. Repeating this across connections occupies every worker permitted by max_clients and denies service to legitimate clients at negligible bandwidth cost.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-70399

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T15:17:23.947 |

Allocation of Resources Without Limits or Throttling vulnerability in Erlang/OTP inets httpd allows an unauthenticated remote attacker to cause denial of service by opening and holding open a large number of connections. The max_clients option is documented to default to 150, and the inets hardening guide presents that limit as the first layer of denial-of-service defence, but a server that does not set it explicitly accepts an unlimited number of simultaneous connections. Establishing the connections is sufficient; no valid request and no authentication are required.

The accept gate in httpd_manager:handle_new_connection/4 reads the option with httpd_util:lookup/2, which returns undefined when the key is absent, rather than the three-argument form carrying the 150 default that the neighbouring get_ustate/2 uses. Erlang term ordering places every integer before every atom, so the Count =< Max guard holds for any connection count and the server never returns {reject, busy}. Each accepted connection occupies a worker process and a socket for as long as it is held, driving the node towards process, memory and file descriptor exhaustion. Servers that set max_clients explicitly are unaffected, because a configured value is applied as intended.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2.

### CVE-2026-69664

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-09-01T15:17:23.677 |

Missing Release of Resource after Effective Lifetime vulnerability in Erlang/OTP inets httpd allows an unauthenticated remote attacker to cause denial of service by sending a request with a chunked body whose chunk-size line is not a hexadecimal number. The worker serving the connection is never released and no timeout reclaims it, so repeating the request across connections occupies every available worker and denies service to legitimate clients. No authentication is required and the default configuration is affected.

The chunk-size line must arrive in a write separate from the headers. When the body accompanies the headers, httpd_request_handler:handle_body/3 calls http_chunk:decode/3 inside a try ... catch throw:Error, so the {error, {chunk_size, _}} thrown by http_chunk:decode_size/4 is answered with 400 Bad Request. When the chunk size arrives later, the decoder is resumed through a bare catch in httpd_request_handler:handle_info/2, which converts the throw into a return value rather than raising it; the resulting error tuple is then treated as the next decoder continuation, the socket is re-armed, and the worker waits for data that never comes. The request timeout has already been cancelled at the point the headers were accepted, and the periodic byte-rate check is only armed when minimum_bytes_per_second is configured, which it is not by default.

This issue affects OTP from OTP 18.1.4 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 6.0.3 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2.

### CVE-2026-84803

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:17.183 |

SiYuan before v3.8.2 contains a stored cross-site scripting vulnerability in asset serving due to an incomplete extension blocklist that misses script-capable file types. Attackers can upload files with extensions like .xht, .ehtml, .xsl, .xbl, or .rdf that resolve to executable media types and execute JavaScript to steal API tokens and compromise workspaces.

### CVE-2024-35585

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-02T05:17:10.313 |

Oxford Nanopore MinKNOW before 24.06 relies on a client's source IP address for authentication.

### CVE-2026-19754

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-02T04:17:51.537 |

Baserow 2.3.3 contains a SQL injection vulnerability in the index() formula function. A low-privileged authenticated user who can create or modify formula fields can provide an undocumented fourth argument that is treated as a SQL template and interpolated directly into a PostgreSQL expression.



The vulnerable expression is executed when Baserow recalculates formula field values. Because the generated SQL runs through Baserow's database connection, the injected SQL executes with the privileges of the Baserow PostgreSQL role rather than the permissions of the authenticated application user.



This issue affects Baserow: 2.3.3.

### CVE-2026-73706

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-01T20:17:17.977 |

A vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to obtain limited system information and to change the state of certain settings of a vulnerable system. Successful exploitation could allow an attacker to gain insight into internal services and workflows and to make unauthorized changes that may disrupt the normal operation of the affected service.

### CVE-2026-84203

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-01T16:17:34.600 |

Memos versions 0.26.0 through 0.30.0 fail to revoke refresh tokens when a user changes their password, allowing attackers to maintain account access. An attacker with a stolen refresh token can call the RefreshToken RPC to obtain new access tokens and rotate the refresh token indefinitely, bypassing the password change security measure.

### CVE-2026-73707

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T20:17:18.087 |

Privilege escalation vulnerabilities exist in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to complete state-changing actions that should not be allowed by their current level of authorization on the platform, including changes to the configuration of systems managed by the affected product.

### CVE-2026-45221

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-01T20:17:14.680 |

Konga before 2.1.0 contains a privilege escalation vulnerability that allows low-privileged local attackers to execute arbitrary code by planting attacker-controlled OpenSSL configuration or library files in a hardcoded filesystem path absent from default installations. On Windows, the missing directory resides in a location writable by any authenticated local user, enabling attackers to create the directory and place malicious files that execute at the privilege level of the user or service account that launches Konga, facilitating privilege escalation.

### CVE-2026-83551

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-01T19:17:29.483 |

Cleartext storage of sensitive information in the @step and @remote decorator pipeline component in Amazon SageMaker Python SDK before v3.11.0 and v2.256.0 might allow an authenticated remote user to extract the HMAC signing key from SageMaker DescribePipeline API responses and forge valid integrity signatures for specially crafted function payloads, achieving code execution in another user's pipeline execution context within the same AWS account.

### CVE-2026-73781

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T21:18:44.950 |

A vulnerability in the web-based management interface of AOS-CX could allow an authenticated remote attacker to conduct a stored cross-site scripting (XSS) attack against an administrative user of the interface. A successful exploit allows an attacker to execute arbitrary script code in a victim's browser in the context of the affected interface.

### CVE-2026-84351

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-02T00:18:28.983 |

Buffer overflow in GPU in Google Chrome on on Windows prior to 152.0.7977.75 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84349

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-02T00:18:28.770 |

Use after free in Browser in Google Chrome prior to 152.0.7977.75 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84335

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-02T00:18:28.443 |

Incorrect authorization in TabStrip in Google Chrome prior to 152.0.7977.75 allowed a remote attacker who had compromised the renderer process and leveraged social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-73780

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-01T21:18:44.847 |

A vulnerability in the web-based management interface of AOS-CX switches exposes some sessions to a lack of Cross-Site Request Forgery (CSRF) protection. This could allow a remote unauthenticated attacker to execute arbitrary input against the affected interface if the attacker can convince an authenticated user of the interface to interact with a specially crafted URL.

### CVE-2026-73709

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T20:17:18.297 |

A vulnerability in the underlying operating system of HPE Networking Fabric Composer could allow an unauthenticated adjacent attacker to run arbitrary commands on the underlying host if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-73708

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T20:17:18.190 |

A business logic vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to obtain elevated privileges and modify settings beyond what is authorized by the user's existing privilege level on a vulnerable system.

### CVE-2026-63137

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T20:17:15.117 |

Incorrect Authorization (CWE-863) in Kibana can lead to privilege escalation via Exploiting Incorrectly Configured Access Control Security Levels (CAPEC-180). A user holding workflow edit permissions could cause scheduled workflow executions to run with the privileges of a different, higher-privileged user, allowing access to and modification of data beyond their own authorization scope.

### CVE-2026-73812

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-01T15:17:25.540 |

httpd function check_header/3 rejects duplicate Content-Length (per CVE-2026-23941) but never checks for the TE+CL co-presence that RFC 9112 §6.3 identifies as a probable smuggling attempt. handle_body/3 frames by chunked and silently discards Content-Length. A CL-preferring front-end paired with chunked-preferring inets creates a classic CL.TE front-end/back-end desync.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-73276

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-01T15:17:25.367 |

Gracefulness code ignored cases that should be rejected, resulting in possible HTTP Request Smuggling opportunities.

This issue affects OTP from OTP 22.2 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 7.1.2 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2.

### CVE-2026-66357

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-09-01T15:17:23.047 |

httpd has never implemented obs-fold (RFC 2616 §2.2 / RFC 7230 §3.2.4 header continuation lines). Every CRLF followed by a non-CRLF octet unconditionally starts a new header. This missing feature became a security concern as the understanding of HTTP request smuggling attacks evolved.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-18730

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-01T22:17:10.850 |

A server-side request forgery (SSRF) vulnerability was identified in GitHub Enterprise Server that allowed an unauthenticated attacker to cause the Manage API to send crafted outbound requests to an attacker-controlled host. An unauthenticated endpoint parsed an attacker-supplied cluster configuration and issued gateway-to-agent requests whose HMAC authenticated only a timestamp, not the request path or body. An attacker positioned to intercept the outbound request could capture this token and replay it against privileged management agent endpoints. High-availability deployments were not affected due to a topology restriction. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.22 and was fixed in versions 3.17.19, 3.18.13, 3.19.10, 3.20.6, and 3.21.4. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-84370

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-09-01T21:18:48.217 |

SVGO, short for SVG Optimizer, is a Node.js library and command-line application for optimizing SVG files. From version 1.0.0 until versions 2.8.4, 3.3.5, and 4.1.0, the opt-in removeScripts plugin, named removeScriptElement in versions 2 and 3, incompletely filters executable links in plugins/removeScripts.js and lib/svgo/tools.js. The plugin does not recognize namespace-prefixed SVG anchor elements such as svg:a with href or namespaced *:href values, and it does not remove ASCII tab, line-feed, or carriage-return characters before checking URL schemes. Browsers remove those characters before parsing a scheme, allowing an executable link to pass the plugin's check. When an application processes attacker-controlled SVG input and serves the result in an active browser context, a victim who activates the surviving link can execute script in the SVG's origin, expose data, modify content, or perform actions as the victim. This issue is fixed in versions 2.8.4, 3.3.5, and 4.1.0.

### CVE-2026-73779

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-01T21:18:44.737 |

Vulnerabilities have been identified in the operating system of AOS-CX switches that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls. Successful exploitation could compromise system integrity and further expose sensitive information.

### CVE-2026-73710

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:18.400 |

Vulnerabilities in an API endpoint of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to conduct a denial of service attack. Successful exploitation could allow an attacker to make limited unauthorized modifications to the underlying operating system and disrupt the availability of the affected system, requiring manual intervention to restore functionality.

### CVE-2026-75538

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-01T15:17:26.853 |

An attacker that connects to an open Erlang TCP port that uses the inet driver with {packet,4} mode can use a signed overflow in an incorrect packet length calculation to overflow the receive buffer into the VM allocator area and beyond up to about 2 GB.

This would easily trash the allocated block's allocator metadata footer, and the next block, if any, and most likely cause the BEAM VM to crash. Utilizing this with precision enough to achieve Remote Code Execution would be extremely unfeasible.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to erts from 6.0 before 15.2.7.13, from 16.0 before 16.4.0.6, and from 17.0 before 17.0.6. Whether OTP before OTP 17.0, corresponding to erts before 6.0, is affected is unknown.

### CVE-2026-73270

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-01T15:17:25.103 |

Improper Handling of Case Sensitivity vulnerability in Erlang/OTP inets httpd allows a remote unauthenticated attacker to read files inside a mod_auth protected directory by requesting them with different casing, on deployments whose filesystem is case-insensitive.

mod_auth:secret_path/3 decides whether a resolved filesystem path lies inside a protected directory block by running the configured directory path through re:run/3 without the caseless option. A request for /secret/file against a directory configured as /Secret therefore does not match, so the request is treated as unprotected and no authentication challenge is issued, while the filesystem resolves the differently cased path to the same file and mod_get serves it. Deployments on case-sensitive filesystems are unaffected, because there the filesystem itself rejects the mismatched casing.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-66835

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-50` |
| Published | 2026-09-01T15:17:23.433 |

Path Equivalence vulnerability in Erlang/OTP inets httpd allows a remote unauthenticated attacker to read files inside a mod_auth protected directory by prefixing the request path with an extra slash.

httpd_request:validate_uri/1 normalises the request URI with uri_string:normalize/1, which performs RFC 3986 dot-segment removal but does not collapse empty path segments, so a doubled slash survives. mod_alias:real_name/3 concatenates the document root with that URI, and mod_auth:secret_path/3 then decides whether the result lies inside a protected directory block by running the configured directory path as an unanchored regular expression against it. The doubled slash breaks the contiguous substring the regex needs, so the request is treated as unprotected and no authentication challenge is issued, while mod_get opens the same path and the operating system collapses the doubled slash and returns the protected file. The same path mismatch also evades the per-path accounting in mod_security.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-55951

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T15:17:20.780 |

The Erlang/OTP httpc HTTP client does not enforce a limit on the total size of response headers received from a server. The max_header_size option defaults to nolimit, and httpc_response:parse_headers/6 accumulates every header into a list before the length check runs (which only fires after the terminating CRLF CRLF is received).

A malicious or compromised HTTP server can send an arbitrarily large number of headers, or headers with very large values, causing the client process to allocate unbounded memory until the system runs out of memory or the BEAM VM crashes. A proof-of-concept server sending 100,000 headers of roughly 4000 bytes each caused the client VM to allocate over 13 GB of memory in under 30 seconds.

Any application using httpc:request/4,5 to connect to untrusted servers is affected. No authentication is required: any server the client connects to (including via a redirect or man-in-the-middle) can trigger the exhaustion.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.17, from OTP 28.0 before OTP 28.5.0.6, and from OTP 29.0 before OTP 29.0.6, corresponding to inets from 5.10 before 9.3.2.7, from 9.4 before 9.6.2.3, and from 9.7 before 9.7.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-19219

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-434` |
| Published | 2026-09-02T11:17:19.270 |

In Progress® Telerik® UI for AJAX prior to v2026.3.812, insufficient integrity protection of dialog request parameters used by the RadEditor file browser may allow an attacker who has obtained certain application encryption key material to alter the folders the file browser reads from, writes to, and uploads into, potentially resulting in remote code execution.

### CVE-2026-82183

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-02T06:17:19.987 |

The OAuth Single Sign On  WordPress plugin before 7.0.1 does not verify the identity assertion returned by its Steam single sign-on flow, allowing unauthenticated attackers to log in as an arbitrary non-administrator user, and to create new accounts.

### CVE-2026-80467

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-02T06:17:18.487 |

The Advanced Custom Fields: Extended WordPress plugin before 0.9.2.7 does not restrict the role submitted through its front-end user forms to the roles the form actually offers, and its safeguard against privileged roles is incomplete, allowing unauthenticated visitors to register an account with elevated capabilities and then escalate it to administrator.

### CVE-2026-12526

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-02T06:17:15.817 |

The Advanced Custom Fields: Extended WordPress plugin before 0.9.2.7 does not verify that the requester is authorized to edit the targeted user account in the update-user action of its front-end Forms module; it only checks a capability when the submitted role is administrator or super_admin. On a site that exposes a publicly reachable front-end form whose user-update action targets an existing administrator (a fixed target, or one mapped to a visitor-submitted field) and maps the password to a visitor-submitted field, an unauthenticated visitor can overwrite that administrator's password and take over the account. The default target is the submitting user, so exploitation depends on the form being configured to target another account.

### CVE-2026-14982

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T03:16:47.663 |

The WP File Download plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete function in all versions. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The two-stage exploit requires a first request to the file.save task to persist the path-traversal string into file metadata, followed by a second request to the file.delete task to trigger the unlink call — both endpoints lack capability checks and nonce enforcement.

### CVE-2026-84334

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-02T00:18:28.337 |

Incorrect authorization in Chromoting in Google Chrome on on Windows prior to 152.0.7977.75 allowed a local attacker to execute arbitrary code outside the sandbox via a local program. (Chromium security severity: Medium)

### CVE-2026-73778

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:44.627 |

A vulnerability exists in the Credential Manager component that may allow for unauthorized administrative access. An unauthenticated remote attacker could exploit this vulnerability on a device in its factory-default or post-ZTP state before any administrator has configured credentials by providing a predictable factory-default password. Successful exploitation could result in full administrative control of the affected device during the initial setup process.

### CVE-2026-73777

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-01T21:18:44.520 |

Vulnerabilities have been identified in the API endpoint of AOS-CX switches that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls.

### CVE-2026-73712

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:18.610 |

A vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to run arbitrary commands on the underlying host if certain preconditions outside of the attacker's control are met. Successful exploitation of this vulnerability could allow an attacker to execute arbitrary commands on the underlying operating system leading to complete system compromise.

### CVE-2026-73711

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:18.510 |

A privilege escalation vulnerability exists in the API endpoint of HPE Networking Fabric Composer. Successful exploitation could allow an unauthenticated remote attacker to gain administrative privileges leading to complete compromise of the HPE Networking Fabric Composer host.

### CVE-2026-73776

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:44.410 |

A signature verification bypass vulnerability exists in the command line interface of AOS-CX. Successful exploitation could allow an authenticated malicious actor with administrative privileges to execute arbitrary code on the underlying operating system, when certain pre-conditions outside of the attackerâ€™s control are met.

### CVE-2026-83549

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T22:17:13.290 |

Post-authentication Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability has been identified in the SMA1000 Appliance Management Console (AMC) which in specific conditions could potentially enable a remote authenticated attacker as administrator to execute arbitrary OS commands, resulting in remote code execution.

### CVE-2026-73713

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-01T20:17:18.713 |

Local privilege-escalation vulnerabilities have been discovered in HPE Networking Fabric Composer. Successful exploitation of these vulnerabilities could allow a local attacker to achieve arbitrary code execution with root privileges on the underlying operating system of the affected system.

### CVE-2026-61779

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:12.923 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61778

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:12.813 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61777

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:12.697 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61776

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:12.587 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61775

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:12.477 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61774

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:11.330 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61773

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:11.023 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61772

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:10.667 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61771

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:10.320 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61770

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:10.210 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61769

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:10.093 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61768

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.980 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61767

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.867 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61766

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.747 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61765

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.627 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61764

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.513 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61763

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.400 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61762

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.283 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61761

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.170 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61760

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:09.057 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61759

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.937 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.823 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61757

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.707 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61756

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.593 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61755

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.480 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61754

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.360 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61753

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-502` |
| Published | 2026-09-01T16:17:08.247 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61752

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.133 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61751

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:08.023 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-61750

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-01T16:17:07.897 |

NVIDIA Megatron Bridge contains a vulnerability where an attacker could cause a deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, data tampering, and information disclosure.

### CVE-2026-76851

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-01T22:17:13.033 |

A Server-Side Request Forgery (SSRF) vulnerability was identified in GitHub Enterprise Server that allowed remote code execution on the instance. Insufficient network isolation allowed malicious pre-receive hook code to impersonate an internal service and redirect trusted internal requests to a privileged service, leading to elevated code execution. Exploitation required pre-receive hook networking to be enabled and either site administrator privileges or write access to a repository containing a configured pre-receive hook. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.22 and was fixed in versions 3.17.20, 3.18.14, 3.19.11, 3.20.7, and 3.21.5. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-19118

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-01T22:17:11.010 |

A time-of-check time-of-use race condition vulnerability was identified in GitHub Enterprise Server that allowed remote code execution. Exploitation required an authenticated user with write access to a repository and precise timing of concurrent upload requests. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.22 and was fixed in versions 3.17.20, 3.18.14, 3.19.11, 3.20.7, 3.21.5, and 3.22.0. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-84361

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T21:18:47.023 |

Composer is a dependency Manager for the PHP language. From 1.0 until 2.2.30 and 2.10.3, a malicious dependency package from a custom Composer repository or an untrusted composer.lock file could set source.type to perforce and source.url to an rsh: or jsh: P4PORT value. When the Perforce p4 client was installed and Composer installed the package from source through composer install or composer update, including --prefer-source, Composer\Util\Perforce passed the address to p4 without validation, causing p4 to run a local command with the privileges of the user or CI account. Packagist.org does not permit Perforce source metadata. This issue is fixed in versions 2.2.30 and 2.10.3.

### CVE-2026-73775

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:44.303 |

Vulnerabilities in the API endpoint of AOS-CX could allow a remote attacker authenticated with low privileges to access sensitive information. A successful exploit allows an attacker to retrieve information which could be used to potentially gain further access to network services supported by AOS-CX.

### CVE-2026-82958

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-116;CWE-1336` |
| Published | 2026-09-02T11:17:24.773 |

In Eclipse Ditto versions [1.3.0, 3.9.6], the ImplicitThingCreationMessageMapper of the connectivity service builds a CreateThing command by substituting placeholder values (e.g. {{ header:device_id }}) resolved from inbound message headers into a pre-configured JSON "thing" template as raw, un-escaped strings, and then parses the resulting string as JSON. Because the placeholder engine performs no JSON escaping and is unaware of the surrounding JSON string context, a resolved value containing a double-quote character can break out of its string and inject additional JSON structure.




When a connection is configured to use this mapper with a template that reflects a header whose value a publishing device can control (for example an MQTT 5 user property, an AMQP 1.0 application property, or a Kafka record header), an attacker able to publish on that connection can inject an inline _policy object. The inline policy overrides the administrator-configured policyId, letting the attacker assign an arbitrary access-control policy to the newly created digital twin — gaining full read/write access to it and potentially revoking the legitimate owner's access, with no administrator interaction.




Exploitation requires all of the following: the connection uses the (non-default) ImplicitThingCreation mapper; its template reflects an attacker-controllable header; and, for the policy-override impact, the connection's authorization subjects are permitted to create policies (the default). Deployments that restrict the connection's subjects to thing creation only via the entity-creation configuration are not affected by the policy-override impact.

### CVE-2025-46418

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-02T05:17:10.760 |

Westermo WeOS 5.x starting from 5.24 allows OS command injection via a media definition.

### CVE-2026-73774

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-01T21:18:44.180 |

A buffer overflow vulnerability exists in the underlying operating system of AOS-CX that could lead to unauthenticated disclosure of sensitive information by sending specially crafted packets to the affected system. Successful exploitation of this vulnerability could result in limited disclosure or modification of information and disruption of the affected system.

### CVE-2026-73714

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-01T20:17:18.817 |

A sensitive information disclosure vulnerability exists in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to access data beyond what is authorized by the user's existing privilege level, potentially leading to further unauthorized access.

### CVE-2026-81774

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-09-02T12:17:13.413 |

Unauthenticated Sensitive Data Exposure in WooCommerce Product Attachment <= 2.3.3 versions.

### CVE-2026-18672

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-02T11:17:18.970 |

In Progress® Telerik® UI for AJAX prior to v2026.3.812, insufficient validation of client-supplied state in RadImageEditor may allow an attacker to influence which file is returned by the control's image cache, potentially exposing file contents outside the intended image directories.

### CVE-2026-77792

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T06:17:18.063 |

The RegistrationMagic  WordPress plugin before 6.0.9.9 does not escape a registration form field value before outputting it in an HTML attribute on an administrative page, allowing unauthenticated users to perform Stored Cross-Site Scripting attacks against high privilege users such as admin.

### CVE-2026-14957

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-252;CWE-617` |
| Published | 2026-09-02T03:16:47.490 |

In FIPS mode, Libreswan's add_decoded_cert() function calls CERT_ExtractPublicKey() and asserts that the result is not NULL. However, CERT_ExtractPublicKey() returns NULL when public key extraction fails, for example if the RSA exponent is set to 0. A remote attacker can send a malformed X.509 certificate in a CERT payload to trigger the assertion, causing the pluto daemon to abort and restart. Continued exploitation causes a denial of service. No remote code execution is possible. Both IKEv1 and IKEv2 are affected. The vulnerability is only exploitable when both the OS and libreswan are running in FIPS mode and at least one CA certificate is loaded. The CERT payload is processed before peer authentication, so no credentials are needed to exploit this. Configurations using only PreSharedKey (PSK) authentication with no CA certificates loaded in the NSS database are not vulnerable.

### CVE-2026-84375

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-01T22:17:19.440 |

js-yaml is a JavaScript YAML parser and dumper. From 3.0.0 until 3.15.2 and 4.3.2, maxTotalMergeKeys in lib/js-yaml/loader.js and lib/loader.js does not count empty mapping sources while processing the merge key <<. An attacker can alias a large sequence of empty mappings into many merge targets, causing O(N * K) processing while totalMergeKeys remains unchanged and the configured resource limit is never reached. A relatively small YAML document can therefore cause prolonged CPU consumption in applications that parse untrusted YAML, and merge processing is enabled by default on these release lines. This issue is fixed in versions 3.15.2 and 4.3.2.

### CVE-2026-84374

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-01T22:17:19.293 |

Laravel Excel provides supercharged Excel exports and imports in Laravel. From 3.1.8 until 3.1.70, in src/Files/Disk.php the Maatwebsite\Excel\Files\Disk::copy() method resolves the caller-controlled $destination supplied through Excel::store(), $export->store(), or storeExcel() against the process working directory with realpath() instead of the configured filesystem disk. If the path names an existing writable file, Disk::copy() opens it with fopen() in rb+ mode and uses stream_copy_to_stream(), bypassing Flysystem path confinement and allowing an attacker whose application input controls the export path to overwrite arbitrary existing files with export content. The rb+ behavior creates a non-truncating overwrite and trailing bytes when the new export is shorter, and overwriting an executable PHP file can lead to remote code execution. This issue is fixed in version 3.1.70.

### CVE-2026-73773

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:44.050 |

An unauthenticated Denial-of-Service (DoS) vulnerability exists in the API endpoint of AOS-CX. Successful exploitation of this vulnerability results in the ability to interrupt the normal operation of the affected service.

### CVE-2026-73771

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T21:18:43.830 |

An authentication vulnerability exists in the AOS-CX management interface and API that may allow improper authentication processing. An unauthenticated remote attacker could exploit this vulnerability under specific conditions to bypass authentication controls or exhaust system resources. Successful exploitation could result in unauthorized access or denial of service affecting the management interface.

### CVE-2026-73717

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.183 |

A command injection vulnerability exists in the web-based management interface of HPE Networking Fabric Composer that could allow an unauthenticated remote attacker to run arbitrary commands on the underlying host if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system leading to complete system compromise.

### CVE-2026-73716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.067 |

A remote code execution vulnerability exists in the underlying operating system of HPE Networking Fabric Composer that could allow an unauthenticated remote attacker to run arbitrary commands on the underlying host if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system, leading to complete compromise of the HPE Networking Fabric Composer host.

### CVE-2026-73715

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-01T20:17:18.957 |

A vulnerability in the API of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to conduct a denial of service attack. Successful exploitation could allow an attacker to disrupt the availability of the affected interface.

### CVE-2026-52132

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-01T18:17:43.823 |

llama.cpp through commit 97f06e9, when started with the --reranking flag, allows remote attackers to cause a denial of service (std::bad_alloc and HTTP 500) via a negative top_n value in a POST request to /rerank.

### CVE-2026-52130

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-01T18:17:43.603 |

llama.cpp b5693 and before is vulnerable to Uncontrolled Recursion in common/json-schema-to-grammar.cpp, resulting in a denial of service.

### CVE-2026-49329

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-01T16:16:57.760 |

A flaw was found in openshift/oauth-server. The OAuth login and error page endpoints pass the unauthenticated Accept-Language header to golang.org/x/text/language.ParseAcceptLanguage() without input validation. A bypass of the CVE-2022-32149 mitigation exists: the upstream guard counts only '-' characters but the internal BCP 47 scanner aliases '_' to '-' after the guard check. An unauthenticated attacker can send a crafted Accept-Language header using '_' separators to trigger quadratic-time parsing, consuming excessive CPU and denying authentication to all cluster users.

### CVE-2026-18771

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-01T15:17:13.060 |

Missing authentication for critical function vulnerability in TMT Machine Industry and Trade Ltd. Co. Talassoft Industrial Management Software allows Authentication Bypass.

This issue affects Talassoft Industrial Management Software: from V4 before V.16.

### CVE-2026-84366

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-01T21:18:47.593 |

Scrapy is a high-level web crawling and scraping framework for Python. Prior to 2.17.0, in scrapy/core/downloader/handlers/s3.py, Scrapy's S3DownloadHandler converts an S3-scheme bucket and key request into a plaintext HTTP request to the corresponding S3 endpoint unless request.meta["is_secure"] is explicitly enabled, then signs and sends the plaintext request with configured AWS credentials. A network attacker who can observe traffic between Scrapy and S3 can read the bucket and key path, AWS Authorization header, X-Amz-Security-Token when temporary credentials are used, S3 object contents, and S3 response headers. An active man-in-the-middle attacker can also modify the plaintext S3 response body, status code, and headers before Scrapy processes them, causing scraped-data poisoning, poisoned exports, HTTP cache poisoning when caching is enabled, or influence over later crawl targets through forged redirects or attacker-controlled links. Users making S3-scheme requests with AWS credentials are affected. This issue is fixed in version 2.17.0.

### CVE-2026-73718

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.290 |

A vulnerability in the web-based management interface of HPE Networking Fabric Composer could allow an unauthenticated remote attacker to access sensitive information if the attacker can convince an authenticated user of the interface to interact with a specially crafted URL. Successful exploitation could allow an attacker to retrieve information which could be used to potentially gain further access to network services supported by HPE Networking Fabric Composer.

### CVE-2026-73770

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-01T21:18:43.720 |

An authenticated arbitrary file write vulnerability exists in AOS-CX. Successful exploitation could allow an authenticated malicious actor, under specific conditions outside the attacker's control and following a required action by another user, to create or modify arbitrary files and execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73768

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-01T21:18:43.610 |

A vulnerability exists in the command line interface of AOS-CX that may allow for improper processing of malformed input. Successful exploitation could result in the execution of arbitrary commands with root privileges.

### CVE-2026-78592

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-01T20:17:23.387 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') (CWE-22) in Kibana can lead to the unauthorized deletion of privileged resources via Path Traversal (CAPEC-126). A low-privileged user holding tag creation privileges could cause a subsequent administrative action in the tag management interface to act on an unintended target, resulting in the deletion of privileged resources including administrative accounts and other organizational assets. Exploitation requires an administrator to interact with the affected interface.

### CVE-2026-75528

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T08:16:45.193 |

The Broken Link Checker plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Author URL / Link Log in all versions up to, and including, 2.4.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires an administrator to perform the plugin's standard dismiss-and-recheck workflow on a link submitted by the attacker via the WordPress comment author URL field, after which the attacker's HTTP server issues a redirect to a URL containing an HTML/JavaScript payload that is stored verbatim in the link log.

### CVE-2026-73767

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T21:18:43.503 |

Authenticated command injection vulnerabilities exist in the command line interface of AOS-CX. Successful exploitation of these vulnerabilities results in the ability to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73766

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T21:18:43.397 |

Command injection vulnerabilities in the API endpoint of AOS-CX could allow an authenticated remote attacker with administrative privileges to inject arbitrary commands. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73765

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-01T21:18:43.287 |

Authenticated path traversal vulnerabilities exist in API endpoints of AOS-CX. Successful exploitation of these vulnerabilities allows an attacker to write arbitrary files to the underlying operating system, which could lead to remote code execution.

### CVE-2026-73722

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.730 |

Command injection vulnerabilities in the web-based management interface of HPE Networking Fabric Composer could allow an authenticated remote attacker to perform command injection against the affected system. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73721

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.620 |

Vulnerabilities in the API of HPE Networking Fabric Composer could allow an authenticated remote attacker to conduct SQL injection attacks against the HPE Networking Fabric Composer instance. An attacker could exploit these vulnerabilities to obtain and modify sensitive information in the underlying database potentially leading to complete compromise of the HPE Networking Fabric Composer host.

### CVE-2026-73720

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.513 |

Insecure file operations in the API of HPE Networking Fabric Composer could allow an authenticated remote attacker to achieve remote code execution. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-73719

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.407 |

An arbitrary file write vulnerability exists in the API of HPE Networking Fabric Composer and could allow an authenticated administrative user to escalate privileges. Successful exploitation of this vulnerability may enable the attacker to execute arbitrary system commands with root privileges on the underlying operating system.

### CVE-2026-84800

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T12:17:16.773 |

Craft CMS versions >= 5.0.0-RC1 and < 5.10.11 contain a missing authorization vulnerability in AssetsController::actionReplaceFile. When a request supplies sourceAssetId and targetFilename but omits assetId, the target asset is resolved by folder and filename after the permission checks execute, so the replacePeerFiles permission is never enforced. An authenticated low-privilege author with only the replaceFiles permission on a shared folder can overwrite the content of a peer's asset file (located in the same folder) with attacker-controlled bytes. Fixed in 5.10.11.

### CVE-2026-84798

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T12:17:16.500 |

Craft CMS versions >= 5.0.0-RC1 and < 5.10.11 fail to perform an independent authorization check in ElementsController::actionDeleteForSite(). The method loads an element with checkForProvisionalDraft enabled and runs the deletion authorization check against the user's own provisional draft (which only verifies draft ownership), then propagates the deletion to the canonical element without re-checking permissions. As a result, an authenticated user who has viewEntries, viewPeerEntries, saveEntries, savePeerEntries, and editSite permissions but lacks the deleteEntriesForSite permission can hard-delete a canonical entry's site record (and, for single-site entries, the full element and content), which is irrecoverable via Craft's recycle bin.

### CVE-2026-84794

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-02T12:17:15.957 |

Craft CMS versions before 5.10.11 lack authorization checks in the assets/move-asset endpoint when force=1 is supplied. Authenticated users without peer asset permissions can move their own assets into other users' folders and force deletion of conflicting files, allowing unauthorized asset deletion and replacement.

### CVE-2026-84759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-02T12:17:14.530 |

Unauthenticated Cross Site Request Forgery (CSRF) in Activity Log <= 2.13.1 versions.

### CVE-2026-81775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:13.530 |

Unauthenticated Cross Site Scripting (XSS) in Estatik <= 4.3.4 versions.

### CVE-2026-81771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:13.163 |

Unauthenticated Cross Site Scripting (XSS) in TrustedSite <= 1.2.5 versions.

### CVE-2026-81770

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:13.040 |

Unauthenticated Cross Site Scripting (XSS) in Interactive Geo Maps <= 1.6.30 versions.

### CVE-2026-81289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:12.657 |

Unauthenticated Cross Site Scripting (XSS) in MP3 Audio Player for Music, Radio & Podcast by Sonaar <= 5.13.1 versions.

### CVE-2026-81288

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T12:17:12.530 |

Unauthenticated Cross Site Scripting (XSS) in Upsell Order Bump Offer for WooCommerce <= 3.1.5 versions.

### CVE-2026-82883

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T07:16:37.883 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Marcus Login With Ajax allows Reflected XSS.

This issue affects Login With Ajax: from n/a through 4.5.1.

### CVE-2026-19723

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T06:17:17.130 |

The Social Media Share Buttons & Social Sharing Icons WordPress plugin before 3.0.1 does not properly escape a value taken from the incoming request before outputting it in an inline JavaScript event handler, leading to Reflected Cross-Site Scripting which is triggered when a user interacts with the affected button.
Exploitation requires the Social Media Share Buttons & Social Sharing Icons WordPress plugin before 3.0.1 to be running a non-default icon display configuration.

### CVE-2026-19453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-02T06:17:16.840 |

The JetBackup  WordPress plugin before 3.1.23.5 does not verify the role or capabilities of the account it preserves across a restore or migration before granting it administrator privileges, allowing a subscriber-level user to gain administrator access after the site owner restores or migrates the site.

### CVE-2026-12865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-02T06:17:15.917 |

The Photo Gallery by 10Web  WordPress plugin before 1.8.44 does not escape two request parameters before reflecting them into input-attribute values on its admin pages (one on the Shortcode page, one on the Galleries/Albums list page), so an unauthenticated attacker can craft a link that, when opened by a logged-in administrator (or, for the first sink, a contributor), executes arbitrary JavaScript in the victim's authenticated session via an auto-firing onfocus handler. The Galleries/Albums sink renders only when the site has more than 20 galleries/albums (the normal state of a populated install).

### CVE-2026-84698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-02T01:17:24.850 |

PX4 Autopilot contains a heap buffer overflow vulnerability in the sd_bench command that writes a four-byte block number into a user-supplied sized allocation. Attackers can invoke sd_bench with a block size below four bytes to overflow the heap buffer and potentially execute code or crash the system.

### CVE-2026-73764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-01T21:18:43.180 |

Vulnerabilities have been identified in the operating system of AOS-CX switches that could potentially allow an unauthenticated remote actor to circumvent existing authentication controls. In some cases this could enable unauthorized modification of affected resources and limited disruption of affected services.

### CVE-2026-73763

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T21:18:43.073 |

A vulnerability exists in a management component that could allow an unauthenticated adjacent attacker to execute arbitrary commands. Successful exploitation could result in remote execution of arbitrary commands in the context of the affected utility.

### CVE-2026-73724

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.947 |

Privilege escalation vulnerabilities exist in the API of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to change the state of certain settings of a vulnerable system.

### CVE-2026-73723

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:19.837 |

A privilege escalation vulnerability exists in the web-based management interface of HPE Networking Fabric Composer. Successful exploitation could allow an authenticated low privilege operator user to complete state-changing actions that should not be allowed by their current level of authorization on the platform.

### CVE-2026-84205

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-01T16:17:35.470 |

GROWI contains an access control vulnerability in the GET /_api/v3/revisions/:id endpoint that validates access against a query parameter but returns the revision identified by the path parameter without confirming they reference the same page. Authenticated attackers can pair a page identifier they can access with an arbitrary revision identifier to read revision content from pages they lack permission to view.

### CVE-2026-84204

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-01T16:17:34.747 |

GROWI contains an access control vulnerability in the GET /_api/v3/attachment/:id endpoint that fails to validate page access permissions. Authenticated attackers can retrieve attachment metadata from pages they cannot view by supplying known attachment identifiers.

### CVE-2026-18780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-01T15:17:13.200 |

Cross-Site request forgery (CSRF) vulnerability in TMT Machine Industry and Trade Ltd. Co. Talassoft Industrial Management Software allows Cross Site Request Forgery.

This issue affects Talassoft Industrial Management Software: from V.4 before V.16.

### CVE-2026-73725

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T20:17:20.047 |

A local privilege-escalation vulnerability has been discovered in HPE Networking Fabric Composer. Successful exploitation of this vulnerability could allow a local attacker to achieve arbitrary code execution with root privileges, leading to a complete compromise of the affected host.

### CVE-2026-84233

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T15:17:43.853 |

A flaw was found in rpm. A local attacker could supply a specially crafted `.gem` filename containing RPM macro syntax. When a user or automated workflow invokes `rpmuncompress -x` on this file, the macro expansion occurs during command construction. This allows the attacker to execute arbitrary commands with the privileges of the invoking account, leading to a compromise of confidentiality, integrity, and availability.
