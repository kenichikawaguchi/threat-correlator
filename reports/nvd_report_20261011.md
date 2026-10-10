# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-10 15:01 UTC
- **対象期間**: `2026-10-09T15:00:35.000Z` 〜 `2026-10-10T15:01:21.000Z`
- **重要CVE数**: 153 件（Critical 9.0+: 47 件 / High 7.0〜: 106 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 30 件以上**と非常に多く、特に **リモートコード実行 (RCE)・認証バイパス・オブジェクトインジェクション** が目立ちます。  
- WordPress 系プラグイン（ThemeREX 系、WPCOM Member、3D Product Configurator など）と、AI ワークフロー基盤（Astron Agent）や開発ツール（JetBrains Exposed）で深刻な脆弱性が集中しています。  
- 多くは **入力検証・サニタイズ不足** が根本原因で、攻撃者が任意コードを実行したり、管理者権限を取得できる点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑108263** | 9.9 (CVSS:3.1) | Astron Agent のコードノードが `LocalExecutor` をデフォルトで選択し、任意コード実行が可能 | AI エージェント基盤は企業の内部プロセス自動化に利用されることが多く、**リモートで任意コードが実行されると全システムが乗っ取られる危険**。バージョン **1.1.2 未満** が対象。 |
| **CVE‑2026‑103889** | 9.8 | WooCommerce 用 3D Product Configurator プラグインで RCE（`xpv_image` パラメータ） | e‑コマースサイトに直接組み込まれるプラグインで、**顧客が画像をアップロードするだけでサーバ上でコードが実行**できる。全バージョン **2.16.2 まで** が影響。 |
| **CVE‑2026‑94589** | 9.8 | Contact Form 7 拡張プラグインで任意ファイルアップロード | ファイルアップロードのバリデーションが全く無く、**Web シェルやマルウェアを設置**できる。バージョン **3.4.5 まで** が対象。 |
| **CVE‑2026‑104803** | 9.8 | WPCOM Member プラグインで認証バイパス（`uuid`/`code` パラメータ） | ソーシャルログインフローの検証が抜けており、**認証なしで管理者権限が取得**可能。全バージョン **1.7.27 まで** が影響。 |
| **CVE‑2026‑108474** | 9.8 | JetBrains Exposed 1.5.1 未満で SQL インジェクション | データベース操作用 API が文字列をエスケープせず、**任意の SQL が実行**できる。開発・テスト環境だけでなく本番環境でも利用されるケースが多い。 |

> **共通点**：すべて **ネットワーク越しに直接攻撃が成立** し、**認証不要または低権限で実行** できる点が危険度を高めています。  

---

## 3. 推奨アクション  

### (1) 速やかなパッチ適用・バージョンアップ
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン | 備考 |
|-------------------|-------------------|----------------|------|
| Astron Agent | < 1.1.2 | **≥ 1.1.2** | `CODE_EXEC_TYPE` の明示的設定が必須になるパッチが含まれる |
| WooCommerce 3D Product Configurator | ≤ 2.16.2 | **≥ 2.16.3** | `xpv_image` パラメータに認証・nonce チェックが追加 |
| Extensions For CF7 | ≤ 3.4.5 | **≥ 3.4.6** | ファイル拡張子・MIME・サイズ検証を実装 |
| WPCOM Member | ≤ 1.7.27 | **≥ 1.7.28** | `uuid`/`code` の検証ロジックを強化 |
| JetBrains Exposed | < 1.5.1 | **≥ 1.5.1** | プレースホルダー化されたクエリに置き換え |

> **※** それぞれのベンダーが提供する「Security Advisory」や「Release Note」を必ず確認し、**アップデート手順に従ってロールバックプランを用意**してください。

### (2) 入力検証・サニタイズの徹底
- **サーバ側でのホワイトリスト方式**（許可された文字列・ファイルタイプのみ受け付ける）を実装。  
- WordPress では `wp_nonce_field()` と `current_user_can()` を必ず組み合わせ、プラグイン側の独自バリデーションが不十分な場合は **Must‑Use プラグイン** で追加チェックを行う。  
- AI/Workflow 系（Astron Agent 等）では **`CODE_EXEC_TYPE` を必ず設定し、外部からのコード実行を禁止** するコンフィグをデフォルト化。

### (3) アクセス制御・ネットワーク分離
- 管理画面・プラグインのエンドポイントは **IP アクセス制限**（例：社内 IP のみ）や **WAF でのパラメータ検査** を導入。  
- JetBrains Exposed のような開発ツールは **内部ネットワークのみ** に限定し、外部からの直接アクセスを防止。  

### (4) ログ監視・インシデント対応体制の強化
- `auth.log`, `access.log`, `php_error.log` などに **不審なパラメータ（例：`xpv_image=...`, `uuid=...`）** が記録されたら即時アラート。  
- 侵入テストツール（Burp Suite, OWASP ZAP）で **定期的なスキャン** を実施し、未パッチの脆弱性が残っていないか確認。  

### (5) バックアップとリカバリ手順の見直し
- 特に **CVE‑2026‑107806 (Nginx UI の復元機能)** のようにバックアップデータが攻撃材料になるケースがあるため、バックアップファイルは **暗号化・署名** し、復元時のキー検証を必ず行う。  

---

### まとめ
- 今回の CVE は **リモートからのコード実行や認証回避** が共通テーマであり、**プラグイン・フレームワークの入力検証不足** が根本原因です。  
- **最優先でパッチ適用**し、**入力サニタイズ・アクセス制御**を強化すれば、被害拡大リスクは大幅に低減できます。  


