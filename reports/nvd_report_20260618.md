# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-17 23:16 UTC
- **対象期間**: `2026-06-16T22:15:52.000Z` 〜 `2026-06-17T23:16:02.000Z`
- **重要CVE数**: 642 件（Critical 9.0+: 228 件 / High 7.0〜: 414 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **リモートから認証不要でコード実行や情報漏洩が可能** な脆弱性が目立ちます。  
- **Web アプリケーション系（WordPress プラグイン、Electron デスクトップアプリ）** と **エンタープライズ基盤（Oracle Fusion Middleware／Solaris）** が集中して報告され、攻撃対象の広がりが顕著です。  
- 多くの脆弱性は **入力サニタイズ不備や権限チェックの欠如** が根本原因で、パッチ適用だけでなく **開発・デプロイ時のセキュリティ設計見直し** が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 主な影響 | 重大性 (CVSS) | 注目理由 |
|-----|----------------------|----------|---------------|----------|
| **CVE‑2026‑25470** | ACPT (Pro) – Custom Post Types Plugin for WordPress (≤ 2.0.47) | リモートコードインクルージョン（RCE） | 10.0 (3.1) | WordPress は世界で最も利用される CMS。プラグインの脆弱性は **多数のサイトで即座に攻撃対象** になる。 |
| **CVE‑2026‑48055** | Streambert (Electron デスクトップアプリ) 2.4.0 以前 | Zip Slip による任意ファイル書き込み・コード実行 | 10.0 (3.1) | Electron アプリはデスクトップ環境に直接インストールされるため、**ローカルユーザーだけでなくネットワーク経由の攻撃者** がマシン全体を乗っ取れる。 |
| **CVE‑2026‑3490** | picklescan (Python ライブラリ) < 1.0.4 | ブロックリスト回避により任意関数呼び出しが可能 | 10.0 (4.0) | Python 環境は CI/CD パイプラインやサーバーレス関数で広く利用。**サプライチェーン攻撃** の足掛かりになる可能性が高い。 |
| **CVE‑2026‑46846** / **CVE‑2026‑46803** / **CVE‑2026‑46800** | Oracle WebCenter Portal / WebCenter Sites (12.2.1.4.0, 14.1.2.0.0) | 認証不要のリモートコード実行 (HTTP/RMI) | 10.0 (3.1) | Oracle 製品は金融・官公庁等の **ミッションクリティカル環境** で使用されており、脆弱性が放置されると大規模情報漏洩・サービス停止につながる。 |
| **CVE‑2026‑46978** | Oracle Solaris 11.4 – Remote Administration Daemon (RADM) | HTTPS 経由での未認証リモートコード実行 | 10.0 (3.1) | Solaris は一部のインフラで根幹を担う OS。RADM は管理者権限で動作するため、**完全なシステム乗っ取り** が可能になる。 |

> **共通点**：すべてが「認証不要」か「ユーザー操作不要」でエクスプロイト可能。特にエンタープライズ製品は **パッチ適用が遅れがち** であるため、早急な対策が求められます。

---

## 3. 推奨アクション  

### 3.1 パッチ・アップデートの適用
| 製品 | 現行バージョン (脆弱) | 推奨バージョン | 取得先・備考 |
|------|----------------------|----------------|--------------|
| **ACPT (Pro) – Custom Post Types Plugin** | ≤ 2.0.47 | **2.0.48 以上** | WordPress 管理画面 → プラグイン更新、または公式リポジトリから手動ダウンロード |
| **Streambert** | ≤ 2.4.0 | **2.4.1 以上** | GitHub Releases（`streambert-2.4.1.zip`） |
| **picklescan** | < 1.0.4 | **1.0.4** 以上 | PyPI (`pip install -U picklescan`) |
| **Oracle WebCenter Portal / Sites** | 12.2.1.4.0, 14.1.2.0.0 | **12.2.1.4.1** 以降、または **14.1.2.1** 以降 | Oracle My Oracle Support (MOS) → “Critical Patch Update” (CPU) 2026‑Q2 で提供 |
| **Oracle Solaris 11.4 (RADM)** | 11.4 (全リリース) | **11.4.11.0** 以上（Solaris 11.4 Patch 2026‑001） | Solaris 11.4 Update (SRU) から取得、`pkg update` 推奨 |

### 3.2 追加の防御策
1. **Web アプリケーションファイアウォール (WAF)**  
   - WordPress のプラグイン脆弱性に対し、`/wp-content/plugins/acpt-pro/` への **リクエストボディサイズ制限** と **不審なファイルアップロードのブロック** を設定。  
2. **Electron アプリのサンドボックス化**  
   - `app.setAppUserModelId` と `BrowserWindow` の `sandbox: true` オプションを有効化し、外部からのアーカイブ展開時に **パス・トラバーサル防止** を徹底。  
3. **Python 環境の依存関係ロック**  
   - `requirements.txt` に `picklescan>=1.0.4` を明記し、CI パイプラインで **依存関係スキャン（Bandit, Safety）** を実行。  
4. **Oracle 製品の最小権限化**  
   - RADM, WebCenter の管理ポートは **内部ネットワークのみ** に限定し、TLS 1.3 以上で暗号化。  
   - 不要な管理機能（例：RMI コンソール）を **無効化** し、ファイアウォールで IP 制限。  
5. **ログ監視とインシデント対応**  
   - すべての対象製品で **異常なファイル書き込み・プロ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-3490

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-183` |
| Published | 2026-06-17T17:16:50.727 |

picklescan before 1.0.4 fails to block pkgutil.resolve_name, allowing attackers to bypass the entire blocklist by resolving any dangerous function through indirect REDUCE calls. Remote attackers can invoke any blocked function such as os.system, builtins.exec, or subprocess.call to achieve remote code execution.

### CVE-2026-48055

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-22` |
| Published | 2026-06-17T13:20:42.257 |

Streambert is a cross-platform Electron Desktop App to stream and download any video media. In versions 2.4.0 and prior, a high-severity Zip Slip vulnerability was identified in Streambert's subtitle extraction logic. The application does not sanitize archive entry filenames during extraction, allowing a malicious archive to perform path traversal and write arbitrary files to the host filesystem. The subtitle extraction process downloads a ZIP archive and extracts its entries. The destination file path is constructed by concatenating the raw archive entry name (extracted.name) directly to the temporary directory path. If a malicious ZIP archive containing directory traversal sequences is processed, it escapes the temporary directory boundaries. The application then writes the extracted payload anywhere on the host filesystem subject to the application's current write permissions. This issue has been fixed in version 2.5.0.

### CVE-2026-28615

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:15.630 |

In Telecomm, there is a possible way to initiate an unauthorized phone call due to a permissions bypass. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28587

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:15.490 |

In MmsSmsProvider of MmsSmsProvider.java, there is a possible way to retrieve sensitive information due to a missing permission check. This could lead to local information disclosure with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28576

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:15.357 |

In Contacts Provider, there is a possible way to access the contacts database due to SQL injection. This could lead to local information disclosure with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28575

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-17T13:20:15.237 |

In PackageInstaller.Session#transfer of frameworks/base/services/core/java/com/android/server/pm/PackageInstallerSession.java, there is a possible memory exhaustion attack due to a logic error in the code. This could lead to local denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-25470

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T13:20:11.603 |

Improper Control of Generation of Code ('Code Injection') vulnerability in ACPT ACPT (Pro) - Custom Post Types Plugin for WordPress allows Remote Code Inclusion.

This issue affects ACPT (Pro) - Custom Post Types Plugin for WordPress: from n/a through 2.0.47.

### CVE-2026-0092

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:26.813 |

In Package Manager, there is a possible device lock controller bypass due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0083

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-06-17T13:19:26.670 |

In Nfc::eventCallback() of Nfc.h, there is a possible use after free due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0082

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-453` |
| Published | 2026-06-17T13:19:26.520 |

In tryStartActivity of NfcDispatcher.java, there is a possible automatic special app access permission assignment due to an insecure default value. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0081

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:26.373 |

In NFC, there is a possible way to spoof an NFC event due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0071

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:26.240 |

In SettingsLib, there is a possible missing permission check due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0068

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-06-17T13:19:26.093 |

In createSessionInternal of PackageInstallerService.java, there is a possible method to remove a DPC app from a managed device without DO consent due to desync from persistence. This could lead to local escalation of privilege if a user can install a malicious app with no additional execution privileges needed. User interaction is needed for exploitation.

### CVE-2026-0064

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-17T13:19:25.947 |

In multiple places, there is a possible persistent denial of service due to resource exhaustion. This could lead to local denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0063

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T13:19:25.800 |

In setAllowedCarriers of PhoneInterfaceManager.java, there is a possible way to disable carrier restrictions due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2025-69129

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:19:18.620 |

Unauthenticated Arbitrary File Upload in WordPress & WooCommerce Scraper Plugin, Import Data from Any Site <= 1.0.7 versions.

### CVE-2026-46978

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:16.803 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Remote Administration Daemon).   The supported version that is affected is 11.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Solaris.  While the vulnerability is in Oracle Solaris, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Solaris accessible data as well as  unauthorized access to critical data or complete access to all Oracle Solaris accessible data. CVSS 3.1 Base Score 10.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-46846

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:54:02.140 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46803

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:57.947 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46800

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-306` |
| Published | 2026-06-17T10:53:57.630 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46798

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-306` |
| Published | 2026-06-17T10:53:57.420 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46781

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:55.673 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46778

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:55.363 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35308

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:22.940 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Centralized Third Party Jars).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35307

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:22.833 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35301

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:22.200 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebLogic Server.  While the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35292

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.323 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebLogic Server.  While the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-48781

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-302;CWE-345;CWE-863` |
| Published | 2026-06-17T13:20:43.060 |

Postiz is an AI social media scheduling tool. In versions prior to 2.21.8, the Skool integration callback signed an attacker-controlled JSON blob into a session-shape JWT using the application's JWT_SECRET, and the auth middleware trusted every claim in that JWT without re-resolving the user from the database. Any authenticated Postiz user could forge a SUPERADMIN session and impersonate arbitrary organizations. This allowed Full Access to the following: all parts of Postiz, including users registered to the specific instance and the ability to post in the name of the victim's social media channels added to that Postiz instance. This issue has been fixed in version 2.21.8.

### CVE-2026-40783

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T13:20:38.090 |

Contributor Remote Code Execution (RCE) in Blocksy Companion Pro <= 2.1.37 versions.

### CVE-2026-40749

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:36.593 |

Subscriber Arbitrary File Upload in Charity Zone <= 1.1.1 versions.

### CVE-2026-40748

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:36.473 |

Subscriber Arbitrary File Upload in Kids Gift Shop <= 0.5.4 versions.

### CVE-2026-40747

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:36.337 |

Subscriber Arbitrary File Upload in Ecommerce Zone <= 0.9.7 versions.

### CVE-2026-40746

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:36.213 |

Subscriber Arbitrary File Upload in Restaurant Zone <= 0.7.8 versions.

### CVE-2026-39589

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:21.523 |

Subscriber Arbitrary File Upload in Webenvo <= 0.0.6 versions.

### CVE-2026-27041

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:12.477 |

Contributor Arbitrary File Upload in Unlimited Elements for Elementor (Premium) <= 2.0.6 versions.

### CVE-2026-25446

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:11.473 |

Subscriber Arbitrary File Upload in WishList Member X <= 3.29.0 versions.

### CVE-2026-22327

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:06.417 |

Subscriber Arbitrary File Upload in Restaurt <= 1.0.4 versions.

### CVE-2025-60218

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:19:15.583 |

Subscriber Arbitrary File Upload in PT Luxa Addons <= 1.2.2 versions.

### CVE-2024-52488

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:19:12.913 |

Subscriber Arbitrary File Upload in Grip <= 1.0.9 versions.

### CVE-2026-46964

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:15.567 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Work Provider Site Level Administration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Universal Work Queue.  While the vulnerability is in Oracle Universal Work Queue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Universal Work Queue. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46963

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:15.460 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Work Provider Site Level Administration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Universal Work Queue.  While the vulnerability is in Oracle Universal Work Queue, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Universal Work Queue. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46933

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:12.843 |

Vulnerability in the Oracle Applications Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications Manager.  While the vulnerability is in Oracle Applications Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Applications Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46918

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:09.560 |

Vulnerability in the Oracle Process Manufacturing Product Development product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Product Development.  While the vulnerability is in Oracle Process Manufacturing Product Development, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Product Development. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46908

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:08.610 |

Vulnerability in the JD Edwards EnterpriseOne Accounts Payable product of Oracle JD Edwards (component: Accounts Payable).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Accounts Payable.  While the vulnerability is in JD Edwards EnterpriseOne Accounts Payable, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Accounts Payable. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46907

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:08.503 |

Vulnerability in the JD Edwards EnterpriseOne Order Promising product of Oracle JD Edwards (component: Order Promising Integration).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Order Promising.  While the vulnerability is in JD Edwards EnterpriseOne Order Promising, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Order Promising. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46901

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-06-17T10:54:07.840 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-46900

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-06-17T10:54:07.737 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46897

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:07.427 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L).

### CVE-2026-46895

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-06-17T10:54:07.223 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46893

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:07.013 |

Vulnerability in the JD Edwards EnterpriseOne General Ledger product of Oracle JD Edwards (component: E1 Foundation).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via SMB to compromise JD Edwards EnterpriseOne General Ledger.  While the vulnerability is in JD Edwards EnterpriseOne General Ledger, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne General Ledger. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46855

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:03.117 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46854

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:03.013 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Target Management).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46852

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:02.803 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46850

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T10:54:02.590 |

Vulnerability in the MySQL Shell product of Oracle MySQL (component: Shell for VS Code).   The supported version that is affected is 2026.2.0+9.6.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise MySQL Shell.  While the vulnerability is in MySQL Shell, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of MySQL Shell. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46847

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:02.280 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46844

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:01.917 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46838

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:01.293 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46832

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:00.770 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Discovery Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46814

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:58.983 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46802

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:57.843 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46794

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:53:57.003 |

Vulnerability in the Identity Manager Connector product of Oracle Fusion Middleware (component: Generic Unix Connector).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via SSH to compromise Identity Manager Connector.  While the vulnerability is in Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46793

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:56.900 |

Vulnerability in the Identity Manager Connector product of Oracle Fusion Middleware (component: Database User).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Identity Manager Connector.  While the vulnerability is in Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46792

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:56.800 |

Vulnerability in the Identity Manager Connector product of Oracle Fusion Middleware (component: Generic Unix Connector).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Identity Manager Connector.  While the vulnerability is in Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46782

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:55.780 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46779

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:55.467 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3 to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46767

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:54.200 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46765

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:53.887 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35323

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.513 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35321

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.303 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35316

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:40:23.780 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35313

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:23.467 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  While the vulnerability is in Oracle Access Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35294

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:21.540 |

Vulnerability in the Identity Manager Connector product of Oracle Fusion Middleware (component: Mainframe Connectors).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Identity Manager Connector.  While the vulnerability is in Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35285

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.807 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35284

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.703 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35283

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.603 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35282

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.500 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35281

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.397 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35280

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:20.293 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35268

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:19.020 |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Identity Manager.  While the vulnerability is in Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Identity Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35263

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:18.600 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebLogic Server.  While the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-49108

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:56.763 |

Unauthenticated PHP Object Injection in Moderno < 1.43 versions.

### CVE-2025-69127

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:33.460 |

Unauthenticated PHP Object Injection in Plumbing <= 1.6 versions.

### CVE-2025-69111

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:32.137 |

Unauthenticated PHP Object Injection in Reisen <= 1.4.1 versions.

### CVE-2025-60236

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:31.320 |

Deserialization of Untrusted Data vulnerability in EMV Creatify allows Object Injection.

This issue affects Creatify: from n/a through 1.5.

### CVE-2025-60231

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:31.167 |

Deserialization of Untrusted Data vulnerability in EMV The Hospital nrghospital allows Object Injection.

This issue affects The Hospital: from n/a through 1.8.1.

### CVE-2025-60230

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:31.023 |

Deserialization of Untrusted Data vulnerability in Themeton The Barber Shop allows Object Injection.

This issue affects The Barber Shop: from n/a through 1.9.

### CVE-2025-60229

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:30.840 |

Deserialization of Untrusted Data vulnerability in Themeton Lagom allows Object Injection.

This issue affects Lagom: from n/a through 2.0.

### CVE-2026-54807

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:20:51.853 |

Unauthenticated Privilege Escalation in Registration Form for WooCommerce <= 1.0.9 versions.

### CVE-2026-54806

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:51.727 |

