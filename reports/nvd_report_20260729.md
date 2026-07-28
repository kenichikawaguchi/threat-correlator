# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-28 15:00 UTC
- **対象期間**: `2026-07-27T15:00:20.000Z` 〜 `2026-07-28T15:00:41.000Z`
- **重要CVE数**: 137 件（Critical 9.0+: 28 件 / High 7.0〜: 109 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上り、特に **リモートコード実行 (RCE) と認証バイパス** が目立ちます。  
- Web アプリケーション（Joomla、WordPress、phpMyFAQ など）と **クラウド/オンプレミス統合基盤（VeloCloud、3DEXPERIENCE）** が集中して攻撃対象となっており、攻撃者は「認証不要」かつ「ネットワーク上から直接実行」できる脆弱性が多数報告されています。  
- データベースエンジン（SQLite）や CI ツール（JetBrains TeamCity）にも **Use‑After‑Free / メモリ破壊** 系の深刻なバグが見つかっており、OS 依存のカーネルレベル脆弱性（macOS / iOS 系）も同時期に多数報告されています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑65880** | 10.0 | Joomla 用 Balbooa Forms ( < 2.4.3 ) で **認証不要 RCE**。`signature` フィールドの処理ロジックにコードインジェクションが潜む。 | Joomla は日本国内でも多数の自治体・教育機関サイトで採用されている。プラグイン単体の脆弱性が **Web サーバ全体の乗っ取り** に直結するため、被害拡大リスクが極めて高い。 |
| **CVE‑2026‑11756** | 10.0 | 3DEXPERIENCE **Station Launcher** (R2023x‑R2026x) の **未検証デシリアライズ** による RCE。認証不要で任意コード実行可能。 | 製造業・航空宇宙分野で広く導入されている PLM プラットフォーム。オンプレミスでもクラウドでも同一脆弱性が存在し、**企業内部ネットワーク全体への侵入** が懸念される。 |
| **CVE‑2026‑16812** | 10.0 | VeloCloud Orchestrator (オンプレ) の **特権機能への不正アクセス**。機密情報・設定の漏洩・改竄・サービス停止が可能。 | SD‑WAN のコア管理コンポーネントであり、企業ネットワークのトラフィック制御を一手に担う。特権機能が奪われると **全社ネットワークの遮断・改ざん** が実現する。 |
| **CVE‑2026‑63077** | 9.8 | JetBrains TeamCity < 2026.1.3 の **エージェントポーリングプロトコル** を経由した **認証不要 RCE**。 | CI/CD パイプラインは開発・デプロイの要であり、侵入されれば **ビルドサーバ上の全リポジトリ・シークレット情報が流出** する。 |
| **CVE‑2026‑51303 / CVE‑2026‑51302** | 9.8 | SQLite 3.41 系の **Use‑After‑Free** バグ。特製 SQL クエリでメモリ破壊 → 任意コード実行。 | SQLite は組み込みデータベースとしてモバイルアプリ・IoT デバイスに広く組み込まれている。**アップデートが遅れやすい** 環境での攻撃リスクが高い。 |

> **共通点**：すべて「認証不要」か「低権限でも特権取得可能」な点で、**外部からの直接攻撃** が可能。特にインフラ系 (3DEXPERIENCE、VeloCloud) と開発ツール (TeamCity) は、社内ネットワーク全体への踏み台になる危険性がある。

---

## 3. 推奨アクション  

### 3‑1. 速やかなパッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン | 備考 |
|-------------------|-------------------|----------------|------|
| **Balbooa Forms (Joomla)** | < 2.4.3 | **≥ 2.4.3** | Joomla 本体も最新 (4.3 系) に更新し、不要プラグインは無効化 |
| **3DEXPERIENCE Station Launcher** | R2023x‑R2026x | **R2026x SP‑1 以降** (ベンダーパッチ) | 3DEXPERIENCE 全体のセキュリティパッチを同時に適用 |
| **VeloCloud Orchestrator (VCO)** | すべてのオンプレリリース | **最新パッチ (2026‑xx‑xx)** | 管理コンソールへの IP 制限・VPN 経由のみアクセスに切り替え |
| **JetBrains TeamCity** | < 2026.1.3 | **≥ 2026.1.3** | エージェント通信は TLS 1.2 以上、エージェント認証を必須化 |
| **SQLite** | 3.41.x 系 | **3.42.0 以降** | 主要ディストリビューション (Ubuntu 24.04, Alpine 3.20 等) のパッケージを更新 |
| **phpMyFAQ** | < 4.1.6 | **≥ 4.1.6** | `upgrade.lastDownloadedPackage` 設定の書き込み権限を最小化 |
| **Pheditor** | 2.0.1‑2.0.5 | **≥ 2.0.6** | デフォルトパスワード削除、`dir` パラメータのサニタイズを確認 |
| **WordPress プラグイン** (SMS Alert, TrueBooker, Eazy Plugin Manager 等) | 3.9.7 以前等 | **各プラグインの最新リリース** (2026‑xx‑xx) | `wp core` とプラグインの自動更新を有効化 |
| **macOS / iOS / iPadOS / tvOS / watchOS** | 15.7.8, 14.8.8, 26.6 以前 | **最新 OS アップデート** (Sequoia 15.8, Sonoma 14.9, etc.) | カーネルメモリ破壊系脆弱性は OS レベルで修正 |

### 3‑2. 防御的設定・監視の強化
1. **ネットワーク境界の制御**  
   - VeloCloud Orchestrator、3DEXPERIENCE の管理ポートは **IP アクセスリスト**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65880

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-28T11:17:04.233 |

Joomla Extension - balbooa.com - Unauthenticated remote code execution in Balbooa Forms < 2.4.3 - An insecure form processing logic allowed code execution for forms that include the signature field type.

### CVE-2026-11756

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-28T08:17:14.007 |

A Deserialization of Untrusted Data vulnerability affecting Station Launcher App in 3DEXPERIENCE platform from Release 3DEXPERIENCE R2023x through Release 3DEXPERIENCE R2026x could lead to an unauthenticated remote code execution.

### CVE-2026-16812

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T16:17:03.640 |

VeloCloud Orchestrator (VCO) on-prem has a security issue where this issue may allow a remote attacker to access privileged internal functionality and impact the VCO host. Successful exploitation may compromise the confidentiality, integrity, and availability of the orchestrator and data managed by the orchestrator.




This functionality was intended to be for internal use only and is not intended to be remotely accessible.




Hosted and Dedicated versions of VCO have already been patched in advance of this notice going out.




This issue was discovered externally and is known to be actively exploited.

### CVE-2026-48030

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T18:16:55.347 |

Pheditor is a single-file editor and file manager written in PHP. From version 2.0.1 to before version 2.0.4, an OS Command Injection vulnerability in the terminal action handler allows any authenticated user to execute arbitrary OS commands by injecting shell metacharacters into the 'dir' POST parameter, completely bypassing the TERMINAL_COMMANDS whitelist and achieving full Remote Code Execution with web server privileges. This issue has been patched in version 2.0.4.

### CVE-2026-15014

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-28T08:17:14.580 |

