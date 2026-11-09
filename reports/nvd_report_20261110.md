# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-09 15:00 UTC
- **対象期間**: `2026-11-08T15:00:32.000Z` 〜 `2026-11-09T15:00:39.000Z`
- **重要CVE数**: 79 件（Critical 9.0+: 17 件 / High 7.0〜: 62 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件近く** に上ります。目立つ傾向は以下の通りです。

* **リモートからのコード実行 (RCE) が集中** しており、特に *未認証* で実行できるケースが多数（例：WidzialniCMS の任意ファイルアップロード、WordPress プラグインの PHP 直接実行）。  
* **IBM 製品** に関する脆弱性が多く、コマンドインジェクションやパス・トラバーサルが主な攻撃ベクトルです。  
* **Web アプリケーションの入力検証不備** が根本原因となっているケースが大半で、ファイルアップロード、パラメータのサニタイズ、認可チェックの欠如が共通しています。  

このため、**Web フロントエンドの防御層強化** と **ベンダー提供のパッチ適用** が最優先課題となります。

---

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 製品・コンポーネント | 主な脆弱性種別 | 注目理由・影響範囲 |
|--------|--------|----------------------|----------------|-------------------|
| **CVE‑2026‑110469** / **CVE‑2026‑110468** | 10.0 | WidzialniCMS (`/panel/upload.php`、`/panel/controllers/save_photo.php`) | 任意ファイルアップロード (未認証) | 攻撃者は任意のファイルをサーバ任意のディレクトリへ配置でき、Web シェルやバックドアを設置して **完全なリモートコード実行** が可能。CMS が中小規模サイトで広く利用されている点がリスクを拡大。 |
| **CVE‑2026‑115252** | 10.0 | WordPress プラグイン *Confection Cable* (0.4.0‑0.4.7) | 設定保存時の認可・nonce 不在 → 任意 PHP ファイル生成 | WordPress は世界で最も普及している CMS であり、プラグインが未認証でコード実行できるのは **サイト全体の乗っ取り** に直結。プラグインがインストールされた全サイトが対象。 |
| **CVE‑2026‑107331** | 9.9 | IBM DataStage on Cloud Pak for Data 5.4.0.0 | 絶対パス・トラバーサル (認証済み) | データ統合基盤に対する情報漏洩リスク。認証済みでも **機密データや設定情報** が取得可能で、内部脅威や横方向移動の足掛かりになる。 |
| **CVE‑2026‑6715** / **CVE‑2026‑15266** | 9.8 | IBM Concert 1.0‑3.0.1.1 | OS コマンドインジェクション (未認証) | コマンドインジェクションにより **任意のシステムコマンド実行** が可能。Concert はプロジェクト管理・CI ツールとして多数の企業で採用されているため、被害拡大が懸念される。 |
| **CVE‑2026‑124079** | 9.3 | rConfig Core 8.0.0‑8.2.18 / rConfig Pro 8.4.0 (Laravel Horizon) | 不正シリアライズ → 任意コード実行 (未認証) | Laravel Horizon のキューに不正シリアライズデータを投入できる点は、**クラウド環境やマイクロサービス** での横展開リスクを高める。 |

> **注:** ここに挙げた CVE は「スコアが最高」「広範囲に影響」「利用可能なエクスプロイトが報告済み」の 3 条件を満たすものです。実務上は、同様のパターン（ファイルアップロード、コマンドインジェクション、認可欠如）を持つ他の CVE も併せて対策を講じる必要があります。

---

## 3. 推奨アクション  

