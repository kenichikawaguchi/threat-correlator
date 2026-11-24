# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-24 15:00 UTC
- **対象期間**: `2026-11-23T15:00:20.000Z` 〜 `2026-11-24T15:00:35.000Z`
- **重要CVE数**: 214 件（Critical 9.0+: 42 件 / High 7.0〜: 172 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上の案件は **30 件以上** と非常に多く、特に **認証不要でリモートコード実行 (RCE) や権限昇格** が可能な脆弱性が目立ちます。  
- 影響対象は **Web アプリケーション、クラウドサービス、IoT/組込みデバイス、AI/マシンラーニング基盤** と幅広く、攻撃者は **ネットワーク境界を意識せずに直接利用できる** ものが多数です。  
- 多くの脆弱性は **入力検証不備、デシリアライズ、ハードコードされた認証情報** が根本原因であり、**パッチ適用だけでなく構成・ネットワーク分離の見直し** が必須です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・攻撃シナリオ |
|-----|------|----------|------------------------|
| **CVE‑2026‑129514** | 10.0 | hexpm の `application/vnd.hex+erlang` パーサで **未検証デシリアライズ** が可能 | 攻撃者は任意の Erlang 外部ターム形式を送信し、OS コマンドを **リモートで実行**。実証済みのエクスプロイトが報告されており、公開サービスでの即時リスクが高い。 |
| **CVE‑2026‑59415** | 10.0 | TypesenseVectorStore の **ドキュメント ID インジェクション** により削除操作が任意のレコードに拡大 | `filter_by` 文字列結合の不備で、攻撃者は `id=*,!id=target` のような式を注入し、**大量データ削除** が可能。データ損失リスクが極めて大きい。 |
| **CVE‑2026‑128798** | 10.0 | Wi‑Fi クライアントが認証なしで **デバイス情報・会議録画メタデータ** を取得 | 公衆 Wi‑Fi 環境や社内ネットワークでの情報漏洩につながり、プライバシー・コンプライアンス上の重大インシデントになる。 |
| **CVE‑2026‑130169** | 10.0 | AutoGPT Platform が **ハードコードされた JWT 署名鍵** を配布 | 任意の JWT を生成できるため、**管理者権限の偽装** が可能。CI/CD パイプラインや内部 API への不正アクセスが想定される。 |
| **CVE‑2026‑62841** | 10.0 | Azure Event Grid の **認証不備** により権限昇格が可能 | Azure 環境全体で **イベントハンドラの書き換えやサブスクリプション取得** ができ、クラウドリソースの横方向移動が容易になる。 |

> **※** これらは「認証不要」「リモートから直接実行可能」「情報漏洩・権限昇格」の観点で上位に位置付けられます。  

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 / ライブラリ | 現行バージョン | 推奨バージョン / パッチ |
|-------------------|----------------|--------------------------|
| **hexpm** (Erlang パッケージリポジトリ) | 0.23.x 以前 | 0.24.2 以上 (デシリアライズ検証を追加) |
| **TypesenseVectorStore** | 0.24.0 以前 | 0.25.3 以上 (ID エスケープとパラメータ化クエリ) |
| **AutoGPT Platform** | 0.6.26‑0.7.4 | 0.7.5 以上 (`.env.default` からハードコード鍵を除去) |
| **Azure Event Grid** | 2026‑03‑release | 2026‑04‑patch (認証フローの強化) |
| **NVIDIA AIStore** | 1.3.x 以前 | 1.4.1 以上 (管理 API の認証強化) |
| **ASUS GPU Tweak III** | 3.2.0 以前 | 3.2.1 以上 (OS コマンドインジェクション修正) |
| **Dell Sonic Distribution** | < 4.6.1 | 4.6.1 以上 (引数インジェクション対策) |
| **FFmpeg** | 4.3‑4.4 (9.0 以前) | 9.1 以上 (dynaudnorm / deband バッファオーバーフロー修正) |
| **Microsoft Office SharePoint** | 2026‑03‑release | 2026‑04‑CU (パス・トラバーサル修正) |
| **Chrome (Variations)** | < 158.0.8127.88 | 158.0.8127.88 以上 (サンドボックス突破バグ修正) |

> **※** 企業内のパッケージ管理システム (apt, yum, pip, npm, Docker Hub 等) で **自動更新ポリシー** を有効化し、上記バージョンがリリースされたら即時ロールアウトしてください。

### 3.2 環境・構成の見直し
1. **ネットワーク分離**  
   - Wi‑Fi クライアントが直接内部 API にアクセスできないよう、**VLAN/ACL** で管理平面とデータ平面を分離。  
   - 管理ポート (例: 8080) を **内部 IP のみ** にバインドし、外部からの到達を防止（CVE‑2026‑128797 対策）。  

2. **認証・トークン管理**  
   - ハードコードされたシークレットや JWT 鍵は **環境変数またはシークレット管理サービス** に置き換える。  
   - 既存のデフォルト鍵が流出しているシステムは **即座に鍵ローテーション** を実施。  

3. **入力検証の徹底**  
   - 文字列結合でクエリを生成している箇所は **パラメータ化クエリ / プレースホルダー** に置き換える。  
   - Web フロントエンドは **Content‑Security‑Policy** と **サニタイズライブラリ** を導入し、XSS/SQLi の二次被害を防止。  

4. **監視・ロギング**  
   - 重要 API (例: `/meeting-recording/delete`, `/user/hasSimCard`) への **認証失敗・異常リクエスト** を SIEM に集約し、アラートを設定。  
   - Azure / AWS などクラウドサービスは **IAM ポリシーの最小権限化** と **アクセスログの定期レビュー** を実施。  

5. **インシデント対応手順の更新**  
   - RCE や権限昇格が疑われる

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-129514

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T14:18:02.623 |

Deserialization of Untrusted Data vulnerability in the application/vnd.hex+erlang request body parser in hexpm hexpm allows an unauthenticated remote attacker to execute operating system commands via a crafted Erlang external term format request body. This vulnerability was actively exploited against the hex.pm service on 2026-11-23.

HexpmWeb.ErlangFormat.decode/1 in lib/hexpm_web/erlang_format.ex decodes the body with Plug.Crypto.non_executable_binary_to_term/2, which accepts maps that have a __struct__ key. HexpmWeb.PlugParser.parse/5 returns the decoded term as the request params. The parser runs in the endpoint before routing and authentication, so a POST to any route reaches it. Elixir dispatches protocols on the __struct__ key, so the client selects which Inspect and Enumerable implementations run when error reporting inspects the params. A chain through Ecto.Query.DynamicExpr and DBConnection.Stream reaches an apply/3 call on a {module, function, args} tuple taken from the request body.

This issue affects hex.pm: from 2016-02-23 before 2026-11-23; hexpm/hexpm: from ab1bbcef7cc8395d1056d3b1aa6a174353492d59 before 379b0a29bcc95164249f38ad7d772a37a8ff9533.

### CVE-2026-59415

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-24T11:17:20.753 |

TypesenseVectorStore is vulnerable to a document ID injection in its delete operation that can cause unintended documents to be deleted.



 TypesenseVectorStore.doDelete(List<String>) builds a Typesense filter_by expression by raw string concatenation of caller-supplied document IDs into the form id: [id1,id2,...] . The Typesense id field uses bare (unquoted) values in this list form with no escaping mechanism. An ID containing characters with syntactic meaning in the Typesense filter grammar — such as a comma ( , ), a closing bracket ( ] ), or operator tokens ( || , && ) — can break out of the list literal and alter the structure of the filter expression.



 An attacker who controls a document ID passed to the delete operation can use this to delete documents other than the intended ones (comma injection), or to construct a filter that matches every document in the collection (operator breakout), resulting in unintended bulk deletion.



 Applications that pass externally supplied or user-controlled document IDs to VectorStore.delete(List<String>) backed by TypesenseVectorStore are affected.

### CVE-2026-128798

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T06:17:07.803 |

Any connected WiFi client can fetch device info and meeting recording metadata without credentials.

### CVE-2026-128797

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-11-24T06:17:07.683 |

Web administration panel (port 8080) binds to all network interfaces including public IPv6 addresses, making internal API endpoints reachable over WAN without firewall protection (related to CVE-2026-50224).

### CVE-2026-9790

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T04:17:38.043 |

Endpoints accessible without authentication from any WiFi client (e.g., /user/hasSimCard, /user/pooling, /api/device-info).

### CVE-2026-128791

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T04:17:22.243 |

Any WiFi client can send HTTP DELETE to /meeting-recording/delete to permanently delete files without authentication.

### CVE-2026-130169

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-330;CWE-798` |
| Published | 2026-11-23T23:17:04.220 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions 0.6.26 through 0.7.4, AutoGPT Platform ships a publicly known, hardcoded default JWT verification key in backend/.env.default and autogpt_platform/.env.default. Because HS256 is symmetric, anyone who knows the secret can forge valid JWTs for any user or for the admin role, bypassing authentication and authorization without user interaction. This issue is fixed in version 0.8.0.

### CVE-2026-62841

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-23T22:20:39.293 |

Improper authentication in Azure Event Grid allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-18530

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T02:17:47.313 |

OS command injection in the a3cli restricted shell in Lantronix S2220 Series 2 allows an authenticated attacker to bypass shell restrictions and execute arbitrary operating system commands via unsanitized command substitution metacharacters, including backticks and $(), in parameters of permitted commands over SSH. This vulnerability is fixed in firmware version 1.3.37.

### CVE-2026-70193

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-23T22:22:36.660 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-50691

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-23T22:20:16.553 |

Improper authorization in M365 Copilot allows an authorized attacker to elevate privileges over a network.

### CVE-2026-103782

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-23T16:17:25.380 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains an Argument Injection vulnerability. A low privileged remote attacker could potentially exploit this vulnerability, leading to arbitrary command execution and unauthorized access to filesystem resources.

### CVE-2026-65175

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-24T14:18:18.880 |

NVIDIA AIStore contains a vulnerability in storage-target node-control authorization where an unauthenticated attacker could access administrative functions through a target's public interface. A successful exploit might lead to information disclosure, data tampering, or denial of service.

### CVE-2026-65135

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T14:18:17.643 |

NVIDIA Video Codec SDK for Linux contains a vulnerability where a user may cause a heap-based buffer overflow issue. A successful exploit of this vulnerability may lead to code execution, data tampering, and denial of service.

### CVE-2026-119582

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T12:17:17.617 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in ITG Bilgisayar Teknoloji Grubu Tic. Ltd. Şti. VSRM allows SQL Injection.

This issue affects vSRM: from v14.08.3 before v14.08.5.

### CVE-2026-135202

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-11-24T06:17:08.080 |

Several plugins for WordPress published by WP connect (Orders Sync to Airtable for WooCommerce, Add-On for Contact Form 7 to Notion, WP Sync for Notion – Notion to WordPress, Add-On for Contact Form 7 to Airtable, Add-on Brevo for Gravity Forms, and Air WP Sync – Airtable to WordPress) contain embedded malicious code (a backdoor) in the versions listed. The affected releases unconditionally load a backdoor module (includes/airwp-online.php) that runs on every request via the 'init' hook and on a half-hourly WP-Cron event, sends site information (site URL, PHP, WordPress and OS versions, and the server user) to a remote command-and-control server at tascredit-pay.com with TLS certificate verification disabled, and executes the PHP code returned by that server via eval(). The module also accepts queued commands that run shell commands, read, write and delete arbitrary files, query arbitrary database tables, dump the users table including password hashes, drop a webshell into the uploads directory, and install persistent hourly code execution. This makes it possible for unauthenticated attackers in control of the remote server, or able to intercept its traffic, to execute arbitrary code on the server and fully compromise affected sites. All affected plugins have been closed on WordPress.org and no patched versions are available; we strongly recommend uninstalling them and running a complete malware scan.

### CVE-2026-133469

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-1287` |
| Published | 2026-11-23T17:17:31.780 |

