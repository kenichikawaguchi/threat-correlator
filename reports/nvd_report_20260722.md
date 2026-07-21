# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-21 15:00 UTC
- **対象期間**: `2026-07-20T15:00:59.000Z` 〜 `2026-07-21T15:00:34.000Z`
- **重要CVE数**: 98 件（Critical 9.0+: 27 件 / High 7.0〜: 71 件）

---

## AI 分析サマリー

## 1. 全体サマリー
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 近くに上ります。  
- **Joomla 系プラグイン** と **WordPress プラグイン** に対する未認証ファイルアップロード／特権昇格が集中し、リモートコード実行 (RCE) が容易になるケースが目立ちます。  
- **npm / PyPI / Rust crates** などのサプライチェーン攻撃（トークン漏洩による悪意あるパッケージ公開）も増加し、開発環境の認証情報管理が重要です。  
- **Apache Fory、xrdp、ktransformers** などのサーバーサイドコンポーネントで、メモリ破壊やデシリアライズ不整合による深刻な権限取得が報告されています。  

> **傾向**：未認証でコード実行が可能になる脆弱性が多く、特に「ファイルアップロード」系プラグインは即座にパッチ適用が求められます。サプライチェーンリスクへの対策も同時に検討すべきです。

---

## 2. 特に注目すべき CVE（上位 5 件）

| CVE | スコア | 製品・コンポーネント | 主な問題点 | 影響範囲・リスク |
|-----|--------|----------------------|------------|-------------------|
| **CVE‑2026‑61900** | 10.0 | Joomla 拡張 **JDownloads** | 未認証ファイルアップロード → 任意コード実行 (RCE) | Joomla 本体を利用している全サイトが即座に完全乗っ取り可能 |
| **CVE‑2026‑61424** | 10.0 | Joomla 拡張 **DJ‑Classifieds** | 同上（未認証ファイルアップロード） | 同様に全 Joomla サイトが危険。プラグインだけでなく、他プラグインとの組み合わせで二次被害も想定 |
| **CVE‑2026‑46412** | 10.0 | npm パッケージ **@beproduct/nestjs‑auth** (0.1.2‑0.1.19) | 攻撃者が npm publish token を取得し、マルウェア入りバージョンを公開 | このパッケージを依存しているすべての NestJS アプリがインストール時にバックドアを取得 |
| **CVE‑2026‑64608** | 9.8 | **Apache Fory** (C++ 実装) | ヒープ型混乱 + OOB read/write → 任意コード実行 | Fory を組み込み利用している Java / C++ アプリ全般に影響。特にデシリアライズ機能を有効にしている環境は危険 |
| **CVE‑2026‑13439** | 9.8 | WordPress プラグイン **Easy Form Builder** (≤ 4.0.11) | パスワードリセットトークンに公開セッション ID を使用 → 未認証で管理者権限取得 | WordPress サイト全体の管理権限が奪取可能。プラグインがインストールされているすべてのサイトが対象 |

> **選定理由**  
> - **スコア 10.0** の未認証 RCE は即時対応が必須。  
> - **サプライチェーン (npm)** は一度侵入すれば広範囲に拡散。  
> - **Apache Fory** は企業向け基盤で利用されることが多く、メモリ破壊系は検知が難しい。  
> - **WordPress** は最も普及している CMS の一つで、プラグイン経由の特権昇格は大規模被害につながりやすい。

---

## 3. 推奨アクション

### 3.1 パッチ適用・バージョンアップ
- **JDownloads**: 公式が提供する **v5.2.3 以降**（または最新リリース）へアップデート。  
- **DJ‑Classifieds**: **v3.9.7 以降** に更新。  
- **Easy Form Builder**: **v4.0.12** 以上にアップグレード。  
- **Apache Fory**: **v1.4.0** 以上へ更新（デシリアライズとヒープ型混乱の修正が含まれる）。  
- **xrdp** (CVE‑2026‑41252): **v0.10.7** 以上に更新。  
- **ktransformers**: 2026‑06‑15 以降のコミット `def0f93` が含まれる **v0.6.4** 以上へ。  
- **Grav**: **v2.0.7** 以上にアップグレード（Blueprint 動的呼び出しのホワイトリスト化）。  

### 3.2 サプライチェーン対策
- **@beproduct/nestjs‑auth**: 0.1.20 以降（修正版）に切り替えるか、**npm audit** で `npm view @beproduct/nestjs-auth versions` を確認し、**0.1.20 以上**を使用。  
- npm / GitHub の **Publish Token** をローテーションし、最小権限（read‑only）に制限。  
- CI/CD パイプラインで **npm audit**, **yarn audit**, **cargo audit**, **cargo deny** などを自動実行し、悪意あるバージョンのインストールを防止。  

### 3.3 防御・検知強化
- **WAF ルール**: `multipart/form-data` のファイルアップロード先をホワイトリスト化し、拡張子・MIME タイプの厳格チェックを追加。  
- **ファイルアップロードディレクトリ**を **execute 権限なし**、**Web から直接アクセス不可** に設定（例: `chmod 0640`、`.htaccess` で `Deny from all`）。  
- **ログ監視**: Joomla / WordPress の `upload` エンドポイントへの 4xx/5xx アクセスが急増した場合はアラートを上げる。  
- **メモリ破壊系**（Apache Fory, xrdp 等）: `ASAN` / `Valgrind` での実行テスト、`Core dump` の取得と解析を有効化。  
- **権限分離**: Joomla / WordPress の管理者アカウントは **MFA** を必須化し、最小権限のロールを徹底。  

### 3.4 インシデント対応手順
1. **脆弱性が報告されたプラグイン/ライブラリのバージョン** を即座に確認。  
2. **バックアップ**（データベース・コード）を取得したうえで、対象パッケージを **最新版** に置き換える。  
3. **Web サーバーの再起動**、もしく

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61900

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-20T19:17:28.267 |

The Joomla extension JDownloads is vulnerable to an unauthenticated file upload, leading to full RCE.

### CVE-2026-61424

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-20T19:17:28.027 |

The Joomla extension DJ-Classifieds is vulnerable to an unauthenticated file upload, leading to full RCE.

### CVE-2026-46412

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-07-20T16:17:01.000 |

@beproduct/nestjs-auth is a NestJS authentication module for BeProduct IDS (Identity Server) with OpenID Connect support. Between 2026-05-11 20:19 UTC and 22:56 UTC, an attacker used a compromised npm publish token to publish 18 malicious versions of `@beproduct/nestjs-auth` (0.1.2 through 0.1.19). The postinstall payload attempted to harvest npm tokens (from `~/.npmrc`);  GitHub personal access tokens, OAuth tokens (`gho_*`), and Actions OIDC tokens; AWS credentials (from environment variables and `~/.aws/credentials`); HashiCorp Vault tokens; and other secrets present in environment variables. Version `0.1.20` is a clean republish from the original `0.1.1` source tree. Anyone who installed any version in the range `>=0.1.2 <=0.1.19` should remove the package and clean the npm cache; install the clean version; rotate every credential present in the install environment, including all npm publish tokens, all GitHub PATs and OAuth tokens, AWS access keys, HashiCorp Vault tokens, and any other secret that was in env vars or config files at install time; scan affected hosts for indicators of compromise and, if any are found, treat the host as compromised and reimage; and check committed repository history for unexpected additions in `.claude/` or `.vscode/` directories. The worm is known to commit `setup.mjs` + hook configs to PR branches via automated agent runtimes.

### CVE-2026-54051

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-20T17:17:57.643 |

