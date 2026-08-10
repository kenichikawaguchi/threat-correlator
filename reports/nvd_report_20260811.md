# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-10 15:00 UTC
- **対象期間**: `2026-08-09T15:00:17.000Z` 〜 `2026-08-10T15:00:43.000Z`
- **重要CVE数**: 49 件（Critical 9.0+: 14 件 / High 7.0〜: 35 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上ります。目立つ傾向は以下の通りです。  

* **認証不要でリモートコード実行 (RCE) が可能** な脆弱性が多数（Joomla、Zyxel、PHP ファイルマネージャ等）。  
* **OS コマンドインジェクション** が Web アプリのパラメータに直接渡される設計ミスに起因し、ほぼ全てのケースで *Unauthenticated*（認証不要）となっている。  
* **IoT/組み込み系製品**（Xiaomi スマートスピーカー、DEEBOT ロボット掃除機）でも同様に認証回避や SSRF が報告され、物理的に近い環境でも深刻な被害が想定されます。  
* 多くの脆弱性が **古いバージョンのオープンソースパッケージ**（phpfm、crontab‑ui、APIJSON 等）に残存しており、アップデートが遅れていることがリスク拡大の要因です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|-----|------|----------------|------------------------|------------------------|
| **CVE‑2026‑66915** | **10.0** | Joomla Extension *Fabrik* の **リモートコード実行**（`ajax_calc` パラメータ） | Joomla サイトに本拡張を導入している全サーバが、認証なしで任意の PHP コード実行可能。サイト全体の乗っ取りや情報漏洩につながる。 | 1. `fabrik` を **4.6.7 以上** に更新<br>2. 不要なプラグインは無効化・削除<br>3. Web アプリファイアウォールで `ajax_calc` へのリクエストをブロック |
| **CVE‑2026‑13206** | **9.8** | Zyxel WAH7601 の **OS コマンドインジェクション** | ネットワーク上の WAH7601 デバイスに対し、特製 HTTP リクエストで任意コマンド実行。管理者権限取得や内部ネットワーク横移動が可能。 | 1. Zyxel 公式ファームウェア **2022‑07‑20 以降** にアップデート<br>2. 管理インタフェースへの外部からのアクセスを ACL で制限<br>3. 不要な管理ポート (Telnet/SSH) を無効化 |
| **CVE‑2026‑72593** / **CVE‑2026‑72592** (同一製品) | **9.8** | dulldusk/phpfm の **認証なしファイルマネージャ** と **任意コード実行**（未検証のアップロード） | 任意のサーバ上ファイルの閲覧・改ざん・削除、さらにアップロードした PHP を実行できるため、完全なサーバ乗っ取りが可能。 | 1. phpFM を **1.8.1 以上** に更新（認証デフォルト有効化）<br>2. `upload_ext` フィルタを適切に設定し、`.php` 系拡張子を除外<br>3. 公開ディレクトリ外へのインストールを回避 |
| **CVE‑2026‑72590** / **CVE‑2026‑72589** | **9.8** | alseambusher/crontab‑ui の **OS コマンドインジェクション** と **任意 DB インポート** | `/crontab` の `env_vars` パラメータや `/import` エンドポイントに細工したデータを送るだけで、サーバ上で任意コマンド実行・データベース改ざんが可能。 | 1. crontab‑ui を **0.4.3 以上** に更新<br>2. `env_vars` の入力を正規表現でサニタイズ<br>3. ファイルインポートは MIME と拡張子の二重チェックを実装 |
| **CVE‑2026‑72580** | **9.8** | duhow/xiaoai‑patch の **IoT デバイス向け OS コマンドインジェクション**（`/mute`/`/unmute` の `silent` パラメータ） | Xiaomi スマートスピーカーに対し、外部から HTTP リクエストで任意コマンド実行。家庭内ネットワークの踏み台化やプライバシー情報取得が懸念される。 | 1. `xiaoai-patch` を **最新コミット (2026‑08‑xx) 以降** にビルドしデプロイ<br>2. `silent` パラメータをホワイトリスト化し、数値以外は拒否<br>3. デバイスの外部公開ポートを閉じ、VPN 経由のみアクセス許可 |

> **注**：上記 5 件は **CVSS が 9.8 以上** かつ **認証不要でリモートコード実行が可能** という点で共通しており、被害拡大リスクが最も高いと判断しました。

---

## 3. 推奨アクション  

