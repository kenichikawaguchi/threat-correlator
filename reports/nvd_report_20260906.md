# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-05 15:01 UTC
- **対象期間**: `2026-09-04T15:00:31.000Z` 〜 `2026-09-05T15:01:22.000Z`
- **重要CVE数**: 160 件（Critical 9.0+: 37 件 / High 7.0〜: 123 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **リモートコード実行 (RCE)／認証バイパス** に関するもので、攻撃者が認証なしにサーバ上で任意のコマンドを実行できる点が共通しています。  
- WordPress エコシステム向けプラグインが集中して報告されており、特に **PHP オブジェクトインジェクション** や **フックインジェクション** が原因の脆弱性が多数です。  
- コンテナ・CI/CD 系ツールや IoT デバイス向けソフトウェアでも、デフォルトで認証が無効化されているエンドポイントが露出しているケースが目立ち、**ネットワーク境界の保護が不十分** であることがリスクを拡大させています。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / バージョン | 主な脆弱性種別 | 影響範囲・リスク |
|-----|-------------------|----------------|-------------------|
| **CVE‑2026‑10196** | Mail Mint – Email Marketing, Newsletter, Email Automation & WooCommerce Emails (≤ 1.31.0) | PHP Object Injection (POI) via `handle_form_submission` | 任意の PHP オブジェクトをデシリアライズさせ、サーバ上で **完全なリモートコード実行** が可能。WordPress サイト全体が乗っ取られる危険性が高い。 |
| **CVE‑2024‑11080** | Post Grid and Gutenberg Blocks – ComboBlocks (2.2.32 〜 2.3.1) | Unauthenticated Hook Injection | 認証不要で任意の WordPress フックを実行でき、**管理者権限取得**やプラグインの改ざんが可能。プラグインが広く利用されているため被害拡大が懸念される。 |
| **CVE‑2026‑83627** | Hummingbird – Speed Optimization, Caching, Minify, Compress & CDN (≤ 3.21.0) | Remote Code Execution via `log_msg()` (page‑cache debug log) | デバッグログを書き込めるディレクトリ `wp-content/wphb-logs/` が書き込み可能で、攻撃者が **任意の PHP コード** を配置し実行できる。キャッシュ機能が有効な全サイトに影響。 |
| **CVE‑2026‑75430** | PowerJob Worker 5.1.2 (およびそれ以前) | 未認証の `/worker/deployContainer` エンドポイント公開 | デフォルトポートで **任意のコンテナデプロイ** が可能となり、攻撃者はマルウェアコンテナを実行して内部ネットワークを横移動できる。CI/CD パイプラインに組み込まれているケースが多い。 |
| **CVE‑2026‑86124** | AutoAgent (任意のバージョン) | 未認証 RCE – TCP サーバが全インターフェースでリッスンし、受信コマンドを root で実行 | コンテナ内外から **任意のシェルコマンド** が実行でき、特権昇格やデータ窃取が即座に可能。DevOps 環境で自動化エージェントとして利用されることが多く、放置すると大規模インシデントに発展。 |

> **選定理由**  
> - **CVSS が 9.8**（上位 4 件）で、かつ **広く利用されているプラットフォーム**（WordPress、コンテナオーケストレーション）に影響。  
> - いずれも **認証不要** でリモートコード実行が可能な点が共通し、**即時対応が求められる**。  
> - 影響範囲が大きく、攻撃成功時に取得できる権限が **管理者／root** になるため、組織全体のセキュリティ姿勢に直結する。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | **推奨バージョン** | 実施手順のポイント |
|------|-------------------|-------------------|-------------------|
| Mail Mint (WordPress) | ≤ 1.31.0 | **≥ 1.31.1**（公式リリースがある場合） | `wp plugin update mail-mint` または手動で最新 zip を上書き。 |
| Post Grid & Gutenberg Blocks – ComboBlocks | 2.2.32 〜 2.3.1 | **≥ 2.3.2** | `wp plugin update combo-blocks`。アップデート前にプラグイン設定のバックアップを取得。 |
| Hummingbird | ≤ 3.21.0 | **≥ 3.21.1** | `wp plugin update hummingbird-performance`。`wp-content/wphb-logs/` の書き込み権限を **750** へ縮小。 |
| PowerJob Worker | ≤ 5.1.2 | **≥ 5.1.3** (またはベンダーが提供する修正版) | デプロイパイプラインでイメージを再ビルドし、`/worker/deployContainer` エンドポイントに認証ミドルウェアを追加。 |
| AutoAgent | すべてのバージョン (未パッチ) | **ベンダー提供の修正版**（リリースが未定の場合は **使用停止**） | コンテナ起動オプションで `--listen 127.0.0.1` に限定し、外部からの接続を遮断。 |

### 3.2 速やかな緊急対策（パッチ未提供時）
1. **プラグイン無効化**  
   - `wp plugin deactivate mail-mint` など、脆弱プラグインを一時的に無効化し、影響範囲を限定。  
2. **Web アプリケーションファイアウォール (WAF) でのシグネチャ追加**  
   - `handle_form_submission` の POST パラメータや `function.php` のフック呼び出しをブロックするルールを設定。  
3. **ネットワークレベルでのアクセス制御**  
   - PowerJob の `/worker/deployContainer`、AutoAgent の TCP ポート 8000 への外部アクセスを **ファイアウォールで遮断**（例: `iptables -A INPUT -p tcp --dport 8000 -s <trusted‑subnet> -j ACCEPT`）。  
4. **ファイル・ディレクトリ権限の最小化**  
   - `wp-content/wphb-logs/` → `chmod 750`、所有者を

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-10196

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-05T12:16:46.790 |

The Mail Mint – Email Marketing, Newsletter, Email Automation & WooCommerce Emails plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.31.0 via deserialization of untrusted input in the 'handle_form_submission' function. This makes it possible for unauthenticated attackers to inject a PHP Object. The additional presence of a POP chain allows attackers to execute code on the server. The vulnerability was partially patched in version 1.23.1.

### CVE-2024-11080

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-05T09:16:48.880 |

The Post Grid and Gutenberg Blocks – ComboBlocks plugin for WordPress is vulnerable to Unauthenticated Hook Injection in versions 2.2.32 to 2.3.1 via several functions in the ~/includes/blocks/form-wrap/function.php file. This makes it possible for unauthenticated attackers to execute actions with hooks in WordPress, granted no other security controls are present in the function.

### CVE-2026-83627

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-05T06:17:10.080 |

The Hummingbird – Speed Optimization, Caching, Minify, Compress & CDN plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 3.21.0 via the log_msg() function in core/modules/class-page-cache.php. The page-cache debug log is written to wp-content/wphb-logs/page-caching-log.php, a directly web-accessible PHP file that is supposed to be protected by a leading '<?php die(); ?>' header. That header is guarded by class_exists( 'Filesystem' ), which can never match because class_exists() resolves string arguments in the global namespace while the class is Hummingbird\Core\Filesystem; when the log is created during a front-end request the header is therefore omitted entirely. get_cookies() then writes the raw name of any cookie matching the wphb_cache_ prefix into that file without sanitization. This makes it possible for unauthenticated attackers to write arbitrary PHP into the log file with a single anonymous request and execute it by requesting the file directly, resulting in full remote code execution. Exploitation requires the site administrator to have enabled Page Caching with the Debug Log option (non-default), and the log file to be created during a front-end request — a state reached by the plugin's own 'Clear logs' action, any cache flush, or unattended via the plugin's daily log-rotation cron, which can strip the protective header from an existing log file.

### CVE-2026-13447

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-05T06:17:09.403 |

The Mstore Api plugin for WordPress is vulnerable to Authentication Bypass via JWT Forgery in versions up to, and including, 4.20.0 This is due to missing cryptographic signature verification in the FirebasePhoneAuthHelper::verify_id_token() function, which decodes and validates Firebase ID token claims (alg, kid, aud, iss) but never calls openssl_verify() or any equivalent to validate the JWT signature against Google's actual public key certificates. This makes it possible for unauthenticated attackers to forge a Firebase Phone Auth JWT signed with a self-generated RSA key pair and impersonate any phone number, resulting in unauthorized access to existing WordPress accounts or creation of new arbitrary accounts.

### CVE-2026-75430

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T17:16:57.767 |

PowerJob Worker version 5.1.2 (and likely earlier versions) exposes the /worker/deployContainer HTTP endpoint without authentication on the default transport port. This allows a remote attacker to execute arbitrary code.

### CVE-2026-31020

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T17:16:56.910 |

In DocsGPT 0.15.0 and below, the application provides a custom prompt feature that allows users to define prompt content used during chatbot interactions. This functionality renders user-supplied prompt data using Jinja templates without input sanitization or sandboxing. An unauthenticated attacker can inject malicious template expressions, leading to a server-side template injection (SSTI) vulnerability that can be exploited to achieve full remote code execution (RCE).

### CVE-2026-18658

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T16:17:21.133 |

IBM Operational Decision Manager 9.6.0.0, 9.5.0.0, 8.11.1.0, 8.11.0.1, 8.12.0.1, 9.5.0.1, and 9.0.0.1 is vulnerable to SQL injection. An unauthenticated attacker can execute arbitrary SQL statements and leverage database functionality to write a web shell to the application web root, resulting in remote code execution.

### CVE-2026-19274

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-04T16:17:21.650 |

