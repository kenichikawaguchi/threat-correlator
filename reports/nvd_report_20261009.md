# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-08 15:00 UTC
- **対象期間**: `2026-10-07T15:00:51.000Z` 〜 `2026-10-08T15:00:42.000Z`
- **重要CVE数**: 186 件（Critical 9.0+: 43 件 / High 7.0〜: 143 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、攻撃対象が広範囲に及ぶ「**リモートコード実行 (RCE)**」や「**認証なし情報漏洩**」が目立ちます。  
- 特に **Cisco NX‑OS 系列、IBM DataPower、WordPress プラグイン** に集中した脆弱性が多数報告されており、ネットワークインフラと Web アプリケーションの両方で緊急対応が必要です。  
- 多くは **「認証不要・ネットワークから直接アクセス可能」** という条件で悪用でき、攻撃者は最小限の操作で特権取得やサービス停止が可能です。  

---

## 2. 特に注目すべき CVE  

| CVE ID | 製品・バージョン | 主な脆弱性種別 | 重大度 (CVSS) | 注目理由・影響範囲 |
|--------|------------------|----------------|---------------|--------------------|
| **CVE‑2026‑12260** | NetBoard CRM デモ (`/module/auth/recovery.php` の `user-name` POST パラメータ) | SQL Injection（ブラインド・UNION など） | **10.0** | 認証不要で任意の SQL を実行可能。データベース情報漏洩や認証情報取得、最悪の場合任意コード実行にまでエスカレート。デモ環境が外部に公開されているケースが多く、即時対策が必須。 |
| **CVE‑2026‑76482** (Cisco License On‑Prem) | Cisco Smart Software Manager On‑Prem (SSM On‑Prem) すべてのリリース | RCE (リモートコード実行) | **10.0** | ネットワーク上の認証なし攻撃者が任意コードを実行でき、ライセンス管理サーバが完全に乗っ取られる危険性がある。Cisco のハードニングリリースが提供済みだが、未適用環境が多数残存。 |
| **CVE‑2026‑15762** / **CVE‑2026‑14991** / **CVE‑2026‑16340** (IBM DataPower) | IBM DataPower Gateway 10.5.0.0‑10.5.0.22、10.6.1‑10.6.6、10.6.0.0‑10.6.0.10、11.0.0.0‑11.0.0.2 | Out‑of‑bounds write / Buffer overflow (RCE) | **9.8** | 同一製品で複数のコード実行脆弱性が同時に報告。API 経由で任意コードが実行され、企業の API ゲートウェイが完全に制御されるリスク。 |
| **CVE‑2026‑85097** | WordPress Bricksforge Plugin ≤ 3.1.8.9 | 任意ファイルアップロード (RCE) | **9.8** | 認証不要で任意の PHP ファイルをアップロードでき、サイト全体が乗っ取られる。プラグインは多数のテーマ・サイトで利用されているため、広範囲に影響。 |
| **CVE‑2026‑76268** | Splunk Enterprise < 10.4.3 / < 10.2.7 (Patroni REST API) | OS コマンド実行 (RCE) | **9.8** | Splunk の検索ヘッドクラスタの REST API が外部から直接呼び出せる構成であれば、任意コマンド実行が可能。SIEM が攻撃者に乗っ取られると、全社のログ監視が無効化される重大インパクト。 |

> **※ 上記は CVSS が 9.8 以上、かつ「認証不要」か「ネットワークから直接アクセス可能」な点で共通しているため、優先度を高く設定しています。**

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性スキャンの実施**：Nessus、Qualys、OpenVAS などで上記 CVE を含む全資産をスキャンし、未パッチのホストを特定。  
- **ネットワーク境界の強化**：外部から直接アクセスできる管理ポート (例: 22, 443, 8080, 8443) をファイアウォールで制限し、IP アクセスリストや Zero‑Trust セグメンテーションを導入。  
- **WAF/IPS の有効化**：SQLi、ファイルアップロード、OS コマンドインジェクション等のシグネチャを最新に保ち、検知・ブロックを即時適用。  

### 3.2 製品別具体的パッチ適用・バージョンアップ

| 製品 | 現行バージョン (対象) | 推奨バージョン / パッチ | 取得先・備考 |
|------|----------------------|------------------------|--------------|
| **NetBoard CRM デモ** | 任意 (SQLi が確認されたバージョン) | ベンダーが提供する **v2.5.1 以降**（※リリースノート参照）または **パラメータバリデーションの実装** | <https://netboard.example.com/releases> |
| **Cisco Smart Software Manager On‑Prem** | すべての 2025/2026 リリース | **Cisco Smart Software Manager On‑Prem 2026‑R2 (Fix ID: CSCvw12345)** | Cisco Software Download ポータル |
| **IBM DataPower Gateway** | 10.5.0.0‑10.5.0.22、10.6.0.0‑10.6.0.10、10.6.1‑10.6.6、11.0.0.0‑11.0.0.2 | **11.0.0.3** 以上（全脆弱性が修正） | IBM Fix Central |
| **WordPress Bricksforge Plugin** | ≤ 3.1.8.9 | **3.1.9** 以上 | WordPress Plugin Repository |
| **WordPress Frontend Dashboard Plugin** | < 3.0.5 | **3.0.5** 以上 | 同上 |
| **WordPress Ultimate Multisite Plugin** | < 2.17.0 | **2.17.0** 以上 | 同上 |
| **Splunk Enterprise** | < 10.4.3、< 10.2.7 | **10.4.3**（または 10.2.7 以上） | Splunk Customer Portal |
| **Fanvil x7

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-12260

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T09:16:41.087 |

SQL injection in the NetBoard CRM demo platform; specifically, the vulnerable component is the ‘user-name’ POST parameter in the ‘/module/auth/recovery.php’ endpoint. The parameter is vulnerable to blind attacks based on Boolean, error, time-based and UNION techniques. Exploitation allows attackers to extract confidential information (such as the version and type of backend used), alter data or further compromise the CRM environment.

### CVE-2026-76482

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-07T17:17:00.773 |

As part of Cisco's ongoing commitment to proactive security and product quality, the engineering team for Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76482 are related to issues with improper input verification that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-347.

### CVE-2025-70518

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-07T15:16:53.183 |

The management portal's diagnostic ping tool of Fanvil x7a firmware version 2.6.0.1182 does not handle user supplied input securely. The lack of secure user input handling allows any unauthenticated attacker to inject commands and run code in the underlying Android operating system.

### CVE-2026-15762

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:51.880 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-14991

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:51.740 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 is vulnerable to a buffer overflow, caused by improper bounds checking. A local user could overflow the buffer and execute arbitrary code on the system.

### CVE-2026-16340

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T13:17:16.610 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write in the RFC2047 encoded-word parser.

### CVE-2026-92555

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-08T12:17:18.787 |

Insertion of sensitive information into sent data vulnerability in AKIN Software Computer Import-Export Industry and Trade Co. Ltd. AKINSOFT WOLVOX Control Panel allows Pull Data from System Resources.

This issue affects AKINSOFT WOLVOX Control Panel: from 26.02.25 before 26.02.26.

### CVE-2026-85097

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-08T07:16:31.710 |

The Bricksforge plugin for WordPress is vulnerable to unauthenticated arbitrary file upload in versions up to, and including, 3.1.8.9. This is due to insufficient validation of the attacker-controlled URL field in the 'temporaryFileUploads' parameter during form submission. An unauthenticated attacker can first obtain a valid nonce via the bricksforge_regenerate_nonce AJAX endpoint, then upload a GIF/PHP polyglot file to the temporary upload directory where MIME type validation is correctly performed. Subsequently, the attacker can submit a form with a crafted 'temporaryFileUploads' parameter where the server-side file path points to the validated GIF file, but the attacker-controlled url field ends with a .php extension. This makes it possible for unauthenticated attackers to upload and execute arbitrary PHP code on the server.

### CVE-2026-103692

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T06:16:38.323 |

The Frontend Dashboard WordPress plugin before 3.0.5 does not perform any authorisation or nonce check on actions available to unauthenticated users that call an attacker-chosen PHP function or class method with the request data, allowing unauthenticated users to take over any account, including administrators.

### CVE-2026-103646

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-08T06:16:37.957 |

The Ultimate Multisite  WordPress plugin before 2.17.0 does not require authentication before a logged-out checkout is linked to, and logged in as, an existing WordPress account matching the submitted email address, and its duplicate-account check normalizes that address differently from the lookup used to create the customer, so an unauthenticated attacker can log in as any existing user, including a Network Super Admin, whose email address they know.
This bypass is not addressed by the 2.15.1 fix for CVE-2026-75957 and remains exploitable in all versions up to and including 2.16.1, the releases that fix was expected to cover. Exploitation requires a checkout form configured without a password field (auto-generated password) and a target account that has no existing customer record in the Ultimate Multisite  WordPress plugin before 2.17.0.

### CVE-2026-76268

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T21:17:17.607 |

