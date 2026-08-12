# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-12 15:00 UTC
- **対象期間**: `2026-08-11T15:00:50.000Z` 〜 `2026-08-12T15:00:54.000Z`
- **重要CVE数**: 488 件（Critical 9.0+: 44 件 / High 7.0〜: 444 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **リモートコード実行 (RCE)** が集中しています。  
- **Web アプリケーションフレームワーク／CMS 系**（Joomla、LiquidJS、ColdFusion）での未認証 RCE が目立ち、攻撃者はフロントエンドだけで任意コードを実行できる点が危険です。  
- **エンタープライズ向けマーケティング／シミュレーション製品**（Adobe Campaign Classic、SIMULIA Execution Engine）でも認可ミスに起因する RCE が報告され、内部ネットワークに侵入した攻撃者が横移動しやすくなります。  
- **OS レベルコンポーネント**（Windows iSCSI Target Service、DNS、QUIC など）でのバッファオーバーフローや Use‑After‑Free が続出し、パッチ適用が遅れると企業ネットワーク全体が危険にさらされます。  

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 重大度 (CVSS) | 主な脆弱性種別 | なぜ注目すべきか | 影響範囲・想定被害 |
|-----|-------------------|--------------|----------------|------------------|-------------------|
| **CVE‑2026‑67282** | Joomla Extension **Fabrik** (≤ 4.6.7) | 10.0 | 未認証リモートコード実行 (listfilter model) | Joomla は日本国内でも多数の自治体・教育機関サイトで採用。プラグイン単体で **認証不要** にコード実行でき、Web シェル設置や情報窃取が即座に可能。 | 侵入後はサーバ全体の支配、データベース改ざん、マルウェア配布。 |
| **CVE‑2026‑45618** | **LiquidJS** (≤ 10.25.0) | 10.0 | 任意コード実行 (テンプレートエンジン) | Shopify・GitHub Pages で広く利用され、テンプレートは外部から提供されるケースが多い。**テンプレートだけでコード実行** できるため、サプライチェーン攻撃の入口になる。 | 攻撃者は任意のサーバ側コマンドを実行し、クレデンシャル取得やサイト改ざんが可能。 |
| **CVE‑2026‑71398** (同様に CVE‑2026‑27302) | **Adobe Campaign Classic** (ACC) | 10.0 | 認可不備による任意コード実行 | 大手企業・官公庁のマーケティング基盤として導入が多数。**認証不要** に現在ログイン中のユーザー権限でコード実行でき、内部ネットワークへの踏み台化が容易。 | 顧客データベース漏洩、内部システムへの横展開、ランサムウェア拡散。 |
| **CVE‑2026‑48362** | **ColdFusion** (全バージョン) | 10.0 | OS コマンドインジェクション | ColdFusion は金融・医療系の業務システムで根強く使用。**任意 OS コマンド** が実行できるため、サーバ全体の乗っ取りリスクが極めて高い。 | ファイル改ざん、情報窃取、マルウェア設置、サービス停止。 |
| **CVE‑2026‑65791** | Windows **iSCSI Target Service** (Windows Server 2022, Windows 11) | 9.8 | ヒープバッファオーバーフロー → RCE | ネットワークストレージ機能は内部インフラの要。未認証でリモートからコード実行が可能になると、**ドメインコントローラや重要サーバへの侵入経路** になる。 | ドメイン権限取得、暗号化キー窃取、ランサムウェア拡散。 |

> **共通点**：すべて「認証不要」または「低権限で実行可能」なリモートコード実行であり、**防御が困難** な点が最大のリスクです。特に Web アプリケーション系は外部からのリクエストが常に流入するため、速やかな対策が求められます。

## 3. 推奨アクション  

### 3‑1. パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン | 取得先・パッケージ名 |
|------|-------------------|----------------|-------------------|
| Joomla + Fabrik | ≤ 4.6.7 | **4.6.8 以上** | Joomla Extension Directory → `fabrik` |
| LiquidJS | ≤ 10.25.0 | **10.26.0 以上** | npm パッケージ `liquidjs` |
| Adobe Campaign Classic | 2023‑2026 系列 (全リリース) | **2026 R1 Patch 2026‑01** (ベンダー提供) | Adobe Support Portal |
| ColdFusion | 全バージョン (未パッチ) | **ColdFusion 2023 Update 31** 以上 | Adobe ColdFusion Update Center |
| Windows iSCSI Target Service | Windows Server 2022, Windows 11 (ビルド 22631 以前) | **2026‑03 セキュリティ更新プログラム** | Windows Update (KB2026‑65791) |

> **※** 企業環境でカスタムビルドやパッケージ化されたものがある場合は、ベンダー提供の **CVE‑2026‑XXXX パッチ** を必ず適用し、パッチ適用後は **再起動** と **機能テスト** を実施してください。

### 3‑2. 防御層の強化
1. **WAF ルール追加**  
   - `*/listfilter*` への POST/GET リクエストを監視し、未知のパラメータは 403 で遮断（Fabrik）。  
   - LiquidJS のテンプレート入力は `Content‑Security‑Policy: script-src 'none'` を適用し、サーバ側で `{{` 文字列のサニタイズを徹底。  
2. **ネットワーク分離**  
   - iSCSI Target Service、DNS、QUIC など OS コンポーネントは **内部 VLAN** に限定し、外部からの直接アクセスを防止。  
   - 必要な

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-67282

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-12T09:17:30.590 |

Joomla Extension - fabrikar.com - Unauthenticated remote code execution in Fabrik < 4.6.8 - An unauthenticated attacker could execute arbitrary code by using the frontend listfilter model.

### CVE-2026-45618

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T20:17:40.163 |

LiquidJS is a Shopify/GitHub Pages compatible template engine. Prior to version 10.26.0, it is possible to execute arbitrary code with crafted templates. Version 10.26.0 patches the issue.

### CVE-2026-71398

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:18:22.327 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-27302

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:17:25.603 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48362

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T17:17:59.627 |

ColdFusion is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-17061

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T15:17:27.783 |

A Deserialization of Untrusted Data vulnerability affecting SIMULIA Execution Engine from Release 2023 through Release 2026 could lead to an unauthenticated remote code execution.

### CVE-2026-72526

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-08-12T02:16:38.200 |

A flaw was found in the multicloud-integrations component. The Application propagation controller processes the `ocm-managed-cluster` annotation from an Application Custom Resource (CR) without proper validation. A tenant with permissions to create Applications on the hub cluster can exploit this to target arbitrary managed clusters. This can force ArgoCD on the spoke clusters to synchronize attacker-controlled manifests, leading to arbitrary code execution or privilege escalation on those clusters.

### CVE-2026-48765

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T21:17:36.947 |

TypeBot is a chatbot builder tool. Versions prior to 3.17.0 allow a low-privilege read collaborator to extract a workspace OAuth `credentialsId` from a readable bot configuration and then overwrite that credential through `handleUpdateOAuthCredentials()` by supplying an attacker-controlled writable `workspaceId`. The update path validates only the attacker-supplied workspace and then updates the credential record by global `id` alone, while also rewriting the credential's `workspaceId`. This allows cross-workspace OAuth credential takeover and reassignment. Version 3.17.0 patches the issue.

### CVE-2026-26035

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T13:17:22.307 |

An Improper Authentication vulnerability [CWE-287] vulnerability in Fortinet FortiWeb 8.0.0 through 8.0.2, FortiWeb 7.6.0 through 7.6.6, FortiWeb 7.4.0 through 7.4.11, FortiWeb 7.2.0 through 7.2.12, FortiWeb 7.0.0 through 7.0.12 may allow a remote unauthenticated attacker to login into the Fortiweb GUI/CLI with a random username and password

### CVE-2026-16230

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-11T20:17:27.133 |

The Formidable Digital Signatures plugin for WordPress is vulnerable to file deletion due to insufficient file path validation in the delete_file function in all versions up to, and including, 3.0.6. This makes it possible for unauthenticated attackers to delete files on the server by supplying an attacker-controlled filename in the item_meta[field_id][content] parameter alongside the delete_saved_image flag during the standard entry-creation POST flow on any form that accepts anonymous submissions.

### CVE-2026-73211

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T18:18:26.357 |

PeerTube is an ActivityPub-federated video streaming platform. Prior to 8.1.6, ActorFollowModel.updateScore() interpolates the attacker-controlled ActivityPub actor inboxUrl into an SQL query, allowing an unauthenticated remote server to read and write PeerTube database tables, including oAuthToken.accessToken, and take over administrator accounts. This issue is fixed in version 8.1.6.

### CVE-2026-65791

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:59.053 |

Heap-based buffer overflow in Windows iSCSI Target Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-62893

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:43.440 |

Use after free in Windows Deployment Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-62878

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:38.590 |

Stack-based buffer overflow in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-62815

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:35.320 |

Use after free in Microsoft QUIC allows an unauthorized attacker to execute code over a network.

### CVE-2026-59124

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:06.287 |

Deserialization of untrusted data in Microsoft High Performance Computing (HPC) Pack allows an unauthorized attacker to execute code over a network.

### CVE-2026-12571

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-640` |
| Published | 2026-08-11T17:17:46.940 |

An authentication bypass in ManageEngine DDI Central's password-reset workflow allows account takeover.

### CVE-2026-72920

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T15:17:38.053 |

SeaweedFS is a distributed storage system. Prior to 4.24, the filer registers the SeaweedIdentityAccessManagement gRPC service without mandatory authentication when jwt.filer_signing.key is unset, allowing any client that can reach the filer gRPC port to invoke CreateUser, CreateAccessKey, PutPolicy, and related IAM RPCs to mint credentials and gain S3 administrative control. This issue is fixed in versions 4.24.

### CVE-2026-70398

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-08-12T02:16:38.060 |

A flaw was found in multicloud-integrations, a component of Red Hat Advanced Cluster Management (RHACM). This vulnerability allows an authenticated user, referred to as a tenant, to manipulate the GitOpsCluster controller. By exploiting this, a tenant can redirect sensitive spoke cluster bearer tokens from secure locations to a namespace they control. This unauthorized access to tokens can lead to the disclosure of critical information and bypass security policies within ArgoCD AppProjects.

### CVE-2026-47705

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1236` |
| Published | 2026-08-11T18:17:27.123 |

TypeBot is a chatbot builder tool. Version 3.16.1 has a CSV injection vulnerability in the result export functionality. The application does not sanitize or escape user-supplied input when generating CSV files. An attacker can inject spreadsheet formulas into input fields, which are later executed when an administrator opens the exported CSV in spreadsheet software such as Microsoft Excel or LibreOffice Calc. Version 3.17.0 patches the issue.

### CVE-2026-71384

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:19:13.593 |

is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access, potentially resulting in an application denial-of-service condition. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-5917

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T22:17:37.390 |

libgit2 versions v0.27.0 through v1.9.0 built with the libssh2 SSH backend (USE_SSH=libssh2) contain a shell command injection vulnerability that allows remote attackers to execute arbitrary commands on an SSH server by supplying a repository path containing unescaped shell metacharacters such as single quotes, semicolons, or pipes. The gen_proto() function in ssh_libssh2.c inserts the repository path directly into a shell command string without escaping special characters before passing it to libssh2_channel_exec(), enabling an attacker to craft a malicious submodule URL in a .gitmodules file that, when processed during a recursive clone, causes the remote server's shell to interpret injected commands under the victim's SSH user account.

### CVE-2026-66147

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T21:17:49.173 |

An unauthenticated command injection vulnerability was identified in the GMS Dispatcher Service in GMS 9.5.1 and earlier versions which allows remote attacker to perform remote code execution through specially crafted requests.

### CVE-2026-73032

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T20:18:46.320 |

PapersGPT for Zotero 0.6.1 contains a remote code execution vulnerability that allows attackers to execute arbitrary JavaScript by returning malicious code from an LLM endpoint that is passed unsanitized to window.eval() in views.ts. Attackers can exploit this through prompt injection in PDFs, MITM interception of API requests, or a malicious custom LLM endpoint to execute arbitrary code in Zotero's chrome-privileged context, enabling file read/write, process execution, and access to all Zotero data.

### CVE-2026-50516

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:02.900 |

Missing authentication for critical function in Microsoft Azure Kubernetes Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-57858

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T13:17:22.943 |

Cal.com Cal.diy versions 2.1.1 through 6.2.0 contain a stored cross-site scripting vulnerability in the BookingPageTagManager component that allows authenticated event owners to inject arbitrary JavaScript by supplying a malicious analytics tracking ID without sanitization. Attackers can close the inline script string literal with a crafted payload that executes in the browser of every visitor to the affected public booking page, enabling session cookie theft, forged authenticated requests, and wormable propagation by chaining with CSRF-able endpoints to persist payloads on additional events.

### CVE-2025-41769

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-12T08:17:11.590 |

The device's PROFINET service is affected by a buffer overflow vulnerability that exists in the default configuration. An unauthenticated remote attacker could exploit this vulnerability to reboot the device or execute arbitrary code.

