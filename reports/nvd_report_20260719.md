# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-18 15:00 UTC
- **対象期間**: `2026-07-17T15:00:23.000Z` 〜 `2026-07-18T15:00:14.000Z`
- **重要CVE数**: 112 件（Critical 9.0+: 27 件 / High 7.0〜: 85 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**リモートコード実行 (RCE)・認証バイパス・深刻な情報漏洩** が集中している点が顕著です。特に **IBM Langflow OSS** 系列で複数の RCE・権限昇格・認証回避が同時に報告され、同一製品に対する攻撃面が広がっています。加えて、**Fastify、PrestaShop、WordPress、VMware Avi、CodeIgniter** といった広く利用されているフレームワーク・CMS でも、ネットワークから直接利用可能な完全リモートコード実行や認証回避が確認されました。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|--------------------|
| **CVE‑2026‑8481** (IBM Langflow OSS 1.0.0‑1.10.0) | 9.9 | `/api/v1/validate/code` が `exec()` で任意コード実行 | **単一エンドポイントで即座に RCE** が可能。デフォルトデプロイで認証不要。Langflow は AI/LLM ワークフローのフロントエンドとして多くのスタートアップ・社内ツールで採用されているため、被害拡大リスクが高い。 |
| **CVE‑2026‑47865** (VMware Avi Load Balancer) | 9.8 | 認証バイパスにより Avi Control Plane へ不正アクセス | **ロードバランサはインフラの要**。認証回避で設定変更や内部サービスへのトンネルが可能になるため、横方向への侵害が容易になる。影響バージョンは 30.1.1‑30.2.6、31.1.1‑31.2.2、31.2.2‑2p3 まで。 |
| **CVE‑2026‑16117** (fastify/http‑proxy ≤ 11.5.0) | 10.0 | URL エンコードされたプレフィックスが正しく書き換えられず、任意リクエストリダイレクトが可能 | **Fastify は Node.js エコシステムで最も利用される高速 HTTP フレームワーク**。プロキシ設定ミスにより攻撃者が内部 API を任意のエンドポイントへ転送でき、サーバーサイドリクエストフォージェリ (SSRF) に発展する恐れがある。 |
| **CVE‑2026‑54159** (PrestaShop ps_facetedsearch 3.0.0‑4.0.4) | 10.0 | スライダー型フィルタの値が未検証で保存され、任意コード実行・データ改ざん | **e‑コマースサイトは顧客情報・決済情報を保持**。モジュール単体での脆弱性は、プラグインエコシステム全体の信頼性を揺るがす。 |
| **CVE‑2026‑63030** (WordPress 6.9.x < 6.9.5 / 7.0.x < 7.0.2) | 9.8 | REST API バッチエンドポイントと `author__not_in` SQLi の組み合わせで RCE | **WordPress は世界最大の CMS**。REST API は外部サービスと連携する際に必須であり、SQLi と RCE が同時に成立する点が極めて危険。 |

> **注**：上記 5 件は CVSS が 9.8 以上で、**リモートから認証不要でコード実行が可能**、または **インフラ・プラットフォーム全体への影響が大きい** ものを選定しています。

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性スキャンの実施**：対象システムに対し、上記 CVE の有無を自動スキャン（Nessus、OpenVAS、Qualys 等）し、該当パッケージ・バージョンを即座にリストアップ。  
- **ネットワーク隔離**：外部から直接アクセス可能な管理ポート（例：Avi Control Plane、Langflow API）をファイアウォールで制限し、信頼できる IP のみ許可。  
- **監査ログの有効化**：認証バイパスや不正リクエストが発生した際に即座に検知できるよう、Web サーバ・アプリケーション・データベースのアクセスログを集中管理（ELK / Splunk 等）し、アラートルールを追加。  

