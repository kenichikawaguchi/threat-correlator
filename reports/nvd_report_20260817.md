# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-16 15:00 UTC
- **対象期間**: `2026-08-15T15:01:15.000Z` 〜 `2026-08-16T15:00:26.000Z`
- **重要CVE数**: 54 件（Critical 9.0+: 22 件 / High 7.0〜: 32 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公表された CVE のうち **CVSS 7.0 以上が 40 件** 超と、深刻度の高い脆弱性が集中しています。  
- **WordPress エコシステム**（プラグイン）と **SiYuan ノートアプリ** が特に多く、リモートコード実行 (RCE)・特権昇格・任意ファイル操作が目立ちます。  
- さらに **Python 製ツール (Pandora)** や **Scriban テンプレートエンジン** でも、認証不要でコード実行や情報漏洩が可能になる欠陥が報告され、サーバーサイドの信頼境界が揺らいでいます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲（代表的な製品/プラグイン） | 注目理由 |
|-----|------|----------------|-----------------------------------|----------|
| **CVE‑2026‑74764** | 10.0 | Path Traversal → 任意ファイル読み取り/書き込み | Pandora (Python 製アーカイブ処理ライブラリ) | **最高スコア**。`tarfile.extract()` に対しサニタイズが無く、攻撃者は任意の TAR をアップロードするだけでサーバー上の任意ファイルにアクセス可能。認証不要で広範囲に被害が拡大しやすい。 |
| **CVE‑2024‑13784** | 9.8 | PHP Object Injection (POI) | WordPress **ARForms** ≤ 1.8.5 | POI により **無認証で任意コード実行** が可能。プラグインは多数のサイトで利用されており、データベース改ざん・バックドア設置のリスクが極めて高い。 |
| **CVE‑2026‑18432** | 9.8 | 権限昇格 (Privilege Escalation) | WordPress **Frontend Admin (DynamiApps)** ≤ 3.29.9 | `is_numeric()` でのチェック回避により、一般ユーザーが `edit_user` 権限を取得できる。管理者権限取得が容易になるため、サイト全体の制御が奪われる危険性が大きい。 |
| **CVE‑2026‑73043** | 9.4 | Remote Code Execution (テンプレート計算) | SiYuan ≤ 3.7.3 | ユーザー作成の Go テンプレートが **サニタイズなしで保存** され、HTML/JS がそのまま実行される。Node.js が有効な環境では **フルシステム権限でコード実行** が可能。 |
| **CVE‑2026‑73053** | 9.4 | Stored XSS (unicode2Emoji 関数) | SiYuan ≤ 3.7.3 | アイコン名に特殊文字を埋め込むだけで、レンダラ内で任意スクリプトが実行される。ノート共有やチームコラボで広範囲に影響し、情報漏洩やマルウェア配布に利用できる。 |

> **補足**  
> - 上記 5 件は **CVSS が 9.4 以上** かつ **認証不要／低権限での攻撃が可能** という点で共通。  
> - WordPress 系はプラグインの更新が遅れがちで、サイト全体の攻撃対象になることが多い。  
> - SiYuan はローカルデスクトップアプリだけでなく Web UI でも利用されるため、社内情報資産の漏洩リスクが高まります。

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時アップデート
| 製品 / プラグイン | 現行バージョン (脆弱) | **推奨バージョン (修正済み)** | アップデート方法 |
|-------------------|-----------------------|------------------------------|-------------------|
| **Pandora** (Python) | 任意 (脆弱実装) | **≥ 1.2.5** (リリースノートで Path Traversal 修正) | `pip install --upgrade pandora` |
| **ARForms** (WordPress) | ≤ 1.8.5 | **1.8.6** 以上 | WordPress 管理画面 → プラグイン更新、または手動で zip を上書き |
| **Frontend Admin (DynamiApps)** | ≤ 3.29.9 | **3.30.0** 以上 | 同上 |
| **ProSolution WP Client** | ≤ 2.0.10 | **2.0.11** 以上 | 同上 |
| **Pods – Custom Content Types and Fields** | ≤ 3.3.9 | **3.4.0** 以上 | 同上 |
| **SiYuan** (Desktop / Web) | ≤ 3.7.3 | **3.7.4** 以上 | 公式サイトから最新版 (ZIP/DMG) をダウンロードし上書き |
| **Scriban** (テンプレートエンジン) | < 7.2.2 | **7.2.2** 以上 | NuGet パッケージを `dotnet add package Scriban --version 7.2.2` で更新 |
| **その他多数の WordPress プラグイン** (例: ProSolution WP Client, Link Library, Royal Elementor Addons, Podlove Podcast Publisher, Query Wrangler) | 各プラグインの「脆弱」バージョン | 各プラグインの **最新安定版** (2024‑12‑xx 以降リリース) | WordPress → プラグイン → 更新、または公式サイトからダウンロード |

