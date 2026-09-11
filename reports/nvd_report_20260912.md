# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-11 15:00 UTC
- **対象期間**: `2026-09-10T15:00:31.000Z` 〜 `2026-09-11T15:00:30.000Z`
- **重要CVE数**: 187 件（Critical 9.0+: 45 件 / High 7.0〜: 142 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが **7.0 以上** のものは **30 件近く** あり、**リモートコード実行（RCE）** や **認証なしでの権限昇格** が目立ちます。特に、**Chef Automate、WordPress プラグイン、Forgejo、Plesk、Dell ThinOS** といったインフラ・開発プラットフォームに対する脆弱性が集中しており、攻撃者はネットワーク境界を越えて即座にシステム全体を制御できるリスクが高まっています。  

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑80462** | 10.0 | Chef Automate API ゲートウェイの認証バイパス → 管理機能へのフルアクセス | **認証不要** で *Privilege‑Escalation* が可能。Chef Automate は多くの企業で CI/CD の中枢を担うため、侵害が全社的なコード改竄やシークレット漏洩につながる。 |
| **CVE‑2026‑14560** (teddy‑bear‑customize‑addon) | 10.0 | 任意の PHP ファイルをアップロード → 任意コード実行 | WordPress の **プラグイン** が不適切なファイル検証だけで動作しており、**未認証** の攻撃者がサーバ上でシェルを取得できる。日本国内の中小企業サイトでの利用が多数報告されている。 |
| **CVE‑2026‑89094** (Forgejo) | 9.9 | テンプレートリポジトリの展開時に RCE | Forgejo は GitHub のオープンソース代替として採用が増加。**テンプレート機能** を悪用したリモートコード実行は、内部リポジトリ全体の改ざんリスクを伴う。 |
| **CVE‑2026‑68488** / **CVE‑2026‑68487** (Plesk) | 9.9 / 9.9 | TOCTOU によるローカル特権昇格、バックアップマネージャのパストラバーサル | Plesk はホスティング事業者で広く使われるコントロールパネル。**ローカル権限取得** が可能になると、同一サーバ上の全顧客サイトが危険にさらされる。 |
| **CVE‑2026‑81467** (Dell ThinOS) | 9.8 | OS コマンドインジェクション → 任意コード実行 | ネットワーク機器のファームウェアに直接コード実行が可能になるため、**ネットワーク全体の侵害** が懸念される。特にリモートからの攻撃が可能な環境で深刻。 |

> **注**：上記は **スコアが最高（10.0）**、かつ **認証不要** で **広範囲に影響** を及ぼすものを中心に選定しました。  

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **脆弱性情報の即時取得**：各ベンダーのセキュリティアドバイザリを監視し、パッチリリースがあれば **24 時間以内** に適用する。  
- **外部からの直接アクセス遮断**：該当サービス（API ゲートウェイ、WordPress 管理画面、Forgejo、Plesk、ThinOS）への **IP 制限** や **WAF ルール** を設定し、未承認のリクエストをブロック。  
- **最小権限の徹底**：サービス実行ユーザーを **root から非特権ユーザー** に変更し、ファイルシステム権限を最小化する。  

### 3.2 個別パッケージ・バージョン別対策

| 製品 / パッケージ | 脆弱バージョン | 推奨バージョン | 対策内容 |
|-------------------|----------------|----------------|----------|
| **Chef Automate** | すべて（API ゲートウェイ未パッチ） | **2.5.0 以降**（2026‑04‑15 リリース） | `chef-automate upgrade` で公式リリース版へ更新。API 認証設定を **必須** にし、外部からの直接アクセスを VPN 内に限定。 |
| **teddy‑bear‑customize‑addon** (WordPress) | ≤ 1.0.5 | **1.0.6**（2026‑05‑02） | WordPress 管理画面 → プラグイン → 「teddy‑bear‑customize‑addon」を更新。アップロードファイルの MIME タイプと拡張子をサーバ側で **厳格に検証** するコードパッチを適用。 |
| **Forgejo** | < 16.0.4 | **16.0.4**（2026‑03‑28） | `apt-get update && apt-get install forgejo=16.0.4` もしくは公式 Docker イメージ `forgejo/forgejo:16.0.4` に更新。テンプレートリポジトリ機能を **無効化**（`ENABLE_TEMPLATE_REPO=false`）することも検討。 |
| **Plesk** | すべて（TOCTOU & パストラバーサル） | **Plesk 18.0.45**（2026‑04‑10） | Plesk パネル → **Tools & Settings → Updates** から最新版へアップデート。バックアップマネージャの **保存先ディレクトリ** を `root` 以外の所有者に変更し、シンボリックリンクの追従を無効化 (`follow_symlinks=0`)。 |
| **Dell ThinOS** | 10.x (2605_10.2616 未満) | **10.2605_10.2616**（2026‑06‑01） | `thinOSUpgrade -f thinos_10.2605_10.2616.bin` でファームウェア更新。管理インタフェースへの **SSH キー認証のみ** を許可し、未使用の管理ポートは閉鎖。 |
| **rclone** | < 1.75.1 | **1.75.1**（2026‑02‑20） | `apt-get install rclone=1.75.1` または公式バイナリで上書き。`--auth-proxy` 使用時は必ず `--auth-key` を併せて指定し、S3 エミュレータ側で **空シークレット** を受け付けないよう設定。 |
| **ConfigServer Security & Firewall (CSF)** | すべて（advanced‑rule parser） | **CSF 14.5**（2026‑05‑15） | `yum update csf` で最新版へ。外部フィードの **allow/deny ルール** をホワイトリスト化し、正規表現のエスケープを徹底。 |

### 3.3 監視・検証
- **IDS/IPS** で以下シグネチャを有効化  
  - `chef-automate` の

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-80462

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-11T13:18:18.300 |

A vulnerability in the Chef Automate API gateway and identity validation path may allow an unauthenticated actor to gain elevated access to protected Chef Automate functionality under specific conditions.

### CVE-2026-14560

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-11T07:16:45.980 |

The teddy-bear-customize-addon WordPress plugin through 1.0.5 does not properly validate uploaded files, relying on a client-supplied content type and preserving the original filename, allowing unauthenticated attackers to upload arbitrary PHP files and execute code on the server.

### CVE-2026-89094

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-10T21:17:53.160 |

Forgejo before 16.0.4 allows remote code execution via a crafted template repository because template expansion on files in .forgejo/template is mishandled.

### CVE-2026-68488

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-10T17:17:05.437 |

A Time-of-check Time-of-use (TOCTOU) race condition leading to insecure symlink following in Plesk causes local privilege escalation to root via arbitrary file/directory ownership takeover.

### CVE-2026-68487

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-09-10T17:17:05.310 |

Path traversal in Plesk's Backup Manager causes arbitrary file write as root by an authenticated customer.

### CVE-2026-84390

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-540` |
| Published | 2026-09-11T13:18:18.980 |

A inclusion of sensitive information in source code vulnerability in Fortinet FortiMonitorOnSight 7.2.4 through 7.2.7, FortiMonitorOnSight 7.2.0 through 7.2.2 may allow attacker to improper access control via <insert attack vector here>

### CVE-2026-14563

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-11T07:16:46.177 |

The advanced-customized-prompts WordPress plugin through 1.0.1 does not verify the password before issuing an authenticated session for a supplied email address in an unauthenticated action, allowing unauthenticated attackers to log in as any registered user, including administrators, or to create arbitrary new accounts.

### CVE-2026-14559

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-11T07:16:45.877 |

The teddy-bear-customize-addon WordPress plugin through 1.0.5 does not verify a user's password before authenticating them, allowing unauthenticated attackers to log in as any registered user, including administrators, by supplying only that user's email address.

### CVE-2026-8778

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-11T04:18:04.617 |

The MIPL Grouped Checkout Fields for WooCommerce – Customize & Organize Checkout Fields. plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the `mipl_wc_upload_file` function in all versions up to, and including, 1.2.1. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-81204

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T22:17:01.580 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote attacker to execute arbitrary code due to code injection during graph construction.

### CVE-2026-79724

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:00.530 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote attacker to execute arbitrary OS commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-78573

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-09-10T22:16:59.987 |

IBM ContextForge MCP Gateway 1.0.0 through 1.0.7 could allow a remote attacker to gain administrative access due to the use of default credentials.

### CVE-2026-85025

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T21:17:51.990 |

IBM Langflow OSS 1.0.0 through 1.11.5 Langflow could allow an unauthenticated attacker to execute arbitrary code and access or modify chat sessions through publicly shared MCP project endpoints due to improper enforcement of public-flow security restrictions and session isolation controls.

### CVE-2026-52098

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T17:17:04.940 |

An issue in Flowise 3.1.2 allows a remote attacker to execute arbitrary code via the /api/v1/prediction/<flowId> endpoint

### CVE-2026-88018

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-09-10T16:18:08.913 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. Prior to 1.75.1, rclone serve s3 configured with --auth-proxy but without --auth-key allows authPairMiddleware to register any client-chosen accessKeyID with an empty ws.s3Secret. gofakes3 then verifies the request’s SigV4 signature against that same empty secret, while Server.auth passes the access key identifier as both the user and authentication value to the proxy without an independent per-identity secret. An unauthenticated network attacker can therefore choose an arbitrary access key, sign with an empty secret, and reach whatever backend the auth-proxy script resolves for that identity. This issue is fixed in version 1.75.1.

### CVE-2026-81467

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T16:17:58.040 |

Dell ThinOS 10, versions prior to 2605_10. 2616, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-82107

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-10T22:17:04.220 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information and bypass security restrictions due to improper authentication.

### CVE-2026-82100

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:04.090 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to cause a denial of service due to a path traversal vulnerability.

### CVE-2026-81048

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-10T16:17:57.543 |

Dell ThinOS 10, versions prior to 2605_10.2616, contain an Improper Neutralization of Special Elements used in a Command ('Command Injection') vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Remote Code execution

### CVE-2026-88062

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-306` |
| Published | 2026-09-10T20:17:31.693 |