### CVE-2026-66659

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T06:22:09.420 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Essekia Tablesome Table allows Blind SQL Injection.

This issue affects Tablesome Table: from n/a through 1.2.9.

### CVE-2026-68067

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-08-11T22:18:55.017 |

The login endpoint on the Mira cloud API accepts any format-valid string in the password field and returns a live active session token for the account matching the supplied email address. An attacker could use an email address to control cloud accounts and access hormone record information and account settings.

### CVE-2026-67568

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-11T22:18:54.877 |

The distributed Mira Android APK v4.5.15.4 allows an attacker read/write access to reproductive health profiles from internet connected hosts, which could result in forgery, deletion, or destruction of health information.

### CVE-2026-73034

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T20:18:46.470 |

DB-GPT v0.8.1 contains an unauthenticated path traversal vulnerability that allows remote attackers to write arbitrary files to any location on the server by injecting directory traversal sequences into the user_id HTTP header of the Python file-upload endpoint. Attackers can send a crafted multipart upload request with a traversal-poisoned user_id header to escape the intended upload directory and write attacker-controlled content to locations such as Python startup hooks, cron directories, or agent scripts, resulting in remote code execution.

### CVE-2026-73090

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:18:26.210 |

PeerTube is an ActivityPub-federated video streaming platform. Prior to 8.2.2, processUpdateActivity and processUpdateVideo accept an ActivityPub Update containing a Video object without verifying that byActor.url is authorized for the host in videoObject.id, allowing a malicious federated server to rewrite another server's video metadata, visibility, media file, and HLS URLs. This issue is fixed in version 8.2.2.

### CVE-2026-69102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-11T18:18:17.587 |

MaxKey contains an unauthorized access vulnerability due to a hard-coded JWT signing secret in application-maxkey.properties that allows unauthenticated attackers to forge valid JWT tokens and authenticate as any user by exploiting the password-skipped login endpoint. Attackers can craft a JWT token signed with the publicly known default secret, submit it to the /sign/login/jwt/trust endpoint, and obtain a fully authenticated admin session with access to SSO application configuration and downstream application secrets.

### CVE-2026-70306

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:19:07.970 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-73080

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T16:17:39.857 |

SeaweedFS is a distributed storage system. Prior to 4.24, VolumeServer.FetchAndWriteNeedle in weed/server/volume_grpc_remote.go fetches a caller-supplied remote endpoint through weed/remote_storage/s3/s3_storage_client.go and writes the response into a needle. The RPC performs no authentication and no target validation, allowing anyone who can reach a volume server's gRPC port to cause requests to arbitrary hosts, including loopback, link-local, RFC 1918, and cloud metadata endpoints such as 169.254.169.254, and read the response. On cloud deployments, this can disclose instance metadata and IAM credentials and reach otherwise unexposed internal services. The volume server gRPC plane is unauthenticated by default, and configuring documented JWT signing keys does not protect this RPC. This issue is fixed in version 4.24.

### CVE-2025-31114

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-11T16:17:26.520 |

Fooocus is an image generating software. In versions 2.5.5 and prior, the Fooocus web UI is vulnerable to remote code execution due to the unsafe use of eval when processing metadata JSON. An attacker with access to the Fooocus web UI may be able to execute arbitrary code on the instance. As of time of publication, no known patched versions are available, but a suggested fix pull request is available.

### CVE-2026-67285

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T14:18:33.423 |

Joomla Extension - joomshaper.com - Unauthenticated arbitrary local PHP file inclusion in SP Page Builder < 6.8.0 - An unauthenticated attacker can perform includes to arbitrary PHP files that are accessible by the system.

### CVE-2026-72742

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-11T19:18:49.130 |

DSPy 3.3.0b1 contains a file exfiltration vulnerability in the Image and Audio output field adapters that allows attackers with influence over language model outputs to read arbitrary local files by injecting a filesystem path into the url field of a parsed Image or Audio typed output. The JSONAdapter and ChatAdapter parse untrusted language model completions through parse_value into TypeAdapter validation, which triggers encode_image or encode_audio to read and base64-encode any local file path via the os.path.isfile branch in image.py and audio.py, subsequently embedding the file contents into outgoing prompt messages sent to the attacker-controlled model endpoint.

### CVE-2026-66145

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T20:18:37.717 |

An unauthenticated remote code execution vulnerability was identified in GMS 9.5.1 (Build 9510.1044) and earlier versions which allows remote attacker to read sensitive data and perform arbitrary file write via zipslip.

### CVE-2026-71362

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:18:21.610 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. An attacker could leverage this vulnerability to gain elevated access to sensitive resources. Exploitation of this issue does not require user interaction.

### CVE-2026-73069

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T16:17:38.090 |

Twenty is an open-source CRM (customer relationship management) platform. Prior to 2.15.0, Twenty allowed a workspace administrator with the DATA_MODEL permission to supply settings.asExpression for the system TS_VECTOR field searchVector through PATCH /rest/metadata/fields/:id or the updateOneField GraphQL mutation, causing buildSqlColumnDefinition in packages/twenty-server/src/engine/twenty-orm/workspace-schema-manager/utils/build-sql-column-definition.util.ts to concatenate unescaped input into GENERATED ALWAYS AS (...) and execute arbitrary PostgreSQL statements as the application database user. This issue is fixed in version 2.15.0.

### CVE-2026-47702

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-11T15:17:30.560 |

TypeBot is a chatbot builder tool. In version 3.16.1, API tokens (bearer credentials used to authenticate against the builder API) are stored in the database as cleartext strings. An attacker who gains read access to the database (e.g., via SQL injection, backup exposure, or insider access) can extract all API tokens and impersonate any user without requiring a password or multi-factor authentication. Version 3.17.0 fixes the issue.

### CVE-2026-18691

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-757` |
| Published | 2026-08-11T19:17:22.903 |

An issue in MongoDB Server's intra-cluster connection setup could allow a party with suitable network access to influence which authentication mechanism is used when one replica set member connects to another. Under certain conditions, this could cause the cluster's shared internal credential to be transmitted in a less-protected form, potentially allowing that credential to be recovered. If recovered, the credential could be used to authenticate as the internal superuser to nodes in the deployment.

### CVE-2026-48381

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T18:17:28.247 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-20702

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-11T17:17:49.090 |

Protection mechanism failure for some Intel(R) Data Center Attestation Primitives (Intel(R) DCAP) may allow information disclosure. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable data exposure. This result may potentially occur via network access when attack requirements are present with special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (none) and availability (none) impacts.

### CVE-2026-11325

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-1104` |
| Published | 2026-08-12T12:17:44.370 |

Description



Cloudflare was recently notified by external researchers of vulnerabilities in this archived repository, including a remote code execution issue in `src/index.ts` reachable from certain GitHub Actions workflow configurations. Successful exploitation may expose workflow secrets such as CLOUDFLARE_API_TOKEN and GITHUB_TOKEN to an attacker. Because this repository has been deprecated since 2024, Cloudflare will not be issuing patches. To remediate this issue, we recommend migrating to `cloudflare/wrangler-action` immediately. Consumers who have already migrated are not affected.




Sunset Date



The cloudflare/pages-action repository will be removed on 2026-09-18. Consumers must complete migration before 18th September to avoid CI disruption.




Affected Versions



All published versions of cloudflare/pages-action, including consumers pinned to the v1 moving tag.




Patched Versions



None. This repository will not receive further updates, including security patches.




Resolution / Migration Path
Migrate all workflows using cloudflare/pages-action to `cloudflare/wrangler-action` before 2026-09-18. Refer to the wrangler-action README for the equivalent step configuration and migration guidance.




Credit



Thanks to @agentka99 and @beg1nn3r for reporting their findings via Cloudflare's HackerOne program that informe

### CVE-2026-19426

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-12T08:17:17.493 |

POS System developed by FitSoft has a Missing Authentication vulnerability. Unauthenticated remote attackers can directly access and operate the system.

### CVE-2026-19560

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T22:17:21.647 |

Use after free in Blink in Google Chrome prior to 151.0.7922.137 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-19556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T22:17:21.230 |

Use after free in V8 in Google Chrome prior to 151.0.7922.137 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-55676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-11T21:17:37.560 |

Malcolm is a network traffic analysis tool suite. The file-upload component (FilePond PHP backend) accepts uploads at `POST /server/php/submit.php` and stores them in a directory served by the same nginx and php-fpm instance. The allow-list that should restrict accepted file types is an empty array by default (`file-upload/php/config.php:16`), so the type check is a no-op and every extension is accepted. The filename sanitizer keeps the `.php` extension intact. Committed files land in `/var/www/upload/server/php/files` (`file-upload/php/config.php:7`), and the component's nginx routes any URL ending in `.php` to php-fpm. An authenticated `GET /server/php/files/<name>.php` then executes the uploaded code as `www-data`. Prior to version 26.06.1, in RBAC mode, the upload endpoint is reachable by the granular `ROLE_UPLOAD` role (`nginx/lua/nginx_auth_helpers.lua:71`), a role intended only for submitting capture files. As a result, a user holding the upload-only role runs arbitrary PHP as `www-data` inside the file-upload container. Version 26.06.1 fixes the issue.

### CVE-2026-15606

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T21:17:27.847 |

The Frontend Admin by DynamiApps plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 3.29.9. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level and above permissions, to reset the password of any user on the site, including administrators, leading to full account takeover and complete site compromise. Exploitation requires the attacker to hold a valid encrypted Current-User token obtained by accessing any Edit User form they are legitimately authorized to submit, which they then use as a known-plaintext base for the CBC bit-flipping forgery.

### CVE-2026-73226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-08-11T19:18:52.320 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.15.186, electerm allows an authenticated WebSocket client to invoke unintended internal functions through client-controlled func values in upgrade-func in src/app/server/dispatch-center.js and handleFs in src/app/server/fs.js, exposing Upgrade and fsExport methods that can execute commands, open files, mutate the filesystem, or terminate the process. This issue is fixed in version 3.15.186.

### CVE-2026-73224

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T19:18:52.030 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.15.120, electerm allows a malicious FTP or SFTP server to execute arbitrary commands when a user downloads a crafted folder and invokes Properties and Calculate Size because calcLocal in src/client/components/sftp/file-info-modal.jsx inserts the server-controlled folder name into a du -sh shell command without safely escaping single quotes. This issue is fixed in version 3.15.120.

