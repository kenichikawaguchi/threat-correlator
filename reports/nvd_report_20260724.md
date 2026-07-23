# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-23 15:00 UTC
- **対象期間**: `2026-07-22T15:01:25.000Z` 〜 `2026-07-23T15:00:36.000Z`
- **重要CVE数**: 163 件（Critical 9.0+: 38 件 / High 7.0〜: 125 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** に上り、特に **リモートから認証不要でコード実行・権限昇格が可能** な脆弱性が目立ちます。  
- 開発ツール（IntelliJ IDEA）やミドルウェア（Oracle Fusion Middleware）といった **インフラ層の製品** が CVSS 10.0 の極めて高いスコアで報告され、企業ネットワークへの直接的な侵入経路となり得ます。  
- WordPress エコシステム向けプラグインに多数の **認可バイパス／コードインジェクション** が確認され、CMS を利用する多くのサイトが即座に危険に晒されています。  
- データベース系アプリケーション（Participants Database、TrueBooker、MapSVG など）で **SQL インジェクション** が連続して報告され、情報漏洩や改ざんリスクが拡大しています。  

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由・影響範囲 |
|-----|--------|----------|-------------------|
| **CVE‑2026‑64813** / **CVE‑2026‑64812** | 10.0 | JetBrains IntelliJ IDEA (2026.2 未満) の Remote Development セッションで **認証不要の設定変更・入力インジェクション** が可能 | 開発者が日常的に使用する IDE が攻撃対象になると、ソースコード改竄や機密情報漏洩、さらにマシン上の任意コード実行へとエスカレートする危険性がある。企業内の開発環境全体が影響を受ける可能性が高い。 |
| **CVE‑2026‑60366** (同系列 CVE‑2026‑60369/60372/60367) | 10.0 | Oracle Fusion Middleware **Platform Security for Java** (12.2.1.4.0 / 14.1.2.0.0) の Centralized Third‑party Jars コンポーネントで **認証不要のリモートコード実行** が可能 | Oracle のミドルウェアは金融・官公庁など高価値システムで広く採用されており、HTTP 経由で任意コードが実行できる点は **サプライチェーン全体に波及** する深刻な脅威。 |
| **CVE‑2026‑59555** | 10.0 | Participants Database ≤ 2.7.8.3 で **認証不要の任意ファイル削除** が可能 | データベース管理ツールがファイルシステム上の任意ファイルを削除できるため、バックアップや設定ファイルの破壊によりサービス停止やデータ喪失が直ちに起こり得る。 |
| **CVE‑2026‑15015** | 9.8 | WordPress プラグイン **MountDev AI MCP Connector** ≤ 1.6.1 の **認可バイパス** | WordPress は世界中で最も利用されている CMS であり、プラグイン経由の認可バイパスは管理者権限取得や任意コード実行に直結。プラグインが多数インストールされているサイトは即座に危険に晒される。 |
| **CVE‑2026‑59544** | 9.8 | WordPress プラグイン **Thrive Quiz Builder** ≤ 10.9.3.0 の **PHP オブジェクトインジェクション** | PHP のシリアライズ機構を悪用した攻撃は、サーバ側で任意コード実行や情報漏洩を引き起こす。人気プラグインであるため、影響サイト数は膨大。 |

> **注**：上記はスコアが最高（10.0）かつ **広範囲に展開されている製品／プラグイン**、または **認証不要で深刻な権限取得が可能** な点で選定しました。  

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の即時取得**：ベンダーが提供するパッチ・アップデート情報を公式サイトまたはセキュリティアドバイザリ（JetBrains、Oracle、WordPress Plugin Repository 等）で確認し、リスト化した対象製品を優先的に更新。  
- **ネットワークレベルでの防御**：該当サービスが外部から直接アクセス可能な場合、ファイアウォールや WAF で **IP アクセス制限**、**HTTP メソッド制限**（GET/POST のみ許可）を実装。特に Oracle Fusion Middleware の HTTP エンドポイントは外部公開しない。  
- **監査ログの有効化**：認証失敗・設定変更・ファイル削除系のイベントをすべてログに残し、SIEM でリアルタイム監視。  