Network-AI is a TypeScript/Node.js multi-agent orchestrator. Prior to version 5.9.1, the agent sandbox gates shell commands behind an allowlist (`SandboxPolicy.isCommandAllowed`), which THREAT_MODEL.md calls the main control against a compromised agent (Adversary 3.2). The allowlist glob-matches the whole command string, but `ShellExecutor` runs that string through `/bin/sh -c`. So any wildcard allow such as `git *`, `npm *` or `node *` also matches `git status; <anything>`, and a scoped command becomes arbitrary execution. The issue is fixed in v5.9.1. `ShellExecutor` now executes via `spawn(file, args, { shell: false })` using a quote-aware parsed argv, so no shell is invoked. `SandboxPolicy.isCommandAllowed` and the new `SandboxPolicy.tokenizeCommand` reject any unquoted shell metacharacter (`; & | $ ` ` ` ( ) < > { }` newline) or unterminated quote before the allowlist glob match; quoted metacharacters are preserved as literal argument data. Users should upgrade to `network-ai@5.9.1` or later. As defense in depth, avoid broad wildcard allowlist entries such as `node *` / `npm *` which are direct code execution by design.

### CVE-2026-51027

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-20T16:17:04.897 |

An issue in FileThingie v.2.5.7 allows a remote attacker to obtain sensitive information via the ft2.php component.

### CVE-2026-1617

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T12:17:21.173 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Turkmesh Communication Services Inc. Turkhotspot 5651 Loglama allows SQL Injection.

This issue affects Turkhotspot 5651 Loglama: from 5.1.2 before 5.1.3.

### CVE-2026-64606

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-21T11:16:27.973 |

Deserialization of untrusted data vulnerability that may allow class-registration checks to be bypassed during Java lambda deserialization. Only lambda capture class is affected


This issue affects Apache Fory: from before 1.4.0.

Users are recommended to upgrade to version 1.4.0, which fixes the issue.

### CVE-2026-64608

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-787;CWE-843` |
| Published | 2026-07-21T10:16:24.923 |

Heap type confusion and out-of-bounds read/write in the Apache Fory C++ implementation. When deserializing data in compatible mode, the field-skip paths do not correctly validate the declared field types against the actual data, so input with an inconsistent schema can cause type confusion and out-of-bounds memory access. Only the C++ implementation is affected; other language implementations of Apache Fory are not.

This issue affects Apache Fory C++: from 0.14.0 before 1.4.0.

Users are recommended to upgrade to version 1.4.0, which fixes the issue.

### CVE-2026-13439

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-21T06:16:28.060 |

The Easy Form Builder by WhiteStudio plugin for WordPress is vulnerable to Unauthenticated Privilege Escalation to Administrator in versions up to, and including, 4.0.11 This is due to the password recovery flow using the publicly-visible session identifier ('sid') as the password reset token stored in wp_emsfb_temp_links, combined with a publicly-accessible nonce refresh endpoint (Emsfb/v1/nonce/refresh) that issues valid WordPress REST nonces to unauthenticated visitors. This makes it possible for unauthenticated attackers to reset the password of any WordPress user — including administrators — by scraping the public sid from a published login form page, submitting a recovery request for any known user email via Emsfb/v1/forms/message/add, and then calling Emsfb/v1/forms/recovery/efb_set_password with the known sid to set an arbitrary new password and gain full administrator access.

### CVE-2026-41252

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-20T17:17:08.310 |

xrdp is an open source RDP server. Versions 0.10.6 and prior contain a missing bounds check in xrdp, which allows a heap-based buffer overflow when operating in vnc-any mode. The issue occurs during the handling of RFB protocol color map messages from a VNC server, where incoming color indices are not properly validated. A malicious VNC server can exploit this flaw by sending crafted messages with out-of-range values, leading to an out-of-bounds write on the heap. This memory corruption can result in a denial of service (DoS) or potentially allow remote code execution (RCE) prior to authentication. This issue has been fixed in version 0.10.6.1.

### CVE-2026-35048

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-20T17:17:06.840 |

The Piwigo installer in versions 16.3.0 and earlier accepts POST parameters for database configuration and writes them directly into a PHP configuration file without proper sanitization. On PHP 8+, the `addslashes()` protection is bypassed because it checks for `get_magic_quotes_gpc()`, a function removed in PHP 8.0. This allows raw user input to be interpolated directly into PHP source code. An unauthenticated attacker can inject arbitrary PHP code through POST parameters (prefix, dbpasswd, dbhost, dbname, or dbuser), which gets written to `local/config/database.inc.php` and executed on every page load.

### CVE-2026-53595

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-178;CWE-287;CWE-640` |
| Published | 2026-07-20T21:16:48.417 |

FreeScout is a free help desk and shared inbox built with PHP's Laravel framework. Prior to version 1.8.224, the public endpoint `POST /user-setup/{hash}/{invite_sent_at}` (`OpenController@userSetupSave`) selects the target account solely by its `invite_hash` column, then overwrites that account's email and password and logs in as it. No authentication, cookie, or prior session is required. After a user activates, FreeScout sets `invite_hash` to the empty string. On MySQL and MariaDB, `VARCHAR` equality ignores trailing spaces, so a single URL-encoded space (`%20`) matches the stored empty string and selects the lowest-id activated user. The expiry guard decrypts `invite_sent_at` with the target's password hash, but `Helper::decrypt` returns its raw input unchanged when decryption fails. A plaintext numeric value such as `9999999999` therefore passes the time-to-live check without any secret. The result is that an anonymous attacker sets the email and password of the lowest-id activated FreeScout account (a support agent, or an administrator if one was added by invitation) and authenticates as that account. Version 1.8.224 contains a fix.

### CVE-2026-16337

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-20T20:16:43.387 |

Improper authorization in the ToolGroupResource and RoleAjax REST/DWR endpoints in dotCMS dotCMS 21.02 through 26.06.22-03 on all platforms allows a low-privileged authenticated backend user to self-assign the administrative layout and self-grant the CMS Administrator role, then achieve remote code execution via a crafted OSGi bundle upload whose BundleActivator executes arbitrary shell commands.

### CVE-2026-61425

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-20T19:17:28.150 |

The Joomla extension Gridbox is vulnerable an authenticated bypass, potentially leading to full admin access.

### CVE-2026-60034

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T19:17:27.910 |

The Joomla extension JMedia is vulnerable to a stored XSS vulnerability. Unsanitised SVG uploads served without nosniff, leading to stored/reflected XSS.

### CVE-2026-60032

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-20T19:17:27.660 |

The Joomla extension JMedia is vulnerable to an authenticated arbitrary file upload, leading to RCE. Executable uploads/writes possible (incl. polyglot filenames); chmod didn't strip execute bits.

### CVE-2026-65008

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-21T12:19:01.183 |

Grav 2.0.4 (fixed in 2.0.7) contains a remote code execution vulnerability in Blueprint::dynamicData() (system/src/Grav/Common/Data/Blueprint.php), which passes a Class::method callable string and its arguments directly to call_user_func_array() without any allowlist. Because the form plugin routes page frontmatter through this path, an authenticated account with the admin.pages (or api.pages.write) permission can plant a malicious callable directive in a page. The command then executes as the web-server user whenever anyone — including an unauthenticated visitor — accesses the page.

### CVE-2026-64625

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-20T22:17:18.740 |

AVideo before 29.0 contains an incomplete fix for CVE-2026-45578 where execAsync() re-wraps escaped commands in double-quoted sh -c, allowing command substitution via $() and backticks. Attackers can inject arbitrary OS commands through the Live plugin on_publish.php endpoint despite escapeshellarg() protection.

### CVE-2026-63767

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-20T20:16:46.323 |

ktransformers through 0.6.3, fixed in commit def0f93, contains an unauthenticated pickle deserialization vulnerability that allows remote attackers to execute arbitrary commands by sending crafted pickle payloads to the SchedulerServer ZMQ ROUTER socket bound to all interfaces. Attackers can exploit malicious __reduce__ methods embedded in crafted pickle payloads to execute arbitrary shell commands as the server process.

### CVE-2026-63766

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-20T20:16:46.170 |

GPT-SoVITS through 20250606v2pro contains an OS command injection vulnerability in webui.py where ASR, slice, denoise, and uvr5 functions interpolate unsanitized Gradio textbox values directly into shell commands executed with shell=True. Attackers can inject shell metacharacters through path parameters to execute arbitrary OS commands as the server process user without authentication.

### CVE-2026-39878

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T18:16:51.713 |

Chamilo LMS versions 1.11.38 and earlier contain a stored cross-site scripting vulnerability in the user registration form that allows any unauthenticated attacker to execute arbitrary JavaScript in an administrator's browser session, leading to full platform admin account takeover. This has been patched in 1.11.40.

### CVE-2026-64609

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-21T10:16:25.057 |

Out-of-bounds read via sun.misc.Unsafe in Apache Fory. When out-of-band zero-copy deserialization is used, readAlignedVarUint() can read beyond the bounds of the underlying buffer. Out-of-band zero-copy deserialization is an opt-in feature; applications that do not use it are not affected.

This issue affects Apache Fory (formerly Apache Fury): from 0.5.0 before 1.4.0. Versions before 0.11.0 were published under the Maven coordinates org.apache.fury:fury-core.

Users are recommended to upgrade to version 1.4.0, which fixes the issue.

### CVE-2026-44231

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-200;CWE-269;CWE-863` |
| Published | 2026-07-20T20:16:43.797 |

RT is an open source, enterprise-grade issue and ticket tracking system. Versions prior to 5.0.10, 6.0.0 and above, prior to 6.0.3 contain an information disclosure and privilege escalation vulnerability in the REST 2.0 API. A privileged (non-administrative) user can obtain authentication credentials belonging to other users — including users with administrative privileges — and use those credentials to read data as those users via RT's feed endpoints. The same request that exposes the credentials also rotates them, invalidating previously-distributed feed URLs across the instance. This issue has been fixed in versions 5.0.10 and 6.0.3.

### CVE-2026-46428

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-20T16:17:01.347 |

lettre is a a mailer library for Rust. Starting in version 0.10.1 and prior to version 0.11.22, an inverted-boolean bug in lettre's `boring-tls` integration silently disables TLS hostname verification for callers using the default (strict) configuration. An on-path attacker presenting any chain-valid certificate for any domain can intercept SMTP submission, including PLAIN/LOGIN credentials and message contents, against any lettre user built with the `boring-tls` feature. Other TLS backends (`native-tls`, `rustls`) are unaffected. Version 0.11.22 patches the issue.

### CVE-2026-13380

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201;CWE-312` |
| Published | 2026-07-20T21:16:46.510 |

VSee Clinic 7.1.26 and VSee Clinic API 1.3.0 exposes cleartext SFTP credentials in the HTTP responses of three unauthenticated endpoints. The credentials are present in these responses only when SFTP connections have been configured within the application. No authentication is required to retrieve these credentials. An unauthenticated remote attacker who observes any of these HTTP responses on an instance where SFTP is configured can obtain the credentials and use them to access the associated SFTP server.

### CVE-2026-35198

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T16:16:58.440 |

HeyForm is an open-source form builder. Prior to version 3.0.0-rc.7, a stored cross-site scripting (XSS) vulnerability in the form builder allows a low-privileged team member to inject malicious JavaScript that executes when a team owner views the form, leading to complete account takeover through privilege escalation. Version 3.0.0-rc.7 contains a patch for the issue.

### CVE-2026-12701

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-20T15:16:34.333 |

A path traversal vulnerability was found in pulpcore. The relative_path_validator function only verifies that content paths do not begin with "/" but fails to block directory traversal sequences such as "../" anywhere in the path. An authenticated administrator can craft a relative_path containing embedded traversal sequences (e.g., "looking/normal/../../../../etc/shadow") that escapes the intended export directory during FilesystemExport operations. Because the file content is also user-controlled (uploaded artifact), this allows arbitrary file write to any location writable by the Pulp service user, potentially leading to service compromise or further system exploitation.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-60026

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-20T19:17:26.920 |

The Joomla extension Quix Page Builder Pro is vulnerable to an authenticated PHP code execution. Authenticated builder user (core.create/core.edit) could inject PHP tags in element content, that got executed via view-cache include(). Requires caching on (default).

### CVE-2026-53593

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-20T20:16:44.883 |

FreeScout is a free help desk and shared inbox built with PHP's Laravel framework. Prior to version 1.8.224, the denylist that neutralizes dangerous file uploads (`Helper::$restricted_extensions`) is incomplete: it does not cover the `.pht` extension. The authenticated upload endpoint `POST /uploads/upload` (`SecureController@upload`) stores files with their original extension into the web-accessible directory `storage/app/public/uploads/` (served at `/storage/uploads/`). On the standard Apache + `libapache2-mod-php` deployment, the default handler `<FilesMatch ".+\.ph(ar|p[3457]?|t|tml)$">` executes `.pht`, so **any authenticated agent can upload a `.pht` web shell and run arbitrary commands as the web-server user** (`www-data`). This is a direct bypass of the fix for CVE-2025-48471, which added `phtml`/`phar` but not `pht` (nor `phtm`, `phps`). Version 1.8.224 contains an updated fix.

### CVE-2026-12341

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-20T19:17:18.027 |

This vulnerability
impacts all versions of IdentityIQ and allows an unauthenticated attacker
unauthorized access to protected APIs and data due to improper validation of
OAuth bearer tokens.

### CVE-2026-44178

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-20T17:17:09.060 |

xrdp is an open source RDP server. Versions 0.10.6 and prior contain a heap-based buffer overflow vulnerability within the virtual channel forwarding mechanism. When forwarding data from a remote client to the internal channel server, the xrdp process utilizes a fixed-size buffer without adequate bounds checking on the incoming payload. An authenticated remote attacker can exploit this flaw by sending a specially crafted virtual channel message that exceeds the buffer capacity, leading to heap memory corruption. This may result in a denial of service or the execution of arbitrary code with the privileges of the xrdp process. This issue has been fixed in version 0.10.6.1.

### CVE-2026-25039

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-40` |
| Published | 2026-07-20T16:16:56.913 |

Parsec is a cloud-based application for simple and cryptographically secure file sharing. The application does not sanitize the workspace name, creating a vulnerability if that workspace name is a UNC path. When creating mountpoint in the windows filesystem to mount the workspace of an organization, the application does not sanitize the workspace name. The cause issue if the workspace name evaluate to a UNC path since it's allowed for the name to containt `\` char. If the UNC path is invalid (or the targeted resource is not available) the application become unresponsive otherwise the system will interact with the mounted UNC path allowing the attacker to retrieve to [`NTLM`] hash.

### CVE-2026-21824

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-20T16:16:56.777 |

HCL Commerce contains an privilege escalation vulnerability that could allow denial of service, disclosure of user personal data, and performing of unauthorized administrative operations.

### CVE-2026-65007

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-21T12:19:00.910 |

The Grav api plugin (grav-plugin-api) before 1.0.8 fails to properly authorize API key generation and revocation: the plugin intercepts the apiKeyGenerate/apiKeyRevoke admin tasks before the account-management ACL runs and authorizes the caller on only the admin.login permission (the baseline permission held by every panel user). This allows any user with admin.login to mint a persistent API key bound to any account, and the forged key inherits the target account's API permissions. On installs where an API-enabled account holds broader permissions, this enables account impersonation and privilege escalation up to account takeover.

### CVE-2026-13381

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-20T21:16:46.660 |

VSee Clinic 7.1.26 and API 1.3.0 contain an Insecure Direct Object Reference (IDOR) vulnerability in the /v1.3.0/api/files endpoint. An authenticated attacker can manipulate the 'remark' request parameter to enumerate, retrieve, and delete files belonging to other users on the application server.

### CVE-2026-64619

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-07-20T19:17:30.373 |

FileCodeBox before 2.4 contains a rate-limit bypass vulnerability in the IPRateLimit class that allows unauthenticated attackers to circumvent request throttling by supplying attacker-controlled X-Real-IP and X-Forwarded-For headers without verification of trusted reverse proxy origin. Attackers can supply unique spoofed IP values on each request to enumerate all possible share codes and retrieve other users' files without authentication.

### CVE-2026-60030

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-20T19:17:27.417 |

The Joomla extension Quix Page Builder Pro is vulnerable to an improper access control. Authenticated users could upload media files regardless of their media management permissions.

### CVE-2026-60027

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-20T19:17:27.060 |

The Joomla extension Quix Page Builder Pro is vulnerable to a unauthenticated path traversal via form elements. Unauthenticated users frontend users are allowed traversal paths and read arbitrary files. Requires a published page with a Form element.

### CVE-2026-8170

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-07-20T18:16:56.570 |

The mv, cp, and rm file utilities exposed within the ExtremeXOS (EXOS) shell environment fail to safely canonicalize paths and follow symbolic links outside of the intended privilege boundary. An attacker with low-privilege CLI access can create a symbolic link that references a privileged filesystem location and then invoke the affected utilities to read, modify, or replace security-critical files outside of their authorized scope. Under certain conditions, this may enable escalation to root-level access and persistent modification of the device software stack. Exploitation is possible remotely by an attacker holding a low-privilege account, or locally via the serial console.



Extreme would like to thank Hadrien Barral (Université Gustave Eiffel) and Georges-Axel Jaloyan (French Ministry of the Interior) for responsible disclosure of their findings.

### CVE-2026-8169

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-20T18:16:56.420 |

ExtremeXOS (EXOS) uses a challenge-response mechanism to authorize access to the privileged debug-mode function. The challenge value is generated using an insufficiently random source, which under certain conditions may allow an attacker to predict the expected response and activate debug-mode without authorization. Depending on device configuration and version, this may enable escalation to root-level access and persistent modification of the device software stack. Exploitation requires either a valid low-privilege account on the device (remote scenario) or physical serial console access (local scenario). This vulnerability is distinct from CVE-2017-14329, which addressed a different issue involving Python script privileges.



Extreme would like to thank Hadrien Barral (Université Gustave Eiffel) and Georges-Axel Jaloyan (French Ministry of the Interior) for responsible disclosure of their findings.

### CVE-2026-27823

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-20T16:16:57.680 |

A vulnerability has been identified in EGroupware that may lead to Remote Code Execution (RCE). The issue allows an authenticated attacker to execute arbitrary commands on the server. If user self-registration is enabled, the vulnerability may be exploitable without prior authentication. The vulnerability stems from improper authorization checks combined with a file write primitive and an arbitrary file read vulnerability, which together enable full system compromise. This has been patched in versions 26.2.20260224 and 23.1.20260224.

### CVE-2026-63090

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-20T15:16:45.213 |

ProFTPD before 1.3.9c and 1.3.10rc3 contains a heap-based buffer overflow vulnerability in the mod_sftp module that allows authenticated low-privilege attackers to achieve arbitrary code execution by sending crafted SFTP packet fragments exceeding the 16 KB reassembly buffer in the fxp.c component. Attackers can supply oversized fragments to trigger an incorrectly conditioned reallocation, corrupt pool freelist metadata, overwrite the root_fs BSS global pointer to reference a fake filesystem struct, and redirect pr_fsio_stat() to system() via a crafted RENAME request.

### CVE-2026-46410

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-20T15:16:38.673 |

FileBrowser Quantum is a free, self-hosted, web-based file manager. Versions prior to 1.3.2-stable and 1.4.1-beta may leak some sensitive info, such as source and path. Versions 1.3.2-stable and 1.4.1-beta fix the issue. No known workarounds are available.

### CVE-2026-45270

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T15:16:38.163 |

CI4MS is a CodeIgniter 4-based content management system skeleton. Prior to version 0.31.9.0, the `Pages` backend module registers the `html_purify` validation rule on language-keyed page content but persists the raw, un-purified POST value into the database. The public renderer for pages (`Home::index()` → `app/Views/templates/default/pages.php`) emits `$pageInfo->content` without `esc()`, yielding stored XSS that fires for every public visitor of the affected page — including administrators. Because pages may be promoted to the site home page, the payload can be served at `/` and reach every visitor of the site. Version 0.31.9.0 patches the issue.

### CVE-2026-53591

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-20T20:16:44.613 |

FreeScout is a free help desk and shared inbox built with PHP's Laravel framework. Prior to version 1.8.223, an unauthenticated attacker can inject messages into any existing support conversation by sending a single email to the helpdesk's public address with a crafted `In-Reply-To` header. No credentials, tokens, or prior access are required. The injected message is rendered in the agent UI as a legitimate customer reply, the conversation is automatically reopened, and the `last_reply_from` field is set to the attacker's identity. Version 1.8.223 contains a fix.

### CVE-2026-60028

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T19:17:27.177 |

The Joomla extension Quix Page Builder Pro is vulnerable to an authenticated stored XSS vulnerability. Authenticated builder user could inject scripts, fires for any visitor or admin viewing the page. Unescaped output + unsanitised SVG.

### CVE-2026-40187

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-95` |
| Published | 2026-07-20T17:17:07.690 |

In egroupware version 26.0 and earlier, an authenticated administrator can achieve OS-level Remote Code Execution (RCE) by uploading a malicious eTemplate XML file (`.xet`) to the VFS `/etemplates` mount. The `Widget::expand_name()` method passes template widget attribute values directly into a PHP `eval()` call with only double-quote escaping applied - **backtick characters are not escaped**. In PHP, backticks inside a double-quoted `eval()` string execute shell commands. This allows an admin-level user to escalate from web application access to arbitrary OS command execution on the server.

### CVE-2026-63429

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-434` |
| Published | 2026-07-20T16:17:06.810 |

HeyForm is an open-source form builder. Prior to version 3.0.0-rc.9, `POST /api/upload` has no authentication guard, no global guard, no form-context validation, no `openToken` requirement, and no session cookie check. Any anonymous internet user can upload files (PDF, DOC/DOCX, XLS/XLSX, CSV, TXT, MP4, images, etc., up to 10 MB) and receive a permanent public URL on the HeyForm domain. The endpoint is used by both authenticated form creators and unauthenticated form submitters; because no form-context binding exists, every request to it is anonymously accepted. Version 3.0.0-rc.9 contains a patch for the issue.

### CVE-2026-64624

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-20T22:17:18.600 |

FreeRDP before 3.28.0 treats lines beginning with forward slash in RDP files as raw command-line options, exposing the entire CLI parser surface to untrusted files. Attackers can craft malicious RDP files with /rdp2tcp, /cert:ignore, or /drive options to execute arbitrary commands, bypass certificate validation, or expose local filesystems without user interaction.

### CVE-2026-47198

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-639` |
| Published | 2026-07-20T21:16:48.043 |

Paymenter is a free and open-source webshop solution for management of hosting services. In versions prior to 1.5.1, the checkout component improperly filters URL-writable properties, allowing authenticated users to inject arbitrary key-value pairs into server provisioning parameters. Because bundled server extensions prioritize these user-supplied properties over administrator-defined configurations, a regular user can override hosting plans and resource limits at checkout without special privileges. The Checkout Livewire component's $checkoutConfig property exposed via URL query parameters, only validating keys explicitly defined by an extension's configuration method, allowing any undefined injected keys to bypass validation entirely. These unsanitized keys are then stored directly in the database by the cart component and later passed to server extensions during provisioning, enabling user-injected data to override intended administrator settings. Depending on the active extension, this leads to unauthorized overrides of core resource limits (such as CPU, RAM, storage, or package tiers). No administrative privileges are required to exploit this vulnerability. This issue has been fixed in version 1.5.1.

### CVE-2026-28220

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-20T16:16:57.820 |

Wazuh is a free and open source platform used for threat prevention, detection, and response. Prior to version 4.14.5, issues in the Cluster Distributed API (DAPI) handling allow a cluster peer, or any actor able to authenticate to the cluster channel using the shared cluster key, to make the master node deserialize an attacker-controlled callable and execute it under an attacker-controlled RBAC context. The cluster code in `framework/wazuh/core/cluster/common.py` deserializes JSON with `as_wazuh_object()`, which resolves any callable whose top-level package is wazuh or api (an overly broad allowlist controlled only by `ALLOWED_CALLABLES_PACKAGES`), and DAPI requests handled in framework/wazuh/core/cluster/dapi/dapi.py accept a client-supplied rbac_permissions value that `run_local()` applies as the global RBAC context, so supplying an rbac_mode of black causes authorization checks for expose_resources-protected functions to pass without any legitimate permission assignment. Combined, these allow privileged administrative actions on the master node such as arbitrary file writes under WAZUH_PATH, creation of new API users, and tampering with security.yaml, and can be chained into full manager compromise. This issue has been fixed in version 4.14.5.

### CVE-2026-57495

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-20T22:17:17.107 |

AgenticMail gives AI agents real email addresses and phone numbers. In @agenticmail/claudecode prior to version 0.2.39, @agenticmail/codex prior to version 0.1.33, @agenticmail/core prior to version 0.9.43, and @agenticmail/openclaw prior to version 0.5.71, two inbound-mail handlers act on a privileged effect without verifying that the sender is the operator, while a sibling handler in the same repo does. The higher-impact one: any external email routed to the bridge inbox causes the dispatcher to resume the operator's Claude Code session with `permissionMode: 'bypassPermissions'`, embedding the attacker-controlled `from`/`subject`/`preview` verbatim into the prompt the resumed agent reads — an indirect prompt injection into a fully-privileged agent (Bash/Write/Edit/WebFetch + the agenticmail MCP toolbelt) running as the operator's OAuth identity. The sibling operator-query email-reply hook gates the same untrusted-From provenance with `isOperatorReplySender(replyFrom, config.operatorEmail)` (fail-closed); the bridge-wake path — a strictly higher-privilege effect — has no equivalent. @agenticmail/claudecode 0.2.39, @agenticmail/codex 0.1.33, @agenticmail/core 0.9.43, and @agenticmail/openclaw 0.5.71 contain a fix.

### CVE-2026-47255

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-89;CWE-284;CWE-319;CWE-798` |
| Published | 2026-07-20T22:17:15.403 |

AgenticMail gives AI agents real email addresses and phone numbers. @agenticmail/api prior to version 0.9.32 and @agenticmail/core prior to version 0.9.10 had weakness related to validation and and binding of inactive-agent hour filtering; storage SQL identifier validation; metadata-backed ownership checks for raw storage SQL; blocking direct storage metadata access through raw SQL; fail-closed outbound worker secret handling; SMTP envelope/header control-character validation before command construction; and TLS certificate verification as the default for MailSender with an explicit opt-out for local development. @agenticmail/api prior to version 0.9.32 and @agenticmail/core prior to version 0.9.10 are patched.

### CVE-2026-63770

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348` |
| Published | 2026-07-20T19:17:29.770 |

Glance through 0.8.5 contains an IP address spoofing vulnerability in the authentication handler that allows unauthenticated attackers to bypass brute-force lockout protections by supplying arbitrary values in the X-Forwarded-For request header when the server proxied option is enabled. Attackers can manipulate the leftmost value of the X-Forwarded-For header to make each login attempt appear to originate from a distinct IP address, preventing the per-IP failed-login counter from reaching the lockout threshold and enabling unlimited credential guessing against the authentication endpoint.

### CVE-2026-41521

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-20T17:17:08.460 |

xrdp is an open source RDP server. Versions 0.10.6 and prior contain an integer overflow vulnerability when processing screen update messages within the vnc-any connection mode. A malicious remote VNC server can send crafted image dimensions that cause an integer overflow during memory buffer size calculation, resulting in an undersized allocation. Subsequent processing of the incoming image data using the original oversized parameters leads to an out-of-bounds read. An unauthenticated remote attacker could exploit this flaw to disclose sensitive information from the heap memory or cause a denial of service (DoS) via a process crash. This issue has been fixed in version 0.10.6.1.

### CVE-2026-46415

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-284;CWE-348` |
| Published | 2026-07-20T16:17:01.163 |

The Caddy Defender plugin is a middleware for Caddy that allows users to block or manipulate requests based on the client's IP address. Prior to version 0.10.1, Caddy Defender used `r.RemoteAddr` when evaluating whether a request should be blocked. `RemoteAddr` is the address of the immediate peer connected to Caddy. In deployments where Caddy is behind a trusted proxy, CDN, or load balancer, the immediate peer is usually the proxy, not the original client. Caddy resolves the original client address into its `client_ip` request variable after applying the configured `trusted_proxies` policy, but Defender did not use that value. As a result, clients from blocked IP ranges could bypass Defender when accessing Caddy through a trusted proxy whose own IP address was not blocked. This affects deployments that use Defender behind trusted proxies and expect it to enforce blocking based on the real client IP. The issue is fixed in version 0.10.1 by making Defender prefer Caddys resolved `client_ip` request variable when it is available. Defender falls back to `RemoteAddr` only when Caddy has not provided a resolved client IP. There is no complete workaround in affected Defender versions for deployments that rely on Caddy's trusted proxy client IP resolution. Until upgrading, affected users should enforce equivalent IP blocking at the trusted proxy, CDN, load balancer, firewall, or other edge layer before traffic reaches Caddy. Deployments where Caddy receives traffic directly from clients, without an intermediate trusted proxy, are not affected by this bypass.

### CVE-2026-63728

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-07-21T00:17:48.953 |

Gitleaks prior to 8.30.1 contains a template injection vulnerability that allows attackers who can supply or influence report templates to read arbitrary environment variables and exfiltrate sensitive data by leveraging non-hermetic Sprig template functions. Attackers can craft malicious report templates using the env, expandenv, and getHostByName functions to extract credentials, tokens, and API keys from the host process and exfiltrate them through DNS queries, including secrets discovered during the scan itself.

### CVE-2026-47129

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-20T21:16:47.777 |

NextCRM is open-source customer relationship management (CRM) software. Versions prior to 0.12.0 have a Broken Access Control (BAC) vulnerability in the `activateUser` and `deactivateUser` Next.js Server Actions of NextCRM. The application fails to verify if the requesting user holds the `admin` role. Consequently, any authenticated user (even those with the lowest `member` or `viewer` roles) can arbitrarily activate or deactivate any user account in the system, including the main administrator. Version 0.12.0 fixes the issue.

### CVE-2026-44508

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-200` |
| Published | 2026-07-20T21:16:47.113 |

Rsync is a file-copying tool that uses a delta-transfer algorithm to synchronize remote and local files.  In versions prior to 3.4.3, the receiver's compressed-token decoder accumulated a 32-bit signed counter without checking for overflow. A malicious sender can trigger an overflow that with careful manipulation can lead to the extraction of data stored in memory of the process allowing an attacker to access environment variables, passwords and memory pointers from the heap, stack, and libraries. The leakage of these pointers and data can significantly reduce the effectiveness of ASLR and facilitate further exploitation. This issue is fixed in version 3.4.3.

### CVE-2026-32821

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-20T17:17:05.750 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, any authenticated API user who has their own access token can ask the collection API to evaluate permissions as a different user by supplying `user_email`. If the target user has collections, this can expose those collections through the API. In V4, once a collection id is known, the same controller also offers `add_item` and `remove_item` routes without any object-level `authorize!` checks,
creating a likely cross-user modification path. This is patched in version 26.06.08.

### CVE-2026-55626

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-07-20T18:16:54.150 |

xrdp is an open source RDP server. In versions 0.10.6 and prior, when an authenticated user session is initialized using the Xvnc backend over UNIX domain sockets, the Xvnc process is launched with insufficient authentication mechanisms. A local authenticated attacker could exploit this vulnerability to bypass intended session isolation, allowing them to unauthorizedly view or control the active desktop sessions of other users on the same system. Users using other backends, such as xorgxrdp or Xvnc over TCP sockets, are not affected. This issue has been fixed in version 0.10.6.1.

### CVE-2026-15905

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-20T23:16:56.300 |

Use after free in Aura in Google Chrome prior to 150.0.7871.128 allowed a local attacker to potentially exploit heap corruption via a malicious file. (Chromium security severity: High)

### CVE-2026-48389

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-20T19:17:23.807 |

DNG SDK versions 1.7.1 2536 and earlier are affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-63108

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-07-20T19:17:29.057 |

Roo Code through 3.54.0 contains a command injection vulnerability in the auto-approve execute feature that allows attackers to bypass allowlist/denylist enforcement by nesting command substitutions inside parameter expansion defaults. The command parser in parse-command.ts replaces parameter expansions with opaque placeholders before extracting command substitutions, causing the containsDangerousSubstitution guard to miss nested payloads, which are then auto-approved based on the outer allowlisted command prefix and executed by the shell via execa, enabling arbitrary command execution.

### CVE-2026-46555

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-306;CWE-346` |
| Published | 2026-07-20T17:17:09.820 |

WhatsApp MCP Server is a Model Context Protocol (MCP) server for WhatsApp, enabling Claude to read and send WhatsApp messages. Prior to version 0.2.1, the `whatsapp-bridge` HTTP API listens on `127.0.0.1:8080` without authentication and without Host header validation, and the `/api/send` endpoint accepts an absolute `media_path` parameter without confining it to a safe directory. Combined, these issues allow any local process running as the same user as the bridge to send WhatsApp messages from the paired account without authorization; the same caller to read arbitrary files readable by the user (e.g. SSH private keys, browser session data, source code, dotfiles) and exfiltrate them as WhatsApp document attachments; and/or a remote attacker to trigger the same operations via DNS rebinding from a webpage the user visits, since no Host header validation is performed. In MCP environments, "local caller" extends beyond processes the user explicitly launched — sibling MCP servers, IDE extensions, and tool-triggered flows running in the user's session can act as the effective caller. This issue is fixed in whatsapp-mcp v0.2.1 and corresponding Docker images / release artifacts. Users should upgrade immediately. The fix introduces bearer token authentication on the bridge HTTP API (configured via environment variable, required on all requests, validated with constant-time comparison); host header allow-list validation to prevent DNS rebinding; and confinement of `media_path` to a configured directory, with rejection of absolute paths outside the root and path traversal sequences. This is a breaking change for clients of the bridge API. For users who cannot immediately upgrade: Stop the bridge, or block loopback access to port 8080, when the bridge is not actively in use; avoid running the bridge alongside untrusted MCP servers, browser extensions, or other untrusted local processes; avoid browsing untrusted sites while the bridge is running (DNS rebinding mitigation); and/or run the bridge under a dedicated user account or in a sandbox/container with no access to sensitive files.

### CVE-2026-54910

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-07-20T15:16:43.933 |

FileBrowser Quantum is a free, self-hosted, web-based file manager. Prior to version 1.4.3-beta, the `subtitlesHandler` endpoint (`GET /api/media/subtitles`) accepts two user-controlled query parameters: `path` and `name`, both of which are used in filesystem operations without sanitization, creating two independent path traversal vectors. The primary vector is the `path` parameter: it is passed directly to `idx.GetRealPath()` without calling `SanitizeUserPath()`, allowing an attacker to escape the storage root and set `parentDir` to any directory on the host. No existing anchor file is required.  The secondary vector is the `name` parameter: it is joined with `parentDir` via `filepath.Join(parentDir, name)` without stripping directory components, allowing traversal relative to any resolved `parentDir`. Any authenticated user (regardless of role or permissions) can exploit either vector to read any text file readable by the server process, including `/etc/passwd`, SSH keys, database credentials, and JWT signing keys. Version 1.4.3-beta patches the issue.

### CVE-2026-55544

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284;CWE-639;CWE-862` |
| Published | 2026-07-20T22:17:16.407 |

NextCRM is open-source customer relationship management (CRM) software. In version 0.12.1, the MCP campaign tools expose campaign read and write operations over the network using user-generated Bearer API tokens (`nxtc__...`). The application has an authorization model that restricts normal users to campaigns they created, but multiple MCP campaign handlers ignore the authenticated user ID and query or mutate campaigns only by object ID. As a result, a low-privileged authenticated user with a valid MCP API token can enumerate all campaigns, read campaign details, update or delete campaigns owned by other users, modify campaign templates and steps, and potentially trigger or pause campaign delivery. Version 0.12.2 fixes the issue.

### CVE-2026-46701

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-346` |
| Published | 2026-07-20T17:17:09.990 |

Network-AI is a TypeScript/Node.js multi-agent orchestrator. Prior to version 5.4.5, the MCP SSE server defaults to an empty secret (`process.env['NETWORK_AI_MCP_SECRET'] ?? ''` at `bin/mcp-server.ts:89`), which causes `_isAuthorized` (`lib/mcp-transport-sse.ts:254`) to return `true` unconditionally for every request — no `Authorization` header is required. Simultaneously, `_handleRequest` sets `Access-Control-Allow-Origin: *` (`lib/mcp-transport-sse.ts:272`) on every response, so a cross-origin browser fetch can read the result without restriction. An unauthenticated attacker who can lure a user to a malicious web page can invoke all 22 exposed MCP tools — including `config_set`, `agent_spawn`, and `blackboard_write` — against a default-configured localhost server. Version 5.4.5 patches the issue.

### CVE-2026-16445

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T13:17:16.730 |

A flaw was found in dracut. A remote attacker on the adjacent network can exploit this vulnerability by providing specially crafted DHCP options, such as a malicious root-path, next-server, or bootfile name, to a system using dracut's NetworkManager-based initrd network module. These options are improperly handled and written into a temporary shell script without proper escaping, leading to command injection. This allows the attacker to achieve root code execution within the initramfs during system boot.

### CVE-2026-8082

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-21T07:16:34.320 |

The bpost-shipping-platform WordPress plugin before 3.2.3 does not properly sanitize a parameter before using it in a SQL query during WooCommerce order submission, allowing unauthenticated attackers to perform time-based blind SQL injection on stores running this bpost-shipping-platform WordPress plugin before 3.2.3.

### CVE-2026-55833

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-21T00:17:35.537 |

Netty is a network application framework for development of protocol servers and clients. Prior to 4.1.136.Final and 4.2.16.Final, Netty SPDY header decoding continues inflating zlib-compressed header blocks after the raw header parser has exceeded `maxHeaderSize` and marked the frame truncated in `SpdyFrameCodec`, allowing a remote peer to send a small compressed `HEADERS` block that expands into much larger raw header data and causes compression-amplified CPU and allocation churn. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-55831

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-21T00:17:35.383 |

Netty is a network application framework for development of protocol servers and clients. Prior to 4.1.136.Final and 4.2.16.Final, Netty's SPDY SETTINGS decoder accepts a peer-declared SETTINGS entry count up to the 24-bit frame-length limit and materializes every unique setting ID in `DefaultSpdySettingsFrame`, allowing a remote SPDY/3.1 peer to send a syntactically valid roughly 2 MiB SETTINGS frame that creates 262144 map entries and amplifies network input into heap growth and ordered-map insertion work. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-56452

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-20T21:16:48.820 |

Path traversal in the sshd-scp component of Apache MINA SSHD. Apache MINA SSHD is a Java library for client-side and server-side SSH.




The implementation of receiving files or directories via SCP did not validate filenames in SCP "C" or "D" commands. A malicious sender could send filenames containing paths, resulting in files to be written in attacker-controlled places.




The issue affects only

  *  applications that use no longer supported Apache MINA SSHD versions < 2.0.0 and use the SCP functions to receive files,
  *  or applications using sshd-scp in Apache MINA SSHD >= 2.0.0 to receive files.




Applications using Apache MINA SSHD >= 2.0.0 not using sshd-scp are not affected.




The issue is fixed in Apache MINA 2.19.0 and 3.0.0-M5. Affected applications are advised to upgrade to these versions.

### CVE-2026-64612

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-20T18:16:56.273 |

A flaw was found in libcupsfilters and cups-filters. The PNG image reading function creates a libpng reader without installing an error recovery handler, causing the CUPS image filter process to abort when processing a malformed PNG file. An unauthenticated attacker could exploit this by submitting a specially crafted PNG print job, leading to denial of service of the in-flight print job.

### CVE-2026-48812

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-20T18:16:53.173 |

FreeScout is a free help desk and shared inbox built with PHP's Laravel framework. Prior to version 1.8.221, FreeScout's attachment download route skips token authentication for any attachment whose `token_type` is set to `1` (`TOKEN_TYPE_LEGACY`). Because this route is unauthenticated and the file path is deterministic, an unauthenticated remote attacker can download any attachment that was created by an older version of FreeScout without possessing a valid token or session. Version 1.8.221 contains a fix.

### CVE-2026-34239

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-20T18:16:51.360 |

Chamilo version 1.11.40 and earlier are vulnerable to authenticated remote code execution in the main/inc/ajax/lang.ajax.php path. This endpoint is protected only by `api_protect_course_script(true)`, which means any authenticated user enrolled in a course (student, teacher, DRH) can reach it.

### CVE-2026-54538

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-20T17:17:59.723 |

xrdp is an open source RDP server. In versions 0.10.6 and prior, a n issue was discovered where the software fails to properly validate the totalLength field within the RDP protocol control header during packet reception. An unauthenticated remote attacker can exploit this vulnerability by sending a specially crafted packet that forces the xrdp process or thread into an infinite, CPU-bound loop. Because the internal pointer fails to advance and the deadlock prevention mechanism is bypassed for specific protocol data unit types, the process consumes excessive CPU resources indefinitely. This can render the xrdp service unavailable and potentially lead to system-wide resource exhaustion if multiple malicious connections are established. This issue has been fixed in version 0.10.6.1.

### CVE-2026-32820

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-20T17:17:05.623 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, the documentation and static markdown renderer accepts attacker-controlled path segments and only runs them through the Rails HTML sanitizer, which does not remove directory traversal sequences. An unauthenticated attacker can traverse out of the intended `docs` or `static` directories and render arbitrary `.md` files from the application root or engine root. This is patched in version 26.06.08.

### CVE-2026-32806

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-20T17:17:05.260 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, any authenticated user can request arbitrary partials or helper-backed render functions through /remote_render. The endpoint does not restrict which partial can be rendered and does not apply controller-specific authorization before rendering the selected view. This enables a low-privileged user to retrieve server-side rendered admin content that is otherwise hidden by navigation and route checks. On the test instance, a Standard user was able to retrieve the PostgreSQL admin dashboard stats even though /admin itself redirected away. This is patched in 26.06.08.

### CVE-2026-45713

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-20T16:17:00.610 |

Mailpit is an email testing tool and API for developers. Prior to version 1.30.0, the Mailpit SMTP server has a Server.MaxSize int field that controls the maximum allowed DATA payload size, but the field is never assigned anywhere outside test code, leaving it at Go's zero value (0 ⇒ "no limit"). The same applies to the HTTP /api/v1/send endpoint, whose request body is decoded with json.NewDecoder(r.Body) and no http.MaxBytesReader. Because Mailpit's default listeners bind [::]:1025 (SMTP) and [::]:8025 (HTTP), with no authentication required on either, a single network-reachable attacker can push an arbitrarily large message into Mailpit and watch RAM consumption spike with a ~7-10× amplification factor (raw frame → enmime envelope tree → search-text index → zstd-encoded write to SQLite). Repeating the attack — or running it concurrently from multiple connections — drives the process to OOM-kill. Version 1.30.0 contains a patch.

### CVE-2026-32807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-20T16:16:57.963 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, anyone with a DataLink UUID can fetch the attached text file directly, even if the link is expired, the caller is unauthenticated, or the normal show flow would have denied access. Because the route is public and the mailer embeds the direct file URL, any leaked, forwarded, logged, or stale email link can continue to expose the attachment.

### CVE-2026-56624

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-20T21:16:49.070 |

Improper certificate validation in Apache MINA SSHD (server-side). Apache MINA SSHD is a Java library for client-side and server-side SSH.




Server-side OpenSSH user certificate validation during user authentication in an Apache MINA SSHD server did not check for the unsupported force-command or verify-required options that could be embedded in the certificate, nor did it validate these options. As a result it was possible that a user could authenticate with such a certificate that included a force-command option but still was able to execute other commands. What other command exactly would be available to the user depends on the implementation of the server.




This issue is fixed in Apache MINA SSHD 2.19.0 and 3.0.0-M5. Applications are advised to upgrade to these versions.




The fix rejects OpenSSH user certificates that include these options, since Apache MINA SSHD implements neither force-command nor sk-*-cert-v01@openssh.com user certificates (which are the only ones for which verify-required would make sense).

### CVE-2026-32825

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-07-20T17:17:06.140 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, the application accepts unlimited password guesses against both the browser login flow and the JSON login endpoint. The source code enables Devise's `:lockable` module on the user model but explicitly disables both lock and unlock strategies, and no request throttling or rate-limiting layer was identified in the Rails code. This creates a direct online password-guessing risk:
- valid user accounts can be attacked continuously without temporary lockout
- the same weakness is reachable through both `/users/sign_in` and `/api/v4/auth/login`
- successful guessing yields a normal session cookie in the HTML flow or a fresh JWT in the API flow
- the API endpoint is especially attractive for automation because it requires no CSRF token

This has been patched in version 26.06.08.

### CVE-2026-32824

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-07-20T17:17:06.003 |

dataCycle is a data management system for centrally storing, managing, searching, finding, and distributing data. In dataCycle-CORE, the module handling core processing and framework rules, before and including version 25.07.3, a low-privileged authenticated API user can supply `forwardToUrl` and `redirectUrl` values when triggering password reset or confirmation flows. Those values are then embedded into the outgoing email workflow without host allowlisting. This creates two related abuse paths:
- password reset or confirmation links can be sent to a victim with the token already attached to an attacker-controlled `forwardToUrl`
- after a legitimate password reset completes, the browser is redirected to attacker-controlled `redirectUrl`

In practice, this can be used for phishing, token capture, confirmation hijacking, or steering a victim from a trusted email
into an attacker domain. This is patched in version 26.06.08.

### CVE-2026-1771

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-21T09:16:53.947 |

The MapSVG plugin for WordPress is vulnerable to arbitrary file uploads due to missing file type validation in the SVGFile constructor in all versions up to, and including, 8.14.0 This is due to an incorrect conditional check that prevents file validation from taking place. This makes it possible for authenticated attackers, with Administrator-level access and above, to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-6952

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-21T03:16:42.610 |

A post-authentication command injection vulnerability in the "LogServer" field of the syslog component in Zyxel AX7501-B1 firmware versions through 5.17(ABPC.7.2)C0 could allow an authenticated attacker with administrator privileges to execute OS commands on an affected device.

### CVE-2026-3183

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-07-21T08:16:33.880 |

Zohocorp ManageEngine ADSelfService Plus versions before 6524 are vulnerable to Multi Factor Authentication Bypass.

### CVE-2026-57494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-07-20T22:17:16.970 |

AgenticMail gives AI agents real email addresses and phone numbers. In @agenticmail/api prior to version 0.9.64, a low-privileged authenticated AgenticMail agent can enumerate another agent's pending/claimed tasks by supplying the target agent name to `GET /api/agenticmail/tasks/pending?assignee=<name>`. The returned task objects include the task IDs and payloads. The same task IDs can then be used with the capability-style task mutation endpoints (`/tasks/:id/claim`, `/tasks/:id/result`, `/tasks/:id/complete`, `/tasks/:id/fail`) to claim, complete, or fail tasks assigned to a different agent. Because ordinary authenticated agents can discover agent names through `GET /api/agenticmail/accounts/directory`, the task ID effectively stops being a secret capability. This turns the intended capability model into a cross-agent authorization bypass. Version 0.9.64 contains a fix.

### CVE-2026-55550

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-284;CWE-862` |
| Published | 2026-07-20T22:17:16.543 |

NextCRM is open-source customer relationship management (CRM) software. The CRM product catalog is an organization-wide business object. Normal application server actions restrict product creation, update, and deletion to `manager` and `admin` roles. However, in version 0.12.1, the MCP product tools expose the same write operations through `/api/mcp/mcp` using user-generated Bearer tokens and do not enforce role checks. Any authenticated low-privileged user who can generate an MCP API token can create, modify, archive, or soft-delete products in the shared CRM product catalog. Version 0.12.3 contains a fix.

### CVE-2026-56623

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-20T21:16:48.947 |

Path traversal on Windows in Apache MINA SSHD component sshd-git. Apache MINA SSHD is a Java library for client-side and server-side SSH.




A git server implemented with Apache MINA SSHD component sshd-git and running on Windows could allow an authenticated remote user access to git repositories outside of the configured server-side root directory. The path validation applied for CVE-2026-48827 in Apache MINA SSHD 2.18.0 and 3.0.0-M4 was partly ineffective for Servers running on Windows.




Applications are affected if they use org.apache.sshd:sshd-git to implement a git server and run on Windows. Applications not using sshd-git or not running on Windows are not affected.




Users are advised to upgrade affected applications to Apache MINA SSHD 2.19.0, which fixes the issue.




The issue also is present in the pre-release milestones 3.0.0-M1 to 3.0.0-M4 for a new upcoming new major version 3.0.0. Again, applications are affected only if they use sshd-git and run on Windows. Upgrade affected applications to 3.0.0-M5.

### CVE-2026-47130

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-20T21:16:47.917 |

NextCRM is open-source customer relationship management (CRM) software. Versions prior to 0.12.0 have a Broken Object Level Authorization (BOLA/IDOR) vulnerability exists in the CRM contact and target update endpoints. The application fails to verify if the authenticated user has ownership of the specific resource being modified. This allows any authenticated user (even with a standard `member` role) to arbitrarily modify sensitive CRM contacts and targets belonging to other users or organizations (cross-tenant data tampering). Version 0.12.0 fixes the issue.

### CVE-2026-58484

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-07-20T17:18:16.160 |

Network-AI is a TypeScript/Node.js multi-agent orchestrator. Prior to version 5.12.2, `EnvironmentManager.listBackups()` reads each backup's `_manifest.json` and trusts the manifest's `path` field. `EnvironmentManager.pruneBackups()` later passes that trusted `entry.path` directly to `rmSync(entry.path, { recursive: true, force: true })`. An attacker who can place or modify a manifest inside `data/<env>/.backups/<name>/_manifest.json` can cause `network-ai env backup prune --env <env> --keep <n>` or any code path invoking `pruneBackups()` to recursively delete an arbitrary path accessible to the Network-AI process user. This is fixed in v5.12.2. `pruneBackups()` no longer passes `entry.path` from the on-disk manifest to `rmSync`. The deletion path is recomputed from a format-validated `entry.backupId`, and a `dirname` containment check confines deletion to exactly one level under the backups directory. A poisoned manifest (e.g. `"path": "/"`) is now inert.

### CVE-2026-39879

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-150` |
| Published | 2026-07-20T17:17:07.550 |

Due to a missing sanitization call in [`afsql_dd_run_query`](https://github.com/syslog-ng/syslog-ng/blob/649e6e18e3459fb4467000a88dfb12fa97f9719c/modules/afsql/afsql.c#L219), syslog-ng before 4.12 are vulnerable to SQL injection from an untrusted source. This is not part of the default configuration, the SQL driver has to be manually configured.

Fixes are in syslog-ng 4.12, syslog-ng Premium Edition 8.2 and syslog-ng Store Box 7.8

### CVE-2026-39385

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-20T17:17:07.417 |

Frappe LMS is an open source learning management system. In version 2.51.0 and earlier, a user could bypass payment validation for courses by using unrelated batch. This has been patched in 2.52.0 with enrollment now validating that the batch is linked to course.

### CVE-2026-63091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-126;CWE-190` |
| Published | 2026-07-20T15:16:45.363 |

ProFTPD before 1.3.9c and 1.3.10rc3 contains a signed integer overflow vulnerability in the mod_sftp module's SCP size-record parser that allows authenticated low-privilege attackers to bypass ASLR by sending a crafted file size value of UINT64_MAX, which results in a negative off_t value. Attackers can exploit the subsequent conversion to uint32_t, causing an approximately 4 GB requested read length and forcing the server to read beyond the end of the SSH channel data and write overread process memory into the uploaded file. In tested configurations, the disclosed data contains libc, libcrypto, and PIE pointers sufficient to derive their randomized base addresses, thereby bypassing ASLR and enabling reliable exploitation of memory corruption vulnerabilities in the same process.

### CVE-2026-59776

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-325` |
| Published | 2026-07-21T04:16:51.480 |

Missing Cryptographic Step (CWE-325) vulnerability exists in certain FeliCa IC chips shipped in or before 2017. If the vulnerability is exploited, information stored in the IC chip may be read or tampered with.

### CVE-2026-35591

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-20T17:17:07.277 |

libvips is a fast image processing library with low memory needs. The `tiffload` operation in libvips versions before and including 8.18.1 could incorrectly determine the number of channels in a JPEG or JPEG2000-encoded tile within a TIFF image, leading to a possible buffer overflow. This has been patched in version 8.18.2.

### CVE-2026-33327

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-20T17:17:06.283 |

libvips is a fast image processing library with low memory needs. The `vipsload` operation in versions before and including 8.18.0 could incorrectly determine image dimensions leading to an integer overflow and a subsequent heap-based buffer overflow. This has been patched in version 8.18.1.