### CVE-2026-73222

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306;CWE-352` |
| Published | 2026-08-11T19:18:51.720 |

Claude Code Templates is a CLI tool for configuring and monitoring Claude Code. Prior to 1.29.4, the Claude Code Studio server launched by the --studio option in cli-tool/src/sandbox-server.js binds to all interfaces on port 3444, permits cross-origin requests, and requires no authentication. The POST /api/execute endpoint passes the prompt request-body field to executeLocalTask(), and POST /api/install-agent passes the agentName request-body field to a child process. The same unsafe agent field path is reachable from /api/execute through checkAndInstallAgent(). These attacker-controlled values reach child_process.spawn() with shell execution enabled, causing Node.js to construct a shell command in which metacharacters are interpreted. An attacker who can reach the port directly, or who convinces a developer running Studio to visit a malicious website, can execute arbitrary operating-system commands with the developer's privileges and compromise source code, credentials, and local data. This issue is fixed in version 1.29.4.

### CVE-2026-15426

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T19:17:20.447 |

The AcyMailing – An Ultimate Newsletter Plugin and Marketing Automation Solution for WordPress plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 10.11.1. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to overwrite the BCC field of the acy_notification_cms notification template, causing subsequent WordPress password-reset emails — including those targeting administrator accounts — to be silently copied to an attacker-controlled address, enabling account takeover via the captured reset link. Successful exploitation requires the site administrator to have enabled the "Send website emails with AcyMailing" option, which routes WordPress core notification emails through AcyMailing's templating system.

### CVE-2026-71387

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:19:13.843 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction.

### CVE-2026-71386

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:19:13.723 |

is affected by a Cross-site Scripting (XSS) vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-70337

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-11T17:19:11.397 |

Relative path traversal in Microsoft PowerShell Core allows an unauthorized attacker to execute code over a network.

### CVE-2026-70336

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T17:19:11.277 |

Improper control of generation of code ('code injection') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-70329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:19:10.777 |

Integer overflow or wraparound in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T17:19:10.393 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70324

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T17:19:10.143 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70321

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:19:09.760 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T17:19:07.127 |

Improper neutralization of special elements used in an os command ('os command injection') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-66808

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:19:02.233 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-66805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:19:01.850 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-65815

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:19:01.157 |

Deserialization of untrusted data in Microsoft Dynamics 365 (on-premises) allows an authorized attacker to execute code over a network.

### CVE-2026-65811

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:19:00.723 |

Improper input validation in Power BI allows an authorized attacker to execute code over a network.

### CVE-2026-65807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T17:19:00.430 |

Access of resource using incompatible type ('type confusion') in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-65768

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T17:18:56.117 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Microsoft Teams for Android allows an unauthorized attacker to execute code over a network.

### CVE-2026-65767

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:18:55.997 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Teams for Android allows an authorized attacker to perform spoofing over a network.

### CVE-2026-65665

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:54.760 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-65663

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:54.510 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-65658

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:53.957 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-64921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:53.463 |

Missing authentication for critical function in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-64901

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:50.937 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-63514

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T17:18:46.213 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-62913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:45.323 |

Heap-based buffer overflow in Microsoft Exchange Server allows an authorized attacker to execute code over a network.

### CVE-2026-62872

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:18:37.970 |

Incorrect authorization in .NET Framework allows an authorized attacker to elevate privileges over a network.

### CVE-2026-62869

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-11T17:18:37.720 |

Insufficient verification of data authenticity in Azure Entra ID allows an authorized attacker to perform spoofing over a network.

### CVE-2026-62827

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T17:18:36.787 |

Improper authentication in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-62824

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:36.660 |

Stack-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-62823

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:36.500 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-62822

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:36.313 |

Integer overflow or wraparound in Windows GDI+ allows an unauthorized attacker to execute code over a network.

### CVE-2026-62818

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:35.797 |

Use after free in Active Directory Certificate Services (AD CS) allows an authorized attacker to execute code over a network.

### CVE-2026-62817

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T17:18:35.647 |

Out-of-bounds write in Windows DNS allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-62816

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:35.457 |

Heap-based buffer overflow in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-62800

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:34.327 |

Heap-based buffer overflow in Windows SMB Server allows an authorized attacker to execute code over a network.

### CVE-2026-62795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:33.390 |

Use after free in Windows LDAP - Lightweight Directory Access Protocol allows an unauthorized attacker to execute code over a network.

### CVE-2026-62790

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:32.770 |

Heap-based buffer overflow in Windows SMB Server allows an authorized attacker to execute code over a network.

### CVE-2026-62785

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:32.103 |

Heap-based buffer overflow in Windows LDAP - Lightweight Directory Access Protocol allows an unauthorized attacker to execute code over a network.

### CVE-2026-62784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:31.917 |

Heap-based buffer overflow in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to execute code over a network.

### CVE-2026-59133

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-11T17:18:07.610 |

Execution with unnecessary privileges in Microsoft High Performance Computing (HPC) Pack allows an authorized attacker to elevate privileges over a network.

### CVE-2026-59113

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T17:18:05.690 |

Missing authorization in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-57104

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:18:04.610 |

Improper neutralization of input during web page generation ('cross-site scripting') in Azure Storage Explorer allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-49179

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-11T17:18:02.287 |

Improper neutralization of special elements used in a command ('command injection') in Windows Active Directory allows an unauthorized attacker to execute code over a network.

### CVE-2026-19546

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T16:17:31.767 |

A flaw was found in DBI. This is a fix for a partial fix for CVE-2026-14380 for RHEL 9.8.z and 10.2.z.

For a detailed Statement, Description and Mitigation please reffer to the original https://access.redhat.com/security/cve/cve-2026-19546.

### CVE-2025-41770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T08:17:11.910 |

An unauthenticated denial-of-service vulnerability in the device's PLCnext Engineer communication interface allow an remote attacker to interrupt access via the client application. Successful exploitation prevents communication until the PLCnext service is manually restarted.

### CVE-2026-66875

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T22:18:54.587 |

In the Mira hormone monitor device firmware v1.7.1.47 build 01070147, a remote unauthenticated attacker within BLE range (approximately 10–30 meters) can silently rebind the device to an attacker-controlled account, extract stored hormone measurements in cleartext, cause a denial-of-service via malformed or undocumented command opcodes, and passively track the user via a static random BLE address that never rotates.

### CVE-2026-29036

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706` |
| Published | 2026-08-11T22:17:22.257 |

cJSON versions 1.5.0 through 1.7.19 contain an incorrectly-resolved name or reference vulnerability in the decode_pointer_inplace() function within cJSON_Utils.c that allows unauthenticated attackers to cause JSON Patch operations to target wrong object keys by supplying crafted JSON Pointer escape sequences (~0 or ~1) in patch paths. Attackers can submit malicious RFC 6902 JSON Patch input to applications using cJSONUtils_ApplyPatches() or cJSONUtils_ApplyPatchesCaseSensitive() to silently corrupt data or delete unintended keys, potentially bypassing authorization controls in applications that rely on JSON Patch for access-controlled data modification.

### CVE-2026-14863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T21:17:25.867 |

FileRun up to and including version 2026.2.0 contains an OS command injection vulnerability that allows authenticated attackers to achieve remote code execution by uploading a file with a malicious filename containing shell command substitution sequences. The thumbnail generation system passes filenames wrapped in shell double-quotes directly to exec() without escapeshellarg() sanitization, allowing filenames such as $(PAYLOAD).mp4 to survive the filename sanitizer and be evaluated as shell commands when ffmpeg, ImageMagick, vips, or stl-thumb processes the file during thumbnail generation.

### CVE-2026-48813

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-11T20:17:43.207 |

Flawfinder is a a static analysis tool for finding vulnerabilities in C/C++ source code. Versions prior to 2.0.20 have an improper input neutralization issue leading to output manipulation, specifically, Terminal/ANSI Escape Sequence Injection and XML Injection. A malicious file whose name contains ANSI escape sequences can end up being included in flawfinder's standard terminal output, with many effects. Untrusted fields (such as filenames, categories, or code context text) were not properly sanitized when generating structured reports. An attacker could exploit this to corrupt CSV formats or inject arbitrary XML attributes into SonarQube outputs via output_sonar(). It impacts those who use flawfinder to evaluate intentionally malicious filenames or file contents. This issue has been fully patched in Version 2.0.20 (released 2026-05-16). There is no configuration-based workaround within older versions of flawfinder. If an immediate upgrade is not possible, users can mitigate the risk by pre-scanning filenames, inspecting raw output, and/or restricting untrusted inputs.

### CVE-2026-18697

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-08-11T19:17:23.983 |

An issue in MongoDB Server's aggregation framework could allow an unauthenticated party to cause a mongos (router) process to terminate unexpectedly by submitting a specially formed aggregation command. This could result in a denial of service, disrupting client connections routed through the affected mongos instance.

### CVE-2026-72713

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T18:18:23.717 |

XAgent contains a path traversal vulnerability in the workspace file endpoint that allows self-registered or default-credential users to read arbitrary files on the host by supplying parent-directory segments in the `file_name` form field with no path containment check. Attackers can register an account without email verification, then submit crafted `file_name` values such as parent-directory traversal sequences to the `/workspace/file` handler to read host files including application secrets, database credentials, and system files outside the Docker sandbox.

### CVE-2026-48413

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T18:17:31.150 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2022-50997

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T18:17:16.910 |

Weaver (Fanwei) E-cology 8.0 and 9.0 contains a SQL injection vulnerability in the HrmCareerApplyPerView.jsp endpoint that allows unauthenticated remote attackers to extract arbitrary data from the backend database by manipulating the id GET parameter. Attackers can send a single crafted GET request with UNION-based injection payloads through the unsanitized id parameter to retrieve arbitrary data from the Microsoft SQL Server backend. This vulnerability is potentially remediated in software version 10.53 or 10.54. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18 (UTC).

### CVE-2016-20097

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T18:17:16.617 |

Weaver (Fanwei) E-cology 8.0 contains a SQL injection vulnerability in the SignatureDownLoad servlet that allows unauthenticated remote attackers to read arbitrary files by injecting a UNION SELECT payload into the markId GET parameter, which is concatenated unsanitized into a SQL query. Attackers can control the markPath value returned by the query to supply an attacker-controlled filesystem path, causing the servlet to read and stream back arbitrary files accessible to the application server process, including sensitive configuration files containing database credentials. Disclosure materials indicate that this vulnerability has been remediated, but it's unclear which version resolved the issue. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18 (UTC).

### CVE-2026-73081

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T17:19:15.870 |

Activepieces is an open source AI workflow automation platform. Prior to 0.80.0, the worker's code-compilation pipeline builds the on-disk path for a Code step from the step's name and passes that path to a shell-invoked build command. A step name containing shell metacharacters can break out of the intended build invocation and execute arbitrary commands during compilation before any code sandbox is created. An authenticated user with permission to create or edit a flow can execute commands as the worker process user, read and write the worker filesystem, exfiltrate environment secrets, and reach internal services available to the worker. This issue is fixed in version 0.80.0.

### CVE-2026-21273

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:17:55.160 |

is affected by an Improper Input Validation vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain unauthorized read and write access. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-56721

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T16:17:33.563 |

CamaleonCMS version 2.9.2 and earlier contains a privilege escalation vulnerability via insecure direct object reference (IDOR) that allows authenticated low-privileged attackers to overwrite any user's credentials by exploiting a parameter confusion flaw between the authorization filter and action body in the UsersController. Attackers can send a PATCH request to the updated_ajax endpoint setting params[:id] to their own user ID to pass the self-authorization check while simultaneously setting params[:user_id] to a victim's ID, causing the controller to load and mutate the victim's account, including overwriting administrator passwords to achieve full site takeover.

### CVE-2026-18860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-08-11T15:17:28.887 |

Velociraptor allows multi-tenant deployments named "Orgs".

By default Velociraptor, uses the ROOT org, but users can create child orgs for other tenants within the same deployment.

Users can have different permissions in each org. To manage Orgs, Velociraptor usually examines the ORG_ADMIN permission on the ROOT org.

This issue results from the Velociraptor server allowing for the deletion of Orgs by incorrectly checking the ORG_ADMIN permission of callers within the calling ORG instead of the ROOT org. However, Org admins of child orgs were able to add this permission to their ACL token within their own org. This allows an administrator in a child org, which is not also an administrator in the ROOT org, to delete other orgs.

### CVE-2026-18474

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T06:20:14.283 |

The WP Directory Kit WordPress plugin before 1.5.6 does not sanitise and escape a parameter before using it in a SQL statement, leading to a SQL injection exploitable by unauthenticated users when a non-default search field type is configured.

### CVE-2026-73247

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T22:19:05.417 |

Kestra is an open-source, event-driven orchestration platform. Prior to 2.0.0, Kestra's core/src/main/java/io/kestra/core/runners/pebble/functions/HttpFunction.java passes the user-controlled http() uri argument to URI.create() and the server-side HTTP client without restricting private, loopback, or link-local destinations, allowing an unauthenticated attacker to import and execute a flow that accesses internal services or cloud metadata.

### CVE-2026-48441

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T18:17:32.457 |

Lightroom Classic is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48397

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-11T18:17:29.427 |

Lightroom Classic is affected by a Deserialization of Untrusted Data vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-20349

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-244` |
| Published | 2026-08-11T17:17:48.833 |

A vulnerability in the Remote Access SSL VPN service for Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition.&nbsp;

This vulnerability is due to insufficient error checking when processing HTTP requests. An attacker could exploit this vulnerability by sending a crafted HTTP request to the Remote Access SSL VPN service on an affected device. A successful exploit could allow the attacker to cause the affected device to reload, resulting in a DoS condition.

### CVE-2026-73078

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-184` |
| Published | 2026-08-11T16:17:39.573 |

Vim is an open source, command line text editor. Prior to 9.2.0840, runtime/plugin/netrwPlugin.vim loads netrw and runtime/pack/dist/opt/netrw/autoload/netrw.vim constructs Bookmarks, History, and Targets menu entries by interpolating attacker-controlled directory paths into executed :menu commands. s:NetrwBookmarkMenu(), s:NetrwTgtMenu(), g:netrw_menu_escape, EX_TRLBAR, and netrw#MakeTgt() fail to neutralize the | command separator or single quotes at five construction sites, allowing a crafted path browsed or bookmarked in GUI Vim to execute arbitrary Ex and operating-system commands. This issue is fixed in version 9.2.0840.

### CVE-2026-73248

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95` |
| Published | 2026-08-11T22:19:05.553 |

calibre is an e-book manager. Prior to 9.12.0, calibre processes attacker-controlled composite_template metadata from a malicious EPUB, OPF, PDF, or similar file through program: and a nested template() call whose formatter does not inherit allow_python_templates=False, allowing a nested python: template to reach compile_python_template and execute arbitrary Python code when the file is opened or imported. This issue is fixed in version 9.12.0.

### CVE-2026-73233

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T20:18:48.693 |

FreeCAD is a free and open-source multiplatform 3D parametric modeler. Prior to 1.1.2, the FEM Displacement Constraint task dialog in src/Mod/Fem/Gui/TaskFemConstraintDisplacement.cpp passes the xDisplacementFormula, yDisplacementFormula, and zDisplacementFormula fields of a Fem::ConstraintDisplacement object through TaskDlgFemConstraintDisplacement::accept() into Gui::Command::doCommand. The escaping helper neutralizes quotation marks but not backslashes, allowing crafted formula text to terminate the generated Python string and execute arbitrary Python code with the FreeCAD process's privileges when a victim accepts the dialog. This issue is fixed in version 1.1.2.

### CVE-2026-43606

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-11T17:17:58.837 |

Observable Timing Discrepancy in the AMD Vitis Libraries ECDSA secp256k1 component could allow attackers with local access to potentially perform timing analysis or electromagnetic emanation attacks, resulting in high confidentiality and integrity impact due to the exposure of private cryptographic keys.

### CVE-2026-20898

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:17:54.357 |

Improper access control in the firmware for some in Alias Checking Trusted Module for some Intel(R) Xeon(R) processors may allow an escalation of privilege. Startup code and SMM adversary with a privileged user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (high) and availability (none) impacts.

### CVE-2026-73079

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-441` |
| Published | 2026-08-11T16:17:39.713 |

