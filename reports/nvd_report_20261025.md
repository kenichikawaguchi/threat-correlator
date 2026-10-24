# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-24 15:01 UTC
- **対象期間**: `2026-10-23T15:00:34.000Z` 〜 `2026-10-24T15:01:30.000Z`
- **重要CVE数**: 72 件（Critical 9.0+: 15 件 / High 7.0〜: 57 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超と非常に多く、特に **Web アプリケーション・プラグイン** と **ランタイム/ビルドツール** に集中しています。  
- 最高評価は **9.9**（Critical）で、機密情報漏洩・完全なリモートコード実行が可能になるケースが目立ちます。  
- 多くは **不適切な入力検証**（関数呼び出し制御、パス・トラバーサル、シリアライズ）や **コンパイラ／ランタイムの実装バグ** が根本原因で、パッチ適用だけでなく **防御的コーディング** が求められます。  

---

## 2. 特に注目すべき CVE  

| CVE ID | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨される対策（概要） |
|--------|------|----------------|------------------------|------------------------|
| **CVE‑2026‑115931** | 9.9 | 任意関数呼び出し（Server‑Side Request Forgery 風） | Postiz のバックエンドが「関数名」パラメータを制限せず、認証ユーザーが内部ヘルパー関数を呼び出せる。機密データ取得や任意コード実行が可能。 | 関数ホワイトリスト実装、アクセス制御強化、ログ監視。 |
| **CVE‑2026‑115893** | 9.9 | Cranelift コンパイラのブランチターゲットオーバーフロー（aarch64） | Wasmtime 3 系 (≤36.0.18, 48.0.6, 49.0.3) が 256 k 超の `br_table` を正しく処理できず、任意アドレスへジャンプできる。クラウド・サーバー上で WebAssembly を実行する全ユーザーに影響。 | Wasmtime を **36.0.19 以上**、**48.0.7 以上**、**49.0.4 以上** に更新。 |
| **CVE‑2026‑115889** | 9.9 | SSA インデックスのビットパックオーバーフロー（リリースビルド） | Wasmtime の Cranelift が大規模・特殊な Wasm 関数で SSA インデックスがオーバーフローし、メモリ破壊・コード実行につながる。 | Wasmtime を **36.0.19 以上**、**43.0.0 以上** に更新。 |
| **CVE‑2026‑53942** | 9.9 | GitHub Actions ワークフローの「Pwn Request」脆弱性 | conda/conda の `update.yml` が issue_comment イベントを無制限に受け付け、攻撃者が任意のシークレットやコードを実行できる。Conda の組織インフラ全体に波及。 | コミット **9c0f238** 以降の最新版に更新し、`workflow_dispatch` でのトリガー制限と `GITHUB_TOKEN` の最小権限化を実施。 |
| **CVE‑2026‑94075** | 9.8 | オブジェクトインジェクション（PHP 逆シリアライズ） | WordPress 用プラグイン **Newsletters** (≤4.18.1) がシリアライズデータを検証せずに復元し、任意 PHP オブジェクトを注入できる。管理者権限取得やサイト改ざんが可能。 | プラグインを **4.18.2 以上** に更新、または不要なら削除。 |

> **注**：上記は **CVSS 9.8 以上** のものを中心に選出。その他にも 9.6‑9.8 の WordPress プラグイン（Prime Mover、Paytium など）や Goobi Viewer のディレクトリトラバーサル等が多数報告されていますが、上記 5 件が最も広範囲・深刻な影響を持つと判断しました。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品 / ライブラリ | 現行 (脆弱) バージョン | 修正版 (推奨) |
|-------------------|------------------------|----------------|
| **Postiz** (バックエンド) | 任意（関数制御未実装） | ソースコードで **関数ホワイトリスト** を実装し、`v2.3.0` 以降（リリースがあれば）を適用 |
| **Wasmtime** | 36.0.18 / 48.0.6 / 49.0.3 など | **≥ 36.0.19**、**≥ 48.0.7**、**≥ 49.0.4**（全プラットフォーム） |
| **Wasmtime (SSA overflow)** | ≤ 36.0.18、≤ 43.0.0 | **≥ 36.0.19**、**≥ 43.0.0** |
| **Conda (GitHub Actions)** | コミット 9c0f238 未適用 | **最新コミット**（2026‑10‑xx 以降）へマージ |
| **Newsletters (WordPress)** | ≤ 4.18.1 | **4.18.2** 以上 |
| **Prime Mover – Backup & Migration** | ≤ 2.2.1 | **2.2.2** 以上 |
| **Paytium** | ≤ 5.0.5 | **5.0.6** 以上 |
| **Goobi Viewer** | 24.03‑26.04 | **≥ 26.05** |
| **HP One Agent** | 8.5 以前 | HP が提供する **2026‑10‑xx** のパッチを適用 |

### 3.2 防御的設定・運用上のベストプラクティス
1. **最小権限の原則**  
   - Web アプリや CI/CD ワークフローで使用するトークン・シークレットは **Read‑only** に限定し、不要な `write` 権限は削除。  
2. **入力検証の徹底**  
   - すべての外部入力（REST API、ファイル名、パス、シリアライズ文字列）に対し **ホワイトリスト** または **正規表現** で検証し、相対パス (`../`) や不正な文字列は除外。  
3. **コードレビューと静的解析**  
   - 新規機能追加時に **関数呼び出し制御**、**シリアライズ/デシリアライズ**、**コンパイル時の境界チェック** が正しく実装されているか確認。  
4. **ランタイム監視とアラート**  
   - 高リスク関数呼び出し

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-115931

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-470` |
| Published | 2026-10-23T23:17:43.263 |

Postiz lets a signed-in user ask the backend to run a function on one of their connected channels. The backend did not restrict which functions can be requested, so a user could call internal helper functions that were never meant to be reachable from the web interface.

One of those helpers reads a file from the server's disk. A user who connects a channel whose stored token is a file path can have the backend return the contents of any file it can read, including its environment, which holds the secret used to sign login sessions, the database address and the credentials of connected services. Another helper makes the backend process exit with a single request. Self-registration is open by default, so no existing account and no action by another user is needed.

### CVE-2026-115893

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-691` |
| Published | 2026-10-23T22:16:58.820 |

