# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-25 15:00 UTC
- **対象期間**: `2026-11-24T15:00:35.000Z` 〜 `2026-11-25T15:00:47.000Z`
- **重要CVE数**: 281 件（Critical 9.0+: 68 件 / High 7.0〜: 213 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件近く** に上り、特に **Web アプリケーションフレームワーク・クラウドサービス・Adobe 製品** に集中しています。  
- **リモートからのコード実行 (RCE) や特権昇格** が多数報告され、攻撃者が認証不要でシステム全体を支配できるリスクが顕在化。  
- 多くは **入力サニタイズ不備・セッション管理不備・認可ロジックの欠陥** が根本原因で、パッチ適用だけでなく **設定見直しやネットワーク分離** が併せて求められます。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑78114** | 10.0 | Apache **JSPWiki** (2.10‑3.0.0) の **Session Fixation** | セッション ID が認証後に再生成されず、攻撃者が事前に設定した ID を使って被害者になりすますことが可能。JSPWiki は社内ナレッジベースとして広く利用されているため、情報漏洩や内部不正の入口になり得る。 |
| **CVE‑2026‑86155** | 10.0 | Apache **Jena Fuseki** (≤6.2.0) の **SSRF**（SHACL バリデーション） | 攻撃者が任意の内部サーバへ HTTP リクエストを送信でき、クラウド環境や内部ネットワークの情報取得・サービス横取りが可能。Fuseki は RDF データストアとして多くのデータ連携基盤で使用されている。 |
| **CVE‑2026‑109484** | 10.0 | **Azure App Service** の「特殊要素インジェクション」 | Azure の PaaS 環境で特権昇格が可能になるため、マルチテナント環境や顧客データへの不正アクセスリスクが極めて高い。Microsoft が提供する緊急パッチが必須。 |
| **CVE‑2026‑132877** / **CVE‑2026‑123266** (同一脆弱性) | 9.9 | **Adobe Experience Manager** の **コードインジェクション** | 低権限ユーザーが任意の Java コードを実行でき、管理者権限取得やデータ改ざんが可能。Adobe 製品は大手企業の Web ポータルで広く採用されている。 |
| **CVE‑2026‑125676** (他同系) | 9.9 | **Adobe Campaign Classic** の **コードインジェクション** | キャンペーン管理システムに対するリモートコード実行は、顧客情報・マーケティングデータの流出・改ざんにつながる。多数の同系 CVE が同時に報告されている点も注意が必要。 |

> **注**：上記はスコア・影響範囲・利用者数・公開時期（緊急度）を総合的に評価した結果です。特に **CVE‑2026‑78114** と **CVE‑2026‑86155** は「認証不要でネットワーク横断的に影響を及ぼす」点で、最優先で対策が必要です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 | 現行脆弱バージョン | 推奨バージョン | アップデート手順 |
|------|-------------------|----------------|----------------|
| Apache **JSPWiki** | 2.10 〜 3.0.0 | **3.0.1 以上** | `git clone https://github.com/jspwiki/jspwiki.git && git checkout tags/3.0.1 && mvn clean install` |
| Apache **Jena Fuseki** | ≤ 6.2.0 | **6.3.0 以上** | `apt-get update && apt-get install -y fuseki-server=6.3.0`（Debian 系） |
| **Azure App Service** | すべてのリリース | **2026‑03‑Security‑Patch**（Microsoft が提供） | Azure Portal → 「App Service」→「更新プログラム」→「緊急パッチ適用」 |
| **Adobe Experience Manager** (AEM) | 6.5.0‑6.5.14 | **6.5.15 以上** (または最新の 7.x 系) | Adobe Package Manager で `AEM-6.5.15‑Security‑Fix.zip` をインストール |
| **Adobe Campaign Classic** (ACC) | 23.1‑23.2 | **23.3.0 以上** | Adobe Campaign Console → 「アップデート」→「最新パッチ」適用 |
| **WP Rocket** (WordPress) | < 3.24.2 | **3.24.2 以上** | WordPress 管理画面 → 「プラグイン」→「更新」または `composer require wp-rocket/wp-rocket:^3.24.2` |
| **Genetec Security Center** | 5.12‑5.14 | **5.15 以上** (Microsoft KB 2026‑xxxx) | Genetec 管理コンソール → 「システムアップデート」→「最新リリース」適用 |
| **Thymeleaf** | < 3.1.6.RELEASE | **3.1.6.RELEASE 以上** | Maven: `<dependency><groupId>org.thymeleaf</groupId><artifactId>thymeleaf</artifactId><version>3.1.6.RELEASE</version></dependency>` |

### 3.2 設定・運用上の緩和策
- **セッション管理**：JSPWiki だけでなく社内全 Web アプリで **認証後に必ず新しいセッション ID を発行** する設定を有効化（`session.invalidate()` / `session.regenerateId()`）。  
- **外部リクエスト制御**：Fuseki の SHACL バリデーションを使用しない場合は **機能を無効化**、または **内部ネットワークへのアウトバウンド HTTP をファイアウォールで制限**。  
- **Azure App Service**：**アプリケーション設定で `WEBSITE_DISABLE_SLOW_REQUEST_LOGGING` を無効化**し、特殊文字のエスケープを徹底。Microsoft が提供する **App Service Hardening Guide** に沿って WAF ルールを追加。  
- **Adobe 製品

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-78114

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-25T11:17:13.853 |

Session Fixation in the login flow of Apache JSPWiki versions 2.10 through 3.0.0 on all platforms. The session identifier was not replaced when a user authenticated, so an attacker who could set a known session identifier in the browser of a victim could use the same identifier after the victim logged in.



Users are recommended to upgrade to version 3.0.1 (3.x) or 2.12.6 (2.x), which fix this issue.

### CVE-2026-86155

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T19:18:25.433 |

A vulnerability in Apache Jena Fuseki in the SHACL validation functionality cause server side request forgery (SSRF).



This issue affects Apache Jena Fuseki: through 6.2.0.



Users are recommended to upgrade to version 6.3.0, which fixes the issue.

### CVE-2026-109484

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-75` |
| Published | 2026-11-24T18:18:45.157 |

Failure to sanitize special elements into a different plane (special element injection) in Azure App Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-132877

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T19:18:09.507 |

Adobe Experience Manager is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123266

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T19:18:04.280 |

Adobe Experience Manager is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-125676

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:54.227 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-125675

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:54.080 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123987

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:53.753 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123986

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:53.603 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123723

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:53.453 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123722

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:53.310 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123342

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:18:53.000 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-125812

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T13:17:26.063 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in WP Media WP Rocket wp-rocket allows Path Traversal.This issue affects WP Rocket: from n/a before 3.24.2.

### CVE-2026-124284

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-24T22:18:49.567 |

A critical security vulnerability affects certain authentication methods in Genetec Security Center, including external identity providers using OpenID Connect (OIDC) or SAML 2.0, and Active Directory Federation Services (AD FS) using WS-Trust or WS-Federation.
Under specific conditions, successful exploitation may allow an unauthenticated attacker to gain unauthorized access to the system with the privileges of an affected user. Successful exploitation requires a specific combination of conditions to be met, which reduces the likelihood of a successful attack.

### CVE-2026-112732

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-24T20:18:21.960 |

Double free in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-136441

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-24T19:18:20.130 |

Bytebase DBHub MCP Incorrect Authorization Authentication Bypass Vulnerability. This vulnerability allows remote attackers to bypass authentication on affected installations of Bytebase DBHub. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the implementation of the MCP server. The issue results from an incorrect authorization decision when parsing untrusted SQL. An attacker can leverage this vulnerability to bypass authentication on the system. Was ZDI-CAN-27635.

### CVE-2026-136434

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T19:18:19.273 |

Super Magic PHPSandbox Command Injection Sandbox Escape Vulnerability. This vulnerability allows remote attackers to bypass the sandbox on affected installations of Super Magic. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the PHPSandbox endpoint. The issue results from the lack of proper validation of a user-supplied string before using it to execute PHP code. An attacker can leverage this vulnerability to escape the sandbox and execute arbitrary code in the context of the service account. Was ZDI-CAN-28102.

### CVE-2026-134019

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T17:18:16.213 |

PyTables is a Python package to manage extremely large amounts of data. In 3.11.1 and earlier, tables/attributeset.py treats a NumPy bytes scalar ending in a period as a pickled Python object and calls pickle.loads() when the attribute is accessed through AttributeSet.__getattr__ or AttributeSet.__getitem__. Opening an attacker-controlled HDF5 file and reading an affected metadata attribute can execute attacker-controlled code in the consumer’s process. No fixed version is available as of this review.

### CVE-2026-125717

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T18:18:54.533 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to sensitive data or functionality. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-123721

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-24T18:18:53.160 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to sensitive resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-136410

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-917` |
| Published | 2026-11-24T19:18:16.850 |

Thymeleaf before 3.1.6.RELEASE contains a restricted expression mode bypass vulnerability that allows unauthenticated remote attackers to perform forbidden actions through improperly scoped expression objects. Attackers can inject input into restricted contexts like preprocessing, th:utext, th:on* handlers, fragment names, or TEXT templates to escalate server-side template injection.

### CVE-2026-97180

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T13:17:33.187 |

ASSA ABLOY Seawing SC-1000 WebConfig is vulnerable to remote command injection via HTTP request. Due to the lack of input sanitization, a privileged attacker can inject shell metacharacters in the server parameter, resulting in arbitrary command execution as the root user on the operating system.


This issue was fixed in version 1.5.14.

### CVE-2026-129393

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-24T18:19:01.310 |

Joomla! Core - [20261156] - Core - RCE through media custom field parameters in Joomla 4.0.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of media field parameters in the generated form XML allowed manipulating the form definition, leading to a remote code execution vulnerability.

### CVE-2026-136184

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1385` |
| Published | 2026-11-24T17:18:46.180 |

compose-farm 0.19.0 before 1.22.0 contains a cross-site WebSocket hijacking and cross-site request forgery vulnerability because its unauthenticated web UI performs no Origin validation. Malicious websites visited by users can open /ws/shell/{host} or /ws/exec sockets, or abuse unquoted service parameters and PUT /api/console/file, to execute commands on all managed hosts.

### CVE-2026-129968

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-25T13:17:26.377 |

LiteSpeed Cache Plugin for Prestashop does not verify authenticity of "pd" parameter and uses it to render a template without checking that it is a real .tpl file. An unauthenticated attacker can send specially crafted requests to a store that cause the server to process attacker-suplied content, potentially giving the attacker full control of the store and access to customer and payment data.


This issue was fixed in version 1.6.2.

### CVE-2026-136706

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-25T10:17:15.037 |

This vulnerability exists in the DIGIT Platform due to improper neutralization of user supplied input while constructing SQL queries and execution in the affected User and Access Control Service components. An unauthenticated remote attacker could exploit this vulnerability by sending specially crafted input through the affected API endpoint to the targeted system.

Successful exploitation of this vulnerability could allow the attacker to execute arbitrary SQL queries, potentially resulting in unauthorized disclosure, modification or deletion of database information on the targeted system.

### CVE-2026-136553

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-25T07:17:18.930 |

A vulnerability was detected in Tenda RX3 16.03.13.11_multi. Affected is an unknown function of the file /goform/fast_setting_wifi_set. Performing a manipulation of the argument loginPwd results in improper authentication. It is possible to initiate the attack remotely. The exploit is now public and may be used.

### CVE-2026-136549

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-25T06:17:15.597 |

A security flaw has been discovered in Tenda RX3 16.03.13.11_multi. The impacted element is the function formSetSafeWanWebMan of the file /goform/SetRemoteWebCfg. The manipulation of the argument remoteIp results in command injection. The attack can be executed remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-136548

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-25T06:17:13.967 |

A vulnerability was identified in Tenda RX3 16.03.13.11. The affected element is an unknown function of the file /bin/auto_discover of the component GBK-to-UTF-8 Conversion. The manipulation of the argument Hostname leads to stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit is publicly available and might be used.

### CVE-2026-136547

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-25T05:18:35.270 |

A vulnerability was determined in Tenda RX3 16.03.13.11_multi. Impacted is the function R7WebsSecurityHandler of the component httpd. Executing a manipulation can lead to improper authentication. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-136136

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-25T00:17:10.560 |

A vulnerability was identified in Netis WF2409E up to 20261026. Affected by this issue is some unknown functionality of the file /cgi-bin/skk_set.cgi of the component CGI Interface. The manipulation of the argument app/password/new_pwd_confirm/passwd_set/mode_name/wl_link leads to improper authentication. The attack may be initiated remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-132669

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-352` |
| Published | 2026-11-24T23:17:21.517 |

Improper Access Control vulnerability in Wikimedia Foundation MediaWiki - EditAccount Extension.

### CVE-2026-123215

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T20:18:45.900 |

Copeland XWEB Pro contains a missing authentication vulnerability. Fixed in 1.16.1.