Unauthenticated PHP Object Injection in WP Activity Log <= 5.6.3.1 versions.

### CVE-2026-54803

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-17T13:20:51.343 |

Subscriber Privilege Escalation in SMS Alert Order Notifications <= 3.9.4 versions.

### CVE-2026-54194

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:50.670 |

Contributor PHP Object Injection in Fusion Builder <= 3.15.4 versions.

### CVE-2026-52706

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:49.313 |

Unauthenticated PHP Object Injection in JetEngine <= 3.8.10 versions.

### CVE-2026-49767

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-17T13:20:46.693 |

Unauthenticated Broken Authentication in wpForo Forum <= 3.1.0 versions.

### CVE-2026-49107

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:46.443 |

Unauthenticated PHP Object Injection in Thrive Apprentice < 10.8.10.2 versions.

### CVE-2026-49075

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:45.660 |

Contributor PHP Object Injection in JetEngine <= 3.8.9.1 versions.

### CVE-2026-49058

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:20:44.990 |

Unauthenticated Privilege Escalation in LoginPress Pro <= 6.2.2 versions.

### CVE-2026-42380

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:39.933 |

Unauthenticated PHP Object Injection in AI Lab < 5.4.2 versions.

### CVE-2026-40725

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:35.437 |

Unauthenticated PHP Object Injection in WooCommerce Product Filters < 2.0.6 versions.

### CVE-2026-39529

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:18.777 |

Unauthenticated PHP Object Injection in Elementra <= 1.0.9 versions.

### CVE-2026-32966

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-17T13:20:16.097 |

DataSource API Missing Authorization Check Leads to Arbitrary Data Source Metadata Disclosure in Apache DolphinScheduler.

This issue affects Apache DolphinScheduler: before 3.4.2.

Users are recommended to upgrade to version 3.4.2, which fixes the issue.

### CVE-2026-27429

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:13.113 |

Unauthenticated PHP Object Injection in Nifty <= 1.4.1 versions.

### CVE-2026-27395

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:20:12.620 |

Unauthenticated Privilege Escalation in Support Board < 3.8.9 versions.

### CVE-2026-10094

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:19:32.123 |

A Path Traversal vulnerability affecting SOLIDWORKS Visualize from SOLIDWORKS Desktop Release 2024 through SOLIDWORKS Desktop Release 2026 could allow an attacker to write arbitrary files on the server.

### CVE-2025-69179

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:19:25.407 |

Unauthenticated Privilege Escalation in Support Ticket Management System <= 1.9 versions.

### CVE-2025-69122

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:19:18.190 |

Unauthenticated PHP Object Injection in SeaFood Company <= 1.4 versions.

### CVE-2025-69108

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:19:16.683 |

Unauthenticated PHP Object Injection in Hot Coffee <= 1.7 versions.

### CVE-2025-60205

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:19:15.457 |

Unauthenticated PHP Object Injection in ThemeREX Addons <= 2.36.1.1 versions.

### CVE-2026-46919

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:09.660 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46909

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:08.710 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46905

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:54:08.277 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Web Runtime Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46904

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:08.167 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46902

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:07.950 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Command Center Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46890

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:06.703 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46889

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:06.600 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46887

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:06.393 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46884

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:06.073 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46883

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:05.970 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46882

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:05.870 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46881

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:05.767 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46880

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:05.660 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46879

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:54:05.550 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46878

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:05.440 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46860

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:03.650 |

Vulnerability in the MySQL Router product of Oracle MySQL (component: Router: General).  Supported versions that are affected are 9.0.0-9.7.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise MySQL Router.  Successful attacks of this vulnerability can result in takeover of MySQL Router. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46859

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-17T10:54:03.547 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46857

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:03.330 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Oracle Management Service).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46845

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:54:02.020 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Security Framework).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46813

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:58.880 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46807

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:58.363 |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Identity Manager.  Successful attacks of this vulnerability can result in takeover of Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46801

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-306` |
| Published | 2026-06-17T10:53:57.737 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46799

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-306` |
| Published | 2026-06-17T10:53:57.527 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46797

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:53:57.313 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46783

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:55.883 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46774

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:54.943 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46773

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:54.840 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46766

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:54.097 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35319

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.090 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35312

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:23.357 |

Vulnerability in the Oracle Virtual Directory product of Oracle Fusion Middleware (component: Virtual Directory Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Virtual Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Virtual Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35310

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:23.150 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35309

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:23.040 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Centralized Third Party Jars).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35304

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:22.517 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Coherence.  Successful attacks of this vulnerability can result in takeover of Oracle Coherence. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35300

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T10:40:22.100 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise WebLogic Server.  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35296

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.783 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35293

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.423 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:20.910 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:20.083 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Performance Monitor).  Supported versions that are affected are 8.61 and  8.62. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-12440

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.187 |

Use after free in DigitalCredentials in Google Chrome on Windows prior to 149.0.7827.155 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-46911

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:08.920 |

Vulnerability in the JD Edwards EnterpriseOne Project Costing product of Oracle JD Edwards (component: Job Costing).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne Project Costing.  While the vulnerability is in JD Edwards EnterpriseOne Project Costing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Project Costing accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Project Costing accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-46906

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:08.387 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  While the vulnerability is in JD Edwards EnterpriseOne Tools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Tools accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Tools accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-46899

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-06-17T10:54:07.630 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-46861

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:03.760 |

Vulnerability in the MySQL NDB Cluster product of Oracle MySQL (component: Cluster: NDB Operator).  Supported versions that are affected are 8.0.11-8.0.46,   8.4.0-8.4.9 and    9.0.0-9.7.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise MySQL NDB Cluster.  While the vulnerability is in MySQL NDB Cluster, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all MySQL NDB Cluster accessible data as well as  unauthorized access to critical data or complete access to all MySQL NDB Cluster accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-46856

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-79` |
| Published | 2026-06-17T10:54:03.220 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-46853

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T10:54:02.910 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Metadata Plugin).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-46789

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:56.497 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-46786

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-17T10:53:56.190 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-55743

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-06-17T15:17:02.337 |

The shell tool command allowlist in the SecurityPolicy of OpenHuman desktop agent through 0.54.0 (default Supervised security policy) can be bypassed to execute arbitrary OS commands with the privileges of the desktop user. Two flaws in src/openhuman/security/policy.rs combine: (1) is_args_safe() blocks the find flags -exec and -ok but not the functionally identical -execdir and -okdir, which also execute an arbitrary command for each matched file; and (2) skip_env_assignments() strips leading inline KEY=value environment-variable assignments before allowlist validation, so a command such as GIT_EXTERNAL_DIFF=<cmd> git diff is validated as the allowed git diff but, when executed via the shell, runs <cmd> through git's environment-driven hooks (for example GIT_EXTERNAL_DIFF or GIT_SSH_COMMAND). Because the sandbox is the primary trust boundary between untrusted LLM-processed content and the host operating system, an attacker can achieve remote code execution via indirect prompt injection: a malicious document, email, calendar event, or web page ingested by the agent instructs it to run a benign-looking allowlisted command, resulting in arbitrary command execution, data exfiltration, arbitrary file read/write, and lateral movement on the user's machine. The issue was fixed in commit 60050aa09a870f53ed7e4cd40ed41fd2860329e7 (first released in 0.54.22-staging; first stable release 0.56.0), which blocks -execdir/-okdir for find.

### CVE-2026-54388

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-17T20:17:27.623 |

Tinyproxy through 1.11.3, fixed in commit 364cdb6, fails to reject requests containing multiple Content-Length headers with differing values, forwarding all duplicate headers to the backend while using the first value to determine how many request body bytes to consume. Remote attackers can desynchronize the proxy and backend parser state, allowing injection of arbitrary HTTP requests to the backend to enable cache poisoning, access control bypass, and request hijacking.

### CVE-2026-54387

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-17T20:17:27.480 |

Tinyproxy through 1.11.3, fixed in commit ff45d3b, fails to reconcile conflicting Content-Length and Transfer-Encoding: chunked headers, forwarding both verbatim to the backend while using Content-Length to determine how many request body bytes to consume. Remote attackers can desynchronize the proxy and backend parser state, allowing injection of arbitrary HTTP requests to the backend to enable cache poisoning, access control bypass, and request hijacking.

### CVE-2026-53805

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T18:18:05.320 |

NVIDIA Spatial Intelligence Lab's (SIL) GEN3C contains an unauthenticated remote code execution vulnerability in the inference API server where the /request-inference and /seed-model endpoints deserialize raw HTTP request bodies using Python's pickle.loads() without authentication or input validation. Attackers can supply a crafted payload containing a __reduce__ gadget to the inference API port to achieve remote code execution as the inference process.

### CVE-2026-53874

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T17:17:25.733 |

picklescan before 1.0.1 contains an unsafe deserialization vulnerability allowing unauthenticated users to execute arbitrary code by hiding eval calls nested under callable objects via getattr. Attackers can embed malicious code in pickle files that evades detection but executes when the pickle is loaded from untrusted sources.

### CVE-2026-53873

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-17T17:17:25.607 |

picklescan before 1.0.4 contains an incomplete blocklist for the profile module that fails to block the module-level profile.run() function, allowing attackers to achieve arbitrary code execution via exec(). Attackers can craft malicious pickle files calling profile.run(statement) to execute arbitrary Python code while picklescan reports zero security issues.

### CVE-2025-71325

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-391` |
| Published | 2026-06-17T17:16:41.247 |

picklescan before 0.0.27 contains a parsing logic error in the _list_globals function when handling STACK_GLOBAL opcodes, failing to track arguments in the correct range and allowing malicious pickle files to bypass detection. Attackers can craft pickle files with arguments at position zero to trigger unexpected exceptions and evade security scanning.

### CVE-2025-71323

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-17T17:16:41.110 |

picklescan before 0.0.33 fails to block the ctypes module, allowing attackers to achieve remote code execution by invoking direct syscalls and accessing raw memory. Attackers can craft malicious pickle files using ctypes.WinDLL to load kernel32.dll and execute arbitrary commands, bypassing sandbox protections and gadget chain detection.

### CVE-2025-71321

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T17:16:40.847 |

picklescan before 0.0.33 contains an arbitrary file writing vulnerability that allows attackers to bypass the dangerous blocklist by using distutils.file_util.write_file. Attackers can construct malicious pickle objects to overwrite critical system files and achieve denial of service or remote code execution.

### CVE-2025-71320

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-17T17:16:40.697 |

picklescan before 0.0.33 contains an incomplete deny-list that fails to block pydoc.locate and operator.methodcaller functions, allowing attackers to bypass security checks. Remote attackers can craft malicious pickle files using these unblocked functions to achieve arbitrary code execution when the pickle is deserialized.

### CVE-2026-54812

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T15:17:01.473 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in StylemixThemes Motors allows Blind SQL Injection.

This issue affects Motors: from n/a through 1.4.109.

### CVE-2026-47103

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-06-17T15:16:58.460 |

Python StateMachine versions 3.0.0 before 3.2.0 contains a remote code execution vulnerability that allows attackers to execute arbitrary code by supplying malicious SCXML documents containing crafted `<data expr="...">` attributes evaluated unsafely. The SCXMLProcessor passes attacker-controlled expression strings through a call chain ending in Python's built-in eval() without sandboxing, enabling arbitrary code execution in the context of the hosting process.

### CVE-2026-54819

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:59.920 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Webilia Inc. Listdom allows Blind SQL Injection.

This issue affects Listdom: from n/a through 5.4.0.

### CVE-2026-54815

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:59.390 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Cargo RD Cargo Shipping Location for WooCommerce allows Blind SQL Injection.

This issue affects Cargo Shipping Location for WooCommerce: from n/a through 5.6.

### CVE-2026-54809

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:58.837 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in VillaTheme GIFT4U allows Blind SQL Injection.

This issue affects GIFT4U: from n/a through 1.0.10.

### CVE-2026-54808

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:58.703 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WP Travel WP Travel Gutenberg Blocks allows Blind SQL Injection.

This issue affects WP Travel Gutenberg Blocks: from n/a through 3.9.4.

### CVE-2025-59554

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:30.390 |

Unauthenticated SQL Injection in Advanced Ads – Tracking < 3.0.7 versions.

### CVE-2026-54811

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:51.997 |

Unauthenticated SQL Injection in WP eMember < v10.9.4 versions.

### CVE-2026-54187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:50.147 |

Unauthenticated SQL Injection in JetEngine <= 3.8.10.1 versions.

### CVE-2026-54186

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:49.990 |

Unauthenticated SQL Injection in JobSearch <= 3.2.9 versions.

### CVE-2026-49084

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:46.323 |

Unauthenticated SQL Injection in JetEngine < 3.8.9.1 versions.

### CVE-2026-49080

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:46.047 |

Unauthenticated SQL Injection in wpDataTables <= 7.3.6 versions.

### CVE-2026-49079

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:45.917 |

Unauthenticated SQL Injection in JetSearch <= 3.5.17 versions.

### CVE-2026-49076

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:45.790 |

Unauthenticated SQL Injection in JetEngine <= 3.8.9.1 versions.

### CVE-2026-48875

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:44.293 |

Unauthenticated SQL Injection in JetSmartFilters <= 3.8.1 versions.

### CVE-2026-48797

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-358;CWE-862;CWE-1295` |
| Published | 2026-06-17T13:20:43.633 |

Backpropagate is a Python library for fine-tuning large language models on a single GPU. In versions 1.1.0 and 1.1.1, the optional Reflex web UI exposes a training control plane without authentication: dataset upload, model load, training start/stop, multi-run orchestration, GGUF export, and HuggingFace Hub push. The CLI accepts two operator-facing flags intended as security controls: --auth user:pass — documented as "require HTTP Basic authentication on every request to the UI." and--share — documented as "expose the UI on a public address; requires --auth." When --auth user:pass is passed, the CLI prints Auth: enabled (user: <username>) to confirm to the operator that authentication is active, then exports BACKPROPAGATE_UI_AUTH=user:pass to the subprocess that launches the Reflex backend. The Reflex backend (backpropagate/ui_app/**) never reads BACKPROPAGATE_UI_AUTH. No authentication middleware is registered. No request-level guard runs. No WebSocket upgrade guard runs. Any client that reaches the bound port — local or remote, depending on whether --share is used — has full UI access. An inline comment at backpropagate/cli.py:1217-1218 in the v1.1.0 source documents the gap: "For Phase 1 the variable is exported but Reflex doesn't read it yet." This comment was internal-facing; the user-facing documentation (README, CHANGELOG, SHIP_GATE) advertised the contract as enforced. An attacker who reaches the bound port can read uploaded datasets, trigger arbitrary training runs against any local base models as well as read their paths, trigger HuggingFace Hub pushes and cause disk-fill DoS. This issue has been fixed in version 1.2.0. If developers cannot immediately upgrade to 1.2.0 run backprop ui with no flags so it binds to localhost, use SSH port-forwarding (ssh -L 7860:localhost:7860 <training-host>) instead of --share for remote access, and audit any host previously launched with --share, re-issuing any HF tokens used during those sessions.

### CVE-2026-48745

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-940` |
| Published | 2026-06-17T13:20:42.743 |

Traccar Client is a GPS tracking mobile app for sending location updates to private servers using the open-source Traccar platform. In versions 9.7.19 and below, a single crafted deep link can silently hijack all GPS tracking parameters and redirect telemetry to an attacker-controlled server. The app registers a custom org.traccar.client://config deep-link scheme that silently writes attacker-supplied parameters (server URL, device ID, accuracy, distance, and interval) into the app's persistent configuration with no confirmation, notification, or visual indication. A single crafted link delivered via SMS, email, a webpage, or any installed app can therefore reconfigure the app the moment the victim taps it, with no special permissions required. As a result, an attacker can covertly redirect all of the victim's GPS telemetry to their own server at maximum precision and frequency, and the change persists across restarts. This gives the attacker continuous, real-time tracking of the victim's location. This issue has been fixed in version 9.7.20.

### CVE-2026-48616

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T13:20:42.600 |

Rocket.Chat versions <8.5.1, 8.4.4, 8.3.6, 8.2.6, 8.1.6, 8.0.7, 7.13.9, 7.10.13 has an access control vulnerability in Livechat files. Protected file downloads at /file-upload/:fileId/:name authorize livechat access using rc_room_type=l with rc_rid+rc_token, but the authorization path does not verify that rc_rid matches the requested file's rid. Furthermore, :fileId is predictable via sequential MongoDB IDs, and :name can be anything, allowing unauthenticated discovery of all uploaded files.

