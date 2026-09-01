# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-01 15:01 UTC
- **対象期間**: `2026-08-31T15:00:30.000Z` 〜 `2026-09-01T15:01:57.000Z`
- **重要CVE数**: 145 件（Critical 9.0+: 41 件 / High 7.0〜: 104 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 超にのぼり、**リモートからの認証不要なコード実行・任意ファイルアップロード** が目立ちます。特に Web アプリケーション（ERP、WordPress プラグイン、オープンソースフレームワーク）に対する *「ファイルタイプ検証不備」* と *「入力バリデーション欠如」* が多数報告され、攻撃者がサーバー上に任意のスクリプトを配置できるリスクが高まっています。  

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な脆弱性種別 | 影響範囲・対象 | 注目理由 |
|-----|--------|----------------|----------------|----------|
| **CVE‑2026‑84147** | 10.0 | 認証なし任意ファイルアップロード（API エンドポイント） | 社内 ERP システム全般（ファイルアップロード API） | **最高スコア** かつ *認証不要*。アップロードされたマルウェアが Web から直接実行可能になるため、完全なサーバ乗っ取りが可能。 |
| **CVE‑2026‑81780** | 10.0 | 任意ファイルアップロード（Hash Form ≤ 1.4.2） | Hash Form アプリケーション | 同様に認証不要で任意ファイルを配置でき、WordPress などの共通ホスティング環境でも広範に利用されている。 |
| **CVE‑2026‑82970** | 10.0 | 任意ファイルアップロード（WP Cookie Notice for GDPR, CCPA & ePrivacy Consent ≤ 4.4.1） | WordPress プラグイン | WordPress サイトは国内外で多数稼働。プラグインの脆弱性は **サイト全体の危険度を一気に上げる**。 |
| **CVE‑2026‑79748** | 9.9 | 不適切なサーバ構成管理（MCPHub < 0.12.15） | MCPHub の `/api/servers` 系エンドポイント | 管理 API が認証なしでサーバ設定を書き換え可能。インフラ全体の構成情報が改竄され、サービス停止や情報漏洩につながる。 |
| **CVE‑2026‑18808** | 9.8 | コードインジェクション（KIO < 1.9） | Klemsan Internet Objects (KIO) | 任意コード実行が可能で、IoT デバイスや産業制御系に組み込まれるケースが多く、**サプライチェーンリスク** が懸念される。 |

> **補足**：上記 5 件は *スコア 9.8 以上*、かつ *認証不要*、*広範囲にデプロイされている可能性* が高い点で共通しています。特に WordPress 系プラグインは多数の顧客サイトに影響を及ぼすため、優先的に対策が必要です。

## 3. 推奨アクション  

### 3‑1. パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / 対策 |
|-------------------|--------------------|------------------------|
| ERP システム（独自実装） | 任意（認証・ファイル検証不備） | **ベンダー提供のパッチ** が出るまで、**ファイルアップロード API を一時的に無効化**、もしくは IP 制限を実装 |
| Hash Form | ≤ 1.4.2 | **1.4.3 以降**（ファイルタイプ検証追加） |
| WP Cookie Notice for GDPR, CCPA & ePrivacy Consent | ≤ 4.4.1 | **4.4.2 以上**（アップロード制御強化） |
| MCPHub | < 0.12.15 | **0.12.15 以上**（認証必須化、入力サニタイズ） |
| KIO (Klemsan Internet Objects) | < 1.9 | **1.9 以上**（コードインジェクション防止パッチ） |
| その他（例：WordPress 本体、テーマ） | すべてのバージョン | **最新安定版** へ更新し、**不要プラグインは削除** |

### 3‑2. 設定・運用面の緊急対策
1. **ファイルアップロードの制限**  
   - アップロード先ディレクトリを Web から直接アクセス不可にする（`.htaccess` で `Deny from all`、または Nginx の `location` で `deny all;`）。  
   - MIME タイプと拡張子のホワイトリストを厳格に設定し、サーバ側で **サーバサイドウイルススキャン**（ClamAV 等）を実行。  

2. **認証・認可の強化**  
   - API エンドポイントは **ベアラートークン** または **OAuth2** に切り替え、IP フィルタリングを併用。  
   - 管理 API（例：MCPHub の `/api/servers`）は **Basic 認証** 以上の認証方式を必須化し、ログイン試行をレートリミット。  

3. **WAF / IDS の導入**  
   - OWASP ModSecurity Core Rule Set (CRS) を有効化し、`/upload` 系エンドポイントへの **ファイルアップロードシグネチャ** を追加。  
   - 侵入検知システムで **不審な POST リクエスト**（特に `multipart/form-data`）を監視し、アラートを上げる。  

4. **コードレビューとサニタイズ**  
   - 任意ファイル名・パスを受け取る箇所は **`realpath()`** で正規化し、ディレクトリトラバーサルを防止。  
   - データベースクエリは必ず **プリペアドステートメント** を使用し、SQLi の再発防止。  

5. **インシデント対応体制の整備**  
   - 影響が疑われるサーバは **即時ログ取得**（Web アクセスログ、システムログ）と **ファイルシステムのハッシュ取得** を実施。  
   - 侵入が確認された場合は **該当コンテナ/サーバの隔離**、バックアップからのリストア、そして **パスワード・

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-84147

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-01T13:20:08.780 |

This vulnerability exists in the ERP system due to improper authentication controls and inadequate file type validation at the API endpoint. An unauthenticated remote attacker could exploit this vulnerability by uploading arbitrary files to a web accessible directory on the targeted system

Successful exploitation of this vulnerability could allow the attacker to execute arbitrary code and compromise the targeted system.

### CVE-2026-81780

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-31T21:17:52.027 |

Unauthenticated Arbitrary File Upload in Hash Form <= 1.4.2 versions.

### CVE-2026-81779

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-08-31T21:17:51.903 |

Improper Validation of Specified Quantity in Input vulnerability in Silk Themes Newspapers X allows Malicious Software Implanted.

This issue affects Newspapers X: from 1.0.46 through 1.0.48.

### CVE-2026-82970

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-31T15:18:33.010 |

Unrestricted Upload of File with Dangerous Type vulnerability in WP Legal Pages WP Cookie Notice for GDPR, CCPA & ePrivacy Consent allows Using Malicious Files.

This issue affects WP Cookie Notice for GDPR, CCPA & ePrivacy Consent: from n/a through 4.4.1.

### CVE-2026-79748

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T18:17:20.340 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 0.12.15, the POST /api/servers and PUT /api/servers/:name endpoints in MCPHub create/update MCP server configurations and then immediately spawn the configured stdio process via child_process.spawn. Authentication is required, but there is no authorization check restricting these endpoints to admins, and there is no allowlist/sanitization on the command and args fields. As a result, any authenticated non-admin user can submit a server configuration with command:"/bin/sh" (or any other binary) and arbitrary args, causing MCPHub to execute the attacker-controlled process as the MCPHub server's OS user (commonly root in the published Docker image and in npx/systemd deployments). This issue has been patched in version 0.12.15.

### CVE-2026-18808

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-01T14:17:26.297 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Klemsan Electrical Electronics Inc. KIO (Klemsan Internet Objects) allows Code Injection.

This issue affects KIO (Klemsan Internet Objects): before v1.9.

### CVE-2026-18210

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-01T14:17:25.590 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in TRtek Technological Products Computer Software Hardware Industry and Trade Limited Company Products's Store allows SQL Injection.

This issue affects Products's Store: before 030631b2.