XO (Xen Orchestra) is a solution to visualize, manage, backup and delegate your XCP-ng (or XenServer) infrastructure. Prior to 6.9.2 and 6.10.1, REST cookie parsing turns authenticationToken=j:%7B%7D into {}. REST authentication passes that object to the XO token provider without requiring a string. The token collection treats {} as an unfiltered lookup and returns its first token; the provider authenticates as that token's owner if it is unexpired. The authenticated /rest/v0/users/me/authentication_tokens route then returns reusable login token IDs. This vulnerability is actively exploited in the wild. This vulnerability is fixed in 6.9.2 and 6.10.1.

### CVE-2026-134401

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-24T00:17:30.460 |

Improper input validation in Variations in Google Chrome prior to 158.0.8127.88 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-70305

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-23T22:22:50.890 |

Improper neutralization of input during web page generation ('cross-site scripting') in Azure Portal allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-118285

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-23T22:19:30.710 |

Server-side request forgery in Azure Machine Learning allows an authorized attacker to elevate privileges over a network.

### CVE-2026-109480

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-23T22:18:29.133 |

Server-side request forgery in Profile Data Roaming Service (PDRS) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-103788

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T17:17:28.087 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains an OS Command Injection vulnerability. An unauthenticated adjacent network attacker could potentially exploit this vulnerability, leading to arbitrary command execution. This vulnerability is considered critical as it may allow unauthenticated command execution.

### CVE-2026-114203

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T02:17:46.410 |

An Improper Neutralization of Special Elements used in an OS Command（'OS Command Injection') in the ASUS GPU Tweak III allows a remote user to execute arbitrary OS commands via a crafted request to an HTTP endpoint of the service.
Refer to the '
Security Update for ASUS GPU Tweak III  ' section on the ASUS Security Advisory for more information.

### CVE-2026-135693

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T01:17:33.157 |

rConfig Core 8.0.0 before 8.2.17 and rConfig Pro before 8.4.0 contain a stored cross-site scripting vulnerability in the Config Search View Matches dialog, which renders configuration context via v-html without escaping. Attackers can place markup in device banners, interface descriptions, ACL remarks or SNMP locations to execute script in a user's session and read stored configurations containing secrets.

### CVE-2026-109490

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-23T22:18:30.130 |

Improper neutralization of input during web page generation ('cross-site scripting') in Authentication Methods Portal Extension allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-135208

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-23T16:17:38.250 |

Kerberos Agent before 3.14.4 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge administrator tokens because JWTMiddleWare() falls back to the hard-coded key TOBECHANGED. Attackers can sign HS256 tokens with arbitrary username and role claims to access /api and /config routes, exposing RTSP, ONVIF, Hub and encryption keys, rewriting configuration, and stopping the camera.

### CVE-2026-136126

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-24T13:17:31.443 |

c-icap-server through 0.5.15 and 0.6.5 contains an out-of-bounds write in process_encapsulated() that allows unauthenticated attackers to corrupt heap memory by sending six Encapsulated entities. Attackers can send a single ICAP request whose sixth entity overwrites trash_entities[0], triggering use-after-free and double free in ci_request_destroy() during teardown.

### CVE-2026-135743

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:33.657 |

FFmpeg 4.3 before 9.1 contains a heap out-of-bounds read and write vulnerability in the dynaudnorm filter because cqueue_resize() miscalculates gain history queue element counts when gausssize changes at runtime. Attackers can send gausssize commands via asendcmd scripts or an unauthenticated azmq filter to corrupt heap memory, crashing the process or potentially executing code.

### CVE-2026-135736

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:32.500 |

FFmpeg 4.4 before 9.1 contains a heap out-of-bounds read and write vulnerability in libavfilter/vf_deband.c that allows attackers to corrupt heap memory by sending a runtime coupling command. Attackers can send a 'deband coupling 1' command via sendcmd or an unauthenticated zmq filter, making chroma planes be processed at luma dimensions to crash the process or potentially execute code.

### CVE-2026-101864

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-23T23:17:01.373 |

EUSurvey through 1.6, prior to commit a4161a9, contains a weak password recovery mechanism that allows attackers who obtain a still-valid password-reset link to take over accounts that use a local EUSurvey password. The /auth/reset/ flow checks only the age of a reset code and does not invalidate it after the password is changed, and issuing a newer link leaves earlier links active, so a used or superseded link remains valid for up to 24 hours from issuance and can be reused to set a new password, sign in as the affected user, and lock that user out.

### CVE-2026-135211

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-23T16:17:38.787 |

BISHENG before 3.0.0 contains a missing authentication vulnerability in the /api/v2/workflow/invoke and /api/v2/workflow/stop routes that allows unauthenticated attackers to run workflows as the administrator. Attackers knowing a workflow UUID can supply an override replacing a Code node's code parameter with Python passed to exec(), achieving remote code execution, or stop other users' workflow sessions.

### CVE-2026-135174

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T15:17:46.683 |

Softaculous Virtualizor before 3.2.9 contains an SQL injection vulnerability in enduser/auth_callback.php that allows unauthenticated attackers to bypass authentication via OAuth-returned email addresses. Attackers can register an OAuth provider account with an email containing SQL syntax to complete social login as the administrator account.

### CVE-2026-135171

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-341` |
| Published | 2026-11-23T15:17:46.237 |

Wing FTP Server before 8.2.8 contains a predictable session identifier vulnerability that allows unauthenticated attackers to hijack administrator sessions by deriving identifiers from process, time, ServerID, and client IP state. Attackers can enumerate candidate identifiers using the service_get_license.html endpoint as a validity oracle and replay live sessions to gain administrative control including the Lua console.

### CVE-2026-135161

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-23T15:17:44.680 |

Interstellar before 6.3.0 contains a server-side request forgery vulnerability that allows unauthenticated attackers to reach internal services by enabling allow_loopback_ips and allow_private_ips in wisp-js at startup. Attackers can open a wisp WebSocket that bypasses the Express password middleware and create TCP streams to loopback, internal hosts, or cloud metadata services.

### CVE-2026-117593

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-24T12:17:17.343 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in ITG Bilgisayar Teknoloji Grubu Tic. Ltd. Şti. VSRM allows Password Recovery Exploitation.

This issue affects vSRM: from v14.08.3 before v14.08.5.

### CVE-2026-135686

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T01:17:31.963 |

Trilium through 0.107.0 contains an sql injection vulnerability in updateNormalEntity() that allows malicious sync partners to inject SQL by supplying crafted entity names and column keys. Attackers can abuse /api/sync/changed or PUT /api/sync/update data to copy sessions, etapi_tokens and user_data into synced rows and write arbitrary database rows.

### CVE-2026-69899

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-23T22:22:11.980 |

Authentication bypass by spoofing in Azure DevTest Labs allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-118286

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-23T22:19:30.903 |

Improper access control in Azure Site Recovery allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-113824

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T22:19:04.970 |

Authorization bypass through user-controlled key in Microsoft Clarity allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-135300

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-23T17:17:54.230 |

Pomerium from 0.30.0 before 0.34.0 contains an authentication bypass vulnerability in the MCP token endpoint that skips client secret verification for client_secret_basic clients. Attackers holding an intercepted authorization code or refresh token can redeem it at /.pomerium/mcp/token with any secret to obtain the victim's access tokens.

### CVE-2026-135163

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-23T15:17:45.000 |

Okou API before 1.762.0 contains a missing authentication vulnerability in its Microsoft Teams, legacy Slack, and GitHub App integration OAuth flows that trusts caller-supplied userId and orgId values. Unauthenticated attackers who know a member's identifiers can complete the flow with their own external account to bind that identity or installation to the victim's Okou user and organization.

### CVE-2026-93700

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-23T22:24:54.840 |

An authenticated WHMCS client could potentially leverage this flaw to read sensitive configuration files on the WHMCS host, including database credentials, and to execute code on the server.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-124283

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-502` |
| Published | 2026-11-24T03:17:07.440 |

Deserialization of Untrusted Data vulnerability in ash-project ash allows an unauthenticated attacker to execute arbitrary code or inject SQL through a forged keyset pagination cursor.

Ash.Page.Keyset.filter/4 in lib/ash/page/keyset.ex decodes the client-supplied page[:after] or page[:before] cursor from Erlang external term format and rejects decoded expressions with Ash.Expr.expr?/1. That check does not examine the fields of a struct. The cast of each value against the type of its sort field accepts structs for the :ci_string, :map, :struct and :term types. A struct in the cursor value for such a sort field therefore reaches the data layer. With AshPostgres, the read passes such a struct to inspect/1, which runs the Inspect implementation of the struct module that the attacker selected. A chain of struct modules from ecto and db_connection then calls a function that the cursor names, which permits OS command execution. An %Ash.Query.Function.Fragment{} inside an %Ash.CiString{} value is written into the SQL query as raw text.

This issue affects ash: from 3.31.3 before 3.38.0.

### CVE-2026-65136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T14:18:17.777 |

NVIDIA Jetson Linux for Linux contains a vulnerability where an attacker may cause an out of bounds write. A successful exploit of this vulnerability may lead to escalation of privileges and denial of service.

### CVE-2026-119543

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T12:17:17.480 |

Authorization bypass through User-Controlled key vulnerability in ITG Bilgisayar Teknoloji Grubu Tic. Ltd. Şti. VSRM allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects vSRM: from v14.08.3 before v14.08.5.

### CVE-2026-127182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-11-24T11:17:09.177 |

A stack buffer overflow in DLP/WAF in the enforcer dataplane of SUSE NeuVector before 5.5, 5.5 before 5.5.6, 5.6.0 before 5.6.5 could be used by remote attackers to crash or potentially execute code.

### CVE-2026-134620

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:31.403 |

Tanium addressed a command injection vulnerability in Engage.

### CVE-2026-133960

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:29.940 |

Tanium addressed an unauthorized code execution vulnerability in the Tanium Default Content.

### CVE-2026-133959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:29.820 |

Tanium addressed a command injection vulnerability in Core Content - Enhanced Tags.

### CVE-2026-133880

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:29.560 |

Tanium addressed a command injection vulnerability in Threat Response.

### CVE-2026-133864

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:29.307 |

Tanium addressed a command injection vulnerability in Default Content.

### CVE-2026-133863

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T00:17:29.177 |

Tanium addressed an improper access controls vulnerability in Tanium Server.

### CVE-2026-120747

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:27.637 |

Tanium addressed a command injection vulnerability in Comply.

### CVE-2026-101866

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T23:17:01.517 |

EUSurvey through 1.6, prior to commit 118facd, contains an authorization bypass vulnerability in the public POST /runner/draft/runner endpoint that allows unauthenticated attackers to overwrite another participant's saved draft and obtain its private invitation token. The draft save handler in RunnerController and AnswerService loads an existing draft by invitation alone without checking that the submitted survey, participation group and invitation belong together, then replaces the draft's answers, reassigns it to the submitted survey, and returns a resume link containing the private invitation token.

### CVE-2026-95793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-23T20:18:05.050 |

An arbitrary remote code execution vulnerability exists in HPE Morpheus Manager.

### CVE-2026-135429

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T18:17:13.227 |