### CVE-2026-39596

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:21.793 |

Unauthenticated SQL Injection in Blocksy Companion Pro < 2.1.29 versions.

### CVE-2026-39438

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:18.193 |

Unauthenticated SQL Injection in ListingPro <= 2.9.10 versions.

### CVE-2026-22340

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:08.863 |

Unauthenticated SQL Injection in WPJobster <= 6.3.5 versions.

### CVE-2026-22332

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:08.067 |

Unauthenticated SQL Injection in Tutor LMS Pro <= 3.9.6 versions.

### CVE-2026-46913

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:09.127 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Installation Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where JD Edwards EnterpriseOne Tools executes to compromise JD Edwards EnterpriseOne Tools.  While the vulnerability is in JD Edwards EnterpriseOne Tools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46912

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:09.020 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Web Runtime Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  While the vulnerability is in JD Edwards EnterpriseOne Tools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Tools accessible data as well as  unauthorized update, insert or delete access to some of JD Edwards EnterpriseOne Tools accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-46805

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:58.153 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-46795

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:57.107 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-46785

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-17T10:53:56.087 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-35306

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:22.730 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Centralized Third Party Jars).   The supported version that is affected is 15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Coherence accessible data as well as  unauthorized update, insert or delete access to some of Oracle Coherence accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-35305

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:22.620 |

Vulnerability in the Oracle Coherence product of Oracle Fusion Middleware (component: Centralized Third Party Jars).   The supported version that is affected is 15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Coherence.  While the vulnerability is in Oracle Coherence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Coherence accessible data as well as  unauthorized update, insert or delete access to some of Oracle Coherence accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-48777

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-16T20:16:46.583 |

FileBrowser Quantum is a free, self-hosted, web-based file manager. Versions prior to 1.3.2-stable, 1.4.0-beta and 1.4.1-beta are vulnerable to Path Traversal through the publicPatchHandler in backend/http/public.go which joins user-controlled fromPath and toPath body fields with the trusted d.share.Path BEFORE the downstream sanitizer runs. Because filepath.Join collapses .. segments during the join, the sanitizer in resourcePatchHandler never sees the traversal and the move/copy/rename operates on a path outside the shared directory. The same root-cause pattern was patched for the bulk DELETE endpoint as CVE-2026-44542 (GHSA-fwj3-42wh-8673), but the PATCH handler with the identical pattern was not updated. A public share link with AllowModify=true is sufficient to exploit this. Anyone holding such a link can move, copy, or rename arbitrary files within the share owner's source root. This issue has been fixed in versions 1.3.3-stable and 1.4.2-beta.

### CVE-2026-53776

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-06-16T17:16:42.620 |

Perry before 0.5.1166 contains a JWT validation vulnerability that allows remote attackers to bypass token expiration by exploiting the unconditional setting of validate_exp = false in the verify_decode helper within the stdlib JWT verification path. Attackers in possession of a previously issued bearer token can present expired tokens to any jwt.verify() call and retain authenticated access indefinitely, bypassing force-expired sessions such as user logout or administrative revocation.

### CVE-2026-55200

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-680` |
| Published | 2026-06-17T20:17:28.667 |

libssh2 through 1.11.1, fixed in commit 7acf3df contains an out-of-bounds write vulnerability in ssh2_transport_read() that fails to enforce upper bounds on packet_length field. Remote attackers can send crafted SSH packets with excessively large packet_length values to corrupt heap memory and achieve remote code execution.

### CVE-2026-3894

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-17T18:17:44.287 |

Out-of-bounds Read vulnerability in RTI Connext Professional (Core Libraries) allows Overread Buffers.This issue affects Connext Professional: from 7.4.0 before 7.7.0, from 7.0.0 before 7.3.1.3, from 6.1.0 before 6.1.*, from 6.0.0 before 6.0.*, from 5.3.0 before 5.3.*, from 5.0.0 before 5.2.*.

### CVE-2026-2467

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-17T18:17:41.890 |

Heap-based Buffer Overflow vulnerability in RTI Connext Professional (Core Libraries) allows Overflow Variables and Tags.This issue affects Connext Professional: from 7.4.0 before 7.7.0, from 7.0.0 before 7.3.1.3, from 6.1.0 before 6.1.*, from 6.0.0 before 6.0.*, from 5.3.0 before 5.3.*, from 5.0.0 before 5.2.*.

### CVE-2026-42530

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T15:16:50.630 |

NGINX Open Source has a vulnerability in the ngx_http_v3_module module. When NGINX Open Source is configured to use the HTTP/3 QUIC module, a remote unauthenticated attacker along with conditions beyond their control can use a specially crafted HTTP/3 session to reopen a QPACK encoder stream. This may cause a Use-after-Free in the NGINX worker process leading to a restart. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.  


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-42055

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-17T15:16:50.353 |

NGINX Plus and NGINX Open Source have a vulnerability in the ngx_http_proxy_v2_module and ngx_http_grpc_module modules. This vulnerability exists when the proxy_http_version to 2 or grpc_pass directives are used to proxy HTTP/2 traffic, the ignore_invalid_headers directive is set to off, and the large_client_header_buffers directive size is larger than 2 megabytes. A remote, unauthenticated attacker, along with conditions beyond their control, could send large headers while creating an upstream request. This may cause a heap-based buffer overflow in the NGINX worker process leading to a restart. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR. 


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2025-13036

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-06-16T15:16:32.870 |

An authentication
bypass security issue exists within FactoryTalk Historian Site Edition. By
continually sending requests to the login endpoint, an attacker may obtain a
valid authentication token.

### CVE-2026-48814

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T20:17:22.260 |

Network-AI is a TypeScript/Node.js multi-agent orchestrator. In versions 5.7.1 and earlier, the MCP SSE server allows unauthenticated cross-origin MCP tool invocation due to an empty default secret. This issue was partially addressed by CVE-2026-46701 in version 5.4.5 by closing the CORS flaw (with Access-Control-Allow-Origin now set only for localhost origins), but the empty-default-secret flaw described in the title remained: the SSE MCP server still defaulted to an empty secret, _isAuthorized() still returned true when the secret was empty, and a non-loopback bind only produced a warning. As a result, the server still ran fully unauthenticated by default. Any non-browser caller (for example, curl, SSRF, or a 0.0.0.0 bind) could invoke all 22 MCP tools (config_set, agent_spawn, blackboard_write, token_*) with no credentials. This issue was fixed in version 5.7.2.

### CVE-2026-55196

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T19:18:13.203 |

Hermes WebUI before 0.51.409 contains an authentication bypass vulnerability in passkey registration endpoints that allows unauthenticated remote attackers to register arbitrary passkeys. When HERMES_WEBUI_PASSKEY=1 is enabled with no existing credentials, POST /api/auth/passkey/register/options and POST /api/auth/passkey/register endpoints are accessible without authentication, allowing attackers to claim the first passkey and gain permanent administrative control.

### CVE-2026-20266

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-78` |
| Published | 2026-06-17T18:17:40.900 |

In Splunk AI Toolkit versions below 5.7.4, a user who holds the "admin" Splunk role could execute arbitrary OS commands on the host running the Splunk Enterprise instance.  

The vulnerability is possible because of an unsafe shell execution pattern in the btool configuration helper, which constructs OS command strings from dynamic parameters without disabling shell interpretation.

### CVE-2026-36418

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T17:16:49.880 |

JimuReport versions 2.3.4 and below are vulnerable to remote code execution due to improper handling of Aviator expressions. The /jmreport/executeSelectApi endpoint passes user-supplied input directly to the Aviator expression engine without adequate validation allowing attackers to execute arbitrary code.

### CVE-2026-20181

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T17:16:42.990 |

A vulnerability in Cisco ISE and ISE-PIC could allow an authenticated, remote attacker to execute arbitrary commands on the underlying operating system of an affected device. To exploit this vulnerability, the attacker must have valid administrative credentials.

This vulnerability is due to insufficient validation of user-supplied input. An attacker could exploit this vulnerability by sending a crafted HTTP request to an affected device. A successful exploit could allow the attacker to obtain user-level access to the underlying operating system and then elevate privileges to root. In single-node deployments, successful exploitation of this vulnerability could cause the affected ISE node to become unavailable, resulting in a denial of service (DoS) condition. In that condition, endpoints that have not already authenticated would be unable to access the network until the node is restored.

### CVE-2026-50203

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:20:47.213 |

A path traversal in the SFTP provider (`SFTPHook.retrieve_directory` / `SFTPOperator(operation=get)`) let a malicious or compromised remote SFTP server write files outside the configured local destination directory via crafted directory-entry names. No Airflow account is required — the attack surface is any deployment downloading directories from an untrusted SFTP server. Upgrade `apache-airflow-providers-sftp` to 5.8.1 or later.

### CVE-2026-32967

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-17T13:20:16.233 |

Incorrect Authorization vulnerability of `/v2` experimental interface in Apache DolphinScheduler.

This issue affects Apache DolphinScheduler: before 3.4.2.

Users are recommended to upgrade to version 3.4.2, which fixes the issue.

### CVE-2026-24611

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:10.920 |

Unauthenticated Broken Access Control in MetForm Pro <= 3.9.1 versions.

### CVE-2026-46949

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:14.113 |

Vulnerability in the Oracle Advanced Outbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Advanced Outbound Telephony.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Advanced Outbound Telephony accessible data as well as  unauthorized access to critical data or complete access to all Oracle Advanced Outbound Telephony accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46946

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo` |
| Published | 2026-06-17T10:54:13.910 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle iSupport.  While the vulnerability is in Oracle iSupport, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle iSupport. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46945

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:13.807 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle iSupport.  While the vulnerability is in Oracle iSupport, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle iSupport. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46944

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo` |
| Published | 2026-06-17T10:54:13.700 |

Vulnerability in the Oracle iSupport product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle iSupport.  While the vulnerability is in Oracle iSupport, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle iSupport. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46930

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:10.613 |

Vulnerability in the Oracle In-Memory Cost Management for Discrete Industries product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.12-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle In-Memory Cost Management for Discrete Industries.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle In-Memory Cost Management for Discrete Industries accessible data as well as  unauthorized access to critical data or complete access to all Oracle In-Memory Cost Management for Discrete Industries accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46910

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-200;CWE-284;CWE-306;CWE-400` |
| Published | 2026-06-17T10:54:08.810 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Enterprise Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Tools accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-46896

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:07.327 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Enterprise Command Center Framework.  While the vulnerability is in Oracle Enterprise Command Center Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Command Center Framework. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46892

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:06.910 |

Vulnerability in the JD Edwards EnterpriseOne Human Resources Management product of Oracle JD Edwards (component: Human Resources).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Human Resources Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Human Resources Management accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Human Resources Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46875

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:05.230 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Deployment Library).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46858

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:03.437 |

Vulnerability in the APM - Application Performance Management product of Oracle Enterprise Manager (component: JADM, JVM Diagnostics).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise APM - Application Performance Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all APM - Application Performance Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of APM - Application Performance Management. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-46809

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:58.570 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Sites accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46784

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:55.987 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all WebCenter Content: Imaging accessible data as well as  unauthorized access to critical data or complete access to all WebCenter Content: Imaging accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46777

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:53:55.260 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-35298

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:21.887 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise WebLogic Server.  While the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35270

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:19.233 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-22313

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-16T20:16:28.710 |

The device has a webserver that exposes a REST API authenticated with a token on the management network. By exploiting an OS command injection vulnerability an authenticated attacker can send
arbitrary commands to the device that are executed with administrative permissions by the underlying operating system.

### CVE-2026-52705

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:49.190 |

Unauthenticated Arbitrary File Upload in SigmaForms Pro – AI Generated Forms <= 1.4.5 versions.

### CVE-2026-46872

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:04.907 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Install).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Manager Base Platform accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H).

### CVE-2026-35320

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.203 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-55202

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-17T20:17:29.250 |

Tinyproxy through 1.11.3, fixed in commit 09312a1, fails to properly validate the Host header during stathost detection, allowing unauthenticated attackers to access the stats page by injecting a matching Host header or bypass detection via port manipulation. Remote attackers can trigger unauthorized access to internal proxy statistics or misroute requests as transparent proxy connections to circumvent access controls.

### CVE-2026-7300

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-17T18:18:05.753 |

Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') vulnerability in RTI Connext Professional (Web Integration Service) allows Filter Failure through Buffer Overflow.This issue affects Connext Professional: from 7.4.0 before 7.*, from 7.0.0 before 7.3.1.3, from 6.1.2 before 6.1.*.

### CVE-2026-30803

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-06-17T18:17:43.410 |

Integer Underflow (Wrap or Wraparound) vulnerability in RTI Connext Micro (Core Libraries) allows Overread Buffers.This issue affects Connext Micro: from 4.0.0 before 4.3.0.

### CVE-2026-30802

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-17T18:17:43.263 |

Out-of-bounds Read vulnerability in RTI Connext Micro (Core Libraries) allows Overread Buffers.This issue affects Connext Micro: from 4.0.0 before 4.3.0.

### CVE-2026-35065

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T15:16:45.807 |

Dell PowerFlex Manager, version(s) [Versions], contain(s) a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Code execution, Denial of service, Information disclosure, Information tampering, Remote execution, Script injection, and Unauthorized access.

### CVE-2026-49268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:A/V:X/RE:L/U:Red` |
| Weaknesses | `CWE-90` |
| Published | 2026-06-17T14:17:56.903 |

A remote attacker can inject LDAP special characters into the Distinguished Name (DN) construction in DefaultLdapRealm class. User-supplied username input is directly concatenated into the LDAP DN template without any escaping of RFC 2253 special characters. This allows an attacker to manipulate the DN structure used for LDAP bind authentication, potentially bypassing authentication or impersonating other users.

This issue affects all Apache Shiro versions through 2.2.0, and 3.0.0-alpha-1 when using DefaultLdapRealm
Upgrade to Apache Shiro 2.2.1 or 3.0.0-alpha-2 or later, which fixes the issue.

### CVE-2025-69130

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:33.893 |

Subscriber PHP Object Injection in Entrepreneur - Booking for Small Businesses WordPress Theme <= 3.1.3 versions.

### CVE-2025-66391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T14:17:31.467 |

In Citrix Cloud through 2025-11-10, an account with read-only access can trigger the beginning of a workflow for write operations, e.g., the system will send a one-time password to an attacker-controlled email address when the attacker attempts to reset the password of a user account.

### CVE-2026-54805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:20:51.593 |

Subscriber Privilege Escalation in Falang multilanguage <= 1.4.2 versions.

### CVE-2026-42629

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-17T13:20:40.287 |

Unauthenticated Broken Authentication in PowerPack Pro for Elementor < v2.13.0 versions.

### CVE-2026-22342

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-17T13:20:08.990 |

Unauthenticated Cross Site Request Forgery (CSRF) in WordPress Dating Theme <= 11.2.0 versions.

### CVE-2026-12466

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-17T13:20:03.843 |

Heap buffer overflow in WebRTC in Google Chrome on Windows prior to 149.0.7827.155 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12452

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:00.670 |

Use after free in Downloads in Google Chrome on Android prior to 149.0.7827.155 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12448

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T13:20:00.180 |

Inappropriate implementation in WebView in Google Chrome on Android prior to 149.0.7827.155 allowed a remote attacker to perform privilege escalation via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12447

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-17T13:20:00.070 |

Heap buffer overflow in WebRTC in Google Chrome prior to 149.0.7827.155 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12443

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.520 |

Use after free in Web Authentication in Google Chrome prior to 149.0.7827.155 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-12442

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.410 |

Use after free in Passwords in Google Chrome on Android prior to 149.0.7827.155 allowed a remote attacker to execute arbitrary code via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-12441

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.293 |

Use after free in File Input in Google Chrome on Linux prior to 149.0.7827.155 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-12439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.080 |

Use after free in Digital Credentials in Google Chrome prior to 149.0.7827.155 allowed a remote attacker to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-12256

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:19:57.723 |

Contributor PHP Object Injection in Avada <= 3.15.3 versions.

### CVE-2026-12165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T13:19:57.433 |

The Contest Gallery – Upload & Vote Photos, Media, Sell with PayPal & Stripe plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 30.0.2 via the `RegistryUserRole` parameter. This is due to the plugin's admin menu being registered at the `edit_posts` capability level — granting Contributor-level users access to the plugin's admin pages and a valid `cg_admin` nonce — while the option-saving handler in `change-options-and-sizes.php` performs no `current_user_can()` capability check beyond `check_admin_referer('cg_admin')`, and the `RegistryUserRole` value is processed only through `sanitize_text_field()` and `htmlentities()` without restriction to an allowlist of permitted role names. This makes it possible for authenticated attackers, with author-level access and above, to overwrite the plugin's stored `RegistryUserRole` option with `administrator`, which the `cg_create_wp_user_from_google_user` function then reads back from the `contest_gal1ery_registry_and_login_options` database table without any allowlist validation and passes directly to `wp_update_user()`, effectively promoting a newly registered Google sign-in account to Administrator.