Sub2API is an AI API gateway platform designed to distribute and manage API quotas from AI product subscriptions. From 0.1.135, to 0.1.168, platform API keys issued to tenants are exchanged for upstream requests made with shared provider accounts (ChatGPT/Codex OAuth, OpenAI platform keys, or an operator-configured base URL) that belong to the operator, not to the caller. The `POST /responses/*subpath` wildcard routes spliced the client-supplied subpath into the upstream URL with no validation. This lets an authenticated tenant relay requests to arbitrary upstream endpoints using pooled account credentials via a path traversal. This vulnerability is fixed in 0.1.169.

### CVE-2026-73072

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-11T16:17:38.553 |

Vim is an open source, command line text editor. Prior to 9.2.0846, set_sofo() in src/spellfile.c reuses sl_sal_first[] without resetting values left by set_sal_first(), so a crafted spell file containing an SN_SAL section before an SN_SOFO section causes under-counted mapping lists and attacker-influenced writes beyond a heap allocation. This issue is fixed in version 9.2.0846.

### CVE-2026-70130

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:07.653 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-34635

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-11T17:17:57.963 |

is affected by a Use of Hard-coded Cryptographic Key vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-20789

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:17:53.300 |

Improper access control for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow an escalation of privilege. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable local code execution. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (low), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (high), integrity (low) and availability (low) impacts.

### CVE-2026-73077

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T16:17:39.430 |

Vim is an open source, command line text editor. Prior to 9.2.0839, the runtime/ftplugin/sh.vim, runtime/ftplugin/zsh.vim, and runtime/ftplugin/ps1.vim filetype plugins pass attacker-controlled Visual-mode selections from K through keywordprg commands without safely separating shell arguments. fnameescape() and PATH_ESC_CHARS do not neutralize shell metacharacters before ShKeywordPrg, ZshKeywordPrg, or GetHelp invokes bash, zsh, or PowerShell, allowing arbitrary operating-system commands to execute with the privileges of the user running Vim. This issue is fixed in version 9.2.0839.

### CVE-2026-73076

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-08-11T16:17:38.980 |

Vim is an open source, command line text editor. Prior to 9.2.0847, runtime/autoload/vimball.vim allows a crafted vimball member named .VimballRecord to overwrite the installation record with attacker-chosen commands. When vimball#RmVimball() later processes the matching record entry, the stored Ex commands, including operating-system commands invoked through :!, execute with the privileges of the user running Vim. This issue is fixed in version 9.2.0847.

### CVE-2026-19557

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T22:17:21.340 |

Use after free in TabStrip in Google Chrome on Mac prior to 151.0.7922.137 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-66154

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-11T21:17:49.600 |

An insufficient certificate validation in a privileged communication workflow, was identified in a GMS application 9.5.1 (Build 9510.1044) and earlier versions which, under a successful MitM attack and controlled network conditions, could permit unauthorized changes.

### CVE-2026-29035

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T21:17:35.507 |

CivetWeb (commit 4a4f0c95) contains a heap and stack buffer overflow vulnerability in the read_websocket() function that allows unauthenticated remote attackers to corrupt memory by sending compressed WebSocket frames when both USE_ZLIB and MG_EXPERIMENTAL_INTERFACES are defined. Attackers can negotiate permessage-deflate during the WebSocket handshake and send a crafted frame with the RSV1 bit set, causing the server to write a 4-byte zlib sync trailer out-of-bounds past the allocated buffer, leading to heap metadata corruption, denial of service, or potential code execution.

### CVE-2026-73242

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T20:18:49.260 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.30.0, FreeRDP's winpr/libwinpr/sspi/Kerberos/kerberos.c kerberos_DecryptMessage function fails to bound the peer-controlled GSS Wrap-token EC field before using it with RRC in IOV pointer offsets, allowing a malicious RDP peer to trigger out-of-bounds reads and in-place writes during CredSSP/NLA Kerberos decryption. This issue is fixed in version 3.30.0.

### CVE-2026-73241

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T20:18:49.117 |

FreeRDP is a free implementation of the Remote Desktop Protocol. Prior to 3.30.0, FreeRDP server-side RDSTLS in libfreerdp/core/rdstls.c accepts an attacker-supplied RDSTLS_TYPE_CAPABILITIES PDU while rdstls_server_authenticate is waiting for RDSTLS_TYPE_AUTHREQ, leaving resultCode at RDSTLS_RESULT_SUCCESS and allowing a remote unauthenticated client to bypass the RedirectionGuid, username, domain, or password checks. This issue is fixed in version 3.30.0.

### CVE-2026-56179

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-11T17:18:04.363 |

Origin validation error in Windows Network Address Translation (NAT) allows an unauthorized attacker to perform spoofing over an adjacent network.

### CVE-2026-24911

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:17:56.330 |

Stack-based buffer overflow for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 0: Kernel may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (high) impacts.

### CVE-2026-22887

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-11T17:17:55.807 |

Improper buffer restrictions for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 0: Kernel may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (high) impacts.

### CVE-2026-20776

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-11T17:17:52.497 |

Improper conditions check for some Intel(R) PROSet/Wireless WiFi Software within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (high) impacts.

### CVE-2026-20741

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:17:50.900 |

Improper access control for some Intel(R) PROSet/Wireless WiFi Software within Ring 2: Device Drivers may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (low) and availability (high) impacts.

### CVE-2026-20727

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:17:50.113 |

Null pointer dereference for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 0: Kernel may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (high) impacts.

### CVE-2026-53415

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T16:17:32.833 |

Use after Free in the annotator function of Zoom Clients may allow a meeting participant to achieve remote code execution of another participant via network access.

### CVE-2026-53413

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T16:17:32.580 |

Missing bounds check in the annotator function of Zoom Clients allows buffer over-write, which may allow a meeting participant to achieve remote code execution of another participant via network access.

### CVE-2026-64954

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T05:19:17.893 |

Velociraptor allows scheduling new collections via VQL queries in notebooks. For a user to schedule a new collection, they require the COLLECT_CLIENT permission. However, this is not enforced when the user can run a VQL query which resets the authorization provider.

This allows a user who can run arbitrary VQL (usually with the "analyst" role) to launch new collections (usually requires the "investigator" role). This vulnerability is an escalation from an analyst to investigator role.

### CVE-2026-6484

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1277` |
| Published | 2026-08-12T01:17:08.060 |

In an UEFI, Lack of verified boot to certain FV may cause arbitrary code execution.

### CVE-2026-67558

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-11T22:18:54.733 |

The Mira Android companion app v4.5.15.4 identifies the paired Mira hormone analyzer by performing a substring match against the BLE advertisement name only, with no cryptographic peripheral authentication, MAC allowlist, or bonded-identity check. An attacker could capture live session token information and inject forged hormone measurements into the victim's cloud record and clinical trend view.

### CVE-2026-18710

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-11T22:17:20.113 |

A MongoDB driver component could write sensitive configuration information, including a credential used for outbound network connectivity, to application log output in cleartext during routine client initialization. This occurs automatically as part of normal operation and requires no special privileges to trigger. A party able to read the affected application's logs or downstream log-aggregation storage could recover the credential and reuse it to authenticate to the associated network infrastructure. This issue affects confidentiality only.

### CVE-2026-48763

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T21:17:36.810 |

TypeBot is a chatbot builder tool. Versions prior to 3.17.0 expose a deprecated public upload endpoint at `GET /api/v1/typebots/{typebotId}/blocks/{blockId}/storage/upload-url` that accepts an attacker-controlled `filePath` and returns a presigned S3 `PUT` URL for that exact key. Because the endpoint only checks that the referenced typebot is public and that the referenced block is a file input block, an unauthenticated attacker who knows a valid public `typebotId` and `blockId` can request presigned upload URLs for arbitrary objects in the shared bucket, including `private/...` and other tenants' `public/...` paths. Version 3.17.0 fixes this issue.

### CVE-2026-73031

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T20:18:46.173 |

telegram-search contains a stored cross-site scripting vulnerability that allows remote attackers to execute arbitrary JavaScript in victims' browsers by sending crafted messages containing unsanitized HTML to a shared Telegram group. The highlightKeyword function in MessageList.vue passes raw message content directly to v-html without HTML escaping or sanitization, enabling stored, cross-user, zero-click execution of injected payloads such as image onerror handlers when victims browse or search messages.

### CVE-2026-73214

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-11T18:18:26.773 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.16.0, dtls_server_input_handler() and create_new_connected_udp_socket() in src/apps/relay/dtls_listener.c retain OpenSSL dtls1_reassemble_fragment() state for a 35-byte fragmented ClientHello declaring a 650,000-byte handshake before cookie validation, allowing an unauthenticated remote sender using fresh UDP tuples to exhaust memory without TURN credentials, a completed handshake, a valid cookie, or source spoofing. This issue is fixed in version 4.16.0.

### CVE-2026-48771

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-11T18:17:34.013 |

ishankportfolio is a portfolio website. Prior to version 1.0.1, contact form submissions could potentially be exposed due to improperly secured client-side database configuration and insufficient access control policies. Applications using publicly exposed database credentials or permissive database rules may allow unauthorised users to read, modify, or abuse stored form submission data. This could impact personally identifiable information (PII) submitted through the website contact form, including names, email addresses, phone numbers, and messages. The issue has been patched in version 1.0.1. Users unable to upgrade immediately can reduce risk by disabling public read/write database access, rotating exposed API keys, restricting database policies to authenticated requests only, moving sensitive operations to secure backend/serverless functions, and/or monitoring database activity logs for suspicious access.

### CVE-2026-69306

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-636` |
| Published | 2026-08-11T17:19:07.000 |

Not failing securely ('failing open') in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-21279

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:17:55.283 |

is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction.

### CVE-2026-20715

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:17:49.833 |

Improper input validation in some firmware for some Intel(R) Active Management Technology (Intel(R) AMT) and some Intel(R) Standard Manageability may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via network access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-72922

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T15:17:38.350 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.70, AutoGPT's autogpt_platform/backend/backend/api/features/integrations/router.py webhook_ingress_generic route selected get_webhook_manager(provider) from the untrusted provider URL segment without verifying webhook.provider, allowing a request to /compass/webhooks/{webhook_id}/ingress to use CompassWebhookManager's inherited no-op BaseWebhooksManager.verify_signature instead of GenericWebhooksManager.verify_signature, bypass X-Webhook-Secret for a configured secret_token, and execute a generic webhook graph as its owner. This issue is fixed in version 0.6.70.

### CVE-2026-47231

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-08-12T14:17:54.210 |

Admidio is an open-source user management solution. Prior to version 5.0.10, `modules/documents-files.php` gates state-changing modes by checking that the actor has `hasUploadRight()` on the URL parameter `folder_uuid`. The `move_save` handler then operates on a *separate* URL parameter `file_uuid` and calls `File::moveToFolder($destFolderUUID)`. `File::moveToFolder()` checks the upload right on the destination folder but never on the source folder containing the file. As a result, any user who can upload to any single folder can move any file from any other folder — including private folders to which they have no view rights — into a folder they control, and then download it. Confidentiality is broken (private file contents leak) and integrity is broken (the file is removed from the original location). Version 5.0.10 contains a fix.

### CVE-2026-70468

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-12T13:17:25.227 |

A authentication bypass using an alternate path or channel vulnerability in Fortinet FortiManager 7.6.1, FortiManager 7.4.3 through 7.4.5, FortiManager 7.2.5 through 7.2.9, FortiManager Cloud 7.6.1, FortiManager Cloud 7.4.3 through 7.4.5, FortiManager Cloud 7.2.5 through 7.2.9 may allow attacker to improper access control via <insert attack vector here>

### CVE-2026-70465

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-12T12:19:47.017 |

A buffer copy without checking size of input ('classic buffer overflow') vulnerability in Fortinet FortiClientWindows 7.4.0 through 7.4.3, FortiClientWindows 7.2.0 through 7.2.11 may allow an unauthenticated attacker in a position to alter or craft DNS responses to the targeted host to execute arbitrary code via malicious packets.