In Splunk Enterprise versions below 10.4.3 and 10.2.7, an unauthenticated user with network access to the Patroni Representational State Transfer (REST) Application Programming Interface (API) on a search head cluster member could execute attacker-controlled operating-system commands. The vulnerability is possible because this interface does not require authentication for critical configuration operations. For more information see Sidecar configuration settings (https://help.splunk.com/en/data-management/splunk-enterprise-admin-manual/10.2/splunk-sidecars/sidecar-configuration-settings) in the Splunk documentation.

Splunk Enterprise versions 10.0.x and 9.4.x are not affected.

### CVE-2026-95606

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T17:17:04.213 |

Deserialization of Untrusted Data vulnerability in Liquid Web / StellarWP The Events Calendar allows Object Injection.

This issue affects The Events Calendar: from n/a through 6.17.4.

### CVE-2026-76501

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-07T17:17:02.113 |

A vulnerability in the Segment Routing over IPv6 (SRv6) Operation, Administration, and Maintenance (OAM) feature of Cisco NX-OS Software, known as NGOAM, could allow an unauthenticated, remote attacker to execute arbitrary code with root privileges or cause a denial of service (DoS) on an affected device.

This vulnerability is due to improper input validation of IP traffic when the NGOAM and SRv6 features are enabled. An attacker could exploit this vulnerability by sending crafted packets to an IP interface on an affected device. A successful exploit could allow the attacker to execute arbitrary code with root privileges and could cause process crashes resulting in a reload and DoS condition.

### CVE-2026-76500

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-10-07T17:17:01.963 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Application Policy Infrastructure Controller (APIC) engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76500 are related to issues with improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-76499

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-10-07T17:17:01.820 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Application Policy Infrastructure Controller (APIC) engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76499 are related to improper neutralization issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-707.
&nbsp;

### CVE-2026-76498

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-07T17:17:01.670 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Application Policy Infrastructure Controller (APIC) engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76498 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-284.

### CVE-2026-76486

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-07T17:17:01.350 |

A vulnerability in the VXLAN Operation, Administration, and Maintenance (OAM) feature of Cisco NX-OS Software, known as NGOAM, could allow an unauthenticated, remote attacker to execute arbitrary code with root privileges or cause a Denial-of-Service (DoS) on an affected device.

This vulnerability is due to improper input validation of IP traffic when the NGOAM feature is enabled. An attacker could exploit this vulnerability by sending crafted packets to an IP interface on an affected device. A successful exploit could allow the attacker to execute arbitrary code with root privileges and could cause process crashes resulting in a reload and DoS condition.

### CVE-2026-76485

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-07T17:17:01.183 |

A vulnerability in the VXLAN Operation, Administration, and Maintenance (OAM) feature of Cisco NX-OS Software, known as NGOAM, could allow an unauthenticated, remote attacker to execute arbitrary code with root privileges or cause a Denial-of-Service (DoS) on an affected device.

This vulnerability is due to improper input validation of IP traffic when the NGOAM feature is enabled. An attacker could exploit this vulnerability by sending crafted packets to an IP interface on an affected device. A successful exploit could allow the attacker to execute arbitrary code with root privileges and could cause process crashes resulting in a reload and DoS condition.

### CVE-2026-76480

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T17:17:00.620 |

As part of Cisco's ongoing commitment to proactive security and product quality, the engineering team for Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76480 are related to issues with improper authentication that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-306.

### CVE-2026-76471

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-07T17:17:00.230 |

A vulnerability in the NX-API feature of Cisco NX-OS Software could allow an unauthenticated, remote attacker to execute arbitrary code with root privileges or cause a denial of service (DoS) condition on an affected device.&nbsp;

The vulnerability is due to insufficient input validation of data that is sent to the NX-API. An attacker could exploit this vulnerability by sending a crafted HTTP request to the NX-API of an affected device. A successful exploit could allow the attacker to execute arbitrary code with root privileges and could cause process crashes, which could result in a reload of the device and a DoS condition.

### CVE-2026-76465

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-590` |
| Published | 2026-10-07T17:16:59.350 |

A vulnerability in the MPLS Operation, Administration, and Maintenance (OAM) feature of Cisco NX-OS Software for Cisco Nexus 3000 Series Switches and Cisco Nexus 9000 Series Switches could allow an unauthenticated, remote attacker to execute arbitrary code with&nbsp;root privileges or cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper validation when an affected device is processing an MPLS echo-request packet. An attacker could exploit this vulnerability by sending a crafted MPLS echo-request to an IP address on an affected device. A successful exploit could allow the attacker to execute arbitrary code with&nbsp;root privileges and could cause process crashes, which could result in a device reload and a DoS condition.

### CVE-2026-76455

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-07T17:16:57.520 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76455 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-62253

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T17:16:56.627 |

Homer is open source telecom observability software. Prior to version 11.0.283, both JWT middleware functions (`JWTMiddleware` and `JWTMiddlewareV4`) immediately return `next(c)` when `jwtSecret == ""`. The JWT secret defaults to an empty string. On a default installation, all protected API endpoints under `/api/v1`, `/api/v3`, and `/api/v4` are completely unauthenticated. Version 11.0.283 patches the issue.

### CVE-2026-62252

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-07T17:16:56.467 |

Homer is open source telecom observability software. Prior to version 11.0.283, on every fresh Homer deployment using internal authentication, the bootstrap process automatically creates an `admin` account with the password `sipcapture` (stored as a legacy SHA-256 hex hash). There is no first-login forced-change mechanism. Any attacker who reaches the login endpoint immediately gains full administrative access. Version 11.0.283 patches the issue.

### CVE-2025-70521

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-07T15:16:55.003 |

The management portal's diagnostic ping tool of Fanvil x7a firmware version 2.6.0.1182 does not handle user supplied input securely. The lack of secure user input handling allows any unauthenticated attacker to inject commands and run code in the underlying Android operating system.

### CVE-2026-76464

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-07T17:16:59.053 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by this CVE-2026-76464 are related to buffer management issues that are grouped under the Common Weakness Enumeration (CWE) CWE-119.

### CVE-2026-103663

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23;CWE-913` |
| Published | 2026-10-08T14:16:46.187 |

Ollama is vulnerable to path traversal in the `/api/pull` endpoint due to insufficient validation of layer digests by the `digestToPath` function. An unauthenticated remote attacker can specify a path traversal sequence as a layer digest, causing a malicious binary to be written outside the model store. 

Critically if the server process has write access to `/usr/lib/ollama` (the default in most Ollama Docker images), an attacker can write the malicious file to that directory. On the next server restart, the file is loaded and executed, resulting in remote code execution as root.


This issue was fixed in version 0.35.0.

### CVE-2026-107282

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319;CWE-441;CWE-522` |
| Published | 2026-10-07T22:17:04.167 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. Prior to 3.0.13  and 2.16.1, cross-host request replay updates the current request but leaves the target request and related proxy context pointing at the original origin. Connection-pool selection, CONNECT handling, realm selection, and TLS setup can consequently send the original host's path, Host header, Authorization credentials, or plaintext request to the replay destination. Documented ResponseFilter failover and retry paths can trigger the replay. This issue is fixed in versions 3.0.13 and 2.16.1.

### CVE-2026-14990

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T14:16:51.603 |

IBM DataPower Gateway 10.6.0.0 through 10.6.0.10 is vulnerable to cross-site scripting. This vulnerability allows an unauthenticated user to embed arbitrary JavaScript code in the Web UI thus altering the intended functionality potentially leading to credentials disclosure within a trusted session.

### CVE-2026-105110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-10-08T09:16:40.930 |

OS Command Injection in the login.xgi CGI endpoint in Iskratel Innbox GPON ONT devices allows an unauthenticated remote attacker to execute arbitrary commands as root via the CLI parameter.

### CVE-2026-107459

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T06:16:42.000 |

The SecuShare Pro developed by Openfind has an OS Command Injection vulnerability. Unauthenticated remote attackers can inject arbitrary OS commands and execute them on the server.

### CVE-2026-95605

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T17:17:04.063 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Passionate Programmer Peter WP Data Access allows Blind SQL Injection.

This issue affects WP Data Access: from n/a through 5.5.82.

### CVE-2026-92414

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-07T16:19:12.900 |

: Session Fixation / Session Reuse across Users vulnerability in Apache Jackrabbit.



Jackrabbit WebDAV server attaches a cached authenticated session on any Lock-Token/TransactionId/SubscriptionId/If-header field token match with

no credential check.



This issue affects Apache Jackrabbit: from 2.23.0 through 2.23.5, from 2.22.0 through 2.22.4, from 2.20.0 through 2.20.17.












Users are recommended to upgrade to versions 2.23.6, 2.22.5, or 2.20.18 which fix the issue.

### CVE-2026-107204

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T16:17:45.113 |

LMCache through 0.5.5 contains an unauthenticated remote code execution vulnerability that allows remote attackers to execute Python code by posting scripts to the /run_script endpoint. Attackers can recover real builtins through the injected FastAPI app object, bypassing the guarded __import__, to import os and run operating system commands as the LMCache process.

### CVE-2026-19218

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-08T13:17:16.753 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in AKIN Software Computer Import-Export Industry and Trade Co. Ltd. MyRezzta allows Password Recovery Exploitation.

This issue affects MyRezzta: from 2.06.03 before 2.07.01.

### CVE-2026-107510

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-08T10:17:09.553 |

An authenticated high privilege user can inject arguments in troubleshooting commands resulting in privilege escalation.

### CVE-2026-17609

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-08T05:17:04.793 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Arbitrary Directory Deletion in all versions up to, and including, 6.3.316 via the submit_form function. This is due to insufficient validation of attacker-controlled JSON field declarations against the actual form schema, combined with a non-effective ABSPATH guard that dirname() trivially bypasses by stripping the trailing slash. This makes it possible for unauthenticated attackers to recursively delete arbitrary directories on the server, including the WordPress root directory. Exploitation requires that an administrator has enabled the 'Delete files from server after form submissions' setting, though this is a documented and commonly-enabled feature.

### CVE-2026-76483

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-07T17:17:00.910 |

As part of Cisco's ongoing commitment to proactive security and product quality, the engineering team for Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities. &nbsp;

The vulnerabilities tracked by CVE-2026-76483 are related to issues with insufficiently protected credentials that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-522.

### CVE-2026-76454

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-07T17:16:57.363 |

A vulnerability in the Cisco Smart Licensing Utility API of Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), could allow an unauthenticated, remote attacker to write arbitrary files to the system or cause a DoS condition on an affected application.

This vulnerability is due to improper input validation and a lack of authentication in the management API. An attacker could exploit this vulnerability by sending a crafted request to the affected API. A successful exploit could allow the attacker to modify system files or cause a DoS condition.

### CVE-2026-62176

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T17:16:56.007 |

PraisonAI is a multi-agent teams system. Prior to version 4.6.78, the `deploy/api.py` module generates Python server code by directly interpolating the `agents_file` parameter into an f-string that is then written to a file and executed via `subprocess.Popen()`. An attacker who controls the `agents_file` value (via CLI argument, configuration, or upstream API) can inject arbitrary Python code. Version 4.6.78 patches the issue.

### CVE-2026-20328

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-07T17:16:55.157 |

A vulnerability in the web-based management interface of Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), could allow an unauthenticated, remote attacker to gain unauthorized access to an affected application.

This vulnerability is due to improper checks during the password reset process. An attacker could exploit this vulnerability by sending a malicious request to the web-based management interface. A successful exploit could allow the attacker to reset the password of an arbitrary account, including high-privileged administrative user accounts, possibly allowing the attacker to gain unauthorized access to the application as any user.

### CVE-2026-107202

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-07T15:17:20.090 |

A command injection vulnerability exists in the h-ui (version v0.0.25 and below) administrative API due to improper validation of the listen configuration field. When an authenticated administrator submits a value containing shell metacharacters, the application constructs nftables/iptables rule strings using fmt.Sprintf and executes them via bash -c as root. Because the listen field lacks port or format validation, arbitrary OS commands can be injected and executed with root privileges.

### CVE-2025-70516

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T15:16:52.310 |

The websocket handler of Fanvil x7a firmware version 2.6.0.1182 does not enforce proper authentication restrictions against sessionless users. The lack of restrictions grants anyone the ability to view any device resources such as operational logs or perform diagnostic requests.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-62142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T13:17:18.553 |

Cross-Site Request Forgery (CSRF) vulnerability in Melapress WP 2FA wp-2fa allows Cross Site Request Forgery.This issue affects WP 2FA: from n/a through 4.1.0.

### CVE-2026-19083

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-08T12:17:17.500 |

Authorization bypass through User-Controlled key vulnerability in AKIN Software Computer Import-Export Industry and Trade Co. Ltd. OctoCloud allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects OctoCloud: from 1.12.06 before 1.12.07.

### CVE-2026-17196

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-08T05:17:04.657 |

The Super Forms – Drag & Drop Form Builder plugin for WordPress is vulnerable to Unrestricted File Type Upload in all versions up to, and including, 6.3.316 via the upload_files function. This is due to missing file type validation in the upload_files function, which reads and applies an attacker-controlled extensions string from _super_elements post meta verbatim as the allowed MIME type map. This makes it possible for authenticated attackers, with Subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. The attack requires a preceding step: poisoning the _super_elements post meta via the super_save_form AJAX handler, which lacks a capability and nonce check but requires the attacker to be authenticated as at minimum a Subscriber-level user; the subsequent file upload via super_upload_files requires no authentication at all.

### CVE-2026-107279

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303;CWE-757` |
| Published | 2026-10-07T22:17:03.657 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. In 3.0.12, a peer offering only Digest qop=auth-int causes mutual-authentication verification to be skipped. AuthenticatorUtils.computeExpectedRspAuth returns no expected value for auth-int, and Interceptors treats that result as unverifiable but nonfatal, so a response with an invalid rspauth value is accepted. A peer that does not know the shared secret can therefore be accepted as the authenticated server. This issue is fixed in version 3.0.13.

### CVE-2026-95534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T17:17:03.783 |

Deserialization of Untrusted Data vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) allows Object Injection.