Wasmtime is a runtime for WebAssembly. Prior to 36.0.19, 48.0.7, and 49.0.4, the Cranelift compiler backend on aarch64 can compile a Wasm br_table instruction with more than approximately 256,000 targets so that it has an incorrect conditional branch target. The branch can then jump to arbitrary other code at a user-controlled offset, allowing a user-controlled Wasm module to escape the sandbox on aarch64 engines using the default Cranelift backend. This issue is fixed in versions 36.0.19, 48.0.7, and 49.0.4.

### CVE-2026-115889

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-197;CWE-843` |
| Published | 2026-10-23T22:16:58.400 |

Wasmtime is a runtime for WebAssembly. Prior to 36.0.19 and 43.0.0, the Cranelift compiler backend bit-packs SSA value indices in a way that can silently overflow in release builds when compiling a sufficiently large or specially crafted Wasm function with many SSA values. The overflow can make Cranelift reference incorrect IR values, causing arbitrary miscompilation, type confusion, and other attacker-controlled effects that may escape the Wasm sandbox on any architecture using the default Cranelift backend. This issue is fixed in versions 36.0.19 and 43.0.0.

### CVE-2026-53942

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T15:17:32.157 |

Conda Organization Infrastructure is a centralized location for infrastructure codes. Prior to commit 9c0f238, a GitHub Actions Pwn Request vulnerability appears to remain present in conda/conda. The affected workflow is .github/workflows/update.yml. It is triggered by issue_comment events containing @conda-bot render or @conda-bot recreate. For the render path, the workflow obtains the pull request head repository and branch from the PR API, checks out that PR-controlled repository/ref using secrets.SYNC_TOKEN, and then runs conda/actions/template-files@7f6830b1428a9bd47f0b068892c77eae95207037. The external template-files action reads its default configuration and templates from the checked-out working directory. In the confirmed finding, that action uses an unsandboxed Jinja2 environment to render attacker-controlled template content. This creates a Pwn Request chain in which an untrusted PR/comment path can reach template rendering in a privileged token context. This issue has been patched via commit 9c0f238.

### CVE-2026-94075

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-24T08:16:52.790 |

Deserialization of Untrusted Data vulnerability in Tribulant Software Newsletters newsletters-lite allows Object Injection.This issue affects Newsletters: from n/a through 4.18.1.

### CVE-2026-114196

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-24T08:16:51.963 |

Deserialization of Untrusted Data vulnerability in paytiumsupport Paytium paytium allows Object Injection.This issue affects Paytium: from n/a through 5.0.5.

### CVE-2026-115806

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-24T05:17:04.900 |

The Prime Mover – Backup and Migration plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 2.2.1 via deserialization of untrusted input in the migration search-and-replace routine (recursiveUnserializeReplace()). An unauthenticated attacker can store a crafted, base64-encoded serialized object in wp_comments.comment_content through the standard comment-submission endpoint (wp-comments-post.php). When an administrator subsequently performs a routine Prime Mover export or restore, the plugin base64-decodes that stored value and passes it to unserialize() with no allowed_classes restriction. A Property-Oriented Programming (POP) chain is present in the plugin's own bundled Freemius library (FS_Clone_Manager::__set → FS_Option_Manager::set_option → store() → update_option()), so no additional plugin or theme is required — the plugin ships the gadget itself.

### CVE-2026-46652

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-23T15:17:31.593 |

The Goobi viewer is a web application that allows digitised material to be displayed in a web browser. From version 24.03 to before version 26.05, ExternalFilesDownloader.getFilename() extracts the destination filename from a server-supplied Content-Disposition response header and passes it directly to Path.resolve() without stripping directory components. This allows for a malicious HTTP server that the viewer fetches from to supply an absolute path or ../ traversal sequences as the filename, writing attacker-controlled content to an arbitrary path writable by the Tomcat process. When targeting the deployed web-application directory, this yields remote code execution as the tomcat OS user. This issue has been patched in version 26.05.

### CVE-2026-46651

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-552;CWE-918` |
| Published | 2026-10-23T15:17:31.453 |

The Goobi viewer is a web application that allows digitised material to be displayed in a web browser. From version 24.03 to before version 26.05, the DownloadTaskEndpoint WebSocket endpoint (/tasks/download/monitor.socket) in goobi-viewer-core accepts download requests from unauthenticated users. This issue has been patched in version 26.05.

### CVE-2026-115932

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-74` |
| Published | 2026-10-24T13:16:37.217 |

When a post is published, Postiz treats a media path that is not a web address as a file on the server's disk, but it does not check that the file lies inside the upload directory. A registered user can store a crafted media path with a post, get it past the checks that normally restrict it, and have the publishing worker read an arbitrary file and send it as an attachment to a Discord server the user controls.

The same unconfined reads can be reached through two further routes. One tells the caller whether a file exists and can exhaust the backend's memory, the other delivers the file the same way as the main route. Self-registration is open by default, so the attacker needs no existing account.

### CVE-2026-112866

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-24T08:16:51.303 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WPFactory Product Filter by WBW woo-product-filter allows Blind SQL Injection.This issue affects Product Filter by WBW: from n/a through 3.4.6.

### CVE-2026-111402

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-24T08:16:50.877 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Tribulant Software Newsletters newsletters-lite allows SQL Injection.This issue affects Newsletters: from n/a through 4.18.1.

### CVE-2026-115812

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-23T18:17:21.460 |

Relative path traversal during model archive extraction in Amazon Web Services Multi Model Server 1.1.11 and earlier might allow remote actors to execute arbitrary code via a crafted model archive.



Multi Model Server is end of life and no fixed version is available. Users should discontinue use of Multi Model Server and migrate to a supported model serving solution.

### CVE-2026-55486

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-113;CWE-1336` |
| Published | 2026-10-23T15:17:33.657 |

The Goobi viewer is a web application that allows digitised material to be displayed in a web browser. From version 25.08 to before version 26.05, the IIIF Auth 2.0 endpoints auth/login and auth/token in AuthorizationFlowResource accept an origin query parameter without validation and then (1) embed it into the Content-Security-Policy: frame-ancestors response header and (2) embed it into an HTML response body as a JavaScript single-quoted postMessage argument. Because the attacker controls both the login and token calls that initiate the flow, the unescaped value yields reflected XSS. This issue has been patched in version 26.05.

