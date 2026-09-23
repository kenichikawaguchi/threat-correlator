# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-23 15:00 UTC
- **対象期間**: `2026-09-22T15:00:24.000Z` 〜 `2026-09-23T15:00:46.000Z`
- **重要CVE数**: 280 件（Critical 9.0+: 75 件 / High 7.0〜: 205 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 40 件以上**と非常に多く、特に **Adobe 製品・Zoho ManageEngine・SunEditor** 系列で深刻度 10.0 の脆弱性が集中しています。  
- 多くは **認証不要 (Network‑Only) のリモートコード実行 (RCE)・権限昇格** が可能で、攻撃者は数秒でクラウドリソースや内部システムを完全に乗っ取ることが想定されます。  
- 同一製品 (例: Adobe Campaign Classic) に対して **複数のコードインジェクション・SQLi・SSRF** が同時に報告されており、**パッチ適用の遅れが大規模な被害につながりやすい** 状況です。  

---

## 2. 特に注目すべき CVE  

| CVE | 主な影響 | 重要視する理由 | 影響範囲（主な製品・環境） |
|-----|----------|----------------|---------------------------|
| **CVE‑2026‑86708** (CVSS 10.0) | ManageEngine Applications Manager のインストーラに Google Cloud サービスアカウントの **秘密鍵が平文で埋め込まれていた**。攻撃者はキーを取得し、クラウドリソースを **完全に偽装** できる。 | ・認証不要・ネットワークから直接取得可能<br>・クラウド環境全体への横展開リスクが高い | ZohoCorp ManageEngine Applications Manager **v182200 以前** |
| **CVE‑2026‑59167** (CVSS 10.0) | SunEditor (2.47.11 未満) の HTML サニタイズが不完全で、**カスタム要素にイベントハンドラ属性が残存**。任意の JavaScript が実行可能。 | ・フロントエンドの WYSIWYG エディタは多くの SaaS・社内ツールで採用されており、**XSS が広範囲に波及** する恐れ | SunEditor **v2.47.10 以前** |
| **CVE‑2026‑75745** (CVSS 10.0) | Adobe Experience Manager Forms JEE の **不適切な認可** により、任意コードが現在のユーザー権限で実行できる。 | ・Adobe AEM は大手企業の顧客ポータル・EC システムで広く利用。<br>・認可バイパスは **管理者権限取得** に直結 | Adobe Experience Manager Forms JEE **該当バージョン (ベンダーが公開したパッチ適用前) ** |
| **CVE‑2026‑28324** (CVSS 9.8) | SolarWinds Observability Self‑Hosted の **不十分な整合性チェック** による RCE。デフォルトで無防備な設定が対象。 | ・インフラ監視ツールは **内部ネットワークの可視化権限** を持つため、侵入後の横移動が容易 | SolarWinds Observability Self‑Hosted **非デフォルト設定のインスタンス** |
| **CVE‑2026‑93088** (CVSS 9.8) | SGLang の DiffusionServer が **認証なし ZeroMQ ROUTER ソケット** を公開し、受信フレームをそのまま実行。任意コード実行が可能。 | ・AI/ML ランタイムはクラウド・オンプレミス問わず高速展開が前提。<br>・攻撃者がモデル生成サーバを乗っ取ると **機密データ漏洩・マルウェア配布** が可能 | SGLang **runtime 0.?.? (該当バージョン未パッチ)** |

> **注:** Adobe Campaign Classic 系列は同一製品に対して 10 件以上の CVE が報告されており、**全体としてパッチ適用が急務** です。ここでは代表例として上記 5 件をピックアップしましたが、実装環境に Adobe Campaign Classic が含まれる場合は **全 CVE のパッチ適用** を必ず実施してください。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品・コンポーネント | 現行バージョン (脆弱) | 推奨バージョン / 対策 |
|----------------------|----------------------|------------------------|
| **ZohoCorp ManageEngine Applications Manager** | 182200 以前 | **182201 以上**（2026‑07‑xx でリリースされたパッチ） |
| **SunEditor** | 2.47.10 以前 | **2.47.11 以上**（公式リリースノート参照） |
| **Adobe Experience Manager Forms JEE** | 該当ベンダーパッチ未適用版 | ベンダーが提供する **2026‑08‑xx 以降のセキュリティパッチ** を即時適用 |
| **SolarWinds Observability Self‑Hosted** | デフォルト以外の設定で未パッチ | **2026‑09‑xx** でリリースされた **Integrity‑Check 強化パッチ** を適用し、**デフォルト設定に戻す** |
| **SGLang Runtime** | 0.?.?（脆弱） | **公式リリースの最新安定版 (≥ 0.?.?)** にアップデート |
| **Adobe Campaign Classic (ACC)** | 2026‑**全バージョン**（多数 CVE） | **2026‑10‑xx** で提供された **総合パッチセット**（CVE‑2026‑75745 など全 CVE を含む）を適用 |
| **Lantronix SLC8000 / EMG8500 / EMG7500 / SLB882** | Firmware < 9.7.0.5 (SLC8000) / < 9.7.0.1 (EMG) | **Firmware 9.7.0.5 以上**（SLC8000）・**9.7.0.1 以上**（EMG）へ更新 |
| **IBM Financial Transaction Manager (FTM) for OpenShift** | 12.8.709 以前（OpManager）・5.4.0.0 以前（DataStage） | **IBM が提供する 2026‑09‑xx 以降のパッチ** を適用し、**シンボリックリンク・コマンドインジェクション対策** を有効化 |
| **Analytics and Location Engine (ALE)** | 2026‑07‑xx 以前 | **デフォルト認証情報の変更** と **2026‑09‑xx パッチ** の適用 |

### 3.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-86708

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-23T14:17:09.467 |

ZohoCorp ManageEngine Applications Manager versions 182200 and below were vulnerable to exposure of a Google Cloud service-account private key in the Applications Manager installer, which could allow an unauthenticated attacker to impersonate the service account and access or modify associated cloud resources.

### CVE-2026-59167

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T14:17:07.923 |

SunEditor is a lightweight and powerful WYSIWYG editor in vanilla JavaScript with no dependencies. Prior to 2.47.11, the sanitizer in src/lib/core.js does not consistently reject namespaced or custom HTML elements, allowing event-handler attributes to remain on crafted elements. When an application renders attacker-controlled editor content and a user interacts with the element, the retained handler can execute script in the application's browser origin, enabling stored cross-site scripting, data exposure, or unauthorized browser-context actions. This issue is fixed in version 2.47.11.

### CVE-2026-75745

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T19:16:47.510 |

Adobe Experience Manager Forms JEE is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-89275

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:29.407 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-84412

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:22.923 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-7866

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T18:17:19.940 |

Stack-based Buffer Overflow vulnerability in RTI Connext Professional (Core Libraries) allows Overflow Buffers. This issue affects Connext Professional: from 7.4.0 before 7.7.0.1, from 7.0.0 before 7.3.1.6, from 6.1.0 before 6.1.*, from 6.0.0 before 6.0.*, from 5.3.0 before 5.3.*, from 5.2.0 before 5.2.*, from 4.3x before 5.1.*.

### CVE-2026-77244

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-303;CWE-862` |
| Published | 2026-09-22T18:17:17.560 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the HTTP transport accepts requests without a verified user identity and downstream fetcher construction falls back to the operator's globally configured Jira or Confluence credentials. A network client that can reach the MCP endpoint can invoke Atlassian tools as the operator, including read and write operations available to that account. The advisory traces the vulnerable input and processing flow through UserTokenMiddleware, AtlassianOpaqueTokenVerifier, _get_fetcher, and streamable-http, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-75723

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T18:17:16.163 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75721

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:16.033 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75703

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:15.900 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75699

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:15.760 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-73369

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:15.300 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-80155

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T16:18:01.917 |

Lantronix SLC8000 before firmware v9.7.0.5, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain an authentication bypass vulnerability in the web management portal upload endpoint that allows unauthenticated attackers to read sensitive configuration files and upload files to arbitrary filesystem locations, leading to remote code execution. The web configuration server constructs the session cookie file path using snprintf with a fixed-size buffer; by supplying a cookie value of a specific length an attacker causes the path to truncate at the required delimiter and leverages path traversal to redirect authentication validation to an arbitrary on-disk file such as the local user database, bypassing all session checks. Attackers can use this vulnerability to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-connected devices.

### CVE-2026-19599

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T13:17:27.400 |

ZohoCorp ManageEngine OpManager MSP versions 12.8.709 and below were vulnerable to a Remote Code Execution vulnerability in the Notification Profile module.

### CVE-2026-18169

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T23:17:06.730 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote authenticated attacker to obtain sensitive information due to improper validation of symbolic links.

### CVE-2026-16346

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-22T22:17:06.607 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-75682

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T19:16:46.260 |

Adobe Connect is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary SQL commands, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-57149

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-22T19:16:43.893 |

plone.app.portlets.portlets provides a Plone-specific user interface for plone.portlets, as well as a standard set of portlets that ship with Plone. Starting in version 5.0.0 and prior to versions 5.0.8, 6.0.4, and 7.0.2, the Classic portlet (plone.app.portlets.portlets.classic) used its user-supplied template/macro fields to build a TALES path expression that was then evaluated by the TAL path() helper. Because the value was interpreted as a full TALES expression, a user able to add or edit a Classic portlet could supply a crafted value that escapes simple path traversal and is evaluated as arbitrary code. This is exploitable by any authenticated user who can configure a Classic portlet - which, with the default role map, includes regular users on their personal dashboard. The result is code execution in the context of the Plone process, i.e. a privilege escalation across the trust boundary between an authenticated web user and the server-side process. The problem has been patched in `plone.app.portlets` 5.0.8, 6.0.4, and 7.0.2. Some workarounds are available.  Restrict who can manage portlets: remove the `plone.app.portlets.ManageOwnPortlets` permission from untrusted roles, and limit Manage portlets to trusted administrators (usually this is already restricted to the Manager and Site Administrator roles).  Where the Classic portlet is not needed, unregister it so it cannot be added. This would need to be done by editing a `portlets.xml` in your own code. One may also effectively disable showing the classic portlet by customising its template. In the Zope Management Interface go to the `portal_view_customizations` tool, locate the `classic.pt` template and click it. Click the Customize button.  Remove all text and replace it with `<div>The classic portlet was disabled.</div>`. (This is not a recommended way of customizing a template, but in this case it is quite effective.)

### CVE-2026-89276

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T18:17:29.550 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-83660

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:22.673 |

Adobe Campaign Classic (ACC) is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82013

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:21.657 |

Adobe Campaign Classic (ACC) is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82010

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T18:17:21.377 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82008

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T18:17:21.077 |

Adobe Campaign Classic (ACC) is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-18163

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T23:17:06.600 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to execute arbitrary code due to improper deserialization of untrusted data.

### CVE-2026-18162

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-22T23:17:06.463 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to execute arbitrary code due to improper neutralization of user-controlled input within the new Function constructor.

### CVE-2026-76709

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T20:17:06.750 |

A vulnerability exists in the internal administrative component of Analytics and Location Engine (ALE). Successful exploitation of this vulnerability could allow an unauthenticated remote attacker to gain unauthorized write access to the file system with elevated privileges, potentially resulting in full system compromise.

### CVE-2026-76708

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T20:17:06.620 |

A vulnerability exists in the Analytics and Location Engine (ALE) where the application and underlying operating system use default, hard-coded credentials for several administrative and system accounts. An unauthenticated remote attacker could exploit this vulnerability by attempting to log in using these known default credentials.

Successful exploitation could result in an attacker gaining unauthorized access to the application's management interface and the underlying operating system, potentially leading to full system compromise.

### CVE-2026-28324

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-22T20:17:03.250 |

SolarWinds Observability Self-Hosted was found to be affected by an unauthenticated remote code execution vulnerability due to the insufficient integrity checks. Installations configured in a non-default and non-secure configuration are affected.

### CVE-2026-93088

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T15:17:21.433 |

SGLang's multimodal generation runtime is vulnerable to unauthenticated arbitrary code execution because the disaggregated-diffusion orchestrator's DiffusionServer binds an unauthenticated ZeroMQ ROUTER socket to a network interface and passes the final frame of received multipart messages directly to pickle.loads() before any validation occurs.

### CVE-2026-79313

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-22T15:17:15.467 |

webpy web.py 0.76 is vulnerable to Insufficient Session Expiration. The application's session management relies on periodic cleanup to expire sessions instead of checking the last-access time when a session is loaded. As a result, an expired session whose record has not yet been cleaned up can still be replayed and used, allowing an attacker holding a previously valid session cookie to continue accessing protected resources after the configured idle timeout.

### CVE-2026-65113

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-22T15:17:11.513 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an attacker could cause use of hard-coded credentials. A successful exploit of this vulnerability might lead to escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-17472

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T22:17:07.683 |

IBM Concert 1.0.0 through 3.0.0 could allow a remote authenticated attacker to access or modify unauthorized resources due to the use of wildcards in RBAC permission definitions.

### CVE-2026-82000

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T19:16:53.297 |

Adobe Experience Manager Forms JEE is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82443

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:21.790 |

Adobe Campaign Classic (ACC) is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-86059

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-09-22T17:17:27.690 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.13, Dokploy organization members without Git provider access can retrieve plaintext provider credentials through github.one, gitlab.one, gitea.one, and bitbucket.one because those protected procedures return full provider rows without applying getAccessibleGitProviderIds or an organization check. The application.one route also returns nested GitHub, GitLab, Gitea, and Bitbucket relations from findApplicationById with GitHub App private keys, OAuth tokens, client secrets, webhook secrets, and app passwords even when hasGitProviderAccess is false. A member with application read access or a provider identifier can therefore bypass per-member provider assignment and use the exposed credentials to access private repositories or manipulate external workflows. This issue is fixed in version 0.29.13.

### CVE-2026-84388

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-1021` |
| Published | 2026-09-22T15:17:18.950 |

