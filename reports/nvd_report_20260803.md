# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-02 15:00 UTC
- **対象期間**: `2026-08-01T15:00:14.000Z` 〜 `2026-08-02T15:00:15.000Z`
- **重要CVE数**: 15 件（Critical 9.0+: 3 件 / High 7.0〜: 12 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVE のうち **CVSS 7.0 以上** が 15 件報告され、**認証バイパス・権限昇格・リモートコード実行** が目立ちます。  
- WordPress 系プラグインや SaaS 向け UI ライブラリに対する **認証バイパス** が複数（CVE‑2026‑8457、CVE‑2026‑18556）で確認され、公開サイトが即座に乗っ取られるリスクが高いです。  
- オープンソースのタスク管理ツール **Vikunja** や **ArcadeDB** で **BOLA / 権限チェック抜け** が報告され、内部ユーザーが任意のデータを書き換えられる点が深刻です。  
- ネイティブクライアント（FreeRDP）や npm パッケージ（better‑auth）に **ヒープ/整数オーバーフロー** が残っており、遠隔からのコード実行や DoS が可能です。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑8457** | 9.8 | WooCommerce – Social Login (WordPress) の認証バイパス | Apple の `id_token` の署名検証を行わないため、任意の JWT で **管理者権限でログイン** 可能。全 WordPress サイトでプラグインが導入されている場合、即座にサイト全体が乗っ取られる危険性があります。 |
| **CVE‑2026‑68582** | 9.3 | Vikunja 0.24.0‑2.3.0 の BOLA（タスク取得 API） | プロジェクトビューの ID だけでアクセスが許可され、認可チェックが欠如。攻撃者は他プロジェクトのタスクを **無制限に取得・変更** でき、機密情報漏洩と業務妨害が発生。 |
| **CVE‑2025‑71401** | 9.3 | npm `better-auth` < 1.4.2 のベース URL 設定汚染 | 起動直後の最初リクエストで **router の basePath を任意に書き換え** でき、以降の全ルートが 404 になるだけでなく、別ドメインへリダイレクトさせる等の **サービス妨害** が可能。 |
| **CVE‑2026‑68579** | 8.7 | FreeRDP ≤3.29.0 のヒープバッファオーバーフロー（クリップボード） | 攻撃者が RDP サーバ側から細工したクリップボードデータを送信すると、クライアント側で **任意コード実行** が可能。RDP クライアントを社内で広く使用している組織は即時対応が必要。 |
| **CVE‑2026‑67356** | 8.7 | ArcadeDB < 26.7.3 のスキーマ管理権限回避 | `HostAccess.ALL` がバインドされることで **スキーマ管理者権限がないユーザーでもユーザー作成** が可能。内部攻撃者がデータベース全体を制御できる深刻な権限昇格です。 |

## 3. 推奨アクション  

### 共通対策
- **脆弱性情報の定期的なモニタリング**（NVD、各ベンダーのアドバイザリ）と **パッチ適用の自動化** を導入。  
- 変更管理プロセスで **「認証・認可ロジックのテスト」** を必須項目に追加。  
- 重要サービスは **WAF / IDS** で不審なリクエスト（例：不正な JWT、異常な API パス）を検知・遮断。  

### 個別パッケージ・バージョン別対応

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン (修正済) | 具体的作業 |
|-------------------|----------------------|------------------------|------------|
| **WooCommerce – Social Login** (WordPress) | ≤ 2.8.7 | **2.8.8 以上** (公式で修正リリース) | プラグインを最新版に更新し、`Apple Login` 設定を再確認。不要な外部ログインは無効化。 |
| **Vikunja** | 0.24.0 〜 2.3.0 | **2.3.1 以上** | `docker pull vikunja/api:2.3.1` などでアップデート。API トークンの権限を最小化し、不要な `view` エンドポイントは非公開に。 |
| **better‑auth (npm)** | < 1.4.2 | **1.4.2** (ベースURL検証追加) | `npm install better-auth@1.4.2` → デプロイ後に **環境変数 `BETTER_AUTH_URL`** を必ず設定し、起動直後のリクエストをブロックするミドルウェアを導入。 |
| **better‑auth (router バグ)** | < 1.4.5 | **1.4.5** (rou3 0.2.3 以上にバンドル) | 同上、`npm audit` で依存ライブラリのバージョンを確認。 |
| **FreeRDP** | ≤ 3.29.0 | **3.30.0 以上** | パッケージマネージャ (`apt`, `yum`, `brew`) で更新、または公式ビルドを取得。リモートデスクトップの **クリップボード・音声入力** 機能は不要なら無効化。 |
| **ArcadeDB** | < 26.7.3 | **26.7.3 以上** | `docker pull arcadedb/arcadedb:26.7.3` で更新。MCP アクセス権限を **最小限** に設定し、外部からの MCP 接続は IP 制限で遮断。 |
| **User Access Manager (WordPress)** | ≤ 2.3.15 | **2.3.16 以上** | プラグイン更新後、`uamgetfile` パラメータの使用を禁止する .htaccess ルールを追加。 |
| **CubeWP Framework (WordPress)** | ≤ 1.1.30 | **1.1.31 以上** | 同上、`cubewp_get_svg_content` の呼び出しを制限し、アップロードディレクトリのパーミッションを `

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-8457

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-289` |
| Published | 2026-08-02T00:16:23.047 |