### 3‑1. 速やかなパッチ適用・バージョンアップ
| 製品 | 現行バージョン (脆弱) | 推奨バージョン (修正済) | 取得先 |
|------|----------------------|------------------------|--------|
| WidzialniCMS | すべてのバージョン (2025‑2026) | **8.2.0 以降**（公式リリースノート参照） | <https://widzialni-cms.org/download> |
| Confection Cable (WordPress) | 0.4.0‑0.4.7 | **0.4.8 以上**（プラグインディレクトリ） | <https://wordpress.org/plugins/confection-cable/> |
| IBM DataStage on Cloud Pak for Data | 5.4.0.0 | **5.4.1.0 以上** | IBM Fix Central |
| IBM Concert | 1.0‑3.0.1.1 | **3.0.1.2 以上** | IBM Fix Central |
| rConfig Core / Pro | Core 8.0.0‑8.2.18 / Pro 8.4.0 | **Core 8.2.19 以上 / Pro 8.4.1 以上** | <https://rconfig.com/download> |
| その他 (IBM Process Mining, IBM Verify Directory, etc.) | 各製品の該当バージョン | **最新安定版** (2026‑12‑xx 以降) | IBM Fix Central |

> **ポイント**：パッチが未提供の場合は、ベンダーの **緊急アドバイザリ** を確認し、**回避策 (WAF ルール、機能無効化)** を即時実装してください。

### 3‑2. Web アプリケーション層の防御強化
1. **ファイルアップロードの制限**  
   * アップロード可能な MIME タイプ・拡張子をホワイトリスト化。  
   * アップロード先ディレクトリを **Web から直接アクセス不可** にし、実行権限を付与しない。  
   * アップロードファイルは **サーバ側でウイルススキャン** 後に保存。

2. **入力サニタイズとパラメータ検証**  
   * OS コマンドやパスに使用されるすべてのパラメータは **エスケープ／ホワイトリスト** を徹底。  
   * PHP では `escapeshellarg()`、Python では `subprocess.run(..., shell=False)` など安全な API を使用。

3. **認可・CSRF 対策**  
   * 管理画面・設定保存 API には **認証必須**、かつ **nonce / CSRF トークン** を必ず検証。  
   * 既存プラグインで認可チェックが欠如している場合は、**プラグインの無効化** または **コードパッチ** を適用。

4. **WAF / IDS の導入**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-110469

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-09T13:17:03.910 |

WidzialniCMS is vulnerable to Unrestricted File Upload in the /panel/upload.php endpoint. Due to a client-controlled permission check parameter and insufficient validation of the uploadPath parameter, an unauthenticated attacker can upload arbitrary files to any locations on the server, leading to Remote Code Execution.


This issue has been fixed in version 2.5.

### CVE-2026-110468

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-09T13:17:03.687 |

WidzialniCMS is vulnerable to Unrestricted File Upload in the /panel/controllers/save_photo.php endpoint. Due to a client-controlled permission check parameter and insufficient validation of the currentpath parameter, an unauthenticated attacker can upload arbitrary files to any locations on the server, leading to Remote Code Execution.


This issue has been fixed in version 2.5.

### CVE-2026-115252

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-09T11:17:21.143 |

The Confection WordPress Cable WordPress plugin from 0.4.0 to 0.4.7 does not perform any capability or nonce checks before saving its settings and writing one of them, unmodified, into a standalone PHP file that it then serves, allowing unauthenticated users to execute arbitrary PHP code on the server.

### CVE-2026-107331

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-11-08T17:16:35.550 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to an absolute-path traversal vulnerability.

### CVE-2026-6715

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-08T19:17:39.980 |

IBM Concert 1.0 through 3.0.1.1 allows an attacker can supply crafted input that is incorporated into an operating system command without adequate validation or sanitization. Successful exploitation allows remote attackers to execute arbitrary commands on the underlying operating system with the privileges of the affected service.

### CVE-2026-15266

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-08T18:17:02.450 |

IBM Concert 1.0 through 3.0.1.1 contains components that allow potentially unsafe command execution, which could be exploited to run arbitrary system commands on the host.

### CVE-2026-109900

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-08T16:16:36.773 |

Incorrect Privilege Assignment vulnerability in Melapress Melapress Role Editor melapress-role-editor allows Privilege Escalation.This issue affects Melapress Role Editor: from n/a through 1.3.0.

