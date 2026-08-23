# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-23 15:00 UTC
- **対象期間**: `2026-08-22T15:01:14.000Z` 〜 `2026-08-23T15:00:22.000Z`
- **重要CVE数**: 35 件（Critical 9.0+: 13 件 / High 7.0〜: 22 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 今回公開された CVE の大半は **Joomla 用 Fabrik 拡張 (v4.7.2 未満)** に集中しており、認証不要でリモートコード実行 (RCE) や任意ファイル取得・書き込みといった深刻な攻撃が可能です。  
- 同様に **WordPress プラグイン**、**justhtml ライブラリ**、**NLTK Python パッケージ**でも高スコア (CVSS ≥ 8.5) の脆弱性が多数報告され、Web アプリケーションだけでなく開発環境全体にもリスクが波及しています。  
- 脆弱性の共通点は **入力検証・ACL の欠如**、**安全でないシリアライズ／デシリアライズ**、**パス検証の不備** です。  
- これらはすべて **ネットワーク越しに直接攻撃できる (AV:N)** ことから、外部からのスキャンや自動攻撃ツールに狙われやすく、早急な対策が必須です。

---

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 主な影響 | 注目理由 |
|--------|--------|----------|----------|
| **CVE‑2026‑76604** | 10.0 | Fabrik の PHP フォーム要素で認証不要の RCE (任意コード実行) | **最も危険度が高く、Web サーバ上で任意コードが即座に実行可能**。ACL が全くチェックされていないため、全サイトが即座に乗っ取られるリスク。 |
| **CVE‑2026‑76605** | 10.0 | Fabrik の画像要素でリモートコード実行 | 画像アップロード機能を経由した **コードインジェクション**。画像処理は多くのサイトで必須機能のため、攻撃対象が広範。 |
| **CVE‑2026‑76606** | 10.0 | Fabrik の画像要素でパス・トラバーサル | 任意ファイル取得が可能で、**機密情報漏洩**や **さらなる RCE の足掛かり**になる。 |
| **CVE‑2026‑76607** | 10.0 | Fabrik のダウンロード要素で ACL 不備 | 認証なしで任意ファイルをダウンロードでき、**情報漏洩**と **内部ネットワーク走査** が容易になる。 |
| **CVE‑2026‑78155** | 9.9 | StackGres Operator の特権昇格 | **テナント権限からクラスター管理者権限へ**昇格でき、Kubernetes 環境全体が危険に晒される。 |

> **共通点**：すべて **認証不要 (PR:N)**、**ネットワーク越しに直接利用可能 (AV:N)** で、攻撃成功時の影響が **機密性・完全性・可用性すべてに重大**（CVSS = 10.0）です。特に Fabrik 系は同一バージョンで多数の脆弱点が報告されているため、**一括パッチ適用が最優先**となります。

---

## 3. 推奨アクション  

### 3.1 Joomla / Fabrik 系統  
- **アップデート**  
  - `fabrik` → **4.7.2 以上**（公式リリースで上記全脆弱性が修正）  
  - Joomla 本体も **4.2.10 以上** に更新し、拡張機能の互換性を確認。  
- **緊急対策**（パッチ適用がすぐにできない場合）  
  - `download`, `image`, `phpform` などの危険要素を **無効化** または **アクセス制御プラグインで ACL を強制**。  
  - `web.config` / `.htaccess` で **`/components/com_fabrik/` 配下の直接実行を禁止**（`Deny from all`）。  
- **監視**  
  - Apache/Nginx のアクセスログで `fabrik` 関連の `/index.php?option=com_fabrik&...` リクエストを **リアルタイムでアラート**（例: Fail2Ban のカスタムフィルタ）。  

### 3.2 StackGres Operator  
- **アップデート**  
  - `stackgres-operator` → **1.9.3 以上**（特権昇格パッチ適用版）。  
- **RBAC 強化**  
  - テナントが所有する `Role`/`RoleBinding` を見直し、`admin` 権限を付与しないように **Namespace‑Scoped** に限定。  
- **監査**  
  - Kubernetes の `audit` ログで `stackgres` 関連の `SubjectAccessReview` を監視し、異常な権限取得を検知。  

### 3.3 WordPress プラグイン  
| プラグイン | 修正バージョン | 主な脆弱性 |
|-----------|----------------|------------|
| WS Form LITE (Drag & Drop Contact Form Builder) | **1.10.81 以上** | PHP Object Injection |
| Security Hardener | **2.4.5 以上** | Missing Authorization |
| PPWP – Password Protect Pages | **1.9.19 以上** | PHP Object Injection |
| その他 (fabrikar.com 由来のプラグインは Joomla 用なので対象外) | – | – |