### CVE-2025-69138

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:19:19.293 |

Subscriber Privilege Escalation in Genemy <= 1.6.6 versions.

### CVE-2025-59563

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:19:15.057 |

Subscriber Privilege Escalation in Sonaar <= 4.27.4 versions.

### CVE-2026-46973

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:16.390 |

Vulnerability in the Oracle Outsourced Mfg for Discrete Industries product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Outsourced Mfg for Discrete Industries.  Successful attacks of this vulnerability can result in takeover of Oracle Outsourced Mfg for Discrete Industries. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46972

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:16.287 |

Vulnerability in the Oracle Outsourced Mfg for Discrete Industries product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Outsourced Mfg for Discrete Industries.  Successful attacks of this vulnerability can result in takeover of Oracle Outsourced Mfg for Discrete Industries. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46967

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:15.873 |

Vulnerability in the Oracle Public Sector Financials (International) product of Oracle E-Business Suite (component: Authorization).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Public Sector Financials (International).  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Financials (International). CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46965

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:15.673 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Work Provider Site Level Administration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks of this vulnerability can result in takeover of Oracle Universal Work Queue. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46962

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:15.360 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in takeover of Oracle Project Portfolio Analysis. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46961

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:15.260 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in takeover of Oracle Project Portfolio Analysis. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46952

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:14.430 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quality.  Successful attacks of this vulnerability can result in takeover of Oracle Quality. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:14.320 |

Vulnerability in the Oracle Quality product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Quality.  Successful attacks of this vulnerability can result in takeover of Oracle Quality. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46950

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:14.217 |

Vulnerability in the Oracle Advanced Outbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Outbound Telephony.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Outbound Telephony. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46947

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:14.010 |

Vulnerability in the Oracle Advanced Outbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Outbound Telephony.  Successful attacks of this vulnerability can result in takeover of Oracle Advanced Outbound Telephony. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46942

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.597 |

Vulnerability in the Oracle Process Manufacturing Process Planning product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Process Planning.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Process Planning. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.497 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Cost Planning).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46937

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.180 |

Vulnerability in the Oracle iSetup product of Oracle E-Business Suite (component: General Ledger Update Transform, Reports).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iSetup.  Successful attacks of this vulnerability can result in takeover of Oracle iSetup. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46931

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:11.493 |

Vulnerability in the Oracle Enterprise Asset Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.6-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Asset Management.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Asset Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46929

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:10.497 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Cost Planning).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46928

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:10.387 |

Vulnerability in the Oracle Spares Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Spares Management.  Successful attacks of this vulnerability can result in takeover of Oracle Spares Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46926

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:10.177 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:09.863 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46916

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:09.450 |

Vulnerability in the Oracle Process Manufacturing Product Development product of Oracle E-Business Suite (component: Quality Management Specs).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Product Development.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Product Development. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46903

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-287;CWE-306` |
| Published | 2026-06-17T10:54:08.063 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Business Logic Infrastructure Security).  Supported versions that are affected are 9.2.0.0-9.2.26.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46886

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:06.287 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46885

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:06.183 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: EAI).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46864

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:04.070 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via SSH to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:53:55.570 |

Vulnerability in the WebCenter Content: Imaging product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebCenter Content: Imaging.  Successful attacks of this vulnerability can result in takeover of WebCenter Content: Imaging. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35325

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.720 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35324

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.620 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35322

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.410 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35318

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:40:23.987 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:40:23.883 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:40:23.680 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35311

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:23.253 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebLogic Server.  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35303

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:22.410 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebLogic Server.  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35299

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.993 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise WebLogic Server.  Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35267

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:18.920 |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: REST WebServices).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Identity Manager.  Successful attacks of this vulnerability can result in takeover of Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35265

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:18.710 |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Identity Manager.  Successful attacks of this vulnerability can result in takeover of Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35259

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-06-17T10:40:18.280 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise WebLogic Server.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-0164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-06-16T20:16:26.790 |

In Modem, there is a possible out of bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0162

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-06-16T20:16:26.697 |

In ParsePayloads of AudioSdpParser.cpp, there is a possible memory corruption due to type confusion. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0161

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-06-16T20:16:26.610 |

In numberOfReportBlocks of RtpSession.cpp, there is a possible out of bounds write due to an integer overflow. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0160

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-16T20:16:26.517 |

In TextRtpPayloadDecoderNode::DecodeT140 of TextRtpPayloadDecoderNode.cpp, there is a possible out of bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0154

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-16T20:16:26.063 |

In Modem, there is a possible way to trigger a modem crash during a SIP REFER request due to memory corruption. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0151

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-06-16T20:16:25.793 |

In IntfGraphCreate of intfgraph.c, there is a possible out of bounds write due to an integer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-06-16T20:16:25.620 |

In RtpSession::rtpSendRtcpPacket, there is a possible OOB write due to a heap buffer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0148

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-06-16T20:16:25.530 |

In multiple functions of VideoRtpPayloadDecoderNode.cpp, there is a possible out of bounds write due to an integer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0147

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-06-16T20:16:25.440 |

In __mfc_core_nal_q_get_dec_metadata_sei_nal of mfc_core_nal_q.c, there is a possible out of bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0146

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-06-16T20:16:25.350 |

In mfc_core_get_dec_metadata_sei_nal of mfc_core_reg_api.c, there is a possible out of bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0139

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-06-16T20:16:24.730 |

In Modem, there is a possible out of bounds write due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0132

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-16T20:16:24.080 |

In Modem, there is a possible out of bounds write due to a heap buffer overflow. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-44932

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-16T17:16:40.953 |

Passing of unsanitized strings from DHCP replies into the wicked dhcp client before wicked 0.6.79 could be used by attackers operating a malicious DHCP server to execute code on the local machine.

### CVE-2024-24909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-06-16T17:16:28.303 |

Dell OpenManage Integration with Microsoft Windows Admin Center contains a Remote Code Execution vulnerability in the gateway plugin. A remote authenticated user could potentially exploit this vulnerability to escalate privileges. The malicious user may gain the ability to run arbitrary code remotely. This is a high severity vulnerability so Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-0647

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-16T15:16:33.687 |

An improper authentication security issue exists within the 1794-AENTR adapter's embedded web server. The vulnerability allows an unauthenticated attacker to change the device's web interface password by sending a crafted HTTP GET request to a specific endpoint, without any prior authentication being required. If exploited, this could lead to unauthorized access, account takeover, and loss of the device’s embedded web server’s availability.

### CVE-2026-53869

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T19:18:10.743 |

Hermes Agent before 0.16.0 contains a DNS rebinding vulnerability in WebSocket endpoints that allows remote attackers to bypass Host and Origin validation. FastAPI HTTP middleware does not execute for WebSocket upgrade requests on /api/pty, /api/ws, /api/pub, and /api/events endpoints, enabling attackers to exploit DNS rebinding and inject malicious commands or read terminal output.

### CVE-2026-53872

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T17:17:25.473 |

picklescan before 0.0.35 contains an unsafe pickle deserialization vulnerability allowing unauthenticated attackers to read arbitrary server files by chaining io.FileIO and urllib.request.urlopen. Attackers can bypass RCE-focused blocklists to exfiltrate sensitive data like /etc/passwd to external servers.

### CVE-2025-71322

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-06-17T17:16:40.980 |

PickleScan before 0.0.33 fails to include the pty.spawn function in its unsafe globals list, allowing attackers to bypass security checks. Malicious actors can craft pickle payloads using pty.spawn to achieve arbitrary code execution when files are processed by PickleScan.

### CVE-2026-55738

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-170` |
| Published | 2026-06-17T14:18:00.057 |

A stack-based buffer overflow exists in the raw_to_header() function in src/microtar.c in rxi microtar 0.1.0. The function copies the 100-byte name and linkname fields of a TAR header with strcpy() without guaranteeing null termination of the source. The POSIX ustar format permits these fixed-width fields to be fully populated with non-null bytes, so a crafted archive whose linkname field (followed by the trailing padding of the 512-byte raw header) contains no null terminator causes strcpy() to read past the end of the 512-byte raw header stack buffer and to write past the destination header buffer. A remote attacker who supplies a crafted TAR archive that the victim opens or parses (via mtar_open(), mtar_read_header(), or mtar_find()) can cause an out-of-bounds read and a stack buffer overflow, resulting in denial of service (crash) and potentially arbitrary code execution. Confirmed with AddressSanitizer: stack-buffer-overflow READ of size 356 in raw_to_header at src/microtar.c:112.

### CVE-2026-54417

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-835` |
| Published | 2026-06-17T14:17:58.540 |

An integer overflow in the mtar_next() function in src/microtar.c in rxi microtar 0.1.0 allows a remote attacker to cause a denial of service (uncontrolled CPU consumption / infinite loop) via a crafted tar archive. mtar_next() computes the offset to the next record as round_up(h.size, 512) + sizeof(mtar_raw_header_t) using 32-bit arithmetic. When the header size field is a multiple of 512 in the range 0xFFFFFC01-0xFFFFFE00 (e.g. 0xFFFFFE00), the addition wraps to 0, so mtar_next() seeks to the current record position instead of advancing. As a result, mtar_find() and any loop that iterates entries with mtar_next() repeat indefinitely over the same record, hanging the process at 100% CPU with no recovery.

### CVE-2026-46808

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:58.467 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-46804

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `NVD-CWE-noinfo;CWE-269` |
| Published | 2026-06-17T10:53:58.053 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-35271

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:19.343 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Weblogic).  Supported versions that are affected are 8.61 and  8.62. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PT PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PT PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PT PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PT PeopleTools accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-35258

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-06-17T10:40:17.287 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise WebLogic Server.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all WebLogic Server accessible data as well as  unauthorized access to critical data or complete access to all WebLogic Server accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-53843

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-06-16T19:17:01.257 |

OpenClaw before 2026.5.26 contains an authorization bypass vulnerability where a surviving pairing-scoped device session can re-establish node token authority after revocation. Attackers with a paired device can regain WebSocket node-level access without renewed approval, weakening revocation controls and maintaining unauthorized access longer than intended.

### CVE-2026-11317

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-404` |
| Published | 2026-06-16T15:16:34.607 |

A denial of service security issue exists in the
affected product. The security issue stems from a fault occurring when a
crafted CIP message is sent. Devices with less memory are more likely to be
affected. This can result in a major nonrecoverable fault (MNRF). A program
download is required to recover.

### CVE-2026-0646

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-06-16T15:16:33.567 |

A denial-of-service security issue exists within the 1794-AENTR adapter due to improper memory handling of CIP protocol requests. This vulnerability can result in the adapter faulting and losing connection to its associated I/O modules, requiring a manual reset to recover.

### CVE-2025-11694

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-06-16T15:16:32.693 |

A security issue exists within 1769 CompactLogix controllers due to the missing validation of sequence numbers and source IP addresses in the CIP protocol. This allows attacker to abuse the exposed Connection ID’s visible on the web interface to perform denial-of-service attacks, resulting in a minor fault.

### CVE-2026-50107

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-06-17T20:17:23.960 |

When NGINX Plus or NGINX Open Source is configured as the data plane for NGINX Gateway Fabric, an injection vulnerability exists in the NGINX configuration generator component of NGINX Gateway Fabric. User-supplied string values from the NginxProxy Custom Resource Definition (CRD) access log format setting are rendered directly into NGINX configuration templates without sanitization or escaping. An authenticated attacker with permission to create or modify these CRDs may craft values that inject arbitrary NGINX configuration directives. This is a control plane issue; there is no data plane exposure from the vulnerability trigger itself. 


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-11407

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-06-17T20:16:48.690 |

Pimcore CMS/DXP version 12.3.8 contains a sandbox bypass vulnerability that allows authenticated administrative attackers to execute arbitrary methods on PHP objects by exploiting empty checkMethodAllowed() and checkPropertyAllowed() implementations in the custom Twig SecurityPolicy. Attackers can supply malicious Twig templates through the DataObject ClassDefinition Layout\Text component to perform arbitrary file reads, execute arbitrary database queries, and potentially achieve remote code execution via PHP object gadget chains, with the pimcore_* function wildcard further broadening the bypass to all Pimcore Twig functions.

### CVE-2026-53871

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-06-17T19:18:11.023 |

Hermes WebUI before 0.51.368 contains an authorization bypass vulnerability in the get_profile_cookie() function that accepts unauthenticated profile names from the hermes_profile cookie. An authenticated attacker can forge the hermes_profile cookie value to bypass profile-scoped authorization checks and access sessions, files, and resources across different profiles.

### CVE-2026-54415

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-06-17T15:17:00.763 |

Missing Authorization in the server management routes (routes/admin.php) in Azuriom Azuriom CMS before 1.2.11 on all platforms allows an authenticated attacker with the admin.access permission to create AzLink server tokens and take over non-admin user accounts by changing their passwords and email addresses via crafted HTTP requests to /admin/servers/create and the AzLink API endpoints (/api/azlink/password, /api/azlink/email, /api/azlink/user/{id}).

### CVE-2026-11311

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-06-17T15:16:42.617 |

When NGINX Plus is configured as the data plane for NGINX Gateway Fabric, an injection vulnerability exists in the NGINX configuration generator component of NGINX Gateway Fabric. User-supplied string values from the NginxProxy Custom Resource Definition serverTokens field and the AuthenticationFilter Custom Resource Definition extraAuthArgs field are rendered directly into NGINX configuration templates without sanitization or escaping. An authenticated attacker with permission to create or modify these Custom Resource Definitions may craft values that inject arbitrary NGINX configuration directives. This is a control plane issue; there is no data plane exposure from the vulnerability trigger itself. 


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2025-69128

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T14:17:33.607 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in EMV JobCareer allows Path Traversal.

This issue affects JobCareer: from n/a through 7.3.

### CVE-2026-53876

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-17T13:20:49.537 |

RadiX AX6600 WiFi 6 Tri-Band Gaming Router contains an OS command injection vulnerability, which may lead to arbitrary command execution with the root privilege by a user who logs in to the web console as an administrator.

### CVE-2026-27400

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:20:12.753 |

Unauthenticated Arbitrary File Deletion in BookPro <= 1.1.0 versions.

### CVE-2026-22343

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:09.130 |

Unauthenticated Broken Access Control in WordPress Dating Theme <= 11.2.0 versions.

### CVE-2025-69139

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:19:19.423 |

Unauthenticated Arbitrary File Deletion in Car Zone <= 3.7 versions.

### CVE-2026-46776

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:55.157 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Unified Directory accessible data as well as  unauthorized read access to a subset of Oracle Unified Directory accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Unified Directory. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-22312

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-16T20:16:28.590 |

The device has a webserver that exposes a REST API authenticated with a constant token. The unauthenticated API can be used by an attacker to get access to system settings, modify the configuration
and execute some commands (e.g. system reboot).

### CVE-2026-53857

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-16T19:17:03.180 |

OpenClaw before 2026.5.3 contains a policy enforcement vulnerability where Zalo contacts with mutable display metadata could match allowFrom policy entries through display name changes. Attackers with mutable display names could receive agent responses intended for different Zalo identities when the feature is enabled.

### CVE-2026-53849

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-16T19:17:02.053 |

OpenClaw before 2026.5.7 contains a privilege escalation vulnerability where the allowFrom feature improperly validates Discord account identity using mutable display names instead of immutable user IDs. Attackers with Discord accounts can change their display name to match a policy entry and gain unauthorized agent access intended for another Discord identity.

### CVE-2026-10748

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-16T19:16:30.607 |

An authenticated user with the nx-licensing-create privilege can upload a specially crafted license file to execute arbitrary operating system commands as the Nexus process user in Sonatype Nexus Repository 3 versions before 3.92.0.

### CVE-2026-42089

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-16T17:16:40.740 |

Yeoman Environment provides an API to discover, create, and run generators, and to configure where and how a generator is resolved. Versions 2.9.0 through 6.0.0 install missing local generator packages from caller-supplied package names without user confirmation. In downstream consumers that pass attacker-controlled project configuration into this path, this can result in arbitrary package installation and code execution during CLI bootstrap. The vulnerable method is installLocalGenerators(), which calls repository.install() directly without prompting the user. This issue has been fixed in version 6.0.0.