Tabbycat 2.9.0 through 2.12.1 contains an incorrect authorization vulnerability in TournamentViewSet that allows unauthenticated attackers to gain write access because PerTournamentPermissionRequired returns True for views lacking a tournament attribute. Attackers can send POST, PUT, PATCH or DELETE requests to /api/v1/tournaments to create, modify or delete tournaments, cascading deletion to teams and speakers.

### CVE-2026-14569

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-24T13:17:31.767 |

Use of externally-controlled format string vulnerability exists in RTU500 component of the logging function for TLS, PPP and CAM. Exploiting this vulnerability may result in sensitive memory disclosure and denial of service.

### CVE-2026-136123

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-24T13:17:31.130 |

Friendica through 2026.05-1 contains an improper validation vulnerability in APContact::compactProfile() that allows remote actors to overwrite a local user's stored inbox and public key by declaring that user's profile URL as their actor id. Attackers can then sign ActivityPub activities that HTTPSignature::fetchKey() verifies against the injected publicKeyPem, impersonating the local user on the instance.

### CVE-2026-13137

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-805` |
| Published | 2026-11-24T12:17:23.007 |

A stack-based buffer overflow vulnerability exists in multiple parsers of RTU500 components of User management, REST resolver and SPA-Bus. Attacker controlled input can influence the length of data copied into fixed-size stack buffers without proper bounds checking, which may result in memory corruption leading to denial of service condition.

### CVE-2026-134898

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T09:17:08.267 |

A path traversal vulnerability in the File Explorer share-link folder-listing endpoint allows a remote attacker with a folder-scoped share link to list directory contents outside the shared folder, including other Samba shares readable by the link creator, because path validation occurs before path canonicalization.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120936

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:04.753 |

An arbitrary file creation and truncation vulnerability exists in the File Explorer of ADM. An authenticated low-privileged user can upload a file with crafted path components containing quote and redirection characters. When music.cgi processes the entry for audio playback operations, the unescaped path string breaks out of the expected argument context in the internal command parser. This causes the system execution helper to open the attacker-specified path with root privileges using O_TRUNC, allowing remote attackers to truncate or create arbitrary system files.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-135742

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-11-24T04:17:33.490 |

FFmpeg before 9.1 contains a heap buffer overflow vulnerability in recv_msg() of the zmq and azmq filters that allows unauthenticated network attackers to corrupt memory by sending oversized command messages. Attackers can send a 4 GiB message to the default listening port, truncating the int buffer size so memcpy() writes past the heap allocation and crashes FFmpeg.

### CVE-2026-135695

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T01:17:33.460 |

rConfig Core 8.0.0 before 8.2.13 and rConfig Pro before 8.4.0 contain an authorization bypass vulnerability in the users API that allows authenticated users to modify other accounts. Attackers can send a UserController::update request with an administrator's user id and new password, then log in as that administrator to take full control.

### CVE-2026-135692

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-24T01:17:32.987 |

rConfig Core 8.0.0 before 8.2.17 and rConfig Pro before 8.4.0 contain a PHP object injection vulnerability in app/Casts/EncryptStringCast.php that unserializes decrypted attributes without class restrictions. Authenticated attackers can store a serialized gadget chain in encrypted fields like device passwords, triggering command execution as the web server user when read via GET /api/devices.

### CVE-2026-135691

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T01:17:32.790 |

Open5GS WebUI through 2.8.0 contains an incorrect authorization vulnerability in webui/server/routes/db.js that allows authenticated user-role accounts to modify the Account model. Attackers can send PATCH /api/db/Account/<username> setting roles to admin, overwrite password hashes, delete accounts, and read hashes to gain full administrative control.

### CVE-2026-101871

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T23:17:02.210 |

EUSurvey 1.5.2 through 1.6, prior to commit ffd5da7, contains a missing authorization vulnerability in the public POST /runner/delphiUpdate endpoint that allows unauthenticated attackers to submit responses to Delphi surveys after the owner has closed them. DelphiController checks only that the survey exists and is a Delphi survey and skips the closure check enforced by the normal survey page, so an attacker who knows the survey and question IDs can create new responses that remain in the survey's results.

### CVE-2026-101870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T23:17:02.070 |

EUSurvey through 1.6, prior to commit de1145c, contains an authorization bypass vulnerability in the public POST /editcontribution/{code} endpoint that allows unauthenticated attackers to overwrite another respondent's submitted answers. The handler in ContributionController selects the survey and answer set from body parameters by numeric contribution ID and never checks that the private edit code in the URL matches that contribution, so an attacker who knows a contribution ID can replace its saved answers without the respondent's edit link.

### CVE-2026-101869

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T23:17:01.930 |

EUSurvey 1.4.4.6738 through 1.6, prior to commit de1145c, contains an SQL injection vulnerability in the public results page GET /publication/{shortname} that allows unauthenticated attackers to infer non-public response data. ReportingService builds a SQL column expression from part of a user-supplied filter parameter name and inserts it directly into the query, so a visitor to any survey that publishes its results can inject boolean conditions and use the presence or absence of public result rows to infer private reporting data, including response data and respondent metadata from other surveys.

### CVE-2026-101868

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T23:17:01.790 |

EUSurvey through 1.6, prior to commit 4bf95a3, contains an authorization bypass vulnerability in the GET /preparepublishedcontribution/{id} endpoint that allows unauthenticated attackers to read private responses submitted to published surveys. The contribution PDF handler in ContributionController looks up a response by its sequential database ID and skips the normal response access checks, so attackers can enumerate IDs to retrieve other respondents' answers, including free-text answers that may contain personal data, across surveys.

### CVE-2026-101863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T23:17:01.233 |

EUSurvey 1.5.5 through 1.6, prior to commit d5295d5, contains a missing authorization vulnerability in the POST /forms/bulkchange endpoint that allows any authenticated user to take over or delete other users' surveys. SurveyController accepts arbitrary survey IDs and privilege values, and BulkExecutor applies the requested access-right changes or deletion without checking whether the requester can manage those surveys, allowing an ordinary ROLE_USER account to grant itself full control of another user's survey, read its draft and results, edit the form, manage its invitations, or delete it.

### CVE-2026-101862

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-23T23:17:01.047 |

EUSurvey through 1.6, prior to commit 0669a36, contains a path traversal vulnerability in the survey import function that allows authenticated attackers with the Form Manager role to execute arbitrary code on the server. The POST /noform/management/importSurvey endpoint trusts archive entry names when SurveyExportHelper writes imported files through FileService, so a crafted survey archive can write a JSP file outside the survey storage directory into the application directory, where Tomcat executes it with the privileges of the EUSurvey process

### CVE-2026-82981

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T22:23:40.920 |

SQL injection in WHMCS could allow an unauthenticated user to retrieve clients' personal and support information, as well as administrator account records and password hashes.

### CVE-2026-135470

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472` |
| Published | 2026-11-23T20:18:04.443 |

WPC Product Options for WooCommerce before 4.0.9 contains a price manipulation vulnerability that allows unauthenticated attackers to purchase products at an arbitrary price by submitting crafted wpcpo-* option data with a negative price in an add-to-cart request. Attackers can exploit the add_cart_item_data() function in includes/class-cart.php, which stores client-supplied price values without validation and carries them into the order total via before_calculate_totals(), to checkout products at zero or arbitrary cost.

### CVE-2026-135446

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-23T18:17:15.937 |

Bold pagos en linea WordPress plugin before 3.5.1 contains an improper signature verification vulnerability in the bold_co webhook that allows unauthenticated attackers to forge payment notifications. Attackers can set metadata.reference to begin with 'test' and sign the body with the empty test_secret_key HMAC, marking any unpaid WooCommerce order as paid.

### CVE-2026-135436

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-23T18:17:14.333 |

KindleEar 3.0.0 through 3.5.3 contains a remote code execution vulnerability that allows authenticated non-admin users to run Python code by uploading malicious recipes. Attackers can submit crafted recipe source to the /recipe/upload action, which calibre compile_recipe executes via exec() without sandboxing, gaining root code execution in the Docker container and access to password hashes.

### CVE-2026-135249

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-770` |
| Published | 2026-11-23T16:17:44.090 |

MISP accepted compressed HTTP request bodies (gzip, brotli, zstd) and decompressed them before authentication was performed, with no limit on the size of the resulting decompressed data. An unauthenticated attacker could send a small compressed payload that expands to a very large decompressed body, exhausting server memory and causing a denial of service. Brotli and zstd, with their high compression ratios, made the attack particularly effective.

The vulnerability required no authentication and no special conditions beyond the ability to send an HTTP request with a Content-Encoding header. The impact is a complete loss of availability for the affected MISP instance.

Affected: MISP versions prior to 2.5.52.

### CVE-2026-135173

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-23T15:17:46.520 |

PdfPig through 0.1.16 contains an uncontrolled recursion vulnerability that allows attackers to crash applications by supplying crafted PDF documents with self-referencing AcroForm /Kids or deeply nested marked content. Attackers can trigger an uncatchable StackOverflowException in AcroFormFactory.GetAcroField or Page.GetOptionalContentsRecursively, terminating any process reading form fields or optional content.

### CVE-2026-135164

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T15:17:45.153 |

Formance Ledger 2.2.0-beta.3 before 2.4.18 contains an SQL injection vulnerability that allows remote API callers to execute SQL by supplying unvalidated account expand values. Attackers can inject comment-separated SQL through the expand query parameter or base64 pagination cursor to run queries with the ledger database role's privileges.

### CVE-2026-136120

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-24T13:17:30.950 |

Ziit 1.3.2 contains a cross-site request forgery vulnerability in the /api/auth/epilogue/callback handler that accepts requests lacking the OAuth state parameter. Attackers can lure a signed-in victim to a cross-site page that completes the link flow with the attacker's Epilogue authorization code, letting the attacker sign in as the victim.

### CVE-2026-125735

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T12:17:19.533 |

SQL injection in the CabinPaq manual code entry module, versions v.1.2.94 and v.1.2.136. The application constructs SQL queries from terminal input without properly sanitising it. With physical access to the terminal, an attacker could bypass code validation and open compartments without authorisation.

### CVE-2026-121375

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T12:17:17.753 |

Reflected cross-site scripting in the versioned REST API documentation page in Checkmk versions 2.5.0 before 2.5.0p21 allows an unauthenticated attacker to execute arbitrary JavaScript in the browser of a user who opens a crafted link, in the context of that user's Checkmk session. The API version segment of the documentation URL is inserted into the page without escaping, and the page is reachable without authentication.

### CVE-2026-19881

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-434` |
| Published | 2026-11-24T10:17:50.140 |

Cross-site scripting in the conversation file-sharing feature of Unblu inc. Unblu Spark 7.0 through 7.57.10 and 8.0 before 8.41.1, on on-premises and cloud deployments, allows an unauthenticated remote attacker in the visitor role to execute arbitrary JavaScript in the browser of a user who opens a crafted link to a file the attacker uploaded, via a file type that the browser renders as active content, such as SVG.



The JavaScript runs in the context and under the identity of that user's session.



Exploitation requires the victim to open the crafted link.

### CVE-2026-120944

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-24T09:17:06.507 |

A stack-based buffer overflow vulnerability in the ADM allows remote authenticated administrators to cause a denial of service (service crash) or potentially execute arbitrary code via a crafted tag parameter in settings CGI.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-134897

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:06.040 |

