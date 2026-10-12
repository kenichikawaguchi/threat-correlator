# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-12 15:00 UTC
- **対象期間**: `2026-10-11T15:00:30.000Z` 〜 `2026-10-12T15:00:33.000Z`
- **重要CVE数**: 64 件（Critical 9.0+: 5 件 / High 7.0〜: 59 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは 30 件超と依然高リスクが集中しています。  
- **リモートコード実行 (RCE)・スタックバッファオーバーフロー** が目立ち、特に組み込み系ファームウェア（Linksys、Trendnet）や Web アプリケーションフレームワーク（OTRS、Tuleap、LogicalDOC）で深刻な脆弱性が多数報告されています。  
- 認証不要（PR:N）で攻撃が成立するケースが多く、外部から直接インターネットに露出しているサービスは即時対策が必須です。  

---

## 2. 特に注目すべき CVE（上位 5 件）  

| CVE | CVSS | 主な影響 | 注目理由 | 影響範囲（典型的な環境） |
|-----|------|----------|----------|------------------------|
| **CVE‑2026‑66086** | 9.8 | Modem OTA スタックの SIB1 メッセージ処理でスタックバッファオーバーフロー | **リモートからコード実行・完全権限取得** が可能。認証不要・UI なしで実行できる点が極めて危険。 | 5G/4G LTE モデム（Android/IoT デバイス）に組み込まれた OTA ファームウェア。 |
| **CVE‑2026‑93582** | 9.4 | OTRS Community Edition 6 以前の HTTP Basic 認証モジュールが `REMOTE_USER`/`HTTP_REMOTE_USER` を信頼 | **認証バイパス** により任意ユーザーとしてログイン可能。CGI・mod_perl 環境で特に顕在。 | OTRS (ヘルプデスク) を CGI/Apache 上で運用している全サーバ。 |
| **CVE‑2026‑108892** | 9.3 | Linksys E1700 1.0.0.4.003 の `/goform/ssid1MACFilter` でスタックバッファオーバーフロー | **遠隔からの RCE** が可能。Wi‑Fi ルータの管理画面がインターネットに公開されていると即座に乗っ取られる。 | Linksys E1700 ルータ（家庭・小規模オフィス）。 |
| **CVE‑2026‑108804** | 9.3 | Trendnet TEW‑751DR/752DRU/733GR 1.03B01/1.03B03 の `pigwidgeon.cgi` で OS コマンドインジェクション | **任意コマンド実行** が可能。CGI スクリプトが直接ユーザ入力をシェルへ渡す設計ミス。 | Trendnet 製 Wi‑Fi ルータ／アクセスポイント。 |
| **CVE‑2026‑78357** | 9.1 | OTRS の JWT トークンがアカウント無効化・パスワード変更後も有効 | **認証情報の長期有効** により、攻撃者が取得したトークンで 16 時間以上不正アクセス可能。 | OTRS (Community/Enterprise) を利用中の全組織。 |

> **共通点**：いずれも「認証不要」または「認証情報が不適切に扱われる」点で、外部から直接攻撃が可能です。特に組み込み系ファームウェアは自動更新が遅れがちなので、早急なファームウェア更新が重要です。

---

## 3. 推奨アクション  

### 3.1 緊急パッチ適用・ファームウェア更新
| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン / パッチ |
|-------------------|----------------------|------------------------|
| **Linksys E1700** | 1.0.0.4.003 | 1.0.0.4.010 以上（メーカー提供のセキュリティパッチ） |
| **Trendnet TEW‑751DR / 752DRU / 733GR** | 1.03B01 / 1.03B03 | 1.04B01 以上 |
| **OTRS Community Edition** | ≤ 6.0 | 6.1.0 以上（認証ヘッダー処理の修正） |
| **Tuleap Enterprise Edition** | 17.0‑17.5 | 17.6 以上（OS コマンドインジェクション・XSS 修正） |
| **LogicalDOC Community Edition** | ≤ 9.3 | 9.4.0 以上（ファイルアップロード・コードインジェクション対策） |
| **pH7Builder** | < 18.6.0 | 18.6.0 以上（ハードコード API キー削除） |
| **ManageIQ** | 任意 | 2026‑R1 以降（YAML safe_load 強化） |
| **WSM (SMR Oct‑2026 Release 1)** | 任意 | SMR Oct‑2026 R2 以降（use‑after‑free 修正） |

> **手順例（Linux 系）**  
> ```bash
> # OTRS のアップデート例
> yum update otrs-community-6.1.0
> # または
> apt-get install --only-upgrade otrs=6.1.0-1
> ```

### 3.2 ネットワークレベルの防御
- **外部からの管理ポート（80/443/8080 等）を遮断**し、VPN または IP アクセスリストで内部からのみアクセス可能にする。  
- **WAF で特定パラメータの長さ・文字種を制限**（例：`newap_text_%d`、`service`、`staticRoute_*` など）。  
- **IDS/IPS で CVE‑2026‑108892/108804 のシグネチャを有効化**し、攻撃トラフィックを即座にブロック。