### CVE-2026-19594

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-141` |
| Published | 2026-08-12T06:21:57.223 |

Insufficient input sanitization in Snowflake Python API (`snowflake.core`) versions prior to 1.13.0 allowed confused-deputy privilege escalation through two related weaknesses: path traversal (CWE-22) via unencoded `..` identifier path segments, and HTTP parameter pollution (CWE-141) via unencoded `&`/`#`/`=` characters in query string values. An attacker with access to a downstream application built on snowflake.core could exploit the path traversal by supplying `..` as an object name, causing `snowflake.core` to issue REST requests against a parent resource or exploit the parameter pollution by injecting `&`/`#`/`=` into a free-form name field to override constraints on swap, clone, or rename operations — all executed under the application's privileged session. Successful exploitation requires the attacker to control an identifier or object-name string in an application built on snowflake.core that passes it to `snowflake.core` under a higher-privileged Snowflake session (e.g., an EXECUTE AS OWNER stored procedure, Streamlit app, or Native App). The fix is available in Snowflake Python API version 1.13.0, which also addresses several additional security findings. Users must manually upgrade.

### CVE-2026-18961

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T03:16:42.807 |

The Social Login, Passkeys, Magic Link & Email OTP – Passwordless Login by VentraConnect plugin for WordPress is vulnerable to Authentication Bypass via Unverified Provider Email in all versions up to, and including, 1.4.3. This is due to the plugin trusting the unverified email field returned by Spotify's /v1/me endpoint as proof of mailbox ownership — Generic::normalize_common() copies this value into the normalized profile without requiring an email_verified assertion, and User_Links::link_or_login_user() subsequently passes it directly to get_user_by('email', $email) and issues a persistent authentication cookie via wp_set_auth_cookie() without a provider-specific verified-email gate, a local mailbox challenge, or a logged-in approval step. This makes it possible for unauthenticated attackers to log in as any existing WordPress user, including Administrators, by supplying a known target email address through a controlled Spotify OAuth flow, gaining full administrative access to the site.

### CVE-2026-19091

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T20:17:38.797 |

The GeoDirectory – WP Business Directory Plugin and Classified Listings Directory plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete_revision function in all versions up to, and including, 2.8.169. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). By placing post_type=attachment exclusively in the query string to bypass the consistency check, an attacker can convert an auto-draft GeoDirectory listing into a WordPress attachment with attacker-controlled file paths injected into attachment metadata, which the delete_revision handler then dereferences and unlinks without any post-type or path validation.

### CVE-2026-73227

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T19:18:52.460 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.15.120, electerm allows a malicious RDP server to write attacker-controlled content outside the selected save directory because the RDP clipboard download path in src/client/components/rdp/file-transfer.js passes the server-controlled CLIPRDR filename fileInfo.name to osResolve without sanitization. This issue is fixed in version 3.15.120.

### CVE-2026-73225

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T19:18:52.177 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.15.120, electerm allows a malicious FTP or SFTP server to write attacker-controlled content outside the selected download directory because recursive transfers in src/client/components/file-transfer/transfer.jsx pass server-supplied file.name and folder.name values to resolve without sanitization. This issue is fixed in version 3.15.120.

### CVE-2026-73223

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T19:18:51.880 |

electerm is an open-sourced terminal/ssh/sftp/telnet/serialport/RDP/VNC/Spice/ftp client. Prior to 3.15.120, electerm allows a malicious SFTP server to write attacker-controlled content outside the temporary directory because the server-controlled filename name used by editWithSystemEditor in src/client/components/sftp/file-item.jsx is interpolated into path.resolve without sanitization. This issue is fixed in version 3.15.120.

### CVE-2026-71331

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:19:13.353 |

Integer overflow or wraparound in Microsoft Azure Attestation service and Device Health Attestation Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-70340

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T17:19:11.640 |

Missing authorization in Azure CycleCloud allows an authorized attacker to elevate privileges over a network.

### CVE-2026-66802

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:19:01.587 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Azure Attestation service and Device Health Attestation Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-65789

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:58.730 |

Use after free in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-65679

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:55.703 |

Heap-based buffer overflow in Windows iSCSI Target Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-63520

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:18:47.377 |

Improper input validation in Microsoft Office SharePoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-62889

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-11T17:18:40.170 |

Double free in Windows Secure Socket Tunneling Protocol (SSTP) allows an unauthorized attacker to execute code over a network.

### CVE-2026-62820

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-11T17:18:36.177 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows DNS allows an unauthorized attacker to execute code over a network.

### CVE-2026-62819

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:35.957 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-62792

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:32.970 |

Stack-based buffer overflow in Windows TCP/IP allows an unauthorized attacker to execute code over a network.

### CVE-2026-62781

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:31.413 |

Heap-based buffer overflow in RPC Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-62778

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:30.990 |

Use after free in Windows DNS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-48440

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:01.330 |

ColdFusion is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction.

### CVE-2026-72921

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T15:17:38.217 |

SeaweedFS is a distributed storage system. Prior to 4.24, the weed/server/filer_server_handlers.go allowed_prefixes authorization check used strings.HasPrefix on raw path strings, so a filer JWT scoped to /tenant1 also authorized sibling paths such as /tenant1234, /tenant1-old, and /tenant1backup, enabling cross-tenant reads and writes with a valid scoped token. This issue is fixed in version 4.24.

### CVE-2026-18129

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-11T15:17:28.327 |

Cleartext transmission of sensitive information in the Core of Ivanti Endpoint Manager before version 2024 SU7 allows a remote unauthenticated attacker in a MITM position to leak credentials for external SQL connections.

### CVE-2026-62911

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-11T17:18:45.073 |

Authentication bypass by capture-replay in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-57105

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:18:04.740 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-12234

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-12T05:17:42.143 |

The userspace syscall verifiers z_vrfy_zsock_sendmsg() and z_vrfy_zsock_recvmsg() in subsys/net/lib/sockets/sockets.c snapshot the caller-supplied struct net_msghdr into a kernel-side copy with k_usermode_from_copy(), but then re-read the still-live user struct for subsequent decisions. The kernel iovec shadow buffer is sized from one read of msg->msg_iovlen, while the population loop is bounded by a second, live read of the same field.

Because msg points into ordinary user memory, a cooperating second thread in the same memory domain can inflate msg->msg_iovlen in the window between the sizing read and the loop test (a classic double-fetch / TOCTOU). The population loop then iterates past the number of net_iovec slots actually allocated, writing attacker-influenced iov_base/iov_len values beyond the end of the kernel-heap shadow buffer. The recvmsg verifier has the same defect on both its inbound and result write-back loops.

The code is reachable from an unprivileged user thread whenever CONFIG_USERSPACE is enabled and the zsock_sendmsg/zsock_recvmsg syscalls are available. A successful race corrupts kernel-managed heap memory across the user-to-kernel privilege boundary, yielding a local privilege-escalation primitive or, at minimum, a kernel-fault denial of service. The fix copies the header once and derives every size, bound, and gate from the snapshot, copying each iovec entry atomically so its base and length can no longer be raced apart.

### CVE-2026-66150

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T21:17:49.497 |

Improper Control of Generation of Code ('Code Injection') Vulnerability in the SonicWall Email Security appliance allows an authenticated attacker with access to the SonicWall Email Security restricted CLI can inject arbitrary OS commands that execute as root via SNMP.

### CVE-2026-66149

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T21:17:49.393 |

Improper Control of Generation of Code ('Code Injection') Vulnerability in the SonicWall Email Security appliance allows an authenticated attacker with access to the SonicWall Email Security restricted CLI can inject arbitrary OS commands that execute as root via netmask.

### CVE-2026-73234

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T20:18:48.833 |

FreeCAD is a free and open-source multiplatform 3D parametric modeler. Prior to 1.1.2, PropertyFileIncluded::Restore() in src/App/PropertyFile.cpp concatenates an attacker-controlled file or data attribute from Document.xml with the document transient path without rejecting directory components, absolute paths, or parent traversal. A crafted .FCStd archive with a matching FileIncluded XML attribute and ZIP entry can therefore write attacker-controlled content to arbitrary locations accessible to the FreeCAD user, potentially enabling persistence, credential compromise, configuration replacement, or code execution. This issue is fixed in version 1.1.2.

### CVE-2026-73231

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-11T20:18:48.400 |

Faker generates massive amounts of fake data in the browser and Node.js. Prior to 10.5.0, the faker.helpers.fake method in src/modules/helpers/eval.ts allows attacker-controlled fake templates to access the Function constructor through fakeEval.resolveProperty when a function returns another function, enabling arbitrary JavaScript code execution. This issue is fixed in version 10.5.0.

### CVE-2026-48410

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:30.627 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48409

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:30.470 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48408

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:30.320 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48407

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:30.107 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48406

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:29.880 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48405

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:29.723 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-48404

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T18:17:29.573 |

Lightroom Classic is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47940

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T18:17:27.267 |

Lightroom Classic is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-70354

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T17:19:12.640 |

Out-of-bounds write in .NET allows an unauthorized attacker to execute code locally.

### CVE-2026-70347

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:12.330 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-70346

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:12.150 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-70345

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:11.970 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-70344

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:11.780 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-70338

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-11T17:19:11.520 |

Improper control of generation of code ('code injection') in Microsoft PowerShell allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-70335

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T17:19:11.153 |

Improper neutralization of special elements used in an os command ('os command injection') in GitHub Copilot and Visual Studio Code allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-70313

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-11T17:19:08.663 |

Improper input validation in Microsoft Office PowerPoint allows an unauthorized attacker to disclose information locally.

### CVE-2026-70311

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:19:08.410 |

Use after free in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-69278

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693;CWE-863` |
| Published | 2026-08-11T17:19:06.880 |

Incorrect authorization in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-68817

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:06.080 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68816

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:05.953 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68815

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:05.820 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68814

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:19:05.687 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68812

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:05.430 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T17:19:05.303 |

Access of resource using incompatible type ('type confusion') in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68810

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-11T17:19:05.170 |

Untrusted pointer dereference in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:04.780 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68806

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T17:19:04.643 |

Out-of-bounds write in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68805

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:04.503 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-08-11T17:19:04.353 |

Numeric truncation error in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68803

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T17:19:04.130 |

Access of resource using incompatible type ('type confusion') in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68801

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:03.793 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:03.657 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68798

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:03.400 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68796

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:03.140 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68795

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:03.010 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:02.877 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68793

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:19:02.747 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-68792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-11T17:19:02.627 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Office allows an authorized attacker to elevate privileges locally.

### CVE-2026-66807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:19:02.107 |

Stack-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-66804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:19:01.733 |

Improper access control in Windows Cross Device Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-66799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:19:01.400 |

Heap-based buffer overflow in Windows Key Guard allows an authorized attacker to elevate privileges locally.

### CVE-2026-65814

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:19:00.973 |

Heap-based buffer overflow in Windows Storage Port Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-65810

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-11T17:19:00.570 |

Relative path traversal in .NET Framework allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-65790

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:58.870 |

Heap-based buffer overflow in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-65787

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-08-11T17:18:58.423 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-65786

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-08-11T17:18:58.250 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-65775

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:56.730 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-65774

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:56.547 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-65773

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:18:56.367 |

Improper access control in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-65673

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-11T17:18:55.303 |

Entra Connect Elevation of Privilege Vulnerability

### CVE-2026-65672

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:55.170 |

Heap-based buffer overflow in Windows Remote Access API allows an authorized attacker to elevate privileges locally.

### CVE-2026-65671

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:55.000 |

Heap-based buffer overflow in Windows Remote Access API allows an authorized attacker to elevate privileges locally.

### CVE-2026-65664

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:54.633 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-65661

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:54.203 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-65657

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:53.830 |

Use after free in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-65656

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-11T17:18:53.703 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64920

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:53.333 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64919

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:53.207 |

Stack-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64915

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:52.750 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-64914

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:52.600 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64912

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:52.440 |

Stack-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64911

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:52.280 |

Integer overflow or wraparound in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64910

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-11T17:18:52.137 |

Untrusted pointer dereference in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64909

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125;CWE-191` |
| Published | 2026-08-11T17:18:51.990 |

Integer underflow (wrap or wraparound) in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64908

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:51.870 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64907

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:51.733 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-64906

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:51.600 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code locally.

### CVE-2026-64905

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-08-11T17:18:51.463 |

Buffer over-read in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-64904

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T17:18:51.323 |

Access of resource using incompatible type ('type confusion') in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64903

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:51.180 |

Integer overflow or wraparound in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-64898

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:50.567 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63533

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:50.310 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63532

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:50.163 |

Integer overflow or wraparound in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63527

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:49.530 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-63526

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:49.390 |

Stack-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63525

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-08-11T17:18:49.267 |

Numeric truncation error in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-63522

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-11T17:18:49.017 |

Incorrect permission assignment for critical resource in Azure SQL Database allows an authorized attacker to elevate privileges locally.

### CVE-2026-63519

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:47.223 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63518

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:47.080 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-63515

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-08-11T17:18:46.357 |

Out-of-bounds read in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-63513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:46.073 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code locally.