IBM Observability with Instana (Agent) Build 1.0.303 through 1.0.323 IBM Instana Agent Operator could allow an authenticated Kubernetes tenant to hijack or permanently destroy another tenant's cluster-level RBAC permissions, caused by cluster-scoped RBAC objects being keyed solely by the bare CR name with no namespace disambiguation, allowing a same-named `InstanaAgent` CR in an attacker-controlled namespace to silently overwrite the shared `ClusterRoleBinding` or delete it outright and revoke the victim agent's cluster monitoring access.

### CVE-2026-86123

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-05T10:16:43.750 |

SQL Chat contains four unauthenticated API endpoints that accept client-supplied database connection parameters and execute arbitrary SQL queries against attacker-specified hosts. Attackers can connect to internal databases, execute SQL commands, enumerate schemas, and pivot into the server's network without authentication.

### CVE-2026-52777

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352;CWE-502` |
| Published | 2026-09-05T00:17:20.663 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.6, there is an authenticated PHP object injection vulnerability in BazarImportAction via unserialize. This issue has been patched in version 4.6.6.

### CVE-2026-75925

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-04T22:17:18.017 |

Improper neutralization of CRLF sequences in IXON VPN Client before version 1.4.7 allows an attacker to execute commands as root or SYSTEM. Configuration values accepted by the local service are written to a file later consumed by a privileged subprocess, without line-ending sequences being neutralized, which allows additional directives to be introduced into that file. The configuration interface accepts changes without authenticating or verifying the origin of the requester. The injected configuration persists on disk across restarts of the client and the operating system, and the VPN connection continues to function normally, so there is no behavioral change visible to the user.

### CVE-2026-86190

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-05T13:18:14.150 |

WWBN AVideo contains a broken access control vulnerability in videoViewsInfo endpoints that returns complete user records including password hashes, recovery tokens, and live session identifiers to unauthenticated callers when a hash parameter is provided. Attackers can use the disclosed session identifier to hijack viewer sessions, including administrator accounts, and obtain sensitive personal data for all video viewers.

### CVE-2026-86189

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-05T13:18:14.000 |

WWBN AVideo contains a path traversal vulnerability in notify.ffmpeg.json.php that allows unauthenticated attackers to write files to arbitrary locations by supplying a caller-chosen path in the avideoRelativePath parameter. Attackers can replay any previously issued ciphertext as a notifyCode token, which is decrypted but never validated, to bypass authentication and write files to the application root and subdirectories.

### CVE-2026-86184

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-05T12:16:49.090 |

Lara Dashboard before 1.3.0 contains an authentication bypass vulnerability in the screenshot-login route that allows unauthenticated attackers to authenticate as any user by email when APP_ENV is not production. Attackers can request the GET /screenshot-login/{email} endpoint with a registered email address to receive a fully authenticated session, enabling access to user administration, settings, database contents, and arbitrary code execution through the module installer.

### CVE-2026-86124

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-05T10:16:43.900 |

AutoAgent contains an unauthenticated remote code execution vulnerability in the TCP server that binds to all interfaces and executes attacker-supplied commands as root. Attackers can connect to the exposed communication port and execute arbitrary bash commands within the container, gaining access to bind-mounted host workspace directories.

### CVE-2026-86121

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-05T10:16:43.463 |

Cua computer-server versions before 0.3.42 skip authentication when the CONTAINER_NAME environment variable is unset and bind to all interfaces by default, allowing unauthenticated attackers to execute arbitrary commands. Attackers can reach TCP port 8000 to run shell commands via the run_command endpoint, read and write arbitrary files through file operation endpoints, and access interactive PTY shells without authentication.

### CVE-2026-44402

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-04T16:17:25.250 |

Voltronic Power SNMP Web Pro 1.1 contains an unauthenticated remote code execution vulnerability in the upload.cgi firmware update endpoint that allows remote attackers to execute arbitrary commands as root by uploading a crafted tar archive without valid credentials. Attackers can supply a malicious tar archive containing arbitrary executable files that are extracted to a privileged directory and executed as root, achieving full system compromise.

### CVE-2026-85696

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T15:17:48.523 |

SadTalker contains an OS command injection vulnerability in the video muxing process where uploaded audio filenames are interpolated into ffmpeg commands without proper escaping. Attackers can upload audio files with shell metacharacters in the filename to break out of quoted arguments and execute arbitrary system commands when video generation occurs.

### CVE-2026-85695

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T15:17:47.690 |

FastChat contains an authentication bypass vulnerability in the /register_worker endpoint that allows unauthenticated attackers to register arbitrary worker addresses and perform server-side request forgery. Attackers can register malicious workers under victim model names to intercept user prompts, images, and responses, or probe internal network ports across the worker mesh.

### CVE-2026-85688

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T15:17:46.657 |

TEN Framework 0.11.71 contains unauthenticated arbitrary file read and write vulnerabilities in the TMAN Designer file-content API endpoints. Attackers can submit POST and PUT requests to the /api/designer/v1/file-content endpoints to read arbitrary files or write malicious content to system paths, enabling code execution through authorized_keys, cron files, or executable graph files.

### CVE-2026-85672

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T15:17:45.293 |

zerox 1.1.20 contains an OS command injection vulnerability in the file download mechanism where the temporary file extension derived from document URLs is interpolated unsanitized into shell commands executed by poppler utilities. Attackers can craft document URLs with malicious file extensions containing command substitution syntax to execute arbitrary OS commands before document processing occurs.

### CVE-2026-85667

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T15:17:44.543 |

xiaobei through 5.5.2 fails to implement authentication or signature validation on webhook endpoints, allowing unauthenticated attackers to inject arbitrary messages into the agent pipeline. Attackers can publish malicious messages via the /webhook_worktool handler and exploit unvalidated media URL fetching to perform server-side request forgery against internal services.

### CVE-2026-85663

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T15:17:43.947 |

Aim 3.29.1 remote tracking server fails to authenticate requests and dispatches arbitrary methods through getattr without allowlist validation. Unauthenticated attackers can register clients, instantiate Repo resources, and invoke arbitrary methods to read experiments or delete runs.

### CVE-2026-85661

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:43.643 |

excel-mcp-server 0.1.8 fails to enforce path confinement in stdio mode when EXCEL_FILES_PATH is unset, allowing attackers to read and write arbitrary files. Attackers can supply unchecked file paths to read and write tools to access any file accessible to the process.

### CVE-2026-86119

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-05T10:16:43.157 |

Webstudio through 0.296.0 contains an unauthenticated server-side request forgery vulnerability in the /cgi/image, /cgi/video, and /cgi/asset proxy routes when RESIZE_ORIGIN environment variable is unset. Attackers can supply arbitrary URLs to these endpoints to read cloud instance metadata, access internal services, and perform network reconnaissance on the instance infrastructure.

### CVE-2026-86117

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-05T10:16:42.860 |

Coolify through 4.3.17 contains an authentication bypass vulnerability in the OAuth callback handler that signs users into existing accounts based solely on email address without verifying provider assertions or binding OAuth identities. Attackers can register a victim's email address on any enabled OAuth provider to obtain authenticated sessions as that user, bypassing password requirements and two-factor authentication.

### CVE-2026-9317

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T18:18:07.297 |

Nango before 0.71.6 contains a missing authentication vulnerability in the runner tRPC server that allows unauthenticated attackers to execute arbitrary JavaScript code by invoking the exposed start procedure without credentials. Attackers with network access to the runner port can send requests to the unauthenticated start procedure, bypassing the unenforced RUNNER_SECRET_KEY environment variable, to achieve remote code execution within the runner process.

### CVE-2026-85694

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T15:17:47.540 |

LaVague 0.2.35 contains a remote code execution vulnerability in PythonFromMarkdownExtractor.extract_as_object that evaluates untrusted language model output derived from web page content. Attackers can inject malicious Python code through web pages using indirect prompt injection to execute arbitrary code on the operator's host without review.

### CVE-2026-85660

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T15:17:43.490 |

cli-mcp-server 0.2.5 contains a command allowlist bypass vulnerability in the _validate_command_with_operators function when ALLOW_SHELL_OPERATORS is enabled. Attackers can use shell command substitution syntax like $(...) or backticks to execute non-allowlisted commands that bypass the ALLOWED_COMMANDS validation check.

### CVE-2026-85625

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-04T15:17:42.880 |

sift (sift.js) 17.1.3 enumerates query keys with for...in, which walks the object prototype chain, and dispatches any matched operator key including $where. The $where operation compiles a string value into a function using new Function unless CSP_ENABLED is set (not set by default). As a result, if a prototype-pollution primitive elsewhere in the process sets Object.prototype.$where to a malicious string, even benign filter calls such as sift({}) execute arbitrary JavaScript. Additionally, passing an untrusted query object containing a string $where directly to sift results in code execution under the default configuration.

### CVE-2026-85620

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T15:17:42.150 |

Postgres MCP Pro 0.3.0 contains a restricted-mode bypass vulnerability where function-name validation is not applied to RangeFunction nodes in FROM clauses. Attackers can execute file-reading functions like pg_read_file through FROM-clause syntax to read arbitrary files despite restricted-mode protections.

### CVE-2026-52766

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-276;CWE-862` |
| Published | 2026-09-05T00:17:19.393 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.6, the {{erasespamedcomments}} wiki action (actions/EraseSpamedCommentsAction.php) accepts a suppr[] array from POST and deletes every wiki page whose tag appears in that array, with no authorization check anywhere in the action body or in the page-deletion path it invokes. Combined with YesWiki's allow-by-default action ACL model, any user who has page write access, which is the default for everyone (default_write_acl='*') on a fresh install can permanently delete arbitrary wiki pages, including the front page, admin pages, and pages owned by other users. This issue has been patched in version 4.6.6.

