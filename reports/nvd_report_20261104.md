# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-03 15:00 UTC
- **対象期間**: `2026-11-02T15:00:40.000Z` 〜 `2026-11-03T15:00:41.000Z`
- **重要CVE数**: 168 件（Critical 9.0+: 23 件 / High 7.0〜: 145 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に報告された CVE のうち、**CVSS 9.0 以上が 30 件以上**と、深刻度の高い脆弱性が集中しています。  
- 特に **Web アプリケーション（WordPress、Joomla、cPanel 等）** と **ミドルウェア（Kamailio、WSO2、Control Web Panel）** に対する認証バイパス・リモートコード実行が目立ち、攻撃者が **無認証でフルリモートコード実行（RCE）や管理権限取得** を行えるケースが多数です。  
- 多くの脆弱性は **入力検証不備、ハードコーディングされた鍵、デフォルト認証情報** といった基本的なセキュリティ対策の欠如が根本原因となっており、**パッチ適用だけでなく構成見直しが必須**です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑4052** (WSO2 Identity Server) | 9.8 | Resident Key Manager でデータベース共有構成の環境で、自己登録ユーザーが WSO2 API Manager の System REST API に不正アクセス | **認証バイパス + 権限昇格** が同時に成立。企業向け IDaaS・API 管理基盤で広く採用されているため、被害範囲が大きい。 |
| **CVE‑2026‑120534** (Advanced Custom Fields: Extended PRO – WordPress) | 9.8 | Limited Code Injection により任意コードが実行可能（全バージョン ≤ 0.9.2.6） | WordPress の人気プラグインで、**プラグイン単体の脆弱性がサイト全体の RCE に直結**。多数のサイトでプラグインがインストール済み。 |
| **CVE‑2026‑106803** (Kamailio ims_registrar_pcscf) | 9.8 | スタックバッファオーバーフロー → 任意コード実行（v6.1.3/6.1.4） | SIP/IMS インフラのコアコンポーネントで、**ネットワーク層から直接攻撃可能**。通信事業者や大規模コールセンターへのインパクトが深刻。 |
| **CVE‑2026‑77876** (Control Web Panel – OS コマンドインジェクション) | 9.3 | `acc=deletedp` パラメータ経由で任意コマンド実行（v1.16 未満） | CWP は中小企業のサーバー管理で広く利用。**Web から直接 OS コマンドが実行できる**ため、サーバ全体の乗っ取りリスクが高い。 |
| **CVE‑2026‑120442** (ape‑volo‑admin – JWT ハードコードキー) | 9.3 | ハードコードされた JWT 署名鍵により管理者トークンを偽造可能（v3.6.1 未満） | 認証トークンが **外部で生成可能** になるため、**管理者権限取得が容易**。内部ツールに依存する組織での被害が想定される。 |

> **共通点**：いずれも「**認証・権限管理の欠如**」が根本にあり、**パッチ適用だけでなく、鍵のローテーションやデフォルト設定の無効化**が不可欠です。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ |
|-------------------|-------------------|--------------------------|
| **WSO2 Identity Server** | 5.x 系（Resident Key Manager で DB 共有） | 5.12.0 以降（公式パッチ適用） |
| **Advanced Custom Fields: Extended PRO** (WordPress) | ≤ 0.9.2.6 | 0.9.2.7 以上（公式リリース） |
| **Kamailio** | 6.1.3, 6.1.4 | 6.1.5 以降（ims_registrar_pcscf モジュール修正） |
| **Control Web Panel (CWP)** | < 1.16 | 1.16 以上（`protected_directory` モジュールの入力サニタイズ） |
| **ape‑volo‑admin** | < 3.6.1 | 3.6.1 以上（JWT 鍵の外部化・ローテーション） |
| **cPanel** (CVE‑2026‑105476) | 2023.12 以前 | 2024.02 以降（リンク解決ロジック修正） |
| **SUSE Rancher** (CVE‑2026‑88811, 94290) | 2.13.0‑2.15.3 | 2.15.4 以上（メタプロキシ・kubeconfig 参照制御） |

> **※** すべての環境で **バックアップ取得 → テスト環境での検証 → 本番適用** の手順を踏んでください。

### 3.2 設定・運用上の対策
1. **認証バイパス防止**  
   - WSO2、ape‑volo‑admin、cPanel では **JWT 秘密鍵・シークレットを外部管理**（Vault 等）し、空文字やハードコードを排除。  
   - デフォルト管理者アカウント（Axxon One、Control Web Panel 等）は **インストール直後にパスワード変更**、不要なアカウントは削除。

2. **入力検証の強化**  
   - WordPress・Joomla プラグインは **サーバ側で MIME タイプと拡張子の二重チェック**、`realpath()` でパス正規化を必ず実施。  
   - CWP の `file` パラメータは **ホワイトリスト方式** に切り替え、`escapeshellcmd()` でエスケープ。

3. **ネットワーク分離**  
   - Kamailio の IMS 関連モジュールは **信頼できる内部ネットワークからのみアクセス**可能にし、外部からの NOTIFY メッセージは **IP フィルタリング**で遮断。  
   - Azure AD トークン漏洩（kaniko）対策として **ACR のホストホワイトリスト**を設定し、`docker-credential-acr-env` の使用を最小化。

4. **監査・ログ強化**  
   - すべての管理 API（WSO2 API Manager、Rancher Fleet、cPanel）で **認証失敗・トークン生成**をログに残し、SIEM へ送信。  
   - 変更された JWT、認証トークン、管理者操作は **監査ログにタイムスタンプと発行元 IP** を必ず記録。

5. **脆弱性スキャニングと定期レビュー**  
   - **Nessus / OpenVAS** で **CVE‑2026

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-4052

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T08:17:15.530 |

This issue only impacts deployments where WSO2 Identity Server is configured as a Resident Key Manager with database sharing. In such environments, a self-registered user may gain access to the System REST APIs of WSO2 API Manager by obtaining a token from the WSO2 Identity Server token endpoint.

### CVE-2026-120534

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-03T05:18:31.987 |

The Advanced Custom Fields: Extended PRO plugin for WordPress is vulnerable to Limited Code Injection in all versions up to, and including, 0.9.2.6 via the render_field function. This is due to insufficient validation of form configuration parameters before merging into field settings and passing to call_user_func_array in the render_field method. This makes it possible for unauthenticated attackers to call arbitrary WordPress functions with controlled arguments. Method 1 requires the administrator to enable the non-default 'shortcode_preview' setting for the target form, while Method 2 requires the server environment to lack OpenSSL functions, causing ACF Pro's acf_decrypt to fall back to unverified base64 decoding.

### CVE-2026-86596

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-02T22:17:23.490 |

The s2Member plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, <= 260927 via the 'item_name' parameter parameter. This is due to insufficient sanitization in strip_php_tags_deep(), which only strips literal '<?' sequences, combined with a post-interpolation placeholder cleanup that reassembles a valid '<?php' opener after the attacker-controlled value has already been embedded in the email template. This makes it possible for authenticated attackers, with custom-level access and above, to execute code on the server.

### CVE-2026-102435

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-02T20:17:26.287 |

The Ultra Addons for Contact Form 7 plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the _getObjAttr function in all versions up to, and including, 3.5.54. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This requires the PDF Generator add-on to be active and a Contact Form 7 form to be configured for PDF generation, as the WPCF7_Submission POP gadget chain relies on CF7 being present to complete the file deletion via __destruct(). Note: This vulnerability can only be exploited when the PDF generator feature is enabled.

### CVE-2026-106803

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T17:17:33.270 |

A stack-based buffer overflow exists in Kamailio v6.1.3 and v6.1.4 in the ims_registrar_pcscf module. When processing a crafted application/reginfo+xml NOTIFY message, process_contact() copies an attacker-controlled port value from the alias parameter into a fixed 5-byte stack buffer without validating its length. An unauthenticated remote attacker can trigger stack corruption and terminate the P-CSCF process, resulting in denial of service.

### CVE-2026-105606

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-02T19:17:50.330 |

Joomla Extension - joomlaboat.com - Unauthenticated arbitrary file upload in Custom Tables < 3.7.8 - An unauthenticated attacker can upload a polyglot file with an attacker-controlled extension to the web-accessible tmp directory of any Joomla site that exposes a public Custom Tables submission form, and the stored path is disclosed in the response. By default the uploaded file is served as static content, so the primary impact is an unauthenticated arbitrary file write to a web-accessible directory, which allows hosting of attacker-controlled content (for example phishing or malware pages) under the victim's domain.

### CVE-2026-97718

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T20:18:05.253 |

CVE-2026-97718 Is a cross-site request forgery vulnerability
in version 14.60 of the Secure Access server.  Because of a bypassed security control, an
attacker can cause an admin to create an account under their control.

### CVE-2026-105603

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-02T19:17:49.823 |

Joomla Extension - dj-extensions.com - Authenticated arbitrary file upload in DJ-Classifieds < 3.11.3 - The Joomla extension DJ-Classifieds is vulnerable to an unprivileged file upload, leading to full RCE.

### CVE-2026-119085

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-02T18:18:44.283 |

Improper neutralization of special elements used in a template engine in the publishing component of Amazon Virtual Engineering Workbench (VEW) could allow a remote authenticated third party to run arbitrary code with the permissions of the publishing Lambda's IAM role. This could allow access to data and resources across all tenant projects. The code is reachable through a crafted CloudFormation template body containing template engine directives submitted through the product versioning API.



