# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-15 15:01 UTC
- **対象期間**: `2026-07-14T15:00:32.000Z` 〜 `2026-07-15T15:01:24.000Z`
- **重要CVE数**: 660 件（Critical 9.0+: 54 件 / High 7.0〜: 606 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **70 件以上** に上り、特に **リモートから認証不要でコード実行や権限昇格が可能** な脆弱性が目立ちます。  
- **インフラ系（Windows カーネル、ネットワークドライバ、OpenSearch 連携）** と **Web アプリケーションフレームワーク（ColdFusion、Vitest、Chrome）** に集中しています。  
- 多くが **ネットワーク経由での遠隔利用**（AV:N, PR:N）であり、内部ネットワークだけでなくインターネットに面したサーバでも即座に侵害が成立するリスクが高いです。  
- ベンダー側のパッチリリースが相次いでいるものの、**バージョン管理が緩いオープンソース製品**（Vitest、OpenHTJ2K、sigstore‑js）でも深刻な欠陥が残っている点が懸念されます。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑56699** | 10.0 | Wazuh Manager (≤ 5.0.0‑beta3) が OpenSearch バルクリクエストで `DataValue.index` をエスケープせず、エージェントが任意の NDJSON 操作（削除・インデックス）を注入可能 | **管理者権限でのデータ改ざん・情報漏洩** が瞬時に実行でき、SIEM 環境全体の信頼性が崩壊する危険性がある。 |
| **CVE‑2026‑15409** | 10.0 | SMA1000 Appliance の Workplace UI に SSRF 脆弱性。認証不要で内部ネットワークへ任意リクエスト送信可能 | **内部システムへの横方向移動** や **クラウドメタデータ取得** が可能になるため、IoT/OT 環境での被害拡大が懸念される。 |
| **CVE‑2026‑57092** | 9.9 | Windows Hyper‑V VMSwitch の Use‑After‑Free による特権昇格（ネットワーク経由） | Hyper‑V を利用するサーバは **クラウド・オンプレミス問わず** 多く、特権取得により全ホスト制御が可能になる。 |
| **CVE‑2026‑5270** | 9.8 | Ciena Navigator / Blue Planet 製品の認証バイパス（HTTP パス/ヘッダー処理不備） | ネットワーク制御系ソフトウェアで **無認証で設定変更** ができ、通信インフラ全体の停止・改竄リスクが高い。 |
| **CVE‑2026‑15773** | 9.6 | Google Chrome (≤ 150.0.7871.124) の Use‑After‑Free によるサンドボックス脱出 | エンドユーザーだけでなく、社内ポータルや SaaS で利用される Chrome が **任意コード実行** できるため、フィッシングやマルウェア拡散の足がかりになる。 |

> **※** これらは **CVSS が 9.6 以上** かつ **リモートから直接利用可能** な点で共通しており、組織の攻撃対象領域（SIEM、ネットワーク制御、仮想化基盤、エンドポイント）に直結します。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / 対策 |
|-------------------|-------------------|------------------------|
| **Wazuh Manager** | < 5.0.0‑beta3 | **5.0.0‑beta3 以降**（公式リリース 5.0.0‑stable も可）にアップグレードし、`DataValue.index` エスケープ処理が修正されたものを使用。 |
| **SMA1000 Appliance** | すべて（ファームウェア未更新） | ベンダーが提供する **2026‑03‑xx 以降のファームウェア**（SSRF 修正）を即時適用。 |
| **Windows Server / Hyper‑V** | Windows Server 2022, Windows 11 (カーネル 10.0.22631) | **2026‑07 月の累積更新 (KBxxxxxx)** を適用し、VMSwitch の Use‑After‑Free を修正。 |
| **Ciena Navigator / Blue Planet** | 5.2.x 以前（具体的バージョンはベンダー資料参照） | **Ciena Security Advisory 2026‑07** に記載の **5.3.0 以降** へアップグレード。 |
| **Google Chrome** | ≤ 150.0.7871.124 | **150.0.7871.125** 以上、もしくは **最新安定版** に自動更新を有効化。 |
| **ColdFusion** (Path Traversal, Code Injection) | 2021‑2025 系列 | **ColdFusion 2023 Update 31** 以降（2026‑03‑リリース）へ更新。 |
| **Vitest** (Browser Mode, UI API) | < 3.2.5, < 4.1.0, < 5.0.0‑beta4 | **3.2.5 以降、4.1.0 以降、5.0.0‑beta4 以降** にアップグレード。 |
| **OpenHTJ2K** | ≤ 0.18.4 | **0.18.5** 以上に更新。 |
| **sigstore‑js** | < 0.7.1 | **0.7.1** 以上へアップデート。 |

### 3.2 環境・設定の見直し
1. **Wazuh / OpenSearch**  
   - `DataValue.index` への入力は **正規表現でホワイトリスト** し、不要なエージェント権限は最小化。  
   - OpenSearch の **Bulk API** への直接書き込みは、プロキシや WAF でリクエストサイズ・形式を検査。  

2. **SMA1000**  
   - 管理 UI への **IP アクセス制限**（VPN・内部ネットワークのみ）を実装。  
   - SSRF 防止のため、外部向け HTTP/HTTPS プロキシを経由させ、**許可ドメインリスト**で制御。  

3. **Windows VMSwitch**  
   - Hyper‑V の **仮想スイッチ管理権限**を AD グループで限定し、不要なローカル管理者アカウントを削

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56699

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-15T12:18:15.293 |

Wazuh Manager before 5.0.0-beta3 fails to escape the DataValue.index field when constructing OpenSearch bulk requests, allowing enrolled agents to inject arbitrary NDJSON operations. Attackers can smuggle delete, index, or update operations into bulk requests executed under the manager's admin credentials, enabling document deletion, alert tampering, and cross-agent SIEM state manipulation.

### CVE-2026-15409

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T20:16:56.783 |

A Server-side request forgery (SSRF) vulnerability has been identified in the SMA1000 Appliance Work Place interface. A remote unauthenticated attacker could potentially cause the appliance to make requests to unintended location.

### CVE-2026-48318

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T21:16:58.493 |

ColdFusion is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-57092

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:33.810 |

Use after free in Windows VMSwitch allows an authorized attacker to elevate privileges over a network.

### CVE-2026-5270

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-14T23:17:34.570 |

An authentication bypass vulnerability exists in certain releases of Ciena Navigator Network Control Suite (NCS), Manage Control Plan (MCP), and Blue Planet products. The issue is caused by improper handling of HTTP request paths and headers, which allows an unauthenticated attacker to manipulate requests in a manner that bypasses authentication and associated audit logging controls.

### CVE-2026-51808

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-14T23:17:29.957 |

Buffer Overflow vulnerability in OpenHTJ2K v.0.18.4 and before allows an attacker to execute arbitrary code via the openhtj2k_decoder_impl::invoke, invoke_line_based, invoke_line_based_stream, and invoke_line_based_predecoded function in source/core/interface/decoder.cpp

### CVE-2026-53633

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749;CWE-862` |
| Published | 2026-07-14T20:17:42.173 |

Vitest is a testing framework powered by Vite. From 3.0.0 until 3.2.5, 4.1.8, and 5.0.0-beta.4, Vitest Browser Mode exposed a cdp() API that forwarded raw Chrome DevTools Protocol methods without being gated by allowWrite or allowExec, allowing a remote client with exposed browser API metadata to use CDP Page.setDownloadBehavior and Runtime.evaluate to overwrite vite.config.ts and execute attacker-controlled Node.js code. This issue is fixed in versions 3.2.5, 4.1.8, and 5.0.0-beta.

### CVE-2026-47429

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T20:17:02.460 |

Vitest is a testing framework powered by Vite. Prior to 3.2.5 and 4.1.0, the Vitest UI/API server on Windows used isFileServingAllowed incorrectly for /__vitest_attachment__, allowing \\?\\..\\ path traversal to read files outside the project; exposed API write and rerun features such as saveTestFile and rerun could also allow arbitrary script execution. This issue is fixed in versions 3.2.5 and 4.1.0.

### CVE-2026-13001

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T20:16:56.610 |

The Podlove Podcast Publisher plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the 'podlove_handle_cache_files' function in all versions up to, and including, 4.5.1. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-56190

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-07-14T18:18:29.240 |

Use of uninitialized resource in Windows RDP allows an unauthorized attacker to execute code over a network.

### CVE-2026-56188

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:18:28.800 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Server Network driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-56159

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:22.797 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-55944

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T18:18:21.850 |

Deserialization of untrusted data in Microsoft Dynamics NAV allows an unauthorized attacker to execute code over a network.

### CVE-2026-55010

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:11.723 |

Heap-based buffer overflow in Minecraft Bedrock Dedicated Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-50518

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:58.373 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-50447

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:49.077 |

Heap-based buffer overflow in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-58644

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:14.257 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-54990

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:06.603 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-50522

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:01.547 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-49172

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:52.233 |

Heap-based buffer overflow in Windows FTP Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-42990

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:48.490 |

Heap-based buffer overflow in SQL Server ODBC driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-48322

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T21:16:58.920 |

ColdFusion is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48284

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T21:16:58.043 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-15773

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:43.007 |

Use after free in Core in Google Chrome on Windows prior to 150.0.7871.125 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-48359

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-14T20:17:08.810 |

Adobe Experience Manager is affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to read sensitive files, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48356

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-14T20:17:08.437 |

Adobe Commerce is affected by an Unrestricted Upload of File with Dangerous Type vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-48259

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T20:17:06.697 |

Adobe Experience Manager is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could leverage this vulnerability to issue unauthorized server-side requests, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-47428

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T20:17:02.307 |

Vitest is a testing framework powered by Vite. From 4.0.17 until 4.1.6 and 5.0.0-beta.3, Vitest Browser Mode served /__vitest_test__/ with the otelCarrier query parameter inserted directly into an inline module script, allowing a crafted browser-runner URL to execute arbitrary JavaScript in the Vitest server origin and recover VITEST_API_TOKEN for authenticated API calls. This issue is fixed in versions 4.1.6 and 5.0.0-beta.3.

### CVE-2026-50380

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:39.483 |

Heap-based buffer overflow in Windows GDI+ allows an unauthorized attacker to execute code over a network.

### CVE-2026-59891

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-14T17:17:15.270 |

sigstore-js provides JavaScript libraries for interacting with Sigstore services. Prior to 0.7.1, getRegistryCredentials() reads credentials from the Docker config file and selects an entry by checking whether any configured auth key contains the target registry string. Because this is a substring match rather than an exact host match, credentials configured for one registry can be selected for and transmitted to a different registry whose hostname has a substring relationship with a configured auth key. This issue is fixed in version 0.7.1.

### CVE-2026-55008

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T17:17:08.763 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Exchange Server allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-48561

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-14T17:16:49.753 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Copilot allows an unauthorized attacker to execute code over a network.

### CVE-2026-13385

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-354` |
| Published | 2026-07-15T02:18:12.090 |

An Improper Validation of Integrity Check Value and Improper Certificate Validation in certain ASUS router models allows a remote man-in-the-middle(MITM) user to make the router download and execute arbitrary command via a spoofed server.
Refer to the ' 
Security Update for ASUS Router Firmware  ' section on the ASUS Security Advisory for more information.

### CVE-2026-61451

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-15T12:18:19.897 |

The Grav API plugin (grav-plugin-api) before 1.0.4 does not validate the origin of the client-supplied admin_base_url field in the POST /api/v1/auth/forgot-password endpoint. The sanitizeHttpUrl() function only checks that the URL scheme is http/https and never verifies the host against the server's own origin, so an attacker can supply an arbitrary host. As a result, an unauthenticated attacker can cause the password reset email sent to a victim to contain a reset link pointing at an attacker-controlled server; when the victim follows the link, the valid reset token is disclosed to the attacker, enabling full account takeover. The vulnerable base URL can also be influenced via the Referer or Origin headers.

### CVE-2026-15265

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-347` |
| Published | 2026-07-14T15:16:57.457 |

A path traversal vulnerability in Tenable Agent 11.2.0 and 11.1.3 and lower allows a privileged attacker to write arbitrary files outside the intended plugin directory, potentially leading to remote code execution.

### CVE-2026-48334

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T22:17:01.717 |

Illustrator is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48325

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T21:16:59.143 |

ColdFusion is affected by a Missing Authentication for Critical Function vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48321

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T21:16:58.813 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain unauthorized read and write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-49798

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:55.857 |

Use after free in Windows Kernel allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-15643

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T21:16:41.293 |

AWS HealthLake MCP Server (awslabs.healthlake-mcp-server) is a Model Context Protocol server that enables AI assistants to interact with AWS HealthLake FHIR datastores. A server-side request forgery in the pagination handling component in AWS awslabs.healthlake-mcp-server before 0.0.14 on all platforms might allow a remote authenticated user to exfiltrate AWS temporary security credentials to an arbitrary endpoint via a crafted next_token parameter. The server does not validate that pagination URLs point back to the expected HealthLake endpoint, allowing an actor to redirect subsequent requests to an actor-controlled server.



Its recommended to upgrade to version 0.0.14 or later.

### CVE-2025-11698

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-14T16:16:41.837 |

A denial-of-service issue exists in 5380/5480/5580 controllers boot firmware lower than version 1.072. This vulnerability could potentially allow a malicious user to write invalid file data to the controller, causing the device to enter a major non-recoverable fault (MNRF).

### CVE-2026-58479

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-14T15:17:06.893 |

Sustainable Irrigation Platform (SIP) through version 5.2.16 contains a command injection vulnerability in the optional cli_control plugin that allows unauthenticated or cross-site request forgery attackers to execute arbitrary operating-system commands by storing a malicious payload via the plugin's HTTP endpoint. Attackers can trigger execution by activating the associated irrigation station, exploiting the absence of passphrase protection or the default passphrase 'opendoor', to achieve arbitrary command execution on the underlying host.

### CVE-2025-12012

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-14T15:16:54.210 |

A denial-of-service issue exists in 5380/5480/5580 controllers. This vulnerability could potentially allow a malicious user to write invalid file data to the controller, causing the device to enter a major non-recoverable fault (MNRF).

### CVE-2025-12011

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-14T15:16:53.323 |

A denial-of-service issue exists in  5370/5570 controllers. This vulnerability could potentially allow a remote user to load an invalid project, causing the device to enter a major non-recoverable fault (MNRF).

### CVE-2026-45363

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-326;CWE-1391` |
| Published | 2026-07-14T22:16:54.463 |

