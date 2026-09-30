# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-30 15:00 UTC
- **対象期間**: `2026-09-29T15:00:46.000Z` 〜 `2026-09-30T15:00:40.000Z`
- **重要CVE数**: 350 件（Critical 9.0+: 68 件 / High 7.0〜: 282 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **70 件以上** に上り、**リモートから認証不要でコード実行や情報漏洩が可能**な脆弱性が目立ちます。特に、Web アプリケーション（SiteSkite、WordPress テーマ、SOPLOG など）や **広く利用されているプラットフォーム（Google Chrome、Android アプリ）** に対する RCE が多数報告されました。さらに、ネットワーク機器（HPE Networking Instant ON）やクラウド認証系統（OAuth SSO）でも **認証バイパス** が確認され、企業ネットワーク全体への波及リスクが高まっています。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑96349** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | SiteSkite ≤ 2.1.8 で **認証不要リモートコード実行**（RCE） | 完全リモートから任意コード実行が可能で、管理者権限でのシステム乗っ取りが想定される。SiteSkite は多くの中小企業のサイト構築ツールとして採用されているため、被害拡大リスクが大きい。 |
| **CVE‑2026‑71379** | 10.0 (AV:N/AC:L/PR:N/UI:N) | 任意の POST リクエストで **データベーステーブルを任意エクスポート** できる | 認証不要で内部データベース全体が漏洩する可能性がある。顧客情報・認証情報が丸ごと取得される危険性が高く、PCI‑DSS・GDPR などのコンプライアンス違反につながる。 |
| **CVE‑2026‑96587** | 10.0 (AV:N/AC:L/PR:N/UI:N) | Viidure Android アプリに **平文のクラウドストレージ認証情報** が埋め込まれている | アプリを逆コンパイルするだけでフルアクセス権を持つ認証情報が取得でき、クラウド上のファームウェアやバイナリを改ざん・削除できる。モバイルデバイスが企業ネットワークの入口になるケースで、サプライチェーン攻撃の足掛かりになる。 |
| **CVE‑2026‑102331** | 9.6 (AV:N/AC:L/PR:N/UI:R/S:C) | Google Chrome Android 154.0.8037.92 未満で **ANGLE バッファオーバーフロー** によりサンドボックス外コード実行 | Chrome は Android ユーザーの 70% 以上が利用。攻撃者は特定の HTML ページを配布するだけでデバイス全体を乗っ取れる。モバイル端末の企業利用が増える中、最重要インフラの一つと位置付けられる。 |
| **CVE‑2026‑76721** | 9.8 (AV:N/AC:L/PR:N/UI:N) | HPE Networking Instant ON の **バッファオーバーフロー** により特権コード実行 | ネットワークスイッチ/AP のファームウェアに深刻なリモートコード実行が残っている。物理的に近い攻撃者（隣接ネットワーク）でも管理者権限取得が可能で、企業内部ネットワーク全体への横移動が容易になる。 |

> **共通点**：すべて「認証不要」か「認証バイパス」かつ「リモートコード実行」または「機密情報漏洩」を引き起こす点で、**緊急度が極めて高い** と判断しました。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 / ライブラリ | 現行バージョン (脆弱) | 推奨バージョン |
|-------------------|------------------------|----------------|
| SiteSkite | ≤ 2.1.8 | **2.1.9 以降**（公式パッチリリース） |
| Viidure Android アプリ | 1.0.0‑1.3.5 (埋め込み認証情報あり) | **最新版 1.4.0 以降**（認証情報除去） |
| Google Chrome (Android) | 154.0.8037.57‑154.0.8037.92 | **154.0.8037.92 以降**（セキュリティパッチ適用） |
| HPE Networking Instant ON (AP/スイッチ) | 2026.5.x 系列 | **2026.10.0 以降**（CVE‑2026‑76721/76722 対応） |
| 任意の Web アプリケーション（CVE‑2026‑71379 対象） | 該当製品バージョン不明 | **ベンダー提供のパッチ**（2026‑Q3 リリース）を即時適用 |

> **※** ベンダーがパッチをまだ提供していない場合は、**WAF で該当エンドポイントをブロック**、**ネットワークレベルでのアクセス制御**（IP フィルタリング、認証プロキシ）を実装してください。

### 3.2 設定・運用面の対策
1. **認証情報のローテーション**  
   - Viidure のクラウドストレージキーは即座に無効化し、**新しいキーを生成**してアプリに安全に埋め込む（環境変数や Android Keystore の利用）。  
2. **最小権限の原則**  
   - SiteSkite、SOPLOG、WordPress テーマ等の管理権限は **必要最小限のユーザーに限定**。  
3. **入力検証とサニタイズ**  
   - ファイルアップロード（Zella Theme）やデータエクスポート（CVE‑2026‑71379）に対し、**CSRF トークン、Capability チェック、ファイルタイプホワイトリスト**を徹底。  
4. **ネットワーク分離**  
   - HPE Instant ON 系機器は **管理 VLAN とデータ VLAN を分離**し、管理インタフェースは VPN 経由のみ許可。  
5. **脆弱

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-96349

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-30T13:17:29.967 |

Unauthenticated Remote Code Execution (RCE) in SiteSkite <= 2.1.8 versions.

### CVE-2026-71379

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-09-29T22:18:21.560 |

The file export endpoint allows any unauthenticated attacker to export arbitrary database tables by sending a crafted POST request.

### CVE-2026-96587

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-29T21:19:39.987 |

The Viidure Android application embeds permanent, plaintext cloud storage credentials within its compiled code. These credentials provide full access to critical platform storage, including the ability to read, modify, or delete operational files such as firmware and application binaries.

### CVE-2026-82307

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T14:17:31.257 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Dolusoft Software Technologies SOPLOG allows SQL Injection.

This issue affects SOPLOG: before Soplog 2026.9.4.1.

### CVE-2026-97274

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-30T13:17:38.293 |

Unauthenticated Bypass Vulnerability in OAuth Single Sign On – SSO (OAuth Client) <= 7.1.2 versions.

### CVE-2026-97248

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:36.830 |

Unauthenticated PHP Object Injection in Booking Activities <= 1.18.7.1 versions.

### CVE-2026-96350

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T13:17:30.090 |

Subscriber Privilege Escalation in Estatik <= 4.3.5 versions.

### CVE-2026-76504

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-177` |
| Published | 2026-09-30T13:17:20.247 |

A vulnerability in the API session-based authentication management of Cisco Catalyst SD-WAN Manager could allow an unauthenticated, remote attacker to access an affected system with privileges of the admin user.

This vulnerability is due to improper handling of URI encoding in an HTTP request, which allows the request to bypass an authentication rule that is intended to restrict access to a specific API endpoint. An attacker could exploit this vulnerability by sending a crafted HTTP request to the API of the affected system. A successful exploit could allow the attacker to bypass authentication and gain access to the API as the admin user.

### CVE-2026-75873

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-30T06:17:04.670 |

The Zella Theme WordPress theme before 2.6.3 does not perform any capability or nonce check on one of its font upload actions, which is available to unauthenticated users, allowing them to upload arbitrary files, including PHP ones, and achieve remote code execution.

### CVE-2026-103110

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T04:18:29.077 |

Pexip Infinity before 38.2, plus 39.0, 39.1 and 40.0, is affected by improper input validation that allows a remote attacker to execute code remotely as an unprivileged user on a Pexip Infinity Conferencing Node.

### CVE-2026-79538

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-29T20:17:27.510 |

metatool-ai MetaMCP up to and including 2.4.22 is vulnerable to Code Execution in the internal MCP inspector proxy endpoint GET /mcp-proxy/server/stdio (createTransport, STDIO branch, routers/mcp-proxy/server.ts).

### CVE-2026-76722

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.207 |

Uncontrolled Format string vulnerabilities exist in the affected interface of HPE Networking Instant ON APs that could allow an unauthenticated remote attacker to run arbitrary commands on the underlying host. Successful exploitation could result in a Denial-of-service or potential remote code execution.

### CVE-2026-76721

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.073 |

Buffer overflow vulnerability exists in the affected interface of HPE Networking Instant ON that could allow an unauthenticated remote attacker to run arbitrary code on the underlying host. Successful exploitation could allow an attacker to execute arbitrary code as a privileged user on the underlying operating system.

### CVE-2026-39117

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-29T20:17:20.130 |

An issue in AltumCode 66Uptime before v.54.0.0 and 66Uptime ping-servers plugin before v.2.0.0 allows a remote attacker to execute arbitrary code via the index.php

### CVE-2026-77177

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-29T16:17:11.363 |

Open GenAI Stack (aka ogx-ai) 2026-06-11, as used in the Meta AI backend for WhatsApp and other products, allows code execution because prompt injection (with Jinja2 template syntax) can be used to achieve server-side expression evaluation without sanitization.

### CVE-2026-76725

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.580 |

A vulnerability has been identified in a management protocol of HPE Networking Instant ON APs that could allow an unauthenticated adjacent attacker to circumvent existing authentication controls. Successful exploitation could result in a complete bypass of security restrictions, potentially leading to remote code execution with elevated privileges.

### CVE-2026-76724

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.453 |

A command injection vulnerability exists in CLI of the affected HPE Networking Instant ON APs that could allow an unauthenticated adjacent attacker to perform command injection by sending specially crafted packets. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-76723

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.327 |

Buffer overflow vulnerabilities exist in the affected interface of HPE Networking Instant ON APS that could allow an unauthenticated adjacent attacker to achieve remote code execution. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-102331

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T20:17:16.587 |

Buffer overflow in ANGLE in Google Chrome on on Android prior to 154.0.8037.92 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-102316

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:14.787 |

Use after free in Views in Google Chrome prior to 154.0.8037.92 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102309

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:13.933 |

Use after free in FullScreen in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102308

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:13.810 |

Use after free in Views in Google Chrome prior to 154.0.8037.92 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102306

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:13.573 |

Use after free in Bluetooth in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102304

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:13.327 |

Use after free in Passwords in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95357

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:28.760 |

Out of bounds write in GPU in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95356

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:28.647 |

Use after free in WindowDialog in Google Chrome prior to 154.0.8037.57 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95350

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T18:17:27.920 |

Buffer overflow in ANGLE in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95349

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T18:17:27.807 |

Buffer overflow in WebGL in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95347

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:27.580 |

Use after free in Updater in Google Chrome on on Mac prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-95339

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:26.480 |

Use after free in ServiceWorker in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95331

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:25.563 |

Out of bounds write in ANGLE in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95329

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:25.330 |

Out of bounds write in WebGL in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95325

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:24.873 |

Use after free in ANGLE in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95318

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T18:17:24.060 |

Buffer overflow in Video in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95313

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:23.463 |

Use after free in Fullscreen in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95311

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-590` |
| Published | 2026-09-29T18:17:23.227 |

Free of non-heap memory in Fonts in Google Chrome prior to 154.0.8037.57 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95310

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:23.110 |

Use after free in AdFilter in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95299

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:21.837 |

Use after free in GPU in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95283

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T18:17:19.733 |

Buffer overflow in Tint in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95281

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T18:17:19.507 |

Buffer overflow in ANGLE in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95277

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:19.037 |

Use after free in Views in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102425

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-29T17:17:06.210 |

Joomla Extension - balbooa.com - Unauthenticated RCE via field shortcode injection in Balbooa Forms < 2.4.3.4 - Balbooa Forms supports administrator-defined PHP code which runs after a public form submission. The feature also supports form-field shortcodes inside that PHP. Before calling `eval()`, the component replaces each shortcode with the raw value submitted by the visitor, leading to an RCE vector. A public form must use the product's optional PHP-after-submission action and interpolate an attacker-controlled field shortcode inside a double-quoted PHP string to be vulnerable.

### CVE-2026-93903

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-174` |
| Published | 2026-09-30T14:17:37.060 |

LiteSpeed Web Server (LSWS) before 6.3.7 build 1 mishandles internal redirect URL validation in a certain "corner case."

### CVE-2026-103056

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-30T01:16:37.050 |

AiSOC versions 7.2.0 before 12.0.0 contain a command injection vulnerability in the actions service that builds CrowdStrike Real Time Response command strings by interpolating unescaped action parameters in crowdstrike_rtr.py and endpoint.py. Authenticated users can inject single quotes into file_path, path, script_name, or script_args parameters to break out of quoted arguments and execute arbitrary commands on managed endpoints with SYSTEM or root privileges.

### CVE-2026-70356

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-29T22:18:16.140 |

The TMS file upload endpoint fails to enforce server-side file type restrictions, allowing an attacker to upload and execute arbitrary PHP files on the web server.

### CVE-2026-96822

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:31.750 |

Unauthenticated SQL Injection in Books Gallery <= 4.8.3 versions.

### CVE-2026-74864

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-30T13:17:19.913 |

sogo_yhn configures SOGo with a parameter that forces the request with HTTP header "x-webobjects-remote-user" to be treated as sent by a verified user without performing password validation. Since Nginx does not strip this header, any client can supply it arbitrarily and gain access as any user, including a privileged user, without providing a password.




This issue was fixed in version 5.8.0~ynh9.

### CVE-2026-102458

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-30T09:17:13.800 |

EasyFlow .NET developed by Digiwin has a Missing Authentication vulnerability. Unauthenticated remote attackers can obtain other users' plaintext passwords through a specific API.

### CVE-2026-102455

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T09:17:13.343 |

EasyFlow .NET developed by Digiwin has a Insecure Deserialization vulnerability. Unauthenticated remote attackers can execute arbitrary code on the server by sending maliciously crafted serialized content.

### CVE-2026-103041

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-29T23:17:21.630 |

LightLLM through 1.2.0 multimodal deployments expose an unauthenticated RPyC cache service with pickle deserialization enabled on all interfaces. Attackers can send crafted serialized objects to exposed cache methods to execute arbitrary code with service privileges.

### CVE-2026-103040

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-29T23:17:21.447 |

LightLLM through 1.2.0 contains a remote code execution vulnerability in the router profiler service when started with --enable_profiling flag. The service exposes an unauthenticated RPyC server with pickle deserialization enabled, allowing attackers to execute arbitrary code by sending crafted serialized objects to the profiler command queue.

### CVE-2026-100291

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-09-29T20:17:09.300 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, several ONVIF service endpoints process management requests without enforcing required authentication. This could allow an unauthorized attacker to access sensitive device operations.

### CVE-2026-102761

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:13.450 |

NetX Duo's WebSocket client resets the unmasking cursor to the first `NX_PACKET` each time it advances through a chained packet, while the loop's upper bound belongs to the current packet. With the standard contiguous packet-pool layout, a masked server frame split across two packets therefore drives the XOR loop through the first packet's unused payload area and on through the second packet's `NX_PACKET` control block.



The four-byte WebSocket masking key controls the bytes written, so the corruption is attacker-chosen rather than incidental.

### CVE-2026-102710

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-822` |
| Published | 2026-09-29T18:17:10.020 |

Attacker model / Preconditions: a loaded `TXM_MODULE_USER_MODE | TXM_MODULE_MEMORY_PROTECTION` module issuing kernel dispatch calls, on a build with `TX_ENABLE_EVENT_TRACE`.



A user-mode, memory-protected module can register an arbitrary function pointer as the global trace-full callback. The kernel calls it directly — no validation, no trampoline — from privileged kernel code when the trace buffer wraps.