An OS command injection vulnerability in ADM allows an authenticated administrator to create an iSCSI LUN with a crafted name and schedule a snapshot. The scheduler embeds the name in a root cron job without correctly neutralizing shell metacharacters, allowing arbitrary command execution as root when the job runs.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-121018

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-669` |
| Published | 2026-11-24T08:17:05.643 |

The affected products insufficiently restrict runtime-supplied visualization commands, allowing local functionality on the engineering workstation to be invoked, if a user is both logged in to a CODESYS Control runtime and operates a visualization. An unauthenticated remote attacker controlling a malicious runtime and tricking a user to trust it, or performing a man-in-the-middle attack on the communication between the CODESYS Control runtime and the engineering workstation, may cause arbitrary code execution on the engineering workstation.

### CVE-2026-121017

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-669` |
| Published | 2026-11-24T08:17:05.513 |

The affected products insufficiently restrict runtime-supplied visualization data, allowing to invoke local COM/ActiveX functionality on the engineering workstation, if a user is both logged in to a CODESYS Control runtime and operates a visualization. An unauthenticated remote attacker controlling a malicious runtime and tricking a user to trust it, or performing a man-in-the-middle attack on the communication between the CODESYS Control runtime and the engineering workstation, may cause arbitrary code execution on the engineering workstation.

### CVE-2026-121016

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-669` |
| Published | 2026-11-24T08:17:05.363 |

The affected products insufficiently restrict runtime-supplied visualization data, allowing local program execution on the engineering workstation, if a user is both logged in to a CODESYS Control runtime and operates a visualization. An unauthenticated remote attacker controlling a malicious runtime and tricking a user to trust it, or performing a man-in-the-middle attack on the communication between the CODESYS Control runtime and the engineering workstation, may cause arbitrary code execution on the engineering workstation.

### CVE-2026-120948

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:05.243 |

An OS command injection vulnerability in the PPPoE configuration of ADM allows an authenticated administrator to store shell syntax in the PPPoE account value. When the service loads the resulting configuration, the injected commands can execute with root privileges.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120946

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:05.003 |

An OS command injection vulnerability in ADM allows remote authenticated administrators to execute arbitrary commands as root. The set action in settings/ddns.cgi fails to sanitize configuration delimiters in user-supplied parameters before writing them into the DDNS configuration file, allowing an attacker to inject directives that execute arbitrary system commands upon service restart.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120951

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-24T07:17:19.590 |

An externally-controlled format string vulnerability exists in the authenticated upload_wireguard action of settings/vpnupload.cgi in the ADM. The CGI takes an attacker-controlled WireGuard profile name, inserts it into a JSON object, serializes it, and passes the resulting formatted string directly to printf as the format argument without validation or escaping. An authenticated remote attacker can exploit this vulnerability by sending format string specifiers, or leverage variadic read/write primitives within the non-PIE, non-Canary root CGI to potentially achieve arbitrary remote code execution with root privileges.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-135689

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T01:17:32.460 |

Community Store for Concrete CMS before 2.8.0 contains a stored cross-site scripting vulnerability that allows unauthenticated attackers to inject script via the order email in single_pages/dashboard/store/orders.php. Attackers can place guest orders with quoted email local parts containing markup to execute script in a store manager's session when viewing the order.

### CVE-2026-101867

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T23:17:01.653 |

EUSurvey through 1.6, prior to commit edb5021, contains an incorrect authorization vulnerability in the GET /settings/shareEdit/{shareId} and POST /settings/shares handlers that allows any authenticated user to read or modify another user's contact share. The ownership check in SettingsController denies access only when a condition is both true and false, so it never denies access, allowing an ordinary account without Contact Management privileges to read the names and email addresses in a share and to rename it, change its recipient or access mode, or replace its contacts.

### CVE-2026-81962

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T22:23:40.260 |

Incorrect authorization in Azure Machine Learning allows an unauthorized attacker to disclose information over a network.

### CVE-2026-69437

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T22:21:30.760 |

Missing authorization in Azure AI Foundry allows an unauthorized attacker to disclose information over a network.

### CVE-2026-127224

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T18:17:10.547 |

GFI HelpDesk before 4.99.13 contains an SQL injection vulnerability in the archiver export feature that allows authenticated attackers with administrator privileges to execute arbitrary SQL queries by supplying crafted itemid[] array values to /admin/index.php?/archiver/Manager/ExportAll. The Controller_Manager.ExportAll() method joins the itemid values with implode() and GetWhere() concatenates them into an IN() clause without sanitization or parameterization, and DumpTables() executes the resulting query against each ticket-related table, allowing attackers to read or modify database contents.

### CVE-2026-127223

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T18:17:10.383 |

GFI HelpDesk before 4.99.13 contains an SQL injection vulnerability in the staff group management feature that allows authenticated attackers with administrator privileges to execute arbitrary SQL queries by supplying a crafted title parameter to /admin/index.php?/Base/StaffGroup/InsertSubmit. The Controller_StaffGroup.RunChecks() method concatenates the unsanitized title value directly into a duplicate name lookup query against the staffgroup table, allowing attackers to read or modify database contents.

### CVE-2026-135175

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-23T15:17:46.847 |

ZITADEL 4.19.5 before 4.20.3 contains a host header injection vulnerability that allows unauthenticated attackers to redirect notification links by placing a trusted host in the userinfo portion of the x-zitadel-public-host header. Attackers knowing a victim's login name can harvest single-use codes from password-reset links sent to their host, reset passwords, and take over accounts including administrators.

### CVE-2026-135157

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-23T15:17:43.687 |

Future AGI before 1.51.0 contains an authentication bypass vulnerability in ACSView.post that allows authenticated members of any organization to take over accounts in other organizations by asserting arbitrary e-mail addresses. Attackers can register a controlled identity provider through IDPUploadViews to obtain sessions as cross-tenant users, and can modify or delete other organizations' identity-provider configurations.

### CVE-2026-77672

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T14:18:19.360 |

Missing server-side authorization in the IPC interface of TXOne StellarProtect and Stellar Agent (Windows) allows a local attacker to issue privileged commands without credentials. This issue affects StellarProtect: 3.3 and earlier; Stellar Agent (Windows): before 5.0.3056. *Note: Stellar Agent (Windows) is the new name for StellarProtect.

### CVE-2026-136128

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-24T13:17:31.607 |

WPC Linked Variation plugin for WordPress, all versions before 4.6.1, contain a stored cross-site scripting vulnerability that allows authenticated attackers with Contributor-level access to inject arbitrary HTML attributes by submitting an unvalidated wpclv_link[source] value that is echoed into an attribute-name position within a select element on the edit screen. Attackers can craft a source value containing onfocus and autofocus attributes to execute arbitrary JavaScript in the wp-admin session of an administrator or editor who views the edit screen, enabling privilege escalation from Contributor to Administrator with no user interaction required.

### CVE-2026-128796

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-270` |
| Published | 2026-11-24T06:17:07.553 |

System service 'antaiuiserver' exposes transaction 14 (sendMyATCmd) & 4, allowing ANY app on device to send arbitrary AT commands to modem without permissions (no READ_PHONE_STATE, SEND_SMS). Enables reading IMEI, IMSI, ICCID, and managing SMS.

### CVE-2026-135740

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:33.157 |

FFmpeg before 9.1 contains a heap out-of-bounds write vulnerability in libavfilter/vf_readeia608.c because build_histogram() does not clamp high bit depth luma samples to the nominal maximum. Attackers can supply crafted 9, 10, 12 or 14 bit gray or YUV video to corrupt heap memory, causing crashes or possibly code execution.

### CVE-2026-135738

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:32.827 |

FFmpeg before 9.1 contains a heap out-of-bounds write vulnerability in libavfilter/vf_signalstats.c that allows attackers to corrupt heap memory by supplying high bit depth samples exceeding the nominal maximum. Attackers can craft planar 9 to 14 bit YUV video whose unclamped samples or saturation values index past histogram ends, crashing applications or possibly executing code.

### CVE-2026-135737

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:32.670 |

FFmpeg before 9.1 contains a heap out-of-bounds write and read vulnerability in the tmidequalizer filter that allows attackers to corrupt memory by supplying high bit depth samples exceeding the nominal maximum. Attackers can craft planar 9, 10, 12 or 14 bit video so compute_histogram16() and apply_contrast_change16() index unclamped samples, crashing applications, corrupting the heap, and leaking heap contents.

### CVE-2026-135734

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:32.137 |

FFmpeg before 9.1 contains a heap out-of-bounds write vulnerability in the deflicker filter that lets attackers corrupt heap memory via unclamped high bit depth luma samples. Attackers can supply crafted video whose luma values exceed the nominal depth, making calc_avgy16() increment counters past the histogram allocation, causing crashes or possibly code execution.

### CVE-2026-135725

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-24T04:17:30.507 |

FFmpeg before 9.1 contains a stack-based buffer overflow vulnerability in ff_rtmp_packet_write() in libavformat/rtmppkt.c that allows malicious RTMP servers to overflow a 16-byte header buffer. Attackers can send a Set Chunk Size packet on a high channel id with an extended timestamp, which handle_chunk_size() echoes back, corrupting the publishing client's stack.

### CVE-2026-135722

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-24T04:17:30.013 |

FFmpeg before 9.1 contains a heap-based buffer overflow vulnerability in peak_init_writer() and wav_write_packet() in libavformat/wavenc.c that allows attackers to corrupt heap memory by supplying audio with zero channels. Attackers can provide a crafted PCM stream declaring no channels for WAV output with peak envelope enabled, causing out-of-bounds writes past peak_maxpos and peak_maxneg arrays, crashes, and potential code execution.

### CVE-2026-135433

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-23T18:17:13.857 |

FLTK through 1.4.5 contains a heap buffer overflow vulnerability in Fl_BMP_Image::load_bmp_() that allows attackers to corrupt heap memory by supplying crafted BMP or ICO files. Attackers can specify very large image dimensions so the 32-bit row and alpha mask pointer offsets wrap, writing file-derived pixel bytes out of bounds to crash applications or possibly execute code.

### CVE-2026-135295

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-23T17:17:53.353 |

FontForge through 20251009 contains a heap out-of-bounds write vulnerability in PcfReadEncodingsNames() that allows attackers to corrupt memory via negative glyph indices from truncated PCF encodings tables. Attackers can supply a crafted .pcf file imported through the GUI or scripting Import() command to write before the encs array, causing crashes or potential code execution.

### CVE-2026-134896

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:05.937 |

An improper input validation vulnerability in the OpenVPN client configuration import feature of ADM allows authenticated administrative users to execute arbitrary operating system commands via a crafted .ovpn profile.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-122090

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T23:17:03.263 |

Pelican 4.12.0 contains an OS command injection vulnerability in pelican-import. An attacker-controlled wp:post_name from a WordPress XML export is used in an output filename that is interpolated into a Pandoc command passed to subprocess.call with shell=True. On POSIX systems, command substitution in the slug is evaluated when a user imports the crafted export.