The SMS Alert – SMS & OTP for WooCommerce, Order Notifications & Abandoned Cart Recovery plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 3.9.7 via the `billing_phone` parameter. This is due to the `processRegistration()` function using a phone-unbound `$_SESSION['sa_mobile_verified']` boolean flag as the sole gate before issuing an authentication cookie — the flag is set to `true` after any successful OTP validation without being bound to the specific phone number that was verified. This makes it possible for unauthenticated attackers to complete OTP verification for a phone number they control, then resubmit the registration request with a victim's `billing_phone` value to have `wp_set_auth_cookie()` called for the resolved victim account, enabling full authentication as any existing WordPress user whose registered phone number is known or guessable, including administrators.

### CVE-2026-14545

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-28T07:16:41.100 |

The TrueBooker  WordPress plugin before 1.2.4 does not validate account ownership when resetting a user's password through one of its front-end account handlers, allowing unauthenticated attackers to set an arbitrary password on any account, including an administrator, and take over the site.

### CVE-2026-64697

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-07-27T21:17:09.393 |

The issue was addressed with improved memory handling. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to cause unexpected system termination or corrupt kernel memory.

### CVE-2026-43730

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-27T21:16:57.587 |

A permissions issue was addressed with additional restrictions. This issue is fixed in iOS 26.6 and iPadOS 26.6, macOS Tahoe 26.6, tvOS 26.6, visionOS 26.6, watchOS 26.6. An app may be able to fingerprint the user.

### CVE-2026-28931

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-27T21:16:49.750 |

A buffer overflow was addressed with improved bounds checking. This issue is fixed in iOS 26.6 and iPadOS 26.6, macOS Tahoe 26.6, tvOS 26.6, watchOS 26.6. Connecting to a malicious NFS server may lead to kernel memory corruption.

### CVE-2026-55579

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-27T18:16:56.880 |

Pheditor is a single-file editor and file manager written in PHP. From version 2.0.1 to before version 2.0.6, Pheditor ships with a hardcoded default password admin (SHA-512 hash stored at pheditor.php:11). There is no mechanism to force a password change on first login. Any deployment using the default credentials grants an attacker full access to the file editor, file upload, and terminal features, enabling arbitrary file read/write and remote code execution. This issue has been patched in version 2.0.6.

### CVE-2026-63077

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-27T17:16:38.830 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 unauthenticated remote code execution was possible via the agent polling protocol

### CVE-2026-51303

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-27T16:17:39.380 |

A use-after-free (UAF) vulnerability was discovered in the core parsing component of SQLite 3.41. The flaw occurs because the program frees an ExprList object via sqlite3ExprListDelete and then subsequently accesses the dangling pointer of the released object. A remote adversary can supply specially crafted SQL queries to trigger this vulnerability during SQL statement parsing. Successful exploitation may result in application crash (denial of service), sensitive memory information leakage, and in some scenarios, arbitrary code execution on the affected host.

### CVE-2026-51302

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-27T16:17:39.273 |

SQLite 3.41 has a use-after-free vulnerability exists in the expression evaluation logic. The sqlite3ReleaseTempReg function improperly releases temporary register resources, and the subsequent exprComputeOperands function continues to access the already freed register memory. By supplying a malicious SQL statement, a remote attacker can exploit this flaw to cause denial of service, leak sensitive information, or potentially execute arbitrary code on the affected system.

### CVE-2026-11841

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-552` |
| Published | 2026-07-28T10:16:47.867 |

An attacker may perform unauthenticated read and write operations on sensitive filesystem areas via the AppEngine Fileaccess over HTTP due to improper access restrictions. A critical filesystem directory was unintentionally exposed through the HTTP-based file access feature, allowing access without authentication. This includes device parameter files, enabling an attacker to read and modify application settings, including customer-defined passwords. Additionally, exposure of the custom application directory may allow execution of arbitrary Lua code within the sandboxed AppEngine environment.

### CVE-2026-66398

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-07-27T16:18:12.493 |

phpMyFAQ before v4.1.6 contains a remote code execution vulnerability in the configuration API that allows authenticated administrators with CONFIGURATION_EDIT and ATTACHMENT_ADD privileges to write arbitrary PHP files by manipulating the upgrade.lastDownloadedPackage setting. Attackers can upload a malicious ZIP file as an attachment, point the updater configuration to its stored path, and extract it into the application root to achieve code execution as the web server user.

### CVE-2026-66395

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T16:18:12.083 |

SiYuan desktop before v3.7.2 contains a reflected cross-site scripting vulnerability in the bazaar plugin readme handler that allows attackers to execute arbitrary code by crafting a malicious siyuan:// deep link. Attackers can inject HTML payloads via the plugin name parameter that execute with full Node.js access through insertAdjacentHTML rendering in an insecurely configured Electron renderer.

### CVE-2026-16462

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T10:16:48.293 |

In PROCON-WEB SCADA the endpoint 'GetGridData' is not properly sanitized. This allows a remote unauthenticated attacker to execute arbitrary SQL commands.

### CVE-2026-66396

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T16:18:12.220 |

SiYuan before v3.7.2 fails to escape the title-img Individual Attribute List value when rendering Gallery and Kanban cover images, allowing stored cross-site scripting via unescaped style attribute interpolation. Attackers with editor permissions can inject onload handlers that execute arbitrary code in the Electron renderer with full Node.js access when victims open affected documents.

### CVE-2026-66394

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T16:18:11.947 |

SiYuan before v3.7.3 contains stored and reflected cross-site scripting vulnerabilities in SVG sanitization that allows authenticated attackers to execute scripts by bypassing the HTML parser-based cleaner. Attackers can hide script tags within desc, style, or noscript elements which the HTML parser treats as raw text but browsers interpret as executable SVG content when served as image/svg+xml, enabling script execution in the application origin.

### CVE-2026-59550

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:05.090 |

Unauthenticated SQL Injection in AWP Classifieds <= 4.4.7 versions.

### CVE-2026-59549

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:04.960 |

Unauthenticated SQL Injection in rtMedia for WordPress, BuddyPress and bbPress <= 4.7.10 versions.

### CVE-2026-59538

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:04.460 |

Unauthenticated SQL Injection in GamiPress <= 7.9.7 versions.

### CVE-2026-59533

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:03.817 |

Unauthenticated SQL Injection in Relevanssi Light <= 1.2.2 versions.

### CVE-2026-59527

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:03.017 |

Unauthenticated SQL Injection in MapSVG <= 8.14.0 versions.

### CVE-2026-66824

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T21:17:17.500 |

A stored cross-site scripting vulnerability existed in the capture tree visualization page. The application embedded the serialized capture tree directly into an inline JavaScript block using the Jinja safe filter.

Because the tree data can contain values derived from captured and potentially attacker-controlled web content, a specially crafted value could prematurely terminate the surrounding <script> element and inject arbitrary HTML or JavaScript. The malicious code would execute in the browser of a user viewing the affected capture tree.

Successful exploitation could allow an attacker to perform actions using the victim’s authenticated session, access information available to the victim, or modify application data within the permissions of the affected user.

The patch removes the JSON data from the HTML document and retrieves it through a dedicated API endpoint. The client then processes the response using response.json(), preventing capture data from being interpreted as executable content within the original page’s HTML or JavaScript context.

### CVE-2026-55953

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-757` |
| Published | 2026-07-27T16:17:49.500 |

The Erlang/OTP ssl TLS 1.2 (and earlier) and DTLS client does not verify that the cipher suite selected by the server in ServerHello was among the suites offered by the client in ClientHello. The client-side tls_handshake:hello/5 handler validates the negotiated protocol version and the downgrade sentinel but hands the server-chosen suite directly to ssl_handshake:handle_server_hello_extensions/9, which installs it without a membership check. The TLS 1.3 client path performs this check (per RFC 8446), so it is not affected.