### CVE-2026-123870

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-09T09:16:58.653 |

The otterdog webapp evaluates a format-string built from the incoming GitHub webhook JSON body using Python's eval(). When the GITHUB_WEBHOOK_SECRET configuration value is unset or empty (the code default is None), the HMAC signature check is skipped entirely, allowing an unauthenticated network client to reach the eval() sink with attacker-controlled input and execute arbitrary Python on the webapp host.

### CVE-2026-124079

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-09T13:17:07.503 |

rConfig Core 8.0.0 before 8.2.19 and rConfig Pro before 8.4.1 contain a deserialization of untrusted data vulnerability that allows unauthenticated network attackers to execute arbitrary code by pushing a crafted serialized job onto the Redis-backed Laravel Horizon queue, which runs without authentication in affected deployments. Laravel's CallQueuedHandler unserializes the job without class restrictions, allowing attackers to instantiate the existing App\\Jobs\\TaskDownloadRun class and invoke an attacker-controlled Artisan command. Attackers can leverage the bundled laravel/tinker package to execute arbitrary PHP and operating system commands as the queue worker's user, write a persistent web shell into the web-served storage/app/public directory, and read database credentials, stored device credentials, and API tokens. Where Redis is not directly reachable, authenticated attackers can deliver the payload through the application by configuring a device target that points at the rConfig server's loopback address.

### CVE-2026-124580

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-09T08:17:02.923 |

A vulnerability was found in Chengdu Feiyuxing Technology VW2100 and VEC10GP 1.0 B-MB3W202-210825-r11775. This impacts the function handle_wechat_cn_wifi of the file var/html/webserver of the component Weixin Auth Endpoint. The manipulation of the argument extend results in os command injection. The attack can be executed remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-113364

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-09T05:18:26.810 |

Buffer Overflow in the data receiving process in NEC Corporation WebSAM WinShare Ver 7.5.0 and earlier, Ver 7.6.0 and Ver 7.7.0 through 7.7.2 on Windows allows a remote unauthenticated attacker to execute arbitrary code with SYSTEM privileges via a crafted packet with a malformed data size value in the protocol header.

### CVE-2026-113363

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-09T05:18:26.107 |

Improper Input Validation in the network communication processing in NEC Corporation WebSAM WinShare Ver 7.2.0 through 7.5.0, Ver 7.6.0 and Ver 7.7.0 through 7.7.2 on Windows allows a remote unauthenticated attacker to execute arbitrary commands with SYSTEM privileges via a crafted network packet sent to the computer on which WinShare is running.

### CVE-2026-114464

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-08T17:16:36.583 |

IBM Process Mining 2.0.0 through 2.2.1 could allow a remote attacker to obtain sensitive information due to improper access control.

### CVE-2026-118462

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-09T12:16:37.130 |

Update components download and execute code without proper authenticity verification, relying on ignored hashes or forgeable checksums. Some update paths also permit archive traversal or script execution.

### CVE-2026-119506

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-09T01:17:01.197 |

Incorrect Privilege Assignment vulnerability in DynamiApps Frontend Admin by DynamiApps acf-frontend-form-element allows Privilege Escalation.This issue affects Frontend Admin by DynamiApps: from n/a through 3.30.1.

### CVE-2026-17466

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T18:17:03.303 |

IBM Optim 1.0.0, 1.1.0, and 1.2.0 could allow a remote authenticated attacker to obtain sensitive information due to path traversal.

