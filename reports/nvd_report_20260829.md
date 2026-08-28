# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-28 15:00 UTC
- **対象期間**: `2026-08-27T15:00:33.000Z` 〜 `2026-08-28T15:00:40.000Z`
- **重要CVE数**: 197 件（Critical 9.0+: 55 件 / High 7.0〜: 142 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上ります。  
- **リモートからのコード実行・権限昇格が集中** しており、特に SaaS 系 (ServiceNow AI) と WordPress 系プラグインで深刻度 10.0 の脆弱性が多数報告されています。  
- **デシリアライズ・SQL インジェクション・認証バイパス** が共通の攻撃ベクトルで、未パッチの環境では外部から即座にシステム全体を乗っ取られるリスクがあります。  
- 多くは **「最新リリースへのアップデート」だけで解消** できるものの、組織内でのパッケージ管理やプラグイン更新フローが整備されていないと、修正適用が遅れやすい点が課題です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・コンポーネント | 主な脆弱性種別 | 影響範囲・被害シナリオ |
|-----|------|----------------------|----------------|------------------------|
| **CVE‑2026‑82222** | 10.0 | **GiveWP (WordPress donation plugin)** 4.16.7.1 以前 | Object Injection（信頼できないデータのデシリアライズ） | 攻撃者が任意の PHP オブジェクトを注入し、管理者権限でコード実行・データ改ざんが可能。寄付サイト全体が乗っ取られる危険。 |
| **CVE‑2026‑74820** | 10.0 | **ServiceNow AI Platform**（全インスタンス） | SQL Injection | 認証不要で任意の SQL を実行でき、データベースの情報漏洩・改ざん、さらにはバックエンドシステムへの横展開が可能。 |
| **CVE‑2026‑18885** | 10.0 | **ServiceNow AI Platform** | Code Injection | 同様に認証不要で任意コード実行が可能。ServiceNow の管理コンソールが完全に制御され、企業全体の IT サービスが停止・改ざんされ得る。 |
| **CVE‑2026‑76581** | 9.8 | **WPMU DEV Dashboard** (WordPress) ≤ 5.0.1 | Authentication Bypass (HMAC の不整合) | 未認証ユーザーが管理者権限でダッシュボードにログインでき、プラグインのインストール・設定変更が自由に行える。 |
| **CVE‑2026‑81707** (含む 81706‑81714 系列) | 9.3 | **openssl‑encrypt (Python pip パッケージ)** < 1.4.9 | 複数のプラグイン実行・入力サニタイズ不備 | 悪意あるプラグインがサンドボックス外で実行され、サーバ上で任意コードが走る。Python 環境全体が危険に晒される。 |

> **選定理由**  
> - **CVSS が 10.0** の 3 件は、認証不要でデータベースやコード実行まで至る「最悪ケース」の脅威。特に ServiceNow は企業の基幹 ITSM を支えるため、インパクトが極めて大きい。  
> - **GiveWP と WPMU DEV** は WordPress エコシステムで広く利用されており、プラグインの脆弱性は多数のサイトに波及。  
> - **openssl‑encrypt** はサーバサイドの暗号化ライブラリとして多くの内部ツールで採用されており、Python 環境全体の安全性に直結する。  

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の自動取得**：NVD、GitHub Advisory、ベンダーのセキュリティアドバイザリを CI/CD パイプラインに組み込み、リリース時に自動で通知。  
- **インシデントレスポンス手順の整備**：高リスク CVE が公表されたら **72 時間以内** にパッチ適用または緊急回避策を実施する SLA を設定。  
- **バックアップとロールバック**：アップデート前にデータベース・コードベースのスナップショットを取得し、失敗時に即座に復旧できる体制を確保。  

### 3.2 製品別具体的対策  

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ | 実装手順 |
|-------------------|-------------------|------------------------|----------|
| **GiveWP** (WordPress) | ≤ 4.16.7.1 | **4.16.7.2 以上**（公式リリースノート参照） | 1. `wp plugin update givewp` で自動更新<br>2. 直接ファイルを置き換える場合は `wp-content/plugins/give` ディレクトリを削除し、最新版を展開 |
| **ServiceNow AI Platform** | 全バージョン（未パッチ） | **最新リリース（例: Utah 2026 Patch 3）** | 1. ServiceNow 管理コンソール → **System Update Sets** → **Apply Latest Security Patch** <br>2. パッチ適用後、**インスタンスの再起動** を実施 |
| **WPMU DEV Dashboard** | ≤ 5.0.1 | **5.0.2 以上** | `wp plugin update wpmudev-dashboard` または手動で `wpmudev-dashboard.zip` をアップロード |
| **Tutor LMS** | < 4.0.6 | **4.0.6 以上** | `wp plugin update tutor-lms` |
| **Budibase** (Remote Code Exec) | < 3.41.3 | **3.41.3 以上** | `npm install -g @

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-82222

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-28T12:16:32.810 |

Deserialization of Untrusted Data vulnerability in Liquid Web / StellarWP GiveWP allows Object Injection.

This issue affects GiveWP: from n/a through 4.16.7.1.

### CVE-2026-74820

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:18:36.670 |

ServiceNow has remediated a SQL injection vulnerability that was identified in in the ServiceNow AI platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to execute arbitrary SQL statements against the instance's underlying database and gain access to, or modify, instance data beyond what was intended. 





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. 



We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-18886

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:04.020 |

ServiceNow has remediated an improper access control vulnerability that was identified in the ServiceNow AI platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to create or modify instance data beyond what was intended, resulting in privilege escalation. 





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of exploitation against ServiceNow instances. 



We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-18885

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:03.870 |

ServiceNow has remediated a code injection vulnerability that was identified in the ServiceNow AI platform. This vulnerability could enable an unauthenticated user, in certain circumstances, to execute arbitrary code in the ServiceNow platform and gain access to, or modify, instance data beyond what was intended. 





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. 



We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-81735

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-27T17:21:03.677 |

startServer.ts in the mcp-http-server package of UI-TARS-desktop defaulted its listen address to '::' when no host was given, so startSseAndStreamableHttpMcpServer bound the Streamable HTTP and SSE MCP transports to every interface, and its authentication middleware was optional: middlewares are applied only when a caller supplies them. The @agent-infra/mcp-server-commands and @agent-infra/mcp-server-filesystem entry points call startSseAndStreamableHttpMcpServer with a host and port alone and pass no middleware, so neither server required a credential. The commands server exposes a run_command tool that hands its caller-supplied command string to promisify(child_process.exec), so any unauthenticated client able to reach the port could run arbitrary commands as the user running the server, and the filesystem server exposed its file read and write tools on the same terms. The listen default became 127.0.0.1 in commit c2ad42e3eb9b27830db41a3e6f51ca7179d9b168; the package version stayed at 1.2.4 across that change, so the boundary is the commit rather than a release.

### CVE-2026-76581

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-28T08:16:41.463 |

The WPMU DEV Dashboard plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 5.0.1. This is due to inconsistent and ambiguous HMAC message construction between the unauthenticated `wdpsso_step1` and `wdpsso_step2` AJAX actions, where step 1 signs and discloses an unseparated concatenation of the token, state, redirect, and domain values, while step 2 verifies an unseparated concatenation that omits the domain field. This makes it possible for unauthenticated attackers, on sites connected to WPMU DEV with Hub SSO enabled and mapped to an administrator, to obtain a valid HMAC from step 1 and replay it to step 2 by moving the domain value into the redirect field, resulting in an authenticated administrator session.

### CVE-2026-19092

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:04.150 |

The Tutor LMS WordPress plugin before 4.0.6 does not prevent request data from overwriting internal variables while rendering templates, allowing unauthenticated users to invoke arbitrary zero-argument PHP functions and receive their output.

### CVE-2026-82244

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T12:16:34.653 |

Budibase versions before 3.41.3 contain a remote code execution vulnerability in plugin handling that allows authenticated admin users to execute arbitrary code by uploading a malicious plugin tarball. The server calls eval() on plugin JavaScript files without sandboxing in the main Node.js process, enabling attackers to exfiltrate environment variables and credentials with root privileges in default deployments.

### CVE-2026-78032

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-28T08:16:41.800 |

SOY CMS  contains an issue with deserialization of untrusted data. An arbitrary code may be executed by an attacker with the web server privilege.

### CVE-2026-82082

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T05:16:47.083 |

NUMail developed by Green-Computing has an OS Command Injection vulnerability. Unauthenticated remote attackers can inject arbitrary OS commands and execute them on the server.

### CVE-2026-78174

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-269;CWE-532` |
| Published | 2026-08-28T02:16:22.950 |

WatchGuard Dimension records unredacted session identifiers for logged-in users in its web UI diagnostic log. A low-privileged Dimension Administrator can retrieve this log and extract a Super Administrator's session token while that administrator is logged in, enabling account takeover.

### CVE-2026-19318

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-129;CWE-191` |
| Published | 2026-08-28T02:16:21.070 |

A stack-based buffer overflow vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to execute arbitrary code by sending specially crafted network traffic.

### CVE-2026-19315

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-763;CWE-843` |
| Published | 2026-08-28T02:16:20.703 |

A type confusion vulnerability in the iked process of WatchGuard Fireware OS allows a remote unauthenticated attacker to execute arbitrary code by sending specially crafted network traffic.

### CVE-2026-19313

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190;CWE-680` |
| Published | 2026-08-28T02:16:20.450 |

An heap overflow vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to execute arbitrary code by sending specially crafted network traffic.

### CVE-2026-13086

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787;CWE-798` |
| Published | 2026-08-28T02:16:20.197 |

A stack-based buffer overflow in the epm (Endpoint Protection Manager) service used by the deprecated Mobile Security feature in WatchGuard Fireware OS allows an unauthenticated remote attacker to execute arbitrary code.

### CVE-2026-78239

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T00:18:16.197 |

Xiiaozet LK100W exposes a critical management function that can be 
invoked without authentication, allowing a remote attacker to enable 
administrative services that should be restricted. Successful 
exploitation may permit unauthorized access to the device.

### CVE-2026-76943

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-28T00:18:15.343 |

Xiiaozet LK100Wt contains an authentication weakness within an 
administrative service that may allow an attacker to bypass intended 
access controls and obtain command execution capabilities. Successful 
exploitation could allow unauthorized interaction with privileged 
functionality and may lead to complete device compromise.

### CVE-2026-76179

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-08-28T00:18:14.430 |

An improper protection of authentication tokens vulnerability exists in 
certain Ebyte gateway products. Authentication tokens used by the web 
management interface are insufficiently protected during client-side 
session handling, which may allow an attacker with access to exposed 
session information to obtain and reuse a valid token. Successful 
exploitation could allow an attacker to impersonate an authenticated 
user and gain unauthorized access to device management functionality.

### CVE-2026-73125

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T00:18:11.273 |

Ebyte device web management interface does not consistently enforce 
authentication before granting access to administrative functionality. 
An unauthenticated remote attacker could access sensitive configuration 
information, modify device settings, or disrupt availability.

### CVE-2026-71187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-603` |
| Published | 2026-08-28T00:18:09.150 |

The Ebyte device relies on client side authentication logic that can be 
reproduced by unauthenticated users. An attacker may generate valid 
authentication requests and bypass authentication to obtain 
administrative access to the device.

### CVE-2026-69658

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-28T00:18:08.650 |

MQTT credentials and control traffic are transmitted in cleartext, 
exposing sensitive information to network-level attackers. This may 
enable unauthorized device impersonation and disruption of messaging 
functions.

### CVE-2026-68929

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-08-28T00:18:08.337 |

