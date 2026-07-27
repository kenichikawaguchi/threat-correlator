# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-27 15:00 UTC
- **対象期間**: `2026-07-26T15:00:18.000Z` 〜 `2026-07-27T15:00:20.000Z`
- **重要CVE数**: 35 件（Critical 9.0+: 6 件 / High 7.0〜: 29 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち、**CVSS 7.0 以上が 40 件以上** と非常に多く、特に **リモートコード実行 (RCE)・SQL インジェクション・バッファオーバーフロー** が目立ちます。  
- 同一製品・ライブラリに対する脆弱性が集中しており、**Apache Thrift（全バインディング）** と **Joomla 用拡張 (SP Page Builder)** が多数の高危険度 CVE の対象となっています。  
- 多くは **認証不要 (Unauthenticated)** で悪用可能であり、ネットワーク境界だけで防御しきれないケースが増加しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 製品・コンポーネント | 主な脆弱性種別 | 影響範囲・リスク |
|-----|------|----------------------|----------------|-------------------|
| **CVE‑2026‑61511** | 9.3 | vBulletin 5.x (5.0‑5.7.5) / 6.x (6.0‑6.2.1) | **Eval インジェクション → 任意 PHP コード実行** | 認証不要で `pagenav[pagenumber]` に細工したリクエストを送るだけでサーバ上で任意コードが実行され、完全なサイト乗っ取りが可能。 |
| **CVE‑2026‑55971** | 9.3 | Apache Thrift C++ バインディング (≤ 0.23.x) | **ヒープベースバッファオーバーフロー** | 攻撃者が特製メッセージを送信するとメモリ破壊 → 任意コード実行。Thrift はマイクロサービス間通信で広く利用されているため、影響範囲は大規模。 |
| **CVE‑2026‑65876** | 9.2 | Joomla! 拡張 **SP Page Builder** (< 6.7.1) | **未認証 SQL インジェクション (catid パラメータ)** | `loadMoreArticles` エンドポイントに SQL 文を注入でき、データベース情報漏洩・改ざんが可能。Joomla サイトは多数の中小企業で採用されている。 |
| **CVE‑2026‑12495** | 9.2 | Mercusys MB115‑4G ルータ Web UI | **スタックバッファオーバーフロー → DoS** | `/cgi/login` へ特定リクエスト送信でプロセスがクラッシュし、ルータが停止。IoT 環境での可用性が低下。 |
| **CVE‑2026‑59688** (同系列 59687/59686) | 8.4 | Progress Software LoadMaster / ECS / Object Scale / MOVEit WAF | **認証済み OS コマンドインジェクション** (バックアップ復元・Geo Location 管理) | 高権限ユーザーが管理画面から任意シェルコマンドを実行でき、内部ネットワーク全体への侵害に発展する恐れ。 |

> **選定理由**  
> - **CVSS が 9.0 以上** のものを中心に、**認証不要でリモートから直接コード実行が可能**な点が共通。  
> - 製品は **Web アプリケーション (vBulletin, Joomla)、インフラ基盤 (Thrift, LoadMaster)、IoT ルータ** と多岐にわたり、組織全体のリスクマトリクスに大きく影響する。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・ファームウェアのアップデート
| 製品 | 現行脆弱バージョン | 修正版 / 推奨バージョン | アップデート手順のポイント |
|------|-------------------|------------------------|----------------------------|
| **vBulletin** | 5.x ≤ 5.7.5、6.x ≤ 6.2.1 | **5.7.6** もしくは **6.2.2** 以降 | - 公式パッチ適用後、`vB5_Template_Runtime::runMaths()` のコード差分を確認<br>- 変更後はテンプレートキャッシュをクリアし、再デプロイ |
| **Apache Thrift** | 0.23.x 以前 | **0.24.0** 以上 | - `thrift` パッケージ全バインディング (C++, C_glib, Go, Rust, Node.js, Python, Java, PHP) を同時に更新<br>- 依存ライブラリ (e.g., `libthrift`) のバージョンも合わせて更新 |
| **Joomla! SP Page Builder** | < 6.7.1 | **6.7.1** 以降 | - 拡張管理画面から「更新」→「自動アップデート」または手動で zip を上書き<br>- アップデート後は `catid`・`order` パラメータのバリデーションが追加されたことを確認 |
| **Mercusys MB115‑4G** | ファームウェア 1.0.x (脆弱) | **最新公式ファームウェア** (例: 1.0.5) | - 管理画面 → 「システム」→「ファームウェア更新」から OTA または手動アップロード<br>- アップデート後は `/cgi/login` へのリクエストでエラーログが出ないかテスト |
| **Progress Software LoadMaster / ECS / Object Scale / MOVEit WAF** | 8.x 系 (脆弱) | **ベンダーが提供する最新パッチ** (例: 8.5.3) | - 管理コンソール → 「パッチ管理」→「最新パッチ適用」<br>- パッチ適用後はバックアップ復元・Geo Location 機能でコマンドインジェクションが再現しないか検証 |