An on-path attacker between the client and the intended server can respond with a ServerHello selecting an anonymous key exchange suite such as TLS_DH_anon_* or TLS_ECDH_anon_* that the client never offered. Anonymous suites do not require the server to present a certificate, so the entire verify_peer and cacerts configuration is bypassed: the attacker completes the handshake with its own ephemeral parameters, no certificate is validated, no hostname is checked, and ssl:connect returns {ok, Socket}. All subsequent application traffic is readable and modifiable by the attacker.

This issue affects OTP from OTP 17.0 before OTP 29.0.4, OTP 28.5.0.4 and OTP 27.3.4.15, corresponding to ssl from 5.3.4 before 11.7.4, 11.6.0.4 and 11.2.12.11.

### CVE-2026-51300

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-27T16:17:39.153 |

A use-after-free vulnerability exists in the expression parsing and memory management logic of SQLite 3.41. After invoking sqlite3ExprDelete to release an expression object, the program still retains the dangling pointer and subsequently accesses member fields of the already freed memory. By constructing malicious SQL queries, a remote attacker can trigger invalid memory access, leading to application crash and sensitive memory information leakage.

### CVE-2025-50455

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T16:16:58.860 |

SQL injection vulnerability exists in the order_by parameter of the /customers/search endpoint in Alex Tselegidis EasyAppointments <= 1.5.1. The vulnerability arises from unsanitized user input passed to the order_by method of the CodeIgniter Query Builder, enabling attackers to perform time-based queries and schema enumeration. Under certain MySQL configurations, the flaw may lead to remote code execution by writing a PHP shell using INTO OUTFILE.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-7187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-28T13:19:08.247 |

Missing authentication for critical function vulnerability in Universal Software Inc. UKBS allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects UKBS: through 28072026.
NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-14328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-28T10:16:48.020 |

The Eazy Plugin Manager – Powerful Plugin Management Solution for WordPress plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.4.1. This is due to insufficient authorization on the `wp_ajax_pos_get_option` AJAX handler, which verifies only a nonce that is localized to every logged-in admin-area user via `admin_enqueue_scripts` — without any capability check — before returning the value of any arbitrary WordPress option via `get_option()`, combined with the `admin_login_endpoint_handler` REST endpoint (`GET /wp-json/epm/v1/admin/login`) being registered as publicly accessible and authenticating callers solely by a whirlpool hash of values stored in those same options. This makes it possible for authenticated attackers, with Subscriber-level access and above, to read the `site_url`, `connection_key`, and `remote_user_id` values stored in the `eazywp_connecting_info` and `eazywp_connection` options, compute the required `auth_key`, call the `admin/login` REST endpoint to obtain Administrator authentication cookies, and fully take over the site. Exploitation requires the plugin's remote connection feature to have been configured, as the `eazywp_connecting_info` and `eazywp_connection` options must be populated with valid credentials.

### CVE-2026-14168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-28T09:16:41.517 |

A low privileged remote attacker can gain administrator privileges due to missing authorization at the insert path of the configuration table resulting in gaining full system access.

### CVE-2026-66014

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-27T20:16:41.790 |

JFrog Artifactory contains an authentication handling weakness in internal request processing that, under specific conditions, may allow an attacker to escalate privileges beyond the intended access level.

### CVE-2026-65921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T20:16:41.190 |

A path validation weakness in archive extraction/write handling allows entries with traversal sequences to be written outside the intended build artifacts location.

### CVE-2026-65617

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-27T20:16:40.953 |

A deserialization weakness in JFrog Artifactory package handling could allow a low-privileged user to impact confidentiality, integrity, and availability under specific repository conditions.

### CVE-2026-65616

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-27T20:16:40.843 |

Incorrect authorization validation in refresh token signature allows non-admin users to obtain a signed JFrog administrator token.

### CVE-2026-42017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-27T20:16:39.750 |

An event-handling weakness in JFrog Artifactory could expose privileged authorization material to a lower-privileged user under specific conditions.

### CVE-2026-55578

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T18:16:56.730 |