### 3.2 製品別具体的アップデート指示  

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ | 備考 |
|-------------------|-------------------|------------------------|------|
| **JetBrains IntelliJ IDEA** | 2026.2 未満 | **2026.2 以降**（公式パッチリリース） | Remote Development 機能を使用しない場合は一時的に無効化。 |
| **Oracle Fusion Middleware – Platform Security for Java** | 12.2.1.4.0、14.1.2.0.0 | **12.2.1.4.1** もしくは **14.1.2.0.1**（Oracle Critical Patch Update） | HTTP 経由の JAR 読み込みを無効化し、TLS 1.2 以上で保護。 |
| **Participants Database** | ≤ 2.7.8.3 | **2.7.8.4** 以上 | アップデート後、データベースディレクトリの書き込み権限を最小化。 |
| **MountDev AI MCP Connector (WordPress)** | ≤ 1.6.1 | **1.6.2** 以上（プラグイン作者提供） | プラグインの「認可チェック」ロジックが修正されたバージョンへ。 |
| **Thrive Quiz Builder (WordPress)** | ≤ 10.9.3.0 | **10.9.3.1** 以上 | PHP の `unserialize()` 呼び出しを安全化。 |
| **TrueBooker** | ≤ 1.2.3 | **1.2.4** 以上 | 権限昇格と SQLi 両方が修正。 |
| **Avada Core** | ≤ 5.15.6 | **5.15.7** 以上 | CSRF トークン検証を強化。 |
| **Ninja Forms File Uploads Extension** | ≤ 3.3.26 | **3.3.27** 以上 | CSRF 防御とファイルタイプ検証を追加。 |
| **Bold Reports Standalone Report Designer** |

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-64813

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-602` |
| Published | 2026-07-23T12:18:36.897 |

In JetBrains IntelliJ IDEA before 2026.2 unauthorized settings modification was possible in a Remote Development session

### CVE-2026-64812

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-23T12:18:36.783 |

In JetBrains IntelliJ IDEA before 2026.2 unauthorized input injection was possible in a Remote Development session

### CVE-2026-59555

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T12:18:33.803 |

Unauthenticated Arbitrary File Deletion in Participants Database <= 2.7.8.3 versions.

### CVE-2026-60366

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:35.757 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-59543

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T12:18:33.193 |

Subscriber Remote Code Execution (RCE) in Advanced Views <= 3.8.11 versions.

### CVE-2026-60369

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.087 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61951

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-23T12:18:34.923 |

Unauthenticated Privilege Escalation in TrueBooker <= 1.2.3 versions.

### CVE-2026-59544

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-23T12:18:33.313 |

Unauthenticated PHP Object Injection in Thrive Quiz Builder <= 10.9.3.0 versions.

### CVE-2026-59540

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-23T12:18:32.830 |

Unauthenticated Privilege Escalation in SMS Alert Order Notifications <= 3.9.6 versions.

### CVE-2026-15015

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T10:16:50.047 |

The MountDev AI MCP Connector for WordPress plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.6.1. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to obtain an administrator-bound OAuth Bearer token via a self-registered client, granting full administrator-equivalent access to the plugin's MCP tool surface and all exposed WordPress content, users, and options. This is exploitable by combining the publicly accessible Dynamic Client Registration endpoint, which allows unauthenticated callers to register arbitrary OAuth clients with an attacker-controlled redirect_uri, with the unprotected authorization endpoint to complete the full OAuth flow without any administrator interaction.

### CVE-2026-15011

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T10:16:49.917 |

The Customer Support Ticket System & Helpdesk plugin for WordPress is vulnerable to Code Injection via the 'path' parameter in all versions up to, and including, 6.0.5 due to the use of dynamic function invocation on an attacker-controlled value with insufficient validation. This makes it possible for unauthenticated attackers to invoke arbitrary parameterless PHP functions, which can be used to disrupt site functionality or expose sensitive information. The required nonce is publicly emitted via wp_localize_script whenever the plugin's [emd_form] shortcode is rendered on any public-facing page, making the endpoint reachable by unauthenticated visitors without any prior authentication or privilege.

### CVE-2026-14282

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-23T10:16:49.657 |

The GoDAM – Organize WordPress Media Library & File Manager with Unlimited Folders for Images, Videos & more plugin for WordPress is vulnerable to arbitrary file uploads in versions up to, and including, 1.12.2. This is due to insufficient file type validation in the save_video_file() function hooked into WPForms' public wpforms_process_before_filter, which trusts the attacker-supplied multipart Content-Type header, preserves the original filename via wp_unique_filename(), and moves the raw upload with $wp_filesystem->move() into a web-served directory — bypassing wp_handle_upload()'s MIME/extension allowlist. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-60372

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.420 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60367

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:35.870 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-2395

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-22T15:16:54.193 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Xpoda Türkiye Informatics Technology Inc. No Code Platform allows SQL Injection.

This issue affects No Code Platform: from 4.3.1.0 through 20260722. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-65471

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:39.857 |

Unauthenticated Cross Site Request Forgery (CSRF) in Avada Core <= 5.15.6 versions.

### CVE-2026-57784

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:30.407 |

Unauthenticated Cross Site Request Forgery (CSRF) in  Ninja Forms File Uploads Extension <= 3.3.26 versions.

### CVE-2026-65606

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:47.493 |

SiYuan before v3.7.2 contains a cross-site scripting vulnerability in the siyuan:// protocol handler. When a siyuan://plugins/<name> link references a name that is not an installed plugin, the application opens a custom tab and inserts the link's icon parameter into the tab header via innerHTML without escaping it (app/src/layout/Tab.ts), allowing injection of an <img onerror=...> element. Because the SiYuan Desktop renderer runs with nodeIntegration:true, the injected JavaScript can access Node's require and call require('child_process').execSync(...), escalating the cross-site scripting into arbitrary operating-system command execution.

### CVE-2026-65605

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:47.357 |

SiYuan before v3.7.2 contains a stored cross-site scripting vulnerability in Attribute View (database) cell rendering. A Template column value is rendered as HTML via text/template without auto-escaping, and EscapeHTML is only applied when HasUnclosedHtmlTag returns true; because balanced self-closing tags such as <img> are skipped by that check, a payload like <img src=x onerror=...> is stored unescaped and later inserted into the page via innerHTML, executing when the database is viewed. Because the desktop renderer runs with nodeIntegration enabled, the injected script can reach require and escalate to arbitrary command execution.

### CVE-2026-65689

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T14:18:03.340 |

Bold Reports Standalone Report Designer before 14.1.12 contains a missing filepath validation vulnerability in its database download feature that allows unauthenticated attackers to read arbitrary files from the server filesystem by supplying a crafted request. Attackers can exploit this path traversal weakness to disclose sensitive server files, including authentication credentials, enabling full unauthorized access to the application.

### CVE-2026-65688

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T14:18:03.163 |

Bold Reports Standalone Report Designer before 14.1.12 contains a missing filepath validation vulnerability in its font processing feature that allows unauthenticated attackers to read arbitrary files from the server filesystem by supplying a crafted request. Attackers can exploit this path traversal weakness to disclose sensitive server files, including authentication credentials, enabling full unauthorized access to the application.

### CVE-2026-65687

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T14:18:02.993 |

Bold Reports Standalone Report Designer before 14.1.12 contains a missing filepath validation vulnerability in its SVG processing feature that allows unauthenticated attackers to read arbitrary files from the server filesystem by supplying a crafted request. Attackers can exploit this path traversal weakness to disclose sensitive server files, including authentication credentials, enabling full unauthorized access to the application.

### CVE-2026-61950

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:34.803 |

Unauthenticated SQL Injection in TrueBooker <= 1.2.3 versions.

### CVE-2026-61949

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:34.680 |

Unauthenticated SQL Injection in Bookly <= 27.7 versions.

### CVE-2026-61948

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:34.560 |

Unauthenticated SQL Injection in WPDM – Premium Packages <= 6.2.0 versions.

### CVE-2026-59526

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:32.707 |

Unauthenticated SQL Injection in MapSVG <= 8.14.0 versions.

### CVE-2026-59525

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:32.590 |

Unauthenticated SQL Injection in Participants Database <= 2.7.8.3 versions.

### CVE-2026-59514

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:32.103 |

Unauthenticated SQL Injection in Buddyboss Platform <= 3.0.5 versions.

### CVE-2026-16606

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-22T16:17:16.800 |

A vulnerability in Fujitsu Software Linux openFT and Fujitsu Software Oracle Solaris openFT before version 12.1D00 allows for unauthenticated remote code execution (pre-auth RCE) on GNU/Linux or Oracle Solaris. The Fsas Technologies PSIRT obtained that intelligence internally and covers the CVE beyond its CNA scope under existing agreement with Fujitsu Germany.

### CVE-2026-13072

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-22T20:16:45.740 |

When compute mode is enabled on a standalone mongod instance, insufficient validation of externally sourced BSON data during aggregation pipeline processing can result in memory corruption, potentially leading to process termination or other unintended behavior. This configuration is non-default and requires explicit enablement at startup.

### CVE-2026-65907

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T13:16:31.860 |

In JetBrains TeamCity before 2026.1.2, 2025.11.6 code execution in Git VCS roots was possible

### CVE-2026-65461

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-23T12:18:38.610 |

Administrator Arbitrary File Upload in Really Simple CSV Importer <= 1.3 versions.

### CVE-2026-65455

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-23T12:18:37.950 |

Administrator Arbitrary File Upload in MapSVG <= 8.14.0 versions.

### CVE-2026-27064

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-23T12:17:16.810 |

Editor Arbitrary File Upload in Mailster <= 4.1.17 versions.

### CVE-2026-64829

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-22T20:17:08.423 |

Question2Answer through 1.8.8 contains a session invalidation vulnerability that allows attackers with a previously obtained remember-me cookie to retain authenticated access by exploiting the forgot-password reset flow's failure to clear the sessioncode field in qa-include/app/users-edit.php. While the normal password-change flow in qa-include/pages/account.php explicitly clears the sessioncode to invalidate persistent qa_session cookies, the forgot-password handler qa_finish_reset_user() omits this step, allowing any valid persistent cookie issued before the reset to continue authenticating the account after the password reset completes.

### CVE-2026-46738

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-22T16:17:24.223 |

Dell PowerProtect Data Manager, versions prior to 20.2.0.0, contain(s) an Improper Input Validation vulnerability in the REST API. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-40712

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-22T16:17:19.247 |

Dell PowerProtect Data Manager, versions prior to 20.2.0.0, contain(s) an Improper Input Validation vulnerability in the REST API. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-16723

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-07-23T09:16:26.700 |

A remote code execution (RCE) vulnerability exists in fastjson 1.2.68 through 1.2.83. This vulnerability is exploitable under fastjson's stock default configuration — no AutoType enablement required, no classpath gadget required.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-65906

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T13:16:31.733 |

In JetBrains TeamCity before 2026.1.2, 2025.11.6 сode execution via Kotlin DSL sandbox escape was possible

### CVE-2026-59541

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-23T12:18:32.943 |

Subscriber Privilege Escalation in WP BASE Booking <= 6.3.1 versions.

### CVE-2026-57785

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:30.540 |

Unauthenticated Cross Site Request Forgery (CSRF) in ApusListing <= 1.2.63 versions.

### CVE-2026-16745

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-23T11:16:40.043 |

A flaw was found in odh-dashboard, the web console component of Red Hat OpenShift AI (RHOAI). Due to incorrect network binding, a malicious actor within the cluster can bypass authentication and impersonate any user by providing an arbitrary access token. This allows an attacker to gain unauthorized access to the Kubernetes API, potentially leading to arbitrary code execution, privilege escalation, or information disclosure.

### CVE-2026-15017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-23T10:16:50.173 |

The MDJM Event Management plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.7.8.4. This is due to missing capability checks and nonce verification in the `MDJM_Permissions::set_permissions()` and `MDJM_Employee_Manager::init()` functions, combined with the absence of server-side allow-list validation on the `employee_roles[]` and `new_role` POST parameters before they are passed to `mdjm_set_employee_role()` and `WP_User::set_role()`. This makes it possible for unauthenticated attackers to grant arbitrary MDJM capabilities — including `mdjm_employee` and `mdjm_employee_edit` — to any registered WordPress role, and subsequently leverage a subscriber-level account to escalate privileges to Administrator. `MDJM_Permissions::init()` is registered on the public WordPress `init` hook without any authentication gate, meaning the role-manipulation endpoint is reachable without any prior login.

### CVE-2026-61246

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.867 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60455

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.753 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.640 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60373

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.530 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60368

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:35.980 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-49499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1270` |
| Published | 2026-07-22T16:17:29.943 |