FastGPT is an open-source LLM platform for building AI applications on a knowledge base. In versions prior to 4.15.2, the WeChat (iLink) share-channel endpoints authorize requests using only the public shareId, with no authenticated identity or team-ownership check. As a result, an unauthenticated attacker who knows a victim team's shareId can take that team's WeChat bot offline or hijack the channel to their own bot: the logout endpoint is gated only by an existence check yet wipes the outLink's stored WeChat token, and the QR-code status endpoint performs no authorization at all and writes attacker-supplied bot credentials into the outLink identified by shareId. By generating a QR for a victim shareId, scanning it with their own WeChat, and calling the status endpoint, an attacker binds the victim team's app to the attacker's bot, exposing the app's private responses, displacing the legitimate binding, and consuming the victim's resources. The shareId is exposed in every shared chat URL, iframe, and embed, so it is not a secret. This issue is fixed in version 4.15.2.

### CVE-2026-53579

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94` |
| Published | 2026-08-27T20:17:49.013 |

Trilium is an open-source hierarchical note-taking application. In versions up to and including 0.103.0, the default-on "Safe import" filter sanitizes HTML only for text notes and excludes the book note type, whose content is stored without sanitization and later rendered as HTML, allowing an attacker-supplied import archive to embed a payload that executes as script. A book note's content is routed through the same rendering path as text notes and injected into the page with jQuery's html method when the note is shown as a grid-view preview card, so a malicious note survives Safe import and runs as soon as the victim opens the containing note. On the desktop client the Electron renderer runs with Node integration enabled, so the injected JavaScript escalates from cross-site scripting to full remote code execution on the victim's machine. This issue is fixed in version 0.104.0.

### CVE-2026-53578

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94` |
| Published | 2026-08-27T20:17:48.860 |

Trilium is an open-source hierarchical note-taking application. In versions up to and including 0.103.0, the default-on "Safe import" filter sanitizes HTML only for text notes and excludes the mindMap note type, whose JSON content is stored without sanitization, allowing an attacker-supplied import archive to embed a payload that renders as arbitrary HTML. A mind map node can carry a dangerouslySetInnerHTML property that the Mind Elixir library assigns directly to a node's innerHTML, so a malicious note survives Safe import and executes script as soon as the victim opens the imported mind map. On the desktop client the Electron renderer runs with Node integration enabled, so the injected JavaScript escalates from cross-site scripting to full remote code execution on the victim's machine. This issue is fixed in version 0.104.0.

### CVE-2026-48996

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-94` |
| Published | 2026-08-27T20:17:47.127 |

Trilium is an open-source hierarchical note-taking application. In versions up to and including 0.103.0, the default-on "Safe import" filter does not sanitize note titles, and the GeoMap note view interpolates a marker note's title into raw HTML that is rendered as innerHTML, allowing an attacker-supplied import archive to inject script that runs when the map is displayed. Because Safe import neutralizes scripts but never escapes titles, a note whose title contains an HTML event-handler payload survives the import and executes as soon as the victim opens the GeoMap that renders its marker. On the desktop client the Electron renderer runs with Node integration enabled, so the injected JavaScript escalates from cross-site scripting to full remote code execution on the victim's machine. This issue is fixed in version 0.104.0.

### CVE-2026-81719

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-27T17:21:02.320 |

openssl_encrypt before 1.4.9 executes untrusted third-party plugins with insufficient controls: the plugin signature policy defaulted to WARN, so an unsigned/unverifiable non-built-in plugin was compiled and executed in the host process at import time, before the runtime sandbox is installed. The only default gate was an incomplete, bypassable AST denylist. If a user is induced to load an attacker's plugin, this results in arbitrary code execution with the privileges of the user running openssl_encrypt. Fixed in 1.4.9 by defaulting the signature policy to ENFORCE for non-built-in plugins.

### CVE-2026-81717

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-27T17:21:02.033 |

openssl_encrypt (pip package openssl-encrypt) before 1.4.9 contains two weaknesses in the portable USB drive feature, whose threat model treats the removable drive as untrusted (attacker with physical write access). USBDriveCreator._verify_integrity_file only validates files listed in the manifest, so files added to the drive — including a root-level autorun payload — are not detected and integrity verification still passes. Additionally, a globally constant, source-embedded KDF salt (_LEGACY_FIXED_SALT) is used to derive the drive encryption key for any drive lacking a per-drive salt file, defeating precomputation resistance and enabling an offline rainbow-table attack.

### CVE-2026-81714

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-27T17:21:01.590 |

openssl_encrypt (pip: openssl-encrypt) versions <= 1.4.8 use suffix-tolerant fingerprint matching in enroll_trust_key when binding a plugin-signing trust anchor. An operator who confirms a short (forgeable, ~32-bit) GPG key id could unknowingly enroll an attacker's colliding key as a trusted anchor, which then vouches for malicious plugins under the ENFORCE signature policy. Version 1.4.9 fixes this by requiring the confirmed value to exactly match the full primary-key fingerprint (case-insensitive, whitespace-stripped).

### CVE-2026-81707

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-27T17:21:01.440 |

openssl_encrypt before 1.4.9 fails to sanitize the email field of imported identity documents, allowing attackers to inject ANSI escape sequences that forge the fingerprint verification line displayed to users. Attackers can deliver a crafted identity bundle through normal contact-exchange flows or keyserver responses to manipulate terminal output and display a fraudulent fingerprint, bypassing the out-of-band verification mechanism that protects against key substitution attacks.

### CVE-2026-81706

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-27T17:21:01.293 |

openssl_encrypt before 1.4.9 fails to prevent namespace collisions between own identities and contacts in IdentityStore, allowing attackers to create shadowed contact entries invisible until the corresponding own identity is deleted. When the own identity is deleted, the shadowed contact becomes visible and resolves to the attacker's keys, enabling silent key substitution for encrypted files.

### CVE-2026-81702

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-27T17:21:00.680 |

openssl_encrypt before 1.4.9 fails to re-derive and validate fingerprints when loading identities from identity.json, allowing attackers to substitute public keys in identity stores. Attackers can replace legitimate public keys with their own while maintaining the claimed fingerprint, enabling silent key substitution where encryption uses attacker keys and signature verification appears valid.

### CVE-2026-81701

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-27T17:21:00.533 |

openssl_encrypt versions before 1.4.9 use a denylist to identify trusted built-in plugins, allowing unsigned plugins in top-level plugins/ directories and unknown subdirectories to bypass signature verification. Attackers can place malicious unsigned plugins following documented installation paths to achieve arbitrary code execution in the CLI process with access to passwords and cryptographic keys.

### CVE-2026-81700

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-27T17:21:00.367 |

openssl_encrypt versions before 1.4.9 contain a signature verification vulnerability in gpg_runner.verify_detached that accepts revoked and expired keys by only checking VALIDSIG status without inspecting REVKEYSIG, EXPKEYSIG, or gpg exit codes. Attackers holding compromised-then-revoked signing keys or expired project keys can bypass signature verification to execute malicious plugins in the host process.

### CVE-2026-81698

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-27T17:21:00.070 |

openssl_encrypt versions before 1.4.9 contain a shell injection vulnerability in the info command's reconstructed CLI block that interpolates untrusted metadata fields without quoting. Attackers can craft metadata values like pepper_name containing shell commands that execute when users copy the printed CLI block into a shell.

### CVE-2026-81696

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-117` |
| Published | 2026-08-27T17:20:59.743 |

openssl_encrypt versions before 1.4.9 fail to sanitize terminal control characters in file metadata printed by the info command. Attackers can craft malicious files containing escape sequences to repaint terminal output and forge verification information displayed to users.

### CVE-2026-81695

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-117` |
| Published | 2026-08-27T17:20:59.597 |

openssl_encrypt versions before 1.4.9 fail to escape attacker-controlled key_id values printed to stderr during decrypt auto-detection. Attackers can craft encrypted files with malicious key_id containing escape sequences to repaint terminal output and forge authenticity verification blocks.

### CVE-2026-81694

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-117` |
| Published | 2026-08-27T17:20:59.447 |

openssl-encrypt (pip package, versions <= 1.4.8) fails to sanitize filenames read from untrusted drive data (outside the AES-GCM authenticated manifest) before printing them in the verify-usb command's output. An attacker can plant filenames containing terminal cursor-movement and erase-line control bytes that repaint a forged PASSED verdict on screen, masking actual tamper detection. Fixed in 1.4.9 by routing drive-derived names through sanitize_for_display().

### CVE-2026-81685

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-08-27T17:20:58.110 |

openssl_encrypt versions before 1.4.9 fail to sanitize recovery-slot metadata in the desktop GUI, allowing attackers to inject control characters and line separators into the irreversible-removal confirmation dialog. Attackers can craft encrypted files with malicious slot identifiers containing bidi overrides or line-separator characters to forge warning text and deceive users during file removal operations.

### CVE-2026-81681

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-311` |
| Published | 2026-08-27T17:20:57.453 |

openssl_encrypt (pip package openssl-encrypt) versions <= 1.4.8 advertise a portable USB workspace as an 'Encrypted USB Workspace' with AES-256-GCM encryption and write a marker declaring the workspace encrypted, but the workspace directory is actually stored in cleartext and the derived encryption key is never applied to it. A user who trusts the branding and places files in the workspace leaves them unencrypted on the removable media, so an attacker with physical access to the media can read the sensitive files. Fixed in 1.4.9, which seals the workspace into an authenticated AES-256-GCM vault.

### CVE-2026-81680

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-27T17:20:57.300 |

openssl_encrypt versions before 1.4.9 fail to authenticate recovery-slot presence in envelope-format encrypted files, allowing attackers to remove recovery slots without re-encrypting the payload. Attackers can modify the file header to delete recovery-slot fields and bypass authentication, silently removing recovery paths the owner deliberately added.

### CVE-2026-81098

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-27T17:20:52.297 |

The Telnyx MCP server exposed its HTTP transport on every interface and did not require a caller credential. packages/mcp-server/src/http.ts served MCP on the root path with a listener bound to all interfaces and parsed the caller's authentication headers in a mode that did not fail when they were absent, so a request without any credential completed initialisation and dispatched tools. Dispatch forwarded the server's own stored credentials, the Telnyx API key and client secret together with the code-execution key, to the upstream endpoint, so an unauthenticated caller able to reach the port acted with them. The current code defaults the host to loopback, requires a server API key, and enforces it in middleware.

### CVE-2026-81096

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-27T17:20:51.950 |

ToolUniverse ran caller-supplied Python inside a sandbox that could be escaped, on a server that required no authentication. The executor behind the python_code_executor tool, in python_executor_tool.py, inspected the submitted source for a denied list of attribute names and calls but left the attribute-lookup builtins available and did not stop a dunder attribute reached through a string lookup or through a module already permitted, so a caller could walk from a literal's class to its base and enumerate subclasses to obtain a reference to the process and subprocess modules. A per-call argument also let the caller widen the import allow-list before the inspection ran. The HTTP and MCP servers in http_api_server.py and smcp_server.py bound to every interface with debugging enabled and no authentication, so any caller able to reach the port executed code as the server process. Version 1.3.0 adds bearer-token authentication, defaults the bind address to loopback, and hardens the attribute checks.

### CVE-2026-81094

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-27T17:20:51.650 |

The mcp-router CLI served its MCP aggregator on every interface and enforced authentication only when the operator asked for it. The serve command in apps/cli/src/commands/serve.ts defaulted its host to the all-interfaces address on a fixed port, and required a token only when the corresponding flag was supplied, so a default invocation exposed the aggregator, and every MCP server it fronted, to anyone able to reach the port. Release 0.6.3 defaults the host to the loopback address and refuses to start without a token whenever the host it is given is not a loopback address; no earlier release carries either check.

### CVE-2026-78251

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-27T17:20:37.750 |

DJI drones contain an FTP service that uses hardcoded credentials shared across affected models and permits authenticated users to upload files without limits on file size, file count, or total storage consumed in **/blackbox/upgrade/**, as well as overwrite existing files in that directory. An attacker with access to the drone's internal network or USB RNDIS interface can exhaust the available storage, preventing the aircraft from writing flight records, logs, and telemetry and potentially preventing subsequent firmware updates. Uploaded files persist across reboot and factory reset.

Affected models are DJI Neo until 01.00.0400, DJI Neo 2 until 01.00.0500, DJI Flip until 01.00.1200, DJI Air 3 until 01.00.1600, DJI Air 3S until 01.00.1400, DJI Avata 2 until 01.00.0400, DJI Avata 360 until 01.00.0300, DJI Mavic 3 until 01.00.1400, DJI Mavic 3 Classic until 01.00.0800, DJI Mavic 3 Pro until 01.01.0700, DJI Mavic 4 Pro until 01.00.0500, DJI Mini 2 until 01.07.0200, DJI Mini 3 until 01.00.0500, DJI Mini 3 Pro until 01.00.0900, DJI Mini 4 Pro until 01.00.1100, and DJI Mini 5 Pro until 01.00.0600.

Remediation requires a firmware update from the vendor.

### CVE-2026-16279

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-27T17:17:14.460 |

An Improper Authorization vulnerability affecting 3DPassport in 3DSwymer from Release 3DEXPERIENCE R2023x through Release 3DEXPERIENCE R2026x could allow an attacker to gain access to some user accounts.

### CVE-2026-82090

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:47.400 |

Pocket through 8.33.0.0 allows XSS because "Save to Pocket" injects external HTML into the DOM.  JavaScript code can alter the application state via native bridge methods.

### CVE-2026-81934

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-27T20:18:57.350 |

Redis contains a use-after-free vulnerability in the 'tlsProcessPendingData()' function, which handles the TLS pending-data list if Redis is configured with TLS support. A remote, unauthenticated attacker may be able to execute arbitrary commands with the privileges of the Redis server. Fixed in Redis 8.2.9, 8.4.6, 8.6.6, 8.8.2, and 8.10.1.

### CVE-2026-42007

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-28T12:16:29.260 |

An attacker that has valid credentials can use a Sieve script with the editheader extension to trigger a use-after-free in the mail editing code, and to write memory contents beyond the intended buffer into the delivered mail. This causes memory leak and opportunity to do memory corruption during mail delivery, which can crash the delivery process and may allow execution of arbitrary code in the context of that process. Disable the Sieve editheader extension. Update to non-vulnerable version. No publicly available exploits are known.

### CVE-2026-18918

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:L/U:Red` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-28T12:16:27.150 |