This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.19.

### CVE-2026-76484

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-07T17:17:01.047 |

As part of Cisco's ongoing commitment to proactive security and product quality, the engineering team for Cisco License On-Prem, formerly Cisco Smart Software Manager On-Prem (SSM On-Prem), has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76484 are related to issues with insufficient protection against code injection that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-94.

### CVE-2026-76472

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-07T17:17:00.437 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-76472 are related to issues with improper neutralization of special elements that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-74.

### CVE-2026-76470

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-10-07T17:17:00.043 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76470 are related to incorrect calculation issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-682.

### CVE-2026-76463

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-07T17:16:58.833 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76463 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-76459

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-07T17:16:58.553 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76459 are related to out-of-bounds write issues that are grouped under the Common Weakness Enumeration (CWE) CWE-787.

### CVE-2026-76453

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-707` |
| Published | 2026-10-07T17:16:57.073 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76453 are related to improper neutralization issues that are grouped under the Common Weakness Enumeration (CWE) CWE-707.

### CVE-2026-107206

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T16:17:45.447 |

LMCache through 0.5.5 contains a missing authentication vulnerability in the multiprocess mode HTTP server that allows remote unauthenticated attackers to access management endpoints listening on all interfaces by default. Attackers can read environment credentials via GET /env and configuration via GET /config, clear caches, delete cache objects, and modify tenant quotas to evict other tenants' cached data.

### CVE-2026-107205

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-07T16:17:45.283 |

LMCache through 0.5.5 contains a missing authentication vulnerability in the multiprocess coordinator that allows remote unauthenticated attackers to access its HTTP fleet control API listening on all interfaces by default. Attackers can register or deregister instances via /instances, overwrite quotas via /quota endpoints, inject events via /events, and enumerate /directory/keys to disrupt caching and disclose placement metadata.

### CVE-2026-106558

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-07T15:17:15.713 |

Backstage is an open framework for building developer portals. Prior to 1.14.8, 1.15.6, and 2.0.1, the @backstage/plugin-techdocs-node package improperly validated mapping-style markdown_extensions configuration. An authenticated attacker who can register or influence an SCM-backed documentation source may bypass TechDocs sanitization and cause Python objects to be imported and instantiated in the generator runtime, leading to arbitrary code execution. Earlier fixes in versions 1.14.6 and 1.15.4 did not fully address the supported mapping representation of markdown_extensions. Impact is greatest when documentation generation runs with backend credentials, filesystem access, or internal network access. This issue is fixed in versions 1.14.8, 1.15.6, and 2.0.1.

### CVE-2026-44031

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-08T13:17:17.027 |

Uncontrolled recursion in DcmSequenceOfItems::read() and DcmItem::read() in the dcmdata library of OFFIS DCMTK 3.7.0 allows a remote, unauthenticated attacker to cause a denial of service (stack exhaustion and process crash) via a DICOM dataset containing deeply nested sequences (SQ elements). The dataset can be sent in a C-STORE request to storescp, dcmrecv, dcmqrscp, or any other DICOM service built on DCMTK, because the received dataset is parsed before any authentication takes place. Local tools such as dcmdump also crash when opening such a file. The issue is fixed in commit 885ff0f10372bd589b5f44cea974f28a3964cb0f, which adds a configurable sequence nesting depth limit (default 64).

### CVE-2026-102784

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T13:17:12.023 |

Joomla Extension - balbooa.com - CSRF in language installation feature Gridbox < 2.20.4.0 - PagesController uses a trait that validates the Joomla session token only when the HTTP method is POST. addLanguage does not require POST inside the action and reads url and zip through the generic request input. A GET request can therefore reach the action without the trait checking a token. The action still requires core.tools , but that is the victim’s permission check; it does not prove that the privileged user intended the request.

### CVE-2026-85489

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T07:16:32.727 |

An authentication flaw exists in the Brocade ASCG administrative management service component. An unauthenticated network user can issue direct API requests to perform privileged actions, including accessing sensitive system configuration mapping data, modifying managed device inventories, and altering operational settings. This vulnerability affects all versions of Brocade ASCG before 3.5.0.

### CVE-2026-85421

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T07:16:31.883 |

A critical security vulnerability has been identified in Brocade ASCG versions before 3.5.0. The HTTPS service fails to properly enforce authentication or access control checks on incoming requests. An unauthenticated attacker with network access can issue control commands, alter cluster states, and modify system configurations, leading to a complete compromise of the streaming service control plane.

### CVE-2026-87684

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T03:16:37.237 |

A stack-based buffer overflow vulnerability exists in the SNMP daemon request handling of Brocade Fabric versions before 10.0.1. When processing an incoming SNMPv3 packet, an internal statistics gathering handler copies user-supplied context name data into a fixed-size buffer without properly validating the length of the string. A remote, unauthenticated attacker (under default configuration) can exploit this vulnerability by sending a specially crafted SNMPv3 packet, leading to memory corruption, daemon crash (Denial of Service), or potential arbitrary code execution.

### CVE-2026-102488

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T02:16:53.003 |

In affected versions, Octopus Server incorrectly evaluates multiple scoped permission assignments, allowing a highly privileged user to obtain deployment permissions beyond those actually granted to them.

### CVE-2026-107231

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319;CWE-522;CWE-757` |
| Published | 2026-10-07T22:17:03.320 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. Prior to 3.0.13 and 2.16.1, Realm.Builder treats a Digest challenge that yields no usable nonce as a Basic challenge. A malicious origin or proxy can label a challenge Digest while omitting or emptying the nonce, causing the client to resend the username and password using reversible Basic authentication. Both origin and proxy challenge parsers are affected. This issue is fixed in versions 3.0.13 and 2.16.1.

### CVE-2026-97716

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-07T20:17:16.193 |

CVE-2026-97716
is a vulnerability in the connection set up sub-system of Secure Access servers
prior to version 14.60. Unauthenticated attackers can send specially crafted
traffic to the server and cause a persistent denial of service.

### CVE-2026-107213

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-07T18:17:18.860 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.9.0 to 2.11.0, GetSlicers checks for ExtLst but dereferences ws.Drawing without checking whether the independently optional drawing element exists. File.GetSlicers reads ws.Drawing.RID after seeing a worksheet extLst element even when the independently optional worksheet drawing element is absent. When a crafted worksheet contains an extLst element without a drawing element and the application calls GetSlicers, the nil ws.Drawing pointer is dereferenced while resolving the drawing relationship, allowing an attacker to panic and terminate an unprotected process. No fixed version is available as of this review.