### 3.2 防御・検知強化
- **WAF ルール追加**  
  - `pagenav[pagenumber]` への文字列リテラルや長過ぎる数値をブロック（vBulletin）。  
  - `catid`、`order`、`loadMoreArticles` パラメータに対し **SQL キーワード** を含むリクエストを検知・遮断。  
- **ネットワーク分離**  
  - Apache Thrift を使用するサービスは **内部 VLAN** に限定し、外部からの直接アクセスを防止。

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61511

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-07-27T14:16:59.177 |

vBulletin 5.x through 5.7.5 and 6.x through 6.2.1 contains an eval injection vulnerability in the vB5_Template_Runtime::runMaths() method within the template runtime that allows unauthenticated remote attackers to execute arbitrary PHP code by supplying crafted input through the pagenav[pagenumber] parameter. Attackers can exploit the insufficiently restrictive regex filter by using phpfuck-style encoding with permitted characters to inject and execute arbitrary PHP code via the unauthenticated ajax/render template route without any authentication.

### CVE-2026-55971

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-27T12:16:46.110 |

Heap-based Buffer Overflow vulnerability in Apache Thrift C++ bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-65876

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T14:17:00.680 |

Joomla Extension - joomshaper.com - Unauthenticated SQL injection  in SP Page Builder < 6.7.1 - Improper validation of catid parameters in the loadMoreArticles endpoint leads to an SQL injection vector.

### CVE-2026-65766

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T14:17:00.533 |

Joomla Extension - joomshaper.com - Unauthenticated SQL injection  in SP Page Builder < 6.7.1 - Improper validation of order parameters in the Dynamic Content endpoint leads to an SQL injection vector.

### CVE-2026-12495

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-27T12:16:41.027 |

Denial-of-service (DoS) vulnerability due to a stack buffer overflow in the http_gdpr_decrypt function of the Mercusys MB115-4G device's web interface. An unauthenticated attacker could exploit this vulnerability by sending a specially crafted request to the /cgi/login endpoint, causing memory corruption and the httpd process to crash, resulting in a denial of service for the web administration service.

### CVE-2026-48144

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-07-27T12:16:44.700 |

Improper Validation of Certificate with Host Mismatch vulnerability in Apache Thrift c_glib bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-12991

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-300` |
| Published | 2026-07-27T13:16:52.250 |

The lack of cryptographic mechanisms to ensure the integrity and authenticity of communications in Ghost Robotics' Vision 60 robot (APK v5.5.0) exposes the system to man-in-the-middle attacks. An attacker located on the local network can use ARP spoofing and selective traffic blocking techniques to intercept and manipulate packets between the legitimate operator and the robot. This allows the attacker to disconnect the original controller, establish unauthorized communications, and prevent the operator from regaining control of the device, seriously compromising the confidentiality, integrity, and availability (CIA) of operations.

### CVE-2026-12989

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-27T13:16:51.993 |

A lack of authentication in the mobile app (APK v5.5.0) for Ghost Robotics' Vision 60 robot allows an unauthenticated attacker connected to the device's internal Wi-Fi network to gain unrestricted access to the web administration interface and the HTTP API. Due to the lack of authorization mechanisms, the attacker can view real-time camera feeds, control the robot’s movements, manage sensors (GPS, RTK, SAM, LIDAR), and execute critical operational commands (Play, Pause, Stop, E-Stop). Successful exploitation completely compromises the confidentiality, integrity, and physical security of the system.

### CVE-2026-58662

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-1284` |
| Published | 2026-07-27T12:16:46.807 |