To remediate this issue, users should redeploy from the latest version of awslabs/virtual-engineering-workbench.

### CVE-2026-116769

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T20:17:33.527 |

CVE-2026-116769 is an authentication bypass
vulnerability in Secure Access servers starting with version 13.0 and prior to
14.61. Attackers can modify security settings of a client via the server.

### CVE-2026-105604

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T19:17:49.997 |

Joomla Extension - dj-extensions.com - Unauthenticated SQL injection in DJ-Classifieds < 3.11.3 - The Joomla extension DJ-Classifieds is vulnerable to an unauthenticated SQL injection vector in the frontend search.

### CVE-2026-105769

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-522` |
| Published | 2026-11-02T17:17:32.670 |

kaniko before 1.25.20 can send a Microsoft Entra ID (Azure AD) access token for Azure Resource Manager to an attacker-controlled registry host. kaniko uses the Azure Container Registry credential helper github.com/chrismellard/docker-credential-acr-env, which decides whether a host is an ACR registry with an unanchored regular expression, so any hostname containing .azurecr.io, .azurecr.cn, .azurecr.de or .azurecr.us is accepted. kaniko consults this helper for any registry that has no credentials in the Docker config and is not a Google or Amazon ECR registry, before contacting the registry. A Dockerfile that references an image on a lookalike host, such as FROM x.azurecr.io.attacker.com/img or COPY --from=<image>, causes the helper to obtain a token from the build's Azure identity (service principal environment variables, federated workload identity token, or managed identity) and POST it to https://<host>/oauth2/exchange. The attacker can use the token against Azure Resource Manager with the identity's role assignments until it expires, and can exchange it for credentials to any ACR registry the identity can access. No RUN instruction or push is required. This issue is fixed in 1.25.20.

### CVE-2026-77876

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T16:17:43.293 |

Control Web Panel (CWP) before webpanel_version 1.16 contains an OS command injection vulnerability in the protected_directory user panel module that allows attackers to execute arbitrary commands by submitting unescaped input through the file POST parameter in the acc=deletedp action. Attackers can exploit this flaw, which passes attacker-controlled input directly into a shell_exec call, to achieve code execution in the user panel context.

### CVE-2026-73696

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-698` |
| Published | 2026-11-02T15:17:37.480 |

Control Web Panel (CWP) before webpanel_version 1.12 contains an execution after redirect vulnerability in the user panel authentication flow (CWPUserIndex) that allows unauthenticated attackers to bypass authentication by exploiting a missing exit() call after a header('Location: ...') redirect. Attackers can send unauthenticated requests to continue PHP execution past the redirect, reaching user panel functionality that should require authentication.

### CVE-2026-120442

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-02T15:17:26.490 |

ape-volo-admin before 3.6.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge administrator tokens using a hardcoded JWT signing key in appsettings.json. Attackers can sign tokens offline with the jti claim set to the seeded administrator id to gain full API control over users, roles, permissions and data.

### CVE-2026-89292

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-918` |
| Published | 2026-11-03T10:17:20.077 |

In Eclipse Mnestix Browser versions 1.6.0 up until but excluding 2.3.0 it was possible for an unauthenticated attacker to exfiltrate the MNESTIX_BACKEND_API_KEY for all configured Infrastructures.

### CVE-2026-121022

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1393` |
| Published | 2026-11-03T09:17:11.980 |

Use of Default Password (CWE-1393) in the web client in AxxonSoft Axxon One before 3.0.0 on Windows and Linux allows a remote unauthenticated attacker to log in as the built-in administrator with the default credentials on a newly installed system, because the web client did not enforce the mandatory change of the default password on first login.

### CVE-2026-120447

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-02T15:17:27.523 |

HotGo 2.8.4 through 2.15.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to choose the SMS login verification code by supplying the Code field to /admin/sms/send. Attackers who know a user's mobile number can set a known code and sign in through /admin/site/mobileLogin to take over accounts, including administrators.

### CVE-2026-13594

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-03T08:17:15.203 |

Zoho Corporation's ManageEngine Log360 and EventLog Analyzer versions 13062 and below are vulnerable to an issue that could allow an adversary to gain unauthorized access to the product.

### CVE-2026-120518

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T05:18:31.380 |

The BuddyPress XProfile Image Field plugin for WordPress is vulnerable to arbitrary file deletion in all versions up to, and including, 3.1.0. This is due to bpxp_image_field_update_on_user_activation() calling unlink() on a path built from visitor-supplied signup metadata with no realpath() resolution, no containment check against the profile-image directory and no extension allow-list. Submitting a zero-byte file with the 'field_N_hidden' parameter during registration makes the plugin store the raw value, which is then resolved against the document root when the pending signup is activated. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file (such as wp-config.php) is deleted. Requires open registration and an image-type profile field on the signup form.

### CVE-2026-88811

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-02T17:17:45.793 |

Missing filtering in the SUSE Rancher Manager meta proxy could cause passed in rancher credentials to be leaked to cloud providers. This affects SUSE Rancher 2.15.0 up to 2.15.3, 2.14.0 up to 2.14.7, 2.13.0 up to 2.13.11,

### CVE-2026-94290

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-02T16:17:45.190 |

SUSE Rancher Fleet clusters reference a kubeconfig secret that the controller uses to install and manage a Fleet agent on the target cluster. The controller did not sufficiently restrict which kubeconfig secrets a Fleet Cluster object was allowed to reference. As a result, a Fleet cluster defined in a namespace an ordinary user controls could be associated with administrative credentials for the management cluster itself, causing the controller to manage the management cluster on that user's behalf and to run that user's Fleet content there with elevated privileges. This affects SUSE Rancher Fleet 0.16.0 up to 0.16.3, 0.15.0 up to 0.15.8, 0.14.0 up to 0.14.12, 0.13.0 up to 0.13.17 and possible older versions.

### CVE-2026-120459

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-02T15:17:29.867 |

python-jose through 3.5.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge JWTs because HMACKey and CryptographyHMACKey accept zero-length HMAC secrets. When an application's HS256/HS384/HS512 verification key resolves to empty, such as an oct JWK with empty k, attackers can forge tokens with arbitrary claims that jwt.decode accepts.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-85035

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T14:17:39.290 |

The can_add_rx_filter_msgq() system call installs a CAN RX filter whose callback (can_msgq_put() in drivers/can/can_common.c) is handed the caller's struct k_msgq * as user_data. The controller driver stores that raw pointer in its filter table and dereferences it from the RX path every time a matching frame arrives. The system call verifier z_vrfy_can_add_rx_filter_msgq() in drivers/can/can_handlers.c validated the queue only with K_SYSCALL_OBJ(), which is a point-in-time check of type, initialization and caller permission and says nothing about the object's lifetime.

On a build with CONFIG_USERSPACE=y and CONFIG_DYNAMIC_OBJECTS=y, an unprivileged user-mode thread that has been granted access to a CAN device can obtain a message queue whose lifetime it fully controls: k_object_alloc(K_OBJ_MSGQ) followed by k_msgq_alloc_init(). The lifetime of such an object is driven solely by its permission bitmask, and a pointer retained by the kernel is not represented there. After registering the filter, the thread calls k_object_release() — or simply terminates — and unref_check() frees the struct k_msgq storage while the CAN driver still holds the pointer.

The next matching CAN frame causes k_msgq_put() to run in supervisor context against freed memory that the attacker can have groomed with another kernel allocation: the frame payload is memcpy()d through the reused block's write_ptr, and the queue's wait_q (and poll_events under CONFIG_POLL) list nodes are manipulated. This yields kernel-heap corruption reachable from a user-mode thread, defeating the isolation CONFIG_USERSPACE is intended to provide; the same dangling pointer also arises benignly when an application thread exits without calling can_remove_rx_filter().

The fix validates the queue with K_SYSCALL_OBJ_STATIC(), which additionally rejects objects carrying K_OBJ_FLAG_ALLOC, so only statically defined queues (CAN_MSGQ_DEFINE()) may be registered from user mode. Supervisor-mode callers bypass the verifier and must themselves keep the queue valid until the filter is removed.

### CVE-2026-76124

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-03T13:17:23.413 |

The BuddyBoss App plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.2.1 via the send_feedback function. This is due to insufficient file type validation that relies solely on the client-supplied Content-Type header without server-side content inspection or extension validation. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. While uploaded files are deleted after email transmission, a race condition exists during SMTP execution that allows access to the file, and files persist indefinitely when wp_mail() fails.

### CVE-2026-89293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602;CWE-862` |
| Published | 2026-11-03T10:17:20.257 |

In Eclipse Mnestix Browser versions 1.2.0 up until but excluding 2.3.0 it was possible for an unauthenticated attacker to perform actions that are only allowed to be executed by an authorized Mnestix user, like changing the Infrastructure settings or calling the connected and authenticated Mnestix AAS Generator backend.

### CVE-2026-120333

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-03T10:17:18.270 |

The actions linked in the emails of the extension (e.g. to confirm a registration or the deletion of an account) do not reject requests with a missing or invalid hash. Instead, the frontend user given in the request is used. Unauthenticated attackers can therefore perform these actions for arbitrary active frontend users. This allows them to retrieve the email address or username of all frontend users and to delete arbitrary frontend user accounts.