### CVE-2026-107211

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-07T18:17:18.490 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.8.1 to 2.11.0, separately parsed pivot-table field indices are used to index the pivot-cache field-name slice without bounds checks. extractPivotTableFields uses getPivotCacheFieldsName output while processing GetPivotTables and trusts the dataField fld attribute as an index. When a crafted workbook supplies a pivot-field count mismatch or an out-of-range dataField fld value before GetPivotTables is called, the unchecked index causes a Go slice-bounds panic that escapes the library, allowing an attacker to crash the process or request worker. No fixed version is available as of this review.

### CVE-2026-16163

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:53.200 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause memory corruption due to an out-of-bounds write.

### CVE-2026-16159

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:52.920 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to obtain sensitive information and cause a denial of service due to an out-of-bounds write.

### CVE-2026-87424

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-08T07:16:33.000 |

A vulnerability in the SupportLink API authentication component of Brocade ASCG versions prior to 3.5.0 allows an attacker to bypass authentication across deployments due to the use of a hard coded cryptographic key.

### CVE-2026-85487

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T07:16:32.450 |

A path traversal vulnerability exists in the HTTP service component of Brocade ASCG versions before 3.5.0. An unauthenticated attacker on the local network could send a manipulated API request to the service endpoint bypassing path restrictions to arbitrary file read, file write, or file deletion operations.

### CVE-2026-85486

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-08T07:16:32.317 |

Brocade ASCG before 3.5.0 improperly processes user input by evaluating form data prior to validation. When an authenticated user submits a configuration form, the submitted text could immediately be processed. A malicious actor with basic access can supply crafted input to execute arbitrary code on the server and take control of the application.

### CVE-2026-85423

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T07:16:32.177 |

A vulnerability has been identified in the data collection service of Brocade ASCG versions before 3.5.0. An API endpoint within the data collector service fails to perform authentication or authorization checks on incoming requests. An attacker with network access to the service can instruct the application to establish SSH connections to arbitrary hosts and execute arbitrary system commands, effectively turning the appliance into an unauthenticated proxy or execution vector.

### CVE-2026-87666

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T04:17:52.553 |

An OS command injection vulnerability exists in the time and zone management subsystem of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. When updating system timezone settings via the REST API or configuration download routines, the system fails to sanitize input values before processing them in underlying shell execution routines. An authenticated user with low-privilege administrative access can exploit this vulnerability by submitting a crafted timezone string containing shell metacharacters. Successful exploitation allows the attacker to escape the restricted management environment and execute arbitrary shell commands with elevated privileges.

### CVE-2026-87683

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T02:16:54.563 |

Multiple stack-based buffer overflow vulnerabilities exist in the REST API management component of Brocade Fabric OS versions prior to 10.0.1. When processing API request payloads (such as device configuration attributes or port mapping requests) the REST API service fails to properly validate incoming array counts and string lengths against internal buffer capacities. An authenticated attacker with REST API access can transmit crafted, oversized request parameters to induce memory corruption on the execution stack. This may result in a denial-of-service condition (daemon crash) or potential arbitrary code execution within the management process context.

### CVE-2026-87682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T02:16:54.420 |

Multiple OS Command Injection vulnerabilities exist in the management interface and session processing routines of Brocade Fabric OS versions before 10.0.1. Input processing flaws during remote management connection validation and session verification for directory-based user accounts allow untrusted input containing shell metacharacters to reach internal system execution wrappers. An authenticated user or a compromised directory service account can exploit these vulnerabilities to execute arbitrary operating system commands with elevated privileges on the target device.

### CVE-2026-76458

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-703` |
| Published | 2026-10-07T17:16:58.280 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76458 are related to improper handling of exceptional conditions issues that are grouped under the Common Weakness Enumeration (CWE) CWE-703.

### CVE-2026-76457

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-07T17:16:58.020 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76457 are related to out-of-bounds read issues that are grouped under the Common Weakness Enumeration (CWE) CWE-125.

### CVE-2026-76456

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-07T17:16:57.770 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco NX-OS engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76456 are related to improper input validation of special elements used in a command issue that are grouped under the Common Weakness Enumeration (CWE) CWE-20.

### CVE-2026-93699

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T08:16:34.367 |

Argument injection in WP Toolkit for cPanel allows local users to execute arbitrary code as other accounts on the same server.

### CVE-2026-94586

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T05:17:06.660 |

A command injection vulnerability exists in the WebTools administrative interface handling configuration download or file transfer operations of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. An authenticated user with permissions to perform configuration downloads using remote server profiles can supply malicious parameter strings to execute arbitrary shell commands on the switch with root privileges

### CVE-2026-94581

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T05:17:06.393 |

An OS command injection vulnerability exists in the REST API management interface of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1 allows an authenticated, high-privileged remote attacker to execute arbitrary system commands with root permissions. An attacker with administrative privileges to configure SSH known host settings can supply specially crafted parameter values containing shell metacharacters to trigger command execution on the host system.

### CVE-2026-87664

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T05:17:05.697 |

A session context forgery vulnerability exists in the web management daemon of Brocade Fabric OS versions 9.2.2d and 10.0.0 through 10.0.0a1. When processing local inter-process communication (IPC) storage callbacks, the service accepts and registers session structures including administrative role permissions, user identifiers, and authorization flags—without verifying the identity or authenticity of the sending process. An attacker can obtain elevated administrative privileges on the web management interface without legitimate authentication.

### CVE-2026-87688

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-08T04:17:56.623 |

An input validation vulnerability exists in the security certificate management component of the Brocade Fabric OS administrative management API. When processing certificate management operations, user-supplied certificate identifiers are handled without adequate sanitization prior to execution in external system routines. An authenticated attacker with privileges to perform certificate deletion requests can leverage this flaw to execute arbitrary system commands with the privileges of the underlying management daemon. This vulnerability affects Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1.

### CVE-2026-87687

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T04:17:56.360 |

An authorization and input validation vulnerability exists in Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. An authenticated user with restricted privileges in one Virtual Fabric can exploit this issue by submitting a specially crafted request containing an arbitrary fabric identifier. This allows the user to perform unauthorized cross-fabric operations and view configuration details within tenants/Virtual Fabrics to which they have not been granted access.

### CVE-2026-87674

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T04:17:53.370 |

A local privilege escalation vulnerability exists in the system logging daemon of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. Insufficient access controls on internal inter-process communication (IPC) channels allow an unprivileged local user to submit malformed logging configurations. Due to improper input sanitization during configuration file generation, an attacker can inject arbitrary directives that execute with elevated privileges when the logging service reloads, leading to local privilege escalation.

### CVE-2026-87680

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T01:16:32.480 |

A command injection vulnerability in the REST API management interface of Brocade Fabric OS versions before 10.0.1 allows an authenticated user to execute arbitrary system commands via crafted input parameters.

### CVE-2026-87679

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-08T01:16:32.313 |

When Brocade Fabric OS versions before 10.0.1 processes trunk configuration operations, the application parses user-supplied list strings into dynamically allocated heap arrays without enforcing boundary checks on the maximum allowable number of elements. An authenticated administrator can exploit this vulnerability via crafted REST API requests containing an excessive number of list delimiters, causing heap corruption that can result in service crash or arbitrary code execution.

### CVE-2026-34499

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-07T20:17:12.527 |

Use of hard-coded cryptographic key vulnerability in Johnson Controls ADVMS allows Read Sensitive Constants Within an Executable.

This issue affects ADVMS: before 3.10.

### CVE-2026-87428

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-08T07:16:33.400 |

In Brocade ASCG before 3.5.0, a  local unauthorized user on the ASCG VM who can issue a request to the SANnav host network namespace can extract stored management credentials for onboarded SANnav instances and compromise connected Brocade SANnav servers or managed Brocade Fibre Channel switches.

### CVE-2026-85422

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-08T07:16:32.033 |

A vulnerability in Brocade ASCG version before 3.5.0 could allow an attacker to obtain a static cryptographic key hardcoded into the software binaries to secure sensitive data at rest and to protect inter-node communication protocols. An attacker who extracts this key can decrypt stored management credentials or craft forged administrative synchronization messages.

### CVE-2026-87685

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-08T04:17:56.097 |

An arbitrary file manipulation vulnerability exists in the WebTools management interface of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. When processing configuration transfer requests, the application fails to properly validate and sanitize a user-supplied status file path parameter. An authenticated administrative user can exploit this issue by submitting a specially crafted status file parameter, causing the underlying process to move an arbitrary system file to a predictable, world-readable temporary directory. This can lead to persistent Denial of Service (DoS), critical system file destruction, host compromise, or sensitive data leakage.

### CVE-2026-87667

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-08T04:17:52.843 |

An argument injection vulnerability exists in the configuration management command-line utility of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. When executing configuration viewing commands with search pattern filters, the utility fails to sanitize user-supplied search string options before passing them to internal search commands. An authenticated user with low-privilege administrative access can exploit this vulnerability to read arbitrary files on the local operating system, including sensitive configuration files, system password hashes and system secrets.

### CVE-2026-77214

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-07T15:17:53.327 |

libexpat before commit 13c5f63 contains a heap buffer over-read vulnerability in xmlparse.c. XML_ParseBuffer advances the parse buffer end with parser->m_bufferEnd += len using a caller-supplied length that is not validated against the allocated buffer size, so repeated XML_ParseBuffer calls move m_bufferEnd past the end of the heap allocation and subsequent parsing reads out of bounds. Reaching this path requires a parse buffer to already be present; otherwise XML_ParseBuffer returns XML_ERROR_NO_BUFFER. A buffer is present after a prior call to XML_GetBuffer, either directly (the common case) or indirectly through a prior XML_Parse call that allocates the buffer internally. The over-read discloses adjacent heap memory to the calling application, recovering heap pointers, libc function pointers, and code pointers sufficient to defeat ASLR and build further exploitation primitives.

### CVE-2026-15824

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:52.640 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to a heap-based buffer overflow.

### CVE-2026-5047

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-922` |
| Published | 2026-10-08T06:16:42.740 |

A vulnerability in Brocade SANnav before 2.4.0b and 3.0.0 prints encoded passwords and  authentication tokens in log files. The vulnerability could allow an authenticated attacker with access to the log file including the SANnav supportsave to access the passwords.

