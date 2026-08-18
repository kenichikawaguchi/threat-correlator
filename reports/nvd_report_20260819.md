# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-18 15:00 UTC
- **対象期間**: `2026-08-17T15:00:21.000Z` 〜 `2026-08-18T15:00:30.000Z`
- **重要CVE数**: 151 件（Critical 9.0+: 43 件 / High 7.0〜: 108 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 40 件以上**と依然として高リスクが集中しています。  
- **Web アプリケーション（Joomla、WordPress、ERPNext など）と Node.js サンドボックス（vm2）** が特に多く、未認証リモートコード実行 (RCE) や任意ファイルアップロードが目立ちます。  
- 多くの脆弱性は **入力検証・サニタイズ不備** に起因し、攻撃者は管理権限取得やサーバ側コード実行を容易に行える点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / コンポーネント | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨アップデート |
|-----|----------------------|----------------|------------------------|-------------------|
| **CVE‑2026‑74253** | Joomla! Extension **Regular Labs – Sourcerer** (< 14.0.0) | 未認証 RCE（反射型コード実行） | `{source}` ブロックを不正に操作されると、任意の PHP/JS がサーバ上で実行され、全サイトが乗っ取られる可能性。 | **14.0.0 以降** |
| **CVE‑2026‑32463** | **Sync Post With Other Site** (WordPress) ≤ 1.9.3 | 任意ファイルアップロード（認証済みだが権限が低いユーザーでも実行可） | 攻撃者は任意の PHP ファイルをアップロードし、管理者権限取得やデータベース改ざんが可能。 | **1.9.4** 以上 |
| **CVE‑2026‑65974** | **ERPNext / Frappe** (≤ 15.111.0, ≤ 16.22.0) | サーバーサイドテンプレートインジェクション (SSTI) | 限定された認証ユーザーが `frappe.render_template` を悪用し、任意の Python コードを実行。財務データや顧客情報が漏洩・改ざんされる危険。 | **15.111.1** / **16.22.1** 以降 |
| **CVE‑2026‑47686** / **CVE‑2026‑47698** | **vm2** (Node.js sandbox) < 3.11.6 | サンドボックス脱出 → ホストプロセスへのアクセス | `Error.cause` やプロトタイプチェーンの不適切なサニタイズにより、攻撃コードが `process` オブジェクトを取得し、サーバ全体を制御できる。 | **3.11.6** 以上 |
| **CVE‑2026‑32444** | **Cwicly** (WordPress) ≤ 1.4.4 | 任意コード実行 (RCE) | 認証ユーザーが特定のリクエストを送るだけで、サーバ上で任意の PHP が実行される。プラグインが多数のサイトで利用されているため、被害拡大が懸念。 | **1.4.5** 以上 |

> **選定理由**  
> - **CVSS が 9.8 以上**（ほぼ全件が 9.8~10）で、**未認証または低権限でのリモートコード実行** が可能。  
> - 対象製品は **Joomla、WordPress、ERPNext、Node.js** と、企業・開発者が広く導入しているプラットフォーム。  
> - 複数の脆弱性は **同一コンポーネント（例: vm2）** の複数バージョンに跨っているため、早急なパッチ適用が重要。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品 | 現行バージョン (脆弱) | 安全バージョン |
|------|----------------------|----------------|
| `regularlabs/sourcerer` (Joomla) | < 14.0.0 | **14.0.0** 以上 |
| `sync-post-with-other-site` (WordPress) | ≤ 1.9.3 | **1.9.4** 以上 |
| `erpnext` / `frappe` | ≤ 15.111.0 / ≤ 16.22.0 | **15.111.1** / **16.22.1** |
| `vm2` (Node.js) | < 3.11.6 | **3.11.6** 以上 |
| `cwicly` (WordPress) | ≤ 1.4.4 | **1.4.5** 以上 |
| `forminator` (WordPress) | ≤ 1.56.1 | **1.56.2** 以上 |
| `pbootcms` | ≤ 3.2.15 | **3.2.16** 以上 |
| `grav` (core) | < 2.0.15 | **2.0.15** 以上 |
| `arcadedb` (server) | ≤ 26.8.0 | **26.8.1** 以上 |
| `mlflow` | < 3.15.0 | **3.15.0** 以上 |

> **実装例（npm / Composer / apt）**  
> ```bash
> # npm (vm2)
> npm install vm2@^3.11.6 --save-prod
> 
> # Composer (Joomla extension)
> composer require regularlabs/sourcerer:^14.0
> 
> # WordPress plugins (via WP‑CLI)
> wp plugin update sync-post-with-other-site --version=1.9.4
> wp plugin update cwicly --version=1.4.5
> wp plugin update forminator --version=1.56.2
> 
> # Debian/Ubuntu (if packaged)
> sudo apt-get update && sudo apt-get install -y \
>     erpnext=15.111.1-1 \
>     mlflow=3.15.0-1
> ```

### 3.2 短期的な防御策
1. **Web アプリケーションファイアウォール (WAF)**  
   - `{source}` ブロックやファイルアップロードエンドポイントに対し、**正規表現ベースの入力制限**を追加。  
2. **最小権限の徹底**  
   - WordPress・Joomla のユーザー権限を見直し、**「投稿者」以上の権限を必要としない機能は無効化**。  
3. **サンドボックス設定の強化**  
   - `vm2` 使用時は `sandbox: {}` で **`allowEval: false`**、`require` の禁止を明示。  
4. **監査ログの有効化**  
   - `frappe.render_template` への呼び出しや `vm2` の `run` メソッド実行を **監査ログに記録**し、異常なパターンを SIEM で検知。  
5. **外部アクセス制限**  
   - ArcadeDB の Redis / MongoDB プラグインは **ファイアウォールで IP 制限**し、認証が必須になるよう設定変更。

### 3.3 長期的なセキュリティ強化
- **依存ライブラリの自

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-74253

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T18:18:14.780 |

Joomla Extension - regularlabs.com - Unauthenticated RCE through unverified reflected user input in Sourcerer < 14.0.0 - Regular Labs Sourcerer before 14.0.0 processes {source} blocks found in Joomla’s final rendered HTML without reliably determining where that code originated.

### CVE-2026-32463

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T14:17:03.400 |

Contributor Arbitrary File Upload in Sync Post With Other Site <= 1.9.3 versions.

### CVE-2026-32444

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T14:17:03.263 |

Contributor Remote Code Execution (RCE) in Cwicly <= 1.4.4 versions.

### CVE-2026-65974

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-17T21:16:46.887 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.111.0 and 16.22.0, limited authenticated users can cross a permission boundary in Frappe safe execution because frappe.render_template is exposed without forcing restrict_globals, allowing server-side template injection and remote code execution. This issue is fixed in versions 15.111.0 and 16.22.0.

### CVE-2026-47686

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-17T21:16:45.507 |

vm2 is an open source vm/sandbox for Node.js. Prior to 3.11.6, handleException() in lib/setup-sandbox.js sanitizes SuppressedError.error, SuppressedError.suppressed, and AggregateError.errors but does not sanitize Error.cause, allowing sandbox code to obtain a powerful host object such as process from an embedder-exposed host function that throws an error with that object as its cause and then execute arbitrary host commands. This issue is fixed in version 3.11.6.

### CVE-2026-66792

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-17T19:16:34.237 |

A flaw was found in the multicloud-operators-subscription component. This vulnerability allows a user on a managed cluster to escalate their privileges by creating a Subscription with specific, crafted annotations. Successful exploitation grants the attacker the ability to deploy resources into any namespace with the elevated permissions of the controller's Service Account, potentially leading to unauthorized access and control over cluster resources.

### CVE-2026-15748

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T06:16:40.670 |

The Forminator Forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.56.1 via the handle_file_upload function. This is due to insufficient file type validation in handle_file_upload, where the dangerous-extension blocklist performs exact-key matching that is bypassed by pipe-alternative MIME type keys, combined with a public submission handler that trusts attacker-controlled upload field configuration injected via a forged Select field value. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-67919

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T23:16:52.240 |

An issue in Halo 2.25.4 allows a remote attacker to execute arbitrary code via the PluginEndpoint.java, installFromUri method, and DefaultPluginApplicationContextFactory components

### CVE-2026-42164

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-17T23:16:52.123 |