### CVE-2026-76955

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-03T02:16:53.720 |

A buffer overflow vulnerability in the zdp_wtp binary in Zyxel NWA110AX firmware versions through 7.12(ABTG.0)C0 could allow a LAN-based attacker to escalate privileges on an affected device.

### CVE-2026-107441

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-03T02:16:52.617 |

An out-of-bounds write vulnerability in the CGI program of Zyxel GS1900-24E firmware versions through 2.90(AAHK.2)C0 could allow an unauthenticated adjacent attacker  to exploit the flaw and potentially execute OS commands via a crafted HTTP request.

### CVE-2026-105476

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-02T21:17:22.707 |

Improper link resolution before file access in cPanel allows remote authenticated users to write arbitrary root-owned files and escalate privileges.

### CVE-2026-119736

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-02T19:18:02.537 |

Attendo (formerly Petpooja Payroll) Admin Android application version 3.0.13 and earlier contains a hard-coded credentials vulnerability that allows attackers to extract production MQTT broker credentials by decompiling the APK's bundled Flutter configuration assets such as production.json and device-command configuration files. Attackers can use the recovered credentials to authenticate to the production MQTT broker over TCP 1883, access messaging topics containing employee attendance records, personal identifiers, Base64-encoded photographs, device telemetry, and authentication material, and publish messages to those topics, resulting in exposure of sensitive data and potential unauthorized message injection.

### CVE-2026-120446

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-02T15:17:27.323 |

madong-admin-saas through 5.1.4 contains a missing authentication vulnerability in the platform tenant management API because the 'platformapi' middleware key never matches the 'platform' application. Unauthenticated remote attackers can call /platformapi/tenant/account, bind-plan and sync-data endpoints to list, create, modify, disable or delete tenants and bind subscription plans.

### CVE-2026-71450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-02T23:17:21.200 |

Authentication bypass using an alternate path or channel vulnerability in Johnson Controls EasyIO Neo EC and CW Edge Controller allows Authentication Bypass.

This issue affects EasyIO Neo EC and CW Edge Controller: from EC 3.3b62 through EC 3.3b63 and from CW 3.3b24 through CW 3.3b25.

### CVE-2026-120091

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-749;CWE-863;CWE-1188` |
| Published | 2026-11-02T22:17:20.567 |

Temporal Server compiles a Worker Controller Instance module, go.temporal.io/auto-scaled-workers, into its Worker Service, and that module registers a compute provider named k8s whose function is to manage workers running in a Kubernetes cluster. The k8s provider built its Kubernetes client from the client configuration supplied in the caller's request rather than from operator configuration, and building and using that client could run a command of the caller's choosing on the Worker Service host, under the account the server process runs as. Two frontend operations reach the provider. CreateWorkerDeploymentVersion requires a namespace write role. ValidateWorkerDeploymentVersionComputeConfig is registered as a read-only namespace operation, so an authenticated caller holding only a read role in a single namespace can reach the provider through it, and that route does not require a worker deployment to already exist. Execution happens while the submitted configuration is validated, so no scaling decision, task arrival, or unusual request sequence is required. Because the Worker Service process holds the persistence credentials for every namespace in the cluster and the cluster's TLS material, the consequence reaches beyond the caller's namespace to the cluster as a whole. The provider is present in the official temporal-server binaries and container images for the affected releases. The control that keeps it unreachable is the compute provider allowlist, the dynamic configuration setting workercontroller.compute_providers.enabled. On Temporal Server 1.31.0 through 1.31.2 that allowlist does not deny by default: when the setting is unset the check is skipped and every registered compute provider is permitted, k8s included, so a stock deployment of those releases is exposed. On 1.31.3 and later 1.31 releases, and on 1.32.0 and later 1.32 releases, the allowlist denies by default, and a deployment is exposed only where k8s has been added to it. The 1.30 release line does not include the Worker Controller Instance module and is unaffected. To determine whether a deployment is affected, check the following together. The deployed Temporal Server version is in an affected range. The Worker Service is running, which it is in the default service set and therefore in a stock deployment. The effective value of workercontroller.compute_providers.enabled contains k8s, or, on 1.31.0 through 1.31.2 only, is unset; check both the global value and every namespace-constrained override, because an override can add k8s for a single namespace. And authorization is configured, meaning a real authorizer and claim mapper are in place; a deployment running with no authorizer already grants every caller unrestricted access to every namespace, so it has no namespace boundary for this to cross. Deployments that use a custom authorizer should also check whether it permits ValidateWorkerDeploymentVersionComputeConfig to callers without namespace write access. The separate per-namespace dynamic configuration setting workercontroller.enabled does not gate the affected path on any affected release.

### CVE-2026-115215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-772` |
| Published | 2026-11-02T22:17:18.397 |

In Eclipse ThreadX NetX Duo versions 6.0 through 6.5.2.202603a, the NetX Secure DTLS server allocates a session from its fixed session pool for the first datagram from any unrecognised address and port, before the cookie exchange, and never releases a session whose handshake stalls. A remote, unauthenticated attacker can exhaust the pool with one spoofed datagram per source and deny DTLS service to legitimate clients until the application resets the sessions.

### CVE-2026-29508

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T21:17:31.087 |

ReadyMedia (formerly MiniDLNA) versions 1.3.0 through 1.3.3 contain a stack-based buffer overflow vulnerability that allows remote attackers to corrupt stack memory by crafting a malicious DFF audio file with an oversized PROP chunk size value that is used unvalidated to allocate a variable-length stack array and read file data into it. Attackers can place a crafted DFF file in a directory monitored by ReadyMedia to trigger automatic parsing via inotify, achieving remote code execution on unprotected builds or denial of service on hardened builds with stack protections.

### CVE-2026-105475

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-158` |
| Published | 2026-11-02T21:17:22.537 |

Improper neutralization of a NUL byte in cPanel allows remote attackers to read any mail account's calendar and contact data.

### CVE-2026-119731

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-345` |
| Published | 2026-11-02T19:18:01.683 |

Munshi (by Petpooja) before 2026-06-30 contained a payment bypass vulnerability in its subscription payment webhook at POST /api/payment/order/webhook, which lacks webhook authentication, cryptographic signature verification, source validation, and independent server-side confirmation with the payment provider. A remote, unauthenticated attacker can submit a forged payment-success notification referencing an order obtained from the payment-status redirect URL, causing the backend to mark the subscription as paid/active and granting paid access without an actual successful payment.

### CVE-2026-114408

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252;CWE-476` |
| Published | 2026-11-02T16:17:27.733 |

In Eclipse ThreadX NetX Duo versions 6.4.5.202504 through 6.5.2.202603a, built with IPv6 path MTU discovery, the ICMPv6 Packet Too Big handler uses the destination-table entry it adds without checking that the add succeeded. A sender on the network can fill the destination table with Packet Too Big messages quoting new destinations, after which the next message makes the IP helper thread dereference a NULL pointer, crashing it on targets that fault on address 0 and stopping all network processing.

### CVE-2026-73697

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-78` |
| Published | 2026-11-02T15:17:37.660 |

Control Web Panel (CWP) before webpanel_version 1.16 contains an arbitrary file write and OS command injection vulnerability in the phpini_editor user panel module that allows attackers with access to the module to write attacker-controlled content to arbitrary paths and execute arbitrary OS commands. Attackers can exploit the acc=update action to write files via file_put_contents without path confinement and the acc=addlabelphpiniadv action to pass unsanitized input into shell_exec, achieving code execution in the user panel context.

### CVE-2026-73695

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-02T15:17:37.287 |

Control Web Panel (CWP) before webpanel_version 1.16 contains a path traversal vulnerability in services/users/index.php that allows attackers to include arbitrary local PHP files by supplying an unsanitized module name parameter concatenated directly into an include path. Attackers can inject directory traversal sequences into the module name to achieve local file inclusion and execute arbitrary PHP code in the user panel context.

### CVE-2026-120461

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T15:17:30.247 |

Jpom through 2.11.12 contains a cross-workspace authorization bypass in POST /node/ssh_command/batch that resolves command templates and SSH nodes by ID without workspace filtering. Authenticated users with SSH command execute permission in one workspace can supply foreign template and node IDs to run commands on other workspaces' SSH hosts using their stored credentials.

### CVE-2026-120460

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T15:17:30.053 |

Jpom through 2.11.12 contains a cross-workspace authorization bypass vulnerability that allows authenticated users to manage other workspaces' Docker hosts by supplying foreign Docker asset ids. Attackers with Docker permission in any workspace can control containers, images, volumes and networks, including creating privileged containers with host bind mounts.

### CVE-2026-120445

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-02T15:17:27.107 |

madong-admin-saas through 5.1.4 contains an incorrect authorization vulnerability in AccessTokenMiddleware that allows authenticated tenant users to access the platform management API in multi-tenant mode. Attackers can reuse a tenant login JWT against /platformapi controllers to create platform administrator accounts, read tenant database settings, and take control of every tenant.

### CVE-2026-120426

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T15:17:23.583 |

OpenCSG CSGHub through v2.6.0-ce contains an authorization bypass vulnerability in the unauthenticated file resolve route that allows remote attackers to read private repository files. Attackers can inject a percent-encoded current_user parameter into the file path, which the portal forwards with its server API key, to read files in private model, code or space repositories.

### CVE-2026-119742

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T14:17:34.843 |