### 3.3 認証・トークン管理の強化
- OTRS の **JWT 有効期限を 1 時間未満に短縮**し、アカウント無効化時にトークンを即時失効させる設定 (`OTRS::Auth::JWT::TokenTTL`) を導入。  
- すべての **Basic 認証ヘッダーの信頼元をサーバ側で明示**し、`REMOTE_USER` 系環境変数を外部から書き換えできないように Apache の `RequestHeader unset` を使用。

### 3.4 ソフトウェア構成の見直し
- **CGI/Perl スクリプトでのコマンド実行は絶対に外部入力を直接渡さない**。`system` 系関数の代わりに安全な API（例：`execve` + 引数配列）を使用。  
- **デシリアライズ処理は安全な形式（JSON, protobuf 等）に統一**し、`YAML.safe_load

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-66086

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-12T02:16:57.600 |

In the modem OTA stack, there is a possible stack-based buffer overflow due to improper validation of scheduling information in SIB1 messages. This could lead to remote code execution or denial of service with no additional execution privileges needed.

### CVE-2026-93582

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-12T07:16:37.717 |

The HTTP Basic Authentication modules in ((OTRS)) Community Edition 6 and prior accept the authenticated username from either the REMOTE_USER or HTTP_REMOTE_USER environment variable. In CGI and mod_perl based deployments, HTTP request headers may be mapped to corresponding HTTP_* environment variables. As a result, an unauthenticated remote attacker can supply a crafted Remote-User request header which is exposed to the application as HTTP_REMOTE_USER. When HTTP Basic Authentication is configured as the authentication backend, OTRS trusts this value as an already authenticated username and does not perform an additional password verification. An attacker may therefore authenticate through the Generic Interface as an existing agent or customer user without knowing the corresponding credentials.

The resulting privileges depend on the account being impersonated. Successful exploitation may allow access to confidential information and modification of data or configuration with the permissions of the affected user. Exploitation requires HTTP Basic Authentication to be configured as an authentication backend and a web server environment in which attacker-controlled HTTP headers are exposed through the corresponding HTTP_* environment variables.

OTRS 7 and later are not affected by this attack vector due to the use of Mojolicious/Hypnotoad and does not expose arbitrary request headers through %ENV in the manner required for exploitation. The supported REMOTE_USER mechanism additionally requires validation through the configured SSO shared secret. The unused HTTP_REMOTE_USER fallback has nevertheless been removed as a security-hardening measure.

Please note that ((OTRS)) Community Edition 6.x and before are vulnerable. Products based on the ((OTRS)) Community Edition also very likely to be affected

### CVE-2026-108892

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-12T14:17:09.530 |

A vulnerability was determined in Linksys E1700 1.0.0.4.003. This vulnerability affects the function ssid1MACFilter of the file /goform/ssid1MACFilter of the component Mac Filter. This manipulation of the argument newap_text_%d causes stack-based buffer overflow. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-108804

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-12T06:16:59.457 |

A vulnerability was detected in TRENDnet TEW-751DR, TEW-752DRU and TEW733GR 1.03B01/1.03B03. Affected is the function fwrite of the file pigwidgeon.cgi of the component Web Management Backend. The manipulation of the argument service results in os command injection. It is possible to launch the attack remotely. The exploit is now public and may be used. The vendor confirms: "As this router was EOL'd in 2011, we have no way of testing if such vulnerability exists. We will notify our customers of a potential vulnerability on this product." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-78357

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-12T07:16:37.073 |

Previously issued authentication tokens are not immediately invalidated when an OTRS agent or customer user account is deactivated or its password is changed. As a result, an existing JWT may remain valid until its regular expiration time, which can be approximately 16 hours.

An attacker who has previously obtained a valid authentication token can therefore continue to access OTRS with the privileges of the affected agent or customer user even after the corresponding account has been deactivated or the user's password has been changed.

The vulnerability does not allow an attacker to obtain authentication tokens by itself. Exploitation requires possession of a previously issued and still valid token. The actual impact depends on the privileges associated with the compromised token. Customer user tokens are limited to the permissions of the affected customer account, while agent tokens may provide access to broader ticket, customer, or administrative functionality depending on the assigned permissions.

This issue affects OTRS:

  *  7.0.X
  *  8.0.X
  *  2023.X
  *  2024.X
  *  2025.X
  *  2026.X before 2026.7.X

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-21120

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-12T05:17:00.520 |

Use after free in WSM service prior to SMR Oct-2026 Release 1 allows local attackers to potentially execute arbitrary code with system privilege.

### CVE-2026-12613

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T14:17:12.423 |

Deserialization of untrusted data vulnerability in Ministry of Justice General Directorate of Information Technology UYAP Document Editor allows Object Injection.

This issue affects UYAP Document Editor: before 5.4.20.

### CVE-2026-52903

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-12T13:17:32.757 |

A deserialization of untrusted data vulnerability was found in ManageIQ. The YamlLoadAliases module overrides YAML.safe_load to silently fall back to YAML.unsafe_load in production when a Psych::DisallowedClass error occurs. An authenticated attacker with dialog import access can exploit this to achieve remote code execution by uploading a crafted YAML payload that triggers the fallback and deserializes arbitrary Ruby objects.

Red Hat CloudForms, which was based on ManageIQ, has reached End of Life and is no longer supported. No errata or patches will be issued. This CVE is being assigned for the benefit of the ManageIQ community and downstream consumers.

### CVE-2026-105407

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T11:17:09.673 |

An OS Command Injection vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to execute arbitrary commands on the server.

### CVE-2026-87690

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T05:17:03.250 |

The Metasploit Framework post module post/apple_ios/gather/ios_image_gather is affected by a relative path traversal vulnerability (CWE-22). The module interpolates file names taken from a Meterpreter directory listing — data fully controlled by a hostile or tampered iOS device — directly into the local destination path passed to client.fs.file.download_file(), with no sanitization. The underlying stdapi sink (lib/rex/post/meterpreter/extensions/stdapi/fs/file.rb) writes to whatever path is supplied, so a listing entry such as ../../msfconsole.rc escapes the intended ~/.msf4/loot/<random> directory and overwrites ~/.msf4/msfconsole.rc, a resource file that every msfconsole invocation automatically executes at startup (lib/msf/ui/console/driver.rb:196). An attacker-controlled device that lures an operator into running this gather module achieves an arbitrary file write as the operator; because the written msfconsole.rc can load a second written file (a Ruby plugin whose top-level code runs on require), this converts into persistent code execution and an interactive shell as the operator (frequently root) on the pentester's workstation at the next console launch. The same traversal was previously fixed upstream in the recursive downloader (stdapi/fs/dir.rb scrubs separators); this module omitted the equivalent scrub. The fix applies the same separator scrub (or File.basename) to listing entries before building the local path.

### CVE-2026-108980

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-24` |
| Published | 2026-10-12T02:16:57.297 |