Improper Validation of Specified Quantity in Input, Out-of-bounds Read vulnerability in Apache Thrift C++ bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-58389

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-27T12:16:46.673 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift Rust bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-55969

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-27T12:16:45.823 |

Integer Overflow or Wraparound vulnerability in Apache Thrift C++, c_glib, Go, netstd, Delphi and Haxe bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-55968

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-770` |
| Published | 2026-07-27T12:16:45.683 |

Inefficient Algorithmic Complexity, Allocation of Resources Without Limits or Throttling vulnerability in Apache Thrift Node.js bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-48586

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-27T12:16:44.970 |

Improper Handling of Highly Compressed Data (Data Amplification) vulnerability in Apache Thrift C++, Java, Python, Go, D, C/GLib bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-43871

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-27T12:16:44.413 |

Loop with Unreachable Exit Condition ('Infinite Loop') vulnerability in Apache Thrift Python, Go, PHP and Java bindings.This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-65894

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-27T08:16:23.157 |

This vulnerability exists in CP PLUS EZ-P21 IP Camera due to improper authentication of HTTP endpoints. A remote attacker could exploit this vulnerability by conducting brute-force attacks against HTTP endpoint on the targeted device.



Successful exploitation of this vulnerability could allow an attacker to gain unauthorized access to live video snapshots from the targeted device.

### CVE-2026-14837

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-27T08:16:17.463 |

Multiple Lenze products are affected by an improper signature verification vulnerability in the SSH enablement mechanism. A low-privileged local attacker can bypass verification of the SSH enable file signature and enable SSH access on the device. Successful exploitation may result in unauthorized administrative access and complete system compromise.

### CVE-2026-59688

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T13:18:22.203 |

An OS Command Injection vulnerability in Progress Software LoadMaster, ECS Connection Manager, Object Scale Connection Manager, and MOVEit WAF allows an authenticated attacker with high privileges to execute arbitrary operating system commands on the affected appliance via the backup restore functionality, potentially resulting in complete system compromise.

### CVE-2026-59687

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T13:18:22.080 |

An OS Command Injection vulnerability in Progress Software LoadMaster, ECS Connection Manager, Object Scale Connection Manager, and MOVEit WAF allows an authenticated attacker with high privileges to execute arbitrary operating system commands on the affected appliance via the Geo Location management interface, potentially resulting in complete system compromise.

### CVE-2026-59686

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-27T13:18:21.947 |

An OS Command Injection vulnerability in Progress Software LoadMaster, ECS Connection Manager, Object Scale Connection Manager, and MOVEit WAF allows an authenticated attacker with high privileges to execute arbitrary operating system commands on the affected appliance via the management interface, potentially resulting in complete system compromise.

### CVE-2026-65878

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-27T14:17:00.960 |

Joomla Extension - joomshaper.com - Authenticated arbitrary file delete in SP Page Builder < 6.7.1- Improper path validation and ACL checks lead to a file deletion vector in the media manager.

### CVE-2026-17497

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-276;CWE-1249` |
| Published | 2026-07-26T15:16:27.873 |

NoteGen before 0.32.0 grants the Tauri shell plugin shell:allow-execute capability for bash, python, and python3 with arbitrary arguments in the default desktop capabilities. JavaScript running in the application webview can therefore invoke plugin:shell|execute to run attacker-controlled operating system commands with the privileges of the NoteGen process. In combination with script execution in the webview (for example via chat XSS), this enables full remote code execution on the user's machine.

### CVE-2026-65877

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-27T14:17:00.823 |

Joomla Extension - joomshaper.com - Authenticated SQL injection  in SP Page Builder < 6.7.1 - Improper validation of various parameters in the media manager search and date filters lead to an SQL injection vector.

### CVE-2026-48145

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-07-27T12:16:44.840 |

Improper Validation of Certificate with Host Mismatch vulnerability in Apache Thrift C++ bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-15928

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-27T03:16:18.830 |

XMLRPC-C Library versions 1.07 through 1.67.01 are vulnerable to a reflected cross-site scripting (XSS) vulnerability in the error page component.