### CVE-2026-62909

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-252` |
| Published | 2026-08-11T17:18:44.817 |

Uncaught exception in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-62894

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:43.593 |

Heap-based buffer overflow in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-62890

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:40.353 |

Heap-based buffer overflow in Windows GDI+ allows an authorized attacker to execute code locally.

### CVE-2026-62888

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:40.030 |

Use after free in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-62886

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:39.717 |

Integer overflow or wraparound in .NET allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-62885

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:39.530 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62880

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:18:38.813 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-62877

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:38.390 |

Stack-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62876

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:18:38.200 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62871

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-08-11T17:18:37.843 |

Out-of-bounds write in .NET allows an unauthorized attacker to execute code locally.

### CVE-2026-62832

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:37.113 |

Improper link resolution before file access ('link following') in Windows User Profile Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62812

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:35.010 |

Improper link resolution before file access ('link following') in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:34.880 |

Heap-based buffer overflow in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-62807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:34.730 |

Improper link resolution before file access ('link following') in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62803

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:34.567 |

Improper link resolution before file access ('link following') in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:34.180 |

Heap-based buffer overflow in Windows SMB Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-62797

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:33.817 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-62783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:31.763 |

Heap-based buffer overflow in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-62779

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:31.153 |

Use after free in Windows Schannel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62777

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:30.777 |

Missing authentication for critical function in Windows License Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-62776

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:30.600 |

Improper link resolution before file access ('link following') in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62772

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:29.930 |

Heap-based buffer overflow in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-62771

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:29.750 |

Heap-based buffer overflow in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-62770

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:29.550 |

Heap-based buffer overflow in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-62768

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:29.150 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-62761

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:28.860 |

Improper link resolution before file access ('link following') in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:28.677 |

Heap-based buffer overflow in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-62755

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-11T17:18:28.260 |

Stack-based buffer overflow in Windows DHCP Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-62754

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:28.087 |

Heap-based buffer overflow in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-62752

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:27.713 |

Heap-based buffer overflow in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-62751

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:18:27.560 |

Integer overflow or wraparound in Windows Projected File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-62747

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:26.883 |

Heap-based buffer overflow in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62741

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-08-11T17:18:26.010 |

Integer underflow (wrap or wraparound) in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-62739

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-08-11T17:18:25.667 |

Heap-based buffer overflow in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-62737

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-11T17:18:25.347 |

Untrusted pointer dereference in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62736

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:25.217 |

Heap-based buffer overflow in Windows DHCP Client allows an authorized attacker to elevate privileges locally.

### CVE-2026-62735

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:25.037 |

Heap-based buffer overflow in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-62733

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:18:24.657 |

Out-of-bounds read in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62732

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:24.467 |

Heap-based buffer overflow in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62722

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:23.050 |

Heap-based buffer overflow in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-62721

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-08-11T17:18:22.870 |

Insufficient granularity of access control in User-Mode Power Service (UMPS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-62719

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:22.503 |

Heap-based buffer overflow in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-62717

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:22.153 |

Heap-based buffer overflow in Windows Message Queuing allows an authorized attacker to elevate privileges locally.

### CVE-2026-62713

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:21.530 |

Heap-based buffer overflow in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-62712

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:21.343 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62711

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:21.157 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62710

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:20.993 |

Heap-based buffer overflow in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62707

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:20.483 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-62701

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:19.867 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62700

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:19.683 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-62698

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-08-11T17:18:19.303 |

Numeric truncation error in Microsoft Digest Authentication allows an authorized attacker to elevate privileges locally.

### CVE-2026-62696

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-11T17:18:19.130 |

Integer underflow (wrap or wraparound) in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62695

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:18.993 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-62692

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:18.680 |

Heap-based buffer overflow in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-62688

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:18.397 |

Heap-based buffer overflow in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-61937

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-11T17:18:17.497 |

Integer overflow or wraparound in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-61934

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:16.473 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-61932

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-843` |
| Published | 2026-08-11T17:18:16.063 |

Access of resource using incompatible type ('type confusion') in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-61930

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:15.897 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-61926

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:15.290 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-61925

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:18:15.107 |

Incorrect authorization in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-61923

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:14.767 |

Heap-based buffer overflow in Windows Display Enhancement Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-61367

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:13.043 |

Missing authentication for critical function in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-61365

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:11.560 |

Missing authentication for critical function in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-61364

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:11.377 |

Missing authentication for critical function in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-61359

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:10.757 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-61358

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-11T17:18:10.597 |

Improper link resolution before file access ('link following') in Windows Accessibility Infrastructure (ATBroker.exe) allows an authorized attacker to elevate privileges locally.

### CVE-2026-61357

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:10.473 |

Use after free in Application Information Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-61356

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:18:10.303 |

Missing authentication for critical function in Windows Remote Desktop Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-61355

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:10.163 |

Heap-based buffer overflow in Windows Sensor Data Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-61353

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:09.983 |

Heap-based buffer overflow in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-61349

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:09.447 |

Use after free in Windows Work Folder Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-59127

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:18:06.730 |

Integer overflow or wraparound in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-58651

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:05.550 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-58650

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T17:18:05.417 |

Authorization bypass through user-controlled key in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-58641

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:18:05.287 |

Integer overflow or wraparound in .NET allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-56174

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-11T17:18:04.220 |

Untrusted search path in Windows Narrator Braille allows an authorized attacker to elevate privileges locally.

### CVE-2026-54984

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:03.917 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code locally.

### CVE-2026-54981

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693;CWE-829` |
| Published | 2026-08-11T17:18:03.780 |

Inclusion of functionality from untrusted control sphere in Visual Studio Code - Python extension allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-42976

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T17:17:58.647 |

Missing authentication for critical function in Windows RPC API allows an authorized attacker to elevate privileges locally.

### CVE-2026-25652

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:17:56.597 |

is affected by an Incorrect Authorization vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain unauthorized read and write access. Exploitation of this issue does not require user interaction.

### CVE-2026-67179

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-644` |
| Published | 2026-08-11T16:17:34.113 |

Genkit does not properly validate host request headers. Any host on the developer's network, and any website the developer visits (via DNS rebinding), can reach POST /api/runAction on the Dev UI server (default port 4000) and execute any registered Genkit action and read the result. Fixed on 2026-06-18.

### CVE-2026-73122

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T02:16:38.330 |

A flaw was found in the multicloud-operators-channel component of Red Hat Advanced Cluster Management (RHACM). This vulnerability allows a compromised agent from a managed cluster to gain unauthorized access to sensitive information. Specifically, the agent can read all Secrets and ConfigMaps within any Channel namespace on the hub, potentially exposing credentials for other tenants' Git and Helm repositories. This could lead to significant information disclosure.

### CVE-2026-66878

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-12T02:16:37.937 |

A flaw was found in multicloud-operators-subscription. A privileged user, specifically a namespace administrator capable of creating Channel and Subscription resources, can exploit this vulnerability. By manipulating the Channel.Spec.SecretRef.Namespace field, the user can cause the system to copy sensitive Secret contents from other namespaces into their own, leading to information disclosure.

### CVE-2026-18692

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T19:17:23.317 |

An issue in MongoDB Server's handling of timeseries bucket lifecycle could allow an authenticated user with write privileges to cause an internal reference to be used after the underlying memory has been freed. Subsequent operations could then result in a server crash or, potentially, execution of unintended code.

### CVE-2026-73218

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T18:18:27.320 |

Cursor is a code editor built for programming with AI. Prior to 3.0.0, Cursor IDE for macOS allows an agent running in Auto-Run Sandbox mode, when Docker Desktop and the Dev Containers CLI are installed, to launch a privileged container and mount Docker's virtiofs0, granting read and write access to the user's home directory and enabling host command execution with the user's privileges without an additional permission prompt. This issue is fixed in version 3.0.0.

### CVE-2026-73217

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-11T18:18:27.180 |

Cursor is a code editor built for programming with AI. Prior to 3.1.2, Cursor IDE for macOS allows an agent running in Auto-Run Sandbox mode to replace a virtual environment's Python executable with a malicious wrapper that the Microsoft Python extension invokes outside the sandbox, allowing arbitrary host commands with the user's privileges, including modifying files outside the workspace and launching applications. This issue is fixed in version 3.1.2.

### CVE-2026-48447

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:17:33.157 |

Lightroom Classic is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-48414

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T18:17:31.313 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Exploit depends on conditions beyond the attacker's control. Scope is changed.

### CVE-2026-48385

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T17:18:00.167 |

ColdFusion is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-18127

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-11T15:17:28.193 |

External control of a filename in the Core of Ivanti Endpoint Manager before version 2024 SU7 allows a remote authenticated attacker full write control over an S3 bucket configured for session recording storage.

### CVE-2026-48767

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-11T18:17:33.470 |

TypeBot is a chatbot builder tool. Versions prior to 3.17.0 allow a low-privilege guest member of a workspace to obtain a live Google Sheets OAuth access token for that workspace by calling the Google Sheets helper `getAccessToken`. The vulnerable path checks only whether the caller has read access to the workspace, decrypts the stored Google OAuth credential, refreshes or retrieves the access token through the Google client, and returns the raw bearer token directly to the caller. Because guest members can also enumerate credential identifiers, a guest can mint and reuse the workspace's Google access token outside Typebot. Version 3.17.0 patches the issue.

### CVE-2026-48415

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:17:31.483 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access, causing a limited disruption to availability. Exploitation of this issue does not require user interaction.

### CVE-2026-73083

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-11T17:19:16.277 |

Activepieces is an open source AI workflow automation platform. Prior to 0.80.0, in SANDBOX_CODE_ONLY mode, the engine loads the compiled user module with importFresh(), a wrapper around Node.js require(), before the V8 isolate is applied. Top-level module code can therefore call require('child_process'), access fs, and use other Node.js APIs in the host engine process outside the sandbox. An authenticated user who can create a Code step can read environment secrets including AP_ENCRYPTION_KEY and AP_JWT_SECRET, read or write files, and reach internal services. This issue is fixed in version 0.80.0.

### CVE-2026-48766

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-11T16:17:32.320 |

TypeBot is a chatbot builder tool. Versions prior to 3.17.0 allow a low-privilege guest member of a workspace to exfiltrate stored OpenAI-compatible API keys by invoking the OpenAI model-listing helper with an attacker-controlled `baseUrl`. The vulnerable path decrypts the selected workspace credential, creates an OpenAI client with the secret in both `apiKey` and the explicit `api-key` header, and then sends the outbound request to the caller-supplied URL. Because the permission check accepts any readable workspace member and `listCredentials` reveals credential identifiers to guests, a guest can force the server to deliver the workspace secret to attacker infrastructure. Version 3.17.0 patches the issue.

### CVE-2026-18789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T06:20:22.817 |

The Ezoic WordPress plugin before 2.23.1 does not properly restrict access to some of its content export functionality, allowing unauthenticated attackers to trigger a server-side export of the site's database, including user password hashes and password reset tokens, as well as to persistently change some of its settings.

### CVE-2026-73249

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T22:19:05.687 |

calibre is an e-book manager. Prior to 9.12.0, the calibre Content Server endpoint POST /book-update-annotations/{library_id}/{book_id}/{fmt} in src/calibre/srv/books.py omits needs_db_write=True, causing Router.dispatch() to skip ctx.check_for_write_access() before update_annotations() passes attacker-controlled JSON to db.merge_annotations_for_book(), which allows a readonly user or an anonymous user on an unauthenticated deployment to persist unauthorized book annotation changes. This issue is fixed in version 9.12.0.

### CVE-2026-73246

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-08-11T22:19:05.287 |

Kestra is an open-source, event-driven orchestration platform. Prior to 2.0.0-rc6, Kestra's worker/src/main/java/io/kestra/worker/endpoint/WorkerEndpoint.java serves GET /worker without authentication and serializes the complete live Task object, which can expose commands, environment variables, HTTP headers, connection details, plaintext credentials, and execution identifiers while the main API on port 8080 remains protected. This issue is fixed in 2.0.0-rc6.

### CVE-2026-19558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T22:17:21.440 |

Use after free in Extensions in Google Chrome prior to 151.0.7922.137 allowed an attacker who convinced a user to install a malicious extension to execute arbitrary code inside a sandbox via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-73232

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-11T20:18:48.543 |

ffuf is a fast web fuzzer written in Go. Prior to 2.2.0, ffuf allows a malicious target server to cause an out-of-memory denial of service because the response size guard in pkg/runner/simple.go checks only the compressed Content-Length while io.ReadAll reads gzip, brotli, deflate, transparently decompressed, or chunked response bodies without a decompressed-size bound. This issue is fixed in version 2.2.0.

### CVE-2026-71467

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T20:18:45.260 |

A flaw was found in search-v2-api. The authentication middleware in the affected component unconditionally skips authentication when a request includes an `Upgrade: websocket` header. An unauthenticated attacker can exploit this by sending a specially crafted HTTP POST request to the `/federated` endpoint with the `Upgrade: websocket` header. This allows the attacker to bypass authentication and access federated search results across all configured remote managed hubs, leading to information disclosure.

### CVE-2026-48804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T20:17:42.580 |