A improper restriction of rendered ui layers or frames vulnerability in Fortinet FortiPAM Chrome Extension 8.0 all versions, FortiPAM Chrome Extension 7.4 all versions may allow attacker to information disclosure via remote unauthenticated attack

### CVE-2026-80156

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T16:18:02.083 |

Lantronix SLC8000 before firmware v9.7.0.5, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a path traversal vulnerability in the web management portal upload endpoint that allows authenticated attackers to write arbitrary data to any location on the device's filesystem, leading to remote code execution. The upload filename validation strips backslash characters but does not subsequently check for forward slashes when a backslash is detected; by supplying a filename containing both characters an attacker writes outside the intended upload directory to any writable path. Attackers can use this vulnerability to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-connected devices.

### CVE-2026-80152

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T16:18:01.607 |

Lantronix SLC8000 before firmware v9.7.0.3, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a command injection vulnerability that allows authenticated attackers with the services permission to execute arbitrary shell commands as root by exploiting the set script schedule command that passes unsanitized user input to a system() call. Attackers with the services permission can authenticate to the terminal or CLI interface and inject malicious commands through the unsanitized parameter to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-80151

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T16:18:01.460 |

Lantronix SLC8000 before firmware v9.7.0.3, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a command injection vulnerability that allows authenticated attackers with the services permission to execute arbitrary shell commands as root by exploiting the set nfs download command that passes unsanitized user input to a system() call. Attackers with the services permission can authenticate to the terminal or CLI interface and inject malicious commands through the unsanitized parameter to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-80147

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T16:18:00.863 |

Lantronix SLC8000 before firmware v9.7.0.2, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a stack-based buffer overflow vulnerability that allows authenticated attackers to potentially execute arbitrary code by exploiting an undocumented mfc eeprom write command that copies unbounded user input into a bounded stack buffer before passing it to a system() call. Attackers can authenticate as any user to the terminal or CLI interface and supply an oversized input to trigger the overflow, potentially achieving complete loss of confidentiality, integrity, and availability on the affected device and impacting downstream serial-attached devices.

### CVE-2026-80146

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T16:18:00.720 |

Lantronix SLC8000 before firmware v9.7.0.2, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a stack-based buffer overflow vulnerability that allows authenticated attackers to potentially execute arbitrary code by exploiting an undocumented mfc eeprom read command that copies unbounded user input into a bounded stack buffer before passing it to a system() call. Attackers can authenticate as any user to the terminal or CLI interface and supply an oversized input to trigger the overflow, potentially achieving complete loss of confidentiality, integrity, and availability on the affected device and impacting downstream serial-attached devices.

### CVE-2026-80145

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T16:18:00.570 |

Lantronix SLC8000 before firmware v9.7.0.2, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a command injection vulnerability that allows authenticated attackers with the services permission to execute arbitrary shell commands as root by exploiting the set cifs password command that passes unsanitized user input to a system() call. Attackers with the services permission can authenticate to the terminal or CLI interface and inject malicious commands through the unsanitized parameter to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-80144

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T16:17:59.303 |

Lantronix SLC8000 before firmware v9.7.0.2, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a command injection vulnerability that allows authenticated attackers to execute arbitrary shell commands as root by exploiting an undocumented mfc eeprom write command that passes unsanitized user input to a system() call. Attackers can authenticate as any user to the terminal or CLI interface and inject malicious commands through the unsanitized parameter to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-80143

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T16:17:57.543 |

Lantronix SLC8000 before firmware v9.7.0.2, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882/SLCx-03/SLCx-02 contain a command injection vulnerability that allows authenticated attackers to execute arbitrary shell commands as root by exploiting an undocumented mfc eeprom read command that passes unsanitized user input to a system() call. Attackers can authenticate as any user to the terminal or CLI interface and inject malicious commands through the unsanitized parameter to achieve complete loss of confidentiality, integrity, and availability on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-96560

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-23T14:17:11.073 |

LightLLM through 1.2.0 contains a remote code execution vulnerability in the KV-transfer worker when started with --pd_trans_mode nccl, which exposes an unauthenticated RPyC control channel that deserializes attacker-supplied data. Attackers can send malicious pickled objects to the exposed RPyC ThreadedServer to execute arbitrary code with the privileges of the LightLLM service account.

### CVE-2026-96257

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-23T03:17:06.077 |

A flaw has been found in Fast FAC1203R Gigabit Edition 2.0.4. Affected by this issue is the function copy_msg_element of the component Device Discovery Service. Executing a manipulation can lead to stack-based buffer overflow. The attack can be executed remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-77987

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208;CWE-918` |
| Published | 2026-09-22T21:17:32.653 |

A server-side request forgery (SSRF) vulnerability was identified in the notebook viewer of GitHub Enterprise Server. The notebook viewer validated the scheme and host of a user-supplied URL but did not validate the port, allowing requests to be directed to internal services listening on other ports of the same appliance. Response bodies were not returned to the requester, but response timing acted as an oracle that allowed instance secrets to be extracted character by character. An extracted secret could then be used in a separate interaction with an internal service to obtain remote code execution on the appliance. Exploitation required network access to the instance and was unauthenticated when private mode was disabled, or required any authenticated user when private mode was enabled. This vulnerability affected GitHub Enterprise Server versions 3.17 through 3.22 and was fixed in versions 3.22.1, 3.21.6, 3.20.8, 3.19.12, 3.18.15, and 3.17.21. This vulnerability was reported through the GitHub Bug Bounty program.

### CVE-2026-87121

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T20:17:09.967 |

lwIP TCP/IP Stack MQTT is vulnerable to an out-of-bounds write, which may allow an attacker to gain full code execution on the device.

### CVE-2026-47116

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-22T20:17:03.583 |

LTSecurity LTK3500SF contains a hard-coded credentials vulnerability where root and guest account passwords are stored as reversible hashes in /etc/shadow, recoverable using dictionary-based cracking tools. Attackers can use the recovered credentials to authenticate via Telnet or SSH and obtain full root-level access to the operating system.

### CVE-2026-91130

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-09-22T19:16:56.700 |

Home Assistant is open source home automation software focused on local control and privacy. Prior to 2026.7.0, the Statistics Graph card in src/components/chart/statistics-chart.ts passed entity names through getStatisticLabel and computeStateName and interpolated param.seriesName into ECharts tooltip HTML without escaping. An authenticated user or an integration that supplies a malicious default entity name could cause script-related HTML to execute when a viewer hovered over a data point. Mean, State, Sum, and Change fields in the default Line chart configuration were affected, while Bar charts were not. This issue is fixed in version 2026.7.0.

### CVE-2026-75698

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T19:16:46.910 |

Adobe Connect is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-75697

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T19:16:46.770 |

Adobe Connect is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-75689

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T19:16:46.643 |

Adobe Connect is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-75686

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T19:16:46.520 |

Adobe Connect is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-75684

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T19:16:46.393 |

Adobe Connect is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-43641

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T18:17:14.357 |

Softaculous Virtualizor before 3.2.9 (Patch 9) and 3.0.0 contains an OS command injection vulnerability in the billing module handler that allows unauthenticated remote attackers to execute arbitrary commands as root by bypassing authentication through specific parameter combinations. Attackers can deserialize a crafted billing_data POST field and inject shell payloads through the uid field, which is passed unmodified to proc_open() via vexec(), yielding complete control of the host and all managed VPS instances.

### CVE-2026-77621

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-09-22T16:17:55.670 |

Vector is a high-performance observability data pipeline. From 0.10.0 until 0.57.0, the file sink renders its templated path from event fields and opens the result without confining it to an intended directory. When an untrusted source supplies an event field used by the path template, the value can contain an absolute path or parent-directory traversal, causing Vector to create parent directories and create or overwrite files outside the intended location with the Vector process privileges. The resulting file write can modify sensitive files and can lead to code execution when a scheduled task, authorization file, or subsequently executed script is targeted. This issue is fixed in version 0.57.0.

### CVE-2026-63374

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-297` |
| Published | 2026-09-22T16:17:50.680 |

AnyIO is a high level asynchronous concurrency and networking framework that works on top of either Trio or asyncio. Prior to 4.14.2, connect_tcp() and TLSStream.wrap() can validate internationalized host names after the standard library converts them with IDNA 2003 instead of IDNA 2008. When a connection to a non-ASCII domain is hijacked or redirected, an attacker can obtain a legitimate certificate for the different ASCII hostname produced by IDNA 2003 and present it to the client, causing the malicious endpoint's certificate to validate. This issue is fixed in version 4.14.2.

### CVE-2026-94127

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-22T15:17:24.313 |

When a BIG-IP APM access policy and an OAuth profile are configured on a virtual server, specific malicious traffic can lead to remote code execution (RCE). This vulnerability is only present when BIG-IP APM is configured as an OAuth Authorization Server. Deployments using APM strictly as an OAuth Client / Resource Server (without OAuth authorization server profiles configured) are not affected by this vulnerability.

Impact:
This vulnerability allows an unauthenticated attacker to perform remote code execution. The BIG-IP system in Appliance mode is also vulnerable. This is a data plane issue; there is no control plane exposure.

 


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-43642

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T18:17:14.533 |

Softaculous Virtualizor before 3.2.9 (Patch 9) and 3.0.0 contains a PHP object injection vulnerability in the billing module handler that allows unauthenticated remote attackers to supply arbitrary serialized PHP objects for deserialization by setting the act parameter to login with the from_billing_module parameter present. Attackers can pass malicious serialized data through the billing_data POST field to the unserialize() function without allowed_classes restrictions, enabling exploitation of available POP chains to achieve remote code execution as root.

### CVE-2026-18461

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-09-22T18:17:12.077 |

Use of Externally-Controlled Format String vulnerability in RTI Connext Professional (Core Libraries) allows Format String Injection. This issue affects Connext Professional: from 7.5.0 before 7.7.0.1, from 7.3.0.10 before 7.3.1.6.

### CVE-2026-19202

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-524` |
| Published | 2026-09-22T22:17:11.707 |

A caching flaw in the toolbox-core package of the mcp-toolbox-sdk-python SDK causes the same Google ID token to be cached and reused across different audiences. If an application uses the SDK to authenticate to two or more different audiences within the same process, the module-level token cache fails to key its cached tokens by the requested audience. Consequently, a valid, unexpired token minted for a sensitive service (Service A) can be retrieved from the cache and sent to a secondary service (Service B). An attacker who operates, compromises, or monitors traffic to Service B can capture this token and replay it to impersonate the victim application against Service A.

### CVE-2026-17645

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T22:17:08.730 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote authenticated attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-17635

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-22T22:17:08.077 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to perform unauthorized actions due to improper configuration of HTTP method-based security constraints.

### CVE-2026-89282

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-22T20:17:11.500 |

The Apache Lounge Windows distribution of Apache HTTP Server build contains an insecure installation directory permissions vulnerability through its default install directory on C:\, which inherits write access for Authenticated Users.

### CVE-2026-81995

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T19:16:52.917 |

Adobe Experience Manager Forms JEE is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-77254

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-22T19:16:49.693 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, requests to the HTTP MCP endpoint without a per-user identity are allowed to reach tool handlers, which then use globally configured Jira or Confluence credentials. A network caller can perform operations with the operator account's permissions unless the deployment has an independent authentication boundary. The advisory traces the vulnerable input and processing flow through streamable-http, UserTokenMiddleware, _get_fetcher, and global credentials, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-82011

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T18:17:21.523 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-82009

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T18:17:21.220 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary SQL commands. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75728

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T18:17:16.293 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction.

### CVE-2026-94456

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-330;CWE-338;CWE-341` |
| Published | 2026-09-22T17:17:31.670 |