ruby-jwt is a Ruby implementation of the RFC 7519 OAuth JSON Web Token standard. Prior to 2.10.3 and 3.2.0, JWT.decode(token, '', true, algorithm: 'HS256') accepts an attacker-forged token because OpenSSL::HMAC.digest('SHA256', '', payload) returns a valid digest under an empty key and no empty-key precondition exists in the HMAC algorithm. The same path is reached when a keyfinder block or key_finder: argument returns an empty string, nil, or an array containing nil for an unknown key, affecting HS256, HS384, and HS512 verification through JWT.decode and JWT::EncodedToken#verify_signature!. This issue is fixed in versions 2.10.3 and 3.2.0.

### CVE-2026-53486

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-59;CWE-732` |
| Published | 2026-07-14T21:17:05.447 |

The decompress package for Node.js extracts archives. Prior to 10.2.1 and 11.1.3, archive extraction can create files and links outside the target directory. When extracting an archive to a directory, a crafted archive can read or write files outside that directory because hardlink and symlink entries are created without checking where targets point, path containment used a string prefix comparison, and file modes failed to remove setuid, setgid, or sticky bits. This issue is fixed in @xhmikosr/decompress versions 10.2.1 and 11.1.3.

### CVE-2026-48324

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-14T21:16:59.023 |

ColdFusion is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48319

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T21:16:58.600 |

ColdFusion is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48358

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-07-14T20:17:08.653 |

Adobe Commerce is affected by an Improper Encoding or Escaping of Output vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-45063

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-14T19:17:05.620 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, X509Authenticator extracts the user identifier from $_SERVER['SSL_CLIENT_S_DN'] with an unanchored regex that matches emailAddress= anywhere in the distinguished name, allowing an attacker with a trusted certificate containing emailAddress=victim inside another RDN value such as CN to authenticate as the victim. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-55040

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-07-14T18:18:15.413 |

Weak authentication in Microsoft Office SharePoint allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-55954

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-14T16:17:01.093 |

Authentication Bypass by Spoofing vulnerability in ueberauth ueberauth_apple allows account takeover via unvalidated ID token claims.

The Ueberauth.Strategy.Apple.Token.payload/2 function verifies the JWT signature of the callback id_token against Apple's JWKS but does not validate any registered claims. The iss, aud, exp, and iat claims are read from the token and passed on to Ueberauth.Strategy.Apple.handle_callback!/1, which derives the logged-in user's uid and email directly from the unvalidated sub claim.

An attacker who obtains any Apple-signed ID token bearing the victim's sub (via a captured expired token, or via an ID token issued to a sibling client in the same Apple developer team) can replay it against the vulnerable callback and be authenticated as the victim. The absent exp check makes stolen tokens usable indefinitely, and the absent aud check enables cross-application account takeover across clients that share an Apple developer team.

This issue affects ueberauth_apple: from 0.1.0 before 0.6.2.

### CVE-2026-56400

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-15T12:18:03.017 |

open-webui before 0.3.14 contains a cross-origin resource sharing misconfiguration allowing arbitrary origins with allow_origins=* and authenticated requests to the /api/v1/functions endpoint. Attackers can execute arbitrary code on the openwebui instance by crafting malicious cross-site requests from attacker-controlled websites when an admin user visits them.

### CVE-2026-48327

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T21:16:59.257 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue does not require user interaction. Scope is changed.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-15701

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T17:16:45.477 |

A weakness has been identified in Totolink NR1800X 9.1.0u.6279_B20210910. Affected by this issue is the function Form_Logout of the file /formLogout.htm of the component lighttpd. This manipulation of the argument Host causes stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-43637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T14:18:10.793 |

Cornac before 2.6.0 contains a path traversal (Tar Slip) vulnerability that allows attackers to write arbitrary files outside the intended cache directory by supplying a crafted TAR archive containing ../ sequences, absolute paths, or symlink/hardlink entries to the _extract_archive() function in cornac/utils/download.py. Attackers can trigger this vulnerability through the built-in dataset loaders, which automatically download and extract archives, causing archive.extractall() to write files to arbitrary locations on the filesystem accessible to the running process.

### CVE-2026-61436

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-15T12:18:18.847 |

PraisonAI before 4.6.78 fails to verify Svix webhook signatures in AgentMail webhook mode, allowing unauthenticated attackers to forge message.received events. Attackers can send crafted JSON payloads to the webhook endpoint to invoke configured agents with arbitrary sender addresses and message content.

### CVE-2026-61435

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-15T12:18:18.700 |

PraisonAI before 4.6.78 contains an authentication bypass in the Call API agent invocation endpoints (src/praisonai/praisonai/api/agent_invoke.py) when PRAISONAI_CALL_AUTH=disabled is configured. The safeguard intended to restrict the disabled-auth opt-out to localhost binding derives the bind host from request.url.hostname, which is taken from the client-controlled HTTP Host header. A remote, unauthenticated attacker who can reach the service over the network can send a spoofed 'Host: 127.0.0.1' header to bypass the localhost-only restriction and list (GET /api/v1/agents) and invoke (POST /api/v1/agents/{agent_id}/invoke) registered agents without authentication.

### CVE-2026-59733

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-639` |
| Published | 2026-07-14T22:17:30.050 |

Rclone is a command-line program to sync files and directories to and from different cloud storage providers. Prior to 1.74.4, rclone serve restic --private-repos enforces authorization using the routed user path segment while building the backend object key from the raw uncleaned URL path, allowing an authenticated user to include .. in a request such as //..//config and read, overwrite, or delete another user's private repository on backends that clean path components. This issue is fixed in version 1.74.4.

### CVE-2026-50130

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-282` |
| Published | 2026-07-14T22:17:13.203 |

Pi-hole is a DNS sinkhole that protects devices from unwanted content without installing any client-side software. From 6.0 to 6.4.2, a user with code execution as the unprivileged pihole user can escalate to root by replacing /etc/pihole/logrotate. The replacement is laundered to root:root ownership by pihole-FTL-prestart.sh and then parsed as root by the daily pihole flush cron, executing firstaction shell as uid 0. This issue is fixed in version 6.4.3.

### CVE-2026-15776

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T21:16:43.393 |

Inappropriate implementation in V8 in Google Chrome prior to 150.0.7871.125 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15767

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:42.187 |

Heap buffer overflow in libyuv in Google Chrome on Windows prior to 150.0.7871.125 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted video file. (Chromium security severity: High)

### CVE-2026-47303

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-90;CWE-302;CWE-863` |
| Published | 2026-07-14T19:17:08.707 |

Authentication bypass by assumed-immutable data in ASP.NET Core allows an authorized attacker to elevate privileges over a network.

### CVE-2026-47301

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T19:17:08.420 |

Improper access control in Microsoft Configuration Manager allows an authorized attacker to elevate privileges over a network.

### CVE-2026-47300

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-07-14T19:17:08.303 |

Incorrect implementation of authentication algorithm in ASP.NET Core allows an authorized attacker to elevate privileges over a network.

### CVE-2026-45069

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-1287` |
| Published | 2026-07-14T19:17:06.017 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 6.4.40, 7.4.12, and 8.0.12, OidcTokenHandler::verifyClaims() registered audience (aud), issuer (iss), and expiry (exp) checkers but did not pass the mandatory claims list to ClaimCheckerManager::check(), so a validly signed JWT that omitted those claims could pass verification. This issue is fixed in versions 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-58626

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:44.650 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to execute code over a network.

### CVE-2026-58594

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-14T18:18:43.067 |

Integer overflow or wraparound in Windows RDP allows an unauthorized attacker to execute code over a network.

### CVE-2026-58534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:40.380 |

Heap-based buffer overflow in Microsoft Input Method Editor (IME) allows an authorized attacker to elevate privileges locally.

### CVE-2026-58277

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T18:18:36.873 |

Improper authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-57102

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-829` |
| Published | 2026-07-14T18:18:34.977 |

Inclusion of functionality from untrusted control sphere in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-57094

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-07-14T18:18:34.170 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-57090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:33.430 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-57087

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:32.903 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-56647

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-14T18:18:30.930 |

Integer overflow or wraparound in Windows Remote Access Service Infrastructure allows an authorized attacker to elevate privileges over a network.

### CVE-2026-56642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:30.353 |

Stack-based buffer overflow in Microsoft Fabric Data Warehouse allows an authorized attacker to execute code over a network.

### CVE-2026-56197

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-14T18:18:30.200 |

Improper neutralization of special elements used in a command ('command injection') in Windows Admin Center allows an authorized attacker to execute code over a network.

### CVE-2026-56196

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-14T18:18:30.070 |

Relative path traversal in Windows Admin Center allows an authorized attacker to execute code over a network.

### CVE-2026-56194

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:29.757 |

Heap-based buffer overflow in Windows Network File System allows an authorized attacker to elevate privileges over a network.

### CVE-2026-55052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-14T18:18:17.287 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-54121

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T18:18:08.057 |

Improper authorization in Active Directory Certificate Services (AD CS) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50692

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:05.440 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-50687

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:04.310 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50670

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122;CWE-125` |
| Published | 2026-07-14T18:18:01.063 |

Out-of-bounds read in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50666

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:00.240 |

Use after free in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50489

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:55.117 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-50477

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:53.537 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50474

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:53.013 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-50444

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T18:17:48.737 |

Missing authentication for critical function in Windows Server Update Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50438

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T18:17:47.993 |

Improper link resolution before file access ('link following') in Microsoft PC Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-50413

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:44.287 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50398

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:42.020 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Media allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:40.090 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50382

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T18:17:39.727 |

Untrusted pointer dereference in Windows DirectX allows an authorized attacker to execute code locally.

### CVE-2026-50370

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-07-14T18:17:37.850 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-50369

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:37.673 |

Use after free in Windows Remote Desktop Services allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50360

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-07-14T18:17:36.323 |

Incorrect implementation of authentication algorithm in Windows SMB Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-47295

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-14T18:17:17.883 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-58608

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:17:12.930 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Print Spooler Components allows an authorized attacker to execute code over a network.

### CVE-2026-57969

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T17:17:10.980 |

Missing authentication for critical function in Azure CycleCloud allows an authorized attacker to elevate privileges over a network.

### CVE-2026-55005

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:08.537 |

Heap-based buffer overflow in Microsoft Exchange Server allows an authorized attacker to execute code over a network.

### CVE-2026-54999

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T17:17:07.657 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows TCP/IP allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-54982

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-14T17:17:05.663 |

Integer underflow (wrap or wraparound) in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-54118

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:04.530 |

Deserialization of untrusted data in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-54117

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:04.407 |

Deserialization of untrusted data in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-54107

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T17:17:03.570 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-50663

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-14T17:17:01.930 |

Relative path traversal in Age of Empires II: Definitive Edition Game allows an unauthorized attacker to execute code over a network.

### CVE-2026-50342

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:17:00.140 |

Improper access control in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-49795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:55.377 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-49178

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:52.933 |

Heap-based buffer overflow in Active Directory Domain Services allows an authorized attacker to execute code over a network.

### CVE-2026-48564

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:49.873 |

Heap-based buffer overflow in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-47632

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-14T17:16:49.637 |

Improper certificate validation in Azure Monitor Agent allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-58477

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-07-14T15:17:06.620 |

Sustainable Irrigation Platform (SIP) through version 5.2.16 contains a mass assignment vulnerability that allows unauthenticated attackers to overwrite sensitive configuration settings by supplying arbitrary parameter names in HTTP requests. Attackers can manipulate parameters corresponding to sensitive values such as the passphrase and listening port, and can also achieve the same result through cross-site request forgery due to the absence of adequate request validation.

### CVE-2026-10714

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-07-14T15:16:55.673 |

A security issue exists within FactoryTalk® Services Platform (FTSP), allowing an attacker to bypass JWT signature validation during Okta Web Authentication. The vulnerability stems from the application not verifying that the JWT algorithm is configured for RSA, enabling an attacker to set the algorithm to "none" and craft forged tokens. This could allow an authenticated low-privilege user to impersonate any authorized user on the FTSP server, resulting in unauthorized access to system configuration and the ability to grant permissions to other systems protected by FTSP.

### CVE-2026-60085

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-273` |
| Published | 2026-07-15T12:18:17.933 |

PraisonAI before 4.6.78 contains an unenforced security policy vulnerability in the default Subprocess Sandbox backend where blocked_commands, blocked_paths, blocked_imports, allow_subprocess, and allow_file_write restrictions are completely ignored. Attackers can execute arbitrary subprocess commands, read sensitive files, and perform destructive operations despite explicit security policy configuration.

### CVE-2026-58655

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T12:18:17.367 |

The bundled Grav Flex Objects plugin (getgrav/grav-plugin-flex-objects) before 1.4.0 contains a stored server-side template injection vulnerability. When rendering dynamic collection or object titles, the plugin passes user-controlled frontmatter values (page.header.flex.collection.title or page.header.flex.object.title) to Twig's template_from_string(), causing them to be evaluated as Twig code rather than treated as text. This path bypasses Grav's Security::cleanDangerousTwig() sanitization. An attacker who can control the title frontmatter of a publicly reachable Flex Objects page can achieve arbitrary Twig execution and escalate to remote command execution via access to internal Grav services such as the scheduler.

### CVE-2026-57996

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-15T12:18:16.143 |

phpMyFAQ before 4.1.5 contains a privilege escalation vulnerability in the user/add API endpoint that allows non-SuperAdmin administrators to create SuperAdmin accounts. A delegated administrator with USER_ADD/EDIT/DELETE permissions can call POST /admin/api/user/add with isSuperAdmin: true and attacker-chosen credentials to create a SuperAdmin account, then authenticate as that account to achieve full instance takeover.

### CVE-2026-56339

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-07-15T12:18:02.140 |

Capgo (Cap-go/capgo) before 12.128.2 contains an information disclosure vulnerability in the Supabase PostgREST SECURITY DEFINER RPC function public.rescind_invitation that allows unauthenticated attackers to enumerate organization existence. The function returns distinct error messages (NO_ORG vs NO_RIGHTS) when called with only a publishable API key, enabling attackers to discover valid organization IDs and increase the attack surface for targeted phishing or social engineering campaigns.

### CVE-2026-59235

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-15T11:16:33.493 |

