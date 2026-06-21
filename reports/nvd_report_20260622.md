# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-21 15:00 UTC
- **対象期間**: `2026-06-20T19:01:13.000Z` 〜 `2026-06-21T15:00:32.000Z`
- **重要CVE数**: 25 件（Critical 9.0+: 4 件 / High 7.0〜: 21 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公表された CVE のうち **CVSS 7.0 以上が 20 件以上** と、深刻度の高い脆弱性が集中しています。  
- **認証バイパス／権限昇格** と **リモートコード実行 (RCE)** が目立ち、特に SaaS 型プラットフォームや AI 推論サーバーでの入力検証不備が原因です。  
- 多くは **パッケージメタデータや API のサニタイズ不足、ハードコードされたシークレット** が根本要因で、簡単なバージョンアップで対策可能なケースが多数です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・被害シナリオ | 推奨アップデート |
|-----|------|----------------|------------------------|-------------------|
| **CVE‑2026‑56397 / CVE‑2026‑56395** | 9.4 | **XSS → RCE** (SiYuan Bazaar マーケットプレイス) | パッケージメタデータ・README がサニタイズされず、悪意ある HTML/JS が埋め込める。Bazaar を閲覧した全ユーザーが任意コード実行可能。 | **SiYuan ≥ 3.6.1** (Marketplace のサニタイズ処理を追加) |
| **CVE‑2026‑56265** | 9.3 | **認証バイパス** (Crawl4AI Docker API) | デフォルトの JWT 署名鍵がハードコード。鍵を知っている攻撃者は任意トークンを生成し、Docker API の全機能に無制限アクセス。 | **Crawl4AI ≥ 0.8.7** (鍵のランダム生成・設定ファイル化) |
| **CVE‑2026‑56340** | 8.7 | **入力検証欠如 → RCE** (vLLM 0.10.2‑0.12.9) | マルチモーダル埋め込みでスパーステンソルのインデックス検証が無効。細工したリクエストでメモリ破壊・コード実行が可能。 | **vLLM ≥ 0.13.0** (スパーステンソル検証を強制) |
| **CVE‑2026‑56382** | 8.6 | **RCE** (Craft CMS 5.5.0‑5.9.13) | `FieldsController::actionRenderCardPreview()` が `fieldLayoutConfig` を無検証で `Fields::createLayout()` に渡す。任意 PHP コードが実行される。 | **Craft CMS ≥ 5.9.14** (パラメータのサニタイズと型チェック) |
| **CVE‑2026‑56396** | 8.7 | **権限昇格** (phpMyFAQ < 4.1.4) | `editUser()` / `updateUserRights()` が適切な権限チェックを行わず、管理者権限でも `is_superadmin` フラグを変更可能。 | **phpMyFAQ ≥ 4.1.4** (権限ロジックの修正) |

> **注記**  
> - 同一製品の重複 CVE（例: CVE‑2026‑56397 と CVE‑2026‑56395）は同一脆弱性の別報告です。最も新しい修正版を適用すれば両方解消します。  
> - Capgo 系列 (CVE‑2026‑56253,‑56242,‑56239,‑56251 など) は **認証情報漏洩・権限昇格** が多数報告されており、同様に **12.128.2 以降** のバージョンで対策が入っています。  

---

## 3. 推奨アクション  

### a. 直ちに実施すべきパッケージアップデート
| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン |
|-------------------|----------------------|-----------------|
| SiYuan (Bazaar) | < 3.6.1 | **≥ 3.6.1** |
| Crawl4AI | < 0.8.7 | **≥ 0.8.7** |
| vLLM | ≥ 0.10.2 & < 0.13.0 | **≥ 0.13.0** |
| Craft CMS | 5.5.0‑5.9.13 | **≥ 5.9.14** |
| phpMyFAQ | < 4.1.4 | **≥ 4.1.4** |
| Capgo | < 12.128.2 | **≥ 12.128.2** |
| AVideo | ≤ 29.0 (Meet/Payment plugins) | **≥ 30.0** (公式で修正リリース) |
| picklescan | < 0.0.30 | **≥ 0.0.30** (検知ロジック強化) |