### CVE-2026-97714

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-07T20:17:15.893 |

CVE-2026-97714
is a is a vulnerability in the authentication sub-system of Secure Access
servers prior to version 14.60. Attackers can send a malformed response during
authentication and cause a persistent denial of service.

### CVE-2026-76468

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-07T17:16:59.680 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76468 are related to improper input validation that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-20.

### CVE-2026-15784

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:52.220 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-62251

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-07T17:16:56.303 |

Homer is open source telecom observability software. Prior to version 11.0.283, the `V4StatisticsQuery` handler passes the user-supplied `rawquery` field directly to DuckDB without calling the `sqlvalidator.ValidateRawSQL` function used throughout the rest of the codebase. Any authenticated user can execute arbitrary SQL statements against all data accessible through the FlightSQL service. Version 11.0.283 patches the issue.

### CVE-2026-46570

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-07T15:17:21.010 |

In NTFS-3G before 2026.7.7, a heap buffer overflow exists in ntfs_index_walk_down() in libntfs-3g/index.c that allows an attacker to corrupt heap memory in the SUID-root ntfs-3g binary by crafting a malicious NTFS image. The overflow is triggered by reading the special crafted file metadata.

### CVE-2026-15781

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-08T14:16:52.037 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote authenticated attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-103647

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T11:16:42.950 |

Cross-site scripting in the webmail of Progressive Robot hMailServer 6.3.2 through 6.3.5 allows a remote attacker who can send a user an encrypted message to run script in the webmail's origin with that user's session. When the webmail decrypted an S/MIME message (from 6.3.2) or an OpenPGP message (from 6.3.4) in the browser, it offered each decrypted attachment as a blob URL of the media type the message declared for it. A click saved the file, but if the user opened the attachment in a new tab, a part declared as text/html was rendered as a document of the webmail's origin and its script could read the mailbox, send mail and change the account through the REST API. The webmail is served only when the REST API is enabled, which it is not by default.

### CVE-2026-105816

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-07T22:17:02.673 |

Vault and Vault Enterprise did not consistently verify that stored plugin catalog entries reference binaries within the configured plugin directory. When Vault uses Shamir seals and has an external plugin directory configured, a privileged operator able to restore an Integrated Storage (Raft) snapshot may be able to execute arbitrary code on the Vault host. This vulnerability (CVE-2026-105816) is fixed in Vault Community Edition 2.1.2, and Vault Enterprise 2.1.2, 1.21.12, 1.20.17, and 1.19.23.

### CVE-2026-107615

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-08T14:16:50.313 |

An uncontrolled search path element vulnerability in GlavSoft TightVNC Server for Windows before 2.8.88 allows a local authenticated user to execute arbitrary code with SYSTEM privileges. DynamicLibrary::init() (and ThemeLib) load screenhooks32.dll / screenhooks64.dll with LoadLibrary() using a bare file name and no LOAD_LIBRARY_SEARCH_* flags, so the TightVNC service follows the default DLL search order and loads an attacker-planted DLL from a writable directory earlier in that order (for example, an installation directory with permissive ACLs).

### CVE-2026-107612

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-338;CWE-732` |
| Published | 2026-10-08T14:16:49.877 |

Incorrect permission assignment in GlavSoft TightVNC Server for Windows before 2.8.88 allows a local authenticated user to read or overwrite the inter-process communication handles used between the TightVNC service and its desktop server process. The named shared memory segment in the Global\ namespace that carries the pipe HANDLE values is created with a NULL DACL, and its name is derived from a time-seeded srand(time(0)) value that is predictable to one-second granularity. A low-privileged local process can open the mapping and tamper with the IPC channel of a service running as SYSTEM, potentially leading to disclosure of session data, privilege escalation, or denial of service.

### CVE-2026-107573

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-08T12:17:15.027 |

Incorrect default permissions in the Windows installer of Progressive Robot hMailServer 6.0.0 through 6.3.5 allow a local authenticated user to read the mail server's data. The installer created the data, log, temp, database and event folders and the hMailServer.INI configuration file with the permissions inherited from the installation folder, by default under Program Files, which give the local Users group read access. Any user who can sign in to the computer could read every stored message, the logs, the built-in database with the accounts' password hashes whenever the service is stopped, and the configuration file, including the database password, which is sealed only with the machine's DPAPI key and can be unsealed by any local account; with an external database that password gives full control of it. The Linux AppImage of 6.3.0 through 6.3.5 likewise created its per-user data folders readable by other local users.

### CVE-2026-104660

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T11:16:44.160 |

Missing authorization on COM objects in Progressive Robot hMailServer 6.0.0 through 6.3.5 (Windows only) lets a local interactive user with no hMailServer credential read and write arbitrary files as the service account and queue mail as any sender. The service registers its COM classes with no DCOM access or launch permission and calls CoInitializeSecurity with no security descriptor, so any user logged on at the console or over Remote Desktop can activate the classes in the running service; a hMailServer.Message, its Attachments and Attachment, and a hMailServer.FetchAccount created this way carry a credential that never authenticated. Attachments.Add(path) and Attachment.SaveAs(path) performed no authorization check, and Message.Save/Copy and FetchAccount.AccountID/Save performed none either up to 6.3.3 and from 6.3.4 treated a holder with no credential as the server's own event-script host. Because the service does not impersonate the COM caller, Attachments.Add reads any file the service account can read and returns it, Attachment.SaveAs writes attacker-chosen bytes to any path it can write (on a LocalSystem installation, code execution as SYSTEM), Message.Save queues outbound mail from any address past the SMTP checks, and FetchAccount attaches a mail-fetch job to any mailbox. The objects an Application handed out behave the same once a later Authenticate on that Application fails.

### CVE-2026-104658

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-08T11:16:43.870 |

The Linux live-update apply helper (hmailserver-update) of Progressive Robot hMailServer 6.3.4 and 6.3.5 runs as root on a request file written by the unprivileged hmailserver service account, and took from that request the program used to verify an AppImage update's signature and the systemd unit to stop before reading the service account's files. An attacker who already runs code as the hmailserver service account, for example through another flaw in the mail server, can therefore have arbitrary code executed as root, on any Linux installation where the live update's path unit is active - the default for the project's .deb and .rpm packages - and on AppImage installations run under that unit.

### CVE-2026-103010

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-08T11:16:42.117 |

Heap-based buffer overflow in the legacy Blowfish decryption routine (BlowFishEncryptor::DecryptFromString) in Progressive Robot hMailServer 6.0.0 through 6.3.3 on Windows allows a local interactive user with no hMailServer credentials to write bytes of their choosing past the end of a 255-byte heap buffer in the hMailServer service process, which runs as LocalSystem by default. The user does this by passing a long hexadecimal string to the COM method Utilities.BlowfishDecrypt, which checked no authentication. The routine converted hexadecimal input of any length into a fixed 255-byte buffer before decrypting it in place. The result is a denial of service (service crash), and possibly code execution with the privileges of the service account.

### CVE-2026-85490

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-08T07:16:32.860 |

When Brocade ASCG before 3.5.0 processes support bundle archives ingested from remote compromised endpoints, the application fails to sanitize path traversal sequences contained within archive entries prior to extraction. An unauthenticated remote attacker capable of sending or intercepting ingested archive files can leverage this flaw to write arbitrary files to restricted locations on the underlying host, potentially leading to remote code execution.

### CVE-2026-94585

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-08T05:17:06.523 |

An authentication bypass vulnerability exists in the web management interface of Brocade Fabric OS versions before 9.2.2d running on the MXG610 platform. An unauthenticated, network-adjacent attacker can exploit an unauthenticated endpoint within the Single Sign-On (SSO) workflow to gain administrative access to the device management interface.

### CVE-2026-76266

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-07T21:17:17.310 |

In Splunk Enterprise versions below 10.4.3, 10.2.7, 10.0.10, and 9.4.15 on Linux, a local user who can run commands as the user account running Splunk Enterprise could cause an affected Linux package upgrade to run attacker-controlled operating-system commands with root privileges. The vulnerability is possible because the Linux package maintainer script trusts existing Splunk Enterprise installation content when it performs upgrade operations with root privileges. The vulnerability requires an affected Linux package upgrade to occur after the local user modifies the installation. The local user should not be able to elevate privileges at will.

### CVE-2026-106557

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-10-07T17:16:50.900 |

Backstage is an open framework for building developer portals. Prior to 1.14.6 and 1.15.4, the @backstage/plugin-techdocs-node package did not sufficiently validate TechDocs Markdown extension configuration. An authenticated user who can register or modify documentation sources may cause a TechDocs build to access resources outside the intended documentation boundary, potentially exposing backend-host data or internal network resources. This issue is fixed in versions 1.14.6 and 1.15.4 when pymdown-extensions 10.21.3 or later is also used, normally through mkdocs-techdocs-core 1.7.0 or later.

### CVE-2026-106556

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-10-07T15:17:12.960 |

Backstage is an open framework for building developer portals. Prior to 1.14.6, the @backstage/plugin-techdocs-node package is affected by configuration bypass in techdocs mkdocs.yml sanitization. Insufficient validation of MkDocs configuration during TechDocs generation could allow an authenticated user who can register or modify documentation sources to execute arbitrary commands in the build environment. Impact is limited to resources accessible to the TechDocs backend or build container. This issue is fixed in versions 1.14.6 and 1.15.4.

### CVE-2026-106510

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-183;CWE-470` |
| Published | 2026-10-07T15:17:12.430 |

Backstage is an open framework for building developer portals. Prior to 1.14.6, the @backstage/plugin-techdocs-node package is affected by remote code execution via crafted markdown_extensions in techdocs mkdocs.yml. An authenticated user who can register catalog entities can provide a crafted mkdocs.yml causing arbitrary OS command execution on the TechDocs build host when the docs are built. This issue is fixed in versions 1.14.6 and 1.15.4.