Missing Authorization (CWE-862) in BankAccountListController (app/Http/Controllers/Api/BankAccount/BankAccountListController.php), exposed at GET /api/bank-account, in Prospero Flow CRM <5.5.3, which allows a remote, authenticated attacker holding a low-privileged role (e.g. the "User"/"Usuario" role) to read arbitrary bank account records belonging to their company by sending an authenticated request to the endpoint with a valid bearer token, because the API route is protected only by the auth:api middleware and carries no permission gate, unlike the equivalent web route, which enforces can('read bank'), and the handler resolves records with Account::where('company_id', Auth::user()->company_id)->get(), performing only company scoping and no role or permission check before returning the data. This results in the unauthorized disclosure of sensitive banking information (e.g. IBAN, SWIFT/BIC, account identifiers) to users who should not have access to it.

### CVE-2026-58077

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T10:16:47.870 |

The Joomla extension 4Analytics is vulnerable to an unauthenticated stored XSS. A specially crafted unauthenticated request may result in website takeover under some circumstances.

### CVE-2026-57832

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T09:16:33.450 |

The Joomla extension EDocman is vulnerable to an unauthenticated SQL injection.

### CVE-2026-57831

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T09:16:33.310 |

The Joomla extension DP Calendar is vulnerable to an unauthenticated SQL injection.

### CVE-2026-15804

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T08:16:23.100 |

The HCM developed by MetaGuru has a SQL Injection vulnerability. Authenticated remote attackers can inject SQL commands via specific parameters, thereby compromising the confidentiality, integrity, and availability of database data.

### CVE-2026-46640

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T22:16:56.840 |

Twig is a template language for PHP. From 3.15.0 until 3.26.0, _self.(<string>) and import-alias dynamic attribute syntax can concatenate an attacker-controlled string into a MacroReferenceExpression name without identifier validation, causing raw PHP to be emitted into the generated template source and executed at template-load time. This issue is fixed in version 3.26.0.

### CVE-2026-46633

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T22:16:55.997 |

Twig is a template language for PHP. Prior to 3.26.0, Compiler::string() does not escape single quotes when a template name from a {% use %} tag is placed inside a PHP single-quoted string literal, allowing a crafted template name to terminate the string and inject arbitrary PHP expressions into the compiled cache file. This issue is fixed in version 3.26.0.

### CVE-2026-48801

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-14T21:17:01.247 |

linkify-it is a links recognition library with full Unicode support. Prior to 5.0.1, LinkifyIt.prototype.match, the package's primary public API, has O(N²) algorithmic complexity for inputs containing many fuzzy links or emails because the JavaScript-level scan loop re-slices input and re-runs unanchored regex searches on progressively shorter tails. Any service that synchronously renders untrusted Markdown with linkify:true on a request hot path can inherit a worker-process denial of service triggerable by a tens-of-KB request body. This issue is fixed in version 5.0.1.

### CVE-2026-48489

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:09.330 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.53, 6.4.41, 7.4.13, and 8.0.13, DefaultAuthenticationFailureHandler honored the request-supplied _failure_path parameter when failure_forward: true was enabled, allowing an unauthenticated failing login request to dispatch a subrequest to access_control-protected GET routes that skipped firewall listeners. This issue is fixed in versions 5.4.53, 6.4.41, 7.4.13, and 8.0.13.

### CVE-2026-47994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T20:17:04.597 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-45071

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-07-14T20:17:00.370 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, Crawler::addXmlContent() set DOMDocument::$validateOnParse = true before loadXML(), re-enabling external entity resolution and allowing attacker-supplied XML to expand file:// entities such as local files. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-45068

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-14T20:17:00.107 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, SendmailTransport in -t mode appended recipient addresses to the sendmail command line without a -- end-of-options separator, allowing an address beginning with - to be interpreted as a sendmail command-line option instead of an address. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-45305

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-14T19:17:07.187 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, Symfony\Component\Yaml\Parser::cleanup() used regular expressions with overlapping quantifiers for YAML directive, comment, and document marker cleanup, allowing crafted input to make parsing hang for an arbitrarily long time. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-45304

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-776` |
| Published | 2026-07-14T19:17:07.050 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, Symfony\Component\Yaml\Parser resolved YAML collection aliases recursively, allowing a small untrusted YAML input to expand into a multi-gigabyte structure and exhaust memory. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-59204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789;CWE-770` |
| Published | 2026-07-14T16:17:02.227 |

Pillow is a Python imaging library. From 8.2.0 through 12.2.0, src/libImaging/Jpeg2KDecode.c accumulates total_component_width across every tile in a JPEG2000 image instead of recomputing it per tile, allowing a crafted tiled JPEG2000 file to force substantially higher transient memory usage and trigger out-of-memory failures during decoding. This issue is fixed in version 12.3.0.

### CVE-2026-12659

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-14T16:16:45.170 |

A denial-of-service security issue exists in the affected products. The security issue stems from improper handling of exceptional conditions when processing crafted CIP packets sent to the adapter. A power cycle is required to recover the module and associated I/O.

### CVE-2026-11403

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-331` |
| Published | 2026-07-14T16:16:44.217 |

A vulnerability in Sonatype Nexus Repository Manager's format-specific API key generation may allow a remote attacker to gain unauthorized access to repository operations as a targeted user. A format-specific API key realm (NuGet API Key, Docker Bearer Token, or npm Bearer Token) must be enabled and the targeted user must have an active API key for this vulnerability to be exploitable.

### CVE-2026-9653

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-07-14T15:17:11.347 |

A denial-of-service security issue exists across all the 1756-EN2, EN3, and ENBT communication module due to improper validation of CIP Implicit Connection packets. An attacker on the network can exploit this by sending crafted packets to continuously disrupt device connections, though device connections will recover immediately after.

### CVE-2026-9140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T15:17:10.897 |

A denial-of-service security issue exists in the 1719-AENTR. The security issue stems from improper handling of a UDP unicast network storm, which causes the device to become overloaded and lose communication. A power cycle is required to recover.

### CVE-2026-8590

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-07-14T15:17:10.740 |

Vulnerability in Spotfire Spotfire Enterprise (Spotfire Server modules), Spotfire Spotfire Enterprise with External Consumers (Spotfire Server modules), Spotfire Spotfire on Kubernetes (Spotfire Server modules).

This issue affects Spotfire Enterprise: through 14.0.12, through 14.4.2, through 14.5.0, through 14.6.1, through 14.6.2, through 14.7.0, through 14.8.0; Spotfire Enterprise with External Consumers: through 14.0.12, through 14.5.0, through 14.6.0, through 14.6.1, through 14.6.2, through 14.7.0, through 14.8.0; Spotfire on Kubernetes: through 4.2.0, 5.0.X, 6.0.X.

### CVE-2026-60114

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T15:17:08.017 |

Sustainable Irrigation Platform (SIP) through version 5.2.16 contains a path traversal vulnerability that allows attackers with access to the restore functionality to write files to arbitrary locations by uploading crafted JSON backup files with unvalidated keys used to construct file paths. Attackers can exploit the lack of key validation in the JSON restore process, combined with the absence of a required passphrase in the default configuration or the default passphrase 'opendoor', to write arbitrary JSON files outside the intended data directory.

### CVE-2026-10573

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T15:16:55.097 |

A denial-of-service security issue exists in 1734 POINT I/O™ module. The security issue stems from improper handling of crafted CIP messages, which can cause the module to enter a faulted state. A restart is required to recover.

### CVE-2026-61446

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T12:18:19.607 |

PraisonAI (praisonaiagents) before 1.6.78 contains a remote code execution vulnerability in the plugin manager, which loads and executes arbitrary Python (.py) files from project-level and user-home .praisonai/plugins/ directories using importlib spec_from_file_location() and exec_module() without code signing, integrity verification, or sandboxing. An attacker who can write a malicious .py file to a plugin directory (for example via path traversal, a supply chain attack, or a compromised dependency) achieves arbitrary code execution when the plugin system initializes.

### CVE-2026-61443

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-15T12:18:19.467 |

PraisonAI before 1.6.78 contains a remote code execution vulnerability in SkillTools.run_skill_script() that executes scripts without path containment validation. Attackers can supply absolute file paths to execute arbitrary scripts from any filesystem location, including those outside the intended working directory.

### CVE-2026-57833

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-15T10:16:47.737 |

The Joomla extension 4Analytics is vulnerable to an unauthenticated stored XSS in relation to the AI analysis feature.

### CVE-2026-15583

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-15T08:16:22.977 |

A confused-deputy flaw in Grafana MCP Server allows an unauthenticated remote attacker to exfiltrate the server's environment-configured Grafana service-account token by supplying a crafted X-Grafana-URL request header. This also enables SSRF against arbitrary internal services, including cloud metadata endpoints.

### CVE-2026-12512

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T06:16:44.757 |

The Quotes llama WordPress plugin before 3.1.6 does not properly sanitize and escape a user-supplied parameter before using it in a SQL query, allowing unauthenticated attackers to perform UNION-based SQL injection and read arbitrary data from the database, including password hashes.

### CVE-2026-9770

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-07-15T01:17:10.387 |

Kasa EC71 v4 and EC70 v4 firmware contains a static cryptographic private key stored in a read-only filesystem
that is shared across devices.  An
attacker with access to the firmware image can extract the embedded key.  









Successful
exploitation may allow an unauthenticated attacker on the same network to use
this key in the web management service, compromising the confidentiality of
encrypted communications. This may enable passive decryption of traffic or
active man-in-the-middle (MITM) attacks

### CVE-2026-48275

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-14T22:17:00.580 |

Illustrator is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48350

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T20:17:08.180 |

Animate is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to access sensitive files or directories outside the intended restrictions. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48310

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T20:17:07.450 |

Adobe Experience Manager is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48252

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T20:17:06.053 |

Adobe Experience Manager is affected by a Missing Authentication for Critical Function vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-47988

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:04.347 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access. Exploitation of this issue does not require user interaction.

### CVE-2026-15720

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T19:16:51.470 |

In Open5GS through version 2.7.7 a pre-authentication heap out-of-bounds read in the AMF NAS 5GS mobile-identity handler may result in subscriber-wide denial of service.

### CVE-2026-15427

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-14T17:16:44.653 |

An OS command
injection vulnerability exists in the TR-069 / CWMP management interface of Archer VX1800v v1 due to insufficient input validation and sanitization of
parameters, allowing crafted input to be executed as system-level commands.
Exploitation requires specific conditions such as TR-069 being enabled and ability
to influence ACS-delivered commands, compromise or control an ACS server.





Successful
exploitation may allow arbitrary command execution with root privileges,
resulting in complete compromise of the device.

### CVE-2026-59835

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-668` |
| Published | 2026-07-14T16:17:02.593 |

A exposure of resource to wrong sphere vulnerability in Fortinet FortiSandbox 5.0.0 through 5.0.2, FortiSandbox 4.4.3 through 4.4.8 may allow an unauthenticated attacker to access the VNC server of VMs performing scanning via network requests.

### CVE-2026-61433

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-15T12:18:18.553 |

PraisonAI before 4.6.78 fails to safely encode deployment configuration values when generating Python source code for API servers. Attackers can inject arbitrary Python expressions through the deploy.api.host and agents_file configuration parameters that execute when the generated server starts or handles requests.

### CVE-2026-56398

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-15T12:18:02.870 |

Open WebUI before 0.9.5 contains a stored cross-site scripting vulnerability in the OAuth authentication flow where the picture claim URL MIME type is inferred from file extension rather than Content-Type header, allowing SVG files to bypass the profile image validator and be stored as data URIs. Authenticated users who visit the profile image endpoint receive attacker-controlled SVG content with inline disposition and no default security headers, enabling script execution in the same origin to steal authentication tokens and achieve account takeover.