### b. 環境別追加対策
| 項目 | 内容 |
|------|------|
| **JWT / シークレット管理** | デフォルト鍵が残っているコンテナイメージは全て削除し、`Crawl4AI` の `JWT_SECRET` をランダムに再生成。既存トークンは無効化。 |
| **Web アプリケーションファイアウォール (WAF)** | XSS・RCE 攻撃向けのシグネチャを追加。特に `SiYuan` の Bazaar、`Craft CMS` の `/fields/render-card-preview` エンドポイントを保護。 |
| **入力検証の強化** | カスタムコードで外部から受け取る JSON/YAML/HTML を必ずサニタイズ。スパーステンソルやマルチモーダル埋め込みはサイズ・インデックス範囲を検証。 |
| **権限・ロールの最小化** | `phpMyFAQ`、`Capgo`、`AVideo` などは **SuperAdmin** 権限を必要最小限のユーザーに限定し、`is_superadmin` フラグ変更 API を無効化または内部で二段階承認を導入。 |
| **監査ログの有効化** | 認証バイパスや権限変更が行われた際に即座にアラートを上げられるよう、`Crawl4AI`、`Capgo`、`phpMyFAQ` の監査ログをオンにする。 |
| **依存ライブラリの定期的なスキャン** | `picklescan` のようなサードパーティ検知ツールは **0.0.30 以降** を使用し、CI パイプラインで pickle ファイルの安全性を自動検証。 |

### c. 長期的なセキュリティ強化策
1. **脆弱性情報の自動取得** – NVD、GitHub Advisory Database、各ベンダーのセキュリティアドバイザリを RSS/Webhook で取得し、社内チケットシ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-56397

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-21T14:16:26.783 |

SiYuan before v3.6.1 fails to sanitize package metadata and README content in the Bazaar marketplace, allowing malicious package authors to inject arbitrary HTML and JavaScript. Attackers can achieve remote code execution on any user browsing the Bazaar by embedding XSS payloads in package displayName, description, or README fields, exploiting Electron's nodeIntegration setting to execute OS commands.

### CVE-2026-56395

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-21T14:16:26.530 |

SiYuan before v3.6.1 fails to sanitize package metadata and README content in the Bazaar marketplace, allowing malicious package authors to inject arbitrary HTML and JavaScript. Attackers can achieve remote code execution on any user browsing the Bazaar by embedding XSS payloads in package displayName, description, or README fields, exploiting Electron's nodeIntegration setting to execute OS commands.

### CVE-2026-56265

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-21T14:16:24.980 |

Crawl4AI before 0.8.7 contains an authentication bypass vulnerability due to a hardcoded default JWT signing key in the Docker API server. Attackers who know the default key can forge valid authentication tokens for any user, bypassing authentication and gaining full access to protected functionality.

### CVE-2026-56345

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-20T19:16:23.983 |

AVideo through 29.0 contains an authorization bypass vulnerability in the Meet plugin's uploadRecordedVideo.json.php endpoint that derives the target users_id from the uploaded filename without verification. An attacker with knowledge of the Meet shared secret can craft a malicious file upload with a filename containing an arbitrary users_id to invoke passwordless User->login() and establish an authenticated session as any user including admin. Attackers can obtain the Meet shared secret through path-traversal vulnerabilities or timing attacks against checkToken.json.php, then POST a crafted file to uploadRecordedVideo.json.php with a filename like '1-anything.mp4' to hijack admin sessions and gain full account takeover.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-56396

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-21T14:16:26.660 |

phpMyFAQ before 4.1.4 contains missing authorization vulnerabilities in editUser() and updateUserRights() endpoints that allow authenticated administrators to escalate privileges. Non-SuperAdmin users with edit_user permission can set is_superadmin flag or grant arbitrary rights to escalate to SuperAdmin access.