### CVE-2026-81939

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T19:17:29.237 |

A Zip Slip vulnerability in the SonicWall Network Security Manager (NSM) On-Prem file upload and archive processing functionality allows an attacker to extract files outside the intended destination directory using a specially crafted archive.

### CVE-2026-78328

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T19:17:27.463 |

A missing authorization vulnerability in the SonicWall Network Security Manager (NSM) On-Prem Management interface allows a lower-privileged Admin user to escalate privileges to SuperAdmin.

### CVE-2026-78327

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T19:17:27.347 |

An Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the SonicWall Network Security Manager (NSM) On-Prem Management interface allows an authenticated attacker with SuperAdmin privileges to inject arbitrary commands that are executed on the underlying host, resulting in remote code execution.

### CVE-2026-75431

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-04T16:17:59.413 |

PowerJob Server version 5.1.2 (and likely earlier) uses a predictable JWT signing key for HS256-based authentication. This allows a remote attacker to execute arbitrary code.

### CVE-2026-75160

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-04T16:17:57.827 |

An issue in X-Serie Gateway Firmware V6_00_05 allows a remote attacker to escalate privileges via the endpoints /cgi-bin/wwwugw.cgi and /cgi-bin/ugwdownload.cgi.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-48019

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-04T23:17:09.143 |

Laravel is a web application framework. Prior to versions 12.60.0 and 13.10.0, a CRLF injection vulnerability in Laravel's email validation, in combination with how Symfony Mailer and Symfony Mime handle certain character sequences, may allow an unauthenticated attacker to interfere with outbound email processing in applications that send mail to user-supplied addresses. This issue has been patched in versions 12.60.0 and 13.10.0.

### CVE-2025-9049

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-05T12:16:46.653 |

The Nokri – Job Board WordPress Theme theme for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the 'nokri_account_member_permissions' function in all versions up to, and including, 1.6.4. This makes it possible for authenticated attackers, with Subscriber-level access and above, to add new Subscriber users with employer account member permissions, who in turn can escalate privileges by updating the email address of any user, including Administrator users.

### CVE-2026-81543

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-05T08:16:40.730 |

The Abandoned Cart Pro for WooCommerce plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 10.7.1. This is due to missing capability checks and nonce verification on multiple AJAX actions including wcap_save_connector_settings, wcap_send_manual_email, wcap_abandoned_cart_info, and wcap_change_manual_email_data. This makes it possible for authenticated attackers, with subscriber-level access and above, to modify SMTP connector settings to route administrator recovery emails through an attacker-controlled server and intercept auto-login links to gain full administrative access. The plugin's auto-login feature must be enabled, which is the default configuration.

### CVE-2026-19887

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-05T07:17:11.657 |

The Welcart e-Commerce plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.12.1 via deserialization of untrusted input in the Telecom EDY payment callback (usces_action_acting_transaction). Unauthenticated attackers can store arbitrary 'reserve' key/value pairs as order metadata during a public checkout, then invoke the callback with an attacker-chosen 'option' parameter to select and unserialize that metadata without any provider signature, source-address, transaction-identity or ownership check. A POP chain is present in the TCPDF library bundled with the plugin itself, so no additional plugin or theme is required. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, including wp-config.php, which can lead to remote code execution when an attacker re-runs the WordPress installer against a database they control. Successful exploitation is contingent on an admin printing an invoice to trigger file deletion.

### CVE-2026-52775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-05T00:17:20.520 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.6, YesWiki through the latest development branch contains a SQL injection vulnerability in ReactionManager::deleteUserReaction() that allows any authenticated user to inject arbitrary SQL via the {idreaction} and {id} URL path parameters. The parameters are concatenated directly into a SQL LIKE clause without escaping or parameterization. This issue has been patched in version 4.6.6.

### CVE-2026-57163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T18:17:54.547 |

PJSIP is a free and open source multimedia communication library written in C. Prior to commit c4a151a, a stack buffer overflow exists in the GnuTLS TLS backend when parsing the Subject Alternative Name extension of a peer certificate (tls_cert_get_info() in ssl_sock_gtls.c). Only GnuTLS builds are affected (--with-gnutls); OpenSSL and Apple SecureTransport/Network.framework builds are not affected. While extracting certificate information after a TLS handshake, an incorrect buffer-size value can cause an oversized SubjectAltName entry to be written past the end of a fixed-size stack buffer. A network-positioned attacker presenting a crafted certificate — a malicious server to a connecting client, or a malicious client to a server that requests certificates — can trigger this during the TLS handshake, before any SIP-level authentication. Impact may range from unexpected application termination to control flow hijack/memory corruption. This issue has been patched via commit c4a151a.

### CVE-2026-57162

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T18:17:54.360 |

PJSIP is a free and open source multimedia communication library written in C. Prior to commit a1b707c, a stack buffer overflow exists in the SRTP/SDES media transport when processing a=crypto attributes during SDP offer/answer (sdes_encode_sdp() in transport_srtp_sdes.c). This affects applications with SRTP enabled (use_srtp optional or mandatory, using SDES keying). During media negotiation, the crypto attributes from the remote SDP are collected into a fixed-size array without bounding their number; a remote peer that includes an excessive number of a=crypto attributes in a single media description can write past the end of that array on the stack. This is reachable from an incoming SIP INVITE during offer/answer, before application-level authentication. Impact may range from unexpected application termination to control flow hijack/memory corruption. Applications that do not enable SRTP are not affected. This issue has been patched via commit a1b707c.

### CVE-2026-57161

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-04T18:17:54.193 |

PJSIP is a free and open source multimedia communication library written in C. Prior to commit acc03b5, a stack buffer overflow exists in PJSUA when processing Service-Route headers in a registration response (update_service_route() in pjsua_acc.c). This affects applications that register using the PJSUA/PJSUA2 account API (the default registration path). The Service-Route URIs from a 2xx response to REGISTER are stored into a fixed-size array without bounding the number of headers; a registrar that returns an excessive number of Service-Route headers can write past the end of the array on the stack. The values written are internal pointers rather than arbitrary data, so the most likely impact is unexpected application termination (denial of service), though memory corruption cannot be excluded. The malicious response may come from a compromised or malicious registrar, or — over unprotected transports — a spoofed response. This issue has been patched via commit acc03b5.

### CVE-2026-18486

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-04T17:16:56.420 |

IBM ContextForge MCP Gateway <= v1.0.7 MCP Context Forge could allow a remote authenticated attacker to obtain sensitive credentials and escalate privileges due to improper validation of jq filters.

### CVE-2026-19298

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T16:17:21.900 |

IBM Langflow OSS 1.0.0 through 1.11.2 could allow a remote authenticated attacker to execute arbitrary code due to an authorization bypass in the flow build process.

### CVE-2026-85684

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-04T15:17:46.077 |

marker through 2.0.0 contains a path traversal vulnerability in the FastAPI /marker/upload handler that fails to sanitize the file.filename parameter. Unauthenticated attackers can supply filenames containing directory traversal sequences to write arbitrary files to any location or delete existing files on the system.

### CVE-2026-86196

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-05T13:18:14.980 |

Grav API plugin versions before 1.0.20 build password reset links from the untrusted Host header in the forgot-password endpoint, allowing unauthenticated attackers to redirect reset tokens to attacker-controlled domains. Attackers can send password reset requests for any account with a malicious Host header, intercept the reset token from victim emails, and complete account takeover including super-admin accounts.

### CVE-2026-86195

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-05T13:18:14.853 |

grav-plugin-api versions before 1.0.20 contain a privilege escalation vulnerability in the InvitationsController where the stripSuperFlags() method only removes nested super flags but fails to strip dot-keyed equivalents like api.super. A non-super user manager with api.access and api.users.write permissions can create an invitation with a dot-keyed super flag in the access payload that bypasses the guard and persists to the new account. Attackers can accept the invitation through the public endpoint without real invitee interaction to create a super-admin account and immediately receive a valid JWT for full site control.

### CVE-2026-86193

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-05T13:18:14.593 |

grav-plugin-api before 1.0.20 fails to validate group-inherited super permissions in user-management guards, allowing non-super user managers to modify super-admin accounts. Attackers with api.access and api.users.write can patch password fields on group-super accounts to gain full administrative control.

### CVE-2026-86177

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-05T11:16:46.397 |

Pterodactyl Panel before 1.14.1 fails to validate action-specific permissions in scheduled task creation, allowing subusers with only schedule.update permission to execute arbitrary console commands. Attackers can create and immediately trigger scheduled tasks that run game-server console commands, control server power state, or create backups without proper authorization checks.

### CVE-2026-86173

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-05T11:16:45.850 |

MindsDB through 26.1.0 contains a server-side request forgery vulnerability in the web crawler handler that allows unauthenticated attackers to fetch arbitrary URLs by supplying caller-controlled URLs to CrawlerTable.list. Attackers can bypass the allowlist control by exploiting the default empty configuration and access internal services and cloud metadata endpoints without authentication.

### CVE-2026-86169

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-09-05T11:16:45.703 |