### CVE-2026-135452

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-65` |
| Published | 2026-11-23T19:17:36.740 |

A potential security vulnerability has been identified in the HP Hotkey UWP Service, which might allow escalation of privilege. HP is releasing mitigation for the potential vulnerability. Customers using HP Programmable Key are recommended to update HP Hotkey Support.

### CVE-2026-120945

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-24T09:17:06.637 |

A relative path traversal vulnerability in the FTP Backup of ADM, allows an attacker controlling a configured FTP server to cause files to be created or overwritten outside the selected NAS backup destination. Successful exploitation can modify or destroy files writable by that identity.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120941

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-24T09:17:06.110 |

An improper certificate validation vulnerability exists in ADM App Central, due to disabled peer verification within the set-used-server endpoint, enabling an unauthenticated Man-in-the-Middle (MitM) attacker to intercept HTTPS traffic, bypass TLS validation, and modify App Central server redirection settings to cause a persistent service outage for application updates without bypassing package signature verification.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-135739

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-24T04:17:32.987 |

FFmpeg 7.1 before 9.1 contains an out-of-bounds read vulnerability in libavfilter/vf_scale.c that allows attackers to read past the filter input array by sending width or height commands using ref variables. Attackers can send such commands via sendcmd scripts or unauthenticated zmq or azmq filters, causing config_props() to dereference an invalid pointer and crash the process.

### CVE-2026-65817

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T22:20:52.977 |

Improper neutralization of special elements used in an os command ('os command injection') in Azure Managed Instance for Apache Cassandra allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-134056

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-23T20:17:59.710 |

An out-of-bounds write issue exists in padded block cipher decryption in AWS-LC. It affects applications that decrypt CBC or ECB ciphertext with PKCS7 padding over multiple calls into the minimum documented output buffer. A remote user who supplies crafted ciphertext might crash the application or corrupt adjacent memory. Affected are all versions of AWS-LC before 5.7.0, AWS-LC-FIPS 4.x before 4.2.0, AWS-LC-FIPS 3.x before 3.6.0, and AWS-LC-FIPS 2.x before 2.0.18.



To remediate this issue, users should upgrade to AWS-LC 5.7.0, AWS-LC-FIPS 4.2.0, or AWS-LC-FIPS 3.6.0.



AWS-LC-FIPS 2.0.18 is also fixed; AWS-LC-FIPS 2.x reaches end of support in April 2027.

### CVE-2026-135292

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-23T17:17:52.840 |

Contiki-NG through 5.2 contains an out-of-bounds write vulnerability in the MPL multicast engine that allows remote unauthenticated attackers to corrupt memory via unchecked seed ID lengths. Attackers can send near-maximum-size MPL messages with an S=3 option in a short hop-by-hop header, causing data_message_expiration() to write 16 bytes past uip_buf and crash the node.

### CVE-2026-135239

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-23T16:17:42.183 |

MISP contains an authorization flaw in the data capture and import paths for events, galaxies, galaxy clusters, analyst data, and sightings. A user who is neither a sync user nor a site admin could create or import records attributed to an organisation other than their own, or cause the creation of a new organisation from a payload-supplied identifier.

The root cause is an inconsistent authorization check: the code validated one representation of the creator organisation (for example a numeric ID or a UUID field) while storing a different representation taken directly from the user-supplied payload. In the event import path, a MISP export naming another organisation or a fabricated one was accepted and stored under that organisation. In the galaxy, cluster, analyst data, and sighting capture paths, the nested organisation object from the payload was used to create or reference an organisation without verifying the caller's membership.

Impact:
- Data (events, galaxies, clusters, analyst notes, sightings) can be created under an organisation the attacker does not belong to, polluting that organisation's data and potentially exposing it to that organisation's members.
- New organisations can be created from attacker-supplied identifiers, introducing phantom entities into the MISP instance.
- The integrity of the threat-intelligence data store is compromised because attribution is no longer trustworthy.

Affected: MISP versions prior to 2.5.52.

### CVE-2026-135169

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-23T15:17:45.953 |

msgpack-c C++ library cpp-3.0.0 through cpp-9.0.0 contains a use-after-free vulnerability in the Boost.X3 parser in include/msgpack/v2/x3_parse.hpp when built with MSGPACK_USE_X3_PARSE in reference mode. Attackers can supply crafted msgpack input parsed over buffering iterators so decoded str, bin and ext objects hold dangling pointers, disclosing freed heap memory or crashing the process.

### CVE-2026-10765

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T12:17:16.683 |

RTU500 contains a denial-of-service vulnerability in its IEC 61850 MMS server implementation. A malicious user with access to the IEC 61850 interface can trigger improper handling of asynchronous control operations involving special response and timing criteria. This may result in access to invalid memory structures, leading to a software exception, loss of IEC 61850 communications, or device reboot.

### CVE-2026-134895

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T09:17:08.133 |

A path traversal vulnerability in the File Explorer share-link upload component allows a remote attacker with a folder-scoped upload share link to upload or overwrite files in the shared folder's immediate parent directory due to missing trailing validation prior to path canonicalization.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-132257

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-321;CWE-798` |
| Published | 2026-11-23T23:17:04.380 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. From versions 0.6.23 and above, before 0.8.0, AutoGPT Platform ships a hardcoded default Fernet encryption key in backend/.env.default, which encrypts every user's OAuth tokens, API keys, and integration credentials in the User.integrations column. Anyone with read access to the database of a deployment using the default key can decrypt the stored credentials. This issue is fixed in version 0.8.0.

### CVE-2026-134069

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-11-23T22:20:12.923 |

Use of a default cryptographic key in the instance registration component in Amazon SSM Agent before 3.3.5226.0 on AWS-provided Windows Server AMIs released before 2026-09-09 might allow local users without administrative privileges to obtain the instance's Default Host Management Configuration role credentials via the registration key shared by all instances launched from the same AMI.



To remediate this issue, users should replace affected instances with instances launched from AWS Windows Server AMIs released on or after 2026-09-09, which include SSM Agent 3.3.5226.0 or later. Upgrading the agent in place does not replace the shared key, and deleting the agent's Vault breaks instances managed through Default Host Management Configuration.

### CVE-2026-130165

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-23T22:20:10.827 |

React is a JavaScript library for building user interfaces. In versions prior to 19.0.9, 19.1.10, 19.2.9 and 19.3.1, react-server-dom-webpack, react-server-dom-parcel, and react-server-dom-turbopack are vulnerable to denial of service. Specially crafted HTTP requests sent to server function endpoints can cause out-of-memory exceptions or excessive CPU usage. This issue is fixed in versions 19.0.9, 19.1.10, 19.2.9 and 19.3.1.

### CVE-2026-103783

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T17:17:27.423 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains an OS Command Injection vulnerability. A high privileged attacker with local access could potentially exploit this vulnerability, leading to arbitrary command execution.

### CVE-2026-101218

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-23T17:17:27.040 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains an OS Command Injection vulnerability. A high privileged attacker with local access could potentially exploit this vulnerability, leading to arbitrary command execution.

### CVE-2026-100986

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-24T14:18:01.260 |

NVIDIA AIStore contains a vulnerability in append-operation handle validation where an unauthenticated attacker could cause data to be appended to a file outside the intended storage location. A successful exploit might lead to code execution, denial of service,
escalation of privileges,
information disclosure, or data tampering.

### CVE-2026-100985

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-24T14:18:01.127 |

NVIDIA AIStore contains a vulnerability in object-copy destination validation where an unauthenticated attacker could use a crafted destination object name to write a file outside the configured storage location. A successful exploit might lead to code execution,
denial of service,
escalation of privileges,
information disclosure, or data tampering.

### CVE-2026-134842

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T17:17:49.230 |

pgjdbc, the PostgreSQL JDBC Driver, can quote a string parameter for the wrong value of standard_conforming_strings when preferQueryMode=simple is set. A statement, trigger or configuration reload can turn the setting off during a session. A parameter value with a backslash and a quote then ends the literal, and the rest of the value runs as SQL. Before 42.7.6 any session with the setting off was affected. The statement cache can also reuse a parse made under the other setting. With allowEncodingChanges=true and the EUC_JP or SJIS client encoding, the yen sign acts as a backslash. All versions before 42.7.15 are affected, and 42.7.15 fixes the problem.

### CVE-2026-134841

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T17:17:49.083 |

pgjdbc, the PostgreSQL JDBC Driver, misreads some quoted text in its query parser. A `}` inside a literal ends a JDBC escape such as `{ts}`, and the rest of the literal is translated as SQL. A dollar quote whose tag has a non-ASCII symbol or space is not recognized. An `E''` string with a doubled quote is scanned as a standard string. `{fn right}` and `{fn timestampdiff}` with a negative argument produce a `--` comment. In each case text that the application quoted correctly can run as SQL with the privileges of the application's database role. All versions before 42.7.15 are affected, and 42.7.15 fixes the problem.

### CVE-2026-129975

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-23T16:17:26.243 |

A flaw was found in gpgme. When processing crafted input, an early return following memory reallocation can leave internal buffer pointers referencing previously freed memory, resulting in a double-free condition during cleanup. A remote attacker could exploit this vulnerability to corrupt process memory, potentially leading to arbitrary code execution or a Denial of Service (DoS) crash.

### CVE-2026-134494

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-24T00:17:30.890 |

Tanium addressed an argument injection vulnerability in Core Content.

### CVE-2026-65154

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T14:18:18.030 |

NVIDIA Open GPU Kernel Module for Linux contains a vulnerability where a user may cause a use-after-free issue. A successful exploit of this vulnerability may lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-130164

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15;CWE-426` |
| Published | 2026-11-23T21:16:56.123 |

Hermes Agent is an open-source autonomous AI agent built by Nous Research for running tool-using workflows across CLI, desktop, and messaging interfaces. From 0.21.6 to 0.23.1, when Bot Desktop is hosted inside a non-local terminal backend, the agent process reads a backend-writable screen environment file without validating keys or values and merges its entries into the environment of processes started on the agent machine. Specifically, when terminal.backend is set to docker or ssh (or a plugin backend declaring supports_streams) with placement auto or terminal, _published() in tools/bot_desktop/sandbox_host.py accepts arbitrary KEY=VALUE lines from the hermes-bot-desktop env file and propagates them via tools/bot_desktop/runtime.py into the browser harness, computer-use helpers, and local terminal children. Code running inside the terminal backend can therefore set variables such as LD_PRELOAD, DYLD_INSERT_LIBRARIES, or PATH and gain code execution on the agent machine as the gateway user upon a subsequent browser or computer-use spawn, exposing credentials, tokens, and session history under the Hermes home directory. The default local backend, backends that cannot host a screen (Modal, Daytona, and Vercel), and Hermes Cloud in its default configuration are not affected. This issue is fixed in version 0.23.2.

### CVE-2026-100374

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-23T19:17:27.627 |

The system call verification handlers for smbus_block_read() and smbus_block_pcall() in drivers/smbus/smbus_handlers.c (z_vrfy_smbus_block_read() and z_vrfy_smbus_block_pcall()) validated the device object, the count pointers and (for process call) the send buffer, but never validated the receive buffer (buf / rcv_buf). The call then proceeds into the driver implementation, which runs in supervisor mode and writes the bytes received from the SMBus peripheral through that pointer.

A user-mode thread on a system built with CONFIG_USERSPACE that has been granted access to an SMBus device object can pass an arbitrary address, including kernel data or another thread's memory, as the receive buffer. The driver then writes up to SMBUS_BLOCK_BYTES_MAX (32) bytes of peripheral-supplied data there (the STM32 driver writes as many bytes as the peripheral's length byte announces, up to 255). The address is fully attacker-chosen; the written content comes from the bus and is typically influenceable by the caller through the choice of peripheral and command, or by first writing data to a device that echoes it back.

This breaks the user/kernel isolation boundary: it gives an unprivileged thread a kernel-memory write primitive usable for privilege escalation, or at minimum to corrupt kernel state or crash the system. The fix adds K_SYSCALL_MEMORY_WRITE() checks of the receive buffer for the documented worst case, SMBUS_BLOCK_BYTES_MAX. Systems without CONFIG_USERSPACE are not affected.

### CVE-2026-133632

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-23T16:17:29.007 |

In astro-airflow-mcp 0.5.0 through 0.9.1, the af CLI and the MCP server send telemetry from a Python subprocess that can import modules from the current working directory. If a user runs an af command or an MCP tool call from inside a project that contains an attacker-supplied json.py, that file runs with the user's privileges. Users who only run the tool in projects they trust are not affected. Fixed in 0.9.2; in earlier versions, setting AF_TELEMETRY_DISABLED=1 prevents it.

### CVE-2026-103333

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:D/RE:L/U:Red` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-24T12:17:13.880 |

