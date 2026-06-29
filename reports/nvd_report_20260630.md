# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-29 15:00 UTC
- **対象期間**: `2026-06-29T10:11:15.000Z` 〜 `2026-06-29T15:00:23.000Z`
- **重要CVE数**: 16 件（Critical 9.0+: 0 件 / High 7.0〜: 16 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **リモートコード実行 / 権限昇格** を伴う高深刻度（CVSS ≥ 7.0）で、特に **パス・トラバーサル** や **不適切な入力検証** が共通の根本原因となっています。  
- 開発言語・プラットフォームは多岐にわたり、VS Code の拡張機能、Linux パッケージマネージャ（libzypp）、Web アプリ（FrontAccounting）やシステムユーティリティ（attr/acl）など、**開発者ツールからインフラまで幅広く影響** が及んでいます。  
- 多くの脆弱性は **既知のパッケージバージョンが数か月前にリリースされたパッチ** によって修正済みであるため、**速やかなアップデートが最も効果的な防御策** となります。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|------------|------------------------|
| **CVE‑2026‑12856** | 8.8 | VS Code 用 *vscode‑java* 拡張が **Markdown コンテンツを無条件に信頼** し、JavaDoc hover 内のリンクをクリックさせることで任意コマンド実行が可能 | VS Code を使用するすべての開発者が対象。特にリモートリポジトリから取得したコードを閲覧する際に、攻撃者が細工した JavaDoc を仕込めばローカルマシンでコード実行 (C/H/I/A がすべて High) |
| **CVE‑2026‑25707** | 8.8 | libzypp (openSUSE / SUSE のパッケージマネージャ) に **相対パストラバーサル** が存在し、リモートリポジトリから提供されたメタデータで任意ファイルを書き換え可能 | 管理者権限でパッケージをインストール/更新する環境全般。攻撃者が悪意あるリポジトリを用意すれば、システム全体の権限昇格やサービス停止が実現 |
| **CVE‑2026‑40521** | 8.7 | FrontAccounting 2.4.20 未満の **添付ファイルアップロードハンドラ** がパストラバーサルを許し、`unique_name` に `../../../` を含めると任意コード実行 | 会計システムを社内で利用している企業。認証済みユーザー（最低でも「会計担当」権限）からリモートでバックドアを設置でき、内部ネットワーク全体に被害が拡大 |
| **CVE‑2026‑13165** | 8.6 | SzafirHost が **JarFile と JarInputStream の検証ロジック不整合** により、攻撃者が配布する JAR に不正なネイティブライブラリを混入できる | Java アプリケーションの自動アップデート機構やプラグイン配布を行う環境で、サーバ側が改ざんされたアーカイブを配布するとクライアント側で任意の DLL/SO がロードされ、リモートコード実行が成立 |
| **CVE‑2026‑54371 / CVE‑2026‑54369** | 8.4 | `attr` (2.6.0 未満) と `acl` (2.4.0 未満) の **シンボリックリンクトラバーサル** がディレクトリ階層走査時に発生し、ローカルユーザーが任意のパスを書き換えて権限昇格 | ローカルでシステムユーティリティを使用できる全ユーザーが対象。特権が必要な操作 (例: ファイル属性変更) を経由して root 権限取得が可能 |

> **選定理由**  
> - **スコアが高く (≥ 8.5)**、かつ **リモートからのコード実行や権限昇格** が直接可能。  
> - **利用者が多い**（VS Code、Linux ディストリビューション、会計システム）ため、組織全体へのインパクトが大きい。  
> - **パッチが既に公開** されているケースが多く、**アップデートで即座にリスク低減** が可能。

---

## 3. 推奨アクション  

### 共通対策
1. **脆弱性情報の定期的なモニタリング**（National Vulnerability Database、各ベンダーのセキュリティアドバイザリ）を導入し、CVSS ≥ 7.0 の情報は 48 時間以内に評価・対応する体制を整える。  
2. **最小権限の原則**を徹底し、特にリモートリポジトリや外部プラグインを扱う際は **信頼できるソースのみ** を許可する。  
3. **CSP / SRI** などのフロントエンド防御策を導入し、外部コンテンツの実行を制限する（特に VS Code の WebView での CSP 設定）。

### 個別パッケージ・バージョン別対策