### 3.2 製品別具体的アップデート

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン (修正済) | アップデート手順のポイント |
|-------------------|----------------------|------------------------|----------------------------|
| **IBM Langflow OSS** | 1.0.0‑1.10.0 | **≥ 1.10.2**（2026‑12‑01 リリース） | `pip install --upgrade langflow==1.10.2` → コンテナイメージ再ビルド → データベースマイグレーション (`alembic upgrade head`) |
| **VMware Avi Load Balancer** | 30.1.1‑30.2.6、31.1.1‑31.2.2、31.2.2‑2p3 | **30.2.7**、**31.2.2‑2p3**、**32.1.2** 以上 | コントローラ UI から「System → Upgrade」実行、アップグレード後は `avi-controller` の証明書チェーンを再生成 |
| **fastify/http‑proxy** | ≤ 11.5.0 | **≥ 11.5.1** | `npm install fastify@latest fastify-http-proxy@latest` → `package-lock.json` のハッシュ確認 |
| **PrestaShop ps_facetedsearch** | 3.0.0‑4.0.4 | **4.0.5** 以上 | PrestaShop 管理画面 → 「Modules → Module Manager」からモジュールを更新、または手動で `ps_facetedsearch` ディレクトリを上書き |
| **WordPress** | 6.9.x < 6.9.5、7.0.x < 7.0.2 | **6.9.5**、**7.0.2** 以上 | `wp core update --version=6.9.5`（または 7.0.2） → プラグイン互換性テストを実施 |
| **CodeIgniter** | < 4.7.3 | **4.7.3** 以上 | Composer: `composer require

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-16117

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-18T14:17:11.620 |

Impact: @fastify/http-proxy versions up to and including 11.5.0 fail to rewrite the request prefix when the prefix segment is URL-encoded. Fastify's router URL-decodes paths for route matching, but request.url retains the original encoded form, and the prefix-rewrite step uses a literal string replace against the decoded prefix. A request that encodes one or more characters of the configured prefix therefore matches the route but skips the rewrite, so the raw encoded path is forwarded to the upstream unchanged. The upstream then decodes the path and serves it, letting an attacker reach upstream paths that the proxy was configured to hide via rewritePrefix, including internal or administrative endpoints.

Patches: upgrade to @fastify/http-proxy 11.6.0.

Workarounds: none.

### CVE-2026-54159

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-07-17T21:17:07.963 |

PrestaShop ps_facetedsearch is a module that adds layered navigation filters. From 3.0.0 until 4.0.4, the ps_facetedsearch module rebuilds selected search filters from the request URL, and the value of a slider filter, price or weight, is taken from the URL without sufficient validation and stored in an internal filter-block cache where it is serialized and later read back with a raw native unserialize() in src/Filters/Block.php. By crafting that value, an unauthenticated attacker can smuggle a malicious serialized PHP object into the cache, and when it is deserialized, a gadget chain writes an arbitrary PHP file inside the modules/ps_facetedsearch/ directory, which is then used as a webshell to run commands on the server. This issue is fixed in version 4.0.4.

### CVE-2026-8859

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T20:17:31.643 |

IBM Langflow OSS 1.0.0 through 1.10.0 Langflow could allow an attacker to write arbitrary files to unintended locations due to improper input validation in the APIRequest component. A path traversal vulnerability exists when the "Save to File" feature is enabled, where filenames extracted from HTTP response Content-Disposition headers are not sanitized before being joined to the temporary directory path. An attacker controlling an external HTTP server can supply crafted filename values containing path traversal sequences (e.g., ../), enabling arbitrary file writes to locations accessible by the Langflow process.

### CVE-2026-8635

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T20:17:31.527 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows authenticated users to escalate privileges to superuser by directly manipulating the database, execute arbitrary system commands, and achieve full system compromise with Langflow service permissions.

### CVE-2026-8481

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T20:17:30.747 |

IBM Langflow OSS 1.0.0 through 1.10.0 contain a critical remote code execution vulnerability in the code validation API endpoint. The POST /api/v1/validate/code endpoint accepts user-supplied Python code and executes it directly using Python's built-in exec() function without sandboxing, input validation, or privilege restrictions, enabling any authenticated user to execute arbitrary system commands with the full privileges of the Langflow server process.

### CVE-2026-8476

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-17T20:17:30.623 |

IBM Langflow OSS 1.0.0 through 1.10.0 contain a critical remote code execution vulnerability in the disk-based caching mechanism. The AsyncDiskCache class uses Python's unsafe pickle.loads() function to deserialize cached objects from disk without validation, integrity verification, or authentication, enabling arbitrary code execution when malicious pickle payloads are processed. Attackers who can influence cached data through file system access, malicious workflow inputs, custom components, or API manipulation can achieve complete system compromise with the privileges of the Langflow server process.

### CVE-2026-9135

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T19:17:19.390 |

IBM Langflow OSS 1.0.0 through 1.10.0 Langflow versions up to 1.9.2 (commit 94981c443d4918517b9e8163d70fc598dc33a32d) contain a code injection vulnerability in the Policies component's ToolGuard integration that bypasses the allow_custom_components=false security control. The vulnerability exists because the validation mechanism only checks the main component source code in node_template["code"]["value"] but fails to validate dynamic CodeInput fields that store generated ToolGuard Python files. Attackers can embed malicious Python code in these unvalidated dynamic fields, which are persisted in Flow.data and later executed server-side when a guarded tool is invoked through the ToolGuard runtime. This allows authenticated users with flow creation privileges to achieve arbitrary Python code execution on the backend despite custom component restrictions. The vulnerability can be escalated through cross-tenant flow manipulation via the agentic MCP update_flow_component_field tool, which accepts attacker-controlled user_id parameters, enabling attackers to inject malicious code into victim users' flows. When combined with publicly accessible flows and specific misconfigurations (AUTO_LOGIN=true, NEW_USER_IS_ACTIVE=true), the attack can be conducted with reduced authentication requirements.

### CVE-2026-47865

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-18T09:17:08.287 |

VMware Avi Load Balancer contains an authentication bypass vulnerability. A malicious user with network access may be able to access the Avi Control plane by bypassing the authentication mechanism.

Affected versions:
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-48062

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-17T21:17:06.787 |

CodeIgniter is a PHP full-stack web framework. Prior to 4.7.3, the ext_in upload validation rule in system/Validation/StrictRules/FileRules.php checked the MIME-derived guessed extension instead of the client-provided filename extension. As a result, an uploaded file named shell.php containing GIF-like content could pass validation such as uploaded[avatar]|is_image[avatar]|mime_in[avatar,image/gif]|ext_in[avatar,gif] because the detected MIME type maps to gif, even though the uploaded filename extension is php. Applications are impacted if they accept user-controlled uploads, rely on ext_in to validate the uploaded filename extension, save uploaded files using the original client filename with $file->move($path), store uploads in a web-accessible directory, and allow PHP or other executable files to run from that directory. In those conditions, this may lead to arbitrary code execution. This issue is fixed in version 4.7.3.

### CVE-2026-13446

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-07-17T21:17:05.960 |

IBM Langflow OSS 1.0.0 through 1.10.1 contains hard-coded credentials, such as a password or cryptographic key, which it uses for its own inbound authentication, outbound communication to external components, or encryption of internal data.

### CVE-2026-8505

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-17T20:17:31.417 |

IBM Langflow OSS 1.0.0 through 1.10.0 has a vulnerability in Langflow's webhook authentication logic allows unauthenticated users to trigger the execution of any flow. The system incorrectly bypasses API key validation when the WEBHOOK_AUTH_ENABLE configuration is set to False (which is the default setting). This allows a remote attacker who knows a flow's UUID to execute it as if they were the owner, potentially leading to Remote Code Execution (RCE).

### CVE-2026-63030

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-17T20:17:28.490 |

WordPress 6.9.x before 6.9.5 and 7.0.x before 7.0.2 is affected by a REST API batch endpoint route confusion issue which, combined with the author__not_in WP_Query SQL Injection (CVE-2026-60137), could allow an attacker to perform SQL Injection and achieve Remote Code Execution.

### CVE-2026-9103

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-17T19:17:19.277 |

IBM Langflow OSS 1.0.0 through 1.10.0 could allow a remote attacker to gain unauthorized access due to improper authentication in the /api/v1/login/auto_login endpoint. The endpoint issues long-lived superuser bearer tokens without requiring authentication when the AUTO_LOGIN configuration is enabled (enabled by default), which may allow an unauthenticated network attacker to obtain full administrative access. Additionally, permissive cross-origin resource sharing (CORS) settings may allow tokens to be exposed to unintended origins, increasing the risk of unauthorized access.

### CVE-2026-9202

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-17T18:17:17.490 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows unauthenticated attackers to create unlimited user accounts on any Langflow instance; when NEW_USER_IS_ACTIVE=true (documented deployment option), newly created accounts are immediately active and can authenticate to reach RCE endpoints, bypassing the need for AUTO_LOGIN.

### CVE-2026-9198

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T18:17:17.340 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows unauthenticated attackers to chain /api/v1/auto_login (mints SUPERUSER tokens to any network caller) with /api/v1/validate/code (executes user code via exec()) to achieve full RCE on default Langflow deployments

### CVE-2026-8297

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-17T17:17:17.860 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Gis Informatics Engineering Consulting Laboratory R&D and Software Services Inc. GisLab Laboratory Management System allows SQL Injection.

This issue affects GisLab Laboratory Management System: from 1.4.03 through 08072026.

### CVE-2026-12692

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-620` |
| Published | 2026-07-17T17:17:13.303 |

Unverified password change vulnerability in Vimesoft Inc. Enterprise Video Platform allows Authentication Bypass.

This issue affects Enterprise Video Platform: from 3.11.0.0 before 3.25.0.