### CVE-2026-10649

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-16T17:16:30.773 |

A flaw was found in Pacemaker. An unauthenticated remote attacker can exploit an integer overflow vulnerability in the remote message decompression process. By sending a specially crafted compressed remote message before authentication, an attacker can cause memory corruption, leading to a denial of service (DoS) in the CIB remote listener. This can result in the affected service crashing.

### CVE-2025-71261

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-16T17:16:30.193 |

An attacker with network-level access between the SUSE Virtualization 
and Rancher Manager in SUSE Harvester before 1.8.0 could interfere with the TLS handshake and abuse it 
to bypass TLS as a security control.

### CVE-2026-54818

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:59.780 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in VeronaLabs Slimstat Analytics allows Blind SQL Injection.

This issue affects Slimstat Analytics: from n/a through 5.4.11.

### CVE-2026-54813

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T14:17:59.010 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Brainstorm Force SureDash allows Blind SQL Injection.

This issue affects SureDash: from n/a through 1.8.0.

### CVE-2026-54185

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:49.817 |

Subscriber SQL Injection in Cornerstone < 7.8.8 versions.

### CVE-2026-49113

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T13:20:46.563 |

Subscriber Arbitrary Code Execution in Cornerstone < 7.8.8 versions.

### CVE-2026-49073

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:45.397 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in wpWax Directorist Booking allows Blind SQL Injection.

This issue affects Directorist Booking: from n/a through 3.0.3.

### CVE-2026-48967

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:44.683 |

Subscriber SQL Injection in  Geo Mashup <= 1.13.19 versions.

### CVE-2026-22335

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:20:08.360 |

Subscriber SQL Injection in WooCommerce Frontend Manager – Ultimate < 6.7.7 versions.

### CVE-2026-11410

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-17T13:19:33.340 |

An authenticated OS command injection vulnerability exists in the BigPond Cable (BPA) WAN configuration module in TL-WR940N v6 due to improper sanitization of user input. An attacker with administrative access may exploit this issue to execute arbitrary system commands with elevated privileges.

### CVE-2026-11409

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-17T13:19:33.187 |

An authenticated OS command injection vulnerability exists in the IPv6 PPPoE configuration handler in TL-WR940N v6 due to improper sanitization of user input. An attacker with administrative access may exploit this issue to execute arbitrary system commands with elevated privileges.

### CVE-2025-69135

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:19:18.903 |

Subscriber SQL Injection in Events Schedule - WordPress Events Calendar Plugin <= 2.7.2 versions.

### CVE-2026-46915

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:09.340 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Production).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  While the vulnerability is in Oracle Complex Maintenance, Repair and Overhaul, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46870

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:04.697 |

Vulnerability in the MySQL Shell product of Oracle MySQL (component: Shell for VS Code).   The supported version that is affected is 2026.2.0+9.6.1. Difficult to exploit vulnerability allows low privileged attacker with network access via multiple protocols to compromise MySQL Shell.  While the vulnerability is in MySQL Shell, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of MySQL Shell. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2025-26240

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-17T17:16:38.383 |

In JazzCore python-pdfkit 1.0.0, the from_string method enables the execution of JavaScript code within the context of the server application and the exfiltration of local files.

### CVE-2026-11858

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:33.807 |

Quanos SCHEMA ST4 on-premises contains a local privilege escalation vulnerability in the Client Update Service. The update service runs as NT AUTHORITY\SYSTEM and exposes a .NET Remoting interface over a named pipe without sufficient access controls or authorization. A local authenticated low-privileged user can connect to the interface and invoke privileged update methods such as Update(). This allows arbitrary file write and delete operations with SYSTEM privileges and can be used to achieve local privilege escalation.

### CVE-2026-11857

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:19:33.650 |

Quanos SCHEMA ST4 on-premises contains a local privilege escalation vulnerability in the Client Update Service due to insecure deserialization in the .NET Remoting service. The service is configured with TypeFilterLevel.Full and is bound to local interfaces only through named pipes. A local authenticated attacker can connect to the local named pipe, obtain the .NET Remoting endpoint, and send specially crafted serialized objects. Successful exploitation results in arbitrary code execution in the context of the update process with NT AUTHORITY\SYSTEM privileges. Network-only exploitation is not possible and local host access with an authenticated user session is required.

### CVE-2026-46788

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:56.393 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-35272

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:40:19.453 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Deployment Package).  Supported versions that are affected are 8.61 and  8.62. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where PeopleSoft Enterprise PT PeopleTools executes to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 8.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-9591

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-17T14:18:00.227 |

Cross-site request forgery (CSRF) in NewsItemApiController in SimplCommerce prior to commit 6233d73e allows an unauthenticated remote attacker to create or modify news items as an administrator via a crafted form submitted to `/api/news-items`, due to missing anti-CSRF protection.

### CVE-2026-12468

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-06-17T13:20:04.070 |

Race in Updater in Google Chrome on Mac prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12467

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:03.960 |

Use after free in Extensions in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12465

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-17T13:20:03.727 |

Object lifecycle issue in Metrics in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12464

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:03.607 |

Use after free in Browser in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12454

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-06-17T13:20:00.953 |

Race in Safe Browsing in Google Chrome on Mac prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12451

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:00.560 |

Use after free in DigitalCredentials in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12438

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-06-17T13:19:58.980 |

Inappropriate implementation in WebView in Google Chrome on Android prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-12437

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:58.863 |

Use after free in WebShare in Google Chrome on Windows prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2024-32949

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:11.650 |

Missing Authorization vulnerability in Prince Integrate Google Drive allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Integrate Google Drive: from n/a through 1.3.8.

### CVE-2026-46925

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:10.073 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 17.0-26.5. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35302

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-06-17T10:40:22.307 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 12.2.1.4.0 and  14.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise WebLogic Server.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of WebLogic Server. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-35262

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:18.493 |

Vulnerability in the Oracle Data Integrator product of Oracle Fusion Middleware (component: Market Place).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Data Integrator.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Data Integrator accessible data as well as  unauthorized access to critical data or complete access to all Oracle Data Integrator accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Data Integrator. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2025-14272

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-16T15:16:33.000 |

A security issue was identified in Pavilion due to improper authorization enforcement in API endpoints. This vulnerability can allow an unauthorized actor to execute privileged operations, including user/role management and other administrative actions.

### CVE-2026-55199

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-06-17T20:17:28.520 |

libssh2 through 1.11.1, fixed in commit 1762685, contains a pre-authentication denial of service vulnerability in the SSH_MSG_EXT_INFO handler in src/packet.c that allows a malicious SSH server to cause a client CPU exhaustion loop by sending a crafted extension count value. A malicious server can set nr_extensions to 0xFFFFFFFF during key exchange, causing the client to spin in a tight CPU loop for over 60 seconds because return values from _libssh2_get_string() are unchecked and the session timeout does not apply to CPU-bound loops.

### CVE-2026-54184

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-17T13:20:49.677 |

Unauthenticated Insecure Direct Object References (IDOR) in Clean Login <= 1.15 versions.

### CVE-2026-49081

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:46.200 |

Unauthenticated Broken Access Control in User Registration Stripe <= 1.3.12 versions.

### CVE-2026-48788

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-436` |
| Published | 2026-06-17T13:20:43.490 |

Remark42 is a self-hosted comment engine for blogs, articles, or any other place where readers can add comments. Versions 1.6.0 through 1.15.0 contain a Cross-Site Scripting (XSS) vulnerability exploitable through content-type spoofing. The Remark42 image proxy fetches an arbitrary remote URL and re-serves the response from Remark42's own origin. During the download phase, the proxy determines whether the resource is an image by inspecting only the Content-Type header advertised by the remote server, never examining the actual bytes; during the serving phase, it instead derives the response Content-Type by sniffing those bytes with http.DetectContentType. An attacker can exploit this inconsistency by hosting a URL that advertises Content-Type: image/png while returning an HTML/JavaScript body: the download check accepts it as an image, the serving path sniffs the body and emits Content-Type: text/html, and the browser renders the attacker-controlled HTML/JavaScript as a document within Remark42's origin. Exploitation requires no Remark42 account on the target instance; the attacker only needs to host the malicious upstream URL and deliver the proxy link to a victim by any means, such as email, direct message, or a link on another website. This issue has been fixed in version 1.16.0.

### CVE-2026-40726

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:35.560 |

Unauthenticated Broken Access Control in User Registration Stripe <= 1.3.14 versions.

### CVE-2026-46866

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-400` |
| Published | 2026-06-17T10:54:04.270 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Enterprise Manager Base Platform as well as  unauthorized update, insert or delete access to some of Oracle Enterprise Manager Base Platform accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-46865

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:04.170 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Extensibility Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Enterprise Manager Base Platform executes to compromise Oracle Enterprise Manager Base Platform.  While the vulnerability is in Oracle Enterprise Manager Base Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46806

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-06-17T10:53:58.260 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-35288

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:40:21.013 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Deployment Package).  Supported versions that are affected are 8.61 and  8.62. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PT PeopleTools executes to compromise PeopleSoft Enterprise PT PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PT PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-35274

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:19.663 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Deployment Package).  Supported versions that are affected are 8.61 and  8.62. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PT PeopleTools accessible data as well as  unauthorized update, insert or delete access to some of PeopleSoft Enterprise PT PeopleTools accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-48780

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-16T15:16:41.640 |

Forem is open source software for building communities. Prior to commit a2ab6d4, a maliciously crafted email address could allow an attacker to bypass domain allowlist or denylist restrictions and gain access to invite-only forem deployments. The issue is patched as of `a2ab6d4`. As a workaround, some SMTP servers and email delivery providers may drop or refuse to send maliciously crafted email addresses.

### CVE-2026-32804

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-17T15:16:45.663 |

Dell PowerFlex Manager, version(s) [Versions], contain(s) an Improper Authentication vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-54814

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:59.230 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in StylemixThemes Motors allows PHP Local File Inclusion.

This issue affects Motors: from n/a through 1.4.109.

### CVE-2026-52707

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-06-17T14:17:57.053 |

Unauthenticated Local File Inclusion in Kastell <= 2.0 versions.

### CVE-2026-40757

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:52.600 |

Unauthenticated PHP Object Injection in Château <= 1.2.1 versions.

### CVE-2026-40756

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:52.480 |

Unauthenticated PHP Object Injection in Zoya <= 1.4 versions.

### CVE-2026-40752

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:52.360 |

Unauthenticated PHP Object Injection in Manufaktur Solutions <= 1.1.1 versions.

### CVE-2026-40738

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:52.233 |

Unauthenticated PHP Object Injection in Eldon <= 1.4.1 versions.

### CVE-2026-40733

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:52.107 |

Unauthenticated PHP Object Injection in ShiftUp <= 1.3 versions.

### CVE-2026-39590

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:51.720 |

Unauthenticated Local File Inclusion in Atomlab <= 2.4.5 versions.

### CVE-2026-39576

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:51.593 |

Unauthenticated PHP Object Injection in SingleMalt <= 1.5 versions.

### CVE-2026-39560

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:51.463 |

Unauthenticated PHP Object Injection in Hiroshi <= 1.5.1 versions.

### CVE-2026-39559

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:51.343 |

Unauthenticated Local File Inclusion in Uppercase < 1.2.2 versions.

### CVE-2026-39556

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:51.217 |

Unauthenticated PHP Object Injection in Konsept <= 1.9 versions.

### CVE-2026-39523

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:50.983 |

Unauthenticated Local File Inclusion in Solene Core <= 2.3.2 versions.

### CVE-2026-39445

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:50.847 |

Unauthenticated PHP Object Injection in Alukas < 3.0.0 versions.

### CVE-2026-39442

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T14:17:50.690 |

Unauthenticated PHP Object Injection in PressMart <= 1.2.26 versions.

### CVE-2025-69175

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:35.790 |

Unauthenticated Local File Inclusion in Line Agency <= 1.3.1 versions.

### CVE-2025-69174

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:35.630 |

Unauthenticated Local File Inclusion in Etude <= 1.6 versions.

### CVE-2025-69170

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:35.220 |

Unauthenticated Local File Inclusion in Eventicity <= 1.5 versions.

### CVE-2025-69166

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:35.070 |

Unauthenticated Local File Inclusion in Gunslinger <= 1.7 versions.

### CVE-2025-69164

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:34.923 |

Unauthenticated Local File Inclusion in Skyward <= 1.10 versions.

### CVE-2025-69158

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:34.777 |

Unauthenticated Local File Inclusion in Granola <= 1.13 versions.

### CVE-2025-69157

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:34.617 |

Unauthenticated Local File Inclusion in Gamic <= 1.15 versions.

### CVE-2025-69144

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:34.340 |

Unauthenticated Local File Inclusion in Preservation <= 1.10 versions.

### CVE-2025-69126

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:33.170 |

Unauthenticated Local File Inclusion in Fortius <= 2.3.0 versions.

### CVE-2025-69123

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:32.927 |

Unauthenticated Local File Inclusion in Snow Club <= 1.1 versions.

### CVE-2025-69120

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:32.470 |

Unauthenticated Local File Inclusion in Dazzle <= 1.0.0 versions.

### CVE-2025-69115

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:32.283 |

Unauthenticated Local File Inclusion in LuxMed | Medicine & Healthcare Doctor WordPress Theme <= 1.2.2 versions.

### CVE-2025-69106

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T14:17:31.797 |

Unauthenticated Local File Inclusion in Imba <= 1.5.0 versions.

### CVE-2026-40761

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:37.687 |

Unauthenticated PHP Object Injection in Valeska <= 1.2.2 versions.

### CVE-2026-40760

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:37.547 |

Unauthenticated PHP Object Injection in Behold <= 1.5 versions.

### CVE-2026-40759

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:37.417 |

Unauthenticated PHP Object Injection in Esmée <= 1.4 versions.

### CVE-2026-40758

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:37.287 |

Unauthenticated PHP Object Injection in Léonie <= 1.2.1 versions.

### CVE-2026-40755

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:37.127 |

Unauthenticated PHP Object Injection in TechLink <= 1.3 versions.

### CVE-2026-40754

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:36.993 |

Unauthenticated PHP Object Injection in Roisin <= 1.4 versions.

### CVE-2026-40753

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:36.867 |

Unauthenticated PHP Object Injection in EasyMeals <= 1.5.1 versions.

### CVE-2026-40751

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:36.730 |

Unauthenticated PHP Object Injection in Ashtanga <= 1.2 versions.

### CVE-2026-40739

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:36.080 |

Unauthenticated PHP Object Injection in LuxeDrive <= 1.4 versions.

### CVE-2026-40736

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:35.943 |

Unauthenticated PHP Object Injection in Laurits <= 1.5.1 versions.

### CVE-2026-40735

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:35.823 |

Unauthenticated PHP Object Injection in Reina <= 2.1 versions.

### CVE-2026-40731

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:35.700 |

Unauthenticated Local File Inclusion in ChapterOne <= 1.7 versions.

### CVE-2026-39582

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:21.397 |

Unauthenticated Local File Inclusion in Hitek < 1.8.3 versions.

### CVE-2026-39580

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:21.263 |

Unauthenticated PHP Object Injection in Micdrop <= 1.3.1 versions.

### CVE-2026-39573

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:20.840 |

Unauthenticated PHP Object Injection in Mildhill <= 1.5 versions.

### CVE-2026-39568

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:20.703 |

Unauthenticated Local File Inclusion in Mr. SEO <= 2.0 versions.

### CVE-2026-39567

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:20.567 |

Unauthenticated PHP Object Injection in Santé <= 1.5.1 versions.

### CVE-2026-39558

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:20.443 |

Unauthenticated Local File Inclusion in Malmö <= 2.2 versions.

### CVE-2026-39557

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:20.310 |

Unauthenticated PHP Object Injection in NeoBeat <= 1.7 versions.

### CVE-2026-39554

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:20.173 |

Unauthenticated PHP Object Injection in Fidalgo <= 1.2.2 versions.

### CVE-2026-39549

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:20.043 |

Unauthenticated Local File Inclusion in Aperitif <= 1.5 versions.

### CVE-2026-39547

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:19.760 |

Unauthenticated Local File Inclusion in Getaway < 1.8 versions.

### CVE-2026-39545

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:19.490 |

Unauthenticated PHP Object Injection in Zermatt <= 1.6.1 versions.

### CVE-2026-39539

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:19.353 |

Unauthenticated PHP Object Injection in Alloggio - Hotel Booking <= 2.1.2 versions.

### CVE-2026-39537

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:19.210 |