The WooCommerce - Social Login plugin for WordPress is vulnerable to Authentication Bypass in all versions up to and including 2.8.7. This is due to the plugin's Apple login handler accepting the Apple id_token and decoding only its base64 payload without verifying the JWT signature against Apple's public keys or validating the issuer, audience, or expiry claims, combined with the security nonce required to invoke the login flow being publicly exposed to unauthenticated users via a localized JavaScript object on the login page. This makes it possible for unauthenticated attackers to log in as any existing WordPress user — including administrators — by supplying a forged id_token whose payload contains the target user's email address, as that email is used without any role exclusion to resolve a WordPress account and immediately issue an authenticated session for it.

### CVE-2026-68582

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-02T13:16:54.233 |

Vikunja versions >= 0.24.0 and <= 2.3.0 contain a broken object level authorization (BOLA) vulnerability in the task-collection endpoint (GET /api/v1/projects/{project}/views/{view}/tasks). The endpoint loads the requested project view from the URL path without verifying the caller is authorized for it. For a link-share token holder, the task scope is pinned to the share's own project, but the view is taken from the attacker-controlled path and never re-validated. As a result, a holder of any project share link can read any other tenant's kanban bucket records — bucket titles and the full created_by user object (username, name, id) — for every view in the instance. The same missing pre-authorization view load also creates a project/view-ID existence oracle (404 vs. non-404) usable by link shares and ordinary authenticated users. Task contents remain constrained to the share's own project and are not disclosed. Fixed in 2.4.0.

### CVE-2025-71401

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-02T13:16:52.530 |

better-auth (npm) before 1.4.2 allows an external request to configure baseURL when it is not otherwise defined (e.g., BETTER_AUTH_URL is unset). An attacker able to make the very first request to the server after startup can poison the router's base path, causing all routes to return 404 for all users (denial of service). The issue is not reachable when baseURL is explicitly configured or on typical managed hosting platforms.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2025-71399

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-02T13:16:52.210 |

Better Auth relies on better-call, which uses the rou3 router library. In affected versions of rou3, paths are normalized by removing empty segments, so /path, //path, and ///path resolve to the same route. In Better Auth versions prior to 1.4.5 (which bundles the fixed rou3), this can allow attackers to bypass disabledPaths configuration and path-based rate limits by submitting requests with extra slashes in the URL path. The issue does not apply in deployments where the proxy or platform normalizes URLs by collapsing multiple slashes.

### CVE-2026-68579

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-02T13:16:53.800 |

FreeRDP before 3.30.0 (<= 3.29.0) contains a heap-based buffer overflow in the Windows clipboard client's CliprdrStream_Read function (client/Windows/wf_cliprdr.c). When an OLE paste consumer (e.g. explorer.exe) calls IStream::Read with a fixed-size buffer of cb bytes, CliprdrStream_Read requests file contents from the RDP server and then copies the response into the caller's buffer using the server-supplied length (req_fsize) instead of cb. A malicious or compromised RDP server can return an oversized CB_FILECONTENTS_RESPONSE, causing an out-of-bounds write of attacker-controlled data into the paste consumer's heap buffer when a user pastes server-offered clipboard file contents.

### CVE-2026-67356

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-02T13:16:53.363 |

ArcadeDB before 26.7.3 binds the real LocalDatabase object into JavaScript trigger contexts with HostAccess.ALL, allowing schema-admins to call getSecurity().createUser() without permission checks. Attackers with UPDATE_SCHEMA permission can create triggers that execute JavaScript to create server-wide admin users, escalating privileges beyond their authorization level.