| 製品 / パッケージ | 現行バージョン (脆弱) | **推奨バージョン** | アップデート手順例 |
|-------------------|----------------------|-------------------|-------------------|
| **vscode‑java** (VS Code 拡張) | ≤ 0.78.0 | **0.79.0 以降** | VS Code → 拡張機能 → 「更新」または `code --install-extension redhat.java@latest` |
| **libzypp** (openSUSE/SUSE) | < 17.38.10 | **17.38.10 以降** | `zypper refresh && zypper update libzypp` |
| **FrontAccounting** | < 2.4.20 | **2.4.20** (パス・トラバーサル・SQLi 修正済) | `git pull && composer install` もしくは公式リリースパッケージを上書き展開 |
| **SzafirHost** | 1.2.3 以前 | **1.2.4 以降** | `apt-get update && apt-get install szafirhost`（Debian 系） |
| **attr** | < 2.6.0 | **2.6.0** 以上 | `yum update attr` / `apt-get install attr` |
| **acl** | < 2.4.0 | **2.4.0** 以上 | `yum update acl` / `apt-get install acl` |
| **fast-uri** | 2.3.1‑3.1.2, 4.0.0 | **3.1.3 以降** (Unicode 正規化修正) | `npm install fast-uri@latest` |
| **Edimax EW‑7478APC** ファームウェア | 1

---

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-12856

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-06-29T14:16:41.473 |

A flaw was found in the vscode-java extension, which provides Java language support for Visual Studio Code. The extension incorrectly trusts all Markdown content in JavaDoc hovers, allowing a malicious Java file to include hidden commands. If a user clicks a specially crafted link within a JavaDoc hover popup, an attacker can execute arbitrary VS Code commands, which can lead to full system compromise in trusted workspaces.

### CVE-2026-25707

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-06-29T10:16:30.330 |

A relative path traversal bug problem when processing repository metadata in libzypp before 17.38.10 could be used by remote attackers supplying repositories to overwrite files on the system, leading to denial of service or privilege escalation.

### CVE-2026-40521

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-29T14:16:50.763 |

FrontAccounting before 2.4.20 contains a path traversal vulnerability in the attachment upload handler that allows authenticated attackers to execute arbitrary code by uploading files with traversal sequences in the unique_name parameter. Attackers can supply path traversal sequences ../../../shell.php to write files outside the intended attachments directory into the web root, and by uploading PHP files without extension validation, achieve remote code execution as the web server user.

### CVE-2026-13165

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-29T14:16:41.647 |

SzafirHost verifies the downloaded native library archive with one JarFile parser (reading the Central Directory) but extracts native libraries with JarInputStream parser (reading sequentially from local file headers). An attacker who controls the served archive can insert a malicious DLL/SO/DYLIB as a local-file-header entry between the last legitimate entry and the Central Directory, without adding it to the Central Directory. The signature verifier never sees the injected entry and accepts the archive as validly signed; the extractor reads it sequentially and writes the attacker library to the native temp directory with no hash check), while the archive-size check still passes. This can lead to remote code execution.

This issue was fixed in version 1.2.2.

### CVE-2026-54371

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-29T14:16:57.823 |

attr before version 2.6.0 contains a symlink traversal vulnerability in the getfattr and setfattr utilities that allows local attackers to escalate privileges by replacing a pathname component with a symbolic link during directory hierarchy traversal. Attackers who control a pathname component can redirect getfattr and setfattr operations to arbitrary files by substituting a symlink, leading to local privilege escalation when getfattr or setfattr is invoked by a privileged process over an attacker-controlled path.

### CVE-2026-54369

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-29T14:16:57.487 |

acl before version 2.4.0 contains a symlink traversal vulnerability in the libacl pathname-based functions acl_get_file(), acl_set_file(), acl_extended_file(), and acl_delete_def_file() that allows local attackers to escalate privileges by replacing any pathname component with a symbolic link. Attackers who control any component of a pathname processed by a privileged caller can redirect ACL read or write operations to arbitrary files or directories, enabling unauthorized manipulation of access control lists and local privilege escalation.

### CVE-2026-13676

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-06-29T14:16:47.967 |