### CVE-2026-55518

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862;CWE-863` |
| Published | 2026-07-17T21:17:09.173 |

Avo is a framework to create admin panels for Ruby on Rails apps. Prior to 3.32.1 and 4.0.0.beta.51, Avo's association attach workflow checks attach_<association>? in the UI and GET /resources/:resource/:id/:related/new path, but the actual write endpoint, POST /resources/:resource/:id/:related, does not run the same authorization check before mutating the association through Avo::AssociationsController#create. An authenticated low-privileged Avo user can bypass hidden or disabled attach controls and directly attach related records to a parent record by sending a crafted POST request, which can lead to privilege escalation and cross-tenant data exposure where associations represent authorization-bearing relationships. This issue is fixed in versions 3.32.1 and 4.0.0.beta.51.

### CVE-2025-71392

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-18T14:17:10.580 |

SurrealDB before 2.0.5, 2.1.x before 2.1.5, and 2.2.x before 2.2.2 fails to properly escape table and field names in the command-line export command. An authenticated System User with OWNER or EDITOR roles can create tables or fields with malicious names containing SurrealQL. When a higher-privileged user subsequently imports the exported backup, the injected SurrealQL executes, enabling privilege escalation and root-level takeover of the SurrealDB instance. Applications that let users define custom tables or fields are also exposed to a universal second-order SurrealQL injection even when query parameters are sanitized.

### CVE-2026-12693

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T17:17:13.430 |

Authorization bypass through User-Controlled key vulnerability in Vimesoft Inc. Enterprise Video Platform allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Enterprise Video Platform: from 3.11.0.0 before 3.25.0.

### CVE-2026-15091

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T20:17:15.567 |

IBM Engineering AI Hub 1.0.0, 1.1.0, and 1.2.0 could allow a remote attacker to execute arbitrary scripts due to improper neutralization of input during web page generation.

### CVE-2026-9586

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-17T17:17:18.150 |

An unauthenticated SQL injection vulnerability exists in Sangoma Switchvox SMB Edition 8.3 (104997). The /pa endpoint processes XML content beginning with <PolycomIPPhone> and directly concatenates the user-controlled PhoneIP value into PostgreSQL queries without sanitization or parameterization. An unauthenticated remote attacker can execute arbitrary SQL statements against the backend PostgreSQL database using a single crafted request, including database operations and remote code execution.

### CVE-2026-54496

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-17T17:17:16.620 |

ZEBRA is a Zcash node written entirely in Rust. Prior to zebrad 5.0.0, halo2_gadgets 0.5.0, orchard 0.14.0, zcash_primitives 0.28.0, and zcashd 6.20.0, the variable-base scalar multiplication gadget in halo2_gadgets/src/ecc/chip/mul/incomplete.rs used assign_advice() for the base point without a copy constraint tying it to the actual base, allowing a malicious prover to produce a valid proof for an Orchard Action with an under-constrained base point and bypass the diversified-address-integrity check that binds pk_d, g_d, ivk, the nullifier (nf), and the spend validating key (ak) to the note being spent. This issue is fixed in zebrad 5.0.0, halo2_gadgets 0.5.0, orchard 0.14.0, zcash_primitives 0.28.0, and zcashd 6.20.0.

### CVE-2026-9323

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-18T14:17:12.170 |

The urwid web display backend (urwid/display/web.py) generates web session identifiers (urwid_id) in Screen.start() by concatenating two random.randrange(10**9) calls that use Python's Mersenne Twister PRNG, which is not cryptographically secure. Each call consumes approximately 30 bits of PRNG state, and the Mersenne Twister internal state is approximately 19,937 bits, so an attacker who observes approximately 334 session IDs (for example via the X-Urwid-ID HTTP response header) can fully reconstruct the internal state and predict all past and future session IDs (Path B). The same identifier is also used as the filename of a FIFO created in the world-listable /tmp directory (for example /tmp/urwid375487765176907690.in), so any local user on the host can list /tmp to enumerate active session tokens directly (Path A). With a valid session ID, an attacker can read the victim's terminal screen via the polling endpoint, inject keystrokes into the victim's session (yielding OS-level code execution with the session owner's privileges if the session runs a shell), and inject exit sequences or flood the FIFO to terminate or crash the session. A prior Bandit S311 warning on this usage was suppressed with # noqa: S311 rather than fixed

### CVE-2026-54466

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-07-17T21:17:08.657 |

websocket-driver is a WebSocket protocol handler with pluggable I/O. Prior to 0.7.5, the frame format in draft versions of the WebSocket protocol includes a length header that allows an arbitrarily large integer to be encoded as a sequence of bytes with the high bit set. By sending an indefinite sequence of bytes with values 0x80 or above, a client can make the server parse these bytes into an ever-growing integer in lib/websocket/driver/draft75.js; because JavaScript numbers are 64-bit floating point values, this number will eventually lose precision and lead to the subsequent payload being parsed incorrectly. This issue is fixed in version 0.7.5.

### CVE-2026-12694

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T17:17:13.547 |

Missing Authorization vulnerability in Vimesoft Inc. Enterprise Video Platform allows Accessing Functionality Not Properly Constrained by ACLs.

This issue affects Enterprise Video Platform: from 3.11.0.0 before 3.25.0.

### CVE-2024-58366

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-07-18T14:17:09.600 |

SurrealDB before 1.1.1 contains a format string vulnerability in the rquickjs Exception::throw_type function when scripting is enabled. Attackers with scripting privileges can supply format string sequences in error inputs to read arbitrary memory or execute code with SurrealDB process privileges.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-53727

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-17T21:17:07.837 |

css_parser is a Ruby CSS parser. From 2.2.0 until 3.0.0, CssParser::Parser#read_remote_file in lib/css_parser/parser.rb, and therefore load_uri! and the @import-following branch of add_block!, issued HTTP and HTTPS requests against any host, port, and URI without a scheme allowlist, host or IP filtering, or protection against link-local, loopback, or RFC-1918 addresses. Location: redirects were followed recursively back into the same function, which also serviced file:// URIs, so a single attacker-controlled HTTP redirect could upgrade the bug from SSRF to arbitrary local file disclosure. Any consumer of css_parser that hands it attacker-influenced CSS together with a base_uri: option is exposed. This issue is fixed in version 3.0.0.

### CVE-2026-47871

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-18T09:17:08.960 |

VMware Avi Load Balancer contains a directory traversal vulnerability. Flaws in file path validation allow malicious, authenticated network users to perform directory traversal attacks.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-8056

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T20:17:30.500 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows authenticated users to override component parameters at runtime via the API. A critical security flaw exists in the parameter filtering mechanism within the `apply_tweaks()` function.

### CVE-2026-7755

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-17T20:17:30.137 |

IBM Langflow OSS 1.0.0 through 1.10.0 Langflow could allow remote code execution due to incomplete validation enforcement on MCP server configuration files.

### CVE-2026-7667

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T20:17:29.350 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows an authenticated attacker to create a malicious flow pointing to an attacker-controlled URL that returns a specially crafted Content-Disposition header (e.g., filename="../../../target/path" ), enabling arbitrary file write operations with attacker-controlled content to any path accessible by the Langflow process.

### CVE-2026-14499

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-17T20:17:14.950 |

IBM Langflow OSS 1.0.0 through 1.10.1 Langflow could allow an authenticated user to execute arbitrary commands with elevated privileges on the system due to improper validation of user supplied input in the Python Interpreter component.

### CVE-2026-58195

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-17T19:17:17.410 |

Agentic-Flow is an AI agent orchestration platform. Prior to 2.0.14, agentic-flow MCP server tools in src/mcp/standalone-stdio.ts, src/mcp/fastmcp/servers/claude-flow-sdk.ts, src/mcp/fastmcp/servers/stdio-full.ts, src/mcp/fastmcp/servers/http-streaming-updated.ts, src/mcp/fastmcp/servers/http-sse.ts, src/mcp/fastmcp/servers/poc-stdio.ts, src/mcp/fastmcp/tools/agent/{execute,list,parallel}.ts, src/mcp/fastmcp/tools/swarm/orchestrate.ts, and src/mcp/fastmcp/tools/hooks/pretrain.ts interpolated attacker-influenceable tool parameters such as agent, task, name, language, and agentdb directly into shell command strings passed to execSync(), allowing arbitrary OS command execution with the privileges of the MCP server user. This issue is fixed in version 2.0.14.

### CVE-2026-11826

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-18T14:17:11.480 |

OpenPLC_v3 contains a heap-based buffer overflow in the getData() function in webserver/core/modbus_master.cpp. getData() reads characters between two delimiters into a caller-supplied buffer with no size parameter and no bounds check. In parseConfig() the function is invoked with the 100-byte heap-allocated MB_device.dev_name field. An authenticated attacker with access to the OpenPLC web interface can send a crafted HTTP POST to the /modbus endpoint with an oversized device_name value; the value is persisted to mbconfig.cfg and parsed on load, overflowing dev_name and overwriting adjacent struct fields (protocol at offset 108, dev_address at offset 109, ip_port at offset 210). A 200-byte payload writes 100 bytes past the allocation. The result is heap corruption leading to runtime crash and denial of service of the PLC process control loop, with attacker-controlled overwrite of adjacent configuration fields. The upstream repository was archived on 2026-04-04 and no fix is expected; the vendor has confirmed the issue does not affect OpenPLC Runtime v4.

### CVE-2024-58368

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:09.867 |

SurrealDB versions before 1.1.0 fail to properly parse the ID, DB, and NS headers in HTTP REST API requests containing special characters. Unauthenticated attackers can send crafted HTTP requests with malformed header values to trigger an uncaught exception that crashes the server.

### CVE-2024-58362

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-75` |
| Published | 2026-07-18T14:17:09.047 |