### CVE-2026-116014

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-24T12:16:57.607 |

open62541 1.5.0 before 1.5.7 contains an integer overflow in UA_DataType_fromStructureDescription() that wraps the 16-bit memSize field for large custom structure definitions. A malicious OPC UA server can supply DataType definitions via UA_Client_getRemoteDataTypes(), causing decodeBinaryStructure() to overflow the heap, crashing clients or enabling code execution.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-110018

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-24T12:16:54.783 |

The aBlocks – Gutenberg Blocks, User Dashboard Builder, Popup Builder, Form Builder & Animation Builder plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.17.0 via the `/ablocks/v1/form-builder/registration` REST endpoint. The vulnerability exists because the endpoint is registered with `permission_callback => __return_true` and the `register()` handler reads `roleSlug` directly from attacker-controlled block attributes in `post_content` without ever verifying that the block's `formType` is `registration` — a condition that `RegistrationFormSanitizer::verify()` imposes only at save-time, meaning a Contributor can preserve an arbitrary `roleSlug` by saving a block with `formType='login'` and then triggering the endpoint via a valid `wp_rest` nonce and post-ownership check. This makes it possible for authenticated attackers, with Contributor-level access and above, to escalate their WordPress role to Editor or any other non-administrator role and receive a fully authenticated session at the elevated privilege level via `WP_User::set_role()` and `wp_set_auth_cookie()`. Escalation is bounded below administrator-tier roles because `is_safe_registration_role()` rejects any role holding `manage_options`, `edit_users`, `delete_users`, `create_users`, `promote_users`, or `edit_theme_options`, meaning the highest practically reachable role on a standard WordPress installation is Editor.

### CVE-2026-115895

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T22:16:58.987 |

Happy DOM is a JavaScript implementation of a web browser without its graphical user interface. From 17.0.0 until 21.0.4, packages/happy-dom/src/module/ECMAScriptModuleCompiler.ts accepts a named ESM import alias without validating that it is a JavaScript binding identifier before inserting it into a generated destructuring binding. With enableJavaScriptEvaluation enabled, attacker-controlled HTML or module source can use an invalid alias that becomes a valid default initializer after compilation, causing the generated JavaScript to execute in the Node.js host process. The demonstrated reachable path uses a JSON module import attribute, which prevents the malicious alias from being emitted again in a later ESM circular-import assignment and keeps the generated function syntactically valid. This incomplete fix for CVE-2026-33943 is a distinct residual path because the earlier remediation validated the local export importName path but not the named-import alias. This issue is fixed in version 21.0.4.

### CVE-2026-79982

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-23T20:17:28.167 |

The Bluetooth HCI USB transport class of the new USB device stack, subsys/usb/device_next/class/bt_hci.c, copies every controller-to-host HCI packet into a USB transfer buffer before enqueuing it on an endpoint. bt_hci_tx_sync_in() allocated that buffer from bt_hci_ep_pool, a fixed pool whose slots are only USBD_MAX_BULK_MPS bytes (64 on full-speed-only builds), and then performed net_buf_add_mem(buf, bt_buf->data, bt_buf->len) with no length check. HCI event and ACL buffers are sized by CONFIG_BT_BUF_EVT_RX_SIZE and CONFIG_BT_BUF_ACL_RX_SIZE and can be far larger, so the copy runs past the end of the 64-byte slot into the adjacent slots and into whatever follows the statically allocated pool.

The device runs the local Bluetooth controller in raw HCI mode (CONFIG_BT_HCI_RAW), so the oversized packets originate over the air. With the HCI buffer sizes recommended for full-featured controllers, an unauthenticated attacker within Bluetooth range can supply the overflowing bytes: a connected peer that negotiates Data Length Extension can send ACL fragments up to CONFIG_BT_CTLR_DATA_LENGTH_MAX bytes, and an attacker that merely broadcasts extended advertising data reaches the same path through LE Extended Advertising Report events, which the controller fragments only to CONFIG_BT_BUF_EVT_RX_SIZE. In the stock configuration the overflow is already reached without any radio traffic: the mandatory Read Supported Commands command-complete event is 70 bytes and overruns the 64-byte slot by six bytes on every host initialization.

Because net_buf_add_mem() validates tailroom only through an assertion unless CONFIG_NET_BUF_HARDENING is enabled, builds with CONFIG_ASSERT=n — the usual production setting — silently corrupt memory adjacent to the USB buffer pool with attacker-chosen contents, which on a target without memory protection between subsystems can lead to arbitrary code execution. Builds with assertions enabled fail the assertion instead and panic, giving a remotely triggerable denial of service. The fix introduces a separate bt_hci_tx_pool sized to MAX(BT_BUF_ACL_RX_SIZE, BT_BUF_EVT_RX_SIZE) for the controller-to-host direction while leaving the host-to-device pool at the endpoint packet size, which is already bounds-checked during reassembly.

### CVE-2026-116019

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-24T12:16:58.473 |

Grav 2.0.15 before 2.2.13 contains an allowlist bypass vulnerability that allows page editors to invoke arbitrary public static methods by relocating data-*@ directives with unset-name@ or integer keys. Attackers with page-edit permission can embed crafted fields in Flex form overrides in page frontmatter to call methods like Folder::delete or Utils::download, deleting directories, overwriting files, or reading files outside the page tree.

### CVE-2026-116011

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-24T12:16:57.070 |

Crow before 1.3.4 contains an uncontrolled recursion vulnerability in crow::json::load() that allows remote unauthenticated attackers to crash the server by sending deeply nested JSON. Attackers can send a request body with thousands of nested objects to exhaust the worker thread stack, terminating the process and dropping all connections.

### CVE-2026-116009

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-24T12:16:56.640 |

Camaleon CMS before 2.9.3 contains a path traversal vulnerability that allows users with only the media permission to write arbitrary files by supplying ../ sequences in the name parameter. Attackers can send a base64 data: URI to the crop_url media action to write an ERB template into a theme's views directory, which executes when rendered.

### CVE-2026-115938

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-23T22:16:59.597 |