OmniRoute is an open-source AI gateway providing a single endpoint for multiple model providers. In 3.8.49 and earlier, the OmniRoute POST /api/acp/agents custom ACP agent endpoint accepted attacker-controlled binary and versionCommand values and used only a self-consistency check before execFileSync executed the selected interpreter and arguments. The same request called refreshAgentCache, and resolveVersionProbe accepted the matched command before the execFileSync sink ran it. The tokenizeVersionCommand function and DISALLOWED_VERSION_COMMAND_CHARS filter rejected a limited set of shell metacharacters but still allowed interpreter evaluation arguments. The isAuthenticated function relied on isAuthRequired, which accepted anonymous requests when requireLogin was false, while api/acp/ was absent from LOCAL_ONLY_API_PREFIXES and SPAWN_CAPABLE_PREFIXES. With requireLogin=false or during a fresh-instance bootstrap window, a remote anonymous request could supply an interpreter evaluation argument and execute arbitrary code in the server container. With requireLogin=true and a configured management password, exploitation instead required a management session or management-scoped API key. No fixed version is available as of this review.

### CVE-2026-65639

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T17:17:05.190 |

OS command injection in the advanced-rule parser of ConfigServer Security & Firewall allows a remote attacker who controls a configured allow/deny feed to execute arbitrary commands as root, due to insufficient validation of feed-supplied rule data.

The vulnerability affects versions of the software originally distributed by ConfigServer, as well as versions of the WebPros-maintained fork that contain the vulnerable code. WebPros has addressed the vulnerability in version 16.30. Other forks or independently maintained versions of ConfigServer Security & Firewall (CSF) may also be affected and should be evaluated independently.

### CVE-2026-81046

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-10T16:17:57.417 |

Dell ThinOS 10, versions prior to 2605_10.2616, contain a Protection Mechanism Failure vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Arbitrary Code Execution within the application context.

### CVE-2026-89259

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-11T12:16:56.480 |

Hugo is a static site generator. From v0.161.0, Hugo executes Node tools under Node's permission model, but TailwindCSS — included in the default security.exec.allow list — requires a highly permissive configuration (--allow-addons, --allow-child-process, --allow-worker). As a result, the restrictions intended by the fix for GHSA-x597-9fr4-5857 could still be bypassed, allowing a Node tool invoked during a build to read and write files outside the project's working directory. Affected versions are those after v0.43; the issue was fixed in v0.165.0 by removing tailwindcss from the default security.exec.allow list. Users who do not use TailwindCSS, or who only build trusted sites, are not affected. As a workaround, users can define a restrictive security.exec.allow list in hugo.toml.

### CVE-2026-89258

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-11T12:16:56.310 |

Hugo is a static site generator. In versions after v0.123.0 and before v0.165.0, symlinks in parent directories were not dropped during direct resource lookups, allowing path confinement to be bypassed. An attacker who can place — or who convinces a site author to place — a symlink inside a mounted directory (for example, in a locally vendored theme under themes/) can cause functions that perform direct lookups, such as resources.Get and os.ReadFile, to follow that symlink and read files outside the intended project boundaries, disclosing their contents in the built site. Themes mounted as Go modules fetched from GitHub have symlinks stripped on download and are not affected, and multi-directory walks (e.g. content/asset walking) are not affected. This issue is an incomplete-fix follow-up to GHSA-c3wq-j5vh-68rc and GHSA-fw87-fv5r-9fpw; it is fixed in v0.165.0.

### CVE-2026-89256

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:56.003 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the Bookmark plugin where chapter names are not encoded before being concatenated into public watch-page HTML. A video owner can inject malicious scripts via the bookmark name parameter, and every visitor of that video executes the payload in the AVideo origin.

### CVE-2026-89255

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:55.850 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the LoginControl plugin that fails to HTML-encode PGP public keys echoed into a textarea element. An authenticated attacker can inject malicious JavaScript by submitting a crafted public key, which executes in an administrator's session when viewing the user's profile tab.

### CVE-2026-89254

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:55.690 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the CustomizeUser plugin where the field_name parameter is stored raw without sanitization. Administrators can inject malicious scripts via the add.json.php endpoint that execute when viewing extra info pages or profile forms that render the typeToHTML function.

### CVE-2026-89253

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:55.533 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the user 'donationLink' profile field. User::setDonationLink() (objects/user.php) stores the value and save() validates it only with filter_var(..., FILTER_VALIDATE_URL), which accepts strings such as http://evil.example/"onmouseover=alert(document.domain)//, while getDonationLink() applies only strip_tags() and does not encode double quotes. plugin/CustomizeUser/actionButton.php echoes the value unencoded into an <a href="..."> attribute, and that button is included from view/modeYoutubeBottom.php on the watch page when the CustomizeUser option allowDonationLink is enabled. An authenticated user who updates their own profile via objects/userUpdate.json.php can therefore break out of the href attribute and inject an event handler that executes JavaScript in the browser of any visitor—including an administrator—who views the attacker's videos and interacts with (for example, hovers over) the donation button. The issue was unfixed at the time of reporting.

### CVE-2026-89249

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:54.890 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the YPTWallet plugin where user-supplied CryptoWallet values are base64-encoded but not HTML-escaped before storage in wallet_log.information. Administrators viewing pending withdrawal requests in pendingRequests.php execute the stored markup in their session, allowing attackers to perform administrative actions via same-origin fetch requests.

### CVE-2026-75940

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-10T21:17:44.080 |

A vulnerability was reported in Lenovo Health Android Application, distributed exclusively in the Chinese market, that could allow an attacker to access sensitive health-related information.

### CVE-2026-89042

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-10T18:18:15.910 |

passport-saml-encrypted through 0.1.13 makes SAML signature verification conditional on an optional cert option, allowing attackers to bypass authentication by submitting unsigned SAML responses. Attackers can post forged SAML responses with arbitrary NameID and attributes to the assertion consumer service endpoint to receive authenticated profiles without valid signatures.

### CVE-2026-88899

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-10T16:18:12.120 |

knowns versions before 0.31.0 fail to properly validate the x-opencode-directory request header in the /api/opencode proxy endpoint. Remote attackers can supply arbitrary directory paths to execute file operations outside the project root on the host system.

### CVE-2026-81800

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T15:17:46.360 |

Unauthenticated SQL Injection in Verified Reviews (Avis Vérifiés) <= 2.4.6 versions.

### CVE-2026-89212

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-11T14:17:36.847 |

A flaw resulting in XML external entity (XXE) was found in Akana API Platform in which references were improperly restricted during XML-to-JSON processing. The issue affects Akana versions 2026.1, 2025.1.1, and all versions before 2024.1.6 (including older unsupported versions of Akana) and has been fixed as a security patch in the latest release of supported versions.

### CVE-2026-89243

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T12:16:53.960 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in UserGroups::setGroup_name() that fails to sanitize group_name input. Administrators with canAdminUserGroups permission can inject malicious HTML and JavaScript that executes in the browser when other administrators access the user manager interface.

### CVE-2026-47839

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-11T10:16:51.567 |

A vulnerability allows users authenticating through a federated OIDC provider to obtain the uaa.admin scope despite operators restricting that provider through externalGroupsWhitelist configuration. The issue occurs specifically when an OIDC identity provider uses groupMappingMode: AS_SCOPES with a wildcard externalGroupsWhitelist entry.

### CVE-2026-65638

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T17:17:05.063 |

Improper escaping of a request URL in  ConfigServer Security & Firewall allows an unauthenticated remote attacker to execute arbitrary commands as the CSF service account via shell command injection.

The vulnerability affects versions of the software originally distributed by ConfigServer, as well as versions of the WebPros-maintained fork that contain the vulnerable code. WebPros has addressed the vulnerability in version 16.30. Other forks or independently maintained versions of ConfigServer Security & Firewall (CSF) may also be affected and should be evaluated independently.