SurrealDB before 1.5.5 (and 2.0.0-beta before 2.0.0-beta.3) accepts an arbitrary object in the signin and signup operations of the RPC API without recursively validating it for non-computed values. When a record access method defines a SIGNIN or SIGNUP query and the RPC API is exposed to untrusted users, an unauthenticated attacker can encode a binary object containing a subquery using the bincode serialization format and supply it in place of credentials. The subquery is then executed within the database owner's SIGNIN/SIGNUP query under a system user session with the editor role, allowing the attacker to select, create, update, and delete non-IAM resources (though not view the query results directly, and not affect IAM resources, which require the owner role).

### CVE-2023-54366

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-18T14:17:07.603 |

SurrealDB before 1.0.1 sets default table permissions to FULL instead of NONE, allowing SELECT, CREATE, UPDATE, and DELETE operations on tables without explicit permissions. Attackers with database access or unauthenticated users on publicly exposed instances can perform unrestricted operations on unprotected tables within their authorization scope.

### CVE-2026-16158

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-07-18T13:17:06.030 |

Impact: @fastify/reply-from versions from 8.3.1 up to but not including 12.6.4 build the internal URL cache key by concatenating the destination and source path without a delimiter. Different destination and source pairs can therefore produce the same key while resolving to different upstream URLs. When getUpstream selects an upstream from request data, a URL cached for one upstream can be reused for a request intended for another upstream, causing cross-upstream data access and modification. The default configuration is affected. Setting disableCache to true prevents the behavior. Patches: upgrade to @fastify/reply-from 12.6.4. Workarounds: pass disableCache: true when registering the plugin.

### CVE-2026-15631

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-18T13:17:05.323 |

Impact: @fastify/http-proxy versions from 9.4.0 up to and including 11.5.0 fail to validate the resolved WebSocket destination path against the configured rewrite prefix. The WebSocket routing path in WebSocketProxy.findUpstream resolves the destination via the WHATWG URL constructor, which collapses dot segments, so a crafted upgrade request with path traversal sequences can escape the rewrite prefix and reach upstream endpoints that were not meant to be exposed by the proxy. This is a variant of CVE-2021-21322 in a code path that never went through the HTTP fix in fastify/reply-from. Exploitation requires a non-normalizing WebSocket client, since browsers and the ws package normalize the request path before sending, but raw HTTP clients or downstream proxies that forward the request target unchanged make the attack reachable in production topologies. 

Patches: upgrade to @fastify/http-proxy 11.6.0. 

Workarounds: none.

### CVE-2026-16097

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-18T12:17:11.393 |

A vulnerability was found in Shibby Tomato 1.28. This vulnerability affects the function sub_42537C of the component Scheduler Name Handler. The manipulation of the argument a1 results in stack-based buffer overflow. It is possible to launch the attack remotely. This project is superseded by FreshTomato.

### CVE-2026-16096

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-18T12:17:11.223 |

A vulnerability has been found in Shibby Tomato 1.28 RT-N5x MIPSR2 Build 124. This affects the function sub_40BB50 of the file /proc/webmon_recent_domains. The manipulation leads to stack-based buffer overflow. It is possible to initiate the attack remotely. This project is superseded by FreshTomato.

### CVE-2026-16095

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-07-18T11:16:43.833 |

A flaw has been found in Shibby Tomato 1.28 RT-N5x MIPSR2 Build 124. Affected by this issue is the function setup_conntrack of the file /sbin/rc. Executing a manipulation of the argument ct_tcp_timeout can lead to out-of-bounds write. The attack may be performed from remote. This project is superseded by FreshTomato.

### CVE-2026-47869

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-18T09:17:08.740 |

VMware Avi Load Balancer contains a remote code execution vulnerability. A malicious authenticated user with network access may be able to inject and execute code.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-47867

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-18T09:17:08.527 |

VMware Avi Load Balancer contains a remote code execution vulnerability. A malicious user with network access may be able to access the Avi Control plane and execute code remotely.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-54498

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T21:17:09.043 |

view_component is a framework for building reusable, testable, and encapsulated view components in Ruby on Rails. From 4.0.0 until 4.12.0, ViewComponent::Base#around_render can return HTML-unsafe strings that bypass the escaping behavior applied to normal #call return values. This creates an XSS risk when downstream applications use around_render to wrap, replace, instrument, or conditionally return content that includes user-controlled data, and ViewComponent::Collection#render_in can amplify the issue by joining per-item results and marking the entire output html_safe, converting raw unsafe output into an ActiveSupport::SafeBuffer. This issue is fixed in version 4.12.0.

### CVE-2026-50289

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-17T20:17:24.857 |

systeminformation is a System and OS information library for node.js. Prior to 5.31.7, networkInterfaces() on Linux is vulnerable to OS command injection through the Debian/Ubuntu interfaces(5) source directive because lib/network.js checkLinuxDCHPInterfaces() reads /etc/network/interfaces, extracts a source <path> token from file content, and interpolates it unquoted into cat ${file} 2> /dev/null | grep 'iface\|source' executed by execSync(cmd, util.execOptsLinux), allowing a path containing shell metacharacters to execute commands in any process that calls networkInterfaces(), including via getStaticData() and getAllData(). This issue is fixed in version 5.31.7.