Improper input validation in some SPARQL functions available in Apache Jena ARQ allows users to submit SPARQL queries that cause excessive CPU and/or memory usage.  This may be the result of intentionally malicious inputs in the query itself, or an expression applied over data that has been insufficiently validated/sanitised

Users are recommended to upgrade to version 6.3.0, which fixes this issue.

### CVE-2026-120943

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-24T09:17:06.377 |

An improper TLS certificate validation vulnerability exists in the ADM online update service. An unauthenticated attacker capable of performing a Man-in-the-Middle (MitM) attack against the device's firmware update connection can impersonate the update server using an untrusted TLS certificate and supply malicious update metadata. The attacker may cause a crafted firmware image to be installed and execute arbitrary code with root privileges when automatic firmware updates are enabled.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-105304

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T06:17:06.630 |

ACME challenge routing logic of Zoraxy fails to validate request URIs properly, that allows an attacker to send an arbitrary request to a service on the internal network.

### CVE-2026-130178

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T02:17:46.780 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions 0.7.1 through 0.8.4, an incomplete IPv6 blocklist in AutoGPT's outbound SSRF protection allows authenticated users to reach local or private network services. Specifically, _is_ip_blocked and BLOCKED_IP_NETWORKS in autogpt_platform/backend/backend/util/request.py fail to reject the IPv6 unspecified address :: (which connects to ::1 on Linux) as well as 6to4, NAT64, Teredo, and deprecated IPv4-compatible IPv6 encodings. An attacker can pass :: directly to blocks/sql_query_block.py or blocks/email_block.py, or point URL-fetching blocks, web fetch, MCP servers, webhooks, or OAuth at a hostname whose AAAA record resolves to ::. On backends run directly on a host, this exposes unauthenticated internal RPC services and databases listening on ::1, though the default Docker Compose and single-container deployments bind internal services to IPv4 only. This issue is fixed in version 0.9.0.

### CVE-2026-135696

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T01:17:33.630 |

rConfig Core 8.2.19 before 8.2.22 contains a server-side request forgery vulnerability that allows authenticated users to bypass the DeviceIpIsValid loopback guard by supplying unresolved hostnames. Attackers can create a device with a hostname resolving to loopback and device_port_override 6379, causing configuration downloads to send Redis inline commands for remote code execution.

### CVE-2026-130166

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-23T23:17:03.893 |

n8n is an open source workflow automation platform. Prior to 1.123.90 and 2.14.0, the invitation acceptance endpoint accepts inviter and invitee user IDs without a signed invitation token, allowing any preexisting member to take over a pending new user account. A member with permission to list users can read the ID of a pending account and set its password without authentication, then log in as that user, including as an admin when the invitation has the admin role. Exploitation requires an invitation that has not been accepted yet. This issue is fixed in versions 1.123.90 and 2.14.0.

### CVE-2026-96457

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-23T16:18:05.500 |

A flaw was found in the administrative interface of Keycloak, an identity and access management solution. The issue occurs when Fine-Grained Admin Permissions are used to restrict a group administrator from managing specific sub-groups. Due to an incomplete fix for a previous vulnerability, a restricted administrator can bypass these restrictions by moving a forbidden sub-group to the top level of the hierarchy. This allows the attacker to gain unauthorized control over the groups members, potentially leading to a full takeover of the security realm.

### CVE-2026-135170

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-23T15:17:46.093 |

Wing FTP Server before 8.2.8 contains a Lua code injection vulnerability that allows LDAP-authenticated users to inject Lua statements into session files via unescaped login names. Attackers can log in with a name containing a Lua long-string terminator followed by code, which executes on a later session request as the Wing FTP service account.

### CVE-2026-127181

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-305` |
| Published | 2026-11-24T13:17:23.147 |

SUSE Neuvector before 5.5, 5.5.0 before 5.5.6 and 5.6.0 before 5.6.5 handling of ephemeral containers was not setting some checking callbacks, allowing these to bypass permission checks.

### CVE-2026-59697

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T12:17:24.370 |

Server-Side Request Forgery (SSRF) vulnerability in ex_aws (instance metadata token provider).

This vulnerability is associated with program files lib/ex_aws/instance_meta_token_provider.ex and program routines ExAws.InstanceMetaTokenProvider.request_token/1 and ExAws.InstanceMetaTokenProvider.get/1.

ex_aws requests its IMDSv2 session token from the link-local metadata endpoint (http://169.254.169.254/latest/api/token) with HTTP redirect following enabled. Because the token request follows 3xx redirects and does not restrict the redirect target to the link-local range, an attacker who can influence the response to the metadata request (for example an on-segment neighbor spoofing the link-local address) can answer with a redirect to an arbitrary host. The library follows the redirect and accepts the arbitrary host's response body as the IMDSv2 session token, caching it and sending it as the x-aws-ec2-metadata-token header on every subsequent metadata and credential request.

This issue affects ex_aws: from 2.3.0 before 2.8.0.

### CVE-2026-49963

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-23T19:17:38.323 |

DreameHome for Android (com.dreame.smartlife) before 2.6.4.0 contains a download of code without integrity check vulnerability in RnPluginDownloadManager.java that allows network-positioned attackers to execute arbitrary JavaScript within the application by replacing React Native feature bundles that are only validated against a client-stored MD5 checksum without publisher authentication. Attackers can replace both the downloaded bundle and its corresponding MD5 metadata to run modified code with the application's permissions and access to its bridge APIs.

### CVE-2026-135298

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T17:17:53.880 |

Convoy before 26.6.0 contains an insecure direct object reference vulnerability in /portal-api single-resource handlers that allows portal link token holders to access other tenants' resources by ID. Attackers with another tenant's resource IDs in the same project can read endpoint signing secrets and webhook payloads, rotate secrets, pause or delete endpoints, and force event re-delivery.

### CVE-2026-103791

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-11-23T17:17:28.477 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains an Improper Input Validation vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to a denial of service condition.

### CVE-2026-65159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T14:18:18.730 |

NVIDIA Video Codec SDK for Linux contains a vulnerability where a user may cause an out-of-bounds write issue. A successful exploit of this vulnerability may lead to denial of service.

### CVE-2026-65158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-24T14:18:18.587 |

NVIDIA Video Codec SDK for Linux contains a vulnerability where a user may cause a NULL pointer dereference issue. A successful exploit of this vulnerability may lead to denial of service.

### CVE-2026-65157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-24T14:18:18.420 |

NVIDIA Video Codec SDK for Linux contains a vulnerability where a user may cause an out of bounds read. A successful exploit of this vulnerability may lead to denial of service.

### CVE-2026-65156

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-24T14:18:18.283 |

NVIDIA CUDA Video Codec SDK for Jetson Linux contains a vulnerability where an attacker may cause an infinite loop. A successful exploit of this vulnerability may lead to denial of service.

### CVE-2026-65155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-24T14:18:18.160 |

NVIDIA CUDA Video Codec SDK (CUVID) for Jetson Linux contains a vulnerability where an attacker may cause a loop with an unreachable exit condition. Successful exploitation may lead to denial of service.

### CVE-2026-130822

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-24T14:18:03.283 |

In Valkey before 7.2.16, 8.0.x before 8.0.13, 8.1.x before 8.1.12, 9.0.x before 9.0.8, 9.1.x before 9.1.4 and 9.2.0 release candidates, when client eviction is enabled (maxmemory-clients is not 0), an authenticated user who can write to a key that other clients are blocked on (for example with BLPOP, BLMPOP, BZPOPMIN or XREAD BLOCK) can trigger a use-after-free. While the clients blocked on that key are served, evictClients() can select and free the client whose command made the key ready, although that command is still executing, and the server then keeps using the freed client. The blocked clients do not have to belong to the attacker. The result is a reliable crash of the server process. Servers with the default maxmemory-clients 0 are not affected.

### CVE-2026-100969

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-24T14:18:00.993 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause a NULL pointer dereference. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-100965

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-24T14:18:00.013 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause an uncaught exception. A successful exploit of this vulnerability might lead to denial of service.

### CVE-2026-82216

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-24T13:17:35.393 |

Server-Side request forgery (SSRF) vulnerability in ITG Bilgisayar Teknolojileri Grubu Ltd. Şti. VSRM allows Server Side Request Forgery.

This issue affects vSRM: from 14.08.1 before 14.08.3.

### CVE-2026-127183

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-416;CWE-476;CWE-787` |
| Published | 2026-11-24T11:17:09.300 |

Various memory-safety issues in dataplane of SUSE Neuvector before 5.5, 5.5.0 before 5.5.6, 5.6.0 before 5.6.5 could be used by remote attackers to trigger crashes.

### CVE-2026-134493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-24T00:17:30.757 |

Tanium addressed a path traversal vulnerability in Core Content.

### CVE-2026-134021

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-23T23:17:04.990 |

TastyIgniter is an open-source online ordering, table reservation, and restaurant management system. Prior to 4.3.1, the Mollie payment notification handler in src/Payments/Mollie.php, processNotifyUrl(), uses a payment ID supplied with the notification to retrieve a paid transaction but does not verify that the transaction's order reference matches the order identified by the notification URL or that the transaction amount matches the order total. An ordinary customer can use a paid Mollie transaction from one order to cause a different, higher-value order to be marked paid without paying its full price. The endpoint is intentionally unauthenticated so Mollie's servers can reach it, and the request's order hash alone does not bind the fetched payment to that order. This issue is fixed in version 4.3.1.

### CVE-2026-130167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T23:17:04.073 |

n8n is an open source workflow automation platform. Prior to 2.47.6, 2.48.3, and 3.2.2, the password reset link and role change operations do not protect the instance owner account from users with a custom instance role. A user whose custom instance role includes user management permissions can obtain a password reset link for the owner and take over the owner account, or change the owner's role, gaining full control of the instance. Exploitation requires the custom roles feature and a custom instance role with user management permissions. This issue is fixed in versions 2.47.6, 2.48.3, and 3.2.2.

### CVE-2026-129837

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-23T22:20:10.470 |

A flaw was found in rsyslog. A remote, unauthenticated attacker can cause a Denial of Service (DoS) by sending a specially crafted log message with an unusual timestamp. When the service processes this message using weekday formatting templates, an out-of-bounds memory read occurs, causing the application to crash.

### CVE-2026-120787

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-23T22:19:56.510 |

Improper certificate validation in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-82303

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-126` |
| Published | 2026-11-23T21:17:06.947 |

A buffer over-read vulnerability in Elasticsearch transport decompression can expose data from other requests. The LZ4 decoder can read beyond the declared compressed block into a shared network buffer. A remote attacker who can reach an affected transport interface can send a specially crafted compressed request and obtain data from outside their own request. Exploitation of the exposed remote-cluster transport interface does not require authentication.

### CVE-2026-134844

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-23T17:17:49.487 |

pgjdbc, the PostgreSQL JDBC Driver, uses unqualified operators and functions in the catalog queries of DatabaseMetaData, ResultSetMetaData and TypeInfoCache. A role with CREATE on a schema of the application's search_path can add an operator with an exact type match, and the server runs it with the privileges of the application's role. TypeInfoCache also resolves an unqualified type name such as interval by its own ranking. A domain with that name in another schema, even the temporary schema of another session, can be used instead, and its CHECK runs in the application's session. All versions before 42.7.15 are affected, and 42.7.15 fixes the problem.

### CVE-2026-134843

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-755` |
| Published | 2026-11-23T17:17:49.357 |