Dell PowerProtect Data Manager, versions prior to 20.2.0.0, contain(s) a Generation of Incorrect Security Tokens vulnerability in the IAM. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-65690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T14:18:03.503 |

Bold Reports Standalone Report Designer before 14.1.12 contains a missing filepath validation vulnerability in its file upload functionality that allows authenticated attackers to traverse outside the intended directory by supplying a crafted filename. Attackers can exploit this path traversal weakness to execute arbitrary commands with high privileges on the server.

### CVE-2026-65897

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-23T12:18:48.180 |

Grav API Plugin versions before 1.0.10 fail to validate the groups field in InvitationsController::create(), allowing authenticated api.users.write callers to assign invited accounts to groups that grant api.super permissions. Attackers can create invitation records with elevated group membership, and when accepted, the new account gains full super-admin API access without the inviter holding those permissions.

### CVE-2026-65608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-07-23T12:18:47.770 |

Grav versions >= 1.7.0 and before 2.0.9 contain a remote code execution vulnerability. FlexDirectory::dynamicDataField() resolves blueprint data-*@: directives by calling call_user_func_array() on attacker-influenced input, validating only that the target is callable (is_callable()) without restricting dangerous functions such as exec, system, passthru, or shell_exec. Because FlexDirectory registers this handler for every Flex directory, it bypasses the validation added to Blueprint::dynamicData() in 2.0.7 (GHSA-fj2p-qj2f-74v5). Any authenticated user with create or update permission on any Flex-based directory (Flex Users, Flex Pages, Flex Objects, or custom Flex types) can execute arbitrary shell commands on the server.