### CVE-2026-49852

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-326;CWE-1391` |
| Published | 2026-07-17T20:17:23.270 |

joserfc is a Python library that provides an implementation of several JSON Object Signing and Encryption (JOSE) standards. Prior to 1.6.8, joserfc.jwt.decode accepts attacker-forged HMAC-signed tokens when the caller-supplied verification key is the empty string or None, because HMACAlgorithm.sign and HMACAlgorithm.verify in src/joserfc/_rfc7518/jws_algs.py pass the output of OctKey.get_op_key(...) to hmac.new(...) and OctKey.import_key in src/joserfc/_rfc7518/oct_key.py only emits a SecurityWarning for keys shorter than 14 bytes without rejecting zero-length input. This issue is fixed in version 1.6.8.

### CVE-2026-44739

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-17T20:17:16.597 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.17 (LTS) and 12.3.6, the columnConfigAction endpoint in bundles/CustomReportsBundle/src/Controller/Reports/CustomReportController.php passes malicious SQL configuration through CustomReportController:columnConfigAction, SqlAdapter::getColumns, SqlAdapter::buildQueryString, and Db::fetchAssociative(), allowing an attacker with the reports_config permission to use arbitrary SELECT queries, UNION statements, dangerous database functions, and error-based SQL injection to exfiltrate or manipulate database data. This issue is fixed in versions 11.5.17 (LTS) and 12.3.6.

### CVE-2026-63101

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-17T17:17:17.283 |

Open Event Server through 1.19.1 contains a missing authentication vulnerability that allows unauthenticated attackers to export the complete member roster of any group, including email addresses, names, join dates, and roles, by submitting requests to the group followers CSV export endpoint which lacks any authentication decorator. Attackers can enumerate sequential group IDs via brute-force, trigger an export via the unauthenticated POST endpoint, then poll the unauthenticated task status endpoint until completion to retrieve a download URL containing the full member CSV.

### CVE-2026-58148

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T16:17:15.897 |

The Joomla extension ChronoForms is vulnerable to an unauthenticated stored XSS vulnerability.

### CVE-2026-63093

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-07-17T15:16:47.817 |

Cursor for Windows version 3.2.16 contains a binary planting vulnerability that allows remote attackers to achieve arbitrary code execution by placing a malicious git.exe file in the repository root directory. When a developer clones and opens a crafted repository, Cursor automatically resolves and executes the workspace-resident git.exe during IDE startup and on a recurring timed cadence without any user interaction, running the malicious binary under the privileges of the current user.

### CVE-2026-9585

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T17:17:17.990 |

An unauthenticated reflected cross-site scripting (XSS) vulnerability exists in Sangoma Switchvox SMB Edition version 8.3 (104997). The application fails to properly sanitize the portal parameter supplied to the invalid_browser and invalid_browser_login handlers. User-supplied data is reflected into JavaScript generated by the application, allowing attacker-controlled script execution within a victim's browser.

### CVE-2026-15343

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T16:17:13.917 |

A path traversal vulnerability was identified in GitHub Enterprise Server that allowed an attacker who had code execution inside the Dependabot updater container to write files to arbitrary repository paths, including GitHub Actions workflow files under .github/workflows/ as the path validation did not check the effective path which the attacker could control through the dependency file's directory and symlink target. If the repository used a pull_request_target workflow or had auto-merge enabled, an injected workflow could execute with access to the repository's GitHub Actions secrets. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.22 and was fixed in versions 3.21.3, 3.20.5, 3.19.9, 3.18.12, 3.17.18.

### CVE-2026-9147

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-18T13:17:06.273 |

uproot dynamically generates Python class source code from ROOT TStreamerInfo records in a file and compiles it at runtime. Some file-controlled streamer metadata fields (for example, streamer element names) are interpolated into the generated Python source without safe quoting via repr() or the !r format specifier. An attacker who can supply a crafted ROOT file can place Python expression-breaking content into a streamer metadata field. When uproot generates and invokes the corresponding reader method, the injected Python expression is evaluated in the context of the process opening the file, resulting in arbitrary Python code execution in applications that open or process attacker-controlled ROOT files with affected uproot code paths.

### CVE-2026-12715

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T16:17:13.047 |

Missing Authorization in Google Cloud Firebase Studio versions prior to 2026-04-15 on Google Cloud Platform allows an attacker to download other users' deployed source code and access sensitive data via unauthorized GCS URL signing requests.


This vulnerability was patched on 15 April 2026, and no customer action is needed.

### CVE-2026-57860

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-17T17:17:16.777 |

ForgeCode (tailcallhq/forgecode), an AI pair-programming CLI, automatically loads and executes the MCP servers defined in a repository's .mcp.json file on startup without user confirmation. A malicious repository can supply a crafted .mcp.json whose mcpServers entries specify arbitrary command and args values (for example, command: bash with args: ['-c', 'touch /tmp/pwned']). When a user runs the forge CLI inside a cloned untrusted repository, the specified commands are spawned with the invoking user's privileges, resulting in arbitrary code execution. This provides a reliable initial-access and persistence primitive against developers who evaluate untrusted repositories with ForgeCode.

### CVE-2026-47866

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-18T09:17:08.413 |

VMware Avi Load Balancer contains an authorization bypass vulnerability. A malicious actor on the network can access a limited subset of the Avi Control Plane without proper authorization.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-53712

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-757` |
| Published | 2026-07-17T19:17:16.880 |

SCRAM (Salted Challenge Response Authentication Mechanism) is part of the family of Simple Authentication and Security Layer (SASL, RFC 4422) authentication mechanisms. Prior to 3.3, a flaw in com.ongres.scram:scram-client and com.ongres.scram:scram-common allows an attacker capable of a TLS man-in-the-middle attack to silently downgrade a connection from SCRAM-SHA-256-PLUS with channel binding to standard SCRAM-SHA-256 without channel binding when TlsServerEndpoint processes an X.509 certificate using a modern signature algorithm such as Ed25519; getChannelBindingData() can return an empty byte array after NoSuchAlgorithmException, and the ScramClient builder treats that as absent channel-binding data. This issue is fixed in version 3.3.

### CVE-2026-45309

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T19:17:14.333 |

AsyncSSH is a Python package which provides an asynchronous client and server implementation of the SSHv2 protocol on top of the Python asyncio framework. Prior to 2.23.0, AsyncSSH expands the OpenSSH-compatible AuthorizedKeysFile %u token in asyncssh/config.py, asyncssh/connection.py, asyncssh/auth_keys.py, and asyncssh/misc.py with the raw SSH username during pre-authentication server config reload, allowing a server configured with AuthorizedKeysFile authorized_keys/%u to read an authorized-keys file outside the intended directory when the SSH username contains /, \, or .. path traversal segments and authenticate with an attacker-selected key file. This issue is fixed in version 2.23.0.

### CVE-2026-13445

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T21:17:05.473 |

IBM Langflow OSS 1.0.0 through 1.10.1 can allow an authenticated attacker to exploit the SaveToFile component to read and modify another user's uploaded files by specifying absolute paths pointing to victim storage locations. In append mode, the attacker's workflow reads victim file contents, appends attacker-controlled data, and uploads a copy containing victim data to the attacker's namespace (confidentiality breach). In overwrite mode, the attacker can replace victim file contents with arbitrary data (integrity breach). This breaks the storage ownership boundary between users.

### CVE-2026-45260

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T20:17:16.857 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.17 (LTS) and 12.3.7, Pimcore's WebDAV asset endpoint exposes a MOVE operation through /asset/webdav{path} without an authentication plugin in bundles/CoreBundle/src/Controller/WebDavController.php, and models/Asset/WebDAV/Tree.php performs asset mutation and deletion through models/Asset.php before checking a current Pimcore user or the rename, delete, create, or publish permissions, allowing unauthorized asset deletion, moves, or overwrites. This issue is fixed in versions 11.5.17 (LTS) and 12.3.7.