### CVE-2026-136411

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36` |
| Published | 2026-11-24T19:18:17.003 |

BusyBox through 1.38.0 contains an absolute path traversal vulnerability in tftpd that allows unauthenticated remote attackers to access files outside any intended directory when started without a DIR argument. Attackers can send RRQ or WRQ packets with file names beginning with '/' to read sensitive files like /etc/shadow or overwrite files, typically as root.

### CVE-2026-136404

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-24T19:18:16.040 |

ntop n2n supernode 3.0 through 3.1.1 contains a stack-based buffer overflow vulnerability that allows remote unauthenticated attackers to leak memory and execute code by sending an untrusted 16-bit auth token_size in REGISTER_SUPER_NAK datagrams. Attackers can register an edge in a chosen community, then send an oversized token_size to leak stack canaries and pointers, overwrite the return address, or crash the supernode.

### CVE-2026-135797

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T19:18:14.630 |

A vulnerability was identified in Volans NGFW Next-Generation Firewall r5.1. Impacted is the function exec of the file sslvpn/sslvpn_client.php of the component SSLVPN Client. Such manipulation of the argument img leads to os command injection. The attack can be executed remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-135792

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T18:19:03.150 |

A vulnerability has been found in Panabit Smart Application Gateway TANGr7p10. This issue affects the function send_email_authcode of the file user.cgi of the component Email Auth Code Sender. Such manipulation of the argument Username leads to os command injection. The attack may be launched remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-125716

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:54.380 |

Adobe Campaign Classic (ACC) is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-135888

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-11-25T13:17:28.230 |

Directory traversal vulnerability in the custom-homepage asset endpoint (/__api__/custom/home/) 
allows remote attackers to read arbitrary files readable by the Package Manager service account via a filesystem path appended to the request URI in Posit Software, PBC Posit Package Manager: 





  *  before 2025.09.6,
  *  2025.12.x before 2025.12.4
  *  2026.04.x before 2026.04.4
  *  2026.05.x before 2026.05.2
  *  2026.06.x before 2026.06.2
  *  2026.08.x before 2026.08.2
  *  2026.09.x before 2026.09.2
  *  2026.10.x before 2026.10.2
  *  2026.11.x before 2026.11.2








NOTE: In the default configuration, where Server.LandingPage is unset, request paths are resolved from the filesystem root, so no directory-traversal sequences are required and exploitation is not detected by scanners that test only for ../ sequences.

### CVE-2026-133335

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-25T11:17:08.870 |

Joomla Extension - virtuemart.net - Unauthenticated local file inclusion leading to remote code execution via controller fallback in VirtueMart extension 4.0.0-4.8.7 - The main controller of the component fell back to including a controller file derived from the request without filtering the name, allowing path traversal to arbitrary local PHP files. Depending on the server setup, for example an available pearcmd.php, this could be used to execute code. The issue has been exploited in the wild. Fixed in 4.8.8.

### CVE-2026-134639

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-25T04:17:32.617 |

Webmin through 2.670 contains an insecure default configuration in its Windows setup.bat script that provisions an administrator account with the credentials admin/admin and SSL disabled. Unauthenticated network attackers can log in over plain HTTP on port 10000 with these unchanged credentials to gain full Webmin administrative access.

### CVE-2026-132726

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T23:17:28.767 |

Deserialization of Untrusted Data vulnerability in Wikimedia Foundation MediaWiki - Echo Extension. This vulnerability is associated with program files includes/Model/Event.php. This issue affects MediaWiki - Echo Extension: from 1.43.0 before 1.43.12, from 1.45.0 before 1.45.7, from 1.46.0 before 1.46.3, 1.47.

### CVE-2026-136412

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T19:18:17.163 |

OpenResty stream-lua-nginx-module before 0.0.20rc4 contains a use-after-free vulnerability that allows remote peers to trigger access to freed memory when a receiveuntil() pattern iterator is garbage-collected while still referenced by the socket. Attackers can interrupt or close the cosocket connection so later reads or socket closure use the stale pattern pointer, crashing or corrupting the nginx worker.

### CVE-2026-127297

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-24T18:18:56.117 |

Joomla! Core - [20261117] - Core - Race condition in formatted text logger in Joomla 3.6.0-5.4.10, 6.0.0-6.2.0 - A race condition in the formatted text logger can recreate a log file without its protective header.

### CVE-2026-126045

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-24T18:18:55.453 |

Joomla! Core - [20261112] - Core - Local file inclusion through language parameter in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - The language request parameter is not validated before it is used to build the path of included language files.

### CVE-2026-123214

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T18:18:52.870 |

Joomla! Core - [20261111] - Core - Missing authentication in web installer in Joomla 4.0.0-5.4.10, 6.0.0-6.2.0 - The web installer remains usable on an installed site as long as the installation folder exists, allowing unauthenticated users to rewrite the configuration.

### CVE-2026-65320

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T15:17:39.113 |

fastcore through 2.2.44 contains a path traversal vulnerability in the fastcore.xtras.untar_dir() archive extraction helper that allows attackers who supply a crafted tar archive to write files outside the intended extraction directory. The internal _unpack() function passes the archive to shutil.unpack_archive() without a tar extraction filter, member path validation, or a containment check, so archive members with absolute paths or ../ traversal sequences are written to arbitrary locations writable by the application process when running on Python versions before 3.14. Applications that extract untrusted archives with untar_dir() can have application files, configuration, or importable code overwritten, which can lead to code execution, data modification, or denial of service.

### CVE-2026-136132

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-647` |
| Published | 2026-11-24T15:17:33.240 |

Pangolin before 1.21.0 contains an authentication bypass vulnerability in isPathAllowed() in server/lib/pathMatch.ts that splits paths on literal slashes without percent-decoding or resolving dot segments. Unauthenticated remote attackers can send paths with encoded slashes and dot segments to match public bypass rules while backends serve protected paths.

### CVE-2026-130411

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T15:17:18.990 |

Deserialization of Untrusted Data vulnerability in woylie flop allows a remote attacker to execute code on the server via a crafted pagination cursor.

Flop.Cursor.decode/2 in lib/flop/cursor.ex decodes the after and before parameters with :erlang.binary_to_term/2 in :safe mode. Its check rejects functions, PIDs, ports and references, but it accepts maps, and therefore structs of any module. Flop passes the decoded values to Ecto as query parameters. A cursor value that nests an Ecto.Query.DynamicExpr struct with a DBConnection.Stream struct as its binding fails the Ecto cast. Ecto then inspects the value for the error message, the Inspect implementation enumerates the stream, and DBConnection calls the module, function and arguments in the :log option of the stream.

This issue affects flop: from 0.8.0 before 0.26.7, from 0.27.0 before 0.27.3, from 0.28.0 before 0.28.1, and from 0.29.0 before 0.29.2.

### CVE-2026-132697

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T23:17:25.073 |

Missing Authorization vulnerability in Wikimedia Foundation MediaWiki - EmailAuth Extension. This vulnerability is associated with program files includes/EmailAuthSecondaryAuthenticationProvider.php. This issue affects MediaWiki - EmailAuth Extension: 1.43, 1.45, 1.46, 1.47.

### CVE-2026-132694

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-24T23:17:24.687 |

Vulnerability in Wikimedia Foundation MediaWiki - OATHAuth Extension. This vulnerability is associated with program files src/Key/WebAuthnKey.php. This issue affects MediaWiki - OATHAuth Extension: from 1.46.0 before 1.46.3, 1.47.

### CVE-2026-133453

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T21:18:18.070 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions 0.7.1 through 0.10.0, a user can add a version under another user's workflow ID and take over its Marketplace listing. An attacker with an account and the target's workflow ID can replace the creator's pending Marketplace submission with their own, so that approval installs the attacker's workflow under the creator's listing. Without reviewer involvement, the attacker can also stop the owner from saving new versions and break runs that name no version. This issue is fixed in version 0.11.0.

### CVE-2026-125718

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T18:18:54.717 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-111546

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T18:18:45.487 |

Dell PowerStore contains an OS Command Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability, potentially leading to privilege escalation to root on the appliance.

### CVE-2026-82322

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-24T17:18:54.850 |

SolarWinds Serv-U is affected by an Insecure Direct Object Reference (IDOR) vulnerability that allows a domain group administrator to bypass restrictions and escalate privileges to the server administrator level. The risk is lower for Windows installations.

### CVE-2026-82321

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-24T17:18:54.720 |

SolarWinds Serv-U was found to be affected by a type 
confusion vulnerability that may allow domain 
administrators to escalate privileges to that of a system 
administrator. The risk is lower for Windows installations.

### CVE-2026-82320

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-24T17:18:54.587 |

SolarWinds Serv-U was found to be affected by another 
type confusion vulnerability that may allow domain 
administrators to escalate privileges to that of a system 
administrator. The risk is lower for Windows installations.

### CVE-2026-82319

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-24T17:18:54.453 |

SolarWinds Serv-U is affected by a time-of-check to time-of-use (TOCTOU) vulnerability. A user with domain 
administrator or higher privileges may allow a user to 
modify protected files outside their home directory. The 
issue can result in read and write access to the 
application files and privilege escalation. The risk is 
lower in Windows installations.

### CVE-2026-82316

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-24T17:18:54.193 |

SolarWinds Serv-U is affected by a Time-of-Check to 
Time-of-Use (TOCTOU) vulnerability. A user with domain 
administrator or higher privileges may be able to access 
or modify protected files outside the intended directory, 
potentially leading to code execution. The risk is lower in
Windows installations.

### CVE-2026-82315

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-24T17:18:54.047 |

SolarWinds Serv-U is affected by another Time-of-Check 
to Time-of-Use (TOCTOU) vulnerability. A user with 
domain administrator or higher privileges may be able to
access or modify protected files outside the intended 
directory, potentially leading to code execution. The risk 
is lower in Windows installations.

### CVE-2026-135389

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-24T17:18:24.040 |

Pion DTLS is a Go implementation of Datagram Transport Layer Security. From 2.1.0 until 3.1.14, a server with a SessionStore saved the session ID and master secret after ClientKeyExchange, before receiving a valid Finished message and before enforcing the configured client-authentication checks. A remote client can omit its Certificate message, send ClientKeyExchange, leave the first handshake unfinished, and then resume the cached session using the master secret it learned during key exchange. The server must use a SessionStore and negotiate a certificate-based cipher suite. The attack can bypass client certificates required through RequireAnyClientCert or RequireAndVerifyClientCert, or a rejecting VerifyConnection callback. WebRTC users are not affected. The abbreviated handshake can allow unauthorized access to application data. The issue is fixed in version 3.1.14.

### CVE-2026-135388

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-24T17:18:23.867 |

Pion DTLS is a Go implementation of Datagram Transport Layer Security. From 2.0.0 until 3.1.13, the implementation selected signature verification based on the certificate public key while deriving the digest from the peer-controlled signature scheme without validating that the scheme, key type, and hash requirements were consistent. The affected verification functions are verifyKeySignature for ServerKeyExchange and verifyCertificateVerify for CertificateVerify. An unauthenticated network attacker who can redirect a DTLS handshake and obtain the genuine peer certificate can submit crafted handshake signatures that are accepted without possession of the certificate private key. This can let the attacker impersonate the peer and compromise the confidentiality and integrity of protected traffic; checking a WebRTC SDP certificate fingerprint does not prevent the attack because the genuine certificate is presented. The issue is fixed in version 3.1.13.

### CVE-2026-123172

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-24T17:18:13.933 |

Solarwinds Serv-U is affected by a privilege escalation vulnerability that, when exploited, could lead to the escalation of privileges to root for Linux installations. The risk is lower for Windows installations.

### CVE-2026-123168

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-24T17:18:13.427 |

SolarWinds Serv-U is affected by an insufficient 
validation vulnerability that, when exploited, could lead 
to privilege escalation into the root user in Linux 
installations. The risk is lower for Windows installations.

### CVE-2026-123167

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-11-24T17:18:13.293 |

SolarWinds Serv-U is affected by a privilege escalation vulnerability that, when exploited, can allow a domain administrator to access files that otherwise would require elevated privileges. The risk is lower for Windows installations.

### CVE-2026-136165

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-24T15:17:34.320 |

Fider before 0.40.0 contains an account takeover vulnerability that allows unauthenticated attackers to sign in as existing users by linking OAuth identities through unverified email matches. Attackers can use a Google account carrying an unverified copy of a victim's email, including a tenant administrator's, to bind their identity via the OAuthToken handler and obtain persistent session access.

### CVE-2026-124286

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-24T15:17:15.807 |

Improper Verification of Cryptographic Signature vulnerability in Erlang OTP ssl (ssl_handshake module) allows an on-path attacker to impersonate any server to a TLS 1.2 or DTLS client.

When a server sends no Certificate message and a ServerKeyExchange without a signature, ssl_handshake:decode_server_key/3 reports the signature algorithm as anon, and ssl_handshake:verify_signature/5 returns true for anon without a public key. The client does not require a certificate for a certificate-authenticated key exchange, so the handshake completes for the ecdhe_rsa, ecdhe_ecdsa, dhe_rsa and dhe_dss key exchanges with a cipher suite the client offered. Certificate path validation, verify_fun and the hostname check do not run, and ssl:connect/3 returns {ok, Socket} with {verify, verify_peer} set. The TLS 1.3 client is not affected.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.14, OTP 28.5.0.9, and OTP 29.0.3, corresponding to ssl from 5.3.4 before 11.2.12.10, 11.6.0.8, and 11.7.3.

### CVE-2026-125723

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:55.303 |

Adobe Campaign Classic (ACC) is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session and causing impact to the availability of the product. Scope is changed.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-123210

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-24T18:18:52.297 |

Joomla! Core - [20261107] - Core - Insufficient file extension checks in com_media rename and copy actions in Joomla 4.0.0-5.4.10, 6.0.0-6.2.0 - The rename and copy actions of the local media adapter only validate the final file extension, allowing files with a blocked extension in their name.

### CVE-2026-133555

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-24T15:17:20.360 |

Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') vulnerability in elixir-ecto db_connection allows an attacker to execute arbitrary code via a forged DBConnection.Stream or DBConnection.PrepareStream struct. The Enumerable implementations of both structs in lib/db_connection.ex run with the options stored in the struct. The :log option accepts a {module, function, arguments} tuple, which DBConnection applies. When code enumerates a forged struct, DBConnection calls the chosen function.

This issue is not exploitable in db_connection alone. It is, in theory, a vulnerability of the downstream component. The root cause is a component that decodes untrusted input with :erlang.binary_to_term/2 and does not restrict which terms the result contains. The :safe option does not reject structs, and these structs contain only plain terms. Structs of other libraries can possibly lead to the same result, so a component that decodes untrusted terms stays at risk independently of db_connection. This record exists because the struct was used in attacks on such components.

This issue affects db_connection: from 1.1.0 before 2.10.3.

### CVE-2026-135959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T11:17:11.457 |

Cross-Site Request Forgery (CSRF) vulnerability in Paul Shield Security wp-simple-firewall allows Cross Site Request Forgery.This issue affects Shield Security: from n/a through 22.3.4.

### CVE-2026-135937

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T11:17:11.000 |

Cross-Site Request Forgery (CSRF) vulnerability in Groundhogg Groundhogg groundhogg allows Cross Site Request Forgery.This issue affects Groundhogg: from n/a through 4.11.

### CVE-2026-135932

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T11:17:10.687 |

Cross-Site Request Forgery (CSRF) vulnerability in WP ManageNinja LLC FluentBoards fluent-boards allows Cross Site Request Forgery.This issue affects FluentBoards: from n/a through 2.3.0.

### CVE-2026-135840

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T09:17:20.087 |

Cross-Site Request Forgery (CSRF) vulnerability in Arraytics Timetics timetics allows Cross Site Request Forgery.This issue affects Timetics: from n/a through 1.0.67.

### CVE-2026-135049

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T09:17:19.763 |

Cross-Site Request Forgery (CSRF) vulnerability in Brainstorm Force Presto Player presto-player allows Cross Site Request Forgery.This issue affects Presto Player: from n/a through 4.5.6.