### CVE-2026-8920

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-923` |
| Published | 2026-07-15T02:22:57.790 |

Improper Restriction of Communication Channel to Intended Endpoints and External Control of File Name or Path in Aura Wallpaper Service allow a local user to perform file operations by sending crafted commands containing an arbitrary file path and bypassing the service’s path restrictions . On specific models , this can also cause a single feature to become unavailable .
Refer to the ' Security Update for Aura Wallpaper Service ' section on the ASUS Security Advisory for more information.

### CVE-2026-48320

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T21:16:58.703 |

ColdFusion is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-50340

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:33.617 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges over a network.

### CVE-2026-15428

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-14T17:16:44.790 |

An OS
command injection vulnerability exists in Archer VX800v v1 due to insufficient input sanitization of
the domain name parameter. An adjacent attacker who can access the relevant
HTTP interface can modify the parameter to inject shell metacharacters, resulting
in arbitrary code execution with root privileges.









Successful
exploitation may allow remote code execution and complete compromise of the
device.

### CVE-2026-61430

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-15T12:18:18.410 |

PraisonAI before 1.6.78 contains a server-side request forgery vulnerability in the web_crawl tool that validates hostnames at check time but re-resolves them at connection time without IP pinning. Attackers can use DNS rebinding to bypass SSRF protection and retrieve internal HTTP response bodies from private or loopback services.

### CVE-2026-42936

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-15T06:16:45.003 |

The installer of HYPER SBI 2 insecurely loads Dynamic Link Libraries. If there is a crafted DLL at the same directory when invoking the affected installer, arbitrary code may be executed with the privilege of the user invoking the installer.

### CVE-2026-15029

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-15T02:18:13.033 |

Untrusted Pointer Dereference in ASUS System Control Interface v3, ASUS System Control Interface, and ASUS Business Manager allows a local administrator to perform arbitrary physical memory read and write operations via crafted IOCTL requests to the driver, bypassing OS-enforced memory protections.
Refer to the ' 
Security Update for ASUS System Control Interface  ' section on the ASUS Security Advisory for more information.

### CVE-2026-42049

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T22:16:52.940 |

jadx is a Dex to Java decompiler. Prior to 1.5.6, jadx inserts the android:versionName value from an AndroidManifest into the generated app/build.gradle Groovy template without proper sanitization when exporting a decompiled APK as an Android Gradle project. A malicious APK can break out of the string context so that opening or building the exported Gradle project executes attacker-controlled Groovy code on the victim machine. This issue is fixed in version 1.5.6.

### CVE-2026-24233

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T21:16:44.187 |

NVIDIA TensorRT-LLM for Linux contains a vulnerability in the restricted unpickler used for model weight deserialization, where a local, unauthenticated attacker could cause deserialization of untrusted data. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, data tampering, and information disclosure.

### CVE-2026-55045

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:16.193 |

Out-of-bounds read in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-54128

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:08.873 |

Use after free in Windows DHCP Client allows an unauthorized attacker to execute code locally.

### CVE-2026-54992

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:06.830 |

Heap-based buffer overflow in Windows Message Queuing Queue Manager allows an unauthorized attacker to execute code locally.

### CVE-2026-54122

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:04.833 |

Heap-based buffer overflow in Windows GDI+ allows an unauthorized attacker to execute code locally.

### CVE-2026-50520

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-14T17:17:01.420 |

Improper neutralization of special elements used in a command ('command injection') in Visual Studio Code allows an unauthorized attacker to execute code locally.

### CVE-2026-49184

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:53.580 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-9292

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T16:17:05.723 |

A Stored Cross-Site Scripting security issue exists within FactoryTalk® DataMosaix™ Private Cloud. The vulnerability stems from improper neutralization of user-supplied input within the Workflows configuration. An authenticated attacker with high privileges can inject malicious scripts that are permanently stored on the server. This vulnerability can result in the execution of malicious JavaScript when other users access the affected page, potentially allowing for account takeover, credential theft, or redirection to a malicious website.

### CVE-2026-15774

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:43.160 |

Use after free in Skia in Google Chrome prior to 150.0.7871.125 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15772

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:42.860 |

Use after free in GPU in Google Chrome on Android prior to 150.0.7871.125 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15769

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T21:16:42.420 |

Insufficient validation of untrusted input in Linux Toolkit Theming in Google Chrome on Linux prior to 150.0.7871.125 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-47767

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-14T19:17:09.237 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. From 5.4.46 until 5.4.52, 6.4.40, 7.4.12, and 8.0.12, the CVE-2024-50340 fix gated runtime argv parsing on empty($_GET), but parse_str() and the web SAPI can disagree, allowing a crafted query string to leave $_GET empty while $_SERVER['argv'] still carries attacker-controlled --env or --no-debug flags that change APP_ENV or APP_DEBUG. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-45075

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T19:17:06.650 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 7.4.12 and 8.0.12, method-scoped #[IsGranted], #[IsSignatureValid], and #[IsCsrfTokenValid] attributes can be configured for GET only, but Symfony routes HEAD requests to the GET handler while the attribute check is skipped, allowing protected controllers to execute and leak headers or perform side effects. This issue is fixed in versions 7.4.12 and 8.0.12.

### CVE-2026-56181

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-14T18:18:24.793 |

Origin validation error in Windows Network Address Translation (NAT) allows an unauthorized attacker to perform spoofing over an adjacent network.

### CVE-2026-45077

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502;CWE-668` |
| Published | 2026-07-14T18:17:17.130 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, the server:log listener (Symfony\Bridge\Monolog\Command\ServerLogCommand) binds to 0.0.0.0:9911 by default and processes each received frame with unserialize(base64_decode($message)) without authentication, integrity checks, or an allowed_classes allowlist, allowing any reachable host to submit attacker-chosen serialized PHP payloads that can crash the listener and may trigger object-injection gadget effects. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-54058

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T17:17:03.433 |

Pillow is a Python imaging library. Prior to 12.3.0, when Pillow loads an uncompressed McIdas AREA image from a filename through the mmap raw codec path, attacker-controlled header words can set a row stride smaller than the natural row width, causing pixel access such as Image.tobytes(), getpixel, convert, or save to read beyond the mapped region and disclose adjacent process memory or fault. This issue is fixed in version 12.3.0.

### CVE-2026-15736

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-73;CWE-89` |
| Published | 2026-07-14T15:17:01.073 |

Snowflake SQLAlchemy versions prior to 1.11.0 contain several security vulnerabilities, including: Improper handling of user-supplied column identifiers in merge operations could allow SQL injection through attacker-controlled input keys. An attacker may be able to exploit this through request field names in a dynamic upsert endpoint, potentially enabling read access to data visible to the application's database role or modification of values within the same MERGE statement. Improper literal rendering of bound parameters when building certain Snowflake-specific table creation queries could allow SQL injection. An attacker may be able to exploit this by supplying a crafted string to any application endpoint that passes user-controlled data through the affected query-building API, potentially causing arbitrary data exfiltration within the scope of the connection role. Improper forwarding of connection configuration parameters could allow an attacker to cause the library to read arbitrary local files and transmit their contents to an attacker-controlled endpoint. An attacker may be able to exploit this in deployment environments that accept user-controlled connection parameters, potentially exposing sensitive files accessible to the application process. The fix is available in Snowflake SQLAlchemy version 1.11.0. Users must manually upgrade.

### CVE-2026-13585

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:N/VI:N/VA:H/SC:H/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-226;CWE-770` |
| Published | 2026-07-15T02:18:12.213 |

Allocation of Resources Without Limits and Throttling and Sensitive Information in Resource Not Removed Before Reuse in the ASUS System Control Interface driver and ASUS Business Manager allow a local administrator to disclose sensitive information via crafted IOCTL requests, which, in severe cases, may lead to a Denial of Service (DoS) on the system.
Refer to the ' 
Security Update for ASUS System Control Interface  ' section on the ASUS Security Advisory for more information.

### CVE-2026-48290

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T22:17:00.840 |

CAI Content Credentials is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-50528

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-302;CWE-636;CWE-863` |
| Published | 2026-07-14T20:17:37.533 |

Incorrect authorization in .NET allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-48345

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-14T20:17:07.573 |

Animate is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-47984

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:04.223 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access. Exploitation of this issue does not require user interaction.

### CVE-2026-47423

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T20:17:02.143 |

DOMPurify is a DOM-only cross-site scripting sanitizer for HTML, MathML, and SVG. In 3.4.4, DOMPurify allowed selectedcontent by default, allowing browsers to re-clone an XSS payload after sanitization so that unsanitized markup inside <selectedcontent> is returned. This issue is fixed in version 3.4.5.

### CVE-2026-45133

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-776;CWE-1333` |
| Published | 2026-07-14T19:17:06.913 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. Prior to 5.4.52, 6.4.40, 7.4.12, and 8.0.12, when the parser is exposed to attacker-controlled input, deeply nested mappings or sequences cause both the block-level (Parser::parseBlock()) and inline (Inline::parseSequence() / Inline::parseMapping()) parsers to recurse without a depth limit. A crafted document exhausts the PHP stack and crashes the worker. This issue is fixed in versions 5.4.52, 6.4.40, 7.4.12, and 8.0.12.

### CVE-2026-50680

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:02.470 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-50429

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125;CWE-200` |
| Published | 2026-07-14T18:17:46.573 |

Out-of-bounds read in Windows Kernel allows an unauthorized attacker to disclose information over a network.

### CVE-2026-45756

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-07-14T18:17:17.563 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. From 7.3.0-BETA1 until 7.4.12 and 8.0.12, the JsonPath component compiles attacker-controlled match() and search() filter patterns directly into preg_match() without a length cap, i-regexp restriction, or bounded backtracking, allowing catastrophic-backtracking expressions to pin worker CPU and cause denial of service. This issue is fixed in versions 7.4.12 and 8.0.12.

### CVE-2026-59197

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-07-14T17:17:14.487 |

Pillow is a Python imaging library. Prior to 12.3.0, Pillow's public rank-filter API can trigger a native heap out-of-bounds write when given a very large odd filter size because ImageFilter.RankFilter.filter() calls image.expand(size // 2, size // 2) before rank-filter size validation and ImagingExpand() computes output dimensions with unchecked signed int arithmetic. This issue is fixed in version 12.3.0.

### CVE-2026-50338

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-14T17:17:00.020 |

Improper authentication in Azure Spring Apps allows an authorized attacker to elevate privileges over a network.

### CVE-2026-9636

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-299` |
| Published | 2026-07-14T16:17:05.860 |

A security issue exists within CompactLogix® 5380, ControlLogix® 5580, and EN4 communication modules related to CIP Security certificate revocation handling. The security issue stems from the controller failing to properly reject certificates signed by an intermediate certificate that has been revoked via a Certificate Revocation List (CRL). This could allow a network-based attacker to establish a connection using a certificate that should be untrusted, potentially bypassing CIP Security protections.

### CVE-2026-14504

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-14T16:16:45.423 |

An authorization bypass in Nexus Repository 3's component upload API allowed a user with only read/browse privileges on a Swift, Terraform, or Conda hosted repository to upload arbitrary artifacts, bypassing the intended write-permission check.

### CVE-2026-10672

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T15:16:55.560 |

subsys/net/lib/lwm2m/lwm2m_pull_context.c copied the firmware-update Package URI into a fixed static buffer (context.uri, size CONFIG_LWM2M_SWMGMT_PACKAGE_URI_LEN, default 128) with memcpy(context.uri, uri, LWM2M_PACKAGE_URI_LEN), copying exactly the destination size with no length validation. The Firmware-Update object stores the server-supplied Package URI (/5/0/1) in a 255-byte buffer, so a LwM2M management server (or an on-path attacker on a session lacking strong DTLS) can WRITE a URI of 128-254 characters; only the first 128 bytes are then copied into context.uri with no NUL terminator. That buffer is subsequently consumed as a C string by http_parser_parse_url(context.uri, strlen(context.uri), ...), strlen-based CoAP URI-path/PROXY-URI option appends, and lwm2m_parse_peerinfo(), causing an out-of-bounds read of adjacent static memory. The over-read bytes are appended to outbound CoAP requests (information disclosure of adjacent device memory to the server/proxy) and can crash the device (denial of service). The vulnerable copy was introduced by the pull-context refactor (first released in v3.0.0) and is present through v4.4.0; the default-on CONFIG_LWM2M_FIRMWARE_UPDATE_PULL_SUPPORT path is affected. The fix adds a strlen(uri) >= sizeof(context.uri) check returning -ENOMEM and switches to strcpy(), guaranteeing a bounded, NUL-terminated buffer.

### CVE-2026-57821

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-15T10:16:47.620 |

A SQL Injection vulnerability exists in Apache Fineract's Office Search API (GET /api/v1/offices) in versions up to and including 1.14.0. The orderBy request parameter is concatenated into a SQL query without sufficient validation, allowing an authenticated user with permission to view offices to inject arbitrary SQL via a crafted orderBy value. This is a bypass of the ColumnValidator fix introduced for CVE-2024-32838, which does not detect bare subqueries in the ORDER BY position. This can be leveraged to perform time-based blind SQL injection for data exfiltration. Because the injected query blocks the database connection for its full duration, concurrent exploitation can exhaust the application's database connection pool, resulting in denial of service for other users. Users are recommended to upgrade to a version containing the fix.

### CVE-2026-12281

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-15T06:16:43.840 |

The Shibboleth WordPress plugin before 2.5.4 does not fail closed when its HTTP header identity mode is enabled without an anti-spoofing key, treating any request that carries identity headers as an authenticated session without verifying them. On a deployment where untrusted client headers reach the application, an unauthenticated attacker can log in with forged identity headers and, when automatic account creation and the default administrator role mapping are enabled, create and sign in as a new administrator. Exploitation requires the non-default HTTP header attribute mode, an empty or absent spoof key, automatic account creation enabled, and a deployment that does not strip untrusted client headers before they reach the application.

### CVE-2026-48349

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:08.067 |

Animate is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-47995

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T20:17:04.727 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a high-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-47304

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-07-14T19:17:08.830 |

Improper verification of cryptographic signature in .NET allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-58617

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:18:44.260 |

Improper access control in Microsoft 365 Copilot for iOS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-56186

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:28.440 |

Out-of-bounds read in Windows Schannel allows an authorized attacker to disclose information over a network.

### CVE-2026-50686

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:03.900 |

Access of resource using incompatible type ('type confusion') in Windows OLE allows an unauthorized attacker to execute code over a network.

### CVE-2026-50487

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:54.870 |

Use after free in Microsoft Windows DNS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50460

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:51.167 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50439

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:48.123 |

Use after free in Microsoft Message Queuing Queue Manager allows an unauthorized attacker to execute code over a network.

### CVE-2026-58595

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-1021` |
| Published | 2026-07-14T17:17:12.530 |

Improper restriction of rendered ui layers or frames in Microsoft Bing App for IOS allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-56169

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-14T17:17:10.027 |

Improper authentication in Windows Admin Center allows an authorized attacker to elevate privileges over a network.

### CVE-2026-54995

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:07.143 |

Use after free in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over a network.

### CVE-2026-50694

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:02.327 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an unauthorized attacker to execute code over a network.

### CVE-2026-49164

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:51.033 |

Heap-based buffer overflow in Active Directory Domain Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-42900

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:47.993 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows App Store allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50683

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:02.967 |

Heap-based buffer overflow in Windows DHCP Server allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-50502

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-07-14T18:17:57.277 |

Insufficient granularity of access control in Windows Event Logging Service allows an authorized attacker to execute code over a network.

### CVE-2026-50365

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-14T18:17:37.010 |

Improper authentication in Windows RPC API allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-58647

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T17:17:14.370 |

Improper neutralization of input during web page generation ('cross-site scripting') in Power BI allows an authorized attacker to perform spoofing over a network.

### CVE-2026-49169

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:51.813 |

Use after free in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-42975

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:48.157 |

Heap-based buffer overflow in Windows Bluetooth Port Driver allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-40400

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-14T17:16:47.447 |

Relative path traversal in Windows PowerShell allows an authorized attacker to execute code over a network.

### CVE-2026-48346

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-14T20:17:07.700 |

Animate is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-58558

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-840` |
| Published | 2026-07-15T13:17:31.053 |

Permission control vulnerability in the file system. Impact: Successful exploitation of this vulnerability may affect service confidentiality.

### CVE-2026-15809

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-07-15T13:17:03.933 |

A flaw was found in CRI-O. The fix for a previous vulnerability (CVE-2022-4318) was incorrect, allowing it to be bypassed. An attacker capable of setting environment variables on a container can inject a newline character into the HOME environment variable. This issue allows the addition of arbitrary lines into /etc/passwd by use of a specially crafted environment variable.