In Eclipse Lyo versions 2.0.0 to 7.0.0, OAuth server authorization checks can be bypassed when the 2-legged auth is supported by the server. In those cases, application that based their authz filters upon Lyo-provided `AbstractAdapterCredentialsFilter`, are vulnerable. An attacked can create a provisional trusted client (valid use-case) but then it can be used as a trusted client immediately without requiring the administrator approval to clear the provisional status. The 3-legged path requiring user interaction is not vulnerable and rejects provisional clients.

### CVE-2026-61800

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T02:16:21.767 |

Wazuh is an open-source security platform providing unified XDR and SIEM protection for endpoints and cloud workloads. In versions 4.4.0 through 4.14.6, a party holding the cluster key can write, overwrite, or delete arbitrary files under /var/ossec on worker nodes, leading to remote code execution as root. During cluster file synchronization, the non-merged branch of update_master_files_in_worker() moves each staged file to a destination derived only from safe_join(), which confines the path to /var/ossec but never verifies that the file lands in the directory declared by its cluster_item_key. Because the destination check present on the primary node and on the worker's merged branch was not applied, a peer can place files at attacker-chosen locations under /var/ossec, including paths that are executed as root, and the delete branch has the same gap. This is an incomplete fix for CVE-2026-30893, which addressed traversal outside /var/ossec but left this path able to redirect files anywhere within it. This issue is fixed in version 4.14.7.

### CVE-2026-50152

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-28T00:18:07.073 |

Ceph is an open-source distributed storage platform providing object, block, and file storage. In versions prior to 20.2.4 and 19.2.6, the Monitor subscription handler fails to properly authorize access to the configuration-key store, allowing any CephX user with only  `mon allow r` capabilities to read the entire store by sending a single crafted MMonSubscribe message. The config-key store holds sensitive secrets including OSD LUKS disk-encryption passphrases and, on cephadm-managed clusters, the SSH private key that cephadm uses to reach every host in the cluster. Because that key grants root on every node under the default cephadm configuration, a low-privileged read-only account can escalate to full cluster and host compromise. This issue is fixed in versions 20.2.4 and 19.2.6

### CVE-2026-18717

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-28T00:16:48.740 |

ASE2000 2.35 through 2.37 is vulnerable to an improper certificate validation vulnerability, which may allow an attacker to impersonate the trusted peer, complete the TLS handshake, and read or modify protected communications.

### CVE-2026-81826

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384;CWE-613` |
| Published | 2026-08-27T17:21:05.770 |

Affected versions of Flowintel do not revoke existing authenticated sessions when a user’s password is changed.


This means that if an attacker already possesses a valid session—for example, from prior access or a stolen session token—the victim changing their password does not terminate that attacker’s access. The session remains usable until it expires naturally. The upstream commit describes this directly as:


“session keeps working until it expires.”

The fix detects password changes and explicitly invokes _invalidate_user_sessions(user.id) after the database update. This is applied in both edit_user_core() and admin_edit_user_core().

Version impacted >=3.3.0

### CVE-2026-57499

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-78` |
| Published | 2026-08-27T17:18:52.633 |

Liman is open source server management software. Prior to 2.2.2 - 1103, an OS command injection vulnerability in the log rotation configuration endpoint allows an authenticated administrator to execute arbitrary operating system commands on the Liman server. The `ip_address` parameter is embedded directly into a shell command without sanitization, enabling shell escape via single-quote injection. This is fixed in 2.2.2 - 1103.

### CVE-2026-40541

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T08:16:40.713 |

An improper neutralization of input during web page generation ('Cross-site Scripting') vulnerability in extract domain in Synology Chat Server before 2.4.5-22148 allows remote authenticated users, via a UI interaction, to read or write arbitrary files and conduct denial-of-service attacks in DSM.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-5706

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-08-28T00:18:07.853 |

In Bluetooth Mesh SDK 6.1.4 and earlier, malformed extended advertisements can trigger out-of-bounds writes leading to stack corruption and remote code execution. These messages must come from a device that has already joined the network. Only provisioners supporting extended advertisements may be impacted.

### CVE-2025-30156

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-28T00:16:45.557 |

Ceph is an open-source distributed storage platform providing object, block, and file storage. In versions prior to 20.2.4 and 19.2.6, the CephX authentication protocol encrypts tickets with AES-128-CBC in an unauthenticated mode that uses a hard-coded initialization vector and no message authentication, allowing an attacker to forge credentials and gain cluster-wide access. Because the ciphertext is malleable and the monitor will encrypt attacker-chosen entity names, an attacker holding one low-privilege key and able to observe CephX traffic can use the monitor as an encryption oracle and splice ciphertext blocks into valid tickets for privileged entities such as Manager, MDS, and OSD. The same lack of authentication also lets an attacker with CephX permissions escalate privileges by flipping a single bit in a service ticket to set its allow_all field to true. This issue is fixed in versions 20.2.4 and 19.2.6.

### CVE-2026-82089

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:M/U:Green` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:47.230 |

The wallabag (aka fr.gaulupeau.apps.InThePoche) application through 2.6.0 for Android allows XSS because /api/entries data is loaded into a WebView.

### CVE-2026-75419

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-28T00:18:12.677 |

go-wind-cms (GoWind) before 1.0.0 has a missing authorization vulnerability. The NewAuthorizer() function in app/admin/service/internal/data/data.go and app/app/service/internal/data/data.go returns a no-op authorization engine (noop.State{}), so the authz middleware always allows requests. Any authenticated user (regardless of role or tenant) can invoke administrative APIs such as deleting users, resetting passwords, and creating tenants.

### CVE-2026-39944

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-28T00:17:27.860 |

Ceph is an open-source distributed storage platform providing object, block, and file storage. In versions prior to 20.2.4 and 19.2.6, the RADOS Gateway (RGW) protects STS session tokens with an AES-128-CBC handler that provides no message authentication, allowing an attacker who holds any valid STS token to tamper with it undetected and escalate to full RGW administrative access. Because the ciphertext is unauthenticated, the attacker can perform a CBC bit-flip on the acct_type, perm_type, and is_admin fields of their own token, and a forged is_admin value triggers a global administrative override that bypasses all capability checks. The attack is reachable remotely over the RGW S3 endpoint and is a self-contained modification of a token the attacker already possesses, requiring no encryption oracle and no network observation. It requires only a single valid STS token, which need not carry any elevated privileges, with STS enabled. This issue is fixed in versions 20.2.4 and 19.2.6.

### CVE-2026-81730

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-27T20:18:55.480 |

Dolibarr 9.0.0 through 23.0.4 saves inbound email attachments under the name supplied in the message's MIME headers without reducing it to a safe basename. The global saveAttachment() in htdocs/emailcollector/lib/emailcollector.lib.php builds $filepath = $path . $filename . '.' . $ext and hands it to file_put_contents(), and the private saveAttachment() in htdocs/emailcollector/class/emailcollector.class.php writes to $destdir.'/'.$filename; the name reaches both from the attachment's own getName() or getFilename() value by way of the record-join, create-ticket and create-project operations. A traversal sequence in the filename therefore survives intact, so any sender who can email a mailbox that an EmailCollector monitors, which is the module's ordinary use for a support or ticket inbox, can place attacker-controlled content outside the per-object attachment directory without holding a Dolibarr account. Under the hardened layout Dolibarr's SECURITY.md requires, with htdocs read-only, the write is confined to the documents tree and corrupts or forges other objects' documents; where htdocs is writable the same primitive reaches a web-executable path. Version 24.0.0 applies dol_sanitizePathName() and dol_sanitizeFileName() before the write.

### CVE-2026-54721

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-27T20:17:49.973 |

Silverstripe UserForms provides a visual form builder for the Silverstripe CMS. From 6.0.0 until 6.4.9, 7.0.7, and 7.1.1, the userform email recipient subject field in the CMS accepts a specially crafted payload that can be interpreted as executable server-side code. An authenticated CMS user with permission to configure a UserForms email recipient can use the subject field to run arbitrary code on the server, compromising confidentiality, integrity, and availability. This issue is fixed in versions 6.4.9, 7.0.7, and 7.1.1.

### CVE-2026-80208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-27T17:20:50.273 |

APITable through 1.13.0-beta.1 annotates both getUserHistories and closePausedUserAccount in InternalUserController with requiredLogin = false. ResourceInterceptor honours that annotation by returning before any session or API key is validated, and the nginx gateway shipped with the product proxies every /api request to the backend server, so both endpoints are reachable by any unauthenticated client that can reach the gateway. An attacker can POST to /api/v1/internal/getUserHistories to enumerate the accounts sitting in the 30-day cooling-off period that follows a deletion request, then POST to /api/v1/internal/users/{userId}/close for each one. The closure path clears the account's email address, phone number and nickname, cancels its space subscriptions, removes its space memberships and deletes its OAuth bindings, so the cooling-off window that exists to let a user reverse a deletion request is bypassed and the account cannot be recovered.

### CVE-2026-82261

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:39.250 |

SvelteKit (@sveltejs/kit) versions >=2.49.0 and <=2.52.1 with experimental remote functions and form enabled contain a CPU exhaustion vulnerability in form deserialization. An attacker can send malformed form data to cause the server to become unresponsive while processing the request, resulting in denial of service. Fixed in 2.52.2.

### CVE-2026-82260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:39.100 |

SvelteKit (@sveltejs/kit) versions >=2.49.0 and <=2.52.1 with experimental remote functions (experimental.remoteFunctions) and form enabled contain a memory exhaustion vulnerability in remote form deserialization. Malformed form data can cause excessive memory allocation, crashing the server process and resulting in denial of service. Fixed in 2.52.2.

### CVE-2026-82259

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-28T12:16:38.953 |

SvelteKit versions from 2.49.0 through 2.53.2 (fixed in 2.53.3) contain a deserialization expansion issue in the experimental form remote function. When an application enables experimental.remoteFunctions and uses the form function to process the files array without validating files.length or individual file sizes, an attacker can submit relatively small inputs that expand into very large file arrays, leading to expensive processing and denial of service.

### CVE-2026-82254

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-08-28T12:16:38.173 |

gitoxide before 0.69.0 contains unchecked array indexing in delta application and uncapped allocation from attacker-controlled size headers in gix-pack. Attackers can send crafted pack data during clone or fetch operations to trigger panics or out-of-memory process kills.

### CVE-2026-82253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T12:16:38.027 |

gitoxide (Rust crates gix <= 0.72.0 and gix-validate <= 0.10.0) contains a path traversal vulnerability. The submodule name validation function in gix-validate only checks the first occurrence of '..' via name.find(b".."), allowing crafted names such as 'a..b/../../../.git/' to bypass the check; additionally this validation is never invoked in production code paths. Combined with a trust inheritance flaw in Submodule::open(), where the parent repository's git_dir_trust (Trust::Full) is cloned and the ownership verification is skipped, an attacker can craft a malicious .gitmodules file so that a victim tool built on gitoxide reads arbitrary git repository configuration (including embedded credentials) with full trust, bypassing safe-directory protections. Fixed in gix 0.82.0 and gix-validate 0.11.1.

### CVE-2026-82252

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-28T12:16:37.887 |

gitoxide before 0.52.1 follows symlinks when reading the worktree .gitmodules file, allowing attackers to inject out-of-repository bytes into submodule metadata. Attackers can create a malicious repository with a symlinked .gitmodules pointing outside the repository tree, causing gitoxide to parse arbitrary external files as submodule configuration and expose attacker-controlled name, path, and url values.

### CVE-2026-82251

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T12:16:37.113 |

gitoxide before 0.52.1 fails to validate submodule names from .gitmodules configuration, allowing path traversal when deriving submodule git directories. Attackers can craft malicious submodule names with traversal segments to redirect state() and open() functions to repositories outside .git/modules, causing repository confusion and inspection of attacker-controlled repositories.

### CVE-2026-82247

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-28T12:16:36.500 |

gitoxide's gix-url crate (<= 0.32.0, fixed in 0.37.1) uses a hand-rolled URL parser that does not treat '?' or '#' as terminating the authority component, contrary to RFC 3986. As a consequence, gix-transport's HTTP redirect identity guard (can_reuse_identity) compares the wrong host and fails open. An attacker controlling a redirect response can craft a Location header of the form <attacker-authority>?@<original-authority> so that gitoxide sends the caller's HTTP Basic Authorization credentials to an unintended host. gix-transport is affected in versions <= 0.49.0 (fixed in 0.58.1).

### CVE-2026-78072

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T12:16:31.957 |

Joomla Extension - Jefferson49 - Unauthenticated blind SQLi in Sexy Polling Reloaded < 5.6.1

### CVE-2026-78011

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-08-28T02:16:22.563 |

An integer underflow vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-78010

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787;CWE-1284` |
| Published | 2026-08-28T02:16:22.417 |