### CVE-2026-56253

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-21T14:16:24.850 |

Capgo before 12.128.2 contains an improper access control vulnerability in the public.get_org_members RPC function that allows unauthenticated attackers to enumerate organization members. Attackers can invoke the endpoint using only the public sb_publishable_* key and an organization UUID to retrieve sensitive member information including email addresses, user IDs, roles, and pending invitations.

### CVE-2026-56242

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-21T14:16:24.583 |

Capgo before 12.128.2 contains an unauthenticated security definer RPC function get_identity_apikey_only that returns the owning user_id for supplied API keys, creating an API key validity oracle and user identity disclosure primitive. Attackers can call this endpoint with valid or invalid API keys to confirm key validity and map keys to user identifiers, then chain results into other exposed RPCs like get_orgs_v6 to retrieve organization membership and management email PII.

### CVE-2026-56341

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-20T19:16:23.700 |

AVideo through version 26.0 contains multiple unauthenticated list.json.php endpoints in payment plugins lacking authorization checks, exposing PayPal tokens, Authorize.Net webhooks, and Bitcoin transaction records. Unauthenticated attackers can retrieve all payment transaction data including agreement IDs, user financial records, and API responses via direct GET requests to vulnerable endpoints.

### CVE-2026-56340

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-20T19:16:23.567 |

vLLM versions >= 0.10.2 and < 0.13.0 are missing sparse tensor validation in multimodal embeddings processing. Because PyTorch disables sparse tensor invariant checks by default, an attacker can submit crafted embedding requests with malformed (negative or out-of-bounds) tensor indices, when the prompt-embeds feature is enabled, to trigger crashes or resource exhaustion (denial of service), with potential for out-of-bounds/write-what-where memory corruption. This continues CVE-2025-62164, whose prior fix only disabled the feature by default rather than addressing the root cause.

### CVE-2026-56382

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-21T14:16:25.757 |

Craft CMS (composer package craftcms/cms) versions >= 5.5.0 and <= 5.9.13 contain a remote code execution vulnerability in the FieldsController::actionRenderCardPreview() method, which passes the fieldLayoutConfig POST parameter directly to Fields::createLayout() without calling Component::cleanseConfig(). An authenticated admin user can inject Yii2 event handlers (e.g., 'on init' keys) via the fieldLayoutConfig parameter to execute arbitrary PHP code and disclose sensitive information (such as environment variables containing database credentials and CRAFT_SECURITY_KEY). The issue is fixed in version 5.9.14.

### CVE-2025-71378

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-21T14:16:23.140 |

picklescan before 0.0.30 fails to detect cProfile.runctx function calls in pickle file reduce methods, allowing attackers to execute arbitrary code. Malicious pickle files bypass picklescan detection and execute remote code when loaded via pickle.load().

### CVE-2025-71357

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-21T14:16:23.017 |

picklescan before 0.0.30 fails to detect malicious pickle files using idlelib.pyshell.ModifiedInterpreter.runcommand in reduce methods. Attackers can embed undetected code in pickle files that executes remote commands when loaded by victims.

### CVE-2025-71351

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-06-21T14:16:22.897 |

picklescan before 0.0.25 fails to detect malicious pickle files that use timeit.timeit() in the __reduce__ method, allowing remote code execution. Attackers can craft pickle files that import dangerous libraries like os and execute arbitrary system commands, which evade picklescan detection and execute when pickle.load() is called.

### CVE-2025-71348

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-21T14:16:22.750 |

picklescan before 0.0.28 fails to detect malicious pickle files that invoke torch.utils._config_module.load_config function within reduce methods. Attackers can craft pickle files embedding arbitrary code that evades detection but executes during pickle.load, enabling remote code execution in supply chain attacks.

### CVE-2026-56239

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-21T14:16:24.457 |