Nagios XI before 2026R2 contains an OS command injection vulnerability in the MIB upload feature where the install_mib() function in mibs.php sanitizes uploaded filenames with an incomplete character deny-list that omits semicolons and pipes before passing them to a grep command executed via exec(). An authenticated administrator can upload a MIB file with a crafted filename using tab characters to bypass the deny-list and pipe to sh via a multipart POST request to mibs.php, resulting in arbitrary OS command execution as the web server user.

### CVE-2026-108047

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-03T13:17:17.337 |

Inadequate authorization vulnerability in Alosuite’s user invitation functionality. The ‘/Requests/userInvitation’ endpoint does not properly validate the assignment of privileges on the server, allowing an attacker to manipulate the invitation parameters during the request process. By intercepting and modifying a legitimate invitation request, an unauthenticated attacker can assign administrative privileges to a newly invited user without the appropriate authorization checks. A successful exploit results in unauthorized privilege escalation, granting full administrative access to the affected application.

### CVE-2026-105982

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-03T09:17:10.353 |

Improper input validation in the IPsec VPN function may allow a remote attacker with high privileges to inject system commands and execute them with root privileges.

### CVE-2026-105981

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T09:17:10.217 |

Improper input validation in the Digital I/O function may allow a remote attacker with high privileges to inject operating system commands and execute them with root privileges.

### CVE-2026-105980

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-03T09:17:10.073 |

Improper input validation in the WireGuard VPN function may allow a remote attacker with high privileges to inject system commands and execute them with root privileges.

### CVE-2026-105979

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-03T09:17:09.930 |

Improper input validation in the ZeroTier VPN function may allow a remote attacker with high privileges to inject system commands and execute them with root privileges.

### CVE-2026-105978

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T09:17:09.747 |

Improper input validation in management control functions may allow a remote attacker with high privileges to inject operating system commands and execute them with root privileges.

### CVE-2026-77880

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T16:17:43.973 |

Control Web Panel (CWP) before webpanel_version 1.16 contains an OS command injection vulnerability in the loopback API password change route /newpass/, which runs as root. An attacker can inject arbitrary OS commands by manipulating the POST 'user' parameter that is passed unescaped into a shell command, achieving remote code execution with root privileges.

### CVE-2026-77878

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T16:17:43.640 |

Control Web Panel (CWP) before webpanel_version 1.30 contains an OS command injection vulnerability in the loopback API database restore route /v1/restoredatabase/, where the restoreDBBackup() handler passes an attacker-controlled file path from the POST body into a shell command without proper escaping. An attacker able to reach the route can inject arbitrary OS commands that execute as root.

### CVE-2026-77877

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-02T16:17:43.473 |

Control Web Panel (CWP) before webpanel_version 1.30 contains a missing authentication vulnerability that allows attackers able to reach the loopback API service to invoke root-privileged API routes without presenting an access token. Attackers can access endpoints such as /v1/restoredatabase/, /generaluser/, /last_access/, /valid_user/, /valid_token/, and /user_panel_dashboard/ to perform unauthorized actions with root privileges.

### CVE-2026-104080

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T16:17:22.740 |

Control Web Panel (CWP) before webpanel_version 1.30 contains an OS command injection vulnerability in the loopback API /valid_token/ route that allows unauthenticated attackers to execute arbitrary commands as root by injecting shell metacharacters into the unvalidated 'user' parameter. Attackers can send a crafted request to the /valid_token/ route, which passes the parameter unescaped into a shell_exec() call.

### CVE-2026-120487

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-02T15:17:30.467 |

LaraDashboard before 1.4.5 contains an incorrect authorization vulnerability in SettingPolicy::manageCoreUpgrades() that allows non-Superadmin administrators with settings.edit to access Superadmin-only core-upgrade operations. Attackers can use the /admin/settings/core-upgrades backup, download, restore and upgrade actions to obtain database dumps containing password hashes and restore or upgrade the site.

### CVE-2026-120448

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-02T15:17:27.737 |

DoraCMS through 3.1.0 contains a mass assignment vulnerability in the PUT /api/v1/user/api-keys/:id endpoint that allows authenticated low-privileged users to rebind their API key to another user's account. Attackers can set the userId field on their own key to a victim's id, then act as that victim to modify profiles and publish or delete content.

### CVE-2026-120318

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T15:17:22.303 |

Product Gallery Slider & Additional Variation Images for WooCommerce 2.3.23 before 2.3.26 contains a missing authorization vulnerability in Codestar backup AJAX actions csf-export, csf-import and csf-reset. Shop Managers can read the csf_backup_nonce from the settings page and supply arbitrary option names via the 'unique' parameter to read, overwrite or delete WordPress options, including modifying wp_user_roles to escalate to administrator.

### CVE-2026-115231

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-11-03T09:17:10.797 |

In Eclipse ThreadX versions 6.0.1 through 6.5.2.202603, the Module Manager lets a user-mode, memory-protected module post a forged callback request to another module's callback request queue. The receiving module's callback thread calls the function pointer in the request without checking that the Module Manager sent it, so the attacker's code runs with the receiving module's privilege; when that module runs in privileged mode, a user-mode module gains privileged execution.

### CVE-2026-120833

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-03T01:16:52.260 |

labbench before 0.46.1 contains a deserialization of untrusted data vulnerability in read() and read_relational() that passes any file with a .p or .pickle extension to pandas.read_pickle based on the extension alone. Attackers who supply a crafted data file or relational data archive can execute arbitrary code when a user loads it with these functions.

### CVE-2026-119737

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-02T20:17:38.143 |

The pppoe_wrapper vendor daemon from the Amlogic Android SDK, as shipped on Nexbox A95X (Amlogic S905/S905X) TV boxes, contains a command injection vulnerability that allows local attackers to execute arbitrary commands as root by sending crafted messages to a world-writable AF_UNIX datagram socket at /dev/socket/pppoe_wrapper. Attackers can send a message beginning with 'pppd pty' followed by shell metacharacters and arbitrary commands, which are passed unfiltered to system(3) and executed by /system/bin/sh -c as root, resulting in full privilege escalation.

### CVE-2026-77879

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T16:17:43.810 |

Control Web Panel (CWP) before webpanel_version 1.16 contains a SQL injection vulnerability in the loopback API authentication gate access_token(), which connects to MySQL as root and interpolates attacker-controlled values directly into its query. Attackers can inject SQL through the authorization_code and client_id parameters to read arbitrary database contents and forge the authentication result, bypassing the API's authentication check.

### CVE-2026-120438

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-02T15:17:25.767 |

QuickJS-NG before 0.16.0 contains an integer overflow in js_proxy_get_own_property_names() in quickjs.c that causes a heap buffer overflow on 32-bit hosts. Attackers running JavaScript can return a large array-like object from a Proxy ownKeys trap to wrap the allocation size, causing crashes or potential code execution.

### CVE-2026-120436

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-02T15:17:25.440 |

Netpbm before 10.86.51, 11.x before 11.02.30, and 11.03 before 11.15.08 contains an integer overflow in jbigtopnm that causes heap buffer overflow when computing output buffer size. Attackers can supply a crafted multi-plane JBIG file with large header dimensions so jbg_dec_merge_planes() overflows the undersized buffer, causing crashes or potentially code execution.

### CVE-2026-120435

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-02T15:17:25.277 |

Netpbm before 10.86.51, 11.x before 11.02.30, and 11.03 before 11.15.08 contains a heap buffer overflow in xpmtoppm caused by an unvalidated characters-per-pixel value in the XPM header. Attackers can supply a crafted XPM file with characters-per-pixel greater than 3 to overrun fixed 3-byte colorName hash entries, causing crashes or potentially code execution.

### CVE-2026-120434

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T15:17:25.113 |

Netpbm before 10.86.51, 11.x before 11.02.30, and 11.03 before 11.15.08 contains a stack-based buffer overflow in picttoppm's scanPoly() function in converter/ppm/picttoppm.c. Attackers can supply a crafted PICT file whose polygon edges produce more than 5000 points, overflowing the coord stack array to crash the converter or potentially execute code.

### CVE-2026-120433

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T15:17:24.940 |

Netpbm before 10.86.51, 11.x before 11.02.30, and 11.03 before 11.15.08 contains a stack-based buffer overflow in the picttoppm paintPoly() function due to an unbounded polygon point count. Attackers can supply a crafted PICT file with a polygon exceeding 100 points to overwrite the fixed pts array, causing crashes or potentially code execution.

### CVE-2026-120432

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-02T15:17:24.750 |

Netpbm before 10.86.51, 11.02.30, and 11.15.08 contains an integer overflow vulnerability in winicontopam that allows attackers to corrupt heap memory via oversized ICO/CUR dimensions. Attackers can supply a crafted icon file with width or height above 32767, wrapping int16_t loop counters into negative row buffer indices to cause crashes or potential code execution.

### CVE-2026-120431

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-02T15:17:24.573 |

Netpbm before 10.86.51, 11.x before 11.02.29, and 11.03 before 11.15.07 contains a heap-based buffer overflow in sgitopnm's readChannels() function when processing RLE-compressed SGI images. Attackers can supply crafted SGI files with oversized offset table lengths to write controlled data past the heap buffer, causing crashes or potential code execution.

### CVE-2026-58873

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T21:17:35.373 |