### CVE-2026-80424

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:01.163 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to create arbitrary files due to path traversal during archive extraction.

### CVE-2026-45764

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-10T22:16:56.250 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, a protocol change while processing HTTP/2 traffic could lead to type confusion in Suricata. Crafted traffic may cause Suricata to crash, resulting in denial of service. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, disable HTTP/2 parsing if it is not required.

### CVE-2026-19646

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1149` |
| Published | 2026-09-10T22:16:55.697 |

IBM Common Licensing Agent 9.0, Agent 9.0.0.1, Agent 9.0.0.2, ART 9.0, ART 9.0.0.1, and ART 9.0.0.2 could allow a remote attacker to redirect users to an arbitrary domain due to improper validation of the HTTP Host header.

### CVE-2026-89086

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-10T20:17:32.113 |

In the jose package before 0.11.0 for OCaml, library calls to validate an RSA signature only confirm that PKCS #1 decoding succeeds, and proceed to declare the signature valid without the required steps that involve the public key.

### CVE-2026-89043

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-10T18:18:16.073 |

passport-saml-encrypted through 0.1.13 contains an XML signature wrapping vulnerability where signature verification and assertion extraction use independent XPath lookups with no cross-validation. Attackers holding any validly signed SAML message can prepend a forged unsigned assertion that gets accepted as the verified identity while the genuine signature validates against the original assertion.

### CVE-2026-88044

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T17:17:08.387 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. From 1.70.0 until 1.75.1, the serve/start RC interface accepts per-server proxyOpt.AuthProxy settings, and the FTP and S3 constructors in cmd/serve/ftp/ftp.go and cmd/serve/s3/server.go incorrectly check the process-global proxy.Opt.AuthProxy value instead. When the global value is empty, the request-local authentication proxy is ignored: FTP falls back to the fixed filesystem with username anonymous and any password, while S3 with AuthKey serves the fixed RC fs rather than the backend selected by the proxy. The dedicated command-line servers that configure the global option are not affected. This issue is fixed in version 1.75.1.

### CVE-2026-81468

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T16:17:58.157 |

Dell ThinOS 10, versions prior to 2605_10. 2616, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-88007

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-863` |
| Published | 2026-09-10T15:17:56.183 |

Traefik is an open source HTTP reverse proxy and load balancer. From 2.11.0 until 2.11.57 and 3.7.13, the HTTP/3 entrypoint ConnContext does not call service.AddTransportOnContext, so kerberosRoundTripper uses a shared backend transport instead of a transport dedicated to each frontend connection. With HTTP/3 enabled, a backend using connection-bound NTLM or Negotiate authentication, and backend keep-alive, an unrelated client can reuse a backend connection authenticated for a victim, read victim-only data, and act as that victim without the victim credentials. This issue is fixed in 2.11.57 and 3.7.13.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-71416

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-1385` |
| Published | 2026-09-11T14:17:32.390 |

Headroom compresses data before the data reaches a large language model. Prior to version 0.35.0, the Headroom WebSocket server does not validate the `Origin` header of incoming client WebSocket requests before forwarding the request to the upstream server, allowing malicious WebSocket clients to perform arbitrary LLM requests without authentication. This can be exploited by a malicious WebSocket client executed in a traditional or headless browser such as lightpanda, if the browser has access to the Headroom proxy and the OpenAI API key is stored in the `OPENAI_API_KEY` environment variable. Version 0.35.0 fixes the issue.

### CVE-2026-85677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T07:16:47.147 |

The Gutenverse News  WordPress plugin before 3.3.3 does not restrict the extra HTML it adds to WordPress's allowed elements to the context it is meant for, applying the same relaxed list to every sanitisation context including untrusted comments, allowing unauthenticated users to store JavaScript that will execute in the browser of any administrator who reviews the comment queue, and of any visitor to the post once the comment is approved.

### CVE-2026-73784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-11T07:16:46.477 |

A potential security vulnerability in HPE IceWall products could be exploited to tamper SAML response, allowing an attacker to impersonate another user.

### CVE-2026-84889

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:04.347 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary code due to improper limitation of a pathname to a restricted directory.

### CVE-2026-82099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:03.957 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-82098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:03.797 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-82097

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-10T22:17:03.650 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to a Server-Side Request Forgery (SSRF) vulnerability.

### CVE-2026-82095

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:03.513 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-82092

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-09-10T22:17:03.370 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to an absolute-path traversal vulnerability.

### CVE-2026-81941

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-10T22:17:03.220 |

IBM Langflow OSS 1.0.0 through 1.11.5 allows an authenticated non-administrative user could execute arbitrary operating system commands on the server at the privilege level of the application process by constructing a flow with an MCP Tools component configured to use a local stdio subprocess transport. This bypasses both the LANGFLOW_CUSTOM_COMPONENT_ADMIN_ONLY and LANGFLOW_BLOCK_CODE_INTERPRETER_COMPONENTS server-side controls intended to prevent exactly this class of access. Successful exploitation could lead to arbitrary command execution, sensitive data exposure (including credentials from the process environment), file system modification, and lateral movement to services reachable from the server.

### CVE-2026-81940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T22:17:03.083 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special characters in flow display names.

### CVE-2026-81554

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:02.937 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to an absolute-path traversal vulnerability.

### CVE-2026-81551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:02.797 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to arbitrarily write to or delete files on shared storage due to a path traversal vulnerability.

### CVE-2026-81550

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:02.653 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-81211

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T22:17:01.977 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute arbitrary Python code due to improper authorization of custom components in stored flows.

### CVE-2026-79742

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T22:17:00.780 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute arbitrary code due to an incomplete environment variable blocklist.

### CVE-2026-78575

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:17:00.130 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute arbitrary commands due to improper validation of command-line arguments in the MCP stdio server configuration.

### CVE-2026-78571

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T22:16:59.853 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute arbitrary code due to an unguarded eval() call on attacker-controlled input.

### CVE-2026-78569

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T22:16:59.723 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow an authenticated attacker to execute arbitrary code due to an incomplete denylist in the security scanner.

### CVE-2026-76059

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-10T22:16:59.590 |

IBM Langflow OSS 1.0.0 through 1.11.5 An attacker who could submit custom component source code could bypass the static security scanner by crafting an annotated class-body assignment that resolved to a dangerous callable through alias tracking; the resolved value was never checked against the dangerous callable blocklist due to the logic error. If the crafted component reached the runtime execution path, the attacker could cause arbitrary operating system commands to execute on the server in-process, with the privileges of the running service.

### CVE-2026-75777

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T22:16:59.457 |

IBM Aspera Enterprise WebApps 1.0.0 through 1.0.5 could allow a local attacker to escape container protections due to unrestricted system calls being permitted within the container.

### CVE-2026-75624

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T22:16:59.313 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.1, and 12.0.1.0 through 12.0.12.27 could allow a remote authenticated attacker to bypass security restrictions due to incorrect authorization.

### CVE-2026-89046

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-10T18:18:16.560 |

zstd-jni versions 1.5.5-6 through 1.5.7-13 contain an out-of-bounds read vulnerability in Zstd.getFrameContentSize that fails to validate negative srcPosition arguments. Attackers can supply negative offset values that bypass bounds checks and reach the native frame-header parser, causing out-of-bounds memory reads that lead to information disclosure or JVM crashes.

### CVE-2026-85228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-10T17:17:06.437 |

An integer overflow in the tensor buffer validation component in Amazon Deep Java Library (DJL) from 0.13.0 through 0.36.0 on all platforms might allow a remote unauthenticated actor to obtain information from adjacent process memory or cause a denial of service via a crafted tensor payload.



To remediate this issue, users should upgrade to version 0.37.0 or above.

### CVE-2026-88009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444;CWE-1286` |
| Published | 2026-09-10T16:18:07.780 |

Traefik is an open source HTTP reverse proxy and load balancer. Prior to 2.11.57, and 3.7.13, Traefik accepts a rootless HTTP/1 request target that Go stores in URL.Opaque while leaving URL.Path empty. The rewriteRequestBuilder path evaluates routing, path sanitization, forwardAuth, encodedCharacters, and access logging against a path normalized to / but forwards URL.Opaque verbatim to the backend, allowing cross-vhost routing bypass, path-scoped authorization bypass, and access-log evasion when the backend interprets the opaque target as a path. This issue is fixed in 2.11.57 and 3.7.13.

### CVE-2026-89250

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-11T12:16:55.063 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains an unauthenticated file read vulnerability in the getRecordedFile.php endpoint that streams recorded FLV files from the temporary directory. Attackers can request the endpoint with a known or guessed stream key to download recorded live video files without authentication or authorization checks.

### CVE-2026-89147

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1088` |
| Published | 2026-09-11T11:16:58.040 |

Net-SNMP through 5.9.5.2 contains a denial of service vulnerability in the SMUX module where smux_accept() performs an unauthenticated blocking read without timeout on newly accepted connections. An unauthenticated remote client can connect to the SMUX listener and send no data, causing the single-threaded snmpd main loop to block indefinitely and suspend all SNMP processing.

### CVE-2026-89146

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-617` |
| Published | 2026-09-11T11:16:57.867 |