Craft CMS allows any authenticated control panel user to submit an element-search condition whose element selector is evaluated as a sandboxed Twig object template. Craft’s allowed column filter delegates property lookup to Yii ArrayHelper, outside Twig’s SecurityPolicy. Repeated single-segment lookups therefore bypass the sandbox’s empty property/method allowlists.



The vulnerable condition value is ultimately cast to an integer. That does not protect the secret: the template can return author ID 1 when a guessed key character is correct and an impossible ID otherwise. The JSON endpoint returns entries for the first case and an empty array for the second, forming a stable remote character oracle.



After recovering GeneralConfig::securityKey, the same user can compute Craft’s generic HMAC wire format offline. Signed parameters such as redirect are then accepted and passed to unsandboxed View::renderObjectTemplate(), where Twig’s string-callable form can invoke native PHP callables. The regression proof uses the harmless substr() callback and observes abcdef becoming cdef; it does not execute an OS command.

### CVE-2026-115937

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-23T22:16:59.453 |

The Mollie webhook endpoint accepts two independent, attacker-controlled parameters and never verifies that they belong together:

  *  commerceTransactionHash — selects which Craft Commerce transaction is completed
  *  id — selects which Mollie payment is queried for its status




An unauthenticated attacker holding any paid Mollie payment ID from the merchant’s account can pair it with any transaction hash.



Commerce queries Mollie, sees status: paid, and marks the target transaction successful for that transaction’s full
amount, regardless of how much was actually paid.

### CVE-2026-115935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-23T22:16:59.290 |

The app/process-api-response-headers action accepts fake Craft API response headers from any authenticated control panel user.



A non-admin user with only accessCp can place newline characters in X-Craft-Plugin-Licenses. Craft passes this value to its .env writer without removing the newlines.



This lets the user insert a new attacker-known CRAFT_SECURITY_KEY into .env. After Craft loads that key, the user can forge a signed login redirect containing a Twig system() callback.



This is different from the previous report. That report reads the existing key through a Twig sandbox bypass. This report replaces the key through fake API headers and CRLF injection. Fixing either source does not fix the other.

### CVE-2026-115775

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-23T21:17:23.050 |

Twisted is an event-based framework for internet applications, supporting Python 3.6+. Prior to 26.10.0rc1, the twisted.words.xish.domish ExpatElementStream parser allows an unauthenticated remote peer to keep a container element open while continuously adding child elements. The parser retains the unfinished stanza as an in-memory tree without a byte or element-count limit, and XMPP pre-authentication stream parsing exposes this behavior before credentials are accepted. A single connection can therefore exhaust server memory and terminate the process. This issue is fixed in version 26.10.0rc1.

### CVE-2026-57845

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-23T16:16:52.000 |

Hugging Face Datasets through 5.1.0 contains an insecure deserialization vulnerability that allows attackers to execute arbitrary Python code by crafting a malicious pickle file loaded through the deprecated pandas packaged builder. Attackers can supply a pickle-backed dataset that is processed by Pandas._generate_tables via pandas.read_pickle() without validation, so when a victim calls datasets.load_dataset("pandas", data_files=...), the embedded __reduce__ payload executes code with the victim process's privileges.

### CVE-2026-54668

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-23T15:17:32.427 |

Kitodo.Production is a workflow management tool for mass digitization and is part of the Kitodo Digital Library Suite. Prior to version 3.9.2, org.kitodo.production.helper.XMLUtils exposes several XML parsing helpers that construct a JAXP parser with the default, non-secure configuration. The methods parseXMLString(String), getNumberOfEADElements(String, String) and checkIfXmlIsWellFormed(String) build a DocumentBuilderFactory / XMLInputFactory / SAXParserFactory via newInstance() and parse the attacker-supplied string without disabling DOCTYPE declarations or external entity resolution. These helpers sit directly on the EAD-import path: an authenticated user who uploads an EAD/XML file through the "Create process" file-upload dialog has the uploaded bytes parsed by these methods. A crafted document with an external entity therefore yields XML External Entity (XXE) injection: local file disclosure and outbound SSRF requests from the server. This issue has been patched in version 3.9.2.

### CVE-2026-58497

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346;CWE-352` |
| Published | 2026-10-23T15:17:34.257 |

Uni-CLI gives people and agents one command interface for websites, browsers, desktop applications, local tools, and MCP. Prior to version 0.225.2, Uni-CLI exposed the legacy JSON-RPC-over-HTTP MCP transport on loopback without validating browser Origin headers before routing requests. A malicious web page could send a CORS simple POST request, such as text/plain, to the local /mcp endpoint and deliver a JSON-RPC body to the dispatcher. If the user had started the local MCP HTTP transport, that page could drive tools/call requests against the user's local Uni-CLI server. The Streamable HTTP transport already enforced this browser-to-localhost boundary. The legacy stateless HTTP path did not, so the two HTTP transports had drifted. This issue is about the browser-to-localhost boundary; it does not change Uni-CLI's local-code-execution trust model. This issue has been patched in version 0.225.2.

### CVE-2026-102786

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T15:17:22.807 |

Joomla Extension - phoca.cz - Authenticated stored cross-site scripting through HTML attribute injection in Phoca Gallery 4.5.0 - 6.1.5

### CVE-2026-91093

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-23T19:17:45.287 |

A potential security vulnerability has been identified in HP One Agent for certain HP PC products, which might allow for escalation
               of privilege and/or arbitrary code execution. HP is releasing software updates to mitigate the potential vulnerability.

### CVE-2026-58202

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-23T21:17:24.473 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 2.0.0, the account-confirmation link in emails is built from the request Host header, with no allowlist. The unauthenticated POST /api/auth/resend-confirmation rotates a pending invitee's confirmation token and emails a link whose host comes from the request. An attacker who sends one resend-confirmation with Host: attacker.example and a pending invitee's email causes that invitee to receive a confirmation email whose only link points to the attacker. If the invitee clicks, the one-time confirmation token reaches the attacker, who then confirms the account on the real tenant domain and registers a passkey they control, taking over the account before the legitimate invitee ever uses it. All released versions through v1.1.0 are affected; no patched version exists yet. Reaching the app with a spoofed Host depends on the front proxy: the stock Caddy catch-all forwards it, while an operator who configures explicit per-tenant proxy blocks is not affected (see Details 4). The invite path builds links from the trusted tenant.domain (invite/+server.ts:204-210); the resend-confirmation path builds them from the request Host. This issue has been patched in version 2.0.0.

### CVE-2026-87901

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-23T17:17:22.137 |

Improper sanitization in the registration module allows reflected Cross-Site Scripting.

### CVE-2026-79977

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-306;CWE-346` |
| Published | 2026-10-23T20:17:27.523 |