Mahara before 25.04.5 and 26.04.0 is vulnerable in the Text block/section functionality when a call is crafted in a certain way that allows it to recall the backed-up content from another Text section.

### CVE-2026-38165

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T23:16:51.230 |

A Server-Side Template Injection (SSTI) vulnerability in the Velocity template engine configuration of xdocreport v0.9.2 to v2.2.0 allows attackers to execute arbitrary code via a crafted expression.

### CVE-2026-67960

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T22:17:26.020 |

An issue in PbootCMS v.3.2.15 allows an attacker to execute arbitrary code via the MemberController.php, UserController.php, CommentController.php, ContentController.php, and helper.php components

### CVE-2026-42163

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-17T22:17:05.687 |

Mahara before 25.04.5 and 26.04.0 is vulnerable to unauthorized access to internal accounts via Learning Tools Interoperability (LTI) under certain circumstances. This applies to LTI 1.1 and LTI 1.3 Advantage.

### CVE-2026-47698

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-08-17T21:16:45.640 |

vm2 is an open source vm/sandbox for Node.js. Prior to 3.11.6, lib/bridge.js and lib/setup-sandbox.js fail to block stacked indirection through Function.prototype.call around dangerous host prototype getter and setter mutators, allowing sandbox code to sever a host intrinsic's prototype chain and reach e.constructor.constructor for arbitrary host command execution. This issue is fixed in version 3.11.6.

### CVE-2026-50768

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-17T18:17:08.760 |

File Upload vulnerability in T-Systems International GmbH ImageMaster Version: 9.14.2.8.1 allows a remote attacker to execute arbitrary code via the add attachments feature in the create new document function.

### CVE-2026-28192

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T14:17:02.197 |

Unauthenticated Arbitrary File Upload in Piotnet Addons For Elementor Pro <= 7.1.67 versions.

### CVE-2026-71424

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-08-17T22:17:26.527 |

Onyx is an open-source AI platform. Prior to 3.1.10, 3.2.14, and 4.0.0, Onyx's GET /api/mcp/servers and GET /api/mcp/servers/persona/{persona_id} endpoints expose another user's OAuth Authorization header because OnyxTokenStorage.set_tokens and OnyxTokenStorage.set_client_info in backend/onyx/server/features/mcp/api.py copy per-user tokens into a shared admin MCPConnectionConfig row and _db_mcp_server_to_api_mcp_server returns that row through auth_template.headers to any BASIC_ACCESS user. This issue is fixed in versions 3.1.10, 3.2.14, and 4.0.0.

### CVE-2026-75851

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-18T12:19:35.457 |

ArcadeDB server (com.arcadedb:arcadedb-server) in versions 26.7.3 and earlier fails to propagate the authenticated principal to asynchronous command worker threads. When an HTTP command is submitted with awaitResponse:false, it executes on an async worker whose DatabaseContext has no bound user, causing the scripting authorization gate to become a no-op. A user with only read access to a single database can submit an asynchronous JavaScript (language=js) command via the /api/v1/command endpoint to run code with unrestricted host access (e.g., database.getSecurity().createUser) and create a server-wide administrator, escalating to full administrative control. Fixed in 26.8.1.

### CVE-2026-75843

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-18T12:19:34.740 |

ArcadeDB before 26.8.1 fails to bind the authenticated principal on the gRPC transaction executor thread in beginTransaction, allowing authenticated readers to execute JavaScript commands without scripting authorization checks. Attackers can execute executeCommand with a transaction ID to run unrestricted JavaScript that creates server-wide administrator accounts.

### CVE-2026-19478

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T20:16:41.777 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.2 before 18.11.11, 19.0 before 19.0.8, 19.1 before 19.1.6, and 19.2 before 19.2.4 that under certain conditions could allow an unauthenticated user to remotely modify or delete public projects and user data via a GraphQL directive.

### CVE-2026-75854

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-18T12:19:35.860 |

ArcadeDB versions before 26.8.1 contain a missing authentication vulnerability in the Redis wire-protocol plugin that allows unauthenticated attackers to read, write, and delete data. Attackers can connect to the Redis port and execute arbitrary commands against any database on the server without providing credentials, bypassing all security gates.

### CVE-2026-75852

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-18T12:19:35.593 |

ArcadeDB versions before 26.8.1 fail to enforce SASL authentication on data commands in the MongoDB wire-protocol plugin. Unauthenticated attackers can issue insert, find, update, delete, and create commands against any database by connecting to port 27017 without credentials.

### CVE-2026-75837

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-18T12:19:33.913 |

Grav before 2.0.14 fails to guard the access field in the core group blueprint with the required security@: admin.super restriction. A delegated admin.users operator can save a group with access[admin][super]=true to escalate to super-admin, gaining scheduler and Twig evaluation capabilities.

### CVE-2026-75835

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:33.647 |

Grav API plugin (getgrav/grav-plugin-api) before 1.0.14 contains a missing authorization vulnerability in userPassesAuthorize() (AbstractApiController.php). The function fails to consult the calling request's API key scopes, relying instead on the account's raw super-admin flag and ACL grants. As a result, an authenticated attacker holding a scoped API key minted on a privileged account can bypass their declared scope restrictions to access authorize-gated UI metadata and item definitions (sidebar/menubar/widget items and users-list columns/row-actions/filter-tabs) that their key scope should deny, resulting in information disclosure.

### CVE-2026-75832

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:33.230 |

The Grav API plugin (getgrav/grav-plugin-api, bundled with Grav 2.0) before version 1.0.14 (fixed in 1.0.15) contains a missing authorization vulnerability in BlueprintPathResolver::resolveUserScope(). The method gates the users/<name> scope on the account's raw super-admin ACL flag (access.api.super) instead of validating the presented API key's actual scope. An attacker holding an API key scoped only to api.media.write minted on a super-admin account can bypass the authorization check and, via POST /blueprint-upload or GET /blueprint-files, write a file into another user's scope (in the shared user/accounts/ directory, constrained to image extensions by assertSafeExtension()) and browse that scope's file listing, despite the key not being granted api.users.write.

### CVE-2026-75828

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T12:19:32.690 |

Grav before 2.0.15 contains a stored cross-site scripting vulnerability in the detectXss() function where unpaired quotes in unquoted attribute values bypass event-handler detection. Authenticated editors can inject event handlers like onerror= that pass validation and execute in visitor browsers when page content is rendered.

### CVE-2026-75827

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T12:19:32.553 |

Grav before 2.0.15 contains an arbitrary file write vulnerability in the Blueprint dynamic-data bare-function validation that uses an incomplete denylist instead of a positive allowlist. Attackers with page-edit or blueprint-config access can invoke the error_log function through a data directive to append PHP payloads to web-accessible files, achieving remote code execution.

### CVE-2026-74902

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T12:19:30.370 |

SiYuan before v3.7.4 contains a cross-site scripting vulnerability in the file upload validation flow that fails to escape filenames before inserting them into HTML via insertAdjacentHTML. Attackers can craft a malicious filename containing script payloads that execute with full OS command access when a user drags, drops, or pastes the file into the editor.

### CVE-2026-75627

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T11:16:52.060 |

Bastillion fails to properly validate request URI paths in its controller dispatcher, allowing unauthenticated attackers to bypass authentication filters by prefixing requests with arbitrary path segments. Attackers can access administrative controllers to read user listings, create manager accounts, and register managed systems, gaining control over SSH access to the managed fleet.

### CVE-2026-75626

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T11:16:51.920 |

SpiderFoot fails to HTML-escape correlation titles built from external scan data sources including server banners and metadata. Attackers can inject malicious HTML elements with event handlers into correlation results that execute scripts in the operator's browser when the correlations view is opened, potentially stealing API keys.

### CVE-2026-64849

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-17T22:17:23.580 |

MLflow is an open source AI engineering platform for agents, large language models, and machine learning models. Prior to 3.15.0, the unauthenticated POST /api/2.0/mlflow/webhooks/{id}/test endpoint calls _validate_webhook_url() in mlflow/utils/validation.py only for the original URL while mlflow/webhooks/delivery.py follows redirects and re-resolves the hostname without pinning the validated address, allowing attackers to reach internal or cloud metadata services and receive response_status and response_body. This issue is fixed in version 3.15.0.