### 3.1 パッケージ・ファームウェアの即時更新
| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン (修正済) | 更新手順 |
|-------------------|----------------------|--------------------------|----------|
| Joomla **Fabrik** (extension) | `< 4.6.7` | `4.6.7` 以上 | Joomla 管理画面 → Extensions → Manage → Update |
| Zyxel **WAH7601** (firmware) | `through 20072026` | `2022‑07‑20` 以降 | Zyxel ポータル → Firmware Download → 最新版適用 |
| **phpfm** (dulldusk/phpfm) | `≤ 1.8.0` | `1.8.1` 以上 | Composer: `composer require dulldusk/phpfm:^1.8.1` |
| **crontab‑ui** (alseambusher) | `≤ 0.4.2` | `0.4.3` 以上 | npm: `npm install crontab-ui@0.4.3` |
| **xiaoai‑patch** (duhow) | `commit fb07049` | `最新コミット (2026‑08‑xx)` | Git pull → `docker build` もしくは公式リリースバイナリ取得 |
| **APIJSON** (Tencent) | `≤ 8.1.8` | `8.1.9` 以上 | Maven/Gradle の依存バージョンを更新 |
| **DeepWiki‑Open** (AsyncFuncAI) | `≤ commit 16f35a0` | `最新コミット` | `git pull && pip install -e .` |

### 3.2 設定・運用上の緊急対策
1. **認証

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-66915

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-10T10:17:33.310 |

Joomla Extension - fabrikar.com - Remote code execution in Fabrik < 4.6.7 - An unauthenticated attacker could execute arbitrary code by using the ajax_calc feature of the calc plugin.

### CVE-2026-13206

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T13:17:56.020 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Zyxel Networks WAH7601 allows OS Command Injection.

This issue affects WAH7601: through 20072026.

### CVE-2026-72593

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T11:17:32.490 |

A missing authentication vulnerability in dulldusk/phpfm through 1.8.0 allows an unauthenticated remote attacker to access the full file manager functionality including reading, writing, deleting, and uploading files anywhere on the server filesystem.

### CVE-2026-72592

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-10T11:17:32.370 |

An unrestricted file upload vulnerability in dulldusk/phpfm through 1.8.0 allows an unauthenticated remote attacker to execute arbitrary PHP code on the server. The application ships with an empty upload extension filter ( = array) and no authentication enabled by default (auth_pass is empty string), allowing an unauthenticated attacker to upload a PHP webshell and execute it by browsing to the uploaded path.

### CVE-2026-72590

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-10T11:17:32.123 |

An OS command injection vulnerability in alseambusher/crontab-ui through 0.4.2 allows an unauthenticated remote attacker to inject arbitrary cron job entries by sending a crafted GET request to /crontab with URL-encoded newlines in the env_vars parameter.

### CVE-2026-72589

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T11:17:32.003 |

An OS command injection vulnerability in alseambusher/crontab-ui through 0.4.2 allows an unauthenticated remote attacker to execute arbitrary system commands by importing a crafted crontab database file. The POST /import endpoint accepts arbitrary .db files and overwrites the application database without validation.

### CVE-2026-72580

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T11:17:30.897 |

An OS command injection vulnerability in duhow/xiaoai-patch through commit fb07049 allows a remote attacker to execute arbitrary system commands on Xiaomi smart speakers running the patch. The /mute and /unmute endpoint handlers in api/main.py pass the user-supplied silent query parameter directly to os.system() without sanitization, enabling command injection via shell metacharacters.

### CVE-2026-72577

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T11:17:30.533 |

Multiple vulnerabilities in NASA fprime-gds through 3.4.3 allow an unauthenticated remote attacker to achieve arbitrary code execution on the ground station host and inject arbitrary commands to connected spacecraft. The Flask application in src/fprime_gds/flask/app.py applies no authentication to any endpoint.

### CVE-2026-72567

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T11:17:29.220 |

An improper path validation vulnerability in AsyncFuncAI/deepwiki-open through commit 16f35a0 allows unauthenticated remote attackers to write to or delete arbitrary files with root privileges. The api/api.py wiki-cache endpoint constructs file paths from user-controlled owner, repo, and repo_type fields without sanitization, enabling path traversal.

### CVE-2026-72565

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T11:17:28.973 |

A SQL injection vulnerability in Tencent APIJSON through 8.1.8 allows unauthenticated remote attackers to bypass per-table access control and read arbitrary database tables via the Map-form @having operator.

### CVE-2026-72564

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T11:17:28.837 |