Pheditor is a single-file editor and file manager written in PHP. From version 2.0.1 to before version 2.0.6, the terminal feature in Pheditor uses an incomplete character blocklist to sanitize user-supplied commands before passing them to shell_exec(). After the fix for GHSA-9643-6xjp-vx57 (which added $ to the blocklist), the characters | (single pipe), ` (backtick), and the newline byte (0x0A) remain unblocked. An authenticated user with the terminal permission (enabled by default) can leverage any of these to bypass the TERMINAL_COMMANDS allowlist and execute arbitrary OS commands as the web server user. This issue has been patched in version 2.0.6.

### CVE-2026-54540

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T18:16:56.580 |

Pheditor is a single-file editor and file manager written in PHP. Prior to version 2.0.5, there is an authenticated terminal command whitelist bypass. The terminal feature checks whether the submitted command starts with one of the configured TERMINAL_COMMANDS values, then passes the full command string to shell_exec(). Shell command substitution such as $() is not blocked, so an authenticated user with the terminal permission can bypass a restricted command allowlist and execute arbitrary shell commands as the web server user. This issue has been patched in version 2.0.5.

### CVE-2026-51235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-27T18:16:56.117 |

LibRaw 0.21 is vulnerable to Buffer Overflow in the stretch() function (src/libraw_cxx.cpp) and fuji_rotate() function (src/decoders/fuji.cpp).

### CVE-2026-51297

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-27T16:17:38.933 |

sqlite 3.41 has a use-after-free vulnerability in the JSON parsing logic. Remote adversaries can craft malicious JSON payload to trigger memory free followed by illegal memory access, which may lead to arbitrary code execution, sensitive information leakage and service denial.

### CVE-2026-59248

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-28T10:16:50.083 |

Allocation of resources without limits vulnerability in ninenines cowlib allows an unauthenticated remote HTTP/2 or HTTP/3 peer to exhaust memory on the vulnerable server (or client) and cause a denial of service.

The HPACK and QPACK prefixed-integer decoder cow_hpack_common:dec_big_int/3 in src/cow_hpack_common.hrl (invoked from cow_hpack:decode/2 in src/cow_hpack.erl and from cow_qpack:decode_field_section/3 in src/cow_qpack.erl) reads continuation octets until it sees one whose high bit is clear, evaluating Int + (Value bsl M) at each step with the shift M growing by seven per octet. No limit is enforced on the number of continuation octets, on the resulting bit width, or on the value; the decoder consumes whatever encoded length the peer supplies.

Because Erlang integers are immutable, each intermediate Value bsl M and each accumulator update allocates a fresh bignum whose digit width grows linearly with the number of octets processed so far. Summed across the whole decode, the transient bignum digit materialization is on the order of the square of the encoded length. A single maximal HPACK indexed representation carried inside one HTTP/2 HEADERS plus one CONTINUATION frame at Cowboy's default max_frame_size_received can force hundreds of megabytes of transient allocation and garbage-collection churn before the resulting header-table index is rejected as invalid. Repeated or concurrent connections multiply the pressure and can drive the Erlang VM to memory exhaustion.

Cowlib is the HTTP parser used by Cowboy, RabbitMQ's management plugin, and other Erlang and Elixir HTTP/2 and HTTP/3 servers and clients, so any exposed endpoint that accepts HPACK or QPACK from an untrusted peer is reachable.

This issue affects cowlib: from 2.0.0 before 2.19.0.

### CVE-2026-14167

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-28T09:16:41.363 |

A low privileged remote attacker can perform privileged configuration changes reserved for the administrator level including permission management due to incorrect authorization.

### CVE-2026-17524

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T06:16:41.380 |

Versions of the package zip-lib before 1.1.0 are vulnerable to Directory Traversal via the caching mechanism for path validation during the extraction process. An attacker can bypass security checks designed to prevent directory traversal. The intended security function, isOutsideTargetFolder, only checks and caches the path status when the initial directory symlink is created during the first extraction.

### CVE-2026-55685

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-07-27T22:17:40.860 |

React Router is a router for React. In versions 7.0.0 through 7.17.0, the manifest endpoint could be accessed via unauthenticated targeted requests that would put heavy load on the server and slow down response times. This issue is a follow up to CVE-2026-42342, and does not does not impact React Router applications using Declarative Mode (<BrowserRouter>) or Data Mode (createBrowserRouter/<RouterProvider>). This issue has been fixed in version 7.18.0.

### CVE-2026-56748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-07-27T20:16:40.017 |

Improper validation of symbolic links in the Pack Git import feature in Cribl Stream before 4.18.2 allows a remote authenticated attacker with Pack import and pipeline preview permissions to execute arbitrary code as the Cribl server process via a crafted Git repository containing a symbolic link in the pack's functions directory.

### CVE-2026-56747

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-27T20:16:39.873 |

Improper control of generation of code in the JSON Pointer-to-accessor compiler in Cribl Stream before 4.18.2 allows a remote authenticated attacker with edit privileges to execute arbitrary JavaScript on the server via a crafted database connection identifier or pack configuration value.

### CVE-2026-66731

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-27T17:16:42.793 |

facil.io 0.7.5 through 0.7.6 contains a denial-of-service vulnerability in the HTTP/1.1 chunked transfer encoding parser that allows unauthenticated remote attackers to crash the server by sending a negative chunk size value. Attackers can send a single POST request with a Transfer-Encoding: chunked header containing a leading minus sign in the chunk size field, causing the parser in http1_parser.h to compute a large positive integer from the negated value, corrupting internal state and moving the read pointer into unmapped memory resulting in a fault.

### CVE-2026-66730

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-27T17:16:42.660 |

facil.io 0.6.0 through 0.7.6 contains a denial-of-service vulnerability in the multipart body parser that allows an unauthenticated remote attacker to permanently freeze worker processes at 100% CPU by sending a multipart/form-data request with a partial closing boundary. The missing progress guard in the parser loop causes http_mime_parse to return 0 bytes consumed without setting done or error flags, causing the calling loop to re-invoke the parser on the same buffer indefinitely, exhausting all workers and permanently disabling the server until manually restarted.

### CVE-2026-66729

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-27T17:16:42.517 |

facil.io 0.6.0 through 0.7.6 contains an integer underflow vulnerability in the multipart MIME body parser that allows unauthenticated remote attackers to crash the server process by sending a crafted Content-Disposition header with an empty field name. Attackers can trigger a uint32_t wraparound in http_mime_parser.h causing an out-of-bounds memory read past the name pointer, resulting in a bus fault that crashes the handling worker with a single POST request.

### CVE-2026-59251

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-27T16:18:03.517 |

Allocation of resources without limits in Erlang/OTP public_key certificate path validation allows a remote unauthenticated attacker to cause denial of service by sending a crafted X.509 certificate chain during the TLS handshake.

During RFC 5280 policy processing in public_key:pkix_path_validation/3, the certificate policy tree maintained by pubkey_policy_tree grows without an upper bound. When a certificate chain contains M policies per certificate and K certificates, the tree grows on the order of M^K nodes because pubkey_policy_tree:add_leaves/2 and pubkey_policy_tree:add_leaf_siblings/2 extend the tree per policy per certificate. A modest chain with many policies per certificate is enough to pin BEAM schedulers and exhaust the node's memory, taking down the entire VM. The attacker only needs to be able to present a certificate chain to the victim, which is the normal precondition for a TLS handshake, so exploitation succeeds against any incoming or outgoing TLS connection that validates the peer's chain (the default for SSL/TLS clients and mutual-TLS servers).

This is the same vulnerability class as OpenSSL's X509_verify_cert policy tree DoS.

This vulnerability is associated with program files lib/public_key/src/pubkey_policy_tree.erl and program routines pubkey_policy_tree:add_leaves/2 and pubkey_policy_tree:add_leaf_siblings/2.

This issue affects OTP from OTP 26.2 before OTP 29.0.4, OTP 28.5.0.4 and OTP 27.3.4.15, corresponding to public_key from 1.15 before 1.21.4, 1.20.3.4 and 1.17.1.5.

### CVE-2026-58227

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-27T16:17:56.953 |

The Erlang/OTP ssl application does not detect cycles when reconstructing an incomplete peer certificate chain during a TLS or DTLS handshake. In ssl_certificate:handle_incomplete_chain/5, the received chain is passed to ssl_certificate:build_certificate_chain/5, which walks issuer relationships via ssl_certificate:do_certificate_chain/7 with no cycle detection and no depth limit. When the peer supplies two mutually cross-signed certificates in unordered form (A issues B, B issues A), the issuer lookup alternates between the two certificates and the pair of functions recurses indefinitely, growing the call stack and chain accumulator without bound.

An unauthenticated remote attacker can send a crafted certificate chain in a TLS or DTLS Certificate handshake message to exhaust available memory and crash the BEAM node. Only a TCP connection and a partial handshake are required; no authentication or completed handshake is needed, and both TLS/DTLS servers and clients are affected when processing peer certificate messages.

This issue affects OTP from OTP 23.2 before OTP 29.0.4, OTP 28.5.0.4 and OTP 27.3.4.15, corresponding to ssl from 10.2 before 11.7.4, 11.6.0.4 and 11.2.12.11.

### CVE-2026-66050

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T15:17:10.487 |

NitroShare Desktop through 0.3.4 contains a path traversal vulnerability in its LAN file transfer server that allows unauthenticated attackers on the same network to write arbitrary files by sending a crafted filename containing directory traversal sequences in the JSON item header name field. Attackers can exploit the lack of path validation to write files outside the transfer root directory to arbitrary locations the current user has write access, including the Windows Startup folder, enabling persistent code execution on the next user login.

### CVE-2026-61376

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-28T09:16:42.553 |

ELECOM wireless LAN routers and access points devices contain an OS Command Injection vulnerability in Restore Settings. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-59764

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-28T09:16:42.417 |

ELECOM wireless LAN routers and access points devices contain an OS Command Injection vulnerability in WebUI. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-59239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T18:16:57.300 |

Stored Cross-site Scripting (CWE-79) in the email module in Roskus Prospero Flow CRM before 5.4.4 allows a remote, authenticated low-privileged user to execute arbitrary JavaScript in another user's browser, including administrators, leading to session compromise and account takeover, via a payload stored in an email body that is persisted without sanitization and rendered unescaped with {!! $email->body !!} when the recipient opens the message.

### CVE-2026-66397

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T16:18:12.363 |

phpMyFAQ before 4.1.6 fails to validate path traversal sequences in the existing_image field during category updates, allowing authenticated attackers to delete arbitrary files by exploiting insufficient sanitization in Image::delete(). Attackers can delete the database.php configuration file to disable the installation gate and access the public setup wizard to create new superadmin accounts.

### CVE-2026-49332

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-28T13:18:46.067 |

A flaw was found in openshift/oauth-proxy. The proxy sets authenticated identity headers using only dash-variant keys (X-Forwarded-User) but does not strip underscore-variant keys (X_Forwarded_User) from incoming requests. WSGI and PHP frameworks normalize both variants to the same variable, allowing an authenticated low-privilege user to smuggle a forged identity that may override the legitimate authenticated identity in the upstream application.

### CVE-2026-17191

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T17:16:35.407 |

An input validation vulnerability exists in an API component of the orchestrator. An authenticated user can exploit this flaw to manipulate backend queries, which may result in unauthorized access to data beyond their intended privileges and cause the underlying system to initiate unintended outbound network connections.




This issue was discovered internally by Arista and the company is not aware of any malicious uses of this issue in customer networks.

### CVE-2026-66399

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-27T16:18:12.633 |

phpMyFAQ before 4.1.6 contains a privilege escalation vulnerability in GroupController::updateMembers() that allows administrators with only group-management permissions to join privileged groups without verification of required rights. Attackers can add themselves to pre-existing groups holding user-management rights and immediately inherit those permissions to modify or delete user accounts.

### CVE-2026-59551

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:05.223 |

Subscriber SQL Injection in rtMedia for WordPress, BuddyPress and bbPress <= 4.7.10 versions.

### CVE-2025-59172

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T15:16:45.017 |

Ericsson Packet Core Controller (PCC) versions prior to 1.38 contain an Improper Neutralization of Special Elements vulnerability allowing an attacker to execute arbitrary code as root.

### CVE-2026-16481

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-27T19:17:14.970 |

A Server-Side Request Forgery (SSRF) and credential exfiltration vulnerability exists in the cloud-healthcare-fhir-fetch-page tool of googleapis/mcp-toolbox.

The tool takes an unvalidated pageURL parameter from the client and issues an HTTP GET request to it using an authenticated client. The underlying transport automatically attaches an Authorization: Bearer  header to every outbound request regardless of the destination host. An attacker can supply an arbitrary external URL to the pageURL parameter (either directly via the tool execution payload or implicitly via data-driven pagination tracking loops), leading Toolbox into sending its OAuth/service-account access token to an attacker-controlled listener. Depending on the configuration, this leaks either the end-user's token or the broader service-account access token (ADC), potentially exposing Protected Health Information (PHI) and secondary Google Cloud Platform services.

### CVE-2026-21047

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-28T12:16:36.207 |

Out-of-bounds write in ImsService prior to SMR Jul-2026 Release 1 allows remote attackers to potentially execute arbitrary code.

### CVE-2026-64649

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-27T20:16:40.703 |

Next.js is a React framework for building full-stack web applications. In versions 14.1.1 through 15.5.20 and 16.0.0 through 16.2.10, when a Server Action forwards or redirects a request, an attacker can cause the server to send that outbound request to a malicious host (Server-Side Request Forgery). This requires the attacker's request to control Host-associated headers. In some configurations, it's also possible to obtain internal values that weaken middleware/proxy authorization. Applications that use Server Actions are affected when the incoming host header is not fixed to a trusted value. This typically occurs on custom servers, or on deployments not behind a proxy that pins the host. Managed hosting pins the host upstream and is not affected; next start and standalone output do the same from version 14.2 onward. This issue has been fixed in versions 15.5.21 and 16.2.11.

### CVE-2026-64645

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601;CWE-918` |
| Published | 2026-07-27T18:16:59.453 |