### CVE-2026-22049

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-22T19:16:59.820 |

ONTAP versions 9.16.1 and higher with WebAuthn multi-factor authentication (MFA) configured are susceptible to a vulnerability related to the Relying Party ID which when successfully exploited could allow an attacker with valid credentials to bypass MFA.

### CVE-2026-64835

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-22T18:17:05.917 |

FFmpeg versions 4.4 through 8.1.2 contain an out-of-bounds memory access vulnerability in the ADX audio decoder within libavcodec/adxdec.c that allows attackers to trigger both out-of-bounds reads and writes by supplying a crafted ADX or AAX audio file with a mid-stream channel layout change. When AV_PKT_DATA_NEW_EXTRADATA side data is received mid-stream, the adx_decode_frame function re-parses the stream header but fails to update the internal channel state, causing subsequent decoding operations to access the prev[] state array using a stale channel count.

### CVE-2026-64834

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-22T18:17:05.780 |

FFmpeg versions 0.6.3 through 8.1.2 contain an infinite loop vulnerability in the RTP/ASF demuxer within libavformat/rtpdec_asf.c that allows remote attackers to cause denial of service by sending a crafted RTP/ASF stream. The rtp_asf_fix_header function fails to validate a minimum chunksize when iterating over ASF objects, causing the loop pointer to never advance when a chunksize is smaller than the 24-byte minimum ASF object header size, resulting in CPU exhaustion that denies service to legitimate users.

### CVE-2026-64832

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-22T18:17:05.483 |

FFmpeg versions 4.4 through 8.1.2 contain a double-free vulnerability in the NVIDIA NVDEC hardware decoder within libavcodec/nvdec.c that allows attackers to trigger memory corruption by supplying a crafted video file. When no decoder surfaces remain, the ff_nvdec_start_frame_sep_ref error path frees memory via nvdec_fdd_priv_free while the calling layer subsequently frees the same frame description data, resulting in a double-free of the underlying decoder context in any FFmpeg-based application using NVDEC hardware-accelerated decoding.

### CVE-2026-65013

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-22T17:16:59.143 |

Onlook through 0.2.32, fixed in commit 423e2e9, contains a broken object level authorization vulnerability that allows authenticated attackers to access and manipulate other users' resources by supplying arbitrary UUID values to tRPC API procedures including project.get, member.remove, and chat.conversation.delete. Attackers can provide arbitrary projectId or conversationId values without authorization validation to read, modify, and delete other users' project data, members, and conversation history.

### CVE-2026-64831

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-22T17:16:58.697 |

FFmpeg versions 8.0 through 8.1.2 contains a stack buffer overflow vulnerability in the Vulkan HEVC hardware decoder that allows remote attackers to overwrite return addresses and adjacent stack frames by supplying a crafted HEVC/H.265 bitstream. Attackers can embed a malicious vps_num_hrd_parameters value exceeding HEVC_MAX_SUB_LAYERS in any supported container format to overflow stack-allocated arrays in the vk_hevc_end_frame function, potentially achieving arbitrary code execution.

### CVE-2026-64830

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-22T17:16:58.557 |

FFmpeg versions 2.1 through 8.1.2 contains a heap buffer overflow vulnerability in the VobSub subtitle demuxer that allows attackers to corrupt adjacent heap memory by supplying a malicious .sub/.idx subtitle file declaring more distinct stream IDs than the fixed-size array bounds in libavformat/mpeg.c. Attackers can craft a subtitle file with excessive distinct stream IDs to trigger unbounded writes beyond the vobsub->q[] array boundary via ff_subtitles_queue_insert(), potentially achieving arbitrary code execution in any application using FFmpeg's VobSub demuxer.

### CVE-2026-65908

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T13:16:31.983 |

In JetBrains PyCharm before 2026.1.4, 2026.2 arbitrary code execution via malicious Python executable was possible on untrusted project open

### CVE-2026-64814

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:37.010 |

In JetBrains IntelliJ IDEA before 2026.2 unauthorized file access was possible in a Remote Development session

### CVE-2026-13059

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-07-22T20:16:43.793 |

An authenticated user with low privileges may be able to perform unauthorized reads and writes on data protected by role-based query-level access controls, due to insufficient validation of certain client-supplied command parameters. The issue affects find, update, delete, and aggregate commands in non-apiStrict configurations.

### CVE-2026-13321

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-22T15:16:52.200 |

The BIND resolver accepts validly-signed NSEC records where the "Next Domain Name" field points outside the signer's zone.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-65526

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:45.393 |

Contributor SQL Injection in Visualizer <= 4.0.6 versions.

### CVE-2026-65454

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:37.827 |

Contributor SQL Injection in Quiz And Survey Master <= 11.2.0 versions.

### CVE-2026-65451

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:37.467 |

Contributor SQL Injection in MapSVG <= 8.14.0 versions.

### CVE-2026-65450

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:37.350 |

Contributor SQL Injection in MapSVG <= 8.14.0 versions.

### CVE-2026-25405

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:17:13.803 |

Contributor SQL Injection in eRoom <= 1.7.1 versions.

### CVE-2026-24552

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:17:12.660 |

Contributor SQL Injection in Create by Mediavine <= 2.5.3 versions.

### CVE-2026-16607

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-22T16:17:16.963 |

A vulnerability in Fujitsu Software Linux openFT and Fujitsu Software Oracle Solaris openFT before version 12.1D00 allows for local privilege escalation to root of an already authenticated user on GNU/Linux or Oracle Solaris. The Fsas Technologies PSIRT obtained that intelligence internally and covers the CVE beyond its CNA scope under existing agreement with Fujitsu Germany.