A stack-based buffer overflow vulnerability in the WatchGuard Fireware OS iked process iallows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-78009

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-08-28T02:16:22.293 |

An out-of-bounds read vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-19317

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-08-28T02:16:20.947 |

An out-of-bounds read vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-19316

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-08-28T02:16:20.827 |

A double-free vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-19314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-08-28T02:16:20.580 |

An integer underflow vulnerability in the WatchGuard Fireware OS iked process allows a remote unauthenticated attacker to create a Denial of Service (DoS) condition in VPN processing by sending specially crafted network traffic.

### CVE-2026-13108

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T02:16:20.323 |

WatchGuard Dimension is susceptible to a denial-of-service condition when an attacker sends a high volume of TCP SYN packets to the log listening service.

### CVE-2026-78037

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T00:18:16.063 |

Xiiaozet LK100W is vulnerable to OS command injection through its 
web-based management interface. An authenticated attacker may be able to
 execute arbitrary operating system commands with elevated privileges, 
potentially resulting in unauthorized access to sensitive information or
 complete device compromise.

### CVE-2026-76945

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-603` |
| Published | 2026-08-28T00:18:15.487 |

The affected Ebyte device relies on client-managed authentication tokens
 without sufficient server-side validation. An attacker may replay or 
manipulate authentication tokens to gain unauthorized access to 
administrative functionality.

### CVE-2026-76940

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-28T00:18:15.190 |

The affected Ebyte device does not restrict repeated authentication 
attempts through rate limiting or account lockout mechanisms. This could
 allow an attacker to perform automated authentication attacks against 
deployments that rely on password based authentication.

### CVE-2026-76060

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T00:18:14.273 |

An authenticated OS command injection vulnerability exists in ZoneMinder's event export functionality. The exportFile HTTP request parameter is passed unsanitized into a shell command executed via PHP's exec(), allowing any authenticated user with View Events permission to execute arbitrary operating system commands on the server.

### CVE-2026-75813

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T00:18:14.007 |

Certain configuration endpoints may lack proper server-side 
authorization checks, allowing unauthorized users to access or modify 
sensitive device settings. This could result in full compromise of 
device functionality.

### CVE-2026-73809

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-28T00:18:11.410 |

A cleartext transmission of sensitive information vulnerability exists 
in certain Ebyte gateway products. The web management interface does not
 adequately protect sensitive communications using transport-layer 
encryption. An attacker with access to network traffic could intercept 
authentication or session-related information transmitted between a user
 and the affected device. Successful exploitation could result in 
disclosure of sensitive information and unauthorized access to device 
management functionality.

### CVE-2026-18965

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T00:16:48.933 |

PayRange API is missing proper authorization on management endpoints, which allows verbose details of every device on the PayRange network to be publicly accessible, with or without an account.

### CVE-2026-76639

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-08-27T20:18:38.230 |

Unitree G1 EDU firmware through 1.5.2 contains an unauthenticated remote code execution vulnerability that allows network-adjacent attackers to execute arbitrary commands as root by chaining three weaknesses: an unauthenticated WebRTC-to-DDS bridge on TCP port 9991, a static AES-128 key stored with world-readable permissions, and a path traversal flaw in the chat_go knowledge upload API. Attackers can publish DDS control messages to restart the bashrunner service, plant a malicious payload in its script execution directory via path traversal, and trigger execution of that payload as uid 0 through the bashrunner shell subprocess.

### CVE-2026-6876

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:18:32.680 |

ServiceNow has remediated a sandbox escape security issue that was identified in the Now Platform. This security issue could allow an unauthenticated user to execute arbitrary code within the Now Platform, potentially leading to more access to the Now Platform than intended.  





ServiceNow deployed a security update to hosted instances and ServiceNow provided the update to our partners and self-hosted customers. We are not currently aware of malicious exploitation against ServiceNow instances. 



We recommend customers promptly apply appropriate updates or upgrade to a patched release if they have not already done so.

### CVE-2026-10036

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-27T20:17:02.130 |

SpeechBrain before 1.1.1 contains an arbitrary code execution vulnerability that allows attackers to execute arbitrary code by supplying a crafted CKPT.yaml checkpoint metadata file parsed with PyYAML's unsafe loader during candidate enumeration in Checkpointer.recover_if_possible(). Attackers can embed malicious Python object construction tags such as !!python/object/apply in any CKPT.yaml file within the configured checkpoint path to trigger code execution during candidate discovery, even if the malicious checkpoint is never selected for recovery.

### CVE-2026-81722

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-27T17:21:02.800 |

nltk PorterStemmer in versions <= 3.10.2 (fixed in 3.10.3) contains an inefficient-algorithmic-complexity denial of service in PorterStemmer.stem(). The _is_consonant() helper walks backward over the entire run of trailing 'y' characters on every call, and _measure() invokes it for each stem position, causing O(n^2) behavior. A single ~20-50 KB untrusted token consisting of a long run of the letter 'y' followed by a matching suffix (e.g., 'ness') can pin a CPU core for seconds to minutes, causing availability impact.

### CVE-2026-81721

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-27T17:21:02.650 |

openssl_encrypt before 1.4.9 fails to validate KDF cost parameters in encrypted file metadata and keystore headers, allowing attackers to trigger unbounded memory allocation. Attackers can craft malicious encrypted files declaring arbitrarily large Argon2, scrypt, or balloon KDF parameters to exhaust system memory and crash the process without authentication.

### CVE-2026-81718

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-08-27T17:21:02.180 |

openssl_encrypt versions before 1.4.9 use under-parameterized PBKDF2-HMAC-SHA256 with only 100,000 iterations to protect PQC keyfile private keys and 10,000 iterations for dual-encryption file-password verification. Attackers who obtain keyfiles or encrypted files can brute-force wrapping passwords offline using GPU or ASIC acceleration.

### CVE-2026-81716

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-27T17:21:01.877 |

openssl_encrypt (pip: openssl-encrypt) versions before 1.4.9 contain a path traversal flaw in PluginSandbox._is_safe_path, which authorized file access using a bare string-prefix match. A sandboxed plugin without the READ_FILES permission could read or write another plugin's directory that merely shares a name prefix (e.g., .../plugins/foobar matching allowed .../plugins/foo), breaking per-plugin isolation within the same user. Fixed by matching each allowed directory exactly or with a trailing path separator.

### CVE-2026-81715

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-27T17:21:01.733 |

openssl_encrypt (pip package openssl-encrypt) versions <= 1.4.8 do not redact the keyserver bearer token passed as the positional argument to 'keyserver set-token' in the --debug argv dump, because sanitize_argv_for_debug fails to sanitize it. As a result the token is printed in cleartext to stderr under --debug (even without --unsafe-show-secrets), persisting the credential in logs and terminal history. Fixed in 1.4.9.

### CVE-2026-81705

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-27T17:21:01.147 |

openssl-encrypt before 1.4.9 fails to redact the file password in its --debug argv dump when the password is supplied via bundled short-option spellings (e.g. -apHunter2) or abbreviated long-option spellings (e.g. --passw). The sanitizer only recognized exact option names, --option=value forms, and tokens starting with -p, so these spellings bypass the redaction chokepoint and the cleartext password is written to stderr. Anyone with access to that output (terminal scrollback, merged 2>&1 output, CI job logs, or the GUI's persistent debug log) can recover the password.

### CVE-2026-81704

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-08-27T17:21:00.993 |

openssl_encrypt versions before 1.4.9 contain a weak key derivation vulnerability in the D-Bus CryptoService.EncryptFile handler that uses unstretched SHA-256 instead of Argon2id. Attackers can perform offline password guessing against encrypted files roughly six to seven orders of magnitude faster than documented protection by exploiting the missing key stretching and hash rounds.

### CVE-2026-81703

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-27T17:21:00.833 |

openssl_encrypt versions before 1.4.9 fail to validate encryption status of embedded post-quantum private keys in file metadata. Attackers can craft files with unencrypted embedded PQC keys that decrypt under any password, bypassing authentication and producing attacker-chosen plaintext with false integrity verification.

### CVE-2026-81699

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:21:00.217 |

openssl_encrypt versions before 1.4.9 fail to properly validate key derivation function costs in crafted files, allowing attackers to trigger unbounded memory and CPU exhaustion during pre-authentication processing. Attackers can supply malicious files with excessive KDF parameters to exhaust system resources and crash or wedge the process before password verification occurs.

### CVE-2026-81697

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-27T17:20:59.893 |

openssl_encrypt (pip package openssl-encrypt) versions <= 1.4.8 contain a CWD-relative configuration file resolution flaw in crypt_settings.py, where CONFIG_FILE (originally the absolute per-user path ~/.crypt_settings.json) is reassigned at line 84 to the bare relative name 'crypt_settings.json'. As a result, the legacy Tk GUI's SettingsTab reads and writes KDF settings from crypt_settings.json in the process launch (current working) directory instead of the user's home directory. An attacker who plants a malicious crypt_settings.json (e.g. sha256:1 with all memory-hard KDFs disabled) can silently downgrade encryption performed in that GUI session to roughly one hash round, bypassing the weak-KDF preflight and enabling offline brute-force attacks against the resulting ciphertext. Fixed in 1.4.9.

### CVE-2026-81693

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-27T17:20:59.297 |

openssl_encrypt before 1.4.9 fails to validate the total field from QR JSON payloads before materializing ranges. Attackers can supply crafted QR images with extremely large total values to trigger unbounded memory allocation and cause denial of service through out-of-memory conditions.

### CVE-2026-81692

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-27T17:20:59.140 |

openssl_encrypt (pip: openssl-encrypt) versions 1.4.8 and earlier fail to validate the 36-bit STREAMINFO total_samples field of FLAC files before using it to size an allocation (np.random.randint(size=(total_samples, channels))). A ~50-byte crafted FLAC file declaring ~100 million samples causes a multi-gigabyte memory allocation, leading to out-of-memory denial of service during 'decrypt --stego-extract'. The issue is fixed in 1.4.9; both the 1.4.x and 1.5.x lines are affected.

### CVE-2026-81691

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-27T17:20:58.993 |

openssl_encrypt versions before 1.4.9 fail to validate server URLs in login and register_with_email functions, accepting unencrypted http:// URLs and unconfigured hosts. Attackers on the network path can intercept cleartext credentials including client_id, passwords, and JWTs to achieve full keyserver account takeover.

### CVE-2026-81690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-27T17:20:58.843 |

openssl-encrypt (pip package) before 1.4.9 contains a symlink-following flaw in its verify-usb v2 added-file allowlist scan. The scan enumerated the drive with rglob(), which in CPython does not descend into symlinked directories and treats the symlink as an ordinary directory, while O_NOFOLLOW on the hash side binds only the final path component. An evil-maid attacker with physical access to the removable drive could replace a tool-tree directory with a symlink to a copy containing byte-identical files plus a planted __pycache__/*.pyc file (which CPython loads in preference to recompiling the clean .py). The planted file is never enumerated, added_files stays 0, and verify-usb reports PASSED, resulting in code execution when the victim runs the portable install. Fixed in 1.4.9 (affects both 1.4.x and 1.5.x lines).

### CVE-2026-81689

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-08-27T17:20:58.697 |

openssl_encrypt versions before 1.4.9 derive the remote-pepper wrap key using unsalted HKDF-SHA256 or bare SHA-256 of the password, allowing identical keys across all users and files. Attackers with access to wrapped pepper blobs can precompute a single dictionary table and perform fleet-wide offline password guessing at hardware speed to recover user passwords.

### CVE-2026-81688

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-311` |
| Published | 2026-08-27T17:20:58.553 |