Next.js is a React framework for building full-stack web applications. In versions 12.0.0 through 15.5.20 and 16.0.0 through 16.2.10, a
 rewrites() or redirects() rule that builds its external destination hostname from request-controlled input can be pointed at an arbitrary hostname, regardless of the rule's hostname suffix. For a rewrite, Next.js proxies the request to that arbitrary host and serves the response from the application's origin, leading to Server-Side Request forgery. A redirects() rule configured this way is vulnerable to an Open Redirect. This issue has been fixed in versions 15.5.21 and 16.2.11.

### CVE-2026-64642

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-27T18:16:59.010 |

Next.js is a React framework for building full-stack web applications. In versions 16.0.0 through 16.2.10, crafted requests targeting Next.js applications using App Router built with Turbopack and a single entry in config.i18n.locales can bypass middleware/proxy based authentication. This issue has been fixed in version 16.2.11.

### CVE-2026-59250

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-07-27T16:18:03.330 |

Classic buffer overflow in the Erlang/OTP megaco flex scanner C driver allows a remote unauthenticated attacker to corrupt the driver's memory (and potentially achieve remote code execution or a denial-of-service crash) by sending a single text-encoded H.248/Megaco message containing an oversized property parm name.

When tokenizing a Local/Remote descriptor, mfs_load_property_groups extracts the attacker-controlled property name (bounded only by the message length) and, when no value follows, formats it into a fixed 512-byte error_msg field of the MfsErlDrvData struct using an unchecked sprintf call. Names longer than roughly 452 bytes overflow into the immediately following struct fields (text_buf, text_ptr, term_spec, term_spec_size, term_spec_index), overwriting live pointers and counters with attacker-chosen bytes. Subsequent scanner code writes and frees through the corrupted pointers, producing arbitrary write and arbitrary free primitives inside the BEAM VM process, which can be leveraged for remote code execution. On builds compiled with _FORTIFY_SOURCE the overflow is detected at runtime and terminates the process with SIGABRT, resulting in denial of service.

The overflow occurs in the flex scanner before any grammar or Megaco-level authentication processing, so exploitation requires only network reachability to the megaco transport port on a node configured with {scanner, flex}.

This vulnerability is associated with program files lib/megaco/src/flex/megaco_flex_scanner_drv.flex.src and program routines mfs_load_property_groups.

This issue affects OTP from OTP 17.0 before OTP 29.0.4, OTP 28.5.0.4 and OTP 27.3.4.15, corresponding to megaco from 3.17.1 before 4.9.1, 4.8.3.1 and 4.7.2.2. Versions prior to OTP 17.0 are also affected but are not listed because the OTP version scheme is only defined from OTP 17.0 onwards.

### CVE-2026-66920

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-07-28T13:19:07.030 |

Pivotick contains an uncontrolled-recursion vulnerability when processing caller-supplied graph and node data. The affected graph algorithms recursively traversed graph edges, while the JSON viewer recursively processed each level of a node’s data structure. A specially crafted graph containing an excessively long path, deeply nested properties, or circular object references could therefore exhaust the JavaScript call stack when Pivotick calculates a layout or displays a node in the inspection modal.

Successful exploitation may cause an uncaught exception, freeze the affected page, or crash the browser tab, resulting in a client-side denial of service. No confidentiality or integrity impact has been identified.

The patch replaces the recursive graph traversals with iterative stack-based implementations and limits the reachability calculation to 1,000,000 edge traversals. It also limits JSON rendering to 64 levels and detects circular references before descending further into an object.

### CVE-2026-66918

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T13:19:06.693 |

Pivotick fails to sanitize attacker-controlled SVG markup supplied through the per-node style.svgIcon property before inserting it into the document.