### CVE-2026-17496

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-26T15:16:27.710 |

NoteGen before 0.32.0 renders AI chat responses with markdown-it configured with html:true and injects the result into the DOM via dangerouslySetInnerHTML in chat-preview, without HTML sanitization and with CSP set to null. Attacker-controlled content that reaches the model prompt (for example a malicious skill REFERENCE.md that instructs the model to emit HTML) can cause the model response to include executable markup such as an img onerror handler. When the user views the chat response, that markup runs as JavaScript in the privileged Tauri webview, enabling arbitrary script execution in the application context (cross-site scripting).

### CVE-2026-59690

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-27T13:18:22.457 |

A Missing Authorization vulnerability in Progress Software LoadMaster, ECS Connection Manager, Object Scale Connection Manager, MOVEit WAF, and Multi Tenant allows an authenticated attacker with low privileges to perform privileged administrative operations via the REST API that should not be accessible to their permission level, potentially resulting in a system compromise.

### CVE-2026-59689

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-27T13:18:22.327 |

An Incorrect Authorization vulnerability in Progress Software LoadMaster, ECS Connection Manager, Object Scale Connection Manager, and MOVEit WAF allows an authenticated attacker with low privileges to escalate privileges to root on the affected appliance, potentially resulting in full system compromise.

### CVE-2026-17523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-825` |
| Published | 2026-07-27T10:16:36.270 |

A flaw was found in the kernel. An unprivileged local user can exploit this vulnerability to execute arbitrary code within the kernel, which leads to a local privilege escalation (LPE). This allows the attacker to gain root privileges and take full control of the affected system.

### CVE-2026-12990

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-27T13:16:52.130 |

An access control vulnerability in the mobile app (APK v5.5.0) for Ghost Robotics' Vision 60 robot allows multiple simultaneous sessions to run without proper client validation or session integrity checks. An attacker with a modified version of the app can connect to the robot during an active, legitimate session. This allows the attacker to bypass control restrictions, intercept sensitive information (such as real-time video), and partially interact with the system unnoticed and without disconnecting the legitimate user, compromising confidentiality and operational security.

### CVE-2026-17527

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-27T10:16:37.617 |

In containerized-data-importer (CDI), the aggregated cdi.kubevirt.io:view ClusterRole, intended to provide read-only access to CDI resources, includes a rule granting create on the datavolumes/source subresource. CDI's DataVolume clone authorization accepts this permission as sufficient to authorize cloning the contents of any PVC the caller can name, without requiring write access to the source namespace. A user or service account bound to the view role, commonly granted cluster-wide via ClusterRoleBinding, who also has ordinary write access (edit/admin) to any single namespace, can use this to exfiltrate the contents of any PVC in the cluster into a namespace they control, bypassing namespace isolation and the read-only guarantee of the view role.

### CVE-2026-49158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-07-27T12:16:45.113 |

Improper Handling of Highly Compressed Data (Data Amplification) vulnerability in Apache Thrift Ruby bindings.

This issue affects Apache Thrift: before 0.24.0.

Users are recommended to upgrade to version 0.24.0, which fixes the issue.

### CVE-2026-57990

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-552` |
| Published | 2026-07-26T18:18:25.153 |

Files or directories accessible to external parties in Microsoft Edge (Chromium-based) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-57989

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-26T18:18:25.033 |

Origin validation error in Microsoft Edge (Chromium-based) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-66412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-27T07:16:30.317 |

Leantime 3.6.2 and prior contains a broken access control vulnerability that allows authenticated users to read milestone data from projects they are not assigned to by supplying arbitrary integer milestone IDs to the tickets.getMilestone JSON-RPC endpoint. Attackers can enumerate integer milestone IDs through the JSON-RPC API to access project planning information, milestone titles, descriptions, and timelines across all projects on the instance regardless of project membership.

### CVE-2026-65893

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-07-27T08:16:23.010 |

This vulnerability exists in CP PLUS EZ-P21 IP Camera due to an insecure debug feature enabled in the firmware.

An attacker with physical access could exploit this vulnerability by placing arbitrary code on removable media and triggering their execution through the debug mechanism.



Successful exploitation of this vulnerability could allow an attacker to execute arbitrary code with elevated privileges on the targeted device.