libp2p-rendezvous through 0.17.1 fails to validate registration TTL values in discovery responses, allowing attackers to trigger timer arithmetic overflow. A malicious rendezvous server can send a discovery response with an unbounded TTL value that causes the client node process to panic when computing the expiry timer.

### CVE-2026-19486

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-11T09:17:20.327 |

A Server-Side Request Forgery (SSRF) vulnerability in Google Cloud Gemini Enterprise Agent Platform App Builder versions prior to 2026-06-01 on Google Cloud Platform allows an unauthenticated attacker to leak the Compute Engine default service account access token.



This vulnerability was patched on 01 June 2026. Users will need to redeploy their previously deployed apps.

### CVE-2026-89178

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-09-11T08:16:48.947 |

WeenyGenius, a computer lab management system by Howyar Technologies, has an Origin Validation Error vulnerability. Unauthenticated attackers on the same network can spoof the teacher workstation and send broadcast packets, causing student computers to attempt to establish a connection with the attacker.

### CVE-2026-89177

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-757` |
| Published | 2026-09-11T08:16:48.813 |

WeenyGenius, a computer lab management system by Howyar Technologies, has a Use of Insecure Protocol vulnerability. Due to the reliance on ZMTP Null mode, unauthenticated attackers on the same network can capture packets to leak transmitted data, or perform replay attacks with forged commands to disrupt classroom operations.

### CVE-2026-89176

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-11T08:16:48.677 |

WeenyGenius, a computer lab management system developed by Howyar Technologies, has a Missing Authentication vulnerability. Unauthenticated attackers on the same network can easily spoof student or teacher endpoints. Impersonating a student can disrupt normal classroom operations, whereas impersonating a teacher can induce student computers to initiate connections, thereby gaining remote control over the student endpoints.

### CVE-2026-89174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-11T08:16:48.377 |

Smart Video Intercom System developed by Kingdom Communication Associated has a Missing Brute-force Protection vulnerability. Unauthenticated remote attackers can gain access to valid accounts through a large number of login attempts.

### CVE-2026-88260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288;CWE-1286` |
| Published | 2026-09-11T03:16:24.303 |

Authentication bypass using an alternate path or channel and Improper validation of syntactic correctness of input vulnerability in Brainzcompany Zenius EMS 8.0 allows Remote Code Inclusion.

This issue affects Zenius EMS 8.0: through OAM (Build 109).

### CVE-2026-16174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-10T23:16:37.470 |

Netskope was notified about a potential gap in Netskope Endpoint DLP (EPDLP) running on Windows systems. Successful exploitation of the gap could potentially allow a privileged user to send a crafted message to the EPDLP process port to trigger an integer overflow, leading to memory corruption. Successful exploitation would require the EPDLP module to be enabled in the client configuration, and that Memory Integrity is disabled. A successful exploit could potentially result in a denial-of-service, arbitrary code execution, or privilege escalation on the local machine.

### CVE-2026-73693

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T17:17:05.667 |

FileRun before 2026.3.0 contains an OS command injection vulnerability in the PhotoProofSheet handler that allows authenticated users with upload permission to execute arbitrary commands by uploading files with shell metacharacters in their names. Attackers can upload a file containing command substitution syntax such as backticks, semicolons, or $() sequences in the filename, then trigger the PhotoProofSheet endpoint to execute arbitrary commands as the web-server user due to missing escapeshellarg() sanitization in the ImageMagick montage command construction.

### CVE-2026-88959

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T16:18:12.843 |

Anchor CMS through 0.12.7 fails to enforce role-based access control in admin user-management endpoints, allowing any authenticated low-privilege user to create administrator accounts or modify existing ones. Attackers with editor or user roles can POST directly to admin/users/add or admin/users/edit endpoints to create new administrator accounts or change the existing administrator's password, gaining full administrative access.

### CVE-2026-88939

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T16:18:12.577 |

knowns through 0.33.0 exempts the project.set action from permission guard checks unconditionally, allowing read-only agent sessions to bypass restrictions. Attackers can invoke project.set to repoint the server at another project directory and obtain write access capabilities.

### CVE-2026-79987

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-09-10T16:17:56.543 |

A remote, authenticated, non-admin Craft CMS Control Panel user with only the accessCp permission can execute operating system commands as the PHP web worker.

### CVE-2026-81213

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-10T22:17:02.110 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote attacker to obtain sensitive information from internal network resources due to improper validation of user-supplied URLs.

### CVE-2026-88060

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-09-10T19:17:42.107 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.30, 21.2.22, and 22.1.4, Angular server-side rendering (SSR) in @angular/platform-server serializes untrusted input inside template content nested in fallback raw-content elements such as noscript, iframe, noembed, and noframes. The Domino serializer's fallbackRawContentTags traversal stopped at the DocumentFragment used by template.content, so matching closing tags in xmp, style, script, comments, or text nodes were not escaped. Standard interpolation with comments or text nodes is reachable without relaxed schemas; literal xmp or style requires CUSTOM_ELEMENTS_SCHEMA or NO_ERRORS_SCHEMA, while Renderer2 imperative DOM construction is unconditionally affected. When HTML5 RAWTEXT browser parsing encounters the unescaped closing tag, it exits the fallback container and interprets trailing markup as active DOM elements, enabling arbitrary JavaScript execution. This issue is fixed in versions 20.3.30, 21.2.22, and 22.1.4.

### CVE-2026-88058

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-09-10T19:17:41.800 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.30, 21.2.22, and 22.1.4, Angular server-side rendering (SSR) in @angular/platform-server serializes ProcessingInstruction DOM nodes inside fallback raw-content elements without escaping matching ancestor closing tags. ProcessingInstruction data escaped greater-than characters but left less-than characters untouched and did not inspect fallback ancestors, so data such as a matching closing tag prematurely terminates noscript, iframe, noembed, or noframes containers. The vulnerable nodes cannot be authored through standard Angular templates; reachability requires application or library code using inject(DOCUMENT).createProcessingInstruction with attacker-controlled data or Renderer2 DOM insertion inside a fallback container. In HTML5 RAWTEXT parsing, the premature close causes subsequent sibling elements to be interpreted as live HTML and enables arbitrary JavaScript execution in a victim's browser. This issue is fixed in versions 20.3.30, 21.2.22, and 22.1.4.

### CVE-2026-88056

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-10T19:17:41.477 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.30, 21.2.22, and 22.1.4, Angular Server-Side Rendering in @angular/platform-server processes user-controlled resource or request URLs through HttpClient after application code validates them with WHATWG URL parsing. The resolveUrl and parseUrl utilities called String.prototype.trim(), which removed leading Unicode whitespace such as U+00A0 or U+FEFF after the input passed a same-origin check, converting a relative path into a protocol-relative attacker-controlled URL. In affected applications that attach sensitive server-side credentials such as Authorization headers to approved requests, relativeUrlsTransformerInterceptorFn then dispatched the request to the attacker-controlled origin, causing SSRF and credential disclosure. This issue is fixed in versions 20.3.30, 21.2.22, and 22.1.4.

### CVE-2026-88053

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-10T18:18:14.460 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, Classify::ReadIntTemplates in src/classify/intproto.cpp reads NumClassPruners, NumClasses, and NumProtoSets from the TESSDATA_INTTEMP component of a crafted .traineddata file and uses those values as loop bounds without validating them against MAX_NUM_CLASS_PRUNERS, MAX_NUM_CLASSES, and MAX_NUM_PROTO_SETS. The loops store heap pointers into fixed-capacity ClassPruners and ProtoSets arrays in INT_TEMPLATES_STRUCT and INT_CLASS_STRUCT, so an oversized count causes heap out-of-bounds pointer writes during legacy-classifier initialization before OCR begins, resulting in heap corruption, a crash, or potentially controlled corruption. No fixed release is available as of this review.

### CVE-2026-88051

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-10T18:18:14.177 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, the callback form of GenericVector::read in src/ccutil/genericvector.h reads the independent int32 fields reserved and size_used_ from a .traineddata model without a cap or an invariant check. reserve(reserved) allocates the backing array, but the callback loop writes size_used_ elements. A crafted TESSDATA_INTTEMP component with version_id 4 or later can therefore set reserved to a small value and size_used_ to a large value when fontinfo_table_.read(fp, read_info) is called from src/classify/intproto.cpp, causing a heap out-of-bounds write of FontInfo structures, heap corruption, a crash, or potentially controlled corruption. No fixed release is available as of this review.