- **即時対策**：脆弱プラグインを **無効化** し、代替プラグインへ移行。  
- **自動更新**：`WP‑CLI` の `wp plugin update --all` を CI/CD に組み込み、定期的に最新バージョンを取得。  

### 3.4 justhtml ライブラリ  
- **アップデート**  
  - `justhtml` → **1.12.0 以上**（HTML エスケープ不備修正）  
  - さらに **1.16.0 以上** にすれば XSS バイパスも解消。  
- **設定見直し**  
  - `JustHTML(..., sanitize=True)` を必ず有効化し、`html_passthrough=False` をデフォルトに設定。  

### 3.5 NLTK (Python)  
- **アップデート**  
  - `nltk` → **3.10.2 以上**（ローカルファイル読取・シンボリックリンクバイパス・JSON デコード DoS の全修正）  
- **ダウンロード時の検証**  
  - `nltk.download()` の前後で **TLS/SSL 検証** を強制し、`pip install --upgrade nltk` と同時に `pip install --upgrade certifi` を実行。  

### 3.6 その他重要製品  
| 製品 / ライブラ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-76607

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-22T15:16:22.797 |

Joomla Extension - fabrikar.com - Missing ACL check in download element in Fabrik < 4.7.2.

### CVE-2026-76606

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-22T15:16:22.680 |

Joomla Extension - fabrikar.com - Path Traversal via image element in Fabrik < 4.7.2.

### CVE-2026-76605

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-22T15:16:22.563 |

Joomla Extension - fabrikar.com - Remote code execution via image element in Fabrik < 4.7.2.

### CVE-2026-76604

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-22T15:16:22.440 |

Joomla Extension - fabrikar.com - Unauthenticated remote code execution via PHP form element in Fabrik < 4.7.2 - The PHP form element is vulnerable to the execution of user provided codes.

### CVE-2026-78155

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-23T10:16:28.757 |

privilege escalation in StackGres operator allows a low-privilege tenant who owns a database to gain administrator privileges

### CVE-2026-4703

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-22T16:16:29.497 |

The WS Form LITE – Drag & Drop Contact Form Builder plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.10.80 via deserialization of untrusted input from form submission meta values. This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-77992

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-22T15:16:23.293 |

Joomla Extension - fabrikar.com - heredoc terminator breakout in the calc element in Fabrik < 4.7.2 - The onUpdateComment endpoint did not perform any access checks.

### CVE-2026-8445

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-23T14:16:54.957 |

justhtml versions <= 1.11.0 (fixed in 1.12.0) do not sufficiently escape HTML-significant characters (angle brackets) in text nodes when converting a parsed document to Markdown via to_markdown(). While a small set of Markdown metacharacters are escaped, characters such as < and > are preserved, so untrusted input that is safe in to_html() — including entity-decoded text (e.g. &lt;script&gt;) or text from RCDATA/RAWTEXT-parsed elements like <title>, <textarea>, <noscript>, and <plaintext> — can be emitted as raw HTML in the Markdown output, enabling a sanitizer bypass and potential cross-site scripting when that output is rendered.

### CVE-2026-7808

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-23T14:16:54.810 |

justhtml before 1.16.0 contains multiple HTML sanitization bypass issues that can allow active/dangerous content (e.g., script or style) to survive sanitization, potentially leading to cross-site scripting. The issues primarily affect advanced usage rather than the default JustHTML(..., sanitize=True) path for ordinary parsed HTML: mutating or reusing sanitization policy objects (including exported defaults) could weaken later sanitization; programmatic DOM input to sanitize()/sanitize_dom() could miss mixed-case tag names (e.g., ScRiPt, StYlE); crafted programmatic doctype names could serialize into active markup; and custom policies preserving SVG or MathML could allow animation elements, presentation attributes with external url(...) references, or DOM trees mislabeled as namespace="html" to bypass foreign-content checks. Fixed in 1.16.0.

### CVE-2026-5388

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-23T14:16:53.470 |

justhtml before 1.15.0 contains multiple security issues in URL sanitization helpers (clean_url_value/clean_url_in_js_string), HTML serialization, Markdown passthrough (html_passthrough=True), and several custom sanitization-policy edge cases. Depending on configuration, an attacker can bypass sanitization to inject active HTML and JavaScript — for example via encoded javascript: URLs, backslash-based relative URLs resolved as remote hosts, markup-breaking programmatic element/attribute names or HTML comments, raw </textarea> reintroduction through Markdown passthrough, or preserved <style>/<meta http-equiv=refresh>/<base href> tags in custom policies. Most custom-policy issues do not affect the default sanitize=True configuration; they primarily affect helper APIs, programmatic DOM construction, html_passthrough=True, and custom policies/transform pipelines.

### CVE-2026-76602

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-22T15:16:22.200 |