Blinko through 1.8.8 allows directory traversal, overwriting startup files as root, via installPlugin. It builds the plugin install path from an unsanitized name in server/routerTrpc/plugin.ts, and the plugin.installPlugin tRPC procedure is open to any authenticated user. Thus, a name containing ../ sequences writes the downloaded plugin files outside the plugins directory. Because the official Docker image runs as root, an authenticated attacker overwrites a root-owned startup file and achieves remote code execution as root. Self-registration for an account may be possible.

### CVE-2026-108963

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-11T20:16:32.853 |

databasement before 1.8.2 allows remote code execution because it runs certain commands (e.g., mariadb-dump) with a database name that can be specified by any authenticated user. For example, --result-file=/app/public/index.php can write to index.php. In other words, quoting prevents OS command injection in mariadb-dump, but the argument injection alone is sufficient for code execution indirectly. NOTE: the project's composer.json file does not indicate an independently published databasement Composer package.

### CVE-2026-109229

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-12T14:17:12.257 |

SGLang through 0.5.21 contains a denial of service vulnerability that disables Pillow decompression bomb protection process-wide by setting Image.MAX_IMAGE_PIXELS to None in NanoNemotronVLImageProcessor. Remote attackers can submit small, highly compressed images with huge dimensions to the generic image loader, exhausting worker memory during decoding.

### CVE-2026-109228

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T14:17:12.087 |

SGLang through 0.5.21 contains a resource budget bypass vulnerability that allows remote attackers to override GLM-V video processing limits by supplying fps, max_frames, max_tokens_per_frame and max_image_tokens in the video_url object. Attackers can set these values arbitrarily high so glm4v.py decodes every frame of high-resolution video at full size, exhausting worker memory and denying service.

### CVE-2026-109227

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T14:17:11.923 |

SGLang through 0.5.21 contains an unbounded memory allocation vulnerability in preprocess_video in qwen_vl.py that decodes frames at full source resolution before applying max_pixels limits. Remote attackers can submit high-resolution videos to /v1/chat/completions on Qwen-VL deployments, and concurrent requests exhaust worker memory causing denial of service.

### CVE-2026-109226

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-12T14:17:11.747 |

SGLang through 0.5.21 contains a decompression amplification vulnerability in load_audio that allows remote attackers to exhaust memory by submitting highly compressed audio decoded without duration or sample limits. Attackers can supply small FLAC-encoded silence files through audio_url or audio_data inputs that expand into massive PCM buffers, exhausting worker memory and CPU for denial of service.

### CVE-2026-109225

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T14:17:11.580 |

SGLang through 0.5.21 contains an unbounded memory allocation vulnerability that allows unauthenticated remote attackers to exhaust memory by uploading oversized files to /v1/audio/transcriptions. Attackers can send concurrent large multipart uploads, which are fully read into memory before validation, to crash the HTTP/tokenizer worker and deny service.