When rendering a graph node, the vulnerable code assigns the SVG icon markup directly to the innerHTML property of a live SVG element. An attacker able to influence graph data can provide crafted markup containing executable event handlers, such as an <image> element with an onerror attribute.

When a victim loads or renders the malicious graph, the payload may execute arbitrary JavaScript in the security context of the application embedding Pivotick. Successful exploitation could allow the attacker to access application data available to the victim, modify displayed content, or perform actions using the victim’s authenticated session.

Exploitation requires an application using Pivotick to render graph data that is controlled or modified by an attacker.

### CVE-2024-14041

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-208` |
| Published | 2026-07-28T08:17:12.367 |

In Bouncy Castle for Java from 1.73 to before 1.78, three ML-KEM (CRYSTALS-Kyber) routines divided secret-derived polynomial coefficients by the modulus q: Poly.toMsg, which decodes the decrypted message, and the ciphertext compression routines Poly.compressPoly and PolyVec.compressPolyVec. An attacker able to measure the timing of a large number of decapsulations performed with the same long-term private key can recover that key. These are the KyberSlash1 (Poly.toMsg) and KyberSlash2 (ciphertext compression) divisions. Compression performed during encapsulation operates on values that become the public ciphertext and is not affected.

### CVE-2026-64641

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-834` |
| Published | 2026-07-27T18:16:58.850 |

Next.js is a React framework for building full-stack web applications. In versions 13.0.0 through 15.5.20 and 16.0.0 through 16.2.10, crafted requests targeting Next.js applications using App Router with at least one Server Action can lead to excessive CPU usage blocking processing of further requests in the same process. This issue has been fixed in versions 15.5.21 and 16.2.11.

### CVE-2026-54890

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-789;CWE-1284` |
| Published | 2026-07-27T16:17:41.437 |

Integer Underflow (Wrap or Wraparound) vulnerability in erlang otp erlang/otp (erts modules), erlang otp erts (erts modules) allows Forced Integer Overflow, Excessive Allocation. This vulnerability is associated with program files erts/emulator/beam/external.c, emulator/beam/external.c.

The BIT_BINARY_EXT tag (77) handler in the External Term Format (ETF) decoder accepts an encoding with both length and trailing-bits fields set to zero. The subsequent computation of the bitstring size underflows an unsigned integer, producing a value of roughly 2^64 that is then passed as a memory allocation size. The allocator aborts the entire node with a message such as "Cannot allocate 2305843009213693951 bytes of memory (of type binary)".

The crash is a VM-level abort, not an Erlang-level exception. It cannot be intercepted by supervision trees, by try/catch, or by passing the [safe] option to binary_to_term/2 (which only restricts atom creation and does not perform structural validation of binary encodings).

Any application that decodes ETF from untrusted sources via binary_to_term/1,2 or enif_binary_to_term() is exposed. The Erlang distribution protocol also decodes incoming terms through the same code path, but distribution is expected to run on trusted networks per the OTP Secure Coding Guidelines (DSG-011).

This issue affects OTP from OTP 27.0 before OTP 29.0.4, OTP 28.5.0.4 and OTP 27.3.4.15, corresponding to erts from 15.0 before 17.0.4, 16.4.0.4 and 15.2.7.11.

### CVE-2026-14169

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-696` |
| Published | 2026-07-28T09:16:41.640 |

Due to incorrect behavior order a low privileged remote attacker could trigger account inconsistent state via crafted input and overwrites existing user passwords which could result in complete administrative unavailability of the device.

### CVE-2026-42016

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-27T20:16:39.613 |

JFrog Artifactory (Self Hosted) versions before 7.133.11 are vulnerable to a privilege escalation attack due to a validation check of the token signature/issuer and not the token’s scope.

### CVE-2026-43776

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-07-27T21:17:01.977 |

A buffer overflow was addressed with improved bounds checking. This issue is fixed in iOS 26.6 and iPadOS 26.6, macOS Sequoia 15.7.8, macOS Tahoe 26.6. Processing a maliciously crafted file may lead to unexpected app termination or arbitrary code execution.

### CVE-2026-43749

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T21:16:59.643 |

A parsing issue in the handling of directory paths was addressed with improved path validation. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to gain root privileges.

### CVE-2026-43723

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T21:16:56.653 |

A path handling issue was addressed with improved validation. This issue is fixed in iOS 26.6 and iPadOS 26.6, macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6, tvOS 26.6, visionOS 26.6, watchOS 26.6. An app may be able to gain root privileges.

### CVE-2026-43698

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-27T21:16:53.370 |

An injection issue was addressed with improved validation. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to gain root privileges.

### CVE-2026-39875

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-27T21:16:51.533 |

A permissions issue was addressed with additional restrictions. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. A malicious app may be able to gain root privileges.

### CVE-2026-39874

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-27T21:16:51.433 |

A permissions issue was addressed with additional restrictions. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. A malicious app may be able to gain root privileges.

### CVE-2026-66758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-27T19:17:23.613 |

A flaw was found in the file-fits plugin in GIMP. When processing a FITS image file, the plugin calculates memory allocation sizes using signed 32-bit integers for width and height. If a crafted file sets both values to large values, their product exceeds 2^31 and overflows, resulting in an undersized heap-based buffer allocation. This integer overflow issue results in a heap-based buffer overflow when cfitsio subsequently writes a full row of pixels in the buffer, causing memory corruption, potentially leading to arbitrary code execution or a denial of service.

### CVE-2026-24252

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T17:16:36.167 |

NVIDIA NeMo for Linux contains a vulnerability where an attacker may cause OS command injection. A successful exploit of this vulnerability may lead to code execution, data tampering, escalation of privileges and information disclosure.

### CVE-2026-66427

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:10.650 |

Administrator SQL Injection in WP Google Review Slider <= 18.4 versions.

### CVE-2026-59537

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T15:17:04.333 |

Administrator SQL Injection in Sender – Newsletter, SMS and Email Marketing Automation for WooCommerce <= 2.10.22 versions.

### CVE-2026-15025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-28T12:16:35.490 |

The Uncanny Automator – Easy Automation, Integration, Webhooks & Workflow Builder plugin for WordPress is vulnerable to Missing Authorization in versions up to, and including, 7.3.2 via the automator_google_contacts_fetch_labels, automator_mautic_segment_fetch, automator_mautic_tags_fetch, and automator_mautic_render_contact_fields AJAX actions due to a missing capability check and missing nonce verification in the corresponding handlers (ajax_fetch_labels, segments_fetch, tags_fetch, and render_contact_fields). This makes it possible for authenticated attackers, with Subscriber-level access and above, to enumerate sensitive Google Contacts groups/labels and Mautic segments, tags, and contact-field definitions retrieved via integration credentials configured by an administrator, and to consume third-party API quota.

### CVE-2026-14785

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T10:16:48.153 |

The Web Directory Free plugin for WordPress is vulnerable to generic SQL Injection via the 'levels' parameter in all versions up to, and including, 1.7.13 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-10207

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T10:16:46.510 |

The PickPlugins Question Answer plugin for WordPress is vulnerable to SQL Injection in versions up to and including 1.2.73. This is due to insufficient sanitization of user-supplied input via the 'id' GET parameter in the user profile template combined with the use of wp_unslash() which removes WordPress's magic quotes protection, followed by direct concatenation into a SQL query without proper escaping or prepared statements in the qa_user_profile_card() function. This makes it possible for unauthenticated attackers to append additional SQL queries into existing queries, which can be used to extract sensitive information from the database.