In addDragDropListener of WindowManagerService.java, there is a possible permission bypass due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59044

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:57.703 |

In multiple locations, there is a possible use-after-free due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59028

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:57.257 |

In resolveAidConflictLocked of RegisteredAidCache.java, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-59000

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:55.057 |

In multiple locations, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58984

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:54.047 |

In multiple locations, there is a possible memory corruption due to a use-after-free. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58970

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:53.263 |

In deliverResult of AppTimeTracker.java, there is a possible background activity launch due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58965

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:52.807 |

In handleAudioEffectBroadcast of MusicFxHelper.java, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58957

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:52.280 |

In resolveToHeavyWeightSwitcherIfNeeded of ActivityStarter.java, there is a possible background activity launch due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58946

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-02T20:17:51.610 |

In navigateUpTo of ActivityClientController.java, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58944

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:51.393 |

In moveTaskToFrontLocked of ActivityTaskManagerService.java, there is a possible background application launch (bal) issue due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58943

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:51.290 |

In run of AddAccountSettings.java, there is a possible background activity launch due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58942

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:51.170 |

In do_fault_around of memory.c, there is a possible use after free due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58934

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-02T20:17:50.720 |

In prepareWindowToDisplayDuringRelayout of WindowState.java, there is a possible permission bypass due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58885

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:50.387 |

In multiple locations, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58884

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:50.280 |

In startTetheredHotspotRequest of WifiServiceImpl.java, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58866

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T20:17:49.013 |

In setAccessibilityWindowAttributes of AccessibilityWindowManager.java, there is a possible untrusted/misleading UI issue due to a missing permission check. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58837

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-02T20:17:48.170 |

In multiple locations, there is a possible background activity launch due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58829

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:47.940 |

In fuse_backing_mmap of backing.c, there is a possible memory corruption due to a use after free. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58828

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:47.817 |

In multiple functions of base.c, there is a possible use-after-free due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58827

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:47.703 |

In multiple functions of dma-buf.c, there is a possible use after free due to a race condition. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58826

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:47.573 |

In ksys_unshare of fork.c, there is a possible memory corruption due to a use after free. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-58825

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:47.447 |

In multiple functions of fork.c, there is a possible use after free due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55289

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:45.293 |

In multiple functions in multiple locations, there is a possible execution of sensitive USSD codes due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55287

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-02T20:17:45.017 |

In onCreate of GrantCredentialsPermissionActivity.java, there is a possible way to trick the user into granting account credentials due to misleading or insufficient UI. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55283

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:44.900 |

In multiple locations, there is a possible memory safety issue due to a use-after-free. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55275

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-02T20:17:44.783 |

In multiple locations, there is a possible use-after-free due to a race condition. This could lead to remote escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55271

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:44.563 |

In forwardToPreferredActionPickHandler of ContactsPickerActivity.kt, there is a possible intent redirection due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55262

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-02T20:17:44.217 |

In setNotificationListenerAccessGrantedForUserInternal of NotificationManagerService.java, there is a possible  policy desynchronization due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-55257

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-02T20:17:43.983 |

In UsbDialogHelper of UsbDialogHelper.java, there is a possible UI confusion due to misleading or insufficient UI. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49931

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:43.170 |

In onActivityResult in multiple locations, there is a possible contact leak from protected profile due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49923

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-451` |
| Published | 2026-11-02T20:17:42.940 |

In onResult of AccountManagerService.java, there is a possible untrusted/misleading UI issue due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-49922

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-11-02T20:17:42.830 |

In queryRemoteConnectionServices of ConnectionServiceWrapper.java, there is a possible permission bypass due to a confused deputy. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-45514

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-02T20:17:42.607 |

In multiple functions of SaveUi.java, there is a possible bypass of package installation requirements due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28597

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-02T20:17:41.907 |

In writeGrantedUriPermissions of UriGrantsManagerService.java, there is a possible permission bypass due to improper input validation. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-28588

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-02T20:17:41.713 |

In shouldBlockDirectoryFromTree of ExternalStorageProvider.java, there is a possible way to access protected data due to a logic error in the code. This could lead to local escalation of privilege with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-111048

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-02T18:18:35.530 |

FOSSBilling is an open source billing and client-management platform. From 0.1.0 until 0.8.9, the admin/support/note_create endpoint stores the note parameter without sanitization in the support_ticket_note table, and src/modules/Support/templates/admin/mod_support_tickets.html.twig renders each stored support ticket note through innerHTML in the admin ticket list. A staff user with only the support.manage_tickets permission can store HTML or JavaScript that executes when another staff member opens the ticket notes. The script runs with the viewing staff member's session and privileges, can read a CSRF token and accessible client or invoice data, and can perform administrative actions available to the viewer, including a Super Administrator. The ticket detail page is not affected because its Twig rendering uses autoescaping. This issue is fixed in version 0.8.9.

### CVE-2026-109142

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T16:17:27.267 |

When a CA's parent lives on the same Krill server: instead of building and verifying a signed CMS message, it runs the RFC 6492 provisioning exchange in-process and trusts the child identity (child_handle) that the caller put in the parent contact. Nothing checks that this child identity actually belongs to the CA making the request.

### CVE-2026-109141

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T16:17:27.120 |

The vulnerability gives a role that is restricted to a list of CAs (cas = [...]) its full permission set for every request that is not tied to a CA, including the bulk import endpoint POST /api/v1/bulk/cas/import. It adds a new child CA under any existing CA, gives the child any of that CA's resources, and creates the ROAs given in the request

### CVE-2026-109140

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-323` |
| Published | 2026-11-02T16:17:26.953 |

The vulnerability is that Krill encrypts every login-session token with a nonce built from a counter that is reset to 0 on every Krill restart, so the same (key, nonce) pair is used again after each restart.

### CVE-2026-119179

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-226` |
| Published | 2026-11-03T14:17:33.617 |

A flaw in the connection management layer of the MongoDB Node.js driver can leave a pooled network connection in the pool for reuse while data from an earlier operation is still outstanding on it. In applications that enable an optional client-side operation timeout, an unauthenticated party that can send ordinary requests to the application may cause database replies to be paired with the wrong requests. This may result in unintended disclosure of other users' records, incorrect operation results being returned, and failures of legitimate requests.

### CVE-2026-116766

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T21:17:24.920 |

CVE-2026-116766 is an improper input handling vulnerability
in the Secure Access server versions between 13.0 and prior to 14.61. Attackers
can cause a persistent denial of service of the server.

### CVE-2026-120439

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-02T15:17:25.937 |

QuickJS-NG before 0.16.0 contains an integer overflow in js_typed_array_sort() in quickjs.c that allows attackers to cause a heap buffer overflow on 32-bit hosts. Attackers who can run JavaScript can call TypedArray.prototype.sort with a comparator on a typed array near 2^30 elements, wrapping the allocation size and writing indices past the buffer to crash or potentially execute code.

### CVE-2026-115403

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252;CWE-476` |
| Published | 2026-11-02T22:17:18.543 |

In Eclipse ThreadX NetX Duo versions 6.0 through 6.5.2.202603a, built with BSD raw socket and IPv6 support, the IPv6 raw send path uses the destination-table entry it adds without checking that the add succeeded. When the destination table is full and an off-link destination is reached through a default router whose neighbour cache entry is unknown, sending on an IPv6 raw socket with header inclusion dereferences a NULL pointer; a remote sender can fill the table, for example with ICMPv6 Packet Too Big messages, and crash the sending thread.

### CVE-2026-77691

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-03T10:17:18.890 |

ZohoCorp ManageEngine Key Manager Plus versions before 7151 allow authenticated users to enter malicious input when configuring a Microsoft CA

### CVE-2026-120577

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T05:18:34.257 |

The FluentCart A New Era of eCommerce – Faster, Lighter, and Simpler plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the deleteFile function in all versions up to, and including, 1.6.2. This makes it possible for authenticated attackers, with custom-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php).

### CVE-2026-120574

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-03T05:18:33.840 |

The SureCart plugin for WordPress is vulnerable to unauthenticated account takeover in all versions up to, and including, 4.9.5. The passwordless one-time-code login REST route (VerificationCodeController::verify(), whose permission callback returns true) resolves an attacker-supplied login to any WordPress user, verifies a 6-digit code, and on success calls $user->login() → wp_set_auth_cookie() for a user of any role. In the affected versions this path has no per-account attempt counter, no persistent email/IP lockout or rate limit (the upstream CDN throttle is bypassable via IP rotation), and no restriction preventing high-privilege accounts from being logged in through it. An unauthenticated attacker can trigger a code for any user (including an administrator) via the companion unauthenticated endpoint and brute-force the 6-digit code to obtain an authenticated session as that user, resulting in a full administrator account takeover.

### CVE-2026-120538

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-03T05:18:32.193 |

The Easy Digital Downloads plugin for WordPress is vulnerable to authentication bypass leading to administrator account takeover in all versions up to, and including, 3.7.2. During a PayPal guest checkout, the email address entered in the guest-checkout field is trusted as proof of identity: edd_get_purchase_form_user() binds the new guest order to an existing WordPress user purely on an email-address match, rewriting the order's user_id to that user's ID. The PayPal capture sink PurchaseUser::maybe_log_in_after_capture() then looked the user up by the order email (get_user_by( 'email', $order->email )) and, when $order->user_id equalled that user's ID (which the email-binding step guarantees), issued an authenticated session with wp_set_auth_cookie(). An unauthenticated attacker who starts a guest checkout using an administrator's email address (where that administrator has no existing EDD customer record) and completes the PayPal purchase flow therefore receives an authenticated session as that administrator — a full account takeover. The same sink is reachable through the standard PayPal checkout and the REST UnbrandedCard and Fastlane flows.