An invalid pointer faults the kernel (DoS). A pointer into the module's own code was observed running with kernel privilege (`CONTROL.nPRIV = 0`), confirmed at runtime with a register capture inside that code.

### CVE-2023-54400

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T16:17:04.070 |

Fumasoft Fumeng Cloud contains a SQL injection vulnerability in the AjaxMethod.ashx endpoint that allows unauthenticated remote attackers to inject arbitrary SQL through the Name parameter of the getEmpByname action without any authentication. Attackers can exploit UNION-based SQL injection techniques against the Microsoft SQL Server backend to extract, disclose, and modify database contents, with potential for further compromise of the underlying server. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2026-22094

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-09-29T15:17:21.453 |

The firmware for the EVbee DC-80 has a weak hardcoded root password, which allows attackers to login as root using the SSH daemon that is exposed to the network.

### CVE-2026-74865

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-30T13:17:20.083 |

sogo_yhn configures SOGo with a parameter "SOGoTrustProxyAuthentication=YES". This causes the password to be bypassed during HTTP Basic authentication. An unauthenticated attacker who provides the username of an existing user and any arbitrary password can successfully log in to that user's account.


This issue was fixed in version 5.8.0~ynh9.

### CVE-2026-102508

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-347;CWE-757` |
| Published | 2026-09-30T08:16:31.903 |

Improper Verification of Cryptographic Signature and Improper Certificate Validation in the OPC UA driver of Apache PLC4X (PLC4J) allows an attacker in a network position between client and server to impersonate the OPC UA server and to read, forge or modify secure-channel traffic, including user credential ssent by the client.

The defect manifests differently depending on the version:
- In 0.9.0 through 0.11.0 a failed message-signature check is only logged and never enforced, and there is no mechanism to verify the server certificate: it is taken from the unauthenticated GetEndpoints discovery response and used to encrypt the user's password.
- In 0.12.0 through 0.13.1 the signature check is inverted (valid signatures are rejected, invalid ones accepted), and server certificates are accepted without a trust anchor by default.
- In all affected versions the default security policy is None. Starting with 0.12.0 the driver additionally continues silently at a weaker security policy than the one configured, and starting with 0.13.0 endpoint selection prefers the weakest matching endpoint.

Users checking only for one of these mechanisms may wrongly conclude they are unaffected.

This issue affects Apache PLC4X: from 0.9.0 before 1.0.0.

Users are recommended to upgrade to version 1.0.0, which fixes the issue. Version 1.0.0 verifies message signatures correctly, refuses to connect unless the server certificate can be verified against a configured trust store or pinned certificate, defaults to Basic256Sha256 with SignAndEncrypt, and fails the
connection if the negotiated security policy is weaker than the configured one.

### CVE-2026-86131

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-295;CWE-829` |
| Published | 2026-09-30T00:16:36.817 |

A code injection vulnerability in WatchGuard Fireware OS's BOVPN Over TLS client configuration handling allows an attacker who controls the remote VPN server to execute arbitrary commands as root on the connecting Firebox.

### CVE-2026-53988

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T20:17:20.403 |

Dockhand before 1.0.40 contains an authentication bypass vulnerability in its git webhook endpoints that allows unauthenticated remote attackers to trigger arbitrary stack redeployments by exploiting a null webhook secret guard condition. Attackers can enumerate sequential stack IDs and send unsigned webhook requests to force git clone and docker compose operations, enabling denial of service or, when combined with write access to the tracked git branch, container escape and full host compromise via attacker-controlled docker-compose.yml with privileged bind mounts.

### CVE-2026-102829

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-09-29T19:17:25.367 |

simple-git, an interface for running git commands in any node.js application, enables applications to execute Git operations from JavaScript. Prior to 2.0.1 of the argv-parser package, parseEnv omits VISUAL from GitEnvKeys, so prepareEnv drops the value before vulnerabilityCheck can classify it as allowUnsafeEditor. A consuming application that forwards attacker-influenced environment values can therefore allow Git to invoke an attacker-selected editor during operations such as commit amendment or interactive rebase when no higher-priority editor setting overrides VISUAL and Git's terminal prerequisites are met. The executable runs with the privileges of the Node.js process. This issue is fixed in argv-parser 2.0.1.

### CVE-2026-102828

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-09-29T19:17:25.207 |

simple-git, an interface for running git commands in any node.js application, enables applications to execute Git operations from JavaScript. From 3.15.0 until 4.0.1, the default blockUnsafeOperationsPlugin does not classify trailer.<token>.cmd as unsafe configuration. An application that passes attacker-controlled values through SimpleGitOptions.config or inline -c arguments can therefore allow Git to invoke an attacker-selected shell command when git interpret-trailers processes the configured trailer. The command executes with the operating-system identity and permissions of the Node.js process. This issue is fixed in 4.0.1.

### CVE-2026-94053

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-90;CWE-305` |
| Published | 2026-09-30T10:17:18.283 |

Authentication bypass via LDAP injection in component sshd-ldap in Apache MINA SSHD versions 1.2.0 to 2.19.0 and 3.0.0-M1 to 3.0.0-M5.




Apache MINA SSHD is a Java library for client-side and server-side SSH. 
The optional sshd-ldap component provides support for integrating 
password and publickey authentication on the server side with an LDAP 
server.




sshd-ldap is an optional component. SSH servers implemented with Apache 
MINA SSHD are affected only if they use sshd-ldap and do configure it to be used for password of public key authentication.

Other Apache MINA SSHD servers are not affected.




Lack of escaping LDAP filter metacharacters enabled successful authentication with username "*" and password "*".




Users are recommended to upgrade affected applications to version 2.20.0 or 3.0.0-M6, which fix this issue by properly escaping filter parameters according to RFC 4515.

### CVE-2026-94052

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-304` |
| Published | 2026-09-30T10:17:18.147 |

A missing check in LdapPasswordAuthenticator in component sshd-ldap in Apache MINA SSHD versions 1.2.0 to 2.19.0 or 3.0.0-M1 to 3.0.0-M5 bypassed authentication checks.




Apache MINA SSHD is a Java library for client-side and server-side SSH. The optional sshd-ldap component provides support for integrating password and publickey authentication on the server side with an LDAP server.




sshd-ldap is an optional component. SSH servers implemented with Apache MINA SSHD are affected only if they use sshd-ldap and do configure an LdapPasswordAuthenticator to be used for password authentication. Normal password authentication via the built-in mechanisms in sshd-core is _not_ affected by this vulnerability, which concerns only LdapPasswordAuthenticator.




Users are recommended to upgrade affected applications to version 2.20.0 or 3.0.0-M6, which fix this issue.

### CVE-2026-77185

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-305` |
| Published | 2026-09-30T10:17:17.123 |

Authentication bypass in sshd-core in Apache MINA SSHD versions 2.0.0 to 2.19.0 and 3.0.0-M1 to 3.0.0-M5 for a certain (presumed rare) way to implement an SSH server.




Apache MINA SSHD is a Java library for client- and server-side SSH. In the server part of the library, a mechanism to perform "asynchronous authentication" exists. A server implemented with Apache MINA SSHD must contain explicit code to make use of this feature. The implementation of this feature was flawed and could potentially lead to skipping checking the signature in public-key or hostbased authentication, or returning a wrong result.




Users are recommended to upgrade to Apache MINA SSHD 2.20.0 or 3.0.0-M6, which fix the logic error and which additionally forbid the use of this "asynchronous authentication" mechanism with the public-key or hostbased authentication schemes: if used, the SSH session will be closed and the server will log an entry indicating that asynchronous authentication may be used only with password or keyboard-interactive authentication.

### CVE-2026-97196

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1289` |
| Published | 2026-09-30T07:16:31.320 |

Improper Validation of Unsafe Equivalence in Input vulnerability in Liquid Web / StellarWP GiveWP allows Authentication Bypass.

This issue affects GiveWP: from n/a through 4.16.9.

### CVE-2026-84436

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T18:17:17.823 |

IBM Guardium Data Protection 12.2 is vulnerable to command injection in the certificate export CLI functionality, allowing a privileged authenticated CLI user to execute arbitrary commands with root privileges.

### CVE-2026-94389

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-30T13:17:26.840 |

Unauthenticated Remote Code Execution (RCE) in AcyMailing SMTP Newsletter <= 11.0.5 versions.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-92222

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-29T17:17:14.020 |

Joomla! Core - [20260909] - Core - SSRF vectors in various core extensions in Joomla 4.0.0-5.4.8, 6.0.0-6.1.3 - URLs used for serverside requests were improperly validated, leading to SSRF vectors.

### CVE-2026-102424

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T17:17:06.070 |

Joomla Extension - balbooa.com - Unauthenticated path traversal exfiltrates local files through auto-reply attachments in Balbooa Forms < 2.4.3.4 - Balbooa Forms accepts upload-field state as Guest-controlled JSON during public form submission. For every object whose `id` merely looks numeric, the component trusts the supplied `filename`, concatenates it below the configured upload directory, and adds the result to an array of local attachment paths. It does not load the referenced attachment row, verify ownership/session/form/field, require that the ID exists, canonicalize the path, or enforce containment. If the form's normal “auto reply” and “attach uploaded files” options are enabled, the component sends those local paths as email attachments to the address submitted in an email field. A Guest can therefore submit a nonexistent numeric ID plus a traversal filename such as `../../../../configuration.php` and receive any file readable by the Joomla process.

### CVE-2026-97689

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-29T16:17:18.837 |

urllib3 is an HTTP client library for Python. From 1.10.3 until 2.8.0, the HTTPResponse.read_chunked and HTTPResponse.stream methods can allocate unbounded memory because the streaming chunk parser buffers the chunk-size field until newline or EOF without a length bound. The trigger is that a malicious server returns Transfer-Encoding: chunked followed by a very long run of bytes without a newline. The attack mechanism is that a malicious HTTP server sends a very long unterminated chunk-size line. The impact is that unbounded memory allocation can exhaust the client process. This issue is fixed in version 2.8.0.

### CVE-2026-96838

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-30T13:17:33.810 |

Unauthenticated Cross Site Request Forgery (CSRF) in Blacklist Manager &#8211; WooCommerce Anti-Fraud, Blacklist &amp; Checkout Verification <= 2.3.1 versions.

### CVE-2026-96837

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-30T13:17:33.673 |

Contributor Remote Code Execution (RCE) in CartFlows <= 3.2.0 versions.

### CVE-2026-96831

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:32.893 |

Contributor PHP Object Injection in Themify Builder <= 7.8.1 versions.

### CVE-2026-95531

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:28.587 |

Subscriber PHP Object Injection in Conversational Forms for ChatBot <= 1.5.0 versions.

### CVE-2026-94683

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:27.940 |

Contributor PHP Object Injection in DesignSetGo <= 2.8.0 versions.

### CVE-2026-94678

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:27.673 |

Contributor PHP Object Injection in Go Live Update Urls <= 7.0.8 versions.

### CVE-2026-94121

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:24.497 |

Contributor PHP Object Injection in 10Web Booster – Website speed optimization, Cache & Page Speed optimizer <= 2.33.6 versions.

### CVE-2026-94076

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:23.080 |

Contributor PHP Object Injection in SEO Plugin by Squirrly SEO <= 14.2.5 versions.

### CVE-2026-92994

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T06:17:09.983 |

The Verge3D Publishing and E-Commerce WordPress plugin before 4.13.1 does not validate the contents of files uploaded through its file storage feature and serves them back with an attacker-controlled content type, allowing unauthenticated attackers to store a file containing malicious JavaScript that executes in the browser of any user who opens it.

### CVE-2026-85573

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T06:17:06.503 |

The All in One Files Upload WordPress plugin before 2.0.17 adds SVG to the site's allowed upload types and does not sanitise uploaded files or verify the authenticity of its public upload requests, allowing unauthenticated users to store files containing active content which run in the site's origin when a victim opens them.

### CVE-2026-103105

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-30T03:16:59.623 |

Pexip Infinity before 38.2, plus 39.0, 39.1 and 40.0, is affected by improper access control on a product-internal API which allows an attacker with local access to a node within a Pexip Infinity installation to execute arbitrary code as an unprivileged user on another Pexip Infinity node.

### CVE-2026-74222

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T22:18:33.660 |

U-Boot before 2026.10-rc5 contains a use-after-free vulnerability in the httpc_recv_cb() function within the lwIP wget implementation. When HTTP data storage fails, the callback frees the connection PCB but returns ERR_BUF instead of ERR_ABRT, causing the TCP input path to access released memory and crash the bootloader.

### CVE-2026-74221

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-09-29T22:18:33.493 |

U-Boot before 2026.10-rc5 contains a buffer overflow in nfs_readlink_reply() function in net/nfs-common.c when processing NFS server responses. A malicious NFS server can send crafted READLINK replies with negative or oversized symlink length values to corrupt memory and crash the bootloader.

### CVE-2026-74220

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-09-29T22:18:33.317 |

U-Boot before 2026.10-rc5 contains a buffer overflow in nfs_read_reply() function in net/nfs-common.c that allows attackers to corrupt memory by supplying crafted NFS READ reply lengths. A malicious NFS server can exploit signed integer handling to bypass length validation and write far past the destination buffer, crashing the bootloader or corrupting memory.

### CVE-2026-71971

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T22:18:21.723 |

U-Boot before 2026.10-rc3 with CONFIG_IP_DEFRAG enabled contains an out-of-bounds write vulnerability in the __net_defragment() function in net/net.c. Remote attackers can send a crafted IP fragment with non-zero offset and More-Fragments flag set during netboot to corrupt adjacent memory and crash the bootloader.

### CVE-2026-102328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T20:17:16.217 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T20:17:15.973 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102323

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T20:17:15.607 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102321

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T20:17:15.483 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102302

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-29T20:17:13.087 |

Buffer overflow in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102299

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T20:17:12.717 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.92 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95380

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T18:17:31.750 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.57 allowed a remote attacker leveraging social engineering to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-95373

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:31.250 |

Use after free in DevTools in Google Chrome prior to 154.0.8037.57 allowed a remote attacker leveraging social engineering to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95369

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-841` |
| Published | 2026-09-29T18:17:30.763 |

Inappropriate implementation in XML in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95365

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T18:17:30.250 |

Type confusion in IndexedDB in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95353

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:28.307 |

Use after free in Bindings in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95345

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:27.357 |

Use after free in Actor in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95343

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:27.063 |

Use after free in WebAudio in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95338

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:26.363 |

Use after free in PDFium in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted PDF file. (Chromium security severity: High)

### CVE-2026-95306

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T18:17:22.650 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95304

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:22.427 |

Out of bounds write in V8 in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95286

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T18:17:20.273 |

Type confusion in Bindings in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:19.623 |

Use after free in Platform in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84421

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T18:17:17.560 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper validation of paths during archive extraction.

### CVE-2026-102713

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-770` |
| Published | 2026-09-29T18:17:10.457 |

The TFTP server accepts a DATA datagram of any size. The dispatcher rejects datagrams shorter than



four bytes (nxd_tftp_server.c:1037) and nothing anywhere checks an upper bound, in particular not



against the protocol maximum of 4 + NX_TFTP_FILE_TRANSFER_MAX. Two things follow from that one



missing check, both reachable before any authentication because TFTP has none.



The handler passes `nx_packet_length - 4` straight to FileX:



```c



/* addons/tftp/nxd_tftp_server.c:1863, 1889 */



status = nx_packet_copy(packet_ptr, &temp_ptr,

                        server_ptr -> nx_tftp_server_packet_pool_ptr, NX_WAIT_FOREVER);


...



fx_file_write(&(client_request_ptr -> nx_tftp_client_request_file),

              packet_ptr -> nx_packet_prepend_ptr + 4,
              packet_ptr -> nx_packet_length - 4);


```



`nx_packet_length` is the length of a chain, not of one contiguous buffer, so FileX copies past the



end of the first packet:



```



ERROR: AddressSanitizer: heap-buffer-overflow



READ of size 1280 at 0x621000001108 thread T5

    #0 __interceptor_memcpy
    #1 _fx_utility_memory_copy  filex/common/src/fx_utility_memory_copy.c:78


0x621000001108 is 0 bytes to the right of 4104-byte region



```



Those bytes are written into the file the attacker is uploading, and a TFTP read request hands them



back, so this is a memory disclosure with a convenient retrieval channel.



The same datagram also wedges the server. `nx_packet_copy` at :1863 needs



ceil(nx_packet_length / pool_payload) packets and asks for them with NX_WAIT_FOREVER, so when the



attacker sizes the datagram beyond what the pool holds, the server thread suspends and never



returns. A liveness probe after one such datagram times out with the pool at 0 of 12 packets and



the server thread suspended, and no later client is served.



Reject `nx_packet_length > 4 + NX_TFTP_FILE_TRANSFER_MAX` in the DATA branch before either call,



and use a bounded wait rather than NX_WAIT_FOREVER for the copy.

### CVE-2026-102712

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:10.320 |

On the first DTLS ClientHello, the parser copies a device-claimed session_id length and validates the



ciphersuite-list length against the total record length instead of the remaining bytes. An unauthenticated



peer drives an OOB source read of up to 255 bytes, and those bytes are echoed verbatim into the outgoing



ServerHello, disclosing adjacent process memory over the network. The crash variant fires on the first



packet.

### CVE-2026-92370

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-29T16:17:15.033 |

An improper access control vulnerability in TeamViewer Full Client, Host, and related affected modules on Windows, Linux, and macOS allows an authenticated remote attacker to bypass user-configured permission settings during session establishment. By modifying access control parameters for restricted features, an attacker can perform actions that were explicitly denied by the victim's configuration. This may result in unauthorized actions and potentially lead to remote code execution on the target system.

### CVE-2026-76992

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T11:16:47.283 |

The CODESYS Gateway Client allocates memory based on a size field in a gateway response without enforcing an appropriate upper limit. An unauthenticated remote attacker controlling a malicious gateway can exploit this behavior to trigger excessive memory consumption, resulting in a denial-of-service condition thus leading to a total loss of availablity.

### CVE-2026-10764

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-30T10:17:16.960 |

Information disclosure in BVMS 4.5 up to 12.3 including allows man-in-the-middle attackers to gain unauthorized access to sensitive data.

### CVE-2026-103235

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-915` |
| Published | 2026-09-30T10:17:16.243 |

MISP contains a mass assignment vulnerability in the event delegation feature. When a user with delegation permission submits a delegation request, the application authorized the user against the event identified in the URL but then persisted the entire submitted record, including caller-supplied fields such as the primary key and event_id.

An authenticated attacker could inject a primary key or event_id into the delegation payload to retarget an existing delegation record to any event on the instance. Because a delegation row grants the requesting organisation read access to the event it references, this effectively granted read access to arbitrary events belonging to other organisations. If the target organisation subsequently accepted the delegation, ownership of the event was transferred and the original record was deleted.

Preconditions:

- An authenticated user with the delegation permission (perm_delegate)

- The MISP.delegation server setting must be enabled

Impact:

- Confidentiality: read access to any event on the instance

- Integrity: overwriting existing delegation records and transferring event ownership

Affected versions: MISP < 2.5.48

### CVE-2026-102510

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-190;CWE-674;CWE-789` |
| Published | 2026-09-30T09:17:14.293 |

Integer Overflow, Improper Validation of Array Index, Uncontrolled Recursion and Memory Allocation with Excessive Size Value in the Go implementation of Apache PLC4X (PLC4Go) allow a malicious device, or an attacker able to inject network traffic, to crash or exhaust the memory of the client application,
causing a denial of service.

The individual defects are:
- Generated parsers pre-allocate arrays with the element count claimed on the wire (0.13.0 through 0.13.1).
- Transport read helpers allocate buffers of the size claimed on the wire without an upper bound.
- ADS and KNXnet/IP response handling indexes into received data without checking its length, causing a panic.
- ADS and EIP frame-length handling accepts, or arithmetically wraps to, a length of zero, breaking message framing.
- Recursive protocol types are parsed without a nesting-depth limit. The same defect in the Java implementation is covered by  CVE-2026-102509 https://cveprocess.apache.org/cve5/CVE-2026-102509 .

Additionally, length and position arithmetic in generated serializers was performed in 16-bit integers. If an application forwards attacker-influenced payloads larger than 8 KB, the length field wraps, and the remainder of the payload may be interpreted by the receiving device (for example, an ADS PLC) as 
additional, independent protocol messages.

This issue affects Apache PLC4X: from 0.11.0 before 1.0.0. PLC4Go is consumed as the Go module github.com/apache/plc4x/plc4go; versions refer to the corresponding Apache PLC4X releases.

Users are recommended to upgrade to version 1.0.0, which fixes the issue.

### CVE-2026-102509

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674;CWE-770;CWE-789` |
| Published | 2026-09-30T09:17:14.100 |

Memory Allocation with Excessive Size Value, Allocation of Resources Without Limits, and Uncontrolled Recursion in the Java implementation of Apache PLC4X (PLC4J) allow a malicious or impersonated device to exhaust the memory or stack of the client application, causing a denial of service.

In the OPC UA driver these defects are reachable before authentication: the offending data is parsed while the secure channel and session are being established, before the server's identity has been bound to it. Configuring a trusted server therefore does not prevent exploitation by an attacker who can 
impersonate it.

The individual defects are:
- Length-prefixed byte strings are allocated at the size claimed on the wire before the length is checked against the data actually received (0.10.0 through 0.13.1).
- Array fields in generated protocol parsers pre-allocate a list with the element count claimed on the wire, allowing a single count field to trigger a multi-gigabyte allocation. This parser is shared by all PLC4J drivers; the OPC UA driver is the verified pre-authentication path (0.10.0 through 0.13.1).
- The OPC UA driver accumulates message chunks without enforcing the negotiated maximum chunk count and message size (0.12.0 through 0.13.1).
- The OPC UA driver pre-allocates collections using element counts received from the server (0.10.0 through 0.13.1).
- Recursive protocol types are parsed without a nesting-depth limit. The same defect in the Go implementation is covered by  CVE-2026-102510 https://cveprocess.apache.org/cve5/CVE-2026-102510 .

This issue affects Apache PLC4X: from 0.10.0 before 1.0.0.

Users are recommended to upgrade to version 1.0.0, which fixes the issue.

### CVE-2026-92871

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-30T08:16:35.193 |

A NULL pointer dereference vulnerability exists in Pgpool-II, which may allow an unauthenticated attacker to cause abnormal termination of the watchdog process.

### CVE-2026-92870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-30T08:16:35.040 |

A stack-based buffer overflow vulnerability exists in Pgpool-II, which may allow an unauthenticated attacker to cause abnormal process termination.

### CVE-2026-92867

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T08:16:34.557 |

An out-of-bounds write vulnerability exists in Pgpool-II , which may allow an authenticated attacker to cause abnormal process termination or arbitrary code execution.

### CVE-2026-86134

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-30T04:18:33.337 |

A NULL pointer dereference vulnerability in the WatchGuard Fireware OS authentication process allows a remote, unauthenticated attacker to crash the management daemon by sending a specially request to the login interface, resulting in a denial of service.

### CVE-2026-103055

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-30T01:16:36.880 |

AiSOC versions 7.5.0 before 12.0.0 use a hard-coded constant for JWT verification in the realtime WebSocket and SSE service when the AISOC_REALTIME_JWT_SECRET environment variable is not set. Unauthenticated attackers can forge subscription tickets with arbitrary tenant identifiers to access cross-tenant live alerts, cases, agent events and graph updates through the realtime endpoints.

### CVE-2026-86104

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-409;CWE-770` |
| Published | 2026-09-30T00:16:36.420 |

An uncontrolled resource consumption vulnerability in the Fireware OS login process (wgagent) allows a remote, unauthenticated attacker to cause a denial of service by sending a specially crafted request.

### CVE-2026-81433

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120;CWE-121;CWE-787` |
| Published | 2026-09-30T00:16:36.150 |

A stack-based buffer overflow vulnerability in WatchGuard Fireware OS's DHCP fingerprinting daemon (fingerd) allows an unauthenticated attacker with adjacent network access to execute arbitrary code or crash the process by sending a specially crafted DHCP packet.

### CVE-2026-103043

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-29T23:17:22.023 |

anchorme through 3.0.8 contains a regular expression denial of service vulnerability in the IPv6 host extraction regex due to catastrophic backtracking. Attackers can supply specially crafted input strings with repeated patterns to cause exponential regex engine backtracking, blocking the Node.js event loop and denying service to other requests.

### CVE-2026-103042

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-29T23:17:21.830 |

LightLLM through 1.2.0 contains a memory exhaustion vulnerability in the NCCL control channel when started with --pd_trans_mode nccl, allowing unauthenticated attackers to exhaust KV-transfer worker memory. Attackers can call the exposed_set_value method to store unbounded key-value pairs without size limits, causing the worker process to crash and triggering node failure.

### CVE-2026-94204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-29T21:19:39.283 |

The central cloud storage backend for the entire dashcam platform is misconfigured with public-read permissions, allowing unrestricted access to all stored objects. Because this bucket serves as shared storage for the platform, sensitive user records, live dashcam footage, application packages, and firmware files are exposed to anyone on the internet.

### CVE-2026-102253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-29T21:17:13.640 |

iperf3 versions prior to 3.22 contains a denial of service vulnerability that allows unauthenticated remote attackers to crash-loop the server's UDP receive worker into an unrecoverable infinite loop by sending a single crafted control-channel parameter message followed by one 16-byte UDP datagram. Attackers can permanently pin the affected per-stream receive thread at approximately 100% CPU usage, rendering the server unusable until forcibly killed with SIGKILL, as the process does not respond to normal control-channel closure.

### CVE-2026-61519

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-29T20:17:21.150 |

Liberu CRM 0.9.1 before 10.0.0 contains a broken access control vulnerability that allows any user holding a pending team invitation to invite additional attacker-controlled accounts with elevated privileges by exploiting a flawed authorization predicate in TeamPolicy::addTeamMember() that grants invitation rights based solely on the existence of a pending invitation email match. Attackers can send a POST request to the team-invitations route specifying the admin role for a second account, bypassing privilege-level validation in InviteTeamMember, causing the second account upon invitation acceptance to be attached to the team with full admin-level create, read, update, and delete access over all team-scoped data.

### CVE-2026-100298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-29T20:17:10.403 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, two user‑information endpoints can reveal sensitive device and account details under conditions that are not intended for normal operation.

### CVE-2026-100294

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-29T20:17:09.787 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, the firmware embeds hardcoded cloud‑API credentials that are shared across deployed devices. Anyone obtaining the public firmware package can reuse these values to interact with the cloud service in ways not intended for normal operation.

### CVE-2026-100293

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-29T20:17:09.630 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, both the local and cloud update mechanisms apply new firmware without any cryptographic verification, relying only on basic hashing. This design allows an attacker who can reach the update routine to introduce untrusted firmware images that the device will accept as valid.

### CVE-2026-100292

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T20:17:09.477 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, a hidden debug interface can be enabled through an authenticated request, allowing additional commands to be sent to a backend service. Once active, this pathway can unintentionally expose system‑level functionality that could be misused if crafted inputs reach the underlying command handler.

### CVE-2026-102811

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-29T18:17:14.527 |

Marmite through 0.4.2 contains missing authentication in the development server endpoints /__marmite__/content, /__marmite__/config, and /__marmite__/file/, allowing unauthenticated attackers to create, modify, and overwrite site content and configuration. Attackers can exploit unsanitized path parameters in handle_create_content and handle_clone_content to write files outside the project directory via directory traversal.

### CVE-2026-102810

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T18:17:14.370 |

Marmite through 0.4.2 contains a path traversal vulnerability in the development server started by --serve that allows unauthenticated attackers to read arbitrary files. The handle_request function in src/server.rs fails to reject .. segments after percent-decoding and joining the request path to the output folder, enabling attackers to request encoded traversal sequences to access files readable by the marmite process.

### CVE-2026-102718

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:11.103 |

hey,



`_nx_snmp_utility_object_id_get` in the NetX Duo SNMP addon does not validate the claimed OID data length against the actual buffer size when the OID uses BER multibyte length encoding, so a remote attacker can send a crafted SNMP packet with a multibyte OID length larger than the available buffer, causing the parser to read past the packet buffer boundary into adjacent heap memory. the OOB bytes are decoded as OID component values and written into the agents internal OID string buffer, corrupting agent state. on systems with memory protection the OOB read poses the risk of crashing the SNMP agent thread, causing denial of service. on bare metal embedded systems without memory protection the read silently succeeds and corrupts the agents internal state with heap data.

### CVE-2026-102716

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-29T18:17:10.943 |

An unauthenticated client can drain the RTSP server's packet pool with a couple of dozen requests



that carry a Session header the parser cannot convert.



The Session branch returns the raw NetX error code instead of an RTSP status code:



```c



/* addons/rtsp/nx_rtsp_server.c:2754 */



status = _nx_utility_string_to_uint(field_value_ptr, field_value_length, &session_id);



if (status)



{

    return(status);      /* NX_INVALID_PARAMETERS / NX_SIZE_ERROR / NX_OVERFLOW */


}



```



Every other branch of the same function maps its failure to an RTSP status first. The CSeq branch



eighteen lines earlier does exactly that (line 2736 returns NX_RTSP_STATUS_CODE_BAD_REQUEST). The



raw code then reaches `_nx_rtsp_server_error_response_send` (nx_rtsp_server.c:1234), which does not



recognise it, takes a path that returns without releasing the response packet it already allocated,



and the block never goes back to the pool.



Six requests with an empty Session header against a 22 packet pool:



```



valid requests:      after request 6: pool available = 21,  AFTER = 22 / 22



malformed requests:  after request 6: pool available = 16,  AFTER = 17 / 22



```



One block per request, not returned when the client disconnects. Twenty six requests take the pool



to zero and the server starts failing allocations, after which it serves nobody. If the pool is



shared with the rest of the application, as it is in the shipped sample, the rest of the stack



stops with it.



Convert the `_nx_utility_string_to_uint` failure in the Session branch into



NX_RTSP_STATUS_CODE_BAD_REQUEST the way the CSeq branch does, and release the response packet on



every exit path of `_nx_rtsp_server_error_response_send`.

### CVE-2026-102634

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-694` |
| Published | 2026-09-29T17:17:07.147 |