Capgo before 12.128.2 contains a potential privilege escalation vulnerability in the public.apply_usage_overage SECURITY DEFINER function, which performs sensitive billing operations without enforcing internal authorization checks (no validation of auth.uid(), org membership, or check_min_rights). Because the function runs with the owner's privileges, it bypasses Row Level Security. If EXECUTE permission is available to the authenticated or anon roles (explicitly or via default privileges), an authenticated user could invoke it via Supabase RPC to manipulate billing data for arbitrary organizations, including unauthorized credit depletion and fraudulent overage event insertion.

### CVE-2026-56394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-21T14:16:26.403 |

Craft CMS from 4.0.0-RC1 contains an authenticated path traversal vulnerability in the assets/icon endpoint where the extension parameter is not validated before file existence checks. Attackers can bypass extension validation by passing traversal sequences that resolve to existing SVG files, allowing local file read access.

### CVE-2026-56229

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-21T14:16:24.120 |

Capgo before 12.128.2 contains an authorization bypass vulnerability in the /build/status and /build/logs endpoints that allows attackers to access build jobs belonging to different applications by supplying a mismatched app_id and job_id combination. Limited API keys restricted to a single app can retrieve build status and logs from other apps by providing an authorized app_id while using a job_id from an unauthorized app, exposing sensitive build information including logs, metadata, and potentially credentials.

### CVE-2026-12786

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T09:16:25.130 |

A vulnerability has been found in Ezbsystems UltraISO Premium Edition up to 9.76. Affected by this issue is some unknown functionality in the library bootpt64.sys of the component Kernel Driver. The manipulation leads to improper access controls. Local access is required to approach this attack. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-12784

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T08:16:23.443 |

A weakness has been identified in IM-Magic Partition Resizer up to 7.9.0. This affects an unknown function in the library MDA_NTDRV.sys of the component Kernel Driver. This manipulation causes improper access controls. The attack requires local access. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-12782

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T08:16:23.280 |

A security flaw has been discovered in EaseUS Partition Master up to 14.5. The impacted element is an unknown function in the library EUEDKEPM.sys of the component Kernel Driver. The manipulation results in improper access controls. The attack requires a local approach. The exploit has been released to the public and may be used for attacks. The affected component should be upgraded. The vendor explains: "We have confirmed that this issue was present only in older versions of the product. Our product has since been updated, and the issue has been resolved in the latest version, so it no longer exists."

### CVE-2026-12781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T08:16:21.907 |

A vulnerability was identified in EaseUS Partition Master up to 14.5. The affected element is an unknown function in the library epmntdrv.sys of the component Kernel Driver. The manipulation leads to improper access controls. The attack needs to be performed locally. The exploit is publicly available and might be used. You should upgrade the affected component. The vendor explains: "We have confirmed that this issue was present only in older versions of the product. Our product has since been updated, and the issue has been resolved in the latest version, so it no longer exists."

### CVE-2026-12780

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T06:16:22.957 |

A vulnerability was determined in AOMEI Backupper up to 8.3.0. Impacted is an unknown function in the library amwrtdrv.sys of the component Kernel Driver. Executing a manipulation can lead to improper access controls. The attack needs to be launched locally. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-12779

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T06:16:22.807 |

A vulnerability was found in AOMEI Dynamic Disk Manager up to 10.10.1. This issue affects some unknown processing in the library ddmdrv.sys of the component Kernel Driver. Performing a manipulation results in improper access controls. The attack must be initiated from a local position. The exploit has been made public and could be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-12778

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266;CWE-284` |
| Published | 2026-06-21T06:16:22.637 |

A vulnerability has been found in AOMEI Partition Assistant up to 10.10.1. This vulnerability affects unknown code in the library ampa10.sys of the component Kernel Driver. Such manipulation leads to improper access controls. The attack must be carried out locally. The exploit has been disclosed to the public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-56251

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-21T14:16:24.713 |

Capgo before 12.128.2 contains a broken row level security policy in the org_users table that allows authenticated users to elevate privileges from admin to super_admin. Attackers can exploit the insufficient RLS enforcement to gain unauthorized super_admin access and compromise system security.