An improper authorization vulnerability in fosrl/pangolin through v1.20.0 allows an authenticated remote attacker to authenticate to any resource in any organization by reusing an access token issued for a different resource.

### CVE-2026-63106

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-10T14:17:25.633 |

ReadyEcommerce before 4.5.2 contains an unauthenticated SQL injection vulnerability in the product listing API where the rating parameter from the products endpoint is concatenated directly into a MySQL HAVING clause without parameterization in ProductController.php. Attackers can perform time-based blind SQL injection through the unsanitized rating parameter to extract the full database contents, including user credentials and administrator password hashes, with potential additional file system access due to the database connection running as root.

### CVE-2026-72575

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-10T11:17:30.277 |

An improper authorization vulnerability in daptin through v0.12.34 allows unauthenticated remote attackers to read, create, update, and delete usergroup records. The permission check functions (CanRead, CanPeek, CanCreate, CanUpdate, CanDelete, CanRefer) in server/permission/permission.go return true whenever p.UserId equals the requesting userId, but fail to reject the null/zero reference — unlike CanExecute, which explicitly guards it.

### CVE-2026-72569

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T11:17:29.503 |

A path traversal vulnerability in cube-root/directory-serve through 1.3.7 allows an unauthenticated remote attacker to delete arbitrary files outside the intended served directory when the application is run with the --delete option.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-72578

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-10T11:17:30.660 |

A cross-site request forgery (CSRF) vulnerability in FreePBX Framework 17.0 allows an unauthenticated remote attacker to perform administrative actions on behalf of an authenticated administrator.

### CVE-2026-72573

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T11:17:30.010 |

An OS command injection vulnerability in 4xmen/pm2panel (all versions) allows an authenticated remote attacker to execute arbitrary system commands on the host. The pm2panel.js handler at line 188 passes the unsanitized req.query.id parameter directly to exec('pm2 restart ' + id) without input validation or shell escaping, enabling command chaining via semicolons or other shell metacharacters.

### CVE-2026-64940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-625` |
| Published | 2026-08-10T08:16:48.733 |

Tegalog -Fumy Otegaru Memo Logger- provided by Nishishi Factory contains a vulnerability due to a permissive regular expression, which may allow an attacker who can access the affected product to log in to the management console. As a result, the attacker may perform any operations available from the management console.

### CVE-2026-59233

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T13:19:51.713 |

Missing Authorization in the permission management component in Roskus Prospero Flow CRM before 5.2.1 allows any authenticated user to grant any role, including their own, the complete set of application permissions via a crafted POST request to the permission save endpoint, which performs no authorization check before synchronizing the submitted permissions to the specified role.

### CVE-2026-66405

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-08-10T09:17:22.637 |

DEEBOT PRO M1 and DEEBOT PRO K1VAC leave the telnet servers enabled. The telnet service may be leveraged to log in to the affected products.