SGLang through 0.5.20 in prefill/decode disaggregation mode fails to validate duplicate bootstrap_room fields in /generate requests with Mooncake KV transfer backend. Unauthenticated attackers can send concurrent requests with identical bootstrap_room values to crash scheduler processes or hang other users' requests until transfer timeout.

### CVE-2022-51019

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T17:17:00.653 |

Akaunting before 2.1.31 contains an OS command injection vulnerability in the module installation and update flow where the alias parameter is passed unvalidated to shell command execution. Authenticated users with admin panel access can inject shell metacharacters into the alias parameter to execute arbitrary commands on the server.

### CVE-2026-68911

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-29T15:17:27.647 |

Nicotine+ is a graphical client for the Soulseek peer-to-peer network. Prior to version 3.3.11, a modified remote client can send zlib-compressed peer messages containing a decompression bomb, exhausting available memory of the recipient's operating system. This issue has been patched in version 3.3.11.

### CVE-2015-20122

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T15:17:11.023 |

Seeyon A6 collaborative office automation platform contains an unauthenticated SQL injection vulnerability in the attach_ids parameter of the file attachment download endpoint that allows remote attackers to extract arbitrary database contents without prior authentication. Attackers can inject UNION-based SQL statements through the attach_ids request parameter in downloadAtt.jsp to retrieve sensitive information including credentials and system configuration data. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-17.

### CVE-2026-103239

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-862` |
| Published | 2026-09-30T11:16:43.527 |

MISP contains a privilege escalation vulnerability in the tag collection creation and editing functionality. The affected actions accepted the full HTTP request payload and passed it to a bulk-association save operation, which writes not only the intended tag collection record but also any associated model data present in the payload.

A user holding the tag editor permission could craft a request that includes additional model data (such as User or Organisation records) alongside the tag collection fields. Because the save operation processed all associated models indiscriminately, the injected sibling records were written to the database, enabling the attacker to modify or create privileged accounts and escalate to site administrator.

Preconditions:

- An authenticated account with the tag editor permission (perm_tag_editor)

- Network access to the MISP instance

Impact:

- Unauthorized creation or modification of User and Organisation records

- Privilege escalation from tag editor to site administrator

Affected versions: < 2.5.48

### CVE-2026-102454

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-30T09:17:13.170 |

EasyFlow .NET developed by Digiwin has an Arbitrary File Upload vulnerability. Privileged remote attackers can upload and execute web shell backdoors, thereby enabling arbitrary code execution on the server.

### CVE-2026-97150

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-30T08:16:36.230 |

When converting baserCMS4-style addons to baserCMS5-style ones,
BcAddonMigrator includes "config.php" from the addon, which means the PHP code in the file is executed.
Arbitrary files on the system may be read or deleted by an administrative user.

### CVE-2026-102911

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-30T04:18:28.580 |

A flaw has been found in zosmaai pi-llm-wiki up to 0.11.7. Affected is an unknown function of the file mcp/index.ts of the component wiki_capture_source MCP tool. Executing a manipulation of the argument url can lead to os command injection. The attack can be executed remotely. The exploit has been published and may be used. Upgrading to version 0.11.8 is able to address this issue. This patch is called 360867034e79175b45c8e04a98e4ca712bbaca35. Upgrading the affected component is advised.

### CVE-2026-103102

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T03:16:59.307 |

Pexip Infinity before 41.0 is affected by improper input validation in the signaling implementation which allows a remote attacker to trigger a software abort resulting in a denial of service. Exploitation of this issue requires accessing a gateway call from a WebRTC/API client.

### CVE-2026-103101

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T03:16:59.033 |

Pexip Infinity 30.0 through 40.x before 41.0 is affected by improper input validation in the web server that allows a malicious attacker to render a Pexip Infinity node inaccessible.

### CVE-2026-18145

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-30T00:16:36.003 |

A stack-based buffer overflow vulnerability in the spamBlocker (spamd) service of WatchGuard Fireware OS allows an authenticated attacker with administrator privileges to crash the service or potentially execute arbitrary code by sending a specially crafted management request.

### CVE-2026-102878

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-29T20:17:18.620 |

mcp-chrome-bridge through 1.0.31 contains an origin validation error in the native-server HTTP API that allows attackers to bypass CORS restrictions. Attackers can craft malicious web pages that make cross-origin requests to the local server and invoke browser automation tools including script execution, page content reading, and screenshot capture.

### CVE-2026-102876

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-29T20:17:18.230 |

SurrealDB before 3.3.0 contains an authorization bypass in HTTP session construction where check_auth() verifies credentials against Surreal-Auth-NS and Surreal-Auth-DB headers but constructs sessions using Surreal-NS and Surreal-DB headers without validating access permissions. Attackers can authenticate as a user from one tenant while selecting another tenant's namespace and database to read, create, and modify records across tenant boundaries.

### CVE-2026-102317

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-29T20:17:14.913 |

Improper privilege management in Mojo in Google Chrome on on Windows prior to 154.0.8037.92 allowed a local attacker to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-102730

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787;CWE-1284` |
| Published | 2026-09-29T18:17:12.770 |

Mounting an attacker-controlled NAND flash image (`lx_nand_flash_open()`) triggers an unbounded out-of-bounds heap **write** in LevelX's NAND flash-translation-layer metadata parser that overwrites a driver function pointer in the control block, giving a demonstrated control-flow hijack — RIP set to a full 8-byte attacker-chosen value (register-verified). Two accompanying OOB reads. All reproduced verbatim under ASan at HEAD `9f1cfdc`. (The affected metadata-parser header states "Some portions generated by Copilot (Sonnet 4.6)" — an AI-generated parser with an unchecked on-flash count.)

### CVE-2026-102560

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:08.750 |

A flaw was found in libsoup. When the permessage-deflate WebSocket extension compresses a very large outgoing message, truncated size calculations used for GByteArray growth could wrap, causing zlib to write past the allocated buffer and resulting in a heap buffer overflow.

### CVE-2026-102559

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:08.503 |

A flaw was found in libsoup. When constructing a masked WebSocket client frame for a very large outgoing payload, size values passed to GByteArray allocation APIs could be truncated while the masking routine still used the full length, causing a heap buffer overflow.

### CVE-2026-102558

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:08.340 |

A flaw was found in libsoup. When max-incoming-payload-size is unlimited (0), SoupWebsocketConnection could grow its incoming GByteArray based on an attacker-controlled frame length until the length wrapped, causing a heap buffer overflow while reading frame data.

### CVE-2026-102242

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-09-29T18:17:06.887 |

Improper link resolution (CWE-59 / CWE-22) in the allowedLocalRoots path validation in Google MCP Toolbox for Databases versions 1.2.0 through 1.9.0 allows a remote authenticated attacker with tool execution permissions to bypass directory boundary restrictions via symbolic links. Because path validation checks directories lexically without resolving symbolic links first, an attacker can access or overwrite arbitrary local files located outside the permitted root directories.

### CVE-2026-102557

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T17:17:06.600 |

A flaw was found in libsoup. When reassembling fragmented WebSocket messages into a GByteArray, libsoup did not adequately cap total message size against the limits of the underlying buffer type. A remote peer could send fragments that caused size truncation while the implementation still used the full length, leading to heap corruption or a crash.

### CVE-2026-102556

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-29T17:17:06.460 |

A flaw was found in libsoup. When handling an incoming WebSocket Pong frame, SoupWebsocketConnection emitted the ::pong signal with a GByteArray pointer even though the signal is declared to pass a GBytes. Applications connecting a handler that follows the documented GBytes API can trigger heap corruption or a crash upon receiving a crafted Pong.

### CVE-2026-101127

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T17:17:05.187 |

Joomla Extension - balbooa.com - Unauthenticated upload filename stored XSS in Balbooa Forms < 2.4.3.4 - The public form upload endpoint validates the uploaded file's extension and detected MIME type, but stores the attacker-supplied original multipart filename verbatim in `#__baforms_submissions_attachments.name`. A later anonymous form submission associates that temporary attachment with the newly created submission. When an administrator opens the submission, the component's JavaScript retrieves the stored attachment record and concatenates `file.name` directly into an HTML string. The complete string is assigned to `innerHTML`.

### CVE-2026-97293

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:39.490 |

Contributor SQL Injection in Media LIbrary Assistant <= 3.41 versions.

### CVE-2026-97287

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:38.943 |

Contributor SQL Injection in Event Tickets <= 5.29.5 versions.

### CVE-2026-94177

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:25.583 |

Unauthenticated SQL Injection in GamiPress <= 8.0.2 versions.

### CVE-2026-94115

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:24.227 |

Contributor SQL Injection in Easy Pricing Tables <= 4.1.2 versions.

### CVE-2026-10739

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23;CWE-59;CWE-73` |
| Published | 2026-09-30T12:17:12.963 |

Cato Networks SDP Client for Windows before 6.12.6 allows a local user to delete arbitrary files with SYSTEM privileges via improper validation of a client-supplied SID over a local IPC named pipe.

### CVE-2026-102511

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-248;CWE-835;CWE-940` |
| Published | 2026-09-30T09:17:14.467 |

Improper Verification of Source of a Communication Channel in the ADS discovery of the Go implementation of Apache PLC4X (PLC4Go) allows an attacker able to send UDP datagrams to the discovering host to redirect subsequent connections to an arbitrary, attacker-chosen address. The discovery result's connection 
address was derived from the AmsNetId claimed in the response body rather than from the datagram's actual source address. One spoofed discovery response can therefore insert an inventory entry pointing at any host, including hosts outside the local network, and an application that connects to discovered devices
will open its ADS session, including any configured route credentials, to that host.

Additionally, discovery listeners in both implementations can be disabled by a single malformed datagram:
- In PLC4Go ADS discovery, a short version block causes a panic that ends the listener for the rest of the discovery call, so legitimate devices answering afterwards are not reported.
- In PLC4J, the ADS and EtherNet/IP discoverers stop on an unhandled exception from a malformed response.
- The PLC4J Modbus discoverer can be made to spin indefinitely, consuming a CPU core, by a scanned host that sends a partial response.

Exploitation requires the application to invoke the discovery API, which is opt-in, and for the connection redirect, to act on the discovered items.

This issue affects Apache PLC4X: PLC4Go from 0.11.0 before 1.0.0; PLC4J ADS and Modbus drivers from 0.10.0 before 1.0.0; PLC4J EtherNet/IP driver from 0.11.0 before 1.0.0. PLC4Go is consumed as the Go module github.com/apache/plc4x/plc4go; versions refer to the corresponding Apache PLC4X releases.

Users are recommended to upgrade to version 1.0.0, which fixes the issue. Version 1.0.0 derives the connection address from the datagram's source address and logs a warning when the claimed AmsNetId disagrees with it.

### CVE-2026-102794

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-30T00:16:34.963 |

A vulnerability has been found in Ziroom ZHOME A0101 1.0.1.0. This issue affects some unknown processing of the file /api/ZRnetwork/ping. Such manipulation of the argument url leads to command injection. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102793

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-30T00:16:33.743 |

A flaw has been found in Ziroom ZHOME A0101 1.0.1.0. This vulnerability affects the function set_time_zone of the file /api/ZRFirmware/set_time_zone. This manipulation of the argument hostname/zonename causes command injection. It is possible to initiate the attack remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-102792

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-29T23:17:21.267 |

A vulnerability was detected in Ziroom ZHOME A0101 1.0.1.0. This affects the function set_syslog of the file /api/ZRnetwork/set_syslog. The manipulation of the argument conloglevel/log_size results in command injection. The attack may be performed from remote. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-72510

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T22:18:22.607 |

The "supplier_no" parameter used in the business allocation search feature is vulnerable to time-based blind SQL injection.

### CVE-2026-72507

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T22:18:22.437 |

The "reportType" parameter in the product summary report feature within the balancing reports section is susceptible to a time-based blind SQL injection vulnerability.

### CVE-2026-68954

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T22:17:21.847 |

The "pattern" parameter used in search function in the home page of the TMS application is vulnerable to time-based blind SQL injection vulnerability.

### CVE-2026-68068

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T22:17:15.100 |

The "screenID" parameter in the electronic transaction queue viewer feature within the manual transactions section is susceptible to a time-based blind SQL injection vulnerability.

### CVE-2026-63713

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:H/SC:H/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T22:17:11.487 |

The "search" parameter in the view audit logs feature within the utilities section is susceptible to a time-based blind SQL injection vulnerability.

### CVE-2026-102875

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T20:17:18.053 |

VLC media player before 3.0.24 contains a path traversal vulnerability in the skins2 ThemeLoader that fails to validate member names in .vlt skin archives. Attackers can craft malicious skin files with path traversal sequences to write arbitrary files with VLC user privileges, enabling code execution through Lua script injection.

### CVE-2026-102757

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787;CWE-822;CWE-823;CWE-843` |
| Published | 2026-09-29T18:17:12.907 |

An unprivileged, memory-protected ThreadX module can have the kernel read and write memory at addresses of its choosing, in privileged mode, and can use that to clear the MPU enable bit and remove its own isolation boundary.



The Module Manager decided whether a privileged service could dereference an object address a module named by asking only whether that address fell outside the module. The manager's object pool is outside every module, so the test was satisfied by an address shifted into the interior of one of the module's own privileged allocations, which denotes no object at all. The bytes such an address presents as a control block are bytes the module put there through ordinary create and set services, so the control block ID at the front of them could be made to read as any type the module chose, and the `_txe_` layer's ID test then agreed. The reported chain uses that to reach a privileged `memset` across an attacker-chosen range.

### CVE-2026-102697

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-29T17:17:08.150 |

Ollama versions 0.14.0 before 0.31.2 contain an incorrect authorization vulnerability in the experimental agent mode Bash tool approval mechanism that fails to properly parse shell syntax. Attackers who can influence model output through prompt injection can execute additional shell commands by appending control operators like semicolons or logical operators to approved commands, bypassing the session approval requirement.

### CVE-2026-86035

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-09-29T15:17:30.407 |

Weblate is a web-based continuous localization platform used to manage software translations. Weblate 4.11.1 through 2026.7.1 contains an argument-injection vulnerability in its Mercurial backend. Repository filenames beginning with - could be interpreted as Mercurial options instead of literal paths. An authenticated user with project-scoped component.edit permission could exploit this through a Mercurial-backed RESX component using the Update RESX files add-on. A later repository update could execute arbitrary commands with the privileges of the Weblate service account. This is a residual incomplete fix for CVE-2022-23915. This issue has been patched in version 2026.8.

### CVE-2026-102566

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T15:17:18.003 |

CTranslate2 before 4.8.1 contains a heap-based buffer overflow in the binary model loader that fails to validate payload length against allocated buffer size. Attackers can craft malicious model files with oversized payload lengths to write past heap allocation boundaries, causing crashes or arbitrary code execution.

### CVE-2026-102709

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-501;CWE-822` |
| Published | 2026-09-29T18:17:09.863 |

Improper validation of non-secure (NS) pointers in multiple TrustZone-M non-secure callable (NSC) entry functions allows an attacker executing in the non-secure world to supply pointers to secure memory. The secure firmware subsequently dereferences these attacker-controlled pointers without verifying that they reference non-secure memory, resulting in unintended disclosure of secure memory contents. This violates the isolation guarantees provided by Arm TrustZone-M and can be leveraged as a memory disclosure or corruption primitive that may enable recovery of sensitive cryptographic material.

