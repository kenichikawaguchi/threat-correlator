# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-18 15:00 UTC
- **対象期間**: `2026-10-17T15:01:25.000Z` 〜 `2026-10-18T15:00:30.000Z`
- **重要CVE数**: 55 件（Critical 9.0+: 6 件 / High 7.0〜: 49 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **リモートからのコード実行／権限昇格** を可能にする深刻な脆弱性で、CVSS が 9.0 以上のものが目立ちます。  
- 攻撃手法は **デシリアライズ、デフォルト認証情報、SQL インジェクション、認証バイパス** と多様化しており、特に Web アプリケーションプラグインやマイクロサービス基盤での実装ミスが原因です。  
- 多くは **認証不要（PR:N）** か **低い権限での実行（PR:L）** で成立し、攻撃者はネットワーク上から直接悪用できる点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品・バージョン | 主な脆弱性種別 | 重大度 (CVSS) | 注目理由・影響範囲 |
|-----|----------------|----------------|--------------|-------------------|
| **CVE‑2026‑110886** | QuantumCloud *Conversational Forms* (≤ 1.5.1) | **デシリアライズによるオブジェクトインジェクション** | 9.8 | 任意オブジェクトをサーバ側で生成でき、リモートコード実行 (RCE) が可能。チャットボットを導入している全サイトが対象。 |
| **CVE‑2026‑110372** | Brainstorm Force *OttoKit* (≤ 1.1.40) | **不適切な権限付与 → 権限昇格** | 9.8 | 権限のないユーザーが管理者権限を取得でき、サイト全体の改ざん・情報漏洩リスクが高い。 |
| **CVE‑2026‑111998** | *Vanus* (0.8.0 – 0.9.0) | **ハードコードされた管理トークン** | 9.3 | 認証なしでクラスタ管理権限 (cluster‑admin) を取得でき、全リソースの作成・削除が可能。K8s 環境で広範に展開されている可能性。 |
| **CVE‑2026‑109894** | Arraytics *Booktics* (≤ 1.0.29) | **SQL インジェクション** | 9.3 | 任意 SQL が実行でき、データベースの情報漏洩・改ざん・破壊が可能。特に書籍管理システムは内部データが機密情報になるケースが多い。 |
| **CVE‑2026‑111911** | phpMyFAQ 4.0.0 – 4.1.8 | **WebAuthn 認証バイパス** | 9.3 | 認証なしで任意アカウントにパスキーを登録でき、以後のログインが完全に乗っ取られる。FAQ システムは多数の顧客向けサイトで利用されるため影響が広範。 |

> **補足**：上記以外にも *WhoDB* のパストラバーサル (CVE‑2026‑112005) や *FreeRDP* のヒープ書き込み (CVE‑2026‑111880) など、インフラ層での深刻な脆弱性が散見されます。  

---

## 3. 推奨アクション  

### 3‑1. 速やかなパッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン | 対応手順 |
|------|-------------------|----------------|----------|
| **QuantumCloud Conversational Forms** | ≤ 1.5.1 | **≥ 1.5.2** | `composer update` / プラグイン管理画面から最新版へ更新 |
| **Brainstorm Force OttoKit** | ≤ 1.1.40 | **≥ 1.1.41** | WordPress 管理画面 → プラグイン更新、または `wp plugin update otto-kit` |
| **Vanus** | 0.8.0 – 0.9.0 | **≥ 0.9.1** | `helm upgrade vanus vanus/vanus --set image.tag=0.9.1` など、公式 Helm チャートでアップグレード |
| **Arraytics Booktics** | ≤ 1.0.29 | **≥ 1.0.30** | `npm install booktics@latest`（Node.js 環境）または Docker イメージの再ビルド |
| **phpMyFAQ** | 4.0.0 – 4.1.8 | **≥ 4.1.9** (または 4.2.0‑beta) | `composer require phpmyfaq/phpmyfaq:^4.1.9`、または公式リリースの zip を展開 |