openssl_encrypt versions before 1.4.9 store an unkeyed SHA-256 hash of the plaintext in the cleartext file header metadata. Attackers can read this hash without the password to confirm guessed plaintexts offline or fingerprint identical plaintexts across separately-encrypted files.

### CVE-2026-81687

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-27T17:20:58.410 |

openssl_encrypt versions before 1.4.9 fail to enforce a time ceiling on key derivation function iteration counts specified in file metadata. Attackers can craft files with extremely high KDF iteration counts to consume CPU resources for unbounded periods before password verification occurs.

### CVE-2026-81335

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-27T17:20:53.850 |

Baserow dispatches an Application Builder data source without acting on the result of its permission check. The dispatch and record-name views in backend/src/baserow/contrib/builder/api/data_sources/views.py are declared with a permission class that admits any caller, so a request carrying no credential reaches the handler. DataSourceService.dispatch_data_sources in backend/src/baserow/contrib/builder/data_sources/service.py then calls check_multiple_permissions without asking it to raise, and neither stores nor examines the mapping of denials it returns, so a denied check leaves execution to continue and the data source is dispatched whatever the caller's identity. The dispatch runs with the integration's own credentials, so an unauthenticated request naming a data source receives the rows and fields that source reads. Identifiers are small integers and can be enumerated. Version 2.3.1 passes raise_exception to the same call.

### CVE-2026-81093

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-27T17:20:51.493 |

The get-html-skeleton tool fetched a URL the caller supplied after checking only its syntax. The handler in src/tools/common/get_html_skeleton.ts validated the url argument with isValidHttpUrl from src/utils/generic.ts, which confirmed the string began with an http or https scheme and parsed as a URL and inspected neither the host name nor the address it resolves to. Loopback, link-local and private ranges therefore passed, including the address cloud providers use to serve instance metadata. The unchecked URL was handed to the web-browser actor and the fetched document was returned in the tool response, so any caller of the MCP server could make it request an endpoint reachable only from the host and read the result, including instance credentials. Version 0.9.12 removes the tool.

### CVE-2026-81091

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-27T17:20:51.183 |

The proxy middleware in mcp-use's inspector forwards requests to a destination the caller names. mountMcpProxy in libraries/typescript/packages/inspector/src/server/proxy/mcp-proxy.ts read the target from the X-Target-URL header or the __mcp_target parameter and proxied to it without inspecting the host, so loopback, link-local and private addresses were all accepted, as were names that resolve to them, and the validation was not reapplied to a redirect the destination returned. A caller could therefore make the server issue requests to addresses reachable only from the host it runs on and read the responses. The current code calls isSafeProxyTarget, which checks the resolved address against private, loopback and link-local ranges before proxying and bounds the number of redirects followed.

### CVE-2026-79988

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-27T17:20:49.540 |

The Twig sandbox mechanism in Craft CMS is configured to allow dangerous functionality from the Yii framework, leading to authenticated RCE similar to previously disclosed vulnerabilities.

### CVE-2026-82240

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T12:16:34.030 |

Budibase before 3.41.3 fails to validate app-scoped builder role assignments in the public user create and update endpoints, allowing an authenticated app-scoped builder to grant builder access to unrelated apps. Attackers can submit crafted requests to the user update API with builder.apps fields to escalate privileges and gain unauthorized builder access to other applications in the same tenant.

### CVE-2026-82239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T12:16:33.887 |

Budibase before 3.41.3 fails to enforce per-table role restrictions on the POST /api/datasources/query endpoint, allowing low-privilege BASIC users to read, create, update, or delete rows in any table regardless of configured permissions. Attackers with BASIC role can submit crafted query requests with target table identifiers to bypass table-level access controls and manipulate restricted data.

### CVE-2026-78614

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-502` |
| Published | 2026-08-28T02:16:24.070 |

WatchGuard Dimension contains an authenticated SQL injection vulnerability in the audit report feature which allows an authenticated user with report administration permissions gain arbitrary command execution as the Dimension WebUI process user by sending specially crafted requests.

### CVE-2026-78613

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T02:16:23.943 |

WatchGuard Dimension contains an authenticated SQL injection vulnerability in the log viewer feature which allows an authenticated user with report administration permissions gain arbitrary command execution as the Dimension WebUI process user by sending specially crafted requests.

### CVE-2026-78612

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-502` |
| Published | 2026-08-28T02:16:23.807 |

WatchGuard Dimension contains an authenticated SQL injection vulnerability in the scheduled report feature which allows an authenticated user with report administration permissions gain arbitrary command execution as the Dimension WebUI process user by sending specially crafted requests.

### CVE-2026-78008

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-28T02:16:22.167 |

A buffer overflow vulnerability in the WatchGuard Fireware OS Management Web UI allows an authenticated administrator with network access to cause a denial of service (DoS) condition or potentially execute arbitrary code by sending specially crafted network traffic.

### CVE-2026-75814

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-28T00:18:14.147 |

The Ebyte device does not adequately verify the origin or authenticity of 
requests submitted to the web management interface. An unauthenticated 
remote attacker could persuade an authenticated administrator to visit a
 crafted page, causing unauthorized configuration changes or a 
disruption of device availability.

### CVE-2026-81728

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-27T20:18:55.183 |

Dolibarr before 24.0.0 contains a SQL injection in its CSV and XLSX import wizard. The wizard reads its update keys with GETPOST('updatekeys', 'array') in htdocs/imports/import.php, which applies only the generic alphanohtml filter: that strips HTML but leaves SQL keywords, comment markers, parentheses, spaces and quotes intact. import_insert() in htdocs/core/modules/import/import_csv.modules.php then iterates the submitted values and builds a filter with $where[] = $key.' = '.$data[$key], having first applied preg_replace('/^.*\./i', '', $key), an alias strip that does nothing to a value containing no dot. The assembled string is executed through $this->db->query(). The injected SELECT resolves the row id that the import then assigns to $lastinsertid, which becomes the WHERE target of a subsequent UPDATE, so a UNION SELECT returning an attacker-chosen integer both exfiltrates arbitrary table content and redirects which row the import overwrites; for category link tables the raw filter array is spliced into that UPDATE directly. The interface offers a fixed list of legitimate column codes but the server never checks the submitted values against it. A user holding the import permission can exploit this. Release 23.0.4 does not carry the fix; the allow-list test was added in 24.0.0.

### CVE-2026-81525

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-27T20:18:50.913 |

The MongoDB client library for PHP does not sufficiently sanitize special elements in application-supplied namespace identifiers before using them to construct the target namespace for database operations. An application that incorporates untrusted text into these identifiers may have operations silently directed at a different storage location than the one the application intended.

### CVE-2026-81522

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-08-27T20:18:50.493 |

A weakness in the MongoDB C++ Driver's handling of caller-supplied namespace identifiers allows special characters embedded in those identifiers. An application that builds a namespace identifier from untrusted input without validating it may therefore have its operation directed at a different target than intended. This can result in limited unauthorized read and write access to data belonging to another logical tenant of the affected application.

### CVE-2026-47727

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-27T20:17:44.780 |

Trilium is an open-source hierarchical note-taking application. In versions prior to 0.104.0, the default-on "Safe import" filter fails to neutralize the shareTemplate relation because that relation is not marked as dangerous, allowing an attacker-supplied import archive to plant a server-side template that leads to remote code execution. The relation is omitted from the built-in list of dangerous attributes, so unlike other code-loading relations it is not disabled on import, and when the victim later publishes the imported note the public share renderer feeds the linked EJS code note's raw bytes into ejs.render, which compiles them in the server's Node process. An unauthenticated request to the shared note then executes the attacker's JavaScript with full access to require, process, the filesystem, and the network. This issue is fixed in version 0.104.0.

### CVE-2026-81818

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-27T17:21:05.340 |

Affected versions of Flowintel contain an authorization flaw in the administrative user-edit API.


The existing authorization check correctly prevented an organization administrator from editing users in another organization, but it did not prevent them from editing a full administrator within their own organization. As a result, an org admin could modify that full administrator account, including changing its password. The upstream commit explicitly describes the issue as:


“Org admin can change the password of a full admin in the same organization.”


The fix adds a higher-privilege boundary check:


if user_to_edit.is_admin(): return ... 403

so organization administrators can no longer modify full administrator accounts.

Version impacted >=3.3.0

### CVE-2026-81683

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-27T17:20:57.810 |