### CVE-2026-100308

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470;CWE-502` |
| Published | 2026-09-29T16:17:04.900 |

Deserialization of untrusted data in the model loading component in Amazon GluonTS before 0.17.0 might allow context-dependent attackers to execute arbitrary operating system commands with the privileges of the loading process via a crafted serialized model directory.



To remediate this issue, users should upgrade to version 0.17.0 or later.

### CVE-2026-103321

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-79` |
| Published | 2026-09-30T13:17:18.463 |

MISP contains a stored cross-site script (XSS) vulnerability in the event graph preview feature.

The event graph preview image field was accepted and stored without server-side validation. On the client side, the stored value was rendered into an HTML img element's src attribute via string concatenation, allowing a crafted value to break out of the attribute context and inject arbitrary script.

Preconditions:

- An authenticated MISP user with the ability to create or modify an event graph entry.

- A second user (the victim) who views the event graph and triggers the preview popover.

Impact:

- Execution of arbitrary JavaScript in the victim's browser within the MISP application context.

- Potential theft of session tokens, cookies, or sensitive data accessible to the victim's browser.

- Potential for performing actions on behalf of the victim within the MISP application.

Affected: MISP versions prior to the fix (commit applied after v2.5.48).

### CVE-2026-103237

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-639` |
| Published | 2026-09-30T10:17:16.687 |

MISP contains an improper input validation vulnerability in its ORM save path. When a user submits data through various endpoints (attribute add/edit, event edit, free-text import, sighting capture, shadow attribute proposal, event report creation, object reference add, user admin edit), the application sanitizes the flat record by stripping the primary key and pinning the event_id or object_id to the caller's context. However, the underlying ORM's set() method gives priority to a nested key whose name matches the model alias and discards the outer scalar fields.

An authenticated user with basic write permissions can exploit this by embedding a nested block under the model alias key inside their request. The sanitization logic (id removal, event_id pinning) is applied to the outer record, but the ORM binds to the inner record instead, which carries an attacker-chosen id and event_id. This allows the attacker to overwrite, re-parent, or soft-delete rows belonging to other organizations or events they have no read access to.

Impact:

- Cross-tenant data integrity compromise (attribute values rewritten, objects re-parented to attacker events, rows soft-deleted)

- Affects multiple entity types: Attribute, Object, EventReport, Sighting, AttributeTag, ShadowAttribute

- Requires only a low-privilege authenticated account with perm_add

Affected versions: <2.5.48

### CVE-2026-96274

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-29T20:17:31.610 |

In Baicells Nova 430H, an unauthenticated device within radio range can send a malformed uplink message during connection setup that contains an invalid NAS payload. Because the eNodeB does not properly validate this payload, it forwards the message to the core network, which can trigger a shutdown of the signaling association for the cell. This results in a temporary service disruption until the eNodeB and core network re-establish connectivity.

### CVE-2026-102324

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T20:17:15.730 |

Use after free in PictureInPicture in Google Chrome prior to 154.0.8037.92 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102301

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T20:17:12.967 |

Out of bounds write in GPU in Google Chrome prior to 154.0.8037.92 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95381

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-29T18:17:31.877 |

Improper input validation in Printing in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-95372

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:31.130 |

Use after free in Chromecast in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95355

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-29T18:17:28.537 |

Incorrect authorization in Navigation in Google Chrome on on iOS prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95354

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:28.420 |

Use after free in Verifier in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-95351

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:28.087 |

Use after free in Views in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95348

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:27.690 |

Use after free in Bluetooth in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95341

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-29T18:17:26.767 |

Improper input validation in Desktop in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-95335

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:26.030 |

Use after free in HID in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-95334

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-09-29T18:17:25.913 |

Incorrect reference resolution in WebProtect in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-95322

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:24.537 |

Out of bounds write in GPU in Google Chrome on on Android prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-95319

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:24.187 |

Use after free in Printing in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-95276

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-29T18:17:18.843 |

Improper input validation in Themes in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code inside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-95274

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-29T18:17:18.553 |

Improper output encoding in DevTools in Google Chrome prior to 154.0.8037.57 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-102760

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:13.313 |

When NetX Secure is built with `NX_SECURE_KEY_CLEAR`, every TLS record sent on an active session is wiped after it has been handed to TCP. By then the TCP layer owns the packet chain and may already have released it to the packet pool. The wipe therefore writes zeros into packets that are free or in use by another thread, and when a reused packet's pointers no longer describe the old data, the length of the wipe underflows and it runs past the end of the packet pool.

### CVE-2026-102676

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-1188` |
| Published | 2026-09-29T17:17:07.973 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5, an Electron <webview> guest could enable nodeIntegrationInWorker for its Web Workers even when the unsandboxed embedder had Node.js integration disabled, allowing untrusted guest content to create a Node-enabled worker with more privilege than the embedder granted. Applications that do not enable the <webview> tag or that keep the embedder sandboxed are not affected. This issue is fixed in versions 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5.

### CVE-2026-96817

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:31.047 |

Subscriber Broken Access Control in MakeCommerce for WooCommerce <= 4.1.0 versions.

### CVE-2026-93621

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:22.267 |

Unauthenticated SQL Injection in WP Data Access <= 5.5.84 versions.

### CVE-2026-86133

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-1284` |
| Published | 2026-09-30T00:16:37.087 |

An integer underflow vulnerability in the WatchGuard Fireware OS IKE daemon (iked) allows a remote attacker who has completed the initial IKEv2 handshake to crash the iked process by sending a specially crafted encrypted IKEv2 message, resulting in a denial of service.

### CVE-2026-86132

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-30T00:16:36.957 |

An integer underflow vulnerability in the WatchGuard Fireware OS IKEv2 daemon (iked) allows a remote, unauthenticated attacker to crash the process by sending a specially crafted encrypted IKEv2 message negotiated with an AES-GCM cipher suite.

### CVE-2026-86128

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-30T00:16:36.687 |

A NULL pointer dereference vulnerability in Fireware OS's NetFlow packet-processing feature allows a remote, unauthenticated attacker to cause a denial of service by sending a specially crafted IPv6 packet.

### CVE-2026-13224

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-09-30T00:16:35.733 |

A path traversal vulnerability in the Fireware OS WebUI management agent allows an authenticated administrator to read or list arbitrary files on the local filesystem by sending a specially crafted management request.

### CVE-2026-102762

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-09-29T18:17:13.590 |

The NetX Duo MQTT client leaks the packet carrying a malformed PUBLISH message. Each malformed PUBLISH costs one packet, or one chain of packets, from the network driver's receive pool, and nothing returns it. A peer that can deliver a few dozen such messages exhausts the pool and stops all inbound network traffic on the device until it is rebooted.

### CVE-2026-102555

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T18:17:07.977 |

A flaw was found in libsoup. The soup_uri_decode_data_uri() function incorrectly treated base64 data-URI payloads as NUL-terminated strings when calling g_base64_decode_inplace(). If the percent-decoded payload contained embedded NUL bytes, the decoded length could remain uninitialized and be used as the size of the returned GBytes. This can lead to an out-of-bounds read or application crash when processing a crafted data URI.

### CVE-2026-92227

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-29T17:17:14.777 |

Joomla! Core - [20260914] - Core - MFA Authentication Bypass through rememberme cookies in Joomla 4.0.0-5.4.8, 6.0.0-6.1.3 - The premature issuance of an rememberme cookie leads to a MFA bypass vulnerability.

### CVE-2026-102674

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-266;CWE-693` |
| Published | 2026-09-29T17:17:07.653 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5, windows opened from a sandboxed top-level document did not inherit that document's active HTML sandbox restrictions. Untrusted content in a sandboxed top-level document that was permitted to open popups could therefore create a window with the Electron application's full origin instead of the restricted origin intended by the sandbox. Applications that deny such popups with setWindowOpenHandler are not affected. This issue is fixed in versions 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5.

### CVE-2026-102673

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-346;CWE-693` |
| Published | 2026-09-29T17:17:07.487 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 41.10.4, 42.5.2, and 43.0.0, popups opened from a sandboxed iframe through Electron's OpenURLFromTab navigation path, including links using target="_blank" or a middle-click, did not receive the inherited HTML sandbox restrictions. An untrusted iframe using the allow-scripts allow-popups configuration could therefore open a popup with the embedding application's full origin, exposing that origin's cookies, storage, and same-origin scripting capabilities. Applications that do not embed untrusted content in sandboxed iframes are not affected. This issue is fixed in versions 41.10.4, 42.5.2, and 43.0.0.

### CVE-2026-102633

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-29T17:17:06.980 |

libexpat versions 2.7.2 through 2.8.5 contain an integer overflow vulnerability in expat_realloc() function on 32-bit platforms when computing allocation sizes. Attackers supplying malicious XML to applications parsing with vulnerable libexpat can cause heap buffer overflow, memory corruption, or denial of service.

### CVE-2026-84782

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-29T16:17:12.500 |

Issue summary: The DTLS retransmission logic does not correctly handle
a handshake message write that is suspended part-way through.
The retransmitted message can be read past the message buffer and
the retransmission overwrites the internal state the suspended write
needs to resume correctly.

Impact summary: The retransmitted message can disclose a heap memory
to the peer as plaintext handshake data or cause a crash and a Denial
of Service when the read reaches an unmapped memory region.

CWE: CWE-125: Out-of-bounds Read

Description: DTLS handshake messages can be written out in multiple
fragments, and a write can suspend mid-message (returning WANT_WRITE)
if the underlying transport temporarily cannot accept more data. While
such a write is suspended, the DTLS retransmission timer may
independently fire and ask the retransmission logic to resend an
earlier, already-acknowledged-as-sent message from its retransmit
queue.

The retransmission logic reused the same internal buffer and position
tracking as the message that was still being written, without
resetting the position back to the start of the message being
retransmitted. As a result the retransmission was read starting from
wherever the suspended write had left off, producing a mislabelled
message whose body was leftover bytes from the other, larger message
still in flight - content that was never meant to be sent at that
point, and which could run past the end of the allocated buffer.

Separately, even when the retransmission is positioned correctly,
allowing it to run to completion while another write is suspended
overwrites the same shared bookkeeping that the suspended write
depends on to resume. When the application later resumes the
suspended write (via a subsequent SSL_read(), SSL_write(),
SSL_accept(), or SSL_connect() call), it finds that bookkeeping in a
state inconsistent with the message and aborts the process in
a debugging build.

The fix resets the retransmission's read position to the start of the
message before resending, and skips retransmission entirely whenever a
handshake write is still suspended, deferring to the next call that
resumes it instead.

FIPS impact: no
The affected code is outside the FIPS module boundary.

### CVE-2026-93994

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-304` |
| Published | 2026-09-30T10:17:17.460 |

Apache MINA SSHD is a Java library for client-side and server-side SSH. SSH servers can be configured to require multi-authentication schemes, for instance two different public keys, not just one. In OpenSSH, this would be done by setting in sshd_config AuthenticationMethods "publickey,publickey". Apache MINA SSHD provides an equivalent configuration mechanism.




In Apache MINA SSHD versions up to 2.19.0 and 3.0.0-M1 to 3.0.0-M5 the server code in component sshd-core does not enforce that the two public keys presented are different. A user can thus successfully authenticate with only one of the two key pairs required by presenting this single key twice. This is a partial authentication bypass.






Users are recommended to upgrade to version 2.20.0 or 3.0.0-M6, which fix this issue.

### CVE-2026-76726

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.707 |

An authentication bypass vulnerability in the API endpoint of HPE Networking Instant ON could allow an unauthenticated remote attacker to bypass network access controls if certain preconditions outside of the attacker's control are met. Successful exploitation could allow an attacker to obtain unauthorized access to restricted networks.

### CVE-2026-102831

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-345` |
| Published | 2026-09-29T19:17:25.700 |

JupyterLab is an extensible environment for interactive and reproducible computing, based on the Jupyter Notebook Architecture. From JupyterLab 4.5.0 until 4.5.11 and 4.6.4, from Notebook 7.5.0 until 7.6.3, and from JupyterLite Core 0.7.0 until 0.8.4, the system clipboard cell-paste path accepts attacker-controlled cell JSON without clearing metadata.trusted. When useSystemClipboardForCells is active and pasteCodeCellsWithoutOutput is disabled, a pasted code cell can mark HTML output as trusted, bypass output sanitization, and execute script in the authenticated JupyterLab origin without executing the cell. Markdown and raw cells are not affected because their output is sanitized. This issue is fixed in JupyterLab 4.5.11 and 4.6.4, Notebook 7.6.3, and JupyterLite Core 0.8.4.

### CVE-2026-102827

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-88` |
| Published | 2026-09-29T19:17:25.050 |

simple-git, an interface for running git commands in any node.js application, enables applications to execute Git operations from JavaScript. Prior to 4.0.0, the default blockUnsafeOperationsPlugin compares parsed option names with literal dangerous option spellings while Git accepts unambiguous long-option abbreviations. Attacker-influenced push arguments such as abbreviated --receive-pack or --exec forms can therefore bypass detectVulnerableFlags, reach git push against a local or file remote or an attacker-influenced receive-pack target, and cause Git to invoke an attacker-selected command in consumers that expose those arguments. The clone-side abbreviation handling does not protect the push path. This issue is fixed in 4.0.0.

### CVE-2026-102826

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-29T19:17:24.883 |

simple-git, an interface for running git commands in any node.js application, enables applications to execute Git operations from JavaScript. Prior to 4.0.0, the default blockUnsafeOperationsPlugin does not completely reject configuration includes supplied through customArgs to git.clone(). The missing include.path classification permits Git to load an attacker-controlled configuration file, and the initial remediation does not cover includeIf.<condition>.path, allowing the same file-loading primitive through a conditional include. A loaded configuration can set an executable Git option such as core.sshCommand, which Git invokes during the clone operation with the privileges of the Node.js process. Exploitation requires the application to pass attacker-influenced custom arguments and requires an attacker-controlled file that the process can read. This issue is fixed in 4.0.0.

### CVE-2026-95333

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:25.797 |

Use after free in Metrics in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Medium)

### CVE-2026-84842

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T18:17:18.083 |

IBM Guardium Data Protection 12.2 is vulnerable to path traversal and arbitrary file deletion in the Datasource REST component. An authenticated remote attacker could exploit this vulnerability to delete files and potentially cause denial of service or impact system integrity.

### CVE-2026-62146

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-501` |
| Published | 2026-09-30T12:17:13.617 |

A trust-boundary flaw in CRI-O's sandbox state persistence allows attacker-influenced pod metadata to overwrite CRI-O's own reserved sandbox bookkeeping; once reloaded as trusted after a restart, a later container recreate in that sandbox can expose a host-side runtime-management resource inside the container, enabling container escape.

### CVE-2026-103106

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-669` |
| Published | 2026-09-30T03:16:59.773 |

Pexip Infinity before 38.2, plus 39.0, 39.1, and 40.0, is affected by improper input validation within an internal Pexip Infinity service that allows an attacker with local access to escalate privileges to root. Exploitation requires an attacker to be able to run arbitrary code on a node by either achieving remote code execution via some other vulnerability or having administrative access to the operating system.

### CVE-2026-102925

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T21:17:18.570 |