### 3‑2. 追加的な防御策
- **デシリアライズ対策**：受信データのシリアライズ形式を限定し、`unserialize()` 系関数の使用を避けるか、`allowed_classes` オプションで許可クラスを絞る。  
- **認証情報管理**：デフォルトトークンやハードコードされたシークレットは **絶対にリポジトリに残さない**。環境変数やシークレットマネージャーで管理し、デプロイ時に注入。  
- **入力検証・エスケープ**：SQL インジェクション対策として、プリペアドステートメント／ORM の利用を徹底し、すべての外部入力をサニタイズ。  
- **WebAuthn / SSO の実装見直し**：登録フローで必ずユーザー認証・チャレンジ検証を行い、`fmt=none` のようなスキップ可能なパラメータを受け付けない。  
- **監査ログの強化**：特権操作（例：トークン発行、権限変更）を行うエンドポイントは **詳細ログ** を残し、SIEM で異常検知を設定。  

### 3‑3. 緊急時のインシデント対応
1. **影響範囲の特定**：該当プラグイン/サービスが稼働している全サーバをリスト化。  
2. **一時的な遮断**：可能であれば該当エンドポイントをファイアウォールで遮断し、攻撃者のアクセスをブロック。  
3. **証跡取得**：ログ（アクセスログ、認証ログ）を保存し、フォレンジック解析に備える。  
4. **パッチ適用後の検証**：アップデート後に脆弱性スキャナ（例：Nessus、OpenVAS）で再スキャンし

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-110886

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-18T11:16:37.450 |

Deserialization of Untrusted Data vulnerability in QuantumCloud Conversational Forms for ChatBot conversational-forms allows Object Injection.This issue affects Conversational Forms for ChatBot: from n/a through 1.5.1.

### CVE-2026-110372

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-18T11:16:36.580 |

Incorrect Privilege Assignment vulnerability in Brainstorm Force OttoKit suretriggers allows Privilege Escalation.This issue affects OttoKit: from n/a through 1.1.40.

### CVE-2026-111998

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-18T12:17:11.730 |

Vanus 0.8.0 through 0.9.0 contains a default credentials vulnerability that allows unauthenticated remote attackers to gain cluster-admin access by using the hardcoded admin token. Attackers can send the fixed Bearer token to the gateway gRPC proxy port to manage namespaces, eventbuses, users, tokens, and role bindings, and read or publish events.

### CVE-2026-109894

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-18T11:16:36.190 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Arraytics Booktics booktics allows SQL Injection.This issue affects Booktics: from n/a through 1.0.29.

### CVE-2026-111911

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-17T19:16:33.500 |

phpMyFAQ 4.0.0 before 4.1.9 contains an authentication bypass vulnerability where WebAuthn registration endpoints attach credentials to any account without authentication or challenge validation. Attackers can stage a victim username, submit a forged fmt=none attestation to register a passkey, then log in bypassing passwords and TOTP for account takeover.

### CVE-2026-112005

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-18T12:17:12.790 |

WhoDB 0.104.0 before 0.135.0 contains a path traversal vulnerability that allows remote attackers to read and write arbitrary host files by running DuckDB filesystem functions through the query editor. Attackers can log in to a DuckDB file without credentials and use read_text, read_blob, COPY ... TO or ATTACH to steal session.key and stored database credentials or overwrite files.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-107436

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-18T11:16:34.720 |

Deserialization of Untrusted Data vulnerability in WP Chill Strong Testimonials strong-testimonials allows Object Injection.This issue affects Strong Testimonials: from n/a through 3.3.12.

### CVE-2026-112021

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-18T12:17:15.200 |

snac2 before 2.93 contains a heap-based buffer overflow vulnerability in _xs_json_load_lexer() that allows unauthenticated remote attackers to corrupt heap memory by sending JSON strings containing a \u0000 escape. Attackers can send a single crafted application/activity+json POST to activitypub_post_handler(), which parses it before signature checks, overflowing heap allocations and crashing the server.

### CVE-2026-111999

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-18T12:17:11.870 |

Vanus 0.8.0 through 0.9.0 contains a missing authentication vulnerability that allows unauthenticated remote attackers to publish events to any eventbus through the gateway CloudEvents HTTP receiver. Attackers can send forged CloudEvents to the /namespaces/{ns}/eventbus/{name}/events or legacy /gateway/{name} paths, bypassing token authentication and authPublish checks, so they are stored and delivered to subscription sinks.

### CVE-2026-111927

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-17T19:16:35.527 |