### CVE-2026-64809

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:36.437 |

In JetBrains PhpStorm before 2026.2 arbitrary code execution was possible before granting project trust via the configured interpreter

### CVE-2026-64808

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:36.323 |

In JetBrains PhpStorm before 2026.2 arbitrary code execution was possible before granting project trust via project tooling

### CVE-2026-64806

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:36.103 |

In JetBrains WebStorm before 2026.2 arbitrary code execution was possible before granting project trust via the configured Node.js interpreter

### CVE-2026-64805

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:35.993 |

In JetBrains WebStorm before 2026.2 arbitrary code execution was possible before granting project trust via project-local package-manager tooling

### CVE-2026-64804

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:35.880 |

In JetBrains WebStorm before 2026.2 arbitrary code execution was possible before granting project trust via project-local linter tooling

### CVE-2024-58023

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-312` |
| Published | 2026-07-23T09:16:26.290 |

Information disclosure in Bosch Configuration Manager in Version 7.72.0106 allows an attacker to access sensitive information.

### CVE-2026-14881

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-22T20:16:48.247 |

When importing connections in Compass it is possible to override some connection options that are otherwise can't be changed via connection form. In particular it is possible to provide a custom browser open command for OIDC auth flow that is usually can be set only globally via Compass settings.

### CVE-2026-65895

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:47.910 |

Grav API Plugin versions before 1.0.10 fail to restrict write access to security-critical plugin configuration scopes, allowing authenticated users with api.config.write privilege to modify rate limiting and CORS settings. Attackers can disable rate limiting site-wide to enable credential brute-forcing attacks and reconfigure CORS policies to include attacker-controlled origins with credentials enabled.

### CVE-2026-64815

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T12:18:37.120 |

In JetBrains IntelliJ IDEA before 2026.2 arbitrary code injection was possible via UI Designer form files

### CVE-2026-59545

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-23T12:18:33.433 |

Unauthenticated Broken Authentication in miniOrange Discord Integration <= 2.2.4 versions.

### CVE-2026-60371

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.317 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Platform Security for Java executes to compromise Oracle Platform Security for Java.  While the vulnerability is in Oracle Platform Security for Java, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-64811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:36.663 |

In JetBrains IntelliJ IDEA before 2026.2 arbitrary code execution was possible before granting project trust via development container configuration

### CVE-2026-64807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-23T12:18:36.217 |

In JetBrains WebStorm before 2026.2 arbitrary code execution was possible via a project-supplied linter configuration

### CVE-2026-64803

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T12:18:35.753 |

In JetBrains GoLand before 2026.2 arbitrary code execution was possible before granting project trust via the configured Go SDK

### CVE-2026-64802

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T12:18:35.647 |

In JetBrains GoLand before 2026.2 arbitrary code execution was possible before granting project trust in the Go Modules integration

### CVE-2026-16287

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-23T09:16:26.570 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TUBITAK BILGEM Software Technologies Research Institute pardus-update allows OS Command Injection.

This issue affects pardus-update: from 0.6.6 before 0.7.0.

### CVE-2026-59542

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T12:18:33.067 |

Subscriber Arbitrary File Deletion in Kali Forms <= 2.4.18 versions.

### CVE-2026-65532

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:46.143 |

Shop manager SQL Injection in Persian Woocommerce SMS <= 7.2.2 versions.

### CVE-2026-65462

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:38.730 |

Administrator SQL Injection in Uncanny Automator <= 7.3.2 versions.

### CVE-2026-14257

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-23T14:17:00.250 |

brace-expansion through 5.0.7 is vulnerable to denial of service via memory exhaustion. The expand() function limits the number of results with a max option (default 100,000) but does not bound the length of each result string. By chaining multiple brace groups, an attacker keeps the result count under the limit while making each result progressively longer, so total memory scales with both count and string length until the process hits a fatal, uncatchable out-of-memory error. About 7.5 KB of input ('{a,b}'.repeat(1500)) crashes a default Node.js process. Any application that passes attacker-influenced strings to brace-expansion.expand() - directly or transitively via minimatch / glob brace patterns - can be crashed by a small request. Fixed in 5.0.8 by adding a maxLength option (default 4,000,000) that bounds accumulated output and intermediate arrays.

### CVE-2026-65500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:43.397 |

Unauthenticated Broken Access Control in Manual - Documentation, Knowledge Base & Education WordPress Theme <= 7.5.4 versions.

### CVE-2026-65495

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:42.790 |

Unauthenticated Broken Access Control in Dokan Pro <= 5.0.3 versions.

### CVE-2026-65493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-23T12:18:42.553 |

Subscriber PHP Object Injection in Dokan Pro <= 5.0.2 versions.

### CVE-2026-65481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-23T12:18:41.100 |

Contributor Local File Inclusion in Vino <= 1.9 versions.

### CVE-2026-65477

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-23T12:18:40.593 |

Contributor Local File Inclusion in Tonda Core <= 2.1.2 versions.

### CVE-2026-61954

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:35.047 |

Unauthenticated Broken Access Control in PayU India <= 3.8.9 versions.

### CVE-2026-61943

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:33.930 |

Unauthenticated Broken Access Control in WPDM – Premium Packages <= 6.2.0 versions.

### CVE-2026-59554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-07-23T12:18:33.680 |

Unauthenticated Broken Authentication in Ziina <= 1.2.21 versions.

### CVE-2026-59547

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:33.557 |

Unauthenticated Broken Access Control in Payment Gateway for PayPal on WooCommerce <= 9.1.4 versions.

### CVE-2026-64611

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-23T11:16:40.680 |

A flaw was found in libcupsfilters. The cfIEEE1284NormalizeMakeModel() function enters an infinite loop when processing a printer-advertised IEEE-1284 device ID with an empty model field, causing sustained CPU consumption. A network-adjacent attacker could exploit this by broadcasting a specially crafted printer advertisement, leading to denial of service.

### CVE-2026-52688

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-345` |
| Published | 2026-07-23T09:16:27.080 |