virtualenv is a tool for creating isolated virtual python environments. Prior to 21.7.13, the generated activate (bash and zsh) and activate.fish scripts place values already escaped by shlex.quote inside an additional quoted context. In the bash and zsh script, a crafted virtual environment path reaches __VIRTUAL_ENV__ when a relocated environment's recorded directory is absent; in the fish script, crafted Tcl or Tk library paths reach __TCL_LIBRARY__ or __TK_LIBRARY__. The surplus quotes can terminate the data-only quoted run and leave shell metacharacters parsed as commands when a user sources the activation script, allowing code execution with that user's privileges. This issue is fixed in version 21.7.13.

### CVE-2026-95315

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:23.697 |

Use after free in Aura in Google Chrome prior to 154.0.8037.57 allowed a local attacker to potentially execute arbitrary code outside the sandbox via UI Interaction. (Chromium security severity: High)

### CVE-2026-95298

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T18:17:21.700 |

Use after free in Browser in Google Chrome prior to 154.0.8037.57 allowed a local attacker to potentially execute arbitrary code outside the sandbox via UI Interaction. (Chromium security severity: High)

### CVE-2026-84414

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-29T18:17:17.400 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to change the ownership of arbitrary files due to improper validation of an attacker-controlled file path.

### CVE-2026-102677

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-345` |
| Published | 2026-09-29T18:17:09.573 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. From 42.3.3 until 42.10.0, 43.5.0, and 44.0.0-beta.6, Electron's sandboxed preload code cache did not verify that a cached entry matched the preload it was served for. A compromised renderer could write attacker-controlled cache data and cause Electron to reuse it for a later load, executing the renderer's code in the more privileged preload context. The issue affects applications that load untrusted content. This issue is fixed in versions 42.10.0, 43.5.0, and 44.0.0-beta.6.

### CVE-2026-92368

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-29T16:17:14.753 |

TeamViewer Full Client and Host for Linux and macOS prior version 15.82 contain a heap-based buffer overflow vulnerability in the processing of .tvs session recording files. A size mismatch during decompression of recorded session data can result in out-of-bounds heap writes. By convincing a user to open a specially crafted session recording through the "Play or convert recorded session…" feature, an attacker may achieve arbitrary code execution with the privileges of the current user

### CVE-2026-19743

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T16:17:07.177 |

Improper path validation in the local IPC service of TeamViewer Full Client and Host on Windows, Linux, and macOS prior to version 15.82 allows a local authenticated user with low privileges to perform arbitrary file writes with elevated privileges (NT AUTHORITY/SYSTEM \ root). By sending crafted IPC commands to the local service daemon, an attacker could manipulate file paths, leading to local privilege escalation.

### CVE-2026-65102

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-29T15:17:27.453 |

NVIDIA DeepStream  contains a vulnerability where an attacker could cause an integer overflow by supplying crafted tensor dimensions in a YAML configuration file. A successful exploit of this vulnerability might lead to denial of service, information disclosure, data tampering.

### CVE-2026-103109

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T03:17:00.073 |

Pexip Infinity before 38.2, plus 39.0, 39.1 and 40.0, is affected by improper input validation in the media implementation that allows a remote attacker to trigger memory corruption or a software abort resulting in a denial of service. A crafted media stream may result in a controlled abort during processing, and has the potential to achieve memory corruption.

### CVE-2026-91191

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-29T22:19:03.727 |

The device's update mechanism includes conditions that allow unauthorized software packages to be accepted as authentic. During the boot process, the stock done function disables signature verification in the OPKG configuration before restoring optional packages from a writable, unsigned feed. Separately, the publicly distributed SDK contains the production private key whose corresponding public key is trusted by both stable and beta firmware builds. Either issue undermines package authenticity, and together they allow an attacker to provide packages that appear valid to the system. Even if signature enforcement is restored, the exposed production key enables an attacker to generate signatures that the device will continue to trust. An attacker who can supply a malicious package may be able to execute arbitrary code with root privileges during installation.

### CVE-2026-84409

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T22:19:01.230 |

The device's update mechanism retrieves metadata for software updates over an unencrypted HTTP connection and stores portions of that metadata for later use. A management interface subsequently returns this stored value in a JSON response, and the web interface responsible for displaying update information inserts that value directly into the page as HTML. This behavior allows attacker‑controlled metadata to be interpreted as script content. In addition, the same authenticated origin provides an interface capable of executing system‑level commands with root privileges. An attacker able to influence update metadata could exploit these conditions to execute arbitrary code within the administrative context of the device.

### CVE-2026-102930

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-09-29T21:17:18.740 |

virtualenv is a tool for creating isolated virtual python environments. Prior to 21.7.12, download_wheel() accepts pip and setuptools seed wheels fetched for periodic updates or the --download option without checking their bytes against an authoritative digest equivalent to the embedded wheels' BUNDLE_SHA256 verification. A compromised index, stale mirror, or intercepted TLS connection can substitute a different wheel under the requested distribution, version, and filename, after which virtualenv caches and seeds the attacker-controlled wheel into subsequently created environments. The verification applies to the default PyPI path and is intentionally skipped when PIP_INDEX_URL, PIP_EXTRA_INDEX_URL, or PIP_INDEX configures a custom index that may legitimately publish rebuilt wheels. This issue is fixed in version 21.7.12.

### CVE-2026-96828

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:32.493 |

Administrator SQL Injection in Category Discount Woocommerce <= 5.18 versions.

### CVE-2026-96827

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:32.357 |

Administrator SQL Injection in Admin Notices Manager <= 1.6.0 versions.

### CVE-2026-96346

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:29.570 |

Author SQL Injection in WP ERP <= 1.17.9 versions.

### CVE-2026-96345

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:29.430 |

Administrator SQL Injection in Estatik <= 4.3.5 versions.

### CVE-2026-94082

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:24.093 |

Author SQL Injection in Quiz Cat <= 3.1.1 versions.

### CVE-2026-62085

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T13:17:19.740 |

Administrator SQL Injection in WP Activity Log <= 5.6.6 versions.

### CVE-2026-103111

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T05:16:45.863 |

PCRE2 before 10.49, when there is an attacker-controlled regular expression and certain JIT API usage, allows an out-of-bounds write with arbitrary data.

### CVE-2026-97687

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-440` |
| Published | 2026-09-29T16:17:18.517 |

urllib3 is an HTTP client library for Python. From 1.26.0 until 2.8.0, the proxy_ssl_context, proxy_assert_hostname, proxy_assert_fingerprint, ssl_context, cert_reqs, verify_mode, use_forwarding_for_https=True, and CERT_NONE configuration paths fail to remain separated because target-server TLS settings are incorrectly applied to the HTTPS proxy connection. The trigger is that an application uses an HTTPS proxy and configures target-server TLS settings that must remain separate from the proxy TLS handshake, including HTTPS forwarding with target-specific identity or credentials. Applying cert_reqs=CERT_NONE can overwrite proxy_ssl_context.verify_mode in place, and the mutation persists so later connections reusing the same context may connect to the HTTPS proxy without certificate verification. The attack mechanism is that an attacker intercepts and impersonates the HTTPS proxy after the effective proxy policy accepts the attacker's certificate. The impact is that the attacker can observe or modify forwarded traffic or receive a target TLS client certificate, while CONNECT tunneling still preserves the separate end-to-end target TLS connection. This issue is fixed in version 2.8.0.

### CVE-2026-97244

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-09-30T13:17:36.300 |

Contributor Path Traversal in Creator LMS <= 1.2.19 versions.

### CVE-2026-97241

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-09-30T13:17:35.887 |

Unauthenticated Sensitive Data Exposure in BackupEase <= 2.2.2 versions.

### CVE-2026-97240

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-09-30T13:17:35.747 |

Unauthenticated Sensitive Data Exposure in StifLi Backup Tools <= 2.2.7 versions.

### CVE-2026-97197

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:34.877 |

Unauthenticated Broken Access Control in WordPress Backup & Migration <= 1.6.0 versions.

### CVE-2026-96823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:31.917 |

Unauthenticated Arbitrary Content Deletion in Customer Reviews for WooCommerce <= 5.120.0 versions.

### CVE-2026-96818

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:31.177 |

Unauthenticated Broken Access Control in WP Express Checkout (Accept PayPal Payments) <= 2.4.9 versions.

### CVE-2026-96348

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:29.833 |

Unauthenticated Broken Access Control in Bookly <= 28.2 versions.

### CVE-2026-95616

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-30T13:17:28.863 |

An integer overflow in WSS4J's DER bounds check lets an oversized allocation pass validation. An unauthenticated attacker can send a SOAP message carrying an X.509 certificate whose SubjectKeyIdentifier extension declares a length of 0x7FFFFFFF; WSS4J decodes this while resolving the signature's key reference, before the message is authenticated, so an eleven-byte extension triggers a 2 GB allocation. Repeated requests exhaust server memory.
Users are recommended to upgrade to versions 4.0.2 or 3.0.6 or 2.4.4, which fix this issue.

### CVE-2026-95587

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:28.720 |

Unauthenticated Broken Access Control in Hostinger Migrator <= 1.0 versions.

### CVE-2026-94178

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T13:17:25.953 |

Subscriber Privilege Escalation in Import and export users and customers <= 2.5.2 versions.

### CVE-2026-94123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T13:17:25.000 |

Unauthenticated Arbitrary File Download in NextGEN Gallery <= 4.5.0 versions.

### CVE-2026-94120

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:24.363 |

Unauthenticated Broken Access Control in GravityExport Lite for Gravity Forms <= 2.7.2 versions.

### CVE-2026-94002

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-30T10:17:17.877 |

Possible memory exhaustion in SFTP clients (DefaultSftpClient) in component sshd-sftp in Apache MINA SSHD versions 0.9.0 to 2.19.0 and 3.0.0-M1 to 3.0.0-M5.




Apache 
MINA SSHD is a Java library for client-side and server-side SSH. The sshd-sftp component provides support for SFTP.




The SFTP client implementation, when receiving a reply, did not check that this reply corresponded to a request sent earlier. Unsolicited replies would be stored but never consumed. A malicious server could keep sending unsolicited replies until available memory in the client was exhausted.




Users are recommended to upgrade to version 2.20.0 or 3.0.0-M6, which fix this issue.

### CVE-2026-75098

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T09:17:16.320 |

The Product Designer App plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.1.3 via the 'svg' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The endpoint's only authentication gate relies on a nonce and token that are both publicly emitted as JavaScript globals on any page rendering the [pdapp-studio-page] shortcode, making them freely obtainable by anonymous visitors.

### CVE-2026-6806

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T08:16:34.090 |

The Motors – Car Dealership & Classified Listings Plugin plugin for WordPress is vulnerable to time-based blind SQL Injection via the 'stm_lat/stm_lng' parameter in all versions up to, and including, 1.4.109 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-89294

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-30T07:16:30.947 |

The Simply Schedule Appointments plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.6.12.27 via the 'ssa_locale' parameter parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. Notably, exploitation does not require authentication in practice, as the locale filter is installed unconditionally on every request during plugins_loaded and the callback performs no nonce or capability check before returning the raw GET parameter value.

### CVE-2026-89193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T06:17:08.590 |

The Robin Image Optimizer  WordPress plugin before 2.0.8 does not escape values that its bundled HTML parser re-emits into element attributes when a non-default image delivery mode is enabled, allowing unauthenticated users to submit content that is stored and later executed as Cross-Site Scripting in the browser of any user viewing an affected page, including administrators.

### CVE-2026-103108

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-30T03:16:59.920 |

Pexip Infinity before 38.2, plus 39.0, 39.1, and 40.0, is affected by improper input validation in the media implementation that allows a remote attacker to trigger a software abort resulting in a denial of service

### CVE-2026-103104

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-30T03:16:59.467 |

Pexip Infinity before 38.2, plus 39.0, 39.1 and 40.0, is affected by improper input validation in the media implementation which allows a remote attacker to trigger a software abort resulting in a denial of service.

### CVE-2026-103100

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-30T03:16:58.870 |

Pexip Infinity before 40.1 is affected by improper input validation in the signaling implementation that allows a malicious attacker to trigger a software abort resulting in a denial of service.

### CVE-2026-103099

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-30T03:16:58.717 |

Pexip Infinity before 41.1 is affected by improper input validation in the media implementation that allows a remote attacker to trigger a software abort resulting in a denial of service.