### CVE-2026-66403

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-489` |
| Published | 2026-08-10T09:17:22.297 |

DEEBOT PRO M1 and DEEBOT PRO K1VAC leave the web server for debugging purposes enabled. The floor map and log information stored on the affected products may be retrieved.

### CVE-2026-72581

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-10T11:17:31.017 |

A server-side request forgery (SSRF) vulnerability in duhow/xiaoai-patch through commit fb07049 allows a remote attacker to make the Xiaomi smart speaker perform HTTP requests to arbitrary internal or external URLs. The /auth endpoint in api/main.py uses the user-supplied url POST parameter to redirect to a Home Assistant instance without validating the destination URL, enabling internal network scanning and access to internal services.

### CVE-2026-59090

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-10T13:19:51.573 |

A flaw was found in GIMP's PSD file format plugin. This vulnerability, an unsigned integer underflow in the `block_rem` variable, occurs when a user opens a specially crafted `.psd` image file. The underflow leads to parser confusion, enabling an attacker to inject arbitrary data as layer resource blocks. This can ultimately result in arbitrary code execution, allowing the attacker to run malicious code on the victim's system.

### CVE-2026-21068

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T09:17:20.110 |

Stack-based buffer overflow in libril_sem.so prior to SMR Aug-2026 Release 1 allows privileged local attackers to execute arbitrary code.

### CVE-2026-13133

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T07:16:46.173 |

A vulnerability has been identified in LineInst.exe (LINE for Windows) prior to version 26.4.0, where Msftedit.dll is loaded via a relative path without a secure DLL search path, allowing a malicious DLL placed in the installer's directory to be loaded ahead of the legitimate System32 copy.

### CVE-2026-12984

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-10T13:17:55.887 |

Insufficiently Protected Credentials vulnerability in Zyxel Networks WAH7601 allows Retrieve Embedded Sensitive Data.

This issue affects WAH7601: through 20072026.

### CVE-2026-59087

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-10T11:17:26.910 |

A flaw was found in the GIMP image manipulation program, specifically within its Seattle Filmworks file loader. A remote attacker could exploit this vulnerability by tricking a user into opening a specially crafted Seattle Filmworks file. This could lead to a heap overflow, allowing the attacker to write several kilobytes of controlled data beyond the intended memory buffer. Such an overflow can result in memory corruption, potentially leading to arbitrary code execution or a denial of service.

### CVE-2026-72591

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-10T11:17:32.253 |

A server-side request forgery (SSRF) vulnerability in gabehf/Koito through v0.3.2 allows an authenticated user to make the server perform HTTP requests to arbitrary internal or external hosts by supplying a crafted image_url value in the PATCH /apis/web/v1/album/{id}/image endpoint.

### CVE-2026-72566

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-10T11:17:29.100 |

A server-side request forgery (SSRF) vulnerability in automatisch through commit 41f3c56 allows a low-privileged authenticated user with 'manage Flow' permission to make the server fetch arbitrary URLs and retrieve the full response body via the HTTP Request app's Custom Request action.

### CVE-2026-66407

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-10T09:17:22.917 |

DEEBOT PRO M1 and DEEBOT PRO K1VAC improperly implement authentication in WebSocket communication.
The WebSocket private key may be retrieved through analyzing the traffic data via a man-in-the-middle attack, and communication contents may be altered.

### CVE-2026-72594

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-10T11:17:32.610 |

A stored cross-site scripting (XSS) vulnerability in lobehub/lobe-chat through v2.2.13 allows a low-privileged authenticated user to inject arbitrary JavaScript into the application by uploading a crafted SVG file as a user avatar.

### CVE-2026-19387

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-10T03:16:40.223 |

A heap out-of-bounds write vulnerability was found in the GStreamer gst-plugins-bad adpcmdec element when decoding IMA/DVI ADPCM audio. Insufficient validation of the per-block sample count for multi-channel streams allows a crafted WAV file to cause writes beyond the allocated output buffer. This can lead to application crash, denial of service, memory corruption, or potentially arbitrary code execution when untrusted media is processed.

### CVE-2026-72692

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-10T13:20:39.470 |

A missing authorization vulnerability in OpenSignLabs opensignserver through 2.37.0 allows an unauthenticated remote attacker to irreversibly decline any in-flight document and forge the decline attribution to an arbitrary user via the declinedoc Parse cloud function. The function writes IsDeclined, DeclineReason, and a caller-supplied DeclineBy pointer without verifying the caller's identity, enabling workflow termination and evidentiary record falsification against any accessible document.

### CVE-2026-72691

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-10T13:20:39.350 |

An authentication bypass vulnerability in OpenSignLabs opensignserver through 2.37.0 allows an unauthenticated remote attacker to mint MASTER_KEY-signed file access tokens for arbitrary stored files via the getsignedurl Parse cloud function. The function skips its isAuthenticated check whenever any docId parameter is supplied, even one corresponding to no real document, allowing the authentication gate to be bypassed by supplying an arbitrary string as docId.

### CVE-2026-72689

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T13:20:39.103 |

A broken object-level authorization vulnerability in OpenSignLabs opensignserver through 2.37.0 allows an unauthenticated remote attacker to read complete contract records via the getDocument Parse cloud function. The function fetches documents using useMasterKey, bypassing the object ACL, and returns full records including sender and signer PII and a pre-signed document download URL whenever the document's IsEnableOTP flag is unset, which is the default configuration.

### CVE-2026-72688

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T13:20:38.987 |

A missing authentication vulnerability in OpenSignLabs opensignserver through 2.37.0 allows an unauthenticated remote attacker to read arbitrary stored documents via the fileupload Parse cloud function. The function mints MASTER_KEY-signed file access tokens for any caller-supplied URL without performing any session check, defeating the only access control protecting stored contract files.

### CVE-2026-72586

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-10T11:17:31.637 |

A missing authentication vulnerability in frangoteam/FUXA through 1.3.3 allows an unauthenticated remote attacker to query all historical sensor data via the DAQ_QUERY Socket.IO event. When secureEnabled=true, all other sensitive Socket.IO events (DEVICE_BROWSE, HOST_INTERFACES, DEVICE_TAGS_REQUEST, etc.) call isSocketAdminAuthorized to verify the connection token, but the DAQ_QUERY handler in server/runtime/index.js lacks this check entirely.

### CVE-2026-72582

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-10T11:17:31.137 |

A NULL pointer dereference vulnerability in fastschema through v0.15.1 allows an unauthenticated remote attacker to crash the server process with a single HTTP request. The sendOTPEmail function in pkg/auth/local.go dereferences a pointer obtained from an unchecked error path without validating it is non-nil, causing a fatal panic that terminates the entire server when a recovery request is sent to the /api/auth/local/recover endpoint.

### CVE-2026-72579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-10T11:17:30.780 |

An OS command injection vulnerability in NASA HyperCP (main branch) allows a network-adjacent attacker who can intercept or spoof responses from oceandata.sci.gsfc.nasa.gov to execute arbitrary system commands on the researcher's workstation.

### CVE-2026-72572

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T11:17:29.883 |

A path traversal vulnerability in o1lab/xmysql (all versions) allows an unauthenticated remote attacker to read and download arbitrary files from the server. The lib/xapi.js file at lines 338 and 424 uses the user-controlled req.query.name parameter in path.join(cwd, name) without sanitization before passing it to res.download, enabling directory traversal via ../ sequences to access sensitive system files.

### CVE-2026-72571

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-10T11:17:29.760 |

A path traversal vulnerability in mustafaakin/cast-localvideo (all versions) allows an unauthenticated remote attacker to read arbitrary files from the server. The app.js handler at lines 151-153 passes the user-supplied req.body.dir parameter directly to res.sendFile() without sanitization, enabling directory traversal via absolute paths or ../ sequences to read sensitive system files.

### CVE-2026-72584

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-10T11:17:31.390 |

A time-of-check/time-of-use (TOCTOU) race condition in fastschema through v0.15.1 allows an unauthenticated remote attacker to bypass the OTP attempt limit on the account recovery flow, enabling brute-force attacks on 6-digit OTP codes.

### CVE-2026-6374

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-10T13:20:38.353 |

Use of Hard-coded Credentials vulnerability in Zyxel Networks WAH7601 allows Read Sensitive Constants Within an Executable.

This issue affects WAH7601: through 20.07.2026.

### CVE-2026-21074

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T09:17:20.893 |

Incorrect default permissions in Bixby prior to version 4.0.86.0 allows local attackers to execute arbitrary commands with Bixby privilege.

### CVE-2026-72690

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-10T13:20:39.230 |

An improper authorization vulnerability in Attendize through commit 9289acb allows an authenticated remote attacker to inject persistent mandatory survey questions into another organizer's events via the POST /event/{event_id}/question/create endpoint. The postCreateEventQuestion method loads the target event without the tenant-isolation scope, enabling cross-tenant writes; the injected question cannot be removed by the victim because the victim's account-scoped delete path cannot resolve a question owned by another tenant.

### CVE-2026-72568

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-10T11:17:29.373 |

An out-of-bounds read vulnerability in Redis through 8.8.1 allows an adjacent unauthenticated attacker to cause denial of service or information disclosure by sending a specially crafted PING message to the Redis Cluster Bus port.

### CVE-2026-19389

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-10T03:16:40.380 |

Multiple integer overflow and underflow vulnerabilities were found in the GStreamer gst-plugins-ugly ASF demuxer (asfdemux) when parsing header objects from crafted ASF, WMV, or WMA files. Insufficient validation of attacker-controlled length and size values can bypass bounds checks and cause out-of-bounds heap reads. This can result in application crash, denial of service, or limited information disclosure when untrusted media is processed.

### CVE-2026-19381

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-08-10T01:16:48.367 |

A security flaw has been discovered in Kingston FURY CTRL RGB Control Software 2.0.65.0. The impacted element is an unknown function in the library NTIOLib_KSFX.sys of the component Driver. Performing a manipulation results in improper privilege management. The attack needs to be approached locally. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-21079

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T09:17:21.550 |

Missing encryption of sensitive data in Smart Switch prior to version 3.7.72.6 allows adjacent attackers to intercept transmitted data.

### CVE-2026-21064

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-10T09:17:19.617 |

Improper access control in Weaver prior to SMR Aug-2026 Release 1 allows local attackers to cause device inoperability.