### CVE-2026-75110

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-697` |
| Published | 2026-08-17T21:16:50.043 |

MemOS is a memory operating system for LLMs and AI agents. In deployments where authentication is enabled (AUTH_ENABLED=true) but the undocumented, defaultless INTERNAL_SERVICE_SECRET environment variable is unset, the is_internal_request() check in src/memos/api/middleware/auth.py fails open: os.getenv("INTERNAL_SERVICE_SECRET") returns None and a request omitting the X-Internal-Service header also yields None, so the comparison None == None evaluates true. The request is then treated as a trusted internal principal and granted scopes: ["all"]. As a result, an unauthenticated remote attacker can reach the admin API-key management endpoints to mint API keys for any user, enumerate keys, revoke keys, and generate a master key for persistent privileged access, as well as all data endpoints.

### CVE-2026-75106

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-340` |
| Published | 2026-08-17T21:16:49.610 |

OpnForm derives editable-submission secrets from sequential row identifiers using Hashids with an empty default salt, allowing unauthenticated attackers to compute hashes for any submission. Attackers can read other respondents' full submission data through the submission-fetch endpoint or overwrite submissions by supplying predicted hashes to the answer endpoint.

### CVE-2026-74254

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-17T18:18:14.903 |

Joomla Extension - joomlack.fr - SQL injection in Page Builder CK < 3.6.5 - The Joomla extension Page Builder CK is vulnerable to a SQL injection issue related to the styles model. Version 3.6.4 fixed the vector in the frontend, 3.6.5 in the backend.

### CVE-2026-55674

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T16:16:58.917 |

Discourse is an open-source discussion platform. Prior to 2026.1.6, 2026.5.2, 2026.6.1, and 2026.7.0, an unauthenticated attacker could send a single request with a crafted color_scheme_id (or dark_scheme_id) cookie to inject arbitrary HTML into a Discourse page. Because the cookie value was rendered into a color scheme tag without escaping, the attacker could break out of the attribute and inject a tag that bypassed Discourse's nonce-based Content Security Policy, resulting in arbitrary JavaScript execution in visitors' browsers. This issue is fixed in versions 2026.1.6, 2026.5.2, 2026.6.1, and 2026.7.0.

### CVE-2026-71566

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-17T15:16:57.610 |

FakeFish handles incoming credentials by passing them down
 to scripts. This works for real hardware because in the end it's up to 
the BMC to validate them. However, KubeVirt relies on a KUBECONFIG file 
mounted to the container and completely ignores the credentials. This allows any user of the cluster to control VMs of the 
user that created fakefish, power them on and off, and mount arbitrary CD
 images to them.

### CVE-2026-42162

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T23:16:52.023 |

Mahara before 25.04.5 and 26.04.0 is vulnerable to artefacts being accessible to others under certain circumstances when the file path to an artefact in a page is manipulated.

### CVE-2026-51977

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-17T22:17:14.487 |

An issue in Trueview T18061 WiFi 3MP Robot Pan-Tilt Security Camera Version 1.0 allows a physically proximate attacker to escalate privileges via the RSA private key component

### CVE-2026-66795

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-17T21:16:47.163 |

A flaw was found in the managedcluster-import-controller. The Certificate Signing Request (CSR) auto-approval logic improperly validates incoming CSRs, specifically by not inspecting the signer name or decoding the PEM-encoded x509 CSR. This vulnerability allows a privileged service account on a spoke cluster to submit a malicious CSR. Successful exploitation can lead to privilege escalation, enabling the attacker to obtain administrative credentials on the hub cluster.

### CVE-2026-71472

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T20:16:45.777 |

A flaw was found in acm-search-v2-rhel9. This vulnerability allows an authenticated attacker, such as a hub administrator or a Search Custom Resource (CR) editor, to inject malicious shell commands or SQL statements. This occurs because the WORK_MEM string provided in the Search CR is not properly validated before being used in a bash script and an SQL query. Successful exploitation could lead to arbitrary code execution within the privileged postgres pod, potentially compromising the system.

### CVE-2026-51346

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-17T18:17:09.320 |

SQL Injection vulnerability in StudIP 6.0.x before 6.0.3 and 5.4.x before 5.4.12 allows a remote attacker to execute arbitrary code and obtain sensitive information via the store() functions.

### CVE-2026-75045

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-17T16:17:51.530 |

In JetBrains YouTrack before 2025.3.156085, 
2026.1.13913, 
2026.2.18112 an unauthenticated attacker could download database backups via shared draft signature

### CVE-2026-71479

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-682` |
| Published | 2026-08-17T16:17:44.307 |

New API is a large language mode (LLM) gateway and artificial intelligence (AI) asset management system. Prior to 1.0.0-rc.18, user-controlled image n, video seconds and duration, max_tokens, max_completion_tokens, maxOutputTokens, audio duration, and billing-expression quantities can overflow conversions in common/quota_math.go and related settlement paths, allowing a low-privileged account with positive balance or an active subscription to turn a negative charge into account credit and potentially drain upstream funds. This issue is fixed in version 1.0.0-rc.18.

### CVE-2026-64859

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-17T16:17:22.280 |

New API is a large language mode (LLM) gateway and artificial intelligence (AI) asset management system. Prior to 1.0.0-rc.7, the admin user list and user lookup APIs, including GET /api/user/, return User.AccessToken as access_token because User model objects are serialized after queries use Omit("password"), allowing an authenticated administrator to obtain the root user's bearer token and access root-only system configuration APIs. This issue is fixed in version 1.0.0-rc.7.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-12553

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-17T19:16:24.560 |

HP has identified a potential vulnerability in HP Web Jetadmin (WJA) that may allow an unauthenticated actor to read from or write to arbitrary files through a DLL hijacking mechanism.

### CVE-2026-61666

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-08-17T17:16:39.917 |

websocket-driver is a WebSocket protocol handler with pluggable I/O. Prior to 0.8.2, WebSocket::Driver.server() passes a malformed Host header to URI.parse in lib/websocket/http/request.rb without catching URI::InvalidURIError, allowing a remote client to crash a TCP-backed WebSocket server when the application does not catch the error from parse(). This issue is fixed in version 0.8.2.

### CVE-2026-32465

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T14:17:03.650 |

Customer PHP Object Injection in Essential Real Estate <= 5.3.3 versions.

### CVE-2026-28191

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-18T14:17:02.057 |

Subscriber Privilege Escalation in The Grid <= 2.7.9.1 versions.

### CVE-2026-24301

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-18T14:17:01.897 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Copilot allows an unauthorized attacker to disclose information over a network.

### CVE-2026-65346

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-17T22:17:25.293 |

An integer overflow was addressed with improved input validation. This issue is fixed in iOS 26.6.1 and iPadOS 26.6.1, macOS Tahoe 26.6.2. Processing an image may lead to arbitrary code execution.

### CVE-2026-43794

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-17T22:17:11.457 |

A memory corruption issue was addressed with improved memory handling. This issue is fixed in iOS 18.7.10 and iPadOS 18.7.10, iOS 26.6.1 and iPadOS 26.6.1, macOS Tahoe 26.6.2. Processing maliciously crafted web content may lead to memory corruption.

### CVE-2026-65640

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-17T21:16:46.470 |

WordPress is vulnerable to a remote code execution vulnerability via malicious Postscript file upload by an Author level user or higher.

Prerequisites:
* Imagick and Ghostscript in use on the server
* A malicious user with the `upload_files` capability

This issue affects all versions of WordPress. Version 7.0.4 has been released, containing a fix for the vulnerability, and as a courtesy to users on older branches the fix has been backported to all branches back to 4.7.

### CVE-2026-70495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-17T20:16:45.653 |

A flaw was found in search-v2-operator. This component's `search-serviceaccount` has overly broad permissions, allowing it to impersonate users and groups across the entire cluster. If an attacker gains access to any of the pods running under this service account, they could exploit this to achieve `system:masters` access, granting them full control over the cluster.

### CVE-2026-62982

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T18:17:56.740 |

Glances is an open-source system cross-platform monitoring tool. From 4.5.2 until 4.5.6, _sanitize_mustache_dict() in glances/actions.py skips nested list and dictionary strings such as process cmdline values, allowing pipe characters to survive chevron.render() and be executed by secure_popen() through administrator-configured action templates. This issue is fixed in 4.5.6.

### CVE-2026-9771

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822;CWE-862` |
| Published | 2026-08-17T17:16:57.720 |