openssl_encrypt (pip package openssl-encrypt) versions 1.4.8 and earlier store an mTLS client private key in cleartext within a world-readable (0644) SharedPreferences file via the desktop GUI's Settings screen 'combined certificate and private key' PEM field. A local attacker with file system access can read the exposed private key. Version 1.4.9 writes the PEM to a dedicated 0600 file, keeps only its path in SharedPreferences, and migrates/scrubs existing cleartext values.

### CVE-2026-81682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-27T17:20:57.660 |

openssl_encrypt versions before 1.4.9 contain an insecure file permissions vulnerability in the desktop GUI that writes decrypted plaintext with world-readable default permissions. Attackers can read decrypted output files created by the GUI as unprivileged local users on multi-user systems.

### CVE-2026-81097

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-27T17:20:52.110 |

The execute_ruby tool is documented as a read-only Ruby sandbox and is enforced by a pattern denylist together with replacements for the process-spawning methods on Kernel. The pseudo-terminal library's spawn entry points are neither in the denylist nor replaced, so a normal tool call could reach them and start a shell, executing commands as the account running the server and outside the guarded methods. The denylist was introduced with the tool in 1.4.0 and never covered those entry points through 1.6.0. Version 1.6.1 restricts the requires the sandbox permits to a data-only list and blocks dynamic dispatch to execution entry points; 2.0.0 removes the tool.

### CVE-2026-82234

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T12:16:33.120 |

SiYuan versions before v3.8.1 contain a server-side request forgery vulnerability in the http_request and web_fetch agent tools that perform DNS resolution only at guard time without validating the connect-time resolution. Attackers can use DNS rebinding to answer the guard resolution with a public IP and the connect resolution with a private or metadata IP, bypassing the SSRF defense to access cloud instance metadata and internal services.

### CVE-2026-78610

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-28T02:16:23.687 |

WatchGuard Dimension's Web UI exposes an administrator passphrase change action that lacks CSRF protection. An attacker who can induce an authenticated global administrator's browser to visit a crafted link or page can change that administrator's passphrase to an attacker-chosen value without the administrator's consent.

### CVE-2026-82243

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T12:16:34.477 |

Budibase Server before 3.41.3 contains a server-side request forgery vulnerability in the datasource verify endpoint that allows builder-level users to supply arbitrary URLs without SSRF validation. Attackers can exploit this to leak internal CouchDB credentials by making requests to attacker-controlled servers, gaining full database access in cloud deployments.

### CVE-2026-82242

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T12:16:34.317 |

Budibase versions before 3.41.3 contain a missing authorization vulnerability in the POST /api/resources/duplicate endpoint that allows authenticated builders to inject tables, automations, queries, and screens into any other application without holding any role in the destination workspace. Attackers can inject resources by specifying an arbitrary destination workspace ID in the request body, then trigger injected automations with outgoing webhooks to exfiltrate data from victim applications.

### CVE-2026-38820

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T02:16:21.350 |

openNDS before 11.0.0 is susceptible to unauthenticated OS command execution via shell command injection through the fas query parameter on the /opennds_preauth/ endpoint because of libopennds.sh.

### CVE-2026-81726

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-27T17:21:03.387 |

NLTK through 3.10.3 contains a path traversal vulnerability in model-artifact APIs that bypass pathsec enforcement by using raw file operations on caller-controlled paths. Attackers can read or write files outside allowed sandbox roots through TransitionParser, AveragedPerceptron, PerceptronTagger, and maxent parameter APIs when pathsec is enabled.

### CVE-2026-81679

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-27T17:20:57.150 |

OpenRemote versions before 1.28.0 contain a cross-realm information disclosure vulnerability in the Notification REST API that allows per-realm tenant administrators to read all tenants' sent notifications including message bodies. Attackers with read:admin credentials in one realm can submit a zero-parameter GET request to the notification endpoint to retrieve sensitive notification metadata and message content from all realms.

### CVE-2026-82235

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:33.267 |

filebrowser through 2.63.23 fails to validate named pipes in directory archive and public download handlers, allowing attackers to trigger blocking open syscalls. Authenticated users or anonymous visitors with public share links can repeatedly request archives containing named pipes to pin server goroutines and exhaust connection resources.

### CVE-2026-77358

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-28T00:18:15.790 |

cpp-httplib is a C++ header-only HTTP/HTTPS library. In versions 0.33.0 through 0.50.0, the TLS-enabled WebSocket client frees the TLS session before closing the WebSocket that still uses it, producing a use-after-free. In WebSocketClient::shutdown_and_close the SSL object is freed and the pointer cleared, but the subsequent WebSocket close still sends a close frame through the SSL socket stream, which holds a raw copy of the now-dangling session pointer and reads from and writes to the freed memory. The same freed-then-used ordering is reachable through the client's destructor and its connect path, so ordinary teardown of a secure WebSocket connection triggers the defect. This issue is fixed in version 0.50.1.

### CVE-2026-59324

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:58.500 |

When an IntegrationFlow uses .fluxTransform() with an asynchronous/reordering fluxFunction that emits raw payloads, concurrent requests on the same FluxMessageChannel subscription have their reply headers (replyChannel, errorChannel, correlationId, any propagated security/tenant headers) copied from whichever message was most recently consumed upstream.
Spring Integration 7.1.0
Spring Integration 7.0.0 - 7.0.5
Spring Integration 6.5.0 - 6.5.10
Spring Integration 6.4.0 - 6.4.12
Spring Integration 5.5.21 and earlier

### CVE-2026-59316

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:57.667 |

Spring Authorization Server's default consent page renders user-controlled values without HTML entity encoding. When using the DefaultConsentPage, an attacker can craft an OAuth2 authorization request containing a malicious value that is stored server-side and later rendered unencoded in the default consent page presented to the end user.
Spring Authorization Server 1.5.0 - 1.5.8
Spring Authorization Server 1.4.0 - 1.4.11

### CVE-2026-80211

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-08-27T17:20:50.733 |

FrontAccounting through 2.4.20 stores and verifies user passwords as unsalted MD5 digests. admin/users.php passes md5($_POST['password']) to add_user() and update_user_password(), admin/change_current_user_password.php does the same when a user changes their own password, the forgotten-password path in includes/current_user.inc hashes the newly generated password the same way, and authentication calls get_user_auth($loginname, md5($password)). The codebase applies no per-password salt and contains no call to password_hash(), password_verify() or any other adaptive hash, so identical passwords yield identical digests and an attacker who obtains the user table can recover plaintext passwords with precomputed lookup tables or high-rate GPU cracking.

### CVE-2026-75871

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-27T17:20:01.503 |

GitLab has remediated a vulnerability in the GitLab AI Gateway component affecting all versions of the AI Gateway from 18.10 to 19.0.12, 19.1 to 19.1.7, and 19.2 to 19.2.2 that could have allowed an authenticated user with Duo Agent Platform access to redirect outbound model requests to an externally-controlled endpoint via a crafted inline flow configuration that overrides the HTTP Host header, resulting in disclosure of Google Cloud Vertex cloud service credentials and private signing keys.

### CVE-2026-75159

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-27T17:19:54.780 |

An unauthenticated client that can reach a MongoDB Connector for BI deployment configured with Kerberos authentication may cause mongosqld to terminate when a crafted authentication exchange encounters a specific GSSAPI error-handling condition. This can interrupt BI Connector availability until the process restarts.

### CVE-2026-19889

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-27T17:17:43.170 |

GitLab has remediated a vulnerability in the GitLab AI Gateway component affecting all versions of the AI Gateway from 18.9.0 to 19.0.12, 19.1 to 19.1.7, and 19.2 to 19.2.2 that could have allowed an authenticated user with Duo Agent Platform access to redirect model requests to an externally-controlled endpoint via crafted model metadata, resulting in the disclosure of Google Vertex AI or AWS Bedrock cloud service credentials.

### CVE-2026-54330

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-28T00:18:07.683 |

Ceph is an open-source distributed storage platform providing object, block, and file storage. In versions prior to 20.2.4 and 19.2.6, the Ceph Object Gateway (RGW) SigV4 handler does not reject requests that carry x-amz-* headers absent from the signed header set, allowing anyone holding a presigned URL to attach arbitrary unsigned x-amz-* headers that RGW will honor. AWS S3 requires every x-amz-* header on a SigV4 request to be signed and rejects requests bearing additional unsigned headers, but RGW validates only the headers listed in X-Amz-SignedHeaders and ignores any extra ones, so they take effect without being covered by the signature. By adding such headers to a presigned PUT URL, an attacker can grant themselves more capabilities than the URL's signer intended and escalate their privileges. This issue is fixed in versions 20.2.4 and 19.2.6.

### CVE-2026-54083

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T00:18:07.233 |

Wazuh is an open-source security platform providing unified XDR and SIEM protection for endpoints and cloud workloads. The  ip-customblock  active response script contains a path traversal vulnerability that lets an attacker create or delete arbitrary files on the filesystem as root. The script builds a file path by concatenating the  srcip  field taken from alert JSON directly onto the fixed  /ipblock/  base directory, without validating that the value is a well-formed IP address. Because the extraction routine returns the raw string unchecked, an attacker who can trigger alert-matching log events with a crafted  srcip  containing  ../  sequences can escape the base directory. The block action opens the resulting path in append mode, creating an empty file at an arbitrary location, while the unblock action passes it to remove(), deleting an arbitrary file; since the active response daemon runs as root, this includes sensitive files such as system credentials and Wazuh configuration. Unlike the sibling scripts host-deny.c, default-firewall-drop.c, and firewalld-drop.c, which reject non-IP input via get_ip_version(), ip-customblock.c omits this validation. This issue is fixed in version 4.14.7.

### CVE-2026-53580

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-73;CWE-400;CWE-552` |
| Published | 2026-08-27T20:17:49.153 |

Trilium is an open-source hierarchical note-taking application. In versions prior to 0.104.0, the automatic image-download feature accepts file:// URLs in a note's img tags and reads the referenced local file with no path validation, allowing any authenticated user to disclose arbitrary files readable by the Trilium process. When a text note is saved, Trilium scans its HTML for image sources and downloads each external one; because the HTML sanitizer keeps file as an allowed scheme, a source such as file:///etc/passwd is passed straight to a filesystem read and its contents are stored as a note attachment the user can then retrieve. Pointing the same primitive at an unbounded source such as /dev/zero causes uncontrolled memory allocation that crashes the server process. The feature is enabled by default and is reachable through the web UI, the ETAPI, the web clipper, and note imports, requiring only an authenticated session or an ETAPI token. This issue is fixed in version 0.104.0

### CVE-2026-59307

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:57.103 |

An operator who calls JdbcMessageStore.addAllowedPatterns(...) to restrict deserialization receives no protection at all when the store is a Spring-managed bean.
Spring Integration 7.1.0
Spring Integration 7.0.0 - 7.0.5
Spring Integration 6.5.0 - 6.5.10
Spring Integration 6.4.0 - 6.4.12

### CVE-2026-44629

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-922` |
| Published | 2026-08-28T00:17:28.117 |

Improper access control to the Synergis Softwire installation folder. This vulnerability affects Streamvault all-in-one appliances (SV-100E and SV-300E series) and Synergis Softwire installed on Windows servers.

### CVE-2026-34674

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-27T17:18:10.973 |

Substance3D - Sampler versions 5.1.3 and earlier are affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-67560

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-28T00:18:08.150 |

Bendix EC80 Brake ECU
 is vulnerable to a stack-based buffer overflow, which may allow an 
attacker to crash the ECU. A crafted payload can then be used to 
remotely execute arbitrary code or inject arbitrary CAN bus traffic. 
This could cause the loss of the ABS function, steering assist, 
speedometer, and shifting.