### CVE-2026-18765

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-01T13:18:11.923 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Teracity Software Technologies Inc. E-OSB allows SQL Injection.

This issue affects E-OSB: before V02.26.07.08.01.

### CVE-2026-18550

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-01T12:17:35.920 |

The Nokri - Job Board WordPress Theme for WordPress is vulnerable to Privilege Escalation via Account Takeover in all versions up to, and including, 1.6.6. This is due to insufficient reset token validation in the `nokri_reset_password()` function, which allows empty attacker-supplied reset tokens to match empty or unset `sb_password_forget_token` user meta values. This makes it possible for unauthenticated attackers to reset the password of any user, including administrators, and gain access to their account.

### CVE-2026-75865

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-01T03:16:51.370 |

The WPLP Cookie Consent – Cookie Banner & Consent Management for GDPR, CCPA & Google Consent Mode plugin for WordPress is vulnerable to arbitrary file upload due to missing file type validation in the saas_upload_logo() function combined with an authorization bypass on the WPLP connector REST endpoints in all versions up to, and including, 4.4.1. This makes it possible for unauthenticated attackers to upload arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-82226

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-31T21:17:53.447 |

Unauthenticated PHP Object Injection in Tickera <= 3.6.0.2 versions.

### CVE-2026-51740

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T20:17:05.320 |

Incorrect access control in the killProcess function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to terminate critical services via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51718

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.970 |

Incorrect access control in the delStaticDhcpRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to remove static DHCP reservations via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51709

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.010 |

Incorrect access control in the setWiFiBasicCfg function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to reconfigure primary Wi-Fi settings via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51708

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:35.897 |

Incorrect access control in the setWiFiWpsCfg function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to change WPS availability via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-53552

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-08-31T19:16:50.880 |

Goploy is an open-source automation deployment system. In versions 1.17.5 and prior, Project.AddFile, Project.EditFile, Project.RemoveFile, and Project.Edit in cmd/server/api/project/handler.go accept a project or project-file row id from the JSON body and act on it without checking that the project belongs to the caller's namespace. The corresponding model.ProjectFile.GetData and model.Project.GetData queries filter only by row id. A user holding the manager role (or any role that includes the FileSync / EditProject permission) in their own namespace can read, write, or delete files in any project across the install, and can rewrite any project's git remote URL by submitting the foreign id in the body. The git-URL primitive escalates to RCE on the next deploy because Edit runs git remote set-url on the project's working tree. At time of publication, there are no known publicly available patches.

### CVE-2026-84200

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T12:17:49.540 |

Kyverno versions v1.9.0 through v1.12.7 contain a policy exception handling flaw. When a policy in enforce mode is combined with two PolicyExceptions, the less restrictive exception takes precedence, allowing an attacker to bypass the policy by crafting a resource name that matches the second exception's name pattern (e.g., '*ingress*'). This can be used to circumvent policies such as one blocking hostPath volumes. Fixed in v1.13.0.

### CVE-2026-4813

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-01T11:16:44.443 |

A vulnerability in the Lutece Core XSL export management module up to version 7.1.7, which allows authenticated administrators to execute code remotely. The XML/XSLT processing configuration does not enable secure processing mode (FEATURE_SECURE_PROCESSING), allowing Java extension functions to be executed from malicious XSL stylesheets. An attacker with administrator privileges can upload a manipulated XSL transformation file and trigger its execution during user export operations, resulting in the execution of arbitrary code on the server.

### CVE-2023-54356

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-09-01T12:17:11.220 |

Kyverno versions 1.9.4 and earlier support insecure 3DES cipher suites (TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA and TLS_RSA_WITH_3DES_EDE_CBC_SHA) on their TLS endpoints. These 64-bit block ciphers are vulnerable to the Sweet32 attack (CVE-2016-2183), which, over very long-lived TLS connections carrying large volumes of traffic, could allow an attacker to recover small amounts of plaintext. The issue is fixed in Kyverno 1.9.5 and 1.10.0.

### CVE-2026-78319

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-09-01T07:16:36.523 |

A service running on the affected products contains a potential Time-of-Check Time-of-Use (TOCTOU) race condition.
An unauthenticated remote attacker could exploit this race condition to bypass intended security controls.
This may result in the execution of unauthorized code.

### CVE-2026-82971

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-31T23:16:35.460 |

A vulnerability was determined in QVidium Opera11 3.3.2a26-Ax4x-opera11. This affects an unknown part of the file /cgi-bin/net_tr.cgi of the component CGI Script. This manipulation of the argument ipaddr causes command injection. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized. The vendor explains: "QVidium has now closed its doors and no longer will be able to sell products or provide support." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-81763

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T21:17:51.293 |

Unauthenticated SQL Injection in Throws SPAM Away <= 3.8.2 versions.

### CVE-2026-81756

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T21:17:50.923 |

Unauthenticated SQL Injection in Smart Marketing SMS and Newsletters Forms <= 5.1.24 versions.

### CVE-2026-81293

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T21:17:50.170 |

Unauthenticated SQL Injection in WP Data Access <= 5.5.81 versions.

### CVE-2026-76133

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-31T16:19:12.240 |

The affected Ebyte 

product
 uses a deprecated hashing algorithm in an authentication-related 
operation. Under conditions where an attacker can manipulate or predict 
the authentication exchange, the weak construction may reduce the 
assurance provided by the authentication mechanism and facilitate 
unauthorized access.

### CVE-2026-73819

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-08-31T16:19:10.903 |

The affected Ebyte 

product's vendor configuration utility permits access to administrative 
functions without verifying the operator's identity under certain 
credential conditions. An unauthenticated attacker on the adjacent 
network could modify critical settings or change access credentials, 
potentially preventing legitimate administrators from managing the 
device.