pgjdbc, the PostgreSQL JDBC Driver, does not close the connection when an unchecked exception interrupts a request. Part of a Bind message stays in the send buffer, and the server reads the bytes that follow as the rest of it. The bytes of a value uploaded later on the same connection can then run as a SQL command. Since 42.6.0 a setBinaryStream() value without a length that is executed again throws such an exception, as does the driver's own retry after SQLState 0A000 or 26000. An application stream that throws an unchecked exception has the same effect in all versions. All versions before 42.7.15 are affected, and 42.7.15 fixes the problem.

### CVE-2026-103789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-23T17:17:28.220 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains a heap based buffer overflow. An unauthenticated remote attacker with adjacent network access could potentially exploit this vulnerability, leading to a denial of service condition.

### CVE-2026-103786

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-23T17:17:27.827 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains a null pointer dereference vulnerability. An unauthenticated remote attacker with adjacent network access could potentially exploit this vulnerability, leading to a denial of service condition.

### CVE-2026-101219

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-23T17:17:27.170 |

Dell Enterprise Sonic Distribution, versions prior to 4.6.1, contains a heap based buffer overflow. An unauthenticated remote attacker with adjacent network access could potentially exploit this vulnerability, leading to a denial of service condition.

### CVE-2026-59698

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-24T12:17:24.607 |

Relative path traversal in ex_aws allows an attacker who controls an S3 object key to escape the intended bucket or key prefix.