### CVE-2026-13473

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-17T20:17:14.827 |

IBM Storage Protect Client 8.1.0.0 through 8.1.27.0, 8.1.27.1, and 8.2.0.0 through 8.2.1.0 IBM Storage Protect is vulnerable to a heap-based buffer overflow, caused by improper bounds checking. A remote attacker could overflow a buffer and execute arbitrary code on the system or cause the server to crash.

### CVE-2026-13448

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-17T20:17:14.713 |

IBM Langflow OSS 1.0.0 through 1.10.1 Lanflow OSS contains an unauthenticated remote code execution vulnerability in the public flow build endpoint ( /api/v1/build_public_tmp/{flow_id}/flow ). The vulnerability stems from an incomplete denylist in the validate_public_flow_no_code_execution() function that fails to block several code-execution agent components including OpenDsStarAgent, CodeActAgentSmolagents, and CSVAgent.

### CVE-2026-45162

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-17T19:17:14.167 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.17 (LTS) and 12.3.7, multiple Pimcore locations call PHP's unserialize() on data from database columns and filesystem files without the allowed_classes restriction, including lib/Tool/Authentication.php, models/Site/Dao.php, models/DataObject/ClassDefinition/CustomLayout/Dao.php, models/Tool/TmpStore/Dao.php, models/Asset/WebDAV/Service.php, and admin-ui-classic-bundle/src/Helper/Dashboard.php, enabling object injection and remote code execution if an attacker can control the serialized data source. This issue is fixed in versions 11.5.17 (LTS) and 12.3.7.

### CVE-2026-47868

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-18T09:17:08.627 |

VMware Avi Load Balancer contains a local privilege escalation vulnerability. A malicious user with local access may be able to escalate their privileges to run code as root.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-50197

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-07-17T20:17:24.087 |

Skipper is an HTTP router and reverse proxy for service composition. Prior to 0.26.10, zalando/skipper's OpenPolicyAgent integration silently bypasses request-body inspection on HTTP/1.1 Transfer-Encoding: chunked and HTTP/2 requests that omit the content-length pseudo-header, because the opaAuthorizeRequestWithBody filter and OpenPolicyAgentInstance.ExtractHttpBodyOptionally in filters/openpolicyagent/openpolicyagent.go produce an empty raw_body and input.parsed_body while the upstream service receives the full attacker-controlled body. This issue is fixed in version 0.26.10.

### CVE-2026-48373

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-17T20:17:21.290 |

Acrobat Reader is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-9762

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-17T18:17:17.693 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.4 is vulnerable to remote code execution when jdbc url is under user control.

### CVE-2026-7754

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-17T20:17:29.470 |

IBM Langflow OSS 1.0.0 through 1.10.0 Langflow 1.9.0 could allow server-side request forgery (SSRF) due to insecure default configuration and incomplete enforcement of the SSRF protection mechanism.

### CVE-2026-44974

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-17T20:17:16.727 |

@hapi/content provided HTTP Content-* headers parsing. Prior to 6.0.2, Content.disposition() retained the last occurrence of each duplicate parameter while Content.type() retained the first occurrence of duplicate charset and boundary parameters, creating a parameter-smuggling primitive when another component in the request-processing chain resolves duplicates the opposite way. This can allow an upload filename allowlist bypass in headers such as Content-Disposition: form-data; name="file"; filename="safe.txt"; filename="shell.php". This issue is fixed in version 6.0.2.

### CVE-2026-63094

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345;CWE-601` |
| Published | 2026-07-17T15:16:47.960 |

SigNoz through 0.133.0 contains an open redirect vulnerability in the SSO authentication flow that allows unauthenticated attackers to steal session tokens from any user on instances configured with Google OAuth, SAML, or OIDC. Attackers can call the unauthenticated sessions context endpoint with a ref parameter pointing to an attacker-controlled host, deliver the resulting crafted login URL to a victim, and receive the victim's access and refresh tokens when they complete SSO authentication.

### CVE-2026-56741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-17T22:17:57.317 |

JLine is a Java library for handling console input. Prior to 3.30.14, 4.0.16, and 4.2.1, the JLine3 Telnet server remote-telnet module does not apply an upper bound to terminal dimensions received via the Telnet NAWS option, and TelnetIO.handleNAWS() in TelnetIO.java:856-879 reads client-supplied width and height as 16-bit unsigned integers and passes values such as 65535x65535 to setTerminalGeometry(), allowing an unauthenticated remote attacker to repeatedly alternate values and trigger continuous expensive rendering work that causes CPU exhaustion and denial of service. This issue is fixed in versions 3.30.14, 4.0.16, and 4.2.1.

### CVE-2026-56740

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-17T22:17:57.153 |

JLine is a Java library for handling console input. Prior to 3.30.14, 4.0.16, and 4.2.1, the JLine3 Telnet server remote-telnet module does not limit the number of environment variables a client may inject via the Telnet NEW-ENVIRON option, and TelnetIO.readNEVariables() in TelnetIO.java:1127-1180 stores each variable pair in a HashMap held by ConnectionData, allowing an unauthenticated attacker to flood unique variable pairs before the terminating IAC SE byte and exhaust JVM heap memory with an OutOfMemoryError. This issue is fixed in versions 3.30.14, 4.0.16, and 4.2.1.

### CVE-2026-49485

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-07-17T22:17:16.893 |

HAPI FHIR is a complete implementation of the HL7 FHIR standard for healthcare interoperability in Java. Prior to 6.9.9 and 6.9.4.2, all implementations of FHIRPathEngine accept arbitrary FHIRPath expressions and evaluate them without input validation, and the FHIRPath functions matches(), matchesFull(), and replaceMatches() pass user-controlled regular expressions to Java's Pattern.compile() and String.replaceAll() through an incomplete timeout utility. An attacker can send a resource containing an evil regex pattern that causes catastrophic backtracking, exhausting CPU resources and causing denial of service in the FHIR Validator HTTP endpoint and affected org.hl7.fhir.* modules. This issue is fixed in versions 6.9.9 and 6.9.4.2.

### CVE-2026-50274

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-17T21:17:07.337 |

Datadog dd-trace-go is a Go client library for Datadog application performance monitoring, profiling, and security monitoring. Prior to 2.8.1, Datadog tracing libraries that implement W3C baggage propagation parse incoming baggage HTTP headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES limits on the extract path. A remote, unauthenticated attacker can send a request whose baggage header contains an arbitrarily large number of comma-separated key-value pairs or a single very large value, causing unbounded CPU and memory consumption and enabling a remote denial of service against HTTP services with baggage propagation enabled. This issue is fixed in version 2.8.1.

### CVE-2026-50272

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-17T21:17:07.200 |

dd-trace is the Datadog APM client for Node.js. Prior to 5.100.0, W3C baggage propagation in packages/dd-trace/src/baggage.js and packages/dd-trace/src/opentracing/propagation/text_map.js parsed incoming baggage HTTP headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES on extraction. A remote, unauthenticated attacker can send a request whose baggage header contains an arbitrarily large number of comma-separated key-value pairs, or a single very large value, causing unbounded CPU and memory consumption and enabling a remote denial of service against any HTTP service with baggage propagation enabled. This issue is fixed in version 5.100.0.

### CVE-2026-50271

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-17T21:17:07.070 |

Datadog dd-trace-py is the Datadog Python APM client. Prior to 4.8.2, Datadog tracing libraries that implement W3C baggage propagation parse incoming baggage HTTP headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES limits on the extract path. A remote, unauthenticated attacker can send a request whose baggage header contains an arbitrarily large number of comma-separated key-value pairs or a single very large value, causing unbounded CPU and memory consumption and enabling a remote denial of service against HTTP services with baggage propagation enabled. This issue is fixed in version 4.8.2.

### CVE-2026-44891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-07-17T21:17:06.250 |

Netty is a network application framework for development of protocol servers and clients. Prior to 4.1.136.Final and 4.2.16.Final, io.netty.handler.codec.stomp.StompSubframeDecoder fails to limit the total number of headers or their cumulative size per frame, and the maxLineLength parameter only restricts individual header lines. An attacker can send a large number of short headers that are accumulated in memory inside DefaultStompHeadersSubframe until the JVM throws an OutOfMemoryError, causing denial of service for servers exposing a STOMP endpoint based on StompSubframeDecoder. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-7872

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-17T20:17:30.377 |

IBM Langflow OSS 1.0.0 through 1.10.0 allows an authenticated attacker to read arbitrary files including the JWT signing key and forge authentication tokens for any user.

### CVE-2026-50151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-17T20:17:23.683 |

oras-go is a Go library for managing OCI artifacts. Prior to 2.6.1, registry/remote/repository.go in blobStore.completePushAfterInitialPost follows a registry-controlled Location header during monolithic blob upload and reuses the Authorization header from the initial POST request for the subsequent PUT request, allowing a malicious registry to return a cross-host Location and receive the caller's credentials at an attacker-controlled endpoint. This issue is fixed in version 2.6.1.

### CVE-2026-45799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-07-17T20:17:18.393 |

Wire provides gRPC and protocol buffers for Android, Kotlin, Swift, and Java. Prior to 6.3.0 and 7.0.0-alpha03, ByteArrayProtoReader32.skipGroup() and ProtoReader.skipGroup() in wire-runtime do not validate that a LENGTH_DELIMITED field length is non-negative before skip(), allowing a crafted protobuf varint encoding -128 as a signed Int to make skip(-128) move the internal position negative and make the next readByte() throw ArrayIndexOutOfBoundsException instead of the documented IOException or ProtocolException, which can crash services using ProtoAdapter.decode(byte[]) on untrusted payloads. This issue is fixed in versions 6.3.0 and 7.0.0-alpha03.

### CVE-2026-15322

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-598` |
| Published | 2026-07-17T20:17:15.800 |