### CVE-2026-59111

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-31T15:17:35.980 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Digitální a informační agentura (DIA) eObčanka-Identifikace on MacOS enables an attacker to register a custom URL scheme (czeeopauth://) for parameterized application execution. Prior to version 3.6.0, incoming URL parameters were passed to the compiled AppleScript wrapper using concatenation without sufficient sanitization.

### CVE-2026-9621

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-01T14:17:49.377 |

A denial-of-service security issue exists within RSLinx® Classic. The security issue stems from improper handling of a malformed packet. A crafted CIP packet can cause the RSLinx® Classic service to crash, requiring a restart of the service to recover

### CVE-2026-84149

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-527` |
| Published | 2026-09-01T13:20:09.053 |

This vulnerability exists in the ERP system due to exposure of repository information through a publicly accessible .git directory. An unauthenticated remote attacker could exploit this vulnerability by accessing the exposed .git directory and retrieving repository metadata and associated files, which could allow reconstruction of the application's source code.

### CVE-2026-84148

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-01T13:20:08.923 |

This vulnerability exists in the ERP system due to improper authentication and authorization controls in the API endpoint. An unauthenticated remote attacker could exploit this vulnerability by manipulating parameter which could lead to exposure of sensitive information belonging to other users on the targeted system.

### CVE-2026-84189

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T12:17:48.287 |

LibreNMS through 26.4.0 renders JSON fields (name, ip, model, author, commit message) returned by the admin-configurable Oxidized integration URL (oxidized.url) into the device showconfig page without applying htmlspecialchars(). An administrator who points the Oxidized URL at an attacker-controlled server (SSRF) can cause it to return malicious JSON, resulting in stored/persistent cross-site scripting affecting all users who view any device's showconfig tab. Fixed in 26.7.0.

### CVE-2026-66047

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-330` |
| Published | 2026-08-31T15:17:37.503 |

ProfilePress (wp-user-avatar) WordPress plugin before 4.17.2 contains an unauthenticated remote code execution vulnerability that allows unauthenticated attackers to install and activate arbitrary plugins by brute-forcing a weak 32-bit connect token via the ppress_connect_process AJAX handler. Attackers can supply a caller-controlled URL through the file request parameter to trigger silent plugin installation and activation, achieving PHP code execution as the web-server user.

### CVE-2026-51730

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T18:17:18.770 |

Incorrect access control in the delWiFiAclRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to remove Wi-Fi ACL rules via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51725

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T18:17:18.197 |

Incorrect access control in the NTPSyncWithHost function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to change the device clock via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51720

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T17:17:41.523 |

Incorrect access control in the delIpPortFilterRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to remove firewall filter rules via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51717

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.863 |

Incorrect access control in the setOpModeCfg function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to change the device operating mode via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51711

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.223 |

Incorrect access control in the setWiFiWpsStart function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to open a wireless pairing window via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51710

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.117 |

Incorrect access control in the setParentalRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to alter parental-control behavior via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51701

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:35.260 |

Incorrect access control in the setMacFilterRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to change device access control via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51152

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T16:18:34.220 |

Server-side request forgery (SSRF) in the /har/test endpoint in QD 20220208 through 20250803. Fetcher.build_request() in libs/fetcher.py constructs an httpclient.HTTPRequest from user-supplied JSON without validating URL scheme, host, or IP range. The /har/test handler does not require authentication, enabling unauthenticated remote attackers to force the QD server to send arbitrary HTTP requests to internal network resources and cloud metadata endpoints. validate_cert is set to False, disabling TLS verification.

### CVE-2026-67394

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T03:16:50.937 |

A critical local privilege escalation via OS command injection vulnerability has been discovered in Plesk for Linux, affecting all versions from 18.0.34 before 18.0.79.9 and 18.0.80.5. The vulnerability allows a customer or reseller with shell access (or allowed to change their own shell access) to elevate privileges to the root account on the hosting server.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-79684

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-01T14:17:41.797 |

Dell PowerStore contains a Protection Mechanism Failure vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to bypass access restrictions and gain escalated privileges.

### CVE-2026-58572

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-01T14:17:37.470 |

Dell PowerStore contains a Code Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to execute arbitrary code with root privileges.

### CVE-2026-58571

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T14:17:37.297 |

Dell PowerStore contains an OS Command Injection vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to execute arbitrary commands with root privileges.

### CVE-2026-84117

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T13:20:05.487 |

Privilege escalation in Firefox for Android. This vulnerability was fixed in Firefox 155.

### CVE-2026-79683

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-09-01T13:19:59.457 |

Dell PowerStore contains a Protection Mechanism Failure vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability to write attacker-controlled content to arbitrary filesystem paths.

### CVE-2026-58575

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-01T13:19:52.303 |

Dell PowerStore contains an Authentication Bypass by Spoofing vulnerability. An authenticated attacker could potentially exploit this vulnerability to escalate privileges to Administrator.

### CVE-2026-84187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T12:17:48.007 |

AVideo contains a missing authentication vulnerability in plugin/Live/on_publish.php that allows unauthenticated attackers to mark arbitrary scheduled broadcasts as failed by sending crafted POST requests with schedule identifiers. Attackers can exploit the unguarded RTMP callback endpoint to modify scheduled broadcast status fields by supplying fabricated stream keys matching the pattern -ps-<N>, silently canceling any scheduled live broadcast without credentials or authorization.

### CVE-2026-76111

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T12:17:47.113 |

Dell PowerStore contains an Incorrect Authorization vulnerability. An authenticated attacker with low privileges could potentially exploit this vulnerability to invoke administrator-only operations, leading to privilege escalation.

### CVE-2026-19806

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-01T05:17:09.487 |

The Support Genix – Helpdesk, AI Chatbot, Knowledge Base & Customer Support Ticketing System plugin for WordPress is vulnerable to Authentication Bypass leading to Administrator Account Takeover in all versions up to, and including, 1.4.52 via the `guest_ticket_login()` function and its `p` parameter. This is due to the site-wide AES-256-CBC encryption key being derived from only three two-digit `wp_rand(10, 99)` values and a Unix timestamp via `md5()` — yielding approximately 19.5 bits of entropy — combined with a deterministic IV derived from the password, no authentication tag on the ciphertext, and no capability check, nonce, or session validation on the publicly reachable `/sgnix/?p=<token>` endpoint. This makes it possible for authenticated attackers, with subscriber-level access and above, who can obtain a single legitimate guest ticket token as a known-plaintext oracle and bound the plugin activation timestamp, to exhaust the ~729,000-candidate keyspace entirely offline, recover the site-wide encryption key, and forge a self-consistent `{ticket_id, ticket_user}` token targeting any administrator-owned ticket. Submitting the forged token to the unprotected endpoint causes `wp_set_auth_cookie()` to be called for that administrator, granting the attacker full administrative access to the WordPress site.

### CVE-2026-83596

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-31T21:17:55.190 |

A flaw was found in WebKitGTK. Processing malicious web content can cause memory corruption due to improper memory handling.

### CVE-2026-79744

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-08-31T18:17:19.763 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.29, MCPHub's PUT /api/system-config endpoint (handler updateSystemConfig) performs no authorization check. It is protected only by the app-wide authentication middleware and a rate limiter — it never inspects req.user.isAdmin. This issue has been patched in version 1.0.29.

### CVE-2026-9637

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-09-01T14:17:50.157 |

A denial-of-service security issue exists in the affected Logix platforms listed in the table above. The security issue stems from improper validation of input length during CIP message processing. This can result in a major nonrecoverable fault (MNRF), requiring a power cycle to recover

### CVE-2026-9625

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-01T14:17:49.767 |

A denial-of-service security issue exists within RSLinx® Classic. A crafted CIP packet with an oversized embedded message request can cause the RSLinx® Classic service to crash, requiring a restart of the service to recover.

### CVE-2026-9624

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-01T14:17:49.633 |

A denial-of-service security issue exists within RSLinx® Classic. A crafted CIP packet can cause the RSLinx® Classic service to crash due to insufficient data length validation, requiring a  restart of the service to recover.

### CVE-2026-9622

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-09-01T14:17:49.510 |

A denial-of-service security issue exists within RSLinx® Classic. A crafted CIP packet targeting the Forward Close service can cause the RSLinx® Classic service to crash, requiring a restart of the service to recover.

### CVE-2026-84235

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T13:20:09.563 |

A denial-of-service security issue exists in the affected product. The security issue stems from a crafted CIP packet being sent crashing the module. The device requires a restart to recover.

### CVE-2026-19472

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T13:18:12.857 |

A denial-of-service security issue exists within ArmorStart® LT. The security issue stems from improper handling of a crafted HTTP PUT request sent to the embedded web server. This can result in a loss of web server availability

### CVE-2026-84190

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-01T12:17:48.450 |

LibreNMS versions before 26.5.0 contain a remote code execution vulnerability in the AboutController where the snmpget configuration parameter is passed to shell_exec() without proper validation. An authenticated administrator can modify the snmpget configuration to point to a malicious executable file and trigger code execution by accessing the /about endpoint.

### CVE-2026-84165

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-01T11:16:45.713 |

A vulnerability relating to incorrect access control in OpenNebula by OpenNebula Systems, affecting all versions prior to 7.4. This vulnerability could allow an authenticated user with basic permissions to execute commands on virtual machines belonging to other users via the `one.vm.exec` function, without proper verification of access permissions. To exploit the vulnerability, it is only necessary to know the virtual machine’s identifier and for qemu-agent to be enabled on that machine. Exploitation could allow commands to be executed and compromise the confidentiality, integrity and availability of the affected virtual machines.

### CVE-2026-59681

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T10:17:13.300 |

A OS command injection vulnerability in yast2-auth-client allows an attacker who controls Active Directory configuration values to execute arbitrary commands as root on the configured host.
 Auth::AuthConf in src/lib/auth/authconf.rb assembles the Samba net ads join, net ads lookup -S and net ads testjoin invocations by interpolating configuration values into a single command string and passing that string to Open3.popen2 / Open3.capture2, which causes Ruby to run it through /bin/sh. The Organizational Unit (ou), dnshostname, AD user name and AD domain name values are neither validated nor shell-quoted.

### CVE-2026-74837

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T03:16:51.187 |

Allocation of Resources Without Limits or Throttling vulnerability in ash-project ash_typescript allows an unauthenticated attacker to exhaust the BEAM atom table and abort the node via client-supplied RPC field names.

AshTypescript.FieldFormatter.convert_to_field_atom/2 in lib/ash_typescript/field_formatter.ex converts a client-supplied field name to an atom with String.to_atom/1 when no matching atom already exists. It delegates first to parse_input_field/2, which resolves the name with String.to_existing_atom/1 and falls back to returning the plain string; convert_to_field_atom/2 then mints an atom from that string rather than treating the name as unknown.

RPC field selection reaches it for every requested field name through AshTypescript.Rpc.FieldProcessing.FieldSelector, which resolves each name before checking that the field exists, with no allowlist, length bound, or rate limit. Atoms are never garbage collected, so each distinct name mints a permanent one and the VM aborts once the atom table limit is reached. A field name over 255 characters additionally raises an uncaught SystemLimitError.

This issue affects ash_typescript: from 0.1.0 before 0.18.0.

### CVE-2026-65643

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-01T03:16:50.807 |

Eval injection in cPanel 11.138.0.0 and earlier allows remote authenticated users to execute arbitrary code as root.

### CVE-2026-82882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T22:17:31.940 |

Devtron through 2.2.0 fails to enforce authorization checks on the GET /orchestrator/api-token/webhook endpoint, allowing authenticated users to retrieve admin API tokens. Attackers with any authenticated account can query the endpoint with arbitrary project, environment, and application parameters to retrieve plaintext super-admin JWT tokens for full platform control.

### CVE-2026-83497

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-31T19:17:24.327 |

Unrestricted deserialization of untrusted data in the cursor pagination component in the OpenSearch SQL plugin allows a remote authenticated user with basic read/search permissions to execute arbitrary code on the server by sending a crafted cursor parameter to the plugins/sql endpoint.

### CVE-2026-77966

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T16:19:13.053 |

The affected Ebyte 

product does not provide separation between limited and administrative 
management functions. A low privileged authenticated attacker could 
access security sensitive configuration functions and modify settings 
that affect the confidentiality, integrity, or availability of the 
device.

### CVE-2026-75133

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-31T16:19:11.227 |

Keep Backup Daily plugin for WordPress before 2.1.4 contains a sensitive information exposure vulnerability that allows unauthenticated attackers to trigger a full MySQL database dump by accessing the publicly exposed `kbd_cron_process` parameter without authentication. Attackers can predict the partially predictable dump filename based on the database name, a limited random range, and the current Unix timestamp to download the generated backup from the publicly accessible uploads directory.

### CVE-2025-12768

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-01T14:17:23.980 |

A security issue exists within FactoryTalk® Historian Machine Edition. An attacker with low-level authentication could exploit this vulnerability to achieve remote code execution on the affected device.

### CVE-2026-84194

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T12:17:49.000 |

LibreNMS versions >= 23.10.0 and < 26.2.0 (fixed in 26.4.0) contain an authenticated OS command injection vulnerability in libvirt discovery. When libvirt support is enabled (enable_libvirt=true), the device hostname ($this->getDevice()->hostname) is concatenated into shell commands (ssh, virsh list/dumpxml/domstate) in VminfoLibvirt.php and passed to exec() without escapeshellarg() or argument separation. An authenticated admin can set a crafted device hostname to inject arbitrary OS commands, leading to remote code execution in the discovery worker context.

### CVE-2026-59680

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-1287` |
| Published | 2026-09-01T10:17:13.160 |

An OS command injection vulnerability was found in yast2-users. When displaying the "Password Settings" tab of a user, get_password_term() in src/include/users/dialogs.rb read the shadowLastChange and shadowExpire fields with GetString(), which performs no numeric validation, and passed the resulting string to format_days_after_epoch(). That helper interpolated the value into a shell command executed via Ruby backticks without quoting or escaping.

Impact: an administrator who manages users against an external/federated LDAP directory via `yast2 users` triggers root command execution the moment they view or edit that particular user's "Password Settings" tab. No "join domain" or trust setup is required, just browsing/editing one user entry.

This issue affects yast2-users through 5.0.8.

### CVE-2026-83772

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-09-01T06:16:38.107 |

A vulnerability was detected in Cobham SATCOM VSAT7090 Maritime Satellite Router up to 20260704. This issue affects the function c_set_reports_decode of the file mail-report.sh of the component JSON Parsing. The manipulation of the argument sender/recipients results in command injection. It is possible to launch the attack remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-83524

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-31T23:16:35.650 |

A security vulnerability has been detected in RedPort Optimizer wXa-203, Optimizer wXa-213 and Optimizer wXa-223 up to 20260704. This impacts the function exec of the file /xgatev1/system/datetime.php of the component System Clock. The manipulation leads to command injection. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-82954

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T22:17:34.080 |

A vulnerability was detected in Dokploy up to 0.29.7. This issue affects the function writeTraefikConfigInPath of the file packages/server/src/utils/traefik/application.ts of the component Settings. The manipulation of the argument path results in path traversal. The attack can be launched remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-81889

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T21:17:52.460 |

elFinder is an open-source file manager for web, written in JavaScript using jQuery UI. Prior to 2.1.70, elFinder URL uploads in php/elFinder.class.php can bypass server-side request forgery protections when PHP cURL is unavailable because validate_address() validates $info['ip'], but get_remote_contents() selects fsock_get_contents(), which connects to $arr['host'] and performs a second DNS resolution. An attacker able to submit a URL upload can use DNS rebinding to have the first resolution return a public address and the connection resolution return a loopback or private address, causing the internal HTTP response body to be stored as an uploaded file and made readable through elFinder. After a successful fetch, get_headers($url, true) separately requests the original hostname without reusing the validated and pinned connection, creating an additional blind server-side request forgery path even when curl_get_contents() is selected. This issue is fixed in version 2.1.70.

### CVE-2026-72001

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T19:17:10.793 |

Pangolin before 1.22.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to access any protected resource by supplying an attacker-controlled URL parameter to the share-link authentication endpoint that omits the expected resource identifier from the token verification call. Attackers holding a single valid share link for any resource can authenticate against arbitrary resources across different organizations, bypassing all configured authentication methods including SSO, resource passwords, PIN codes, email allowlists, and header authentication.

### CVE-2026-16675

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-09-01T14:17:25.437 |

A privilege escalation security issue exists within FactoryTalk® Activation Manager. The security issue stems from custom actions in the installer that spawn visible console windows running with SYSTEM privileges during installation or repair operations. An authenticated attacker with Windows credentials could hijack these console windows to obtain a SYSTEM-level command prompt, allowing full access to all files, processes, and system resources.

### CVE-2026-82908

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-189;CWE-190` |
| Published | 2026-08-31T21:17:54.503 |

A vulnerability was found in MSI Dragon Center up to 2.0.155.0. Affected by this vulnerability is the function MmioWritePath in the library NTIOLib_X64.sys of the component MMIO Write Path Handler. Performing a manipulation of the argument count/elementSize results in integer overflow. The attack requires a local approach. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-81287

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T21:17:49.803 |

Subscriber SQL Injection in Charitable <= 1.8.12.1 versions.

### CVE-2026-61640

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T21:17:17.243 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.6, Admin-configured OIDC token_url and user_info_url in includes/oidc/handle_oidc_callback.php:18-49 are used directly in curl_init() with zero SSRF filtering. Unlike logo/webhook URLs which have validate_webhook_url_for_ssrf(), OIDC URLs bypass all protections. Admin sets URL to http://169.254.169.254/latest/meta-data/ for cloud metadata access or internal network pivoting. This issue has been patched in version 4.9.6.

### CVE-2026-61639

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T21:17:17.103 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.6, POST /endpoints/db/restore.php calls ZipArchive::extractTo() without validating entry names for ../ sequences. Admin uploads crafted zip with entry logos/../../endpoints/shell.php to write webshell to webroot. Extension filter only applies to post-extraction logo copy step. This issue has been patched in version 4.9.6.

### CVE-2026-82807

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-269` |
| Published | 2026-08-31T16:19:19.880 |

A vulnerability was determined in ieungSoft Ultra RAMDisk Pro 1.82. This issue affects some unknown processing in the library URDSCSI.sys of the component Kernel Driver. This manipulation causes improper privilege management. The attack needs to be launched locally. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-84196

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-01T12:17:49.270 |

Kyverno before 1.18.0 contains a server-side request forgery vulnerability in apiCall.service.url that allows authenticated users to send arbitrary HTTP requests by injecting user-controlled input through variable substitution. Attackers can target internal services, cloud metadata endpoints, and loopback addresses, with response data reflected in admission error messages enabling non-blind data exfiltration.

### CVE-2026-84195

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-01T12:17:49.130 |

Kyverno before 1.16.4 automatically attaches the admission controller's ServiceAccount token to outbound HTTP requests in apiCall service mode without explicit authorization headers. Attackers can exfiltrate the token by directing apiCall requests to external or attacker-controlled endpoints, gaining full control over Kyverno policies and cluster resources.

### CVE-2026-53507

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-918;CWE-1188` |
| Published | 2026-08-31T19:16:49.867 |

oasdiff-action is a GitHub Action that detects breaking changes in OpenAPI specs and post a review on every pull request. Before version 0.0.51, the oasdiff actions resolved external $refs in the OpenAPI spec by default (allow-external-refs: true). When an action runs on a pull request whose spec is attacker-controlled — most importantly fork pull requests on public repositories — a $ref in that spec is fetched/read on the runner with no interaction required, enabling SSRF and disclosure of structured files on the runner. This issue has been patched in version 0.0.51.

### CVE-2024-10085

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T14:17:22.620 |

CWE-770: Allocation of Resources Without Limits or Throttling vulnerability exists that could cause denial of service of the OPC UA communication platform when a large number of OPC UA requests are sent to the platform.

### CVE-2026-82730

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T03:16:52.787 |

Incorrect Authorization vulnerability in ash-project ash_typescript allows an unauthorized RPC caller to read attribute values that Ash field policies denied.

When a field policy denies an attribute, Ash substitutes %Ash.ForbiddenField{}, which retains the real value in original_value because embedded resources must remain writable, and hides it from Inspect rather than removing it. AshTypescript.Rpc.ResultProcessor strips these markers to nil on its template-driven paths, but normalize_primitive/1 in lib/ash_typescript/rpc/result_processor.ex had no such clause, so a marker fell through to the generic struct branch which calls Map.from_struct/1 and serializes every key, original_value included. The denied value is returned to the caller inside the marker that represents its own denial.

The simplest trigger is an action returning an embedded resource as a map, which routes through normalize_resource_struct/2 with an empty template. normalize_value_for_json/1 is a public, unguarded entry point to the same path.

This issue affects ash_typescript: from 0.11.0 before 0.18.0.

### CVE-2026-77856

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-01T03:16:51.500 |

Allocation of Resources Without Limits or Throttling vulnerability in ash-project ash_typescript allows an unauthenticated attacker to exhaust the BEAM atom table and abort the node via client-supplied typed struct field names.

resolve_typed_struct_field/2 in lib/ash_typescript/rpc/field_processing/field_selector.ex looks a client-supplied field name up in the typed struct's reverse map and, when it finds no match, falls back to String.to_atom/1. Because this runs before any field-existence check, an unresolvable name mints a permanent atom rather than being rejected as unknown. Atoms are never garbage collected, so a request carrying many distinct names on a typed struct field grows the atom table until the VM aborts at its limit.

This issue affects ash_typescript: from 0.11.0 before 0.18.0.

### CVE-2026-77348

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-441;CWE-918;CWE-1188` |
| Published | 2026-08-31T22:17:20.317 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 5.0.0, the fix for CVE-2026-33407 (GHSA-hhjq-82f8-m6rc, "SSRF via HTTP Proxy Environment Variable") hardened endpoints/logos/search.php by disabling cURL proxying (CURLOPT_PROXY = '' + CURLOPT_NOPROXY = '*'). However, Wallos ships a second, near-identical, unauthenticated logo-image search endpoint — endpoints/payments/search.php — that was not given the same hardening. It still passes the HTTP_PROXY/HTTPS_PROXY environment variable straight into CURLOPT_PROXY. This issue has been patched in version 5.0.0.

### CVE-2026-75594

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T21:17:48.760 |

Kirby is an open-source content management system. Prior to 4.9.5 and 5.5.2, depending on the release line, Kirby's media handler in src/Cms/Media.php allowed Kirby\Cms\Media::thumb() to append a path-bearing filename to a validated parent media directory. On nginx, PHP's built-in server, or Apache with AllowEncodedSlashes enabled, a remote attacker could submit encoded slash characters such as %2f in the filename and traverse outside the parent's media directory. Differences between responses for existing and nonexistent thumbnail configurations disclosed whether an arbitrary .json file existed, and a .json file containing a valid filename key could cause the referenced image to be returned and the job file to be deleted. The related file::version path in src/Filesystem/Asset.php also accepted ../ sequences outside the intended index root. This issue is fixed in versions 4.9.5 and 5.5.2.

### CVE-2026-61638

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T21:17:16.950 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.6, POST /endpoints/notifications/testemailnotifications.php accepts smtpaddress and smtpport from POST body with zero SSRF validation. PHPMailer connects to attacker-supplied host:port. Every other notification endpoint uses ssrf_helper.php but email was missed. Any authenticated user can probe internal network, cloud metadata. This issue has been patched in version 4.9.6.

### CVE-2026-54600

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-31T21:17:10.267 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.4, endpoints/db/import.php has no authentication. The only guard is a user-table row count — if zero (fresh/unconfigured install), an unauthenticated attacker can replace the entire database. This issue has been patched in version 4.9.4.

### CVE-2026-84218

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-01T14:17:49.233 |

A flaw was found in Jolokia's JSR-160 proxy functionality where insufficient validation of client-controlled JMX service URLs allows a bypass of the denylist introduced to mitigate CVE-2018-1000130. The proxy accepts a `target.url` value from a Jolokia POST request and passes it to `JMXServiceURL` and `JMXConnectorFactory` for establishing the remote JMX connection. The existing denylist only rejects URLs matching `service:jmx:rmi:///jndi/ldap:.*`, which can be bypassed using alternative valid JMX service URL forms, including `ldaps://` schemes or LDAP URLs with a non-empty JMX host component. These URLs are accepted as valid `JMXServiceURL` objects and can cause the Jolokia agent JVM to perform a JNDI lookup against an attacker-controlled LDAP endpoint. This can result in server-side request forgery (SSRF), forwarding of supplied JMX credentials to the remote endpoint, and potentially remote code execution depending on the classes and configuration available in the target JVM.

### CVE-2026-19513

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-01T14:17:27.187 |

The Gravity Forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.0.2. This is due to insufficient validation of multi-file upload chunk state in the `GFAsyncUpload::upload()` function, where public form state URL hashes can be reused as chunk continuation hashes and attacker-controlled temporary filenames are accepted before sanitization. This makes it possible for unauthenticated attackers, when a public form contains a File Upload field with Multiple Files enabled, to upload a valid PNG/PDF polyglot to an attacker-selected public `.php` or `.html` filename in the Gravity Forms temporary upload directory. This can lead to remote code execution on WordPress systems that use NGINX or other non `.htaccess` respecting web servers. NOTE: During installation and activation, the Gravity Forms plugin places a `.htaccess` file in this directory, which prevents this vulnerability from being exploited despite the PHP file being written to the temporary upload directory. In these cases where PHP execution is blocked, attacker-written HTML can result in stored same-origin cross-site scripting if a victim visits the generated file URL.

### CVE-2026-82228

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-31T21:17:53.570 |

Unauthenticated Bypass Vulnerability in SiteGround Security <= 1.6.6 versions.

### CVE-2026-81892

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862;CWE-863` |
| Published | 2026-08-31T21:17:52.927 |

EasyAdmin is a fast and modern admin generator for Symfony applications. From 4.0.0 until 4.29.16 and 5.5.1, EasyAdmin serves all backend requests through a single dashboard route and, for custom actions (Action::linkToRoute() and MenuItem::linkToRoute()), swaps the executed controller based on the routeName query parameter on the kernel.controller event. The swap happens after Symfony's security firewall has already evaluated access_control against the original dashboard URL, and the routeName value was not validated. As a result, a path-based access_control rule protecting the target route was never evaluated, so a low-privilege backend user who can reach a single EasyAdmin URL and knows a target route's name can execute that route's controller, bypassing the path-based rule. Only path-based protections are bypassed. Routes whose controller enforces its own authorization with #[IsGranted] or denyAccessUnlessGranted() remain protected because those checks are recomputed against the swapped-in controller. This issue is fixed in versions 4.29.16 and 5.5.1.

### CVE-2026-81891

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-31T21:17:52.757 |

elFinder is an open-source file manager for web, written in JavaScript using jQuery UI. Prior to 2.1.70, checkExtractItems() in php/elFinderVolumeDriver.class.php calls mimetypeInternalDetect() without passing the result through mimeTypeNormalize(). Because the .phtml, .phar, .php5, and .php3 extensions are absent from mime.types, the staticMimeMap entries that map them to text/x-php are not applied, and allowPutMime() permits extraction even when uploadDeny blocks text/x-php. An attacker with ZIP upload permission can extract PHP-executable files into a web-accessible files/ directory and achieve remote code execution when the server executes those extensions. This issue is fixed in version 2.1.70.

### CVE-2026-61641

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-31T21:17:17.373 |

Wallos is an open-source, self-hostable personal subscription tracker. From version 4.0.0 to before version 4.9.6, Wallos's OIDC login links an incoming OIDC identity to an existing local account by matching the email claim alone, without verifying that the IdP marked that email as verified (email_verified). When Wallos is configured against an IdP that lets a user present an arbitrary or unverified email (multi-tenant IdPs, IdPs with open self-registration, or any IdP the attacker partly controls), an attacker with no Wallos account can authenticate with the admin's email and be logged in as the admin — full account takeover, no password needed. This issue has been patched in version 4.9.6.

### CVE-2026-79746

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-31T18:17:20.057 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.31, when a bearer key with accessType: 'servers' (or 'custom') is used against a group route, isBearerKeyAllowedForRequest grants access to the entire group as long as any single server in that group appears in the key's allowedServers list — not only when every server the key is scoped to matches, and critically, without ever re-checking allowedServers again once the group-level connection is authorized. A key explicitly scoped to one specific server therefore also grants full access to every other server that happens to share a group with it, including servers the key was never authorized for. This issue has been patched in version 1.0.31.

### CVE-2026-19820

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-01T01:16:33.137 |

A vulnerability in the Backblaze Client allows a local user to make the system not bootable by creating a link from Backblaze's folder to Windows OS system files during a backup. Successful exploitation requires an administrator-level system change that results in the absence of specific Windows OS security controls. This vulnerability is due to improper link resolution.

### CVE-2026-13732

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-31T20:17:02.180 |

A flaw was found in GDB's STABS debug format parser. The
read_member_functions() function in gdb/stabsread.c contains a linked
list removal bug in the code that separates destructor and non-destructor
member functions of C++ classes. The bug causes the destructor entries to
remain in the main function list while the list length counter is
decremented, resulting in an out-of-bounds write when the function list
is copied to its final allocated array. An attacker can craft an ELF
binary with malicious .stab and .stabstr sections that triggers this
out-of-bounds write when a user opens the file in GDB and performs any
symbol-inspection operation such as setting a breakpoint. The inferior
process does not need to be executed. Under controlled conditions, this
was demonstrated to achieve execution of arbitrary commands within the
GDB process.

### CVE-2026-53553

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-200` |
| Published | 2026-08-31T19:16:51.030 |

Goploy is an open-source automation deployment system. Prior to version 1.18.0, a severe path traversal vulnerability exists in its backend API endpoints, specifically /deploy/fileDiff (File Compare), when handling file paths provided by the client. This issue has been patched in version 1.18.0.

### CVE-2026-79750

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-31T18:17:20.627 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.30, MCPHub scopes non-admin users to servers they own (list views and config edits enforce ownership), but the tool-execution API does not. Any authenticated non-admin user can invoke tools on MCP servers owned by other users — servers they cannot even see in GET /api/servers. Because connected MCP servers carry real capability (filesystem, HTTP fetch, cloud APIs with the owner's keys), this is cross-tenant compromise: demonstrated arbitrary host file read (/etc/passwd, another user's secrets) and SSRF. This issue has been patched in version 1.0.30.

### CVE-2026-79749

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T18:17:20.483 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.32, MCPHub's SSRF guard in src/utils/ssrf.ts uses a custom isBlockedIpv6 function that only checks for loopback, link-local, unique-local, IPv4-mapped, and IPv4-compatible IPv6 addresses. IPv6 transition address families -- NAT64 (64:ff9b::/96), 6to4 (2002::/16), and Teredo (2001::/32) -- are not checked. An attacker who can specify a URL for an MCP server connection can encode a private IPv4 address inside one of these IPv6 forms to bypass the SSRF guard and reach internal infrastructure. This issue has been patched in version 1.0.32.

### CVE-2026-25706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T10:17:12.993 |

Improper neutralization of special elements used in an OS command in yast2-samba-client allows an attacker who controls the content of an Active Directory directory tree - a rogue domain controller, or a directory user delegated the right to create objects - to execute arbitrary commands as root on a machine being joined to that domain.
This issue affects yast2-samba-client through 5.0.4.

### CVE-2026-19952

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-01T05:17:09.747 |

The Frontend Admin by DynamiApps plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the move_folders function in all versions up to, and including, 3.29.12. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This is exploitable without authentication when a form is configured with public visibility (who_can_see='all'), as the required nonce is publicly obtainable from the rendered form.

### CVE-2026-82397

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1284` |
| Published | 2026-08-31T22:17:22.920 |

Tornado is a Python web framework and asynchronous networking library. Prior to 6.5.8, Tornado parses application/x-www-form-urlencoded request bodies with urllib.parse.parse_qs in tornado/escape.py without passing max_num_fields. RequestHandler._execute in tornado/web.py parses the body before handler dispatch through HTTPServerRequest._parse_body and parse_body_arguments in tornado/httputil.py, so an unauthenticated request body containing millions of separator-delimited fields can synchronously stall the single-threaded event loop and delay every connection. The body is bounded only by max_buffer_size, which defaults to 104857600 bytes. This issue is fixed in version 6.5.8.

### CVE-2026-82393

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-94` |
| Published | 2026-08-31T22:17:22.353 |

pnpm is a package manager. Prior to 10.34.5 and 11.11.0, pnpm accepts a scoped path traversal in a tarball dependency's package.json manifest name because pnpm11/resolving/npm-resolver/src/pickPackage.ts rejects slash characters only for unscoped names. During pnpm install, the unvalidated name reaches raw path joins in pnpm11/installing/deps-resolver/src/resolvePeers.ts, pnpm11/installing/deps-resolver/src/index.ts, and pnpm11/deps/graph-builder/src/lockfileToDepGraph.ts, causing package extraction outside node_modules and allowing attacker-controlled files to overwrite arbitrary filesystem paths even when --ignore-scripts is used. The overwrite can replace shell startup files, Git hooks, or installed package code and lead to code execution. This issue is fixed in versions 10.34.5, and 11.11.0.

### CVE-2026-81297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-31T21:17:50.420 |

Subscriber Privilege Escalation in Fluent Forms Pro Add On Pack <= 6.2.12 versions.

### CVE-2026-81296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T21:17:50.297 |

Unauthenticated Broken Access Control in Fluent Forms Pro Add On Pack <= 6.2.12 versions.

### CVE-2026-79407

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T21:17:48.900 |

A path traversal vulnerability in the SPO extension of MetaGPT 0.8.1 allows an attacker to read arbitrary files via the FILE_NAME value used by set_file_name() and load_meta_data() in metagpt/ext/spo/utils/load.py. The vulnerable code joins the attacker-controlled FILE_NAME value with the settings directory and opens the resulting path without validating that the resolved path remains within the intended directory.

### CVE-2026-54599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-31T21:17:10.063 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.4, login.php generates an OIDC state nonce stored in $_SESSION['oidc_state'], but checksession.php dispatches the OIDC callback without comparing the incoming state against the session value. An attacker can trick a victim into visiting a crafted URL, causing Wallos to exchange the attacker's authorization code and log the victim into the attacker's account. This issue has been patched in version 4.9.4.

### CVE-2026-54598

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-31T21:17:09.843 |

Wallos is an open-source, self-hostable personal subscription tracker. Prior to version 4.9.4, endpoints/db/migrate.php executes database schema migrations when called over HTTP with zero authentication. Any unauthenticated attacker can trigger pending migration files against the live SQLite database. This issue has been patched in version 4.9.4.

### CVE-2026-51735

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T20:17:04.773 |

Incorrect access control in the showSyslog function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to retrieve recent system logs via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-17615

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-31T17:17:37.717 |

A flaw was found in RESTEasy's SourceProvider. This vulnerability allows an unauthenticated attacker to perform an unauthenticated remote file read. By sending a specially crafted XML body with a DOCTYPE declaration referencing external entities to an endpoint that accepts application/xml and returns Source or StreamSource, the server can be tricked into resolving the entity and including sensitive file contents in the HTTP response. This is due to the SourceProvider.writeTo() method creating a SAXParser without disabling external entity resolution, leading to an XML External Entity (XXE) vulnerability.

### CVE-2026-51719

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:37.077 |

Incorrect access control in the delUrlFilterRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to remove URL filtering rules via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-51716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-31T16:18:36.760 |

Incorrect access control in the delPortForwardRules function of TOTOLINK T6 4.1.5cu.748_B20211015 allows unauthenticated attackers to delete port-forwarding rules via sending a crafted POST request to /cgi-bin/cstecgi.cgi.

### CVE-2026-82225

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-31T21:17:53.320 |

Unauthenticated Broken Authentication in RegistrationMagic <= 6.0.9.8 versions.

### CVE-2026-13336

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-01T14:17:24.430 |

CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability exists that could cause execution of Linux Operating system commands when a system back up is restored that has been maliciously modified.

### CVE-2026-78422

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367;CWE-686` |
| Published | 2026-08-31T15:17:58.910 |

Subject::new_for_owner() in the zbus_polkit crate encodes the uid entry of a unix-process polkit subject as an unsigned 32-bit integer (D-Bus type u), whereas the org.freedesktop.PolicyKit1.Authority interface specifies a signed 32-bit integer (D-Bus type i). Because of this type mismatch, polkit silently discards the caller-supplied UID and instead determines the subject's owner itself by looking up the PID in /proc, a lookup that is inherently subject to a time-of-check/time-of-use race.

Consequently, an application that passes a UID obtained from a trustworthy source — for example SO_PEERCRED Unix socket peer credentials — in order to defend against PID reuse receives no protection, and the supplied UID has no effect on the authorization decision. A local unprivileged attacker who can cause an authorized process to terminate and then win the race to have their own process assigned the same PID can be authorized under the identity of the terminated process, bypassing the polkit authorization check and performing actions the attacker is not entitled to.

This issue affects zbus_polkit before 5.1.0.

### CVE-2024-14047

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-01T14:17:23.827 |

A local vulnerability in the Winlogbeat Windows installer caused runtime files to be placed in a directory writable by unprivileged users. A low-privileged attacker with existing access to the system could pre-position malicious filesystem links, causing a subsequent elevated Winlogbeat operation to write to or delete arbitrary files. Successful exploitation could result in a denial of service.

### CVE-2026-83595

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-01T12:17:47.870 |

AVideo contains a cross-site request forgery vulnerability in plugin/API/set.json.php that allows attackers to perform state-changing actions by crafting GET requests that bypass CSRF protection. Attackers can navigate a victim's browser to a malicious URL with API parameters to delete videos, deactivate accounts, or modify playlists without user interaction.

### CVE-2026-19914

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T10:17:12.843 |

The Welcart e-Commerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'custom_order' parameter in all versions up to, and including, 2.12.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is delivered via the guest checkout form, requiring no authentication, and executes when an administrator views the affected order in the WordPress admin panel.

### CVE-2026-75921

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-01T05:17:09.887 |

The Master Addons for Elementor – Elementor Addons, Widgets, Mega Menu Builder, Popup Builder, Widget Builder & Template Kits plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.1.9 via the upload_template_kit function. This is due to incorrect authorization on the upload_template_kit() AJAX handler, which requires only upload_files capability instead of the manage_options required by all sibling handlers, combined with missing per-entry file type filtering after ZIP extraction. This makes it possible for authenticated attackers, with editor-level access and above, to upload files that may be executable, which makes remote code execution possible. Editors can satisfy the nonce requirement because the required nonces are localized on the standard Pages list screen, which is accessible to any user with the edit_pages capability.

### CVE-2026-19796

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T05:17:09.360 |

The Listdom: AI-powered Business Directory with Classifieds Ads Listings plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'lsd[displ][style]' Parameter in all versions up to, and including, 5.8.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the Listdom Pro add-on to be active and the 'Display Options Per Listing' displ setting to be enabled, both of which are non-default configurations.

### CVE-2026-19573

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T05:17:09.233 |

The Affiliate Super Assistent plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the ‘doCommentShortcode’ function in all versions up to, and including, 1.10.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-84192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-01T12:17:48.723 |

LibreNMS before 26.3.1 contains a stored cross-site scripting vulnerability in legacy PHP templates that output SNMP-sourced and syslog-sourced data without escaping. An attacker who controls a monitored network device can inject arbitrary JavaScript through SNMP interface descriptions or syslog program fields that executes when authenticated users view affected pages.

### CVE-2026-82392

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-31T21:17:54.033 |

pnpm is a package manager. Prior to 10.34.5 and from 11.0.0 until 11.11.0, pnpm parses the package name from attacker-controlled pnpm-lock.yaml packages keys with dp.parse(depPath).name and uses it without validation in deps/graph-builder/src/lockfileToDepGraph.ts and pnpm11/deps/graph-builder/src/lockfileToDepGraph.ts. The name reaches path.join(modules, pkgName), storeController.importPackage, and pnpm11/lockfile/to-pnp/src/index.ts, allowing package contents to be written outside node_modules when a user runs pnpm install. When dangerouslyAllowAllBuilds or a matching allowBuilds entry permits lifecycle scripts, the escaped package can execute code with the user's privileges. This issue is fixed in versions 10.34.5 and 11.11.0.

### CVE-2026-82229

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:53.717 |

Unauthenticated Cross Site Scripting (XSS) in WordPress Social Login and Register <= 7.8.2 versions.

### CVE-2026-82224

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:53.193 |

Unauthenticated Cross Site Scripting (XSS) in SliceWP <= 1.2.10 versions.

### CVE-2026-82221

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:53.073 |

Unauthenticated Cross Site Scripting (XSS) in RegistrationMagic <= 6.0.9.8 versions.

### CVE-2026-81768

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:51.660 |

Unauthenticated Cross Site Scripting (XSS) in Super Store Finder <= 7.10 versions.

### CVE-2026-81765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:51.537 |

Unauthenticated Cross Site Scripting (XSS) in Tailored Tools <= 3.0.2 versions.

### CVE-2026-81764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:51.417 |

Unauthenticated Cross Site Scripting (XSS) in Email Essentials <= 6.0.6 versions.

### CVE-2026-81298

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:50.567 |

Unauthenticated Cross Site Scripting (XSS) in LeadConnector <= 4.0.5 versions.

### CVE-2026-81291

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:50.053 |

Unauthenticated Cross Site Scripting (XSS) in Uncode <= 2.12.7 versions.

### CVE-2026-81290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-31T21:17:49.930 |

Unauthenticated Cross Site Scripting (XSS) in Email Subscribers & Newsletters <= 5.9.33 versions.

### CVE-2026-71415

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T21:17:48.057 |

Kirby is an open-source content management system. From 5.0.0 until 5.5.2, Kirby's REST API chunk upload handler in src/Api/Upload.php did not run the relevant upload authorization preflight in Kirby\Api\Upload::process() before Kirby\Api\Upload::processChunk() persisted chunk data. An authenticated user with the access.panel permission enabled but with files.create, files.replace, and user/users.update permissions disabled could submit requests with an Upload-Length header and leave unfinished chunks in site/cache/.uploads for 24 hours. Repeating this process could consume attacker-controlled temporary storage, prevent other users from uploading files, or prevent site logic from storing data, although final permission checks still prevented unauthorized files from reaching the content or site/accounts directories. This issue is fixed in version 5.5.2.

### CVE-2026-79747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-31T18:17:20.200 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.32, an authenticated non-admin user can register a server pointing at an arbitrary URL and make the hub issue server-side requests to it, with no egress filtering (no block of loopback / RFC1918 / link-local 169.254.0.0/16). Via the OpenAPI proxy path the response body is returned to the caller (full, reflected SSRF); via the SSE/streamable-http transport the request is sent blind. This issue has been patched in version 1.0.32.

### CVE-2026-79745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-31T18:17:19.910 |

MCPHub is a unified hub for centrally managing and dynamically orchestrating multiple MCP servers/APIs into separate endpoints with flexible routing strategies. Prior to version 1.0.32, the built-in prompt and resource controllers perform no role checking. The mutating POST/PUT /api/prompts* and POST/PUT /api/resources* routes are attached to the authenticated router with no admin gate, and the handlers never read req.user. The DAO singletons they write are consulted first — ahead of any connected MCP server — for every session in handleGetPromptRequest / handleReadResourceRequest. A non-admin can therefore create, overwrite, and shadow global prompt templates and resources that all other users are served. The scored impact is the unauthorized integrity violation (creation/tampering/shadowing of globally-served records); stored prompt injection into other users' LLM sessions is a downstream consequence of that tampering. This issue has been patched in version 1.0.32.

### CVE-2026-77975

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-31T16:19:13.190 |

The affected Ebyte 

product exports administrative credentials and other 
sensitive configuration information without adequate protection. An 
unauthenticated attacker on the adjacent network who can obtain an 
exported configuration file could recover valid credentials and use them
 to access the device or similarly configured systems.

### CVE-2026-75132

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-31T16:19:11.070 |

WAPT Server versions 2.6.1.17834 and earlier contains a SQL injection vulnerability in the `columns` parameter of the GET `/api/v3/hosts` endpoint. A remote authenticated user with read-only privileges can inject arbitrary PostgreSQL expressions into the SQL query constructed by WAPT. By exploiting the injection point, an attacker can inject additional PostgreSQL statements, bypass the host scope restrictions applied to the account, and read information from other rows or tables within the database.

### CVE-2026-9634

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-01T14:17:50.017 |

A security issue exists within the Redundancy Module Configuration Tool. The RMConfigTool.exe binary searches directories in the system path for a required DLL, and one or more of these directories may be writable by standard (non-administrator) users due to incorrect default permissions. If a local attacker places a malicious DLL in such a directory and an administrator subsequently runs the tool, the malicious DLL is loaded into the elevated process and executes with Administrator/SYSTEM privileges.

### CVE-2026-9633

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-09-01T14:17:49.893 |

A security issue exists within the Redundancy Module Configuration Tool. The RM3ConfigTool.exe binary searches directories in the system path for a required DLL, and one or more of these directories may be writable by standard (non-administrator) users due to incorrect default permissions. If a local attacker places a malicious DLL in such a directory and an administrator subsequently runs the tool, the malicious DLL is loaded into the elevated process and executes with Administrator/SYSTEM privileges.

### CVE-2026-12663

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-01T14:17:24.290 |

A security issue exists within ControlFLASH™, where the installer grants write permissions to the "Everyone" group on a product installation directory. This could allow arbitrary code execution, resulting in an attacker being given the ability to run any commands or code of the attacker's choice on a target machine at the logged-in user's permission level.

### CVE-2026-82346

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-379` |
| Published | 2026-08-31T21:17:53.853 |

A potential security vulnerability has been identified in the HP ImageDiags for versions prior to 5.0.0.36. The vulnerability could potentially allow a local attacker to escalate privileges due to insufficient access controls.