### 3.2 防御的設定・運用上のベストプラクティス
- **最小権限の原則**  
  - WordPress の管理者権限は必要最小限のユーザーに限定し、`edit_user` など高権限 API の呼び出しは **Capability チェック** を必ず実装。  
- **ファイルアップロードの制御**  
  - `php.ini` の `file_uploads` を有効にする場合は `upload_max_filesize`・`post_max_size` を適切に制限し、**MIME タイプと拡張子のホワイトリスト** を導入。  
  - SiYuan の API トークンや WordPress のメディアアップロードは **CSRF トークン** と **Referer ヘッダー検証** を必ず行う。  
- **Web アプリケーションファイアウォール (WAF)**  
  - OWASP ModSecurity Core Rule Set などを導入し、**パス・トラバーサル**、**PHP

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-74764

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-15T22:16:55.563 |

Pandora contains a path traversal vulnerability in its TAR archive extraction functionality. When processing a submitted TAR archive, the extractor passed archive member names directly to Python's tarfile.TarFile.extract() without applying an extraction filter.


An attacker able to submit a specially crafted TAR archive containing malicious member paths, such as paths using ../ sequences or absolute paths, could cause extracted files to be written outside the intended extraction directory. This may allow the attacker to overwrite files accessible to the Pandora worker process and could potentially result in application compromise, arbitrary code execution, or denial of service depending on the files targeted and the privileges of the Pandora process.


The vulnerability is corrected by using Python's filter='data' extraction filter, which rejects or sanitizes dangerous TAR members, including paths that escape the destination directory and unsafe link targets. 


The weakness corresponds to MITRE's general path traversal category, which includes archive extraction cases where attacker-controlled filenames cause files to be written outside the intended directory.

### CVE-2024-13784

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-16T09:16:19.900 |

The Contact Form, Survey, Quiz & Popup Form Builder – ARForms plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.8.5 via deserialization of untrusted input from form submissions. This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-18432

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-16T05:16:48.307 |

The Frontend Admin by DynamiApps plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.29.9. The vulnerability exists because `ActionUser::conditions_logic()` gates the `current_user_can('edit_user', $user_id)` authorization check behind an `is_numeric()` test, causing the check to be skipped entirely when `$user_id` is a non-numeric string — a condition that can be induced by passing a crafted value such as `1one` through the unvalidated `item_id` parameter of the unauthenticated `wp_ajax_nopriv_frontend_admin/forms/change_form` AJAX endpoint. This makes it possible for attackers to escalate privileges to administrator by obtaining a server-signed `_acf_objects` payload carrying the non-numeric user ID, which WordPress subsequently coerces to integer 1 (the default administrator), allowing the attacker to overwrite that account's password or email address. Exploitation by unauthenticated users requires a public-facing frontend user form to be configured; in all other cases a subscriber-level account is sufficient.

### CVE-2026-16098

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-16T05:16:47.667 |