The WireGuard VPN service in subsys/net/lib/wireguard/wg.c updated the peer endpoint from a message it could not authenticate. In handle_transport_data(), when the 32-bit receiver index of an incoming transport-data message matched no session, the code both scheduled a new handshake and copied the datagram's source address into peer->endpoint with memcpy(&peer->endpoint, peer_addr, sizeof(peer->endpoint)). Because the receiver index is unknown, there is no key with which such a message could be verified, so the address written into peer->endpoint is entirely attacker-supplied. Every other endpoint update in the implementation happens only after authentication — after the Noise handshake in handle_handshake_init(), or after AEAD decryption plus the anti-replay check in wg_process_data_message().

The WireGuard listener is registered with net_udp_register() using no remote address or port filter and defaults to UDP port 51820 (CONFIG_WIREGUARD_PORT), and wg_ctrl_recv() resolves the peer by interface rather than by any cryptographic identity. Any host able to send a UDP datagram to that port can therefore reach the defect off-path, with no need to observe legitimate traffic: a 16-byte datagram carrying the transport-data type, zeroed reserved bytes and an arbitrary receiver index is sufficient. The vulnerable branch runs whenever the peer has neither a valid handshake nor a current keypair — the state at boot and after a session expires.

A single spoofed datagram redirects peer->endpoint to an address of the attacker's choosing, and all subsequent handshake initiations, keepalives and encrypted data packets are sent there. The legitimate peer never receives the initiations and so never re-authenticates, and nothing resets the endpoint afterwards, leaving the tunnel persistently unusable on devices whose peer does not initiate handshakes itself. The attacker can also relay the redirected initiations to the real peer to place itself in the path of the tunnel, observing ciphertext and traffic metadata and selectively dropping packets. WireGuard's end-to-end cryptography still prevents decryption or forgery of tunnel content, so the impact is loss of availability plus limited confidentiality, not key compromise.

The fix removes the endpoint learning from this path entirely: the stale-session recovery is kept, but the handshake is sent only to an endpoint learnt from an authenticated message, falling back to the configured cfg_endpoint, and the message is dropped when neither is known. CONFIG_WIREGUARD is marked experimental and is not enabled by default.

### CVE-2026-79979

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-23T20:17:27.783 |

The arm64 MMU backend invalidates a single virtual address from the TLB with invalidate_tlb_page() in arch/arm64/core/mmu.c, which issued TLBI VAE1{IS} with an operand of virt >> 12. That operand encodes the ASID in bits [63:48], so the invalidation only ever matched ASID 0 (the kernel page tables) and global entries. Memory domains, however, are allocated ASIDs starting at 1 in arch_mem_domain_init(), and every domain-private leaf created by private_map() is mapped with MT_NG, i.e. non-global. A domain's cached translation therefore survived the invalidation.

All callers of invalidate_tlb_page() are demand-paging paths. When the eviction algorithm reclaims a frame, page_frame_prepare_locked() in kernel/mmu.c calls arch_mem_page_out(), which marks the kernel leaf invalid, propagates the invalid descriptor into every domain via sync_domains(), and then flushes only ASID 0. do_page_fault() immediately reuses the very same page frame for the incoming mapping through arch_mem_page_in(). A user thread that had already touched the evicted page — a k_mem_partition added with arch_mem_domain_partition_add(), or its own stack mapped by map_thread_stack() — retains a valid EL0 read/write translation to that physical frame under its own ASID.

Unprivileged code running in a user thread can drive memory pressure to force eviction and then keep accessing the stale address, obtaining read and write access to whatever the kernel subsequently placed in that frame: supervisor data, another memory domain's partition, or another thread's stack. This defeats the isolation that CONFIG_USERSPACE is meant to enforce, allowing information disclosure and memory corruption up to full compromise of the system.

The fix switches the implementation to TLBI VAAE1{IS}, which matches every ASID and both global and non-global entries, so no domain-tagged translation survives a page out, dirty-bit update or access-flag clear. Exploitation requires an arm64 build with both CONFIG_USERSPACE and CONFIG_DEMAND_PAGING enabled, an active backing store, and at least one demand-paged page that is also privately mapped into a user memory domain. The same commit additionally stops globalize_table() from stripping EL0 permission and non-global attributes off domain-private leaves during paging synchronization, which previously caused user threads to lose access to their own partitions and stacks.

### CVE-2026-115929

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-24T01:17:08.250 |

MongoDB Compass relies on Electron, a third-party runtime that carries its own TLS root certificate store. This root certificate store has the recoverable eMudhra intermediate CA certificates. Issue is resolved by updating to Compass 1.53.1, which includes Electron 44.9.1.

### CVE-2026-115863

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-23T18:17:21.757 |

ConnMan through 2.0 has a stack-based buffer overflow via a DHCPv6 Reply message. This occurs in get_domains in gdhcp/client.c. It copies a fixed NS_MAXDNAME (1025) bytes from a DHCPv6 DOMAIN_LIST (option 24) value into a 1026-byte stack buffer dns_name regardless of the actual option length, then walks DNS labels with an unbounded "c += jump + 1" loop. A crafted DHCPv6 REPLY with a DOMAIN_LIST option of >= 1025 non-zero bytes makes the label walk leave the buffer and read/write '.' past its end in attacker-chosen strides. An on-link attacker can trigger this without authentication via a forged Router Advertisement (O=1) and a forged DHCPv6 REPLY matching xid/CLIENTID with a long DOMAIN_LIST. The impact is unauthenticated on-link crash of connmand (runs as root). This was introduced in bb06c47.

### CVE-2026-114191

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-24T14:16:38.870 |

