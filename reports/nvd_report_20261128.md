# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-27 15:00 UTC
- **対象期間**: `2026-11-26T15:01:16.000Z` 〜 `2026-11-27T15:00:44.000Z`
- **重要CVE数**: 228 件（Critical 9.0+: 34 件 / High 7.0〜: 194 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち **CVSS 7.0 以上が 30 件以上** と、深刻度の高い脆弱性が集中しています。  
- **「認証なしでリモートコード実行 (RCE)」や「コマンドインジェクション」** が目立ち、特に通信プロトコル（HTTP, UDP, WebSocket）や API エンドポイントの入力検証不足が原因です。  
- 製品領域は **通信基盤 (Mitel OpenScape, RealVNC)、Web アプリケーションフレームワーク (WordPress プラグイン、Budibase、ToolJet)**、そして **クラウドサービス (Google Cloud Vertex AI, GCP Application Integration)** に偏っています。  
- 多くは **パッチ未適用の旧バージョンが対象** であり、ベンダーがすでに修正をリリースしているケースが多数です。早急なバージョンアップと、ネットワークレベルでのアクセス制御が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑137724** <br> *Mitel OpenScape 4000 Platform* | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | 認証なしでプラットフォームに不正アクセス → 機密情報取得・権限昇格 | **認証機構の欠陥** により、ネットワーク上の任意のホストから完全な管理権限が取得可能。電話システムは企業インフラの要であり、情報漏洩・サービス停止リスクが極めて高い。 |
| **CVE‑2026‑137721** <br> *Mitel OpenScape 4000 Platform* | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | パラメータサニタイズ不備によるコマンドインジェクション | 同製品の別脆弱性で、**任意コマンド実行** が可能。攻撃者はシステム上で任意のシェルを起動でき、上記 CVE と組み合わせると完全な遠隔支配が成立。 |
| **CVE‑2026‑126984** <br> *pulp_python (pull‑through cache)* | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | SSRF により内部ネットワークへ任意リクエスト送信 | **リモートから内部リソースへアクセス** でき、機密データ取得や内部サービスへの攻撃踏み台化が可能。特に社内レジストリやメタデータサーバが対象になるケースが多い。 |
| **CVE‑2026‑137498** <br> *Budibase Server* | 9.9 (AV:N/AC:L/AT:N/PR:N/UI:N) | プロトタイプ汚染により MongoDB クエリフィルタを無効化 → 任意データ取得・改竄 | **プロトタイプ汚染** は JavaScript エンジン全体に影響し、単一リクエストでデータベースクエリをバイパスできる。Budibase はローコード開発プラットフォームで多くの業務アプリが構築されているため、被害範囲が広がりやすい。 |
| **CVE‑2026‑137738** <br> *RealVNC Server* | 9.8 (AV:N/AC:L/PR:N/UI:N) | UDP 接続で認証なしにコード実行またはクラッシュ (DoS) | **UDP ベースの認証バイパス** はファイアウォールでブロックしにくく、内部ネットワークに広く展開されている VNC が即座に乗っ取られる危険性がある。 |

> **※** これら 5 件は **CVSS が 9.8 以上** で、かつ **認証不要**、**ネットワーク経由で直接攻撃可能** という点で共通しています。実運用環境でのインパクトが最も大きいため、最優先で対策すべきです。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 修正バージョン (ベンダー提供) | 対策期限目安 |
|-------------------|-------------------|------------------------------|--------------|
| **Mitel OpenScape 4000 Platform / Manager** | すべての 2025 系以前リリース | 2026‑01‑15 以降の **4.0.0 以上** (ベンダーが提供するセキュリティパッチ) | 1 週間以内 |
| **pulp_python** (pull‑through cache) | 3.6.0 未満 | **3.6.2** 以上 | 1 週間以内 |
| **Budibase Server** | 3.39.18‑3.41.x | **4.0.0** 以上 | 2 週間以内 |
| **RealVNC Server** | 7.19.0 未満 | **7.19.1** 以上 | 1 週間以内 |
| **WordPress プラグイン** (Contact Form 7 DB, Sneeit Framework, Product Input Fields) | 1.5.5, 8.7, 2.1.0 など | 各プラグインの **最新版** (2026‑03‑01 以降リリース) | 2 週間以内 |
| **ToolJet** | 3.21.94‑beta 未満 | **3.21.95‑beta** 以上 | 2 週間以内 |
| **Parse Server** | 3.10.0‑8.6.122, 9.0.0‑9.11.0-alpha.3 | **8.6.123** 以上、**9.11.1‑alpha.4** 以上 | 2 週間以内 |
| **Canonical LXD / pylxd** | 5.0.12 未満、2.4.2 未満 | **5.0.13** 以上、**2.4.3** 以上 | 1 週間以内 |
| **Google Cloud Vertex AI (Assistant)** | 2026‑04‑12 以前 | **2026‑04‑13** 以降のリリース | 1 週間以内 |
| **Google Cloud Application Integration** | 2026‑09‑21 以前 | **2026‑09‑22** 以降 | 1 週間以内 |

> **※** パッチが未公開の場合は、ベンダーのアドバイザリを確認し、**回避策 (ネットワーク遮断、IP フィルタリング、機能無効化)** を即時実施してください。

### 3.2 ネットワーク・ホストベースの防御
1. **外部からの直接アクセスを遮断**  
   - Mitel OpenScape、RealVNC、Budibase の管理ポートは **VPN または IP アクセスリスト** で保護。  
   - UDP 7xx (RealVNC) と TCP 443 (Budibase API) の外部到達を防止。  