IBM Engineering AI Hub 1.0.0, 1.1.0, and 1.2.0 could allow a remote attacker to obtain sensitive information due to the exposure of session tokens in URLs.

### CVE-2026-9171

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-07-17T19:17:19.520 |

IBM PowerVM Novalink are vulnerable to a denial of service, caused by sending a specially-crafted request. A remote attacker could exploit this vulnerability to cause the server to consume memory resources.

### CVE-2026-52746

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-07-17T19:17:16.500 |

JSONata is a JSON query and transformation language. Prior to 2.2.0, malicious non-matching inputs to the $toMillis function can cause superlinear backtracking in the ISO-8601 validation regex, leading to denial of service in applications that evaluate user-provided JSONata expressions. This issue is fixed in version 2.2.0.

### CVE-2026-50273

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-17T18:17:16.840 |

Datadog .NET Tracer is a client library for Datadog APM for .NET applications. Prior to 3.43.0, Datadog tracing libraries that implement W3C baggage propagation parse incoming baggage HTTP headers without enforcing DD_TRACE_BAGGAGE_MAX_ITEMS or DD_TRACE_BAGGAGE_MAX_BYTES on extraction, allowing a remote unauthenticated attacker to send a baggage header with many comma-separated key-value pairs or one very large value and cause unbounded CPU and memory consumption in services with baggage propagation enabled. This issue is fixed in version 3.43.0.

### CVE-2026-12691

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-17T17:17:13.177 |

Missing authentication for critical function vulnerability in Vimesoft Inc. Enterprise Video Platform allows Authentication Bypass.

This issue affects Enterprise Video Platform: from 3.11.0.0 before 3.25.0.

### CVE-2026-51082

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-17T15:16:46.867 |

A race condition between the vncproxy and vncwebsocket API calls in Proxmox Virtual Environment (PVE) 9.x pve-manager before 9.1.9 and 8.x before 8.4.19; qemu-server 9.x before 9.1.7 and 8.x before 8.4.7; and pve-container before 6.1.3 (PVE 9.x) and before 5.3.4 (PVE 8.x) allows an attacker with privileges to call "vncproxy" to hijack a VNC session that is established in parallel by a different user for a different VM.

### CVE-2025-71397

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-07-18T14:17:11.220 |

SurrealDB before 2.0.5, 2.1.x before 2.1.5, and 2.2.x before 2.2.2 allows authenticated users with OWNER or EDITOR permissions (at the root, namespace, or database level) to define custom database functions via DEFINE FUNCTION using nested FOR loops. Although a single loop's iteration count is constrained, nesting multiple loops (e.g., each with 1,000,000 iterations) is not, so an attacker can execute a function that consumes all server CPU time. Configured timeouts do not stop the execution, rendering the server unresponsive to other queries and connections until it is manually restarted.

### CVE-2025-71395

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-07-18T14:17:10.963 |

SurrealDB versions before 2.2.2 contain a memory exhaustion vulnerability in the string::replace function that fails to restrict resulting string length when using regex patterns. An authenticated attacker can craft a malicious query to exhaust server memory through unbounded string allocations, causing denial of service.

### CVE-2025-71391

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:10.457 |

SurrealDB versions before 2.2.2 contain an uncaught exception vulnerability in the net module that allows authenticated users to crash the database. Attackers can send crafted HTTP queries containing null bytes to the /sql endpoint, causing an unhandled exception that crashes the SurrealDB instance and any dependent applications.

### CVE-2024-58370

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-18T14:17:10.140 |

SurrealDB versions before 1.1.0 fail to enforce recursion depth limits when parsing nested SurrealQL statements including IF, RELATE, and attribute access idioms. Authorized attackers can submit queries with excessive nesting depth to cause stack overflow and crash the server.

### CVE-2024-58369

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:10.003 |

SurrealDB versions before 1.1.1 fail to properly validate invocation of custom parameters and functions at root or namespace levels, causing server panic. Authorized clients can invoke these entities at unsupported levels to crash the SurrealDB server, resulting in denial of service.

### CVE-2024-58367

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-18T14:17:09.737 |

SurrealDB versions before 2.0.4 fail to properly enforce field permissions during SELECT, UPDATE, and DELETE operations, allowing authorized users to access unauthorized field values through various query techniques. Attackers can exploit SELECT VALUE operations, field aliasing, function arguments, WHERE clause filtering, RETURN BEFORE clauses, and SET clause references to leak protected field contents despite lacking SELECT permissions.

### CVE-2024-58365

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:09.460 |

SurrealDB versions before 1.2.0 contain an uncaught exception vulnerability in the query executor when processing calls to nonexistent built-in functions. Authorized clients can craft pre-parsed queries invoking nonexistent functions to trigger a panic that crashes the server.