---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-108263

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95;CWE-306;CWE-653;CWE-863;CWE-1392` |
| Published | 2026-10-09T21:17:04.527 |

Astron Agent is an agentic workflow platform for building and running AI agents. Prior to 1.1.2, the default workflow code-node path through /console-api/workflow/code/run and /workflow/v1/run selects LocalExecutor in core/workflow/engine/nodes/code/code_node.py when CODE_EXEC_TYPE is not explicitly changed. LocalExecutor supplies complete Python builtins to dynamic code execution without the documented sandbox restrictions. An authenticated low-privilege tenant can execute code as root in the core-workflow container and use shared service and database credentials to bypass application-level tenant checks, read or modify other tenants' data, and disrupt shared services. This issue is fixed in version 1.1.2.

### CVE-2026-93945

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:07.057 |

Deserialization of Untrusted Data vulnerability in Axiomthemes Balance balance allows Object Injection.This issue affects Balance: from n/a through 1.12.0.

### CVE-2026-93944

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.930 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Camelia camelia allows Object Injection.This issue affects Camelia: from n/a through 1.2.15.

### CVE-2026-93943

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.803 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Convex convex allows Object Injection.This issue affects Convex: from n/a through 1.16.0.

### CVE-2026-93942

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.683 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Dwell dwell allows Object Injection.This issue affects Dwell: from n/a through 1.16.0.

### CVE-2026-93941

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.557 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Edema edema allows Object Injection.This issue affects Edema: from n/a through 1.2.2.2.

### CVE-2026-93940

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.433 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Greeny greeny allows Object Injection.This issue affects Greeny: from n/a through 2.10.0.

### CVE-2026-93938

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.310 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Hogwords hogwords allows Object Injection.This issue affects Hogwords: from n/a through 1.2.7.

### CVE-2026-93937

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.187 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Hygia hygia allows Object Injection.This issue affects Hygia: from n/a through 1.21.0.

### CVE-2026-93936

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:06.060 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group IPharm ipharm allows Object Injection.This issue affects IPharm: from n/a through 1.2.4.

### CVE-2026-93935

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.933 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Let's Play playhockey allows Object Injection.This issue affects Let's Play: from n/a through 1.1.15.

### CVE-2026-93934

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.810 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Partiso partiso allows Object Injection.This issue affects Partiso: from n/a through 1.1.13.

### CVE-2026-93933

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.680 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Rosalinda rosalinda allows Object Injection.This issue affects Rosalinda: from n/a through 1.2.4.

### CVE-2026-93932

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.547 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Smart Casa smart-casa allows Object Injection.This issue affects Smart Casa: from n/a through 1.0.12.

### CVE-2026-93931

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.427 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Smash smash allows Object Injection.This issue affects Smash: from n/a through 1.12.0.

### CVE-2026-93930

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.300 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Tantra tantra allows Object Injection.This issue affects Tantra: from n/a through 2.9.0.

### CVE-2026-93929

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.183 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Travesia travesia allows Object Injection.This issue affects Travesia: from n/a through 1.1.16.

### CVE-2026-93927

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:05.050 |

Deserialization of Untrusted Data vulnerability in Axiomthemes Veto veto allows Object Injection.This issue affects Veto: from n/a through 1.6.0.

### CVE-2026-62046

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:04.777 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Gutentype gutentype allows Object Injection.This issue affects Gutentype: from n/a through 2.1.12.

### CVE-2026-62045

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:04.647 |

Deserialization of Untrusted Data vulnerability in ThemeREX Group Booklovers booklovers allows Object Injection.This issue affects Booklovers: from n/a through 2.13.0.

### CVE-2026-104803

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-10T08:17:04.210 |

The WPCOM Member plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 1.7.27 via the `uuid` and `code` parameters of the social-login callback handler registered on the `init` hook. The vulnerability exists because the `login` function's social-login flow performs no nonce validation, no OAuth state verification, and no per-visitor namespace isolation in the session store, allowing an unauthenticated attacker to issue a crafted GET request that writes an attacker-named, attacker-valued entry into the global session namespace (bypassing the per-visitor prefix by prepending an underscore), then issue a second GET request triggering `weapp_new_user()` to read that forged entry and resolve the attacker-supplied `openid` value to a bound WordPress account before `wp_set_auth_cookie()` establishes a fully authenticated session. This makes it possible for unauthenticated attackers to log in as any WordPress user — including administrators — whose bound social provider identifier (openid/unionid) is known or discoverable. Successful exploitation requires that the target site has at least one social provider configured (which activates the vulnerable handler) and that the attacker knows or can enumerate the victim account's bound openid or unionid.

### CVE-2026-103889

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T05:16:39.130 |

The 3D Product configurator for WooCommerce plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 2.16.2 via the 'xpv_image' parameter parameter. This is due to missing authentication and nonce checks on the wp_loaded handler combined with no sanitization of the xpv_image POST parameter before it is echoed unescaped into a Dompdf-rendered HTML template with PHP execution enabled. This makes it possible for unauthenticated attackers to execute code on the server. The only nonce and authentication check in the handler is entirely enclosed in a block comment with no replacement, making the endpoint reachable via a single unauthenticated POST to any URL on the site.

### CVE-2026-94589

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T04:18:19.713 |

The Extensions For CF7 (Contact form 7 Database, Conditional Fields and Redirection) plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.4.5 via the extcf7_submit function. This is due to missing file extension, MIME type, and size validation in the signature field's validation_filter(), combined with the absence of PHP-execution guards in the upload directory and a sanitize_file_name() bypass that converts shell.php- into shell.php. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-104732

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-10T04:18:08.493 |

The Advanced IP Blocker plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 8.13.13 The vulnerability exists because `handle_login_action()` performs no server-side check — via transient, session marker, or equivalent — that a requester completed step-1 password authentication before processing a step-2 TOTP submission for the POSTed `user_id`; compounding this, an error branch in the function unconditionally mints a fresh `advaipbl-2fa-interim-{user_id}` nonce and delivers it in a `Location` header to any unauthenticated caller, after which `display_2fa_login_form_step_2()` renders a valid `advaipbl-2fa-verify-{user_id}` nonce in HTML — both nonces computed against a fixed `uid=0` empty-session context and therefore fully reusable by the attacker across subsequent requests. This makes it possible for unauthenticated attackers to bypass authentication entirely for any 2FA-enabled account, including administrators, by brute-forcing an unthrottled 6-digit TOTP code (no attempt counter, no account lockout, and no `wp_login_failed` firing) and receiving a fully authenticated session cookie via `wp_set_auth_cookie` without ever supplying the account password, resulting in complete site takeover. Exploitation requires only a known `user_id` for an account that has the plugin's 2FA feature enabled.

### CVE-2026-108474

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T00:17:03.673 |

In JetBrains Exposed before 1.5.1 sQL injection was possible via unescaped string arguments of several SQL functions

### CVE-2026-107806

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-09T15:17:10.150 |

Nginx UI is a web user interface for the Nginx web server. From 2.3.8 until 2.5.0, an authenticated administrator with an active secure session can submit attacker-controlled portable backup key material and a matching manifest to POST /api/restore. The restore flow trusts the supplied key, decrypts attacker-controlled contents, and replaces the live app.ini, including protected nginx command settings such as TestConfigCmd. Triggering POST /api/nginx/test then executes the restored command in the Nginx UI runtime context, affecting confidentiality, integrity, and availability. This issue is fixed in version 2.5.0.

### CVE-2026-108261

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-441;CWE-601` |
| Published | 2026-10-09T21:17:04.347 |