Missing Authorization vulnerability in Knit Pay UPI QR Code Payment Gateway for WooCommerce upi-qr-code-payment-for-woocommerce allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects UPI QR Code Payment Gateway for WooCommerce: from n/a through 1.6.3.

### CVE-2026-115887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-23T22:16:58.253 |

GraphQL Scalars is a library of custom GraphQL scalars for creating precise type-safe GraphQL schemas. From 1.24.1 until 2.0.1, GraphQLPhoneNumber in src/scalars/PhoneNumber.ts uses ambiguous nested digit quantifiers that backtrack exponentially when a PhoneNumber value contains a run of digits followed by a character that makes the match fail. GraphQL evaluates parseLiteral during document validation and parseValue during variable coercion before resolver authentication or authorization, so a small unauthenticated request can block the Node.js event loop and stall the server process. serialize is also affected when unvalidated stored values are returned through the scalar. This issue is fixed in version 2.0.1.

### CVE-2026-65825

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-23T21:17:24.870 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. In versions 2.1.0 and prior, a returning client's six-digit booking PIN can be brute-forced online in the victim tenant. A successful guess yields the client's booking access token, granting access to that client's appointment tunnel, which holds their end-to-end-encrypted appointment data, and the ability to act as the client, for example adding or cancelling appointments in the tunnel. The bypass is cross-tenant: state owned by one tenant removes an authentication protection of a different tenant. This crossing of the tenant boundary is the basis for the scope-changed vector. At time of publication, there are no publicly available patches.

### CVE-2026-115778

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-23T21:17:23.320 |

Twisted is an event-based framework for internet applications, supporting Python 3.6+. Prior to 26.10.0rc1, twisted.conch.telnet.Telnet.dataReceived appends every byte received after IAC SB to a persistent subnegotiation buffer until IAC SE is received, without applying a maximum length. Telnet option negotiation occurs before authentication, so an unauthenticated peer can omit the terminator and continuously grow the buffer. The resulting memory exhaustion can terminate the process and every service it hosts. This issue is fixed in version 26.10.0rc1.

### CVE-2026-115776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-23T21:17:23.180 |

Twisted is an event-based framework for internet applications, supporting Python 3.6+. Prior to 26.10.0rc1, twisted.words.protocols.irc.IRC.dataReceived retains all bytes received without a line feed in its per-connection buffer and applies no maximum line length. The twisted.words.service.IRCUser server subclass inherits this behavior, and buffering occurs before PASS, NICK, or USER authentication commands. An unauthenticated connection can continuously grow the buffer until the shared server process runs out of memory and drops all users. This issue is fixed in version 26.10.0rc1.

### CVE-2026-19741

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-23T20:17:21.867 |

Zephyr's OpenThread integration defined CONFIG_OPENTHREAD_JOINER_PSKD with default "J01NME" in modules/openthread/Kconfig.thread (previously subsys/net/l2/openthread/Kconfig, then subsys/net/l2/openthread/Kconfig.thread). J01NME is the example Joining Device Credential used throughout the public OpenThread and Thread commissioning documentation, including Zephyr's own samples/net/sockets/echo_client/README.rst, so it is not a secret. A firmware image built with CONFIG_OPENTHREAD_JOINER_AUTOSTART=y that never overrode the PSKd therefore shipped with a publicly known joining credential compiled in, with no build-time or run-time warning.

The PSKd is the only value that authenticates Thread commissioning: joiner and commissioner run a DTLS-PSK handshake keyed on it, after which the commissioner supplies the full operational dataset. In ot_configure_instance() (modules/openthread/openthread.c), a device with no stored dataset calls otJoinerStart() with the configured PSKd, and ot_joiner_start_handler() calls otThreadSetEnabled() on success. An unauthenticated attacker within 802.15.4 radio range of an uncommissioned device (factory-fresh, after a factory reset, or after a settings erase) can run any stock Thread commissioner registered with J01NME, complete the handshake, and hand the device an attacker-controlled operational dataset.

The device then joins and enables Thread on the attacker's mesh. The attacker becomes its router, seeing, dropping, injecting and spoofing all of the device's IPv6 traffic and impersonating the peers the application expects, while the device is cut off from the network it was meant to join and stays mis-provisioned until it is reset. Only application-layer security with independently provisioned credentials survives. Exposure is limited to builds that enable joiner autostart and leave the PSKd unset; the option is not enabled by default and no in-tree sample uses the vulnerable combination.

The fix removes the default from CONFIG_OPENTHREAD_JOINER_PSKD and adds a BUILD_ASSERT() in modules/openthread/openthread.c, active only under CONFIG_OPENTHREAD_JOINER_AUTOSTART, that fails the build unless a 6-to-32-character PSKd is configured. Products should provision a per-device PSKd from factory data and call otJoinerStart() from the application rather than relying on a credential compiled identically into every unit.

### CVE-2026-106765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-23T15:17:23.333 |

An issue in @rog0x/mcp-docker-tools 1.0.1 allows a remote attacker to execute arbitrary code via the handleImageList function.

### CVE-2026-106764

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-23T15:17:23.203 |

An issue in @rog0x/mcp-git-tools 1.0.1 allows a remote attacker to execute arbitrary code via the resolveBaseBranch function.

### CVE-2026-106763

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-23T15:17:23.063 |

An issue in @justice8096/sagemath-mcp-server 1.0.1 allows a remote attacker to execute arbitrary code via the escapeShellString and sanitizeCode functions.

### CVE-2026-65824

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-23T21:17:24.730 |

OpenReception's appointment booking software provides an end-to-end encrypted appointment booking platform. Prior to version 2.2.1, an attacker who captures a pending invite token can replay it to obtain a passkey-registration credential and register their own passkey on the invited account, taking control of that account. For a staff or tenant-admin invite this yields access to the tenant context tied to that account. This issue has been patched in version 2.2.1.

### CVE-2026-115570

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-299` |
| Published | 2026-10-23T19:17:44.470 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 42.11.16, 43.8.1, 44.9.1, and 45.0.0-beta.6, Electron does not block compromised eMudhra intermediate certificates in Chromium networking, Node.js tls, Node.js https, or Node.js fetch. An attacker who holds a certificate issued through one of these intermediates and can intercept network traffic can impersonate a TLS server to an affected application. This issue is fixed in versions 42.11.16, 43.8.1, 44.9.1, and 45.0.0-beta.6.

### CVE-2026-110975

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-256` |
| Published | 2026-10-23T18:17:20.503 |