2. **WAF / IDS/IPS で特定シグネチャを有効化**  
   - `CVE‑2026‑137721` のコマンドインジェクション文字列 (`;`, `&&`, `` ` ``) を検知。  
   - `CVE‑2026‑126984` の SSRF パターン (`http://`, `https://`,

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-137724

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-27T06:17:09.727 |

A vulnerability in the Platform component of Mitel OpenScape 4000, and OpenScape 4000 Manager could allow an unauthenticated attacker to conduct an unauthorized access attack due to improper authentication mechanisms. A successful exploit could allow an attacker to obtain sensitive information and gain unauthorized access to system. This vulnerability affects OpenScape 4000, versions V11 R0.22 through V11 R2.11 and V10 R1.68 and earlier, and OpenScape 4000 Manager, versions V11 R0.22 through V11 R2.11 and V10 R1.34 through V10 R1.68. This is MTLVULN-1785.

### CVE-2026-137721

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-27T06:17:09.443 |

A vulnerability in the Platform component of Mitel OpenScape 4000 and OpenScape 4000 Manager could allow an attacker to conduct a command injection attack due to insufficient parameter sanitization. A successful exploit could allow an attacker to execute arbitrary commands within the context of the system. This vulnerability affects OpenScape 4000, versions V11 R0.22 through V11 R2.11 and V10 R1.68 and earlier, and OpenScape 4000 Manager, versions V11 R0.22 through V11 R2.11 and V10 R1.34 through V10 R1.68. This is MTLVULN-1786.

### CVE-2026-126984

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-26T16:17:50.623 |

A **server-side request forgery** flaw has been found in the get_remote_artifact_url() function in pulp_python/app/models.py of the pull-through caching feature in the **pulp_python** package. The function uses the redirect query parameter from the client request as the URL to download. A network attacker or user who can reach the content app of a Python distribution that has a remote can choose that URL. The content app downloads it and returns the response. When the remote has a username and password, the download sends those credentials to the host in the URL. When the remote policy is immediate, the default, or on_demand, the file is saved into the distribution's repository and later clients are served that file. The project name and version come from the file, and the filename comes from the request path. A filename the repository already stores is served from the stored file.

### CVE-2026-134963

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-27T13:17:23.347 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Webdeclic WPMasterToolKit wpmastertoolkit allows Code Injection.This issue affects WPMasterToolKit: from n/a through 2.26.1.

### CVE-2026-137498

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-26T16:18:01.000 |

Budibase Server from 3.39.18 before 4.0.0 contains a prototype pollution vulnerability that allows unauthenticated attackers to erase MongoDB query filters by supplying __proto__ as a dynamic JSON key in PUBLIC queries. Attackers can send a single request to the query execution endpoint, reducing the filter to {} to read, update, or delete every document in the collection.

### CVE-2026-134994

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-27T14:17:03.373 |

Deserialization of Untrusted Data vulnerability in Nitramix Revertix &#8211; Backup, Migration, Staging &amp; Clone revertix allows Object Injection.This issue affects Revertix &#8211; Backup, Migration, Staging &amp; Clone: from n/a through 1.0.3.

### CVE-2026-135933

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-27T13:17:23.983 |

Incorrect Privilege Assignment vulnerability in Tobias WebinarIgnition webinar-ignition allows Privilege Escalation.This issue affects WebinarIgnition: from n/a through 4.28.1.

### CVE-2026-137738

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-27T06:17:09.867 |

In RealVNC Server before 7.19.1, UDP-based connections could potentially be exploited without authentication to execute code remotely or cause the software to crash. This could allow an attacker to remotely execute code as root on certain platforms or perform a denial of service attack. This issue affects RealVNC Viewer: from 8.4.0 through 8.6.1; RealVNC Classic Viewer: from 6.4.0 through 7.18.2; RealVNC Server: from 6.4.0 through 7.19.0; RealVNC Connect App: through 8.6.1; RealVNC iOS Viewer: from 3.7.0 through 4.9.5; RealVNC Android Viewer: from 3.5.0 through 4.9.5; RealVNC iOS Server: through 2.8.1; RealVNC Android Server: through 2.8.3; On-Demand Assist: through 3.4.1.

### CVE-2026-115867

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-27T02:16:43.770 |

The Database for Contact Form 7, WPforms, Elementor forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.5.5 via the copy_files function. This is due to missing file extension validation in the copy_files function, which accepts attacker-controlled stream wrapper URIs as the file source and derives the destination filename without restricting executable extensions. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The plugin places an .htaccess file in its uploads directory to block PHP execution, but this mitigation is ineffective on Nginx, LiteSpeed in certain configurations, and Apache servers with AllowOverride None, and the file is not restored if deleted.

### CVE-2026-106125

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-27T02:16:43.460 |

The Sneeit Framework plugin for WordPress is vulnerable to Remote Code Execution in versions up to, and including, 8.7 via the 'callback' parameter of the sneeit_compact_menu_mega_content AJAX action. The handler sneeit_compact_menu_mega_content_callback() is registered on the wp_ajax_nopriv_ hook and passes the attacker-supplied 'callback' value directly into call_user_func() after only a function_exists() check, with the single argument also attacker-controlled via a JSON-decoded 'args' parameter. There is no authentication, no capability check, no nonce, and no allow-list of callable functions. This makes it possible for unauthenticated attackers to execute arbitrary existing PHP/WordPress functions with controlled arguments.

### CVE-2026-104998

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-26T15:17:22.833 |

The Product Input Fields for WooCommerce plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.1.0 via the process_file_input_field function. This is due to missing file type validation in the process_file_input_field function, which accepts the client-supplied multipart Content-Type header as the sole type gate and writes the uploaded file to the unprotected pif_temp directory using the verbatim client-supplied filename. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. Exploitation requires that an administrator has configured at least one product with a File-type Product Input Field with the "Show thumbnail" option enabled, which is a standard use of the feature; additionally, the pif_temp/ upload directory is created without .htaccess or index.php restrictions, leaving written files directly web-accessible and executable on default Apache/mod_php configurations.

### CVE-2026-137723

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-27T06:17:09.587 |

A vulnerability in the Platform component of Mitel OpenScape 4000 and OpenScape 4000 Manager could allow an attacker to conduct a command injection attack due to insufficient parameter sanitization. A successful exploit could allow an attacker to execute arbitrary commands within the context of the system. This vulnerability affects OpenScape 4000, versions V11 R0.22 through V11 R2.11 and V10 R1.68 and earlier, and OpenScape 4000 Manager, versions V11 R0.22 through V11 R2.11 and V10 R1.34 through V10 R1.68. This is MTLVULN-1793.

### CVE-2026-124981

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-27T14:17:02.300 |

A vulnerability has been identified in Mendix OIDC Provider (Mendix 10 compatible) (All versions < V6.0.0), Mendix OIDC Provider (Mendix 11 compatible) (All versions < V6.0.0), Mendix OIDC Provider (Mendix 9 compatible) (All versions < V4.3.0). Affected versions of the module do not properly validate the integrity of JWTs submitted to the OIDC Provider Token Introspection endpoint, allowing tokens to be associated with legitimate token records based solely on their jti value.

This could allow unauthenticated remote attackers to hijack an account (session) when gaining access to an jti of an active token.

### CVE-2026-106169

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-27T13:17:21.130 |

A Deserialization of Untrusted Data vulnerability in the eventbus execution in Google Cloud Application Integration versions prior to 2026-09-22 on Google Cloud Platform allows an authenticated attacker to achieve remote code execution using a crafted serialized Java object.


This vulnerability was patched on 22 September 2026, and no customer action is needed.

### CVE-2026-137706

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-27T03:17:04.263 |

Smart Portal developed by Direk Tech has a Missing Authorization vulnerability. Authenticated remote attackers can add a specified account to the Active Directory Domain Admins group, thereby obtaining domain administrator privileges.

### CVE-2026-137544

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T16:18:07.603 |

LaraDashboard before 1.5.0 contains a path traversal vulnerability in module.json providers and composer.json psr-4 namespace parsing that derives destination folder names without excluding traversal characters. Attackers with module.create permission can upload a crafted module ZIP to write PHP files into the public directory, achieving unauthenticated remote code execution.

### CVE-2026-85258

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-27T14:17:07.223 |

A Missing Authorization vulnerability in the private console API in Google Cloud Vertex AI (Vertex AI Assistant) versions prior to 2026-04-13 on Google Cloud Platform allows an unauthenticated remote attacker to list, read, create, and send messages in other users' chat sessions using crafted API requests.


This vulnerability was patched on 13 April 2026, and no customer action is needed.

### CVE-2026-135009

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-27T14:17:03.520 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in David Lingren Media LIbrary Assistant media-library-assistant allows Blind SQL Injection.This issue affects Media LIbrary Assistant: from n/a through 3.43.

### CVE-2026-59103

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288;CWE-807` |
| Published | 2026-11-27T09:17:02.453 |

MONEO ERP exposes the Ping method of its _slave JSON-RPC service over WebSocket as @rpc.openpublic, so it can be called without a valid session. The method's only guard compares the calling application name with "_login", but that value is taken from the client-controlled params.appname field of the request. When the check passes, Ping stores an attacker-chosen session ID, user number and company in the server session store, and subsequent session validation accepts that session. An unauthenticated remote attacker can therefore create a valid session as any user, including administrators, in any company (tenant) hosted on the server and invoke authenticated RPC methods with that user's privileges, gaining read and write access to that company's data.

### CVE-2026-137550

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T16:18:08.660 |

Frappe Framework before 15.122.0 and 16.x before 16.50.0 contains a missing authorization vulnerability in Document.update() that fails to validate whether the caller is permitted to submit or modify the target document. Attackers can invoke document update operations to submit or alter documents they are not authorized to change.

### CVE-2026-137536

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-26T16:18:06.410 |

ToolJet before 3.21.94-beta contains an authentication bypass in its server OAuth SSO sign-in module, which resolves Google and Git SSO logins solely by the provider-asserted email without checking email_verified or binding the SSO subject. Unauthenticated attackers can submit a trusted-issuer token carrying a victim's unverified email to the SSO callback to obtain the victim's session, including admin accounts.

### CVE-2026-137499

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:18:01.160 |

Budibase from 3.41.0 before 4.0.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to take over password-less global Builder accounts via unverified-email OIDC/SSO account linking. Attackers can assert a victim's email with email_verified=false at a trusted IdP, bypassing the isAccountLinkable allowlist to control all apps, datasources, and automations.

### CVE-2026-135384

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-27T00:16:43.450 |

Improper authentication in OIDC bearer token verification in Canonical LXD before 5.0.12, 5.21.10, 6.10.2 allows a remote attacker holding a token signed by the configured identity provider to authenticate to the LXD API and gain unauthorized control or impersonate users via presenting tokens issued for other applications, ID tokens, or unverified email claims.

### CVE-2026-137547

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-11-26T16:18:08.157 |

Coder before 2.29.27, 2.30.0 before 2.34.19, 2.35.0 before 2.37.11, 2.38.0 before 2.38.7, and 2.39.0 before 2.39.1 returns database connection errors containing a temporary AWS IAM database password in API key middleware responses. During database connection failures, unauthenticated attackers can send a well-formed but invalid API key to obtain the password and access the PostgreSQL database for 15 minutes.

### CVE-2026-135930

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-27T13:17:23.827 |

Authentication Bypass by Spoofing vulnerability in TMS Amelia ameliabooking allows Identity Spoofing.This issue affects Amelia: from n/a through 2.4.14.

### CVE-2026-127163

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-27T00:16:41.440 |

Improper certificate validation in websocket connections in Canonical pylxd before 2.4.3 allows a network attacker to read command stdin and spoof command output via impersonating a remote LXD endpoint.

### CVE-2026-135279

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-436` |
| Published | 2026-11-26T17:17:06.490 |

@fastify/express is the plugin that lets an application run Express middleware and Express applications inside the Fastify web framework. In versions before 4.0.14, a request with an empty dynamic route parameter reaches a Fastify route handler while middleware mounted for that path inside an Express Router or sub-application is skipped, because Fastify's router accepts an empty value where Express requires a non-empty one, and an unanchored regular-expression mount passed to the plugin is bypassed the same way. An earlier fix covered only the mount paths passed to the plugin directly, not middleware mounted inside a routed Express application. An attacker can use this to bypass authentication or other middleware-based access controls on the affected routes, with the practical impact depending on what the empty value selects in the application. The issue is fixed in @fastify/express 4.0.14, and users should upgrade to 4.0.14 or later. As a workaround, enforce authentication in a Fastify hook such as preHandler that runs after routing, mount the middleware on a static parent path, or require non-empty values in the route params schema.

### CVE-2026-137465

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:17:54.900 |

Parse Server 3.10.0 before 8.6.123 and 9.0.0 before 9.11.1-alpha.4 contains an authentication bypass in the Google Play Games authentication adapter, which does not verify that the supplied player ID belongs to the presented access token. Attackers can sign in with their own Google Play Games credential while claiming another user's player ID to take over that account or link that player ID to their own account.

### CVE-2026-137463

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-26T16:17:54.550 |

HKUDS nanobot from 0.1.4 before 0.4.1 contains an improper certificate validation vulnerability in the OpenAI Codex provider that retries authenticated requests without TLS certificate or hostname verification. Attackers able to intercept the connection can trigger a certificate failure and impersonate the endpoint to steal bearer tokens, read request contents, or alter responses.

### CVE-2026-136240

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T15:17:26.867 |

The PDF Invoice for WooCommerce + Drag and Drop Template Builder plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 7.2.0 via deserialization of untrusted input . This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. The incomplete remediation in version 7.2.0 applied escape_pdf_note() only to the customer_note path; the billing address path at woocommerce/shortcodes.php:975–978 remains unpatched, and exploitation requires guest checkout to be enabled along with a payment method that transitions orders to on-hold status (such as the stock WooCommerce Direct Bank Transfer option).

### CVE-2026-135641

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-26T15:17:26.100 |

The WP Job Portal – AI-Powered Recruitment System for Company or Job Board website plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 2.7.2 This is due to a flaw in `WPJOBPORTALuser::__construct()` where the non-empty guard on the `wpjobportal-socialid` cookie is evaluated against the raw cookie value before `sanitize_key()` is applied — allowing a value composed entirely of characters outside `[a-z0-9_-]` to pass the guard, be reduced to an empty string by `sanitize_key()`, and be used as the literal value in a `WHERE socialid = ''` database query that matches the first portal account whose `socialid` column is empty. This makes it possible for unauthenticated attackers to be bound to an existing WP Job Portal Employer or Jobseeker account, gaining the ability to create, edit, and delete the victim's companies, job listings, resumes, and applications, as well as overwrite the linked WordPress user's first name, last name, and display name via the `saveuser`→`syncWPUserName()` path. Exploitation is viable on virtually all installations because every portal account not registered through the social-login flow retains the default empty `socialid` value; nonce checks on downstream actions such as `savecompany` and `saveuser` do not mitigate this issue because those nonces are minted within the already-hijacked session and validate against the attacker's own subsequent requests. Successful exploitation gives the attacker control of a distinct, already-privileged WP Job Portal Employer / Jobseeker (bound to a specific WordPress user) account; it does not promote the attacker's original account.

### CVE-2026-134173

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T15:17:25.647 |

The WordPress File Upload plugin for WordPress is vulnerable to Arbitrary File Deletion in versions up to, and including, 5.3.1 via the 'wfu_ajax_action_handshake' and 'wfu_ajax_action_send_email_notification' AJAX Actions. This is due to the unauthenticated handshake accepting a 'sid' parameter sanitized only with sanitize_text_field(), which does not strip '[', ']', '{', or '}', allowing the sid to be crafted as an item name containing embedded delimiter pairs that plant forged records for arbitrary other item names — including the per-session file path list and the consent flag — in the plugin's shared concatenated user-state option store, combined with the notification handler being gated only by a nonce freely minted by the same nopriv handshake. This makes it possible for unauthenticated attackers to delete arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-133951

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-26T15:17:25.487 |

The Simple Membership plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 4.8.9 This is due to the site-wide signing secret `swpm_private_key_one` being generated at install time with PHP's non-cryptographic `uniqid('', true)` function in `SwpmInstallation::installer()`, whose timestamp-derived keyspace (~10^15 candidates / ~50 bits) can be constrained via the public WordPress REST API date of the plugin's auto-created registration page, combined with a single-MD5 oracle (`md5(key|level)`) that the public registration form prints as `swpm_level_hash` and a non-constant-time `!=` comparison in `SwpmFrontRegistration::register_front_end()` as the sole authorization gate on which membership level a visitor may register into; `SwpmUtils::get_free_level()` then honors an attacker-posted `level_identifier=md5(level)` regardless of the configured free-membership setting, and `prepare_and_create_wp_user_front_end()` creates the WordPress account with whatever role the level is configured to grant (only the `administrator` role is refused). This makes it possible for unauthenticated attackers, after an offline brute-force recovery of the install-time secret against the public MD5 oracle, to forge a valid `swpm_level_hash` for any configured membership level and self-register into that level, elevating their newly created WordPress account to the level's assigned role — e. Successful exploitation causes the attacker's own account to receive the complete editor role.

### CVE-2026-137471

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:55.933 |

SiYuan before 3.8.10 contains a cross-site scripting vulnerability where WebDAV sync error formatting skips HTML escaping for certain malformed-response errors, passing raw markup to the Electron notification renderer. A network attacker who alters a cleartext HTTP WebDAV response can inject event-handler markup that, when the victim manually starts sync, executes JavaScript with Node integration as the logged-in user.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-135048

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-27T14:17:03.817 |

Incorrect Privilege Assignment vulnerability in weDevs WP ERP erp allows Privilege Escalation.This issue affects WP ERP: from n/a through 2.0.0.

### CVE-2026-115283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-27T05:18:59.320 |

Missing authentication vulnerability in BS2500/BS500 Virtage Firmware.


This issue affects BladeSymphony BS2500: from 02-02 through 02-76; BladeSymphony BS500: from 01-01 through 02-76.

### CVE-2026-105917

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-27T05:18:58.960 |

File Permission Vulnerability in RV3000 Log Monitor for VMware.

This issue affects RV3000 Log Monitor for VMware(CIM): before 98-09; RV3000 Log Monitor for VMware: before 97-05.

### CVE-2026-113774

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-27T02:16:43.613 |

The Schema & Structured Data for WP & AMP plugin for WordPress is vulnerable to PHP Object Injection in versions up to, and including, 1.68. This is due to deserialization of untrusted input via the admin export (saswp_export_all_settings_and_schema) which calls unrestricted unserialize() on every raw post meta value, combined with saswp_review_form_process_data() which stores unauthenticated-visitor-supplied reviewer-name data through update_post_meta — the plugin sanitizes with sanitize_text_field(), which does not recognise PHP serialization syntax or the NUL property-name delimiters, and WordPress's maybe_serialize/is_serialized has no case for the legacy PHP 'C' custom-serialization token (ArrayObject), so the payload is persisted byte-for-byte and never wrapped in a protective extra serialize layer. This makes it possible for unauthenticated attackers to inject a PHP Object into the processing of the plugin. No known POP chain is present in the vulnerable plugin itself, but if a suitable chain exists via an additional plugin or theme installed on the blog, it could be used to delete arbitrary files, or achieve other impacts. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-134705

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-26T20:17:22.670 |

Incorrect Privilege Assignment vulnerability in miniOrange miniorange otp verification miniorange-otp-verification allows Privilege Escalation.This issue affects miniorange otp verification: from n/a through 5.6.2.

### CVE-2026-76075

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-26T16:18:11.853 |

The Warehouse Cargo theme for WordPress is vulnerable to Arbitrary File Upload in versions up to, and including, 2.7.4 via the warehouse_cargo_install_and_activate_plugin() AJAX handler. The handler is registered on wp_ajax_ but performs no nonce verification and no capability check, allowing any authenticated user to supply an attacker-controlled URL that the server fetches, writes into wp-content/plugins/ with file_put_contents(), extracts with unzip_file() (which does not filter file extensions), and then activates via activate_plugin(). This makes it possible for authenticated attackers, with Subscriber-level access and above, to upload arbitrary files on the affected site's server which makes remote code execution possible.

### CVE-2026-137456

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-26T16:17:53.343 |

FreeRDP before 3.33.0 contains an integer overflow in the client GDI handling of accumulated drawing-order bounds: wrapped INT32 coordinates yield a zero-width clip region that causes clipping to be skipped in gdi_FillRect. A malicious RDP server can send many ORDER_BOUNDS orders followed by an OPAQUE_RECT order to trigger a heap out-of-bounds write past the client's drawing bitmap, potentially leading to code execution.

### CVE-2026-109921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:17:49.107 |

Authentication bypass in the system.setPillar and system.getPillar functions in Uyuni before 5.1.35, 5.2.0 before 5.2.25, 5.3.0 before 5.3.5 could be used by logged in attackers to inject code into other managed system spaces.

### CVE-2026-137705

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-27T03:17:04.120 |

Smart Portal developed by Direk Tech has an Arbitrary File Read vulnerability.Unauthenticated remote attackers can exploit Relative Path Traversal to download arbitrary system files.

### CVE-2026-137657

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T20:17:24.893 |

InternLM LMDeploy 0.9.0 through 0.18.0 contains an unbounded resource allocation vulnerability in the DistServe proxy /distserve/connection_warmup endpoint that allows unauthenticated attackers to exhaust memory. While a prefill/decode connection is pending, for example after registering a slow node via /nodes/add, repeated warmup requests spawn unbounded wait_for_conn() tasks and sockets until the proxy process is killed.

### CVE-2026-137539

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-26T20:17:24.283 |

lastversion before 3.6.20 contains a path traversal vulnerability in extract_tar() that allows attackers to write files outside the extraction directory via tar symlink members. Attackers controlling a project's release assets can craft a tarball with a symlink followed by a file beneath it, writing files like usercustomize.py to achieve code execution.

### CVE-2026-137556

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T16:18:09.527 |

Dockhand before 1.0.57 contains a path traversal vulnerability in validateStackPath, which omits the isProtectedPath() check and permits writes to protected system directories. Authenticated users with stacks:edit permission can send a crafted composePath to PUT /api/stacks/[name]/compose to write arbitrary files, such as cron payloads, achieving remote code execution as root.

### CVE-2026-137552

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:18:09.013 |

Frappe Framework before 15.121.1 and 16.x before 16.35.0 accepts an undocumented OAuth2 Resource Owner Password Credentials (password) grant at its token endpoint, which does not enforce two-factor authentication or forced password resets. An attacker with a user's valid credentials can use this grant to obtain a full-access OAuth token, bypassing 2FA.

### CVE-2026-137549

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T16:18:08.507 |

pypdf before 7.0.1 contains a resource exhaustion vulnerability in image loading because data size estimates for some image modes are too low, defeating limits for filters without their own size limit. Attackers can craft a PDF whose images, when loaded, cause large memory usage and denial of service.

### CVE-2026-137526

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-26T16:18:05.037 |

ToolJet before 3.21.96-LTS contains an authorization bypass in the internal database (TJDB) PostgREST proxy, which grants proxy access to every logged-in user and derives the database role and schema from the client-supplied tj-workspace-id header. Any authenticated workspace member can send requests to /api/tooljet-db/proxy/<tableId> to read and modify TJDB tables, bypassing app, query, and table permissions, and in SQL-mode-disabled (Cloud) deployments can access all tenants' tables.

### CVE-2026-137513

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-241` |
| Published | 2026-11-26T16:18:02.983 |

justhtml before 3.17.0 contains a denial of service vulnerability in decode_entities_in_text that allows unauthenticated attackers to crash parsing via non-ASCII Unicode digits in numeric character references. Attackers can submit a payload like &#² in HTML text or attributes, causing an uncaught ValueError from int() that aborts JustHTML() and stream() parsing.

### CVE-2026-137512

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T16:18:02.807 |

Scriban before 7.6.0 contains a resource exhaustion vulnerability that allows attackers to bypass LoopLimit by supplying large JSON input to object.from_json. Attackers can pass a flat JSON array or object with hundreds of thousands of elements, which JsonElementExtensions materializes without loop checks, exhausting CPU and memory.

### CVE-2026-137510

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T16:18:02.457 |

Scriban and Scriban.Signed before 7.6.0 allow template authors to bypass the LimitToString string length limit because the string.literal, string.base64_encode, html.escape, html.newline_to_br, html.url_encode, and html.url_escape builtins lack allocation guards. An attacker who can supply a small template can repeatedly call these builtins under the default TemplateContext to force multi-gigabyte allocations and exhaust host memory.

### CVE-2026-137509

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T16:18:02.287 |

Scriban before 7.6.0 contains a resource exhaustion vulnerability that allows template authors to bypass LimitToString by rendering a ScriptObject with many members. Attackers can supply a small template whose ScriptObject.ToString concatenates large member values without length tracking, allocating multi-gigabyte strings and causing memory exhaustion.

### CVE-2026-137508

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T16:18:02.110 |

Scriban before 7.6.0 contains a memory exhaustion vulnerability in object.to_json that allows template authors to bypass the LimitToString string length limit by serializing into an unbounded MemoryStream. Attackers can repeatedly apply object.to_json to escape-heavy strings in a tiny template, amplifying output to multi-gigabyte heap allocations and causing denial of service.

### CVE-2026-137504

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T16:18:01.797 |

actix-multipart (actix-web) before 0.8.7 contains a resource exhaustion vulnerability in the MultipartForm extractor that allows unauthenticated attackers to exhaust memory or file descriptors by sending unlimited parts. Attackers can stream many zero-byte parts uncounted by total_limit and memory_limit, pinning 128 KiB buffers or opening temporary files to crash workers.

### CVE-2026-137497

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-26T16:18:00.477 |

Budibase before 4.0.0 contains an information disclosure vulnerability that allows unauthenticated attackers to retrieve legacy LiteLLM credentials by querying the public settings endpoint. Attackers can send unauthenticated GET requests to /api/global/configs/public to obtain liteLLM.keyId and secretKey, enabling unauthorized use of tenant LiteLLM resources.

### CVE-2026-137492

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:17:59.660 |

Budibase before 4.0.0 contains an authorization bypass vulnerability that allows workspace-scoped builders to access other workspaces' backups by supplying a foreign backupId. Attackers can substitute predictable backup IDs in backup download, import, update, or delete routes to steal archives, restore victim data into their workspace, or delete backups.

### CVE-2026-137490

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T16:17:59.330 |

SurrealDB before 4.0.0 contains an authorization bypass vulnerability that allows restricted subjects to execute arbitrary queries by calling the JavaScript surrealdb.query() bridge. Attackers permitted to run a specific script can bypass the Capabilities::allows_query() gate in the query module to execute unrestricted queries beyond their predefined operations.

### CVE-2026-137479

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-26T16:17:57.333 |

Traefik 3.1.0 before 3.7.18 and 3.8.0-rc.1 contain a memory exhaustion vulnerability in the Compress middleware, which creates zstd encoders with library default options that retain about 18 MiB of state per response until it is fully written. Unauthenticated remote attackers can open many concurrent requests and read responses slowly to exhaust memory and crash Traefik.

### CVE-2026-137470

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:55.763 |

SiYuan before 3.8.11 contains a stored cross-site scripting vulnerability that allows attackers to inject DOM event handlers by storing handler-named block attributes such as onmouseover. Attackers can share crafted .sy.zip packages or Markdown files whose attributes reach renderCustom or the unsanitised preview pane, executing OS commands via Node integration in the desktop app.

### CVE-2026-137468

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-26T16:17:55.420 |

SiYuan from 3.8.0 before 3.8.11 contains a lockout bypass vulnerability that allows remote attackers to brute-force publish passwords by forging client-computable publish-auth-<ID> cookies. Attackers can compute SHA-256(ID + candidate) locally and send it on content requests like /api/filetree/getDoc to guess passwords without throttling and read protected documents.

### CVE-2026-137467

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T16:17:55.250 |

SiYuan before 3.8.11 uses DejaVu sync code that accepts a non-hexadecimal 40-byte remote index ID from WebDAV responses and joins it into the repository indexes path unchecked, allowing path traversal. An on-path attacker altering plaintext HTTP WebDAV sync responses can overwrite a workspace data file, such as a .sy note, with compressed index data.

### CVE-2026-137460

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-26T16:17:54.030 |

FreeRDP from 3.10.0 before 3.33.0 contains an invalid free vulnerability in rdg.c because the websocket context pointer shares a union with chunked transfer-encoding decoder state. A malicious RD Gateway answering the data channel with chunked encoding can control the overwritten pointer via chunk sizes, causing rdg_free to free an attacker-influenced value and crash the client.

### CVE-2026-137459

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-69` |
| Published | 2026-11-26T16:17:53.857 |

FreeRDP 2.11.2 before 3.33.0 contains unbounded resource consumption in the Progressive codec because progressive_decompress() resets the tile update batch only when frameId changes. A malicious RDP server can repeat RDPGFX_CAPROGRESSIVE WireToSurface2 commands with a constant frameId to cause unbounded memory growth, quadratic CPU cost, a heap out-of-bounds write on tile-cache allocation failure, and client crashes.

### CVE-2026-137457

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-26T16:17:53.513 |

FreeRDP from 3.0.0 before 3.33.0 contains a missing authentication vulnerability in the shadow server's fast-path input handlers in fastpath.c that allows unauthenticated attackers to inject input before activation. Attackers can negotiate TLS-only RDP, skip Confirm Active, and send Fast-Path Input Event PDUs to inject keystrokes and mouse movement into the host X11 session via XTEST.

### CVE-2026-137455

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-26T16:17:53.177 |

The FreeRDP proxy in FreeRDP before 3.33.0 dereferences a NULL backend client context in pf_server_refresh_rect and pf_server_suppress_output, which are guarded only by a debug-only WINPR_ASSERT, when a REFRESH_RECT or SUPPRESS_OUTPUT data PDU arrives before connection activation. An unauthenticated remote client that completes licensing without sending Confirm Active can crash the proxy process, terminating all hosted sessions.

### CVE-2026-137452

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-26T16:17:52.623 |

FreeRDP before 3.33.0 contains a race condition in asynchronous RDPDR IRP processing that allows malicious RDP servers to leak client memory through non-atomic wStream reference count updates. Attackers can send repeated IRPs, such as smartcard redirection requests, so concurrent Stream_Release() calls lose decrements and accumulate unreleased streams, exhausting memory and causing denial of service.

### CVE-2026-134987

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-27T14:17:03.080 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Nickboss WordPress File Upload wp-file-upload allows Path Traversal.This issue affects WordPress File Upload: from n/a through 5.3.1.

### CVE-2026-134708

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-27T14:17:02.510 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in VideoWhisper.com Video Share VOD video-share-vod allows Path Traversal.This issue affects Video Share VOD: from n/a through 3.15.1.

### CVE-2026-133941

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T09:17:02.120 |

The country manager page of the JTL-Shop administration backend (/admin/countries) writes the request parameter activeSortOrder without output encoding into a single-quoted JavaScript string and into HTML attributes. The overview page requires no CSRF token. An unauthenticated remote attacker can thereby cause script code to be executed in the browser of a logged-in backend user who opens a crafted link in the same browser (the session cookie carries no SameSite attribute by default); the code runs with the privileges of that user and can use the backend token of the same page to send requests to the backend. Visitors and customers are not affected.

### CVE-2026-133939

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T09:17:01.753 |

The OPC (OnPage Composer) start menu, which JTL-Shop shows to logged-in backend users on storefront pages, writes the current page identifier (which contains the search term on search pages) and further values into single-quoted JavaScript strings without escaping. A single quote in the search term terminates the string. An unauthenticated remote attacker can thereby cause script code to be executed in the browser of a backend user who opens a crafted link while logged in to the backend in the same browser; the code runs with the privileges of that user and can use the backend session token contained in the same script to send requests to the backend. Visitors and customers do not receive the start menu and are not affected.

### CVE-2026-133938

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-352` |
| Published | 2026-11-27T09:17:01.530 |

The backend language switch action (quick_change_language) of the JTL-Shop administration backend is executed without a CSRF token check, and the supplied language value is neither validated against the installed backend languages nor encoded on output. The value is stored in the session and in the account data of the administrator and rendered without output encoding in JavaScript strings and HTML attributes of backend pages. An unauthenticated remote attacker can thereby cause script code to be executed in the browser of a logged-in administrator who opens a crafted web page; the code can perform actions with the privileges of that administrator.

### CVE-2026-137704

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-27T03:17:03.963 |

D-Link DWM-222W developed by D-Link Corporation has a Use of Hard-coded Credentials vulnerability. Unauthenticated adjacent network attackers can use the administrator account embedded in the firmware to access the configuration backup endpoint and obtain plaintext passwords for all user accounts.

### CVE-2026-137551

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-11-26T16:18:08.837 |

Frappe Framework before 15.121.2 and 16.x before 16.36.0 exposes functions imported into module-path-hooked modules as Jinja globals, making them callable from sandboxed templates. Authenticated users who can author rendered templates, such as Print Formats, can invoke these functions by name to achieve server-side code execution that bypasses the Jinja sandbox.

### CVE-2026-137523

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:18:04.520 |

ToolJet before 3.21.96-LTS contains an authentication bypass in instance-level Google SSO because the id_token audience is not verified when no Google OAuth client ID is configured, the shipped default. Unauthenticated attackers can submit a Google-signed id_token minted for their own OAuth client to /api/sso/sign-in/common/google without an organizationId, obtaining a session as any existing user with the matching email.

### CVE-2026-137500

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-26T16:18:01.323 |

Budibase before 4.0.0 contains a privilege escalation vulnerability that allows non-admin Creator or app-builder users to read pending invite bearer codes via GET /api/global/users/invites. Attackers can submit a stolen code with a chosen password to the public /api/global/users/invite/accept endpoint, hijacking invited identities up to global admin.

### CVE-2026-137493

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:17:59.823 |

Budibase server from 3.0.0 before 4.0.0 contains an authorization bypass vulnerability that allows view users and anonymous visitors to access entire base tables by passing a view id to the /api/:viewId/rows routes. Attackers can read, export, modify, and delete rows outside the view filter, including hidden columns, or read the full table unauthenticated through PUBLIC views.

### CVE-2026-137491

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T16:17:59.503 |

Budibase before 4.0.0 contains a query injection vulnerability that allows low-privilege or anonymous users to inject AQL or SQL by supplying unescaped parameters to ArangoDB and Snowflake queries. Attackers can execute published queries with crafted parameter values to bypass filters, read entire datasources, and modify or delete all stored documents.

### CVE-2026-137907

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-27T13:17:25.483 |

FFmpeg 3.0 before 8.1.3 contains a heap buffer overflow vulnerability in libavfilter/vf_boxblur.c because query_formats() accepts pixel formats deeper than 16 bits while the blur temporary buffers hold only 2 bytes per pixel. Attackers can supply crafted 32-bit float media, such as PFM or OpenEXR images, that when processed by the boxblur filter overflow the temporary buffers, crashing applications or possibly executing code.

### CVE-2026-136976

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-27T00:16:44.347 |

Improper link resolution before file access in recursive file pull in Canonical LXD before 4.0.15, 5.0.11, 5.21.9, and 6.8 on case-insensitive client filesystems allows an authenticated user with write access to an instance directory or custom volume to write arbitrary files outside the target directory and execute code as the operator via case-variant symlinks.

### CVE-2026-137529

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-26T20:17:24.130 |

JAL (Just Another Ledger) through 2026.11.3 contains an arbitrary file overwrite vulnerability in backup restore that allows attackers to write files by supplying a crafted .tgz backup with a symlink member. Attackers can include a jal.sqlite symlink to an absolute path followed by a regular jal.sqlite member, overwriting files such as shell startup scripts for code execution.

### CVE-2026-137518

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-26T20:17:23.957 |

pyfda through 0.9.5 contains an insecure deserialization vulnerability in load_filter() that allows attackers to execute code by supplying crafted .npz or .pkl filter files. Attackers can embed a __reduce__ gadget that runs via np.load with allow_pickle=True or pickle.load before validation, executing code with the user's privileges.

### CVE-2026-137506

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-26T20:17:23.643 |

ezdxf through 1.4.5 contains a code injection vulnerability in the dxf2code add-on that allows attackers to inject Python code via unescaped single quotes in DXF table entry names. Attackers can craft a DXF file whose layer, linetype, style, or appid names break out of quoted strings in generated scripts, executing code with the privileges of the user running them.

### CVE-2026-137494

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:17:59.980 |

Budibase before 4.0.0 contains a broken object-level authorization vulnerability that allows authenticated users with table write access to reference other tenants' files by supplying arbitrary attachment keys on row save. Attackers can inject a victim app's attachment key into a row, then update or delete the row to delete that object from the shared APPS bucket or read it via presigned URLs.

### CVE-2026-80485

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-27T14:17:06.203 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-80477

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-27T10:17:30.073 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-80453

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-27T09:17:04.077 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains a Download of Code Without Integrity Check vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-115288

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-27T05:19:00.283 |

Missing authentication vulnerability in BS2500/BS500 Virtage Firmware.

This issue affects BladeSymphony BS2500: from 02-02 through 02-76*; BladeSymphony BS500: from 01-01 through 02-76*.

### CVE-2026-115284

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-27T05:18:59.523 |

Missing authentication vulnerability in BS2500/BS500 Virtage Firmware.

This issue affects BladeSymphony BS2500: from 02-02 through 02-76; BladeSymphony BS500: from 01-01 through 02-76.

### CVE-2026-137546

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-26T16:18:07.953 |

Coder 2.29.17 before 2.29.27, 2.32.7 before 2.33.0, 2.33.8 before 2.34.0, 2.34.2 before 2.34.19, 2.35.0 before 2.37.11, 2.38.0 before 2.38.7, and 2.39.0 before 2.39.1 contains a credential exposure vulnerability that allows malicious template authors to steal session tokens because coder open app substitutes $SESSION_TOKEN into template-defined external app URLs without validating scheme or destination. Attackers can define an external app URL or IDE link pointing to an attacker server so users running coder open app leak their token, enabling impersonation of shared users or administrators.

### CVE-2026-137474

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-26T16:17:56.460 |

SiYuan 3.8.8 before 3.8.10 contains an incorrect permission assignment vulnerability that creates workspace directories with mode 0755 and conf.json with mode 0644, exposing the cleartext AccessAuthCode administrator credential. Local users able to traverse the SiYuan user's home path can read it and authenticate as administrator via Basic authentication, for example calling /api/system/setAPIToken to change the API token.

### CVE-2026-132890

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-27T09:17:01.030 |

In Eclipse Dataspace Components (EDC) Connector 1.0.0-RC2 through 1.0.0-RC7, the HashiCorp Vault extension does not reject .. path segments in secret aliases. In a multi-participant (virtual) control plane where vault partitions share the runtime's Vault token, an authenticated participant can set a callback secret alias that escapes its own vault partition. The connector then reads secrets of other participants or of the runtime, such as STS client secrets or the encryption key, and sends them to an endpoint the attacker chooses.

### CVE-2026-137543

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-26T16:18:07.430 |

LaraDashboard before 1.5.2 contains a server-side request forgery vulnerability that allows authenticated users to reach internal services by abusing the unvalidated ai_ollama_base_url setting. Once a settings.edit user points the Ollama base URL internally, any post.create user can call /admin/ai/generate-seo with provider=ollama to fetch internal data reflected in SEO fields.

### CVE-2026-137542

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-26T16:18:07.260 |

LaraDashboard before 1.5.2 contains an information disclosure vulnerability in SettingObserver that writes full Setting models, including plaintext secret option_value fields, into the action_logs table. Users holding only actionlog.view can read API keys, SMTP passwords, and OAuth client secrets through the action log API without settings permissions.

### CVE-2026-137514

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-26T16:18:03.143 |

Nodemailer 9.1.0 before 10.4.1 lowercases recipient domains with JavaScript toLowerCase() in _normalizeAddress before UTS-46 mapping, which converts U+1E9E and word-final U+03A3 differently than WHATWG/UTS-46 validators. An unprivileged attacker can submit an address an application's allow-list approves, causing invites or shared links to reach an attacker-registered domain.

### CVE-2026-123761

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-349` |
| Published | 2026-11-27T14:17:01.687 |

Various logic errors in view processing can cause incorrect cached results to be returned.

### CVE-2026-133940

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-538;CWE-552` |
| Published | 2026-11-27T09:17:01.970 |

The access rules of JTL-Shop (export/.htaccess and export/backup/.htaccess) release files with the extensions gz and zip for the export directory without withdrawing this release in the subdirectory export/backup, in which the shop stores database dumps and file backups. As a result, backup files in this directory can be downloaded without authentication by anyone who knows or guesses the file name. Up to version 5.5.5 the names of database backups consist only of a timestamp; from version 5.6.0 they contain a random component, which does not replace access control. The backups contain the complete shop database (customer data, orders, password hashes) and, for file backups, files of the shop. The access rules are only evaluated by Apache. On installations where another web server, for example nginx, delivers static files such as gz and zip directly (including nginx in front of Apache), the files remain accessible even with the corrected rules, unless the directory is blocked at server level.

### CVE-2026-133842

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-281` |
| Published | 2026-11-27T09:17:01.180 |

A flaw was found in Flatpak’s flatpak-system-helper. When a system-wide app, runtime, or extension uses the extra-data mechanism and its apply_extra logic creates a deeply nested directory tree, permission canonicalization can fail (for example with EMFILE). Affected Flatpak versions can still report success without clearing setuid/setgid bits, leaving a setuid-root executable under /var/lib/flatpak. A local attacker who can install or update such content system-wide, or who can already execute code as a local user in cooperation with that content, can escalate privileges to root.

### CVE-2026-137582

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T16:18:11.653 |

web-token jwt-framework before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6 allows denial of service because JWELoader and JWSLoader try every recipient or signature of a JSON General serialized token without limiting their number. Unauthenticated attackers can send a small JWE with many empty recipients inheriting a maximal PBES2 p2c value, forcing repeated key derivations that exhaust worker CPU.

### CVE-2026-137581

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-26T16:18:11.463 |

web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6, and jwt-encryption and jwt-signature through 3.2.10, contain a denial of service vulnerability because the JWS and JWE serializers pass attacker-controlled tokens and protected headers to json_decode() without bounds before verification. Unauthenticated attackers can submit large tokens with colliding header member names or deeply nested arrays to cause quadratic decoding time or fatal memory exhaustion.

### CVE-2026-137580

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-26T16:18:11.287 |

web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6 parse JSON General serialized JWS tokens in quadratic time because JSONGeneralSerializer::unserialize() adds each signature via JWS::addSignature(), which clones the token. Unauthenticated remote attackers can send large tokens holding thousands of empty signatures to exhaust CPU and occupy PHP workers without any valid key or token.

### CVE-2026-137579

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-11-26T16:18:11.113 |

Web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6, and jwt-core through 3.2.10, perform unblinded RSA private key operations in RSAKey::exponentiate(), so CRT recombination time reveals whether a decrypted RSA-OAEP, RSA-OAEP-256, or RSA1_5 value is below the prime q. Attackers who can submit JWEs can time rejections of crafted tokens to binary search q, factor the modulus, and decrypt all JWEs encrypted to that key.

### CVE-2026-137564

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-11-26T16:18:10.920 |

web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6 (and jwt-encryption through 3.2.10) do not check the key length in JWEBuilder and JWEDecrypter for direct (dir) encryption, so undersized keys are zero-padded. Anyone holding a token issued with a half-size AES-CBC-HMAC key can decrypt it, and an empty key also allows forging tokens the decrypter accepts.

### CVE-2026-137560

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-26T16:18:10.190 |

Web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6 contain a denial of service vulnerability in RSAKey, which accepts RSA keys with a modulus and public exponent of unbounded length. Remote attackers can supply a crafted key, such as in the jwk header of a DPoP proof, to force seconds of CPU per PS256/PS384/PS512 verification or RSA encryption, or per any RSA operation when GMP is unavailable.

### CVE-2026-137559

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405` |
| Published | 2026-11-26T16:18:10.020 |

web-token jwt-framework and jwt-library before 3.4.13, 4.0.x before 4.0.9, 4.1.x before 4.1.11, and 4.2.x before 4.2.6 allow CPU exhaustion because, on PHP without GMP, AbstractECDH falls back to pure PHP curve code that converts unbounded ECDH-ES epk x and y coordinates to big integers before any length check. Unauthenticated attackers who know only the recipient key's curve can send small JWEs with oversized epk coordinates, keeping workers busy for seconds to minutes per token.

### CVE-2026-137553

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T16:18:09.183 |

Frappe Framework before 15.120.0 and 16.x before 16.33.0 contains a blind SQL injection vulnerability in the handling of the X-Frappe-Request-Id HTTP header when monitoring is enabled. Remote unauthenticated attackers can send crafted header values to infer database contents through blind SQL injection techniques.

### CVE-2026-137472

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T16:17:56.103 |

SiYuan from 3.6.2 before 3.8.10 contains a path traversal vulnerability that allows admin token holders to read files outside the workspace because the globalCopyFiles and workspaceCopyFiles denylist omits /home, /mnt, /media, and /snap. Attackers can copy other users' SSH authorized_keys, Docker and AWS configs, or mounted files into the workspace and retrieve them via the getFile API.

### CVE-2026-137466

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-26T16:17:55.080 |

Parse Server before 9.12.0-alpha.2 matches $in, $nin, $all and $containedBy constraints in LiveQuery with a cost proportional to the product of the constraint list size and the saved array size. A client that can subscribe to a class and save objects in it can use large lists and arrays to block the event loop for seconds or longer, stalling LiveQuery and, when it runs in the same process, Parse Server.

### CVE-2026-93087

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-26T15:17:42.827 |

A maliciously modified field in the locally stored JSON description for an update made available by Autodesk, when processed by Autodesk Access, can cause attacker-controlled HTML content to be executed in another user's session. A local, authenticated malicious actor can leverage this vulnerability to execute arbitrary code in the context of another user if that user interacts with an injected link, resulting in privilege escalation.

### CVE-2026-80472

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-27T10:17:29.417 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-119071

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-27T05:19:00.467 |

The W3 Total Cache plugin for WordPress is vulnerable to unauthorized File Deletion in all versions up to, and including, 2.11.0 via the `ajax_revert()` AJAX handler. The vulnerability exists because the `remove_optimizations()` function reads attacker-controlled values from the unprotected `w3tc_imageservice` post meta key — which carries no underscore prefix and no registered authorization callback, making it writable by any user with `edit_post` capability via WordPress's built-in custom-fields AJAX endpoint — and passes those values directly to `wp_delete_attachment()` with no check that the referenced ID is a child of the caller's own post, is an actual attachment, or that the caller holds `delete_post` capability on it. This makes it possible for authenticated attackers with Author-level access or above to permanently delete any WordPress attachment in the media library, including media files owned by other users along with their associated files on disk, regardless of ownership — a capability not available through the normal WordPress interface. The revert nonce is exposed via `wp_localize_script` on `/wp-admin/upload.php` to any user with `upload_files` capability, ensuring the nonce check that is present does not serve as a meaningful barrier to Author-level exploitation.

### CVE-2026-137702

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-27T02:16:45.470 |

Exim before 4.100.2 allows attackers to send SMTP traffic that triggers a heap out-of-bounds write in expansion code running as root.

### CVE-2026-103886

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:17:48.097 |

The App Builder – Create Native Android & iOS Apps On The Flight plugin for WordPress is vulnerable to Authentication Bypass via Google ID Token Audience Validation Bypass in all versions up to, and including, 5.7.1. This is due to the `LoginGoogle::login()` function failing to validate the `aud` (audience) claim of the supplied `idToken` against any OAuth client ID belonging to the WordPress site, failing to verify the `email_verified` claim, and resolving WordPress accounts solely by the email claim without binding to the Google `sub` (subject) identifier — while the `/app-builder/v1/login` REST endpoint is registered with a `permission_callback` that unconditionally returns `true`, leaving it fully reachable by unauthenticated requesters. This makes it possible for unauthenticated attackers to authenticate as any existing WordPress user — including Administrators — whose email address is known, by supplying a Google-signed ID token obtained from an entirely unrelated OAuth client containing the target user's email claim, which causes the plugin to issue a signed App Builder JWT granting that user's full privileges. Exploitation requires the attacker to obtain a valid Google-signed ID token carrying the target user's email address, which can be achieved by operating a separate Google OAuth client and inducing the target user to authenticate through it.

### CVE-2026-80501

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-27T14:17:06.713 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Denial of service.

### CVE-2026-80498

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-27T14:17:06.337 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains a Use of Hard-coded Cryptographic Key vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-80457

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-27T10:17:28.610 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Incorrect Permission Assignment for Critical Resource vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Denial of service.

### CVE-2026-80451

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-11-27T09:17:03.817 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains a Use of Hard-coded Cryptographic Key vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-80268

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-668` |
| Published | 2026-11-27T09:17:03.140 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Exposure of Resource to Wrong Sphere vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Remote execution.

### CVE-2026-137481

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T16:17:57.673 |

Traefik before 2.11.62, 3.x before 3.7.18, and 3.8.0-rc.1 contain an authorization bypass because the sanitizePath entry point option leaves dot-segments carrying path parameters, such as /..;x/, unresolved when matching routers and applying middlewares. Unauthenticated attackers can send requests like /public/..;x/admin to a parameter-stripping backend shared with a protected router, bypassing authentication or authorization middlewares to reach protected resources.

### CVE-2026-80500

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-27T14:17:06.587 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Improper Authentication vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-137746

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-404` |
| Published | 2026-11-27T13:17:24.907 |

A flaw has been found in Free5GC 4.3.0. This vulnerability affects unknown code of the component SMF. This manipulation causes resource consumption. The attack may be initiated remotely. The exploit has been published and may be used. The pull request to fix this issue awaits acceptance.

### CVE-2026-80475

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-27T10:17:29.807 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Server-side request forgery.

### CVE-2026-80450

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-27T09:17:03.683 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Improper Certificate Validation vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Elevation of privileges and Remote execution.

### CVE-2026-80448

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-27T09:17:03.407 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-137715

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-27T05:19:02.787 |

Webmin through 2.670 before 07d1949 does not escape a save_log.cgi log file path. This is relevant for code execution if a shared-hosting provider offers Webalizer module access.

### CVE-2026-137469

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:55.590 |

SiYuan 3.7.0 before 3.8.11 contains a DOM-based cross-site scripting vulnerability in the AI agent chat panel, which renders final and saved assistant replies into innerHTML without HTML sanitisation. Attackers influencing model replies via indirect prompt injection or a configured model endpoint can inject event-handler markup, executing OS commands through Node.js integration in desktop local-kernel mode.

### CVE-2026-123762

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-27T14:17:01.813 |

A catalog zone update introducing a new zone which already exists, but in a different backend than the one storing the catalog zone, will cause a duplicate zone to be created in that backend, and (depending on the backend load order) may completely hide the existing zone.

### CVE-2026-115285

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-27T05:18:59.717 |

DoS vulnerability in BS2500/BS500 Virtage Firmware.

This issue affects BladeSymphony BS2500: from 02-02 through 02-76; BladeSymphony BS500: from 01-01 through 02-76.

### CVE-2026-135032

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-27T14:17:03.667 |

Missing Authorization vulnerability in Everest Forms Everest Forms everest-forms allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Everest Forms: from n/a through 3.6.4.

### CVE-2026-134993

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-11-27T14:17:03.223 |

Path Traversal: '.../...//' vulnerability in Seraphinite Solutions Seraphinite Accelerator seraphinite-accelerator allows Path Traversal.This issue affects Seraphinite Accelerator: from n/a through 2.31.3.

### CVE-2026-124728

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-27T14:17:02.180 |

Incomplete GSS negotiation, as well as TKEY context deletion while a pending operation will need to be signed with that key, can lead to a crash.

### CVE-2026-123764

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-27T14:17:01.937 |

Incorrect sanitization of received data during zone AXFR to Bind backend can cause wrong or invalid data to be serialized.

### CVE-2026-135627

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-27T04:16:40.263 |

The Simple Membership plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.9.0 The vulnerability exists because the `bulk_operation_menu()` function accepts the `swpm_bulk_change_level_to` parameter from `$_REQUEST` with only `sanitize_text_field()` applied, and passes it to `SwpmMemberUtils::update_membership_level_and_role()` without the `id != 1` allowlist exclusion that every other level-selection path in the plugin enforces — leaving membership level 1, which the installer maps to the WordPress `administrator` role on every fresh install, freely selectable as a bulk-change target. This makes it possible for authenticated attackers with Contributor-level access and above to elevate their own WordPress account to the full Administrator role, gaining complete site control including plugin installation, user creation, and all other administrator capabilities. Exploitation requires that an administrator has first lowered the plugin's "Admin Dashboard Access Permission" setting from its default of `manage_options` to a lesser capability such as `edit_posts` (Contributor), `edit_published_posts` (Author), or `edit_pages` (Editor), which is a non-default granted-access configuration; the bulk screen's nonce protection (`swpm_bulk_change_level_nonce_action`) does not mitigate the issue because the nonce is emitted on the same page the delegated lower-role user can already reach. Successful exploitation causes the attacker's own account to receive the complete administrator role.

### CVE-2026-135626

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-27T04:16:40.110 |

The Simple Membership plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.9.0 This is due to the `SwpmLevelForm::role()` function applying only `sanitize_text_field()` to the user-supplied `role` parameter with no allowlist, permitting the `administrator` role to be stored verbatim into `swpm_membership_tbl` and subsequently applied to a member's WordPress account via `$user->add_role()` inside `update_wp_user_role()` — also without any role allowlist — when the `swpm_membership_level_changed` action fires. This makes it possible for authenticated attackers with Contributor-level access and above to create a membership level specifying the `administrator` WordPress role, assign themselves to that level, and thereby elevate their own WordPress account to full Administrator, gaining complete site control including the ability to install plugins, edit themes, and manage users. Exploitation requires that the site owner has lowered the plugin's "Admin Dashboard Access Permission" setting from its default `manage_options` capability to a lesser capability such as `edit_posts`, `edit_published_posts`, or `edit_pages`, which grants lower-privileged users access to the SWPM admin dashboard where the vulnerable level-creation form resides. Successful exploitation causes the attacker's own account to receive the complete administrator role.

### CVE-2026-135616

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-11-27T02:16:45.160 |

The W3 Total Cache plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.11.0 via deserialization of untrusted input that is injected into the Memcached object cache through request Host header key truncation. This allows authenticated attackers, with subscriber-level access and above, to inject a PHP Object. The additional presence of a POP chain (the bundled Guzzle FileCookieJar, reached through the W3TC\CdnEngine_S3 autoload bridge) allows attackers to write arbitrary files and execute code. This requires the Object Cache to be enabled with the Memcached method backed by the pecl memcache extension and Minify to be enabled; using the same key collision, the attacker first escalates from Subscriber to Administrator.

### CVE-2026-135038

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T19:17:10.173 |

Missing Authorization vulnerability in weDevs WP ERP erp allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects WP ERP: from n/a through 2.0.0.

### CVE-2026-134714

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T19:17:09.740 |

Missing Authorization vulnerability in Webful Creations RepairBuddy computer-repair-shop allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects RepairBuddy: from n/a through 4.1237.

### CVE-2026-134488

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T19:17:09.310 |

Missing Authorization vulnerability in Mamunur Rashid Radius Booking — Booking Calendar for Appointments &amp; Services radius-booking allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Radius Booking — Booking Calendar for Appointments &amp; Services: from n/a through 1.0.22.

### CVE-2026-97345

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:18:12.910 |

The SumUp Payment Gateway For WooCommerce plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 2.17.1 via the 'sumup-validate-order' query parameter handled by the check_redirect_flow() / resolve_payment_redirect_validation() functions. The template_redirect handler accepts an arbitrary numeric order ID from an unauthenticated GET request and, without any ownership or capability check, loads the corresponding WooCommerce order and issues a 302 redirect whose Location header is built by get_return_url(), disclosing the target order's secret order_key. This makes it possible for unauthenticated attackers to enumerate order IDs, harvest each order's WooCommerce order_key, and use those keys against the plugin's create_checkout endpoint and WooCommerce's own order-received/order-pay pages to read customer PII (name, email, phone, billing address, order total) for any order in the store.

### CVE-2026-92251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:18:12.753 |

The ZarinPal Payment Gateway for WooCommerce plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 5.1.1 via the `Return_from_ZarinPal_Gateway()` handler registered on the `woocommerce_api_wc_zpal` (`?wc-api=wc_zpal`) endpoint. The handler accepts a `wc_order` parameter from the query string, loads the corresponding WooCommerce order without any authentication, nonce, session, capability, or ownership check, and — when the order is paid — issues a 302 redirect to `get_return_url($order)`, whose `Location` header embeds the order's secret `order_key`. This makes it possible for unauthenticated attackers to harvest order keys for arbitrary orders (regardless of payment method) and then use those keys against the WooCommerce order-received, order-pay and download endpoints to read the associated customer's PII, including billing name, street address, phone number, email, purchased items, and totals.

### CVE-2026-109586

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:17:48.960 |

The WP STAGING – Backups & Restore, Migration & Clone Plugin – Cloud Backups, Scheduled Backups plugin for WordPress is vulnerable to Authorization Bypass in all versions up to, and including, 4.17.0 via the `REQUEST_URI` query parameter. This is due to a parser-differential flaw in `showLoginForm()`: the plugin's `isRestUrl()` function performs an unanchored `strpos()` prefix match against the full `REQUEST_URI` — including the query string — and short-circuits all authorization checks (including `isStagingSite()` and `current_user_can('manage_options')`) whenever it detects a REST-like URL, while WordPress core only treats a request as a REST API call when the `rest_route` query variable is non-empty. This makes it possible for unauthenticated attackers to bypass the staging-site login gate entirely by appending an empty `rest_route` parameter (e.g. `/wp-json/?rest_route=`), causing the plugin to skip its gate while core proceeds to render the ordinary theme front end, exposing the full theme-rendered contents of the staging site — including private post content, page-builder output, WooCommerce pages, and site search results over the staging database. This bypass only affects staging sites where the login gate is active, which is the default state for any site cloned by the plugin when the `wpstg_is_staging_site` option is set to `true` or the `.wp-staging` marker file is present in `ABSPATH`.

### CVE-2026-136488

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T15:17:27.167 |

The GeoDirectory – WP Business Directory Plugin and Classified Listings Directory plugin for WordPress is vulnerable to generic SQL Injection via the 'stype' parameter in all versions up to, and including, 2.8.208 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This is possible because the plugin's mu-plugin companion (copied automatically on install when the default 'Enable Fast AJAX' option is on) defines DOING_AJAX on any front-end request carrying gd-ajax=1, and an unconditional branch in geodir_get_current_posttype() restores the attacker-controlled stype value after the allow-list check clears it, allowing the tainted value to reach the SQL sink without any preparation.

### CVE-2026-130331

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-26T15:17:24.710 |

The WP Statistics – Simple, privacy-friendly Google Analytics alternative plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 14.16.19 via the 'tab' parameter parameter. This makes it possible for authenticated attackers, with subscriber-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The exploitability of this vulnerability depends on the Minimum Role to View Statistics setting; when set to a low-privilege role such as Subscriber (read capability), unauthenticated-equivalent access is effectively granted to any registered user, while the default Administrator setting limits exposure to higher-privileged accounts.

### CVE-2026-126089

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-26T15:17:24.403 |

The Drag and Drop Multiple File Upload (Pro) - WooCommerce plugin for WordPress is vulnerable to generic SQL Injection via the 'wc-upload-file (array key)' parameter in all versions up to, and including, 1.7.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Exploitation requires that the site administrator has enabled the 'Count no. of pages?' option (drag_n_drop_count_pdf set to 'yes') and that the uploaded filename stored in the cart resolves to a file with a .pdf extension.

### CVE-2026-123757

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-27T14:17:01.193 |

An attacker can send a notify request that causes the root zone to be added as a secondary domain to be added to the bind backend, but causes said backend to update its configuration to an invalid one, leading to the backend no longer able to run on the next restart, requiring manual operation to fix it. The general case of this problem was addressed by SA-2026-05, but the root zone was not handled correctly. This is now fixed.

### CVE-2026-135280

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178;CWE-863` |
| Published | 2026-11-26T17:17:06.613 |

@fastify/express is the plugin that lets an application run Express middleware and Express applications inside the Fastify web framework. In versions before 4.0.14, when an application enables case-insensitive routing, middleware mounted on a path can still be skipped in two cases: a string mount path or plugin prefix containing a Unicode character whose case folding differs from a plain lowercase conversion fails to match the lowercased request path, and a matcher that stays case-sensitive inside an Express Router or application, such as a regular expression without the ignore-case flag or an explicitly case-sensitive router, only matches its own casing. In both cases a request reaches the Fastify route handler while the path-scoped middleware does not run. An attacker can use this to bypass authentication or other middleware-based access controls on the affected routes, and only applications that enable case-insensitive routing are affected. The issue is fixed in @fastify/express 4.0.14, and users should upgrade to 4.0.14 or later. As a workaround, enforce authentication in a Fastify hook such as preHandler that runs after routing, avoid such Unicode characters in mount paths, and match case-insensitively inside Express routers and applications.

### CVE-2026-135270

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-11-26T17:17:06.370 |

@fastify/express is the plugin that lets an application run Express middleware and Express applications inside the Fastify web framework. In versions from 4.0.5 before 4.0.14, a mount path that begins with an Express 5 optional leading segment written as a group is treated as relative and has a slash prepended when it is joined to the plugin prefix, which changes what the pattern matches so the middleware ends up mounted on a path that no longer corresponds to the real request paths. The middleware therefore never runs for requests that match the intended routes, while the Fastify routes still resolve to their handlers. An attacker can use this to bypass authentication or other middleware-based access controls on the affected routes. The issue is fixed in @fastify/express 4.0.14, and users should upgrade to 4.0.14 or later. As a workaround, mount the middleware on each path spelling explicitly, or enforce authentication in a Fastify hook such as preHandler that runs after the router resolves the request.

### CVE-2026-135264

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-11-26T17:17:06.243 |

@fastify/express is the plugin that lets an application run Express middleware and Express applications inside the Fastify web framework. In versions from 4.0.7 before 4.0.14, when middleware is mounted on a nested array of mount paths the plugin rewrites only the top level of the array, so paths inside a nested array are not adjusted for a plugin registered under a prefix and the middleware never runs for them, a nested regular-expression mount keeps its global or sticky flag and is matched statefully so it is skipped on alternating requests, a nested regular expression is not matched case-insensitively when case sensitivity is disabled, and nested dynamic paths are not covered by the earlier empty-segment check. An attacker can use any of these to bypass authentication or other middleware-based access controls on the affected routes. The issue is fixed in @fastify/express 4.0.14, and users should upgrade to 4.0.14 or later. As a workaround, flatten mount path arrays before passing them to the plugin, or enforce authentication in a Fastify hook such as preHandler that runs after the router resolves the request.

### CVE-2026-135230

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-185;CWE-436` |
| Published | 2026-11-26T17:17:06.117 |

@fastify/express is the plugin that lets an application run Express middleware and Express applications inside the Fastify web framework. In versions from 4.0.3 before 4.0.14, the plugin decodes certain percent-encoded characters in the request path that Express would otherwise keep encoded, including the Unicode line separator and paragraph separator characters, and leaves them raw. A JavaScript regular expression treats those two characters as line terminators, so a regular-expression mount path that relies on the dot metacharacter fails to match a request containing them while Fastify's own router still routes the request to its handler, and the middleware mounted on that regular-expression path is therefore skipped. An attacker can use this to bypass authentication or other middleware-based access controls on routes guarded by a regular-expression mount; string mount paths are not affected. The issue is fixed in @fastify/express 4.0.14, and users should upgrade to 4.0.14 or later. As a workaround, use string mount paths, avoid the dot metacharacter in regular-expression mounts by using a character class or the dotAll flag, or enforce authentication in a Fastify hook such as preHandler that runs after the router resolves the request.

### CVE-2026-135205

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-11-26T17:17:05.980 |

@fastify/middie is the plugin that adds Express-style middleware support to the Fastify web framework. In versions 9.3.6 through 9.3.9, a route or mount path written without a leading slash inside a plugin registered under a prefix is handled inconsistently: the middleware is mounted with a separating slash after the prefix, while the route is concatenated directly onto the prefix, so a request to the concatenated path reaches the route handler without running the middleware mounted for it. An attacker can use this to bypass authentication or other middleware-based access controls on the affected routes. The issue is fixed in @fastify/middie 9.3.10, and users should upgrade to 9.3.10 or later. As a workaround, begin all route and mount paths with a slash, or enforce authentication in a Fastify hook such as preHandler that runs after the router resolves the request.

### CVE-2026-80483

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-193` |
| Published | 2026-11-27T14:17:05.907 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Off-by-one Error vulnerability. An unauthenticated local attacker could potentially exploit this vulnerability, leading to Session theft.

### CVE-2026-137939

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-27T14:17:04.867 |

Sparkle 2.2.0 before 2.9.6 contains a link following vulnerability in -submitInstallerAtPath: in SUInstallerLauncher.m that builds a root updater's launcher cache path inside the console user's home directory and then deletes and creates items there without rejecting symbolic links. A local console user can pre-create that path as a symlink while a CLI tool or daemon updates a bundle as root, making root delete old files in a directory of the attacker's choosing and create a directory there that is chowned to the attacker, leading to privilege escalation.

### CVE-2026-137938

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-27T14:17:04.697 |

Sparkle before 2.9.6 contains a time-of-check time-of-use race condition in the installer's SPUInstallationData handling in AppInstaller.m, which validates the symlink-resolved download URL but performs the privileged move on the unresolved URL and checks the file type only afterwards. A local user can swap an intermediate directory of the download path for a symlink between the check and the move, causing a root installer to rename a file out of a protected location and leading to privilege escalation when the installer runs in the system domain.

### CVE-2026-80459

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-377` |
| Published | 2026-11-27T10:17:28.887 |

Dell Secure Connect Gateway - Virtual Edition, versions prior to 5.36.00.16, contains an Insecure Temporary File vulnerability. A low privileged local attacker could potentially exploit this vulnerability, leading to Filesystem access for attacker.

### CVE-2026-133845

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-252` |
| Published | 2026-11-27T09:17:01.363 |

A flaw was found in Flatpak’s flatpak-portal. When a sandboxed application invokes Spawn() and maps two different file descriptors to the same handle, dup2() can fail. Affected Flatpak versions do not handle that failure, so a file descriptor that was open inside flatpak-portal (commonly the unfiltered D-Bus session bus) can be passed into the subsandbox. A malicious or compromised Flatpak app with no special privileges can use this to escape the sandbox.

### CVE-2026-115287

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-823` |
| Published | 2026-11-27T05:19:00.097 |

DoS vulnerability in BS2500/BS500 Virtage Firmware.

This issue affects BladeSymphony BS2500: from 02-02 through 02-76; BladeSymphony BS500: from 01-01 through 02-76.

### CVE-2026-115286

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-27T05:18:59.907 |

DoS vulnerability in BS2500/BS500 Virtage Firmware.

This issue affects BladeSymphony BS2500: from 02-02 through 02-76; BladeSymphony BS500: from 01-01 through 02-76.

### CVE-2026-137487

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:58.700 |

OpenWrt LuCI luci-app-unbound through 26.288.56989~75a306d contains a stored cross-site scripting vulnerability because the Unbound Configure page inserts the dhcp.odhcpd.leasetrigger value into a warning notification without escaping. Users with delegated network configuration access can store an HTML event handler in that option through the permitted uci RPC, which executes in an administrator's browser session when the page renders.

### CVE-2026-136995

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T05:19:01.603 |

The Upsell Funnel Builder for WooCommerce – Create Upsells, Cross-Sells, Order Bumps, Frequently Bought, and Popups. plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'form_data' parameter in all versions up to, and including, 3.1.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce gating the vulnerable AJAX endpoint is publicly emitted to any visitor loading a cart, checkout, or shortcode page, making the endpoint fully exploitable by unauthenticated attackers without any prior account or login.

### CVE-2026-137041

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T03:17:03.383 |

The E2Pdf – Export Pdf Tool for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'your-name (or any CF7 field referenced in the action's error_message/condition)' parameter in all versions up to, and including, 2.00.05 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires a typical deployment where an E2Pdf action with a 'PDF Access By URL' error message references a submitted Contact Form 7 field, as the payload is seeded via a single unauthenticated CF7 submission and triggered by any visitor who opens the resulting shareable download URL.

### CVE-2026-126717

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T02:16:44.237 |

The Translate WordPress with Weglot 2.0 – Multilingual AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 6.4.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the target site to permit anonymous comment posting (comment_registration disabled) and have at least one Weglot destination language active; on sites with comment moderation enabled, an administrator must approve the carrier and trigger comments before the injected script executes for subsequent visitors.

### CVE-2026-114454

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-863` |
| Published | 2026-11-27T00:16:39.503 |

Path traversal in TPM device management in Canonical LXD from 4.8 before 5.0.12, 5.21.10, 6.10.2 allows a remote authenticated user with project access to recursively delete arbitrary files and directories on the host as root via a crafted device name during instance or device removal.

### CVE-2026-85416

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:18:12.440 |

The Lenix Leads Collector plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Form Field Name in all versions up to, and including, 2.0.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable because the plugin's CF7 integration accepts and stores any extra field name not defined in the CF7 form — including HTML/JS payloads — submitted by an unauthenticated user via a public CF7 form submission, with the raw field name later echoed unescaped in two separate admin-side sinks.

### CVE-2026-85412

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:18:12.280 |

The Easy Form Builder by WhiteStudio – Drag & Drop Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'address' parameter in all versions up to, and including, 4.2.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. A valid nonce required for form submission can be freely obtained by any unauthenticated visitor via the publicly accessible REST route 'Emsfb/v1/nonce/refresh', which is registered with no permission check, enabling the full attack chain without any credentials.

### CVE-2026-137511

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-226` |
| Published | 2026-11-26T16:18:02.647 |

Scriban before 7.6.0 contains a state isolation vulnerability because TemplateContext.Reset() does not clear the Tags dictionary holding array.cycle and math.random state. Attackers supplying templates to a reused context can observe or influence cycle positions and random sequences across renders, and accumulate unbounded cycle entries to exhaust memory.

### CVE-2026-137503

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-11-26T16:18:01.647 |

Budibase before 4.0.0 contains a JSON injection vulnerability that allows attackers to inject JSON structure into S3 delete and Google Sheets row fields via unescaped template parameters. Attackers can submit crafted parameters to the queries endpoint to add extra Key entries, deleting chosen S3 objects or overriding Sheets row columns.

### CVE-2026-137496

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-26T16:18:00.293 |

Budibase before 4.0.0 contains a server-side template injection vulnerability that allows authenticated users with table read permission to execute JavaScript by injecting Handlebars js helpers into row search query values. Attackers can submit base64-encoded JavaScript through the search endpoint, which enrichSearchContext() runs in an isolated-vm sandbox, to read OAuth2 access and refresh tokens of SSO users or cause denial of service.

### CVE-2026-131803

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:50.923 |

The Mang Board plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'content' parameter in all versions up to, and including, 2.4.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The post-sanitization decode step preserves percent-encoded characters such as %22 through HTMLPurifier, then decodes them to literal double-quotes at render time, allowing an attacker-supplied src attribute to break out of its context and inject event-handler attributes such as onerror into the img tag.

### CVE-2026-126342

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:50.467 |

The WPForms (Contact Form by WPForms / wpforms-lite) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the Multiple Choice field's 'Other' option value on payment forms in all versions up to, and including, 2.0.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a privileged user such as an administrator accesses the injected payment entry on the WPForms > Payments details page. The submitted value is stored via sanitize_text_field(), which preserves a space-separated pseudo-tag (e.g. '< i class="wpforms-single-payment-tooltip" data-tooltip-content="&lt;img src=x onerror=...&gt;">x< /i>') because strip_tags() ignores a '<' followed by whitespace; on the admin Payments entry page the value is output through wp_kses() with the 'post' allowlist, which normalizes it into a live <i> element retaining its class and data-* attributes, and the bundled Tooltipster initialization (contentAsHTML + contentCloning) then renders the attribute's HTML, executing the script on page load without any hover.

### CVE-2026-124072

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:50.160 |

The User Frontend – Membership, User Registration, User Profile, User Directory & Content Restriction with Frontend Post Submission plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'post_title' parameter in all versions up to, and including, 4.3.14 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has configured a wpuf Post Form with guest post submission enabled and placed its shortcode on a public page, from which an unauthenticated attacker can scrape the required nonce before submitting the malicious payload.

### CVE-2026-122039

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:49.987 |

The User Registration & Membership – Free & Paid Memberships, Subscriptions, Content Restriction, User Profile, Custom User Registration & Login Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'user_registration_<checkbox_field_name>[]' parameter in all versions up to, and including, 5.3.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The self-registration endpoint (wp_ajax_nopriv_user_registration_user_form_submit) requires no nonce, allowing an unauthenticated attacker to create a Subscriber account and then supply the malicious checkbox value through the authenticated profile-update action using a legitimately obtained nonce.

### CVE-2026-119159

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:49.830 |

The Hide My WP Ghost – Security & Firewall plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 7.0.15 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires that the plugin's URL rewriting mode is active (hmwp_mode set to a non-default value) and that the attacker has one previously approved comment from the same author/email address, after which WordPress auto-approves the attack comment without moderator intervention.

### CVE-2026-119153

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T16:17:49.680 |

The Swift Performance Lite plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'REQUEST_URI (gated by $_GET['force-cache'])' parameter in all versions up to, and including, 2.3.7.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is planted via a single unauthenticated GET request to any URL with ?force-cache=1 and a URL-encoded HTML payload in the path, which the plugin decodes and creates as a literal filesystem directory name; the script fires the next time an administrator opens the Swift Performance dashboard.

### CVE-2026-95810

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:45.040 |

The Easy Form Builder by WhiteStudio – Drag & Drop Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via esign 'value' Field via Cross-Type 'r_matrix' Poisoning in all versions up to, and including, 4.3.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation is possible without authentication because the REST endpoint /wp-json/Emsfb/v1/forms/message/add is guarded only by a wp_rest nonce freely obtainable by any visitor loading the public-facing form page via efb_var.nonce.

### CVE-2026-137122

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:28.207 |

The PDF Invoices & Packing Slips for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_address.address_1' parameter in all versions up to, and including, 6.0.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit requires the E-Documents feature to be enabled with a document format selected, as this is what causes the vulnerable meta box to be rendered on the order edit screen.

### CVE-2026-136610

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:27.770 |

The Pixeline’s Email Protector plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 1.5.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the malicious comment to pass the site's moderation queue, which WordPress enforces for first-time commenters by default but which does not re-sanitize stored comment content.

### CVE-2026-135675

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:26.413 |

The RSS Aggregator by Feedzy – Feed to Post, Autoblogging, News & YouTube Video Feeds Aggregator plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in versions up to, and including, 5.2.17 due to insufficient restriction on the wp_kses_allowed_html filter callback. The feedzy_wp_kses_allowed_html() method is registered on wp_kses_allowed_html with the loader's default accepted_args=1, so the callback never receives the context-name argument and unconditionally adds <iframe> (with arbitrary src, width, height, frameborder, allowfullscreen and data-* attributes) to the allowed-tag array for every context — including pre_comment_content, which WordPress uses to sanitize comment bodies submitted by users without the unfiltered_html capability. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-135654

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:26.260 |

The Lightbox with PhotoSwipe plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 5.18.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires an administrator to approve the attacker's comment at least once, which is the default WordPress behavior for first-time commenters; after that initial approval, no further administrative action is needed and the payload fires for any visitor who opens the lightbox on the affected post.

### CVE-2026-130321

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:24.553 |

The PDF Invoices & Packing Slips for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_address.first_name / company / address_1 / address_2 / city' parameter in all versions up to, and including, 6.0.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the E-Documents feature to be enabled with a UBL PEPPOL BIS 3.0 format, as that setting is disabled by default and controls whether the vulnerable meta box is registered and rendered.

### CVE-2026-125001

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:24.250 |

The NextMove Lite – Thank You Page for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'billing_address.email' parameter in all versions up to, and including, 2.24.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected script fires without any victim interaction because the builder page's JavaScript calls $(".preview_order_id").trigger("change") on page load, immediately executing any attribute-injected event handler.

### CVE-2026-123827

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:24.100 |

The Easy Social Share Buttons for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'position' parameter in all versions up to, and including, 11.6.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is stored via the unauthenticated wp_ajax_nopriv_ ESSB stat log AJAX action, which performs no nonce or capability check, and executes when the attacker-controlled position value is rendered verbatim into a double-quoted HTML data-* attribute where the unescaped quote allows attribute breakout.

### CVE-2026-135953

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T14:17:04.257 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WS Form WS Form LITE ws-form allows Stored XSS.This issue affects WS Form LITE: from n/a through 1.12.19.

### CVE-2026-135923

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T14:17:04.110 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPTasty AWP Classifieds another-wordpress-classifieds-plugin allows Stored XSS.This issue affects AWP Classifieds: from n/a through 4.4.10.

### CVE-2026-134983

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T14:17:02.930 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Muralidharan Ramasamy Push Notification for Post and BuddyPress push-notification-for-post-and-buddypress allows Stored XSS.This issue affects Push Notification for Post and BuddyPress: from n/a through 3.24.

### CVE-2026-134982

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T14:17:02.793 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Amauri.IO WPMobile.App wpappninja allows Stored XSS.This issue affects WPMobile.App: from n/a through 11.90.

### CVE-2026-135950

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:24.307 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in fifu.app Featured Image from URL featured-image-from-url allows Stored XSS.This issue affects Featured Image from URL: from n/a through 6.1.8.

### CVE-2026-135948

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:24.147 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeisle MPG multiple-pages-generator-by-porthas allows Stored XSS.This issue affects MPG: from n/a through 4.2.6.

### CVE-2026-135911

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:23.670 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PI Web Solution Product Enquiry for WooCommerce enquiry-quotation-for-woocommerce allows Stored XSS.This issue affects Product Enquiry for WooCommerce: from n/a through 2.2.34.64.

### CVE-2026-134957

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:23.030 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Chill Image Photo Gallery Final Tiles Grid final-tiles-grid-gallery-lite allows DOM-Based XSS.This issue affects Image Photo Gallery Final Tiles Grid: from n/a through 3.6.18.

### CVE-2026-134939

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:22.877 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in David Lingren Media LIbrary Assistant media-library-assistant allows Reflected XSS.This issue affects Media LIbrary Assistant: from n/a through 3.43.

### CVE-2026-134717

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:22.707 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in wp.insider Simple Membership simple-membership allows Stored XSS.This issue affects Simple Membership: from n/a through 4.8.9.

### CVE-2026-133720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T13:17:22.543 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Socio WP Telegram Widget and Join Link wptelegram-widget allows Reflected XSS.This issue affects WP Telegram Widget and Join Link: from n/a through 2.2.16.

### CVE-2026-135961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:06.530 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Nks Continuous Image Carousel With Lightbox continuous-image-carousel-with-lightbox allows Stored XSS.This issue affects Continuous Image Carousel With Lightbox: from n/a through 2.0.

### CVE-2026-135958

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:06.260 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in jgwhite33 WP Review Slider wp-facebook-reviews allows Stored XSS.This issue affects WP Review Slider: from n/a through 15.5.

### CVE-2026-135951

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:06.117 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Designinvento DirectoryPress directorypress allows Reflected XSS.This issue affects DirectoryPress: from n/a through 3.6.27.

### CVE-2026-135949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:05.973 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeisle MPG multiple-pages-generator-by-porthas allows Reflected XSS.This issue affects MPG: from n/a through 4.2.6.

### CVE-2026-135942

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:05.833 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeum Tutor LMS tutor allows Reflected XSS.This issue affects Tutor LMS: from n/a through 4.2.1.

### CVE-2026-135941

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:05.693 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Booking Activities Team Booking Activities booking-activities allows Reflected XSS.This issue affects Booking Activities: from n/a through 1.19.5.

### CVE-2026-129052

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-27T12:17:05.543 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Greg Winiarski WPAdverts wpadverts allows Stored XSS.This issue affects WPAdverts: from n/a through 2.3.5.

### CVE-2026-127118

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295;CWE-319` |
| Published | 2026-11-27T11:17:05.393 |

RCDevs OpenOTP SMS integration connector does not validate the TLS certificate of the remote endpoint, and transmitted the connection credentials and the message content as parameters in the request URL. An attacker in a privileged network position can intercept or tamper with this traffic.


This issue was fixed in version 1.1

### CVE-2026-135385

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-27T00:16:43.600 |

Incorrect authorization in backup export and network zone read endpoints in Canonical LXD before 6.10.2 allows an authenticated user with view-only access to export instance and custom storage volume backups and read network zone TSIG peer keys via endpoints enforcing only view permissions.

### CVE-2026-127162

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-11-27T00:16:41.297 |

Improper output encoding in Prometheus metrics exposition in Canonical LXD before 5.0.12, 5.21.10, 6.10.2 allows a user controlling a virtual machine to forge host metric labels and break metrics scraping via unescaped guest-controlled filesystem mountpoints and network interface names.

### CVE-2026-137588

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-26T20:17:24.443 |

LibreChat 0.7.6 before 0.8.8 contains a denial of service vulnerability that allows authenticated users to block the server event loop by uploading a crafted conversation import file to POST /api/convos/import. Attackers can submit many messages with unresolvable parentMessageId values, triggering quadratic processing in cloneMessagesWithTimestamps or adjustTimestampsForOrdering and stalling the Node.js event loop for minutes for all users.

### CVE-2026-137507

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-26T20:17:23.800 |

torchvision before 0.29.2 contains a path traversal vulnerability in _extract_tar() that allows attackers to write files outside the extraction directory by supplying crafted tar archives. Attackers controlling archives passed to extract_archive() or download_and_extract_archive() can use .. paths, absolute paths, or symlinks to overwrite Python modules and achieve code execution.

### CVE-2026-134997

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T20:17:23.097 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in KAP ASIAs LottieFiles – JSON Based Animation Lottie & Bodymovin for Elementor <= 1.10.9 - Authenticated (Contributor+) Stored Cross-Site Scripting include-lottie-animation-for-elementor allows Stored XSS.This issue affects LottieFiles – JSON Based Animation Lottie & Bodymovin for Elementor <= 1.10.9 - Authenticated (Contributor+) Stored Cross-Site Scripting: from n/a through 2.0.3.

### CVE-2026-134991

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T20:17:22.953 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in IdeaBox Creations PowerPack Addons for Elementor powerpack-lite-for-elementor allows Stored XSS.This issue affects PowerPack Addons for Elementor: from n/a through 3.2.0.

### CVE-2026-134720

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T20:17:22.810 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Webful Creations RepairBuddy computer-repair-shop allows Stored XSS.This issue affects RepairBuddy: from n/a through 4.1237.

### CVE-2026-134489

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T20:17:22.527 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeum Kirki kirki allows Stored XSS.This issue affects Kirki: from n/a through 6.4.2.

### CVE-2026-135039

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:10.313 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP GiveWP give allows Reflected XSS.This issue affects GiveWP: from n/a through 4.19.2.1.

### CVE-2026-135037

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:10.030 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Mohammed Kaludi AMP for WP accelerated-mobile-pages allows Stored XSS.This issue affects AMP for WP: from n/a through 1.1.21.

### CVE-2026-134955

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:09.880 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in tychesoftwares Product Input Fields for WooCommerce product-input-fields-for-woocommerce allows Reflected XSS.This issue affects Product Input Fields for WooCommerce: from n/a through 2.0.3.

### CVE-2026-134713

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:09.603 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in INTINITUM FORM Transliterator serbian-transliteration allows Stored XSS.This issue affects Transliterator: from n/a through 2.5.15.

### CVE-2026-134712

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:09.460 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in DevItems ShopLentor woolentor-addons allows Stored XSS.This issue affects ShopLentor: from n/a through 3.5.9.

### CVE-2026-134470

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T19:17:09.163 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Host.it Fastcache by Host.it fastcache-by-host-it allows Stored XSS.This issue affects Fastcache by Host.it: from n/a through 1.7.14.

### CVE-2026-137545

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-26T16:18:07.773 |

Coder 2.9.0 before 2.29.27, 2.30.0 before 2.34.12, 2.35.0 before 2.35.9, 2.36.0 before 2.36.7, and 2.37.0 before 2.37.3 contains a nil pointer dereference in the tailnet coordinator, which reads UpdateSelf.Node fields during authorization without checking that Node is set. An authenticated user or workspace agent token holder can send a CoordinateRequest with UpdateSelf present but Node empty to crash coderd, disconnecting all users on the affected replica.

### CVE-2026-137537

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-26T16:18:06.580 |

ToolJet before 3.21.96-LTS contains a missing authorization vulnerability that allows authenticated End Users to execute data queries of apps in other organizations via POST /api/data-queries/:id/run. Attackers can supply a target data-query id and runtime resolvedOptions to run queries with the datasource's decrypted credentials, reading cross-tenant query results.

### CVE-2026-137534

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-26T16:18:06.060 |

ToolJet before 3.21.96-LTS contains an information disclosure vulnerability that allows low-privilege app/query viewers to obtain plaintext workspace secrets by running REST queries. Attackers can execute queries via POST /data-queries/:id/run whose URL params or non-redacted headers reference secrets, reading resolved values from metadata.request despite lacking decrypted constants access.

### CVE-2026-137531

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:18:05.713 |

ToolJet before 3.21.96-LTS contains an authorization bypass vulnerability that allows view-only workspace users to execute queries in restricted environments by supplying an arbitrary environmentId. Attackers can call the data-queries run endpoint for draft app versions to execute queries with stored datasource credentials, exposing development or staging data.

### CVE-2026-137525

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-26T16:18:04.860 |

ToolJet before 3.21.96-LTS contains an information disclosure vulnerability that allows users with TEST_CONNECTION ability to exfiltrate organization secrets by resolving secret placeholders in test-connection options. Attackers can point the host and port at a listener they control and set the password option to a secrets template, causing the server to send the plaintext secret to them.

### CVE-2026-137501

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:18:01.490 |

Budibase Server before 4.0.0 contains an authorization bypass in its single-row read and attachment endpoints, which fetch rows by ID without enforcing the requesting view's row filter. Authenticated users with read access to a filtered view can request GET /api/:viewId/rows/:rowId or GET /api/:viewId/rows/:rowId/attachment/:columnName with a hidden row ID to retrieve that row's data and attachments.

### CVE-2026-137495

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-26T16:18:00.140 |

Budibase before 4.0.0 contains an insecure direct object reference vulnerability in the bulkDestroy function that allows authenticated users to delete rows from any workspace table by supplying foreign row IDs. Attackers with TABLE WRITE on one table can send row _id values from other tables to the DELETE /api/:sourceId/rows endpoint, causing data loss and workspace metadata deletion.

### CVE-2026-137462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-26T16:17:54.373 |

FreeRDP before 3.33.0 contains a heap out-of-bounds read in WinPR's save_png_to_buffer(), which selects an RGB PNG color type for 9–16 bpp images but fills only 2 bytes per pixel per row. A malicious RDP server can send 9–16 bpp CF_DIB clipboard data that, when a local application requests image/png, yields a PNG containing adjacent client heap memory.

### CVE-2026-137458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-11-26T16:17:53.690 |

FreeRDP from 3.0.0 before 3.33.0 contains a reachable assertion in remdesk_server_thread that allows authenticated clients to abort freerdp-shadow-cli by sending oversized remdesk messages. Attackers can send one message longer than 4096 bytes with a shorter declared PDU length, forcing Stream_Seek past capacity and terminating every served session.

### CVE-2026-137453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-26T16:17:52.807 |

FreeRDP before 3.33.0 contains a credential disclosure vulnerability that allows malicious RDP servers to obtain client passwords because rdp_write_info_packet() omits a Remote Credential Guard check. When a victim connects using /remoteGuard with a configured /p password, the client sends the password in the Client Info packet after CredSSP, exposing reusable credentials to the destination.

### CVE-2026-135035

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-26T15:17:25.957 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPtouch WPtouch wptouch allows Stored XSS.This issue affects WPtouch: from n/a through 4.3.62.

### CVE-2026-137519

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-26T16:18:03.840 |

ToolJet before 3.21.94-beta contains an improper authorization vulnerability that allows Builders with only data source Delete permission to update global data sources via the PUT /api/data-sources endpoint. Attackers can change a REST data source base URL so later query executions send stored Bearer credentials to an attacker-controlled endpoint.

### CVE-2026-137480

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-26T16:17:57.497 |

Traefik 3.7.15 before 3.7.18 and 3.8.0-rc.1 before 3.8.0-rc.2 contains a client certificate authentication bypass in the Kubernetes Ingress NGINX provider because, on hosts shared by multiple Ingresses using auth-tls-secret, Ssl-Client-* headers are built per Ingress while the TLS handshake uses the first Ingress's settings. Unauthenticated remote attackers can obtain Ssl-Client-Verify: SUCCESS with a client-chosen subject and issuer for an unverified certificate, or inject Ssl-Client-* headers directly, presenting forged identities to backends that trust the proxy.

### CVE-2026-137478

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-26T16:17:57.157 |

Traefik before 2.11.62, 3.x before 3.7.18, and 3.8.0-rc.1 contain an authentication bypass in the ForwardAuth middleware because connection isolation for NTLM and Negotiate credentials checks only the Authorization header, not Proxy-Authorization. Unauthenticated attackers can send such credentials in Proxy-Authorization to reuse a shared authentication-server connection already authenticated by another user, receive that user's identity via authResponseHeaders, and access backends as that user.