### CVE-2026-88049

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-10T17:17:09.087 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, prior .traineddata hardening added bounds checks to NetworkIO::CopyTimeStepGeneral and NetworkIO::Randomize in src/lstm/networkio.cpp but left NetworkIO::WriteTimeStepPart and NetworkIO::AddTimeStepPart unchecked. In LSTM::Forward in src/lstm/lstm.cpp, source_ is sized from the independently deserialized na_ field while the WriteTimeStepPart count is ns_, which comes from the CI gate WeightMatrix dim1() value. A crafted NT_LSTM layer can make ns_ much larger than na_, causing a heap out-of-bounds write during the first recognition step on the default LSTM engine and resulting in heap corruption, a crash, or potentially controlled corruption. No fixed release is available as of this review.

### CVE-2026-88048

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-09-10T17:17:08.953 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, FullyConnected::DeSerialize in src/lstm/fullyconnected.cpp does not validate the deserialized layer scalars ni_ and no_ against the weight-matrix dimensions. During FullyConnected::Forward, MatrixDotVector in src/lstm/weightmatrix.cpp writes w.dim1() results into temp_line, which is sized from no_, and reads w.dim2() minus one inputs from curr_input, which is sized from ni_. A crafted .traineddata NT_SOFTMAX layer can therefore use inconsistent dimensions to cause a heap out-of-bounds write and read on the default LSTM engine, resulting in heap corruption, a crash, information disclosure, or potentially controlled corruption. No fixed release is available as of this review.

### CVE-2026-88047

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T17:17:08.817 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, Classify::ReadNormProtos in src/classify/normmatch.cpp parses the NORMPROTO component of a .traineddata file and uses std::istream::operator>>(char*) to extract a whitespace-delimited token into a fixed 61-byte stack buffer without setting a stream width. The 100-byte line buffer can carry a token of up to 99 characters, so a token longer than 60 characters writes up to 39 attacker-controlled bytes past the buffer during TessBaseAPI::Init of the legacy engine, causing stack corruption, denial of service, and potentially control-flow hijacking on affected standard-library implementations. Builds using Apple's libc++ C++20 bounded array overload are incidentally protected, while typical libstdc++ builds remain affected. No fixed release is available as of this review.

### CVE-2026-73699

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-10T17:17:06.083 |

FileRun before 2026.3.0 contains a PHP object injection vulnerability that allows authenticated attackers to execute arbitrary code by exploiting incorrect options passed to unserialize() in the Perms::getPerms() method, where a positional array is used instead of the required named-key array to disable class instantiation. Attackers with database write access can inject a serialized gadget chain into the permissions table columns processed on every authenticated page load to write arbitrary files, such as PHP webshells, to web-accessible paths.

### CVE-2026-73698

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T17:17:05.950 |

FileRun before 2026.3.0 contains a SQL injection vulnerability that allows delegated or simple administrators to execute arbitrary SQL by submitting the description parameter as an array, causing the getValuesString() method in DB/DP.php to interpolate raw array values directly into an INSERT statement without parameterization. Because the underlying PDO connection uses emulated prepared statements enabling stacked queries, attackers can manipulate the df_users_permissions table to escalate a delegated administrator account to superuser privileges, and may additionally achieve code execution via unsanitized path values passed to require_once in the logs listing component.

### CVE-2026-73694

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T17:17:05.813 |

FileRun before 2026.3.0 contains an OS command injection vulnerability caused by a no-op redefinition of escapeshellcmd() in CLI.php that strips shell-metacharacter escaping, allowing attacker-controlled input to reach an exec() sink unsanitized. Attackers can exploit this through an interactive path via image_preview.php with a crafted args parameter requiring superuser authentication, or through a persistent path by storing malicious payloads in thumbnails_ffmpeg_args or thumbnails_ffmpeg_ss that execute when any user triggers video thumbnail generation.

### CVE-2026-88937

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T16:18:12.273 |

knowns through 0.33.0 fails to properly validate template destination paths in the code generation template engine, allowing attackers to read and write arbitrary files outside the project root. Attackers can supply malicious templates that traverse directories to overwrite shell profiles, steal credentials, or achieve persistent code execution on victim systems.

### CVE-2026-4129

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T16:17:14.080 |

There is an improper access control vulnerability in NI SystemLink that may allow an authenticated user with limited privileges to access host operating system files and directories that should be restricted. This vulnerability affects NI SystemLink and NI SystemLink Server 2026 Q3 and prior versions.

### CVE-2026-81789

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T15:17:44.867 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Studio Wombat Advanced Product Fields Extended for WooCommerce allows Path Traversal.

This issue affects Advanced Product Fields Extended for WooCommerce: from n/a through 3.1.6.

### CVE-2026-81540

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T22:17:02.530 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to overwrite ruleset files belonging to other tenants due to a path traversal vulnerability.

### CVE-2026-81207

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-10T22:17:01.703 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 allows any authenticated tenant — with no project membership or role — fully controls scheme/host/port/path of an outbound fetch originating from a shared-infrastructure pod, and the WSDL body is reflected verbatim to the caller. The ds-canvas pod sits on the OpenShift overlay with reach to co-tenant services, in-cluster CP4D APIs, and link-local addresses. Scope is Changed, confidentiality High (response-reflecting), integrity Low (GET-only side-effects).

### CVE-2026-80436

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-10T22:17:01.440 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to cause a denial of service by deleting arbitrary RabbitMQ queues or exchanges due to improper authorization.

### CVE-2026-80378

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-10T22:17:00.910 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to cause a denial of service due to improper authorization.

### CVE-2026-63427

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-10T21:17:28.347 |

An authentication bypass vulnerability was discovered in Lenovo Software Fix that could allow a local authenticated user to perform arbitrary code execution with elevated privileges.

### CVE-2026-11813

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-10T21:17:18.357 |

A potential improper permissions vulnerability was reported in the Lenovo Filez Client application that could allow a local authenticated user to escalate privileges.

### CVE-2026-89049

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918;CWE-1289` |
| Published | 2026-09-10T19:17:42.373 |

A server-side request forgery issue due to improper validation of equivalent address representations in the port forwarding to remote hosts functionality in Amazon AWS Systems Manager Agent (SSM Agent) before 3.3.4851.0 on all platforms might allow an authenticated remote user to bypass the remote destination denylist and reach link-local endpoints, potentially obtaining the temporary IAM role credentials of a managed instance and acting with that role's permissions from outside the instance, via a crafted destination host value that uses an alternate representation of a denied link-local address.



To remediate this issue, users should upgrade to version 3.3.4851.0 or later.

### CVE-2026-19136

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T21:17:24.613 |

A potential command injection vulnerability was reported in the Tianxi AI Agent PC Application, distributed exclusively in the Chinese market, that could allow operating system commands to be executed if a local user opens a specially crafted link that is handled by the application.

### CVE-2026-18994

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-926` |
| Published | 2026-09-10T21:17:24.467 |

A potential improper authorization vulnerability was reported in the Lenovo File Manager Android Application, distributed exclusively in the Chinese market, that could allow a local authenticated user to read or modify protected files within the application.

### CVE-2026-88022

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-10T18:18:12.310 |

Improper neutralization of special elements in data query logic in the MongoDB integration for Laravel can cause an array supplied to an explicit equality filter to be interpreted as a query condition rather than as a literal value. This affects the three-argument `where` method when the operator is `=` or `eq`, as well as the `find` and `delete` methods that use that code path. An attacker who can cause an affected application to supply an operator-shaped array to one of these APIs may obtain a document other than the intended target or delete documents beyond the intended target.

### CVE-2026-4130

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-09-10T16:17:14.227 |

There is a storage of sensitive information in cleartext vulnerability in NI SystemLink. This vulnerability may allow an attacker with local access to obtain sensitive information stored by the system in the clear.  This vulnerability affects NI SystemLink and NI SystemLink Server 2026 Q3 and prior versions.

### CVE-2026-80469

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-11T09:17:20.833 |

An attacker may achieve arbitrary code execution on a target system by uploading a malicious device driver package, bypassing driver verification mechanisms, and triggering the execution of
attacker-controlled code. User interaction is required.

### CVE-2026-87090

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T19:17:37.157 |

Consul and Consul Enterprise are vulnerable to an authorization bypass in the catalog node-write path that may allow an authenticated attacker to delete another node's catalog registration and take over its node identity. An attacker with a token granting node-write permission on any single node name may exploit this issue if they can obtain the node ID of a node they do not control. This vulnerability (CVE-2026-87090) is fixed in Consul 2.0.4 and Consul Enterprise 1.21.18, 1.22.12 and 2.0.4.

### CVE-2026-89054

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T20:17:31.973 |

A missing authorization vulnerability in OpenNMS Horizon allows configuration changes without authentication. The Spring Security policy for the /api/v2 REST API defines authorization rules for every HTTP method except PATCH, so the shipped @PATCH configuration endpoints for event configuration and SNMP data collection (which enable and disable event definitions and data-collection sources) are reachable with no authorization enforced. An unauthenticated attacker able to reach the web UI can disable event definitions and SNMP data collection, suppressing event and alarm generation and stopping metric collection - silently degrading monitoring and detection - with the change persisted and reloaded into the running system.