Joomla Extension - fabrikar.com - Unauthenticated SQL injection in ORDER BY in Fabrik < 4.7.2 - The order parameter in list models is used in queries without validation, allowing read SQLi vectors.

### CVE-2026-76571

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-22T15:16:21.383 |

Joomla Extension - fabrikar.com - Unauthenticated SQL injection in list filter condition parameter in Fabrik < 4.7.2 - The condition parameter passed to a list filter is concatenated verbatim into the WHERE clause built by getFilterQuery(). An unauthenticated attacker can supply arbitrary SQL through the filter condition, giving full read of the database.

### CVE-2026-63310

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-22T15:16:19.100 |

NLTK before 3.9.3 fails to verify file integrity after downloading packages and before extraction in the downloader module. Attackers can perform man-in-the-middle attacks or DNS poisoning to inject malicious package contents that are extracted without validation.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-23T00:16:50.233 |

The Security Hardener plugin for WordPress is vulnerable to Missing Authorization in all versions up to, and including, 2.4.4. The vulnerability exists because the plugin's user-enumeration protection, which is enabled by default, hooks the rest_endpoints filter via secure_user_endpoints() and overwrites every registered handler's permission_callback on both the /wp/v2/users and /wp/v2/users/(?P<id>[\d]+) routes — including POST, PUT, PATCH, and DELETE handlers — with a bare closure that returns only is_user_logged_in(), completely stripping WordPress Core's original capability checks such as create_users, promote_user, edit_users, and delete_users that WP_REST_Users_Controller normally enforces. This makes it possible for authenticated attackers with Subscriber-level access and above to create new Administrator accounts by sending POST request to /wp/v2/users with administrator role, or to reset an existing Administrator's password by issuing a PUT/POST request to /wp/v2/users/<id>. Because the block_user_enum option defaults to enabled, no special plugin configuration is required — the overwrite is active on every request as soon as the plugin is installed.

### CVE-2026-0551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-23T00:16:49.777 |

The PPWP – Password Protect Pages plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.9.18 via deserialization of untrusted input from the 'post_protection_roles' vulnerable parameter. This makes it possible for authenticated attackers, with Contributor-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-9769

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-23T14:16:55.277 |

justhtml through 1.9.1 (fixed in 1.10.0) is vulnerable to uncontrolled recursion leading to denial of service. During JustHTML() construction, TreeBuilder.finish() unconditionally calls _populate_selectedcontent(), which recursively traverses the DOM tree via _find_elements()/_find_element() without a depth bound. An attacker who can supply HTML for parsing can provide deeply nested elements (e.g., ~1000 nested <div> tags, roughly 11 KB) to exceed CPython's default recursion limit and trigger an unhandled RecursionError, which may abort parsing, fail requests, or terminate a worker/process depending on the host application's exception handling.

### CVE-2026-4671

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-23T14:16:53.293 |

justhtml before 1.18.0 contains multiple low-severity denial-of-service issues in CSS selector handling and linkification. Applications that evaluate attacker-controlled selector strings (via query(), matches(), or selector-based transforms), run selector matching over very large untrusted documents, construct DOM trees from untrusted structure, or enable linkification over attacker-controlled text may consume disproportionate CPU or memory. Triggers include oversized selectors, large selector lists, oversized compound selectors, long combinator chains, deeply nested functional pseudo-classes, repeated token/positional matching, cyclic DOM graphs causing non-terminating traversal, and punctuation-heavy or trailing-bracket linkification input. These are availability-only concerns and do not by themselves allow script execution, data disclosure, or sanitizer bypass. Default JustHTML(sanitize=True) usage is not expected to be exposed, since selectors are normally supplied by application code.

### CVE-2026-76599

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-22T15:16:21.857 |

Joomla Extension - fabrikar.com - Unauthenticated database table list and table-prefix disclosure in Fabrik < 4.7.2 - The ajax_tables method of the elements model allows listings of arbitrary database tables including columns.