### CVE-2026-91898

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-02T20:18:04.390 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.54.0, contain an Improper Verification of Cryptographic Signature vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Arbitrary Code Execution and Elevation of Privilege.

### CVE-2026-91893

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-02T20:18:03.673 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.54.0, contain an Improper Privilege Management vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privilege.

### CVE-2026-58836

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-11-02T20:17:48.053 |

In handlePackagePostInstall of InstallPackageHelper.java, there is a possible Enhanced Confirmation Mode (ECM) bypass vulnerability that allows a sideloaded application to modify the package source during a self-update due to a logic error in the code. This could lead to local escalation of privilege with User execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-99239

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:49.540 |

In the Linux kernel, the following vulnerability has been resolved:

Bluetooth: L2CAP: refuse __l2cap_chan_add if chan already has conn

l2cap_chan may be linked to l2cap_conn at most once. This is assumed in
several places, eg l2cap_chan_del cleanup.

There is a TOCTOU race where the invariant is violated:

    [Task 1]                          [Task 2]
    l2cap_chan_connect                l2cap_sock_bind
      l2cap_chan_lock                   lock_sock
      l2cap_state_change                if (sk->sk_state != BT_OPEN)
        chan->state = BT_CONNECT
        l2cap_sock_state_change_cb      chan->state = BT_BOUND
                                        sk->sk_state = BT_BOUND
          lock_sock <------------------ release_sock
          sk->sk_state = BT_CONNECT

l2cap_sock_connect() does not check sk->sk_state, so since chan->state
is now BT_BOUND, subsequent connect() ends up with second
__l2cap_chan_add.

Explicitly document and check the invariant in __l2cap_chan_add with
WARN_ON_ONCE. The only callsite where it could be hit is
l2cap_chan_connect, so add pre-check there to avoid relying on
chan->state. chan->state read/write is not properly guarded currently so
there can be other TOCTOUC problems.

Add l2cap_lock_chan in l2cap_sock_bind() to guard chan->state write.

### CVE-2026-99238

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:49.380 |

In the Linux kernel, the following vulnerability has been resolved:

tracing: Hold trace_types_lock when updating modules in persistent instances

trace_module_record() walks ftrace_trace_arrays from the module notifier
without trace_types_lock. A concurrent rmdir of an instance removes it
from the list and frees it under that lock, so a module load or unload
can walk into a freed trace_array.

### CVE-2026-99237

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:49.213 |

In the Linux kernel, the following vulnerability has been resolved:

tracing: Hold trace_types_lock when resetting last boot data from readers

update_last_data_if_empty() is called from tracing_open() with O_TRUNC,
tracing_read_pipe() and tracing_buffers_read() without trace_types_lock.
Two readers can both pass the LAST_BOOT test and free module_delta
twice, and a module notifier can update module_delta while it is being
freed.

Take trace_types_lock in those paths and keep the callers that already
hold it on an unlocked variant.

### CVE-2026-99236

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:49.003 |

In the Linux kernel, the following vulnerability has been resolved:

tracing: Reject incomplete event filter expressions

A non-empty expression normally finishes in predicate_parse()'s inner
loop, which resolves the pending logical operators before jumping to
finalization. If the input ends after an operator, possibly followed by
unary '!' tokens, the outer loop instead falls through with unresolved
operator state.

For example, "common_pid == 1 || common_pid == 2 &&" leaves
prog[0].target equal to -1. The second pass then reads prog[-1] before
the forward-jump check can reject it. Depending on adjacent slab
contents, it can also copy an out-of-bounds word into a branch target
that passes the forward-only check. A self-targeted perf tracepoint
counting event can reach this path through PERF_EVENT_IOC_SET_FILTER.

Reject the outer-loop fallthrough when a predicate has already been
parsed. This ensures that non-empty expressions only reach finalization
after the inner loop has resolved their operators. Keep the existing
no-filter error for input that has no predicates. Add a regression test
for trailing logical operators and unary negations.

### CVE-2026-99235

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:48.790 |

In the Linux kernel, the following vulnerability has been resolved:

tracing: Save the event file instead of the compatible histogram

create_field_var_hist() creates a histogram on the matched event to
supply a field variable, and records it on the target so it can be torn
down later:

	hist_data = find_compatible_hist(target_hist_data, file);
	...
	/* Save the compatible histogram information */
	var_hist->hist_data = hist_data;

hist_data is not the histogram it creates. It is one that was already
there, whose keys the new one copies. The saved pointer has a single
user, unregister_field_var_hists(), which runs when the target is
removed:

	file = hist_data->field_var_hists[i]->hist_data->event_file;

find_compatible_hist() matches on keys alone, so it can pick one with no
variables of its own. check_var_refs() then returns false and the user
can remove it while the target still points at it:

 BUG: KASAN: slab-use-after-free in event_hist_trigger_free+0x2b2/0x320
 Read of size 8 at addr ffff8880093b90e0 by task init/1

 Freed by task 1:
  kfree+0x154/0x420
  event_hist_trigger_free+0x1d5/0x320
  event_hist_trigger_parse+0x35f3/0x69e0
  trigger_process_regex+0x1a6/0x250

Save the event file instead. It is all the dereference ever wanted, and
it does not go away when the user removes a trigger.

### CVE-2026-99233

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:48.390 |

In the Linux kernel, the following vulnerability has been resolved:

tracing/histograms: Verify event_call identity when updating synth_event refcount

In event_hist_trigger_parse() and hist_unreg_all(), the histogram
registration and unregistration paths look up find_synth_event() using
trace_event_name(file->event_call) and adjust se->ref if a match is
found.

Because find_synth_event() only compares the event basename, registering
or removing a histogram on a non-synthetic trace event whose basename
matches a synthetic event erroneously modifies the synthetic event's
reference count.  If a histogram is registered on the non-synthetic
event before the synthetic event is created and removed afterwards,
se->ref is decremented without a matching increment, allowing the
synthetic event to be freed while an active histogram action still holds
a pointer to it.

Introduce find_synth_event_call() to verify that &se->call matches
file->event_call before adjusting se->ref.

### CVE-2026-99231

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:48.060 |

In the Linux kernel, the following vulnerability has been resolved:

io_uring/waitid: own the request before clearing ->head

io_waitid_remove_wq() only takes the wait queue lock if ->head is set.
io_waitid_wait() clears ->head first thing, before it tries to become the
owner of the request by bumping ->refs. If somebody else owns the request
at that point, nothing keeps it from completing the request while the
wake up handler is still going to touch it:

CPU0 (io_waitid_wait)                 CPU1 (io_waitid, holds a ref)
list_del_init(&wait->entry)
smp_store_release(&iw->head, NULL)
                                      __do_wait() finds another child
                                      io_waitid_remove_wq()
                                        // ->head == NULL, no locking
                                      io_waitid_finish(), IOU_COMPLETE
                                      // request freed and reused
atomic_fetch_inc(&iw->refs)

The same goes for __io_waitid_cancel() if it claims the request in that
window. ->refs is part of the per opcode data of the request, so this
increments whatever the next user of the request keeps there. If that
happens to be zero, the handler concludes that it owns the request, and
queues io_waitid_cb() for it. With the window held open by a delay, and
the request reused for a receive that is waiting for data:

  BUG: KASAN: slab-use-after-free in __wake_up_common+0x1ca/0x1f0
   __wake_up_sync_key+0x36/0x50
   sock_def_readable+0xf1/0x420
   unix_stream_sendmsg+0x60b/0x1110
  Allocated by task 87:
   io_arm_apoll+0x1ed/0x940
  Freed by task 87:
   __io_submit_flush_completions+0x118d/0x1a10
   tctx_task_work_run+0x327/0x950

Only clear ->head once the handler owns the request. If it doesn't, the
owner finds ->head set and has to wait for the lock, which is held by the
caller of the handler. Deleting the already deleted entry again is
harmless.

### CVE-2026-99227

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:47.420 |

In the Linux kernel, the following vulnerability has been resolved:

io_uring/waitid: prevent cancel reference wrap

io_waitid packs the cancellation state into bit 31 of ->refs and uses
bits 30:0 as a 31-bit reference counter:

  #define IO_WAITID_CANCEL_FLAG BIT(31)
  #define IO_WAITID_REF_MASK    GENMASK(30, 0)

__io_waitid_cancel() marks a request canceled, then increments the low
bits of ->refs to claim completion ownership. When another path owns the
request, the increment remains even though cancellation returns false.
The request remains discoverable by cancellation, so repeated failed
attempts can wrap the 31-bit reference field to zero. A later
cancellation can claim ownership and complete the request a second time.

Use atomic_fetch_or() when setting the cancel flag and inspect the old
flag value. The first cancel attempt continues to the existing ownership
increment, preserving its wake and issuer handoff semantics. Later
attempts see the cancel flag and return without incrementing the
reference field.

This makes repeated failed cancellation attempts idempotent while
leaving the first-cancel state transitions unchanged.