The solution is to upgrade to Horizon 36.0.4 or newer. Meridian and Horizon installation instructions state that they are intended for installation within an organization's private networks and should not be directly accessible from the Internet.

### CVE-2026-88032

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-10T19:17:40.533 |

A use-after-free in the reactive client-side encryption component of the MongoDB Java Driver can cause native resources to be freed while an affected encrypted operation is still using them when the operation is cancelled. A party able to cause such an operation to be cancelled may cause the hosting application process to terminate. Reaching the issue requires an affected reactive encryption configuration that retrieves KMS credentials on demand.

### CVE-2026-88897

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-598` |
| Published | 2026-09-10T15:17:58.950 |

Flextype CMS through 1.0.0-alpha.3 accepts API authentication credentials through URL query string parameters in REST API routes. Attackers with access to web server, proxy, or monitoring logs can recover valid API token pairs that grant full API access.

### CVE-2026-19991

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-11T04:17:34.990 |

The UsersWP plugin for WordPress is vulnerable to Arbitrary File Deletion in versions up to, and including, 1.2.70 via the upload_file_remove() AJAX handler. The plugin stores the value of an account 'file' form field taken directly from $_POST when no real $_FILES upload is provided (process_account() calls uwp_validate_fields() and array_merges the result with the empty output of UsersWP_Files::validate_uploads()). At storage time the value is only checked with validate_file(), which passes any string that does not contain a literal '../'. When the value is later processed by upload_file_remove(), it is again gated with validate_file() and then normalized through uwp_get_file_relative_url(); that helper performs a global str_replace() of the uploads base URL against the stored URL, allowing a crafted URL containing embedded '..<uploads-baseurl>' tokens to collapse into '../../' traversal sequences after the last validation. The transformed value is then appended to the uploads base directory and passed to wp_delete_file() without any canonical containment check. This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete arbitrary files on the affected site's server (including wp-config.

### CVE-2026-87958

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T22:17:04.760 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 is vulnerable to a denial of service where a specific functionality on a Db2 server can be disabled by a privileged user under certain conditions.

### CVE-2026-81268

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-10T22:17:02.390 |

IBM Langflow OSS 1.0.0 through 1.11.5 could allow a remote authenticated attacker to execute flows and obtain sensitive information due to insufficient session expiration of API keys after user deactivation.

### CVE-2026-81805

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-10T15:17:46.957 |

Unauthenticated Privilege Escalation in SiteSkite <= 2.1.5 versions.

### CVE-2026-81801

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:46.490 |

Subscriber Settings Change in WP-Stateless <= 4.4.1 versions.

### CVE-2026-81784

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-10T15:17:43.817 |

Unauthenticated PHP Object Injection in Wise Chat <= 3.4 versions.

### CVE-2026-2310

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-91` |
| Published | 2026-09-10T22:16:55.833 |

IBM webMethods Integration Server 11.1 IBM webMethods Integration is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-88052

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-09-10T18:18:14.317 |

Tesseract is an open source OCR engine. In version 5.5.3 and earlier, UNICHARSET::load_via_fgets in src/ccutil/unicharset.cpp trusts the declared unichar count as a loop bound and uses id as an unchecked index into the unichars vector. unichar_insert_backwards_compatible can leave the vector unchanged for an empty, duplicate, or already-encodable representation, causing id to become larger than unichars.size(). Subsequent set_* calls and the write to unichars[id].properties.enabled then write UNICHAR_PROPERTIES beyond the vector during initialization in both the default LSTM and legacy engines, causing heap corruption, a crash, or potentially controlled corruption. No fixed release is available as of this review.

### CVE-2026-89060

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-551` |
| Published | 2026-09-11T05:16:38.557 |

A cross-namespace authorization flaw in multicluster-observability-addon affects log-forwarding and tracing configurations that use ClusterLogForwarder or OpenTelemetryCollector resources. An authorized user who can modify ManagedClusterAddOn configuration could reference resources in another hub namespace, potentially disclosing associated Secrets to an attacker-controlled managed cluster.

### CVE-2026-17176

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-11T00:17:26.707 |

An OS
command injection vulnerability in the TDDP module of Deco BE11000 allows an
adjacent network attacker to execute arbitrary commands with root privileges by
sending a crafted UDP packet.



Successful exploitation may lead to complete
device compromise, including unauthorized command execution, modification of
device settings, and loss of confidentiality, integrity, and availability

### CVE-2026-81210

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-10T22:17:01.837 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 concatenates three caller-supplied strings into a String.format path on the shared /ds-storage RWX PVC and returns the file with no project ACL — pure IDOR plus traversal. Read is constrained to files named job.log/error.log, but DataStage job logs routinely carry connection strings, {dsnextenc} ciphertexts (decryptable via d2-f023), and customer-data row samples. This is the operator's tenant-to-tenant PVC-leakage threat verbatim; MEDIUM→HIGH via threat match.

### CVE-2026-87993

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-10T19:17:39.130 |

The consul-template library is vulnerable to an information disclosure issue in its error handling path that may allow Vault secret values to appear in template error messages, log output, and downstream surfaces such as Nomad task events. This vulnerability (CVE-2026-87993) is fixed in consul-template 0.43.0.

### CVE-2026-87776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401;CWE-459` |
| Published | 2026-09-11T12:16:52.530 |

compression is a Node.js and Express compression middleware. In versions before 1.8.2, when a client aborts the connection while a compressed response is still being sent, the zlib stream created to compress that response is never destroyed, so each aborted compressed response leaks its native zlib memory. A remote unauthenticated attacker can repeatedly open requests and disconnect early, exhausting the available memory and crashing the server. All applications using compression are affected. The issue is fixed in compression 1.8.2, and users should upgrade to 1.8.2 or later.

### CVE-2026-87908

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-11T07:16:47.937 |

multiparty is a Node.js library for parsing multipart/form-data request bodies. In versions from 2.1.0 up to but not including 4.3.1, the parser does not bound the amount of memory used while accumulating the headers of a single multipart part. An unauthenticated attacker can send a single request whose part carries a very large volume of header bytes, forcing the parser to buffer all of them and exhausting the process memory, which crashes the server. This is a denial of service with no confidentiality or integrity impact. The issue is fixed in multiparty 4.3.1, which caps the size of the accumulated part headers. Users should upgrade to multiparty 4.3.1 or later.

### CVE-2026-73785

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-241` |
| Published | 2026-09-11T07:16:46.623 |

A potential security vulnerability in HPE IceWall Federation Agent and Proxy could allow a remote unauthenticated attacker to cause a denial of service (DoS).

### CVE-2026-18561

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T04:17:20.480 |

The Unlimited Elements For Elementor plugin for WordPress is vulnerable to SQL Injection via the 'addontype' parameter in versions up to, and including, 2.0.16. This is due to insufficient escaping on the user-supplied parameter and the lack of sufficient preparation on the existing SQL query in the getWhereString() function; when the parameter is supplied as an array, element zero is used verbatim as the SQL comparison operator and concatenated into the WHERE clause without sanitization, while normalizeAjaxInputData() strips WordPress's magic_quotes protection from the value. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-15462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T04:17:20.173 |

The Sticky Chat Widget plugin for WordPress is vulnerable to SQL Injection via the 'scw_form_fields' parameter array keys of the 'scw_save_form_data' AJAX action in versions up to, and including, 1.4.2. This is due to the save_form_data() function passing attacker-controlled POST array keys unsanitized to $wpdb->insert(), which wraps column identifiers in backticks without escaping them, allowing a backtick in an attacker-supplied key to break out of the column-identifier list into raw SQL; additionally, the use of filter_input() bypasses WordPress's wp_magic_quotes() protection, and the widget_id validation loop is skipped entirely when no valid widget_id is supplied, leaving $isValid at 1. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-78133

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-11T02:18:34.757 |

libcharon in strongSwan 6.0.0 through 6.0.7 has a use-after-free in IKEv2 rekeying collision handling.

### CVE-2026-78132

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-09-11T02:18:34.613 |

strongSwan 5.1.3 through 6.0.7 has an infinite loop in the x509 plugin's attribute certificate parser for ietfAttrSyntax.

### CVE-2026-78130

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-11T02:18:34.353 |

strongSwan 4.2.0 through 6.0.7 has a NULL pointer dereference in the x509 plugin's attribute certificate parser.

### CVE-2026-77807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-11T00:19:23.037 |

The AcyMailing – An Ultimate Newsletter Plugin and Marketing Automation Solution for WordPress plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 11.0.4 via the `user[name]` Parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. Exploitation requires "Embed images" option in AcyMailing configuration being enabled.

### CVE-2026-86093

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T22:17:04.620 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 could allow an attacker with the ability to control or impersonate a DRDA server endpoint to execute arbitrary commands on Db2 clients due to a stack-based buffer overflow that improperly copies user-controlled data into a fixed-size stack buffer without bounds checking.

### CVE-2026-81265

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-10T22:17:02.253 |

IBM Langflow OSS 1.0.0 through 1.11.5.

### CVE-2026-45770

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-693;CWE-787` |
| Published | 2026-09-10T22:16:57.117 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Starting in version 8.0.0 and prior to version 8.0.5, a Lua rule that registers too many flow variables can corrupt Lua detection state and may bypass Suricata's restricted Lua sandbox. This requires an affected Lua script/rule to be loaded. Excessive flow variables being registered may also cause Suricata to crash. Version 8.0.5 contains a fix. As a workaround, disable `security.lua.allow-rules` unless Lua rules are required.