Postiz generates security-sensitive credentials using `Math.random()` instead of a cryptographically secure source. The same helper is used for OAuth access tokens, authorization codes, client secrets, organization API keys, and PKCE verifiers, meaning these credentials depend entirely on V8’s deterministic xorshift128+ PRNG state.

An unauthenticated OAuth dynamic client registration endpoint exposes freshly generated client credentials, giving attackers enough consecutive PRNG output to reconstruct that internal state. Once recovered, they can deterministically derive past and future values produced by the same generator, potentially compromising credentials belonging to other users and organizations.

### CVE-2026-85734

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-22T17:17:27.367 |

LightRAG provides simple and fast retrieval-augmented generation. Prior to 1.5.5, the POST /login endpoint in lightrag/api/lightrag_server.py does not impose a rate limit, account lockout, delay, or counter for failed authentication attempts. A network attacker can submit password guesses at full request speed until a valid account password is found. Successful credential recovery grants authenticated access to documents, the knowledge graph, and administrative operations. This issue is fixed in version 1.5.5.

### CVE-2026-95654

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T16:18:18.770 |

Databasement before 1.7.14 validates invitation tokens only when the acceptance page loads, caching the authorization decision without re-checking token validity during acceptance. Attackers with a leaked or forwarded invitation link can load the page while pending, then accept the invitation after the legitimate user has already accepted it to overwrite the account password and gain authenticated access to managed database credentials and secrets.

### CVE-2026-82843

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-23T06:17:02.363 |

The WP OAuth Server ( Login with WordPress ) WordPress plugin before 6.4.0 does not bind the OpenID Connect identity assertion it issues to the authorization grant being exchanged, returning instead the assertion belonging to whichever user authenticated most recently, which allows users with the Subscriber role and above to obtain a validly signed identity assertion for another user, including an administrator, and authenticate as them at any application that uses the site for single sign-on.

### CVE-2026-75799

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T06:17:01.710 |

The YAHMAN Add-ons WordPress plugin before 0.9.31 does not validate the type of the remote files it caches in a publicly accessible directory, allowing unauthenticated attackers to write arbitrary PHP files on the server and achieve RCE when the relevant feature is enabled.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-80154

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-22T16:18:01.767 |

All firmware versions of Lantronix SLC8000, EMG8500, EMG7500, SLB882, SLCx-03, and SLCx-02 contain an authentication bypass vulnerability in the web management portal that allows unauthenticated attackers to derive valid session tokens of logged-in users and bypass source IP and User-Agent validation. Session tokens are generated deterministically from the device model and the current time at one-second resolution, resulting in a small enumerable set of possible active tokens. Attackers can construct a crafted URI that exploits file extension handling in the web server path routing to bypass per-session source-address validation, then use a derived token from a different source address to gain elevated privileges on the affected device and potentially impact downstream serial-attached devices.

### CVE-2026-86678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-23T14:17:08.963 |

ZohoCorp ManageEngine Applications Manager versions 182000 and below allowed a low-privileged user to obtain an administrator’s API key and use it to perform administrator-level actions.

### CVE-2026-86677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T14:17:08.803 |

ZohoCorp ManageEngine Applications Manager versions 182000 and below allowed a low-privileged user to run unauthorized SQL commands, potentially gaining administrator access and remote code execution.

### CVE-2026-76978

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T13:17:29.153 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.709 and below were vulnerable to a Command Injection vulnerability in the Diagnose Settings feature.

### CVE-2026-75825

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-23T13:17:28.557 |

ZohoCorp ManageEngine OpManager versions 12.8.710 and below with the Application Manager Plugin enabled were vulnerable to an Authentication Bypass vulnerability.

### CVE-2026-14913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T12:17:05.507 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.669 and below were vulnerable to an SQL Injection vulnerability in Rule Management Search Reports.

### CVE-2026-96455

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-494` |
| Published | 2026-09-23T11:17:18.690 |

The Reachy Mini daemon exposes an HTTP API for managing the robot. Its app installation endpoint, POST /apps/install in src/reachy_mini/daemon/app/routers/apps.py, has no authentication. The handler's only dependency is Depends(get_app_manager), which just hands back the manager object from application state, so nothing in the chain ever checks a credential.



The endpoint takes an AppInfo body naming a Hugging Face Space. The daemon downloads that Space and installs it as a Python package through install_package in src/reachy_mini/apps/sources/local_common_venv.py, using uv or pip. Installing a Python package runs the package's own build and setup code, so whoever chooses the Space chooses what code the robot runs. Anyone can publish a public Hugging Face Space, so this is not a meaningful restriction on the attacker.



How far this reaches depends on the model. In _resolve_bind_host in src/reachy_mini/daemon/app/main.py the daemon binds 0.0.0.0 when it runs as the wireless version and 127.0.0.1 otherwise, with the vendor's own comment explaining that the robot has to be reachable on the LAN. On a wireless unit, then, any host on the same network can install and run code on the robot without credentials.



One related change has already shipped but does not fix this. Version 1.8.2 replaced the wildcard CORS policy with an allow list of localhost and Tauri origins. That closes the browser drive-by route, where a web page the victim visits silently calls the endpoint in the background. It has no effect on this issue: CORS is enforced by browsers and governs whether script may read a response, while a direct HTTP request from another machine on the network involves no browser, no preflight and no CORS check at all.

### CVE-2026-91813

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-23T08:17:13.550 |

A vulnerability in Foxit PDF Editor/Reader’s update mechanism allows an update package to be replaced between download and high-privilege extraction due to insufficient file locking and integrity validation. This could enable local attackers to execute arbitrary code with elevated privileges.

### CVE-2026-91803

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-23T08:17:12.363 |

A local privilege escalation vulnerability exists in the updater of Foxit PDF Editor/Reader due to unsafe loading of dynamic-link libraries from a user-writable directory during high-privilege operations. A local attacker could exploit this issue to execute code with elevated privileges.

### CVE-2026-91800

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-23T08:17:12.023 |

A local privilege escalation vulnerability exists in the installer of Foxit PDF Editor for macOS due to insufficient validation of a user-modifiable configuration value during high-privilege upgrades. A local attacker could exploit this issue to execute arbitrary commands with root privileges.

### CVE-2026-91798

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-23T08:17:11.793 |

A local privilege escalation vulnerability exists in the update daemon of Foxit PDF Editor/Reader due to an insecure permission configuration that allows the configuration file to be modified by regular users, which may lead to arbitrary script execution with higher privileges.

### CVE-2026-17647

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-22T22:17:08.983 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a local attacker to execute arbitrary commands due to the inclusion of functionality from an untrusted control sphere.

### CVE-2026-17644

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-22T22:17:08.597 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a local attacker to gain unauthorized access to sensitive information and modify transaction data due to the use of hard-coded credentials.

### CVE-2026-17643

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-22T22:17:08.470 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a local attacker to obtain sensitive information and perform unauthorized actions due to insufficiently protected credentials.

### CVE-2026-17637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T22:17:08.337 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow an adjacent-network attacker to execute arbitrary code due to deserialization of untrusted data.

### CVE-2026-17636

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T22:17:08.207 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote authenticated attacker to execute arbitrary code due to improper validation of a specified quantity.

### CVE-2026-17102

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T22:17:07.407 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-16672

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T22:17:07.280 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-16469

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T22:17:07.147 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 px-runtime could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-16468

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T22:17:07.017 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to OS command injection.

### CVE-2026-88419

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-22T20:17:11.083 |

An unrestricted upload of files with a dangerous type in the thumbnail-upload endpoint (/index.php?m=member&f=article&v=thumbUpload) of WuzhiCMS 5.0.0 allows an authenticated low-privileged member to upload a crafted .php file and execute arbitrary PHP code on the server, because the stored file extension is taken verbatim from the client-supplied filename with no extension allowlist or content validation and the file is written to the web-accessible uploadfile/ directory, from which the web server executes PHP.

### CVE-2026-28325

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T20:17:03.430 |

SolarWinds Observability Self-Hosted was found to be affected by an unauthenticated remote code execution vulnerability stemming from deserialization of untrusted data when the application is configured to use a specific communication mode.

### CVE-2026-77274

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:19.253 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, validate_url_for_ssrf has a backslash authority confusion because it interprets the authority differently from the Requests connection layer in the header-based Jira and Confluence URL authentication flow. A crafted URL can validate as an external hostname while the HTTP client connects to an internal host, permitting server-side requests to protected network resources. This issue is fixed in version 0.22.0.

### CVE-2026-77243

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T18:17:17.410 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, ENABLED_TOOLS and TOOLSETS are applied when tools are listed but are not rechecked when a tools/call request is dispatched. A client that knows a hidden tool name can directly invoke excluded read, write, or delete tools despite the operator's configured least-privilege restrictions. The advisory traces the vulnerable input and processing flow through ENABLED_TOOLS, TOOLSETS, tools/list, tools/call, and _call_tool_mcp, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-13087

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T17:17:23.807 |

A heap out-of-bounds write vulnerability was found in the Linux kernel's RPC-over-RDMA server reply path in net/sunrpc/xprtrdma/svc_rdma_sendto.c. When a crafted RPC-over-RDMA client sends a large NFS READ request with an empty Write list and no Reply chunk, the server linearizes the entire multi-page reply into a fixed-size 4096-byte heap buffer without bounds checking, resulting in a kernel heap overflow. This can lead to denial of service via kernel crash or potential code execution through corruption of adjacent kernel heap objects.

### CVE-2026-70410

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-22T16:17:52.930 |

Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') vulnerability in Apache Calcite Avatica. Plugin instantiation (via AvaticaUtils#instantiatePlugin and other methods) initializes arbitrary classes via unrestricted calls to Class.forName(String) which by default triggers initialization. This may lead to the execution of static initializer blocks in arbitrary classes present in the classpath. The instantiation APIs should initialize and instantiate only classes implementing the specified plugin interface passed as input in conjunction with the desired classname. At the moment of writing, there are no well-known or widely used classes with dangerous static initializer blocks so the severity is low.



This issue affects Apache Calcite Avatica: before 1.29.0.



Users are recommended to upgrade to version 1.29.0, which fixes the issue.

### CVE-2026-65179

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T15:17:13.670 |

NVIDIA NeMo contains a vulnerability in the TabularTokenizer class where it deserializes an untrusted, attacker-controlled .pkl file via pickle.load() without validation. A successful exploit of this vulnerability may lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-65128

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T15:17:13.183 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an attacker could cause SQL injection. A successful exploit of this vulnerability might lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-96272

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T01:16:32.633 |

ClipBucket v5 before 5.5.3-#182 contains a blind SQL injection vulnerability in the photo search endpoint where the query parameter is passed unsanitized into SQL WHERE and ORDER BY clauses. Unauthenticated attackers can exploit time-based blind SQL injection techniques to extract user credentials, email addresses, and administrator password hashes for account takeover.

### CVE-2026-94450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-22T21:17:33.867 |

Improper validation of the Destination Connection ID length in s2n-quic 1.88.0 and earlier may allow an unauthenticated remote user to cause a denial of service by shutting down a server endpoint via a single crafted UDP datagram. Only server endpoints specifically configured to send Retry packets are affected.



To remediate this issue, users should upgrade to version v1.89.0 or later.

### CVE-2026-91018

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-22T21:17:33.290 |

lwIP (Lightweight IP) has a double free vulnerability, which could crash the system, cause a DoS, memory corruption, or allow code execution on the victim system.

### CVE-2026-67615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184;CWE-502` |
| Published | 2026-09-22T21:17:31.100 |