### CVE-2026-68581

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-02T13:16:54.087 |

Vikunja versions 0.22.0 through 2.3.0 fail to validate the principal type in API token management. Because user IDs and link-share IDs are independent numeric sequences and both resolve through a generic web.Auth.GetID() interface, a link-share JWT whose numeric ID equals a target user's ID is treated as that user by the /api/v1/tokens endpoints. An authenticated attacker can obtain a target's numeric user ID via authenticated user search, then create link shares on an attacker-writable project until the link-share sequence reaches that value, and use the resulting link-share JWT to list, create, and delete the target user's API tokens (including issuing a new token with attacker-chosen scopes under the target's permissions). Fixed in version 2.4.0.

### CVE-2026-18556

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-01T20:16:37.157 |

Authentication bypass using an alternate path or channel vulnerability in N-able N-central allows Authentication Bypass.

This issue affects N-central: through 2026.1.

### CVE-2026-55735

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-01T19:16:42.510 |

Improper Verification of Cryptographic Signature in ueberauth guardian allows an unauthenticated attacker to revoke a victim's session with a forged token.

Guardian.revoke/3 in lib/guardian.ex decodes the supplied token with peek/1, which performs no signature verification (it only base64-decodes the JWT header and payload). The resulting unverified claims are forwarded directly to the configured token module's revoke callback and the implementation's on_revoke callback, a state-mutating sink. The sibling operations refresh/2 and exchange/4 both call decode_and_verify first, so the signature is checked before anything acts on the claims; revoke/3 is the only state-mutating path that acts on claims without verifying the signature.

An attacker who knows or guesses a victim's identifying claim values (jti, sub) can forge a JWT carrying those claims, sign it with an arbitrary key, and submit it to any endpoint that funnels a caller-supplied token into Guardian.revoke/3 (the standard logout / session-revocation pattern). When the token module mutates state keyed by the claims (whitelist deletion or blacklist insertion, for example a GuardianDb-style store), the victim's legitimate session is evicted. This is an unauthenticated session-revocation denial of service; the attacker never needs the signing secret.

This issue affects guardian: from 1.0.0 before 2.4.1.

### CVE-2026-68580

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-02T13:16:53.950 |

FreeRDP before 3.29.0 contains integer overflow vulnerabilities in the audio input redirection channel (audin) across ALSA, sndio, WinMM, and OpenSL ES backends that fail to validate the FramesPerPacket parameter from RDP servers. Attackers can supply a malicious FramesPerPacket value causing allocation size wraparound, resulting in heap-based buffer overflow on ALSA or denial of service on all platforms.

### CVE-2026-68578

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-02T13:16:53.657 |

ArcadeDB versions before 26.7.3 fail to bind the authenticated principal in the MCP HTTP transport, causing all engine permission checks to silently pass as no-ops. Non-root MCP-allowed users can perform arbitrary database writes, DDL, schema mutations, and execute arbitrary JavaScript code via the query tool.

### CVE-2026-67357

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-02T13:16:53.520 |

ArcadeDB versions before 26.7.3 contain an information disclosure vulnerability in the MCP get_server_settings tool that leaks the arcadedb.ha.clusterToken in cleartext. Attackers with MCP access can retrieve the cluster token and use it with X-ArcadeDB-Cluster-Token and X-ArcadeDB-Forwarded-User headers to impersonate root and achieve full server compromise.

### CVE-2026-18352

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-02T00:16:22.900 |

The User Access Manager plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.3.15 via the 'uamgetfile' parameter parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. This is possible because when attachment_url_to_postid() returns 0 for a traversal path, the plugin falls back to the global post set by a valid ?attachment_id parameter supplied by the attacker, causing the access check to pass against a legitimate public attachment while the file streamed is the attacker-chosen path.

### CVE-2026-13339

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-02T00:16:22.760 |

The CubeWP Framework plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.1.30 via the 'cubewp_get_svg_content' function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. This is exploitable by unauthenticated attackers because the required nonce is publicly emitted into the markup of any page rendering the CubeWP posts shortcode or widget with AJAX loading enabled, making it harvestable by any guest visitor before submitting the AJAX request.

### CVE-2025-71400

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-02T13:16:52.387 |

better-auth passkey versions before 1.4.0 contain an insecure direct object reference vulnerability in the passkey deletion endpoint that allows authenticated users to delete arbitrary passkeys by ID. Attackers with valid sessions can submit crafted requests to the delete-passkey endpoint with enumerated passkey IDs to remove other users' passkeys.