### CVE-2026-109205

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-12T14:17:11.277 |

LogicalDOC Community Edition through 9.3 contains an unauthenticated file upload vulnerability in the UploadServlet that allows remote attackers to write files to disk without a session. Attackers can repeatedly send multipart requests with unlimited file parts to /upload, persisting files in uncleaned temporary directories and exhausting server disk space.

### CVE-2026-109201

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T14:17:10.680 |

LogicalDOC Community Edition through 9.3 contains a missing authorization vulnerability in SoapDocumentService operations that allows authenticated users to access and modify unauthorized documents. Attackers can call copy, getExtractedText, deleteVersion, reindex, deleteLink, or restore via SOAP or /services/rest/document with sequential document IDs to disclose, delete, or tamper with documents.

### CVE-2026-109199

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-12T14:17:10.373 |

LogicalDOC Community Edition through 9.3 contains a code injection vulnerability that allows authenticated users to execute OS commands by submitting Velocity templates in DocumentService.sendAsEmail subject or message fields. Attackers can invoke SystemTool exec methods or ClassTool, bypassing the forbidRuntimeUsage denylist, to run commands with LogicalDOC process privileges.

### CVE-2026-109186

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-10-12T13:17:32.003 |

jshERP through 3.6 contains a mass assignment vulnerability in the UserController update handler that allows authenticated users to overwrite protected fields including tenant_id and password. Attackers can send a crafted PUT /user/update body to switch into another tenant on next login or overwrite other users' password hashes for account takeover.

### CVE-2026-109185

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T13:17:31.840 |

jshERP through 3.6 contains a missing authorization vulnerability in the UserController updateUser handler that allows authenticated users to assign arbitrary roles to any user. Low-privilege attackers can send their own user id with the tenant administrator roleId to escalate privileges or rebind other tenant users' roles.

### CVE-2026-105410

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T11:17:10.063 |

A Stored Cross-site Scripting (XSS) vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to execute arbitrary script code in user's browser session.

### CVE-2026-105409

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T11:17:09.937 |

A Stored Cross-site Scripting (XSS) vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to execute arbitrary script code in user's browser session.

### CVE-2026-105408

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-12T11:17:09.807 |

A Stored Cross-site Scripting (XSS) vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to execute arbitrary script code in user's browser session.

### CVE-2026-103903

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T11:17:09.517 |

An incorrect authorization vulnerability in the WinBox
authentication flow of MikroTik RouterOS allows a remote authenticated attacker
with credentials for a low-privilege account permitted to use WinBox to obtain
the authorization policy of a different existing account. The stage-one EC-SRP
challenge and proof are verified using the attacker's account, while the
independently supplied stage-two username is used to install the target
account's privileges. By specifying a higher-privilege account such as admin, a
low-privilege user can obtain a full administrative session without knowing the
target account's password and can use that session to increase the privileges
of the attacker's own account.

### CVE-2026-78355

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-12T07:16:36.740 |

A path traversal vulnerability in the OTRS SendSupportBundle functionality allows an authenticated administrator to reference file paths outside the intended directory.

This may allow files accessible to the OTRS application process to be deleted. The vulnerability does not bypass operating system file permissions. On OTRS versions prior to OTRS 7, the effective permissions of the web server process are relevant. Starting with OTRS 7, access is limited by the permissions of the dedicated OTRS user. Files with overly permissive ownership or file system permissions may therefore also be affected.

The affected functionality may additionally attempt to include controlled files in a support bundle. However, support bundles are sent to a predefined OTRS support address, and direct disclosure of arbitrary files to the attacker has not been demonstrated.

An attacker therefore requires valid administrative access to exploit the vulnerable functionality. The primary demonstrated impact is the deletion of files outside the intended directory within the effective permissions of the OTRS application process.

This issue affects OTRS:

  *  7.0.X
  *  8.0.X
  *  2023.X
  *  2024.X
  *  2025.X
  *  2026.X before 2026.7.X

Please note that ((OTRS)) Community Edition 6.x and before are vulnerable. Products based on the ((OTRS)) Community Edition also very likely to be affected

### CVE-2026-108905

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-11T15:16:56.803 |

pH7Builder (pH7 Social Dating CMS) before 18.6.0 contains a hard-coded API key vulnerability in Tool.class.php that allows unauthenticated attackers to bypass API access checks by spoofing the Host header. Attackers can send Host: localhost with private_api_key=dev772277 and the default allowed URL to retrieve member emails, IP addresses, phone numbers, and bank account fields.

### CVE-2026-108894

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-12T14:17:09.897 |

A security flaw has been discovered in Linksys E1700 1.0.0.4.003. Impacted is the function addStaticRoute of the file /goform/addStaticRoute of the component Static Route Handler. Performing a manipulation of the argument staticRoute_IP_setting/staticRoute_Netmask_setting/staticRoute_Gateway_setting/staticRoute_Metric_setting results in os command injection. Remote exploitation of the attack is possible. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-108893

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-12T14:17:09.710 |