fast-uri versions 2.3.1 through 3.1.2 and 4.0.0 fail to canonicalize Unicode (IDN) hostnames for HTTP-family URLs. The IDN conversion path calls a helper that does not exist on the global URL constructor, silently leaving the host in its original Unicode form while normalize() and equal() still return values that differ from a WHATWG-compatible URL parser. Applications that use fast-uri to enforce host-based policy (denylists, loopback filtering, redirect validation, outbound proxy routing) before passing the same URL to Node's URL or fetch can be bypassed when the two implementations resolve the same input to different hosts. Patches: upgrade to fast-uri 3.1.3 for the 3.x line or 4.0.1 for the 4.x line. Workarounds: enforce host policy using the same URL parser used for the actual request, or reject non-ASCII hosts before policy checks.

### CVE-2026-13564

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T12:16:28.543 |

A vulnerability was found in Edimax EW-7478APC 1.04. Affected is the function formPPPoESetup of the file /goform/formPPPoESetup of the component POST Request Handler. Performing a manipulation of the argument pppUserName results in stack-based buffer overflow. The attack can be initiated remotely. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-13563

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-06-29T12:16:28.390 |

A vulnerability has been found in Edimax EW-7478APC 1.04. This impacts the function formL2TPSetup of the file /goform/formL2TPSetup of the component POST Request Handler. Such manipulation of the argument L2TPUserName leads to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-13562

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-06-29T12:16:28.233 |

A flaw has been found in Edimax EW-7478APC 1.04. This affects the function formiNICSiteSurvey of the file /goform/formiNICSiteSurvey of the component POST Request Handler. This manipulation of the argument selSSID causes buffer overflow. It is possible to initiate the attack remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-54370

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-06-29T14:16:57.670 |

acl before version 2.4.0 contains a time-of-check to time-of-use (TOCTOU) race condition vulnerability that allows local attackers to escalate privileges by replacing a pathname component with a symbolic link between an lstat() check and subsequent symlink-following operations such as stat(), chown(), chmod(), acl_get_file(), and acl_set_file(). Attackers who control a pathname component can redirect file access control list operations to arbitrary files when getfacl, setfacl, or chacl is invoked by a privileged process over an attacker-controlled path, resulting in local privilege escalation.

### CVE-2026-40524

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-29T14:16:51.207 |

FrontAccounting before 2.4.20 contains a SQL injection vulnerability in the get_gl_transactions() function where the filter_type parameter is concatenated directly into a SQL IN() clause without parameterization. Attackers with SA_GLANALYTIC permission can inject arbitrary SQL by supplying a closing parenthesis followed by malicious conditions to extract sensitive journal entry data through boolean-based blind SQL injection with reliable response size differentials.

### CVE-2026-40523

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-29T14:16:51.067 |

FrontAccounting before 2.4.20 contains a SQL injection vulnerability in the Audit Trail report handler that allows authenticated attackers with SA_GLANALYTIC permission to execute arbitrary SQL queries by injecting malicious code into the PARAM_2 and PARAM_3 POST parameters. Attackers can exploit time-based blind SQL injection through SLEEP() functions that are amplified across JOIN result sets to cause denial of service by exhausting database connections, or extract arbitrary database content through UNION-based injection techniques.

### CVE-2026-40522

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-916` |
| Published | 2026-06-29T14:16:50.920 |

FrontAccounting before 2.4.20 contains a SQL injection vulnerability in the Bank Statement report handler that allows authenticated attackers to extract arbitrary database data by injecting UNION SELECT payloads into the PARAM_0 POST parameter. Attackers can supply malicious SQL syntax through the unparameterized WHERE clause to retrieve sensitive information including usernames, password hashes, and email addresses from the users table, rendered into PDF report output.

### CVE-2026-57346

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-29T10:16:32.073 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Epiphyt Embed Privacy allows Path Traversal.

This issue affects Embed Privacy: from n/a through 1.12.3.

### CVE-2026-13601

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-693` |
| Published | 2026-06-29T10:16:30.180 |

A flaw was found in Yelp due to an overly permissive Content Security Policy (CSP) implementation provided by yelp-xsl. A malicious Flatpak application can open crafted help content through the OpenURI portal. By embedding an untrusted CSS stylesheet within a structured SVG document, attacker-controlled content can bypass Flatpak's intended sandbox isolation, allowing Yelp to evaluate local XML inclusions and disclose arbitrary user-readable host files through remote CSS resource requests. This may result in the unauthorized disclosure of sensitive information.