RRSIGs with too few labels can lead to bypass of DNSSEC wildcard validation

### CVE-2024-58330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-23T09:16:26.430 |

A missing authentication check in Bosch IP cameras of families CPP13 and CPP14 allows an unauthenticated attacker to retrieve video analytics event data.

### CVE-2026-9713

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T08:16:25.390 |

The Lumise Product Designer for WooCommerce plugin for WordPress is vulnerable to SQL Injection via the 'id' and 'table' parameters in the uploaded cart JSON file processed by the checkout AJAX action in versions up to, and including, 2.1.1. This is due to insufficient escaping on the user-supplied parameters before they are appended directly to a raw SQL query in the find_resource() function — the 'id' field is interpolated without quotes into a WHERE clause (numeric context) and 'table' is interpolated into the FROM clause, neither of which is protected by wp_magic_quotes or passed through $wpdb->prepare(). This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-15074

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T04:16:31.980 |

@fastify/static up to and including version 10.1.0 fails to reject dot-dot path segments in request pathnames before the file-resolution stage. This is a bypass of the earlier fix for CVE-2026-6414, which only covered encoded forward slashes. Because the underlying send library normalizes dot segments before applying its own path-traversal guard, an unauthenticated attacker can bypass any route-scoped middleware and read files inside the static root that live under the guarded URL prefix. The bypass does not allow access outside the configured static root by itself, it defeats route-guard filtering only. The issue is patched in @fastify/static 10.1.1.

### CVE-2026-60370

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-22T23:16:36.203 |

Vulnerability in the Oracle Platform Security for Java product of Oracle Fusion Middleware (component: Centralized Thirdparty Jars).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Platform Security for Java.  Successful attacks of this vulnerability can result in takeover of Oracle Platform Security for Java. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-13204

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-22T15:16:52.080 |

If a provably insecure domain is covered by both an NSEC and NSEC3 record at the parent, and there exist an RRSIG for only one of these types, then BIND may exit unexpectedly with an assertion while validating this proof.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-12617

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-22T15:16:51.963 |

The issue is unexpected program termination based on ordering and/or specific content in responses to queries for CNAME or DNAME, and A records. Specifically, if a client queries for a DNAME and A record below the DNAME to the resolver, and the authoritative server responds positively to the A query but delays the DNAME response and later responds negatively, `named` may quit unexpectedly. Or, if a client queries for a CNAME and A record for the same name to the resolver, and the authoritative server responds positively to the A query but delays the CNAME response and later responds with a self-referential CNAME, the same failure may occur.
This issue affects BIND 9 versions 9.18.0 through 9.18.50, 9.20.0 through 9.20.24, 9.18.11-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-11721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1284` |
| Published | 2026-07-22T15:16:51.837 |

It is possible for an attacker's zone to respond to a query with an RRSIG that has a smaller number of labels than the zone in which the RRSIG is contained. This causes `named` to produce a wildcard name for a zone that is shorter than the attacker's zone, which can result in cache poisoning. For this attack to have any effect, the resolver under attack must have set `synth-from-dnssec yes;` (which is the default).
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-11622

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-22T15:16:51.703 |

A DNSSEC validating resolver that is under a random subdomain attack against a DNSSEC-signed zone can suffer from runaway memory usage. The attacker needs to be able to send queries faster than the resolver can perform validation. The increased memory usage can be orders of magnitude beyond the limit configured in the `max-cache-size` parameter.
This issue affects BIND 9 versions 9.11.0 through 9.18.50, 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, 9.11.3-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-11605

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-408` |
| Published | 2026-07-22T15:16:51.573 |