Axolotl through 0.18.0 contains a remote code execution vulnerability in the multipack patch path where trust_remote_code defaults to None instead of False, causing the security guard to be bypassed. Attackers can execute arbitrary Python code by crafting a malicious Hugging Face model repository selected as base_model, which is loaded with hardcoded trust_remote_code=True during AutoModelForCausalLM.from_pretrained.

### CVE-2026-77393

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-04T22:17:18.333 |

In Ignition 8.1.53 and earlier, the Gateway "Create Project Role(s)" setting shipped blank, which permitted any authenticated user to create projects (if they can execute gateway scripts). Ignition 8.1.54 restricts project creation to Designer sessions and no longer relies on this setting. The 8.3 series is not affected.

### CVE-2026-46636

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-04T22:17:17.360 |

Twig is a template language for PHP. From version 1.0.0 to before version 3.27.0, SecurityPolicy::checkMethodAllowed() unconditionally whitelists all method calls on instances of Twig\Markup. Twig\Markup is not final, so subclasses inherit the bypass. An application that passes an object of a Markup-derived class into a sandboxed template (typically to mark a chunk of HTML as safe) inadvertently exposes every public method of that subclass to template authors, regardless of the configured allowedMethods list. This issue has been patched in version 3.27.0.

### CVE-2026-85786

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-04T20:17:33.153 |

Improper handling of highly compressed data in Amazon ion-java before 1.12.1 might allow remote attackers to cause a denial of service via a crafted compressed Ion document that expands to an arbitrarily large size upon decompression due to insufficient coverage of the GZIP auto-decompression opt-out introduced for CVE-2026-75936.



To remediate this issue, users should upgrade to version 1.12.1.

### CVE-2026-82538

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T18:18:01.357 |

ILIAS before versions 9.22, 10.10, and 11.3 contains a SQL injection vulnerability in the repository trash table where the table navigation sort field from HTTP requests is passed directly into the ORDER BY clause of a SQL query without validation against declared sortable columns. Authenticated users with write permission on any container can inject arbitrary SQL through the sort parameter, and because multi-statement execution is enabled in the database layer, stacked queries enable full database read and write access as well as administrator account takeover.

### CVE-2026-53758

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-04T18:17:52.640 |

Emlog is an open source website building system. In versions 2.6.29 and prior, article content is processed by Parsedown without enabling safe mode, which means raw HTML including <script> tags embedded in Markdown is passed through unescaped. The output is rendered with no additional sanitization, resulting in stored XSS visible to all site visitors. At time of publication, there are no publicly known patches.

### CVE-2026-85699

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:48.967 |

jina-ai reader contains a server-side request forgery vulnerability where URL validation is performed only on the initial request but not re-applied to subsequent redirect hops. Attackers can craft a public URL that redirects to internal network addresses or cloud metadata endpoints, allowing the server to fetch and return the target's response body to the attacker.

### CVE-2026-85691

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:47.097 |

MegaParse 0.0.55 contains an unauthenticated server-side request forgery vulnerability in the POST /v1/url endpoint that fetches caller-supplied URLs server-side. Attackers can supply internal service URLs or metadata endpoints without authentication to read their responses directly from the JSON response.

### CVE-2026-85687

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-04T15:17:46.507 |

surya 0.22.1 screenshot server contains an unauthenticated arbitrary file read vulnerability in the /info, /page, and /process routes that accept raw file_path parameters. Attackers can read any image or PDF file on the host by supplying arbitrary file paths to Image.open or pypdfium2.PdfDocument, obtaining rendered contents as base64 and using /info as an existence oracle.

### CVE-2026-85686

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:46.360 |

ms-swift 4.5.2 contains a server-side request forgery vulnerability in the swift deploy OpenAI-compatible API that fetches multimodal media URLs without validation or redirect filtering. Unauthenticated attackers can supply arbitrary image_url, audio_url, or video_url parameters to make the server issue requests to internal services and cloud metadata endpoints.

### CVE-2026-85685

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:46.220 |

AgentScope through 2.0.7.post1 contains a path traversal vulnerability in LocalWorkspace.add_skill that copies arbitrary server directories into the agent workspace via an unconfined source path parameter. Attackers can supply any directory path in the skill_path request parameter to copy files into the skills directory, making them accessible through the workspace skill listing.

### CVE-2026-85675

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:45.763 |

OWL's DocumentProcessingToolkit contains a server-side request forgery vulnerability in the extract_document_content tool that fetches caller-supplied URLs with no scheme, host, or IP filtering. Attackers can inject malicious URLs through prompt injection to make the server fetch internal resources, with responses returned to the agent context.

### CVE-2026-85673

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:45.440 |

LLaMA-Factory contains a server-side request forgery vulnerability in the OpenAI-compatible API multimodal media URL handler that allows unauthenticated attackers to bypass SSRF validation. The check_ssrf_url guard validates URLs once but requests.get follows redirects and re-resolves DNS without re-validation, enabling attackers to use HTTP redirects or DNS rebinding to access internal addresses and cloud metadata endpoints.

### CVE-2026-85671

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-04T15:17:45.150 |

QAnything 2.0.0 contains an authentication bypass vulnerability in the /api/local_doc_qa/get_file_base64 and /api/local_doc_qa/get_doc endpoints that allows unauthenticated attackers to access any uploaded file or document. Attackers can enumerate file identifiers through unauthenticated endpoints and retrieve base64-encoded files or parsed document chunks without ownership verification to disclose cross-tenant knowledge base content.

### CVE-2026-85668

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-04T15:17:44.693 |

Xinference (affected commit 4a94832, v3.x) contains an unauthenticated arbitrary-path file read vulnerability in the POST /v1/models/llm/auto-register endpoint, which accepts a caller-supplied model_path parameter without authentication or path confinement. The endpoint reads and parses config.json, tokenizer_config.json, and chat_template.jinja files at the supplied path and reflects the parsed content back to the caller, allowing an unauthenticated attacker to probe the server filesystem and extract content of files with those names in any directory.

### CVE-2026-85666

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:44.397 |