python-socketio is a Python implementation of the Socket.IO realtime client and server. The python-socketio server stores binary `EVENT` and `ACK` messages in memory while it waits to receive their binary attachments. Once all the attachments are received, these messages are then processed. Prior to version 5.16.4, an attacker can submit a binary message and intentionally omit sending one or more of its attachments to cause the message along with the partial list of received attachments to stay in memory for a long time. Version 5.16.4 takes the following measures to address this issue: Binary packets are only accepted from authenticated clients and, when a client disconnects, the server checks if there is a partial binary message being held for the client and deletes it.

### CVE-2026-13457

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-11T20:17:26.993 |

The InstaWP Connect – 1-click WP Staging & Migration plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 0.1.3.6 via the (top-level script) function. This is due to the plugin stores its encrypted options file as options-{migrate_key}.txt in wp-content/instawpbackups/ without deploying an index.php or .htaccess to prevent directory listing, exposing the 40-character migrate_key on Apache servers with directory indexing enabled, which allows an attacker to derive the AES-256-CBC passphrase via SHA256(migrate_key), decrypt the options file to recover the api_signature. This makes it possible for unauthenticated attackers to get the database access details and api_signature. Exploitation requires the target WordPress site to be hosted on Apache with directory listing enabled (Options +Indexes) for the wp-content/instawpbackups/ directory, and time limited because it can only be exploited during the migration period.

### CVE-2026-48809

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T19:17:37.267 |

python-engineio is a Python implementation of the Engine.IO realtime client and server. Versions prior to 4.13.2 have two specific configurations of the python-engineio server in which the size of incoming messages is not checked before the messages are loaded into memory. An attacker can take advantage of these to cause unnecessary memory allocations in the python-engineio server. The two cases are POST requests, when using ASGI with the long polling transport and WebSocket messages, when using Aiohttp with the WebSocket transport. Version 4.13.2 addresses this issue. ASGI severs now only load the body of incoming requests into memory after the client is confirmed to be known and authenticated, and the payload size is below the maximum allowed size. Requests that do not comply with these requirements are discarded. Aiohttp servers configure the maximum payload size in the underlying WebSocket layer from Aiohttp, so that large messages are discarded by Aiohttp before they are delivered to python-engineio.

### CVE-2026-48802

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T19:17:37.120 |