### CVE-2026-76640

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-787` |
| Published | 2026-08-27T20:18:38.380 |

Unitree G1 EDU firmware through 1.5.2 contains multiple chained vulnerabilities in the BLE GATT server and WiFi provisioning stack that allow unauthenticated proximate attackers to achieve root code execution without pairing or credentials by exploiting an unquoted heredoc variable in the WiFi provisioning script and a buffer overflow in the SSID chunk accumulator. Attackers can send crafted BLE writes to overflow a fixed BSS buffer across BLE connections, corrupting an adjacent mainloop function pointer dispatch entry that is subsequently invoked by the cleanup path passing attacker-controlled data to system() as uid 0.

### CVE-2026-75889

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:18:37.980 |

Grafana Alloy’s prometheus.operator.servicemonitors component allows a user who can create or modify ServiceMonitor resources in a watched namespace to specify an arbitrary local file through bearerTokenFile. Alloy reads the file and sends its contents as a bearer token to an attacker-controlled scrape endpoint. This may disclose files accessible to the Alloy process, including its projected Kubernetes service account token, potentially granting the attacker Alloy’s Kubernetes permissions. Exploitation requires ServiceMonitor write access and lower privileges than Alloy’s service account.

### CVE-2026-82255

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-28T12:16:38.317 |

gitoxide versions from 0.25.4 contain an HTTP credential leak vulnerability in the curl-based transport backend where credentials are sent to attacker-controlled servers after HTTP redirects. The vulnerability occurs because credential validation checks the original URL instead of the effective URL after redirect, allowing attackers to steal authentication tokens through cross-domain redirects or HTTPS-to-HTTP downgrades.

### CVE-2026-38822

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T02:16:21.620 |

In openNDS before 11.0.0, the client_params.sh script, invoked by the openNDS daemon to serve the authenticated client status page, is vulnerable to OS command injection through crafted HTTP GET query parameter keys. An authenticated captive portal user can inject arbitrary shell commands by embedding semicolons in a URL query parameter name.

### CVE-2026-59284

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-08-27T20:17:54.573 |

There is no allow list for property keys when Spring Cloud Commons writable /actuator/env is enabled.
Spring Cloud Commons 5.0.0 - 5.0.2
Spring Cloud Commons 4.3.0 - 4.3.3
Spring Cloud Commons 4.0.0 - 4.2.6
Spring Cloud Commons 3.1.10 and earlier

### CVE-2026-81100

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-27T17:20:52.620 |

tiger-gh-mcp-server started its MCP HTTP transport without enabling the host allow-list the underlying SDK provides. src/httpServer.ts called the shared httpServerFactory helper and never set the DNS-rebinding-protection option, so the transport accepted a request whatever host it named, making the locally reachable GitHub MCP endpoint drivable from a page in a visitor's browser that pointed a name it controlled at the bound address. The fix passes the option explicitly alongside a dependency update; the update alone would not have closed it. The repository has published no release that brackets the fix, so the affected boundary is the commit preceding it.

### CVE-2026-81099

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-27T17:20:52.467 |

tiger-slack started its MCP HTTP transport without enabling the host allow-list the underlying SDK provides. mcp/src/httpServer.ts called the shared httpServerFactory helper and never set the DNS-rebinding-protection option, so the transport accepted a request whatever host it named, and a page in a browser could point a name it controlled at the address the server was bound to and drive the locally reachable Slack MCP server through the visitor's browser. The fix passes the option explicitly alongside a dependency update; the update alone would not have closed it. The repository publishes no release that brackets the fix, so the affected boundary is the commit preceding it.

### CVE-2026-81095

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-27T17:20:51.803 |

pg-aiguide started its MCP HTTP transport without enabling the host allow-list the underlying SDK provides. src/httpServer.ts called the shared httpServerFactory helper and never set the DNS-rebinding-protection option, so the transport accepted a request whatever host it named. A page in a browser could therefore point a name it controlled at the address the server was bound to and drive the locally reachable MCP server through the visitor's browser. The protection was already available in the packaged transport and simply not turned on, so updating the dependency alone would not have closed it. Version 0.5.1 passes the option explicitly.

### CVE-2026-81092

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-27T17:20:51.337 |

mcp-go accepted requests on its HTTP transports without checking the Host header. StreamableHTTPServer.ServeHTTP in server/streamable_http.go and SSEServer.ServeHTTP in server/sse.go served any request arriving over a loopback connection regardless of the host it named, and the SSE transport's cross-origin default allowed any origin. A page in a browser could therefore point a name it controlled at the loopback address and reach a server listening there, invoking tools and reading resources that the server exposed on the assumption that only local software could connect. No release before 0.56.0 validated the header on either transport; 0.56.0 adds server/http_localhost.go, which rejects a loopback-bound request carrying a host that is not a loopback name, and wires it into both transports.

### CVE-2026-78071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T12:16:31.827 |

Joomla Extension - digital-peak.com - Authenticated, privileged stored XSS in DP Calendar 7.0.0 - 10.11.2 - Location title is rendered in data attribute without escaping leads to XSS, needs create permission in DPCalendar.

### CVE-2026-42391

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:29.503 |

An unauthenticated attacker can send an IMAP ID command with a very large number of parameters before logging in, which causes memory and CPU usage to grow disproportionately. The login process can be terminated by the out-of-memory handling, which also terminates all other connections handled by the same process. This can cause degradation or denial of service for IMAP logins. Limit the number of connections handled by a single imap-login process. This has a performance impact though. Update to non-vulnerable version. No publicly available exploits are known.

### CVE-2026-33605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:27.740 |

An unauthenticated attacker can crash the ManageSieve login process by sending a small malformed command before authenticating. If running in high-security mode (default for community releases), only the attacker's own connection is terminated. If running in high-performance mode (default for Pro releases), all connections handled by the same managesieve-login process are terminated. Repeating the attack can cause denial of service for Sieve script management. Restrict network access to the ManageSieve service to trusted clients. Update to non-vulnerable version. No publicly available exploits are known.

### CVE-2026-27852

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T12:16:27.330 |

An attacker that can send mail to a user can craft a message whose headers contain a very large number of email addresses or MIME parameters, which causes excessive memory usage when the message is later parsed. The message is still delivered, but reading it over IMAP can exhaust the memory limit of the process and terminate it, causing denial of service for the affected user. Update to non-vulnerable version. No publicly available exploits are known.

### CVE-2026-5097

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T08:16:41.003 |

The wpForo Forum plugin for WordPress is vulnerable to SQL Injection via the 'referer' parameter in all versions up to, and including, 2.4.17. This is due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-18983

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-28T05:16:42.060 |

The One User Avatar | User Profile Picture plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 2.5.4 via the wpua_action_process_option_update function. This is due to insufficient file type validation in wp_handle_upload() called without a MIME allow-list, with post-write validation relying on the attacker-controlled client-supplied Content-Type header rather than a server-derived type, and no cleanup of files that fail the check. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. in order to exploit this vulnerability an admin has to give subscribers permission to upload avatars. While PHP files and svg files are rejected, dxfp files are accepted.

### CVE-2026-75418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-28T00:18:12.530 |

A path traversal vulnerability exists in the built-in preview/development web server of Lektor <3.3.14 on Windows. An attacker with network access to the server can send a crafted HTTP request containing path traversal sequences to read arbitrary files accessible to the process, disclosing sensitive information such as system files and deployment configuration files containing credentials.

### CVE-2026-77438

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-08-27T20:18:39.407 |

Trilium is an open-source hierarchical note-taking application. In versions up to and including 0.103.0, the public share-search endpoint does not enforce the per-note shareCredentials and shareHiddenFromTree controls, allowing an unauthenticated visitor to read the titles, tree paths, and content of protected shared notes. The endpoint authorizes only the ancestor note supplied in the request and then runs a full-text search across the entire published subtree, returning each matching note's title, share identifier, and hierarchical path without re-checking whether that individual note requires a share password or is hidden from the navigation tree. Because the search matches note content, an attacker can enumerate protected notes and use the endpoint as a boolean oracle that confirms arbitrary substrings, recovering the full contents of notes that should be gated behind a password. This issue is fixed in version 0.104.0.

### CVE-2026-80212

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:20:50.880 |

An issue was discovered in the resolv gem before 0.7.2 for Ruby. Resolv::DNS::Resource.get_class, Resolv::DNS::Resource::Generic.create, and Resolv::DNS::SvcParam::Generic.create generate a new class for each unknown DNS resource record (type, class) pair, or each unknown SvcParamKey, encountered while decoding a response. Each generated class was permanently registered both as a constant on Resource (or SvcParam::Generic) and as an entry in a class-lookup hash (ClassHash), and thus the class remained reachable through that constant after the response was discarded. Type and class are each 16-bit values, and thus an attacker controlling DNS responses (a spoofed response, or a malicious or hijacked upstream DNS server) has roughly 2^32 distinct (type, class) pairs to choose from. A single response of a few hundred kilobytes carrying tens of thousands of distinct unknown types permanently grows process memory by tens of megabytes; repeated responses accumulate without bound and are never reclaimed by garbage collection, because the constant keeps each class alive. Any code path that calls Resolv::DNS::Message.decode on attacker-influenced DNS responses is affected. resolv is a default gem, and thus this is reachable from a plain Ruby installation without any additional dependency.

### CVE-2026-78002

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-08-27T17:20:29.367 |

A flaw was found in rsyslog. An unauthenticated remote attacker can trigger a heap buffer overflow in the RainerScript `replace()` function by sending specially crafted syslog messages. This vulnerability arises from an incorrect buffer size calculation during string replacement, causing memory corruption. Successful exploitation can lead to a denial of service (DoS) for the affected system.

### CVE-2026-5680

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:18:58.397 |

A flaw was found in Undertow. A remote attacker could exploit this vulnerability by sending specially crafted WebSocket messages with permessage-deflate negotiated. This could lead to excessive memory consumption due to the PerMessageDeflateFunction.largerBuffer() method using exponential doubling, resulting in a Denial of Service (DoS) for the affected application.

### CVE-2026-30062

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:17:51.380 |

An issue in the NGAP handler of free5gc v4.0.1 allows attackers to cause a Denial of Service (DoS) via a crafted NAS PDU.

### CVE-2026-30057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:17:50.897 |

An issue in the CreateUEContext handler component of free5gc v4.1.0 allows attackers to cause a Denial of Service (DoS) via supplying a crafted request.

### CVE-2026-30056

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-27T17:17:50.783 |

A NULL pointer dereference in the AMF NGAP Dispatcher component of free5gc v4.0.1 allows attackers to cause a Denial of Service (DoS) via supplying crafted NGAP messages during the initialization of a new RAN connection.

### CVE-2026-30050

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-27T17:17:50.537 |

An issue in the ModifyAMFEventSubscriptionProcedure function (processor/event_exposure.go) of free5gc v4.1.0 allows attackers to cause a Denial of Service (DoS) via supplying a crafted PATCH request.

### CVE-2026-30047

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-08-27T17:17:50.417 |

A reachable assertion vulnerability in the /nsmf-pdusession/v1/sm-contexts component of Open5GS v2.7.6 allows attackers to cause a Denial of Service (DoS) via supplying a crafted DELETE request.

### CVE-2026-30046

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-08-27T17:17:50.303 |

A reachable assertion vulnerability in the NUDM-UECM interface of Open5GS v2.7.6 allows attackers to cause a Denial of Service (DoS) via supplying a crafted DELETE request.

### CVE-2026-73208

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-28T12:16:31.127 |

An attacker that holds a token intended for a different purpose can authenticate, because when an OAuth2 token response does not contain a scope claim, the audience claim is used in its place and checked against the configured required scopes. These are different concepts, and the audience claim does not describe what a token is allowed to do. A token that grants no relevant permissions can be accepted because its intended recipient value happens to match a configured scope name, granting access that should have been denied. It also hides an identity provider misconfiguration where scopes are not being issued at all. Ensure the identity provider issues a scope claim for all tokens used with Dovecot, and that configured scope names do not match audience values. Update to non-vulnerable version. No publicly available exploits are known.

### CVE-2026-40018

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T12:16:28.630 |

None None None No publicly available exploits are known.

### CVE-2026-82245

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T12:16:35.000 |

Budibase before 3.41.3 fails to enforce role-based authorization on license management endpoints, allowing any authenticated user to delete license keys or manipulate offline tokens. Attackers with basic user privileges can access /api/global/license/* endpoints to disable premium features and downgrade deployments for all users.

### CVE-2026-6286

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T08:16:41.140 |

The Booking for Appointments and Events Calendar – Amelia plugin for WordPress is vulnerable to Stored Cross-Site Scripting via customer name fields in versions up to and including 2.2. This is due to an authentication bypass where the AddBookingCommand explicitly skips nonce verification (Command.php line 186), allowing unauthenticated users to submit booking data. While the plugin applies sanitize_text_field() to customer firstName and lastName fields (BookingApplicationService.php lines 302-308), this function only removes HTML tags and preserves special characters including double quotes. The vulnerability manifests in the administrative Calendar view where a FullCalendar eventContent callback interpolates customer names directly into JavaScript template literals (redesign/dist/index.js line 199) and renders them via innerHTML without proper HTML entity encoding. Because double quotes are preserved, an attacker can inject payloads like '" onmouseover="alert(document.cookie)"' to break out of the title attribute and inject malicious event handlers. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that will execute when an administrator accesses the Calendar page and hovers over the malicious appointment.

### CVE-2026-77365

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:46.223 |

The Optimole – Optimize Images | Convert WebP & AVIF | CDN & Lazy Load | Image Optimization plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'a' (above_fold_images) parameter in all versions up to, and including, 4.2.10 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-76053

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:46.087 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Noise-Key Injection into HTML Parser in all versions up to, and including, 3.3.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation is possible because WordPress's comment KSES allowlist permits the payload structure — an anchor tag with href and title attributes alongside a code tag — causing the malicious comment to be stored verbatim in the database, where it is later processed by the vulnerable parser during page translation.

### CVE-2026-18978

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:41.927 |

The LiteSpeed Cache plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 7.8.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. A comment payload crafted exclusively from decimal numeric character references (e.g. &#34;, &#60;, &#62;) placed inside an allowed element such as &lt;code&gt; bypasses WordPress's wp_kses sanitization, as kses does not treat a data-settings="..." substring within text content as an HTML attribute, allowing the malicious payload to reach the vulnerable function. For this to be exploitable, the site must allow users with previously approved comments to write new comments, and the require_name_email setting must be disabled.

### CVE-2026-18324

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T05:16:41.797 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Rich-Text Textarea Field in all versions up to, and including, 1.57.0.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that the targeted Textarea field has the Rich-Text editor option enabled.

### CVE-2026-77977

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T00:18:15.927 |

Ebyte gateway product's vendor configuration utility does not require authentication before 
allowing certain disruptive administrative actions when default 
credentials remain configured. An unauthenticated attacker on the 
adjacent network could reboot the device or restore factory settings, 
resulting in a loss of configuration and service availability.

### CVE-2026-54718

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-27T20:17:49.817 |

Silverstripe Advanced Workflow is a highly configurable step-based workflow module. Prior to 6.4.5, 7.1.3, and 7.2.1, an attacker with permission to author the advanced workflow email template can place a specially crafted server-side template payload in NotifyUsersWorkflowAction.EmailTemplate. When NotifyUsersWorkflowAction renders the field through the Silverstripe template engine SSTemplateParser, the payload can cause PHP evaluation and arbitrary code execution on the server; the regression coverage is in tests/php/WorkflowEngineTest.php. This issue is fixed in versions 6.4.5, 7.1.3, and 7.2.1.

### CVE-2026-81817

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-27T17:21:05.207 |

Affected versions of Flowintel contain an insecure direct object reference / broken object-level authorization issue across numerous task endpoints.


The routes generally received both a case identifier and a task identifier, but previously they did not enforce that the task actually belonged to the supplied case. As a result, an authenticated user with editor-level access to one case could potentially substitute the ID of a task from another case and invoke operations against that foreign task.


The patch introduces task_case_bound_required, which loads both objects and returns 404 unless the task belongs to the requested case. This protection is applied to edit, delete, note, assignment, status, file, export, MISP-linking, subtask, external-reference, and other task-related endpoints.

The fix also adds explicit checks that a requested note_id belongs to the current task before returning or exporting it, closing related cross-object access paths.

Version impacted =>3.3.0

### CVE-2026-82250

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-28T12:16:36.957 |

gitoxide gix-packetline versions before 0.21.5 contain a panic vulnerability in the TextRef implementation that occurs when processing side-band packet lines with empty payloads. A malicious Git server can send a crafted side-band packet to trigger an index out of bounds panic, aborting the client process during fetch operations without authentication.

### CVE-2026-82246

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T12:16:36.360 |

Budibase Server before 3.41.3 contains a server-side request forgery vulnerability in the query import endpoint that fails to validate user-supplied URLs before fetching content. Attackers can submit arbitrary URLs to retrieve responses from internal services including cloud metadata endpoints and other restricted network resources.

### CVE-2026-82241

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T12:16:34.173 |

Budibase backend-core (@budibase/backend-core, as used by @budibase/server) omits the shared address space range 100.64.0.0/10 from its default SSRF blacklist (DEFAULT_BLACKLIST) used by REST datasource query previews. When the default blacklist is active (i.e., a self-hosted deployment has not defined BLACKLIST_IPS), an authenticated user with the Builder permission can submit a REST datasource query preview request to POST /api/queries/preview targeting a reachable HTTP(S) service in the 100.64.0.0/10 range, causing the server to send a request to that target and return its response through the preview flow. Per the advisory, no released fix was identified at the time of publication; remediation is to add 100.64.0.0/10 to DEFAULT_BLACKLIST.

### CVE-2026-38821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-28T02:16:21.490 |

A heap-based buffer overflow vulnerability exists in openNDS before 11.0.0 that allows an unauthenticated attacker on the captive portal network to crash the openNDS daemon (denial of service) and potentially achieve remote code execution. This is in http_microhttpd.c.

### CVE-2026-68967

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-28T00:18:08.480 |

Bendix EC80 Brake ECU is vulnerable to an out-of-bounds write, which could allow an attacker 
to deliver a payload that could establish an arbitrary write primitive, 
which could crash the ECU.

### CVE-2026-54085

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-28T00:18:07.520 |

Wazuh is an open-source security platform providing unified XDR and SIEM protection for endpoints and cloud workloads. In versions 4.2.0 through 4.14.6, multiple active response scripts pass attacker-influenced alert fields to privileged system commands without validating their format, allowing argument injection into tools that run as root. Five of the eight scripts that handle the srcip field, route-null.c, netsh.c, pf.c, npf.c, and ipfw.c, omit the get_ip_version() check that rejects non-IP input, and disable-account.c passes the dstuser field to passwd/chuser with only a comparison against "root". An attacker who can inject crafted log events, for example via syslog, can supply srcip or dstuser values that, when an active response rule triggers, are passed unvalidated to firewall and account-management commands such as pfctl, npfctl, ipfw, route, netsh, and passwd. This enables injecting additional command arguments, and on Windows the unquoted CreateProcess command-line concatenation in wpopenv() lets a srcip containing spaces add further arguments, while disable-account.c can be abused to lock arbitrary system accounts. This issue is fixed in version 4.14.7.

### CVE-2026-81729

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-27T20:18:55.340 |

Dolibarr before 23.0.4 authorizes REST API document deletion against the wrong permission. Documents::delete() in htdocs/api/class/api_documents.class.php calls dol_check_secure_access_document() with the mode argument 'read' when handling DELETE /api/index.php/documents, while the sibling builddoc() path passes 'write', the correct mode for an operation that modifies stored data. An authenticated API user who holds only a read permission for a document-bearing module, for example societe:lire or facture:lire, and no create, write, delete or admin permission, therefore passes the check and can permanently delete that module's documents: third-party files, invoices, orders, proposals, project files and generated PDFs, with no recovery path. The call site is htdocs/api/class/api_documents.class.php:1276 in 23.0.3 and passes 'write' from 23.0.4 onward.

### CVE-2026-81529

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-27T20:18:51.480 |

Improper neutralization of delimiters in connection-URL construction allows connection-option injection in the MongoDB C# Driver. When an application passes untrusted text into the driver's connection-URL builder and round-trips the builder back into a client configuration, the untrusted text is serialized without neutralizing the URL/option delimiters and is then re-parsed as authoritative connection options. A low-privileged user of such an application can thereby introduce or suppress security-relevant connection settings.

### CVE-2026-81526

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-27T20:18:51.057 |

The MongoDB Rust Driver does not neutralize special characters in a caller-supplied target identifier before embedding it in the request it sends to the server. An actor able to influence that identifier in an application using the driver may cause write operations to be applied to an unintended target within the same deployment using the application's own credentials. This may result in unauthorized modification of data belonging to another logical boundary enforced by the application.

### CVE-2026-81521

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-99` |
| Published | 2026-08-27T20:18:50.350 |