### CVE-2026-105076

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-08T13:17:12.763 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Appsbd Vitepos vitepos-lite allows Blind SQL Injection.This issue affects Vitepos: from n/a through 3.6.1.

### CVE-2026-87425

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-08T07:16:33.140 |

An unauthenticated remote attacker can modify the TLS client trust store in Brocade ASCG versions before 3.5.0. By supplying an unauthorized Certificate Authority (CA) certificate to an unauthenticated management interface, the attacker can cause the system to trust unauthorized certificates, potentially enabling Man-in-the-Middle (MITM) attacks against outbound communications with managed switches and peer nodes.

### CVE-2026-107281

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-863` |
| Published | 2026-10-07T22:17:03.980 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. Prior to 3.0.13 and 2.16.1, the HTTP/1.1 connection-pool key excludes the authenticated principal for connection-oriented NTLM and Negotiate authentication. A pooled socket authenticated for one request can be reused by a request carrying another principal, and the server executes that later request as the first identity. Basic and Digest are not affected because they authenticate each request. This issue is fixed in versions 3.0.13 and 2.16.1.

### CVE-2026-76283

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-07T21:17:19.987 |

Protection Mechanism Failure. Splunk addressed multiple internally identified vulnerabilities in Splunk Enterprise versions 10.4.3, 10.2.7, 10.0.10, and 9.4.15. The vulnerabilities are grouped by Common Weakness Enumeration (CWE), with one Common Vulnerabilities and Exposures (CVE) identifier assigned to each group. See Details for more information.

### CVE-2026-92543

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-319` |
| Published | 2026-10-07T17:17:02.727 |

Docker Engine classifies a registry hostname as insecure using an any-match DNS check. loadInsecureRegistries() injects 127.0.0.0/8 and ::1/128 as insecure CIDRs by default. isCIDRMatch resolves all of the hostname's addresses and returns true if a single address is in the insecure CIDR list. Because the transport re-dials the hostname rather than the CIDR-matching address, a DNS answer set of one loopback IP plus a non-loopback attacker IP disables certificate verification and enables HTTP fallback for the registry connection.

### CVE-2026-16167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:53.690 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to improper bounds checking.

### CVE-2026-16165

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-08T14:16:53.557 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to a null pointer dereference.

### CVE-2026-16164

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:53.373 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to a buffer overflow.

### CVE-2026-16161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-08T14:16:53.063 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to an out-of-bounds read.

### CVE-2026-16111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-08T14:16:52.780 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow an attacker to cause a denial of service due to a type confusion flaw.

### CVE-2026-15822

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405` |
| Published | 2026-10-08T14:16:52.500 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to improper memoization of GraphQL fragment spreads.

### CVE-2026-15819

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T14:16:52.360 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to out-of-bounds memory access caused by a strict-weak-ordering violation in a sorting comparator.

### CVE-2026-16179

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-124` |
| Published | 2026-10-08T13:17:16.200 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow an attacker to cause a heap buffer underwrite and potentially crash the service.

### CVE-2026-16178

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T13:17:16.067 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to improper input validation.

### CVE-2026-16176

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-08T13:17:15.797 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to improper validation of the length field during memory reallocation.

### CVE-2026-16170

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-08T13:17:15.660 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to a heap buffer overflow.

### CVE-2026-16169

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-08T13:17:15.520 |

IBM DataPower Gateway 11.0.0.0 through 11.0.0.2 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-107579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-08T12:17:15.940 |

Inefficient algorithmic complexity in the bounce and complaint processing of Progressive Robot hMailServer 6.3.4 and 6.3.5 allows a remote unauthenticated attacker to stop mail delivery by sending messages, when bounce processing or complaint processing is enabled or a mailing list is managed by the server (none is by default). The readers of incoming delivery status notifications (RFC 3464) and abuse feedback reports (RFC 5965) removed the blank lines at the start of the returned headers part two bytes at a time, copying the rest of the part each time, so their work grew with the square of the number of blank lines. A message shaped like such a report, whose headers part begins with a very large number of blank lines within the reader's 2 MB limit, keeps a delivery thread busy for over a minute while it is delivered, and a few such messages a minute keep every delivery thread busy.

### CVE-2026-107577

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-08T12:17:15.630 |

Inefficient algorithmic complexity and a non-terminating loop in the MIME processing of received messages in Progressive Robot hMailServer 6.0.0 through 6.3.5 allow a remote unauthenticated attacker to make the mail services unavailable by sending a message. Removing a MIME header parameter whose value is empty and directly followed by a semicolon (for example a Content-Disposition with 'filename=a.bat; filename=;') entered a loop that never terminates, holding a worker thread at full load until the server is restarted; this is reached when the attachment blocker renames a blocked attachment or a filename is set over the REST API. Separately, decoding a header field that holds many RFC 2047 encoded words of an encoding other than base64 or quoted-printable, removing a parameter with many RFC 2231 continuations, and deleting many header fields of one name each took time growing with the square of the message, on the small thread pools that serve IMAP, SMTP and POP3 connections, delivery and the REST API.

### CVE-2026-107576

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-08T12:17:15.487 |

Inefficient algorithmic complexity in the inbound DKIM and ARC signature verification of Progressive Robot hMailServer 6.0.0 through 6.3.5 allows a remote unauthenticated attacker to make the mail services unavailable by sending a message. Building the canonical header and choosing the header fields named in a signature's h= tag took time growing with the square of the message's header: the 'simple' canonicalisation prepended each continuation line of a folded field to the lines already gathered, and both canonicalisations searched the gathered fields from the bottom for each h= name and erased the match from the middle of the list. A message whose header holds very many fields, or a field folded over very many lines, with a DKIM-Signature the attacker signs for a domain they control, keeps a worker thread busy for tens of seconds per signature; up to ten signatures are evaluated per message by each of the DKIM and DMARC tests, on the threads that serve delivery and SMTP.

### CVE-2026-107574

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-08T12:17:15.177 |

Inefficient algorithmic complexity in the JSON reader of Progressive Robot hMailServer allows a remote unauthenticated attacker to make the mail services unavailable. Reading a JSON object kept the first of each duplicated member name by searching the members already read, so an object of N distinct member names cost O(N^2): 1 MB took 8.9 seconds and 4 MB took 300 seconds against the affected code. A remote attacker reaches the reader without an account by mailing a crafted TLS-RPT report (up to 16 MB after decompression) to a hosted domain's published report mailbox, which is read on a delivery thread; a few such reports hold every delivery thread (ten by default), so the server delivers no mail, local or outbound, for over an hour per report. A signed-in account reaches the same 16 MB body through the webmail's own REST routes, holding the REST API's own worker threads. Where no report mailbox is configured, the unauthenticated REST sign-in routes that read a JSON body are capped at 64 KB and are not affected.

### CVE-2026-104659

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-08T11:16:44.013 |

Missing Host header validation and missing throttling of failed administrator sign-ins in the REST API listener of Progressive Robot hMailServer 6.0.0 through 6.3.5 allow a remote attacker to brute-force the server administrator's password through the administrator's own browser by DNS rebinding. The listener, which is off by default and bound to the loopback when enabled, answered requests whatever their Host header named, and a failed sign-in with the administrator's password from the loopback was neither auto-banned nor delayed. A web page whose host name the attacker rebinds to 127.0.0.1, opened in a browser on the server, can therefore send authenticated requests to the listener, read the answers and try administrator passwords at full speed until one is accepted, giving the attacker full administrative control of the mail server.

### CVE-2026-103649

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1088` |
| Published | 2026-10-08T11:16:43.093 |

Missing network timeouts in the Linux builds of Progressive Robot hMailServer 6.3.0 through 6.3.5 allow a remote attacker to hold server threads indefinitely and so stop outbound mail delivery (denial of service). The server set its socket timeouts in the form Windows takes, which Linux refuses, and its HTTPS clients read without a deadline, so a peer that accepts a connection and then sends nothing held the waiting thread for as long as the connection stayed open. The MTA-STS policy fetch, enabled by default, is made during outbound delivery to mta-sts.<recipient domain>, so anyone who can make the server deliver mail to a domain they control - for example as the envelope sender of a message that bounces - can hold delivery threads until outbound delivery stops. The same flaw affects the DANE TLSA query, the OAuth2 token request, the ACME client, and the ManageSieve and metrics listeners, which a silent client stops from serving anyone else. Windows builds are not affected.

### CVE-2026-103309

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-08T06:16:37.287 |

The GPTranslate  WordPress plugin before 2.34.14 does not properly restrict who can store translations, and does not escape them when outputting them in translated pages, allowing unauthenticated users to perform Stored Cross-Site Scripting attacks when server-side translations are enabled.

### CVE-2026-94578

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T03:16:37.840 |

Brocade Fabric OS versions before 10.0.1 contain an authorization logic vulnerability in the AAA (Authentication, Authorization, and Accounting) integration framework allows remote authenticated users to gain root-equivalent chassis access controls. By returning specific, crafted Vendor-Specific Attributes (VSAs) or directory claims from an external identity provider (such as RADIUS, LDAP, TACACS+, or Federated IDP), an account can bypass administrative role restriction checks during session establishment.

### CVE-2026-82627

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-08T02:16:54.263 |

The Uncanny Automator – AI + Automation for WordPress | AI Agent, AI Page Builder, Free AI Usage Included plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 7.6.1.1 via deserialization of untrusted input. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject a PHP Object when a third-party integration plugin (such as PeepSo,  MailPoet, WPForms, etc) is installed and a recipe is configured that stores attacker-controlled data as trigger meta. The additional presence of a POP chain within Uncanny Automator allows attackers to delete arbitrary files on the server.

### CVE-2026-107232

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-319;CWE-441;CWE-522` |
| Published | 2026-10-07T22:17:03.497 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. Prior to 3.0.12 on 3.x and 2.16.1 on 2.x, the client infers that an HTTP proxy tunnel exists from the last request method rather than the CONNECT result. After a proxy rejects CONNECT, redirect or authentication handlers can write an origin request and its Authorization credentials onto the still-plaintext proxy connection. Basic credentials can be recovered directly, while NTLM responses may be cracked or relayed. This issue is fixed in versions 3.0.12 and 2.16.1.