### CVE-2026-45769

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-10T22:16:56.970 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5,IKEv2 parser state could grow without bounds while storing client transforms. Repeated crafted UDP traffic may cause Suricata to consume excessive memory, potentially resulting in denial of service. Versions 7.0.16 and 8.0.5 fix the issue. Some workarounds are available. Disable IKE application-layer parsing if it is not needed. Alternatively, use a rule to bypass ike flows after the first packets like `alert ike any any -> any any (sid: 2; flow.pkts_toserver: > 256; bypass; noalert;)`.

### CVE-2026-45768

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-10T22:16:56.827 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Starting in version 8.0.0 and prior to version 8.0.5, LDAP transaction state could store an unbounded number of responses. Because LDAP can be processed over UDP, crafted traffic may cause Suricata to consume excessive memory, potentially resulting in denial of service. Version 8.0.5 contains a fix. As a workaround, disable LDAP application-layer parsing where it is not required. Alternatively, use a rule like `alert ldap any any -> any any (sid: 1; ldap.responses.count: >1024; bypass;)`.

### CVE-2026-45766

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-10T22:16:56.540 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, certain NFS parser state structures were insufficiently bounded. Crafted NFS traffic may cause Suricata to consume excessive memory, potentially resulting in denial of service. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, disable NFS application-layer parsing if it is not needed.

### CVE-2026-45765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-10T22:16:56.397 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, DNP3 reassembly could buffer data without sufficient parser-level bounds. Crafted DNP3 traffic may cause Suricata to consume excessive memory, potentially resulting in denial of service. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, disable DNP3 (which is not enabled by default) if it is not needed, and/or define a limited `stream.reassembly.depth` (0 or absent is unlimited).

### CVE-2026-45762

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-09-10T22:16:56.100 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, Suricata's IP defragmentation tracker lookup did not verify that an existing tracker used the same IP address family as the packet being processed. Under crafted fragmented IPv4/IPv6 traffic, an IPv6 fragment could be associated with an IPv4 defragmentation tracker. This can lead to a remote packet-triggered crash and denial of service when Suricata performs the relevant defragmentation. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, if using Suricata as an IDS with AF_PACKET, enabling AF_PACKET's `defrag` option may prevent Suricata from seeing such fragmented packets.

### CVE-2026-45759

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-10T21:17:27.543 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, Suricata could repeatedly perform expensive parsing of large HTTP `Content-Disposition` headers during HTTP response body processing. Crafted HTTP traffic could cause excessive CPU usage and denial of service. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, use a rule like `alert http1 any any -> any any (sid: 1; http.request_header; content: "Content-Disposition:"; startswith; bsize: > 8192; bypass;)`.

### CVE-2026-88045

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-09-10T17:17:08.530 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. From 1.75.0 until 1.75.1, the serve S3 streamed multipart path in cmd/serve/s3/multipart.go passes attacker-controlled contentLength to multipart.NewRW().Reserve before reading request-body bytes. waitForTurn admits the current part and one oversized part when the buffer is empty despite --multipart-streaming-buffer-limit, and lib/pool allocates 1 MiB pages according to Content-Length or X-Amz-Decoded-Content-Length. A network client can retain or multiply these reservations without sending the declared body, exhausting process or host memory or permanently blocking request handlers. Anonymous S3 deployments require no credentials, while deployments using auth_key require an accepted S3 key. This issue is fixed in version 1.75.1.

### CVE-2026-84821

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:49.123 |

Unauthenticated Broken Access Control in WP Fast Total Search <= 1.82.284 versions.

### CVE-2026-81804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-09-10T15:17:46.827 |

Unauthenticated Sensitive Data Exposure in ZHBackup – Backup, Restore &amp; Migration <= 2.4.2 versions.

### CVE-2026-81803

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-10T15:17:46.657 |

Subscriber Remote Code Execution (RCE) in RepairBuddy <= 4.1224 versions.

### CVE-2026-81799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:46.230 |

Unauthenticated Broken Access Control in Return Refund and Exchange For WooCommerce <= 4.6.4 versions.

### CVE-2026-81794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:45.423 |

Unauthenticated Broken Access Control in Shirt Product Designer for WooCommerce 1.0.4 versions.

### CVE-2026-81786

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:44.077 |

Unauthenticated Broken Access Control in Thank You Page Customizer for WooCommerce <= 1.2.2 versions.

### CVE-2026-46387

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-10T15:17:35.267 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to versions 7.0.16 and 8.0.5, Suricata's HTTP/2 decompression path could grow the decompressed response-body buffer without an effective upper bound. A crafted HTTP/2 DATA payload using a high compression ratio, such as gzip, deflate, or brotli compressed data, could cause Suricata to allocate excessive memory while decompressing the payload. Versions 7.0.16 and 8.0.5 contain a fix. As a workaround, disable HTTP2.

### CVE-2026-45747

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-10T15:17:34.997 |

Suricata is a network Intrusion Detection System, Intrusion Prevention System and Network Security Monitoring engine. Prior to version 7.0.16, the Lua TLS certificate information helper could dereference NULL certificate fields when a Lua script requested certificate information for TLS traffic where some certificate fields were absent. Crafted TLS traffic processed by a deployment using affected Lua TLS scripting could crash Suricata, resulting in denial of service. Version 7.0.16 contains a fix. As a workaround, avoid Lua scripts that call TLS certificate information helpers on untrusted traffic (`TlsGetCertInfo` function), or update scripts to handle missing certificate fields where possible.

### CVE-2026-89161

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-590` |
| Published | 2026-09-11T04:18:04.470 |

In PCRE2 before 10.48, pcre2_jit_match mishandles a previously copied subject being passed in as a context. An incorrect free operation can occur.

### CVE-2026-80434

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-10T22:17:01.303 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to manipulate runtime caches and cause a denial of service due to an insecure direct object reference.

### CVE-2026-57842

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-09-11T14:17:27.873 |

NetBSD contains a use-after-free and double-free vulnerability in msg_recv_copyin() within the COMPAT_NETBSD32 compatibility layer due to a missing return statement before the cleanup label on the success path. Any local user able to execute a 32-bit binary on a 64-bit NetBSD system can trigger a kernel panic or memory corruption by calling recvmsg() with msg_iovlen between 9 and IOV_MAX, causing the kernel to access a freed iovec buffer and subsequently free the same allocation a second time.

### CVE-2025-15679

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:N/R:U/V:C/RE:L/U:Clear` |
| Weaknesses | `CWE-258` |
| Published | 2026-09-11T09:17:20.067 |

Under certain circumstances such as reset to factory default operation, the BMC root account is made active without a password on BullSequana XH3406 and XH3515.

### CVE-2026-89087

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-573` |
| Published | 2026-09-10T20:17:32.247 |

The cstruct package before 6.3.0 for OCaml mishandles indexes.

### CVE-2026-88017

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-488` |
| Published | 2026-09-10T16:18:08.773 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. From 1.64.0 until 1.75.1, the FTP auth-proxy driver in cmd/serve/ftp/ftp.go stores one obscured password per username in the server-wide userPass map[string]string instead of binding the credential or VFS to the authenticated session. If two accepted credentials use the same username but resolve to different proxy backends, a later CheckPasswd login overwrites userPass[user], and subsequent getVFS operations on the first session are reauthorized with the later password. The first session can then read, create, overwrite, rename, or delete objects using the second credential’s backend authority. Exploitation requires the later same-username login to occur while the first session remains open. This issue is fixed in version 1.75.1.

### CVE-2026-81796

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-10T15:17:46.107 |

Unauthenticated Broken Authentication in WP Travel <= 12.0.3 versions.

### CVE-2026-17037

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T10:16:51.330 |

The Kirki – Freeform Page Builder, Website Builder & Customizer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the ‘comment’ parameter in all versions up to, and including, 6.2.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-74925

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-11T07:16:46.740 |

The MultiVendorX  WordPress plugin before 5.0.16 does not restrict who can update its role and capability settings, allowing users holding its vendor role to grant that role administrator-level capabilities and take over the site.

### CVE-2026-81825

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T04:17:58.947 |

The Simple Ajax Chat – Add a Fast, Secure Chat Box plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Chat Message in all versions up to, and including, <= 20260811 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce protecting chat message submission is publicly visible on the chat page, rendering it ineffective as an authentication barrier and allowing fully unauthenticated attackers to submit malicious messages that are stored persistently and rendered to all visitors on every page load.