The ProSolution WP Client plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.0.10 via the proSol_handleFileUpload function. This is due to missing validation of the attacker-controlled Content-Disposition header filename, which overrides the allow-listed multipart filename before the file is saved, and a post-save extension check that fails to delete the already-written file. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The nonce required to reach the upload handler is publicly exposed via wp_localize_script on any front-end page rendering the job portal shortcode, allowing unauthenticated visitors to obtain a valid nonce and bypass that gating check entirely.

### CVE-2026-19598

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-15T18:16:23.860 |

The Pods – Custom Content Types and Fields plugin for WordPress is vulnerable to Privilege Escalation via Authorization Bypass in all versions up to, and including, 3.3.9. The vulnerability exists because the pods_admin AJAX router funnels every access check — including the method allowlist, nonce verification, login enforcement, and capability gate — through pods_error(), which under the JSON meta-box-loader compatibility path only writes failures to the PHP error log and returns false instead of terminating the request, rendering all guards ineffective.  This makes it possible for unauthenticated attackers to escalate their privileges to Administrator or overwrite the password of any user account, including the site owner's, enabling complete site takeover, or perform another administrator action.

### CVE-2026-73053

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:55.157 |

SiYuan versions before v3.7.4 contain a cross-site scripting vulnerability in the unicode2Emoji function that fails to sanitize codepoint branch output. Attackers can craft document icons with hex-encoded markup that executes in the renderer with Node integration enabled, achieving arbitrary code execution on the host system.

### CVE-2026-73052

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:55.017 |

SiYuan before v3.7.4 stores attribute-view field names without HTML escaping and interpolates them directly into option elements via innerHTML in the sort menu. Attackers can inject markup by renaming a database field to execute arbitrary JavaScript when users open the sort menu, with Node integration enabled in the desktop client enabling code execution.

### CVE-2026-73050

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:54.870 |

SiYuan versions before v3.7.4 fail to validate or escape the color field in attribute-view select options, allowing stored cross-site scripting through eight unescaped render sites. Attackers can inject event-handler attributes by including quotation marks in the color value, executing arbitrary JavaScript when viewing databases containing the malicious select field.

### CVE-2026-73044

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:54.330 |

SiYuan versions before v3.7.4 fail to validate or escape table column width values, allowing stored cross-site scripting injection into style attributes. Attackers can inject malicious payloads through the setAttrViewColWidth API that break out of style attributes and inject event handlers on every table cell, executing arbitrary code in the Electron renderer with Node integration enabled.

### CVE-2026-73043

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:54.200 |

SiYuan versions before v3.7.4 contain a remote code execution vulnerability in the Template calculation operator, which renders user-authored Go templates and stores output verbatim without sanitization. Attackers can inject malicious HTML and JavaScript into template calculations that execute in the desktop client renderer with Node integration enabled, allowing arbitrary code execution when the database is opened.

### CVE-2026-73042

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:54.030 |

SiYuan before v3.7.4 fails to properly escape database menu metadata in HTML interpolation, allowing stored values to execute script when users open group, view, or field-edit menus. Attackers can inject markup through field descriptions or names that close containing elements and execute arbitrary code via event handlers, reaching Node built-ins due to Electron's insecure configuration.

### CVE-2026-73041

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-15T22:16:53.883 |

SiYuan versions before v3.7.4 fail to validate or escape annotation fields written to disk by the setFileAnnotation endpoint. Attackers can inject malicious markup into annotation fields that execute as script in the PDF renderer with full Node.js access when a user opens an annotated PDF.

### CVE-2026-74790

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-16T14:16:57.050 |

Scriban before 7.0.0 caches TypedObjectAccessor by Type only without considering MemberFilter changes, allowing reused TemplateContext instances to expose members that should be hidden. Attackers can access filtered properties and fields by reusing a TemplateContext after tightening its MemberFilter, bypassing sandbox policies across requests or tenants.

### CVE-2026-73061

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-16T14:16:55.770 |