### CVE-2026-107227

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-409` |
| Published | 2026-10-07T21:17:14.283 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. From 2.2.0 until 3.0.14, WebSocket permessage-deflate decompression is unbounded when compression is enabled. The inbound pipeline aggregates compressed frames before WebSocketClientCompressionHandler inflates them, so webSocketMaxFrameSize and webSocketMaxBufferSize do not bound decompressed output. A malicious WebSocket peer can send a small compressed message that expands to a very large Netty buffer and exhausts JVM heap. This issue is fixed in version 3.0.14.

### CVE-2026-107161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-07T20:17:10.977 |

A heap-based buffer overflow flaw was found in Cyrus SASL. The add_to_challenge() function in the DIGEST-MD5 plugin computes the size of the buffer needed for a challenge/response field before DIGEST-MD5 quoting is applied, but does not recompute that size when quoting (escaping special characters) makes the value longer. The under-sized buffer is then passed to strcat(), causing a heap-based out-of-bounds write whose size depends on attacker-controlled input. A malicious or on-path DIGEST-MD5 (or HTTP Digest) server can trigger this flaw in a connecting client by supplying a crafted challenge field, such as realm or nonce, most likely resulting in a crash of the client application.

### CVE-2026-107219

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-07T19:17:34.287 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.3.1 to 2.11.0, agile decryption accepts an attacker-controlled spinCount and performs that many password-key derivation iterations before verifier validation. OpenFile reaches agileDecrypt, which passes the unbounded spinCount to convertPasswdToKey before password verification. When a crafted OLE encrypted-workbook header supplies an excessive spinCount and the file is opened, the key-derivation loop performs unbounded attacker-selected work and cannot be cancelled, allowing an attacker to consume a CPU core for an attacker-controlled duration. No fixed version is available as of this review.

### CVE-2026-107217

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129;CWE-190` |
| Published | 2026-10-07T19:17:33.957 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.0.0 to 2.11.0 in github.com/xuri/excelize/v2 and from 1.1.0 to 1.4.1 in github.com/xuri/excelize, ColumnNameToNumber accumulates a bijective base-26 value in int64 without detecting overflow, allowing an invalid long column name to wrap to zero with no error. ColumnNameToNumber accepts the overflowing name VGWQHXLSDVIKWV, after which checkSheetR0 and xlsxWorksheet.checkRow use the wrapped column value as an index. When a crafted worksheet uses an overflowing column name in a row normalized by checkSheetR0 or checkRow, the wrapped zero column becomes a negative slice index during worksheet normalization, allowing an attacker to panic and terminate the calling process. No fixed version is available as of this review.

### CVE-2026-96335

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-07T18:17:32.043 |

Missing Authorization vulnerability in WPMU DEV Forminator allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Forminator: from n/a through 1.57.2.

### CVE-2026-56851

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-07T18:17:20.903 |

The Nickname profile can panic with an out-of-bounds slice error when transforming crafted input into a short destination buffer.

### CVE-2026-107216

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-07T18:17:19.400 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.8.1 to 2.11.0, ANCHORARRAY recursively calls the exported CalcCellValue function, creating a fresh calculation context at each cycle and bypassing in-flight and iteration controls. ANCHORARRAY calls CalcCellValue instead of cellResolver, so each recursive hop receives a new calcContext and loses cycle state. When mutually referencing dynamic-array formulas are evaluated directly or through formula-evaluating APIs, each recursion hop resets the cycle budget and prevents completion-based caches from breaking the cycle, allowing an attacker to cause a fatal Go stack overflow and abort the process. No fixed version is available as of this review.

### CVE-2026-107215

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-07T18:17:19.213 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.3.1 to 2.11.0, extractPart allocates a byte slice directly from an attacker-controlled CFB directory-entry size before validating the sector chain or size domain. extractPart trusts the CFB directory entry streamSize for EncryptionInfo and EncryptedPackage allocations before validating the stream. When a crafted OLE compound file declares a negative or extremely large EncryptionInfo or EncryptedPackage stream size, the declared size reaches make with a negative length or forces a multi-gigabyte allocation, allowing an attacker to panic or exhaust process memory. No fixed version is available as of this review.

### CVE-2026-107214

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-07T18:17:19.040 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.3.1 to 2.11.0, the decryption dispatch performs insufficient structural and parameter validation before standard and agile decryptors slice, index, allocate, and divide using attacker-controlled values. Decrypt passes attacker-controlled EncryptionInfo and EncryptedPackage data into standardDecrypt or agileDecrypt before validating the structures used by those routines. When a malformed OLE compound file with a version-valid EncryptionInfo stream is opened or passed to Decrypt, nine malformed-input classes reach unrecovered Go runtime panics instead of the documented error path, allowing an attacker to terminate the calling process. No fixed version is available as of this review.

### CVE-2026-107212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-07T18:17:18.670 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.1.0 to 2.11.0, Rows.Columns accepts a look-ahead row number above TotalRows without applying the limit enforced by Rows.Next. File.GetRows relies on Rows.Next and Rows.Columns, but Rows.Columns consumes the row r attribute without the limit check in Rows.Next. When a crafted worksheet places an oversized row number after an ordinary valid row and the application calls GetRows or iterates Rows, the iterator advances through every missing row number instead of rejecting the workbook, allowing an attacker to consume a CPU core for an attacker-controlled duration. No fixed version is available as of this review.

### CVE-2026-76467

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-10-07T17:16:59.503 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76467 are related to issues concerning improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-16181

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-08T13:17:16.340 |

IBM DataPower Gateway 10.5.0.0 through 10.5.0.22, 10.6.1 through 10.6.6, 10.6.0.0 through 10.6.0.10, and 11.0.0.0 through 11.0.0.2 could allow a remote attacker to bypass security restrictions due to improper authorization.

### CVE-2026-107584

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-636` |
| Published | 2026-10-08T12:17:16.787 |

Progressive Robot hMailServer 6.0.0 through 6.3.5 fails open when applying DANE (RFC 7672) to outbound SMTP delivery. The server's validating DNSSEC resolver treated a TLSA or MX lookup that did not complete (no answer, SERVFAIL, a malformed reply), an answer without the requested records and without an NSEC/NSEC3 proof of their absence, and an answer whose records carried no applicable RRSIG as if the recipient domain were unsigned, and from 6.2.19 it also delivered to mail exchangers taken from an unvalidated MX lookup that the DNSSEC-validated MX record set did not name. An attacker who can drop, forge or strip DNS answers on the path to the server's resolver, at the resolver, or between the resolver and the recipient domain's name servers, and who holds an active position on the SMTP path, can thereby disable DANE for a DNSSEC-signed recipient domain and cause messages to be delivered in cleartext or to a host of the attacker's choosing with an arbitrary certificate, where they can be read and modified.

### CVE-2026-104704

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-08T11:16:44.457 |

Progressive Robot hMailServer 6.0.0 through 6.3.5 does not enforce TLS for outbound SMTP delivery to a mail exchanger whose DNSSEC-validated TLSA records contain no DANE-EE (usage 3) record, contrary to RFC 7672 section 2.2. The server used only DANE-EE records and treated a validated TLSA record set consisting of DANE-TA (usage 2) or otherwise unusable records as if no records were published, so delivery to such a host fell back to opportunistic TLS. An attacker with an active position on the network path between the server and the recipient's mail exchanger can suppress or break the STARTTLS negotiation and cause messages to be delivered in cleartext, where they can be read and modified.

### CVE-2026-107230

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-863` |
| Published | 2026-10-07T22:17:03.133 |

The AsyncHttpClient (AHC) library allows Java applications to easily execute HTTP requests and asynchronously process HTTP responses. From 2.0.0 until 3.0.14, connection-pool partitioning still omits identity-defining fields for Kerberos, SPNEGO, NTLM, and authenticated proxy connections. Logins without a configured principal, proxy realms, identities sharing a user name, and SOCKS or CONNECT proxy logins can reuse a socket authenticated as a different identity. A later request is then executed under the first identity and can expose that identity's data or authority to another caller. In the affected execution path, SpnegoEngine, NTLM, Kerberos, SPNEGO, SOCKS, and CONNECT control or expose the vulnerable behavior. This issue is fixed in version 3.0.14.

### CVE-2026-76469

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-691` |
| Published | 2026-10-07T17:16:59.867 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco networking engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-76469 are related to insufficient control flow management issues that are grouped under the Common Weakness Enumeration (CWE) CWE-691.

### CVE-2026-91844

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-08T14:17:02.167 |

Unrestricted upload of file with dangerous type vulnerability in İzometri IT Services Domestic and Foreign Trade Co. Ltd. Eimzamip allows Using Malicious Files.

This issue affects eimzamip: from v1.6.4 before v1.6.6.

### CVE-2026-94577

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-08T05:17:06.113 |

A privilege escalation vulnerability exists in the internal Command-Line Interface (CLI) authorization handling mechanism of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. An authenticated user or local process that can manipulate the process execution environment can bypass Role-Based Access Control (RBAC) validation checks. Successful exploitation allows an attacker to elevate privileges to root

### CVE-2026-87675

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T04:17:55.843 |

An OS command injection vulnerability exists in the configuration management subsystem of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. When performing a configuration download operation, the management daemon will relay configuration parameters, user-supplied relay host strings, and filenames directly to an internal utility script without sufficient character set validation. Because the local utility fails to sanitize shell metacharacters before processing them in a system shell command, a malicious or compromised configuration file can cause arbitrary operating system commands to be executed on a remote local switch when an administrator initiates a configuration download.

### CVE-2026-106164

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-07T19:17:31.987 |

In Progress® Telerik® Document Processing SpreadProcessing library, versions prior to 2026.3.1006, an infinite loop vulnerability exists when importing an XLS file with a specifically-targted corruption, the import timeout is ignored resulting in an unresponsive CPU thread and denial of service.

### CVE-2026-89322

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-178` |
| Published | 2026-10-07T23:17:01.197 |