Coder before 2.29.20, 2.33.0 before 2.33.12, 2.34.0 before 2.34.8, and 2.35.0 before 2.35.4 contains an improper hostname validation flaw in GetWorkspaceProxyByHostname whose SIMILAR TO pattern performs a prefix match, so any domain that is a string prefix of a workspace-proxy access URL is trusted as a proxy. Attackers owning such a domain can lure an authenticated victim to a crafted /api/v2/applications/auth-redirect link, capture the redirected application_connect API key, and replay it to access the victim's workspace apps.

### CVE-2026-111924

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-17T19:16:35.257 |

Fleet before 4.83.0 contains a denial of service vulnerability that allows unauthenticated attackers to exhaust server memory by sending gzip-compressed request bodies. Attackers can send small, highly compressed requests with Content-Encoding: gzip to unauthenticated endpoints that expand during decoding, crashing the entire Fleet instance.

### CVE-2026-111923

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-17T19:16:35.117 |

Fleet before 4.89.0 contains an unbounded recursion vulnerability in Apple MDM enrollment property list parsing that allows unauthenticated attackers to crash the server. Attackers can send a crafted binary plist payload of about 150 bytes to the enrollment endpoints, triggering exponential allocation or infinite recursion that exhausts CPU and memory.

### CVE-2026-111908

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-17T19:16:33.043 |

phpMyFAQ 4.0.0 before 4.1.9 and 4.2.0-alpha before 4.2.0-beta contains a broken object-level authorization vulnerability in the PUT /api/v3.1/faq/update endpoint, which checks only the global edit_faq permission and does not verify access to the target FAQ. Authenticated users with edit_faq permission can supply the ID of a restricted FAQ they cannot view to modify its content, bypass moderation, and change its publication state.

### CVE-2026-111901

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-17T19:16:31.953 |

phpMyFAQ 4.2.0-alpha before 4.2.0-beta contains an uncontrolled resource consumption vulnerability in the unauthenticated faqs and search API endpoints. Attackers can send concurrent GET requests that load and process all database records into PHP memory, exhausting CPU and memory to crash the server.