A flaw was found in Kruize Autotune. Its REST API ships without an authentication layer, and the endpoints that return datasource configuration — the list-datasources endpoint (GET /datasources) and the datasource-metadata endpoint — serialized datasource objects using a default Gson configuration with no field-exclusion strategy. As a result, the authentication secrets stored for each configured monitoring datasource (basic-auth passwords, bearer tokens, API keys, and OAuth2 client secrets) were returned in cleartext to any client able to reach the service. An attacker with network access to Autotune could harvest these credentials and reuse them to authenticate to the backing monitoring stack.

### CVE-2026-106069

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-23T17:17:19.740 |

A flaw in Node.js TLS hostname verification can cause a server certificate to be validated against a different IP address than the one the client connected to, when the host is a non-canonical IPv4 literal with a leading zero, such as `0127.0.0.1`.

`tls.checkServerIdentity()` normalizes the host following the WHATWG URL rules, which read a leading-zero octet as octal (`0127.0.0.1` becomes `87.0.0.1`), while the connection is made through the operating system resolver, which on some platforms such as macOS reads it as decimal (`127.0.0.1`). A server at the connected address can then be authenticated with a certificate issued for another IP address.

This vulnerability affects Node.js **26.x**, **24.x**, and **22.x**.

### CVE-2026-105483

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-23T17:17:19.573 |

A flaw in Node.js TLS hostname verification allows a certificate without a matching IP address SAN to authenticate a connection to an IPv4 address when the host is written with non-ASCII characters, such as fullwidth digits (`１２７.0.0.1`).

`tls.checkServerIdentity()` did not recognize such hosts as IP addresses, even though they normalize and resolve to a regular IPv4 address, and matched them against the certificate DNS names and Common Name instead. A certificate containing `DNS:127.0.0.1` or `DNS:*.0.0.1` could therefore be accepted for an IP endpoint it was not issued for. This is a regression introduced after the fix for CVE-2026-48618.

This vulnerability affects Node.js **26.x** and **24.x**.

### CVE-2026-105482

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-23T17:17:19.427 |

A flaw in Node.js DNS resolution allows hostnames containing a NUL byte to be silently truncated by the dns.resolve*() functions and dns.reverse(). This is an incomplete fix of CVE-2026-48930, which only covered dns.lookup() and the net/tls host options.

Because the name is passed to c-ares as a C string, resolving attacker.example\0.trusted.example queries attacker.example and returns its records without any error. Applications that validate a hostname, for example against a domain allowlist, and then resolve it with dns.resolve*() can act on records for a different name than the one they validated.

This vulnerability affects Node.js 26.x, 24.x, and 22.x.

### CVE-2026-55459

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-345` |
| Published | 2026-10-23T15:17:33.207 |

The Goobi viewer is a web application that allows digitised material to be displayed in a web browser. From version 25.01 to before version 26.05, AuthenticationEndpoint.verifyOpenIdToken builds its verifier as JWT.require(algorithm).withIssuer(issuer).build() and does not enforce the aud claim during cryptographic validation. The aud check is performed manually afterwards via a single string-equality call, which only handles single-string aud values. In a multi-RP IdP setup, a token whose single-string aud matches the viewer's client ID but was issued for a different relying party passes the check and authenticates the attacker as the token's sub. This issue has been patched in version 26.05.

### CVE-2026-55457

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-1392` |
| Published | 2026-10-23T15:17:33.060 |

The Goobi viewer is a web application that allows digitised material to be displayed in a web browser. Prior to version 26.05, Configuration.getWebApiToken returns the empty string when webapi.authorization.token is not configured. AuthorizationFilter compares the supplied token against this default without first checking that the configured token is non-empty. A request to any @AuthorizationBinding-protected endpoint with an empty ?token= value is therefore accepted. This issue has been patched in version 26.05.

### CVE-2026-114704

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-24T14:16:39.313 |

Deserialization of Untrusted Data vulnerability in Christoph Vielgrader Relevanssi  relevanssi allows Object Injection.This issue affects Relevanssi : from n/a through 4.28.4.

### CVE-2026-39902

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-23T15:17:30.873 |