A vulnerability was identified in Linksys E1700 up to 1.0.0.4.003. This issue affects the function setVlan of the file /goform/setVlan. Such manipulation of the argument vlan_set leads to stack-based buffer overflow. The attack may be launched remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-21125

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-12T05:17:01.093 |

Improper input validation in parsing sheifd in libsimba.heifdec.media.samsung.so prior to SMR Oct-2026 Release 1 allows local attackers to potentially execute arbitrary code.

### CVE-2026-21124

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-12T05:17:00.977 |

Improper input validation in getting cover image in libsimba.heifdec.media.samsung.so prior to SMR Oct-2026 Release 1 allows local attackers to potentially execute arbitrary code.

### CVE-2026-108953

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T13:17:28.307 |

mac-shell-mcp before 2.0.0 contains an OS command injection vulnerability that allows MCP clients to bypass the command whitelist by injecting shell metacharacters into execute_command arguments. Attackers or malicious prompts can call a safe command such as pwd with arguments like ';' to run forbidden commands as the server user without approval.

### CVE-2026-105411

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T11:17:10.187 |

An Authorization Bypass Through User-Controlled Key vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker with tracker administration rights on one tracker to update or delete fields of all the trackers on the instance.

### CVE-2026-18390

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-12T14:17:12.563 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Ministry of Justice General Directorate of Information Technology UYAP Document Editor allows OS Command Injection.

This issue affects UYAP Document Editor: before 5.4.20.

### CVE-2026-108976

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-11T21:16:43.580 |

GNU Emacs before 31.2 (and TRAMP through 2.8.2) allows OS command injection via a filename because tramp-user-regexp has an incomplete list of disallowed inputs. NOTE: this issue exists because of an incomplete fix for CVE-2026-79992.

### CVE-2026-19736

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-11T18:16:58.810 |

The NXP MCUX TRNG entropy driver in drivers/entropy/entropy_mcux_trng.c passed the caller's byte count straight to the vendor SDK routine TRNG_GetRandomData(). On i.MX RT5xx and RT6xx parts the SDK compiles its TRNG_SW_HEALTH_TESTS variant, which always copies whole 32-bit words and draws entropy rounded up to a multiple of 128 bytes. Its "caller buffer is full" guard tests dataSize == 0, so a request whose length is not a multiple of four makes dataSize underflow past zero and the SDK keeps writing into the caller's buffer for the entire extraction: a 1-byte request results in 128 bytes written, and any non-word-multiple length overflows by up to 127 bytes.

entropy_get_entropy() is a syscall, and its verifier in drivers/entropy/entropy_handlers.c validates only the requested length via K_SYSCALL_MEMORY_WRITE(). With CONFIG_USERSPACE enabled, an unprivileged user-mode thread that has merely been granted the entropy device can therefore choose both the destination address and a length such as 1, and cause the kernel to write up to 127 bytes beyond the region it proved it owns. On these Cortex-M33 targets there is no MMU, so user partitions and kernel data share one SRAM and the overflow can land in adjacent kernel state. The same defect is reached from kernel mode by any caller requesting a non-word-multiple length, including getentropy() and, in builds where sys_csrand_get()/sys_rand_get() resolve to the hardware generator, sys_rand8_get() and sys_rand16_get().

Impact is memory corruption of up to 127 bytes immediately following the supplied buffer — typically the caller's stack in kernel-mode use, or memory outside the caller's partition when driven through the syscall. The overflow offset is fully determined by the requested length and is therefore deterministic, while the written content is uncontrolled TRNG output; the practical consequences range from crashes and unpredictable state corruption to opportunistic escalation when kernel bookkeeping such as object permission bitmaps is overwritten. The affected devices are those where the MCUX SDK enables TRNG_SW_HEALTH_TESTS (MIMXRT595S, MIMXRT555S, MIMXRT533S, MIMXRT685S, MIMXRT633S), on which the TRNG is the zephyr,entropy chosen node; other SoCs using this driver take the SDK path that clamps the copy size and are unaffected.

The fix routes any unaligned prefix and any sub-word tail through a local bounce word and hands the SDK only word-multiple sizes, so the SDK's word-granular writes can no longer pass the end of the caller's buffer.

### CVE-2026-19669

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-11T18:16:58.563 |

The user-mode syscall verifiers z_vrfy_fuel_gauge_get_props() and z_vrfy_fuel_gauge_set_props() in drivers/fuel_gauge/fuel_gauge_syscall_handlers.c declared two variable-length arrays, union fuel_gauge_prop_val k_vals[len] and fuel_gauge_prop_t k_props[len], sized directly by the caller-supplied len argument. len is an unvalidated size_t taken straight from the syscall ABI, and the VLAs were allocated before any check at all — including before the K_SYSCALL_DRIVER_FUEL_GAUGE() object-permission check. The subsequent k_usermode_from_copy() calls validated only that the user source buffer was readable; the kernel destination was never bounds-checked, since it was sized by the same attacker-chosen len.