OGX (formerly Llama Stack, affected at commit fbe8e0f) contains an unauthenticated server-side request forgery vulnerability in the OpenAI-compatible POST /v1/responses endpoint. MCP tool definitions accept a server_url parameter (along with headers and authorization values) that is fetched server-side without destination validation; the existing validate_url_not_private() guard used for other URL inputs is not applied to server_url. On the default starter configuration, which runs without authentication, a remote unauthenticated attacker can cause the server to open connections to arbitrary internal addresses (including cloud metadata endpoints such as http://169.254.169.254/) and forward attacker-supplied headers and bearer tokens to those destinations.

### CVE-2026-85664

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-04T15:17:44.097 |

Chroma 1.5.9 fails to validate maximum bounds on HNSW index parameters max_neighbors, ef_construction, and ef_search in collection-create requests. Unauthenticated attackers can supply arbitrarily large parameter values to exhaust server memory and cause denial of service during index compaction.

### CVE-2026-85626

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-04T15:17:43.040 |

git-mcp-server 2.15.1 contains an argument injection vulnerability in the ref and object parameters of git_log, git_diff, and git_show tools that lack leading-dash validation. Attackers can inject git command-line options like --output= to write files outside the repository to arbitrary paths accessible by the process.

### CVE-2026-85623

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T15:17:42.587 |

goose 1.37.0 executes arbitrary commands from recipe stdio extensions and retry.checks without security inspection. Attackers can distribute malicious recipes that execute shell commands as the user running goose, bypassing the recipe security scan which does not inspect extensions or retry configurations.

### CVE-2026-85608

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:41.707 |

Douyin_TikTok_Download_API through 4.1.2 contains a server-side request forgery vulnerability in the /api/download and /api/hybrid/video_data endpoints that allows unauthenticated attackers to fetch arbitrary URLs by supplying a url query parameter. Attackers can request internal services including cloud metadata endpoints and retrieve response bodies containing sensitive credentials through error messages.

### CVE-2026-85607

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T15:17:41.547 |

Blinko 1.8.7 contains an authorization bypass (IDOR) vulnerability in multiple tRPC procedures (message.list, message.update, message.delete, message.clearAfter in server/routerTrpc/message.ts and conversation.clearMessages in server/routerTrpc/conversation.ts). Although these procedures require authentication, they query the database by caller-supplied conversation or message ID without verifying that the resource belongs to the requesting account. Any authenticated user can therefore read another user's full AI chat history, modify individual message content, and delete or wipe entire conversations by enumerating sequential integer IDs.

### CVE-2026-85606

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:41.393 |

firecrawl-mcp-server 3.20.2 contains an arbitrary local file read vulnerability in the firecrawl_parse tool that accepts unconstrained filePath arguments without directory containment validation. Attackers can supply absolute paths or directory traversal sequences to read sensitive files like credentials and environment variables, which are then uploaded and returned to the model context.

### CVE-2026-86185

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-05T12:16:49.240 |

Bilibili Desktop through 1.18.0 disables TLS certificate verification process-wide and executes unsigned remote JavaScript configuration without integrity checks. An attacker in an on-path network position can intercept configuration fetches, inject arbitrary JavaScript executed in the renderer with access to the privileged IPC bridge, and execute system commands or steal login credentials.

### CVE-2026-82684

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T22:17:18.683 |

Tycon Systems TPDIN-Monitor-WEB3 versions 2.2.9 and prior are vulnerable to a Missing Authorization vulnerability. This could allow an attacker to extract system credentials, configurations, or flash contents.

### CVE-2026-82712

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-04T21:17:26.100 |

Tycon Systems TPDIN-Monitor-WEB3 versions 2.2.9 and prior are vulnerable to a cross-site request forgery vulnerability. This could allow an attacker to perform state changing operations on the device.

### CVE-2026-50553

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-22` |
| Published | 2026-09-04T18:17:52.203 |

Note Mark is an open-source note-taking application. Prior to version 0.19.5, Note Mark validates book and note slug values with the OpenAPI/huma tag pattern:"[a-z0-9-]+". huma compiles this with regexp.MustCompile(s.Pattern) and tests it with patternRe.MatchString(str), an UNANCHORED match. Because the pattern is not anchored (^...$), any string that merely CONTAINS one [a-z0-9-] substring passes validation. A slug such as ../../../../../../tmp/escape is accepted and stored verbatim. The data-export CLI commands (note-mark migrate export and note-mark migrate export-v1) join these unsanitized slugs straight into the output path with path.Join / filepath.Join, then os.MkdirAll the directory and os.Create the note file. path.Join resolves the ../ segments, so the note content file is written OUTSIDE the configured export directory. The export process commonly runs as root (default in Docker / bare-metal admin usage), so this is a root-privilege arbitrary directory create + file write. This issue has been patched in version 0.19.5.

### CVE-2026-19305

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T16:17:24.323 |

IBM Langflow OSS 1.0.0 through 1.11.2 could allow a remote attacker to obtain sensitive information due to server-side request forgery.

### CVE-2026-86095

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-04T23:18:03.220 |

Unidata netcdf-c through 4.10.1 contains an out-of-bounds write vulnerability in NC4_HDF5_inq_attname() that copies HDF5 attribute names into a fixed 256-byte buffer without length validation. Attackers can craft HDF5 files with oversized attribute names to overflow the destination buffer, causing memory corruption and crashes when applications enumerate attribute names.

### CVE-2026-80119

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-497` |
| Published | 2026-09-04T19:17:28.857 |

PassMark PerformanceTest before 11.1 build 1012, BurnInTest before 11.1 build 1000, and OSForensics before 11.1 build 1016 contain an information disclosure vulnerability in DirectIo64.sys that allows unauthenticated local attackers to dump complete physical memory contents by supplying a caller-controlled file path to an exposed IOCTL. Attackers can issue a single IOCTL call to trigger the driver to iterate all physical memory ranges via MmGetPhysicalMemoryRanges and map each page through ZwMapViewOfSection on the PhysicalMemory section object, writing a full RAM image to an attacker-specified path in the SYSTEM context, bypassing user-mode ACLs and exposing LSASS working set, process memory, and cryptographic material from all running processes.

### CVE-2026-80116

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-09-04T19:17:28.420 |

PassMark PerformanceTest before 11.1 build 1012, BurnInTest before 11.1 build 1000, and OSForensics before 11.1 build 1016 contain a privilege escalation vulnerability in DirectIo64.sys that allows local users to modify hardware configuration by exploiting exposed IOCTLs with no validation on device selection, register offset, or value. Attackers can obtain a device handle and issue arbitrary PCI configuration space read/write operations to enable Bus Master DMA on any PCI device, halt storage controller I/O by clearing command registers, or remap Base Address Registers to redirect DMA to an attacker-chosen physical address.

### CVE-2026-80114

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-04T19:17:28.140 |

PassMark PerformanceTest before 11.1 build 1012, BurnInTest before 11.1 build 1000, and OSForensics before 11.1 build 1016 contain a hard-coded credentials vulnerability in DirectIo64.sys that allows local attackers to perform arbitrary physical memory writes by extracting an 8-byte key embedded as a hardcoded literal in the distributed binary and computing valid MD5 authentication tags for arbitrary IOCTL write requests. Attackers can additionally bypass a secondary validation gate by using the driver's own bit-clear IOCTL to clear a single bit in the gating instruction's displacement byte, causing all subsequent write requests to skip MAC verification, size checks, and Vendor ID checks entirely.

### CVE-2026-80112

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-04T19:17:27.823 |

PassMark PerformanceTest before 11.1 build 1012, BurnInTest before 11.1 build 1000, and OSForensics before 11.1 build 1016 contain an improper access control vulnerability in the DirectIo64.sys kernel driver that allows unprivileged local users to perform privileged hardware operations by opening a handle to the device object created without a security descriptor. Attackers can issue IOCTLs through the permissive default Windows ACL applied to the device to access restricted hardware operations regardless of privilege or integrity level.

### CVE-2026-85656

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-04T18:18:06.133 |

An OS command injection issue in the log4j-cve-2021-44228-hotpatch package in Amazon Linux before 1.3-9 might allow a local user to execute arbitrary commands with root privileges via a Java process whose executable path contains embedded newline characters.

### CVE-2026-85690

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:46.947 |

Plandex 2.2.1 contains a path traversal vulnerability in the ApplyFiles function that allows attackers to write files outside the project directory. Attackers can influence model output through poisoned repository files or attacker-controlled context to write to arbitrary locations like shell rc or cron files, achieving code execution.

### CVE-2026-85674

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-04T15:17:45.597 |

aider (aider-chat) automatically loads a .aider.conf.yml configuration file from the root of the git repository it is launched in. A crafted repository can set test-cmd (executed at startup) or lint-cmd (executed on the first file edit), which aider runs through a shell (subprocess with shell=True) without any user confirmation, LLM interaction, or API key. Consequently, a user who clones and runs aider inside an attacker-supplied repository achieves arbitrary command execution on their machine. The behavior is long-standing and was confirmed on 0.86.3.dev (current main).

### CVE-2026-6958

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-04T15:17:35.360 |

Acunetix 25.11.251107123 for Windows contains a local privilege escalation vulnerability in the Web Vulnerability Scanning Engine (wvsc.exe) that allows low-privileged local attackers to execute arbitrary code as SYSTEM by exploiting a missing hardcoded directory path for OpenSSL-related files. Attackers can create the missing directory, place a malicious file at the expected path, and cause the SYSTEM-level wvsc.exe process to load and execute it, resulting in full privilege escalation.

### CVE-2026-80118

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73;CWE-476;CWE-497` |
| Published | 2026-09-04T19:17:28.710 |

PassMark PerformanceTest before 11.1 build 1012, BurnInTest before 11.1 build 1000, and OSForensics before 11.1 build 1016 contain an unauthenticated physical memory disclosure in DirectIo64.sys, reachable by unprivileged local users through a single IOCTL with no caller-identity check. The handler writes a crash-dump-format (PAGEDU64) image of all physical memory to a caller-supplied file path in the SYSTEM context, allowing a standard user to create files in locations they cannot otherwise write and to recover memory belonging to processes of other users. The image is preceded by a header that exposes the kernel loaded-module list, active-process list and PFN database pointers, defeating KASLR. The same handler also dereferences the return value of an internal kernel-structure locator without a NULL check; that locator returns NULL on three distinct failure paths, and a kernel crash results on builds where any of those paths is taken.

### CVE-2026-57159

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-09-04T18:17:53.313 |

PJSIP is a free and open source multimedia communication library written in C. Prior to commit 673b978, a remote out-of-bounds read and write can occur in the SDP negotiator when the remote payload-type map maintenance feature is enabled. assign_pt_and_update_map() in pjmedia/src/pjmedia/sdp_neg.c uses payload-type numbers taken from a remote SDP offer or answer to index fixed-size internal tables without sufficient bounds validation, so a crafted remote SDP can cause memory access outside those tables. The practical impact is memory corruption and denial of service; code execution is not demonstrated. This path is only reached when PJMEDIA_SDP_NEG_MAINTAIN_REMOTE_PT_MAP is enabled. The default is disabled, so default builds are not affected; the feature is an interoperability option that integrating products may enable. This issue has been patched via commit 673b978.

### CVE-2026-85651

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T15:17:43.347 |

Trigger.dev versions before 4.5.2 fail to validate environment membership during run replay operations, allowing authenticated attackers to inject task runs into arbitrary environments. Attackers can replay their own runs into other organizations' or projects' environments to consume victim resources and pollute run history.

### CVE-2026-52771

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-05T00:17:19.963 |

YesWiki is a wiki system written in PHP. From version 4.2.0 to before version 4.6.6, ApiController::deletePage() interpolates a page tag retrieved from the database into a DELETE FROM …_links WHERE to_tag = '$tag' query without escaping. The page tag is attacker-controlled — the POST /api/pages/{tag} API accepts arbitrary URL-encoded values, including single quotes, and stores them. A low-privilege authenticated user can therefore create a page whose tag is a SQL fragment, make the page non-orphaned via the standard {{include page="…"}} link mechanism, and then invoke the delete endpoint to execute arbitrary SQL inside the wiki database - including time-based blind data exfiltration from any table. This issue has been patched in version 4.6.6.

### CVE-2026-52769

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-05T00:17:19.683 |

YesWiki is a wiki system written in PHP. From version 4.6.2 to before version 4.6.6, the POST /api/forms/{formId}/actor/inbox route - exposed publicly with acl:"public" - accepts an HTTP Signature header whose keyId parameter is a URL. HttpSignatureService::verifySignature() parses the header and immediately makes a server-side HTTP GET to that URL, before any cryptographic verification or URL validation. An unauthenticated remote attacker can therefore make YesWiki issue arbitrary outbound HTTP requests to any host the server can reach - internal services, cloud-metadata endpoints (169.254.169.254), intranet-only admin panels, etc. - and read enough back via timing and error-message oracles to scan ports, enumerate services, and (on a real cloud instance) reach IAM metadata. The only deployment-side precondition is that ActivityPub be enabled on at least one Bazar form. This issue has been patched in version 4.6.6.

### CVE-2026-86098

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-04T23:18:03.687 |

ntop nDPI versions before 6.0 contain a heap buffer overflow vulnerability in the ndpi_json_string_escape function that writes beyond caller-supplied buffer boundaries. Attackers can trigger the overflow by supplying crafted network packet data including TLS SNI, HTTP headers, or DNS names that reach the vulnerable function, causing heap corruption.

### CVE-2026-57164

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-04T18:17:54.703 |

PJSIP is a free and open source multimedia communication library written in C. Prior to commit 8d5956a, a heap buffer overflow exists in the PJLIB-UTIL HTTP client (http_client.c) when buffering an HTTP response body. This affects applications that use the PJLIB-UTIL HTTP client to receive a whole response body at once (a completion callback with no incremental on_data_read callback). When growing the response buffer, an incorrect size calculation based on the server-supplied Content-Length can leave the buffer too small, causing response data to be written past the end of the allocation. A malicious or man-in-the-middle HTTP server can trigger this with a crafted response; impact may range from unexpected application termination to memory corruption. Applications that consume the response incrementally (via on_data_read), or that only connect to trusted servers, are not affected. This issue has been patched via commit 8d5956a.

### CVE-2026-86145

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-424` |
| Published | 2026-09-05T06:17:10.370 |

PCRE2 before 10.48 allows a pcre2_dfa_match out-of-bounds write because reuse of a cached workspace block, in a recursive DFA matching workspace, lacks a size check (even though a newly allocated block, for the same purpose, does have a size check). This outcome requires an attacker-controlled regular expression, or a recursive pattern in conjunction with a small heap limit (this can be set through the API).

### CVE-2026-52767

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-05T00:17:19.540 |

YesWiki is a wiki system written in PHP. From version 4.6.2 to before version 4.6.6, HttpSignatureService::verifySignature() checks the result of PHP's openssl_verify() with a loose boolean negation - if (!openssl_verify(...)) { throw ... }. PHP's openssl_verify has four possible return values: 1, 0, -1, and "false". The -1 row is the bypass: PHP's truthiness rules make -1 a truthy value, so !(-1) === false, the throw is skipped, and the controller proceeds to processActivity(). Any condition that makes OpenSSL's EVP_VerifyFinal() return -1 triggers the bypass. The reachable consequence is the controller silently treats a failed verification as success and processes the attacker's payload. This issue has been patched in version 4.6.6.

### CVE-2026-53761

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-04T18:17:52.920 |

Frappe CRM is an open-source customer relationship management tool. Prior to version 1.73.0, there is an authentication bypass vulnerability via logged invitation keys in crm/api. This issue has been patched in version 1.73.0.

### CVE-2026-85730

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606;CWE-835` |
| Published | 2026-09-04T16:18:23.417 |

smol-toml is a small, fast, and correct TOML parser and serializer. Prior to 1.7.1, parse() can enter an infinite loop when a value inside an array or inline table is followed by a comment with no trailing newline. In src/util.ts, skipUntil() calls indexOfNewline(), receives -1 at the end of input, and resets the cursor to the beginning of the string instead of leaving the structure scan. The parser then hangs indefinitely and can consume a service's processing capacity when an application parses attacker-controlled TOML. This issue is fixed in version 1.7.1.

### CVE-2026-77822

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T16:17:59.550 |

IBM ContextForge MCP Gateway could allow a remote authenticated attacker to obtain sensitive information due to server-side request forgery via DNS rebinding.

### CVE-2026-82728

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-04T15:17:35.943 |

Allocation of Resources Without Limits or Throttling vulnerability in elixir-mint mint allows a remote HTTP server to exhaust memory on the client host and cause a denial of service.

Two HTTP/1 response-parser states accumulate server data without any cap. In lib/mint/http1.ex, decode_status_line/4 stores the unconsumed data in conn.buffer when the status line is incomplete, and decode_body/5 does the same for an unterminated chunk-extension line. Both wait for a CRLF the server never has to send, and conn.buffer is prepended to every subsequent socket message. The :max_header_list_size budget is wired only into decode_headers/5 and decode_trailer_headers/4, so neither of these states is covered by it. A malicious server, or one reached through an attacker-controlled redirect or a fetched URL, streams bytes indefinitely until the BEAM node is killed by the operating system out-of-memory handler. The chunk-extension variant is reached after a valid status line and a complete, valid header section, so an intermediary inspecting only headers sees an ordinary 200 response.

This issue affects mint: from 0.1.0 before 1.10.0.

### CVE-2026-61699

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-299;CWE-672` |
| Published | 2026-09-04T20:17:24.347 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh VPN. Prior to version 0.7.1, revocation is the only in-band mechanism that isolates a compromised/offboarded host from a Nebula mesh. Because the blocklist never reaches any peer's config.yml, a Blocked host retains full overlay reachability to every peer under its CA (and internal services on the mesh) for up to 30d (agent) / 365d (mobile). An attacker who exfiltrates host.key+host.crt can run stock slackhq/nebula directly, ignore the agent's 403/410 poll responses, and stay connected after the operator revokes the host. Operator-visible state (UI shows blocked, audit log records it) is misleading. This issue has been patched in version 0.7.1.

### CVE-2026-18221

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-04T17:16:56.150 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to gain unauthorized access due to improper validation of client-supplied authentication parameters.

### CVE-2026-18175

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-04T17:16:56.010 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to manipulate database transactions due to improper authorization in the DDM target dispatcher.

### CVE-2026-19303

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T16:17:24.077 |

IBM Langflow OSS 1.0.0 through 1.11.2 could allow a remote authenticated attacker to delete arbitrary local files or directories due to improper limitation of a pathname to a restricted directory.

### CVE-2026-86140

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-05T05:17:12.877 |

In libxml2 before 2.15.4, xmlSnprintfElements in valid.c has a strcat stack-based buffer overflow.

### CVE-2026-53932

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-04T20:17:23.570 |

laravel-backup-restore restores database backups made with spatie/laravel-backup. Prior to version 1.9.4, a crafted backup archive can trigger OS command injection during database restore. This issue has been patched in version 1.9.4.

### CVE-2026-63464

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862;CWE-918` |
| Published | 2026-09-04T20:17:24.730 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh VPN. From version 0.6.0 to before version 0.7.2, non-admin operators (role user) can set allow_private: true on their own managed webhook subscription (POST/PATCH /api/v1/webhook-subscriptions). No admin check exists on this field. At delivery time, allow_private switches the dispatcher to an unguarded HTTP client, bypassing the private/loopback/link-local SSRF guard — letting a low-privilege operator make the server request internal addresses. This issue has been patched in version 0.7.2.

### CVE-2026-19306

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T16:17:24.793 |

IBM Langflow OSS 1.0.0 through 1.11.2 allows an authenticated attacker to read arbitrary files from the server filesystem — including server secret material (secret_key, JWT signing keys, the application database, /proc/self/environ, and other tenants' upload directories) — by supplying absolute paths or traversal sequences in the files parameter of an authenticated build request. The file contents were embedded as text attachments in the language model prompt and transmitted to the configured model endpoint, resulting in confidential data exfiltration. This bypassed the LANGFLOW_RESTRICT_LOCAL_FILE_ACCESS=true containment boundary, which was enforced for other file-reading components but not for the Chat Input to Message attachment pipeline.

### CVE-2026-19304

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T16:17:24.200 |

IBM Langflow OSS 1.0.0 through 1.11.2 could allow a remote authenticated attacker to obtain sensitive information from internal services due to a URL parser discrepancy.

### CVE-2026-19283

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T16:17:21.777 |

IBM Observability with Instana (Agent) Build 1.0.303 through 1.0.323 IBM Instana Agent Operator could allow an authenticated remote attacker to obtain sensitive information, caused by missing destination namespace validation when copying etcd mTLS client credentials from the openshift-etcd system namespace into an attacker-controlled namespace.

### CVE-2026-18905

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T16:17:21.517 |

IBM ContextForge MCP Gateway (`mcp-contextforge-gateway`) <= v1.0.6 MCP Context Forge could allow a remote authenticated attacker to obtain sensitive information due to a DNS rebinding vulnerability during tool invocation.

### CVE-2026-85619

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T15:17:42.003 |

AppFlowy-Cloud 0.9.64 fails to verify that requested collab objects belong to the workspace in authorization checks, allowing attackers to access documents and database rows across workspaces. Attackers can supply a victim's object ID with their own workspace ID to bypass access controls and read, modify, or delete cross-workspace data.

### CVE-2026-81832

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-04T15:17:35.550 |

IBM App Connect Enterprise 13.0.1.0 through 13.0.8.1, and 12.0.1.0 through 12.0.12.28 and IBM Integration Bus for z/OS 10.1.0.0 through 10.1.0.7 SAP Adapter is vulnerable to an XML external entity (XXE) attack.

### CVE-2026-52770

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-05T00:17:19.827 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.6, YesWiki’s public Bazar entry-listing APIs are vulnerable to unauthenticated SQL injection in numeric query / queries filters. For Bazar fields whose value structure is numeric, YesWiki escapes the attacker-controlled filter value but inserts it into SQL without quotes or numeric validation. An unauthenticated attacker can inject boolean SQL expressions and infer database contents from whether entries are returned. This issue has been patched in version 4.6.6.

### CVE-2026-61686

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-04T18:17:55.437 |

SolidInvoice is an open-source invoicing platform. Prior to version 3.0.1, the `DataGrid` LiveComponent deserializes a `context` prop value using PHP's `unserialize()` after receiving it from the client. Because the prop is marked `writable: true`, an authenticated attacker can supply an arbitrary PHP serialized payload. Version 3.0.1 fixes the issue.

### CVE-2026-19534

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-252` |
| Published | 2026-09-04T18:17:51.647 |

undici's WebSocket client crashes the whole Node.js process during the opening handshake when a server responds with a subprotocol that the client never requested. A default WebSocket connection sends no subprotocol, but if the server's 101 response includes a Sec-WebSocket-Protocol header, undici dereferences a null value while checking it against the requested list and throws an uncaught TypeError. Because that code runs inside a microtask with no surrounding error handling, the exception propagates and terminates the process under Node's default behavior, instead of gracefully failing the connection as required by the WebSocket protocol. Any application that opens a WebSocket to an attacker-controlled or compromised server, or over a plaintext connection subject to a machine-in-the-middle, can be crashed remotely without authentication in the default configuration. This affects undici versions from 6.7.0 up to 6.28.1, from 7.0.0 up to 7.29.1, and from 8.0.0 up to 8.10.2. Users should upgrade to undici 6.28.1, 7.29.1, or 8.10.2.

### CVE-2021-44320

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-04T18:17:44.397 |

Parrot AR.Drone version 1 and 2 does not employ a suitable mechanism to prevent denial-of-service (DoS) attacks. An attacker can harm the device availability (i.e., video streaming and control) by using tool to perform an IPv4 flood attack. Verified attacks includes SYN flooding and UDP flooding.

### CVE-2026-19300

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-04T16:17:22.167 |

IBM Langflow OSS 1.0.0 through 1.11.2 could allow a remote attacker to obtain sensitive information due to incomplete scrubbing of sensitive credential fields.

### CVE-2026-19205

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-09-04T15:17:33.360 |

Observable response discrepancy vulnerability in GastroMenum GastroMenum Web Panel allows Account Footprinting.

This issue affects GastroMenum Web Panel: before 31.08.2026.

### CVE-2026-86187

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-05T13:18:13.703 |

WWBN AVideo generates passwords for external-login accounts using rand() instead of a cryptographic generator, producing only 31-bit integers. Attackers with access to password hashes can recover plaintext passwords in minutes through offline brute-force attacks due to unsalted MD5-based hashing.

### CVE-2026-85152

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-04T17:17:02.717 |

undici 8.10.0 omits the destination origin from the cache and request-deduplication keys when the cache or deduplicate interceptor is composed directly onto a Client or Pool. Because the internal cache key falls back to an empty origin string, a cacheable or in-flight response from one upstream origin is returned for a request to a different, trusted origin whenever the method, path, and relevant headers match, which permits cross-origin information disclosure and persistent cache poisoning. The reporter demonstrated a full authentication bypass in which a JWT signed with an attacker-controlled key was accepted as belonging to a trusted issuer, and the trusted origin was never contacted. This is a regression introduced in 8.10.0 and affects undici versions from 8.10.0 up to 8.10.2. Applications using an Agent, which carries the origin in its dispatch options, are not affected. Users should upgrade to undici 8.10.2.

### CVE-2026-84961

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-04T17:17:02.227 |

undici's BalancedPool constructor passes its entire options object through an internal deep-clone that serializes and reparses the value as JSON. Because JSON cannot represent functions, any function-valued TLS option, such as a caller-supplied checkServerIdentity callback or a custom connector inside the connect option, is silently discarded before it reaches the TLS layer. As a result a peer whose certificate the application's custom checkServerIdentity was written to reject, but which still passes Node's default hostname and chain checks, is accepted when reached through BalancedPool. The Client, Pool, and Agent dispatchers are not affected because they extract the connect and tls options before cloning. This affects undici versions from 7.24.1 up to 7.29.1 and from 8.0.0 up to 8.10.2, and only when the application supplies a function-valued connect or tls option to BalancedPool. Users should upgrade to undici 7.29.1 or 8.10.2.

### CVE-2026-18489

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-488` |
| Published | 2026-09-04T17:16:56.550 |

IBM ContextForge MCP Gateway - Translate utility <= 1.0.8 MCP Context Forge could allow a remote attacker to obtain sensitive information from other sessions due to exposure of data elements to the wrong session.

### CVE-2026-83625

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T08:16:40.857 |

The Contact Form by Supsystic plugin for WordPress is vulnerable to Stored Cross-Site Scripting via IP Address Header in all versions up to, and including, 1.10.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. An unauthenticated attacker can first call the 'updateNonce' action — which is accessible without authentication due to its absence from the plugin's permission list — to obtain a valid nonce, then submit a contact form with a malicious payload in a spoofed IP header such as X-Forwarded-For.

### CVE-2026-78438

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:12.580 |

The W3 Total Cache plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via LazyLoad Background Mutator in all versions up to, and including, 2.10.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the "Lazy Load Images" feature with "Process background images" to be enabled, and the malicious comment to be approved by a moderator before execution is triggered.

### CVE-2026-77830

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:12.163 |

The Spam protection, Honeypot, Anti-Spam by CleanTalk plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content aria-label Placeholder in all versions up to, and including, 6.86 due to insufficient input sanitization and output escaping. This makes it possible for authenticated attackers, with custom-level access and above, to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is deliverable via unauthenticated comment submission and executes exclusively for non-logged-in visitors; if comment moderation is enabled, an approving moderator must first publish the comment before the script reaches other users.

### CVE-2026-19769

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:11.333 |

The Ninja Forms – The Contact Form Builder That Grows With You plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Repeater Child 'type' Confusion via Unmatched Array Key in all versions up to, and including, 3.15.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the Ninja Forms File Uploads add-on to be active, as the attack routes the unwhitelisted child entry through the File Uploads handler to write an attacker-supplied HTML file containing arbitrary JavaScript into any web-server-writable directory, including the site root, where it is served from the site's own origin.

### CVE-2026-18406

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:11.040 |

The SureForms – Contact Form Builder, AI Forms, Payment Form, Survey & Quiz plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Text Field Entity-Encoded Payload in all versions up to, and including, 2.12.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-16649

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:10.917 |

The Gravity Forms plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Post Body Field Value in all versions up to, and including, 2.10.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit survives save-time sanitization because wp_kses_post allows the required HTML tags and attributes, and the client-side tooltip script re-parses the browser-decoded aria-label value as innerHTML while only stripping script elements, leaving onerror and other event-handler attributes fully intact and executable.

### CVE-2026-15984

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T07:17:10.793 |

The QuickCal plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Custom Field Parameters in all versions up to, and including, 1.0.20 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce guarding the unauthenticated booked_add_appt AJAX action is publicly embedded on any page rendering the booking calendar shortcode, making it trivially obtainable by unauthenticated attackers without any prior account or privilege.

### CVE-2026-77263

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T06:17:09.950 |

The iubenda | All-in-one Compliance for GDPR / CCPA Cookie Consent + more plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content in all versions up to, and including, 3.13.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit works by embedding KSES-allowed markup such as abbr title attributes and HTML comments in a submitted comment so that the global strtr() substitution strips substrings from an inert tag, mutating it into an executable element such as an img onerror handler that runs in the WordPress origin for any visitor, including logged-in administrators.

### CVE-2026-77233

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-05T06:17:09.780 |

The iubenda | All-in-one Compliance for GDPR / CCPA Cookie Consent + more plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via AdSense Regex Rewrite in all versions up to, and including, 3.13.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability only manifests when the 'Secondary' parser engine is active (parser_engine=default); it does not exist under the default 'new' DOM-based parser engine.

### CVE-2026-86192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-05T13:18:14.443 |

SiYuan versions before v3.8.2 fail to properly filter private attribute-view cell values in the getAttributeViewKeys endpoint. Publish readers can retrieve hidden KeyValues payloads from rows bound to inaccessible documents, exposing private database contents without authorization.

### CVE-2026-86175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-05T11:16:46.123 |

NetBox through 4.7.0 fails to redact sensitive data source backend credentials in REST and GraphQL API responses. Authenticated users with only view permission can retrieve plaintext passwords and secret keys for Git and Amazon S3 backends through API endpoints, gaining unauthorized access to external repositories and storage buckets.

### CVE-2026-86116

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-05T10:16:42.713 |

Metabase versions before 0.63.1 fail to enforce data analyst permission checks on glossary API endpoints, allowing any authenticated user to create, modify, and delete glossary entries. Attackers can submit requests to POST, PUT, and DELETE glossary endpoints to tamper with instance-wide business glossary data without proper authorization.

### CVE-2026-86114

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-05T10:16:42.423 |

Arcane versions before 2.0.0 fail to properly restrict template operations, allowing default user role accounts to create, modify, and delete compose templates including instance-wide defaults. Attackers can inject malicious container configurations with privileged settings or host path mounts that execute with administrative privileges when deployed by administrators.

### CVE-2026-86113

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-05T10:16:42.273 |

BookWyrm through 0.9.1 contains an authorization bypass vulnerability in the edit_readthrough function that allows authenticated users to modify other users' reading records. Attackers can exploit sequential ReadThrough IDs to overwrite arbitrary users' start dates, finish dates, progress, and progress mode, affecting reading statistics and exported data.

### CVE-2026-86111

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-05T10:16:40.963 |

BookWyrm through 0.9.1 fails to validate user visibility permissions in the status edit endpoint, allowing authenticated attackers to read followers-only and direct-message reviews by enumerating sequential status IDs. Attackers can access the raw content of restricted statuses through the edit view, bypassing the privacy protections documented for these message types.

### CVE-2026-52762

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-05T00:17:18.607 |

YesWiki is a wiki system written in PHP. Prior to version 4.6.6, YesWiki Bazar contains a stored Server-Side Template Injection (SSTI) vulnerability in the semantic template feature that can be escalated to confirmed Remote Code Execution (RCE). An authenticated administrator can place arbitrary Twig expressions into the Semantic template (Twig) field (bn_sem_template), and that content is later executed server-side when public semantic endpoints are requested. This issue has been patched in version 4.6.6.

### CVE-2026-86097

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-04T23:18:03.547 |

PX4 Autopilot through 1.17.0 contains a null pointer dereference vulnerability in param_set_default_file() and param_set_backup_file() functions that allows attackers to crash the autopilot process. Attackers can invoke 'param select' or 'param select-backup' commands with no path argument from any PX4 shell to trigger the crash.

### CVE-2026-86091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T22:17:18.990 |

ntopng before 6.7.260717 fails to check user privileges in the pools bulk-delete endpoint, allowing authenticated non-administrators to delete all host pools and member bindings. Attackers can issue POST requests to the delete pools endpoint to irreversibly destroy every host pool, removing traffic policy bindings and visibility restrictions that may bypass security policies.

### CVE-2026-86090

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T22:17:18.840 |

ntopng before 6.7.260717 fails to perform authorization checks in the delete endpoints and recipients REST v2 handlers. Authenticated non-administrator users can issue POST requests to irreversibly delete all configured notification endpoints and recipients, silencing all alerts.

### CVE-2026-85787

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-04T21:17:27.057 |

An incomplete list of disallowed inputs in the SQL validation component in Amazon awslabs postgres-mcp-server before  version 1.1.7 might allow an unauthenticated actor to modify data beyond the read-only scope by placing crafted SQL into the content that is submitted when an authenticated user interacts with the MCP server.



To remediate this issue, users should upgrade to version 1.1.7 or above.

### CVE-2026-77847

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-04T21:17:25.710 |

Tycon Systems TPDIN-Monitor-WEB3 versions 2.2.9 and prior are vulnerable to a use of hard-coded credential vulnerability. This could allow an attacker to intercept sensitive information or credentials.

### CVE-2026-53604

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-212;CWE-316` |
| Published | 2026-09-04T20:17:23.437 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh VPN. Prior to version 0.3.8, the web handler renderMobileBundle passes the real *pki.CAResolver directly into mobilebundle.Build. Inside Build, resolver.LoadByID decrypts the CA's ed25519 private key into a *pki.CAManager, but Build never calls CAManager.Wipe() on any return path. As a result, when a mobile-bundle request goes through the web UI and Build returns — especially on error (missing network, invalid prefix, DB error, signing failure) — the plaintext CA private key remains on the Go heap, unwiped, until garbage collection. An attacker able to read process memory (core dump, swap, memory-scraping) can recover the CA signing key, which would allow minting arbitrary host certificates for the mesh. The API handler already does this correctly: it loads the CAManager, defer caMgr.Wipe(), and wraps it in caManagerResolver. Only the web path is affected. This issue has been patched in version 0.3.8.

### CVE-2026-53603

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312;CWE-522` |
| Published | 2026-09-04T20:17:23.287 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh VPN. Prior to version 0.3.8, Operator session tokens are stored in plaintext in the operator_sessions table (the token column is the PRIMARY KEY). The session token is a 32-byte random hex value sent directly in a cookie and valid for 24 hours. Anyone who can read the database (backup, snapshot, file copy, or SQL-level disclosure) obtains every active session token and can hijack operator sessions directly, with no further authentication. This issue has been patched in version 0.3.8.

### CVE-2026-85654

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-04T18:18:05.977 |

Improper neutralization of special elements used in a template engine in the CDK generator in Amazon awslabs.dynamodb-mcp-server before 2.1.6 might allow a context-dependent actor to execute arbitrary code on the host that deploys the generated application via crafted table, index, or attribute names in a data model file.

### CVE-2022-35499

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-04T16:17:19.963 |

In Trimble TM4WEB 21.4.0.4, the external bill viewer endpoint is vulnerable to reflected cross-site scripting via injection in a arbitrary parameter appended to the URL.

### CVE-2026-85700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-04T15:17:49.110 |

Onyx 4.6.6 fails to properly restrict access to custom tool credentials stored in custom_headers, allowing any authenticated user to read admin-defined API keys. Attackers with basic authentication can call GET /tool/{tool_id} or GET /tool endpoints to retrieve plaintext authorization headers and third-party API credentials, then use them to directly access upstream APIs.

### CVE-2026-85697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-04T15:17:48.670 |

Documenso 2.17.0 contains an access control vulnerability in the PDF-serving endpoint that fails to validate document visibility settings. Attackers with low privileges can read restricted documents within their team or cross-tenant by leveraging missing ownership validation on document data identifiers.

### CVE-2026-85693

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T15:17:47.397 |

Chatbot UI contains an authorization bypass vulnerability in the retrieval endpoint that allows authenticated attackers to access private file content belonging to other users by supplying arbitrary file UUIDs. The endpoint uses a service-role Supabase client that bypasses row-level security and fails to validate file ownership, enabling attackers to retrieve indexed content chunks from victim files through crafted POST requests.

### CVE-2026-85692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-04T15:17:47.243 |

Nightingale (n9e), as of commit 8362cbe (main branch, confirmed 2026-08-27), contains a server-side request forgery vulnerability in the isPublicIP function in aiagent/tools/http.go, the SSRF guard for the http_fetch AI-agent tool. The function only unwraps standard IPv4-mapped (::ffff:a.b.c.d) IPv6 addresses before checking them against the forbidden-range list, and does not classify 6to4 (2002::/16), NAT64 (64:ff9b::/96, 64:ff9b:1::/48), or deprecated site-local (fec0::/10) addresses. On a dual-stack or NAT64-enabled host, an attacker able to supply a URL to the http_fetch tool can bypass the guard by encoding a forbidden IPv4 address (such as the cloud instance-metadata endpoint 169.254.169.254) in one of these IPv6 forms to reach internal or metadata services.

### CVE-2026-85689

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-04T15:17:46.803 |

llmware 0.4.6 contains an SQL injection vulnerability in the collection-database layer (llmware/resources.py) where filter and lookup values are directly string-interpolated into SQL WHERE clauses without parameterization or escaping, in both the SQLite and PostgreSQL backends. The filter validator only checks keys against an allow-list and never sanitizes values. Attacker-controlled filter values reaching the public API via Library.block_lookup and Query.text_query_with_custom_filter / text_query_by_author_or_speaker can neutralize the intended filter to disclose rows the caller was scoped out of (cross-document/cross-collection disclosure); on PostgreSQL the flaw permits boolean- and UNION-based SQL injection.

### CVE-2026-85670

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-04T15:17:44.993 |

tokenizers (Hugging Face) is affected by an out-of-bounds buffer access in BpeBuilder::build (tokenizers/src/models/bpe/model.rs). When loading a tokenizer.json via Tokenizer::from_file/from_str, the builder sizes a scratch buffer to the longest vocabulary key, then writes each concatenated merge rule into it. A merge whose concatenated token exceeds the longest vocabulary key overruns the buffer, which Rust turns into a panic that aborts the process in Rust and FFI embeddings. This occurs at load time with no encoding required, so an attacker who supplies a crafted tokenizer.json can cause a denial of service. A secondary defect at the same location can cause a usize underflow (panic in debug, potential memory corruption in release) when continuing_subword_prefix is set and a merge token is shorter than the prefix. Observed in version 0.23.1.

### CVE-2026-85669

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-04T15:17:44.847 |

potpie through 2.0.0 fails to verify user ownership on the POST /conversations/{conversation_id}/code-changes/sync endpoint. Authenticated attackers can write arbitrary file changes into other users' conversations by supplying their conversation IDs, allowing unauthorized modification of pending changes.

### CVE-2026-85665

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:44.247 |

Bruno versions through 4.1.0 fail to validate file paths in request body declarations, allowing attackers to read arbitrary local files by using parent-directory traversal segments. When a collection is executed, attackers can craft a request with a body:file path containing ../ sequences that resolve outside the collection directory, causing the application to read and exfiltrate arbitrary files to attacker-controlled endpoints.

### CVE-2026-85624

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-04T15:17:42.737 |

Blinko 1.8.7 contains a cross-user private note disclosure vulnerability in the noteReferenceList procedure that performs no ownership verification on supplied note identifiers. Authenticated attackers can enumerate sequential note IDs and retrieve complete content of other users' private notes including attachments and tags.

### CVE-2026-85618

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-04T15:17:41.857 |

ConvertX 0.17.0 contains an arbitrary file read vulnerability in the xelatex converter that allows authenticated users to read files by uploading LaTeX files with input directives. Attackers can upload .tex files containing \\input{path} or \\verbatiminput{path} directives to have the TeX engine read arbitrary files accessible to the server process and include them in downloadable PDF output.