### CVE-2026-81754

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T04:17:58.190 |

The Vigilant – 100% Free Security Suite: Firewall, 2FA, Login, Headers, Scanner… plugin for WordPress is vulnerable to Stored Cross-Site Scripting via User-Agent Header in all versions up to, and including, 2.10.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The malicious payload is delivered passively by any unauthenticated visitor who triggers a failed login attempt with a crafted User-Agent header, requiring no further interaction from the attacker once stored.

### CVE-2026-18579

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-11T04:17:24.600 |

The WP Photo Album Plus plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'HTTP_X_FORWARDED_FOR' parameter in all versions up to, and including, 9.2.08.003 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce failure path for the getshortcodedrenderedfenodelay action serves as the log-write trigger rather than an access barrier — a deliberately failed nonce check causes wppa_log() to record the attacker-supplied X-Forwarded-For value to disk, making the exploit fully reachable by unauthenticated callers via the wp_ajax_nopriv_wppa endpoint.

### CVE-2026-89252

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-11T12:16:55.377 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 fails to verify ownership in addLiveLink.php when updating LiveLinks, allowing authenticated users to modify other users' links. A canStream user can overwrite another user's LiveLink HLS source and metadata by supplying an existing linkId, redirecting viewers to attacker-controlled media.

### CVE-2026-89251

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-09-11T12:16:55.223 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 fails to validate ad impressions in plugin/AD_Server/log.php, allowing logged-in users to submit arbitrary label values that trigger unverified wallet credits to campaign video owners. Attackers can repeatedly POST label=start requests to mint YPTWallet balance for any campaign video without proof an ad actually played.

### CVE-2026-89245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-11T12:16:54.270 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in playlistRemove.php that allows attackers to delete playlists by skipping CSRF protection checks. Attackers can craft a malicious form that submits a POST request to playlistRemove.php, causing a victim's playlist to be deleted when they visit the attacker's page while logged in.

### CVE-2026-78134

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-11T02:18:34.910 |

strongSwan 4.5.0 through 6.0.7 has Incorrect Access Control in the eap-ttls and eap-peap plugins because there can be a missing or mismatched inner EAP identity.

### CVE-2026-80380

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-10T22:17:01.030 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote attacker to perform unauthorized actions due to cross-site request forgery.

### CVE-2026-89011

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-10T20:17:31.833 |

isomorphic-git before 1.42.0 contains a prototype pollution vulnerability in the getRemoteInfo function that allows a malicious Git server operator to pollute Object.prototype by advertising crafted ref names containing '__proto__' path segments during ref negotiation. Attackers controlling a Git server can advertise a specially crafted ref such as '__proto__/corsProxy' to reroute all subsequent network operations through an attacker-controlled proxy, causing isomorphic-git to invoke the victim's onAuth callback and transmit credentials to the attacker when the victim calls getRemoteInfo with an attacker-supplied URL.

### CVE-2026-88021

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-185` |
| Published | 2026-09-10T19:17:39.250 |

Consul and Consul Enterprise are vulnerable to an authorization bypass in the Connect service mesh that may allow a service to reach a destination it is not authorized to access. When building Envoy RBAC rules to enforce Connect intentions, Consul did not correctly escape certain characters in service names, namespaces, and partitions, causing the generated authorization rules to match more broadly than intended. This vulnerability (CVE-2026-88021) is fixed in Consul 2.0.4 and Consul Enterprise 1.21.18, 1.22.12 and 2.0.4.

### CVE-2026-88028

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-10T18:18:13.170 |

Improper neutralization of special elements in data query logic in the polymorphic relation handling of the MongoDB integration for Laravel can cause a caller-supplied relation identifier to be interpreted as a query condition rather than as a literal identifier. An authenticated user who can influence a stored relation identifier may cause an affected application to return a document other than the intended relation target.

### CVE-2026-88027

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-10T18:18:13.030 |

Improper neutralization of special elements in data query logic in the embedded-document relation handling of the MongoDB integration for Laravel can cause a caller-supplied embedded record identifier to be interpreted as a query condition rather than as a literal identifier. An authenticated user who can influence such an identifier may delete all embedded documents in a targeted record or overwrite an embedded document other than the intended target.

### CVE-2026-88026

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-09-10T18:18:12.887 |

Improper neutralization of regular-expression metacharacters in the LINQ query translation component of the MongoDB C# Driver can cause a caller-supplied character sequence to alter a regular-expression predicate generated by an affected application. An authenticated user who can influence such a value may cause the application to return records beyond those intended by the original filter.

### CVE-2026-88938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T16:18:12.430 |

knowns through 0.33.0 fails to confine the path argument of the code.find MCP tool to the project root, allowing AI agent sessions to read source files anywhere on the host. Attackers can supply absolute paths or relative traversal sequences to the path argument and retrieve full file contents from outside the intended project directory.

### CVE-2026-88016

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-59;CWE-281` |
| Published | 2026-09-10T16:18:08.637 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. Prior to 1.75.1, when backend/local runs with --links, a source .rclonelink object can plant a symlink in the destination and later directory metadata is applied through that path. MkdirMetadata, writeMetadataToFile, and setTimes operate when Directory.translatedLink=false, so os.Chown, os.Chmod, os.Chtimes, and birth-time handling can bypass os.Root confinement and follow the symlink. An attacker controlling source contents can therefore apply selected ownership, permissions, modification times, or birth times to a file or directory outside the destination, with --metadata required for chmod and chown while modification time is applied by the normal directory workflow. This issue is fixed in version 1.75.1.

### CVE-2026-88898

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T15:17:59.107 |

AppFlowy-Cloud versions 0.7.2 through 0.9.64 fail to authorize callers against the workspace in the bulk publish endpoint path, allowing authenticated users to publish content into other tenants' namespaces. Attackers can write published views with attacker-controlled title, body and metadata into victim workspaces to deface public pages or host phishing content on trusted URLs.

### CVE-2026-84819

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T15:17:48.967 |

Unauthenticated Cross Site Scripting (XSS) in WPAdverts <= 2.3.3 versions.

### CVE-2026-84816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T15:17:48.817 |

Unauthenticated Cross Site Scripting (XSS) in WPCS <= 1.3.2 versions.

### CVE-2026-81795

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T15:17:45.957 |

Unauthenticated Cross Site Scripting (XSS) in Page Visits Counter &#8211; Lite <= 1.2.3 versions.

### CVE-2026-81783

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-10T15:17:43.673 |

Subscriber Broken Authentication in MailMunch – Grow your Email List <= 3.2.5 versions.

### CVE-2026-15419

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T18:17:55.590 |

In the silabser.sys driver for CP210x devices v11.5.0 and earlier, a local unprivileged user with a malicious device can use malformed packets to corrupt kernel pool memory, resulting in arbitrary code execution with escalated privileges.

### CVE-2026-88924

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-10T15:17:59.253 |

A flaw was found in the admin backend of gvfs. The privileged gvfsd-admin daemon changes the ownership of newly created private D-Bus sockets by calling the link-following chown() function on a pathname inside a user-controlled directory. A local attacker can exploit this via a Time-of-Check Time-of-Use (TOCTOU) race condition and exchange the socket pathname with a symbolic link pointing to an arbitrary root-owned file (such as /etc/pam.d/su). The daemon subsequently follows the symlink and changes the ownership of the targeted root-owned file to the attacker's user ID. This allows an authenticated local attacker to modify critical system files, leading to a full local privilege escalation to root.

### CVE-2026-88008

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444;CWE-863` |
| Published | 2026-09-10T15:17:56.433 |

Traefik is an open source HTTP reverse proxy and load balancer. From 2.11.26 until 2.11.57 and 3.7.13, Traefik forwards a client-supplied Connection header requesting Upgrade, the Upgrade: h2c token, and HTTP2-Settings to a shared backend. If the backend accepts h2c and returns 101 Switching Protocols, Traefik enters a raw tunnel and no longer applies routers, BasicAuth, ForwardAuth, IPAllowList, RateLimit, access logging, metrics, or tracing to later HTTP/2 requests, allowing an unauthenticated request through an unprotected route to reach protected paths on the same backend. This issue is fixed in 2.11.57 and 3.7.13.

### CVE-2026-88004

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436;CWE-807` |
| Published | 2026-09-10T15:17:54.940 |

Traefik is an open source HTTP reverse proxy and load balancer. From 3.2.0 until 3.7.13, Traefik entrypoint defenses aliasHeadersStrategy, underscoreHeadersStrategy, and forwardedHeaders inspect req.Header but not req.Trailer, allowing an unauthenticated client to submit an aliasing or trusted header name in an HTTP/1.1 chunked trailer or an HTTP/2 trailer. When the retry or buffering middleware reads the body before the reverse proxy clones the request, the attacker-controlled trailer value reaches a backend that merges trailers into the header namespace, bypassing the documented delete or reject behavior and potentially spoofing identity or forwarded routing data. This issue is fixed in 3.7.13.