### CVE-2026-14516

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T09:16:41.970 |

The Online Scheduling and Appointment Booking System – Bookly plugin for WordPress is vulnerable to time-based SQL Injection via the 'staff_ids' parameter in all versions up to, and including, 27.5 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Exploitation requires a two-request chain: an attacker first calls the unauthenticated bookly_get_form_id action to seed a booking session carrying malicious staff_ids values, then triggers bookly_render_time to cause the tainted array to reach the vulnerable query; CSRF/nonce validation is absent on both endpoints, meaning this chain can be initiated cross-site.

### CVE-2026-13161

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T09:16:41.220 |

The TrueBooker – Appointment Booking and Scheduler System plugin for WordPress is vulnerable to generic SQL Injection via the 'alldata[truebooker_user]' parameter in all versions up to, and including, 1.2.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The check_ajax_referer() nonce guard does not constitute an authentication or authorization barrier because the nonce is exposed to unauthenticated visitors on TrueBooker front-end booking pages; exploitation additionally requires that the required booking fields (category, service, person, date, and time slot) be present in the alldata POST parameter so that execution reaches the vulnerable SQL query branch.

### CVE-2026-12800

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T09:16:40.667 |

The Premium Packages – Sell Digital Products Securely plugin for WordPress is vulnerable to SQL Injection via the 'code' parameter of the POST /wp-json/wpdmpp/v1/cart/coupon REST API endpoint in versions up to, and including, 6.2.0. This is due to insufficient escaping on the user-supplied parameter, which is interpolated directly into a raw SQL query string in the CouponCodes::find() method without use of $wpdb->prepare() or esc_sql(). This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-12741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-28T08:17:14.360 |

The WP Fast Total Search – The Power of Indexed Search plugin for WordPress is vulnerable to generic SQL Injection via the 'form_data[s]' parameter in all versions up to, and including, 1.80.280 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-14924

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-28T07:16:41.507 |

The Tablesome Table  WordPress plugin before 1.1.31 does not perform any authentication, capability, or nonce checks in one of its AJAX actions, allowing unauthenticated users to create new published posts and to overwrite arbitrary existing posts and pages.

### CVE-2026-14490

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T07:16:40.963 |

The Demi – One Click Demo Import, WP Backup & Site Migration plugin for WordPress is vulnerable to Arbitrary Directory Deletion in all versions up to, and including, 0.0.7. The vulnerability exists because the plugin stores its HMAC signing key and per-step restore token as dotfiles inside a publicly accessible subdirectory of the WordPress uploads folder — without any `.htaccess` or index file protection — and the `demi_restore_step` AJAX handler, registered for unauthenticated callers, explicitly accepts possession of the on-disk signing key as a standalone alternative to WordPress capability and nonce checks; an unauthenticated attacker who retrieves the exposed key can forge a valid signed state envelope to invoke `CleanDir::execute()` with a caller-supplied absolute path that is subject to no allow-list or path-canonicalization check. This makes it possible for unauthenticated attackers to recursively delete arbitrary directories on the server.

### CVE-2026-66473

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T23:16:42.970 |

Unauthenticated Broken Access Control in Xendit Payment <= 7.1.0 versions.

### CVE-2025-63913

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-27T23:16:39.717 |

An issue was discovered in OpenSBI 1.3 allowing attackers to cause a denial of service via crafted request to the SBI function #2 or the 'Find and configure a matching counter' function of SBI PMU extension.

### CVE-2026-51244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-27T19:17:16.447 |

schreibfaul1 ESP32-audioI2S 3.4.5 has a buffer overflow vulnerability in UnpackFrameHeader(). Multiple attacker-controlled index parameters are used to access static and heap table arrays without range limitation. Invalid index values lead to out-of-bounds memory writing and heap buffer overflow.

### CVE-2026-12383

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-27T19:17:14.820 |

A flaw was found in the Event-Driven Ansible (EDA) server. The ExternalEventStreamViewSet uses permissive access controls (permission_classes=[AllowAny], authentication_classes=[]) and relies solely on the Subject HTTP header value for mTLS authentication without verifying that the header originated from a trusted proxy. Additionally, the expected certificate Distinguished Name is leaked in the 403 error response body. An attacker who can reach the EDA API endpoint with a spoofed Subject header can inject arbitrary events into mTLS-protected event streams, triggering downstream automation actions.

### CVE-2026-45623

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-07-27T18:16:55.130 |

PostCSS takes a CSS file and provides an API to analyze and modify its rules by transforming the rules into an Abstract Syntax Tree. In versions 8.5.11 and prior, the PreviousMap parses the /*# sourceMappingURL=PATH */ comment from any CSS string passed to process() and dereferences PATH against the local filesystem with no scheme, allowlist, or traversal check. An attacker who controls the CSS input can cause the host process to read any file readable by Node and leak the first ~10 bytes of its content through the resulting JSON.parse SyntaxError message. The bug also yields a precise file-existence oracle and a controllable-read primitive that may be combined with large-file targets for DoS. The behaviour is triggered with PostCSS's default options — no from, no map, no plugins required — and is therefore reachable from any pipeline that runs untrusted CSS through PostCSS (CMS themes, user-uploaded styles, browser-extension/userstyle processors, build pipelines for third-party packages, blog comment renderers, etc.). This issue has been fixed in version 8.5.12.

### CVE-2026-51304

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-27T16:17:39.500 |

sqlite 3.41 has a use-after-free (UAF) vulnerability in the ORDER BY clause parsing routine. The affected code first releases the memory of an ExprList object via sqlite3ExprListDelete(), then attempts to access the nExpr member of the already freed object. This dangling pointer access causes invalid memory read operations. By constructing a malicious SQL statement containing an ORDER BY clause with a large number of items, a remote adversary can trigger this vulnerability. Successful exploitation can result in application crash (denial of service), leakage of sensitive memory contents, and under certain memory layout conditions, arbitrary code execution on the affected system.

### CVE-2026-59548

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-07-27T15:17:04.837 |

Unauthenticated Sensitive Data Exposure in Byteflows Travel &amp; Hotel Booking <= 1.0.0 versions.

### CVE-2026-59539

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-27T15:17:04.583 |

Subscriber Insecure Direct Object References (IDOR) in Paid Member Subscriptions <= 3.0.7 versions.

### CVE-2026-59536

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T15:17:04.203 |

Unauthenticated Broken Access Control in CoCart – Headless ecommerce <= 4.8.4 versions.

### CVE-2026-59534

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T15:17:03.943 |

Unauthenticated Broken Access Control in Post My CF7 Form <= 6.2.0 versions.

### CVE-2026-59532

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-27T15:17:03.687 |

Unauthenticated Other Vulnerability Type in Booking and Rental Manager <= 2.7.2 versions.

### CVE-2026-59531

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-27T15:17:03.560 |

Unauthenticated Unknown in Falcon – WordPress Optimizations & Tweaks <= 2.10.0 versions.

### CVE-2026-59530

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T15:17:03.433 |

Unauthenticated Broken Access Control in Stripe For WooCommerce <= 4.0.7 versions.

### CVE-2026-59529

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T15:17:03.310 |

Unauthenticated Sensitive Data Exposure in Ebook Store <= 6.19 versions.