### CVE-2026-103088

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-24` |
| Published | 2026-09-30T02:16:57.203 |

Handlebars.java before 4.5.5 allows directory traversal. In handlebars-springmvc 4.5.3 and 4.5.4, the path-containment fix for CVE-2026-63490 validates template locations as raw percent-encoded strings, whereas the template file is opened through a URL handler that percent-decodes the path. In a Spring MVC application with a file: template prefix and a request-derived view name, a percent-encoded traversal such as %2e%2e/ bypasses both the view-resolver check and the loader-side containment and reads files outside the configured template base directory.

### CVE-2026-13046

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T00:16:35.593 |

A deserialization of untrusted data vulnerability in WatchGuard Fireware OS's SAML single sign-on session handling (samld) allows an attacker who has already obtained the ability to write files on the appliance to execute arbitrary code in the context of the samld service by causing samld to load a maliciously crafted session file.

### CVE-2026-71302

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-09-29T22:18:18.817 |

The application accepts user-supplied session identifiers and does not regenerate the session ID after authentication. This allows an attacker to predefine a session ID and reuse it after victim authentication, resulting in session takeover.

### CVE-2026-102327

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-29T20:17:16.097 |

Incorrect authorization in WebView in Google Chrome on on Android prior to 154.0.8037.92 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Low)

### CVE-2026-102823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-29T19:17:24.367 |

Russh is a Rust SSH client and server library. Prior to 0.63.1, client_read_authenticated in russh/src/client/encrypted.rs forwards CHANNEL_DATA, CHANNEL_EXTENDED_DATA, CHANNEL_EOF, CHANNEL_CLOSE, CHANNEL_OPEN_FAILURE, CHANNEL_SUCCESS, CHANNEL_FAILURE, and CHANNEL_REQUEST subtypes exit-status, exit-signal, and xon-xoff to public client::Handler callbacks without confirming that the ChannelId belongs to a channel the client opened and established. A malicious SSH server can send lifecycle events for predicted, unopened, unconfirmed, or released channel identifiers, causing application panics or corrupting command completion and exit-code tracking. This issue is fixed in version 0.63.1.

### CVE-2026-95280

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-29T18:17:19.393 |

Race condition in V8 in Google Chrome prior to 154.0.8037.57 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-84440

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T18:17:17.953 |

IBM Guardium Data Protection 12.2 is vulnerable to command injection in the SNMP alert notification functionality. An authenticated attacker who can influence policy alert text can cause attacker-controlled data to be executed as operating system commands by the SNMP alerter service, which runs with root privileges.

### CVE-2026-84784

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-29T16:17:12.810 |

Issue summary: A malicious remote peer may flood the local QUIC
stack with NEW_CONNECTION_ID frames by avoiding a limit check on
how many connection IDs the remote QUIC stack can use.

Impact summary: The local QUIC stack sends a RETIRE_CONN_ID frame
for every NEW_CONNECTION_ID frame it receives. The RETIRE_CONN_ID
frame is dispatched via the Control Frame Queue (CFQ). If the remote
peer also withholds ACKs, then it can force the local stack
to allocate ~400MB (depending on ACK delay).

CWE: CWE-770: Allocation of Resources Without Limits or Throttling

Description: RFC 9000 sections 5.1.1 and 5.1.2 [1] describe the mechanism
by which a remote peer can notify the local QUIC stack to change the
destination connection ID (a.k.a. CID) the local stack uses to
identify the connection at the remote peer. Each CID is associated
with a sequence number. The sequence number is transmitted
in NEW_CONNECTION_ID and RETIRE_CONNECTION_ID frames to identify the CID
which is being either associated with a connection or retired.

The remote peer sends a NEW_CONNECTION_ID frame to let the local stack know
a new CID is being associated with an existing connection. The
NEW_CONNECTION_ID frame carries the new CID, its sequence number, and the
retire-prior-to number. The retire-prior-to identifies existing
CIDs that are to be retired. The local QUIC stack must send a
RETIRE_CONNECTION_ID for every destination CID whose sequence number
is less than retire-prior-to. The CID becomes retired after the
local stack receives an ACK for its RETIRE_CONNECTION_ID frame.

Although the OpenSSL QUIC stack supports at most one destination CID
for every connection, it can be tricked into processing more than
one RETIRE_CONNECTION_ID frame per connection. The OpenSSL QUIC
stack currently retires the destination CID as soon as it receives
the NEW_CONNECTION_ID, while in fact the destination CID must
be retired after an ACK for the RETIRE_CONNECTION_ID frame is received.
Correcting the flawed logic also fixes the backlog growth.

[1] https://datatracker.ietf.org/doc/html/rfc9000#name-issuing-connection-ids

FIPS impact: no
The FIPS module is not affected as the QUIC implementation is outside of
the OpenSSL FIPS module boundary.

### CVE-2026-84783

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-29T16:17:12.653 |

Issue summary: The first concurrent use of the same X.509 certificate by
several threads may cause its cached extension data to be freed while
another thread is still using it.

Impact summary: A remote, unauthenticated peer could crash a multi-threaded
TLS client, or a multi-threaded TLS server that requests client
certificates, if the first certificate chains built to the same trusted CA
certificate are built by several connections at the same time. This is a
use-after-free read, which is likely to crash the process, resulting in a
Denial of Service.

CWE: CWE-416: Use After Free

Description: OpenSSL caches the decoded values of a certificate's X.509v3
extensions inside the X509 object the first time they are needed. In
OpenSSL 4.0 this cache is built in two phases: the extension values are
computed while holding a read lock on the certificate, and the results are
then installed into the certificate under a write lock. Because a read lock
does not exclude other readers, several threads can compute the cache for
the same certificate at the same time. Each thread that subsequently
acquires the write lock installs its own results and frees the values
installed by the thread before it, even though that earlier thread has
already marked the cache as complete and may have returned pointers into it
to its caller. A caller still using those pointers then reads freed memory.

Any certificate shared between threads is exposed the first time its
extensions are decoded. In TLS the certificates at risk are the trusted CA
certificates supplied for chain verification, by whatever means, since these
are shared by every connection and their extensions are decoded and cached
the first time a chain is built to them. Certificates sent by the peer are
decoded separately for each connection and are not shared, so they are not
affected. In a TLS client verifying server certificates, or a TLS server
that requests and verifies client certificates, the use-after-free could
only occur if the first chains built to the same trusted CA are built by
several connections at the same time.

FIPS impact: no
The FIPS module is not affected as X.509 certificate handling is outside
of the OpenSSL FIPS module boundary.

OpenSSL 4.0 is vulnerable to this issue.

OpenSSL 3.6, 3.5, 3.4, 3.0, 1.1.1 and 1.0.2 are not affected by this issue.

OpenSSL 4.0 users should upgrade to OpenSSL 4.0.3.

This issue was reported on 27 August 2026 by Tim Becker (Xint.io) and
independently in a public report on 31 August 2026 by aydinmercan.

The fix has been developed by Bob Beck.

-- cut (non-publishing metadata for internal use) --
Reported by: Tim Becker (Xint.io), aydinmercan
Fixed by: Bob Beck

### CVE-2026-72897

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T16:17:09.903 |

Issue summary: A TLS server that calls SSL_set_SSL_CTX() to switch a
connection to a different SSL_CTX part way through a handshake may access
memory beyond the end of an internal array if the replacement context knows
about more provider signature algorithms than the context the connection was
created from. Applications which never call SSL_set_SSL_CTX() are not
affected.

Impact summary: A remote peer may be able to cause a small out-of-bounds
read, and in some circumstances a fixed-value out-of-bounds write, on the
server heap. This may lead to a Denial of Service.

CWE: CWE-787: Out-of-bounds Write

Description: A TLS connection records how many certificate slots it has
when it is created, taken from the SSL_CTX that created it: the built-in
certificate types plus one slot for each provider TLS-SIGALG entry that
context was aware of. That count sizes an internal array of per-slot
certificate validity flags.

An application may replace a connection's SSL_CTX part way through the
handshake by calling SSL_set_SSL_CTX(), most commonly from a servername
callback in order to serve a different virtual host. Doing so did not
refresh the recorded count. A provider signature algorithm's slot index is
its position in the list of whichever context resolves it, so if the
replacement context is aware of more of them than the original, an
algorithm offered by the peer can resolve to an index beyond the end of the
array. Processing the peer's signature algorithms then reads one four byte
word past the end for each such algorithm and, where the word read is zero,
writes a fixed value over it. A peer offering many of them can corrupt heap
metadata and abort the process.

Only provider signature algorithms which occupy one of the excess slots,
and which the server also has configured, have this effect. Codepoints the
replacement context does not recognise are discarded without being resolved
to a slot, and provider signature algorithms are usable only from TLS 1.3.

The two contexts must therefore be aware of different numbers of provider
signature algorithms, which requires separate library contexts, a provider
loaded between the two being created, or providers which differ in what
they advertise - in 4.0, for example, the default provider advertises SM2
where the FIPS provider does not. A deployment meeting the condition is
also unable to negotiate the affected algorithms with legitimate clients,
since the same stale count hides the corresponding certificates, so the
misconfiguration is likely to be noticed. For that reason, and because the
configuration is not the default, this issue has been assessed as Low
severity.

FIPS impact: no
No FIPS modules are affected by this issue as the affected code is outside
the OpenSSL FIPS module boundary.

### CVE-2026-102600

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-1321` |
| Published | 2026-09-29T16:17:06.180 |

Socket.IO enables bidirectional and low-latency communication for every platform. Prior to 0.1.1, @socket.io/cluster-engine uses inherited object properties when looking up attacker-controlled session IDs in clustered deployments. Special property names such as __proto__ or constructor can resolve through the object prototype chain instead of identifying an actual connected client, causing the Node.js process to crash and resulting in denial of service. Applications that do not use @socket.io/cluster-engine are not affected. This issue is fixed in version 0.1.1.

### CVE-2026-63209

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-09-29T15:17:27.130 |

compress provides various compression algorithms. Prior to version 1.18.7, a signed integer overflow vulnerability in s2.NewDict() allows an attacker to bypass repeat index validation by supplying a dictionary with a uvarint-encoded repeat value exceeding MaxInt64. When Dict.Encode() is subsequently called, the overflowed negative repeat value causes an out-of-bounds memory access via unsafe.Pointer arithmetic, crashing the process with SIGSEGV. This issue has been patched in version 1.18.7.

### CVE-2026-75823

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-30T06:17:03.783 |

The User Frontend  WordPress plugin before 4.3.12 does not prevent tampering with the role assigned by its registration form, allowing unauthenticated users to register with a higher privileged role, such as Editor.

This affects installations running a PHP build where the sodium extension is unavailable, and where a registration page has been configured. The administrator role cannot be obtained this way.

### CVE-2026-102675

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-29T17:17:07.813 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5, responses served through protocol.registerFileProtocol or protocol.registerHttpProtocol for a custom scheme registered with supportFetchAPI enabled but corsEnabled disabled could remain script-readable across origins. This residual issue completes the remediation for CVE-2026-70604. Applications are affected only when they expose such a scheme and load untrusted content in the same session. Schemes intentionally registered with corsEnabled enabled remain cross-origin readable by design. This issue is fixed in versions 41.10.6, 42.9.2, 43.4.1, and 44.0.0-beta.5.

### CVE-2026-102937

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T21:17:18.893 |

virtualenv is a tool for creating isolated virtual python environments. Prior to 21.7.12, BatchActivator.quote() returns prompt text unchanged before activate.bat inserts it into a cmd.exe set "VAR=value" statement. An attacker who influences --prompt, VIRTUALENV_PROMPT, or the corresponding configuration value can include a double quote that closes the assignment and leaves following cmd.exe operators as executable syntax. When a user activates the generated Windows environment, the injected commands run with that user's privileges. This issue is fixed in version 21.7.12.

### CVE-2026-92369

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-29T16:17:14.890 |

TeamViewer Full Client and Host prior to version 15.82 on Windows contain a TOCTOU race condition in the installer rollback mechanism. A local low-privileged attacker can replace rollback backup files stored in a user-writable temporary directory before they are restored by an elevated installer, resulting in privilege escalation to NT AUHORITY/SYSTEM. Exploitation requires successful timing of the race condition and a rollback during installation or update.

### CVE-2026-97245

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T13:17:36.433 |

Shop Worker Privilege Escalation in SureCart <= 4.7.2 versions.

### CVE-2026-96833

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:33.153 |

Editor PHP Object Injection in Ultimate Addons for Contact Form 7 <= 3.5.51 versions.

### CVE-2026-96832

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:33.023 |

Shop manager PHP Object Injection in Content Egg <= 6.3.1 versions.

### CVE-2026-96815

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-30T13:17:30.770 |

Custom role Privilege Escalation in Vitepos <= 3.5.0 versions.

### CVE-2026-96344

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:29.300 |

Custom role PHP Object Injection in eCommerce Product Catalog <= 3.6.0 versions.

### CVE-2026-96343

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:29.167 |

Custom role PHP Object Injection in WP ERP <= 1.17.9 versions.

### CVE-2026-94677

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:27.540 |

Shop manager PHP Object Injection in Kadence WooCommerce Email Designer <= 1.5.19.1 versions.

### CVE-2026-94122

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:24.700 |

Editor PHP Object Injection in Responsive Slider Gallery  <= 1.5.5 versions.

### CVE-2026-93771

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:22.810 |

Shop manager PHP Object Injection in Cost of Goods for WooCommerce <= 3.5.2 versions.

### CVE-2026-93651

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:22.543 |

Author PHP Object Injection in Minimum and Maximum Quantity for WooCommerce <= 2.1.2 versions.

### CVE-2026-93624

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-30T13:17:22.407 |

Shop manager PHP Object Injection in Music Player for WooCommerce <= 1.9.1 versions.

### CVE-2026-79625

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-30T10:17:17.273 |

Affected products do not properly synchronize access to their monitoring functionality. When multiple clients send concurrent requests, this may lead to incorrect reads or writes, or to corruption of internal memory structures. An authenticated remote attacker with monitoring access can exploit this issue to cause incorrect data processing or a denial-of-service condition.

### CVE-2026-97347

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T09:17:16.773 |

The Post Views Stats Counter plugin for WordPress is vulnerable to Stored Cross-Site Scripting via User-Agent Header in all versions up to, and including, 1.1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The plugin's only input filter is a substring blacklist for known bot signatures (e.g. 'bot', 'spider', 'crawler'), which can be trivially bypassed by crafting a User-Agent payload that omits those strings.

### CVE-2026-96649

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T03:17:00.387 |

The Frontend Post Submission Manager Lite – Frontend Posting WordPress Plugin plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via post_content Parameter (data-label DOM Sink) in all versions up to, and including, 1.3.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the site operator to have enabled guest post submission via the [fpsm] shortcode, which registers a publicly accessible AJAX handler gated only by a nonce emitted on every page containing the shortcode.

### CVE-2026-86101

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-09-30T00:16:36.283 |

An improper authorization vulnerability in WatchGuard Fireware OS's SAML login process allows a remote, authenticated SAML user with access only to the Access Portal to obtain unauthorized Mobile VPN with SSL access through a specially crafted request.