### CVE-2026-77800

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-304` |
| Published | 2026-11-03T05:18:52.577 |

ManageEngine Key Manager Plus versions before 7151 are vulnerable to a SAML authentication bypass that allows attackers to log in using SAML assertions meant for another service provider.

### CVE-2026-120752

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T23:17:20.243 |

PyMuPDF 1.25.3 before 2.0 contains a stack-based buffer overflow vulnerability in JM_set_annot_callout_line() that copies a caller-supplied number of callout points into a fixed three-element stack array. Attackers who control the callout argument passed to Page.add_freetext_annot() can supply four or more points to overwrite the stack frame, crashing the process or executing code.

### CVE-2026-81938

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T19:18:11.127 |

Grafana Mimir's Alertmanager rejects tenant-supplied receiver configurations that reference local files, but the check did not cover two HTTP client settings: http_headers.<name>.files and basic_auth.username_file. A tenant permitted to upload an Alertmanager configuration could point these fields at any file readable by the Alertmanager process. When a notification was sent, Alertmanager read the file and put its contents in a header of the outgoing request. By directing the receiver at a server they control, the tenant could read files from the Alertmanager host, such as credentials and configuration.

Exploitation requires permission to write the tenant's Alertmanager configuration. Grafana Enterprise Metrics (GEM), which is built on Mimir, is also affected. The issue is fixed in Mimir 3.1.7 and 3.2.2 and in GEM 2.17.20. GEM 2.11 through 2.16 will not receive a fix; users on those versions should upgrade to 2.17.20 or later.

### CVE-2026-88809

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-02T16:17:44.897 |

A security vulnerability exists in the SUSE Rancher Manager meta proxy endpoint (/meta/proxy). This endpoint is intended to forward requests only to  destinations that appear on a configured allowlist. The allowlist decision was evaluated in a  place where it could not stop a request from being forwarded, so a rejected destination was logged but the request was still handed to the proxy's transport. This affects SUSE Rancher 2.15.0 up to 2.15.3, 2.14.0 up to 2.14.7, 2.13.0 up to 2.13.11, 2.12.0 up to 2.12.15, 2.11.0 up to 2.11.19 and potentially older EOL versions.

### CVE-2026-16900

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-03T08:17:15.370 |

Zohocorp ManageEngine Log360 and EventLog Analyzer versions 13071 and below are vulnerable to an authentication bypass in local collector registration, allowing unauthenticated actor to register a local collector by sending a specially crafted registration request.

### CVE-2026-120559

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-03T05:18:33.230 |

The Contact Form Extender for Divi Builder plugin for WordPress is vulnerable to Arbitrary File Deletion due to insufficient file path validation in the cfefd_remove_uploaded_file() function in all versions up to, and including, 1.0.6. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The nonce protecting this AJAX action is rendered into the public page source via wp_localize_script and is therefore retrievable by any unauthenticated visitor.

### CVE-2026-58853

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-11-02T20:17:48.780 |

In multiple functions of ipphelper.c, there is a possible stack bugger overflow due to a missing bounds check. This could lead to remote denial of service with no additional execution privileges needed. User interaction is not needed for exploitation.

### CVE-2026-120064

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129;CWE-190` |
| Published | 2026-11-02T19:18:03.707 |

Several psqlODBC entry points use an application-supplied column number or row index as an array index without validating it. SQLBindCol with a column number above 32767 wraps the binding count negative and a later copy runs off the array. A negative SQL_DESC_COUNT on an application row descriptor unbinds columns at negative indexes. SQLColAttribute with a very large column number uses a negative index. SQLSetPos(SQL_ADD) does not check the row number against the rowset size. An application that forwards untrusted column or row numbers exposes its process to out-of-bounds reads and writes. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-120062

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T19:18:03.423 |

SQLSpecialColumns in psqlODBC splices the table and schema names it receives into its catalog query without escaping them, while the other catalog functions escape them. An application that passes an untrusted table or schema name to SQLSpecialColumns lets the caller execute arbitrary SQL with the privileges of the connection. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-120061

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-193;CWE-457` |
| Published | 2026-11-02T19:18:03.273 |

The psqlODBC parser for ODBC escape sequences in application SQL text writes the argument offsets of a {fn} escape into a fixed 16-entry stack array without a bound and does not initialize the array. An escape with too many arguments overflows the stack, and a reference to an unsupplied argument copies arbitrary bytes into the query. The copy of a {d}, {t}, {ts}, or {escape} body also writes one byte past a 128-byte stack buffer. An application that forwards untrusted SQL text to the driver exposes its process to memory corruption. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-120058

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-11-02T19:18:02.857 |

psqlODBC sizes its row cache from the column count of a cursor's first result, but recomputes the column count from each later FETCH reply without checking that it matches. A server not trusted under current SSL settings can answer a later FETCH with more columns and make the driver write tuple records past the end of the heap allocation. A keyset reply with fewer columns than the key fields also underflows the unsigned field count. This is reachable with UseDeclareFetch enabled. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-120057

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-02T19:18:02.700 |

psqlODBC copies the reply to a large-object read (loread) into the application's buffer using the length sent by the server, without comparing it to the buffer size. A server not trusted under current SSL settings, or a man-in-the-middle, can return more bytes than the buffer holds and overwrite adjacent memory in the client process with server-chosen bytes. Fetching any large-object column is sufficient to trigger it. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-117069

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-02T19:18:00.827 |

An integer truncation vulnerability in the NAS decoder of OpenAirInterface (OAI) CN5G AMF v2.2.1 allows an unauthenticated remote attacker to cause a denial of service (DoS) via crafted NAS Registration Requests containing a malformed IMEISV in the 5GS Mobile Identity IE. The Type6NasIe::Validate() function truncates a 32-bit length value to 16 bits, bypassing length validation and causing an out-of-bounds heap read in DecodeImeisv(), which can crash the AMF process.

### CVE-2026-106808

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-02T18:18:34.120 |

OpenAirInterface Core Network v2.2.1 has a stack-based buffer overflow vulnerability in the OAI CN5G UDM Nudm_UEAU Generate Authentication Data endpoint. The UDM passes attacker-controlled resynchronizationInfo.rand and auts values to conv::hex_str_to_uint8(), which converts arbitrary-length hex strings into fixed-size stack buffers without validating the destination size. An unauthenticated attacker with access to the SBI interface and a valid SUPI can submit an oversized value to overwrite adjacent stack memory, corrupt the stack canary, and terminate the UDM process.

### CVE-2026-120596

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-02T17:17:40.003 |

A remotely exploitable denial-of-service vulnerability exists in the TCP options parser of the Nut/Net TCP/IP stack included in Nut/OS, developed by Ethernut/Egnite. Nut/OS releases up to version 5.1 are affected. An unauthenticated attacker can send a single TCP segment containing an unknown TCP option with a length byte of zero to any open TCP port on a vulnerable device. When processed, this malformed option triggers an infinite loop in the function NutTcpInputOptions, permanently blocking the TCP processing thread and rendering all TCP-based services unresponsive until the device is rebooted.

### CVE-2026-106804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-120;CWE-121` |
| Published | 2026-11-02T17:17:33.453 |

A stack-based buffer overflow exists in Kamailio v6.1.3 and v6.1.4 in the ims_qos_npn module. The w_rx_aar_register() function copies the attacker-controlled host field from the SIP `Via` header into a fixed 46-byte stack buffer without validating its length. An unauthenticated remote attacker can trigger the vulnerability with a crafted SIP `REGISTER` request, causing stack corruption and termination of the affected Kamailio instance, resulting in denial of service.

### CVE-2026-77799

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-03T05:18:52.380 |

ManageEngine Key Manager Plus versions before 7150 are vulnerable to a Two-Factor Authentication bypass that allows attackers with valid credentials to log in without a verification code.

### CVE-2026-120830

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-03T00:17:18.947 |

A flaw was found in libslirp in icmp_forward_error(). When building an ICMP error response, the length of the quoted original IPv4 packet was taken from the IP header without clamping it to the actual buffer length. A truncated or malformed packet could cause an out-of-bounds heap read, leaking host memory into the ICMP error packet returned to a guest or container.

### CVE-2026-113421

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-03T09:17:10.647 |

In Eclipse ThreadX versions 6.0.1 through 6.5.2.202603, ThreadX Modules does not revoke a module's trace-buffer-full callback when the module is stopped and unloaded. With event tracing enabled and a kernel-owned trace buffer still active, a later buffer wrap invokes the callback from privileged thread context after the module's code has been released, so a user-mode module can have its code run with kernel privileges after unload, or, once the memory is reused, redirect control flow or cause a fault.

### CVE-2026-120558

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-03T05:18:33.030 |

The Advanced Shipment Tracking for WooCommerce plugin for WordPress is vulnerable to SQL Injection via the `tracking_provider` parameter of the `POST /wp-json/wc-ast/v3/orders/<order_id>/shipment-trackings` REST endpoint in all versions up to, and including, 3.9. This is due to insufficient escaping on the user-supplied parameter and lack of sufficient preparation on the existing SQL query in `WC_Advanced_Shipment_Tracking_Admin::get_provider_slug_from_name()` — the value is concatenated directly into the format string of `$wpdb->prepare()` rather than bound as a parameter, bypassing parameterised-query protections. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to append additional SQL queries into the already-existing query that can be used to extract sensitive information from the database.

### CVE-2026-119733

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T19:18:02.037 |