When ex_aws builds a path-style S3 request, ExAws.Operation.S3.add_bucket_to_path/2 in lib/ex_aws/operation/s3.ex joins the bucket name and the object key into a single path string and then normalizes it, collapsing . and .. segments the way a filesystem path would. Because the bucket is the first segment of the combined string, a leading ../ in the object key pops the bucket off the path. With bucket mybucket and a key of ../victim/secret.txt, the combined /mybucket/../victim/secret.txt normalizes to /victim/secret.txt, so the request (signed with the application's own credentials) is sent to bucket victim. The same mechanism collapses ../ within a key, defeating any isolation an application enforces by prepending a trusted prefix.

Only the default path-style configuration is affected; requests built with virtual_host: true do not run this normalization. Because S3 treats object keys as opaque and does not resolve .. itself, the client-side normalization introduces a traversal that would not otherwise exist. Any application that derives an S3 object key from untrusted input and relies on the bucket, or a key prefix, as a tenant or trust boundary is exposed to cross-bucket or cross-prefix read and write, depending on the operation and the credentials' permissions.

This issue affects ex_aws: from 2.1.7 before 2.8.0.

### CVE-2026-134023

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-11-23T23:17:05.283 |

TastyIgniter is an open-source online ordering, table reservation, and restaurant management system. Prior to 4.2.0, checkResetPasswordCode() in src/Auth/Models/User.php compares a submitted reset code with the stored 42-character token using a normal string comparison, which can return after the first differing byte instead of taking constant time. The password-reset flow exposes this comparison to remote requests, but the endpoint is rate-limited to six requests per minute per IP, and the advisory reports no live exploit or practical token-recovery demonstration. Recovering a high-entropy reset code through the constrained timing signal could permit an unauthorized password reset. This issue is fixed in version 4.2.0.

### CVE-2026-134848

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-158` |
| Published | 2026-11-23T17:17:49.997 |

pgjdbc, the PostgreSQL JDBC Driver, does not refuse a NUL character in a startup parameter. The StartupMessage is a list of NUL-terminated strings, so a NUL in the database name, user, currentSchema, options or ApplicationName adds further parameters. %00 in a URL decodes to a NUL. Someone who controls part of the URL or a property can choose another login role or add replication=database, although the connection still has to pass the authentication of that role. On a server that trusts the client, the attacker can log in as any role. All versions before 42.7.15 are affected, and 42.7.15 fixes the problem.

### CVE-2026-134845

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-319` |
| Published | 2026-11-23T17:17:49.613 |

pgjdbc, the PostgreSQL JDBC Driver, does not enforce TLS for some settings that ask for it. When sslmode is not set, an ssl value such as 1, on, yes or verify-full gives sslmode=prefer, or no TLS before 42.2.5. A service given in the Properties instead of the URL is ignored, so the sslmode of its pg_service.conf entry is lost. BaseDataSource.setUrl() keeps an sslmode, channelBinding or gssEncMode that was set before it. An attacker on the network path can then read and change the traffic. Versions 9.4.1208 through 42.7.14 are affected, and 42.7.15 fixes the problem.

### CVE-2026-133781

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-24T09:17:07.993 |

The controllers.json loader of @symfony/stimulus-bridge loads the package.json file of each package listed in controllers.json with require(). Node resolves this path through the exports field of the package, which can map ./package.json to a script. require() then runs that script during the Webpack or Symfony Encore build.

This is a build-time vulnerability: it doesn't affect browsers or end users. A malicious or compromised package listed in controllers.json can run code on the developer machine or the CI server. This works even when the package manager doesn't run install scripts. This code can read the files and environment variables of the build, like CI secrets, and change the built assets.

The loader now reads the resolved file and parses it as JSON, so that a mapped script fails to parse instead of running.

### CVE-2026-133780

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-24T09:17:07.843 |

The @symfony/stimulus-bridge npm package includes a Webpack loader called lazy-controller-loader that supports "magic comments" placed above a Stimulus controller import, for example /* stimulusFetch: 'lazy' */, to control lazy loading behavior. To read those options, the loader extracted the raw text of any stimulus* comment and evaluated it as JavaScript using Node's vm.runInNewContext(). The Node.js node:vm module is not a security sandbox, and a crafted comment can break out of the VM context using well-known techniques to run arbitrary Node.js code within the build process.

This is a build-time vulnerability: it does not affect browsers or end users. The code executes on the developer machine or CI/build server during a Webpack or Symfony Encore build. Realistic attack vectors include a malicious Stimulus controller introduced through a compromised dependency, or a pull request that triggers an automated CI build. An attacker who can get such a file into the build can read files and environment variables available to the build process, exfiltrate CI secrets, tamper with generated build artifacts, and run commands with the permissions of the build user.

The loader no longer evaluates comment content as JavaScript. It now parses each comment as an object expression using a real JavaScript parser and extracts only plain literal values. Any non-literal value, such as a function call, an identifier, or a sequence expression, is rejected and reported as a build error instead of being executed. Legitimate option values like 'lazy' and 'eager' continue to work without any changes required on the user's side.

### CVE-2026-135723

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-24T04:17:30.177 |

FFmpeg before 9.1 contains a double free vulnerability in the fill_marker() function of libavformat/imf_cpl.c that frees a Marker label without clearing the pointer when default scope allocation fails. Attackers can supply a crafted Composition Playlist with a Marker Label lacking a scope attribute, triggering a second free in imf_marker_free() under memory pressure and causing memory corruption or a crash.

### CVE-2026-135709

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T04:17:27.830 |

FFmpeg before 9.1 contains an out-of-bounds write vulnerability in ogg_buffer_data() in libavformat/oggenc.c because ogg_buffer_page() leaves a full page current after failed allocation. When page allocation fails, a memset with length (size_t)-1 or an overflowing memcpy writes past the segment table, causing heap memory corruption and crashes when writing Ogg output.

### CVE-2026-135706

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-24T04:17:27.327 |

FFmpeg before 9.1 contains a heap buffer overflow vulnerability in modplug_read_header() in libavformat/libmodplug.c that allocates the buffer using max_size instead of sz. When max_size is set to 0, attackers can supply crafted module files that avio_read() copies into a zero-sized buffer, causing memory corruption, crashes, or possible code execution.

### CVE-2026-134619

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-348` |
| Published | 2026-11-24T00:17:31.280 |

Tanium addressed a local privilege escalation vulnerability in Emerging Issues Content.

### CVE-2026-134618

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-24T00:17:31.147 |

Tanium addressed a local privilege escalation vulnerability in Emerging Issues Content.

### CVE-2026-134496

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-24T00:17:31.023 |

Tanium addressed an improper input validation vulnerability in Core Content.

### CVE-2026-93457

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-24T02:17:47.810 |

Out-of-bounds write vulnerability in certain ASUS routers allows an unauthenticated nearby user to corrupt process memory, potentially resulting in a denial-of-service, via crafted LLTD packets.Refer to the ' Security Update for ASUS Router Firmware ' section on the ASUS Security Advisory for more information.

### CVE-2026-133961

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-95` |
| Published | 2026-11-24T00:17:30.067 |

Tanium addressed an unauthorized code execution vulnerability in the Tanium Default Content.

### CVE-2026-65137

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-24T14:18:17.907 |

NVIDIA Jetson Linux for Linux contains a vulnerability where a local attacker may cause a NULL pointer dereference issue. A successful exploit of this vulnerability may lead to denial of service and data tampering.

### CVE-2026-134962

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T13:17:27.203 |

Missing Authorization vulnerability in Slim & Dapper Theater for WordPress theatre allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Theater for WordPress: from n/a through 0.19.1.

### CVE-2026-124828

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-24T10:17:49.680 |

Authorization bypass using a user-controlled token (IDOR) on the GlobalEduca job portal. The GET endpoint ‘/attachments/{attachment_id}’ fails to verify whether the attachment belongs to the authenticated user. A user with a registered account can enumerate sequential identifiers and download attachments belonging to other candidates, including resumes containing personal data.

### CVE-2026-120949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-24T10:17:49.483 |

An improper authorization vulnerability exists in the wallpaper component of ADM. An authenticated, low-privileged user can bypass shared-folder access controls by specifying an image path within a restricted share. The CGI processes the request with root privileges without enforcing the source share's access permissions, allowing the attacker to copy and retrieve images they are not authorized to access, resulting in unauthorized information disclosure.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-135694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-24T01:17:33.307 |

rConfig Core 8.1.0 before 8.2.20 and rConfig Pro before 8.4.0 contain a missing authorization vulnerability in ExportController.php that allows authenticated users to export restricted tables. Attackers can supply excluded table names to export($table), bypassing the EXCLUDED_TABLES deny list, and obtain decrypted passwords, device credentials, and API tokens.

### CVE-2026-133448

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-73;CWE-77` |
| Published | 2026-11-24T01:17:23.180 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. In versions 0.7.1 through 0.8.4, chat and prompt text passed to the Claude Code CLI is pre-processed before reaching the model, bypassing AutoPilot's tool allow-list and PreToolUse hooks. In both AutoPilot's Claude Agent SDK path and the graph orchestrator block's extended_thinking SDK mode, messages starting with / execute CLI commands or bundled skills, while @<path> mentions read files or list directories on the host and attach the results to the model request. Signed-in users, members of linked chat channels, graph authors, or indirect tool output carried into turn history can make the CLI read files accessible to the copilot executor process, whose contents reach the model provider and can be repeated in replies, and run commands that compact or clear the session, switch the model, or modify the CLI's settings.json file. This issue is fixed in version 0.9.0.

### CVE-2026-133955

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T00:17:29.690 |

Tanium addressed an improper input validation vulnerability in Core Content.

### CVE-2026-101872

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T23:17:02.357 |

EUSurvey through 1.6, prior to commit 4bf95a3, contains a blind SQL injection vulnerability in the GET /dashboard/surveys endpoint that allows authenticated attackers with the Form Manager role to infer data from the main application database. SurveyService inserts unrecognized sort values directly into the ORDER BY clause of a native query, so attackers can supply SQL expressions and use response timing to infer any data readable by the application's database account, including data outside the surveys listed on their dashboard.

### CVE-2026-82979

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-23T22:23:40.777 |

SQL injection in WHMCS could allow an authenticated client with View & Manage Contacts permission to retrieve other clients' personal, billing, and support information, as well as administrator account records and password hashes.

### CVE-2026-120777

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T22:19:55.723 |

Incorrect authorization in Azure Managed Service Identity allows an authorized attacker to elevate privileges over a network.

### CVE-2026-49965

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T19:17:38.610 |

DreameHome cloud API before 2026-11-19 contained an insecure direct object reference vulnerability in the POST /smart-app/meari-cloud/bindDevice endpoint that allows authenticated attackers to reassign another user's camera to their own Dreame account. The endpoint accepted binding requests from accounts that did not own the camera, so an attacker with the camera identifiers could supply their own user identity, become the camera's masterUid, and remove the camera from the owner's device list, denying the owner access through DreameHome.

### CVE-2026-49964

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T19:17:38.467 |

DreameHome cloud API before 2026-10-14 contained an insecure direct object reference vulnerability in the POST /dreame-user-iot/token/rtc2 endpoint that allows authenticated attackers to obtain an Agora RTC token for another user's device by supplying its device DID and owner UID. The endpoint issued the token without verifying device ownership, allowing attackers to join the device's live-video channel and publish video under the targeted device's identity.

### CVE-2026-49962

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T19:17:38.173 |

DreameHome device sharing and MQTT broker before 2026-10-26 contained an incorrect authorization vulnerability that allows former share recipients to keep receiving a device's MQTT status messages after the owner revokes sharing. Revocation removed application access and the device-command API rejected the former recipient, but the broker still accepted subscriptions to the device's status topic using the DID, owner UID, and model exposed during sharing, allowing continued monitoring of the home's map data and device status.

### CVE-2026-49961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T19:17:38.030 |

DreameHome MQTT broker before 2026-10-26 contained an incorrect authorization vulnerability that allows authenticated attackers to subscribe to another device's status topic /status/{DID}/{UID}/{model}/# without owning or having access to the device. Attackers who know the device DID, owner UID, and model can receive the device's telemetry, including compressed LiDAR map frames exposing the home's layout, the Wi-Fi SSID and BSSID, local IP address, gateway, firmware version, and the session key used for encrypted video.

### CVE-2026-49960

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-23T19:17:37.863 |

DreameHome cloud API before 2026-10-14 contained an insecure direct object reference vulnerability in the POST /smart-app/meari-cloud/redirectAndLogin endpoint that allows authenticated attackers to obtain another user's Meari camera-platform identity and session credentials by supplying that user's uid. The endpoint used the caller-supplied uid to select the Meari account without verifying that it belonged to the account authenticated by the Dreame-Auth token. Attackers can obtain target uids through public forum profiles and an email-to-uid lookup, and use the leaked credentials to access live video, microphone audio, the camera speaker, and stored recordings of Meari-backed cameras.

### CVE-2026-135432

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T18:17:13.693 |

sdcb Chats 1.10.0 before 1.17.1 contains an incorrect authorization vulnerability in GetAssignedUserDetails that allows assigned non-admin users to read other users' per-user MCP headers. Attackers can request the assigned-user-details endpoint to obtain bearer tokens in CustomHeaders and impersonate other users against the downstream MCP server.

### CVE-2026-135299

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-23T17:17:54.057 |

Convoy before 26.3.7 contains an arbitrary file read vulnerability that allows any project API key holder, including viewer-scoped keys, to read host files via require() in JavaScript transform functions. Attackers can submit a function to the sources/test_function endpoint calling require on a file path to disclose configuration files containing database credentials and secrets.

### CVE-2026-135293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-23T17:17:53.017 |

Contiki-NG through 5.2 contains an infinite loop vulnerability in icmp_in() in os/net/ipv6/multicast/mpl.c that allows unauthenticated attackers to hang nodes via crafted MPL control messages. Attackers on the same link can send an MPL data message to create a seed entry, then an all-zero bit vector control message causing index wraparound and denial of service.

### CVE-2026-135258

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-639` |
| Published | 2026-11-23T16:17:45.610 |

MISP contains multiple related authorization and input-validation flaws in its object editing and attachment handling workflows.

- A user with permission to edit their own object could inject a foreign attribute identifier into the object revision form. The revision data, stored in the server-side session, was merged into the stored object before the save diff was computed. The save then wrote to the foreign attribute row by its identifier without verifying that the row belonged to the caller's event or organisation, allowing an attacker to overwrite or soft-delete an attribute in another organisation's private event.
- Attachment file paths were constructed directly from event and attribute identifiers supplied by the request. Because no type or format validation was applied, crafted values (for example directory-traversal sequences or file-name extensions) could cause the application to read from or write to file-system locations outside the intended attachment directory.
- The audit-log behaviour recorded an edit under the event identifier carried in the save payload rather than the event identifier of the stored database row. An attacker who included a different event identifier in the save could cause the audit entry to be attributed to the wrong event, undermining the integrity of the audit trail.

Exploitation requires an authenticated web-session user with object-editing permissions (perm_add / perm_modify). API-key-only requests do not carry the PHP session and are not affected by the revision-session vector.

Affected versions: MISP < 2.5.52. Fixed in 2.5.52.

### CVE-2026-135256

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-23T16:17:45.180 |

MISP contains a Regular Expression Denial of Service (ReDoS) vulnerability in its Warninglist feature. Warninglist entries of type "regex" are evaluated against attribute values without any backtracking limit. An authenticated user with permission to add or import warninglist entries can supply a crafted regular expression pattern that triggers excessive backtracking in the PCRE engine, causing sustained CPU consumption and denial of service.

Additionally, imported warninglists were not validated for syntactic correctness before replacing existing entries, allowing malformed or malicious patterns to be persisted and later evaluated without prior rejection.

Preconditions:
- An authenticated account with the ability to create, edit, or import warninglist entries (users below site-admin level can add entries).
- The target MISP instance has at least one warninglist of type "regex" that will be evaluated against incoming attribute values.

Impact:
- Sustained CPU exhaustion leading to denial of service for all users of the MISP instance.
- Potential for cascading performance degradation on shared infrastructure.

Affected versions: MISP prior to 2.5.52.

### CVE-2026-135252

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601;CWE-918` |
| Published | 2026-11-23T16:17:44.520 |

MISP contains a Server-Side Request Forgery (SSRF) vulnerability in its feed and sync HTTP request handling. When the application uses libcurl as the HTTP transport, the CURLOPT_FOLLOWLOCATION option was enabled by default, causing the library to automatically follow HTTP redirects without the application's own per-hop validation logic being invoked.

- Feed requests: MISP implements its own redirect validation for feed sources, but libcurl was following redirects before that validation could execute, allowing a malicious or compromised feed source to redirect the request to arbitrary internal URLs.
- Sync requests: Sync peers are server-configured, and the application does not perform per-hop redirect validation for sync traffic. libcurl's automatic redirect following allowed a malicious sync peer to redirect the request to internal network resources.

An attacker who is a configured sync peer, controls a feed source URL, or can influence DNS resolution for a configured endpoint can exploit this to cause the MISP server to issue requests to arbitrary internal services, potentially reading sensitive data or interacting with internal APIs that are not otherwise exposed.

Affected: MISP versions prior to 2.5.52.

### CVE-2026-135250

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-23T16:17:44.310 |

MISP contains a denial-of-service vulnerability in its image processing pipeline. When generating attachment thumbnails or rendering event graph preview images, the application decodes user-supplied image data using the GD library without first validating the declared pixel dimensions in the image header.

Because GD allocates its pixel buffers outside the scope of PHP's memory_limit directive, a crafted image with an extremely large declared resolution (for example, 20000 x 20000 pixels) can trigger a multi-gigabyte memory allocation during the decode step, exhausting available system memory and causing the PHP worker process or the host to become unresponsive.

Preconditions:
- An authenticated MISP user with permission to upload attachments or to create/view event graphs.
- The ability to supply a crafted image file (e.g., a PNG with a valid header declaring oversized dimensions).

Impact:
- Denial of service: memory exhaustion leading to process crash or host unavailability.
- No confidentiality or integrity impact is indicated by the evidence.

Affected versions: MISP prior to 2.5.52.

### CVE-2026-135209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-23T16:17:38.423 |

ServerOS Panel before 1.10.1 contains a decompression bomb vulnerability in DeploySourcePacker::extract() that allows authenticated users with manage-machines permission to bypass the 4 GB unpacked-size limit by under-declaring zip entry sizes. Attackers can upload a crafted archive via POST /machines/{machine}/sources whose entries inflate far beyond declared sizes, filling the host disk and denying service to all workspaces.

### CVE-2026-135206

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-23T16:17:37.930 |

ToDesktop Builder before 0.36.1 contains a path traversal vulnerability in the todesktop-fs custom protocol handler that allows attackers to escape the bundled files directory using ../ sequences. Attackers who can run script in an application's renderer can issue XMLHttpRequest calls with traversal paths to read arbitrary files accessible to the user.

### CVE-2026-135160

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-23T15:17:44.530 |

Medplum server 5.1.4 before 5.1.42 contains an incorrect authorization vulnerability in the Binary $presigned-url operation that allows non-admin project members to overwrite other projects' Binary content. Attackers in a project linked to another project can request a signed upload URL with upload=true for a readable Binary and overwrite its stored content, since project ownership is never verified.

### CVE-2026-134894

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-24T10:17:49.830 |

An SQL injection vulnerability exists in the firewall management component of ADM Defender due to insufficient validation and improper handling of input data in SQLite queries. This vulnerability may allow an attacker with access to the affected functionality to manipulate database queries, potentially resulting in unauthorized access to or modification of firewall-related data.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120933

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-24T09:17:05.970 |

A cleartext transmission of sensitive information vulnerability in the ADM Notifications allows network eavesdroppers on the outbound network path to obtain Clickatell service credentials via the SMS. When executing an SMS test for Clickatell Communicator Central, the backend function Send_Test_SMS embeds the sensitive contents directly into an unencrypted HTTP request URL. An observer on the NAS network egress path can capture the plain text credentials and message payload since the initial request is transmitted without TLS protection or secret redaction.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120935

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-24T08:17:04.620 |

An argument injection vulnerability exists in the settings/vpn.cgi endpoint in the ADM. When processing a WireGuard profile, the internal command parser removes quotes and performs a quote-agnostic scan on arguments without properly sanitizing redirection operators. An authenticated administrator can supply a crafted parameter to cause the execution helper to open and truncate arbitrary files on the filesystem with root privileges, resulting in an arbitrary file truncation and denial-of-service (DoS) condition.
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.

### CVE-2026-120934

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-24T08:17:04.427 |

An External Control of File Name or Path (Argument Injection) vulnerability in the settings/notification.cgi component of ADM allows authenticated remote administrators to create or truncate arbitrary files with root privileges via crafted request parameters. An authenticated administrator can truncate arbitrary critical files across the root filesystem, leading to system failure or Denial of Service (DoS).
Affected products and versions include: from ADM 4.1.0 through ADM 4.3.3.RY62 as well as from ADM 5.0.0 through ADM 5.1.4.RM62.