### CVE-2026-76598

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-284` |
| Published | 2026-08-22T15:16:21.733 |

Joomla Extension - fabrikar.com - Unauthenticated arbitrary directory listing via onAjax_getFolders in Fabrik < 4.7.2 - The onAjax_getFolders method of the elements model allows arbitrary directory listings.

### CVE-2026-76597

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-22T15:16:21.620 |

Joomla Extension - fabrikar.com - Unauthenticated arbitrary file upload to web root via list email plugin in Fabrik < 4.7.2 - The list email plugin controller allows to upload non-executable files to the webroot.

### CVE-2026-76596

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-22T15:16:21.500 |

Joomla Extension - fabrikar.com - Unauthenticated table truncation via list.doempty in Fabrik < 4.7.2- The list controllers doemtpy endpoints lacks ACL gates, a plain GET empties the target list's table

### CVE-2026-66393

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-22T15:16:19.633 |

NLTK versions before 3.9.4 contain an unbounded recursion vulnerability in JSONTaggedDecoder.decode_obj() that allows attackers to cause denial of service by supplying deeply nested JSON structures. Attackers can craft JSON payloads exceeding the recursion limit to trigger an unhandled RecursionError that crashes the Python process.

### CVE-2026-63312

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-22T15:16:19.367 |

NLTK before 3.10.0 contains an arbitrary local file read vulnerability in StreamBackedCorpusView that bypasses pathsec.ENFORCE by calling builtins.open() directly instead of pathsec.open(). Attackers who control the fileid argument can read arbitrary local files regardless of the ENFORCE setting, including sensitive system files and application credentials.

### CVE-2026-62388

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-08-22T15:16:18.967 |

NLTK versions before 3.10.0 default to ENFORCE=False in pathsec.py, causing all security validation functions to emit warnings instead of raising exceptions. Attackers can bypass path traversal and pickle deserialization protections by exploiting the disabled security controls that are only active when manually enabled.

### CVE-2026-62384

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-22T15:16:18.700 |

NLTK versions before 3.10.2 contain a symlink-based sandbox bypass in FramenetCorpusReader that allows attackers to read arbitrary XML files outside the corpus root. Attackers can place symlinks with names containing no path separators inside the corpus subdirectory, which pass the path validation guard and are resolved to files outside the intended corpus root when accessed via frame_by_name(), _lu_file(), or doc() methods.

### CVE-2026-78050

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-23T00:16:50.590 |

A vulnerability was found in Comfast CF-N1-S 2.6.0.1. The affected element is the function sub_41AD7C of the file /cgi-bin/mbox-config?method=SET&section=ntp_timezone of the component Web Management. The manipulation of the argument timestr/ntp_client_enabled results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been made public and could be used.

### CVE-2026-77027

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-22T15:16:23.150 |

Joomla Extension - fabrikar.com - Unauthenticated stored XSS in Fabrik < 4.7.2 - The handling of user supplied input in the jsactions feature leads to an stored XSS vector.

### CVE-2026-70626

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-22T15:16:21.100 |

NLTK versions before 3.9.4 contain a symlink escape vulnerability in CorpusReader.open() that allows local attackers to read arbitrary files outside the corpus root. The vulnerability exists because path validation is lexical and does not account for symlink resolution, enabling attackers to place symlinks inside the corpus root to access files outside the intended boundary.

### CVE-2026-10053

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-23T10:16:27.140 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.8 before 19.0.6, 19.1 before 19.1.4, and 19.2 before 19.2.2 that under certain conditions could have allowed an authenticated user to achieve remote code execution due to a path traversal vulnerability in the package registry.

### CVE-2026-68766

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-22T15:16:20.633 |

hashcat fails to restrict command-line options when parsing restore files, allowing attackers to inject output-redirecting options like --outfile and --potfile-path. Attackers can craft restore files with malicious options to append attacker-controlled content to arbitrary files, enabling code execution when targeting shell startup files.

### CVE-2026-78122

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1220` |
| Published | 2026-08-22T23:16:22.923 |

docker-socket-proxy fails to properly gate read endpoints in the /containers Docker API namespace when the CONTAINERS environment variable is set. Attackers can use GET requests to /containers/{id}/archive, /containers/{id}/export, /containers/{id}/logs, and /containers/{id}/top to read arbitrary files and download entire container filesystems as tar archives.

### CVE-2026-62385

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-22T15:16:18.833 |

NLTK versions before 3.10.0 contain a path traversal vulnerability in FramenetCorpusReader and NKJPCorpusReader that allows attackers to parse XML files outside the corpus root by supplying unsafe selectors or poisoned index state. Attackers can exploit frame_by_name, doc, lu, and header methods with crafted parameters to read arbitrary XML files accessible to the application.

### CVE-2026-78136

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-23T01:17:20.143 |

chirpmyradio CHIRP before 39178db allows eval injection via crafted CSV data. This occurs in _clean_tmode in drivers/kenwood_itm.py.

### CVE-2026-47895

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-08-22T22:16:28.153 |

In strongSwan before 6.0.7, identity parsing/cloning is mishandled. Parsed EAP-Identities that result in an empty but non-NULL encoding are not correctly cloned and trigger a double-free once the duplicates are destroyed.

### CVE-2026-65915

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-22T15:16:19.500 |

NLTK versions before 3.10.0 contain a logic bug in FileSystemPathPointer.open() where the sandbox validation check compares a normalized path against itself, making the security check permanently inert. Attackers can pass file:// URLs to nltk.data.load() to read arbitrary files accessible to the process user, including credentials and configuration files.