Tina is a headless content management system. Prior to tinacms 3.14.0 and @tinacms/app 2.5.14, the /~/* admin preview route in packages/tinacms/src/admin/index.tsx can turn an attacker-controlled hash-router splat into an off-origin iframe URL through packages/@tinacms/app/src/preview.tsx, while packages/@tinacms/app/src/lib/preview-origin.ts derives expectedOrigin from that same URL for the GraphQL message channel in packages/@tinacms/app/src/lib/graphql-reducer.ts. An unauthenticated attacker can send a crafted link to a signed-in editor, cause the admin to frame an attacker origin, and have that frame treated as the trusted preview. The attacker-controlled frame can submit GraphQL reads or mutations that the admin executes with the editor credentials, exposing or modifying protected content. This issue is fixed in tinacms 3.14.0 and @tinacms/app 2.5.14.

### CVE-2026-107845

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-10-09T20:17:10.457 |

Contao is an Open Source CMS. From version 4.0.0 until 5.3.50 and 5.7.12, an unauthenticated visitor can submit a comment whose email or website metadata is rendered without sufficient attribute and URL encoding by listComments() in comments-bundle/contao/dca/tl_comments.php. When a backend user opens the Comments module, attacker-controlled script can execute in the Contao backend origin under that user's session. Unpublished comments remain visible to moderators, so moderation does not prevent exposure. This issue is fixed in versions 5.3.50 and 5.7.12.

### CVE-2026-107824

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-09T18:17:04.350 |

x64dbg-MCP Server is a native Model Context Protocol (MCP) plugin for x64dbg that exposes the debugger's full functionality over HTTP. Prior to 1.1, x64dbg-MCP Server exposes all MCP debugger tools over HTTP and SSE without authentication while listening on 0.0.0.0 by default. Any unauthenticated network client that can reach the default port, 9094 for x64 or 9095 for x32, can execute arbitrary x64dbg commands, attach to processes by PID, read and write debuggee memory, and write files to arbitrary paths. This issue is fixed in version 1.1.

### CVE-2026-39460

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-09T15:17:14.660 |

Usernames and passwords, including the default factory credentials, are stored in plaintext within the configuration file. With administrator rights, the configuration file can be viewed through the CLI or they can be exported from the device through a TFTP transfer from the web interface. A TFTP transfer can be initiated through SNMP which does not require authentication.

### CVE-2026-33367

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-09T15:17:14.340 |

SNMP can be used to perform administrative actions such as retrieving configuration files, modifying user accounts or device settings, and initiating firmware or bootloader upgrades or downgrades—all without any authentication.

### CVE-2026-28745

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-257` |
| Published | 2026-10-09T15:17:13.670 |

Usernames and passwords, including the default credentials, are stored in the configuration file using weak encryption. If the default credentials are known by a malicious user, they could obtain other credentials on the system.

### CVE-2026-15340

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-09T15:17:13.510 |

lwIP SMTP client does not check the size of inputs, potentially allowing a buffer overflow.

### CVE-2026-108109

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-09T15:17:12.047 |

PHPNuxBill through 2025.3.20 contains an account takeover vulnerability in the customer password reset flow in system/controllers/forgot.php that allows unauthenticated attackers to brute-force the 6-digit otp_code. Attackers knowing a customer username can guess the code without attempt limits or lockout, then read the newly set password from the HTTP response to hijack the account.

### CVE-2026-108107

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T15:17:11.713 |

PHPNuxBill through 2025.3.20 contains an unauthenticated SQL injection vulnerability in the radius.php FreeRADIUS REST endpoint that interpolates request parameters into whereRaw() queries. Attackers can send crafted username, macAddr or nasid parameters to the accounting or authenticate actions to extract customer records and credentials via time-based blind SQL injection.

### CVE-2026-105278

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-09T15:17:08.197 |

The published Docker image for openPDC includes a fixed administrative credential with no forced change on first use. An attacker with network access to the management interface can authenticate using this credential and gain full administrative control of the application.

### CVE-2026-108157

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-09T17:16:46.703 |

Pingvin Share X from 0.19.0 before 1.22.0 contains an improper authentication vulnerability that allows remote unauthenticated attackers to take over accounts by abusing automatic OAuth email linking in OAuthService.signUp(). Attackers can register a victim's unverified email on an enabled OAuth/OIDC provider, exploiting the missing email_verified check in GenericOidcProvider, to sign in as the victim including administrators while bypassing TOTP.

### CVE-2026-32645

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-09T15:17:14.017 |

Default factory credentials with administrative access are enabled and persist even after configuring other administrator accounts.

### CVE-2026-104801

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-10T07:16:40.560 |

The PPOM – Product Addons & Custom Fields for WooCommerce plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the rename_files function in all versions up to, and including, 34.0.10 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The relocated file is moved byte-identically into the publicly accessible wp-content/uploads/ppom_files/confirmed/ directory, meaning the attack also results in arbitrary file read for any web-readable file on the server.

### CVE-2026-97670

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T05:16:40.850 |

The Avada (Fusion) Builder plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 7.16.1. This is due to the plugin not properly verifying authorization before dispatching a WordPress action hook whose name is taken from an attacker-supplied form-field value (via the notification email_message [field] placeholder and the {action_hook,...} dynamic-data token; the 3.16.1 trust gate is_content_request_supplied() only inspects $_POST['args']/$_GET['args'], never the $_POST['formData'] the public form-submit endpoint parses). This makes it possible for unauthenticated attackers to invoke arbitrary WordPress action hooks (multiple per request), causing state changes up to permanent, irreversible destruction of site content: a verified unauthenticated request permanently deleted trashed posts, pages, and comments via the core wp_scheduled_delete action. Other non-deny-listed hooks extend the impact to denial of service (e.g. wp_maybe_auto_update) and, where vulnerable third-party handlers are installed, further privileged writes. The same unauthenticated dynamic-data pipeline additionally exposes a blind arbitrary user/post-meta read; the read result is delivered only to the site owner and is not attacker-exfiltrable through the plugin's own email/response paths. Exploitation requires a published Avada form with AJAX submission and a notification whose email_message template includes an [all_fields] or explicit [field] placeholder - the default form configuration.

### CVE-2026-107645

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T04:18:10.090 |

The Blocksy Companion plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 2.1.58 This is due to the implement_user_registration() AJAX handler explicitly disabling Dokan's vendor-registration nonce check (via add_filter('dokan_register_nonce_check', '__return_false')) and then trusting an attacker-supplied $_POST['role'] value when invoking wc_create_new_customer() and wc_set_customer_auth_cookie(). This makes it possible for unauthenticated attackers to elevate their privileges to a Dokan 'seller' (vendor) account — including sites where the Dokan vendor signup is explicitly turned off — and to be auto-authenticated into that account, which grants publishing capabilities beyond those of a normal customer.

### CVE-2026-108269

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-09T22:16:59.793 |

Remote Attestation TLS Clients provides multi-language utilities for verifying attested TLS connections. Prior to 0.5.0, the Rust and Go RA-TLS challenge verifiers accepted quote ReportData that was bound to the certificate public key and client nonce but not to the active TLS session before permitting application traffic. An attacker who obtained an enclave TLS private key could relay a genuine quote onto another connection, causing the clients to accept an attacker-terminated connection as the attested enclave. This issue is fixed in 0.5.0.

### CVE-2026-108268

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-09T22:16:59.643 |

Enclave OS Virtual runs container workloads inside confidential virtual machines with end-to-end attestation. Prior to tdx-v0.2.43 and tdx-gpu-v0.6.27, the TDX/GPU RA-TLS certificate issuer placed the certificate public-key hash and client nonce in quote ReportData but omitted a value bound to the active TLS session. An attacker who obtained an enclave TLS private key could relay a genuine quote onto another connection, causing a relying party to accept an attacker-terminated connection as the attested enclave. This issue is fixed in tdx-v0.2.43 and tdx-gpu-v0.6.27.

### CVE-2026-108267

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-09T22:16:59.490 |

Privasys Go is a maintained fork of the Go programming language that adds RA-TLS support to crypto/tls. Prior to privasys-v0.5.1-go1.26.5, challenge-mode RA-TLS certificates bound quote ReportData to the certificate public key and client nonce but not to the active TLS session. An attacker who obtained an enclave TLS private key could relay a genuine quote onto another connection, causing a relying party to accept a handshake terminated by the attacker as an attested enclave connection. This issue is fixed in privasys-v0.5.1-go1.26.5.

### CVE-2026-108266

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-09T21:17:05.023 |

Privasys rustls is a maintained fork of the rustls TLS library that adds RA-TLS challenge and channel-binding support. Prior to privasys-v0.8.1, the fork emitted RA-TLS challenge certificates whose quote ReportData was bound to the certificate public key and client nonce but not to the active TLS session. An attacker who obtained an enclave TLS private key could relay a genuine quote onto another connection, causing a relying party to accept an attacker-terminated connection as the attested enclave. This issue is fixed in privasys-v0.8.1.

### CVE-2026-108265

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-09T21:17:04.870 |

Enclave OS Mini is a Rust-based runtime for confidential applications inside Intel SGX enclaves. Prior to wasm-v0.40.0, the SGX runtime's RA-TLS challenge certificate path placed the certificate public-key hash and client nonce in quote ReportData but omitted a value bound to the active TLS session. An attacker who obtained an enclave TLS private key could relay a genuine quote onto another connection, causing a relying party to accept an attacker-terminated connection as the attested enclave. This issue is fixed in wasm-v0.40.0.

### CVE-2026-108264

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-09T21:17:04.703 |

Wizarr is an advanced user invitation and management system for Jellyfin, Plex, Emby, and other media servers. Prior to 2026.9.1, wizard step Markdown supplied through the editor or imported bundles was evaluated by app/blueprints/wizard/routes.py in the application's non-sandboxed Jinja2 environment with application globals exposed. An authenticated user able to create steps, or an administrator importing an untrusted bundle through POST /settings/wizard/import, could execute arbitrary Python when GET /wizard/{server}/{idx} rendered the stored step; app/jinja_filters.py and app/services/wizard_widgets.py contained additional evaluation sinks. This could execute operating-system commands as the application user, disclose the Flask SECRET_KEY, access connected service credentials and the database, and produce stored cross-site scripting. This issue is fixed in 2026.9.1.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-105885

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T14:16:37.087 |

Deserialization of Untrusted Data vulnerability in 10Web Slider by 10Web slider-wd allows Object Injection.This issue affects Slider by 10Web: from n/a through 1.2.62.

### CVE-2026-87780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T06:16:43.667 |

The LTL Freight Quotes  WordPress plugin before 4.2.19 does not sanitise and escape values submitted through an unauthenticated endpoint before storing them and outputting them back in an administrative page, leading to Stored XSS which will execute in the session of any administrator viewing it.

### CVE-2026-83526

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T06:16:43.340 |

The FV Player 8 plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 8.1.7 via the check_mimetype function. This is due to insufficient file type validation in check_mimetype(), which writes attacker-supplied remote file content to the public uploads directory before any MIME or extension check, combined with a missing capability check on new player creation. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. This requires successfully exploiting a race condition.

### CVE-2026-77183

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T06:16:43.013 |

The FooSales – Point of Sale (POS) for WooCommerce plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 1.43.0. This is due to the plugin not properly validating a user's identity prior to updating their details like email. This makes it possible for authenticated attackers, with FooSales Cashier-level access and above, to change arbitrary user's email addresses, including administrators, and leverage that to reset the user's password and gain access to their account.

### CVE-2026-104766

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T06:16:40.007 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 5.7.3. This is due to the `OsSettingsController::update()` handler iterating over attacker-supplied `settings` parameters without an allowlist of permitted setting names or values, and `OsSettingsHelper::prepare_value()` performing no role allowlist validation before persisting the `default_wp_role_for_customer` setting — a restriction that exists only in the UI dropdown and is never enforced server-side. This makes it possible for authenticated attackers holding a LatePoint role with the `settings__edit` capability (such as an agent or custom role) to overwrite the default WordPress role for new customers with `administrator`, causing any subsequently self-registered LatePoint customer account to be created with full WordPress administrator privileges. Exploitation requires that a WordPress administrator has granted the `settings__edit` capability to a LatePoint agent or custom role, and that a new customer account is registered through LatePoint after the malicious setting change is persisted.

### CVE-2026-104725

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T06:16:38.920 |

The Groundhogg — CRM, Newsletters, and Marketing Automation plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.9 This is due to a missing ownership and capability check on the `user` parameter within the `process_edit()` function, which allows any authenticated user with the `edit_contacts` capability to reassign a contact record's linked WordPress user ID to any arbitrary account without requiring the `edit_users` or `promote_users` capabilities. This makes it possible for authenticated attackers, with sales_rep-level access and above, to escalate their privileges to administrator by linking a contact to an administrator's WordPress user ID, then creating a note containing the `{auto_login_link}` replacement tag to trigger generation of a valid auto-login permissions-key URL for the administrator-linked contact, and finally visiting that URL to authenticate as the targeted administrator. The auto-login URL is stored in the note content and is readable back by the attacker via the `view_notes` and `add_notes` capabilities that the sales_rep role holds by default.

### CVE-2026-104723

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T06:16:38.760 |

The LifterLMS – WP LMS for eLearning, Online Courses, & Quizzes plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 10.2.1 via deserialization of untrusted input . This makes it possible for authenticated attackers, with custom-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present. This vulnerability is only exploitable during lesson creation when a temporary lesson ID triggers the custom metadata path, and requires the attacker to hold a role with the edit_course capability, such as Instructor, Instructor's Assistant, LMS Manager, or Administrator.

### CVE-2026-55797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-09T17:16:47.710 |

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. From 2.11.0 until 3.3.15, 3.4.10, 3.5.4, and 3.6.0-rc2, the Argo CD repo-server is vulnerable to command injection when it clones, tests, or fetches an SSH Git repository configured with a proxy URL. The proxy host and port are embedded in an SSH ProxyCommand that is executed through a shell without neutralizing shell metacharacters. A user who can create or update a repository or repository credential template can supply a crafted proxy host to execute commands in the repo-server and access its Git, Helm, and OCI credentials. This issue is fixed in versions 3.3.15, 3.4.10, 3.5.4, and 3.6.0-rc2.

### CVE-2026-107813

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-09T16:17:26.007 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, the api/cluster router exposes node and namespace mutation operations and cluster-wide Nginx reload or restart operations with AuthRequired but without RequireSecureSession. An authenticated OTP-enabled user possessing a stolen or persisted JWT can therefore perform node CRUD, read or replace node credentials, change namespaces, and invoke nodes/reload_nginx or nodes/restart_nginx without a fresh second-factor step-up. This issue is an incomplete fix for CVE-2026-84315 and is fixed in version 2.5.0.

### CVE-2026-107811

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-10-09T16:17:25.690 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, ordinary authenticated users can access /api/nodes and /api/nodes/:id, whose responses serialize the node token field. The same token is accepted as X-Node-Secret by AuthRequired and maps the request to initUser, allowing the user to impersonate a trusted node against a reachable cluster member. This cross-node authentication bypass can expose sensitive management operations, including configuration synchronization and service restart. This issue is fixed in version 2.5.0.

### CVE-2026-107809

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-09T16:17:25.387 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, AuthRequired accepts a browser-managed token cookie as an API credential after the front end stores the JWT in that cookie. Because management endpoints do not universally require a CSRF token or perform Origin or Referer validation, a remote attacker can induce a logged-in administrator's browser to submit authenticated cross-site state-changing requests, including POST /api/configs. The attack requires an administrator account without OTP/Passkey or a target endpoint that does not require secure-session proof. The attacker cannot read the cross-origin response but can modify Nginx configuration, trigger reloads, or invoke other management operations reachable with the victim's session. This issue is fixed in version 2.5.0.

### CVE-2026-107807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312;CWE-598` |
| Published | 2026-10-09T16:17:25.087 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, Nginx UI accepts the Node.Secret master credential through the node_secret query parameter in HTTP and WebSocket authentication paths instead of requiring the X-Node-Secret header. The credential can consequently appear in access logs, proxy logs, browser history, Referer headers, configuration URLs, and deployment environment data. A party that obtains the secret can bypass normal password, JWT, session, and second-factor checks and obtain persistent administrative API access, including access to configuration and secret material. This issue is fixed in version 2.5.0.

### CVE-2026-108113

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-09T16:17:26.917 |

ILIAS before 9.24, 10.12, and 11.5 contains an unrestricted file upload vulnerability in QTI question import image handling (ilQtiMatImageSecurity) that allows authenticated authors to write executable files. Attackers with question pool import rights can import a crafted archive writing a .htaccess and PHP file to the web-served image directory, achieving remote code execution as the web server user.

### CVE-2026-104084

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-09T16:17:21.153 |

SmarterMail before build 9777 contains a privilege escalation vulnerability where JWT access and refresh tokens embed a role claim at issuance that is not revalidated against the account's current role when redeemed through POST /api/v1/auth/refresh-token. Attackers who capture a refresh token issued before an administrator demotion, or a demoted user whose session was not actively polling at the time of demotion, can replay the stale token to obtain a new access token retaining the higher-privilege role (such as DomainAdmin or SysAdmin) until natural token expiry.

### CVE-2026-108106

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-09T15:17:11.550 |

Xerial snappy-java before 1.1.10.9 contains an unbounded memory allocation vulnerability that allows attackers to exhaust JVM memory by declaring a large uncompressed length in compressed input. Attackers can supply a few crafted bytes to Snappy.uncompress, uncompressString, SnappyInputStream or SnappyFramedInputStream to force allocations up to 2 GB, causing OutOfMemoryError and denial of service.

### CVE-2026-87781

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T06:16:43.807 |

The LTL Freight Quotes  WordPress plugin before 4.2.19 does not sanitise and escape a parameter before using it in a SQL statement, leading to a SQL injection exploitable by unauthenticated users.

### CVE-2026-104082

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-09T16:17:20.833 |

SmarterMail before build 9777 contains a remote code execution vulnerability that allows an attacker holding a SysAdmin-scoped access token to bypass the Volume Mount script-directory containment control by provisioning a new mail domain with an arbitrary FileStore root path inside the trusted Scripts directory via the domain-put endpoint. Attackers can disclose the Scripts path through the AddOrUpdateMount endpoint, clear the upload extension blacklist via the global-mail endpoint, then upload a malicious script through the ordinary mail file-storage upload API so that saving a CommandMount triggers RunScript before validation, resulting in a reverse shell executing as the SmarterMail service account with SYSTEM-level privileges.

### CVE-2026-107815

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-09T17:16:45.970 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, the CONNECT engine's DOS table type used an incorrect boundary check that permitted a one-byte null write beyond a stack buffer at an attacker-controlled offset. An authenticated user able to use the CONNECT engine could cause a crash and potentially remote code execution. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-95702

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-10-09T15:17:20.447 |

Use-after-free vulnerability in VFS in Google gVisor prior to release 20260831.0 on all platforms allows a local attacker with standard container privileges to achieve code execution in the host sentry process by double-freeing the backing MemoryFile from an in-sandbox overlay filesystem. The sentry process remains confined by host-level Linux seccomp and namespace boundaries.

### CVE-2026-39453

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-09T15:17:14.500 |

Navigating to a certain URL on the switch’s web server causes the switch to reboot. This can be automated using a tool like curl to create DoS conditions where the switch constantly reboots.

### CVE-2026-101947

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-10T04:18:06.413 |

ExifTool for photo and video 5.0.1-gms by CellHubs constructs shell command strings from file paths and invokes /system/bin/sh -c. In the CSV-export path, the selected media path is merely surrounded with single quotes; embedded single quotes are not escaped.

### CVE-2026-107818

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-09T18:17:03.373 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, the mariadb.service unit used /run/mysqld/wsrep-new-cluster during the next service restart. A database user with FILE privilege and a secure-file-priv configuration permitting writes to /run/mysqld could create that file and inject attacker-controlled environment values into the restarted service. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-107814

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-09T16:17:26.150 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, MariaDB RPM packages created the dedicated mysql service account with the database data directory as its home directory. A database user with the FILE privilege could write startup dot-files such as .bash_profile into $HOME, and those files could execute when an administrator opened a login shell for the mysql account. Debian packages are not affected because they use /nonexistent as the account home. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-29797

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-09T15:17:13.843 |

No authentication is required when updating firmware or bootloader, making it easy for malicious files to be pushed to the device. Additionally, anyone with the same software can scan a network for N-Tron devices and push/pull firmware without authenticating by using SNMP/TFTP.

### CVE-2026-22061

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-215` |
| Published | 2026-10-09T23:16:54.157 |

Trident versions v25.02.1 through v26.06.1 are susceptible to a vulnerability that could allow an authenticated attacker with access to debug logs to view LUKS passphrases or SMB Active Directory credentials.

### CVE-2026-108259

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-09T21:17:04.017 |

Tina is a headless content management system. Prior to 3.0.0, @tinacms/cli reads Git branch values from VERCEL_GIT_COMMIT_REF, GITHUB_BRANCH, or HEAD, incorporates the raw value into the API URL, and interpolates that URL into JavaScript string literals in packages/@tinacms/cli/src/next/codegen/index.ts and packages/@tinacms/cli/src/next/codegen/codegen/plugin.ts. A crafted Git-valid branch name containing a quote can terminate the generated string and inject an expression that executes when the generated client module is imported during a preview build. The injected code runs with the build process privileges and can read environment credentials, modify deployment artifacts, or make network requests. This issue is fixed in version 3.0.0.

### CVE-2026-107837

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-09T18:17:05.483 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. In 2026.07 and earlier, _receive() in sys/net/gnrc/network_layer/sixlowpan/gnrc_sixlowpan.c can route an undersized packet into SFF fragment handling after only a minimal payload check. The code then interprets the packet as a sixlowpan_frag_t or larger fragment header without verifying that the packet snip contains the required bytes. A remote attacker can send a malformed 6LoWPAN fragment that causes gnrc_sixlowpan_frag_recv() to read beyond the packet buffer, potentially disclosing memory and crashing the network stack. No fixed repository release is available as of this review.

### CVE-2026-90983

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-603` |
| Published | 2026-10-09T16:17:31.947 |

Use of Client-Side authentication vulnerability in Hayat Health Facilities Inc. (Hayat Hospital) Hayat Mobile allows Authentication Bypass.

This issue affects Hayat Mobile: from 3.3.0 before 3.4.0.

### CVE-2026-102554

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502;CWE-770` |
| Published | 2026-10-09T16:17:20.410 |

Allocation of resources without limits or throttling (CWE-770) during Java object deserialization in Google Guava versions 4.0 through 33.7.1 allows an attacker to cause a Denial of Service via OutOfMemoryError. When deserializing CompactHashMap, CompactHashSet, or MapMakerInternalMap instances, Guava eagerly allocates an array based on a caller-specified size parameter without throttling, permitting memory exhaustion from crafted serialization streams.

### CVE-2026-108105

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-09T15:17:11.380 |

Open5GS through 2.8.0 contains a reachable assertion vulnerability in mme_gn_handle_sgsn_context_request() that allows remote unauthenticated attackers to crash the MME via malformed SGSN Address IEs. Attackers sending GTPv1-C traffic from a configured SGSN address with a known UE IMSI or P-TMSI can supply an invalid address length to terminate open5gs-mmed, denying service to all subscribers.

### CVE-2026-104759

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-10T08:17:04.070 |

The WPO365 | SEAMLESS WORDPRESS + MICROSOFT INTEGRATION (WPO365 | LOGIN) plugin for WordPress is vulnerable to Authentication Bypass via OIDC Nonce Replay in all versions up to, and including, 44.1 This is due to `Id_Token_Service_Deprecated::process_openidconnect_token()` using the incompatible WordPress core `wp_verify_nonce()` function to validate a nonce produced by `Nonce_Service::create_nonce()` — a 64-character hex value that `wp_verify_nonce()` can never successfully verify — causing the nonce check to silently fail without terminating authentication, so execution continues into `authenticate_oidc_user()` with the attacker-supplied `id_token`. This makes it possible for unauthenticated attackers who have obtained a previously-issued, valid `id_token` for a target account to replay that token and authenticate as any WordPress user, including administrators, resulting in full site takeover. This vulnerability is only exploitable when the `use_id_token_parser_v2` plugin option is enabled, as this is the configuration that routes token processing through the deprecated parser containing the broken nonce check.

### CVE-2026-94538

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T07:16:42.070 |

The WP File Download plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 6.3.9. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to permanently delete any file managed by WP File Download, empty the entire trash, move files between categories, and publish or unpublish arbitrary files.

### CVE-2026-94257

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T06:16:44.717 |

The SMS Alert  WordPress plugin before 4.0.1 does not bind the account whose password is being changed to the phone number that was actually verified during its OTP password reset, allowing unauthenticated attackers to set a new password on an arbitrary account, including an administrator, by verifying a one-time code sent to a phone number they control.

### CVE-2026-94256

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-10T06:16:44.590 |

The SMS Alert  WordPress plugin before 4.0.1 does not verify that the account being logged in is the one the verified one-time code belongs to, allowing unauthenticated attackers to sign in as any user with a stored phone number, including an administrator, by completing a code challenge on a phone they control.

### CVE-2026-92975

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-10T06:16:44.253 |

The Groundhogg — CRM, Newsletters, and Marketing Automation plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.8.3 via the `create_support_user()` function. This is due to the function identifying the support account solely by matching against publicly hardcoded constants — `user_login` `'groundhogg'` and email addresses `'support@groundhogg.io'` / `'help@groundhogg.io'` — where the `in_array()` email-equality check at line 238 is not a security boundary because any user fully controls their own email value. This makes it possible for an attacker with an account whose `user_login` is `'groundhogg'` and whose `user_email` matches one of the hardcoded support constants to have that account silently promoted to administrator — and additionally to super admin on multisite when the triggering administrator holds `manage_network_options` — resulting in full site takeover. Exploitation requires a two-actor flow: the attacker must first obtain or pre-plant an account with the hardcoded credentials (possible when open user registration is enabled or another account-creation path exists), after which a legitimate administrator must invoke the support-access feature via the `submit_ticket` or `process_send_support_access` entry points to trigger the promotion.

### CVE-2026-104899

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-10T06:16:40.160 |

The GeoDirectory – WP Business Directory Plugin and Classified Listings Directory plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 2.8.187 via the 'design_type' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. The required nonce is trivially obtainable by any anonymous visitor, as the geodir_basic_nonce value is localized to every public frontend page via the geodir_params script object, meaning no authentication, user interaction, or specific site content is required to exploit this vulnerability.

### CVE-2026-104797

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-10T04:18:08.677 |

The Advanced Form Integration — Connect Forms to 300+ Apps plugin for WordPress is vulnerable to Authentication Bypass via Unverified Password Change in all versions up to, and including, 2.9.0 The `adfoin_ultimatememberac_send_data` function, which powers the Ultimate Member "Update Profile Field" action, resolves the target WordPress user from an attacker-supplied email address and passes an attacker-controlled field key and value directly to `UM()->user()->update_profile()` in the `account` context — which explicitly bypasses Ultimate Member's banned-key validation — without performing any submitter identity verification, ownership check, capability check, current-password reauthentication, or restriction on sensitive keys such as `user_pass`. This makes it possible for unauthenticated attackers to change the password of any WordPress user account, including Administrator accounts, by submitting a public Contact Form 7 form with a target email and `user_pass` as the field key, enabling full site takeover. Exploitation requires an administrator to have pre-configured a Contact Form 7 integration that maps the target email, field key, and value from public form inputs to the Ultimate Member Update Profile Field action — the exact workflow the plugin's own UI advertises for this action type.

### CVE-2026-62376

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312;CWE-916` |
| Published | 2026-10-09T21:17:05.627 |

Vikunja is an open-source self-hosted task management platform. Versions prior to 2.4.0 store password-reset, email-confirmation, and account-deletion tokens in the `user_tokens` table in plaintext. If an attacker gains read access to the database through a backup leak, misconfigured storage, or SQL-level exposure, they can immediately use pending tokens to take over user accounts without knowing passwords. Version 2.4.0 fixes the issue.

### CVE-2026-57458

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-09T21:17:05.190 |

Vikunja is an open-source self-hosted task management platform. In version 2.3.0, a scoped API token limited to the `oauth.authorize` permission can call `POST /api/v1/oauth/authorize`, obtain an OAuth authorization code, and exchange the code at `POST /api/v1/oauth/token` for a normal bearer JSON Web Token (JWT) and refresh token. The resulting credentials are not restricted by the original API token's permissions, allowing access to routes outside its declared scope for the same user. Version 2.4.0 fixes the vulnerability.

### CVE-2026-107810

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-61` |
| Published | 2026-10-09T16:17:25.540 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, internal/backup/restore.go extracts inner archives before applying the restore_nginx and restore_nginx_ui flags and permits symlinks targeting the live Nginx configuration path. An authenticated user who can create and restore backups can craft a valid backup that places a symlink in the staging tree and then writes a regular file through that link, even when both restore flags are false. This can persistently inject configuration or cause denial of service when the modified files are later consumed. This issue is fixed in version 2.5.0.

### CVE-2026-107808

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-305;CWE-308` |
| Published | 2026-10-09T16:17:25.237 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, POST /api/login checks EnabledOTP but does not require a WebAuthn assertion when EnabledPasskey is true and no TOTP secret is configured. A passkey-only account is therefore issued a session after password verification, despite Enabled2FA reporting that the account has a second factor. An attacker who obtains the password can take over the account and reach administrative functionality without the registered passkey. This issue is fixed in version 2.5.0.

### CVE-2026-107821

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1285` |
| Published | 2026-10-09T18:17:03.860 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, MariaDB insufficiently validated counts, offsets, lengths, and field boundaries in FRM metadata while opening binary FRM files. An attacker able to place a crafted FRM file in the data directory could trigger out-of-bounds reads or writes, crash the server, or potentially execute code. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-92705

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-158;CWE-829` |
| Published | 2026-10-09T21:17:06.360 |

Aegisub is a cross-platform advanced subtitle editor. From 3.2.0 to 3.4.2, Aegisub automatically loads Automation scripts referenced by `Automation Scripts` metadata in `ASS` subtitle projects without asking whether the user trusts the scripts or their authors. An attacker can distribute a crafted `ASS` file together with a referenced malicious Automation script, and opening the `AS`  file executes arbitrary code with the privileges of the Aegisub process. From 3.4.0 to 3.4.2, inconsistent handling of embedded `NUL` characters between extension validation and filesystem operations additionally allows a crafted `ASS/Lua` polyglot to reference and execute itself as a single-file variant. The vulnerability is fixed in Aegisub 3.5.0.

### CVE-2026-108161

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-10T14:16:37.223 |

FusionPBX through 5.6.5 contains an OS command injection vulnerability in call_recordings::download() that allows unauthenticated attackers to execute commands by placing calls with malicious caller ID values. When the record_name filename template is enabled, attackers can embed shell metacharacters like $(...) in the Caller-ID name or number, executing commands as the web server user once a privileged user downloads multiple recordings as a ZIP.

### CVE-2026-108160

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-09T17:16:47.180 |

AstronRPA through 1.1.6 contains a download of code without integrity check vulnerability that allows network attackers to deliver malicious updates by abusing the desktop client's auto-update mechanism. Attackers positioned between the client and server can serve a malicious update manifest and NSIS installer, which electron-updater installs without signature verification, executing code as the desktop user.

### CVE-2026-108159

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-09T17:16:47.027 |

AstronRPA through 1.1.6 contains a cross-site scripting vulnerability in the desktop client's smart-component chat that allows remote attackers to execute OS commands by abusing unsanitized LLM output rendered via v-html. Attackers can embed prompt-injection content in a web page so the model emits HTML event handlers invoking the unrestricted open-path IPC handler with shell metacharacters, executing commands as the desktop user.

### CVE-2026-108101

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-09T15:17:10.667 |

HortusFox (hortusfox-web) through 6.3 contains an unrestricted file upload vulnerability in PlantAttachmentModel that allows authenticated users to store files with client-supplied extensions under public/attachments/. Attackers can upload HTML or SVG files via /plants/attachments/add for stored cross-site scripting, or PHP files where .htaccess is unenforced to execute code.

### CVE-2026-108260

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-83` |
| Published | 2026-10-09T21:17:04.180 |

Tina is a headless content management system. Prior to 0.2.1, the tina-markdown element in packages/@tinacms/web-components/src/tina-markdown.js assigns a rich-text node.url value directly to an anchor href without validating the URL scheme. A content author can store a link using a script-capable scheme, and a visitor who clicks the rendered link executes attacker-controlled script in the site's origin. The script can access same-origin application data and, when the visitor is an editor or administrator, may expose credentials stored by the TinaCMS admin on that origin. This issue is fixed in version 0.2.1.

### CVE-2026-108110

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-09T16:17:26.440 |

MOVO through 0.2.3 contains an authorization bypass vulnerability in the chat-api document endpoints that allows authenticated users to access other users' stored objects by supplying arbitrary object paths. Attackers who know a target's object path can send it to /api/documents/fetch or /api/documents/save-blueprint to read private documents and overwrite presentation blueprints.

### CVE-2026-91136

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-10T09:16:39.360 |

The Divi Plus plugin for WordPress is vulnerable to Arbitrary File Read in versions up to, and including, 2.4.0 via the 'svg_image' parameter of the /wp-json/elicus/v1/dipl-modules/svg-animator REST endpoint. This is due to the endpoint's permission callback (SVGAnimatorController::index_permission) returning true unconditionally combined with insufficient validation of the 'svg_image' input — sanitize_text_field() and esc_html() do not restrict filesystem paths, the file:// stream wrapper, or arbitrary URLs — before it is passed to file_get_contents() (with a wp_remote_get() fallback) and the raw response body is returned in the JSON 'html' field. This makes it possible for unauthenticated attackers to read arbitrary files on the affected site's server which may make remote code execution possible.

### CVE-2026-96662

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-10T08:17:08.033 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to generic SQL Injection via 'booking[service_id]' Parameter in all versions up to, and including, 5.7.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-93950

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T08:17:07.307 |

Missing Authorization vulnerability in StylemixThemes Motors motors allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Motors: from n/a through 1.4.108.

### CVE-2026-93746

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-10T08:17:04.907 |

The WebToffee WooCommerce PDF Invoices, Packing Slips, Delivery Notes & Shipping Labels plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 5.0.2 via the 'email' parameter of the guest print_document_from_the_mail_link handler dispatched from print_window() on init. This is due to the handler authorizing access to an order's printable documents when the attacker-supplied (base64-encoded) 'email' equals the order's billing email — a non-secret identifier — instead of requiring the WooCommerce order_key. This makes it possible for unauthenticated attackers, when the site is configured to allow guest access to documents ('wt_pklist_print_button_access_for' != 'logged_in'), to retrieve any other customer's invoice, packing slip, delivery note, dispatch label or shipping label — including customer name, billing/shipping address, phone number, purchased products, prices, taxes and invoice metadata — by knowing the target order ID and the associated billing email address.

### CVE-2026-89301

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-10T05:16:40.403 |

The rtMedia for WordPress, BuddyPress and bbPress plugin for WordPress is vulnerable to limited file deletion due to insufficient file path validation in the process function in all versions up to, and including, 4.7.13 This makes it possible for unauthenticated attackers to delete arbitrary safe files on the server.. The public nonce (rtmedia_upload_nonce) is emitted into frontend JavaScript on any page rendering the rtMedia gallery or upload shortcode, making it retrievable by unauthenticated visitors without any prior authentication or privileged action.

### CVE-2026-62367

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-290;CWE-345` |
| Published | 2026-10-09T21:17:05.470 |

Vikunja is an open-source self-hosted task management platform. In versions 1.0.0 through 2.3.0, when an administrator enables the per-provider `emailfallback` option on an OpenID Connect provider, Vikunja links an SSO login to a pre-existing local (username+password) account using only the `email` claim from the IdP. The fallback never checks an `email_verified` (or Microsoft `xms_edov`) signal and never requires the matched account's password. An attacker who can obtain a token from the configured issuer carrying a victim's email logs in as that victim with a full session, with no consent or interaction from the victim. Version 2.4.0 fixes the issue.

### CVE-2026-75351

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-09T19:16:42.047 |

OpENer v2.3/commit 76b95cf, contains an out-of-bounds read in the server-side EtherNet/IP ForwardOpen connection-path parser. This allows a remote attacker to cause a denial of service.

### CVE-2026-75350

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-09T18:17:14.037 |

EIPStackGroup OpENer v2.3 / master commit 76b95cf contains a buffer overflow in the GetAttributeList() implementation for the EtherNet/IP Get_Attribute_List service. This allows a remote attacker to cause a denial of service

### CVE-2026-107840

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-09T18:17:05.953 |

yopass is a service for securely sharing secrets, passwords, and files. Prior to version 14.7.0, the Prometheus metrics middleware in pkg/server/server.go uses the attacker-controlled r.Method value directly as the method label for yopass_http_requests_total and yopass_http_request_duration_seconds. Because the catch-all route accepts arbitrary HTTP method tokens, an unauthenticated remote attacker can submit many unique methods and create metric series that the Prometheus registry never evicts. The resulting monotonic memory growth can OOM-kill the process, while the expanding registry also degrades /metrics scrape latency and can blind monitoring. This issue is fixed in version 14.7.0.

### CVE-2026-107839

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-09T18:17:05.797 |

ageLANServer provides a cross-platform web server and launcher for offline multiplayer in several Age of Empires and Age of Mythology games. Prior to version 1.15.2, the AoE3 POST /game/cloud/getFileURL handler in the bundled game server has no request body size limit or cap on the attacker-controlled JSON names array and allocates response storage directly from the unbounded array length. A remote unauthenticated client can use the default self-registration flow and send an oversized request that causes excessive memory allocation, crashes or hangs the server process, disconnects active players, and keeps the service unavailable until it is restarted. This issue is fixed in version 1.15.2.

### CVE-2026-107838

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-252;CWE-617` |
| Published | 2026-10-09T18:17:05.640 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. From version 2023.07 through version 2026.07, nanocoap_fileserver callers in sys/net/application_layer/nanocoap/fileserver.c ignore a failure returned by _resp_init() when coap_build_reply() cannot fit a response header into the response buffer. A remote client can send a CoAP request with a sufficiently large extended token when nanocoap_token_ext is enabled, causing response initialization to fail while _get_file() or _get_directory() continues with stale response state. The path then reaches _calc_szx2() and its pdu->payload_len > reserve assertion, terminating the affected service or device task. No fixed release is available as of this review.

### CVE-2026-107826

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-09T18:17:04.673 |

OWASP Coraza WAF is a golang modsecurity compatible web application firewall library. From 3.0.0 until 3.8.1, readJSON in internal/bodyprocessors/json.go can stop its bounded flattening walk after reaching SecArgumentsLimit or the byte budget and then call gjson.Valid on the complete raw body. An unauthenticated attacker can submit shallow values followed by an extremely deeply nested JSON tail that was not visited by the bounded walk, causing gjson.Valid to recurse without a depth bound and terminate the hosting process with an unrecoverable fatal stack overflow. The ProcessRequest and ProcessResponse JSON paths share the affected readJSON validation flow, and the payload can remain within recommended body-size and argument-count limits. This issue is fixed in version 3.8.1.

### CVE-2026-75347

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-09T17:16:48.403 |

EIPStackGroup OpENer v2.3 and master up to commit 76b95cf contain an expired pointer dereference vulnerability in the EtherNet/IP Common Packet Format (CPF) handling logic. This allows a remote attacker to cause a denial of service.

### CVE-2026-75349

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-09T16:17:29.877 |

EIPStackGroup OpENer v2.3.0/master up to commit 76b95cf contains an out-of-bounds read vulnerability in Connection Manager request parsing. This allows a remote attacker to cause a denial of service.

### CVE-2026-75348

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-09T16:17:29.730 |

An out-of-bounds read vulnerability exists in EIPStackGroup OpENer v2.3 and master up to commit 76b95cf in the EtherNet/IP TCP SendRRData Common Packet Format parser. The issue occurs in CreateCommonPacketFormatStructure() when it parses recognized optional socket address information items of type 0x8000 or 0x8001 without first validating that the remaining CPF buffer contains the complete fixed sockaddr structure. This allows a remote attacker to cause a denial of service.

### CVE-2026-75346

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-09T16:17:29.590 |

An out-of-bounds read vulnerability exists in EIPStackGroup OpENer v2.3 and master through commit 76b95cf in the server-side CIP SetAttributeList service. This allows a remote attacker to cause a denial of service

### CVE-2026-75345

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-09T16:17:29.430 |

OpENer v2.3.0 / commit 76b95cf contains an out-of-bounds read in the unconnected explicit messaging path. This allows a remote attacker to cause a denial of service.

### CVE-2026-107812

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-09T16:17:25.847 |

Nginx UI is a web user interface for the Nginx web server. From 2.0.0 until 2.5.0, the self-upgrade mechanism validates a downloaded binary only with a same-origin digest obtained from the same upgrade mirror. A compromised mirror or network attacker able to alter both responses can supply a malicious executable and matching digest. An operator-triggered upgrade is required, and the application installs and runs the attacker-controlled code in the Nginx UI process context on the next upgrade. This issue is fixed in version 2.5.0.

### CVE-2026-78795

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-09T15:17:15.810 |

An issue in Netcore B11 Enterprise-level full Gigabit 9-port shop wireless router v1.3.241114.024540 and before allows a remote attacker to obtain sensitive information

### CVE-2026-107805

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-09T15:17:09.960 |

Nginx UI is a web user interface for the Nginx web server. From 2.5.0 until 2.6.0, the node-signature authentication path performs temporary file staging of an attacker-controlled request body and synchronizes it before validating the body digest and cryptographic signature. An unauthenticated remote client that can reach the API and provide syntactically valid signature metadata can consume temporary filesystem capacity, disk input and output, and request-processing resources before rejection. The issue affects availability and does not bypass authentication or provide confidentiality or integrity impact. This issue is fixed in version 2.6.0.

### CVE-2026-94676

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T14:16:38.130 |

Deserialization of Untrusted Data vulnerability in Tainacan Community Tainacan tainacan allows Object Injection.This issue affects Tainacan: from n/a through 1.3.0.

### CVE-2026-107657

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T09:16:38.940 |

The HivePress – Business Directory, Listings & Classified Ads Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the '<custom user attribute field name, e.g. profile_test>' parameter in all versions up to, and including, 1.7.31 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires an administrator to have configured a text-type custom user attribute whose display format places %value% inside an HTML attribute context (e.g., the documented pattern &lt;a href="%value%"&gt;Custom link&lt;/a&gt;), and for front-end user profiles to be enabled — both of which reflect the plugin's standard, documented configuration.

### CVE-2026-96765

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:08.170 |

The WPO365 | SEAMLESS WORDPRESS + MICROSOFT INTEGRATION (WPO365 | LOGIN) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'id_token' parameter in all versions up to, and including, 44.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is stored in the wpo365_errors transient for up to three days by submitting a crafted unauthenticated request with a forged id_token whose base64url-decoded unique_name or iss claim contains malicious HTML, requiring no prior authentication or user interaction beyond an administrator later visiting the WPO365 wizard page.

### CVE-2026-96278

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:07.567 |

The WP Photo Album Plus plugin for WordPress is vulnerable to Stored Cross-Site Scripting via REQUEST_URI Session History in all versions up to, and including, 9.3.03.002 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The bypass works because esc_url_raw() strips literal angle brackets but retains HTML entities, which wppaEntityDecode() silently converts back to live HTML tags before jQuery('#wppa-modal-container').html() renders them.

### CVE-2026-106606

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T08:17:04.353 |

Deserialization of Untrusted Data vulnerability in YITH YITH WooCommerce Affiliates yith-woocommerce-affiliates allows Object Injection.This issue affects YITH WooCommerce Affiliates: from n/a through 3.31.0.

### CVE-2026-101920

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:03.213 |

The Molongui Authorship – Author Boxes, Guest Authors & Co-Authors for WordPress plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'comment (href attribute inside comment content)' parameter in all versions up to, and including, 5.2.12 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable in the free build because the plugin's author-filter rewriter never appends the ?m_bm=true marker to its own anchors (Plugin::has_pro() returns false), meaning every href the byline script selects and rewrites is fully attacker-controlled.

### CVE-2026-100178

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:03.070 |

The WPAdverts – Classifieds Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'adverts_location' parameter in all versions up to, and including, 2.3.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-100147

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:02.930 |

The FunnelKit – Funnel Builder for WooCommerce Checkout plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'shipping_first_name' parameter in all versions up to, and including, 3.16.0.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-96840

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:42.767 |

The Post Grid Gutenberg Blocks – PostX plugin for WordPress is vulnerable to Stored Cross-Site Scripting via display_name User Field in all versions up to, and including, 5.1.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. WordPress core's pre_user_display_name filter encodes &, <, and > but leaves double-quotes intact (ENT_NOQUOTES), allowing a Subscriber-level user to store a double-quote in their display_name via /wp-admin/profile.php that subsequently breaks out of the alt="" attribute at Archive_Title.php:144.

### CVE-2026-96572

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:42.487 |

The WP Meteor Website Speed Optimization Addon plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Author Name in all versions up to, and including, 3.4.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is delivered via the comment author name field, which must clear WordPress's comment moderation workflow before being displayed, though this represents a display prerequisite rather than any sanitization control.

### CVE-2026-96558

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:42.343 |

The Quiz and Survey Master (QSM) – Quiz Maker & Survey Maker plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'qsm_hidden_questions' parameter in all versions up to, and including, 11.2.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the attacker to force the mlw_results INSERT to fail by submitting an over-length or duplicate qsm_unique_key value, which triggers the audit trail code branch that writes the unescaped payload to wp_mlw_qm_audit_trail.form_data.

### CVE-2026-95684

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:42.200 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'attachments[name]' Parameter in all versions up to, and including, 1.8.15 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-12626

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-10T07:16:41.230 |

The Online Scheduling and Appointment Booking System – Bookly plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 28.2 via deserialization of untrusted input via the ‘value’ parameter. This makes it possible for authenticated attackers, with custom-level access and above, to inject a PHP Object. No known gadget chain is available.

### CVE-2026-107742

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:40.843 |

The 10Web Booster – Website speed optimization, Cache & Page Speed optimizer plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'author' parameter in all versions up to, and including, 2.34.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable because a comment author Name value containing ' src=' and an event-handler payload contains no HTML tags or quote characters, allowing it to survive WordPress core's sanitize_text_field and land verbatim inside the alt attribute, where the plugin's own str_replace subsequently injects the single quote that breaks out of the attribute context.

### CVE-2026-100196

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:39.833 |

The LazyLoad Plugin – Lazy Load Images, Videos, and Iframes plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment_content (rendered inline into the page HTML)' parameter in all versions up to, and including, 2.4.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. WordPress core's wp_kses_data allow-list does not strip the crafted payload on save because it uses only permitted tags and attributes; the event handler is concealed inside a broken attribute region and is only promoted to a real DOM attribute by the plugin's render-time str_replace transformation. Additionally, a site administrator must approve the crafted comment before the payload is served to other visitors.

### CVE-2026-100161

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T07:16:38.767 |

The Photo Reviews for WooCommerce plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'wcpr_image_upload_id' parameter in all versions up to, and including, 1.2.30 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The publicly-emitted `wcpr_image_upload` nonce printed on every product review form is the only gate, and no capability, authentication, or attachment ownership check is performed, allowing the payload to be stored in comment meta — which is not subject to `wp_kses` — by any unauthenticated visitor; the XSS fires once the review is visible on the frontend.

### CVE-2026-96682

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T06:16:45.387 |

The Presto Player plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via <presto-player> Tag in all versions up to, and including, 4.5.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires an initial comment approval, though WordPress default settings will auto-approve all subsequent comments from the same author, allowing a patient unauthenticated attacker to land the payload without further admin intervention.

### CVE-2026-96667

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T06:16:45.230 |

The Real Estate Manager – Property Listing and Agent Management plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'first_name' parameter in all versions up to, and including, 7.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The reCAPTCHA check is trivially bypassed by omitting the g-recaptcha-response parameter entirely, since validation only runs when that parameter is present.

### CVE-2026-93775

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T06:16:44.417 |

The Podlove Podcast Publisher plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Auphonic Webhook in all versions up to, and including, 4.5.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injection is triggered by submitting a request to the Auphonic webhook endpoint with any POST body where the status_string field is not the literal string 'Done', causing the full raw POST superglobal to be stored in the plugin log before any authentication key validation is performed.

### CVE-2026-14335

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T06:16:41.447 |

The Easy Digital Downloads – eCommerce Payments and Subscriptions made easy plugin for WordPress is vulnerable to Stored Cross-Site Scripting via PayPal IPN Parameters in all versions up to, and including, 3.6.9 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-104752

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-10T06:16:39.383 |

The Rank Math SEO  WordPress plugin before 1.0.280 does not correctly validate the type of a file uploaded through its settings import feature, allowing users with administrator-level access to upload a PHP file and achieve remote code execution.

### CVE-2026-104021

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-10T05:16:39.503 |

The Fastcache by Host.it plugin for WordPress is vulnerable to Code Injection in all versions up to, and including, 1.7.4 via the `fastcache_settings[cache_cookie_exclude][]` parameter. This is due to the plugin registering the `cache_cookie_exclude` setting via `register_setting()` without a `sanitize_callback`, while `buildSiteHtaccessRules()` applies only `trim()` to each cookie value before interpolating it directly into an Apache `RewriteCond` line — a normalization that strips surrounding whitespace but leaves embedded newlines intact, allowing an attacker to break out of the capture group and append arbitrary directives. This makes it possible for authenticated attackers, with administrator-level access and above, to inject arbitrary Apache directives into the site's `.htaccess` file via `file_put_contents()`, enabling server-level configuration changes such as setting `php_value auto_prepend_file` to execute attacker-controlled PHP code on every request.

### CVE-2026-107823

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116;CWE-144` |
| Published | 2026-10-09T18:17:04.190 |

MariaDB server is a community developed fork of MySQL server. From 10.6.1 until 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, the MariaDB view FRM parser did not safely encode embedded newline characters in a username. An account with CREATE USER and CREATE VIEW WITH GRANT OPTION could create a crafted username containing additional view metadata, causing the parser to interpret part of the username as security metadata and potentially escalating database privileges. This issue is fixed in versions 10.6.28, 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-104081

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T15:17:06.940 |

KodExplorer before 4.55 contains a path traversal vulnerability in the unzip_pre_name() function within app/function/helper.function.php, where a single non-recursive str_replace() sanitization pass can be bypassed using crafted filenames like "....//", combined with PclZip's extract() call in KodArchive.class.php lacking the PCLZIP_OPT_EXTRACT_DIR_RESTRICTION option. Authenticated attackers can upload a malicious ZIP archive with traversal sequences to overwrite arbitrary files such as core JavaScript assets, enabling stored XSS that leads to admin account takeover and subsequent remote code execution via unrestricted PHP file upload.

### CVE-2026-97264

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T14:16:38.367 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Greg Winiarski WPAdverts wpadverts allows Reflected XSS.This issue affects WPAdverts: from n/a through 2.3.4.

### CVE-2026-97263

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T14:16:38.250 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Greg Winiarski WPAdverts wpadverts allows Stored XSS.This issue affects WPAdverts: from n/a through 2.3.4.

### CVE-2026-108164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-10T14:16:37.663 |

Open Source Social Network (OSSN) through 10.1 contains an insecure direct object reference vulnerability in components/OssnMessages/ossn_com.php that allows authenticated users to read other users' private message attachments. Attackers can request the /messages/attachment/{guid} route with sequential or guessed file GUIDs to retrieve attachments from private conversations without sender or recipient verification.

### CVE-2026-102388

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T14:16:36.167 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPMU DEV Forminator forminator allows Stored XSS.This issue affects Forminator: from n/a through 1.57.3.

### CVE-2026-93951

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-10T08:17:07.437 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Bracketweb Zeinet zeinet allows Reflected XSS.This issue affects Zeinet: from n/a through 1.0.0.

### CVE-2026-93949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-10T08:17:07.180 |

Authentication Bypass Using an Alternate Path or Channel vulnerability in Omegathemes Grocery Shopping Store grocery-shopping-store allows Password Recovery Exploitation.This issue affects Grocery Shopping Store: from n/a through 1.3.3.

### CVE-2026-107852

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-09T21:17:03.080 |

Jexactyl is a customisable game management panel and billing system. Prior to 4.0.5, the POST /api/client/billing/stripe/process endpoint accepts a client-supplied Stripe Checkout Session when payment_status is paid but does not compare amount_total or currency with the referenced order and configured billing currency. On an instance where the billing module is enabled and a Stripe secret key is configured, an authenticated client can therefore complete a lower-value or mismatched-currency payment and cause the order to be processed, provisioning, renewing, upgrading, or unsuspending the purchased server for less than the required price. This issue is fixed in version 4.0.5.

### CVE-2026-108096

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-09T18:17:06.410 |

Improper authorization in the query resolvers generated by @aws-amplify/graphql-index-transformer in AWS Amplify API Category before 3.1.2 might allow an authenticated remote user to read records owned by other users of the same application via crafted queries.



This issue has been addressed in @aws-amplify/graphql-index-transformer  3.1.2 https://www.npmjs.com/package/@aws-amplify/graphql-index-transformer/v/3.1.2  (included in @aws-amplify/data-construct  1.17.4 https://www.npmjs.com/package/@aws-amplify/data-construct/v/1.17.4  and @aws-amplify/graphql-api-construct  1.21.4 https://www.npmjs.com/package/@aws-amplify/graphql-api-construct/v/1.21.4 ). We recommend upgrading to the latest version ensuring any forked or derivative code is patched to incorporate the new fixes and then redeploying their backend.

### CVE-2026-107836

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-09T18:17:05.310 |

RIOT is an open-source microcontroller operating system designed for Internet of Things devices and other embedded systems. In 2026.07 and earlier, the nanoCoAP client function nanocoap_sock_get_slice() in sys/net/application_layer/nanocoap/sock.c accepts a Block2 response when _block_cb() sees the expected block number without also verifying that the server-controlled szx and derived offset match the requested block geometry. A malicious CoAP server can return the expected block number with a larger block size, causing the derived offset to exceed the client slice offset and making ctx->offset - offset underflow in _2buf_slice(). The resulting buffer-relative calculation can read before the payload buffer and crash the client, causing denial of service and potentially exposing adjacent memory. No fixed release is available as of this review.

### CVE-2026-108158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-09T17:16:46.870 |

plugNmeet Server through 2.5.2 contains a path traversal vulnerability in the whiteboard conversion endpoint that allows any meeting participant to read server files via crafted filePath values. Attackers can supply ../ sequences so text or office documents are converted into page images, then fetch them unauthenticated through /download/uploadedFile/.

### CVE-2026-108125

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T15:17:12.600 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in wp-post-author.

This issue affects wp-post-author version 4.0.0 prior to 4.1.0.

### CVE-2026-108108

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-09T15:17:11.887 |

PHPNuxBill through 2025.3.20 contains an authentication bypass vulnerability in RADIUS CHAP verification because Password::chap_verify() returns true when the supplied response does not match. Attackers who know a valid customer or PPPoE username can log in through MikroTik hotspot or PPPoE CHAP with any incorrect password to obtain network access and consume that customer's plan.

### CVE-2026-108100

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-09T15:17:10.443 |

HortusFox (hortusfox-web) before 6.2 contains an SQL injection vulnerability that allows API token holders to inject SQL by supplying crafted include_info values to the /api/locations/list endpoint. Attackers can place subqueries in include_info, which PlantsModel::getSpecificInfo() concatenates into the column list, to read any database table including user password hashes.