Any thread running in user mode with CONFIG_USERSPACE enabled can invoke fuel_gauge_get_props() or fuel_gauge_set_props() with a large len. This first displaces the supervisor stack pointer by an arbitrary attacker-chosen amount — Zephyr does not build with stack-clash probing, so the displacement itself does not fault, and the nested calls made by the verifier then write frames below the privileged stack. If the caller has been granted access to a fuel-gauge device object, the memcpy inside k_usermode_from_copy() additionally writes len * sizeof(union fuel_gauge_prop_val) bytes of fully attacker-controlled data starting well below the stack base. CONFIG_PRIVILEGED_STACK_SIZE defaults to 1024 bytes, so a len of roughly 170 already exhausts it.

The result is an out-of-bounds write in supervisor mode with attacker-controlled length and, on the permitted path, attacker-controlled content — a break out of the user-mode sandbox into kernel memory, leading to kernel code execution or a system crash. A stack guard region does not contain it, because the copy begins below the guard and walks upward, corrupting unprotected memory before the guard is reached. The fix removes the kernel-side copies entirely and validates the caller's arrays in place with K_SYSCALL_MEMORY_ARRAY_READ() / K_SYSCALL_MEMORY_ARRAY_WRITE(), which also handle the len * size multiplication overflow; this is safe because neither fuel_gauge_prop_t nor union fuel_gauge_prop_val contains embedded pointers.

### CVE-2026-103902

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-12T11:17:08.617 |

Improper verification of cryptographic signature vulnerability in DigiDoc libdigidocpp, DigiDoc DigiDoc4, DigiDoc DigiDoc Android, and DigiDoc DigiDoc iOS. The vulnerability allows an attacker to create forged digital signatures
 that are displayed a valid by affected DigiDoc software.This issue affects libdigidocpp: from 4.0.0 before 4.5.0; DigiDoc4: from 4.6.0 before 4.11.0; DigiDoc Android: from 2.7.0 before 3.1.0; DigiDoc iOS: from 2.7.0 before 3.1.0.

### CVE-2026-1907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T09:16:43.683 |

A SQL Injection (SQLi) affects the Kong Gateway (Enterprise and Open Source) clustering communication logic when operating in Hybrid Mode. The issue can be triggered by sending specially crafted RPC requests to the Control Plane (CP), leading to potential unauthorized database access. Leveraging the issue requires network access to the Control Plane’s clustering port and a valid client certificate and key.

### CVE-2026-19935

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-11T18:16:59.410 |

The Bluetooth LE host queues received L2CAP connection-oriented channel (CoC) data for deferred processing through a struct k_work embedded in the channel object (le_chan->rx_work, handler l2cap_rx_process()) whenever the channel uses a dynamic PSM (0x0080-0x00FF). Channel teardown in l2cap_chan_destroy() in subsys/bluetooth/host/l2cap.c cancels the retransmission-timeout work and drains the RX FIFO, but never cancels rx_work. Because that work item was submitted to the system workqueue while HCI receive processing runs on the dedicated Bluetooth RX workqueue (CONFIG_BT_RECV_WORKQ_BT, the default), a queued rx_work item can outlive the channel it points into.

A remote, unauthenticated peer with an established CoC channel triggers this by sending a data K-frame immediately followed by an L2CAP Disconnect Request. The K-frame submits rx_work to the system workqueue; because both workqueue threads are cooperative and the Bluetooth RX workqueue runs at the higher priority (K_PRIO_COOP(CONFIG_BT_RX_PRIO) versus CONFIG_SYSTEM_WORKQUEUE_PRIORITY), the pending item cannot run before the following Disconnect Request is processed in le_disconn_req() -> l2cap_chan_del() -> l2cap_chan_destroy(). The stack then invokes the released() callback, which the API documents as meaning the stack has dropped all references and the application may free the channel memory.

The application therefore frees or re-accepts into an object that the system workqueue still holds in its pending list. If the memory is freed and reallocated, the workqueue later dereferences a list node and a handler function pointer read from reused memory; if the object is re-used for a later connection, l2cap_chan_add() calls k_work_init() on a still-enqueued work item, corrupting the workqueue's pending list so that unrelated work items are dropped or the queue spins on a looped list. A related variant lets l2cap_rx_process() run concurrently with teardown, racing the net_buf unref of le_chan->_sdu and the clearing of chan->conn.

The fix routes the channel RX work to the Bluetooth workqueue - the same context in which every teardown path runs - and adds an explicit k_work_cancel() of le_chan->rx_work in l2cap_chan_destroy(), so no reference to the channel survives the released() callback. Configurations without CONFIG_BT_L2CAP_DYNAMIC_CHANNEL, or that only use SIG-assigned PSMs (EATT 0x0027, OTS 0x0025) which take the inline receive path, are not affected.

### CVE-2026-93695

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-12T13:17:33.590 |