Unauthenticated Local File Inclusion in Mikado Core <= 1.6 versions.

### CVE-2026-39522

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:18.597 |

Unauthenticated Local File Inclusion in Solene <= 3.4 versions.

### CVE-2026-39446

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:18.463 |

Unauthenticated PHP Object Injection in Kapee < 1.7.0 versions.

### CVE-2026-39443

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-17T13:20:18.327 |

Unauthenticated PHP Object Injection in EmallShop <= 2.4.21 versions.

### CVE-2026-34895

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:17.910 |

Unauthenticated Local File Inclusion in Softlab Core < 1.2.11 versions.

### CVE-2026-34894

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:17.760 |

Unauthenticated Local File Inclusion in Integrio Core < 1.2.8 versions.

### CVE-2026-34893

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:17.620 |

Unauthenticated Local File Inclusion in Thegov Core < 2.0.23 versions.

### CVE-2026-25439

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-17T13:20:11.343 |

Unauthenticated Broken Authentication in Booknetic <= 4.8.5 versions.

### CVE-2026-22338

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:08.490 |

Unauthenticated Local File Inclusion in EcoBlue <= 1.15 versions.

### CVE-2026-22331

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:07.940 |

Unauthenticated Local File Inclusion in AutoParts <= 1.5.8 versions.

### CVE-2026-22330

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:07.807 |

Unauthenticated Local File Inclusion in Right Way <= 4.0 versions.

### CVE-2026-22326

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:06.263 |

Unauthenticated Local File Inclusion in Reprizo <= 1.0.8 versions.

### CVE-2026-22325

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:06.133 |

Unauthenticated Local File Inclusion in Promo <= 1.3.0 versions.

### CVE-2025-69178

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:25.267 |

Unauthenticated Local File Inclusion in Truemag <= 4.3.14.2 versions.

### CVE-2025-69177

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:25.133 |

Unauthenticated Local File Inclusion in Roneous <= 2.1.5 versions.

### CVE-2025-69176

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:25.003 |

Unauthenticated Local File Inclusion in ITactics <= 1.0 versions.

### CVE-2025-69173

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.870 |

Unauthenticated Local File Inclusion in Tipsy <= 1.1 versions.

### CVE-2025-69172

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.743 |

Unauthenticated Local File Inclusion in Resurs <= 1.3 versions.

### CVE-2025-69171

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.610 |

Unauthenticated Local File Inclusion in Orpheus <= 1.3 versions.

### CVE-2025-69168

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.470 |

Unauthenticated Local File Inclusion in Spike <= 1.2 versions.

### CVE-2025-69167

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.337 |

Unauthenticated Local File Inclusion in Eros <= 1.3 versions.

### CVE-2025-69165

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.173 |

Unauthenticated Local File Inclusion in Choreo <= 1.6 versions.

### CVE-2025-69163

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:24.013 |

Unauthenticated Local File Inclusion in WineShop <= 3.17 versions.

### CVE-2025-69162

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:23.757 |

Unauthenticated Local File Inclusion in Grecko <= 5.17 versions.

### CVE-2025-69161

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:23.570 |

Unauthenticated Local File Inclusion in Snowy <= 1.13 versions.

### CVE-2025-69160

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:23.407 |

Unauthenticated Local File Inclusion in Gita <= 1.11 versions.

### CVE-2025-69159

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:23.247 |

Unauthenticated Local File Inclusion in Printo <= 1.11 versions.

### CVE-2025-69150

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:21.030 |

Unauthenticated Local File Inclusion in Medeus <= 1.14 versions.

### CVE-2025-69149

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:20.750 |

Unauthenticated Local File Inclusion in Top Dog <= 1.0.5 versions.

### CVE-2025-69148

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:20.437 |

Unauthenticated Local File Inclusion in Quirky <= 1.23 versions.

### CVE-2025-69147

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:20.237 |

Unauthenticated Local File Inclusion in Putter <= 1.17 versions.

### CVE-2025-69146

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:20.097 |

Unauthenticated Local File Inclusion in Dom <= 1.24 versions.

### CVE-2025-69145

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:19.973 |

Unauthenticated Local File Inclusion in Gat <= 1.16 versions.

### CVE-2025-69143

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:19.843 |

Unauthenticated Local File Inclusion in Mission <= 1.22 versions.

### CVE-2025-69142

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:19.710 |

Unauthenticated Local File Inclusion in Abelle <= 1.22 versions.

### CVE-2025-69141

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:19.560 |

Unauthenticated Local File Inclusion in Kelly Young <= 1.1.0 versions.

### CVE-2025-69136

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:19.027 |

Unauthenticated Local File Inclusion in Wanium <= 1.9.8 versions.

### CVE-2025-69125

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:18.467 |

Unauthenticated Local File Inclusion in Food Drop <= 1.3 versions.

### CVE-2025-69124

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:18.330 |

Unauthenticated Local File Inclusion in Especio <= 1.0 versions.

### CVE-2025-69121

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:18.053 |

Unauthenticated Local File Inclusion in Deliciosa <= 1.10.0 versions.

### CVE-2025-69119

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.920 |

Unauthenticated Local File Inclusion in Corbesier <= 1.15.0 versions.

### CVE-2025-69118

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.783 |

Unauthenticated Local File Inclusion in CopyPress <= 1.4.5 versions.

### CVE-2025-69117

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.647 |

Unauthenticated Local File Inclusion in Ingenioso <= 1.14.0 versions.

### CVE-2025-69116

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.517 |

Unauthenticated Local File Inclusion in Iona <= 1.0.8 versions.

### CVE-2025-69114

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.383 |

Unauthenticated Local File Inclusion in MaxiNet <= 1.2.10 versions.

### CVE-2025-69113

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.240 |

Unauthenticated Local File Inclusion in Nexio <= 1.10.0 versions.

### CVE-2025-69112

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:17.100 |

Unauthenticated Local File Inclusion in Planty <= 1.14.0 versions.

### CVE-2025-69110

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:16.947 |

Unauthenticated Local File Inclusion in AirSupply <= 2.0.0 versions.

### CVE-2025-69109

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:16.813 |

Unauthenticated Local File Inclusion in Raider Spirit <= 1.1.2 versions.

### CVE-2025-69107

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:16.550 |

Unauthenticated Local File Inclusion in Rosaleen <= 2.8 versions.

### CVE-2025-69105

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:16.413 |

Unauthenticated Local File Inclusion in Modernee <= 1.6.0 versions.

### CVE-2025-60085

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:15.317 |

Unauthenticated Local File Inclusion in Learnify <= 1.15.0 versions.

### CVE-2025-58954

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:14.793 |

Unauthenticated Local File Inclusion in HomeRoofer <= 2.11.0 versions.

### CVE-2025-58953

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:14.653 |

Unauthenticated Local File Inclusion in Joly <= 1.22.0 versions.

### CVE-2025-58952

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:14.527 |

Unauthenticated Local File Inclusion in Neuronet < 1.14.0 versions.

### CVE-2025-58924

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:14.387 |

Unauthenticated Local File Inclusion in Geya <= 1.15 versions.

### CVE-2026-46939

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.393 |

Vulnerability in the Oracle Configure to Order product of Oracle E-Business Suite (component: Supply to Order Workbench).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Configure to Order.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Configure to Order accessible data as well as  unauthorized access to critical data or complete access to all Oracle Configure to Order accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46927

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:10.283 |

Vulnerability in the Oracle Receivables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Receivables.  Successful attacks of this vulnerability can result in takeover of Oracle Receivables. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46920

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:09.763 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 17.0-26.5. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46898

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:07.530 |

Vulnerability in the Oracle Enterprise Command Center Framework product of Oracle E-Business Suite (component: Core).  Supported versions that are affected are V15 and  V16. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Enterprise Command Center Framework.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Command Center Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Enterprise Command Center Framework accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-46891

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:06.807 |

Vulnerability in the JD Edwards EnterpriseOne Accounts Payable product of Oracle JD Edwards (component: Accounts Payable).   The supported version that is affected is 9.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Accounts Payable.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Accounts Payable accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Accounts Payable accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-46851

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T10:54:02.700 |

Vulnerability in the PeopleSoft Enterprise CS Campus Community product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2.38. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Campus Community.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CS Campus Community. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46849

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:02.490 |

Vulnerability in the PeopleSoft Enterprise CS Student Financials product of Oracle PeopleSoft (component: Other).   The supported version that is affected is 9.2.38. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise CS Student Financials.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise CS Student Financials accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise CS Student Financials accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-35289

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.117 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Deployment Package).  Supported versions that are affected are 8.61 and  8.62. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35279

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:20.187 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Performance Monitor).  Supported versions that are affected are 8.61 and  8.62. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35276

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:19.873 |

Vulnerability in the PeopleSoft Enterprise PT PeopleTools product of Oracle PeopleSoft (component: Application Server).  Supported versions that are affected are 8.61 and  8.62. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PT PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PT PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-39598

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-17T13:20:22.090 |

Unrestricted Upload of File with Dangerous Type vulnerability in Kodezen LLC Academy LMS Pro allows Upload a Web Shell to a Web Server.

This issue affects Academy LMS Pro: from n/a before 3.5.2.

### CVE-2025-48640

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:14.040 |

In multiple locations, there is a possible 3rd party passkey entry pairing approval due to a missing permission check. This could lead to remote (proximal/adjacent) escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-46894

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352;CWE-601;CWE-640` |
| Published | 2026-06-17T10:54:07.113 |

Vulnerability in the Oracle iSupplier Portal product of Oracle E-Business Suite (component: Home Page).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle iSupplier Portal.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle iSupplier Portal. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-46796

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-601` |
| Published | 2026-06-17T10:53:57.210 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-46787

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-17T10:53:56.290 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-46848

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:02.383 |

Vulnerability in the WebLogic Server product of Oracle Fusion Middleware (component: Console).  Supported versions that are affected are 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where WebLogic Server executes to compromise WebLogic Server.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in WebLogic Server, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all WebLogic Server accessible data as well as  unauthorized access to critical data or complete access to all WebLogic Server accessible data. CVSS 3.1 Base Score 7.9 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-32652

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-06-17T17:16:45.103 |

Dell AIOps Collector versions prior to 1.18.3 contain a "Use of Default Credentials" vulnerability. A low privileged attacker with console access could potentially exploit this vulnerability to gain Filesystem access. This vulnerability only affects fresh installations of Collector versions earlier than 1.18.3. Systems that have been upgraded (either manually or automatically) to version 1.18.3 or later are not impacted, even if they were originally installed on an earlier version.

### CVE-2026-12449

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:00.277 |

Use after free in Chromoting in Google Chrome on Windows prior to 149.0.7827.155 allowed a local attacker to perform OS-level privilege escalation via a malicious file. (Chromium security severity: High)

### CVE-2026-0019

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T13:19:25.533 |

In SettingsLib, there is a possible way to disable system components due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2025-48643

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-17T13:19:14.140 |

In multiple locations there is a possible provisioning bypass due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2025-48617

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:13.940 |

In overrideConfig of CarrierConfigLoader.java, there is a possible way to bypass UID check due to a permissions bypass. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-46888

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:06.497 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Database Upgrade).  Supported versions that are affected are 17.0-26.5. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47750

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-16T20:16:44.413 |

stable-diffusion.cpp is a pure C/C++ library for running diffusion model (Stable Diffusion, Flux, Wan, Qwen Image, Z-Image, and more) inference. In versions prior to master-584-0a7ae07,  the pickle .ckpt parser in src/model.cpp contained a heap buffer overflow vulnerability in the GLOBAL opcode handler. The issue was caused by missing validation when searching for newline-delimited fields. A crafted .ckpt file without the expected newline could cause the parser to use -1 as a copy length, resulting in immediate heap corruption. The attack requires the victim or application to load a .ckpt file from an untrusted source, such as a downloaded model from a model sharing site. The issue has been resolved in version master-584-0a7ae07. If developers are unable to immediately update their applications they can work around this issue by following these instructions: do not load .ckpt checkpoint files from untrusted sources, and prefer trusted model sources and safer formats such as .safetensors where possible.

### CVE-2026-47747

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-06-16T20:16:44.163 |

stable-diffusion.cpp is a pure C/C++ library for running diffusion model (Stable Diffusion, Flux, Wan, Qwen Image, Z-Image, and more) inference. In versions prior to master-584-0a7ae07, the pickle .ckpt parser in src/model.cpp contained a heap buffer overflow vulnerability in the BINUNICODE opcode handler. The issue was caused by sign confusion on the opcode length field. A crafted .ckpt file could trigger memcpy with a very large length derived from a negative signed value, causing immediate heap corruption.
The issue has been resolved in version master-584-0a7ae07. If developers are unable to immediately update their applications they can work around this issue by only loading .ckpt checkpoint files from trusted sources and preferring trusted model sources and safer formats such as .safetensors where possible.

### CVE-2026-0153

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-16T20:16:25.970 |

In Write of msg_to_host_buffer.cc, there is a possible out of bounds write due to an incorrect bounds check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0152

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-06-16T20:16:25.883 |

In OSMMapPMRGeneric of pmr_os.c, there is a possible way to leverage a system call to system call to maliciously expand the VMA out of bounds due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0150

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-06-16T20:16:25.707 |

In ExecuteGraph command handler of EdgeTPU firmware, there is a possible out of bounds write due to an integer overflow. This could lead to local escalation of privilege with root privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0143

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-16T20:16:25.083 |

In lwis_device_external_event_emit of lwis_event.c, there is a possible memory corruption due to a use after free. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0138

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-06-16T20:16:24.623 |

In lwis_io_buffer_write of lwis_io_buffer.c, there is a possible out of bounds write due to memory corruption. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0137

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-16T20:16:24.527 |

In edgetpu_sync_fence_group_shutdown() of edgetpu-dmabuf.c, there is a possible elevation of privilege due to a use after free. This could lead to local escalation of privilege with System execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0135

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-16T20:16:24.350 |

In Modem, there is a possible out of bounds read due to a missing bounds check. This could lead to remote code execution with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-0133

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-16T20:16:24.170 |

In smmu_attach_dev of arm-smmu-v3.c, there is a possible way to sign malicious Android Runtime bootclass artifacts due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-50656

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-16T19:16:59.683 |

Microsoft is aware of an elevation of privilege in the Microsoft Malware Protection Engine in Microsoft Defender publicly referred to as &quot;RoguePlanet &quot;. We are working to provide a high quality security update that addresses this vulnerability. We will provide information in this CVE when the update is available.

### CVE-2026-47964

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-16T19:16:56.367 |

DNG SDK versions 1.7.1 2536 and earlier are affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-47749

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-06-16T19:16:55.867 |

stable-diffusion.cpp is a pure C/C++ library for running diffusion model (Stable Diffusion, Flux, Wan, Qwen Image, Z-Image, and more) inference. Versions prior to master-584-0a7ae07 are vulnerable to heap buffer overflow in SHORT_BINUNICODE parsing for PyTorch checkpoint files. The pickle .ckpt parser in src/model.cpp contained a heap buffer overflow vulnerability in the SHORT_BINUNICODE opcode handler. The issue was caused by sign confusion on the opcode length field. A crafted .ckpt file could trigger memcpy with a very large length derived from a negative signed value, causing immediate heap corruption. Any application using affected stable-diffusion.cpp releases to load untrusted .ckpt model files could be vulnerable. A malicious checkpoint file could cause heap corruption through memcpy with an attacker-controlled length. This may lead to process crash and could potentially be leveraged for code execution depending on heap layout. The attack requires the victim or application to load a .ckpt file from an untrusted source, such as a downloaded model from a model sharing site. The issue has been resolved in version master-584-0a7ae07. If developers are unable to immediately update their applications they can work around this issue by not loading .ckpt checkpoint files from untrusted sources, and referring to trusted model sources and safer formats such as .safetensors where possible.

### CVE-2026-24228

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-16T17:16:39.590 |

NVIDIA NeMo Framework for Linux contains a vulnerability where an attacker may cause deserialization of untrusted data. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, data tampering, and information disclosure.

### CVE-2026-24155

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-16T17:16:39.440 |

NVIDIA NeMo Framework for all platforms contains a code injection vulnerability. A successful exploit of this vulnerability might lead to code execution, escalation of privileges, information disclosure, and data tampering.

### CVE-2026-54193

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T14:17:58.383 |

Contributor Arbitrary File Deletion in Fusion Builder <= 3.15.4 versions.

### CVE-2025-60223

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:19:15.710 |

Subscriber Arbitrary File Deletion in WPBot Pro Wordpress Chatbot <= 13.6.5 versions.