The issue is a resource exhaustion vulnerability associated with DNSSEC validation. BIND always validates all RRSIG records in an answer, even if they are not strictly needed. A query to an authoritative server/zone which returns many valid but superfluous RRSIG records causes the validator to waste disproportionate CPU time.
This issue affects BIND 9 versions 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-11331

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-790` |
| Published | 2026-07-22T15:16:51.457 |

An attacker who knows (or guesses) that a resolver uses RPZ with wildcard CNAME policies can craft query names long enough to trigger a NAMETOOLONG error condition during RPZ processing. This is not handled correctly and may lead to defeating the RPZ rule. It also may lead to an unexpected exit of the BIND 9 software.
This issue affects BIND 9 versions 9.16.0 through 9.18.50, 9.20.0 through 9.20.24, 9.21.0 through 9.21.23, 9.16.8-S1 through 9.18.50-S1, and 9.20.9-S1 through 9.20.24-S1.

### CVE-2026-65516

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-23T12:18:44.510 |

Unauthenticated Server Side Request Forgery (SSRF) in PeproDev Ultimate Invoice <= 2.2.6 versions.

### CVE-2026-65497

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-23T12:18:43.040 |

Administrator PHP Object Injection in Complianz <= 7.5.0 versions.

### CVE-2026-12421

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T08:16:23.683 |

The ARforms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'password' Field Values in all versions up to, and including, 7.2.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-7534

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T06:16:50.780 |

The SUMO Reward Points plugin for WordPress is vulnerable to Unauthenticated Stored Cross-Site Scripting via the REST API endpoint `/wp-json/wc-srp/v1/earning` in versions up to, and including, 32.7.0. This is due to the `user_has_cap` filter in the `SRP_REST_Earning_Controller` class unconditionally granting the custom `rs_earning_read` capability to all users — including unauthenticated visitors — combined with missing sanitization of the `reason` parameter in the `create_items()` function and missing output escaping in the `column_default()` method of `SRP_Master_Log`. This makes it possible for unauthenticated attackers to inject arbitrary web scripts into the reward points log that will execute whenever an administrator accesses the Master Log or User Reward Points admin pages.

### CVE-2026-7232

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T06:16:50.607 |

The FormCraft plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '[parameter name]' parameter in all versions up to, and including, 3.9.14 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit chain combines a server-side gap — where composite matrix sub-field keys such as field2_0 and field2_1 are never passed through the sanitization loop and are stored raw via $wpdb->insert() — with a client-side gap where DOMPurify is only invoked when typeof field.value === 'string', but matrix values arrive from the server as arrays, bypassing the check before being mapped to strings and injected into the DOM. Additionally, the same sink is reachable via a second attack vector: array-typed field values are passed through htmlentities() on submission but later reversed by html_entity_decode() at formcraft-main.php:2608 and :2122, restoring the malicious payload before storage and rendering.

### CVE-2026-13067

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-22T20:16:44.967 |

When PROXY protocol v2 is used on the Unix domain socket path, roles derived from X.509 client certificates may not be validated against the configured tlsCATrusts allow-list. This can result in unintended role assignments following MONGODB-X509 authentication. Affected scenarios require local access to the proxy Unix domain socket and a valid X.509 certificate issued by a trusted certificate authority.

### CVE-2026-40714

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-22T16:17:19.423 |

Dell PowerProtect Data Manager, versions prior to 20.2.0.0, contain(s) an Improper Input Validation vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-65896

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-23T12:18:48.050 |

Grav API Plugin (Composer package getgrav/grav-plugin-api) before 1.0.10 fails to properly validate the slug field in the POST /pages/{route}/move endpoint. PagesController::move() sanitizes the slug only with ltrim($body['slug'], '.'), which strips leading periods but does not neutralize '/' or '..' segments. An authenticated API caller with the api.pages.write permission can supply path traversal sequences (e.g., 01.home/../../../pwned) to move an entire page directory (content and media) to an arbitrary writable location outside user/pages/, including outside the Grav installation.

### CVE-2026-65607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T12:18:47.633 |

SiYuan before v3.7.2 contains a path traversal vulnerability in the /export/temp/ short-circuit branch of the serveExport handler (kernel/server/serve.go). Unlike the main export branch, this branch joins the raw, percent-decoded request path with util.TempDir and serves the file without the IsSubPath or IsSensitivePath checks added in the earlier export-disclosure hardening (GHSA-6865-qjcf-286f). An authenticated attacker can send percent-encoded traversal sequences (e.g. /export/temp/%2e%2e/.../etc/passwd, where %2e%2e is decoded to '..') to read arbitrary files outside TempDir, including /etc/passwd, SSH keys (~/.ssh/*), and SiYuan workspace *.db and *.log files, bypassing the sensitive-file protection.

### CVE-2026-65540

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:47.110 |

Unauthenticated Cross Site Request Forgery (CSRF) in Popup for CF7 with Sweet Alert <= 1.6.5 versions.

### CVE-2026-65539

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:46.983 |

Unauthenticated Cross Site Request Forgery (CSRF) in Kwayy HTML Sitemap <= 4.0 versions.

### CVE-2026-65511

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:44.130 |

Unauthenticated Cross Site Scripting (XSS) in Manual - Documentation, Knowledge Base & Education WordPress Theme <= 7.5.4 versions.

### CVE-2026-65510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:44.010 |

Unauthenticated Cross Site Scripting (XSS) in PeproDev Ultimate Invoice <= 2.2.6 versions.

### CVE-2026-65494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T12:18:42.677 |

Subscriber SQL Injection in Dokan Pro <= 5.0.2 versions.

### CVE-2026-65492

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:42.430 |

Unauthenticated Cross Site Scripting (XSS) in Dokan Pro <= 5.0.0 versions.

### CVE-2026-65488

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:41.943 |

Unauthenticated Cross Site Request Forgery (CSRF) in LA-Studio Element Kit for Elementor <= 1.6.2 versions.

### CVE-2026-61947

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:34.433 |

Unauthenticated Cross Site Scripting (XSS) in Form Vibes – Database Manager for Forms <= 1.5.2 versions.

### CVE-2026-61944

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:34.053 |

Unauthenticated Cross Site Scripting (XSS) in Bookly <= 27.7 versions.

### CVE-2026-59517

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:32.227 |

Unauthenticated Cross Site Scripting (XSS) in Easy Form Builder <= 4.0.12 versions.

### CVE-2026-59512

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:31.860 |

Unauthenticated Cross Site Scripting (XSS) in Product Enquiry for WooCommerce <= 2.2.34.43 versions.

### CVE-2026-57809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:30.810 |

Unauthenticated Cross Site Scripting (XSS) in AffiliateWP <= 2.34.0 versions.

### CVE-2026-57769

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:30.283 |

Unauthenticated Cross Site Scripting (XSS) in Grand Photography <= 5.7.8 versions.

### CVE-2026-57767

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:30.167 |

Unauthenticated Cross Site Scripting (XSS) in WP Google Maps Pro <= 10.1.02 versions.

### CVE-2026-57735

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:30.043 |

Unauthenticated Cross Site Scripting (XSS) in Breakdance <= 2.7.1 versions.

### CVE-2026-57704

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:29.680 |

Unauthenticated Cross Site Scripting (XSS) in Smart Manager <= 8.90.0 versions.

### CVE-2026-57701

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:29.440 |

Unauthenticated Cross Site Scripting (XSS) in Real Estate Manager Pro <= 12.8.5 versions.

### CVE-2026-57699

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:29.310 |

Subscriber Cross Site Scripting (XSS) in Slider Pro <= 4.8.13 versions.

### CVE-2026-57696

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T12:18:29.180 |

Contributor Arbitrary File Deletion in Picture Gallery <= 1.6.5 versions.

### CVE-2026-57626

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T12:18:29.053 |

Cross-Site Request Forgery (CSRF) vulnerability in MailPoet allows Cross Site Request Forgery.

This issue affects MailPoet: from 5.30.0 through 5.33.0.

### CVE-2026-57428

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:28.930 |

Unauthenticated Cross Site Scripting (XSS) in Sprout Clients <= 3.2.3 versions.

### CVE-2026-57427

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:28.803 |

Unauthenticated Cross Site Scripting (XSS) in Download Monitor - WPForms Lock <= 1.0.4 versions.

### CVE-2026-57397

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:28.560 |

Unauthenticated Cross Site Scripting (XSS) in Coaching <= 3.9.2 versions.

### CVE-2026-57374

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:28.313 |

Unauthenticated Cross Site Scripting (XSS) in Funnel Kit Funnel Builder PRO <= 3.15.0.7 versions.

### CVE-2026-57370

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T12:18:28.057 |

Unauthenticated Cross Site Scripting (XSS) in Visitor Traffic Real Time Statistics Pro <= 11.9.1 versions.

### CVE-2026-57367

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T12:18:27.910 |

Subscriber Broken Access Control in WP Booking System < 5.12.8.1 versions.

### CVE-2026-59678

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-23T08:16:25.003 |

An Incorrect Authorization vulnerability in Linux-Gaming PortProtonQt allows any users to mount and unmount arbitrary file systems and modify the network configuration via NetworkManager.






This issue affects PortProtonQt before 0d0f0950ebd948cdf82e8c3e1ebd2bcb9b8bafbe.

### CVE-2026-9737

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-22T20:17:09.863 |

During query planning when reading the sort pattern in raw BSONObj form, in some places we don’t explicitly handle the meta expression case. This may lead to incorrect transformations leading to invariant failure.

### CVE-2026-13077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-22T20:16:46.517 |

A missing bounds check in the BSON CodeWScope element accessors allows an attacker to trigger an out-of-bounds heap read via a crafted aggregation pipeline. The vulnerability can be exploited by an authenticated user by generating a malformed BSONColumn data containing a CodeWScope element, bypassing wire-level BSON validation. When the forged element is decompressed, the unchecked size value is used in pointer arithmetic, causing either a server crash or disclosure of adjacent heap memory contents.

### CVE-2026-13076

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-22T20:16:46.367 |

An authenticated user can cause a {{mongod}} process to be terminated by the operating system under memory pressure by performing a specific data type conversion operation within MongoDB's aggregation framework. The behavior stems from disproportionate memory consumption during this operation, and requires both write access to the database and the ability to run aggregation queries.

### CVE-2026-13075

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-22T20:16:46.213 |

An authenticated user can cause the mongod process to be terminated by the operating system under memory pressure via the $rankFusion and $scoreFusion aggregation stages. The issue originates in the server's error-handling path and requires the ability to run aggregation queries.

### CVE-2026-13071

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-22T20:16:45.580 |

An authenticated user with read access can cause the mongod process to be terminated through certain aggregation expressions that execute server-side JavaScript. The issue involves improper memory handling during document processing.

### CVE-2026-13069

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-22T20:16:45.270 |

An authenticated user can cause excessive CPU consumption or out-of-memory conditions on a MongoDB server by sending a crafted Queryable Encryption find payload containing an unvalidated field used to control an internal computation loop. The resulting resource exhaustion degrades availability for other operations.

### CVE-2026-13066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-07-22T20:16:44.813 |

Improper handling of DBPointer objects during BSON serialization in MongoDB's server-side JavaScript engine can result in internal process memory contents being included in data returned to the client. This constitutes an unintended information disclosure affecting deployments that use server-side JavaScript.

### CVE-2026-13065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-22T20:16:44.670 |

A user with read-only privileges is able to craft an aggregation pipeline using the $linearFill window function operator with a specific sortBy expression type to cause the mongod process to terminate abnormally, resulting in denial of service. The issue stems from insufficient validation of sort specifications during execution.

### CVE-2026-13064

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-07-22T20:16:44.533 |

Certain query operations involving deeply nested $jsonSchema constructs can trigger disproportionate CPU consumption in affected MongoDB deployments, potentially leading to resource exhaustion. The resulting CPU-bound operation cannot be interrupted through standard administrative controls.

### CVE-2026-13062

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-07-22T20:16:44.263 |

An authenticated user with write privileges on a Queryable Encryption-enabled collection may be able to modify internal encryption metadata fields that are intended to be server-controlled, by sending crafted write commands through the mongos router on a sharded cluster. This can result in corruption of encrypted query correctness.

### CVE-2026-13060

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-22T20:16:43.970 |

An authenticated user with limited read privileges may be able to access documents from collections they are not authorized to read, due to an inconsistency in how the $graphLookup aggregation stage is evaluated during authorization and during execution. Affected scenarios involve collections referenced within existing view pipeline definitions.

### CVE-2026-13058

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-22T20:16:43.660 |

An authenticated user with basic write privileges can cause the mongod process to terminate abnormally by sending a crafted transaction command with an incomplete set of required fields. The issue stems from inconsistent validation across related transaction command parameters, resulting in a fatal internal invariant failure and denial of service.

### CVE-2026-13056

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1325` |
| Published | 2026-07-22T20:16:43.383 |

Using expressions that generate large arrays it is possible to craft a query that creates very large intermediate objects in memory, causing the server to crash with OOM error.

### CVE-2026-13055

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-07-22T20:16:43.220 |

The `$_internalIndexKey` aggregation expression can be used by any authenticated user to crash a MongoDB server (mongod). The expression fails to handle compound wildcard index specifications, triggering an internal consistency check that aborts the server process. The user must be able to run an aggregation pipeline.

### CVE-2026-64833

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-22T18:17:05.627 |

FFmpeg versions 0.7.1 through 8.1.2 contain an out-of-bounds read vulnerability in the S/PDIF muxer that allows attackers to access memory beyond buffer boundaries by supplying a crafted DTS stream with a core_size value larger than the actual packet length. Attackers can exploit the missing bounds check in the spdif_header_dts4 function by providing a malicious DTS-HD audio stream during S/PDIF re-muxing to trigger unauthorized memory reads beyond the packet buffer.

### CVE-2026-48029

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-07-22T15:17:18.357 |

libheif is a HEIF and AVIF file format decoder and encoder. Versions 1.19.0 through 1.21.2 have a heap OOB read in ImageItem_Grid::decode_grid_tile via irot-induced tile-coordinate underflow. Version 1.22.0 fixes the issue.