### CVE-2026-111884

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-308` |
| Published | 2026-10-17T19:16:29.450 |

phpMyFAQ before 4.1.9 and 4.2.0-alpha before 4.2.0-beta does not require the current password when changing an account e-mail in the user control panel (UserController::updateData, api/user/data/update), checking only the session and CSRF token. An attacker with a hijacked session can set the e-mail to their own mailbox and use the password-reset flow to take over non-2FA accounts, including superadmin.

### CVE-2026-112001

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-18T12:17:12.140 |

ProjectSend 2.0.0 before 2.7.0 contains an incorrect authorization vulnerability that allows restricted API token holders to change the token owner's credentials via PATCH /api/v1/users/{user}. Attackers with a token limited to manage_users and edit_users can set a new owner password, clear two-factor authentication, and sign in interactively with the owner's full role permissions.

### CVE-2026-111882

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-17T19:16:29.240 |

phpMyFAQ 3.2.0-alpha before 4.1.9 and 4.2.0-alpha before 4.2.0-beta contains an authentication bypass vulnerability that allows IdP-authenticated users to skip TOTP two-factor authentication through the Keycloak and Entra ID SSO callbacks. Attackers holding a valid or phished IdP identity linked to a 2FA-enabled account can complete the OIDC flow and obtain a fully authenticated session, including administrator accounts.

### CVE-2026-110895

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-18T11:16:37.577 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in DevItems Support Genix support-genix-lite allows SQL Injection.This issue affects Support Genix: from n/a through 1.4.54.

### CVE-2026-111893

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-17T19:16:30.860 |

phpMyFAQ 4.2.0-alpha before 4.2.0-beta contains a privilege escalation vulnerability in GroupController::saveCategoryRestrictions() that lets delegated administrators assign categories outside their own scope. Category-restricted administrators can POST to /admin/api/group/category-restrictions with out-of-scope or empty categoryIds to grant groups unrestricted category access.

### CVE-2026-112051

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-18T13:16:37.190 |

Xinference through 4.0.1 contains a path traversal vulnerability on Windows that allows unauthenticated attackers to write and delete arbitrary .json files via backslash sequences in model_name. Attackers can register a persisted custom model through POST /v1/model_registrations/{model_type} with names like ..\..\evil to overwrite configuration or data files writable by the Xinference process.

### CVE-2026-112006

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-18T12:17:12.927 |

OpenTelemetry opentelemetry-exporter-otlp-proto-http 1.5.0 before 1.45.0 contains an improper certificate validation vulnerability that disables TLS verification when OTEL_EXPORTER_OTLP_CERTIFICATE variables are empty strings. Man-in-the-middle attackers can impersonate the collector to read or alter exported traces, metrics, and logs, including authentication headers from OTEL_EXPORTER_OTLP_HEADERS.

### CVE-2026-111880

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-17T19:16:28.960 |

FreeRDP versions from 2.0.0 before 3.32.0 contain a heap out-of-bounds write in the server hash-callback NTLM path that fails to validate the MIC offset. Unauthenticated attackers can send a crafted AUTHENTICATE_MESSAGE with a backward session-key offset and MIC offset to write 16 zero bytes beyond the allocation.

### CVE-2026-110373

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-18T11:16:36.703 |

Incorrect Privilege Assignment vulnerability in Hamid Alinia Login with phone number login-with-phone-number allows Privilege Escalation.This issue affects Login with phone number: from n/a through 1.8.77.

### CVE-2026-112015

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-18T12:17:14.303 |

Omnigent 0.3.0 before 0.14.0 contains a path traversal vulnerability that allows authenticated users to escape the workspace by setting os_env.cwd on nested sub-agents. Attackers can upload a bundle whose sub-agent uses an absolute or parent-traversing working directory, bypassing root-only validation in bundles.py, to read and write host files as the runner user.

### CVE-2026-96534

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-18T07:16:53.680 |

The Modern Events Calendar Lite WordPress plugin before 7.37.0, Modern Event Calendar Pro WordPress plugin before 7.37.0 does not sanitise and escape a parameter before using it in a SQL statement, allowing authenticated users with minimal privileges (Subscriber and above) to perform SQL injection attacks.

### CVE-2026-111898

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-17T19:16:31.647 |

phpMyFAQ 4.2.0-alpha before 4.2.0-beta contains an authentication bypass vulnerability that allows Keycloak users to take over local accounts by matching preferred_username or email. Attackers controlling a Keycloak identity with a colliding username or unverified email can log in through /auth/keycloak/authorize to bind their subject and gain superadmin privileges.

### CVE-2026-112002

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-10-18T12:17:12.323 |

ProjectSend 2.5.0 before 2.7.0 contains an unverified password change vulnerability in PasswordController::update() that lets sessions of Social-provisioned accounts set local passwords without the current password. Attackers holding a stolen session cookie can send PUT /settings/password to create a durable local password, enroll their own second factor, and persistently take over the account.

### CVE-2026-111895

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-17T19:16:31.177 |

phpMyFAQ 3.2.0 before 4.0.0 and 4.0.2 before 4.2.0-beta contains an authentication bypass in its Microsoft Entra ID login flow, which links users by the mutable preferred_username claim and whose AuthEntraId::create() ignores the duplicate-login exception while continuing with the existing local account. Attackers controlling an Entra identity in the configured tenant with a matching preferred_username can take over that local account, including super-admin accounts.

### CVE-2026-110383

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-18T11:16:36.943 |

Authorization Bypass Through User-Controlled Key vulnerability in WP E-Signature Electronic Signature Add-on for Fluent Forms signature-fluent-contract-forms-add-on allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Electronic Signature Add-on for Fluent Forms: from n/a through 2.0.5.

### CVE-2026-112018

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-18T12:17:14.747 |

cgltf through 1.15 contains a heap out-of-bounds write vulnerability in cgltf_accessor_unpack_floats() that allows attackers to write outside the output buffer via unchecked sparse accessor indices. Attackers can supply a crafted glTF or GLB file with large sparse indices to corrupt heap memory, crash applications, and potentially execute code when cgltf_validate() is not called.

### CVE-2026-112000

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-18T12:17:12.007 |

Vanus 0.8.0 through 0.9.0 contains a missing authorization vulnerability in the gateway that allows any authenticated user to call Subscribe, Ack, and unregistered methods without permission checks. Attackers can supply another tenant's subscription ID to Subscribe to hijack it, read and acknowledge its events, starve the legitimate consumer, and enumerate cluster users via ListUser.

### CVE-2026-110031

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-18T07:16:52.077 |

The Salon Booking System  WordPress plugin before 10.31.11 does not prevent users holding its custom salon staff role from assigning arbitrary capabilities to other accounts when editing a customer, allowing them to escalate any account to administrator and take over the site.

### CVE-2026-111922

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-10-17T19:16:34.957 |

Vikunja from 2.2.0 before 2.7.0 contains a permissive CORS configuration that trusts every localhost and 127.0.0.1 port with credentials, even when service.publicurl is set. Attackers controlling a page on any localhost port can send a credentialed request to the token refresh endpoint and read the returned bearer JWT to take over the logged-in user's account.

### CVE-2026-111909

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-17T19:16:33.190 |

phpMyFAQ before 4.1.9 contains a missing authorization vulnerability in the deleteUser() API that allows authenticated non-superadmin users with delete_user permission to delete superadmin accounts. Attackers can send a DELETE request to /admin/api/user/delete with a superadmin's userId other than 1, removing administrative access and accountability.

### CVE-2026-111881

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-17T19:16:29.103 |

FreeRDP from 3.14.1 before 3.32.0 contains an integer underflow in the WinPR BMP writer, where a mismatched stride calculation passes SIZE_MAX - 3 to Stream_Zero for sub-byte images. A malicious RDP clipboard peer can return a crafted 1-bpp BMP processed by clipboard_synthesize_image_format_to_bmp for CF_DIB/CF_DIBV5, crashing the client or causing an out-of-bounds write.

### CVE-2026-112017

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-18T12:17:14.600 |

JeecgBoot before 3.9.5 contains an sql injection vulnerability that allows authenticated attackers to bypass the SqlInjectionUtil keyword blocklist by inserting newline characters into dictionary and online report SQL fragments. Attackers can send newline-separated payloads to endpoints like /sys/dict/getDictItems for boolean or time-based blind injection, extracting database contents including administrator password hashes from sys_user.

### CVE-2026-110897

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-18T11:16:37.697 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in IdeaBox Creations PowerPack Lite for Beaver Builder powerpack-addon-for-beaver-builder allows Stored XSS.This issue affects PowerPack Lite for Beaver Builder: from n/a through 1.3.1.

### CVE-2026-110382

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-18T11:16:36.827 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in NSquared Simply Schedule Appointments simply-schedule-appointments allows Stored XSS.This issue affects Simply Schedule Appointments: from n/a through 1.6.12.35.

### CVE-2026-109895

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-18T11:16:36.320 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Arraytics Booktics booktics allows DOM-Based XSS.This issue affects Booktics: from n/a through 1.0.29.

### CVE-2026-108485

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-18T11:16:36.047 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in ThemeGrill eStore estore allows Reflected XSS.This issue affects eStore: from n/a through 1.6.13.

### CVE-2026-110981

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-18T07:16:52.817 |

The WP Photo Album Plus WordPress plugin before 9.2.11.002 does not properly escape a category navigation value before reflecting it into a JavaScript event handler on its gallery breadcrumb links, allowing unauthenticated attackers to inject arbitrary script that executes in the browser of anyone who follows a crafted gallery link and clicks the breadcrumb, including a logged-in administrator.

### CVE-2026-111919

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-17T19:16:34.543 |

Vikunja 0.22.0 before 2.7.0 contains an improper access revocation vulnerability that allows removed collaborators to keep receiving project data through webhooks they created. Former collaborators keep receiving task titles and descriptions through their webhook, including content created after their access was revoked.

### CVE-2026-111917

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-17T19:16:34.263 |

Vikunja 2.3.0 before 2.7.0 contains an improper session validation vulnerability that allows attackers to keep WebSocket access after revocation because handleAuth never checks the JWT sid claim against the sessions table. Attackers holding a stolen access token can open or maintain connections to /api/v2/ws after session deletion or TOTP enrollment, continuing to receive the victim's notification.created pushes, including comment, task and project content.

### CVE-2026-111914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-17T19:16:33.963 |

Admidio from 5.0.11 before 5.0.16 contains a broken access control vulnerability in modules/inventory/inventory_data.php that allows authenticated users to bypass the inventory_module_enabled restriction. Attackers with any valid login can request the DataTables JSON feed to read every inventory item and keeper names, even when the module is disabled.

### CVE-2026-111912

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-17T19:16:33.687 |

Admidio from 5.0.0 before 5.0.16 contains an insecure direct object reference vulnerability in ForumService::saveTopic() that allows authenticated members to modify other users' forum topics. Attackers can replace the topic_uuid parameter in their own topic_save request, reusing their CSRF token, to overwrite the victim topic's title and first post.

### CVE-2026-111910

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-17T19:16:33.343 |

phpMyFAQ before 4.1.9 and 4.2.0-alpha before 4.2.0-beta contains an authorization bypass vulnerability in attachment.php that allows attackers to download attachments of restricted FAQs by bypassing per-record permission checks. Low-privileged users with the dlattachment right, or anonymous users when allowDownloadsForGuests is enabled, can request attachment IDs to retrieve confidential files from restricted FAQs.

### CVE-2026-111907

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-17T19:16:32.883 |

phpMyFAQ 4.0.0 before 4.1.9 contains a cross-site request forgery vulnerability in the POST /admin/api/update-database endpoint, which executes database migrations without validating a CSRF token. Attackers can lure a logged-in user with the CONFIGURATION_EDIT permission into submitting a crafted cross-site request, triggering migrations that may impact database integrity or availability.

### CVE-2026-111906

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-17T19:16:32.723 |

phpMyFAQ before 4.1.9 and 4.2.0-alpha before 4.2.0-beta contains a cross-site request forgery vulnerability in the Elasticsearch and OpenSearch administration API endpoints, which do not validate a CSRF token for the create, drop, and import actions. Attackers can lure a user with CONFIGURATION_EDIT permission to a malicious page that triggers these actions, deleting search indexes, forcing re-indexing, or exhausting resources.

### CVE-2026-111897

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-17T19:16:31.487 |

phpMyFAQ 4.2.0-alpha before 4.2.0-beta contains an authorization bypass vulnerability that allows category-restricted editors to manage attachments of FAQs outside their categories by supplying arbitrary record IDs. Attackers in medium permission mode can send upload or delete requests with a target record_id or attachment ID to tamper with or remove files on unauthorized FAQs.

### CVE-2026-111886

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-17T19:16:29.770 |

phpMyFAQ from 4.2.0-alpha.2 before 4.2.0-beta lacks brute-force lockout in the removeTwofactorConfig() 2FA removal endpoint, allowing authenticated attackers to guess TOTP codes without limit. Attackers holding a hijacked session and CSRF token can repeatedly POST guesses to /api/user/remove-twofactor to permanently disable the victim's 2FA.

### CVE-2026-109701

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-17T17:16:28.973 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in PAYCOMET PAYCOMET for WooCommerce paytpv-for-woocommerce allows Reflected XSS.This issue affects PAYCOMET for WooCommerce: from n/a through 5.45.

### CVE-2026-111905

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-17T19:16:32.563 |

phpMyFAQ 3.2.0 before 4.1.9 and 4.2.0-alpha before 4.2.0-beta contains an insecure direct object reference vulnerability in GET /admin/api/user/data/{userId}, which returns any user's full faquserdata row, including the live TOTP secret, without a SuperAdmin or protected-target check. Delegated administrators with user-management rights can read a SuperAdmin's TOTP secret and generate valid codes to bypass two-factor authentication.

### CVE-2026-111891

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-17T19:16:30.550 |

phpMyFAQ from 4.2.0-alpha.2 before 4.2.0-beta contains a privilege escalation vulnerability in the group permission API, whose updatePermissions and updateMembers endpoints check held rights without regard to language or category scope and write unrestricted group grants. Non-superadmin administrators holding GROUP_EDIT can grant a group a right they hold only in a narrow scope and self-join it via updateMembers, gaining unrestricted FAQ create, edit, and publish access across all languages and categories.

### CVE-2026-111890

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-17T19:16:30.393 |

phpMyFAQ from 4.2.0-alpha.2 before 4.2.0-beta contains a privilege escalation vulnerability in UserController::updateUserRights that drops per-right language restrictions when rights are re-granted. Administrators holding USER_EDIT can submit language-scoped rights to the update-rights API, including for themselves, to gain unrestricted FAQ create, edit, and publish access across all languages.

### CVE-2026-111885

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-10-17T19:16:29.610 |

phpMyFAQ from 4.2.0-alpha before 4.2.0-beta contains a missing authorization vulnerability in GroupController::deleteGroup() that omits privilege-level checks on target groups. Authenticated non-SuperAdmin administrators holding GROUP_DELETE can send a crafted groupId to /admin/api/group/delete to permanently destroy higher-privileged groups and strip members' inherited rights.