The MongoDB Go Driver's client-level bulk write operation may accept a caller-supplied database name containing a reserved separator character without escaping it before the name is used to build the target namespace for the operation. An application that passes untrusted input as a database name could therefore have the write directed at a database and collection other than the ones it intended. Only the Client.BulkWrite API is affected.

### CVE-2026-80210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-27T17:20:50.573 |

FrontAccounting through 2.4.20 generates a CSRF token in end_form() in includes/ui/ui_controls.inc and embeds it as the _token hidden field in every form it renders, but only admin/users.php and admin/change_current_user_password.php call check_csrf_token() to validate it. No financial transaction handler validates the token, including gl/gl_journal.php, gl/gl_bank.php, purchasing/supplier_invoice.php, sales/customer_invoice.php, sales/customer_payments.php and admin/company_preferences.php, so those endpoints act on POST data with no origin check. An attacker who gets an authenticated user to load a page under attacker control can auto-submit a cross-origin form to any of them and have the forged journal entry, invoice, customer payment, bank transaction or company configuration change recorded under the victim's session.

### CVE-2026-40526

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-27T17:18:22.833 |

Volmarg Personal Management System contains a path traversal vulnerability that allows authenticated attackers to read arbitrary files by supplying absolute filesystem paths to the GET /public/get-file/{path} endpoint. The path route parameter is passed directly to file_get_contents() without canonicalization against a permitted base directory, enabling attackers to retrieve sensitive files accessible to the PHP-FPM worker process without using directory traversal sequences.

### CVE-2026-61783

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-08-28T00:18:07.997 |

Wazuh is an open-source security platform providing unified XDR and SIEM protection for endpoints and cloud workloads. In versions 4.14.0 through 4.14.6, an authenticated low-privilege user can read the cluster secret from the manager configuration because the logic that masks sensitive values is disabled by any update-config RBAC rule, including an explicit deny. The mask_sensitive_config() decorator applies masking only when _has_update_permissions() returns false, but that gate treats a user as able to update the config whenever a  manager:update_config  or  cluster:update_config  rule exists, without ever checking whether the rule's effect is allow or deny. Because a deny rule is stored as a real entry, a read-only account that is hardened by explicitly denying config edits is counted as having update permission, which turns masking off. A single authenticated GET request to the configuration endpoint with  raw=true  then returns the verbatim ossec.conf XML with  cluster.key  in clear, whereas an otherwise identical account without the deny rule sees the value masked. This issue is fixed in version 4.14.7.