Cacti is an open source performance and fault management framework. Prior to version 1.2.31, the prior blocklist ([;&| `$\\n\r]) omitted single-quote, double-quote, redirect operators, subshell parens and braces. An authenticated admin could save an input_string` containing single-quote, redirect operator, or subshell parens, and pass the check. This issue has been patched in version 1.2.31.

### CVE-2026-116016

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-24T12:16:57.960 |

yudao-cloud through 2026.09 contains an authorization bypass vulnerability that allows authenticated users to evade row-level data scope restrictions by sending a data-permission-enable header set to false. Attackers can add this header to /admin-api requests, which DataPermissionRpcWebFilter trusts, to read or modify other departments' and users' records within the same tenant.

### CVE-2026-115975

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-24T08:16:52.630 |

Broken access control in JiraController in Cervantes version v1.3-beta could allow an attacker to create, edit, or delete Jira tickets for vulnerabilities in other projects

### CVE-2026-114697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:52.490 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in QuarkA QA Analytics qa-heatmap-analytics allows Stored XSS.This issue affects QA Analytics: from n/a through 5.3.0.1.

### CVE-2026-114695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:52.360 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Infomaniak Network VOD Infomaniak vod-infomaniak allows Stored XSS.This issue affects VOD Infomaniak: from n/a through 1.5.14.

### CVE-2026-114694

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:52.230 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Pixelite Events Manager events-manager allows Reflected XSS.This issue affects Events Manager: from n/a through 7.4.8.

### CVE-2026-114179

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:51.700 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in wordplus BP Better Messages bp-better-messages allows DOM-Based XSS.This issue affects BP Better Messages: from n/a through 3.1.3.

### CVE-2026-114178

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:51.567 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bold Grid W3 Total Cache w3-total-cache allows Stored XSS.This issue affects W3 Total Cache: from n/a through 2.10.7.

### CVE-2026-112869

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:51.437 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Noah Hearle We’re Open! opening-hours allows Reflected XSS.This issue affects We’re Open!: from n/a through 2.6.

### CVE-2026-112844

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-24T08:16:51.160 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Arraytics WP Event Solution wp-event-solution allows Stored XSS.This issue affects WP Event Solution: from n/a through 4.1.26.

### CVE-2026-115807

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-24T05:17:06.500 |

The User Profile Builder – Beautiful User Registration Forms, User Profiles & User Role Editor plugin for WordPress is vulnerable to Limited Privilege Escalation in all versions up to, and including, 4.0.3. This is due to the Gutenberg Register block passing the attacker-controlled Assigned Role attribute directly into the `[wppb-register]` shortcode without server-side authorization. The role guard in the form builder only downgrades roles that carry the manage_options or remove_users capability, leaving the Editor role and other privileged non-Administrator roles completely unrestricted. This makes it possible for authenticated attackers with Author-level access and above to create new WordPress accounts bearing the Editor role (or any other role that lacks the two guarded capabilities).

### CVE-2026-115586

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-23T20:17:21.363 |

virtualenv is a tool for creating isolated virtual python environments. From 21.14.9 until 21.14.13, the bash bin/activate script can copy an attacker-controlled --prompt value into PS1 without escaping dollar signs or backticks when both promptvars and POSIX mode are disabled during activation. Re-enabling promptvars, running set -o posix, or starting an interactive child bash that inherits the exported PS1 can then expand command substitution in the stored VIRTUAL_ENV_PROMPT value and execute commands as the user who activates the environment. This issue is fixed in version 21.14.13.

### CVE-2026-115585

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-10-23T20:17:21.230 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.2, an incomplete remediation for repeated malformed cross-reference entries in GHSA-55h5-xmcq-c37v could still trigger a complete PDF stream reload during each recovery attempt even when a recovery cache was present, causing crafted cross-reference streams to produce long runtimes. This issue is fixed in version 6.21.2.

### CVE-2026-115580

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-834` |
| Published | 2026-10-23T20:17:21.087 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.2, an attacker can craft a PDF with a standard cross-reference table whose declared entry count exceeds what the file can contain, causing excessive processing and long runtimes when the file is opened. This issue is fixed in version 6.21.2.

### CVE-2026-115572

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-23T20:17:20.940 |

pypdf is a free and open-source pure-python PDF library. Prior to 6.21.2, an attacker can craft a PDF that repeatedly references the same nonexistent indirect object, causing relevant file parts such as pages to trigger repeated full-file recovery loads and long runtimes when accessed. This issue is fixed in version 6.21.2.

### CVE-2026-112342

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-23T19:17:43.203 |

Tandoor Recipes before 2.7.0 contains an improper cache-key design in cookbook/helper/permission_helper.py that allows authenticated users to retain stale group-based permissions across different spaces by exploiting a cache key keyed only on user id while omitting the active space, with the cached entry's TTL refreshed on every request. Attackers can create their own space to obtain an admin group designation, then switch their active space to a victim space where they hold lesser privileges, causing the stale cached admin decision to authorize elevated access and bypass group revocations or demotions across multiple permission classes and views.

### CVE-2026-115478

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459;CWE-863` |
| Published | 2026-10-23T15:17:30.023 |

obsidian-tc is a governed, agent-ready Model Context Protocol server for Obsidian vaults. From 1.0.1 until 1.31.4, `create_entity`, `link_entities`, `rename_entity`, `unlink_entities` and `delete_entity` regenerate memory notes from SQLite at the computed `memory/<type>/<name>.md` path without reliably preserving note ownership or the consistency of a failed lifecycle operation. During shared materialization, a hand-authored note or an orphan left by a different entity whose name sanitized to the same path could have its entire body overwritten on the next write naming that type and name, with non-owned frontmatter preserved. `rename_entity` also seeded the destination path with a direct atomic write without validating ownership and could overwrite a foreign note there. Separately, several tools mutated SQLite before fallible filesystem work: `create_entity` and `link_entities` inserted the row or relation before materialization; `rename_entity` updated the entity, including a retired status, before updating its note; `unlink_entities` removed a relation before rematerializing the source note; and `delete_entity`'s cascade removed the target and its relations before rematerializing neighbouring notes. A later filesystem failure could therefore leave a row or relation changed and the memory graph inconsistent with the notes on disk even when the operation failed. An authorized caller with the required memory-tool permissions could, without intending to, destroy the body of a vault note outside the entity being written; `delete_entity` additionally requires its deletion permission and destructive confirmation, which this memory flaw does not bypass. Snapshots-before-write through `restore_note` mitigate the overwrite only where snapshots are enabled and the note had previously been written through obsidian-tc. This issue is fixed in version 1.31.4.

### CVE-2026-115477

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-10-23T15:17:29.840 |

obsidian-tc is a governed, agent-ready Model Context Protocol server for Obsidian vaults. From 1.13.0 until 1.31.4, on a Streamable HTTP deployment with `auth.jwtSecret` configured and a 2026-07-28-era client declaring `elicitation.form` support, a dispatch-gated tool call offered an `inputRequired` confirmation could still complete after the human declined or cancelled, or the elicitation response was omitted or malformed, provided the client echoed the validly bound `requestState` on resubmission. The server trusted an authentic, call-bound state as proof of approval even though that state was minted before the `elicitation/create` leg was asked and proved only that the resubmission belonged to the same call. A client behaving incorrectly or under an attacker's control could therefore execute dispatch-gated destructive vault operations without the human's approval, while still requiring the caller's ordinary tool permissions. Only tools marked `destructive: true` or requiring a scope with a human-in-the-loop floor were reachable through this bypass. The sixteen handler-side conditionally gated tools, including `write_note` overwrite and `move_note`, did not read elicitation state on the modern wire and let neither approval nor decline through that path. Affected deployments using stdio or leaving `auth.jwtSecret` unset instead used the CLI `elicit_token` fallback and did not offer this `requestState` round trip. The fix does not prevent a malicious client from reporting a fabricated approval, because the server cannot verify that the client displayed the form or that a human saw it. This issue is fixed in version 1.31.4.