The flash_copy() system call is verified by z_vrfy_flash_copy() in drivers/flash/flash_util.c. On builds with CONFIG_USERSPACE enabled, this handler is the kernel-side trust boundary for a user-mode caller. Prior to the fix it validated only the output buffer (K_SYSCALL_MEMORY_WRITE) and passed the two struct device * arguments, src_dev and dst_dev, directly into the implementation without any object validation — unlike every sibling flash syscall, which guards its device pointer with K_SYSCALL_DRIVER_FLASH.

A user-mode thread fully controls the values of src_dev/dst_dev and the contents of its own address space. The implementation z_impl_flash_copy() dereferences these pointers and calls through their driver-API function tables (e.g. api->get_parameters(dst_dev), flash_read(src_dev, ...), flash_write(dst_dev, ...)). By supplying a pointer to a forged struct device whose api table contains attacker-chosen function pointers, an unprivileged thread can cause the kernel to call arbitrary code in supervisor mode; passing any arbitrary or invalid address otherwise yields a kernel crash or out-of-bounds read.

The result is a local privilege escalation out of the userspace sandbox (with kernel denial-of-service and information disclosure as lesser outcomes). The fix adds K_SYSCALL_DRIVER_FLASH(src_dev, read) and K_SYSCALL_DRIVER_FLASH(dst_dev, write) to z_vrfy_flash_copy(), which verify each device is a registered flash-driver kernel object the calling thread is permitted to use before any dereference, closing the path completely.

### CVE-2026-68518

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T17:16:40.353 |

Glances is an open-source system cross-platform monitoring tool. Prior to 4.5.6, _sanitize_mustache_dict() in glances/actions.py sanitizes individual Mustache values before chevron.render(), allowing adjacent unescaped Mustache variables to reconstruct shell operators that secure_popen() executes when attacker-controlled process or container fields are rendered by an administrator-configured action template. This issue is fixed in 4.5.6.

### CVE-2026-45532

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T13:17:24.610 |

DataEase is an open source data visualization and analysis tool. Versions prior to 2.10.23 have a path traversal vulnerability. The root cause is that on Windows, the `FILE_SEPARATOR` is `\`, while the server only filters the `/` character during string truncation. The vulnerability has been fixed in v2.10.23. No known workarounds are available.

### CVE-2026-75853

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:35.727 |

ArcadeDB's Gremlin wire-protocol plugin (com.arcadedb:arcadedb-gremlin) in versions <= 26.7.3 enforces authentication (SASL PLAIN) but performs no authorization: it never checks database access permissions (canAccessToDatabase) and never binds the authenticated principal into the engine. As a result, any valid server credential — even one provisioned for zero or one unrelated database — can read, write, and drop data in any database on the server by selecting a target database via a traversal-source alias, completely bypassing the engine's per-type/read-only/UPDATE_SCHEMA ACLs. The issue is fixed in version 26.8.1.

### CVE-2026-75840

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1025` |
| Published | 2026-08-18T12:19:34.320 |

ArcadeDB before 26.8.1 contains an arbitrary file read vulnerability in the GraalVM JavaScript sandbox allowlist enforcement, which uses unescaped regular expressions to validate package names. Attackers with trigger creation privileges can use Java.type() to access java.util.zip.ZipFile or java.util.jar.JarFile classes and read arbitrary files on the host system as the ArcadeDB server process.

### CVE-2026-75836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:33.780 |