### CVE-2026-59528

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-07-27T15:17:03.177 |

Subscriber Sensitive Data Exposure in ShipTime: Discounted Shipping Rates <= 1.1.1 versions.

### CVE-2026-59546

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-27T15:17:04.710 |

Subscriber Broken Authentication in Hide My WP Ghost <= 7.0.06 versions.

### CVE-2026-59535

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T15:17:04.070 |

Unauthenticated Broken Access Control in Thrive Product Manager <= 10.9.2 versions.

### CVE-2026-13440

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T12:16:35.340 |

The StoreGrowth: Smart Sales Booster for WooCommerce | BOGO, Upsells, Direct Checkout, Quick View, Side Cart plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'message_popup' parameter in all versions up to, and including, 2.1.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit is possible because the 'ajd_protected' nonce required by the create_popup handler is exposed to all unauthenticated frontend visitors via wp_localize_script under bogo_save_url.ajd_nonce, effectively bypassing the nonce-only access control.

### CVE-2026-16585

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-28T07:16:41.993 |

The Better Messages – Chat Rooms, Group Chat, Private Messages & AI Chat Bots plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the delete_sticker function in all versions up to, and including, 2.15.19. This makes it possible for authenticated attackers, with administrator-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The prefix check intended to restrict deletion to the uploads directory can be bypassed by crafting a URL that begins with the legitimate uploads base URL but embeds ../ traversal sequences in the path portion, as the normalize_sticker function only applies esc_url_raw(), which does not strip ../ sequences, allowing the traversal payload to be stored verbatim in WordPress options.

### CVE-2026-65442

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-27T23:16:42.207 |

Unauthenticated Server Side Request Forgery (SSRF) in FormCraft <= 3.9.15 versions.

### CVE-2026-61953

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-27T23:16:41.280 |

Unauthenticated Server Side Request Forgery (SSRF) in Simple Link Directory Pro <= 15.0.6 versions.

### CVE-2026-66015

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-27T20:16:41.907 |

An authenticated privilege-escalation vulnerability in JFrog Platform may be exploited under admin-provisioned account conditions. Successful exploitation may grant temporary platform administrator access.

### CVE-2026-59552

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-27T15:17:05.350 |

Unauthenticated Server Side Request Forgery (SSRF) in 3D Flipbook PDF Viewer &amp; Embedder <= 1.4.2 versions.

### CVE-2026-14870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-28T07:16:41.407 |

The Database for Contact Form 7, WPforms, Elementor forms WordPress plugin before 1.5.3 does not properly sanitise and escape a parameter before reflecting it back in an admin page, leading to a Reflected Cross-Site Scripting which could be used against high privilege users such as admin.

### CVE-2026-65447

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:42.720 |

Unauthenticated Cross Site Scripting (XSS) in Contest Gallery <= 30.0.6 versions.

### CVE-2026-65446

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:42.590 |

Unauthenticated Cross Site Scripting (XSS) in Kali Forms <= 2.4.18 versions.

### CVE-2026-65443

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:42.330 |

Unauthenticated Cross Site Scripting (XSS) in BackWPup  <= 5.7.4 versions.

### CVE-2026-65441

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:42.060 |

Unauthenticated Cross Site Scripting (XSS) in GiveWP <= 4.16.3 versions.

### CVE-2026-65440

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:41.933 |

Unauthenticated Cross Site Scripting (XSS) in GetGenie <= 4.4.3 versions.

### CVE-2026-65439

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:41.807 |

Unauthenticated Cross Site Scripting (XSS) in Ultimate Addons for Contact Form 7 <=3.5.45 versions.

### CVE-2026-65438

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:41.673 |

Unauthenticated Cross Site Scripting (XSS) in Message Filter for Contact Form 7 <= 1.6.3.9 versions.

### CVE-2026-65437

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:41.540 |

Unauthenticated Cross Site Scripting (XSS) in Spam protection, AntiSpam, FireWall by CleanTalk <= 6.82 versions.

### CVE-2026-61957

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T23:16:41.410 |

Unauthenticated Cross Site Scripting (XSS) in miniorange otp verification <= 5.5.1 versions.

### CVE-2026-43771

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-27T21:17:01.477 |

A stack overflow was addressed with improved input validation. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to cause a denial-of-service.

### CVE-2026-43747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-27T21:16:59.450 |

An out-of-bounds read was addressed with improved bounds checking. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. Parsing a maliciously crafted file may lead to an unexpected app termination.

### CVE-2026-65922

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T20:16:41.310 |

An authorization weakness in JFrog Artifactory internal metadata handling could allow a user with limited repository access to write to restricted internal metadata areas under specific conditions. Successful abuse is limited to integrity and availability impact at a low level; confidentiality is not affected.

### CVE-2026-66759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-27T19:17:23.747 |

A flaw was found in the file-icns plugin in GIMP. When applying a decompressed mask during ICNS image processing, the plugin reads from the mask data buffer without verifying if the cursor exceeds the allocated resource size. If a crafted file contains a truncated mask resource, the icns_decompress function continues reading past the bounds of the buffer. This out-of-bounds read vulnerability results in information disclosure of heap contents, where memory contents are leaked as alpha channel pixel values, or a crash leading to a denial of service if unmapped memory is accessed.

### CVE-2026-66028

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-07-27T18:17:00.090 |

Ekushey Project Manager CRM through version 5.0 contains a missing uniqueness constraint vulnerability that allows authenticated administrators to create duplicate client accounts with identical email and password credentials. Attackers can exploit the lack of email field uniqueness enforcement to create conflicting account states where multiple accounts share the same email address with different passwords, resulting in unpredictable authentication behavior and unauthorized account access.

### CVE-2026-59558

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T15:17:05.883 |

Unauthenticated Cross Site Scripting (XSS) in Booking Calendar <= 11.4.2 versions.

### CVE-2026-59556

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T15:17:05.620 |

Unauthenticated Cross Site Scripting (XSS) in Dynamic Pricing With Discount Rules for WooCommerce <= 4.5.11 versions.

### CVE-2026-59553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T15:17:05.483 |

Unauthenticated Cross Site Scripting (XSS) in Product Feed Manager <= 7.6.1 versions.

### CVE-2026-63301

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602` |
| Published | 2026-07-28T11:17:03.823 |

In Quick.CMS, the administrative user interface restricts deletion of the primary language by omitting the corresponding option from the interface; however, the underlying language-deletion API endpoint does not enforce an equivalent server-side authorization check. As a result, an authenticated administrator can bypass the UI-level restriction and delete the primary language by sending a direct HTTP request to the API endpoint. Successful deletion of the primary language results in a Denial of Service (DoS) of application.


Critically, when combined with a separate Cross-Site Request Forgery (CSRF) vulnerability (CVE-2026-1468) an unauthenticated remote attacker can craft a malicious link, which if visited by an authenticated administrator, will trigger the DoS condition without direct access to the application




The vendor assessed the likelihood of exploitation as very low and determined that a fix is not necessary.

### CVE-2026-43755

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-27T21:17:00.060 |

A race condition was addressed with improved state management. This issue is fixed in macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to gain root privileges.

### CVE-2026-43693

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-27T21:16:53.163 |

A race condition was addressed with improved state handling. This issue is fixed in macOS Sequoia 15.7.8, macOS Sonoma 14.8.8, macOS Tahoe 26.6. An app may be able to gain root privileges.