Scriban before 7.2.2 contains an access-modifier bypass vulnerability in TypedObjectAccessor that allows template code to write CLR object properties without setter-visibility checks. Attackers can modify properties with private, internal, or init-only setters, and perform mass assignment on public-setter properties, permanently altering live host objects after template rendering.

### CVE-2026-73056

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-16T14:16:55.083 |

SiYuan kernel versions before 3.7.4 contain an improper restriction of excessive authentication attempts vulnerability in the CheckAuth() middleware. The middleware accepts the API token (Conf.Api.Token) via an Authorization header (Token/Bearer) or a ?token= query parameter, and neither path is protected by the application's CAPTCHA/lockout mechanism (NeedCaptcha/WrongAuthCount). As a result, an unauthenticated remote attacker can perform unlimited automated guesses of the API token, particularly when a short or weak custom token has been configured, and upon success gains full RoleAdministrator access enabling arbitrary file operations and SQL queries.

### CVE-2026-74251

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-16T13:16:57.147 |

Joomla Extension - phoca.cz -  Unauthenticated SQL injection via attribute filter in Phoca Cart 5.0.0-6.1.6 - The a[] (attribute) and s[] (specification) GET array parameters on Phoca Cart's public shop items page are concatenated raw into SQL WHERE clauses without parameterization or escaping. An unauthenticated attacker can inject arbitrary SQL through these parameters, enabling full database extraction via time-based blind techniques.

### CVE-2026-73055

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-08-15T22:16:55.427 |

Shescape before 2.1.15 (and 3.0.0 before 3.0.2) fails to properly escape tilde (~) characters in assignment contexts on Unix systems where the shell is explicitly configured to "sh" or true and /bin/sh points to BusyBox. Using the escape and escapeAll APIs with untrusted input in an assignment prefixed to a command, an attacker can inject a tilde payload to disclose the user's home directory location and, depending on usage, alter the location on which a command operates.

### CVE-2026-73046

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-15T22:16:54.600 |