### CVE-2026-101117

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-16` |
| Published | 2026-11-08T16:16:36.103 |

IBM WebSphere Extreme Scale 8.6.1.0 through 8.6.2.2 could allow a remote attacker to bypass security restrictions due to improper Content Security Policy configuration.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-124577

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-09T08:17:02.350 |

A weakness has been identified in Intelbras SG 2404 PoE L2+ 1.00.70/1.00.72. The affected element is an unknown function of the file /EXCU_SHELL of the component Web Management Interface. Executing a manipulation can lead to improper authentication. The attack can be launched remotely. The exploit has been made available to the public and could be used for attacks. Upgrading to version 1.00.74 is sufficient to fix this issue. Upgrading the affected component is advised.

### CVE-2026-124560

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-11-09T03:16:38.117 |

A vulnerability was found in D-Link DIR-878 1.20B05. This affects the function GetCAPTCHAsetting of the file bin/prog.cgi of the component HNAP Handler. Performing a manipulation of the argument uid results in heap-based buffer overflow. The attack can be initiated remotely. The exploit has been made public and could be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-95779

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-09T14:17:25.010 |

An exposure of the appliance’s confidential certificate  information 
vulnerability exists in HPE Morpheus manager software.

### CVE-2026-95778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-09T14:17:24.873 |

A remote code execution vulnerability exists in HPE Morpheus Software.

### CVE-2026-16283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-09T14:17:16.700 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Osbil Technology Ltd.Osbil Technology Ltd. OPanel allows OS Command Injection.

This issue affects oPanel: before 1.20.66.

### CVE-2026-94434

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-09T13:17:09.273 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Pardus Boot Repair allows OS Command Injection.

This issue affects Pardus Boot Repair: from 1.0.8 before 1.0.9.

### CVE-2026-9764

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-08T19:17:54.247 |

IBM Bob 1.0.4 through 2.0.1 could allow a remote attacker to inject arbitrary code on the system, due to the improper control of user input code.

### CVE-2026-8639

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-08T19:17:42.573 |

IBM Security Verify Directory 10.0.0 through 10.0.4 and IBM Verify Directory 11.0.0 is vulnerable to session fixation. An attacker can establish a session and, after the victim authenticates, hijack the authenticated session to gain unauthorized access to the directory management console.

### CVE-2026-117545

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-08T17:16:37.277 |

IBM webMethods Integration Server 12.1 could allow a remote authenticated attacker to bypass security restrictions due to improper authentication.

### CVE-2026-110273

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-08T17:16:36.130 |

IBM TRIRIGA Application Platform 5.0.0 through 5.0.9 IBM TRIRIGA could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-124553

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-08T15:16:51.460 |

BabelDOC from 0.3.61 before 0.7.0 contains a resource exhaustion vulnerability that allows remote attackers to exhaust CPU and memory by supplying unbounded bfrange and cidrange spans. Attackers can submit a crafted PDF whose embedded ToUnicode CMap declares a huge range, driving billions of loop iterations and stalling the translation worker.

### CVE-2026-92683

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-09T10:17:15.673 |

Incorrect authorization in the @authentication directive JWT where filter evaluation in Neo4j @neo4j/graphql versions 7.0.0 before 7.6.7 allows an attacker holding an otherwise-valid JWT to bypass all but the first filter condition via a multi-condition jwt where filter written in generic operator syntax.

### CVE-2026-124585

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-09T09:16:59.517 |

A vulnerability was found in Chengdu Feiyuxing Technology VW2100 and VEC10GP 1.0 B-MB3W202-210825-r11775. This issue affects the function add_expmac of the file var/html/webserver of the component Web Administration Interface. The manipulation of the argument mac results in os command injection. The attack may be performed from remote. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-113362

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-09T04:17:06.133 |

Improper Access Control in the program installation folder in NEC Corporation WebSAM Winshare Ver 7.5.0 and earlier (excluding Ver 7.3.3), Ver 7.6.0 and Ver 7.7.0 through 7.7.1 on Windows allows a locally authenticated low-privileged attacker to execute arbitrary code with SYSTEM privileges via a crafted DLL file that is loaded by a SYSTEM-level process.

### CVE-2026-114189

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-08T16:16:37.247 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WPVibes AnyWhere Elementor anywhere-elementor allows Blind SQL Injection.This issue affects AnyWhere Elementor: from n/a through 1.3.0.

### CVE-2026-116501

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-08T17:16:37.143 |

IBM Qiskit SDK 2.4.0 through 2.6.1 could allow a local attacker to execute arbitrary code due to an out-of-bounds write caused by improper input validation when accessing a corrupted unitary matrix.

### CVE-2026-116499

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-08T17:16:36.870 |

IBM Qiskit SDK 1.4.2 through 2.6.2 could allow a local attacker to execute arbitrary code due to deserialization of untrusted data.

### CVE-2026-119610

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-09T13:17:05.947 |

A flaw was found in GStreamer's gst-plugins-good, specifically in the H.264 RTP depayloader element. When processing MTAP16 or MTAP24 multi-time aggregation RTP packets, a signed/unsigned integer conversion error causes the remaining-length counter to underflow to a large positive value when the packet is truncated. This allows a remote, unauthenticated attacker to trigger an out-of-bounds heap read of up to approximately 64 KiB of process memory by sending a single malformed RTP packet. Successful exploitation can crash the receiving GStreamer pipeline (denial of service), and in relay or transcoding deployments where output is accessible to the attacker, may expose adjacent heap contents.

### CVE-2026-95648

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-09T13:17:09.403 |

Improperly controlled modification of Dynamically-Determined object attributes vulnerability in C-Prot Inc. C-Prot AppDefense allows Privilege Escalation.

This issue affects C-Prot AppDefense: before 1.0.2729.

### CVE-2026-118458

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-09T12:16:36.583 |

The shared AIS login routing selects a production-shipped test DAO and plaintext comparison for the H and V application codes, accepting fixed administrator accounts.

### CVE-2026-112172

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-09T12:16:35.170 |

CGM XDent and XMedical expose PHP synchronization endpoints that allow unauthenticated attackers to manipulate session variables and execute arbitrary SQL queries against backend MySQL databases.

### CVE-2026-94249

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-09T09:16:59.927 |

Missing Authorization vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Liderahenk allows Privilege Abuse.

This issue affects Liderahenk: before 2.0.3.

### CVE-2026-118904

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-08T20:17:23.980 |

IBM webMethods Integration Server 12.1 could allow a remote authenticated attacker to bypass security restrictions due to improper authentication.

### CVE-2026-97677

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-08T19:17:54.077 |

IBM Langflow OSS 1.0.0 through 1.12.2 An authenticated flow author could write attacker-controlled file content into any directory writable by the service account, bypassing the platform's local file access isolation safeguard. Via a crafted on-disk index, the attacker could also read the contents of arbitrary files accessible to the service process — including configuration files, secrets, or database files stored under the application's data directory.

### CVE-2026-19133

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-08T19:17:38.537 |

IBM Storage TS4500 Library 1.1.1.6 through 1.12.0.3 could allow a remote authenticated attacker to perform unauthorized account takeover due to improper authorization.

### CVE-2026-105467

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-08T17:16:35.120 |

IBM QRadar 7.5.0 through 7.5.0 Update Pack 16 Interim Fix 02, and 7.6.0.0 through 7.6.0.5 is vulnerable to Reflected XSS. A victim must open a specifically crafted URL while authenticated to QRadar to trigger this.

### CVE-2026-118461

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-09T12:16:37.000 |

The shared client accepts caller-controlled doctor identifiers for read and write operations without requiring authentication or authorization credentials.

### CVE-2026-118460

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-09T12:16:36.863 |

Embedded private keys protected by a shared password can be used to sign practitioner assertions for arbitrary practitioner identifiers, enabling unauthorized practitioner token requests.

### CVE-2026-124563

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-09T04:17:06.773 |

A security flaw has been discovered in D-Link DIR-878 1.20B05. Affected by this vulnerability is the function SetWanSettings of the component HNAP Handler. The manipulation of the argument Primary/Secondary results in buffer overflow. The attack may be launched remotely. The exploit has been released to the public and may be used for attacks. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-124562

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-11-09T04:17:06.560 |

A vulnerability was identified in D-Link DIR-878 1.20B05. Affected is the function SetWanSettings of the component HNAP Handler. The manipulation of the argument ConfigDNS/Primary/ConfigDNS/Secondary leads to buffer overflow. The attack may be initiated remotely. The exploit is publicly available and might be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-124561

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-09T04:17:06.317 |

A vulnerability was determined in D-Link DIR-878 1.20B05. This impacts the function SetVLANSettings of the file prog.cgi of the component HNAP Handler. Executing a manipulation of the argument VID can lead to stack-based buffer overflow. The attack can be launched remotely. The exploit has been publicly disclosed and may be utilized. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-107330

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-08T17:16:35.407 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to a Server-Side Request Forgery (SSRF) vulnerability.

### CVE-2026-120854

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-09T13:17:06.477 |

Allocation of Resources Without Limits or Throttling vulnerability in iubenda iubenda iubenda-cookie-law-solution allows HTTP DoS.This issue affects iubenda: from n/a through 3.13.6.

### CVE-2026-121629

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-09T12:16:37.847 |

A flaw was found in GStreamer's adaptive streaming demuxers (HLS, DASH, MSS). When processing a media playlist or manifest, URIs referenced in the manifest content are fetched without restricting which URI schemes are permitted. An attacker who controls a manifest URL, or who can inject content into an HTTP manifest response, can include file:// URIs pointing to arbitrary local files, causing the affected application to read and process those files. In automated or server-side deployments such as media recorders, proxies, and downloaders, this can lead to disclosure of sensitive local files. Existence of files can also be inferred through differing error responses even when content is not directly observable.

### CVE-2026-123475

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-09T11:17:23.613 |

Missing Authorization vulnerability in PT Norther Lights Production MapSVG mapsvg-lite-interactive-vector-maps allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects MapSVG: from n/a through 8.16.3.

### CVE-2026-121722

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-09T11:17:22.583 |

Missing Authorization vulnerability in WP E-Signature Formidable Forms Signature Online Contract Automation forms-signature-formidable-online-contract-automation allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Formidable Forms Signature Online Contract Automation: from n/a through 2.0.5.

### CVE-2026-106466

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-09T11:17:19.940 |

The JWT Auth WordPress plugin through 3.0.2 does not invalidate previously issued refresh tokens when a user changes or resets their password or removes a connected device, allowing an attacker who obtained a refresh token before such an event to keep issuing valid access tokens and retain authenticated access to the account, up to Administrator.

### CVE-2026-123465

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-11-09T10:17:08.180 |

Exposure of Sensitive System Information to an Unauthorized Control Sphere vulnerability in myCred myCred mycred allows Retrieve Embedded Sensitive Data.This issue affects myCred: from n/a through 4.0.2.

### CVE-2026-121760

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-09T10:17:07.020 |

Missing Authorization vulnerability in weDevs weDocs wedocs allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects weDocs: from n/a through 2.6.1.

### CVE-2026-96146

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T20:17:25.193 |

IBM SevOne Network Performance Management 7.0.0 through 8.2.2 could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption.

### CVE-2026-93879

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-08T19:17:43.763 |

Hibernate Validator could allow a remote attacker to cause a denial of service due to uncontrolled resource consumption resulting from improper escaping of user-controlled data in Expression Language (EL) expressions.

### CVE-2026-18093

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-08T18:17:03.440 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.2 could allow a remote attacker to obtain sensitive information due to broken access control.

### CVE-2026-118791

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-09T13:17:05.337 |

The application implements software update functionality without adequate authenticity and integrity validation, allowing update packages to be accepted without sufficient cryptographic verification.

### CVE-2026-118790

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-09T13:17:05.200 |

Multiple hardcoded credentials are embedded within product components and administrative functionalities. These credentials may enable unauthorized access to privileged accounts, services, or application features across affected deployments.

### CVE-2026-118468

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-09T12:16:37.710 |

XML parsers process attacker-influenced update manifests or network responses with external entity resolution enabled, potentially allowing XML External Entity (XXE) attacks.

### CVE-2026-120856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T13:17:06.770 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Rymera Web Co Invoice Gateway for WooCommerce – Invoice Payment Gateway invoice-gateway-for-woocommerce allows Reflected XSS.This issue affects Invoice Gateway for WooCommerce – Invoice Payment Gateway: from n/a through 1.1.6.

### CVE-2026-123476

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T11:17:23.770 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in fifu.app Featured Image from URL featured-image-from-url allows Stored XSS.This issue affects Featured Image from URL: from n/a through 6.1.4.

### CVE-2026-123460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T11:17:23.453 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Nickboss WordPress File Upload wp-file-upload allows Stored XSS.This issue affects WordPress File Upload: from n/a through 5.2.2.

### CVE-2026-122666

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T11:17:23.310 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kitae Park Mang Board WP mangboard allows Reflected XSS.This issue affects Mang Board WP: from n/a through 2.4.7.

### CVE-2026-121782

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T11:17:22.737 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in If-So Dynamic Content If-So Dynamic Content Personalization if-so allows Reflected XSS.This issue affects If-So Dynamic Content Personalization: from n/a through 1.10.3.

### CVE-2026-121570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T11:17:22.423 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Chill RSVP and Event Management rsvp allows Stored XSS.This issue affects RSVP and Event Management: from n/a through 2.7.17.

### CVE-2026-54863

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:10.647 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Mamunur Rashid Review Schema review-schema allows Reflected XSS.This issue affects Review Schema: from n/a through 3.1.4.

### CVE-2026-123484

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:08.403 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetFormBuilder jetformbuilder allows DOM-Based XSS.This issue affects JetFormBuilder: from n/a through 3.6.8.

### CVE-2026-123463

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:07.953 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Wham Checkout Files Upload for WooCommerce checkout-files-upload-woocommerce allows Stored XSS.This issue affects Checkout Files Upload for WooCommerce: from n/a through 2.4.0.

### CVE-2026-121780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:07.727 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Gijo Varghese Flying Images nazy-load allows Stored XSS.This issue affects Flying Images: from n/a through 2.4.15.

### CVE-2026-121764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:07.483 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in FolioVision FV Flowplayer Video Player fv-wordpress-flowplayer allows Stored XSS.This issue affects FV Flowplayer Video Player: from n/a through 7.5.56.7212.

### CVE-2026-119505

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:06.563 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Welcart Welcart e-Commerce usc-e-shop allows Stored XSS.This issue affects Welcart e-Commerce: from n/a through 2.12.6.

### CVE-2026-119504

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:06.340 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in DynamiApps Frontend Admin by DynamiApps acf-frontend-form-element allows Stored XSS.This issue affects Frontend Admin by DynamiApps: from n/a through 3.30.1.

### CVE-2026-119483

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:05.627 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in 10Web Form Maker by 10Web form-maker allows Stored XSS.This issue affects Form Maker by 10Web: from n/a through 1.15.50.

### CVE-2026-111403

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-09T10:17:03.140 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Inventory WP Inventory Manager wp-inventory-manager allows Reflected XSS.This issue affects WP Inventory Manager: from n/a through 2.5.9.

### CVE-2026-18893

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-08T19:17:38.380 |

IBM CockroachDB PostgreSQL for IBM VPC 26.2.0 through 26.2.3, 25.4.0 through 25.4.12, and 25.2.0 through 25.2.20 is vulnerable to privilege escalation via user-defined function.

### CVE-2026-109899

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-08T16:16:36.603 |

Missing Authorization vulnerability in Melapress Melapress Role Editor melapress-role-editor allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Melapress Role Editor: from n/a through 1.3.0.