### CVE-2026-135040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T09:17:19.450 |

Cross-Site Request Forgery (CSRF) vulnerability in Themefic Hydra Booking hydra-booking allows Cross Site Request Forgery.This issue affects Hydra Booking: from n/a through 1.2.11.

### CVE-2026-135008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T09:17:17.787 |

Cross-Site Request Forgery (CSRF) vulnerability in Tainacan Community Tainacan tainacan allows Cross Site Request Forgery.This issue affects Tainacan: from n/a through 1.4.1.

### CVE-2026-134706

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T09:17:12.917 |

Cross-Site Request Forgery (CSRF) vulnerability in Soroseo Soro &#8211; SEO Autopilot &amp; AI Content Writer soro-seo allows Cross Site Request Forgery.This issue affects Soro &#8211; SEO Autopilot &amp; AI Content Writer: from n/a through 1.4.3.

### CVE-2026-134942

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T08:16:45.363 |

Cross-Site Request Forgery (CSRF) vulnerability in 10up ElasticPress elasticpress allows Cross Site Request Forgery.This issue affects ElasticPress: from n/a through 5.3.5.

### CVE-2026-134478

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T08:16:45.200 |

Cross-Site Request Forgery (CSRF) vulnerability in WP ManageNinja LLC Fluent CRM fluent-crm allows Cross Site Request Forgery.This issue affects Fluent CRM: from n/a through 3.3.1.

### CVE-2026-134476

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T08:16:45.043 |

Cross-Site Request Forgery (CSRF) vulnerability in WP ManageNinja LLC Fluent Support fluent-support allows Cross Site Request Forgery.This issue affects Fluent Support: from n/a through 2.5.0.

### CVE-2026-134475

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T08:16:44.887 |

Cross-Site Request Forgery (CSRF) vulnerability in WPManageNinja FluentCart fluent-cart allows Cross Site Request Forgery.This issue affects FluentCart: from n/a through 2.3.2.

### CVE-2026-134473

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-25T08:16:43.590 |

Cross-Site Request Forgery (CSRF) vulnerability in WP ManageNinja LLC WP Social Ninja wp-social-reviews allows Cross Site Request Forgery.This issue affects WP Social Ninja: from n/a through 4.5.0.

### CVE-2026-136626

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-25T03:17:48.997 |

SRS 4.0.0 before 6.0.194, 7.0.0 before 7.0.214, and 8.0.0 before 8.0.73 contains a heap-based buffer overflow in SrsRtcpCommon::decode and SrsRtcpTWCC::decode that lets remote WebRTC peers write past the fixed 1500-byte payload_ array. Unauthenticated attackers opening a WHIP or WHEP session can send oversized BYE, APP, unknown-type or TWCC RTCP packets to overwrite up to 64 KB of heap memory, crashing the server.

### CVE-2026-135046

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-24T20:18:52.033 |

Cross-Site Request Forgery (CSRF) vulnerability in Rymera Web Co Store Exporter woocommerce-exporter allows Cross Site Request Forgery.This issue affects Store Exporter: from n/a through 2.8.2.

### CVE-2026-134986

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-24T19:18:11.420 |

Cross-Site Request Forgery (CSRF) vulnerability in Brainstorm Force SureCart surecart allows Cross Site Request Forgery.This issue affects SureCart: from n/a through 4.13.1.

### CVE-2026-134716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-24T19:18:11.040 |

Cross-Site Request Forgery (CSRF) vulnerability in Mahmudul Hasan Arif Ninja Charts ninja-charts allows Cross Site Request Forgery.This issue affects Ninja Charts: from n/a through 3.5.0.

### CVE-2026-129959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T19:18:08.400 |

When sftpEnabled=true (the default configuration in etc/org.apache.karaf.shell.cfg), the SSH server exposes the karaf.base directory tree through the MINA SSHD SFTP subsystem and SCP command factory without verifying the authenticated user's roles beyond the initial sshRole login check. Consequently, an authenticated user with only low-privileged roles (such as viewer and ssh) can read sensitive configuration and key files (including etc/users.properties and etc/host.key) or write arbitrary bundles/configurations into monitored directories (such as deploy/ or etc/), leading to privilege escalation and arbitrary code execution.


Apache Karaf 4.4.13 and 4.5.0 introduce the sftpRole configuration property in org.apache.karaf.shell (defaulting to admin) and enforce role-based access control on SFTP subsystem creation, SCP command execution, and virtual filesystem access.

Mitigation / WorkaroundUsers are recommended to upgrade to Apache Karaf 4.4.13 or 4.5.0.




On earlier versions where SFTP/SCP access is not required, set sftpEnabled=false in etc/org.apache.karaf.shell.cfg and restart the SSH server bundle (or Karaf instance).

### CVE-2026-121756

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-24T18:18:51.650 |

Parallels Desktop CSHAShellExt Improper Access Control Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Parallels Desktop. An attacker must first obtain the ability to execute low-privileged code on the target guest system in order to exploit this vulnerability.

The specific flaw exists within the CSHAShellExt component. The issue results from improper access control. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of the hypervisor. Was ZDI-CAN-30030.

### CVE-2026-116445

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T18:18:47.277 |

Dell PowerStore SDNAS contains a local privilege-escalation vulnerability that could allow a low-privileged attacker to execute code in the kernel on the NAS node.

### CVE-2026-134959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-24T17:18:17.450 |

Cross-Site Request Forgery (CSRF) vulnerability in Webdeclic WPMasterToolKit wpmastertoolkit allows Cross Site Request Forgery.This issue affects WPMasterToolKit: from n/a through 2.26.1.

### CVE-2026-130808

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T17:18:15.310 |

In Apache Karaf, the default command ACL configuration for the feature scope (etc/org.apache.karaf.command.acl.feature.cfg, defined in assemblies/features/standard/src/main/feature/feature.xml and the child-instance template instance/src/main/resources/org/apache/karaf/instance/resources/etc/org.apache.karaf.command.acl.feature.cfg) restricts feature:install, feature:uninstall, feature:start, and feature:stop to users with the admin role, while leaving feature:requirement-add and feature:requirement-remove without ACL entries.


Because Karaf's command guard (SecuredSessionFactoryImpl) allows commands with no matching ACL rule (NO_MATCH) to execute, an authenticated SSH user holding only the ssh and viewer roles can execute feature:requirement-add bundle:<uri> (or feature:<name>). RequirementAdd forwards the requirement directly to FeatureService.addRequirements(), causing the resolver to download, install, and start an arbitrary bundle with the Karaf JVM process's full authority, bypassing the admin-only restrictions on feature:install and bundle:install. Similarly, feature:requirement-remove allows removing provisioning requirements and uninstalling features/bundles.

MitigationUsers are recommended to upgrade to Apache Karaf 4.4.13 or 4.5.0.




For existing deployments or upgrades that preserve existing files in etc/, add the following rules to etc/org.apache.karaf.command.acl.feature.cfg (and any child instance etc/org.apache.karaf.command.acl.feature.cfg files):




requirement-add = admin 

requirement-remove = admin

### CVE-2026-124615

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-24T17:18:14.293 |

The shell command ACL for the feature scope (etc/org.apache.karaf.command.acl.feature.cfg) restricts feature:install, feature:uninstall, feature:start and feature:stop to the admin role, but had no entry for feature:requirement-add or feature:requirement-remove.

The provisioning resolver turns a requirement into the same install/start (or uninstall) action as feature:install / feature:uninstall: a bundle: requirement causes an arbitrary bundle to be downloaded and started, and a feature: requirement installs that feature. Because the two commands had no ACL, a user authenticated with only the viewer (and ssh) role could invoke them and cause Apache Karaf to download, install and start an attacker-chosen bundle, which then runs with the full authority of the Karaf process — thereby bypassing the admin-only authorization enforced on feature:install and bundle:install.

This is the same class of issue as the feature:repo-add -i / feature:repo-remove -u bypass, on sibling commands not covered by that earlier fix.Mitigation:Upgrade to Apache Karaf 4.4.12 or 4.5.0 (or later), which restrict feature:requirement-add and feature:requirement-remove to the admin role.

As an interim workaround on affected versions, add the following two lines to etc/org.apache.karaf.command.acl.feature.cfg; the change is picked up at runtime without a restart:

requirement-add = admin

requirement-remove = admin

### CVE-2026-136158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T15:17:33.913 |

In Valkey JSON 1.0.0 through 1.0.2, a recursive JSONPath expression such as $..* returns both an array and elements nested inside it. The size-changing mutators (JSON.ARRAPPEND, JSON.ARRINSERT, JSON.ARRPOP, JSON.ARRTRIM and JSON.CLEAR) process the ancestor first, which can reallocate its element buffer and free the old storage while the descendant entries in the result set still point into it; the module then writes through those dangling pointers. An authenticated user who can run these commands can use this to reliably crash the server, and it has been developed into remote code execution as the user the server runs as. Servers that do not load the JSON module, including through valkey-bundle, are not affected.

### CVE-2026-136156

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-11-24T15:17:33.677 |

In Valkey before 7.2.15, 8.0.x before 8.0.12, 8.1.x before 8.1.11, 9.0.x before 9.0.7, 9.1.x before 9.1.3 and 9.2.0-rc1, running in cluster mode, clusterCreatePublishMsgBlock computes the length of the cluster bus message for a PUBLISH or SPUBLISH as a size_t but passes it to createClusterMsgSendBlock as a uint32_t. When the channel and message together exceed 4 GiB, the length is truncated, a buffer far smaller than the message is allocated, and the full channel and message are then copied into it. An authenticated user who can publish, for example by building the arguments in a script, can overflow the heap with attacker-controlled bytes. This reliably crashes the server and may lead to remote code execution. Servers that do not run in cluster mode are not affected.

### CVE-2026-136155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T15:17:33.553 |

In Valkey 9.1.0 and 9.1.1, the Lua script debugger builds its command table once and caches it with a pointer to the Lua interpreter state that was current at the time. SCRIPT FLUSH ASYNC recreates the scripting engine and frees the previous interpreter state without invalidating that cache, so the next debugger command dereferences freed memory. An authenticated user who can run scripting commands can use this to reliably crash the server, and by reclaiming the freed heap chunk with attacker-controlled bytes can escalate it to control of an indirect call, which may lead to remote code execution. The fix also addresses a second use-after-free in ldbLogStackValue. Valkey 8.0.x and 8.1.x use the previous debugger and are not affected.

### CVE-2026-134791

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-25T10:17:14.550 |