SiYuan before v3.7.4 improperly restricts excessive authentication attempts in the CheckAuth() middleware. The HTTP Basic Authentication branch, which guards nearly the entire /api/* surface, accepts the workspace access code (Conf.AccessAuthCode) as the Basic Auth password but never consults the CAPTCHA/lockout gate or increments the failure counter used by the cookie/session login path. This allows unauthenticated remote attackers to brute-force the admin access code with unlimited automated requests and obtain full RoleAdministrator access to the kernel. A secondary weakness exists because the access code is compared using a non-constant-time string comparison.

### CVE-2026-74791

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-226` |
| Published | 2026-08-16T14:16:57.183 |

Scriban before 7.0.0 fails to clear the CachedTemplates dictionary when TemplateContext.Reset() is called, allowing cached templates to persist across reused contexts. Attackers can exploit request-dependent ITemplateLoader implementations to access previously authorized template content from earlier renders without triggering TemplateLoader.Load() again.

### CVE-2026-18316

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-16T06:16:51.683 |

The Solace Extra plugin for WordPress is vulnerable to unauthorized modification and loss of data due to a missing capability check on the import_zip() function in versions up to, and including, 1.6.0. The handler is registered on both wp_ajax_action-import-zip and wp_ajax_nopriv_action-import-zip and only verifies the 'ajax-nonce' nonce, which is emitted on every admin page via wp_localize_script (unrestricted admin_enqueue_scripts hook) and is therefore accessible to any authenticated user including Subscribers. This makes it possible for authenticated attackers, with Subscriber-level access and above, to wipe navigation menus, sidebar widgets (via update_option('sidebars_widgets', array())), all theme mods (via remove_theme_mods()), and Elementor templates, as well as trigger arbitrary demo-content imports.

### CVE-2026-14524

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-16T05:16:46.493 |

The ProSolution WP Client plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the proSol_fileDeleteProcess function in all versions up to, and including, 2.0.8. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). An attacker must first call the proSol_fileUploadModalProcess handler to poison their own session with a path-traversal key, then call proSol_fileDeleteProcess with that key as the filename parameter; both steps require only the publicly exposed frontend nonce.

### CVE-2026-18855

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-15T19:16:32.160 |

The Link Library plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the ll_delete_link_fields function in all versions up to, and including, 7.9.4 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Exploitation requires the administrator to have enabled the 'Delete local file on link deletion' plugin option (disabled by default) and to subsequently permanently delete the attacker-submitted link, which is a routine moderation action.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-19924

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-16T02:16:47.247 |

A security vulnerability has been detected in Tenda AC10 16.03.10.09_multi_TDE01. This vulnerability affects the function R7WebsSecurityHandler of the component httpd. The manipulation leads to improper authentication. The attack may be initiated remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-17123

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-16T05:16:48.033 |

The Royal Elementor Addons plugin for WordPress is vulnerable to Server-Side Request Forgery in versions up to, and including, 1.7.1064 via the Form Builder widget's 'webhook_url' setting. The widget's render() method persists the attacker-controlled URL into the wpr_webhook_url_{widget_id} option on every render (including a Contributor previewing their own draft), and the wpr_form_builder_webhook AJAX handler — registered for both authenticated and unauthenticated callers — reads that option and dispatches the outbound request via the non-safe wp_remote_post(), with no host allowlist, no scheme restriction, and no private/loopback IP filter (the plugin's existing wpr_is_blocked_remote_host / wpr_is_private_or_local_ip helpers are not called on this path). This makes it possible for authenticated attackers, with Contributor-level access and above, to make web requests to arbitrary locations originating from the web application and can be used to query and modify information from internal services.

### CVE-2026-16099

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-16T05:16:47.780 |

The Podlove Podcast Publisher plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the create_link_item function in all versions up to, and including, 4.5.3. This makes it possible for authenticated attackers, with contributor-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). A viable POP chain exists within the plugin itself via Podlove\ImageCache\GenerationGuard, whose __destruct() method invokes wp_delete_file() with an attacker-controlled file path populated through unserialization.

### CVE-2026-14498

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-16T05:16:46.360 |

The Query Wrangler plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.5.57 via the 'options' parameter parameter. This is due to missing capability check and nonce verification on the wp_ajax_qw_form_ajax handler, combined with unsanitized attacker-controlled options fully replacing saved query options and being passed directly to call_user_func_array() guarded only by function_exists(). This makes it possible for authenticated attackers, with subscriber-level access and above, to execute code on the server. Exploitation requires only that at least one query row exists in the database, as the query_id is a small enumerable integer with no further access control.

### CVE-2026-74795

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-16T14:16:57.590 |

Scriban before 6.6.0 contains an uncontrolled recursion vulnerability in its recursive-descent parser. The parser does not enforce a default expression depth limit (the ExpressionDepthLimit property in ParserOptions defaults to null/disabled), so an attacker who controls template input can supply a deeply nested template (e.g., thousands of nested parentheses or blocks) that exhausts thread stack space and raises a StackOverflowException. Because a StackOverflowException cannot be caught in .NET, this causes immediate, unrecoverable termination of the hosting process, resulting in a denial of service. Applications that process untrusted or user-supplied templates can be exploited remotely without authentication.

### CVE-2026-74794

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-16T14:16:57.450 |

Scriban before 6.6.0 contains an infinite recursion vulnerability in object rendering when the ObjectRecursionLimit property defaults to unlimited. Attackers can supply circular reference objects to the template context, exhausting stack space and triggering an uncatchable StackOverflowException that terminates the hosting process.

### CVE-2026-74792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-16T14:16:57.317 |

Scriban before 7.0.0 (affected versions <= 6.6.0) contains a stack overflow vulnerability in nested array initializer parsing. Deeply nested array initializers recurse through a path (ParseArrayInitializer → ParseExpression → ParseArrayInitializer) that is not covered by the ExpressionDepthLimit counter added in the fix for GHSA-wgh7-7m3c-fx25. An attacker who can supply untrusted input to Template.Parse can trigger an uncatchable StackOverflowException that immediately terminates the process, even with the default ExpressionDepthLimit enabled.

### CVE-2026-74789

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-16T14:16:56.917 |

Scriban before 7.0.0 (affected <= 6.6.0) applies its LoopLimit constraint only to script loop statements and not to expensive iteration performed inside built-in operators and functions. As a result, a single expression such as {{ 1..1000000 | array.size }} — or a memory-amplification expression such as {{ 'A' * 200000000 }} — can force large CPU or memory consumption even when LoopLimit is configured to a very small value, resulting in denial of service. Applications that render attacker-controlled templates and rely on LoopLimit for safe execution are affected.

### CVE-2026-74788

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-16T14:16:56.787 |

Scriban before 7.0.0 (affected versions <= 6.6.0) contains an uncontrolled memory allocation vulnerability in the string.pad_left and string.pad_right template functions, which perform no validation on the width parameter before delegating to .NET's String.PadLeft/PadRight. When an application exposes Scriban to untrusted template input, an attacker can supply an arbitrarily large width value (e.g., 500,000,000) to trigger ~1GB memory allocations in a single call, resulting in OutOfMemoryException and denial of service. The TemplateContext.LimitToString limit does not prevent this because it is only enforced after the string has been fully allocated.

### CVE-2026-74787

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-16T14:16:56.653 |

Scriban before 7.0.0 contains an uncontrolled recursion vulnerability in the object.to_json builtin function that lacks depth limits and circular reference detection. Attackers can craft templates with self-referencing objects to trigger unbounded recursion, causing a StackOverflowException that fatally terminates the hosting .NET process.

### CVE-2026-74784

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-16T14:16:56.263 |

Scriban before 7.2.0 contains a denial of service vulnerability in the array.insert_at function that allocates unbounded null entries without respecting LoopLimit or LimitToString constraints. Attackers can supply a large index parameter to trigger OutOfMemoryException and crash the host process in under a second.

### CVE-2026-74783

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-16T14:16:56.133 |

Scriban versions 6.6.0 through 7.2.0 contain a non-enforcing ExpressionDepthLimit guard that fails to stop recursive descent parsing of deeply nested expressions. Attackers can supply templates with deeply nested parentheses, array initializers, object initializers, or unary operators to trigger an uncatchable StackOverflowException that immediately terminates the host process.

### CVE-2026-73062

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-16T14:16:55.903 |

Scriban versions 3.0.0 through 7.2.0 contain a denial of service vulnerability in the array multiplication operator that allocates memory without enforcing LoopLimit or overflow-safe arithmetic checks. Attackers can supply a large integer multiplier in a template to force multi-gigabyte memory allocations, causing resource exhaustion and availability degradation.

### CVE-2026-73060

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-16T14:16:55.640 |

Scriban versions from 3.0.0 through 7.2.5 contain a denial of service vulnerability in the ScriptRange.Multiply operator that bypasses LoopLimit when the left operand is a lazy sequence. Attackers can supply templates with array multiplication on lazy sequences to execute billions of uncharged iterations, pinning CPU cores and exhausting garbage collection resources even when LoopLimit is set to 1.

### CVE-2026-73057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-16T14:16:55.230 |

stoatchat before 0.15.0 fails to validate SVG viewBox dimensions in the proxy endpoint, allowing attackers to cause denial of service by memory exhaustion. Attackers can host malicious SVGs with extremely large width and height values and trigger concurrent requests to exhaust available memory across proxy replicas.

### CVE-2024-58375

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-08-16T14:16:53.627 |

OpenTofu versions 1.8.0 through 1.8.2 do not properly restrict sensitive variables and locals when users have opted into static evaluation of module sources, versions, and backend configurations. As a result, values marked as sensitive may be exposed through these configuration elements instead of producing an error. This is fixed in OpenTofu 1.8.3, which adds explicit errors to prevent the use of sensitive values in these contexts.

### CVE-2026-74767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-15T22:16:55.697 |

Pandora contains a denial-of-service vulnerability in its handling of DAA (Direct Access Archive) files. When extracting the internal ISO image from a DAA archive, compressed chunks were decompressed using zlib.decompress() without enforcing a limit on the resulting uncompressed data.


An attacker able to submit a crafted DAA file containing highly compressed data could cause Pandora to decompress a relatively small input into a very large amount of data in memory. Because the decompressed chunks are accumulated to construct the internal ISO image, this could result in excessive memory consumption and potentially CPU exhaustion, causing the extraction worker to become unresponsive, terminate, or affect the availability of the Pandora service.


The patch introduces bounded decompression using decompressobj().decompress() with max_extracted_filesize, verifies the cumulative size of decompressed chunks, and raises a dedicated ZipBomb exception when the configured limit is exceeded. Pandora then aborts extraction and reports the file as too large.

### CVE-2026-73054

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-15T22:16:55.290 |

SiYuan versions before v3.7.4 contain an authentication bypass vulnerability in the WebSocket endpoint caused by differential parsing of query parameters between authentication exemption and session quarantine checks. Unauthenticated attackers can craft a malicious WebSocket URI with duplicated query parameters to bypass access auth code validation and receive the live kernel event stream including document identifiers, titles, and operation logs.

### CVE-2026-73045

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-15T22:16:54.463 |

SiYuan before 3.7.4 contains an improper restriction of excessive authentication attempts vulnerability in the authFilePublishAccess endpoint that allows unauthenticated attackers to brute-force per-notebook publish passwords. Attackers can submit unbounded password guesses without rate limiting or CAPTCHA to gain access to password-protected published notebooks.

### CVE-2026-73047

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-15T22:16:54.737 |

siyuan versions <= 3.7.3 (fixed in v3.7.4) contain a server-side template injection vulnerability in the attribute-view Template calculation feature (introduced in v3.7.0-beta.1). The feature's template engine uses Sprig's unmodified function map, which still exposes the env, expandenv, and getHostByName functions that were removed elsewhere for CVE-2024-55660. A local, unauthenticated attacker (the kernel binds to 127.0.0.1 by default with no per-UID access control) can inject a malicious Template calculation formula to read environment variables belonging to the account running siyuan — including from a separate, unprivileged OS account — and to perform DNS lookups from the server's network position.

### CVE-2026-19901

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-08-15T18:16:24.830 |

A security flaw has been discovered in LB-LINK X-PRO 1.0.22-20231206. This affects an unknown function of the file /etc/config/easycwmp. The manipulation results in hard-coded credentials. It is possible to launch the attack remotely. Attacks of this nature are highly complex. The exploitability is reported as difficult. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-19900

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-08-15T17:16:24.730 |

A vulnerability was identified in LB-LINK X-PRO 1.0.22-20231206. The impacted element is an unknown function of the file /etc/shadow. The manipulation leads to hard-coded credentials. It is possible to initiate the attack remotely. A high degree of complexity is needed for the attack. The exploitability is regarded as difficult. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-17087

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-16T07:16:30.423 |

The WP Travel Engine – Tour Booking Plugin – Tour Operator Software plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 6.8.4. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to view private booking billing details — including the victim customer's first name, last name, email address, street address, city, and phone number — rendered as default values in checkout form fields by binding an arbitrary booking ID to the attacker's session. The only access control on the endpoint is a frontend nonce that is publicly emitted to all visitors via the wteL10n global on trip pages, meaning it provides CSRF protection only and does not restrict unauthenticated access.

### CVE-2026-2497

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-16T07:16:31.030 |

The Gallery by BestWebSoft plugin for WordPress is vulnerable to SQL Injection via the '_gallery_order_{post_id}' parameter array keys in all versions up to, and including, 4.7.9. This is due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. The `gllr_save_postdata()` function stores unsanitized array keys from `$_POST` directly into post meta, which are later used in SQL queries without prepared statements. This makes it possible for authenticated attackers, with Editor-level access and above, to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-13424

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-16T07:16:30.300 |

The Online Scheduling and Appointment Booking System – Bookly plugin for WordPress is vulnerable to Stored Cross-Site Scripting via bookly_speed_up_update_addons AJAX action in all versions up to, and including, 27.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injection point is the bookly_speed_up_update_addons AJAX action, which is registered as wp_ajax_nopriv_* and therefore reachable without authentication; the payload is stored verbatim in the bookly_log.details column when a request is submitted without a valid signature, and executes when an administrator later views the Diagnostics → Logs page.

### CVE-2026-10734

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-16T07:16:30.043 |

The Infility Global plugin for WordPress is vulnerable to Stored Cross-Site Scripting via /cf7_record Log Endpoint in all versions up to, and including, 2.15.21 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The /cf7_records viewer is accessible to any authenticated user including those with Subscriber-level access, meaning the injected payload executes for any logged-in user who visits the records page.

### CVE-2026-17581

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-16T06:16:51.440 |

The WCPOS – Point of Sale (POS) plugin for WooCommerce plugin for WordPress is vulnerable to Code Injection via the 'thermal' Template Engine in all versions up to, and including, 1.9.14 due to the Receipt_Renderer_Factory dispatching templates with the 'thermal' engine to the Legacy_Php_Renderer instead of a safe thermal-specific renderer. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to inject arbitrary PHP code into a template post that is subsequently written to a temporary file and executed via PHP's include(), resulting in remote code execution on the server. This requires the attacker to have Shop Manager-level access or above, as the template save path enforces a wcpos_template_settings nonce and the manage_woocommerce_pos capability check.

### CVE-2026-15002

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-16T05:16:46.620 |

The Platnosci Online Blue Media (Autopay) plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 5.0.0 via the 'bm_woocommerce_css_editor_content' POST parameter. This is due to the Css_Editor::handle_save() method being wired to the WordPress 'init' hook by Settings_Manager::init_once() with no capability check, no nonce verification, and no sanitization on the input — the raw $_POST value is written to the 'woocommerce_bluemedia_settings' option via update_option(), then later echoed directly inside a <style> block on the WooCommerce checkout page by Css_Frontend::print_to_wp_head() with no output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page (the checkout page).

### CVE-2026-74786

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-16T14:16:56.523 |

Scriban before 7.0.0 (affected versions <= 6.6.0) contains a denial-of-service vulnerability in which the LimitToString safety limit (default 1MB) can be bypassed because ObjectToString resets the per-call length counter (_currentToStringLength) on every top-level call and StringBuilderOutput enforces no cumulative output-size limit. An attacker who can supply a template can render a near-limit string repeatedly in a loop, allocating approximately 1GB of memory and causing an out-of-memory condition that crashes the host application.

### CVE-2026-74785

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-16T14:16:56.390 |

Scriban before 7.0.0 contains three distinct denial-of-service vulnerabilities in expression evaluation that bypass existing safety controls through unbounded string multiplication, uncontrolled BigInteger shift operations, and LoopLimit bypass via range enumeration in builtin functions. Attackers who can supply templates can cause out-of-memory exceptions or CPU exhaustion, typically terminating the entire host process.

### CVE-2026-73059

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-16T14:16:55.507 |

stoatchat before 0.15.0 contains a permission bypass vulnerability in the message_fetch route that checks only ViewChannel permission instead of requiring ReadMessageHistory. Attackers with ViewChannel access but ReadMessageHistory denied can retrieve individual message content by ID, bypassing the intended history restriction enforced by bulk read routes.

### CVE-2026-74796

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-16T14:16:57.727 |

OpenTofu before 1.11.7 fails to validate existing symlinks in the provider cache directory during initialization. Attackers can place a malicious symlink in a trusted working directory to cause tofu init to write provider package contents to arbitrary filesystem locations outside the working tree.