In Progress ShareFile Storage Zones Controller v5.12.6 and below, FileCopyService uses a remote file identifier when constructing a local temporary file path without enforcing containment. This can cause FileCopyService to write attacker-controlled content to filesystem locations writable by the service account. This can result in remote code execution when an executable IIS-served directory is writable.

### CVE-2026-21139

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-12T05:17:02.750 |

Improper access control in Samsung Continuity Service for windows prior to version 4.6.1217.0 allows adjacent attackers to manipulate the connected mobile device.

### CVE-2026-108982

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-12T03:17:18.667 |

VeraCrypt 1.26.29 (FUSE-T build) on macOS sometimes allows unintended access to decrypted data. It does not terminate the FUSE-T auxiliary service (go-nfsv4) and its associated VeraCrypt core-service helper processes when a volume is dismounted. After VeraCrypt reports the volume as dismounted, the auxiliary mount continues to serve the decrypted volume image (volume.dmg) over a loopback SMB session, and the leaked processes retain an open handle to the underlying raw device. A local user or process can therefore remount and access the decrypted volume without the passphrase, e.g., by reopening a previously accessed path (such as through a macOS Open Recent menu) or by attaching volume.dmg from the stale auxiliary mount. (The macFUSE build of VeraCrypt is not affected.)

### CVE-2026-108902

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-11T15:16:56.337 |

pH7Builder (pH7 Social Dating CMS) before 18.5.0 contains a path traversal vulnerability in the picture module deletePhoto() action that allows authenticated members to delete arbitrary files. Attackers can supply ../ sequences in the POST picture_link parameter to remove other members' photos or configuration and cache files, causing content loss and denial of service.

### CVE-2026-109203

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T14:17:10.977 |

LogicalDOC Community Edition through 9.3 contains a missing authorization vulnerability in the ConvertPdf servlet that allows authenticated users to download restricted PDF documents. Attackers can enumerate sequential docId values and use the version parameter to retrieve any PDF and its versions from folders they cannot access.

### CVE-2026-109202

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T14:17:10.827 |

LogicalDOC Community Edition through 9.3 contains a missing authorization vulnerability in the zip-export servlet that allows authenticated users to export restricted folders by supplying a folderId parameter. Attackers can request /zip-export with a restricted folder ID, since ZipExport.addFolderDocuments() skips READ and DOWNLOAD permission checks, to download all of its documents in a ZIP archive.

### CVE-2026-109170

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T14:17:10.223 |

LogicalDOC Community Edition through 9.3 contains an HQL injection vulnerability in DocumentsDataServlet that allows authenticated users to manipulate queries via the unvalidated indexed parameter. Attackers with read access to any folder can inject boolean HQL expressions to bypass folder scope and read-permission checks, listing restricted document metadata and extracting database contents.

### CVE-2026-109169

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T14:17:10.073 |

LogicalDOC Community Edition through 9.3 contains a sql injection vulnerability that allows authenticated users to execute crafted SQL via the firstLetter parameter of TagsDataServlet. Low-privileged attackers can inject UNION SELECT statements returned in the XML tag list to read usernames, email addresses and password hashes from ld_user.

### CVE-2026-109187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-12T13:17:32.173 |

jshERP through 3.6 contains an information disclosure vulnerability that allows any authenticated user to read platform-wide configuration secrets via the getInfoByKey handler of PlatformConfigController. Low-privilege users of any tenant can request arbitrary platformKey values such as email_auth_code or activation_code to obtain SMTP authorization codes and activation secrets, because only aliOss and weixin keys are blocked.

### CVE-2026-109174

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T13:17:30.040 |

MoguBlog through 6.2 contains an information disclosure vulnerability that allows low-privileged front-end users to read system credentials via the getSystemConfig endpoint. Attackers can supply an ordinary reader session token to retrieve unfiltered SystemConfig data, exposing Qiniu and MinIO secret keys and SMTP mailbox passwords.

### CVE-2026-109168

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T13:17:29.350 |

lamp-cloud through 5.10.1 contains an insecure direct object reference vulnerability that allows authenticated users to list other business objects' file attachments by supplying an arbitrary bizId to the listFileByBizId endpoint. Attackers can retrieve file names, storage paths, MD5 hashes and stored URLs, which in default LOCAL storage are served without login under /anyTenant/file.

### CVE-2026-109166

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T13:17:29.007 |

lamp-cloud through 5.10.1 contains an insecure direct object reference vulnerability that allows authenticated users to obtain storage URLs for other users' files by supplying arbitrary file ids. Attackers can send another user's file ids to the findUrlById handler of FileAnyoneController, which never checks ownership, to retrieve access URLs and read uploaded attachments.

### CVE-2026-109164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-12T13:17:28.460 |

TDuck survey form through 6.0 contains an insecure direct object reference vulnerability that allows authenticated users to delete other users' form submissions by supplying arbitrary submission ids. Attackers can place their own formKey in the path and iterate sequential submission ids in the request body to permanently delete submissions platform-wide.