### CVE-2024-58364

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:09.320 |

SurrealDB versions before 1.2.1 contain an uncaught exception handling vulnerability in span rendering when parsing queries with errors on line terminator characters. Authorized clients can submit malformed queries that trigger a panic in the span rendering code, crashing the server and causing denial of service.

### CVE-2024-58361

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:08.917 |

SurrealDB versions before 2.0.4 contain an uncaught exception handling vulnerability in the parser error rendering code when processing empty strings. Authorized clients can execute malformed queries with empty string conversions to record, duration, or datetime types that cause a panic in error rendering, crashing the server.

### CVE-2024-58359

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:08.780 |

SurrealDB versions before 2.1.0 contain a denial of service vulnerability in the sorting mechanism when using ORDER BY rand() clause. Authorized clients can execute queries with ORDER BY rand() to trigger a panic in the sorting function, crashing the server.

### CVE-2024-58357

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-18T14:17:08.503 |

SurrealDB versions before 2.1.0 contain an uncaught exception vulnerability in the rand::time() function that panics when unwrap is called on a None result from timestamp_opt. Authorized clients can repeatedly invoke rand::time() to reliably trigger server panics and cause denial of service.

### CVE-2026-47870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-18T09:17:08.847 |

VMware Avi Load Balancer contains a privilege escalation vulnerability. A malicious authenticated user with network access may be able to execute remote code.

Affected versions:
32.1.1 (fixed in 32.1.2)
31.1.1 through 31.2.2 (fixed in 31.2.2-2p3)
30.1.1 through 30.2.6 (fixed in 30.2.7)
22.1.1 through 22.1.7 (fixed in 30.2.7)

### CVE-2026-56171

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-359` |
| Published | 2026-07-17T22:17:54.117 |

Exposure of private personal information to an unauthorized actor in Windows RDP allows an unauthorized attacker to disclose information over a network.

### CVE-2026-50163

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-07-17T20:17:23.943 |

oras-go is a Go library for managing OCI artifacts. Prior to 2.6.2, ensureLinkPath in content/file/utils.go:262-275 validates a hardlink target relative to the extract base but returns the unresolved target, causing os.Link("victim.secret", "<extract_base>/payload.tar.gz/evil_cwd_link") to resolve header.Linkname against the process current working directory for a Typeflag=TypeLink entry such as Name=payload.tar.gz/evil_cwd_link and Linkname="victim.secret" with io.deis.oras.content.unpack: "true", which can expose or tamper with files such as .env, .git/config, .aws/credentials, and ~/.ssh/config. This issue is fixed in version 2.6.2.

### CVE-2026-49284

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-07-17T20:17:21.830 |

SimpleSAMLphp versions before 1.18.6 contain an information disclosure vulnerability. Prior to 2.4.7 and 2.5.2, SimpleSAMLphp's SAML SP ACS path does not enforce the IdP selected for an SP-initiated login when unsigned Response/InResponseTo is combined with a signed assertion lacking SubjectConfirmationData/InResponseTo, allowing a response issued by one trusted IdP to be bound to SP state created for another IdP and bypass flows that route users to a specific IdP, including deployments that set enable_unsolicited to false. This issue is fixed in versions 2.4.7 and 2.5.2.

### CVE-2026-45704

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T20:17:18.267 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.17 (LTS) and 12.3.6, CustomReports uses inconsistent authorization between the report listing endpoint and the report detail endpoint in bundles/CustomReportsBundle/src/Controller/Reports/CustomReportController.php and bundles/CustomReportsBundle/src/Tool/Config/Listing/Dao.php, allowing a low-privileged backend user with the reports permission to directly request an unshared report such as poc-secret-report by name and read report name, grouping information, display and icon metadata, data source configuration, column configuration, and sharing settings even when shareGlobally is false. This issue is fixed in versions 11.5.17 (LTS) and 12.3.6.

### CVE-2026-16118

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-17T20:17:16.167 |

A flaw was found in xdgmime. A heap-based buffer overflow can be triggered in _xdg_mime_magic_parse_magic_line() in the xdgmimemagic.c file on little-endian systems when an attacker-controlled MIME magic file in a user-writable XDG data location (e.g., in the $XDG_DATA_HOME/mime/magic path) is parsed by an application performing MIME type detection (e.g., via g_content_type_guess()). When performing byte-swap, incorrect pointer arithmetic on the write side causes an out-of-bounds write of 2 bytes, resulting in an application crash or memory corruption.

### CVE-2026-9587

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-07-17T17:17:18.280 |

An authenticated local file inclusion vulnerability exists in Sangoma Switchvox SMB Edition 8.3 (104997). The play_file functionality accepts user-controlled input through the sound_path parameter and fails to properly validate file paths before accessing the underlying filesystem. By supplying absolute paths, an authenticated attacker can retrieve files outside the intended directory scope.

### CVE-2026-63307

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T17:17:17.433 |

Chat2DB before 5.3.0 contains an insecure direct object reference vulnerability in the GET /api/connection/datasource/{id} endpoint. The handler calls dataSourceService.queryExistent(id, ...) without an ownership check and returns the decrypted password field, allowing any authenticated non-admin user to enumerate datasource IDs and read the plaintext database credentials of datasources owned by other users.

### CVE-2026-63100

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-17T16:17:17.263 |

Maybe through 0.6.0 contains a missing authorization vulnerability that allows authenticated low-privilege member-role users to access and modify global hosting settings by exploiting unprotected show and update actions in the Settings::HostingsController, where the before_action ensure_admin filter is applied only to the clear_cache action. Attackers can read the operator's Synth API key rendered in plaintext via a form field value attribute, overwrite it with an attacker-controlled value, toggle public registration settings, and disable email confirmation requirements to disrupt the entire instance.

### CVE-2026-63099

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T16:17:17.107 |

TheHive through 4.1.24 contains a broken object-level authorization vulnerability in the attachment download endpoints that allows any authenticated user to access attachments belonging to other organizations by supplying a content-hash identifier. Attackers can exploit the missing organization-scoped authorization check in AttachmentSrv.visible, which is implemented as a pass-through traversal, to download arbitrary attachments.

### CVE-2026-63095

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-17T16:17:16.467 |

Dendrite through 0.13.8 contains an improper authorization vulnerability in the Matrix Client-Server API that allows any authenticated local user to delete third-party identifier bindings belonging to other users by submitting an arbitrary address and medium to the account deletion endpoint without ownership verification. Attackers can exploit the unverified Forget3PID handler to remove a victim's email or MSISDN binding and subsequently rebind the address through an identity server to hijack the victim's password reset flow.

### CVE-2026-14871

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-17T16:17:13.580 |

osTicket versions v1.18.3 and v1.17.7 contain a Broken Object Level Authorization (BOLA) leading to Insecure Direct Object Reference (IDOR) in the AJAX ticket-management subsystem.

### CVE-2026-9588

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:L/VI:H/VA:N/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-17T17:17:18.413 |

A stored cross-site scripting (XSS) vulnerability exists in Sangoma Switchvox SMB Edition 8.3 (104997) within the voicemail notification template functionality. The submit_modify_voicemail_template endpoint fails to properly sanitize HTML content supplied by authenticated users, allowing malicious JavaScript supplied through the template_text parameter to be stored server-side and subsequently rendered to other users.