### CVE-2026-47684

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-16T15:16:41.063 |

Sync-in Server is a secure, open-source platform for file storage, sharing, collaboration, and syncing. Prior to version 2.3.0, the private IP blocklist regex used in the URL download feature does not match IPv4-mapped IPv6 addresses (e.g. ::ffff:127.0.0.1), allowing SSRF protection to be bypassed on dual-stack systems. Version 2.3.0 fixes the issue.

### CVE-2026-54804

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-17T13:20:51.473 |

Subscriber Broken Authentication in Melhor Envio <= 2.16.3 versions.

### CVE-2026-39546

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-17T13:20:19.613 |

Subscriber Privilege Escalation in MultiLoca <= 4.2.15 versions.

### CVE-2026-35327

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.923 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-53866

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-16T19:17:05.023 |

OpenClaw before 2026.5.12 contains an allowlist bypass vulnerability in shell inline-command parsing that allows authenticated operators to execute unapproved commands. A command request using shell inline-command forms could route through a parser case missing the expected allowlist decision, enabling shell content execution without intended approval prompts.

### CVE-2026-53864

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-16T19:17:04.760 |

OpenClaw before 2026.5.26 contains an insufficient sanitization vulnerability in the host environment sanitizer that allows Node.js control variables to bypass validation. Attackers with access to workspace .env files, tool environment overrides, or skill environment blocks can pass malicious Node.js control variables to influence child processes or coverage output paths.

### CVE-2026-53855

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184;CWE-863` |
| Published | 2026-06-16T19:17:02.910 |

OpenClaw before 2026.4.2 contains an inline-eval bypass vulnerability allowing authenticated operators to weaken strict allowlist checks via shell positional parameters. Attackers can combine allowlisted tools with shell positional arguments to place inline-eval content in shell carriers outside intended allowlist rules, enabling execution of unapproved shell-provided content.

### CVE-2026-53853

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693;CWE-863` |
| Published | 2026-06-16T19:17:02.650 |

OpenClaw before 2026.5.12 contains an argument pattern validation bypass in the exec allowlist that allows attackers to execute disallowed arguments for allowlisted executables on Linux and macOS systems. Attackers can bypass configured argPattern restrictions by directly invoking allowlisted executables with unrestricted arguments, potentially enabling unauthorized file access, network access, or command execution.

### CVE-2026-48979

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-17T21:16:23.410 |

PHP Standard Library (PSL) is set of APIs covering async, collections, networking, I/O, cryptography, terminal UI, etc. In versions 6.1.0, 6.1.1 and 6.2.0, the Psl\H2\ServerConnection does not validate that the total bytes received in DATA frames match the content-length header declared in the HEADERS frame, allowing request smuggling. This is in violation of RFC 9113 §8.1.1. A malicious client is able to send more DATA bytes than declared, smuggling additional content past application-level size limits and send fewer DATA bytes than declared and close the stream early, causing applications that trust the declared length to behave incorrectly.
The vulnerability is only reachable for consumers using Psl\H2\ServerConnection directly to accept untrusted client traffic. Consumers of documented high-level PSL APIs are not affected. This issue has been fixed in versions 6.1.2 and 6.2.1.

### CVE-2026-10696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-06-17T20:16:47.670 |

Use of an incorrectly resolved name or reference in the pinget backend 
in Devolutions UniGetUI 2026.2.0 and earlier allows a WinGet community 
catalog contributor to cause an installed application to be correlated 
to an unrelated, attacker-controlled catalog package and to execute an 
attacker-controlled installer via a crafted catalog package whose 
normalized name is contained as a substring within the installed 
application name when a user applies the proposed update.

### CVE-2026-48818

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-17T19:18:09.807 |

Starlette is a lightweight ASGI framework/toolkit. In versions 1.0.1 and earlier, StaticFiles on Windows is vulnerable to SSRF. An UNC path such as \\attacker.com\share can cause os.path.realpath to initiate an outbound SMB connection before the path is rejected, exposing the service account’s NTLMv2 credentials for offline cracking or relay even though the HTTP response is only a 404. The issue affects default follow_symlink=False deployments, including frameworks built on Starlette such as FastAPI; POSIX systems and follow_symlink=True are unaffected. The issue is fixed in 1.1.0.

### CVE-2026-6734

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-06-17T18:18:05.617 |

Impact:
When using Socks5ProxyAgent, undici reuses a single connection pool across different origins without verifying that the pool's origin matches the requested origin. All requests are dispatched through the pool connected to the first origin, regardless of the intended destination.

This causes cross-origin request routing: credentials and request data intended for origin B are sent to origin A, responses from the wrong origin are trusted, and HTTPS requests may be silently downgraded to HTTP.

Impacted users are applications that use Socks5ProxyAgent (directly or via setGlobalDispatcher) and make requests to more than one origin.

This was introduced in undici 7.23.0 via PR #4385 and affects all versions through 8.1.0.

Patches:
Upgrade to undici v7.26.0 or v8.2.0.

Workarounds:
Use a separate Socks5ProxyAgent instance per origin, or avoid using Socks5ProxyAgent with multiple origins.

### CVE-2026-47774

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405;CWE-770` |
| Published | 2026-06-17T18:18:02.643 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to versions 1.35.11, 1.36.7, 1.37.3, and 1.38.1, a vulnerability in Envoy's HTTP/2 downstream request processing allows an unauthenticated remote client to trigger excessive memory consumption, potentially resulting in OOM termination of the Envoy process and denial of service. The issue arises from the combination of two behaviors. First, cookie header bytes are not fully accounted for during request header size validation in Envoy. Second, HPACK header block limits in oghttp2/quiche are enforced on encoded bytes without a corresponding limit on total decoded header size. Together, these behaviors allow a malicious client to cause large decoded header allocations while bypassing the intended request header size protections. Versions 1.35.11, 1.36.7, 1.37.3, and 1.38.1 contain a fix. No complete workaround is known short of applying a fix. Possible temporary mitigations include disabling downstream HTTP/2 where operationally feasible; enforcing stricter request header and cookie limits before traffic reaches Envoy; and monitoring Envoy memory usage for abnormal growth under HTTP/2 traffic.

### CVE-2026-9675

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-06-17T17:17:28.183 |

Impact:
The undici WebSocket client enforces maxPayloadSize per-frame but does not enforce the cumulative size of fragmented uncompressed messages. A malicious WebSocket server can stream many small fragments that each pass per-frame validation but collectively exceed the configured limit, causing unbounded memory growth in the client process. The result is memory exhaustion and a denial of service.

Affected applications are those using the undici WebSocket client (new WebSocket(...)) that can be induced to connect to an attacker-controlled or compromised WebSocket endpoint.

This is a regression specific to undici 8.1.0. The 6.25.0 line shipped the equivalent cumulative check from the start and is unaffected. The 7.x line never had the maxPayloadSize feature and is also unaffected.

Patches:
Upgrade to undici >= 8.5.0.

Workarounds:
No workaround is available. The fix must be applied through an upgrade.

### CVE-2026-20190

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-06-17T17:16:43.130 |

A vulnerability in Cisco ISE and ISE-PIC could allow an unauthenticated, remote attacker to view sensitive information on an affected device.

This vulnerability is due to improper authorization checks when a resource is accessed. An attacker could exploit this vulnerability by sending crafted traffic to an affected device. A successful exploit could allow the attacker to gain access to sensitive information, including hashed credentials that could be used in future attacks.

### CVE-2026-12151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-06-17T17:16:42.370 |

Impact:
The undici WebSocket client enforces maxPayloadSize on the cumulative byte count of fragments in a message but does not enforce a limit on the number of fragments. A malicious WebSocket server can stream many small or empty continuation frames that each pass per-frame and cumulative-size validation, collectively causing unbounded memory growth in the client process. The result is memory exhaustion and a denial of service.

Affected applications are those using the undici WebSocket client (new WebSocket(...)) or the WebSocketStream API that can be induced to connect to an attacker-controlled or compromised WebSocket endpoint.

All releases starting at undici 6.17.0 are affected.

Patches: Upgrade to undici >= 6.26.0, >= 7.28.0, or >= 8.5.0. Workarounds:
No workaround is available. The fix must be applied through an upgrade.

### CVE-2026-54810

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T15:17:01.240 |

Missing Authorization vulnerability in Nexi Payments Nexi XPay allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Nexi XPay: from n/a through 8.3.1.

### CVE-2026-22283

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-06-17T15:16:44.513 |

Dell PowerFlex Manager, version(s) Version prior to 4.8, contain(s) an Inclusion of Functionality from Untrusted Control Sphere vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Information disclosure.

### CVE-2026-54816

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-17T14:17:59.523 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Monetizemore Advanced Ads allows Remote Code Inclusion.

This issue affects Advanced Ads: from n/a through 2.0.21.

### CVE-2026-9690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:21:35.147 |

Unauthenticated Arbitrary File Download in WP Media folder Addon <= 4.0.1 versions.

### CVE-2026-54802

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:51.223 |

Unauthenticated Broken Authentication in SMS Alert Order Notifications <= 3.9.3 versions.

### CVE-2026-52696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1258` |
| Published | 2026-06-17T13:20:48.917 |

Unauthenticated Sensitive Data Exposure in JetBlog <= 2.4.8 versions.

### CVE-2026-49057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:20:44.850 |

Unauthenticated Broken Access Control in JobSearch <= 3.2.7 versions.

### CVE-2026-48929

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-17T13:20:44.550 |

Rocket.Chat in versions <8.5.1, <8.4.4, <8.3.6, <8.2.6, <8.1.6, <8.0.7, <7.13.9, and <7.10.13 is vulnerable to unauthenticated file deletion. The deleteFileMessage Meteor method permanently deletes any uploaded file by ID without requiring authentication. When called via an unauthenticated DDP WebSocket connection, Meteor.userId() returns null, causing the authorization check to be skipped. Execution falls through to FileUpload.getStore('Uploads').deleteById(fileID), which removes the file from storage and database unconditionally. File IDs are discoverable from public channel message payloads and download URLs.

### CVE-2026-48779

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-06-17T13:20:42.887 |

ws is an open source WebSocket client and server for Node.js. All versions from 1.1.0 up to (but not including) 5.2.5, from 6.0.0 up to 6.2.4, from 7.0.0 up to 7.5.11, and from 8.0.0 up to 8.21.0 are affected by a memory exhaustion DoS vulnerability. A peer can send a high volume of exceptionally small fragments and data chunks, with modest network traffic, to force the remote peer into allocating and holding structural wrappers that consume far more memory than the default documented message-size limit, leading to process termination due to OOM. This issue has been fixed in versions 5.2.5, 6.2.4, 7.5.11, and 8.21.0.

### CVE-2026-40721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:20:34.917 |

Contributor Local File Inclusion in Element Pack Pro <= 9.0.6 versions.

### CVE-2026-34888

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-17T13:20:17.493 |

Unauthenticated Sensitive Data Exposure in Bricksforge <= 3.1.8.4 versions.

### CVE-2026-22334

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:20:08.200 |

Subscriber Arbitrary File Download in Woocommerce Book Price <= 1.3 versions.

### CVE-2026-12462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:03.333 |

Use after free in Media in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who had compromised the renderer process to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12455

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:20:01.070 |

Use after free in Tab Strip in Google Chrome prior to 149.0.7827.155 allowed a remote attacker who convinced a user to engage in specific UI gestures to potentially exploit heap corruption via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12445

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-17T13:19:59.803 |

Use after free in Extensions in Google Chrome prior to 149.0.7827.155 allowed an attacker who convinced a user to install a malicious extension to potentially exploit heap corruption via a crafted Chrome Extension. (Chromium security severity: High)

### CVE-2026-12360

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-17T13:19:58.577 |

The JetEngine plugin for WordPress is vulnerable to SQL injection in all versions up to and including 3.8.10.1. The listing_load_more AJAX handler accepts a filtered_query parameter that is intentionally excluded from the HMAC query signature check to support front-end filter integration. However, meta_query row values within filtered_query are not sanitized before being merged into SQL construction. This makes it possible for unauthenticated attackers to perform time-based or boolean blind SQL injection by appending a malicious meta_query value to a Load More AJAX request captured from any public Listing Grid page.

### CVE-2026-12199

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T13:19:57.573 |

A vulnerability in `nltk.app.wordnet_app` up to version 3.9.3 allows unauthenticated remote shutdown of the local WordNet Browser HTTP server when started in its default mode. The server listens on all interfaces and processes a specific unauthenticated GET request (`/SHUTDOWN%20THE%20SERVER`) to terminate the process immediately via `os._exit(0)`. This results in a denial of service, impacting service availability. The issue arises due to insufficient authentication and protection mechanisms for critical server functions.

### CVE-2025-69131

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:19:18.767 |

Unauthenticated Arbitrary File Download in WordPress & WooCommerce Scraper Plugin, Import Data from Any Site <= 1.0.7 versions.

### CVE-2025-69103

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T13:19:16.127 |

Subscriber Arbitrary Content Deletion in Brikk <= 3.0.0 versions.

### CVE-2025-49403

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-17T13:19:14.243 |

Unauthenticated Arbitrary File Download in Premium Age Verification / Restriction for WordPress <= 3.0.2 versions.

### CVE-2024-32729

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T13:19:11.510 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in QuantumCloud Conversational Forms for ChatBot allows Path Traversal.

This issue affects Conversational Forms for ChatBot: from n/a through 1.1.8.

### CVE-2026-46974

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:16.493 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.8. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46971

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284` |
| Published | 2026-06-17T10:54:16.187 |

Vulnerability in the Oracle HR Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle HR Intelligence.  Successful attacks of this vulnerability can result in takeover of Oracle HR Intelligence. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46966

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:15.773 |

Vulnerability in the Oracle Universal Work Queue product of Oracle E-Business Suite (component: Work Provider Site Level Administration).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Universal Work Queue.  Successful attacks of this vulnerability can result in takeover of Oracle Universal Work Queue. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46959

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:15.053 |

Vulnerability in the Oracle Subledger Accounting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Subledger Accounting.  Successful attacks of this vulnerability can result in takeover of Oracle Subledger Accounting. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:14.950 |

Vulnerability in the Oracle Subledger Accounting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Subledger Accounting.  Successful attacks of this vulnerability can result in takeover of Oracle Subledger Accounting. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46957

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:14.843 |

Vulnerability in the Oracle iSupplier Portal product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iSupplier Portal.  Successful attacks of this vulnerability can result in takeover of Oracle iSupplier Portal. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-352;CWE-601` |
| Published | 2026-06-17T10:54:14.637 |

Vulnerability in the Oracle Human Resources product of Oracle E-Business Suite (component: Person).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Human Resources.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Human Resources. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-46935

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.077 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  Successful attacks of this vulnerability can result in takeover of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46934

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:12.953 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  Successful attacks of this vulnerability can result in takeover of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46873

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:05.017 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: VMSVGA device).   The supported version that is affected is 7.2.8. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-46863

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-17T10:54:03.967 |

Vulnerability in the MySQL Server, MySQL Cluster product of Oracle MySQL (component: Server: Connection Handling).  Supported versions that are affected are MySQL Server: 8.4.0-8.4.9, 9.0.0-9.7.0; MySQL Cluster: 8.0.11-8.0.46, 8.4.0-8.4.9 and  9.0.0-9.7.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Server, MySQL Cluster.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Server, MySQL Cluster. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-46862

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-17T10:54:03.863 |

Vulnerability in the MySQL Router product of Oracle MySQL (component: Router: General).  Supported versions that are affected are 8.4.0-8.4.9 and  9.0.0-9.7.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TLS to compromise MySQL Router.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Router. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-46791

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:56.693 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-35295

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-17T10:40:21.670 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35275

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:19.767 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Shared Folders).   The supported version that is affected is 7.2.8. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data as well as  unauthorized access to critical data or complete access to all Oracle VM VirtualBox accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-35269

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:19.130 |

Vulnerability in the Identity Manager product of Oracle Fusion Middleware (component: REST WebServices).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Identity Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Identity Manager accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-12398

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-16T15:16:36.103 |

A command injection vulnerability was found in galaxy_ng. The do_git_checkout() function in the legacy role import API (v1) interpolates unsanitized git ref names (branch/tag names) into shell commands executed via subprocess.run() with shell=True. An authenticated user who controls a git repository can create a branch or tag with shell metacharacters in the name to achieve remote code execution on the pulp worker. The vulnerable endpoint is only reachable when GALAXY_ENABLE_LEGACY_ROLES is set to True, which is not the default configuration.