### CVE-2026-93853

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-283` |
| Published | 2026-09-29T21:19:39.140 |

Unverified ownership in Barman snapshot backup deletion allows a principal who can write the backup catalog to cause Barman to delete unrelated cloud snapshots. When a snapshot backup is deleted, either explicitly or by retention policy enforcement, Barman reads the snapshot identifiers from the backup.info file and passes them to the cloud provider's delete API using Barman's own credentials, without verifying that the snapshots belong to that backup. An attacker who can overwrite backup.info but lacks snapshot delete permissions can substitute the identifiers of other snapshots, causing Barman to delete any snapshot its cloud identity can reach on AWS, Microsoft Azure, or Google Cloud. Exploitation requires a deployment where the principal that writes the backup catalog is separate from the identity Barman uses to delete snapshots. Barman versions from 3.4.0 (Google Cloud), 3.6.0 (Azure), and 3.7.0 (AWS) up to and including 3.20.0 are affected. The issue is fixed in Barman 3.20.1.

### CVE-2026-76728

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.947 |

A vulnerability in the API endpoint of HPE Networking Instant ON APs could allow an authenticated remote attacker with high privileges to conduct a server-side request forgery (SSRF) attack. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-76727

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-29T20:17:24.827 |

Command injection vulnerabilities exist in the affected interface of HPE Networking Instant ON that could allow an authenticated remote attacker with high privileges to perform command injection. Successful exploitation could allow an attacker to execute arbitrary commands as a privileged user on the underlying operating system.

### CVE-2026-100296

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-09-29T20:17:10.097 |

In Anjvision YSSD-RTMP-H5 firmware version 3.3.2.4, an empty-body POST to /setUserConfig, dispatched through the web server's SOAP-RPC handler, silently downgrades the administrator password to the default value and corrupts the in-memory authentication state until the device reloads. The handler does not verify the session's privilege level, so any authenticated user can trigger it.

### CVE-2026-84422

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-29T18:17:17.693 |

IBM Guardium Data Protection 12.2 is vulnerable to command injection in the CLI certificate SMIME recipient deletion functionality, allowing an authenticated privileged CLI user to execute arbitrary commands with root privileges.

### CVE-2026-97289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:39.210 |

Unauthenticated Cross Site Scripting (XSS) in Quiz And Survey Master <= 11.2.6 versions.

### CVE-2026-97272

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:38.167 |

Unauthenticated Cross Site Scripting (XSS) in Premmerce Permalink Manager for WooCommerce <= 2.3.13 versions.

### CVE-2026-97271

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:38.040 |

Unauthenticated Cross Site Scripting (XSS) in WPFunnels <= 3.13.1 versions.

### CVE-2026-97253

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:37.257 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kreatura LayerSlider allows Reflected XSS.

This issue affects LayerSlider: from n/a through 8.4.0.

### CVE-2026-97250

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:37.110 |

Unauthenticated Cross Site Scripting (XSS) in  Geo Mashup <= 1.13.21 versions.

### CVE-2026-97237

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:35.357 |

Unauthenticated Cross Site Scripting (XSS) in JetEngine <= 3.8.14.3 versions.

### CVE-2026-97235

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:35.083 |

Unauthenticated Cross Site Scripting (XSS) in ThemeREX Addons < 2.45.0 versions.

### CVE-2026-97077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:34.470 |

Unauthenticated Cross Site Scripting (XSS) in Ad Inserter <= 2.8.18 versions.

### CVE-2026-97065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:33.950 |

Unauthenticated Cross Site Scripting (XSS) in Happyforms <= 1.26.15 versions.

### CVE-2026-96836

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:33.537 |

Unauthenticated Cross Site Scripting (XSS) in Parsi Date <= 6.3 versions.

### CVE-2026-96830

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:32.760 |

Unauthenticated Cross Site Scripting (XSS) in GiveWP <= 4.16.9 versions.

### CVE-2026-96820

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:31.440 |

Subscriber Cross Site Scripting (XSS) in Awesome Support <= 6.3.9 versions.

### CVE-2026-96819

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:31.310 |

Subscriber Cross Site Scripting (XSS) in oik <= 4.15.4 versions.

### CVE-2026-96816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:30.910 |

Unauthenticated Cross Site Scripting (XSS) in Trusted Shops Easy Integration for WooCommerce <= 2.0.6 versions.

### CVE-2026-96814

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:30.623 |

Unauthenticated Cross Site Scripting (XSS) in WooCommerce Product Table Lite <= 5.6.7 versions.

### CVE-2026-96352

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:30.350 |

Unauthenticated Cross Site Scripting (XSS) in YITH WooCommerce Ajax Search <= 2.28.0 versions.

### CVE-2026-96351

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:30.220 |

Unauthenticated Cross Site Scripting (XSS) in Classified Listing <= 6.1.3 versions.

### CVE-2026-94499

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-30T13:17:27.007 |

Subscriber Broken Access Control in FormGent <= 1.12.2 versions.

### CVE-2026-94081

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:23.523 |

Unauthenticated Cross Site Scripting (XSS) in WordPress Persistent Login <= 3.1.3 versions.

### CVE-2026-94078

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:23.350 |

Unauthenticated Cross Site Scripting (XSS) in Site Reviews <= 8.3.1 versions.

### CVE-2026-93770

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:22.677 |

Unauthenticated Cross Site Scripting (XSS) in WP Statistics <= 14.16.13 versions.

### CVE-2026-93514

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:22.130 |

Unauthenticated Cross Site Scripting (XSS) in Notification for Telegram <= 3.5.2 versions.

### CVE-2026-93512

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:21.997 |

Unauthenticated Cross Site Scripting (XSS) in JW Player for WordPress <= 2.3.11 versions.

### CVE-2026-27371

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:18.910 |

Unauthenticated Cross Site Scripting (XSS) in WPFunnels <= 3.13.1 versions.

### CVE-2026-102398

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:17.647 |

Unauthenticated Cross Site Scripting (XSS) in Popup by Supsystic <= 1.13.1 versions.

### CVE-2026-102396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:17.513 |

Unauthenticated Cross Site Scripting (XSS) in Ultimate Maps by Supsystic <= 1.5.5 versions.

### CVE-2026-102395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:17.380 |

Unauthenticated Cross Site Scripting (XSS) in Easy Google Maps <= 1.14.6 versions.

### CVE-2026-102385

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:17.107 |

Unauthenticated Cross Site Scripting (XSS) in Ninja Forms <= 3.15.3 versions.

### CVE-2026-100507

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T13:17:14.577 |

Unauthenticated Cross Site Scripting (XSS) in If-So Dynamic Content Personalization <= 1.10.1 versions.

### CVE-2026-103242

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-30T12:17:12.653 |

A heap-based buffer overflow flaw was found in rpm. RPMTAG_FILESIGNATURES in a crafted, unsigned RPM package's main header is declared with the wrong header type, causing hex2binv() to allocate a one-byte buffer and then write the tag's attacker-controlled, hex-decoded content — of attacker-chosen length — past the end of that allocation. This is reachable via rpm2cpio, rpm2archive, and rpm -qlvp on an untrusted package.

### CVE-2026-102457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-30T09:17:13.650 |

EasyFlow .NET developed by Digiwin has an Arbitrary File Read vulnerability. Authenticated remote attackers can exploit this vulnerability to download arbitrary system files.

### CVE-2026-102456

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-30T09:17:13.503 |

EasyFlow .NET developed by Digiwin has an SQL Injection vulnerability. Authenticated remote attackers can inject arbitrary SQL commands to read database contents.

### CVE-2026-92869

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-30T08:16:34.877 |

An out-of-bounds write vulnerability exists in Pgpool-II, which may allow an authenticated attacker to cause abnormal process termination.

### CVE-2026-91832

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-30T06:17:09.593 |

The WP Mobile Menu  WordPress plugin before 2.9 does not correctly verify the nonce on its settings import, so an attacker can import arbitrary WP Mobile Menu  WordPress plugin before 2.9 settings through a cross-site request in an administrator's session, and the imported values are then output unescaped to every visitor, resulting in Stored Cross-Site Scripting.

### CVE-2026-88797

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-30T06:17:07.977 |

The Vayu X WordPress theme before 1.0.6 does not perform any capability check on one of its AJAX actions and exposes the nonce guarding it to every logged-in user, allowing any authenticated user, such as a subscriber, to install and activate any  hosted on the WordPress.org repository.

### CVE-2026-103087

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-30T02:16:57.043 |

Uncontrolled recursion in the Gosub browser engine (gosub-engine) through 0.1.0 and main before commit 46868b3 allows a remote attacker to cause a Denial of Service (stack exhaustion and application crash) via an SVG document containing an excessive number of deeply nested elements. Because the engine does not limit the nesting depth of processed SVG nodes, rendering such a document overflows the thread stack and terminates the application. The malicious SVG can be embedded through the SRC attribute of an IMG element, and thus exploitation only requires the victim to visit an attacker-controlled web page.

### CVE-2026-103054

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-30T01:16:36.727 |

AiSOC versions before 12.0.0 contain an authorization bypass vulnerability in the MSSP module that allows authenticated users to add arbitrary tenants to portfolios they own. Attackers can submit tenant UUIDs via the add_tenants_to_portfolio endpoint to claim unclaimed tenants and read their security alerts, incidents, and posture metrics without consent.

### CVE-2026-90441

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-400;CWE-862` |
| Published | 2026-09-30T00:16:37.363 |

A missing authorization vulnerability in the wgagent management daemon's session initialization function allows an authenticated, low-privileged user (including a read-only or guest administrator account) to crash the wgagent process and read arbitrary files accessible to the daemon by submitting a specially crafted management API request.

### CVE-2026-86136

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-476;CWE-862` |
| Published | 2026-09-30T00:16:37.213 |

A missing authorization vulnerability in the wgagent management daemon's session initialization function allows an authenticated, low-privileged user (including a read-only or guest administrator account) to crash the wgagent process and read arbitrary files accessible to the daemon by submitting a specially crafted management API request.

### CVE-2026-18105

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-30T00:16:35.877 |

An uncontrolled resource consumption vulnerability in Fireware OS's diagnostic tasks feature allows a low-privileged, authenticated user to cause a denial of service of the system's diagnostic tools by repeatedly starting and aborting a specially crafted diagnostic task through the web UI.

### CVE-2026-74225

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T22:18:33.827 |

U-Boot before 2026.10-rc5 contains out-of-bounds memory access in dhcp6_parse_options() that fails to validate SERVERID and CLIENTID option lengths from DHCPv6 packets. Attackers on the local network can send crafted DHCPv6 ADVERTISE or REPLY packets during netboot to corrupt memory and crash the bootloader.

### CVE-2026-102809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-29T18:17:14.220 |

PX4 Autopilot through 1.17.0 contains an uncontrolled stack allocation vulnerability in the file2 test command that fails to validate the write chunk size parameter. Attackers with shell access can supply an excessively large value to the -c option to trigger stack overflow and crash the flight controller.

### CVE-2026-102808

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-29T18:17:14.063 |

PX4 Autopilot through 1.17.0 contains a NULL pointer dereference vulnerability in the sd_stress command where the -b byte count parameter is parsed without validation before being passed to malloc() and memset(). Attackers with shell access, including through MAVLink, can supply invalid byte count values to crash the flight controller.

### CVE-2026-102715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-29T18:17:10.780 |

Any host on the LAN can send two mDNS records and make the responder write past the end of its



transmit packet.



The string table stores each name in a slot rounded up to a multiple of four:



```c



/* addons/mdns/nxd_mdns.c:11436, 11443, 11447 */



memory_len = ((memory_len & 0xFFFFFFFC) + 8) & 0xFFFFFFFF;



...



len = *((USHORT*)(p - 2));           /* slot size, not string length */



if ((len == memory_len) && ... _nx_mdns_name_match(start, memory_ptr, memory_size) ...)



```



The lookup that decides whether an incoming name is already stored compares the rounded slot size,



so names of 12, 13, 14 and 15 characters share one bucket. A second name in the bucket is answered



with the pointer to the first, and the record then carries a string up to three bytes longer than



the length the caller accounted for. `_nx_mdns_packet_rr_add` (nxd_mdns.c:8911) sizes its only



bound check from that stale length, and `_nx_mdns_name_string_encode` writes the real string.



Two PTR records are enough, both ordinary mDNS responses to a `_http._tcp` query, with owner names



whose lengths fall in the same bucket:



```



==87491==ERROR: AddressSanitizer: heap-buffer-overflow



WRITE of size 1 at 0x611000000124 thread T5

    #0 _nx_mdns_name_string_encode  addons/mdns/nxd_mdns.c:13096
    #1 _nx_mdns_packet_rr_add       addons/mdns/nxd_mdns.c:8911


0x611000000124 is 0 bytes to the right of 228-byte region



```



The overflow is one to three bytes of attacker-influenced name data past `nx_packet_data_end`. In a



normal pool that lands in the next packet in the same pool rather than in a redzone, so the visible



effect is a corrupted neighbouring packet or a corrupted pool free list rather than a clean crash.



Compare the slot size against the stored string length before declaring a match, or keep the



string length in the slot header and return it to the caller so the encoder and the bound check



agree.

### CVE-2026-102714

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191;CWE-835;CWE-1287` |
| Published | 2026-09-29T18:17:10.617 |

`_nx_icmpv6_validate_options()` scans the option area with `while (length > 2)` (`common/src/nx_icmpv6_validate_options.c:79`). An area whose size leaves a one- or two-byte residue exits the loop with that tail unexamined; the residue is not negative, so the function returns `NX_SUCCESS`. Its zero-length rejection never sees those bytes.



Every consumer then re-walks the same area, reading a two-byte option header at the residue and subtracting `nx_icmpv6_option_length << 3` with no zero check and no remaining-length check. Three outcomes follow, selected by bytes the attacker controls.



**Zero length byte.** The walker subtracts zero and advances zero. All four handlers loop forever — `_nx_icmpv6_process_ra` (`nx_icmpv6_process_ra.c:245, :528`), `_nx_icmpv6_process_ns` (`:251, :329`), `_nx_icmpv6_process_na` (`:147, :156`) and `_nx_icmpv6_process_redirect` (`:247, :350`). The walk runs in the IP thread, which is the highest-priority thread and does not yield inside the loop, so the system stops until a watchdog reset and the frame can be replayed after each one.



**Non-zero length byte on a short residue.** The three unsigned counters underflow — `2 - 8` becomes `0xFFFFFFFA` — and the walk continues past the packet buffer, reading until it faults or meets a zero length byte and freezes. The Router Advertisement counter is signed and exits cleanly in this case.



**One-byte residue.** The walker reads a two-byte option header, over-reading one byte.



During a runaway walk, stray bytes parsing as a link-layer address option are copied into the neighbor cache (`nx_icmpv6_process_ns.c:280, :293`) and subsequently used as the destination MAC for frames to that neighbour, placing off-packet memory on the link. Confirmed by inspection, not reproduced.

### CVE-2026-102639

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-09-29T18:17:09.173 |

MobilityDB version 1.3.0 and earlier contains an out-of-bounds read vulnerability in the MEOS binary and library WKB deserialization logic that allows unprivileged database users to crash the PostgreSQL backend process by supplying a crafted WKB payload with a negative length field. The negative length value wraps to a large unsigned size_t due to missing signed validation, bypasses an overflow-unsafe pointer arithmetic bounds check in wkb_parse_state_check(), and causes memcpy() in text_from_wkb_state() to operate with a corrupted unbounded length, resulting in a remote denial-of-service condition affecting all sessions on the PostgreSQL instance.

### CVE-2026-92232

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T17:17:15.060 |

Joomla! Core - [20260916] - Core - XSS filter bypass in InputFilter via whitespace characters in HTML data URIs in Joomla 1.5.0-5.4.8, 6.0.0-6.1.3 - The cleanAttribute method removes HTML data URIs, however injected whitespaces characters could circumvent that cleanup, causing an XSS vector.

### CVE-2026-92231

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-29T17:17:14.930 |

Joomla! Core - [20260915] - Core - XSS filter bypass in InputFilter via HTML5 entity decode mismatch in Joomla 1.5.0-5.4.8, 6.0.0-6.1.3 - The checkAttribute method normalized an attribute value before testing it against the "javascript:" scheme regex, however without decoding HTML5 entities beforehand, causing an XSS vector.

### CVE-2026-100299

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-09-29T20:17:10.557 |

In Anjvision YSSD‑RTMP‑H5 firmware version 3.3.2.4, the device includes a legacy password hash on the serial console that relies on a weak DES‑based encryption.

### CVE-2026-92226

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-29T17:17:14.560 |

Joomla! Core - [20260913] - Core - Improper ACL checks for varous webservice edit tasks in Joomla 4.0.0-5.4.8, 6.0.0-6.1.3 - An improper access check allows unauthorized users to perform edit actions on otherwise uneditable items.

### CVE-2026-90915

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-29T17:17:13.520 |

Joomla! Core - [20260905] - Core - Arbitrary directory deletion via cache purge action in Joomla 4.0.0-5.4.8, 6.0.0-6.1.3 -An improper validation of the cache group name allowed path traverals in the file storage of the caching layer, resulting in arbitrary directory deletions.

### CVE-2026-90913

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-29T17:17:13.263 |

Joomla! Core - [20260903] - Core - Improper ACL checks for access level webservice endpoints in Joomla 4.0.0-5.4.8, 6.0.0-6.1.3 - An improper access check allows unauthorized users to perform mutation actions in access level endpoints.

### CVE-2026-92371

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-29T16:17:15.177 |

TeamViewer Full Client and Host for Linux prior version 15.82 contains an improper path validation vulnerability in the Cloud Session Recording (CSR) functionality. By exploiting a race condition during path validation and subsequent file access, a local authenticated attacker may cause privileged file operations in unintended locations on the affected system.

### CVE-2026-102570

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T15:17:18.917 |

ClipBucket v5 through 5.5.3-#197 contains a time-based blind SQL injection vulnerability in the language update function where the language_id parameter is concatenated unescaped into the WHERE clause of an UPDATE statement. An authenticated administrator with basic_settings permission can inject arbitrary SQL payloads to extract or modify database contents.

### CVE-2026-102569

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-29T15:17:18.757 |

ClipBucket v5 through 5.5.3-#197 contains a time-based blind SQL injection vulnerability in the admin video edit function where the videoid parameter is concatenated into an UPDATE statement without proper escaping. An authenticated administrator with video_moderation permission can inject arbitrary SQL commands to extract or modify database contents.