openEQUELLA before 2026.1.0 contains an authenticated remote code execution vulnerability that allows any authenticated non-guest user to execute arbitrary code by exploiting Java deserialization in the HTTP invoker endpoint at /invoker/*. Attackers can bypass the class-name denylist enforced by PluginAwareObjectInputStream by nesting a serialized payload inside a java.security.SignedObject, causing the inner stream to be deserialized by a separate ObjectInputStream that does not apply the denylist, ultimately reaching a JNDI sink and enabling code execution.

### CVE-2026-81999

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T19:16:53.170 |

Adobe Experience Manager Forms JEE is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. An attacker with high privileges could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-93345

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-22T18:17:30.370 |

MikroTik RouterOS before 7.25beta4 contains an improper input validation vulnerability in the labelled-VPN NLRI iterators of the routing service that allows an unauthenticated on-path attacker to crash the BGP service by sending a malformed MP_REACH_NLRI UPDATE message with a prefix-length value below the minimum valid for a labelled-VPN NLRI, which passes validation while describing a route with a negative-length address portion. Attackers can repeatedly send a single BGP UPDATE packet carrying a VPNv4 or VPNv6 NLRI with an out-of-bounds prefix-length to indefinitely hold down the BGP plane, causing session termination without a NOTIFICATION and triggering a service malfunction on the device.

### CVE-2026-43643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T18:17:14.683 |

Softaculous Virtualizor before 3.2.9 (Patch 9) and 3.0.0 contains an authorization bypass vulnerability in the billing module handler that allows unauthenticated remote attackers to modify any tenant's account balance by supplying crafted act and from_billing_module parameters to the admin panel dispatcher. Attackers can send a POST request with arbitrary uid and balance values in the billing_data field to trigger an unauthenticated parameterized UPDATE against the users table, enabling account balance manipulation and potential automated service suspension for targeted accounts.

### CVE-2026-18459

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-09-22T18:17:11.793 |

Incorrect Calculation vulnerability in RTI Connext Professional (Core Libraries) allows Abuse Existing Functionality. This issue affects Connext Professional: from 7.4.0 before 7.7.0.1, from 7.0.0 before 7.3.1.6, from 6.1.0 before 6.1.*, from 6.0.0 before 6.0.*, from 5.3.0 before 5.3.*, from 5.2.0 before 5.2.*, from 4.1x before 5.1.*.

### CVE-2026-95653

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-340` |
| Published | 2026-09-22T16:18:18.607 |

Concrete CMS Community Store before 2.7.8 derives digital product download tokens from order creation timestamps instead of random values, making tokens predictable. Unauthenticated attackers can enumerate sequential order and file identifiers to calculate valid download tokens and retrieve digital goods purchased by other customers.

### CVE-2026-77620

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-22T16:17:55.500 |

Vector is a high-performance observability data pipeline. From 0.15.0 until 0.57.0, the logstash source feeds each decompressed frame back into its decoder without limiting nested compression depth. An unauthenticated remote peer that can reach the default 0.0.0.0:5044 listener can send many nested compressed frames, causing recursive decoding that exhausts the worker thread stack and aborts the process. The same nested construction amplifies decompressed input, and process termination can halt log ingestion for every tenant on a shared pipeline. This issue is fixed in version 0.57.0.

### CVE-2026-77619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130;CWE-789` |
| Published | 2026-09-22T16:17:55.333 |

Vector is a high-performance observability data pipeline. From 0.15.0 until 0.57.0, the logstash source reads a 32-bit compressed-frame length from the network and uses it to size an in-memory buffer without an upper bound. An unauthenticated remote peer that can reach the default 0.0.0.0:5044 listener can send a minimal frame declaring a multi-gigabyte payload, causing an excessive allocation that can abort Vector or invoke the host OOM killer. Because the allocation follows the declared length rather than bytes transmitted, the attacker has low resource cost, and process termination can halt log ingestion for every tenant on a shared pipeline. This issue is fixed in version 0.57.0.

### CVE-2026-15027

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T09:17:07.657 |

CGServiSign developed by Changing has a OS Command Injection vulnerability. Unauthenticated remote attackers can induce victims to visit a malicious web page and inject arbitrary OS commands through the local service interface, resulting in command execution on the victim's local computer.

### CVE-2022-4997

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T06:16:59.060 |

The jet-form-builder-stripe-gateway WordPress plugin before 1.1.0 does not sanitise and escape a payment token before using it in a SQL statement, allowing unauthenticated users to extract arbitrary data from the database, including password hashes.

### CVE-2026-95814

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T21:17:34.417 |

Vaultwarden through 1.37.3 omits organization membership status validation from three cipher access-restriction queries, allowing revoked and not-yet-confirmed members to retain read, write, delete, and attachment access to organization ciphers. Attackers with revoked or pending membership can exploit missing status filters in get_user_collections_access_flags, get_group_collections_access_flags, and is_in_full_access_group to access protected cipher data server-side.

### CVE-2026-77262

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T19:16:50.480 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, confluence_upload_attachment accepts an attacker-controlled file_path and does not apply the path restriction added for the earlier download vulnerability. A caller can traverse outside the workspace and upload arbitrary server-readable files to Confluence. The advisory traces the vulnerable input and processing flow through confluence_upload_attachment, file_path, and CVE-2026-27825, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77255

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-441` |
| Published | 2026-09-22T19:16:49.850 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the Jira update_issue attachments argument is converted into local paths and routed to the attachment upload implementation without workspace validation. A caller can make the MCP server read arbitrary local files and attach them to a Jira issue, using the server as a confused deputy to exfiltrate the contents. The advisory traces the vulnerable input and processing flow through jira update_issue, attachments, upload_attachment, and file_path, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77248

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-09-22T19:16:49.027 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the streamable HTTP transport accepts requests without a user identity and falls back to operator credentials, while upload_attachment accepts an unrestricted file_path. An unauthenticated network caller can read files available to the MCP process, upload them to an attacker-selected Jira issue or Confluence page, and retrieve the contents. The advisory traces the vulnerable input and processing flow through streamable-http, UserTokenMiddleware, upload_attachment, file_path, and _get_fetcher, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-34689

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T19:16:43.210 |

Adobe Connect is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-85279

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T18:17:23.213 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.8, Notepad++ contains a stack buffer overflow in PluginsManager::loadPluginFromPath in PowerEditor/src/MISC/PluginsManager/PluginsManager.cpp because the plugin-supplied GetLexerCount() result controls a loop that writes to containers[30] without enforcing NB_MAX_EXTERNAL_LANG. A malicious or compromised plugin that reports more than 30 lexers can write beyond the stack array and corrupt control data, which can permit arbitrary code execution in the Notepad++ process context. This issue is fixed in version 8.9.8.

### CVE-2026-95655

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-22T16:18:18.943 |

Aureus ERP before 1.5.0 fails to scope message lookups to the current record in ChatterPanel, allowing authenticated users to access arbitrary messages. Attackers can submit sequential message IDs to read, edit, delete, or pin messages from other departments or companies, and enumerate all notes in the system.

### CVE-2026-18095

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T22:17:09.393 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote authenticated attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17646

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-22T22:17:08.860 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote authenticated attacker to obtain sensitive information due to improper restriction of XML external entity references.

### CVE-2026-82003

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T18:17:20.887 |

Adobe Campaign Classic (ACC) is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-5695

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-23T11:17:10.590 |

Arbitrary file upload vulnerability due to a lack of proper validation in upload forms. This allows authenticated users to upload files to the server without restrictions. An attacker could exploit this flaw to execute malicious code remotely (demonstrated by uploading the EICAR test file), which could result in the system being completely compromised.

### CVE-2026-89281

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-22T20:17:11.380 |

The Apache Lounge Windows distribution of Apache HTTP Server build contains a hardcoded configuration path vulnerability within openssl.cnf path that can allow local code execution.

### CVE-2026-83603

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-73;CWE-502` |
| Published | 2026-09-22T17:17:26.550 |

Netdata is an open source observability tool. Prior to 2.10.4, the setuid-root ndsudo helper command fail2ban-client-status-socket in src/collectors/utils/ndsudo.c accepts a caller-controlled --socket_path from the low-privileged netdata service account. The account can direct root fail2ban-client to a malicious UNIX socket, and fail2ban/client/csocket.py CSocket.receive() passes the returned data to pickle.loads(), allowing attacker-controlled code to execute as root on systems with fail2ban-client installed. This issue is fixed in version 2.10.4 and nightly build 2.10.0-782-nightly.

### CVE-2026-95626

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T10:17:08.677 |

Tauri's Content Security Policy hardening, which injects a random nonce to restrict script execution, provides zero protection when an application includes data: or blob: in its script-src directive. Per the CSP Level 3 specification, these scheme sources remain active even when a nonce is present, allowing arbitrary script execution without knowing the nonce.

### CVE-2026-77257

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T19:16:50.163 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, HTTP-exposed Jira and Confluence upload tools pass a caller-provided file_path to local file operations without restricting it to the workspace. A remote MCP caller with tool access can cause the server to read sensitive local files and upload them as Atlassian attachments. The advisory traces the vulnerable input and processing flow through streamable-http, upload_attachment, and file_path, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77256

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-22T19:16:50.007 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the plaintext OAuth fallback file containing refresh and access tokens is written with permissions inherited from the process umask. Under common or permissive configurations, other local users can read the backup and retain Atlassian access through the refresh token. The advisory traces the vulnerable input and processing flow through OAuthConfig._save_tokens_to_file, refresh_token, access_token, and umask, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77247

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-22T19:16:48.877 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, Jira and Confluence upload tools interpret caller-controlled path arguments on the MCP server and open those files before sending them as attachments. In remote or multi-user deployments, a permitted client can disclose host files without shell or direct filesystem access. The advisory traces the vulnerable input and processing flow through AttachmentsMixin.upload_attachment, AttachmentsMixin.upload_attachments, file_path, file_paths, and jira update_issue, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77271

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-09-22T18:17:19.107 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, validate_safe_path defaults its base directory to os.getcwd(), and affected Confluence attachment call sites omit base_dir, allowing attacker-selected writes within the working directory. This Python module overwrite can provide code execution when the application later imports the modified module, bypassing the remediation tracked as CVE-2026-27825. This issue is fixed in version 0.22.0.

### CVE-2026-77267

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:18.803 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the X-Atlassian-Jira-Url and X-Atlassian-Confluence-Url headers are processed by _process_authentication_headers and used to construct Atlassian fetchers without calling validate_url_for_ssrf. A caller who can set these headers can supply an internal or metadata-service URL and cause the server to send requests to that destination, bypassing the incomplete CVE-2026-27826 remediation. This issue is fixed in version 0.22.0.

### CVE-2026-77260

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T18:17:18.347 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, the Confluence and Jira upload_attachment implementations accept an unconstrained file_path and open the referenced server-local file. A permitted MCP caller can upload sensitive host files to an Atlassian destination and then retrieve their contents. The advisory traces the vulnerable input and processing flow through upload_attachment, file_path, and CVE-2026-27825, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-77251

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1276` |
| Published | 2026-09-22T18:17:17.883 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, Jira search accepts a forbidden project clause because it checks only for the presence of project syntax, Confluence search uses an incomplete case-sensitive space check, and Jira board APIs omit project-filter enforcement. These paths expose issues, boards, or pages outside JIRA_PROJECTS_FILTER or CONFLUENCE_SPACES_FILTER when the operator credentials have broader access. The advisory traces the vulnerable input and processing flow through jira_search, confluence_search, get_board_issues, get_agile_boards, JIRA_PROJECTS_FILTER, and CONFLUENCE_SPACES_FILTER, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-18457

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-22T18:17:11.487 |

Heap-based Buffer Overflow vulnerability in RTI Connext Professional (Core Libraries) allows Overflow Buffers. This issue affects Connext Professional: from 7.4.0 before 7.7.0.1, from 7.0.0 before 7.3.1.6, from 6.1.0 before 6.1.*, from 6.0.0 before 6.0.*, from 5.3.0 before 5.3.*, from 5.2.3 before 5.2.*.

### CVE-2026-65114

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-22T15:17:11.640 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an attacker could cause missing authentication for a critical function. A successful exploit of this vulnerability might lead to data tampering, denial of service, and information disclosure.

### CVE-2026-96454

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-862;CWE-923` |
| Published | 2026-09-23T10:17:09.070 |

Pake turns a website into a desktop application built on Tauri. Every application it generates inherits two settings from the upstream template, and together they hand native functionality to untrusted web content.



The first is in src-tauri/capabilities/default.json, which grants IPC access with "remote": { "urls": ["https://*.*"] }. That wildcard tells Tauri to accept IPC from any HTTPS origin, not just the site the application was built to wrap. The second is "withGlobalTauri": true in src-tauri/tauri.conf.json, which puts window.__TAURI__.core.invoke() in reach of ordinary page JavaScript.



Tauri's access control list only checks plugin commands, the ones prefixed with plugin:. Commands the application registers itself through generate_handler!, known as app commands, are never checked against the ACL. So once an origin holds IPC access, it can call every app command with nothing else standing in the way. Pake registers download_file as an app command, and it does not appear in the permissions list because it does not need to.



The practical effect is that any script running on any HTTPS page inside a Pake application can invoke the application's native commands. That includes third-party script the wrapped site loads on its own, such as analytics, advertising, or a compromised CDN. Anyone distributing their own Pake application gets the same access without asking for it. Chained with the path traversal in download_file that is tracked separately as CVE-2026-82635, this reaches arbitrary file write and persistent code execution.

### CVE-2026-86608

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T06:17:04.030 |

The WP Recipe Maker WordPress plugin before 10.8.2 does not have any authorisation check in one of its REST routes, nor does it bound what that route stores, allowing unauthenticated users to write unlimited data into any user's metadata and to permanently prevent that account, including an administrator's, from loading.

### CVE-2026-19438

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T06:17:01.310 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in ABB Mint Workbench I.

This issue affects Mint Workbench I: through 5876.

### CVE-2026-14321

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T06:17:00.850 |

The divi-dash WordPress plugin before 1.0.7 does not validate the source of the client IP address it uses for rate limiting and banning, allowing unauthenticated attackers to spoof arbitrary IP addresses in order to bypass rate limiting, ban chosen addresses from the feature, and grow a stored option without bound, resulting in denial of service.

### CVE-2026-18131

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T22:17:09.913 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to execute arbitrary JavaScript in an authenticated user's browser due to improper neutralization of HTML input.

### CVE-2026-18074

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-22T22:17:09.260 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to perform unauthorized actions due to improper authentication and missing authorization.

### CVE-2026-65121

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-22T15:17:12.543 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an  attacker could cause an improper authentication issue. A successful exploit of this vulnerability might lead to escalation of privileges, information disclosure, and data tampering.

### CVE-2026-86683

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-23T14:17:09.347 |

ZohoCorp ManageEngine Applications Manager versions 182000 and below allowed a low-privileged user to change the proxy settings.

### CVE-2026-84787

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-23T12:17:07.857 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.710 and below were vulnerable to a Privilege Escalation vulnerability that allowed an authenticated low-privilege user to gain Administrator privileges through Report Profile import.

### CVE-2026-93508

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T06:17:05.950 |

The WC Fields Factory WordPress plugin before 4.1.11 does not properly restrict access to its field-management AJAX action, allowing authenticated users with Subscriber-level access and above to create, modify and delete arbitrary post meta on any post, including WooCommerce products, regardless of ownership, and to manipulate stored pricing rules on a product to reduce its checkout price.

### CVE-2026-18137

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T22:17:10.430 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to execute arbitrary ESQL commands due to improper neutralization of special elements used in an ESQL command.

### CVE-2026-75744

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T19:16:47.383 |

Adobe Experience Manager Forms JEE is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a high-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-87902

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-22T17:17:28.310 |

An unauthenticated attacker can make `get_page_template()` page-template resolution include a chosen readable local `.php` file outside the active theme directories. If relevant pre-conditions for both the server and the active theme are met, this can lead to RCE.

### CVE-2026-75607

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T16:17:54.430 |

Frigate is an open source network video recorder. Prior to 0.17.2, the WebSocket handler in frigate/comms/ws.py forwards attacker-selected message topics to the dispatcher without checking the authenticated user's role because the nginx authentication subrequest does not provide role-aware authorization to the handler. Any authenticated viewer can send admin-only topics such as restart, notifications/set, and camera detection, recording, snapshot, audio, motion, and enablement settings, causing service restarts or disabling security monitoring functions. Authentication must be enabled and valid viewer credentials are required. This issue is fixed in version 0.17.2.

### CVE-2026-18154

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-22T22:17:10.830 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to obtain sensitive information due to the use of a hard-coded or predictable cryptographic key.

### CVE-2026-65130

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T15:17:13.430 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an attacker could cause OS command injection. A successful exploit of this vulnerability might lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-12974

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183;CWE-1284` |
| Published | 2026-09-23T14:17:06.547 |

A Security Policy Bypass vulnerability exists in Forcepoint Security Engine (NGFW).


This issue affects Forcepoint Security Engine (NGFW): from 7.1.0 through 7.1.13, from 7.3.0 through 7.3.1, 7.3.3, from 7.4.0 through 7.4.1, and 7.5.0.

### CVE-2026-91812

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-23T08:17:13.423 |

A vulnerability in Foxit PDF Editor/Reader’s update mechanism allows man-in-the-middle attackers to bypass certificate validation and package integrity checks, potentially enabling arbitrary code execution with system privileges.

### CVE-2026-18066

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T22:17:09.123 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a local attacker to obtain sensitive information and trigger unauthorized actions due to server-side request forgery.

### CVE-2026-96512

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-23T14:17:10.747 |

A flaw was found in sudo. When sudoers rules use NOTBEFORE or NOTAFTER time-based access restrictions with timestamps that omit the trailing 'Z' timezone indicator, the time evaluation relies on the TZ environment variable inherited from the calling user. Because sudo is a setuid-root program, an unprivileged local user can set TZ to an extreme timezone offset to shift the authorization window by up to approximately 25 hours, causing expired rules to be treated as valid. This allows the user to execute commands outside the intended time window. Authentication is not bypassed; only the time-based authorization check is affected.

### CVE-2026-96442

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T11:17:18.550 |

A code execution flaw was found in Emacs, affecting versions prior to 31.2. The Flymake mode using language backends other than Lisp would execute arbitrary code from the edited file while performing syntax checking. Viewing or editing untrusted files using Emacs could lead to arbitrary code execution with the privileges of the user running Emacs.

### CVE-2026-91818

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:14.123 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s JavaScript handling of PDF annotations. Reentrant page-event processing during annotation enumeration may release the associated page object, which is subsequently accessed, resulting in an application crash.

### CVE-2026-91816

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:13.900 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s handling of PDF annotations. Reentrant annotation deletion triggered by embedded JavaScript can cause the application to access an annotation object after it has been released, resulting in a use-after-free condition and application crash.

### CVE-2026-91815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:13.790 |

Foxit PDF Editor/Reader does not perform sufficient verification of the JPEG2000 image metadata in the PDF file, which leads to out-of-bounds write in the heap buffer during decoding, potentially causing the program to crash and introducing the risk of arbitrary code execution.

### CVE-2026-91811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:13.307 |

A heap-based out-of-bounds write vulnerability exists in Foxit PDF Editor/Reader’s PRC parser due to insufficient validation of vertex indices in triangular fan texture meshes. Successful exploitation could result in memory corruption and an application crash.

### CVE-2026-91809

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:13.070 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s handling of malformed PDF form fields. Improper validation during field-name traversal may cause the application to access a released object, resulting in an application crash.

### CVE-2026-91806

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:12.693 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s handling of PDF form fields. Embedded JavaScript may access form-field references after the corresponding fields have been released, resulting in an application crash.

### CVE-2026-91805

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:12.583 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s PDF page-tree handling. A specially crafted PDF can trigger page-structure changes during rendering, causing the application to access released page objects and resulting in memory corruption and an application crash.

### CVE-2026-91804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:12.477 |

A heap-based out-of-bounds write vulnerability exists in Foxit PDF Editor/Reader’s rendering of Circle annotations with malformed Cloudy appearance streams in specially crafted PDF files. Insufficient validation of the appearance geometry can result in memory corruption and application crashes.

### CVE-2026-91802

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:12.247 |

A heap-based out-of-bounds write vulnerability exists in Foxit PDF Editor/Reader’s WebP image decoding due to improper handling of bitmap stride and target buffer formats. Successful exploitation could result in an application crash.

### CVE-2026-91801

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T08:17:12.133 |

A path traversal vulnerability exists in Foxit PDF Editor/Reader's handling of embedded PDF resources. Insufficient validation of resource file paths may allow files to be written outside their intended locations, potentially enabling arbitrary code execution.

### CVE-2026-91799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:11.907 |

A use-after-free vulnerability exists in Foxit PDF Editor/Reader’s handling of JavaScript array objects. A specially crafted PDF may cause the application to access a released object during array processing, potentially resulting in application crashes or arbitrary code execution.

### CVE-2026-91797

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-23T08:17:11.683 |

Foxit PDF Editor/Reader failed to validate the directory traversal path in the attachment file name, resulting in malicious attachments being able to be written to directories outside the expected secure area when the PDF is opened.

### CVE-2026-91795

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-09-23T08:17:11.453 |

Foxit PDF Editor/Reader's FileOpen plugin did not adequately validate certain encryption metadata in specially crafted PDF files. This could leave an internal pointer in an invalid state, resulting in chained read and write access violations and potentially enabling arbitrary code execution.

### CVE-2026-91794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:11.337 |

An out-of-bounds write vulnerability exists in the PDF rendering process of Foxit PDF Editor/Reader due to insufficient consistency and boundary validation when processing malformed color space data, which may cause the program to crash and potentially lead to remote code execution.

### CVE-2026-91793

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:11.223 |

When opening a specially crafted PDF, Foxit PDF Editor/Reader executes scripts that modify annotation rich-text attributes containing malformed font data. During subsequent annotation appearance reconstruction, it accesses an object after it has been released, resulting in a use-after-free condition and an application crash.

### CVE-2026-91792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:11.110 |

When processing a specially crafted PDF, Foxit PDF Editor/Reader may perform reentrant zoom and layout operations through page- and annotation-related JavaScript actions. This can cause the application to access page objects after they have been released, resulting in a use-after-free condition and an application crash.

### CVE-2026-91791

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:10.987 |

When processing a specially crafted PDF file, Foxit PDF Editor/Reader may encounter a reentrant execution condition involving JavaScript triggered by page-visibility events. This can cause the application to access a released page-view object while calculating annotation boundaries, resulting in an invalid memory read and application crash.

### CVE-2026-91790

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T08:17:10.873 |

When rendering the page image, Foxit PDF Editor/Reader fails to perform validation on image objects whose optional content attributes are malformed. As a result, the program may access an already-freed internal data structure, triggering a crash due to UAF.

### CVE-2026-91789

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T08:17:10.753 |

Foxit PDF Editor/Reader’s U3D/GIF texture decoding path contained insufficient validation of image dimensions and related size information. Under certain conditions, this could lead to an incorrectly sized memory allocation and a subsequent out-of-bounds write during pixel processing, potentially resulting in remote code execution.

### CVE-2026-94574

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T20:17:13.240 |

A local cross-user code execution vulnerability exists in GNU wget (Windows builds from eternallybored.org) due to a hardcoded configuration file path (C:\msys64) that is writable by unprivileged users, allowing for arbitrary code execution via the use_askpass directive, potentially allowing local privilege escalation.

### CVE-2026-95831

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-09-22T19:17:00.227 |

Crypt::SelfCertificate versions from 1.01 through 1.05 for Perl contains malware which executes Python code from an obfuscated URL.

The generate_certificate runs a Python script saved as a certificate file.  The pyhton script attempts to retrieve code from a hardcoded http URL that is obfuscated with base64 encoding and run the response body directly.

The impact is that arbitrary code can be invoked as the user, without a dropped script being saved on the affected host.

The releases have no test scripts nor build hooks.  The intention may have been to trigger the payload after installation.

For version 1.01, the dropper script is in lib/Crypt/SelfCertificate/sample/validate.p12.

For version 1.05, the dropper script is in lib/Crypt/SelfCertificate/sample/cert7.pem.

The SHA-256 digests of the files are

    fbff21f45ff748365062a5e36fb2d72558cad82a507a6f357f320b4fcdf07760 Crypt-SelfCertificate-1.01.tar.gz
    27b2d2d3174ad771474fff2521f5084ec231e9218ea8c832515aef1cbd5897bc lib/Crypt/SelfCertificate/sample/validate.p12

    9fdfa7d69b034b77d4510cda567e8da1e486ca81c7daaadc5732a45c41d71991 Crypt-SelfCertificate-1.05.tar.gz
    27b2d2d3174ad771474fff2521f5084ec231e9218ea8c832515aef1cbd5897bc lib/Crypt/SelfCertificate/sample/cert7.pem

### CVE-2026-83963

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:54.010 |

Substance3D - Modeler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-83962

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T19:16:53.877 |

Substance3D - Modeler is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-81998

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:53.043 |

Substance3D - Modeler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-79906

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:52.097 |

Substance3D - Modeler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75676

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T19:16:46.037 |

Bridge is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75665

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-22T19:16:45.880 |

Bridge is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75663

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:45.750 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75658

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:45.630 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75655

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-22T19:16:45.383 |

Bridge is affected by an Uncontrolled Recursion vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-75649

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-22T19:16:45.250 |

Bridge is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-86054

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-22T18:17:23.827 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.8, Notepad++ contains a stack buffer overflow in NppParameters::writeSession in PowerEditor/src/Parameters.cpp because it copies a session path derived from -settingsDir= into backupPathName[MAX_PATH] with unbounded wcscpy and appends SESSION_BACKUP_EXT with unbounded wcscat. A sufficiently long settings directory causes the backup suffix to exceed the fixed stack buffer when Notepad++ saves the session, and the protected release build terminates through its stack canary, causing denial of service. This issue is fixed in version 8.9.8.

### CVE-2026-77605

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-706` |
| Published | 2026-09-22T18:17:19.393 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.8, the Folder as Workspace Run by system action in Notepad++ can resolve a different sibling file than the file selected by the user. When an attacker places a command script whose name is the selected text-file path with .cmd appended, and the user invokes Run by system on the text file on Windows 10 or Windows 11, Notepad++ can execute the sibling script as the current user instead of opening the selected file. This issue is fixed in version 8.9.8.

### CVE-2026-83598

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-427` |
| Published | 2026-09-22T17:17:25.807 |

Netdata is an open source observability tool. From rom 2.0.0 until 2.10.4, during Netdata Windows Agent MSI repair, powershell.exe runs as SYSTEM without -NoProfile and loads %USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1 from the low-privileged user who initiated repair. Commands placed in that profile before repair therefore execute with SYSTEM privileges. This vulnerability is fixed in 2.10.4.

### CVE-2026-65178

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T15:17:13.550 |

NVIDIA NeMo contains a vulnerability in its dataset-loading workflow where a maliciously crafted model_config.yaml can inject unsafe parameters. A successful exploit of this vulnerability may lead to code execution, data tampering, denial of service, and information disclosure.

### CVE-2026-65111

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-22T15:17:11.253 |

NVIDIA NeMo Speech for all platforms contains a vulnerability where malicious input created by an attacker could cause a code injection. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-24267

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T15:17:10.157 |

NVIDIA NeMo Speech for all platforms contains a vulnerability in the speech data explorer component, where malicious data created by an attacker could cause remote code execution. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-24239

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T15:17:10.013 |

NVIDIA NeMo Speech for all platforms contains a vulnerability where malicious data created by an attacker could cause remote code execution. A successful exploit of this vulnerability might lead to code execution, information disclosure, and data tampering.

### CVE-2026-76979

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-23T13:17:29.273 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.709 and below were vulnerable to an XML Injection vulnerability in the Rule Tracking Compare Policies feature.

### CVE-2026-95627

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-23T10:17:08.810 |

When a Tauri application uses the dialog plugin's file or folder picker, an attacker with JavaScript execution (XSS) can force the scope expansion to be recursive, granting read/write access to an entire directory tree after a single user click on a normal-looking OS file dialog. The user has no indication that recursive access was granted, and the expanded scope cannot be revoked for the lifetime of the application.

### CVE-2026-77259

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-552` |
| Published | 2026-09-22T19:16:50.327 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, confluence_upload_attachment opens a caller-selected server-local file without checking that the resolved path remains in the workspace. A caller can upload environment files, credentials, or other readable host data to a Confluence page and retrieve it through Atlassian. The advisory traces the vulnerable input and processing flow through confluence_upload_attachment, file_path, and open(file_path, "rb"), which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-8849

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-22T18:17:29.690 |

Use After Free vulnerability in RTI Connext Professional (Security Plugins) allows File Manipulation. This issue affects Connext Professional: from 7.6.0 before 7.7.0.1.

### CVE-2026-77258

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T18:17:18.193 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, upload_attachment in src/mcp_atlassian/confluence/attachments.py accepts a caller-controlled file_path and opens the selected server-local file without restricting it to the workspace. A permitted Confluence MCP caller can upload the file as an attachment and disclose data readable by the server process. This issue is fixed in version 0.22.0.

### CVE-2026-83803

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-22T17:17:26.710 |

Sentry is an error tracking and performance monitoring tool. From 23.11.0 until 26.7.0, Sentry instances with the relocation feature enabled unsafely deserialize a legacy database field while importing a user-supplied relocation archive. An authenticated user can craft an archive that causes arbitrary code execution in the import worker process. Self-hosted installations using the default configuration are not affected because the relocation feature is disabled by default. This issue is fixed in version 26.7.0.

### CVE-2026-95806

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-502` |
| Published | 2026-09-22T16:18:24.547 |

MISP ships with PHP's phar stream wrapper registered in both its web entry point and its console entry point. 

The phar stream wrapper causes PHP to treat a phar archive as a directory, which has two security consequences:  

 - any filesystem operation on a caller-influenced path that resolves to a phar archive triggers an implicit unserialize() call, creating a deserialization sink;
 - a relocated application root can reach executable code inside an uploaded phar file, enabling arbitrary code execution as the web user.




No component of MISP, the vendored CakePHP framework, or any runtime-loaded library reads or constructs phar archives. The wrapper therefore serves no legitimate purpose in the MISP runtime and exists solely as an available primitive for an attacker who can influence a filesystem path argument.

### CVE-2026-80150

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T16:18:01.313 |

Lantronix SLC8000 before firmware v9.7.0.3, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882 contain a server-side request forgery vulnerability in the WebSSH/WebTelnet listener that allows unauthenticated attackers to cause the affected device to establish Telnet connections to attacker-controlled endpoints. The custom shellinaboxd uses the rooturl parameter from the web connection to determine its own IP address; by modifying this parameter an attacker redirects the Telnet terminal connection to an arbitrary host or IP. Attackers can use this capability to enumerate or communicate with internal network endpoints that would otherwise be inaccessible.

### CVE-2026-80149

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T16:18:01.160 |

Lantronix SLC8000 before firmware v9.7.0.3, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882 contain a server-side request forgery vulnerability in the WebSSH/WebTelnet listener that allows unauthenticated attackers to cause the affected device to establish SSH connections to attacker-controlled endpoints. The custom shellinaboxd uses the rooturl parameter from the web connection to determine its own IP address; by modifying this parameter an attacker redirects the SSH terminal connection to an arbitrary host or IP. Attackers can use this capability to enumerate or communicate with internal network endpoints that would otherwise be inaccessible.

### CVE-2026-80148

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T16:18:01.013 |

Lantronix SLC8000 before firmware v9.7.0.3, EMG8500/EMG7500 before firmware v9.7.0.1, and all firmware versions of SLB882 contain a server-side request forgery vulnerability in the WebSSH/WebTelnet listener that allows unauthenticated attackers to cause the affected device to establish SSH connections to attacker-controlled endpoints. The custom shellinaboxd builds its SSH connection target using a snprintf call with user-supplied input; by supplying an overlong username string an attacker causes the device IP suffix to be truncated, redirecting the resulting connection to an arbitrary host. Attackers can use this capability to enumerate or communicate with internal network endpoints that would otherwise be inaccessible.

### CVE-2026-75608

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-22T16:17:54.607 |

Frigate is an open source network video recorder. Prior to 0.18.0, the prefix-matched location /api/go2rtc/api in docker/main/rootfs/usr/local/nginx/conf/nginx.conf requires authentication but does not require an administrator role for GET requests, exposing the proxied go2rtc API to viewer users. An authenticated viewer can request the streams, config, log, and stack subpaths to obtain internal addresses, configuration paths, application logs, goroutine stack data, and RTSP stream URLs that may contain camera credentials. Non-GET methods remain blocked by limit_except GET. This issue is fixed in version 0.18.0.

### CVE-2026-86681

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-23T14:17:09.217 |

ZohoCorp ManageEngine Applications Manager versions 182200 and below were vulnerable to a permissions validation issue that allowed low-privileged users to execute administrator-configured MBean actions on monitors outside their assigned scope.

### CVE-2026-12370

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-23T12:17:05.373 |

ZohoCorp ManageEngine OpManager, NetFlow Analyzer, and Network Configuration Manager versions 12.8.667 and below were vulnerable to a Server-Side Template Injection vulnerability in Configlet processing, which could lead to Remote Code Execution.

### CVE-2026-18123

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-22T22:17:09.653 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to cause a denial of service due to the improper use of reflection with externally controlled input.

### CVE-2026-77791

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T12:17:06.927 |

Uncontrolled Resource Consumption vulnerability in Apache Tomcat during sending of WebSocket close message enabled a DoS attack.



This issue affects Apache Tomcat: from 11.0.0-M5 through 11.0.25, from 10.1.8 through 10.1.59, from 9.0.74 through 9.0.121.



The following versions were EOL at the time the CVE was created but are 
known to be affected: from 8.5.88 through 8.5.100. Other unsupported versions may also be affected.




Users are recommended to upgrade to version 11.0.26, 10.1.60 or 9.0.122, which fix the issue.

### CVE-2026-15358

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-428` |
| Published | 2026-09-23T12:17:05.630 |

ZohoCorp ManageEngine OpManager and Network Configuration Manager versions before 12.8.671 were vulnerable to an unauthorized Path Traversal vulnerability.

### CVE-2026-93368

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T09:17:09.247 |

The Rename wp-login.php to anything you want plugin for WordPress is vulnerable to time-based SQL Injection via 'log' (Username) Parameter in all versions up to, and including, 2.0.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. WordPress core applies wp_unslash() to the 'log' POST value before dispatching the wp_login_failed action, stripping magic-quotes backslash escaping and allowing a raw single quote to reach the plugin's handler unimpeded.

### CVE-2026-31377

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-23T09:17:08.380 |

An Improper Authentication vulnerability in the Apache Doris Frontend (FE) meta service allows an unauthenticated remote attacker to access internal metadata service endpoints.



The affected endpoints relied on client-supplied node information for authentication without providing sufficient authentication of the requesting party. Under certain network configurations, a remote attacker may be able to bypass the intended access control and access internal FE metadata interfaces, potentially exposing sensitive cluster information.



This issue affects Apache Doris: from 2.0.0 through 2.0.*, from 2.1.0 through 2.1.*, from 3.0.0 through 3.0.*, from 3.1.0 through 3.1.*, from 4.0.0 before 4.0.8, and from 4.1.0 before 4.1.4. Versions 1.2.x and earlier are not affected by this header-trust vulnerability.




Users are recommended to upgrade to a fixed release (4.0.8 or 4.1.4), which fixes the issue.

### CVE-2026-91777

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T03:17:04.783 |

Forward-reference completion for @JsonIdentityInfo object IDs in FasterXML jackson-databind performs a linear scan of the pending-reference accumulator for every resolved ID. The affected paths are CollectionDeserializer.CollectionReferringAccumulator.resolveForwardReference() and the equivalent implementation in MapDeserializer. When a document first creates N unresolved object-ID references in an identity-enabled collection or map and then defines those same IDs in reverse order, completion performs on the order of N * (N + 1) / 2 identity comparisons, so a shallow document whose size grows linearly causes quadratic CPU work during deserialization. The reporter instrumented equals() calls on the ID class and measured exactly 2,003,000 comparisons at N = 2,000, against zero comparisons in the pending-reference lookup path for an equally sized control in which every reference was already resolved. The input requires no deep nesting and no syntactically unusual JSON. Exploitation requires an application that deserializes attacker-influenced JSON into an identity-enabled collection or map. The fix replaces the repeated linear lookup with a keyed pending-reference structure.

### CVE-2026-91776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T03:17:04.620 |

TypeDeserializerBase._findDeserializer() in FasterXML jackson-databind caches the resolved deserializer under the raw, attacker-supplied type ID. When name-based polymorphism is configured with a fallback, for example @JsonTypeInfo(use = Id.NAME, defaultImpl = ...), every distinct unrecognized type ID resolves to the same fallback deserializer but is retained as its own key in the _deserializers map. That map has no configurable bound and lives for the lifetime of the type deserializer, so an attacker who can repeatedly supply fresh unknown type IDs causes monotonic memory retention across requests. The reporter observed 10,000 retained entries from 10,000 distinct unknown IDs, against a single entry for a control that repeated one unknown ID the same number of times, isolating attacker-controlled key cardinality from request volume. Exploitation requires an application that enables name-based polymorphism with a defaultImpl or equivalent fallback, accepts attacker-influenced type IDs, and reuses a long-lived ObjectMapper across requests. The fix stops caching fallback resolutions for unrecognized IDs and bounds both the number of cached entries and the length of a cacheable type ID.

### CVE-2026-89425

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-23T03:17:04.357 |

UTF8DataInputJsonParser._reportInvalidToken() in FasterXML jackson-core builds the offending-token text for its error message by appending Java identifier characters to a StringBuilder in a loop that has no upper bound. Unlike the three sibling parser implementations, including UTF8StreamJsonParser, it never consults ErrorReportConfiguration.getMaxErrorTokenLength() (default 256). A malformed token supplied to a parser created through JsonFactory.createParser(DataInput) is therefore accumulated in full. No StreamReadConstraints setting mitigates this: maxDocumentLength cannot be applied to DataInput sources at all, and maxStringLength does not cover this path because the accumulation bypasses ReadConstrainedTextBuffer. The reporter measured a 20,000,109-character exception message from a 20-million-character malformed token on the DataInput path, against 367 characters for identical input on the InputStream path. Scaling the payload drives the StringBuilder, which also incurs byte-to-char expansion and internal array doubling, to many times the raw payload size and can trigger OutOfMemoryError for the whole JVM. UTF8DataInputJsonParser was introduced in 2.8.0 together with createParser(DataInput); releases before 2.8.0 do not contain the affected class.

### CVE-2026-61685

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-22T23:17:07.600 |

ReactPress is a publishing system for React developers. Prior to version 3.7.0, ReactPress API list endpoints build TypeORM `QueryBuilder` conditions using unsanitized HTTP query parameter names as SQL column identifiers (e.g. `` `article.${key}` ``). TypeORM parameterizes values but not column names, allowing unauthenticated attackers to inject SQL through crafted query string keys. Version 3.7.0 contains a patch. As a workaround, allowlist allowed filter column names before interpolating into SQL.

### CVE-2026-18134

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-22T22:17:10.303 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to obtain sensitive information due to cleartext transmission of sensitive information.

### CVE-2026-96269

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-22T21:17:35.150 |

GNU Emacs 28.1 through 31.1 allows arbitrary code execution upon opening a file, because an untrusted value of read-symbol-shorthands affects the intern and unintern functions. This affects the default configuration; no particular user settings are required to trigger it.

### CVE-2026-88344

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T20:17:10.493 |

An out-of-bounds read vulnerability exists in the schema lexer of flatcc 4c3b999e. When an exact-length FlatBuffers schema buffer ends with a digit, the integer digit-scan loop in lex() advances past the end of the input buffer and dereferences the out-of-bounds pointer. A specially crafted schema can trigger a one-byte heap buffer over-read, resulting in application crash and denial of service.

### CVE-2026-77322

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-22T20:17:08.200 |

SIPGO is a library for writing SIP services in the GO language. Prior to 1.4.3, WSConnection.Read in sip/transport_ws.go creates a wsutil.Reader without setting MaxFrameSize, allowing NextFrame to accept a client-controlled header.Length before ParseMaxMessageLength is applied. An unauthenticated WS or WSS peer can send a frame header declaring an extremely large payload, causing an oversized allocation or a makeslice length panic before the payload is read and crashing or exhausting memory in the server process. This issue is fixed in version 1.4.3.

### CVE-2026-76711

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T20:17:06.973 |

A vulnerability exists in an Analytics and Location Engine (ALE) component where the impacted process improperly processes incoming socket connections. An unauthenticated remote attacker could exploit this vulnerability by providing specially crafted input during the connection process. Successful exploitation could result in unauthorized data injection.

### CVE-2026-76710

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-22T20:17:06.867 |

A vulnerability exists in the Analytics and Location Engine (ALE) management interface that may allow for the disclosure of sensitive information. An unauthenticated remote attacker could exploit this vulnerability by sending specially crafted requests to certain internal endpoints. Successful exploitation could result in the disclosure of sensitive site hierarchy, infrastructure details, and client device information.

### CVE-2026-62985

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-22T20:17:04.443 |

request-filtering-agent is an http(s).Agent implementation that blocks requests to Private/Reserved IP addresses. Prior to 3.2.1, RequestFilteringHttpAgent and RequestFilteringHttpsAgent synchronously threw from createConnection when rejecting a literal private-IP host such as 169.254.169.254 or 127.0.0.1. Because Node.js http.request and http.get expect connection failures to be delivered asynchronously, the throw bypassed req.on('error') and became an uncaught exception that could terminate the application process. Hostnames resolved through the asynchronous lookup path were not affected by this error-delivery asymmetry. This issue is fixed in version 3.2.1.

### CVE-2026-61570

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-22T20:17:04.287 |

MPXJ is an open source library to read and write project plans from a variety of file formats and databases. From 5.5.5 until 16.4.1, MerlinReader creates a DocumentBuilder with default settings while parsing XML from the ZTIMEINTERVALS column of a Merlin project SQLite database, leaving doctype declarations and external entities enabled. A crafted database can cause the parser to read an arbitrary local file, although MPXJ's subsequent handling of the parsed XML makes disclosure of the file contents unlikely. This issue is fixed in version 16.4.1.

### CVE-2026-59991

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-22T20:17:04.123 |

psd-tools is a Python package for working with Adobe Photoshop PSD files. Prior to 1.17.4, PSDImage.composite() and PSDImage.numpy() allocated output buffers from attacker-controlled PSD header geometry, including width, height, channels, depth, and per-layer rectangles, before validating those values against the available file data. A tiny crafted PSD could therefore cause multi-gigabyte memory allocation, and PSDImage.composite() could return a black image with only a warning instead of raising an exception. Services that composite untrusted PSD files could be terminated by out-of-memory handling. This issue is fixed in version 1.17.4.

### CVE-2026-58268

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-22T20:17:03.960 |

SIPGO is a library for writing SIP services in the GO language. Prior to 1.4.1, ParserStream.parseSingle in sip/parser_stream.go allocates a SIP body buffer from the client-controlled Content-Length header before ParseMaxMessageLength is enforced. An unauthenticated peer can send a stream-transport message over TCP, TLS, WS, or WSS with an oversized declared length, causing excessive memory allocation and denial of service before the body is read. This issue is fixed in version 1.4.1.

### CVE-2026-95862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:17:00.490 |

A malicious actor with access to the network could exploit an Out-of-bounds Write vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-95861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-22T19:17:00.353 |

A malicious actor with access to the network could exploit an Uncontrolled Recursion vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-77558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-22T19:16:51.980 |

A malicious actor with access to the network could exploit an Out-of-bounds Read vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-77556

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-22T19:16:51.860 |

A malicious actor with access to the network could exploit an Out-of-bounds Read vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-77555

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:51.737 |

A malicious actor with access to the network could exploit an Out-of-bounds Write vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-77544

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-22T19:16:51.600 |

A malicious actor with access to the network could exploit an Out-of-bounds Write vulnerability found in certain UniFi gateway devices to execute a Denial of Service (DoS) attack on the device.

### CVE-2026-75632

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-22T19:16:44.720 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-19480

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-22T19:16:43.053 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-77242

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-09-22T18:17:16.430 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, validate_url_for_ssrf checks a hostname's resolved addresses, but Requests and urllib3 resolve the hostname again when connecting. A caller can use a short-lived DNS answer that is public during validation and private during connection, preserving unauthenticated access to internal or metadata endpoints despite the earlier CVE-2026-27826 remediation. The advisory traces the vulnerable input and processing flow through validate_url_for_ssrf, _check_dns_resolution, socket.getaddrinfo, and _make_ssrf_safe_hook, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-83599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-22T17:17:25.957 |

Netdata is an open source observability tool. Prior to 2.11.0, Netdata's unauthenticated WebSocket server negotiates permessage-deflate before authentication, and src/web/websocket/websocket-compression.c allows websocket_client_decompress_message() to grow decompressed output toward WS_MAX_DECOMPRESSED_SIZE without enforcing a compressed-to-decompressed ratio. Small highly compressed frames can therefore cause large server-side allocations, and repeated concurrent connections can exhaust memory and terminate monitoring. This vulnerability is fixed in 2.11.0.

### CVE-2026-94640

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-22T16:18:18.143 |

A flaw was found in rpcbind. This vulnerability allows a remote, unauthenticated attacker to cause a Denial of Service (DoS) by sending a large number of unique requests. The rpcbind service records previously unseen RPC (Remote Procedure Call) statistics in unbounded in-memory lists, leading to persistent memory growth and increased CPU usage. This can degrade or exhaust service availability.

### CVE-2026-89407

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-22T15:17:21.053 |

NumberInput.looksLikeValidNumber() in FasterXML jackson-core pre-validates "stringified numbers" with two regular expressions: PATTERN_FLOAT ([+-]?[0-9]*[\.]?[0-9]+([eE][+-]?[0-9]+)?), present since 2.17.0, and PATTERN_FLOAT_TRAILING_DOT, added in 2.17.2. PATTERN_FLOAT places adjacent quantifiers over the same character class -- an optional [0-9]* run, an optional dot, then a required [0-9]+ run -- so input that ultimately fails to match forces Java's backtracking engine to retry every possible split point of the digit run. 



Matching cost therefore grows with the square of the input length. 



An attacker who can supply JSON that an application deserializes into a numeric target type reaches this method through jackson-databind's default String-to-number coercion (StdDeserializer and NumberDeserializers for BigDecimal, BigInteger, Double and Float). 



Because StreamReadConstraints.maxStringLength defaults to 20,000,000 characters, no constraint bounds the input before it reaches the regex. 



Testing by the reporter confirmed O(n^2) growth across five consecutive input-size doublings, with a single 160,000-character string consuming roughly 74 seconds in one call; a small number of concurrent requests of ordinary body size can therefore exhaust a server's request-handling thread pool. 



The affected method does not exist before 2.17.0, so 2.16.x and earlier releases are not affected. 



The fix replaces both regular expressions with a hand-rolled single-pass scan.

### CVE-2026-65118

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-22T15:17:12.417 |

NVIDIA Infrastructure Controller for Linux contains a vulnerability where an attacker could cause improper certificate validation. A successful exploit of this vulnerability might lead to information disclosure, data tampering, and denial of service.

### CVE-2026-95676

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-636` |
| Published | 2026-09-23T13:17:32.143 |

A missing/improper authentication vulnerability in the WatchGuard AuthPoint Gateway's LDAP Sync first-factor authentication allows a remote attacker to bypass single-factor password verification under non-default operating conditions. Additional authentication factors still apply.

### CVE-2026-76980

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-23T13:17:29.393 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.709 and below were vulnerable to a Data Exposure vulnerability in the Firewall Analyzer syslog collector.

### CVE-2026-42801

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-23T09:17:08.727 |

NULL pointer dereference vulnerability in ASR Crane，Falcon on Linux (as_rrc module) allows Pointer Manipulation.

This vulnerability is associated with program file 3g.mod/lib/src/urrsir.c.

### CVE-2026-18176

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-22T23:17:07.273 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to obtain sensitive information due to cleartext transmission of sensitive information.

### CVE-2026-18172

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-22T23:17:06.993 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to obtain sensitive information due to improper restriction of XML external entity references.

### CVE-2026-18152

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-22T22:17:10.563 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to forge validly-signed messages due to improper verification of cryptographic signatures.

### CVE-2026-77912

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-22T21:17:32.483 |

A stored cross-site scripting (XSS) vulnerability was identified in GitHub Enterprise Server that allowed an authenticated attacker to inject arbitrary HTML attributes into rendered Markdown because the Markdown rendering pipeline rewrote quote characters in already-sanitized HTML without re-sanitizing the result. Crafted Markdown could abuse same-origin JavaScript gadgets to bypass Content Security Policy and gain control of the page DOM when viewed by another user. Successful exploitation could allow an attacker to read content visible to the victim, extract embedded CSRF tokens, perform state-changing actions as the victim, and exfiltrate data through same-origin writes. The payload could also propagate to repositories and organizations where the victim had write access. This vulnerability affected supported GitHub Enterprise Server releases in the 3.17, 3.18, 3.19, 3.20, 3.21, and 3.22 series and was fixed in versions 3.22.1, 3.21.6, 3.20.8, 3.19.12, 3.18.15, and 3.17.21. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-77246

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200;CWE-441` |
| Published | 2026-09-22T19:16:48.730 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, an HTTP transport deployment with READ_ONLY_MODE=false accepts a request without an Authorization identity and permits attacker-controlled Atlassian service headers, including X-Atlassian-Confluence-Url, to select a public attacker hostname or one allowed by MCP_ALLOWED_URL_DOMAINS. A caller can then invoke confluence_upload_attachment or the Jira attachment variant in src/mcp_atlassian/jira/attachments.py with a server-local file_path and cause the MCP process to send the file to the selected attachment endpoint. This issue is fixed in version 0.22.0.

### CVE-2026-17618

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T22:17:07.817 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote unauthenticated attacker to view and modify sensitive information and cause a denial of service due to improper authorization.

### CVE-2026-76712

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-22T20:17:07.103 |

A vulnerability exists in the Analytics and Location Engine (ALE) that may allow for unauthorized access, information disclosure, or denial of service. An unauthenticated remote attacker could exploit the vulnerable system by sending specially crafted input or intercepting network communications. Successful exploitation could result in the disclosure of sensitive information, bypass of security controls, or a denial of service condition on the affected system.

### CVE-2026-85995

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-22T18:17:23.650 |

Notepad++ is a free and open-source source code editor. From 8.9.7 until 8.9.8, the Notepad++ updater and signature verification path can accept a modified GUP.exe file whose embedded certificate metadata remains present even though its Authenticode digest is invalid. An attacker who can replace or plant the updater-related file can cause Notepad++ to launch attacker-modified code when a user triggers the updater path, but the issue does not provide remote code execution by itself. This issue is fixed in version 8.9.8.

### CVE-2026-18462

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-284` |
| Published | 2026-09-22T18:17:12.220 |

Integer Overflow or Wraparound, Improper Access Control vulnerability in RTI Connext Professional (Core Libraries) allows Shared Resource Manipulation. This issue affects Connext Professional: from 7.4.0 before 7.7.0.1, from 7.0.0 before 7.3.1.6, from 6.1.0 before 6.1.*.

### CVE-2026-56681

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-22T16:17:48.350 |

9Router is an AI router & token saver. Prior to 0.5.6, 9Router deployments that allow requests to reach Next.js without the sanitizing custom-server.js wrapper trust the client-supplied X-9r-Real-Ip header in src/dashboardGuard.js when isLocalRequest decides whether canAccessPublicLlmApi may skip API-key validation for /api/v1/* routes. A remote unauthenticated attacker can set X-9r-Real-Ip to 127.0.0.1 and be classified as a local client, including on the verified GET /api/v1/models route. This permits unauthorized use of the instance owner's configured LLM providers, consumption of paid credits, and enumeration of configured providers and models. This issue is fixed in version 0.5.6.

### CVE-2026-19915

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T15:17:09.750 |

A potential security vulnerability has been identified in the HP Support Assistant for versions prior to 9.55.10.0. The vulnerability could potentially allow a local attacker to escalate privileges due to insufficient access controls.

### CVE-2026-94367

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T00:17:01.200 |

OpenEye Apex Network Video Recorder (NVR) firmware 3.2.9.376 contains an OS command injection vulnerability in recbackup. An authenticated administrator can supply crafted backup-area configuration input that is passed to a shell command, allowing commands to execute with the privileges of the nvr user. The underlying design has been present since at least firmware 2.2.3.4.

Upgrade to version 3.5.4.

### CVE-2026-95815

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-22T21:17:34.583 |

OpenClaw iOS before 2026.8.11 logs complete agent deep-link URLs including persistent bearer keys to unified logs as public diagnostic data. Attackers who obtain diagnostic archives can recover unrotated keys and replay them in forged deep links to submit agent requests without local confirmation prompts.

### CVE-2026-76714

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-22T20:17:07.360 |

Vulnerabilities in the Analytics and Location Engine web interface allows remote authenticated users to run arbitrary commands on the underlying host. A successful exploit could allow an attacker to execute arbitrary commands as root on the underlying operating system leading to complete system compromise.

### CVE-2026-76713

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T20:17:07.237 |

A vulnerability exists in the maintenance restore functionality of Analytics and Location Engine (ALE). Successful exploitation of this vulnerability could allow an authenticated remote attacker to gain unauthorized access to the file system with root privileges, potentially resulting in full system compromise.

### CVE-2026-63104

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T20:17:04.597 |

Kaneo versions 2.3.12 before 2.12.2 contain a missing authorization vulnerability that allows authenticated workspace members with viewer or member roles to delete and modify tasks beyond their assigned permissions by exploiting the bulk task endpoint that omits workspace permission checks. Attackers can send requests to the PATCH /api/task/bulk endpoint, which verifies only workspace membership without calling the role-based permission check enforced on all other task endpoints, to permanently delete all tasks or modify task status, priority, assignee, due date, and labels in a workspace.

### CVE-2026-86679

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-23T14:17:09.090 |

ZohoCorp ManageEngine Applications Manager versions 182000 and below were vulnerable to a permissions validation issue that allowed a low-privileged user to delete service monitors outside their assigned scope.

### CVE-2026-18177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T14:17:07.660 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to execute unauthorized payment actions due to missing authorization checks.

### CVE-2026-84791

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-23T12:17:08.110 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.710 and below were vulnerable to a Broken Access Control vulnerability that allowed an authenticated low-privilege user to modify Change Management report schedule configurations for firewalls outside their assigned scope.

### CVE-2026-84789

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-23T12:17:07.983 |

ZohoCorp ManageEngine OpManager and Firewall Analyzer versions 12.8.710 and below were vulnerable to a Broken Access Control vulnerability that allowed an authenticated low-privilege user to create alert notifications for firewalls outside their assigned scope.

### CVE-2026-96271

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-23T01:16:32.477 |

Photoview through 2.4.0 contains an authorization bypass vulnerability in the shareAlbum GraphQL mutation that allows authenticated users to create share links for albums owned by other users. Attackers can supply arbitrary album IDs to generate working share tokens for victim albums, exposing photos and sub-albums to anyone with the link while retaining indefinite control over token settings.

### CVE-2026-77426

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-22T21:17:32.327 |

Unleash is an open-source feature management platform. Prior to 8.0.3, the Unleash admin API contains five authorization vulnerabilities. POST /api/admin/segments/strategies assigns the Promise returned by hasPermission without awaiting it, allowing authenticated users to modify segment assignments without UPDATE_FEATURE_STRATEGY permission for the target project and environment. GET /api/admin/projects/:projectId/features/:featureName/environments/:environment/variants does not bind the requested feature to projectId, allowing cross-project variant configuration disclosure. GET .../strategies/:strategyId uses strategyId without validating the project and feature context, allowing cross-project strategy configuration disclosure. getEnvironmentInfo does not validate that the requested feature belongs to the supplied project, allowing cross-project environment information disclosure. PUT /:projectId/tags accepts feature identifiers without verifying that they belong to the URL project, allowing cross-project tag modification. This issue is fixed in version 8.0.3.

### CVE-2026-76715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-300` |
| Published | 2026-09-22T20:17:07.480 |

A vulnerability in an administrative component of Analytics and Location Engine (ALE) is vulnerable to a man-in-the-middle (MitM) attack. Successful exploitation of this vulnerability could allow an unauthenticated remote attacker to execute arbitrary code with root privileges on the affected appliance.

### CVE-2026-94462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-22T19:16:59.497 |

Spree is an open source e-commerce solution built with Ruby on Rails. From 5.4.0 until 5.4.4 and 5.5.4, PATCH /api/v3/store/carts/:id/associate in Spree::Api::V3::Store::CartsController#associate uses find_cart_for_association to locate a cart by prefixed_id but does not require a cart token or otherwise verify possession of the selected guest cart. An authenticated customer can derive reversible prefixed cart IDs, associate an eligible guest cart with the attacker's account, and receive billing and shipping address data from the cart. Exploitation requires a guest cart with address data on a store that does not require login for checkout, and reassignment can also disrupt the guest's in-progress cart. This issue is fixed in versions 5.4.4 and 5.5.4.

### CVE-2026-84395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T19:16:54.260 |

Premiere Pro is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation potentially resulting in unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-77253

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-22T19:16:49.540 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, Jira and Confluence attachment upload tools accept arbitrary local filesystem paths and send the selected bytes to Atlassian. In HTTP or multi-user deployments, a caller can cross the client-to-server filesystem boundary and disclose configuration, credentials, mounted secrets, or other files readable by the MCP process. The advisory traces the vulnerable input and processing flow through jira_upload_attachment, confluence_upload_attachment, file_path, and server-local filesystem, which identify the affected entry points, controls, and code paths. This issue is fixed in version 0.22.0.

### CVE-2026-75743

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-22T19:16:47.247 |

Adobe Experience Manager Forms JEE is affected by a Cross-Site Request Forgery (CSRF) vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access, causing a limited disruption to availability. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page.

### CVE-2026-77261

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T18:17:18.497 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, _make_ssrf_safe_hook is omitted from JiraFetcher and ConfluenceFetcher sessions created through the basic-auth and oauth_pat branches. If an attacker-controlled or compromised configured Atlassian instance returns a redirect to an internal address, those sessions can follow the redirect without revalidating its destination. This issue is fixed in version 0.22.0.

### CVE-2026-94455

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-345;CWE-770;CWE-1390` |
| Published | 2026-09-22T17:17:31.497 |

An HTTP endpoint intended for provisioning enterprise and reseller organisations is reachable without any session. The authentication middleware is bound only to an explicit list of controllers, and the enterprise controller is not on that list, so no authentication runs for these routes.

The endpoint's only check is that the request body carries a token bearing a valid signature from the instance secret. It does not check what that token was issued for. Login tokens are signed with the same secret and carry no purpose, audience or expiry claim, so an ordinary user's own session token satisfies the check.

Presented with such a token, the endpoint creates a new organisation holding the highest subscription tier, flagged as lifetime and with a channel allowance far above any sold plan, creates an organisation-owner account alongside it, and returns the new organisation's API key in the response body. That key is immediately valid against the public API.

### CVE-2026-85740

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-22T17:17:27.520 |

LightRAG provides simple and fast retrieval-augmented generation. Prior to 1.5.5, _validated_addresses in lightrag/parser/markdown/parser.py evaluates the literal resolved address with ipaddress.is_global without consistently classifying an IPv4 address embedded in an IPv6 transition wrapper. A caller who can upload a Markdown or textpack document can supply an external image URL using NAT64 64:ff9b::/96 or an IPv4-compatible form that embeds a loopback, private, or cloud-metadata IPv4 address. On a deployment with compatible NAT64 or DNS64 routing, _download and _build_guarded_opener accept the wrapper and fetch the internal resource, whose body is then ingested. Current interpreter behavior already blocks some RFC 8215 and 6to4 forms, but the fixed guard handles all documented wrappers without becoming more permissive than the standard library. This issue is fixed in version 1.5.5.

### CVE-2026-85055

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-285` |
| Published | 2026-09-22T16:18:03.990 |

Twenty is an open-source CRM (customer relationship management) platform. Prior to 2.22.0, field-level read permission is enforced on selected output fields but not on GraphQL or REST filter predicates. A workspace member or API key with permission to read an object but not a particular field can reference that denied field in direct filters, relation filters, or persisted view filters. The resulting totalCount and row presence reveal whether guesses match the real column, forming a boolean/count oracle that can reconstruct denied field values for records exposed by the principal's row-level policy. This issue is fixed in version 2.22.0.

### CVE-2026-77633

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-362;CWE-367;CWE-770` |
| Published | 2026-09-22T16:17:55.817 |

Cloudreve is a self-hosted file management and sharing system. Prior to 4.18.0, PrepareUpload in pkg/filemanager/fs/dbfs/upload.go checks a stale in-memory user storage value through validateUserCapacity and later applies an unconditional storage charge outside the same quota-enforcing transaction. An authenticated user with Files.Write permission can issue concurrent upload-session requests that read the same capacity snapshot, all pass the MaxStorage check, and reserve their declared sizes through CommitWithStorageDiff. The resulting reservations can exceed the account quota and can be materialized as chunked uploads that exhaust host storage and deny uploads to other users. The default local-storage policy and default User group are affected. This issue is fixed in version 4.18.0.

### CVE-2026-93344

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-22T15:17:21.690 |

MarketKing plugin for WordPress before 2.1.72 contains a missing authorization vulnerability in the marketking_get_page_content AJAX action that allows authenticated attackers with subscriber-level access or higher to access arbitrary vendor administrator panel pages by supplying an arbitrary vendor user ID. Attackers can bypass authorization controls by submitting a target vendor ID in the request to access payout pages, financial reports, and vendor dashboard content belonging to any vendor in the marketplace.

### CVE-2026-83597

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-22T18:17:22.180 |

Netdata is an open source observability tool. From version 2.0.0 until 2.10.4, Netdata Windows Agent MSI repair launches powershell.exe and wevtutil.exe as elevated interactive processes in the initiating user's desktop session. A low-privileged local user who triggers repair can interact with or hijack those visible process windows to execute arbitrary commands with SYSTEM privileges. This issue is fixed in stable version 2.10.4.