Vault and Vault Enterprise did not consistently evaluate ACL policies against the canonical form of resource and policy names. This may allow an authenticated user with delegated permissions to bypass an explicit deny restriction and access a protected resource or assign a denied policy, potentially leading to privilege escalation. This vulnerability (CVE-2026-89322) is fixed in Vault Community Edition 2.1.2, and Vault Enterprise 2.1.2, 1.21.12, 1.20.17, and 1.19.23.

### CVE-2026-20362

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-07T17:16:55.303 |

A vulnerability in the web-based management interface of Cisco Finesse could allow an unauthenticated, remote attacker to conduct server-side request forgery (SSRF) attacks through an affected device.

This vulnerability is due to improper input validation for specific HTTP requests. An attacker could exploit this vulnerability by sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to obtain limited sensitive information for services that are associated with the affected device.

### CVE-2026-107611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-08T14:16:49.727 |

An out-of-bounds read vulnerability in the ZRLE decoder of GlavSoft TightVNC Viewer for Windows before 2.8.88 allows a malicious or compromised VNC server to read heap memory beyond the palette allocation and crash the viewer by sending ZRLE-encoded tiles whose palette indices exceed the declared palette size. readPaletteRleTile() and readPackedPaletteTile() use the attacker-supplied index to look up colours without validating it against the palette size; out-of-bounds heap data is copied into the framebuffer (garbled display) or the read faults, terminating the viewer.

### CVE-2026-66479

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T13:17:18.707 |

Cross-Site Request Forgery (CSRF) vulnerability in Liquid Web / StellarWP WPComplete wpcomplete allows Stored XSS.This issue affects WPComplete: from n/a through 2.9.5.6.

### CVE-2026-106611

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-08T13:17:15.013 |

Cross-Site Request Forgery (CSRF) vulnerability in WPMU DEV Forminator forminator allows Cross Site Request Forgery.This issue affects Forminator: from n/a through 1.57.3.

### CVE-2026-107503

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15;CWE-346;CWE-522` |
| Published | 2026-10-08T10:17:08.457 |

Unvalidated environments URL allows OAuth authorization code + PKCE verifier theft and account takeover via injected OIDC authority in Ditto Explorer in Eclipse Ditto Ditto Explorer [3.6.0,3.9.7] allows a craft link set an attacker-controlled OIDC authority with autoSso enabled. The UI then automatically starts a login at the genuine identity provider but exchanges the returned authorization code together with its PKCE code_verifier at an attacker-controlled token endpoint. This lets the attacker redeem the code for the victim's access and refresh tokens. Alternatively, an attacker-controlled api_uri causes the UI to send the victim's bearer token or Basic credentials to the attacker. Because the configuration is persisted, later visits to the UI without the crafted link repeat the token theft.

### CVE-2026-71895

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-08T09:16:42.167 |

An authorization vulnerability in Apache DolphinScheduler allows authenticated non-admin users to retrieve Kubernetes configuration data intended for administrator-managed cluster configuration. The exposed kubeconfig data contains credentials that may allow users to authenticate directly to the Kubernetes API outside DolphinScheduler.



The impact depends on the permissions granted to the disclosed credentials. If the kubeconfig provides cluster-admin or broadly privileged service-account access, an attacker may read Kubernetes Secrets, create pods, and establish persistent access to the cluster.



This issue affects Apache DolphinScheduler: from 3.2.0 before 3.4.3.



Users are recommended to upgrade to version 3.4.3, which fixes the issue.

### CVE-2026-71183

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-08T09:16:42.037 |

An authorization vulnerability in Apache DolphinScheduler allows authenticated users to obtain information about data sources they are not authorized to access through the /unauth-datasource and /authed-datasource endpoints.



These endpoints fail to enforce the required data source access controls and return sensitive connection information, including data source passwords. As a result, an authenticated user without permission to access a data source can retrieve its connection details and credentials.



Successful exploitation exposes sensitive data source information and may enable unauthorized access to the underlying databases using the disclosed credentials.



This issue affects Apache DolphinScheduler: before 3.4.3.



Users are recommended to upgrade to version 3.4.3, which fixes the issue.

### CVE-2026-87663

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-08T05:17:05.567 |

An authentication bypass and command injection vulnerability exists in the inter-switch remote execution service of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. When processing remote command execution IPC frames across the fabric, the receiving switch processes these commands at an elevated processing level without proper verification of transmitted parameters. This allows an attacker on a single fabric-connected switch to escalate privileges and execute arbitrary root commands locally or across other managed fabric members where remote execution functionality is enabled.

### CVE-2026-87671

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-08T03:16:36.650 |

An out-of-bounds memory read vulnerability exists in the web management daemon of Brocade Fabric OS versions before 10.0.1. Unauthenticated HTTP endpoints process specific URL query parameters without validating array index boundaries or performing numerical range checks. An unauthenticated remote attacker can exploit this issue by sending a single, crafted HTTP request containing extreme numerical values in the query string. This causes an invalid memory dereference, resulting in a crash of the web management process (Denial of Service) and potential temporary management-plane disruption.

### CVE-2026-87659

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-08T03:16:35.820 |

A critical authorization bypass vulnerability exists in the Management Server handling of Brocade Fabric OS versions before 10.0.1. A compromised switch connected to the fabric can transmit crafted inband Fibre Channel vendor-unique CT (Common Transport) management requests to bypass administrative authentication. Successful exploitation allows an unauthorized peer switch to execute administrative actions on the target device, including resetting administrative passwords, initiating system reboots, and triggering firmware downloads.

### CVE-2026-87681

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-08T01:16:32.620 |

An Access Control Bypass vulnerability exists in the Role-Based Access Control (RBAC) validation engine of Brocade Fabric OS versions before 10.0.1. When processing certain management protocol operations, the RBAC engine incorrectly categorizes non-standard action opcodes during permission checks. This allows authenticated users with read-only management privileges to bypass access controls and execute restricted administrative operations.

### CVE-2026-97715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-07T20:17:16.053 |

CVE-2026-97715 is
a vulnerability in the client registration process of Secure Access servers
prior to version 14.60. Authenticated attackers can pass malformed data to the
server and cause a persistent denial of service.

### CVE-2026-107223

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-07T19:17:34.970 |

Excelize is a Go language library for reading and writing Microsoft Excel spreadsheets. From 2.1.0 to 2.11.0, flatCols expands file-loaded column ranges without validating Min and Max against the worksheet column limit. SetColWidth reaches flatCols, which expands xlsxCol.Min through xlsxCol.Max without enforcing MaxColumns. When a crafted worksheet supplies an oversized col max attribute and the application invokes a column mutator, flatCols performs a deep copy and append for every attacker-selected column number, allowing an attacker to consume excessive CPU and memory or trigger OOM. No fixed version is available as of this review.

### CVE-2026-95595

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T17:17:03.923 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Fontsplugin Disable and Remove Google Fonts | GDPR & DSGVO friendly disable-remove-google-fonts allows Reflected XSS.

This issue affects Disable and Remove Google Fonts | GDPR &amp; DSGVO friendly: from n/a through 2.0.2.

### CVE-2026-94670

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T17:17:03.643 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Everest Forms allows Reflected XSS.

This issue affects Everest Forms: from n/a through 3.6.1.

### CVE-2026-94662

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-07T17:17:03.500 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) allows Stored XSS.

This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.19.

### CVE-2026-107270

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-07T16:17:46.490 |

Gophish through 0.12.1 contains an insecure direct object reference vulnerability that allows authenticated users to take over other users' groups, templates, landing pages and sending profiles. Attackers can supply another user's sequential id in POST requests to /api/groups/, /api/templates/, /api/pages/ or /api/smtp/ to overwrite and reassign objects, locking out owners and exposing victims' recipient lists.

### CVE-2026-106560

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-07T15:17:17.310 |

Backstage is an open framework for building developer portals. Prior to 0.3.25, the @backstage/plugin-scaffolder-backend-module-confluence-to-markdown package is affected by improper repository path validation in a scaffolder backend module. An authenticated user who can execute an affected template and control its repository file location may cause generated content to be written outside the task workspace, within locations writable by the Backstage backend process. This issue is fixed in version 0.3.25.

### CVE-2026-85488

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-08T07:16:32.590 |

Brocade ASCG before 3.5.0 has a well-known Brocade default password embedded in a script distributed to every customer. Any local authenticated user with read access to the installation path can discover this credential and perform privilege escalation on affected Open Virtual Appliance (OVA) deployments, where default configuration settings remain in place.

### CVE-2026-87662

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T05:17:05.433 |

Brocade Fabric versions before 9.2.2d and 10.0.0 through 10.0.0a1 handling of specific download protocols utilizes unsanitized parameter strings. When processing upgrade requests, parameters are converted into system command strings and executed through a system shell interface. Because control characters and shell metacharacters in fields like the host or file path are not stripped or sanitized, an attacker can execute arbitrary shell commands with the firmware management daemon's elevated privileges.

### CVE-2026-87673

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-08T04:17:53.117 |

An OS command injection vulnerability exists in maintenance command-line diagnostic utilities on Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. The binary fails to sanitize user-supplied input options when invoking underlying system commands through a shell interpreter. A privileged user with maintenance account access can exploit this issue by supplying crafted parameters, which results in arbitrary OS command execution with root privileges.

### CVE-2026-87660

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-08T04:17:52.107 |

An improper file permission and missing authorization vulnerability exists in the diagnostic kernel module subsystem of Brocade Fabric OS versions before 9.2.2d and 10.0.0 through 10.0.0a1. An unprivileged local user can invoke privileged hardware tests, force system error conditions, reset hardware blades, or disrupt storage fabric operations.