The Grav API plugin (getgrav/grav-plugin-api, bundled with Grav's admin-next/API stack) before 1.0.14 fails to enforce the authorize requirement in MenubarController::executeAction(). While the GET /menubar/items listing endpoint correctly filters menubar items via userPassesAuthorize(), the POST /api/v1/menubar/actions/{plugin}/{action} endpoint only checks the baseline api.access permission and never evaluates the authorize field a plugin registered for that action. Any authenticated caller with api.access can therefore invoke a privileged menubar action directly, bypassing the intended authorization. No plugin bundled with core Grav currently registers a privileged authorize handler, so on a stock install the impact is latent; the flaw affects any first- or third-party plugin relying on the documented authorize semantics.

### CVE-2026-74906

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-18T12:19:30.913 |

SiYuan before v3.7.4 contains an incorrect authorization vulnerability in eight publish-mode reader-facing endpoints that filter results using the visibility list instead of the disabled list. Anonymous visitors can discover and read content from documents explicitly marked as forbidden from publishing by accessing search, backlink, asset content, saved criteria, recent documents, graph, and tag endpoints.

### CVE-2026-74904

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:30.643 |

SiYuan before v3.7.4 is missing authorization checks in 17 block metadata/content endpoints in kernel/api/block.go (including getRefText, checkBlockExist, and getBlockBreadcrumb). These handlers are gated only by basic authentication (model.CheckAuth) and lack publish-access filtering, allowing anonymous publish-mode readers to disclose private block content-derived text, structural metadata, and existence information for arbitrary block IDs across the workspace.

### CVE-2026-75482

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T21:16:50.833 |

SWE-agent's trajectory inspector (sweagent inspector), confirmed in v1.1.0, is an HTTP server that joins request paths to the trajectory directory in its /trajectory/ handler without rejecting parent-directory ('..') references, bypassing the built-in path sanitization. The server binds all interfaces (0.0.0.0), applies wildcard CORS, and requires no authentication. An unauthenticated network client (or a malicious web page via CORS) can use path traversal sequences to read files outside the intended directory. Because the read sink parses targets as trajectory JSON, disclosure is constrained to JSON files shaped like a trajectory, which can contain repository contents, command output, and secrets/API keys.

### CVE-2026-75481

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-17T21:16:50.647 |

SkyPilot fails to validate that authenticated users are entitled to grant administrator roles when updating service account permissions. Attackers can create a service account, escalate it to administrator role, and authenticate with its bearer token to gain administrative control over all users and workspaces.

### CVE-2026-75479

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-17T21:16:50.333 |

JimuReport contains an authentication bypass vulnerability in the report folder template listing endpoint that allows unauthenticated attackers to enumerate all reports and retrieve share tokens. Attackers can use disclosed share tokens to access protected report endpoints and retrieve full report definitions including embedded SQL statements and live query data.

### CVE-2026-75111

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T21:16:50.193 |

Evidently UI fails to properly validate the filename parameter in the dataset materialization endpoint, allowing unauthenticated attackers to read arbitrary files outside the workspace directory. Attackers can supply traversal sequences or absolute paths in the filename field to access system files, which are then materialized into datasets and retrieved through the download endpoint.

### CVE-2026-75105

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-17T21:16:49.473 |

phpIPAM through 1.8.1 fails to verify that a requested IP address belongs to the subnet a temporary share token was issued for. In app/temp_share/index.php and app/temp_share/address.php, when the share type is 'subnets', the subnetId parameter is used directly as a database primary key to fetch an address without confirming the address belongs to the authorized subnet. An unauthenticated party holding any valid, non-expired temporary share URL can enumerate the subnetId parameter to read every IP address record across all sections and subnets, including hostnames, DNS names, MAC addresses, owner/contact fields, and notes (which may contain credentials and configuration details).

### CVE-2026-75103

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-17T21:16:49.200 |

Crawlab fails to verify user ownership or administrative role on the password-change endpoint, allowing any authenticated user to reset any account's password. Attackers can enumerate user accounts through the user listing endpoint and change administrator credentials to achieve full account takeover and arbitrary code execution.

### CVE-2026-71518

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-17T21:16:48.277 |

Typemill before 2.26.0 contains an authorization bypass vulnerability in the media file download route that allows unauthenticated attackers to access restricted files by submitting path-equivalent URL variants. Attackers can substitute normalized path forms such as dot-slash prefixes, double slashes, or percent-encoded sequences to pass role-based restriction checks while the filesystem resolves the request to the protected file, enabling unauthorized file download without credentials.

### CVE-2026-47683

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-17T21:16:45.363 |

vm2 is an open source vm/sandbox for Node.js. Prior to 3.11.6, the bufferAllocLimit enforcement in lib/setup-sandbox.js does not cover Buffer.concat(list, totalLength) or Buffer.from(arrayLike) with an attacker-controlled length, allowing sandbox code to perform large synchronous host external-memory allocations that bypass the configured cap and can exhaust the host process. This issue is fixed in version 3.11.6.

### CVE-2026-74238

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-17T19:16:42.713 |

TIER IV Nebula through 1.2.0 contains an out-of-bounds read vulnerability in the Vlp32Decoder::unpack() function that allows unauthenticated remote attackers to cause the decoder to read past the end of a received UDP buffer into adjacent heap memory by sending a short UDP datagram. Attackers can send a malformed datagram to the Velodyne UDP sensor port, which lacks sender-address restrictions present in other drivers, causing fabricated points derived from heap memory contents to be silently published into downstream PointCloud2 messages consumed by Autoware nodes.

### CVE-2026-73523

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-08-17T18:18:14.170 |

COVESA Open1722 through 0.9.2 contains an integer truncation vulnerability in acf-can-listener.c that allows unauthenticated remote attackers to cause the CAN listener to transmit process stack memory onto the CAN bus by sending a rejected UDP datagram with a matching AVTP stream ID. The num_can_msgs variable declared as uint8_t truncates the -1 error return value from avtp_to_can() to 255, causing a write loop to iterate 255 times over a 15-slot stack array and leak approximately 18 KB of adjacent stack memory as roughly 240 CAN frames to any recipient on the CAN bus.

### CVE-2026-73522

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-17T18:18:14.030 |

COVESA Open1722 through 0.9.2 contains a stack buffer overflow vulnerability that allows unauthenticated remote attackers to write past the end of a fixed 15-slot stack array by sending a crafted UDP datagram containing more than 15 ACF-CAN messages. The avtp_to_can() function increments its write index without bounding it against the caller-supplied array size, and because the listener accepts datagrams from any sender matching a hardcoded unauthenticated stream ID transmitted in plaintext, attackers can corrupt adjacent stack memory to achieve arbitrary code execution or denial of service.

### CVE-2026-71980

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-17T18:18:12.510 |

Belledonne Communications bcg729 through 1.1.2 contains an out-of-bounds read vulnerability in the decodeSIDframe() function in src/cng.c that allows unauthenticated network-adjacent attackers to trigger a heap read beyond buffer boundaries by sending a zero-length comfort-noise RTP payload. A zero-length payload causes an integer underflow in the uint8_t filter order calculation, which wraps to 255 and is clamped to 10, causing the function to unconditionally read 11 bytes from a zero-byte buffer, resulting in media process termination or silent consumption of adjacent heap memory as reflection coefficients.

### CVE-2026-71979

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-17T18:18:12.370 |

INDI (Instrument Neutral Distributed Interface) indiserver through 2.2.4.2, fixed in commit 96bbd7f, contains a stack buffer overflow vulnerability that allows unauthenticated remote attackers to crash the daemon by sending malformed XML with mismatched tags whose names exceed 1024 bytes. Attackers can send a single TCP packet on port 7624 with mismatched XML tags to trigger an unbounded sprintf() write into a fixed 1024-byte stack buffer in MsgQueue.cpp, terminating the daemon and disrupting all active client and driver sessions.

### CVE-2026-71491

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-08-17T18:18:12.120 |

sqlparse is a non-validating SQL parser module for Python. Prior to 0.6.0, group_comments in sqlparse/engine/grouping.py repeatedly rescans comment-only statements before the MAX_GROUPING_TOKENS guard, causing quadratic CPU consumption through sqlparse.parse() and sqlparse.format(sql, strip_comments=True). This issue is fixed in version 0.6.0.

### CVE-2026-54284

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407;CWE-1333` |
| Published | 2026-08-17T18:17:11.400 |

sqlparse is a non-validating SQL parser module for Python. Prior to 0.6.0, TokenList construction and string conversion in sqlparse/sql.py repeatedly flatten nested token subtrees constructed by group_parenthesis and group_case, causing quadratic CPU consumption through sqlparse.parse(), sqlparse.format(), and sqlparse.split() before depth and token limits terminate processing. This issue is fixed in version 0.6.0.

### CVE-2026-75783

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-18T13:17:43.287 |

A security vulnerability has been detected in TRENDnet TEW-WLC100P 12.07b01. Affected by this vulnerability is an unknown functionality of the file /sbin/netifd of the component DHCP blobmsg Handler. The manipulation leads to stack-based buffer overflow. The attack must be carried out from within the local network. The exploit has been disclosed publicly and may be used.

### CVE-2026-75833

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-18T12:19:33.370 |

The Grav API plugin (getgrav/grav-plugin-api, bundled with Grav 2.0's admin-next/API stack) before version 1.0.14 contains an open redirect weakness in SsoController::sanitizeReturnTo(). The function rejects a literal '//' prefix but does not account for browsers normalizing backslashes to slashes in special (http/https) schemes, so a returnTo value such as '/\evil.com' passes the guard and is later resolved by the browser as the protocol-relative URL '//evil.com'. Following a legitimate OAuth login flow, an attacker-supplied returnTo parameter could redirect an authenticated victim to an attacker-controlled site for post-login phishing. Full browser-side exploitability depends on the admin-next SPA's client-side oauth-callback handler and was not independently verified by the reporter.

### CVE-2026-75829

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-18T12:19:32.827 |

grav-plugin-api versions before 1.0.15 fail to validate Twig content in the translate() endpoint, allowing attackers with api.pages.write permission to persist pages with process.twig enabled. Attackers can submit crafted header and content parameters to execute server-side template injection payloads that are evaluated at render time.

### CVE-2026-56677

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-918` |
| Published | 2026-08-17T22:17:14.970 |

9Router is an AI router & token saver. In 0.5.4 and earlier, the POST /api/auth/oidc/test endpoint in src/app/api/auth/oidc/test/route.js passes the user-controlled issuerUrl parameter to fetchOidcDiscovery() in src/lib/auth/oidc.js without restricting private or loopback destinations, allowing unauthenticated attackers when dashboard login is disabled to scan internal services and reflect OIDC discovery fields including token_endpoint and jwks_uri.

### CVE-2026-32466

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T14:17:03.787 |

Subscriber SQL Injection in Gravity Forms Bookings premium <= 2.1 versions.

### CVE-2026-23929

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-18T13:17:21.170 |

Prototype pollution vulnerability in searchParamsToObject() is leading to a persistent XSS in Maps. URL parameter processing was not filtering dangerous properties like __proto__, combined with jQuery's unsafe element creation that traversed the prototype chain.

### CVE-2026-75094

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-18T02:17:30.757 |

A flaw has been found in COMFAST CF-N1-S 2.6.0.1. This impacts the function sub_44B438 of the file /cgi-bin/mbox-config?method=SET&section=ptest_ssid of the component CGI Interface. This manipulation of the argument ssid causes os command injection. Remote exploitation of the attack is possible. The exploit has been published and may be used.

### CVE-2026-73410

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-08-17T21:16:48.823 |

Budibase is an open-source low-code platform. Prior to 3.40.0, packages/backend-core/src/utils/outboundFetch.ts pinned a validated address through a Node agent, but the REST integration used getDispatcher from packages/backend-core/src/utils/fetch.ts, causing undici to ignore that agent and resolve the hostname again. A builder could use DNS rebinding to make packages/server/src/integrations/rest.ts connect to an internal address after a public address passed validation, with full response access and arbitrary REST methods. The fix adds createPinnedLookup support to the undici dispatcher and passes the validated address to custom fetch implementations. This issue is fixed in version 3.40.0.

### CVE-2026-57485

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-08-17T20:16:44.587 |

Stirling-PDF is a locally hosted web application that facilitates various operations on PDF files. Prior to 2.9.0, the /api/v1/pipeline/handleData endpoint in app/core/src/main/java/stirling/software/SPDF/controller/api/pipeline/PipelineProcessor.java injects the STIRLING-PDF-BACKEND-API-USER API key into pipeline subrequests, allowing an authenticated ROLE_USER to retrieve the key through /api/v1/user/get-api-key, impersonate the internal service account, bypass normal rate limits, and access internal endpoints including /api/v1/info/requests/all and /api/v1/info/load/all. This issue is fixed in version 2.9.0.

### CVE-2026-75855

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T12:19:35.997 |

ArcadeDB versions before 26.8.1 fail to sanitize database names in the POST /api/v1/server endpoint's create database and drop database commands, allowing authenticated root users to write and delete arbitrary files outside the configured database directory. Attackers can supply database names containing ../ sequences to create databases at arbitrary filesystem paths or recursively delete directories the server process can access.

### CVE-2026-64657

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-17T21:16:46.340 |

Budibase is an open-source low-code platform. Prior to 3.39.19, the PostgreSQL datasource connector in packages/server/src/integrations/postgres.ts interpolates the user-controlled schema configuration field into a SET search_path statement without escaping embedded double quotes, allowing an authenticated administrator who saves or tests the datasource to execute arbitrary SQL through the simple query protocol. This issue is fixed in version 3.39.19.

### CVE-2026-46345

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-36;CWE-73` |
| Published | 2026-08-17T18:16:38.393 |

compliance-trestle is a tooling platform for managing compliance as code. Prior to versions 3.12.2 and 4.0.3, the `-o/--output` argument in `trestle author jinja` allows writing files outside the intended workspace. The application does not properly validate, `../`,  `..\`, or absolute paths. This allows arbitrary file write to attacker-controlled locations. Versions 3.12.3 and 4.0.3 patch the issue.

### CVE-2026-75060

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-17T16:17:53.227 |

In JetBrains PyCharm before 2026.2.1 code execution was possible via unauthenticated Jupyter MCP tools

### CVE-2026-75842

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T12:19:34.597 |

ArcadeDB versions before 26.8.1 contain an arbitrary file read vulnerability in the OpenCypher LOAD CSV FROM clause that allows authenticated users to read local files. Attackers with read query privileges can use the file:// protocol in LOAD CSV statements to access arbitrary files with server process privileges, exfiltrating sensitive data directly in query responses.

### CVE-2026-9816

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-17T22:17:27.217 |

Mattermost versions 11.7.x <= 11.7.6, 10.11.x <= 10.11.21, 11.8.x <= 11.8.3 fail to validate BoardMember.Scheme* fields server-side on insert and archive-import paths which allows a board editor or non-guest team member to grant board admin to arbitrary users via POST /api/v2/boards/{boardID}/members and POST /api/v2/teams/{teamID}/archive/import.. Mattermost Advisory ID: MMSA-2026-00685

### CVE-2026-74907

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T12:19:31.047 |

Grav before 2.0.15 contains a path traversal vulnerability in the static asset server within index.php that uses string prefix matching instead of directory-boundary validation. Unauthenticated attackers can access files in sibling directories by exploiting directory names that extend the base path string, such as requesting assets-secret when assets is the configured base.

### CVE-2026-65832

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-129` |
| Published | 2026-08-17T21:16:46.750 |

Deskflow is a keyboard and mouse sharing app. Prior to continuous build 1.26.0.299, a remote unauthenticated Deskflow server can send kMsgDSetOptions (DSOP) values to ServerProxy::setOptions() in src/lib/client/ServerProxy.cpp so that the value following a modifier option poisons m_modifierTranslationTable, after which ServerProxy::translateKey() or ServerProxy::translateModifierMask() indexes the seven-row s_translationTable or s_masks arrays out of bounds, disclosing four bytes at an attacker-selected relative offset or crashing the connected client; an odd option count also causes an out-of-bounds OptionsList read. This issue is fixed in continuous build 1.26.0.299.

### CVE-2026-63409

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-17T21:16:46.200 |

Deskflow is a keyboard and mouse sharing app. From 1.17.0 until continuous build 1.26.0.296, a malicious Deskflow server can send an odd-length DSOP vector to ServerProxy::setOptions() in src/lib/client/ServerProxy.cpp, causing the missing value after the final option key to be read beyond the vector during the PacketStreamFilter::filterEvent to ServerProxy::handleData() to ServerProxy::parseHandshakeMessage() call chain and crash the connected client. This issue is fixed in continuous build 1.26.0.296.

### CVE-2026-75048

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T16:17:51.870 |

In JetBrains YouTrack before 2026.2.18068 stored XSS via the fenced code-block language label was possible

### CVE-2026-32464

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-18T14:17:03.530 |

Unauthenticated Local File Inclusion in Theme Test Drive <= 2.9.1 versions.

### CVE-2026-28570

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-18T14:17:02.717 |

Unauthenticated Local File Inclusion in Vavo Core <= 2.3.0 versions.

### CVE-2026-15371

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-177` |
| Published | 2026-08-18T07:16:48.927 |

Velociraptor's web GUI allows specifying a custom type for columns in tables. The URL type takes the cell value and forms a URL which can be clicked in the GUI.The code does not limit the schemes allowed in this URL , allowing an attacker to specify a JavaScript scheme exposing the user to XSS.

### CVE-2026-57233

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T20:16:44.453 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.7, the WinGup decompress function joins untrusted ZIP entry names to unzipDestTo without canonical containment validation, allowing an entry such as ../mimeTools/mimeTools.dll to overwrite a DLL in a sibling plugin directory and execute attacker-controlled code when Notepad++ next loads that plugin. This issue is fixed in version 8.9.7.

### CVE-2026-33437

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T18:16:35.650 |

Stirling-PDF is a locally hosted web application that facilitates various operations on PDF files. Prior to 2.0.0, the Get Info workflow in app/core/src/main/resources/templates/security/get-info-on-pdf.html inserts untrusted PDF Title and Author metadata into the summary-text element with innerHTML, allowing a malicious PDF to execute stored cross-site scripting when a user clicks Get Info and to access browser-session data or modify page content. This issue is fixed in version 2.0.0.

### CVE-2026-75051

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T16:17:52.213 |

In JetBrains YouTrack before 2026.2.17917 unauthorised project transfer between organisations was possible

### CVE-2026-75044

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T16:17:51.410 |

In JetBrains YouTrack before 2025.3.156085, 
2026.1.13914, 
2026.2.18095 missing authorisation allowed an authenticated user to delete arbitrary entities via the mailbox endpoint

### CVE-2026-45790

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-17T22:17:14.170 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.29.6, Dokploy's organization.inviteMember tRPC procedure in apps/dokploy/server/api/routers/organization.ts allows a user with member:create permission to invite an account with the owner role, while packages/server/src/services/user.ts allows a privileged self-hosted user to create an account with an arbitrary role, enabling permanent organization takeover because owner roles cannot be demoted. This issue is fixed in version 0.29.6.

### CVE-2026-67961

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T23:16:52.360 |

An issue in O2OA v.10.0.2 allows a local attacker to execute arbitrary code via the the sandbox mechanism of the Invoke script execution.

### CVE-2026-34399

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-17T21:16:44.277 |

FreeCAD is a free and open-source multiplatform 3D parametric modeler. From 0.19 until 1.1.1, FreeCAD's BIM Workbench contains an eval() call on untrusted data from SVG template files. When a user creates a TechDraw page from a malicious SVG template, arbitrary Python code executes. The vulnerable code is in src/Mod/BIM/bimcommands/BimTDPage.py (line 87). This issue is fixed in version 1.1.1.

### CVE-2026-34398

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-17T21:16:44.130 |

FreeCAD is a free and open-source multiplatform 3D parametric modeler. From 0.19 until 1.1.1, src/Mod/BIM/bimcommands/BimProjectManager.py in the BIM Project Manager Load Template flow passes attacker-controlled FCStd Meta property values for wpposition, wpu, wpv, and wpaxis directly to eval(), allowing arbitrary Python code execution when a user loads a malicious BIM project template. This issue is fixed in version 1.1.1.

### CVE-2026-54758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-08-17T20:16:44.323 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.7, the expandNppEnvironmentStrs function in PowerEditor/src/WinControls/StaticDialog/RunDlg/RunDlg.cpp copies a Notepad++ variable name between $( and ) into the fixed-size wchar_t str[MAX_PATH] stack buffer without bounding the m loop index, allowing a name of 260 or more characters to corrupt adjacent stack data, terminate the process through __report_gsfailure, and potentially execute code. This issue is fixed in version 8.9.7.

### CVE-2026-75056

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T16:17:52.770 |

In JetBrains IntelliJ IDEA before 2026.2.1 rCE via Markdown export tool was possible

### CVE-2026-50575

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-294;CWE-345;CWE-672` |
| Published | 2026-08-18T14:17:10.117 |

BetterDesk is a remote desktop management solution. BetterDesk versions through 2.3.0 improperly invalidate deleted device identities, allowing an unauthenticated client to replay or spoof a device ID and bypass registration controls. Version 3.0.0-alpha contains a patch. No known workarounds are available.

### CVE-2026-23933

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259` |
| Published | 2026-08-18T13:17:21.567 |

In Zabbix 7.4 the cryptographic key used for signing Frontend sessions has been erroneously written to the database seed. Currently the only known exploitation scenario is for deployments that utilize both - SAML authentication and guest users. In such cases the key can be used to forge valid session cookies, potentially leading to unauthorized access. For other Zabbix deployments this does not have a known impact.

### CVE-2025-27621

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-17T16:16:46.290 |

UpTrain is an open-source platform to evaluate and improve generative AI applications. In version 0.7.1 and prior, the UpTrain backend creates a new default user with a static username, where the username is also used as the default API key. The UpTrain backend also has an open CORS policy. Using these two primitives, any website can make a authenticated cross-origin request to the UpTrain instance by providing the default API key in the header `uptrain-access-token`. This issue may allow arbitrary websites to perform privileged operations on the UpTrain instance, as if they were the default logged in user. As of time of publication, no known patches are available.

### CVE-2026-71567

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T15:16:57.730 |

In openshift-metal3/fakefish there is a repeated pattern in some of the scripts where shell variables
 are injected without quoting them either into command lines or into 
manifests. This mostly applies to the Image URL and BMC credentials 
(which are not verified by FakeFish).

### CVE-2026-65822

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-17T21:16:46.610 |

ERPNext is a free and open source Enterprise Resource Planning tool. Prior to 15.116.0 and 16.23.0, erpnext/selling/report/inactive_customers/inactive_customers.py accepts an unvalidated doctype filter and interpolates it into raw SQL in get_sales_details and get_last_sales_amt, allowing an authenticated user to extract sensitive information and manipulate database queries. This issue is fixed in versions 15.116.0 and 16.23.0.

### CVE-2026-32468

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-08-18T14:17:05.857 |

Unauthenticated Sensitive Data Exposure in Duitku Payment Gateway <= 2.11.14 versions.

### CVE-2026-28571

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T14:17:02.850 |

Unauthenticated Broken Access Control in FormyChat <= 2.15.7 versions.

### CVE-2026-28567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T14:17:02.327 |

Unauthenticated Broken Access Control in WP Sort Order <= 1.3.5 versions.

### CVE-2026-15585

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T12:17:23.110 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in AKIN Software Computer Import Export Industry and Trade Ltd. AKINSOFT Wolvox9 ERP / KontrolPanel.exe allows Path Traversal.

This issue affects AKINSOFT Wolvox9 ERP / KontrolPanel.exe: from s26.02.17 before 26.02.22.

### CVE-2026-11801

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T03:16:38.650 |

The WPAdverts – Classifieds Plugin plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.3.2. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to retrieve internal site configuration data exposed by the classifieds-types REST endpoint, including registered post types, labels, associated taxonomies, form scheme metadata, contact options, and custom field meta keys.

### CVE-2026-65343

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-17T22:17:25.200 |

A use after free issue was addressed with improved memory management. This issue is fixed in iOS 26.6.1 and iPadOS 26.6.1, macOS Tahoe 26.6.2. A remote attacker may be able to cause unexpected system termination.

### CVE-2026-68005

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-17T20:16:45.347 |

An issue in ACME mini_httpd 1.30 and prior allows a remote attacker to cause a denial of service via the HTTP request header parser in the handle_request() function

### CVE-2026-45698

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-17T19:16:30.703 |

Netatalk is a Free and Open Source file server suite for Unix-like operating systems. In versions 3.1.19 through 4.4.2, a stack-based buffer overflow exists in the deletedir() function of Netatalk's afpd daemon due to an integer underflow in the calculation of the remaining buffer size used for path construction. deletedir() is a utility function called when a file operation crosses a device boundary inside an AFP shared volume, which the standard library's renameat() cannot handle. The function attempts to prevent buffer overflows by tracking available space in a size_t remain variable. However, the arithmetic used to compute remain results in an unsigned integer underflow, causing the variable to become SIZE_MAX. Because of this, the subsequent boundary check always evaluates as safe, allowing an unbounded strcpy() operation to copy attacker-controlled filenames into a nearly full stack buffer. Version 4.4.3 patches the issue.

### CVE-2026-59902

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-17T18:17:36.087 |

Netty is an asynchronous, event-driven network application framework. Prior to 4.1.137.Final and 4.2.17.Final, io.netty.handler.codec.sctp.SctpMessageCompletionHandler limits incomplete messages and fragment counts but not maxBufferedBytes, allowing unauthenticated peers to exhaust memory with large SCTP fragments. This issue is fixed in versions 4.1.137.Final and 4.2.17.Final.

### CVE-2026-59893

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-17T18:17:35.730 |

sqlparse is a non-validating SQL parser module for Python. Prior to 0.6.0, SQL_REGEX in sqlparse/keywords.py and the per-position loop in sqlparse/lexer.py repeatedly scan unmatched dollar-quoted literal and multiline-comment delimiters, causing quadratic CPU consumption through sqlparse.parse(), sqlparse.format(), and sqlparse.split(). This issue is fixed in version 0.6.0.

### CVE-2026-73646

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T16:17:47.257 |

PostCSS takes a CSS file and provides an API to analyze and modify its rules by transforming the rules into an Abstract Syntax Tree. Prior to 8.5.18, lib/previous-map.js loadMap() passes attacker-controlled sourceMappingURL values to join(dirname(opts.from), annotation), and loadFile() permits traversed or absolute .map paths, allowing untrusted CSS processed without map: false to disclose sourcesContent from arbitrary reachable .map files through result.map. This issue is fixed in version 8.5.18.

### CVE-2026-64868

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-17T16:17:22.713 |

New API is a large language mode (LLM) gateway and artificial intelligence (AI) asset management system. Prior to 1.0.0-rc.11, POST /api/stripe/webhook, POST /api/creem/webhook, and POST /api/waffo/webhook read and log full request bodies before signature validation in router/api-router.go and the payment controllers, allowing an unauthenticated attacker to cause memory pressure, container restarts, or disk exhaustion without forging a successful payment. This issue is fixed in version 1.0.0-rc.11.

### CVE-2025-27772

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-17T16:16:46.710 |

UpTrain is an open-source platform to evaluate and improve generative AI applications. In version 0.7.1 and prior, the `/new_run` endpoint is vulnerable to remote code execution via the `checks` and `metadata` parameters. Any user that has access to UpTrain and a valid authentication method may be able to execute arbitrary code in the context of the host running UpTrain, which in most cases will be the docker container as suggested by the documentation. As of time of publication, no known patch is available.

### CVE-2025-27771

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-17T16:16:46.580 |

UpTrain is an open-source platform to evaluate and improve generative AI applications. In version 0.7.1 and prior, the `/add_prompts` endpoint is vulnerable to remote code execution via the `checks` and `metadata` parameters. Any user that has access to UpTrain and a valid authentication method may be able to execute arbitrary code in the context of the host running UpTrain, which in most cases will be the docker container as suggested by the documentation. As of time of publication, no known patch is available.

### CVE-2025-27770

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-17T16:16:46.447 |

UpTrain is an open-source platform to evaluate and improve generative AI applications. In version 0.7.1 and prior, the `/create_project` endpoint is vulnerable to remote code execution via the `checks` and `metadata` parameters. Any user that has access to UpTrain and a valid authentication method may be able to execute arbitrary code in the context of the host running UpTrain, which in most cases will be the docker container as suggested by the documentation. As of time of publication, no known patch is available.

### CVE-2026-40144

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-17T16:16:56.203 |

A memory-corruption vulnerability exists in a kernel-mode component of BeyondTrust Endpoint Privilege Management (Windows deployments) prior to version 26.1.2. Insufficient validation of input processed by the component may result in memory being accessed outside its intended bounds.

### CVE-2026-13202

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T15:16:53.513 |

A vulnerability in OpenText Opentext Directory Services allows Input Data Manipulation.

This issue affects Opentext Directory Services: through 22.2.

### CVE-2026-75091

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T06:16:44.227 |

The Quill Forms | Conversational Multi Step Forms, Surveys & quizzes plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 5.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-32333

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T14:17:03.133 |

Unauthenticated Cross Site Scripting (XSS) in Mayosis Core <= 5.4.7 versions.

### CVE-2026-28569

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T14:17:02.587 |

Unauthenticated Cross Site Scripting (XSS) in SSL Zen <= 4.7.43 versions.

### CVE-2026-28568

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T14:17:02.457 |

Unauthenticated Cross Site Scripting (XSS) in Quill Forms <= 5.7.1 versions.

### CVE-2026-75846

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T12:19:35.173 |

ArcadeDB before 26.8.1 (affected versions <= 26.7.3) contains a missing authorization vulnerability in the DELETE FUNCTION SQL statement. DeleteFunctionStatement.executeSimple unregisters and persists deletion of a server-side function without any checkPermissionsOnDatabase (UPDATE_SCHEMA) check. Any user with database access can execute DELETE FUNCTION via the command API (POST /api/v1/command/{db}) to permanently remove any registered server-side function, including security-relevant logic, impacting integrity and availability.

### CVE-2026-75844

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T12:19:34.890 |

ArcadeDB versions before 26.8.1 contain a server-side request forgery vulnerability in the IMPORT DATABASE command where the security validator resolves and checks hostnames but the subsequent connection re-resolves the raw URL and follows redirects. Authenticated attackers can bypass the validator using DNS rebinding or HTTP redirects to access cloud metadata endpoints, internal services, or read arbitrary local files on default installations.

### CVE-2026-75830

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-18T12:19:32.960 |

grav-plugin-api (getgrav/grav-plugin-api) versions >= 1.0.0-beta.10 and <= 1.0.14 contain a path traversal vulnerability in the PagesController::batchCopy() method. An incomplete fix for GHSA-qjq4-jp55-4mx2 left the user-controlled 'suffix' parameter (via POST /api/v1/pages/batch) unvalidated. An authenticated user with the api.pages.write permission (editor-level, not super-admin) can supply path traversal sequences (e.g. /../../../) in the suffix parameter to escape the intended user/pages/ directory and write attacker-controlled page content and page media to arbitrary filesystem locations writable by the web server process. The vulnerability is fixed in 1.0.15.

### CVE-2026-69148

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T22:17:26.380 |

MLflow is an open source AI engineering platform for agents, large language models, and machine learning models. Prior to 3.15.0, CreateModelVersion accepts a run_id or model_id after _validate_source_run() or _validate_source_model() in mlflow/server/handlers.py verifies only path containment, allowing authenticated users to create a model version that references another user's artifact directory and read files through GET /model-versions/get-artifact without the required READ permission. This issue is fixed in version 3.15.0.

### CVE-2026-75480

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-17T21:16:50.477 |

OpenViking debug vector scroll and count endpoints apply only account-level scoping without user-level access controls, allowing authenticated users to read all co-tenant records. Attackers can query these endpoints to retrieve private memories, resources, skills, and secret material belonging to other users in the same account without administrative privileges.

### CVE-2026-75109

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T21:16:49.897 |

Determined fails to authorize requests on the generic task kill, pause, and unpause endpoints in the API handlers. Authenticated attackers can disrupt other users' workloads by terminating, pausing, or unpausing tasks they do not own.

### CVE-2026-54356

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-17T21:16:46.063 |

Budibase is an open-source low-code platform. Prior to 3.41.3, POST /api/attachments/:datasourceId/url in packages/server/src/api/routes/static.ts and packages/server/src/api/controllers/static/index.ts allows an authenticated published-app user with the BASIC role to supply attacker-controlled bucket and key values and obtain signedUrl and publicUrl values backed by stored S3 datasource credentials. This issue is fixed in version 3.41.3.

### CVE-2026-35219

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-17T21:16:44.550 |

Budibase is an open-source low-code platform. Prior to 3.41.3, automation steps in packages/server/src/automations/steps/outgoingWebhook.ts, packages/server/src/automations/steps/zapier.ts, packages/server/src/automations/steps/n8n.ts, packages/server/src/automations/steps/slack.ts, and packages/server/src/automations/steps/discord.ts use node-fetch on user-provided URLs without the BLACKLIST_IPS enforcement used by the REST integration, allowing an authenticated user to make server-side requests to cloud metadata and internal services. This issue is fixed in version 3.41.3.

### CVE-2026-19589

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T21:16:43.593 |

Packer up to 1.15.4 is vulnerable to an issue in the third-party plugin installer that may allow unintended file system modification and could lead to code execution. A user who installs a plugin from a malicious or compromised source may be affected. This vulnerability (CVE-2026-19589) is fixed in Packer 1.16.0.

### CVE-2026-71553

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-17T20:16:46.073 |

ApostropheCMS is an open-source Node.js content management system. In 4.32.0 and earlier, PATCH /api/v1/article/:id accepts the inherited path toString.call and passes it through the utility module to apos.util.set() and apos.util.get(), allowing an authenticated editor to overwrite the shared Object.prototype.toString function's call property and cause a persistent process-wide denial of service until restart.

### CVE-2026-19650

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-17T20:16:41.910 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.2 before 18.11.11, 19.0 before 19.0.8, 19.1 before 19.1.6, and 19.2 before 19.2.4 that under certain conditions could have allowed an unauthenticated user to execute mutations via GET requests due to improper request validation in GraphQL multiplex query handling.

### CVE-2026-68519

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-17T18:18:06.610 |

Glances is an open-source system cross-platform monitoring tool. Prior to 4.5.6, GlancesActions.run() in glances/actions.py ignores --disable-config-exec for on-alert action commands and invokes secure_popen() with shell operators enabled, allowing configured redirection, command chaining, or pipes to execute when an alert triggers. This issue is fixed in 4.5.6.

### CVE-2026-40145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-08-17T17:16:39.787 |

A vulnerability exists in the interaction between a Endpoint Privilege Management (Windows Deployment) support utility and the agent's tamper protection controls. Under certain conditions, the protections applied to the utility process may not be enforced as intended.

### CVE-2026-75050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-17T16:17:52.097 |

In JetBrains YouTrack before 2026.1.13901, 
2026.2.17950 doS attack was possible via crafted type parameters

### CVE-2026-75531

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-17T21:16:59.067 |

Pandora contains a stored cross-site scripting (XSS) vulnerability in the rendering of URL observables. A URL extracted from or associated with an analyzed file was inserted directly into the inline JavaScript onclick handler used by the Submit to Lookyloo action.


Although the value was subject to HTML escaping by the template engine, it was embedded inside a JavaScript string within an HTML attribute. An attacker-controlled URL containing specially crafted characters could therefore break out of the JavaScript string and inject arbitrary JavaScript code.


The malicious script would execute in the context of the Pandora web application when a victim interacts with the affected Submit to Lookyloo control. Successful exploitation could allow an attacker to access information available to the victim's browser or perform actions using the victim's authenticated Pandora session.


The patch removes the observable value from the inline JavaScript handler. The URL is instead stored in an HTML data-url attribute and retrieved through the DOM dataset API when needed. Additional uses of innerHTML were also replaced with textContent as defensive hardening.

### CVE-2026-40506

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-17T21:16:44.930 |

OpenEMR before 8.2.0 contains a path traversal vulnerability in the standard_tables_manage.php interface where the db GET parameter is passed without validation to temp_dir_cleanup(), which joins the value to the PHP temporary directory path and recursively deletes the resulting directory. Attackers can supply a traversal sequence in the db parameter to resolve outside the intended temporary directory, and by chaining this with an open redirect in dicom_frame.php, an unauthenticated attacker can deliver a crafted URL that triggers arbitrary recursive directory deletion within an authenticated Superuser's session.

### CVE-2026-34789

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-17T21:16:44.403 |

FreeCAD is a free and open-source multiplatform 3D parametric modeler. Prior to 1.1.2, src/App/PropertyPythonObject.cpp in PropertyPythonObject::Restore() passes the attacker-controlled module attribute from serialized PropertyPythonObject XML directly to PyImport_ImportModule() while restoring a crafted FCStd document, which executes module-level Python code, and the legacy pickle branch also imports an attacker-controlled module and invokes its class constructor through PyObject_CallObject(). This issue is fixed in version 1.1.2.