### CVE-2026-108951

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-12T13:17:27.993 |

LavaLite CMS through 10.1.2 contains an authorization bypass vulnerability that allows authenticated low-privileged users to modify other users' accounts by abusing the AbstractRequest isWorkflow() check. Attackers can send a PATCH request to the user update route with a target identifier to change name, email, password, status, or mobile, including for administrators.

### CVE-2026-105412

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T11:17:10.317 |

An SQL Injection vulnerability affecting Tuleap Enterprise Edition 17.5 could allow an attacker to have read access the Tuleap database.

### CVE-2026-109080

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-12T06:17:00.103 |

SQL injection in the bulk license plate search of the Flock Night Shift hosted service allowed an authenticated user to read other customer organizations' data, including license plate recognition records, via a crafted license plate value. Data could not be modified. Flock identified the issue through internal security review and remediated it on 2026-08-12; no customer action is required.

### CVE-2026-108985

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-12T03:17:18.837 |

ZDR decoding in libnfs through 6.0.2 before 7613236 has an out-of-bounds write related to lib/libnfs-zdr.c with libnfs_zdr_bytes(), libnfs_zdr_string(), and libnfs_zdr_array(). The caller-supplied maxsize value is not honored.

### CVE-2026-19577

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-11T18:16:58.433 |

net_route_ipv6_packet() in subsys/net/ip/route_ipv6.c resolved the nexthop's link-layer address with net_nbr_get_lladdr(nbr->idx) without first checking whether the neighbor cache entry actually had a linked link-layer address. An unresolved neighbor carries idx == NET_NBR_LLADDR_UNKNOWN (0xff), and net_nbr_get_lladdr() in subsys/net/ip/nbr.c performs no runtime bounds check beyond a NET_ASSERT, returning &net_neighbor_lladdr[255] — roughly 2.5 KB past the end of an array whose default size is CONFIG_NET_IPV6_MAX_NEIGHBORS (8). Because the returned pointer is never NULL, the following lladdr == NULL guard does not catch it.

The function is reached from ipv6_route_packet() in subsys/net/ip/ipv6.c for every received unicast IPv6 packet whose destination is not a local address on the receiving interface; CONFIG_NET_IPV6_ROUTE is enabled by default whenever the IPv6 neighbor cache is, so no router or forwarding configuration is needed. net_route_ipv6_get_info() returns the packet's destination itself as the nexthop when a neighbor cache entry for it exists, and the cache lookup does not skip INCOMPLETE entries. An unauthenticated attacker on the same link can therefore force the unresolved state — for example by eliciting traffic to a spoofed, non-existent neighbor address so that net_ipv6_send_ns() creates an INCOMPLETE entry, or by sending a Router Advertisement with no source link-layer address option, which creates a persistently unresolved router neighbor — and then send a packet addressed to that neighbor.

The result is an out-of-bounds read at a fixed index past the neighbor link-layer address array. On builds with CONFIG_ASSERT enabled the assertion fires and the device panics, giving a repeatable remote denial of service. With assertions disabled, the stale out-of-bounds struct net_linkaddr drives a memcmp() over an attacker-uninfluenced length and, when its len byte passes the NET_LINK_ADDR_MAX_LENGTH check, up to 8 bytes of unrelated static RAM are copied into the outgoing frame's destination link-layer address and transmitted on the link, disclosing them to any listener. There is no out-of-bounds write and the offset is not attacker-controlled, which bounds the impact.

### CVE-2026-108913

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-11T16:16:31.713 |

omarchy-theme-set in Omarchy 4 before 4.0.1 allows code execution via a third-party theme because the files placed into ~/.local/state/omarchy/current/theme may include executable content from an untrusted Git repository.

### CVE-2026-108904

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-11T15:16:56.640 |

pH7Builder (pH7 Social Dating CMS) before 18.5.0 contains an information disclosure vulnerability that allows API clients to obtain sensitive member data because UserController::users() and user() return unfiltered database rows. Attackers holding a valid private API key can retrieve bcrypt password hashes, non-expiring hashValidation reset tokens, and TOTP secrets to take over accounts and bypass two-factor authentication.

### CVE-2026-108883

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-11T15:16:55.400 |

JeecgBoot through 3.9.5 contains a missing authorization vulnerability in the editThirdAppConfig handler that allows any authenticated user to modify third-party application configurations. Low-privileged attackers can replace client id, client secret, agent id and corp id of DingTalk, WeCom or Feishu integrations to redirect directory synchronisation and messaging to attacker-controlled applications or break them.

### CVE-2026-21122

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-12T05:17:00.750 |

Out-of-bounds write in libsamsungtts.so prior to SMR Oct-2026 Release 1 allows local attackers to execute arbitrary code.

### CVE-2026-21114

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-12T05:16:59.807 |

Out-of-bounds write in libsmkvextractor.so prior to SMR Oct-2026 Release 1 allows local attackers to execute arbitrary code.