### CVE-2026-55201

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T20:17:29.093 |

Evil-WinRM through 3.9, fixed in commit 6ecd570, contains a path traversal vulnerability in the download_dir() function that allows a rogue or compromised remote Windows server to write files outside the intended download directory by returning filenames with traversal sequences from Get-ChildItem command output that are passed unsanitized to File.join(). Attackers controlling the remote server can exploit this to overwrite sensitive client-side files such as SSH authorized_keys or shell configuration files, achieving persistent access or privilege escalation on the client machine.

### CVE-2026-9697

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-06-17T18:18:06.473 |

Impact:
undici's ProxyAgent silently drops the requestTls option when configured with a SOCKS5 proxy URI (socks5:// or socks://). The target HTTPS connection through the SOCKS5 tunnel falls back to Node's default trust store, ignoring user-configured ca, cert, key, rejectUnauthorized, and servername settings.

Applications that pin to an internal or corporate CA via requestTls.ca will, when their proxy URI is SOCKS5, get the default Mozilla CA bundle as the trust anchor instead. Any cert signed by any publicly-trusted CA for the target hostname is accepted, breaking the intended pin and enabling MITM read and tamper of the HTTPS exchange.

Affected applications are those that use undici's ProxyAgent (or Socks5ProxyAgent directly) with SOCKS5 AND rely on requestTls for TLS scope restriction. The bug was introduced in undici 7.23.0 when SOCKS5 support was added.

Patches:
Upgrade to undici v7.28.0 or v8.5.0.

Workarounds:
No workaround is available within the SOCKS5 path. If a SOCKS5 proxy with TLS scope restriction is required and an upgrade is not yet possible, route the traffic through an HTTP-proxy ProxyAgent instead, where requestTls is honored correctly.

### CVE-2026-49502

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-17T15:16:59.850 |

Dell PowerFlex Manager, version(s) [Versions], contain(s) an Improper Authentication vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Information disclosure, Information tampering, and Unauthorized access.

### CVE-2026-52698

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-17T13:20:49.060 |

Subscriber Sensitive Data Exposure in PushEngage – Web Push Notifications, eCommerce Automation &amp; Chat Widget <= 4.2.3 versions.

### CVE-2026-48294

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T10:55:01.660 |

Adobe Acrobat PDF Extension (Chrome) versions 26.5.2.2 and earlier are affected by a UXSS-class cross-origin data disclosure vulnerability. An attacker could exploit this vulnerability to gain access to data regarding the victim's session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-12348

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-1021` |
| Published | 2026-06-17T10:14:49.290 |

Address bar spoofing in Arc Search for Android allows a remote attacker to display a trusted domain in the address bar while rendering attacker-controlled content, enabling phishing.

### CVE-2026-10303

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-16T20:16:26.963 |

In ServerCo getssl version 2.49 and prior, the ACME challenge token returned to the client was not strictly validated against RFC 8555 before being used in challenge-file handling, allowing a maliciously crafted token to influence local path/filename usage during validation. An attacker who can supply ACME challenge responses to getssl (for example, a malicious or compromised CA endpoint, or an on-path adversary able to tamper with that response path) could exploit this to achieve unauthorized file write/path traversal effects, usually with elevated privileges, ultimately allowing for remote command injection. This issue appears related in spirit to CVE-2023-38198, and is an instance of CWE-73, "External control of file name or path." Other ACME shell script handlers may be affected by similar issues.

### CVE-2024-39575

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-256` |
| Published | 2026-06-16T19:16:29.040 |

update_disk_psu_baseline.sh requires password in plain text

### CVE-2025-69189

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-17T14:17:35.950 |

Missing Authorization vulnerability in EMV JobBank allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects JobBank: from n/a through 1.2.3.

### CVE-2026-40768

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-17T13:20:37.960 |

Unauthenticated Insecure Direct Object References (IDOR) in Salon booking system <= 10.30.24 versions.

### CVE-2026-35314

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:40:23.573 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Web Server Plugin).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Access Manager accessible data as well as  unauthorized read access to a subset of Oracle Access Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Access Manager. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-0131

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-06-16T20:16:23.990 |

In RtpPacket::decodePacket, there is a possible out of bounds access due to an integer overflow. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is needed for exploitation.

### CVE-2026-5667

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-17T13:20:52.657 |

Use of Hard-coded Credentials vulnerability in Mitsubishi Electric Room Air Conditioners (for Japan and outside Japan); Wireless LAN Adapters for Room Air Conditioners (for Japan and outside Japan); Wireless LAN Adapters for Packaged Air Conditioners (for Japan and outside Japan); Refrigerators (for Japan); Heat Pump Water Heaters / HEMS-Compatible Adapters / Wireless LAN Adapters (for Japan); Bathroom Dryer / Heater / Ventilation Systems (for Japan); Adapters for Airflow Ventilation Systems, Heat Pump Chilled / Hot Water Systems, and Ventilation / Air-Conditioning System Air Resorts (for Japan); Lossnay Central Ventilation Systems (for Japan); Smart Switches for Ventilation Fans and Lossnay (for Japan); IH Cooking Heaters (for Japan); and Rice Cookers (for Japan) allows an attacker within Wi-Fi radio range of an affected product to access the affected product using a hard-coded SSID and password, thereby obtaining device data such as operation status, room set temperature, and room temperature; changing the air-conditioner or Wi-Fi settings; or causing Wi-Fi communication to enter a denial-of-service (DoS) condition.

### CVE-2026-46976

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:16.597 |

Vulnerability in the Oracle Public Sector Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Payroll.  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Payroll. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46970

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:16.083 |

Vulnerability in the Oracle HR Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HR Intelligence.  Successful attacks of this vulnerability can result in takeover of Oracle HR Intelligence. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46969

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:15.980 |

Vulnerability in the Oracle Financials for EMEA product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Financials for EMEA.  Successful attacks of this vulnerability can result in takeover of Oracle Financials for EMEA. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46960

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:15.157 |

Vulnerability in the Oracle Project Portfolio Analysis product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Project Portfolio Analysis.  Successful attacks of this vulnerability can result in takeover of Oracle Project Portfolio Analysis. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46956

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:14.743 |

Vulnerability in the Oracle Property Manager product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Property Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Property Manager. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46953

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-17T10:54:14.533 |

Vulnerability in the Oracle HRMS (UK) product of Oracle E-Business Suite (component: UK Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HRMS (UK).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (UK). CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46938

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-17T10:54:13.280 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Cost Planning).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46922

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-284;CWE-306` |
| Published | 2026-06-17T10:54:09.970 |

Vulnerability in the Oracle HR Intelligence product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HR Intelligence.  Successful attacks of this vulnerability can result in takeover of Oracle HR Intelligence. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46868

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-284` |
| Published | 2026-06-17T10:54:04.487 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Extensibility Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46867

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `NVD-CWE-noinfo;CWE-269` |
| Published | 2026-06-17T10:54:04.383 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Extensibility Framework).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-46769

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:53:54.417 |

Vulnerability in the Oracle Application Development Framework (ADF) product of Oracle Fusion Middleware (component: ADF Shared Components).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Application Development Framework (ADF).  Successful attacks of this vulnerability can result in takeover of Oracle Application Development Framework (ADF). CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-35326

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:40:24.823 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-53865

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-06-16T19:17:04.890 |

OpenClaw before 2026.5.2 contains a path traversal vulnerability in maintenance task execution that allows workspace-derived service paths to influence trash command selection. Attackers can execute unintended local executables from operator-unintended paths during maintenance operations by manipulating workspace-derived environment paths.

### CVE-2026-49133

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-17T21:16:23.720 |

Typemill before 2.24.0 contains a path traversal vulnerability that allows authenticated attackers with Author-level privileges to read arbitrary files outside the content directory by supplying traversal sequences in the path query parameter passed to Storage::getFile() with an empty folder argument. Attackers can bypass traversal-prevention controls in Storage::getFolderPath() to access sensitive files.

### CVE-2026-32682

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-06-17T20:16:50.197 |

When NGINX Gateway Fabric is configured using GRPCRoutes, an authenticated, remote attacker with permission to create or modify GRPCRoute resources can cause the NGINX Gateway Fabric control plane to terminate by sending undisclosed GRPCRoute configurations containing backendRef filters. 


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-55198

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-17T19:18:13.480 |

Hermes WebUI before 0.51.443 contains an authorization bypass vulnerability in the session export endpoint that allows authenticated users to access sessions from other profiles. The _handle_session_export handler in api/routes.py fails to verify active-profile ownership before serializing session data, enabling attackers to exfiltrate foreign session transcripts by guessing or knowing session identifiers.

### CVE-2026-55197

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-17T19:18:13.340 |

Hermes WebUI before 0.51.443 contains a broken access control vulnerability in the /api/session endpoint that allows authenticated users to disclose cross-profile session transcripts. Attackers can bypass profile boundary checks by directly querying session IDs belonging to other profiles via GET /api/session?session_id=<foreign_id>&messages=1 to retrieve unauthorized conversation transcripts and metadata.

### CVE-2026-53875

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-06-17T17:17:25.870 |

picklescan before 1.0.3 contains a scanning bypass vulnerability in the scan_pytorch function that allows attackers to embed malicious magic numbers via dynamic eval using the __reduce__ trick. Attackers can craft malicious PyTorch payloads that evade picklescan detection while remaining executable, enabling arbitrary code execution when loaded with torch.load().

### CVE-2026-35066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T15:16:46.020 |

Dell PowerFlex Manager, version(s) [Versions], contain(s) an Improper Access Control vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to denial of service.

### CVE-2026-40720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T14:17:51.870 |

Unauthenticated Cross Site Scripting (XSS) in Royal Elementor Addons Pro < 1.7.1041 versions.

### CVE-2026-10641

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-17T14:17:37.070 |

Zephyr's Bluetooth Classic Hands-Free Profile (HFP) Hands-Free role parser (subsys/bluetooth/host/classic/hfp_hf.c) contains an out-of-bounds write. During Service Level Connection setup the HF sends AT+CIND=? and parses the AG's +CIND: response in cind_handle(), which assigns a per-entry counter index and calls cind_handle_values() for each list element. cind_handle_values() then wrote hf-ind_table[index] = i without verifying that index is within the 20-element int8_t ind_table[] array of struct bt_hfp_hf. Because the parser places no cap on the number of +CIND: list entries, a remote Attendant Gateway (a malicious, compromised, or spoofed peer the device connects to over Bluetooth) can send a response with more than 20 recognized indicator entries and drive index arbitrarily large, writing a small attacker-positioned value past the array into adjacent struct fields (feature masks, SDP/version state, the calls[] array, work/atomic bookkeeping) and potentially beyond the static connection pool slot. This yields memory corruption and at least denial of service of the Bluetooth host, triggered by a single malformed AT response with no user interaction. The sibling consumer ag_indicator_handle_values() already performed the equivalent bounds check; this commit adds the same index = ARRAY_SIZE(hf-ind_table) guard to close the gap. Affects builds with CONFIG_BT_HFP_HF enabled; introduced with the original HFP HF CIND parser (~v1.7) and present through v4.4.0.

### CVE-2025-69140

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T14:17:34.193 |

Unauthenticated Cross Site Scripting (XSS) in SweetDate Core < 1.1.5 versions.

### CVE-2025-68524

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T14:17:31.623 |

Unauthenticated Cross Site Scripting (XSS) in Avante < 3.0.5 versions.

### CVE-2026-9570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:21:34.983 |

The Taskbuilder  WordPress plugin before 5.0.8 does not properly sanitise a URL parameter before echoing it into inline JavaScript on a frontend page containing one of its shortcodes, leading to a Reflected Cross-Site Scripting vulnerability that can be triggered against any logged-in user.

### CVE-2026-8089

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:21:21.917 |

The weMail: Email Marketing, Email Automation, Newsletters, Subscribers & Email Optins for WooCommerce WordPress plugin before 2.1.3 does not properly escape a user-supplied parameter before reflecting it into an HTML attribute on a non-nonce-protected AJAX response, allowing unauthenticated attackers to deliver Reflected Cross-Site Scripting against any authenticated user (including administrators) via a crafted URL.

### CVE-2026-54195

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:50.820 |

Unauthenticated Cross Site Scripting (XSS) in JetFormBuilder <= 3.6.0.1 versions.

### CVE-2026-54192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:50.533 |

Unauthenticated Cross Site Scripting (XSS) in Popup box <= 6.2.9 versions.

### CVE-2026-54189

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:50.393 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.10 versions.

### CVE-2026-54188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:50.270 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.10 versions.

### CVE-2026-49778

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:46.830 |

Unauthenticated Cross Site Scripting (XSS) in WPFunnels Pro <= 2.9.4 versions.

### CVE-2026-49074

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:45.537 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.9.1 versions.

### CVE-2026-48869

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:44.143 |

Unauthenticated Cross Site Scripting (XSS) in Enfold <= 7.1.4 versions.

### CVE-2026-42385

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:40.067 |

Unauthenticated Cross Site Scripting (XSS) in Profile Builder Pro <= 3.15.0 versions.

### CVE-2026-41557

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:38.410 |

Unauthenticated Cross Site Scripting (XSS) in Kapee < 1.7.1 versions.

### CVE-2026-40765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:37.840 |

Unauthenticated Cross Site Scripting (XSS) in collectchat <= 2.4.9 versions.

### CVE-2026-39597

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:21.953 |

Unauthenticated Cross Site Scripting (XSS) in WPZOOM Addons for Elementor <= 1.3.4 versions.

### CVE-2026-39548

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:19.897 |

Unauthenticated Cross Site Scripting (XSS) in MagOne <= 9.0 versions.

### CVE-2026-22339

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:08.720 |

Unauthenticated Cross Site Scripting (XSS) in WPJobster <= 6.3.5 versions.

### CVE-2026-22329

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:06.903 |

Unauthenticated Cross Site Scripting (XSS) in Skillate <= 1.2.10 versions.

### CVE-2026-22328

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:20:06.593 |

Unauthenticated Cross Site Scripting (XSS) in Auto Repair <= 22.6 versions.

### CVE-2025-69151

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:19:23.097 |

Unauthenticated Cross Site Scripting (XSS) in Grand Car Rental <= 3.7 versions.

### CVE-2025-69104

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:19:16.267 |

Unauthenticated Cross Site Scripting (XSS) in Qreatix <= 1.9.4 versions.

### CVE-2025-59560

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:19:14.927 |

Unauthenticated Cross Site Scripting (XSS) in Sonaar <= 4.27.4 versions.

### CVE-2025-31013

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:19:13.360 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themify Folo allows Reflected XSS.

This issue affects Themify Folo: from n/a through 1.9.6.

### CVE-2024-49269

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-17T13:19:12.767 |

Unauthenticated Cross Site Scripting (XSS) in my flatonica <= 0.0.8 versions.

### CVE-2026-46932

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-17T10:54:12.707 |

Vulnerability in the Oracle Enterprise Asset Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Asset Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Asset Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Asset Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-46914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-269;CWE-400` |
| Published | 2026-06-17T10:54:09.233 |

Vulnerability in the Oracle Solaris product of Oracle Systems (component: Filesystem).   The supported version that is affected is 11.4. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Solaris executes to compromise Oracle Solaris.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Solaris accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Solaris. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-0125

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-06-16T20:16:23.430 |

In multiple functions of vpu_ioctl.c, there is a possible use after free due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-53858

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-06-16T19:17:03.310 |

OpenClaw before 2026.5.2 contains an environment variable injection vulnerability where workspace .env STATE_DIRECTORY could influence bundled runtime dependency roots. Attackers can manipulate the STATE_DIRECTORY variable to load runtime dependencies from unintended local paths, potentially executing malicious code during dependency resolution.

### CVE-2026-53846

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-06-16T19:17:01.653 |

OpenClaw before 2026.4.29 contains a path traversal vulnerability in the install helper that allows workspace .env files to override the npm_execpath configuration used for bundled runtime dependency installation. Attackers with workspace access can execute unintended local package-manager executables during dependency setup to compromise the build environment.

### CVE-2026-53842

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-06-16T19:17:01.127 |

OpenClaw before 2026.5.2 contains an environment variable injection vulnerability allowing workspace .env files to influence Python runtime selection through CLOUDSDK_PYTHON during Gmail setup gcloud execution. Attackers with repository access can manipulate the CLOUDSDK_PYTHON variable to execute setup through unintended local Python paths, potentially enabling arbitrary code execution.

### CVE-2024-38487

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-16T17:16:28.560 |

api-gateway container running with root privilege would allow an attacker to escape the container and access host system to perform unintended actions.