### CVE-2026-40633

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-532` |
| Published | 2026-07-15T11:16:25.463 |

Dell PowerScale OneFS versions 9.5.0.0 through 9.10.1.7, versions 9.11.0.0 through 9.13.0.2 contains an Insertion of Sensitive Information into Log File vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information disclosure.

### CVE-2026-48337

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T22:17:02.090 |

Illustrator is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48336

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T22:17:01.963 |

Illustrator is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48335

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T22:17:01.840 |

Illustrator is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48370

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:01.000 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48369

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:00.893 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48367

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:00.660 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48366

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:00.553 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48344

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-14T21:17:00.327 |

Creative Cloud Desktop is affected by a Time-of-check Time-of-use (TOCTOU) Race Condition vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48343

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:00.217 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48342

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-14T21:17:00.113 |

Bridge is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48341

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:17:00.007 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48340

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T21:16:59.897 |

Bridge is affected by an Untrusted Pointer Dereference vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48339

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:59.790 |

Bridge is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48311

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:16:58.383 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48274

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:16:57.910 |

After Effects is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48272

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-14T21:16:57.710 |

Creative Cloud Desktop is affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48270

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:16:57.580 |

Premiere Pro is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48269

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:57.473 |

Premiere Pro is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47976

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T21:16:57.120 |

Media Encoder is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47971

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T21:16:56.980 |

Media Encoder is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47472

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T21:16:56.333 |

NVIDIA TensorRT-LLM contains a vulnerability in its inter-process communication layer where an attacker with local same-user access could cause deserialization. A successful exploit of this vulnerability might lead to code execution, information disclosure, data tampering, and denial of service.

### CVE-2026-24272

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:44.817 |

NVIDIA TensorRT contains a vulnerability where an attacker might cause an overflow to a heap-based buffer. A successful exploit of this vulnerability might lead to code execution.

### CVE-2026-24268

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:44.610 |

NVIDIA TensorRT contains a vulnerability where an attacker might cause a heap-based buffer overflow. A successful exploit of this vulnerability might lead to code execution.

### CVE-2026-24238

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-07-14T21:16:44.397 |

NVIDIA TensorRT for contains a vulnerability where an attacker might cause an improper validation of array index. A successful exploit of this vulnerability might lead to code execution.

### CVE-2026-50650

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T20:17:38.230 |

Improper control of generation of code ('code injection') in .NET Framework allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-50649

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T20:17:38.103 |

Deserialization of untrusted data in .NET allows an unauthorized attacker to execute code locally.

### CVE-2026-50646

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-693` |
| Published | 2026-07-14T20:17:37.670 |

Protection mechanism failure in .NET Framework allows an unauthorized attacker to execute code locally.

### CVE-2026-47305

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-14T19:17:08.970 |

Protection mechanism failure in Visual Studio allows an unauthorized attacker to execute code locally.

### CVE-2026-58634

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:45.650 |

Use after free in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-58633

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:45.530 |

Use after free in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-58632

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:45.370 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-58628

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:18:44.953 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Wireless Networking allows an authorized attacker to elevate privileges locally.

### CVE-2026-58613

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:44.007 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-58542

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:42.153 |

Heap-based buffer overflow in Windows Media allows an unauthorized attacker to execute code locally.

### CVE-2026-58541

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:41.560 |

Access of resource using incompatible type ('type confusion') in Windows DWM allows an authorized attacker to elevate privileges locally.

### CVE-2026-58540

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T18:18:41.377 |

Improper authorization in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-58538

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:41.060 |

Heap-based buffer overflow in Windows Bluetooth Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-58537

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:40.927 |

Use after free in Microsoft NAT Helper Components (ipnathlp.dll) allows an authorized attacker to elevate privileges locally.

### CVE-2026-58536

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:40.770 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-58532

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-14T18:18:40.027 |

Integer overflow or wraparound in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-58530

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:39.697 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an unauthorized attacker to execute code locally.

### CVE-2026-58527

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:18:39.207 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-57968

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-07-14T18:18:35.273 |

Buffer over-read in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-57096

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:34.520 |

Heap-based buffer overflow in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-57091

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:33.620 |

Stack-based buffer overflow in Windows File History Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-57088

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:18:33.080 |

Improper access control in Extensible Storage Engine (ESENT) allows an authorized attacker to elevate privileges locally.

### CVE-2026-56650

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-07-14T18:18:32.100 |

Heap-based buffer overflow in Windows Network File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-56644

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:30.650 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-56643

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:30.497 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-56189

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:28.997 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code locally.

### CVE-2026-56182

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:25.010 |

Integer overflow or wraparound in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-56176

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:23.630 |

Out-of-bounds read in Windows Win32K - GRFX allows an authorized attacker to elevate privileges locally.

### CVE-2026-56175

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:23.460 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-56156

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:22.537 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55949

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-07-14T18:18:22.320 |

Use of uninitialized resource in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55947

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:22.050 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55141

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:21.123 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55140

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:20.997 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55137

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:20.583 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55136

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T18:18:20.437 |

Untrusted pointer dereference in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55134

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:20.163 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55133

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:20.003 |

Heap-based buffer overflow in Microsoft Office OneNote allows an unauthorized attacker to execute code locally.

### CVE-2026-55132

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-14T18:18:19.850 |

Double free in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55131

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:19.717 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55130

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:19.587 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55129

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:19.463 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55128

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:19.320 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55127

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:19.180 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55125

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:18.920 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55123

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-681` |
| Published | 2026-07-14T18:18:18.633 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code locally.

### CVE-2026-55120

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:18.220 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code locally.

### CVE-2026-55058

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:18.087 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:17.827 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55055

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:17.683 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55053

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:17.410 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55049

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:16.860 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55048

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:16.680 |

Integer overflow or wraparound in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55044

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:16.043 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55043

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:15.897 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code locally.

### CVE-2026-55041

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:15.570 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55039

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-07-14T18:18:15.257 |

Integer underflow (wrap or wraparound) in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55038

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:18:15.083 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55037

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:14.883 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55036

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-07-14T18:18:14.700 |

Buffer over-read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55033

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:14.293 |

Integer overflow or wraparound in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55032

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:14.150 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-55031

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:14.013 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55029

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:13.757 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55025

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:13.190 |

Access of resource using incompatible type ('type confusion') in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55024

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:13.060 |

Access of resource using incompatible type ('type confusion') in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55022

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:12.780 |

Access of resource using incompatible type ('type confusion') in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55018

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:12.287 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-55017

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:12.163 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-54131

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:09.123 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-54125

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:08.513 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-54124

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:08.373 |

Integer overflow or wraparound in Windows Terminal allows an unauthorized attacker to execute code locally.

### CVE-2026-54115

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:18:07.537 |

Integer overflow or wraparound in Windows Active Directory allows an authorized attacker to elevate privileges locally.

### CVE-2026-50689

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:05.017 |

Use after free in Windows Clipboard Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-50688

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:04.580 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50679

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:18:02.310 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-50677

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:02.063 |

Use after free in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50676

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:01.897 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50673

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-476` |
| Published | 2026-07-14T18:18:01.457 |

Null pointer dereference in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50667

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:18:00.433 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-50665

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:00.080 |

Out-of-bounds read in Microsoft Office allows an unauthorized attacker to disclose information locally.

### CVE-2026-50655

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:59.123 |

Heap-based buffer overflow in Windows Media allows an unauthorized attacker to execute code locally.

### CVE-2026-50510

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-641` |
| Published | 2026-07-14T18:17:58.233 |

Improper restriction of names for files and other resources in Github Copilot allows an unauthorized attacker to execute code locally.

### CVE-2026-50509

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T18:17:58.057 |

Deserialization of untrusted data in Windows Wireless Wide Area Network Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50501

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:57.137 |

Stack-based buffer overflow in Windows Resilient File System (ReFS) allows an unauthorized attacker to execute code locally.

### CVE-2026-50499

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:56.813 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-50498

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-07-14T18:17:56.640 |

Windows Universal Disk Format File System Driver (UDFS) Elevation of Privilege Vulnerability

### CVE-2026-50494

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:55.943 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-50493

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:55.800 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50488

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-14T18:17:54.993 |

Improper neutralization of special elements used in a command ('command injection') in Windows Clipboard User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50486

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:54.740 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50484

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:54.420 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50480

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:53.990 |

Heap-based buffer overflow in Windows Web Proxy Auto-Discovery Protocol (WPAD) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50479

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T18:17:53.857 |

Untrusted pointer dereference in Windows USB Hub Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-50478

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:53.710 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50476

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:53.360 |

Use after free in Microsoft Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-50471

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:52.677 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50469

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T18:17:52.357 |

Improper link resolution before file access ('link following') in Windows Projected File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50467

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:52.100 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-50466

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:51.977 |

Use after free in Windows Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50462

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-14T18:17:51.497 |

External control of file name or path in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-50461

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:51.317 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50458

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:50.910 |

Use after free in Microsoft Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50457

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:50.773 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50454

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-14T18:17:50.290 |

Relative path traversal in Windows User Interface Core allows an authorized attacker to elevate privileges locally.

### CVE-2026-50450

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:17:49.633 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Wireless Wide Area Network Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50448

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:49.290 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50441

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T18:17:48.423 |

Untrusted pointer dereference in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50440

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:48.300 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50436

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:47.717 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50435

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126;CWE-190` |
| Published | 2026-07-14T18:17:47.547 |

Buffer over-read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-50433

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:47.240 |

Use after free in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50427

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:46.283 |

Use after free in Content Delivery Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-50425

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:45.990 |

Use after free in Windows Internal System User Profile allows an authorized attacker to elevate privileges locally.

### CVE-2026-50423

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:17:45.737 |

Improper access control in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50422

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:45.567 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-50421

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:17:45.410 |

Access of resource using incompatible type ('type confusion') in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-50417

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-07-14T18:17:44.813 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-50412

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:44.110 |

Stack-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-50407

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:43.333 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50405

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-07-14T18:17:43.033 |