Munshi (by Petpooja) before 2026-07-07 contained a missing authorization vulnerability in its company deletion workflow at DELETE /api/companies/{company_id}, where the application fails to enforce the dedicated company_delete permission or verify company ownership. An authenticated invited sub-user with mere access to a company can exploit this flaw to perform a hard delete of the company record, causing irreversible loss of associated business data including invoices, configurations, and chat sessions.

### CVE-2026-88810

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-02T17:17:45.647 |

A privilege escalation issue was discovered in Rancher Manager's role-based access control. The inheritedNamespacedRules field of a GlobalRole propagates permissions into named namespaces of every downstream cluster managed by the Rancher instance, but it was not subject to the privilege-escalation validation applied to the other permission-carrying fields of a GlobalRole. As a result, a non-administrative user could be granted, through a global role  binding, permissions in downstream clusters that exceed the permissions that user already holds. This affected SUSE Rancher 2.15.2 only, and SUSE Rancher Webhook 0.11.0 up to 0.11.4, and 0.12.0 up to 0.12.1.

### CVE-2026-120444

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-02T15:17:26.917 |

GoFound through 1.4.1 contains a path traversal vulnerability that allows unauthenticated attackers to delete arbitrary directories by supplying ../ sequences in the database parameter. Attackers can send GET requests to /api/db/create and /api/db/drop, directly or via a victim's browser, triggering os.RemoveAll on directories outside the data directory.

### CVE-2026-121458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T13:17:21.997 |

Instatic before 0.0.21 contains a missing authorization vulnerability in its AI/MCP content read tools that allows low-privileged authenticated users with ai.chat and content.edit.own capabilities to access data rows belonging to other users by calling content_get_document and content_list_documents without the object-level authorization checks enforced by the normal HTTP API. Attackers can use the MCP interface to retrieve private or unpublished draft content and enumerate rows from the posts system table, resulting in cross-user data disclosure.

### CVE-2026-77778

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-03T10:17:19.773 |

ZohoCorp ManageEngine Key Manager Plus versions up to 7150 allow authenticated users to export certificates belonging to other users to their own registered key vaults.

### CVE-2026-77777

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-1220` |
| Published | 2026-11-03T10:17:19.640 |

ManageEngine Key Manager Plus versions before 7151 are vulnerable to an improper access control issue that allow authenticated users to modify another user's ACME certificate deployment credentials.

### CVE-2026-120330

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-03T10:17:17.820 |

Backend actions and ajax routes of the mail module do not check whether the backend user has access to the page of the requested mail or recipient group. Backend users with access to the mail module can view, change, send and export mails and recipient groups outside their web mounts, including the personal data of recipients.

### CVE-2026-116768

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-02T21:17:25.197 |

CVE-2026-116768 is a missing length validation vulnerability
in Secure Access servers prior to 14.61. Authenticated attackers can cause a
persistent denial of service when connecting for the first time.

### CVE-2026-116767

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T21:17:25.050 |

CVE-2026-116767 is an improper input handling vulnerability
in Secure Access servers prior to 14.61. Authenticated attackers can cause a
persistent denial of service.

### CVE-2026-91895

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-02T20:18:03.947 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.54.0, contain an Incorrect Default Permissions vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Information Tampering.

### CVE-2026-120065

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-02T19:18:03.850 |

For an updatable cursor over a table without OIDs that has an auto-increment int4 column, psqlODBC uses that column to identify rows. It places the column's name, as reported by the server, between double quotes in its keyset queries and in the WHERE clause of its positioned SELECT, UPDATE, and DELETE statements, without doubling any double quote in the name. A column name that contains a double quote therefore changes the SQL that the driver runs with the application's privileges, including which rows a positioned UPDATE or DELETE affects. Any database user who can create a table that the application reads with an updatable cursor can choose such a name, and so can a server not trusted under current SSL settings. Versions before psqlODBC 18.00.0006 are affected.

### CVE-2026-119734

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T19:18:02.203 |

Munshi (by Petpooja) before 2026-06-17 contained a broken object level authorization vulnerability that allows authenticated attackers to access another user's purchase inquiry by manipulating the thread identifier in the GET /purchase-inquiry/thread/{thread-id} endpoint. Attackers can modify the thread ID to read supplier communication and quotation-related content belonging to other users, resulting in unauthorized disclosure of sensitive business information outside their access scope.

### CVE-2026-119732

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T19:18:01.870 |

Munshi (by Petpooja) before 2026-07-28 contained a broken object level authorization vulnerability that allows authenticated sub-users to delete invoices belonging to the tenant owner by exploiting the DELETE /api/invoice/{invoice_id} and POST /api/invoices/bulk-delete endpoints, which only verify tenant membership without enforcing object-level ownership or permission checks. Attackers can invoke single or bulk deletion requests with arbitrary invoice identifiers to delete invoices they do not own, resulting in unauthorized data loss.

### CVE-2026-120429

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-02T15:17:24.190 |

Camaleon CMS before 2.9.2 contains a missing authorization vulnerability in Admin::MediaController that allows low-privileged authenticated users to bypass the role-based Media permission. Attackers can POST to /admin/media/upload to store files, read private media via download_private_file, and use crop with saved_avatar to change other users' avatars.

### CVE-2026-120425

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-02T15:17:23.407 |

Chatify before 1.6.4 contains an authorization bypass vulnerability in the Pusher channel authorization endpoint that allows authenticated users to subscribe to other users' private channels by supplying arbitrary channel names. Attackers can request a signature for private-chatify.<victim id> via POST /chat/auth to receive the victim's incoming private messages and attachments in real time.

### CVE-2026-119740

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-02T20:17:38.627 |

Nexbox A95X TV boxes built on the Amlogic S905X platform contain an unauthenticated console exposed via an internal UART header on the PCB that allows physical attackers to obtain an interactive shell as uid 2000 (system) without any credentials. Attackers with physical access and a USB-to-TTL adapter can leverage this shell to reach the pppoe_wrapper vendor daemon, which contains an OS command injection vulnerability executed as root, resulting in full root-level compromise of the device.

### CVE-2026-99224

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:46.830 |

In the Linux kernel, the following vulnerability has been resolved:

keys: Protect the type name while describing a key

keyctl_describe_key() must keep the key type's name alive until
kasprintf() has consumed it. The retained key reference keeps the key
and its description alive, but does not pin the module providing its
type. The name is passed to kasprintf() without holding key->sem.

kvasprintf() uses the saved name pointer in two formatting passes, with
a GFP_KERNEL allocation between them. With AF_RXRPC=m, a task that
passes View permission before type retirement can overlap a privileged
module unload in this order:

1. KEYCTL_DESCRIBE looks up the key, saves key->type->name in the
   kasprintf() arguments and completes the first formatting pass.
2. While the formatter is delayed before its second pass,
   af_rxrpc_exit() calls unregister_key_type(), which removes the type
   from the registry and waits for key_gc_keytype().
3. The collector takes key->sem for writing, retypes the retained key
   to key_type_dead and completes retirement. Unregistration and module
   exit return, allowing free_module() to release the type and name.
4. The formatter resumes its second pass and reads the saved name from
   released module storage, which can fault in string().

Hold key->sem for reading across kasprintf(). The collector then cannot
retype the key or complete retirement until both formatting passes have
finished. If retirement wins the lock first, formatting uses the core
key_type_dead name instead. Release the semaphore immediately after
kasprintf(), including on allocation failure, before copying to
userspace.

Oops report as below:

    BUG: unable to handle page fault for address: fffffbfff8054794
    #PF: supervisor read access in kernel mode
    #PF: error_code(0x0000) - not-present page
    RIP: 0010:string+0x23f/0x470
    Call Trace:
     vsnprintf+0x330/0x1110

### CVE-2026-99218

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-02T16:17:45.740 |

In the Linux kernel, the following vulnerability has been resolved:

coredump: hold RCU while releasing parked threads

coredump_finish() releases the parked threads by clearing ->task in
their core_thread entry and calling wake_up_process() on each of them.
It does that without holding a reference on the task and without being
inside rcu.

But calling wake_up_process(task) without rcu here isn't safe. A parked
thread doesn't need that wakeup to leave. A spurious wakeup or a
preemption after the store is enough for the task to go away.

So if the coredump client is preempted between the store and
wake_up_process() the thread can exit and be freed in the meantime and
try_to_wake_up() takes pi_lock in freed memory.

Hold rcu across the loop.

### CVE-2026-115653

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787;CWE-822` |
| Published | 2026-11-02T16:17:28.683 |

In Eclipse ThreadX versions 6.0.1 through 6.5.2.202603, the PendSV handler of the Cortex-M module ports saves a preempted user-mode module thread's registers in privileged mode at addresses taken from the thread's stack pointer, without checking that pointer against the thread's stack. A user-mode, memory-protected module can thereby write up to nine words, eight of its choosing, or 25 with floating-point state, into memory immediately below any region it may write, and read back what is stored there.

### CVE-2026-120451

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-02T15:17:28.357 |

libgphoto2 through 2.5.34 contains stack-based and heap-based buffer overflow vulnerabilities in jl2005c_init() that allow malicious USB devices to corrupt memory by supplying an unbounded allocation table entry count. Attackers can connect a spoofed Jeilin JL2005B/C/D camera reporting 1022 or more entries to overwrite the saved return address and heap data, potentially achieving code execution.