Since Symfony 7.2, expressions can contain comments. The lexer used a regular expression to find the end of a comment. When a /* was never closed, this regular expression scanned the rest of the expression, and the lexer then went on with the next character. So each /* scanned the rest of the expression again. Linting 192 KB of /*  took 9 to 11 seconds, and 96 KB took 34 seconds without PCRE JIT.

The lexer runs before the parser and its nesting limit. Any code that lints or parses untrusted expressions is affected, including the ExpressionSyntax validation constraint. A Length constraint on the same value doesn't help, since the validator runs both constraints.

The lexer now uses strpos() to find the end of a comment, and a comment that is never closed throws a SyntaxError. Such expressions were already invalid. Lexing takes linear time again.

### CVE-2026-133761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-770` |
| Published | 2026-11-25T10:17:14.087 |

CsvEncoder::decode() splits each header cell on the key separator, . by default, and nests the decoded rows one level per separator, with no limit. PHP frees nested arrays recursively, so freeing data that is nested deeply enough overflows the C stack and crashes the process. With a stack of 8 MB, a CSV body of 448 KB is enough.

Each row also builds all the levels of its headers again. With a deep header, a CSV body of 2 KB made of short rows allocates more than 128 MB. A body of 1 MB keeps the CPU busy for 10 seconds or more.

Any code that decodes untrusted CSV with the Serializer is affected. From Symfony 7.4.0, this included every #[MapRequestPayload] argument that doesn't restrict acceptFormat, until 7.4.23 and 8.1.11 stopped decoding CSV payloads by default.

CSV headers can now be nested up to 512 levels, the default depth of json_decode(). Decoding also stops when the rows go through more than 16 header levels, or create more than 4 arrays, per byte of data. A header row of up to 5 levels always fits, whatever the rows contain. Beyond these limits, decode() throws a NotEncodableValueException, which #[MapRequestPayload] turns into a 400 response.

### CVE-2026-133760

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-25T10:17:13.940 |

The fix for CVE-2026-109449 made the expression parser check the nesting level of long expressions. This check exists since Symfony 5.4.54, 6.4.48, 7.4.21 and 8.1.9. The parser builds a ?: b with the node of a used twice, and the check walked every path to every node. With nested short ternaries, the number of paths doubles at each level, so an expression of 256 bytes never finished parsing.

The expression needs no variable and no function. Any code that parses or lints untrusted expressions is affected, including the ExpressionSyntax validation constraint. evaluate() and compile() parse the expression first, so they hang too.

The nesting check now skips the nodes it already checked, so it takes linear time again. evaluate(), compile() and the messages of runtime errors now use the node of a once, so a is evaluated once, as in PHP.

### CVE-2026-118898

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-25T05:18:27.293 |

Deserialization of Untrusted Data vulnerability in lasp-lang partisan allows an unauthenticated remote attacker to abort the Erlang VM of a node via Excessive Allocation. partisan_peer_service_server:handle_info/2 decodes every frame that arrives on the peer listener with binary_to_term/1, without the safe option, before handle_inbound/2 interprets the message and before any peer authentication takes place. TLS is off by default and the listener accepts connections from any host, so one frame that names more atoms than the atom table holds aborts the VM. partisan_peer_service_client:handle_info/2 decodes frames from the server side of a connection the same way.

The decode also materializes funs, ports and references the frame encodes and inflates compressed terms. The demonstrated impact is denial of service. partisan does not invoke decoded funs, so code execution was not shown.

This issue affects partisan: from 3.0.0 before 6.4.0.

### CVE-2026-136627

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-25T03:17:49.177 |

SRS 4.0.0 before 6.0.194, 7.0.0 before 7.0.214, and 8.0.0 before 8.0.73 contains a reachable assertion in RTCP decoding that lets remote WebRTC peers crash the server. Attackers opening an unauthenticated WHIP or WHEP session can send an 8-byte RTCP packet with undersized length, triggering srs_assert aborts that stop every stream.

### CVE-2026-133462

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-441;CWE-863` |
| Published | 2026-11-25T00:17:10.413 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. From 0.6.49 before 0.11.0, the MCPToolBlock auto-lookup allows a shared agent's author to use the MCP credentials of the user who runs it. Anyone who ran a shared agent containing an MCPToolBlock node, and had already connected the MCP server URL that the node names, had that connection used for any read, write, or delete the server exposes, with the result sent to a host chosen by the author. This issue is fixed in version 0.11.0.

### CVE-2026-133460

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-24T23:17:31.360 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.11.0, public webhook endpoints woould buffer request bodies in full before verifying them. Anyone with network access to the API ccould exhaust the memory of platform API workers without an account or a valid signature. The chat-bot webhook routes were reachable only where that chat platform was configured. This issue is fixed in version 0.11.0.

### CVE-2026-132736

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-200` |
| Published | 2026-11-24T23:17:30.037 |

Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Wikimedia Foundation MediaWiki. This vulnerability is associated with program files includes/Rest/Handler.php, includes/Rest/Handler/ParsoidHandler.php, includes/Rest/Module/Module.php, includes/Rest/Validator/UnsupportedContentTypeBodyValidator.php. This issue affects MediaWiki: from 1.43.0 before 1.43.12, from 1.45.0 before 1.45.7, from 1.46.0 before 1.46.3, 1.47.

### CVE-2026-132734

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-24T23:17:29.790 |

Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Wikimedia Foundation MediaWiki - ExternalData Extension. This vulnerability is associated with program files includes/connectors/EDConnectorDb.php, includes/connectors/EDConnectorLdap.php, includes/presets/Test.php, includes/presets/docker-compose.yml. This issue affects MediaWiki - ExternalData Extension: 1.43, 1.45, 1.46, 1.47.

### CVE-2026-132724

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-24T23:17:28.520 |

Vulnerability in Wikimedia Foundation MediaWiki - EasyTimeline Extension. This vulnerability is associated with program files scripts/EasyTimeline.pl. This issue affects MediaWiki - EasyTimeline Extension: 1.43, 1.45, 1.46, 1.47.

### CVE-2026-132710

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-24T23:17:26.637 |

Exposure of Sensitive Information to an Unauthorized Actor vulnerability in Wikimedia Foundation MediaWiki. This vulnerability is associated with program files includes/Rest/Handler/ParsoidHandler.php. This issue affects MediaWiki: from 1.46.0 before 1.46.3, 1.47.

### CVE-2026-132670

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-24T23:17:21.650 |

Improper Access Control vulnerability in Wikimedia Foundation MediaWiki. This vulnerability is associated with program files includes/Api/ApiQueryRevisionsBase.php. This issue affects MediaWiki: from 1.43.0 before 1.43.12, from 1.45.0 before 1.45.7, from 1.46.0 before 1.46.3, 1.47.

### CVE-2026-136522

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T21:18:20.433 |

CubeWP Forms before 1.1.13 contains an unauthenticated stored cross-site scripting vulnerability that allows attackers to inject malicious JavaScript by submitting unregistered field names through the public REST route cubewp-custom-form/v1/submit/, which bypasses its own nonce check and saves unsanitized values due to a missing default case in the sanitizer, later rendered unescaped on the admin Leads detail page. Attackers can send a single crafted GET request containing a script payload in a custom form field to execute arbitrary JavaScript in an administrator's wp-admin session when the lead is viewed, enabling full site takeover such as creating a new administrator account.

### CVE-2026-136455

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-24T20:18:53.817 |

borg-ui before 2.4.1 contains a privilege escalation vulnerability that allows a repository-scoped operator to escalate to full administrator by exploiting an unrestricted source_directories field in the backup-plan API that lacks path allow-listing. Attackers can configure a backup plan to archive the application's data directory, download the resulting archive to extract the static HS256 .secret_key, and use it to forge a JWT with sub":"admin" to access admin-only endpoints like GET /api/auth/users, achieving full application takeover without admin credentials, XSS, or CSRF.

### CVE-2026-126695

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259` |
| Published | 2026-11-24T20:18:48.790 |

Use of hard-coded password vulnerability in Tibco Control Plane and Tibco Control Tower.

This issue affects Control Plane: 1.22.0; Control Tower: 1.22.0.

### CVE-2026-123253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-24T19:18:03.600 |

Adobe Experience Manager is affected by an Improper Neutralization of Special Elements Used in a Template Engine vulnerability that could result in a Security feature bypass. An attacker with high privileges could leverage this vulnerability to bypass security measures and gain unauthorized read and write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-121357

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T19:17:52.083 |

Adobe Experience Manager is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-119579

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T19:17:51.507 |

Adobe Experience Manager is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-136189

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-24T17:18:47.103 |

Schmitech ORBIT before 2.17.15 contains an improper authorization vulnerability in the permission_or_api_key dependency that allows any valid API key to access /admin management routes. Attackers holding a chat inference API key can read other keys in plaintext, rewrite config.yaml, and manage adapters and prompts to take over server administration.

### CVE-2026-136187

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T17:18:46.707 |

Spug 4.0.0 before 4.1.1 contains an OS command injection vulnerability that allows any authenticated user to execute commands by supplying a crafted git URL to the /api/credential/check/ endpoint. Attackers can inject shell metacharacters into the data field passed to git ls-remote with shell=True, executing commands as the Spug service account, which is root in Docker deployments.

### CVE-2026-136183

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T17:18:46.013 |

Mercur @mercurjs/core before 2.3.2 contains a missing object-level authorization vulnerability that allows authenticated vendors to access other sellers by substituting the :id path parameter. Attackers can read payment and tax details, overwrite profiles and addresses, and invite, remove, or re-role team members to take over another vendor's store.

### CVE-2026-136181

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T17:18:45.667 |

cnpmcore 3.46.0 before 3.84.3 and 4.0.0 before 4.37.3 contains an information disclosure vulnerability that allows unauthenticated attackers to obtain upstream registry authTokens via the GET /-/registry endpoints lacking AdminAccess middleware. Attackers can request /-/registry or /-/registry/:id and replay the leaked authToken as a Bearer credential to enumerate, download, or publish packages upstream.

### CVE-2026-135392

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-24T17:18:24.517 |

Pion DTLS is a Go implementation of Datagram Transport Layer Security. From 2.1.4 until 3.1.13, the handshake cache copied and retained submitted messages without deduplicating entries, limiting the entry count, limiting total payload bytes, or stopping new insertions after handshake completion. A remote peer able to deliver suitable DTLS traffic can grow the cache through incoming handshake messages and repeated caching of outgoing retransmissions for the lifetime of the connection. The fragment reassembly buffer's separate size limit does not prevent this issue because completed messages are retained in the append-only handshake cache. Unbounded cache growth can exhaust application memory and cause a denial of service. The issue is fixed in version 3.1.13.

### CVE-2026-133002

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-24T16:17:55.497 |

The DINA-community icsnpp-mms 1.0.0 plugin for Zeek does not release partially decoded Manufacturing Message Specification (MMS) protocol data units when ASN.1 Basic Encoding Rules (BER) decoding fails. An unauthenticated attacker who can send traffic observed by a Zeek worker with the MMS analyzer enabled can cause memory exhaustion by repeatedly sending malformed MMS traffic. This can terminate the worker and interrupt network monitoring.

### CVE-2026-132887

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-11-24T16:17:55.317 |

The DINA-community icsnpp-acse 1.0.0 plugin for Zeek does not release partially decoded ACSE protocol data units when ASN.1 Basic Encoding Rules (BER) decoding fails. An unauthenticated attacker who can send traffic observed by a Zeek worker with the ACSE analyzer enabled can cause memory exhaustion by repeatedly sending malformed ACSE traffic. This can terminate the worker and interrupt network monitoring.

### CVE-2026-132157

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-24T16:17:54.920 |

The OSI Presentation Protocol analyzer in DINA-community's icsnpp-pres 1.0.0 plugin for Zeek uses an incompatible ASN.1 descriptor when decoding resynchronization acknowledgments. An unauthenticated attacker who can send crafted traffic observed by the analyzer can cause a type confusion that crashes the Zeek worker, resulting in a denial of service for traffic monitoring on that worker.

### CVE-2026-136168

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-24T15:17:34.803 |

RedVector before 8.1.0 contains a hard-coded credentials vulnerability that allows unauthenticated attackers to execute commands by supplying the default redvector-dev-token bearer token. Attackers can call /api/python/execute or /api/process/execute-async to run Python scripts and commands as the server user, even via malicious web pages abusing permissive CORS against loopback instances.

### CVE-2026-136159

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-24T15:17:34.037 |

TypiCMS Core before 17.0.46 contains an insufficiently protected credentials vulnerability that allows authenticated users with "read users" permission to view plaintext api_token values for all users, including superusers, via the GET /api/users endpoint. Attackers can steal a superuser's non-expiring, non-rotatable api_token from the JSON response and use it to gain full superuser API access, enabling creation and deletion of users, roles, and all content.

### CVE-2026-116225

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-1284` |
| Published | 2026-11-24T15:17:11.817 |

Improper Validation of Specified Quantity in Input vulnerability in the BER decoder in Erlang/OTP snmp allows an unauthenticated remote attacker to exhaust CPU via an SNMP message that contains an OBJECT IDENTIFIER with a very long sub-identifier.

snmp_pdus:dec_oid_element/3 does not limit the number of base-128 octets in a sub-identifier, and snmp_pdus:dec_oid_elements/3 does not limit the number of sub-identifiers, so one sub-identifier can span the whole datagram. When the value exceeds the native integer size, each further octet copies a growing bignum, and decoding time grows quadratically with the sub-identifier length. The agent and the manager decode OIDs before they check community strings or SNMPv3 credentials, inside the single network interface process (snmpa_net_if or snmpm_net_if). That process does not read the next datagram until decoding completes.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.20, OTP 28.5.0.9, and OTP 29.1.3, corresponding to snmp from 4.25.1 before 5.18.2.3, 5.20.2.4, and 5.20.7. Whether OTP before OTP 17.0, corresponding to snmp before 4.25.1, is affected is unknown.

### CVE-2026-135796

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T19:18:14.430 |

A vulnerability was determined in Volans NGFW Next-Generation Firewall r5.1. This issue affects the function exec/system of the file modules/assets/port_serve_scan.mds of the component Web Management UI. This manipulation of the argument task_name/where/path causes os command injection. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-135794

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-11-24T19:18:14.237 |

A vulnerability was determined in Panabit Smart Application Gateway TANGr7p10. The affected element is the function add_crontab of the file admin/cgi-bin/sac/ajax_sac_crontab of the component SAC. Executing a manipulation of the argument cmd can lead to code injection. The attack can be executed remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-135793

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T18:19:03.360 |

A vulnerability was found in Panabit Smart Application Gateway TANGr7p10. Impacted is the function import_upgrde/upload_modkey of the file /admin/cgi-bin/sac/ajax_sac_ap of the component CGI Backend. Performing a manipulation of the argument file/filename results in path traversal. Remote exploitation of the attack is possible. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-135791

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T18:19:02.880 |

A flaw has been found in Panabit Smart Application Gateway TANGr7p10. This vulnerability affects the function edit_data_pie of the file /cgi-bin/flowcontrol/ajax_data_pie. This manipulation of the argument Name causes os command injection. The attack may be initiated remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-127303

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.917 |

Joomla! Core - [20261123] - Core - XSS in com_associations modal in Joomla 3.7.0-5.4.10 - Inadequate escaping of the forced item type request parameter leads to a reflected XSS vulnerability in the associations modal.

### CVE-2026-127302

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.787 |

Joomla! Core - [20261122] - Core - XSS in com_associations association view in Joomla 3.7.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the item type request parameter leads to a reflected XSS vulnerability in the association edit view.

### CVE-2026-120674

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:50.900 |

Joomla! Core - [20261104] - Core - XSS in com_finder search view in Joomla 2.5.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the search filter values leads to a reflected XSS vulnerability in the smart search view.

### CVE-2026-136190

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T17:18:47.263 |

RayLabsHQ gitea-mirror before 3.38.1 contains an authorization bypass vulnerability in the /api/sso/providers handlers that allows any authenticated user to access other users' SSO providers without ownership checks. Attackers can read every OIDC client secret in clear text and overwrite or delete providers, redirecting authorization and token endpoints to attacker-controlled servers.

### CVE-2026-135790

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T17:18:43.717 |

A vulnerability was detected in Panabit Smart Application Gateway TANGr7p10. This affects an unknown part of the file /cgi-bin/dashboard/ajax_chart_dump. The manipulation of the argument isntmeye results in os command injection. The attack can be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-135788

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T17:18:43.250 |

A weakness has been identified in D-Link DIR-X1860 4.5.2. Affected by this vulnerability is an unknown functionality of the file /usr/sbin/anweb. Executing a manipulation can lead to os command injection. It is possible to launch the attack remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-136552

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-25T07:17:18.643 |

A security vulnerability has been detected in Tenda RX3 16.03.13.11_multi. This impacts the function formSetIPv6status of the file /goform/setIPv6Status of the component multiWAN. Such manipulation of the argument remoteIP leads to command injection. The attack may be performed from remote. The exploit has been disclosed publicly and may be used.

### CVE-2026-136550

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-25T06:17:15.807 |

A weakness has been identified in Tenda RX3 16.03.13.11_multi. This affects the function fromAdvSetMacMtuWan of the file /goform/AdvSetMacMtuWan. This manipulation of the argument mac causes command injection. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-136629

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-25T03:17:49.530 |

Nektos act 0.2.92 before 0.2.95 contains an argument injection vulnerability in readProjectArgsFile and projectFlag that allows malicious repositories to bypass the untrusted project .actrc flag allowlist. Attackers can commit a crafted .actrc smuggling disallowed flags like -P self-hosted or --privileged to run workflow steps on the developer's host.

### CVE-2026-123340

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T20:18:47.960 |

Copeland XWEB Pro contains an OS command injection vulnerability that allows a remote, authenticated attacker to execute arbitrary commands as the root user. Fixed in 1.16.1.

### CVE-2026-123216

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T20:18:46.097 |

Copeland XWEB Pro contains an OS command injection vulnerability that allows a remote, authenticated attacker to execute arbitrary commands as the root user. Fixed in 1.16.1.

### CVE-2026-134066

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-24T19:18:10.293 |

Improper neutralization of special elements in data query logic in the query construction of AWS Graph Explorer before 3.2.1 might allow an authenticated remote user with write access to the connected graph database to access and modify data in that database with Graph Explorer's privileges via a crafted property key or label that is used when another user performs a search.



To remediate this issue, users should upgrade to Graph Explorer version 3.2.1 or later.

### CVE-2026-135789

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-24T17:18:43.480 |

A security vulnerability has been detected in D-Link R95 101B06. Affected by this issue is the function GetBluetoothAdapterSettings/GetBluetoothBloodPressure/GetBluetoothDeviceList/GetBluetoothScanDeviceList/SetBluetoothAdapterSettings/SetBluetoothUnpairDevice/SetTriggerBluetoothScan/SetBluetoothPairDevice of the file /bin/ssi of the component DHMAPI SOAP Handler. The manipulation of the argument inner_xml leads to os command injection. The attack can be initiated remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-136167

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T15:17:34.643 |

vedo through 2026.6.3 contains an insecure deserialization vulnerability that allows attackers to execute code by supplying crafted .npy or .npz files loaded with allow_pickle=True. Attackers can embed an object with a malicious __reduce__ method in mesh, assembly, scene or font files to run code with the victim's privileges when opened.

### CVE-2026-136160

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T15:17:34.177 |

Pyro through 1.9.2 contains an insecure deserialization vulnerability in ParamStoreDict.load() that calls torch.load with weights_only=False, unpickling arbitrary Python objects. Attackers can trick users into loading a crafted parameter file defining __reduce__ to execute code with the privileges of the Python process.

### CVE-2026-80367

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-25T14:17:10.410 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Out-of-bounds Write vulnerability. A local attacker could potentially exploit this vulnerability, leading to application instability, denial of service, disclosure of sensitive information, arbitrary memory modification, and potentially execution of attacker-controlled code within the affected process.

### CVE-2026-80361

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T14:17:09.610 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Missing Authentication for Critical Function vulnerability. An attacker with local access to the appliance could potentially exploit this vulnerability, leading to unauthorized access to sensitive information, unauthorized modification of application data, and execution of actions with elevated privileges within the appliance environment.

### CVE-2026-80291

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T13:17:32.240 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Missing Authentication for Critical Function vulnerability. A local attacker could potentially exploit this vulnerability, leading to unauthorized access to sensitive data, modification of critical resources, and disruption of appliance functionality.

### CVE-2026-80287

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T13:17:31.850 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Missing Authentication for Critical Function vulnerability. An attacker with local access could potentially exploit this vulnerability, leading to unauthorized access to system resources, disclosure of sensitive information, modification of protected configurations, and execution of privileged operations.

### CVE-2024-7431

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-25T13:17:23.737 |

In Application Performance Management versions before 9.60 IP4, The application is vulnerable to cross-site scripting wherein the application does not properly validate the input parameters, allowing scripts to be injected and then executed in the context of a user’s browser. This can lead to the attacker stealing sensitive information, impersonating users, or performing actions on their behalf.  Also, the application may also be vulnerable to the below attacks:

• Link Injection – This occurs when an attacker inserts a malicious link into a webpage, often in a way that makes it appear legitimate. When user clicks on the link, they may be directed to a harmful website or prompted to download malicious files.



• Frame Injection – This attack involved embedding a webpage within an invisible frame on another site, User interacts with what appears to be a legitimate site, but their actions are performed on the malicious page, potentially leading to unintended actions or data theft.

### CVE-2024-7430

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T13:17:23.510 |

Application Performance Management 9.60 patch versions before IP4 are affected. This issue seems to be present throughout the application, as several endpoints or functionalities that are restricted to Admin users can be directly accessed by Regular users. The authorization method of the application can be bypassed allowing users to perform unauthorized actions to their role. The application supports different levels of access. The application performs authorization checks to keep users from accessing functionality outside of their role such as create, verify, and/or repair. 




This authorization method can be bypassed. During VA testing, it was found that under the User Reports inside the Applications menu, it is possible to  create links and different reports. However, the creation of custom links, Excel reports, and service reports are restricted to admin users. Hence, it is possible for regular users with the least privileges to directly access these 

pages and the application allows them to further use these restricted functionalities.

### CVE-2026-80283

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T10:17:16.427 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Missing Authentication for Critical Function vulnerability. An attacker with local access could potentially exploit this vulnerability, leading to unauthorized disclosure of sensitive information, unauthorized modification of system resources, and execution of privileged actions that could lead to compromise of the appliance.

### CVE-2026-80273

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T10:17:16.290 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An attacker with local access to the appliance could potentially exploit this vulnerability, leading to arbitrary command execution and privilege escalation, resulting in complete compromise of confidentiality, integrity, and availability of the appliance.

### CVE-2026-80247

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T08:16:46.057 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Missing Authentication for Critical Function vulnerability. An attacker with local access to the appliance could potentially exploit this vulnerability, leading to unauthorized access to sensitive information, modification of protected resources, and execution of privileged operations within the appliance security context, potentially resulting in compromise of confidentiality, integrity, and availability.

### CVE-2026-16663

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T22:18:51.263 |

MCUboot's encrypted serial-recovery path contains an attacker-controlled out-of-bounds stack write in decrypt_region_inplace() in boot/boot_serial/src/boot_serial_encryption.c. The routine decrypts an uploaded encrypted image one flash sector at a time into a sector-sized stack VLA buf[sz], but when the current sector is still inside the image header it sets the destination index to the absolute header size (idx = hdr->ih_hdr_size; at boot/boot_serial/src/boot_serial_encryption.c:156) and then decrypts into &buf[idx]. The correct sibling routine boot/bootutil/src/loader.c:876 uses the sector-relative idx = hdr->ih_hdr_size - abs_off; the serial path is missing the - abs_off term, so for any sector after the first the index runs past the end of the stack buffer.

The ih_hdr_size field is a uint16_t taken verbatim from the uploaded image header. On the second sector onward, when ih_hdr_size exceeds the sector size, &buf[idx] points beyond buf and boot_enc_decrypt() writes attacker-controlled plaintext into adjacent stack frames. The path is reached pre-authentication: bs_upload() calls boot_handle_enc_fw() (boot/boot_serial/src/boot_serial.c:1208) after upload, and the pre-decryption signature gate in decrypt_image_inplace() is compiled out (#if 0 at boot/boot_serial/src/boot_serial_encryption.c:226-233), so the header is never validated before decryption.

A second error in the same window computation affects the first sector. When a sector holds both the end of the header and the start of the TLV area, the decrypt length is clamped to tlv_off - (off + bytes_copied), measured from the start of the sector rather than from idx (boot/boot_serial/src/boot_serial_encryption.c:166). An encrypted image whose header and payload end within the first sector is therefore decrypted for ih_hdr_size bytes more than it should be: into the TLV area and, when the image ends near the end of the sector, past buf. This form needs no oversized header, so even an ordinary small encrypted image can trigger it, and it reaches devices with sectors of up to about 128 KiB rather than only those whose sector is smaller than the 16-bit ih_hdr_size.

Reaching the sink requires a build with MCUBOOT_ENC_IMAGES and serial recovery enabled, and access to the device's serial/USB recovery interface (unauthenticated by design). With the public-key encryption schemes the AES content key is wrapped to the device's public encryption key, so an attacker can author a fully crafted encrypted image — including a malicious ih_hdr_size — without the image-signing private key. The result is a controllable stack memory-corruption inside the bootloader before any signature check, providing a path to code execution in the secure-boot root of trust that bypasses image authentication, as well as a denial-of-service. A 2048-byte out-of-bounds write was reproduced under AddressSanitizer (sz=4096, off=4096, ih_hdr_size=6144).

On releases before v2.0.0 (v1.9.0 and v1.10.0) the destination is a file-scope static uint8_t buf[SOC_FLASH_ERASE_BLK_SZ] in .bss rather than the stack VLA described above — the code then lived in boot/zephyr/single_loader.c, before commit c9fa6088 relocated it to boot/boot_serial/src/boot_serial_encryption.c and changed the buffer's storage class. The out-of-bounds write is equally real and equally pre-authentication on those releases, but it corrupts adjacent static data rather than the stack, so a stack-smashing proof of concept written against a current release will not reproduce as-is there.

### CVE-2026-129389

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:19:00.783 |

Joomla! Core - [20261152] - Core - XSS in module title attributes in Joomla 3.8.3-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the module title in HTML attributes of the wrapper module and several administrator modules leads to a stored XSS vulnerability.

### CVE-2026-129368

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.990 |

Joomla! Core - [20261131] - Core - XSS in com_banners banner name in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving banners and the raw output of the name in custom banner code lead to a stored XSS vulnerability.

### CVE-2026-129367

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.857 |

Joomla! Core - [20261130] - Core - XSS in com_scheduler task title in Joomla 4.1.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving scheduled tasks leads to a stored XSS vulnerability in the task title.

### CVE-2026-129366

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.720 |

Joomla! Core - [20261129] - Core - XSS in module titles in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving modules and inadequate escaping of the module title in module chromes lead to a stored XSS vulnerability.

### CVE-2026-129364

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.443 |

Joomla! Core - [20261127] - Core - XSS in com_modules module positions in Joomla 2.5.0-5.4.10, 6.0.0-6.2.0 - Inadequate filtering of the module position in the batch process and inadequate escaping in the module list lead to a stored XSS vulnerability.

### CVE-2026-129363

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.313 |

Joomla! Core - [20261126] - Core - XSS in administrator menu module in Joomla 3.8.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of menu item links in the administrator menu module leads to a stored XSS vulnerability.

### CVE-2026-129362

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.183 |

Joomla! Core - [20261125] - Core - XSS in note custom field in Joomla 6.0.0-6.2.0 - Inadequate filtering and escaping of the heading, class and close parameters of the note custom field lead to a stored XSS vulnerability.

### CVE-2026-127304

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.050 |

Joomla! Core - [20261124] - Core - XSS in form field showon attribute in Joomla 3.9.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the showon attribute in form fields leads to a stored XSS vulnerability through custom fields.

### CVE-2026-127301

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.660 |

Joomla! Core - [20261121] - Core - XSS in com_contenthistory version preview in Joomla 3.2.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of field labels in the version preview and comparison leads to a stored XSS vulnerability.

### CVE-2026-127300

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.523 |

Joomla! Core - [20261120] - Core - XSS in com_guidedtours tour and step titles in Joomla 4.3.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving guided tours and inadequate escaping of the titles lead to a stored XSS vulnerability.

### CVE-2026-127299

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.390 |

Joomla! Core - [20261119] - Core - XSS in com_newsfeeds name in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving newsfeeds and inadequate escaping of the feed name lead to a stored XSS vulnerability.

### CVE-2026-127298

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:56.250 |

Joomla! Core - [20261118] - Core - XSS in com_contact name in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - Decoding of HTML entities when saving contacts and inadequate escaping of the contact name lead to a stored XSS vulnerability.

### CVE-2026-82313

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T17:18:53.783 |

SolarWinds Serv-U is affected by a business logic 
vulnerability that may allow access to a higher privileged
account, which can then be used to execute commands 
or code. An account with high privileges and a 
configured SMTP server are required. The risk is lower in 
Windows installations.

### CVE-2026-105609

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352;CWE-362;CWE-488;CWE-601` |
| Published | 2026-11-25T11:17:06.773 |

In Eclipse Che versions 7.61.0 through 7.124.0 three related defects in the SCM-OAuth flow, chain into a Medium-severity finding:



1. Open redirect (CWE-601) — `EmbeddedOAuthAPI.callback()` and the OAuth1 callback issue `307 Temporary Redirect` to whatever URL was carried in the `redirect_after_login` field of the OAuth `state` parameter. The value is fully attacker-controlled and never compared against an allow-list of permitted hosts.



2. Missing CSRF nonce in OAuth `state` (CWE-352) — `OAuthAuthenticator.prepareState()` builds the `state` parameter solely by URL-encoding the original request's query string. No random nonce is bound to the user's session, so an attacker can pre-compute a callback URL carrying _their own_ SCM authorization `code` and have a logged-in victim open it. `callback()` then stores the attacker's SCM token under the victim's Che identity (`personalAccessTokenManager.store(...)`).



3. Mutable field on a `@Singleton` (CWE-362 / CWE-488) — `EmbeddedOAuthAPI` is `@Singleton` but stores the per-request `redirect_after_login` value into the instance field `private String redirectAfterLogin`. Any user's `authenticate()` call overwrites the field for all concurrent users; the `access_denied` error-path of `callback()` then redirects to the _last writer's_ URL.

### CVE-2026-134792

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-25T10:17:14.733 |

When the proxy option isn't set, HttpClient takes the proxy from environment variables like http_proxy or HTTP_PROXY. On web servers, it ignores HTTP_PROXY, because PHP puts the Proxy request header there (the httpoxy issue). On the CLI SAPI, it read HTTP_PROXY from $_SERVER, where PHP also puts the environment.

HTTP workers that run under the CLI SAPI put the headers of each request in $_SERVER too. This is the case of spiral/roadrunner-http, which the RoadRunner runner of php-runtime uses, and of baldinof/roadrunner-bundle and php-pm. A client could then send a Proxy header to choose the proxy of the requests that the application sent while handling its request. That proxy received the full requests to http:// URLs, with their credentials, and could forge the responses. For https:// URLs, it learned the host and port through CONNECT.

NativeHttpClient is affected since Symfony 4.3.0, AmpHttpClient since 5.1.0, and CurlHttpClient since 4.4.40, 5.4.7 and 6.0.7.

On the CLI SAPI, HTTP_PROXY is now read from the environment with $_ENV and getenv(), never from $_SERVER. Other SAPIs still ignore it.

### CVE-2026-134646

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-25T04:17:34.047 |

Webmin through 2.670 contains a cleartext transmission vulnerability in the SMTP service monitor that never issues STARTTLS because get_smtp_status tests an undefined $ssl variable. Passive network attackers can capture AUTH PLAIN credentials sent in plaintext each time a STARTTLS-configured monitor runs, without needing a Webmin login.

### CVE-2026-134644

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T04:17:33.703 |

Webmin through 2.670 contains a path traversal vulnerability in minecraft/minecraft-lib.pl that allows unauthenticated game players to overwrite arbitrary files as root via crafted chat messages. Attackers can send chat messages mimicking logged in lines so the root check_playtime_limits cron job rewrites attacker-chosen files, destroying their contents.

### CVE-2026-134643

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-11-25T04:17:33.530 |

Webmin through 2.670 contains an authentication bypass vulnerability in password_change.cgi that allows unauthenticated attackers to change passwords for accounts with empty stored hashes. When passwd_mode is 2, attackers can POST user, old, new1 and new2 with any old value to set a known password and gain access.

### CVE-2026-134640

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T04:17:32.820 |

Webmin through 2.670 contains an improper certificate validation vulnerability in imap_login in mailboxes/folders-lib.pl that skips certificate verification and hostname checks for IMAP SSL connections. Man-in-the-middle attackers can present any certificate to capture IMAP credentials sent by the System and Server Status IMAP monitor and spoof monitor results.

### CVE-2026-134637

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-25T04:17:32.263 |

Webmin through 2.670 contains a STARTTLS downgrade vulnerability in send_mail in mailboxes/boxes-lib.pl that continues over plaintext when STARTTLS is rejected. Man-in-the-middle attackers can strip or reject STARTTLS to capture configured SMTP AUTH credentials, crackable CRAM-MD5 exchanges, and the content of sent mail.

### CVE-2026-134463

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T04:17:30.330 |

Webmin through 2.670 contains an improper certificate validation vulnerability in switch_smtp_to_ssl in mailboxes/boxes-lib.pl and status/smtp-monitor.pl, which calls Net::SSLeay::connect without certificate verification or a hostname check. Man-in-the-middle attackers can present any certificate when SMTP with SSL or STARTTLS is configured to capture SMTP AUTH credentials and message content.

### CVE-2026-134444

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-25T04:17:29.450 |

Webmin through 2.670 contains a cleartext transmission vulnerability in connect_ldap_db in ldap-server/ldap-server-lib.pl that sends the LDAP root DN password unencrypted when encryption is set to Detect automatically. Passive network attackers observing traffic between Webmin and a remote LDAP server can capture directory root credentials because the connection loop always reaches a plaintext bind attempt.

### CVE-2026-134323

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T04:17:26.970 |

Webmin through 2.670 contains an improper certificate validation vulnerability in generic_ldap_connect in ldap-client-lib.pl that accepts any LDAPS or StartTLS server certificate. Man-in-the-middle attackers can impersonate the LDAP server to capture the bind DN password, often the root DN, and return forged directory data.

### CVE-2026-133438

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-200` |
| Published | 2026-11-24T23:17:31.110 |

Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') vulnerability in Wikimedia Foundation MediaWiki. This vulnerability is associated with program files includes/libs/Http/MultiHttpClient.php, includes/libs/Mime/MimeAnalyzer.php. This issue affects MediaWiki: 1.47.

### CVE-2026-82169

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T17:18:53.513 |

Dell Virtual Storage Integrator for VMware vSphere Web Client, versions prior to 10.12.0.0, contains an OS Command Injection – confirm single CWE vulnerability in Upgrade Service. A low privileged remote attacker could potentially exploit this vulnerability, leading to arbitrary command execution.

### CVE-2026-95533

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-25T11:17:14.123 |

In Eclipse Jetty, the JSON parsing utilities provided by artifact `jetty-util-ajax` are vulnerable to `StackOverflowError` for inputs that have a large recursive structure.

### CVE-2026-133334

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T11:17:08.717 |

Joomla Extension - virtuemart.net - Cross-product paid file download in Download Simple plugin in VirtueMart extension 4.0.0-4.8.0 - The bundled iStraxx Download Simple plugin verified the order secret of a download link against the order item, but not that the requested media belonged to that item. Anyone holding one valid download link could download other files offered for sale. Fixed in 4.8.2.

### CVE-2026-133333

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-841` |
| Published | 2026-11-25T11:17:08.570 |

Joomla Extension - virtuemart.net - Unpaid order confirmation via PayPal Checkout order completion task in VirtueMart extension 4.0.0-4.8.8 - The ordercompleted task of the bundled PayPal Checkout payment plugin set the order held in the current checkout session to the configured success status without verifying a PayPal capture or authorization. A shopper, including a guest, could therefore mark their own unpaid order as confirmed and paid. Fixed in 4.8.10.

### CVE-2026-133757

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-11-25T10:17:13.457 |

Since Symfony 5.4.48, 6.4.16, 7.1.9 and 7.2.0, NoPrivateNetworkHttpClient follows redirects itself, and sends each hop as a new request through the client it decorates. Before a redirect to another origin, it removes the Authorization and Cookie headers it knows about. But the decorated client then added its own default options again. These include the auth_basic, auth_bearer and auth_ntlm credentials, and the Authorization and Cookie headers it was created with. Credentials set with withOptions() on the decorator came back the same way, since the decorator forwards them to the decorated client.

These credentials were then sent to any origin that a response redirected to, for example through an open redirect on the server the application calls. The decorated client alone doesn't send them. The decorator removed the ones passed to request(), but not auth_ntlm. Since Symfony 8.1, DnsResolvingHttpClient follows redirects the same way and is affected too.

With auth_ntlm, curl started the NTLM handshake with the other origin, which could answer with a challenge to get the NTLM response of the application.

On a redirect to another origin, the decorator now passes empty Authorization and Cookie headers and unsets the auth_basic, auth_bearer and auth_ntlm options. The decorated client then can't add its own. Decorators between NoPrivateNetworkHttpClient and the transport, like ScopingHttpClient or CachingHttpClient, can't add theirs either.

### CVE-2026-129380

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-24T18:18:59.560 |

Joomla! Core - [20261143] - Core - Information disclosure in GET request task plugin in Joomla 4.1.0-5.4.10, 6.0.0-6.2.0 - The GET request task plugin stored fetched responses in a publicly accessible folder, exposing the response contents.

### CVE-2026-116382

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-24T15:17:12.620 |

Allocation of Resources Without Limits or Throttling vulnerability in Erlang OTP inets (httpd_script_env module) allows an unauthenticated remote attacker to exhaust the atom table of an httpd server that serves ESI scripts.

When mod_esi builds the environment for an ESI callback, httpd_script_env:http_env_element/3 checks that a request header name already exists as an atom, then creates the atom http_<header-name> with list_to_atom/1. Atoms are never garbage collected, and each new atom passes the existence check on a later request. So a header named node creates http_node, a header named http_node creates http_http_node, and so on. A stream of requests to any ESI URL grows the atom table until it reaches its limit (+t), and then the whole Erlang VM aborts, together with every application on the node.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.20, OTP 28.5.0.9, and OTP 29.1.3, corresponding to inets from 5.10 before 9.3.2.9, 9.6.2.5, and 9.8.2. Whether OTP before OTP 17.0, corresponding to inets before 5.10, is affected is unknown.

### CVE-2026-87753

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-25T12:18:14.623 |

Authorization bypass through User-Controlled key vulnerability in İdeal Data Finansal Teknolojiler A.Ş. IDeal WEB allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects iDeal WEB: before v1.82.

### CVE-2026-132264

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-270;CWE-863` |
| Published | 2026-11-24T21:18:17.603 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions 0.6.63 through 0.10.0, an external API key or OAuth token that has only the EXECUTE_BLOCK permission can run AutoPilotBlock through the external API and receive a full, unattended AutoPilot turn. This lets the holder use the account owner's stored third-party credentials, library agents, and workspace files, and run AutoPilot's sandboxed shell, which the same key is refused when it requests those directly. This issue is fixed in version 0.11.0.

### CVE-2026-134034

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89;CWE-352` |
| Published | 2026-11-24T17:18:16.483 |

HortusFox is a self-hosted web application for collaborative plant management. Prior to 6.2, the toggle_boolean_value() handler in app/controller/admin.php passes the name parameter of the /admin/environment/boolean/toggle route in app/config/routes.php to AppModel::updateSingle() in app/models/AppModel.php, which concatenates the parameter into the SQL UPDATE identifier position without validation. An unauthenticated attacker can induce a signed-in administrator to open a crafted link, causing SQL injection that permits expressions and subqueries to read database contents, including an administrator password hash, or modify settings to enable passwordless administrator access. The hash alone does not permit direct login. This issue is fixed in version 6.2.

### CVE-2026-80369

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-25T14:17:10.677 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Uncontrolled Search Path Element vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-80365

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-25T14:17:10.150 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Use of Externally-Controlled Format String vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-80364

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-25T14:17:10.007 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Download of Code Without Integrity Check vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to full compromise of confidentiality, integrity, and availability.

### CVE-2026-80363

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-25T14:17:09.870 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Use of Hard-coded Credentials vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-80285

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-25T10:17:16.697 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Execution with Unnecessary Privileges vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to elevation of privileges.

### CVE-2026-80271

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-25T10:17:16.023 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Use of Hard-coded Cryptographic Key vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to remote execution.

### CVE-2026-80267

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-25T10:17:15.610 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Use of Hard-coded Credentials vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-136328

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-24T20:18:53.347 |

A flaw was found in the file-psd plugin in GIMP. When processing a specially crafted PSD (Photoshop Document) image file in LAB color mode, the plugin does not properly validate that a fourth channel is present when the transparency flag is set. This mismatch causes the merged-image path to allocate buffers for three components while performing color conversion with four-component formats, resulting in a heap-based buffer overflow. This issue can result in an application crash, leading to a denial of service, or potentially allow for arbitrary code execution.

### CVE-2026-136439

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.880 |

DeepSpeed _get_zero_stage Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of DeepSpeed. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoint data. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29242.

### CVE-2026-136438

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.763 |

DeepSpeed build_engine_from_ds_checkpoint Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of DeepSpeed. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of model configuration data. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29241.

### CVE-2026-136437

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.643 |

DeepSpeed parse_optim_states Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of DeepSpeed. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoint data. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29243.

### CVE-2026-136436

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.523 |

DeepSpeed torch_checkpoint_engine Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of DeepSpeed. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoint data. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29214.

### CVE-2026-136435

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.400 |

DeepSpeed InferenceEngine Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of DeepSpeed. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoint data. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28091.

### CVE-2026-136433

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.153 |

PyTorch Foundation PyTorch torch_save_to_dcp Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch Foundation PyTorch. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the checkpoint format conversion utilities. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-32834.

### CVE-2026-136432

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:19.030 |

PyTorch Foundation PyTorch FileSystemReader Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the FileSystemReader class. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-32600.

### CVE-2026-136431

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:18.910 |

PyTorch Foundation PyTorch load_state_dict_from_url Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch Foundation PyTorch. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the load_state_dict_from_url function. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-32601.

### CVE-2026-136430

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T19:18:18.790 |

PyTorch Foundation PyTorch AOTIModelPackageLoader  Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch Foundation PyTorch. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the AOTInductor model package loader. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-33055.

### CVE-2026-136428

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T19:18:18.543 |

PyTorch Foundation PyTorch load_compiled_function Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch Foundation PyTorch. User interaction is required to exploit this vulnerability in that the target must open a malicious file.

The specific flaw exists within the load_compiled_function function. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-32603.

### CVE-2026-136427

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T19:18:18.417 |

PyTorch Foundation PyTorch AOTIModelPackageLoader Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the AOTIModelPackageLoader. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-32262.

### CVE-2026-136426

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T19:18:18.297 |

PyTorch Foundation PyTorch PT2 File Parsing Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the parsing of PT2 files. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-32602.

### CVE-2026-136425

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T19:18:18.177 |

Soda PDF Desktop App Object Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Soda PDF Desktop. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the handling of App objects. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31959.

### CVE-2026-136424

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-24T19:18:18.050 |

Soda PDF Desktop PDF File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Soda PDF Desktop. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31961.

### CVE-2026-136423

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T19:18:17.923 |

Soda PDF Desktop PDF File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Soda PDF Desktop. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31960.

### CVE-2026-136422

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-24T19:18:17.770 |

Soda PDF Desktop PDF File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Soda PDF Desktop. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PDF files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-31995.

### CVE-2026-121754

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-24T18:18:51.333 |

Parallels Desktop inittool2 Link Following Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Parallels Desktop. An attacker must first obtain the ability to execute low-privileged code on the target host system in order to exploit this vulnerability.

The specific flaw exists within the inittool2 component. By creating a symbolic link, an attacker can abuse the component to take ownership of critical folders. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root on the host system. Was ZDI-CAN-30268.

### CVE-2026-50048

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-24T17:18:51.510 |

Genetec Security Center can expose access control unit credentials in plain text in server log files when specific non-default logging options are enabled. An attacker with local access to the affected log files could retrieve and use these credentials.

### CVE-2026-80284

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-25T10:17:16.560 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Improper Authentication vulnerability. An attacker with local access could potentially exploit this vulnerability, leading to exposure of sensitive data and unauthorized modification of system operations.

### CVE-2026-134647

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-25T04:17:34.220 |

Webmin through 2.670 contains a cleartext transmission vulnerability in web-lib-funcs.pl and fastrpc.cgi that sends cluster RPC traffic over raw TCP despite SSL configuration. Network-positioned attackers can read the session ID and remote_eval payloads or alter calls in transit to execute code as root on managed servers.

### CVE-2026-134642

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-25T04:17:33.360 |

Webmin through 2.670 contains a missing authentication vulnerability in fastrpc.cgi that allows unauthenticated network peers to connect to tcpwrite and tcpread file-transfer listeners without session checks. Attackers can race to connect to the predictable transfer port during cluster operations to steal transferred files or replace staged packages, achieving root code execution.

### CVE-2026-134638

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-25T04:17:32.440 |

Webmin through 2.670 contains a missing integrity verification vulnerability in usermin/upgrade.cgi that downloads Usermin upgrade packages over plaintext HTTP without signature or digest checks. On-path network attackers or DNS spoofers can supply a malicious RPM, Debian, or tar.gz package whose maintainer scripts or setup.sh execute as root during upgrade.

### CVE-2026-134630

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-25T04:17:31.033 |

Webmin through 2.670 contains a remote code execution vulnerability in the Perl Modules (cpan) module, which downloads CPAN indexes and module archives over plaintext HTTP without checksum or signature verification. On-path network attackers can answer the outbound fetch while an administrator installs a CPAN module, supplying a malicious Makefile.PL that cpan/download.cgi runs as root before confirmation.

### CVE-2026-134438

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-25T04:17:28.560 |

Webmin through 2.670 contains an insecure download vulnerability in webmin/upgrade.cgi, cluster-webmin/upgrade.cgi and cluster-usermin/upgrade.cgi that fetches upgrade packages over plaintext HTTP with GnuPG signature verification disabled by default. On-path network attackers can substitute a malicious RPM, Debian or tar.gz package during a default upgrade to execute code as root on the Webmin host and managed cluster servers.

### CVE-2026-134326

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-25T04:17:27.147 |

Webmin through 2.670 contains a signature verification bypass vulnerability in webmin-lib.pl that allows attackers to install unsigned module updates when GnuPG setup fails. Attackers tampering with update downloads via network position or a custom update URL can supply malicious modules that run as root when administrators apply updates.

### CVE-2026-134283

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-25T04:17:26.430 |

Webmin through 2.670 contains an improper certificate validation vulnerability in the http_download function of web-lib-funcs.pl that skips TLS chain and hostname verification. Man-in-the-middle attackers can present any certificate and substitute downloaded modules, themes, or catalog content, leading to root code execution or injected HTML.

### CVE-2026-136630

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-25T03:17:49.700 |

Electerm before 5.9.0 contains an origin validation vulnerability in the MCP Server widget that allows remote attackers to execute commands by bypassing Host and Origin checks through DNS rebinding. Attackers can lure users to a page that rebinds to 127.0.0.1 and calls unauthenticated MCP tools on port 30837 to run OS commands locally and on open SSH sessions.

### CVE-2026-134068

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T19:18:10.440 |

A stack-based buffer overflow in the replication origin name parsing component in AWS pgactive before 2.1.10 might allow an authenticated remote user to execute arbitrary operating system commands as the database operating system user via a crafted replication origin name.



To remediate this issue, users should upgrade to pgactive version 2.1.10 or later.

### CVE-2026-129425

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T18:19:02.053 |

Joomla Extension - regularlabs.com - PHP code injection via content inserted during article preparation in Sourcerer extension < 18.0.0 - Sourcerer decided whether PHP may run based on the author or last editor of the host article and applied that decision to complete code blocks that other extensions, such as Users Anywhere, inserted into the article while it was prepared. A user able to edit a value rendered by such an extension, for example the display name in their own user profile, could therefore have PHP executed in the context of a trusted article. Sourcerer 18.0.0 authorizes each executable block against its own source; Users Anywhere 3.1.0, ReReplacer 16.4.0 and Snippets 11.2.0 supply the source information needed to keep executing eligible saved content.

### CVE-2026-129371

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1024` |
| Published | 2026-11-24T18:18:58.380 |

Joomla! Core - [20261134] - Core - Improper root user check in Joomla 1.6.0-5.4.10, 6.0.0-6.2.0 - A loose comparison of the configured emergency root user against the username allowed accounts with a numeric username to gain super user privileges.

### CVE-2026-82170

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T17:18:53.647 |

Dell Virtual Storage Integrator for VMware vSphere Web Client, versions prior to 10.12.0.0, contains a Server-Side Request Forgery SSRF vulnerability in httpRest.js. A low privileged remote attacker could potentially exploit this vulnerability, leading to unauthorized access to internal services

### CVE-2026-82168

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-24T17:18:53.380 |

Dell Virtual Storage Integrator for VMware vSphere Web Client, versions prior to 10.12.0.0, contains a Use of Hard-coded Credentials vulnerability in ssl_config.properties. An unauthenticated local attacker could potentially exploit this vulnerability, leading to credential exposure.

### CVE-2026-136631

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-25T03:17:49.893 |

Mastodon 4.7.4 and 4.8.0-alpha.3 before 5.0.0-beta.1 contains an authentication bypass vulnerability in authenticate_with_sign_in_token that allows authenticated local users to rebind pending login attempts to other accounts. Attackers can submit sign_in_token_resend with a victim's user[email] parameter, then guess the unthrottled 6-character token to sign in as inactive accounts lacking two-factor authentication.

### CVE-2026-136628

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-25T03:17:49.343 |

Wails before 2.17.1 on Linux contains an origin validation error in the sendMessageToBackend WebKitGTK handler that allows child-frame scripts to invoke the privileged IPC channel. Attackers controlling content loaded in an iframe can post messages that pass the top-level URI origin check and call bound Go methods and Wails runtime operations.

### CVE-2026-132735

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-24T23:17:29.910 |

Improper Access Control vulnerability in Wikimedia Foundation MediaWiki - OATHAuth Extension. This vulnerability is associated with program files src/Auth/ReauthPrimaryAuthenticationProvider.php, src/Auth/SecondaryAuthenticationProvider.php. This issue affects MediaWiki - OATHAuth Extension: 1.47.

### CVE-2026-129378

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:59.300 |

Joomla! Core - [20261141] - Core - XSS in com_installer changelog in Joomla 4.0.0-5.4.10, 6.0.0-6.2.0 - Inadequate filtering of remote extension changelog contents leads to an XSS vulnerability in the changelog view.

### CVE-2026-129377

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:59.160 |

Joomla! Core - [20261140] - Core - XSS in joomla-dialog header in Joomla 5.0.0-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the dialog header text leads to an XSS vulnerability in the extension changelog dialog.

### CVE-2026-129365

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T18:18:57.580 |

Joomla! Core - [20261128] - Core - XSS in com_installer language installation view in Joomla 2.5.7-5.4.10, 6.0.0-6.2.0 - Inadequate escaping of the language update feed metadata leads to an XSS vulnerability in the language installation view.

### CVE-2026-130336

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-25T05:18:29.723 |

Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') in the HWBridge custom methods command dispatcher (lib/rex/post/hwbridge/ui/console/command_dispatcher/custom_methods.rb) in Rapid7 Metasploit Framework versions prior to 6.5.10 on all platforms allows a malicious or compromised hardware bridge to execute arbitrary code in the msfconsole process via a crafted method_name returned by the /custom_methods endpoint. The injected code runs automatically when the operator connects to the bridge, without the operator invoking any custom command.

### CVE-2026-124606

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T04:17:23.933 |

Improper Limitation of a Pathname to a Restricted Directory Vulnerability in Cosminexus Component Container.

This issue affects Cosminexus Component Container: from 11-20 before 11-70-04.

### CVE-2026-136613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T23:17:32.180 |

GNU Inetutils FTP Client File Retrieval Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GNU Inetutils FTP Client. User interaction is required to exploit this vulnerability in that the target must interact with a malicious FTP server.

The specific flaw exists within the processing of filenames. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the current user. Was ZDI-CAN-29119.

### CVE-2026-133456

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-24T22:18:50.277 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. From 0.11.1 before 0.11.3, anyone with an Exa Search Monitor trigger's URL can start one run of the owner's workflow per request with fake event data, even when a secret is set. The workflow runs with the owner's saved credentials and credits, and nothing is returned to the attacker. This issue is fixed in version 0.11.3.

### CVE-2026-129833

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-24T17:18:14.897 |

A flaw was found in rsyslog. A remote, unauthenticated attacker can trigger a stack-based buffer overflow by sending a malformed log message containing an embedded IPv4-in-IPv6 address to an instance configured with the mmanon anonymization module. This flaw causes the logging service to crash, leading to a Denial of Service (DoS).

### CVE-2026-136157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T15:17:33.797 |

In Valkey 8.0.x before 8.0.11, 8.1.x before 8.1.10, 9.0.x before 9.0.6 and 9.1.x before 9.1.2, the RDMA transport's pending-data handler walks its connection list with an iterator that caches the next entry. A command processed from inside that loop, such as CLIENT KILL, can synchronously free another client's connection, and closing an RDMA connection did not remove it from the pending list, so the handler then uses freed memory. An authenticated user can use this to reliably crash the server, and the freed heap chunk can be reclaimed with attacker-influenced bytes. Only servers built with RDMA support (USE_RDMA) and configured with an RDMA listener are affected.

### CVE-2026-16665

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-24T22:18:51.420 |

Summary

MCUboot enforces several security-critical invariants on the boot, image-swap, and validation paths using assert(). In a standard release/production build (NDEBUG defined) assert() expands to a no-op, so an invariant the code intends to halt on instead falls through, and execution continues with the bad or inconsistent state. Where the guarded condition is attacker-influenceable through the flash-write boundary (serial-recovery / DFU), this is a security check that is simply absent in release builds.

This is one root cause (assert-as-security-guard, no-op under NDEBUG) with one fix approach (replace the security-critical asserts with real fail-closed checks), so it is filed as a single advisory covering the enumerated sites.

Worst reachable instance — inconsistent swap status completes the swap without validation

In the swap-resume status read, an inconsistent status (erased_sections > 1) is detected, logged, and — when MCUBOOT_VALIDATE_PRIMARY_SLOT is disabled — is meant to abort, because "there is no way to be sure the swapped primary slot is OK." The abort is assert(0):

boot/bootutil/src/swap_move.c:181-194 — if (erased_sections > 1) { ... #if !defined(MCUBOOT_VALIDATE_PRIMARY_SLOT) / ... abort! / assert(0); #endif }, then execution falls through to compute bs->op/idx/state from the inconsistent status (lines 197-208) and return 0 (success).
boot/bootutil/src/swap_offset.c:266-280 — identical pattern; falls through to bs->op/idx/state and return 0.
boot/bootutil/src/swap_scratch.c:227-241 — same invalid/assert(0) pattern for the scratch backend.

Under NDEBUG with primary-slot validation off, the inconsistent status is neither aborted (assert is a no-op) nor re-validated (validation off), so boot_complete_partial_swap() finishes the swap on inconsistent metadata and the primary slot is booted without a signature check. An attacker who can write the swap-status trailer can craft the inconsistent status.

Reachability (threat model). Secondary slot + scratch trailers are A2-writable by definition (that is what a DFU upload is). Under MCUBOOT_SERIAL_RECOVERY the primary trailer is A2-writable too: boot/boot_serial/src/boot_serial.c:978 opens flash_area_id_from_multi_image_slot(img_num, 0) (== primary) and writes from offset 0 bounded by area_size, so it can paint the primary swap-status/magic. This is how the A2 (recovery/DFU, unauthenticated by design) attacker influences the guarded condition. Property violated: P1 (image authenticity / secure-boot bypass) when un-revalidated content is booted, and P6 (boot/recovery availability).

Second reachable instance — resume-path swap_size from an unguarded trailer

boot/bootutil/src/loader.c:1190-1193: the swap resume branch does fap = boot_find_status(...); assert(fap != NULL); rc = boot_read_swap_size(fap, &bs->swap_size); assert(rc == 0);. boot_find_status() (boot/bootutil/src/bootutil_misc.c:166-204) searches {scratch, primary} and, on no-valid-magic-match, returns the last-iterated area (primary), not NULL — so assert(fap != NULL) cannot fire even in debug, and under NDEBUG neither assert fires. swap_size is then read from an A2-writable (serial-recovery primary, or scratch) trailer with no fail-closed handling. This is the same swap-metadata-trust family as the recorded resume/swap_size disclosure.

Reachable-security sites (center the fix here)

1. boot/bootutil/src/swap_move.c:193 — inconsistent-status assert(0), falls through to complete swap. A2 + !VALIDATE_PRIMARY. [worst]
2. boot/bootutil/src/swap_offset.c:278 — same, swap-offset backend.
3. boot/bootutil/src/swap_scratch.c:239 — same, swap-scratch backend.
4. boot/bootutil/src/loader.c:1191 and :1193 — resume assert(fap != NULL) / assert(rc == 0) guarding swap_size read from an A2-writable trailer; compounded by boot_find_status() never returning NULL.

(Truncated. The full description is in the advisory: https://github.com/mcu-tools/mcuboot/security/advisories/GHSA-cr9j-p626-pwcc)

### CVE-2026-129381

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-24T18:18:59.700 |

Joomla! Core - [20261144] - Core - CSRF token leak in install from web in Joomla 4.0.0-5.4.10, 6.0.0-6.2.0 - The install from web feature submitted the CSRF token of the administrator to third-party sites.

### CVE-2026-135390

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-24T17:18:24.197 |

Pion DTLS is a Go implementation of Datagram Transport Layer Security. From 2.1.0 until 3.1.14, a listener performing DTLS 1.2 resumption accepted a session created by an outbound client connection without checking which role created it. A malicious server previously contacted by the application can retain the outbound session secret, select the client-side cached session through its session key, and present it to the application's reachable listener when both connections share a SessionStore. The attacker must first complete an outbound connection. WebRTC users are not affected. The listener can accept application data without running its normal PSK callback or client-certificate authentication checks, allowing a peer trusted only for an outbound connection to gain unauthorized listener access. The issue is fixed in version 3.1.14.

### CVE-2026-80297

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T13:17:33.047 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Path Traversal vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to unauthorized file access, modification, or disruption of system operations.

### CVE-2026-80296

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-25T13:17:32.900 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains a Path Traversal vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to unauthorized file access, modification, or disruption of system operations.

### CVE-2026-80286

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-25T13:17:31.723 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an External Control of File Name or Path vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to unauthorized file access, modification, potentially compromising confidentiality and integrity.

### CVE-2026-80269

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-377` |
| Published | 2026-11-25T10:17:15.750 |

Dell Secure Connect Gateway (SCG) Virtual Edition, versions prior to 5.36.00.16, contains an Insecure Temporary File vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to filesystem access for attacker.

### CVE-2026-134635

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T04:17:31.920 |

Webmin through 2.670 contains an OS command injection vulnerability in ldap-client/check.cgi that allows LDAP directory writers to execute commands via unquoted uid values. Attackers can create a posixAccount entry with shell metacharacters in its uid, executing commands as root when an administrator runs Check Configuration.

### CVE-2026-134440

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-25T04:17:28.920 |

Webmin through 2.670 contains a Perl code injection vulnerability in cluster-useradmin/sync.cgi that allows attackers to run code by placing single quotes in home directory paths. Attackers with root on one managed host can craft a home path that breaks out of remote_eval() string literals during Sync, executing Perl as root on other managed hosts.

### CVE-2026-61513

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-24T21:18:31.793 |

VeraCrypt through 1.26.31 on Linux contains an improper path restriction vulnerability in the elevated CoreService, which passes the path and owner UID from a SetFileOwnerRequest directly to chown() in CoreUnix::SetFileOwner without target validation on Linux. An attacker with an active elevated CoreService session and same-UID access who reopens the request pipe through /proc/<pid>/fd/<n> can take ownership of arbitrary system files such as /etc/passwd and /etc/shadow, achieving full root compromise.

### CVE-2026-61512

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T21:18:31.613 |

VeraCrypt before 1.26.30 on Linux contains a command injection vulnerability in CoreUnix::CheckFilesystem that allows a local attacker with same-UID access and an active elevated CoreService session to execute arbitrary commands by injecting an unsanitized VirtualDevice value into a shell command string. Attackers can reopen the request pipe through /proc/<pid>/fd/<n> and supply a crafted VirtualDevice value such as /dev/null; <command> to achieve arbitrary command execution as root.

### CVE-2026-136534

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-24T21:18:20.593 |

Devin Desktop Uncontrolled Search Path Element Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Devin Desktop. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the configuration of the Electron framework. The product loads a script file from an unsecured location. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of a target user. Was ZDI-CAN-33385.

### CVE-2026-136440

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-24T19:18:20.000 |

Python Packaging Authority pip Configuration File Incorrect Permission Assignment Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Python Packaging Authority pip. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability. User interaction on the part of a target user is also required.

The specific flaw exists within the way configuration files are stored. The issue results from incorrect permissions on files. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of a target user. Was ZDI-CAN-25377.

### CVE-2026-136172

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T15:17:36.453 |

Assimp through 6.0.6 contains a heap out-of-bounds write vulnerability in the OBJ exporter that allows attackers to corrupt memory via NaN vertex components breaking comparator ordering. Attackers can supply a crafted PLY file with NaN texture coordinates or vertex colors that, when exported to OBJ in libc++ builds, writes file-controlled data past a heap buffer and crashes the application.

### CVE-2026-136170

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T15:17:35.113 |

Assimp through 6.0.6 contains a use-after-free and double free vulnerability in OpenGEXImporter.cpp because InternReadFile does not reset cached importer state between files. Attackers can supply OpenGEX files to applications reusing one Importer instance, causing freed node, camera, and material pointers to corrupt heap memory and crash.

### CVE-2026-136881

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-25T14:17:08.283 |

In the `setup-osc` GitHub Action of Eclipse Apoapsis, from commit 4e9eaff up to, but not including, commit 03efc4c, the ORT Server version returned by the `/api/v1/versions` endpoint is inserted into a shell script via a GitHub Actions expression without validation. An attacker who controls the responses of the configured ORT Server, for example by compromising the server, can execute arbitrary commands on the GitHub Actions runner and access the secrets available to the calling workflow.



The issue is fixed in commit 03efc4c, which only accepts version strings consisting of alphanumeric characters, `.`, `+`, and `-`.

### CVE-2026-133738

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-25T11:17:09.263 |

Vulnerability involving the exposure of sensitive information in the ver_usuarios endpoint. The JSON response includes data that is not required for the query and which should remain restricted, such as Argon2id password hashes, TOTP secrets, internal configuration flags, email addresses, telephone numbers and dates of last access. An authenticated user querying this resource can access this confidential information, which is sent directly to the web client.

### CVE-2026-136632

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-25T03:17:50.250 |

OpenProject 17.2.0 before 17.5.2, 17.6.0 before 17.6.1, 17.7.0 before 17.7.3, 17.8.0 before 17.8.2, and 17.9.0 before 17.9.7 contains an externally controlled method selection vulnerability in InplaceEditFieldsController via the unvalidated attribute parameter. Users who can view a project can request the inplace_edit_fields reset route with attribute destroy to delete projects and subprojects, or invoke other methods exposing restricted data.

### CVE-2026-136539

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T21:18:21.220 |

LiteLLM Pass-Through Endpoint Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of LiteLLM. Authentication is required to exploit this vulnerability.

The specific flaw exists within the handling of pass_through_endpoints. The issue results from the lack of proper validation of code before it is executed via module import. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-31433.

### CVE-2026-136535

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T21:18:20.720 |

LiteLLM MCP Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of LiteLLM. Authentication is required to exploit this vulnerability.

The specific flaw exists within the handling of MCP stdio configurations. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the service account. Was ZDI-CAN-31815.

### CVE-2026-123166

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T17:18:13.160 |

SolarWinds Serv-U fails to properly sanitize user-controlled arguments, which could allow the injection of 
commands. This only affects Windows installations.

### CVE-2026-136624

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-25T03:17:35.000 |

lightNVR before 0.44.3 contains an authorization bypass vulnerability in go2rtc_proxy_authorize_request() that allows authenticated users to access restricted cameras by exploiting inconsistent src parameter parsing. Attackers can percent-encode a second src parameter name or exceed the 255-byte truncation so go2rtc resolves a different camera, obtaining unauthorized snapshots and HLS live streams.

### CVE-2026-136453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-187` |
| Published | 2026-11-24T20:18:53.670 |

browser-use before 1.0.0 contains an allowlist bypass vulnerability in the SecurityWatchdog's _is_url_match function that allows attackers to bypass domain restrictions by exploiting a raw-string startswith() comparison instead of parsed hostname validation. Attackers can craft URLs using userinfo injection or domain prefix confusion (e.g..com@attacker.com or .com.attacker.com) to redirect an LLM-controlled navigation to an arbitrary host, exfiltrating sensitive data such as secrets embedded in the URL to an attacker-controlled endpoint.

### CVE-2026-123256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-24T19:18:03.973 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-136196

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-24T17:18:48.297 |

GPAC through 26.07.0 contains an integer underflow vulnerability in gf_rtp_parse_mpeg4 that allows remote attackers to trigger excessive looping by advertising an undersized AU-headers-length. Attackers can send a crafted 22-byte AAC-hbr RTP packet from an RTP sender or malicious RTSP server to run about 2^28 iterations, pinning a CPU core and stalling clients.

### CVE-2026-136195

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-24T17:18:48.127 |

GPAC through 26.07.0 contains a heap out-of-bounds read vulnerability in gf_rtp_parse_mpeg4 that allows remote attackers to crash clients by sending MP4V-ES RTP payloads shorter than 4 bytes. A remote RTP sender or malicious RTSP server can send a short packet after a marker-bit packet, causing an unsigned wraparound in the VOP start-code search loop that reads past the buffer and causes denial of service.

### CVE-2026-136192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-24T17:18:47.607 |

GPAC through 26.07.0 contains an infinite loop vulnerability in SDP_ParseAttribute that allows attackers to cause unbounded memory growth via a NUL byte in an a=fmtp line. Attackers can supply a crafted .sdp file or malicious RTSP DESCRIBE response to hang gf_sdp_info_parse and exhaust memory, causing denial of service.

### CVE-2026-136191

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-24T17:18:47.420 |

GPAC through 26.07.0 contains an infinite loop vulnerability in gf_rtsp_do_deinterleave that allows malicious RTSP servers to hang clients by sending non-RTSP, non-interleaved data. Attackers can answer a client request with a few bytes not starting with '$', 'RTSP', or 'HTTP', causing the RTSP client thread to spin forever and consume a full CPU core.

### CVE-2026-136188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-24T17:18:46.933 |

Spug before 4.1.1 contains an information disclosure vulnerability that allows authenticated non-administrator users to read per-host SSH private keys through the GET /api/host/ endpoint. Users granted a host can read the cleartext pkey field returned by Host.to_view and log in directly over SSH, bypassing Spug's permissions and audit trail even after revocation.

### CVE-2026-136185

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-11-24T17:18:46.353 |

Prismor before 1.57.0 contains a wildcard CORS misconfiguration and missing authentication in its local HTTP API that allows remote attackers to overwrite security policies via cross-origin requests. Attackers can lure a developer to a malicious page that sends PUT requests to /api/policy/global or /api/policy/project, disabling AI agent guardrails and reading session and event data.

### CVE-2026-136179

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T17:18:45.343 |

EpicStaff 1.2.0 before 1.3.1 contains an insecure direct object reference vulnerability in DocumentViewSet download and copy endpoints that allows authenticated users to access other organizations' documents. Attackers holding Knowledge Sources permissions in one organization can enumerate sequential document IDs to download or copy foreign documents, or insert documents into another organization's collection.

### CVE-2026-135387

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-352;CWE-650` |
| Published | 2026-11-24T17:18:23.690 |

HortusFox is a self-hosted web application for collaborative plant management. Prior to 6.2, state-changing AdminController routes in app/config/routes.php accept GET requests. The affected AdminController in app/controller/admin.php does not invoke Asatru\Controller\PostValidator to check CSRF tokens. An unauthenticated attacker can induce a signed-in administrator to open a cross-site link, causing privileged actions such as changing environment settings, deleting users or locations, managing API keys, or clearing cached data. In the tested build, a cross-site POST to /admin/user/update can promote a user immediately after login; in default Chromium the POST succeeds within the approximately two-minute Lax+POST grace period but not with an aged cookie, and other browser configurations may permit the POST. Version 6.2 mitigates the documented GET path, but no complete anti-CSRF fix is documented.

### CVE-2026-75582

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T15:17:40.503 |

Frappe LMS before 2.65.0 contains an improper authorization vulnerability that allows Batch Evaluators to modify any evaluation because the LMS Certificate Evaluation doctype lacks a has_permission scoping hook. Attackers can call the whitelisted create_lms_certificate method with any evaluation name to issue certificates for unassigned evaluations or learners outside their batches.

### CVE-2026-136863

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-25T14:17:08.143 |

In Eclipse Apoapsis ORT Server versions 0.1.0 to 0.83.0, the file-based configuration providers do not restrict resolved file paths to the configured directory. An authenticated user who is allowed to trigger an ORT run for a single repository can use `../` sequences or absolute paths in `reporter-template://` references of the reporter job configuration to make the reporter worker read arbitrary files and include them in the generated reports. This discloses files such as environment variables, mounted secrets, and configuration files that contain credentials shared across all tenants of the server.



The issue is fixed in Eclipse Apoapsis ORT Server 0.84.0.

### CVE-2026-133743

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-11-25T10:17:11.093 |

The fix for CVE-2026-123339 (GHSA-wg5q-m2ww-f3c9) restores the router context of the main request after an inline fragment, but the cause of that issue is still there. A page can render an inline fragment with render() in Twig, or with an ESI tag when no gateway cache is used. While the fragment runs, SubRequestHandler adds 127.0.0.1 to the trusted proxies of every request. Code that reads the main request during that time trusts its X-Forwarded-* and Forwarded headers if the main request came from 127.0.0.1.

Symfony itself reads the main request there:
- asset() takes the base path and the scheme of the main request. With X-Forwarded-Prefix: //evil.example, asset('build/app.js') returns //evil.example/build/app.js, a script loaded from another host. Request::getBasePath() keeps its first result, so when it's first computed inside the fragment, the later asset() calls of the page return such URLs too.
- absolute_url() in Twig, through UrlHelper, takes the host and the scheme of the main request from X-Forwarded-Host and X-Forwarded-Proto.

When a shared cache stores the page, every visitor gets these URLs. With asset(), the page then runs scripts from a host chosen by the attacker.

This affects applications reached over HTTP from 127.0.0.1 when that address isn't a trusted proxy. That's the case behind a TLS terminator, a reverse proxy or an HTTP cache running on the same host. When framework.trusted_proxies is not configured, which is the default, every forwarded header is trusted during that window, X-Forwarded-Prefix included. Configuring framework.trusted_hosts doesn't help with asset(), since the prefix is not a host. Applications that get requests directly through php-fpm or mod_php are not affected, and neither are those behind a proxy on another host. REMOTE_ADDR is not 127.0.0.1 there.

SubRequestHandler doesn't change the trusted proxies of every request anymore. Only the requests it builds, and the requests copied from them, trust 127.0.0.1. While a fragment renders, the main request keeps ignoring the forwarded headers sent by the client.

symfony/http-kernel now requires the version of symfony/http-foundation that contains this fix.

### CVE-2026-126536

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-25T02:17:39.200 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability in the XLSX tax-import workflow. An authenticated Manager can import HTML in a tax name and associate the tax with an item. When an Administrator attempts to disable that tax, Akaunting renders the original stored name in an error notification through Vue v-html, causing attacker-controlled markup to execute within the browser of another authenticated user.

### CVE-2026-123626

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T23:17:20.347 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability in the company localisation date format. An authenticated Manager can store an arbitrary date format. When another authenticated user opens a recurring invoice, Akaunting formats dates with that value and sends the result to a raw HTML schedule description, causing attacker-controlled markup to execute in the victim's Akaunting origin.

### CVE-2026-136429

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-24T19:18:18.660 |

PyTorch Foundation PyTorch PT2 File Parsing Exposed Dangerous Method Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of PyTorch Foundation PyTorch. User interaction is required to exploit this vulnerability in that the target must open a malicious file.

The specific flaw exists within the parsing of PT2 archive files. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-32653.

### CVE-2026-129394

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T18:19:01.440 |

Joomla! Core - [20261157] - Core - Path traversal in com_scheduler task log file name in Joomla 4.1.0-5.4.10, 6.0.0-6.2.0 - Inadequate validation of the log file name of scheduled tasks allowed writing log entries to files outside the log folder.

### CVE-2026-63583

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-11-24T15:17:38.343 |

ExAws.S3.Utils.build_lifecycle_rule/1 in ex_aws_s3 interpolates caller-supplied lifecycle rule fields (the rule id, filter prefix, tag key and value, storage class, and noncurrent-version count) directly into the PutBucketLifecycleConfiguration XML body without escaping XML metacharacters. An application that populates any of these fields from untrusted input (for example a tenant-supplied object tag) lets an attacker break out of the surrounding element and inject arbitrary XML into the request, including an entirely new lifecycle action such as a delete-after-one-day expiration that destroys the bucket's objects. The public entry point ExAws.S3.put_bucket_lifecycle/2 flows directly into this builder.

This issue affects ex_aws_s3: from 2.3.0 before 2.6.0.

### CVE-2026-116293

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787;CWE-1284` |
| Published | 2026-11-24T15:17:12.070 |

Out-of-bounds Write vulnerability in the external term format decoder in Erlang OTP erts allows an attacker who controls the input to binary_to_term/1,2 to abort the Erlang VM via a NEWER_REFERENCE_EXT term with a zero-length ID. decoded_size in erts/emulator/beam/external.c accepts a reference whose 16-bit Len field is zero, but dec_term always reads one ID word. dec_term then runs 4 bytes ahead of the position that decoded_size validated. It decodes the bytes that follow as terms that were never sized, and writes past the reserved process heap.

The abort takes down every process on the node. Supervision, try/catch and the safe option do not prevent it. enif_binary_to_term() and the distribution protocol reach the same decoder, and distribution is assumed to run on trusted networks only. NEW_REFERENCE_EXT also accepts a zero length, but its range check on the first ID word rejects the shifted input. On 32-bit builds, a zero-length reference of either type at the end of the input, followed by trailing bytes, can write one word past the reserved heap.

This issue affects OTP from OTP 17.0 before OTP 27.3.4.20, OTP 28.5.0.9, and OTP 29.1.3, corresponding to erts from 6.0 before 15.2.7.15, 16.4.0.8, and 17.1.2. Whether OTP before OTP 17.0, corresponding to erts before 6.0, is affected is unknown.