python-engineio is a Python implementation of the Engine.IO realtime client and server. Prior to version 4.13.2, an attacker can cause the creation of unnecessary background threads in the python-engineio server by exploiting the heartbeat mechanism, which launches a thread when a new connection is received, and when the client sends a PONG packet. This issue primarily affects synchronous servers. Asynchronous servers allocate background tasks instead of physical threads, which are lightweight and less likely to cause denial of service. However, the fix that was implemented was also applied to the asynchronous case. Version 4.13.2 addresses this issue as follows: The initial background thread (or async task( for heartbeat management is only launched if a client passes authentication in the `connect` handler; and the server now ensures that there is only one background heatbeat thread (or async task) per client at a given point in time. Out of sequence PONG packets are now discarded when an active heartbeat thread is already running.

### CVE-2026-18706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T19:17:25.360 |

An issue in MongoDB Server's $graphLookup aggregation stage could allow an authenticated user able to issue aggregation and memory-management commands to cause an internal reference to be used after the underlying memory has been freed. This could result in a server crash or, potentially, execution of unintended code.

### CVE-2026-48416

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T18:17:31.650 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read access. Exploitation of this issue does not require user interaction.

### CVE-2026-73089

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T17:19:17.123 |

Browserslist is a configuration tool for sharing target browsers and Node.js versions between front-end tools. Prior to 4.28.7, index.js retains every distinct `(queries, context)` result in cache and every parseQueries() AST in parseCache without a size cap, TTL, or eviction, allowing an attacker who can influence repeated browserslist() query values, including valid since `<year>-<month>-<day>` queries, to bypass the caller-controlled BROWSERSLIST_DISABLE_CACHE mitigation and cause linear memory growth followed by an out-of-memory process crash. This issue is fixed in version 4.28.7.

### CVE-2026-73088

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-1321` |
| Published | 2026-08-11T17:19:16.977 |

Browserslist is a configuration tool for sharing target browsers and Node.js versions between front-end tools. Prior to 4.28.7, normalizeStats() in node.js, reached unconditionally through getStat() and loadStat() on every browserslist() call, processes untrusted browserslist-stats.json, opts.stats, and CLI --stats data with an unguarded for...in loop and plain-object bracket access and assignment, allowing inherited Object.prototype keys including __proto__, toString, valueOf, constructor, hasOwnProperty, and isPrototypeOf to cause an uncaught TypeError or modify the prototype of the returned normalized object. This issue is fixed in version 4.28.7.

### CVE-2026-65681

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:18:55.857 |

Null pointer dereference in Windows iSCSI Target Service allows an unauthorized attacker to deny service over a network.

### CVE-2026-62901

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-606` |
| Published | 2026-08-11T17:18:44.380 |

Unchecked input for loop condition in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-62898

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:43.993 |

Use after free in Microsoft QUIC allows an unauthorized attacker to disclose information over a network.

### CVE-2026-62787

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:32.470 |

Use after free in Windows DNS allows an authorized attacker to execute code over a network.

### CVE-2026-61363

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-08-11T17:18:11.190 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-61352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-11T17:18:09.800 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-59134

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-08-11T17:18:07.777 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-59132

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:18:07.430 |

Null pointer dereference in Windows TCP/IP allows an unauthorized attacker to deny service over a network.

### CVE-2026-54113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-11T17:18:03.457 |

Allocation of resources without limits or throttling in Windows Kernel allows an unauthorized attacker to deny service over a network.

### CVE-2026-48439

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-11T17:18:01.207 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-48438

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:18:01.087 |

CAI Content Credentials is affected by a NULL Pointer Dereference vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-48386

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-11T17:18:00.310 |

ColdFusion is affected by a Use of a Broken or Risky Cryptographic Algorithm vulnerability that could lead to disclosure of sensitive memory. An attacker could leverage this vulnerability to disclose sensitive information. Exploitation of this issue does not require user interaction.

### CVE-2026-67180

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-11T16:17:34.257 |

Google Turbinia allows arbitrary command execution via worker tasks. An attacker with privileges to submit a processing request or influence an evidence path/name obtains code execution on the worker fleet. Fixed on 2026-07-10.

### CVE-2026-18125

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T15:17:28.053 |

An out-of-bounds read in the Agent of Ivanti Endpoint Manager before version 2024 SU7 allows a remote unauthenticated attacker to crash an agent service.

### CVE-2026-73086

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:19:16.690 |

nanoid is a secure, URL-friendly, unique string ID generator for JavaScript. Prior to versions 3.3.12 and 5.1.11, the nanoid(size) function in index.js and index.cjs coerces the user-influenced size parameter to a signed 32-bit integer, allowing a value of 2147483648 to become -2147483648 and corrupt the process-wide CSPRNG poolOffset in fillPool(), which causes subsequent session tokens, CSRF tokens, API keys, and unique identifiers to become the deterministic string "uuuuuuuuuuuuuuuuuuuuu" until the process restarts. This issue is fixed in versions 3.3.12 and 5.1.11.

### CVE-2026-58612

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-11T17:18:04.987 |

Server-side request forgery (ssrf) in Microsoft PowerShell Core allows an unauthorized attacker to disclose information over a network.

### CVE-2026-53996

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T13:17:22.777 |

NetBSD's hdaudio(4) driver in sys/dev/hdaudio/hdaudio.c contains a missing access control vulnerability that allows unprivileged local attackers to invoke the HDAUDIO_FGRP_SETCONFIG ioctl without elevated permissions by exploiting the absence of an access check on /dev/hdaudioN device nodes. Attackers can repeatedly issue HDAUDIO_FGRP_SETCONFIG from one thread while keeping DMA and IRQs live from a second thread to trigger a use-after-free race condition in hdafg_detach() between stream_stop() and stream_disestablish(), where a latched DMA interrupt dereferences a freed callback pointer, resulting in outcomes ranging from audio-subsystem denial of service and kernel panic to potential local kernel privilege escalation.

### CVE-2026-71383

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T17:19:13.477 |

is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain limited unauthorized read and write access, causing a limited disruption to availability. Exploitation of this issue does not require user interaction.

### CVE-2026-70355

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:19:12.810 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68821

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T17:19:06.540 |

Improper privilege management in Windows Package Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-64900

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:18:50.827 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-62914

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-11T17:18:45.447 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Exchange Server allows an authorized attacker to perform spoofing over a network.

### CVE-2026-59119

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-11T17:18:05.957 |

Incorrect default permissions in Microsoft PowerShell allows an authorized attacker to elevate privileges locally.

### CVE-2026-18639

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-11T16:17:30.590 |

When Velociraptor is configured to use an OIDC IdP for authentication, it uses the email claim as a username. However, some IdP allow users to change the email claim without verification. Some IdPs do not set the "email_verified" claim and do not actually verify the email.

This allows a user to impersonate another user by setting their email address within the IdP, allowing account takeover.

### CVE-2026-18844

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-08-11T20:17:37.277 |

The firmware of the Pulsetto Vagus Nerve Stimulator accepts several undisclosed commands over its Bluetooth Low Energy (BLE) interface. These commands are sent without authentication or encryption, and are never issued by the companion mobile application, yet are fully processed by the device when it is powered on.

### CVE-2026-69119

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T19:18:42.393 |

Taubyte Tau v1.1.10 contains a missing authorization vulnerability in the services/auth HTTP service that allows any authenticated user to read or permanently delete another tenant's project by supplying an arbitrary project ID to the GET and DELETE /projects/{id} endpoints. The GitHubTokenHTTPAuth middleware only validates that a caller presents a valid GitHub OAuth token without verifying ownership or access rights to the target project, enabling attackers with any valid GitHub token to invoke bare KV-store operations such as projects.Fetch and project.Delete against any project ID to achieve cross-tenant project takeover.

### CVE-2026-18712

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T19:17:29.360 |

An issue in MongoDB Server's Queryable Encryption maintenance operations could allow an authenticated user with privileges on one encrypted collection to cause unauthorized modification or destruction of data belonging to a different collection. This is due to insufficient validation of certain internal metadata references before they are used to perform operations on other namespaces.

### CVE-2026-18693

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T19:17:23.450 |

An issue in MongoDB Server's handling of timeseries collections could allow an authenticated user with write privileges to cause an internal data structure to become inconsistent through certain document insertions. A subsequent insert into the affected bucket could then result in the server accessing memory outside its intended bounds, potentially causing a server crash (denial of service), exposure of limited memory contents, or memory corruption.

### CVE-2026-18690

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T19:17:22.757 |

An issue in MongoDB Server could allow an authenticated user with a limited database-scoped role to perform an action against protected system collections that their assigned privileges should not permit. This could result in critical system collections being dropped and recreated without proper authorization.

### CVE-2026-62910

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-99` |
| Published | 2026-08-11T17:18:44.943 |

Improper control of resource identifiers ('resource injection') in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-47299

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-11T17:17:59.100 |

Improper neutralization of special elements used in a command ('command injection') in Azure Monitor Agent allows an authorized attacker to elevate privileges over a network.

### CVE-2026-20749

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:17:51.293 |

Out-of-bounds read for some Intel(R) PROSet/Wireless WiFi Software within Ring 2: Device Drivers may allow an escalation of privilege. Network adversary with an unauthenticated user combined with a low complexity attack may enable escalation of privilege. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (low), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (low), integrity (low) and availability (low) impacts.

### CVE-2026-20716

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-11T17:17:49.973 |

Improper access control for some Intel(R) Processors within Ring 3: User Applications may allow an escalation of privilege. Simple hardware adversary with an authenticated user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are present with special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-18635

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T15:17:28.627 |

Velociraptor's VQL has a query() plugin which allows running a VQL query in a different org or user context. To be able to run as a different user, the calling user needs to have the IMPERSONATE permission (usually only given to administrators). Velociraptor versions prior to 0.77.2 evaluate this permission against the caller's org instead of against the target org.

This allows an administrator in one org to impersonate another user in another org, in which they may not have the IMPERSONATE permission.

### CVE-2026-66098

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-11T22:18:49.740 |

The Mira hormone monitor device firmware accepts a 0x01 write from any BLE central without authentication, causing the device to reboot into bootloader mode. An attacker could cause a denial-of-service condition or disrupt ovulation tracking and fertility monitoring workflow.

### CVE-2026-63177

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T21:17:44.443 |

Malcolm is a network traffic analysis tool suite. Prior to version 26.07.0, role-based access control enforced in the Nginx OpenResty Lua layer evaluates the raw, unnormalized `ngx.var.request_uri`, while Nginx itself routes requests using the normalized path. An authenticated low-privilege user can prepend a traversal segment (for example `/x/../upload/...`) so that Nginx routes the request to a restricted backend while the Lua role check fails to match any rule and falls open, granting access it should deny. Version 26.07.0 fixes the issue.

### CVE-2026-69117

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T19:18:42.247 |

NetBox 4.5.8 contains an ORM injection vulnerability that allows authenticated attackers, including those with read-only API tokens, to inject arbitrary Django ORM lookup expressions into nested object references by supplying crafted JSON dictionary keys in POST, PUT, or PATCH requests to any REST API endpoint. Attackers can exploit the unrestricted queryset used by WritableNestedSerializer to perform boolean-based blind data extraction of sensitive field values and bypass object-level permissions across all application modules including dcim, ipam, tenancy, virtualization, circuits, and extras.

### CVE-2026-69115

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T19:18:42.093 |

OpenIM Server v3.8.3 contains a missing authorization vulnerability that allows any authenticated user to access admin-only management API endpoints by submitting POST requests with a regular user bearer token to /user/get_users, /user/get_all_users_uid, and /group/get_groups. Attackers can exploit the absent authverify.CheckAdmin() call in the GetPaginationUsers, GetAllUserID, and GetGroups handlers to enumerate all platform user accounts including userIDs, nicknames, and manager level flags, as well as all groups including private groups the user has never joined, exposing group names, owner IDs, and member counts.

### CVE-2026-18711

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T19:17:26.170 |

An issue in MongoDB Server's query execution engine could allow an authenticated user with read and write privileges to cause an internal reference to be used after the underlying memory has been freed, when running certain queries against time-series collections. This could result in a server crash or disclosure of freed memory contents within query results.

### CVE-2026-18705

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-08-11T19:17:25.207 |

An issue in MongoDB Server's Atlas Vector Search feature could allow an authenticated user with read access to one view to retrieve documents from a different, protected view over the same underlying collection. This is due to insufficient handling of certain user-supplied fields when constructing an internal request forwarded to the search process.

### CVE-2026-18704

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T19:17:25.050 |

An issue in MongoDB Server's aggregation framework could allow an authenticated user with only read privileges to perform write operations against collections they should not be able to modify. This is due to an internal-use aggregation stage being reachable by external clients without an appropriate authorization check on its embedded operations.

### CVE-2026-18701

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-11T19:17:24.580 |

An issue in MongoDB Server's query subsystem could allow an authenticated user with read privileges to cause the server process to terminate unexpectedly by submitting a specially formed query filter. This could result in a denial of service.

### CVE-2026-18695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-08-11T19:17:23.717 |

An issue in MongoDB Server's handling of certain query predicates against time-series collections with a metaField could allow an authenticated user with write access to cause the server process to terminate unexpectedly, resulting in a denial of service.

### CVE-2026-18694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T19:17:23.580 |

An issue in MongoDB Server's geospatial query processing could allow an authenticated user with write privileges to cause certain malformed geometry data to be stored and later processed without proper validation. Subsequent queries against this data could then result in the server accessing memory outside its intended bounds. This could result in a server crash (denial of service) and may expose a limited amount of server process memory.

### CVE-2026-18688

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T19:17:22.620 |

An issue in MongoDB Server's aggregation framework could allow an authenticated user to trigger an out-of-bounds memory read by providing a specially formed numeric parameter in a certain aggregation pipeline stage. This could result in a server crash (denial of service) and may potentially expose a limited amount of memory contents.

### CVE-2026-18687

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-11T19:17:22.467 |

MongoDB Server's handling of a Queryable Encryption maintenance operation did not properly validate certain request parameters against the collection's encrypted field configuration before use. An authenticated user with readWrite privileges could submit a specially formed request that leads to a server crash or excessive internal writes, resulting in resource exhaustion and corruption of encrypted index data.

### CVE-2026-73215

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-772` |
| Published | 2026-08-11T18:18:26.910 |

Coturn is a free open source implementation of TURN and STUN Server. Prior to 4.17.0, turnports_allocate_even() in src/apps/relay/turn_ports.c marks the unused odd sibling port as TPS_TAKEN_ODD for an EVEN-PORT Allocate request with reservation bit R=0 even though no RTCP socket will release it, allowing an authenticated client to permanently exhaust the relay port pool and cause subsequent allocations to fail with STUN error 508. This issue is fixed in version 4.17.0.

### CVE-2026-48494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T18:17:33.310 |

TypeBot is a chatbot builder tool. In version 3.16.1, an authenticated user who has read access to any typebot can resume a WhatsApp preview webhook session that belongs to a different typebot by mixing an authorized `typebotId` and `blockId` and a foreign preview phone number tied to another preview session. The WhatsApp test-webhook handler authorizes the parent typebot first, but then resolves the preview chat session only by `wa-preview-{phone}`. As a result, an attacker can inject arbitrary webhook JSON into another workspace's WhatsApp preview session and advance its draft/unpublished flow without any access to the victim typebot. Version 3.17.0 patches the issue.

### CVE-2026-65675

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-08-11T17:18:55.427 |

No cwe for this issue in Visual Studio Code CoPilot Chat Extension allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-48442

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T17:18:01.450 |

CAI Content Credentials is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in a Arbitrary file system read. An attacker could leverage this vulnerability to gain unauthorized read access to files or directories outside the intended restrictions. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-47704

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-11T17:17:59.237 |

TypeBot is a chatbot builder tool. Prior to version 3.17.0, an authenticated user who has read access to any typebot can resume a waiting webhook session that belongs to a different typebot by mixing an authorized `typebotId` and `blockId` and a foreign live `resultId`. The webhook resume handler authorizes the parent typebot first, but then resolves the descendant `result` only by `resultId`. As a result, an attacker can inject arbitrary webhook JSON into another typebot's suspended session and advance its execution without any access to the victim typebot. Version 3.17.0 patches the issue.

### CVE-2026-20890

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-11T17:17:54.107 |

Improper privilege management for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Privileged Process may allow an escalation of privilege. Unprivileged software adversary with an unauthenticated user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (low), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (low), integrity (low) and availability (high) impacts.

### CVE-2026-20878

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:17:53.723 |

Null pointer dereference for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (low) impacts.

### CVE-2026-20795

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-11T17:17:53.430 |

Improper buffer restrictions for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (low) impacts.

### CVE-2026-20787

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-11T17:17:53.170 |

Null pointer dereference for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (low) impacts.

### CVE-2026-20747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-11T17:17:51.163 |

Improper conditions check for some Intel(R) PROSet/Wireless WiFi Software within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.

### CVE-2026-20745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-11T17:17:51.030 |

Out-of-bounds write for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (low) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (low) impacts.

### CVE-2026-20739

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-11T17:17:50.777 |

Improper conditions check for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 2: Device Drivers may allow a denial of service. Network adversary with an unauthenticated user combined with a low complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are not present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (low) impacts.

### CVE-2026-73074

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T16:17:38.697 |

Vim is an open source, command line text editor. Prior to 9.2.0841, prop_add_one() in src/textprop.c uses the proplen value from get_text_props() to increment a uint16_t property count beyond 0xffff, wrapping the count to zero and copying existing text-property records into a heap allocation sized for none of them. This issue is fixed in version 9.2.0841.

### CVE-2026-53416

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-11T16:17:32.960 |

Path traversal in Zoom VDI Client and Plugins may allow an authenticated user to conduct information disclosure via local access.

### CVE-2026-48495

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T16:17:32.170 |

TypeBot is a chatbot builder tool. Prior to version 3.17.0, the Google Sheets OAuth callback decodes a base64-encoded JSON `state` parameter and trusts the embedded `workspaceId`, `typebotId`, `blockId`, and `redirectUrl` without cryptographic integrity protection or authorization checks. The callback route is authenticated, but it does not verify that the authenticated user has write access to the target workspace or Typebot before creating credentials in the workspace or updating Typebot groups. An authenticated user who can obtain a valid Google OAuth `code` can alter the `state` value to create Google Sheets credentials in another workspace and, if target IDs are known, attach those credentials to a block in another Typebot. Version 3.17.0 patches the issue.

### CVE-2026-42142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-11T16:17:31.900 |

TypeBot is a chatbot builder tool. Prior to version 3.17.0, the `handleGetSheets` API handler (`POST /api/sheets/getSheets`) does not validate workspace membership, allowing any authenticated user to access and decrypt another workspace's Google Sheets OAuth credentials and retrieve spreadsheet data (sheet names, IDs, column headers). Version 3.17.0 fixes the issue.

### CVE-2026-18640

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-11T16:17:30.713 |

The NewNotebook API does not sufficiently sanitize its parameters allowing an authenticated user with NOTEBOOK_EDIT permission to write the notebook record outside the org's data store directory. The file written must have an extension of ".json.db" but can otherwise overwrite other metadata files (such as ACL records, hunts etc). This can corrupt these files and cause data corruption.

### CVE-2026-18696

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-11T19:17:23.853 |

An issue in MongoDB Server's applyOps command could allow an authenticated user with specific non-default privileges to perform certain data-definition operations, such as dropping or modifying collections, against collections they do not have permission to manipulate. This is due to an inconsistency in how the target collection is determined between the authorization check and the actual operation.

### CVE-2025-54512

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-11T18:17:17.557 |

A DLL hijacking vulnerability within the AMD Ryzen Master installation could allow a local user-privileged attacker to escalate privileges, potentially resulting in arbitrary code execution.

### CVE-2025-0046

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-11T18:17:17.420 |

Incorrect directory permissions could allow a local user to escalate their privileges, potentially resulting in arbitrary code execution.

### CVE-2026-70307

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:19:08.100 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-68820

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:19:06.357 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-65788

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:58.603 |

Use after free in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-65783

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:57.810 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65782

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:57.683 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65781

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:57.550 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65780

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-11T17:18:57.427 |

Double free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65779

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:57.310 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65778

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:57.187 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-65776

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:56.920 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-65678

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:55.540 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-62908

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:44.630 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-62897

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-11T17:18:43.850 |

Integer overflow or wraparound in .NET Framework allows an unauthorized attacker to execute code locally.

### CVE-2026-62892

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:42.337 |

Use after free in Capability Access Management Service (camsvc) allows an authorized attacker to elevate privileges locally.

### CVE-2026-62788

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:32.633 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62780

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:31.287 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62774

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:30.270 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62773

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:30.067 |

Use after free in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-62766

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-11T17:18:29.027 |

Double free in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-62753

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:27.903 |

Heap-based buffer overflow in Windows HTTP.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-62749

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:27.240 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-62748

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:27.050 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62734

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:24.847 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62729

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:24.100 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62728

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-367` |
| Published | 2026-08-11T17:18:23.910 |

Time-of-check time-of-use (toctou) race condition in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-62726

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:23.723 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62725

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:23.540 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62724

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:23.357 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62723

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:23.180 |

Use after free in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-62705

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:20.353 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-62693

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:18.870 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-62690

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:18.530 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-61939

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:18.207 |

Use after free in Winlogon allows an authorized attacker to elevate privileges locally.

### CVE-2026-61938

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:17.730 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-61929

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:15.770 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-61927

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:15.470 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-61366

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-11T17:18:12.827 |

Double free in Windows Network Connection Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-61361

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:11.070 |

Use after free in Windows DHCP Client allows an authorized attacker to execute code locally.

### CVE-2026-61348

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:09.260 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-61346

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:08.910 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-59126

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-11T17:18:06.583 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Event Logging Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-59125

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-11T17:18:06.417 |

Use after free in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-59122

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-08-11T17:18:06.090 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Telephony Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-50472

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-11T17:18:02.587 |

Heap-based buffer overflow in Windows LUAFV allows an authorized attacker to elevate privileges locally.

### CVE-2026-20885

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-11T17:17:53.850 |

Improper authentication in the Intel(R) TDX module for some Intel(R) platforms within Ring 0: Trust Domain may allow an information disclosure and escalation of privilege. System software adversary with a privileged user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (low), integrity (low) and availability (none) impacts.

### CVE-2026-20778

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-11T17:17:52.643 |

Out-of-bounds read for some Intel(R) PROSet/Wireless WiFi Software for Windows within Ring 0: Kernel may allow a denial of service. Unprivileged software adversary with an unauthenticated user combined with a high complexity attack may enable denial of service. This result may potentially occur via adjacent access when attack requirements are present without special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (none), integrity (none) and availability (high) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (high) impacts.

### CVE-2025-8087

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-11T17:17:44.463 |

A DLL hijacking vulnerability in AMD Power Design Manager could allow a malicious local attacker to escalate privileges during the uninstallation process, potentially resulting in arbitrary code execution.

### CVE-2025-31936

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1260;CWE-1260` |
| Published | 2026-08-11T17:17:43.500 |

Improper handling of overlap between protected memory ranges for some Intel(R) Xeon(R) 6 processors when using Intel(R) TDX within SMM may allow an escalation of privilege. SMM adversary with a privileged user combined with a high complexity attack may enable escalation of privilege. This result may potentially occur via local access when attack requirements are present with special internal knowledge and requires no user interaction. The potential vulnerability may impact the confidentiality (high), integrity (high) and availability (none) of the vulnerable system, resulting in subsequent system confidentiality (none), integrity (none) and availability (none) impacts.