Insufficient granularity of access control in Windows Filtering Platform (WFP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50402

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126;CWE-681` |
| Published | 2026-07-14T18:17:42.600 |

Incorrect conversion between numeric types in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-50400

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:42.280 |

Stack-based buffer overflow in Windows App Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-50399

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:42.147 |

Out-of-bounds read in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50391

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-14T18:17:41.093 |

Improper privilege management in Windows Group Policy allows an authorized attacker to elevate privileges locally.

### CVE-2026-50388

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-07-14T18:17:40.580 |

Out-of-bounds read in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50387

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:40.390 |

Stack-based buffer overflow in Windows GDI allows an authorized attacker to elevate privileges locally.

### CVE-2026-50386

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:40.213 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50378

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:17:39.183 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Key Guard allows an authorized attacker to elevate privileges locally.

### CVE-2026-50373

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:17:38.360 |

Improper access control in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-50367

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-118;CWE-822` |
| Published | 2026-07-14T18:17:37.363 |

Incorrect access of indexable resource ('range error') in Windows Sensor Data Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50363

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:36.737 |

Heap-based buffer overflow in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-50362

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:36.580 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an unauthorized attacker to execute code locally.

### CVE-2026-50361

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415` |
| Published | 2026-07-14T18:17:36.453 |

Double free in Microsoft Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50357

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-07-14T18:17:35.790 |

Numeric truncation error in Windows Resilient File System (ReFS) allows an authorized attacker to execute code locally.

### CVE-2026-50353

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:35.267 |

Use after free in Windows DirectX allows an authorized attacker to elevate privileges locally.

### CVE-2026-50347

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T18:17:34.627 |

Heap-based buffer overflow in Windows Data dll allows an unauthorized attacker to execute code locally.

### CVE-2026-50346

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T18:17:34.470 |

Improper authorization in RPC Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50344

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T18:17:34.120 |

Improper authorization in Windows OLE allows an authorized attacker to elevate privileges locally.

### CVE-2026-50343

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-14T18:17:33.973 |

Improper privilege management in Microsoft Install Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50337

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-704` |
| Published | 2026-07-14T18:17:33.200 |

Incorrect type conversion or cast in Windows Notification allows an authorized attacker to elevate privileges locally.

### CVE-2026-50336

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:33.073 |

Heap-based buffer overflow in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50335

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:17:32.923 |

Improper access control in Windows Operating Systems allows an authorized attacker to elevate privileges locally.

### CVE-2026-50332

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-07-14T18:17:32.420 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50331

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:32.263 |

Use after free in Windows Application Model allows an authorized attacker to elevate privileges locally.

### CVE-2026-50329

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:31.940 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50327

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:31.657 |

Heap-based buffer overflow in Windows Media allows an authorized attacker to execute code locally.

### CVE-2026-50326

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:31.527 |

Use after free in Windows Unified Consent System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50321

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:30.903 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-50317

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:30.690 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Operating Systems allows an authorized attacker to elevate privileges locally.

### CVE-2026-50315

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-14T18:17:30.003 |

Null pointer dereference in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-50314

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:29.863 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-50313

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:29.680 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50309

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:29.013 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-50306

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-416` |
| Published | 2026-07-14T18:17:28.497 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-50305

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:28.377 |

Use after free in Microsoft Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-50301

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:27.880 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-48368

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T18:17:19.317 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48365

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T18:17:19.197 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48309

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T18:17:19.060 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47968

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T18:17:18.810 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T18:17:18.680 |

Audition is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47642

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:18.550 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-47290

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:17.760 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-58636

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T17:17:13.970 |

Improper link resolution before file access ('link following') in Window PC Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-58635

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-14T17:17:13.833 |

Improper neutralization of special elements used in a command ('command injection') in Windows Narrator Braille allows an authorized attacker to elevate privileges locally.

### CVE-2026-58631

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-14T17:17:13.717 |

Improper authorization in Windows Admin Center allows an authorized attacker to execute code locally.

### CVE-2026-58618

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:13.587 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-58610

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:13.260 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code locally.

### CVE-2026-58609

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T17:17:13.097 |

Out-of-bounds read in Microsoft Graphics Component allows an unauthorized attacker to execute code locally.

### CVE-2026-58602

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:12.817 |

Use after free in Windows Kernel Mode Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-58601

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:12.657 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-57107

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-14T17:17:10.860 |

Improper authentication in Windows Admin Center allows an authorized attacker to elevate privileges locally.

### CVE-2026-56155

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-07-14T17:17:09.763 |

Insufficient granularity of access control in Active Directory Federation Services (AD FS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-55948

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:09.637 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55899

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-121` |
| Published | 2026-07-14T17:17:09.443 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-55014

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:17:09.217 |

Improper access control in Windows Remote Help Defense allows an authorized attacker to elevate privileges locally.

### CVE-2026-55012

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T17:17:09.107 |

Integer overflow or wraparound in Microsoft Defender allows an unauthorized attacker to execute code locally.

### CVE-2026-55011

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-14T17:17:08.990 |

Integer underflow (wrap or wraparound) in Microsoft Defender allows an unauthorized attacker to execute code locally.

### CVE-2026-55009

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:08.883 |

Deserialization of untrusted data in Microsoft Exchange Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-55006

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-07-14T17:17:08.650 |

Insufficient granularity of access control in Microsoft Exchange Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-55004

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-14T17:17:08.367 |

Double free in Microsoft Printer Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-55002

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-14T17:17:08.070 |

External control of file name or path in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-55001

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-14T17:17:07.943 |

Improper certificate validation in Windows Active Directory allows an authorized attacker to elevate privileges locally.

### CVE-2026-54993

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:07.000 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code locally.

### CVE-2026-54991

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-362` |
| Published | 2026-07-14T17:17:06.720 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-54987

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:06.153 |

Heap-based buffer overflow in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-54986

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:06.003 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-54114

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:04.267 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-54112

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:17:04.123 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-54109

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T17:17:03.853 |

Integer overflow or wraparound in Windows Resilient File System (ReFS) allows an authorized attacker to execute code locally.

### CVE-2026-50697

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-14T17:17:02.813 |

Exposure of sensitive information to an unauthorized actor in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-50675

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:02.053 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-50351

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:17:00.390 |

Improper access control in Windows Audio Compression Manager (ACM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50333

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T17:16:59.860 |

Missing authentication for critical function in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-50318

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T17:16:59.410 |

Stack-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50311

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:16:59.090 |

Improper access control in Windows Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-50308

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-07-14T17:16:58.927 |

Integer underflow (wrap or wraparound) in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-50293

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:57.570 |

Use after free in Windows Internal Task Bar allows an authorized attacker to elevate privileges locally.

### CVE-2026-49808

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:57.443 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-49800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-07-14T17:16:56.193 |

Integer overflow or wraparound in Windows Web Proxy Auto-Discovery Protocol (WPAD) allows an authorized attacker to elevate privileges locally.

### CVE-2026-49797

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:55.693 |

Heap-based buffer overflow in Windows NTFS allows an unauthorized attacker to execute code locally.

### CVE-2026-49796

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:55.523 |

Heap-based buffer overflow in Windows GDI+ allows an unauthorized attacker to execute code locally.

### CVE-2026-49793

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:55.050 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to execute code locally.

### CVE-2026-49792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-07-14T17:16:54.893 |

Numeric truncation error in Windows Resilient File System (ReFS) allows an authorized attacker to execute code locally.

### CVE-2026-49783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-358` |
| Published | 2026-07-14T17:16:53.747 |

Improperly implemented security check for standard in Windows Secure Boot allows an authorized attacker to bypass a security feature locally.

### CVE-2026-49176

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-269` |
| Published | 2026-07-14T17:16:52.780 |

Improper privilege management in Windows WalletService allows an authorized attacker to elevate privileges locally.

### CVE-2026-49175

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:16:52.650 |

Heap-based buffer overflow in Windows DNS allows an authorized attacker to elevate privileges locally.

### CVE-2026-49173

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:52.390 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-49170

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-1220` |
| Published | 2026-07-14T17:16:51.930 |

Insufficient granularity of access control in Windows StateRepository API allows an authorized attacker to elevate privileges locally.

### CVE-2026-49166

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:51.370 |

Use after free in Microsoft Printer Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-48581

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-07-14T17:16:50.767 |

Insufficient granularity of access control in Microsoft Surface allows an authorized attacker to elevate privileges locally.

### CVE-2026-47296

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-14T17:16:49.507 |

Improper neutralization of special elements used in an sql command ('sql injection') in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-44800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:48.667 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-42982

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1288` |
| Published | 2026-07-14T17:16:48.330 |

Improper validation of consistency within input in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-10669

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T15:16:55.210 |

On Xtensa SoCs built with CONFIG_XTENSA_MPU and CONFIG_USERSPACE, arch_buffer_validate() in arch/xtensa/core/mpu.c — the architecture hook that verifies a user-mode-supplied buffer is accessible to the calling user thread with the requested permission — defaulted its return value to 0 (access permitted) and only set a denial result inside its per-MPU-region probe loop. When the rounded extent of the buffer wraps the 32-bit address space (size + alignment offset near SIZE_MAX, or ROUND_UP(size + offset) overflowing to 0), the loop executes zero iterations and the function returns 0 = permitted without probing any MPU region.

The syscall-layer pre-checks (K_SYSCALL_MEMORY_SIZE_CHECK / Z_DETECT_POINTER_OVERFLOW) only catch a raw addr+size wrap and do not cover the ROUND_UP-induced wrap, and the string path (arch_user_string_nlen -> arch_buffer_validate) has no syscall-layer guard at all.

An unprivileged user-mode thread can therefore pass a crafted (addr, size) to any syscall that validates user buffers via k_usermode_from_copy/to_copy or k_usermode_string_copy and have validation succeed for memory it must not access; the kernel then reads from (disclosure) or, with write=1, writes to (corruption) attacker-chosen kernel or other-partition memory on the thread's behalf, enabling information disclosure, memory corruption, privilege escalation, and denial of service.

Affected from v3.7.0 (when Xtensa MPU userspace support was added) through v4.4.0. The fix changes the default to -EINVAL (deny by default), adds an explicit size_add_overflow check, and sets the success value only after the full range has been validated.

### CVE-2026-14251

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-15T08:16:22.383 |

A flaw was found in the OpenShift GitOps operator. The ClusterRole reconciler does not validate resource ownership when reconciling ClusterRole objects. A namespace-scoped Argo CD instance can trigger deletion of a ClusterRole owned by a cluster-scoped Argo CD instance by crafting a name collision, resulting in a denial of service.

### CVE-2026-46634

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-14T22:16:56.130 |

Twig is a template language for PHP. From 3.9.0 until 3.26.0, template_from_string() compiles an inner template under a synthesized __string_template__<hash> name that can fall outside a SourcePolicyInterface sandbox decision, allowing a sandboxed template that can call template_from_string and include to render an inner template without security policy enforcement. This issue is fixed in version 3.26.0.

### CVE-2026-49853

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-14T21:17:02.130 |

Tornado is a Python web framework and asynchronous networking library. Prior to 6.5.6, SimpleAsyncHTTPClient shallow-copied redirected requests and removed only the Host header, leaving Authorization, auth_username, auth_password, and auth_mode in place when a redirect changed scheme, host, or port. This issue is fixed in version 6.5.6.

### CVE-2026-48332

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T21:16:59.583 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48328

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T21:16:59.363 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48348

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:07.940 |

Animate is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48347

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-14T20:17:07.820 |

Animate is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-15392

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-07-14T16:16:45.827 |

DBD::File versions before 1.651 for Perl do not ensure the table file is not a symlink to an untrusted location.

The complete_table_name method builds the absolute table file path without checking whether the file is a symbolic link. A link inside the data directory can point to a table file at any path outside of the configured f_dir and f_dir_search directories.

Callers of file-based drivers can read or write files outside of the data directory.

### CVE-2026-14903

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-07-14T15:16:57.113 |

Path traversal in Ivanti  Xtraction before version 2026.2.1 allows a remote authenticated attacker to read arbitrary files outside the web root.

### CVE-2026-47996

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T20:17:04.840 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A high-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-45074

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-14T18:17:16.990 |

Symfony is a PHP framework for web and console applications and a set of reusable PHP components. From 7.1.0 until 7.4.12 and 8.0.12, Cas2Handler builds the CAS service parameter from Request::getSchemeAndHttpHost(), which reflects an attacker-controlled Host header when framework.trusted_hosts is not configured; an attacker controlling another application registered with the same CAS server can replay a victim ticket against the Symfony application and authenticate as the victim. This issue is fixed in versions 7.4.12 and 8.0.12.

### CVE-2026-54572

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T22:17:16.533 |

Rclone is a command-line program to sync files and directories to and from different cloud storage providers. Prior to 1.74.4, with -l/--links, rclone serializes symlinks as .rclonelink text objects and recreates them on a local destination without validating the target, allowing an attacker-controlled remote to plant an escaping symlink and cause a following object write to land outside the destination with attacker-chosen contents. This issue is fixed in version 1.74.4.

### CVE-2026-48352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T22:17:02.357 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-48351

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-14T22:17:02.210 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-48295

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-14T22:17:00.960 |

CAI Content Credentials is affected by an Insufficiently Protected Credentials vulnerability that could result in disclosure of sensitive information. An attacker could leverage this vulnerability to gain unauthorized read access. Exploitation of this issue does not require user interaction.

### CVE-2026-49855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-14T21:17:02.437 |

Tornado is a Python web framework and asynchronous networking library. Prior to 6.5.6, Tornado gzip decompression routines processed limited-size chunks but did not enforce an overall limit on accumulated decompressed chunks, allowing a malicious server accessed by SimpleAsyncHTTPClient or an HTTPServer configured with decompress_request=True to consume effectively unlimited memory. This issue is fixed in version 6.5.6.

### CVE-2026-49477

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-07-14T21:17:02.007 |

Soup Sieve is a CSS selector library designed to be used with Beautiful Soup 4. Prior to 2.8.4, the CSS selector parser in soupsieve contains a regular expression vulnerable to catastrophic backtracking when processing an attribute selector with an unterminated quoted value in soupsieve/css_parser.py, allowing an attacker who can supply untrusted CSS selector strings to soupsieve.compile() or Beautiful Soup .select() / .select_one() to cause CPU exhaustion and denial of service. This issue is fixed in version 2.8.4.

### CVE-2026-49476

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-14T21:17:01.877 |

Soup Sieve is a CSS selector library designed to be used with Beautiful Soup 4. Prior to 2.8.4, the CSS selector parser in soupsieve allocates unbounded memory when compiling large comma-separated selector lists, allowing an attacker who can supply a crafted selector string to soupsieve.compile() or Beautiful Soup .select() / .select_one() to allocate hundreds of megabytes of heap memory from a relatively small input and cause denial of service. This issue is fixed in version 2.8.4.

### CVE-2026-48815

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-14T21:17:01.370 |

sigstore-js provides JavaScript libraries for interacting with Sigstore services. Prior to 4.1.1, the documented certificateOIDs option in sigstore.verify() is accepted by the public API but discarded before verification, so required certificate extension OIDs are never checked and applications relying on certificateOIDs to restrict which certificates may sign artifacts can accept unauthorized certificates. This issue is fixed in version 4.1.1.

### CVE-2026-47471

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T21:16:56.230 |

NVIDIA TensorRT-LLM for any platform contains a vulnerability in tensor deserialization, where an attacker could cause a heap based buffer overflow. A successful exploit of this vulnerability might lead to information disclosure, data tampering, or denial of service.

### CVE-2026-15777

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:43.537 |

Use after free in UI in Google Chrome on Linux prior to 150.0.7871.125 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-15765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:41.887 |

Use after free in Ozone in Google Chrome prior to 150.0.7871.125 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-15764

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T21:16:41.713 |

Use after free in Ozone in Google Chrome on Linux prior to 150.0.7871.125 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-50651

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T20:17:38.387 |

Allocation of resources without limits or throttling in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-50648

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T20:17:37.937 |

Allocation of resources without limits or throttling in .NET Framework allows an unauthorized attacker to deny service over a network.

### CVE-2026-50527

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T20:17:37.363 |

Stack-based buffer overflow in .NET Framework allows an unauthorized attacker to deny service over a network.

### CVE-2026-50525

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T20:17:37.120 |

Allocation of resources without limits or throttling in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-50524

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1287` |
| Published | 2026-07-14T20:17:37.000 |

Improper validation of specified type of input in .NET Framework allows an unauthorized attacker to deny service over a network.

### CVE-2026-48069

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-14T20:17:05.867 |

@grpc/grps-js implements the core functionality of gRPC purely in JavaScript, without a C++ addon. Prior to 1.9.16, 1.10.12, 1.11.4, 1.12.7, 1.13.5, and 1.14.4, an invalid incoming compressed message can cause a client or server process that uses @grpc/grpc-js to crash. This issue is fixed in versions 1.9.16, 1.10.12, 1.11.4, 1.12.7, 1.13.5, and 1.14.4.

### CVE-2026-48068

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-14T20:17:05.710 |

@grpc/grps-js implements the core functionality of gRPC purely in JavaScript, without a C++ addon. Prior to 1.9.16, 1.10.12, 1.11.4, 1.12.7, 1.13.5, and 1.14.4, an invalid incoming HTTP/2 stream initiation can cause a server process created using @grpc/grpc-js to crash. This issue is fixed in versions 1.9.16, 1.10.12, 1.11.4, 1.12.7, 1.13.5, and 1.14.4.

### CVE-2026-47737

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-345` |
| Published | 2026-07-14T20:17:03.767 |

Puma is a Ruby/Rack web server built for parallelism. From 5.5.0 until 7.2.1 and 8.0.2, Puma is vulnerable to source IP spoofing when set_remote_address proxy_protocol: :v1 is enabled and persistent connections are used because Puma incorrectly re-parses PROXY protocol headers after each keep-alive request on the same connection, allowing an attacker to inject a second PROXY header and overwrite REMOTE_ADDR. This issue is fixed in versions 7.2.1 and 8.0.2.

### CVE-2026-47736

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T20:17:03.620 |

Puma is a Ruby/Rack web server built for parallelism. From 5.5.0 until 7.2.1 and 8.0.2, when PROXY protocol v1 support is enabled, Puma reads incoming bytes into an internal buffer while waiting for CRLF to determine whether a PROXY v1 line is present, allowing an attacker that continuously sends bytes without CRLF to cause unbounded in-process memory growth and additional CPU cost from repeatedly scanning the growing buffer. This issue is fixed in versions 7.2.1 and 8.0.2.

### CVE-2026-47482

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-07-14T20:17:03.367 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause missing release of memory after effective lifetime. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-47480

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-14T20:17:03.120 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause an uncaught exception. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-47479

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T20:17:03.003 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause uncontrolled resource consumption. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-47478

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-910` |
| Published | 2026-07-14T20:17:02.890 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause the use of an expired file descriptor. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-47477

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T20:17:02.770 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause a stack-based buffer overflow. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-47476

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T20:17:02.620 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker can cause uncontrolled resource consumption. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-15711

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T20:16:57.177 |

A vulnerability was found in libsoup's WebSocket frame parsing implementation. The library fails to validate length rules specified in RFC 6455 §5.5, which mandates that all WebSocket control frames (e.g., PING, PONG, CLOSE) contain a payload of 125 bytes or less. A remote, unauthenticated attacker can exploit this by sending a non-compliant, oversized control frame. Because the parser handles this protocol violation improperly instead of throwing an immediate connection termination error, it triggers a internal processing crash, resulting in a remote denial of service (DoS) for applications utilizing libsoup WebSockets.

### CVE-2026-15709

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-14T20:16:57.027 |

A flaw was found in libsoup's WebSocket implementation when using the permessage-deflate extension. The extension's decompression loop (inflate()) processes data in chunks without enforcing an upper boundary limit on the output buffer size. While libsoup limits the incoming compressed frame size via max_incoming_payload_size, it fails to track or limit memory allocation during decompression. A separate check for decompressed size (max_total_message_size) exists but executes only after inflation is complete, and it is entirely disabled by default for client connections. A remote, unauthenticated attacker can exploit this by sending a small, highly compressed payload (a decompression bomb), causing unbounded memory allocation that triggers an Out-of-Memory (OOM) crash and a Denial of Service (DoS).

### CVE-2026-47302

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T19:17:08.540 |

Allocation of resources without limits or throttling in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-58627

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T18:18:44.790 |

Uncontrolled resource consumption in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-58531

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:39.853 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows SMB allows an authorized attacker to elevate privileges over a network.

### CVE-2026-57108

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:18:35.150 |

Access of resource using incompatible type ('type confusion') in .NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-57089

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:33.237 |

Use after free in Windows SMB Server Network Transport Driver (srvnet.sys) allows an unauthorized attacker to execute code over a network.

### CVE-2026-56648

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-07-14T18:18:31.127 |

Time-of-check time-of-use (toctou) race condition in Windows Network File System allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50685

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-14T18:18:03.603 |

Double free in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-50647

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-14T18:17:58.743 |

Loop with unreachable exit condition ('infinite loop') in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-50505

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:57.810 |

Use after free in Windows Message Queuing allows an authorized attacker to execute code over a network.

### CVE-2026-50500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:56.960 |

Use after free in Windows Netlogon allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50496

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:56.267 |

Out-of-bounds read in Windows Network Policy Server SNMP allows an unauthorized attacker to disclose information over a network.

### CVE-2026-50470

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:52.500 |

Out-of-bounds read in Windows Network Policy Server SNMP allows an unauthorized attacker to disclose information over a network.

### CVE-2026-50463

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:51.707 |

Out-of-bounds read in Windows Kernel allows an unauthorized attacker to disclose information over a network.

### CVE-2026-50424

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-14T18:17:45.867 |

Untrusted pointer dereference in Windows Domain Controller allows an unauthorized attacker to deny service over a network.

### CVE-2026-50414

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:44.413 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Media allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50411

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:43.937 |

Stack-based buffer overflow in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-50379

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:39.340 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Media allows an authorized attacker to elevate privileges over a network.

### CVE-2026-50368

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:37.523 |

Stack-based buffer overflow in Active Directory Federation Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-50355

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:35.490 |

Stack-based buffer overflow in Active Directory Federation Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-50330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:32.087 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50328

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-248` |
| Published | 2026-07-14T18:17:31.783 |

Uncaught exception in Windows Server Update Service allows an unauthorized attacker to perform tampering over a network.

### CVE-2026-50304

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:28.220 |

Stack-based buffer overflow in Active Directory Federation Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-59886

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-14T17:17:15.010 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.4, the univ.Real type converted its mantissa, base, and exponent value to a Python float using exact big-integer exponentiation. A BER, CER, or DER encoded REAL value only a few bytes long can carry a very large exponent, causing float conversion through prettyPrint(), str(), comparison, arithmetic, int(), or an explicit float() call to consume excessive CPU and memory and hang applications that decode untrusted ASN.1 data and then print, log, or compare decoded objects. This issue is fixed in version 0.6.4.

### CVE-2026-59885

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-07-14T17:17:14.880 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.4, the BER, CER, and DER decoders process OBJECT IDENTIFIER and RELATIVE-OID values in quadratic time relative to the number of arcs, so a small crafted payload containing an OID with many arcs consumes excessive CPU per decode() call and can deny service to applications that decode untrusted ASN.1 data. The corresponding encoders have the same quadratic behavior when an application re-encodes previously decoded attacker-supplied values. This issue is fixed in version 0.6.4.

### CVE-2026-59884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T17:17:14.750 |

pyasn1 is a generic ASN.1 library for Python. Prior to 0.6.4, the BER decoder shared by the CER and DER codecs parses long-form tags by accumulating continuation octets without an upper bound on the tag ID size, allowing a crafted input to force construction of an arbitrarily large integer with CPU cost growing quadratically and to trigger unhandled ValueError exceptions in Python 3.11+ error formatting paths. Any application decoding untrusted BER, CER, or DER input is affected. This issue is fixed in version 0.6.4.

### CVE-2026-59200

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-14T17:17:14.620 |

Pillow is a Python imaging library. From 5.1.0 until 12.3.0, PdfParser.PdfStream.decode() in PIL/PdfParser.py calls zlib.decompress() with bufsize set to the PDF stream Length field without bounding the decompressed output size, allowing a crafted FlateDecode PDF stream to exhaust memory from a small file. This issue is fixed in version 12.3.0.

### CVE-2026-56170

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T17:17:10.140 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-54983

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T17:17:05.833 |

Stack-based buffer overflow in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-54119

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-14T17:17:04.660 |

Loop with unreachable exit condition ('infinite loop') in Windows Active Directory allows an unauthorized attacker to deny service over a network.

### CVE-2026-50696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:02.670 |

Heap-based buffer overflow in Windows Internet Key Exchange (IKE) Protocol allows an unauthorized attacker to deny service over a network.

### CVE-2026-50695

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T17:17:02.493 |

Stack-based buffer overflow in Active Directory Federation Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-50653

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-07-14T17:17:01.790 |

Loop with unreachable exit condition ('infinite loop') in Azure Active Directory allows an unauthorized attacker to deny service over a network.

### CVE-2026-50652

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-14T17:17:01.673 |

Deserialization of untrusted data in Azure Active Directory allows an unauthorized attacker to deny service over a network.

### CVE-2026-50506

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T17:17:01.303 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-49788

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T17:16:54.207 |

Allocation of resources without limits or throttling in HTTP/2 allows an unauthorized attacker to deny service over a network.

### CVE-2026-49787

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T17:16:54.053 |

Allocation of resources without limits or throttling in Windows HTTP.sys allows an unauthorized attacker to deny service over a network.

### CVE-2026-49181

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-191` |
| Published | 2026-07-14T17:16:53.277 |

Integer underflow (wrap or wraparound) in Windows DHCP Client allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-49171

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:52.073 |

Use after free in Microsoft Windows Speech allows an authorized attacker to elevate privileges locally.

### CVE-2026-45646

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T17:16:49.253 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-40378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-14T17:16:47.257 |

Memory allocation with excessive size value in Windows Local Security Authority Subsystem Service (LSASS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-60081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T16:17:03.647 |

DBI::ProfileData versions before 1.651 for Perl do not limit the path index.

The path index column of profile dump files is used to allocate an array of data for the parser. An unbounded value allows an attacker to specify a large index and consume available memory.

### CVE-2026-59841

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-923;NVD-CWE-Other` |
| Published | 2026-07-14T16:17:03.520 |

A improper restriction of communication channel to intended endpoints vulnerability in Fortinet FortiSIEMWindowsAgent 7.4.0 through 7.4.1 may allow attacker to escalation of privilege via <insert attack vector here>

### CVE-2026-59836

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-14T16:17:02.727 |

A improper certificate validation vulnerability in Fortinet FortiClientEMS 7.4.3 through 7.4.5, FortiClientEMS 7.4.0 through 7.4.1, FortiClientEMS 7.2 all versions may allow attacker to information disclosure via <insert attack vector here>

### CVE-2026-59205

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-14T16:17:02.370 |

Pillow is a Python imaging library. Prior to 12.3.0, Pillow's ImageCms.ImageCmsTransform.apply(im, imOut) API can trigger controlled native heap corruption when the caller supplies an output image whose mode does not match the transform's declared output mode. This issue is fixed in version 12.3.0.

### CVE-2026-59199

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-787;CWE-787` |
| Published | 2026-07-14T16:17:01.937 |

Pillow is a Python imaging library. Prior to 12.3.0, Pillow public image coordinate APIs can trigger a native heap out-of-bounds write when given coordinates near the signed 32-bit integer limits in Image.paste(), Image.crop(), or Image.alpha_composite(). This issue is fixed in version 12.3.0.

### CVE-2026-12707

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-14T16:16:45.297 |

Summary



Cloudflare quiche was discovered to be vulnerable to memory resource exhaustion due to unbounded queuing of post-handshake client migration events.



Impact



quiche supports the connection migration features described in Section 9 of RFC 9000, which allows a single QUIC connection to survive changes in the network path. Although quiche implements the protections described in Section 9.3 of RFC 9000 to limit server state commitment, it was discovered that the collection of PathEvents, intended to be consumed by applications via the path_event_next() function, was not bounded.



Once the QUIC handshake completed, a peer could exploit rapid source address migration in order to cause unbounded queuing of the PathEvent::ReusedSourceConnectionId type. Servers are vulnerable even if active connection migration is disabled.



Mitigation:

  *  

Applications can call path_event_next() to drain the PathEvent collection, mitigating the attack.


  *  

Users are requested to upgrade to quiche 0.29.3 which is the earliest version that prevents excessive queueing of PathEvent::ReusedSourceConnectionId.

### CVE-2026-12523

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-14T16:16:45.050 |

Summary



Cloudflare quiche's HTTP/3 layer was discovered to be vulnerable to resource exhaustion (i.e., memory) by means of specially crafted HTTP/3 frames.




Impact



HTTP/3 defines multiple frame types to support HTTP message exchanges and connection management. Each frame has a length and a payload whose length depends on the frame type. quiche was found to be vulnerable when parsing some frame types to pre-allocating memory based on the declared length. An attacker would not need to send the number of declared bytes to trigger this issue.



In addition, quiche was found to not apply QPACK decompression limits correctly. This could allow an attacker to send specially crafted HEADERS frames that would cause more memory commitment than otherwise advertised by MAX_FIELD_SECTION_SIZE (configured by set_max_field_section_size()).






Mitigation:

  *  

Users are requested to upgrade to quiche 0.29.3 which is the earliest version containing the fix for this issue.









Credits: Disclosed responsibly by Sébastien Féry

### CVE-2025-53379

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T16:16:42.477 |

A out-of-bounds read vulnerability in Fortinet FortiAuthenticator 6.6.0 through 6.6.2, FortiAuthenticator 6.5 all versions may allow a remote unauthenticated attacker to retrieve sensitive information via a specially crafted request.

### CVE-2026-51105

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T15:17:04.023 |

Buffer Overflow vulnerability in aMULE-Project aMule v.2.3.3 allows a remote attacker to cause a denial of service via the OP_SERVERMESSAGE Handler.

### CVE-2026-48287

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-14T22:17:00.713 |

CAI Content Credentials is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-47473

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-123` |
| Published | 2026-07-14T21:16:56.440 |

NVIDIA TensorRT-LLM contains a vulnerability where an attacker could cause a write-what-where condition. A successful exploit of this vulnerability might lead to data tampering, denial of service, and information disclosure.

### CVE-2026-4017

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T18:17:26.820 |

Buffer Overflow in the entry handler of the TraceEvent() system call could allow an attacker with local access to cause information disclosure, data tampering or a crash of the QNX Neutrino kernel.

### CVE-2026-54127

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:04.993 |

Use after free in Windows Hyper-V allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-15696

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T15:17:00.913 |

A vulnerability has been found in Tenda BE12 Pro 16.03.66.23. The impacted element is the function fromVirtualSer of the file /goform/VirtualSer. Such manipulation of the argument page leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-15695

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T15:17:00.753 |

A flaw has been found in Tenda BE12 Pro 16.03.66.23. The affected element is the function fromDhcpListClient of the file /goform/DhcpListClient. This manipulation of the argument page causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been published and may be used.

### CVE-2026-15694

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-14T15:17:00.583 |

A vulnerability was detected in Tenda BE12 Pro 16.03.66.23. Impacted is the function fromSetIpBind of the file /goform/SetIpBind. The manipulation of the argument page results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit is now public and may be used.

### CVE-2026-24229

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T21:16:44.087 |

NVIDIA TensorRT-LLM for Linux contains a vulnerability in the disaggregated orchestrator component, where an attacker could read, write, or delete internal cluster state by sending requests to the FastAPI server. A successful exploit of this vulnerability might lead to information disclosure, data tampering, and denial of service.

### CVE-2026-55126

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T18:18:19.063 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-55034

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T18:18:14.437 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-55021

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T18:18:12.663 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-50482

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T18:17:54.117 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-58640

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-14T17:17:14.083 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-50364

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T17:17:00.897 |

Improper link resolution before file access ('link following') in Windows Server Backup allows an authorized attacker to elevate privileges locally.

### CVE-2026-49790

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-07-14T17:16:54.543 |

Windows Universal Disk Format File System Driver (UDFS) Elevation of Privilege Vulnerability

### CVE-2026-49789

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-14T17:16:54.360 |

Stack-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-9128

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-07-14T16:17:05.487 |

A code execution security issue exists within Studio 5000 Logix Designer® due to an unquoted search path in the External Tools configuration. The executable paths specified in the external tools configuration file are not properly quoted, and because these paths contain spaces, the operating system may resolve them to unintended executables placed earlier in the search order. If exploited, an attacker could plant a malicious executable in a location within the search path, resulting in arbitrary code execution with the same permissions of the user running the application.

### CVE-2026-9127

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T16:17:05.347 |

A remote code execution security issue exists within Studio 5000 Logix Designer® due to incorrect authorization on a configuration file. This can allow any authenticated user to modify the paths of external tools configured within the application. If exploited, an attacker could alter the configuration to point to a malicious executable, resulting in arbitrary code execution when any user interacts with the external tools functionality.

### CVE-2026-61873

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-15T12:18:22.533 |

Grav before 9.1.8 contains an arbitrary file write vulnerability in the Form plugin's process.save.filename parameter, which is validated against path traversal before Twig processing but never re-validated after rendering. Attackers can submit form data containing path traversal sequences that are processed through Twig templates, allowing them to write arbitrary files including PHP webshells to the web root or other sensitive directories.

### CVE-2026-8919

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-07-15T02:22:57.653 |

Permissive Cross-domain Security Policy with Untrusted Domains in ASUS GameSDK allows a remote user to obtain a local user’s NTLM hash by convincing the user to visit a crafted web page that sends a request containing a UNC path to the application’s local service endpoint. This can result in information disclosure or data tampering, may cause GameSDK to become unavailable, and may also enable access to the victim’s information on other services.
Refer to the ' Security Update for ASUS GameSDK  ' section on the ASUS Security Advisory for more information.

### CVE-2026-47992

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-14T20:17:04.470 |

Adobe Commerce is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A high-privileged attacker could exploit this vulnerability to execute malicious SQL commands, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction.

### CVE-2026-15410

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-14T20:16:56.903 |

Post-authentication improper control of generation of code ('Code Injection') vulnerability has been identified in the SMA1000 Appliance Management Console (AMC) which in specific conditions could potentially enable a remote authenticated attacker as administrator to execute arbitrary OS commands.

### CVE-2026-54433

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T17:17:05.530 |

In Roundcube Webmail before 1.6.17 and 1.7.x before 1.7.2, there is Stored Cross-Site Scripting (XSS) via a crafted plain-text email message. The attacker-controlled JavaScript executes within the victim's authenticated session simply by opening or previewing the message (zero-click).

### CVE-2026-62643

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-14T16:17:04.670 |

In Roundcube Webmail before 1.6.17 and 1.7.x before 1.7.2, insufficient Cascading Style Sheets (CSS) sanitization in HTML e-mail messages may lead to SSRF or Information Disclosure, e.g., if stylesheet links point to local network hosts. NOTE: this issue exists because of insufficient fixes for CVE-2026-35540 and CVE-2026-48843.

### CVE-2026-11917

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T16:16:44.780 |

A path traversal security issue exists within Rockwell Automation ThinManager® software due to improper limitation of file save operations within the API. An authenticated attacker could exploit this vulnerability to write arbitrary files to restricted system directories outside of the application's intended directory.

### CVE-2026-46458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-07-15T13:17:21.560 |

ICU Scandinavia Boomerang is vulnerable to an information disclosure flaw where sensitive credential files are exposed via static HTTP. This allows an unauthenticated remote attacker to retrieve plaintext service account and SMTP credentials by requesting specific XML files from the webroot.
This issue has been fixed in version 2.4.18.029

### CVE-2026-61449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-15T12:18:19.747 |

Grav 2.0.1 contains a decompression-bomb size-cap bypass in ZipArchiver and GPM\Installer. The size bound introduced in 2.0.1 sums the uncompressed size declared in each entry's ZIP central-directory header (ZipArchive::statIndex()['size']) and rejects archives exceeding system.gpm.archive.max_uncompressed_size before extraction. Because this declared size is attacker-forgeable and is not cross-checked against the actual inflated stream, a crafted archive declaring tiny per-entry sizes passes the cap while extractTo() writes the real, much larger content, filling disk or exhausting inodes. The archive must be supplied by a package source or admin upload (admin/operator trust). Fixed in 2.0.2. This is an incomplete fix for GHSA-928x-9mpw-8h56.

### CVE-2026-61440

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-15T12:18:19.170 |

PraisonAI Platform before 0.1.9 fails to properly authorize label and issue-label mutations, allowing workspace members to rename and recolor shared labels and add or remove labels on owner-created issues. Attackers with workspace member privileges can exploit PATCH and POST/DELETE endpoints to alter shared label taxonomy and manipulate issue-label associations without owner or admin authorization.

### CVE-2026-48807

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693;CWE-863` |
| Published | 2026-07-14T22:17:05.090 |

Twig is a template language for PHP. Prior to 3.27.0, the sandbox __toString() checks do not fully cover Traversable values passed to join and replace filters or operands evaluated by the in and not in operators, allowing contained Stringable objects to be coerced to strings without consulting the sandbox policy. This issue is fixed in version 3.27.0.

### CVE-2026-48806

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693;CWE-863` |
| Published | 2026-07-14T22:17:04.943 |

Twig is a template language for PHP. Prior to 3.27.0, ArrayExpression does not guard dynamic mapping keys that are coerced to strings, allowing PHP to invoke __toString() on a Stringable object used as a mapping key without calling SandboxExtension::ensureToStringAllowed(). This issue is fixed in version 3.27.0.

### CVE-2026-47732

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-14T22:16:59.667 |

Twig is a template language for PHP. Prior to 3.26.0, several Twig language constructs trigger PHP string coercion on a Stringable operand without consulting SecurityPolicy::checkMethodAllowed(), allowing a sandboxed template author to invoke __toString() on objects reachable in the render context through conditional expressions, comparison operators, tests, template-loading tags, dynamic attribute names, spread arguments, the do tag, and the .. range operator. This issue is fixed in version 3.26.0.

### CVE-2026-46639

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-07-14T22:16:56.697 |

Twig is a template language for PHP. From 3.24.0 until 3.26.0, object-destructuring assignment compiles CoreExtension::getAttribute() with the sandbox argument hardcoded to false, disabling property and method policy checks and allowing an attacker with write access to a sandboxed Twig template to read public properties or invoke public getters on objects passed to the template engine. This issue is fixed in version 3.26.0.

### CVE-2026-46627

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-14T22:16:54.700 |

Twig is a template language for PHP. Prior to 3.26.0, the Twig sandbox does not prevent a template from consuming CPU, memory, or wall-clock time, even under the strictest allow-list, allowing untrusted templates to cause resource exhaustion. This issue is addressed in version 3.26.0 by documenting that the sandbox does not protect against resource exhaustion.

### CVE-2026-5040

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-07-14T19:18:03.213 |

TP-Link Deco M5 v1 uses a weak password hashing mechanism to store user credentials.  An attacker who obtains the password hash through system compromise or privileged access could perform brute-force or dictionary attacks.

Successful exploitation may result in disclosure of authentication credentials, enabling unauthorized access to device management functions, depending on the privileges associated with the recovered password. The primary security impact is loss of confidentiality.

### CVE-2026-58529

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:39.550 |

Out-of-bounds read in Active Directory Federation Services (AD FS) allows an authorized attacker to disclose information over a network.

### CVE-2026-57101

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-14T18:18:34.850 |

Improper neutralization of input during web page generation ('cross-site scripting') in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-55122

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:18.500 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to disclose information locally.

### CVE-2026-50682

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:18:02.820 |

Out-of-bounds read in Windows Active Directory allows an authorized attacker to deny service over a network.

### CVE-2026-50465

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T18:17:51.850 |

Improper access control in Microsoft Windows DNS allows an authorized attacker to perform tampering locally.

### CVE-2026-50451

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-14T18:17:49.787 |

Missing authentication for critical function in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50428

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T18:17:46.447 |

Out-of-bounds read in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to disclose information locally.

### CVE-2026-56193

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-14T17:17:10.377 |

Out-of-bounds read in Microsoft Office allows an unauthorized attacker to disclose information locally.

### CVE-2026-55144

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-325` |
| Published | 2026-07-14T17:17:09.327 |

Missing cryptographic step in Windows CryptoAPI allows an authorized attacker to perform tampering locally.

### CVE-2026-50354

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:00.563 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-49791

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-14T17:16:54.720 |

Improper link resolution before file access ('link following') in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-49165

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-908` |
| Published | 2026-07-14T17:16:51.210 |

Use of uninitialized resource in Microsoft Windows App Store allows an authorized attacker to disclose information locally.

### CVE-2026-55651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-14T16:17:00.937 |

Easy!Appointments is a self hosted appointment scheduler. In version 1.5.2, an Excessive Data Exposure vulnerability in the customers search endpoint allows an authenticated user to obtain appointment hashes belonging to other users.
Using these hashes, an attacker can modify or delete appointments of other providers, resulting in an Appointments Takeover. Version 1.6.0 fixes the issue.

### CVE-2026-10671

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-07-14T15:16:55.447 |

In Zephyr's kernel pipe implementation, the userspace syscall verifier z_vrfy_k_pipe_init() in kernel/pipe.c used K_SYSCALL_OBJ() (which requires the kernel object to already be initialized) instead of K_SYSCALL_OBJ_NEVER_INIT() (which rejects an already-initialized object). As a result, on CONFIG_USERSPACE builds an unprivileged user thread that has been granted access to a k_pipe object can invoke the k_pipe_init syscall to re-initialize a pipe that is already in use.

z_impl_k_pipe_init() unconditionally resets the ring buffer, sets pipe->waiting to 0, and re-initializes both wait queues (z_waitq_init on pipe->data and pipe->space) without waking or accounting for threads currently blocked on the pipe. Any thread already pended in k_pipe_read()/k_pipe_write() is left orphaned: still marked pending with pended_on pointing at the cleared wait queue and with stale qnode_dlist links into the (now re-initialized) embedded list head.

When such an orphaned waiter is later timed out or woken, the scheduler calls sys_dlist_remove() on its stale node, writing through dangling prev/next pointers into kernel wait-queue/scheduler structures, causing list corruption (an attacker-driven invalid kernel write), lost wakeups, indefinitely blocked threads, and silent data loss. The flaw lets a deprivileged user thread corrupt the state of a kernel object shared with other threads/partitions.

The fix switches the verifier to K_SYSCALL_OBJ_NEVER_INIT(), matching the existing k_msgq_init verifier, so a user thread can no longer re-initialize a live pipe. The vulnerable code shipped in v4.1.0 and remained through v4.4.0.

### CVE-2026-61438

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-15T12:18:18.993 |

PraisonAI before 4.6.78 contains a remote code execution vulnerability in JobWorkflowExecutor._exec_inline_python() due to insufficient AST validation of workflow script steps. Attackers can create malicious YAML workflow files with import os statements followed by os.system() calls that bypass sandbox checks and execute arbitrary OS commands with process privileges.

### CVE-2026-54684

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-14T22:17:16.680 |

jadx is a Dex to Java decompiler. From 1.5.2 to 1.5.5, a malicious .xapk file can cause jadx to write attacker-controlled archive entry contents outside the intended XAPK plugin temporary unpack directory because XApkLoader resolves each entry name directly with tmpDir.resolve(fileName) after a CWD-based ZIP security check. When jadx is launched from a directory that is an ancestor of the config directory, the arbitrary write can plant a JAR in plugins/dropins, and the next jadx run loads the JAR with URLClassLoader and ServiceLoader, executing attacker-controlled plugin code. This issue is fixed in version 1.5.6.

### CVE-2026-50526

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-345` |
| Published | 2026-07-14T20:17:37.240 |

Improper link resolution before file access ('link following') in .NET allows an authorized attacker to perform tampering locally.

### CVE-2026-58637

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:45.947 |

Use after free in Windows Client-Side Caching (CSC) Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-58629

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:45.093 |

Use after free in Windows DirectX allows an authorized attacker to elevate privileges locally.

### CVE-2026-58619

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:44.497 |

Use after free in Windows Sensor Data Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-58544

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:42.400 |

Use after free in Windows Management Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-57093

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:33.997 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-56187

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:28.650 |

Use after free in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-56183

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:28.063 |

Use after free in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-56173

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:23.310 |

Use after free in Windows WebView allows an authorized attacker to elevate privileges locally.

### CVE-2026-50674

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:18:01.670 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-50672

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:01.290 |

Use after free in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-50669

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:18:00.810 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50658

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-07-14T18:17:59.563 |

Time-of-check time-of-use (toctou) race condition in Microsoft Defender allows an authorized attacker to elevate privileges locally.

### CVE-2026-50503

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T18:17:57.470 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50491

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-843` |
| Published | 2026-07-14T18:17:55.463 |

Out-of-bounds read in Code Integrity DLL (ci.dll) allows an authorized attacker to elevate privileges locally.

### CVE-2026-50490

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:55.290 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-50459

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:51.040 |

Use after free in Windows Kernel allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-50452

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:49.967 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50449

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:49.477 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50410

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:43.790 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50406

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:43.210 |

Use after free in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-50404

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:42.907 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50403

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:42.780 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50397

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:41.850 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50396

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:41.727 |

Use after free in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-50393

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:41.440 |

Use after free in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-50392

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:41.310 |

Use after free in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-50390

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-14T18:17:40.913 |

Access of resource using incompatible type ('type confusion') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-50372

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-126` |
| Published | 2026-07-14T18:17:38.180 |

Buffer over-read in Windows Redirected Drive Buffering allows an authorized attacker to elevate privileges locally.

### CVE-2026-50371

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:38.003 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows LUAFV allows an authorized attacker to elevate privileges locally.

### CVE-2026-50359

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:36.147 |

Use after free in Microsoft XML Core Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-50358

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:35.963 |

Use after free in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-50348

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:34.783 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-50345

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:34.350 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50322

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T18:17:31.090 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50307

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T18:17:28.690 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-58526

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:17:12.387 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-54996

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-362` |
| Published | 2026-07-14T17:17:07.310 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-54989

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:06.440 |

Use after free in Quality Windows Audio/Video Experience (QWAVE) service allows an authorized attacker to elevate privileges locally.

### CVE-2026-54129

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:17:05.113 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-54111

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-362` |
| Published | 2026-07-14T17:17:04.003 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-50384

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:17:01.160 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Clip Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50356

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T17:17:00.717 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Windows App Store allows an authorized attacker to elevate privileges locally.

### CVE-2026-50325

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:16:59.697 |

Improper access control in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-50323

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:59.573 |

Use after free in Windows Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-50297

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:16:58.137 |

Improper access control in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-50296

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:57.987 |

Use after free in Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-49806

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:57.173 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-49805

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-14T17:16:56.990 |

Improper access control in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-49803

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-14T17:16:56.643 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows AppX Deployment Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-49802

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:56.520 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-49784

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:53.900 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Windows App Store allows an authorized attacker to elevate privileges locally.

### CVE-2026-49183

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:53.437 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Clipboard Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-49162

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:50.903 |

Use after free in Microsoft Brokering File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-48572

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-07-14T17:16:50.257 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows App Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-48571

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-14T17:16:50.023 |

Use after free in Windows App Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-58476

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-14T15:17:06.477 |

Sustainable Irrigation Platform (SIP) through version 5.2.16 contains a cross-site request forgery vulnerability that allows remote attackers to perform state-changing administrative actions by luring a logged-in administrator into visiting a malicious page that issues HTTP GET requests without CSRF token validation or origin verification. Attackers can trigger actions such as disabling the passphrase, rebooting the device, deleting programs, or installing plugins, with the default configuration exposing these endpoints to unauthenticated users due to no required passphrase and a default credential of 'opendoor'.
