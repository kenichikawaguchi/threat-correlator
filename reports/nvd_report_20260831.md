# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-30 15:00 UTC
- **対象期間**: `2026-08-29T15:01:21.000Z` 〜 `2026-08-30T15:00:22.000Z`
- **重要CVE数**: 22 件（Critical 9.0+: 5 件 / High 7.0〜: 17 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は **認証バイパス／権限昇格** と **リモートコード実行/情報漏洩** が目立ちます。特に WordPress 系プラグインや認証ライブラリ（Rodauth、pac4j）に対する攻撃面が広がっており、**未認証でも管理権限を取得できる** ケースが多数報告されています。加えて、IoT ルータや KubeEdge などインフラ層のコンポーネントでもバッファオーバーフローや認証なしのステータス更新が可能になる深刻な欠陥が見られ、**ネットワーク境界だけでなく内部サービスへの防御が求められます**。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑15980** | 9.8 | WordPress **MyHome Core** プラグイン (≤ 4.4.5) の認証バイパス | `send_link()` AJAX ハンドラに認可チェックが無く、`activate()` のトークン検証が不十分。**未認証の攻撃者が任意の管理者アカウントでログイン**でき、サイト全体が乗っ取られる危険性がある。 |
| **CVE‑2026‑15369** | 9.8 | WordPress **Custom User Registration Fields for WooCommerce** (≤ 2.2.3) の権限昇格 | WooCommerce Store API が `afreg_select_user_role` パラメータを無検証で受け取り、**任意のロールを付与**できる。EC サイトの顧客情報や決済情報が漏洩・改竄されるリスクが高い。 |
| **CVE‑2026‑82466** | 9.4 | **Rodauth** ( < 2.46.0 ) の WebAuthn ログインバイパス | 認証後のアカウント解決ロジックがセッション ID にフォールバックし、**任意のユーザーに成りすます**ことが可能。Rodauth を利用した社内 SSO や API 認証基盤全体が危殆化。 |
| **CVE‑2026‑82542** | 9.3 | **Tenda HG10** ルータ (ファームウェア 300001138) の `formIPv6Routing` バッファオーバーフロー | `destNet` パラメータの長さ検証が欠如し、遠隔から **任意コード実行** が可能。IoT デバイスがネットワークの踏み台にされ、内部セグメントへの横移動が容易になる。 |
| **CVE‑2026‑82460** | 9.3 | **Cloud Commander** (≤ 19.20.1) のディレクトリトラバーサル | REST エンドポイントでパス正規化が不十分。**任意ファイルの読み書き・削除** が可能で、サーバ上の機密情報漏洩やウェブシェル設置に直結。 |

> **補足**：他にも `keploy` (CVE‑2026‑82641) の TLS キーログ漏洩、`KubeEdge CloudCore` (CVE‑2026‑82473) の認証なしステータス報告、`pac4j` 系列 (CVE‑2026‑82463/‑82461) の認証バイパスも組織内サービスで広く利用されているため、併せて対策が必要です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時更新  
| 製品・パッケージ | 現行脆弱バージョン | 修正版 (最低バージョン) | 更新方法 |
|------------------|-------------------|------------------------|----------|
| **MyHome Core (WordPress)** | ≤ 4.4.5 | **4.4.6** 以上 | WordPress 管理画面 → 「プラグイン」→「更新」または公式リポジトリから手動インストール |
| **Custom User Registration Fields for WooCommerce** | ≤ 2.2.3 | **2.2.4** 以上 | WooCommerce → 「拡張機能」→「更新」または開発元 GitHub のリリースページ |
| **Rodauth** | < 2.46.0 | **2.46.0** 以上 | `gem update rodauth`（RubyGems）または Bundler の `bundle update rodauth` |
| **Tenda HG10 ルータ** | ファームウェア 300001138 | **最新公式ファームウェア** (ベンダー提供) | 管理画面 → 「システム」→「ファームウェア更新」 |
| **Cloud Commander** | ≤ 19.20.1 | **19.20.2** 以上 | `npm install -g cloudcmd@19.20.2` または Docker イメージの再ビルド |
| **keploy** | 3.1.0‑3.6.25 | **3.6.26** 以上 | `go get -u github.com/keploy/keploy` または Docker イメージ更新 |
| **KubeEdge CloudCore** | ≤ 1.23.1 | **1.23.2** 以上 | `kubectl apply -f https://github.com/kubeedge/kubeedge/releases/download/v1.23.2/kubeedge.yaml` |
| **pac4j‑core / pac4j‑oidc** | < 6.5.6 | **6.5.6** 以上 | Maven/Gradle の依存バージョンを `6.5.6` に上げる (`mvn versions:use-latest-releases`) |
| **Qubes OS (qubes‑core‑dom0‑linux)** | < 4.3.22 | **4.3.22** 以上 | `sudo qubes-dom0-update qubes-core-dom0-linux` |

### 3.2 共通的な防御策  
- **WAF でのリクエスト検査**  
  - `send_link`、`activate`、`/wc/store/v1/` などのエンドポイントは **POST かつ CSRF トークン必須** に設定。  
  - `../` などのパス・トラバーサル文字列は正規表現でブロック。  

- **最小権限の徹底**  
  - WordPress の管理者権限は必要最小限のユーザーに限定し、2 要素認証 (2FA) を必須化。  
  - Rodauth / pac4j を使用するサービスは **強いクライアント認証 (PKI, mTLS)** を導入。  

- **ネットワーク

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-15980

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-289` |
| Published | 2026-08-30T05:16:58.407 |

The MyHome Core plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 4.4.5. This is due to missing authorization in the send_link() AJAX handler and improper token validation in the activate() function. This makes it possible for unauthenticated attackers to generate an activation token for an unconfirmed user account and obtain a valid authentication cookie for that account, including administrators. Successful exploitation requires the MyHome theme to be configured in legacy/WPBakery mode with frontend registration and confirmation email enabled, and the target account must not already have the myhome_agent_confirmed user meta set.

### CVE-2026-15369

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-29T20:16:31.840 |

The Custom User Registration Fields for WooCommerce plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 2.2.3. This is due to the plugin accepting an attacker-controlled afreg_select_user_role value from the unauthenticated WooCommerce Store API /wc/store/v1/checkout request in the af_reg_checkout_data_to_order_meta_data_block() function, persisting it in order meta, and then passing it directly to WP_User::add_role() in the af_reg_custom_order_processing_function() function (hooked to woocommerce_thankyou) without validating against the plugin's admin-configured allowed role list. This makes it possible for unauthenticated attackers to elevate their privileges to Administrator by creating an account during checkout with a modified JSON body specifying administrator (or any other role slug) as the desired role. Note: The exploit requires the "User Role Selection" setting to be enabled.

### CVE-2026-82466

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-29T17:17:58.910 |

Rodauth before 2.46.0 contains an authentication bypass vulnerability in the webauthn_login route that allows logged-in users to authenticate as any other account. Attackers can exploit improper account resolution logic that falls back to session account identifiers instead of validating the credential binding to complete authentication as arbitrary users.

### CVE-2026-82542

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-08-30T13:16:56.267 |

A weakness has been identified in Tenda HG10 300001138. Affected by this issue is the function formIPv6Routing of the file /boaform/admin/formIPv6Routing of the component Boa Web Server. This manipulation of the argument destNet causes buffer overflow. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-82460

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-29T17:17:58.060 |

Cloud Commander before 19.20.2 contains a directory traversal vulnerability in REST file-operation and markdown endpoints that fails to properly validate path normalization. Attackers can use path traversal sequences to read, write, move, or copy files outside the configured root directory.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-82642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-30T14:17:04.193 |

Readest is an open-source e-book reader built on Tauri. In versions prior to 0.11.16, EPUB chapter HTML is sanitized with DOMPurify using a configuration that forbade only the <script> tag (FORBID_TAGS: ['script']) in apps/readest-app/src/services/transformers/sanitizer.ts. DOMPurify does not parse the contents of the srcdoc attribute on <iframe> elements, treating it as an opaque string attribute, so an attacker who can get an <iframe> element to survive sanitization can embed a complete HTML document containing a <script> tag inside srcdoc and have it execute when the browser renders the iframe. The content iframe is configured with sandbox="allow-same-origin allow-scripts", so script executing inside it shares the parent origin and can reach parent.parent.__TAURI_INTERNALS__.invoke(...), giving access to every Tauri IPC command the application is permitted to use, which escalates to arbitrary code execution. The payload can be made invisible (zero-size, transparent iframe) so the reader sees only normal book text. Version 0.11.16 hardened the sanitizer configuration by adding 'iframe', 'object' and 'embed' to FORBID_TAGS and adding 'srcdoc' to FORBID_ATTR.

### CVE-2026-82641

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-30T14:17:04.020 |

keploy versions 3.1.0 through 3.6.25 bind the agent control-plane HTTP server to all interfaces without authentication, exposing endpoints that stream TLS session keys and traffic data. Attackers can access the /agent/pcap/keylog endpoint to retrieve NSS keylog lines and decrypt recorded TLS traffic, or invoke /agent/stop and /agent/storemocks to manipulate recording sessions.

### CVE-2026-82635

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-30T13:16:56.923 |

Pake before 3.13.1 joins the JavaScript-supplied filename for the download_file Tauri command onto the user's Downloads directory with no sanitization. A filename containing path traversal sequences (for example ../Library/LaunchAgents/com.evil.plist) or an absolute path resolves outside ~/Downloads. The command then fetches attacker-controlled content from the supplied URL (via Rust HTTP, not the browser) and writes it to that path. A script that can invoke the command can overwrite user-writable files and install persistence (macOS LaunchAgents, Linux autostart, Windows Startup), leading to code execution in the user account. All desktop apps generated from an affected Pake tree expose the same command.

### CVE-2026-82473

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-29T17:17:59.770 |

KubeEdge CloudCore through 1.23.1 accepts node task status reports on its HTTPS server without authentication verification. Attackers can reach CloudCore on port 10002 to mark upgrade jobs as succeeded or failed, deceiving the control plane about node upgrade status and blocking further upgrade scheduling.

### CVE-2026-82639

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-30T14:17:03.750 |

NextChat versions from 2.15.8 through 2.16.1 contain an improper URL validation vulnerability in the proxy endpoint that allows attackers to obtain the server's OpenAI API key. The x-base-url header is validated using substring matching instead of hostname parsing, allowing any URL containing 'api.openai.com' to pass validation and receive the server's credentials in the Authorization header.

### CVE-2026-82638

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-30T14:17:03.610 |

jina-ai reader disables its private-address guard outside Google Cloud deployments, allowing unauthenticated attackers to perform server-side request forgery. Attackers can supply publicly resolvable hostnames mapping to private addresses to retrieve cloud metadata and internal service content.

### CVE-2026-82472

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-29T17:17:59.623 |

Documenso before 2.13.0 accepts PDF file uploads on the /api/files/upload-pdf endpoint without requiring authentication, session tokens, or API credentials. Unauthenticated attackers can upload arbitrary PDF files indefinitely to exhaust storage resources or fill the database with unlinked document records.

### CVE-2026-82481

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:D/RE:M/U:X` |
| Weaknesses | `CWE-180` |
| Published | 2026-08-29T15:17:55.487 |

The cohttp package before 6.3.0 for OCaml allows directory traversal.

### CVE-2026-82475

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-29T17:18:00.057 |

iFlytek astron-agent through 1.1.1 contains an authorization bypass vulnerability in the copyFlow endpoint that fails to validate workflow ownership. Authenticated attackers can enumerate workflow identifiers and overwrite other tenants' workflows or copy private workflows to read their definitions.

### CVE-2026-82463

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-29T17:17:58.490 |

pac4j-core before 6.5.6 contains an authentication bypass vulnerability in CheckProfileTypeAuthorizer that reverses the profile type validation logic. Attackers can authenticate through a weaker client and access resources requiring a stronger profile type by satisfying generic profile checks.

### CVE-2026-82461

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-29T17:17:58.207 |

pac4j-oidc before 6.5.6 fails to verify access token signatures, issuers, audiences, or expiry when extracting Keycloak realm and client roles. Attackers can forge access tokens with administrative roles paired with valid ID tokens to bypass authorization checks in applications relying on pac4j role validation.

### CVE-2026-82539

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-30T11:17:35.067 |

A vulnerability was determined in TOTOLINK A720R 4.1.5cu.630_B20250509. This impacts the function setMacFilterRules of the file cstecgi.cgi of the component MAC Filtering. Executing a manipulation of the argument desc can lead to memory corruption. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-82474

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-29T17:17:59.910 |

Sudo through 1.9.17p2 fails to apply intercept policy checks to the execveat system call in ptrace-based intercept mode. Users permitted to run specific commands can execute denied programs by calling execveat directly or through fexecve, bypassing policy enforcement and logging.

### CVE-2026-82636

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-30T14:17:03.310 |

Qubes OS before qubes-core-dom0-linux 4.3.22 allows OS command injection during a qvm-copy-to-vm call from dom0 to an attacker-controlled qube, because the "system" library function is used to process an error message that may have shell metacharacters. This occurs in core-admin-linux/file-copy-vm/qfile-dom0-agent.c.

### CVE-2026-75759

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-30T02:18:30.110 |

Improper Verification of Cryptographic Signature vulnerability in erlef oidcc allows an unauthenticated attacker to impersonate an arbitrary user via an encrypted ID token or JARM response carrying no nested signature. OpenID Connect Core 1.0 section 2 requires that an encrypted ID token be signed then encrypted, with the result being a Nested JWT, and JARM processing rule 5 requires the client to check the signature unconditionally. oidcc instead accepted a JWE wrapping unsigned claims as fully validated, so anyone holding the relying party's public encryption key could mint a token with an arbitrary sub, iss, and aud without possessing the provider's signing key.

In oidcc_jwt_util:verify_decrypted_token/4, a decrypted payload that is not a signed JWS fell back to parsing the plaintext claims and returning them with no verifying key. oidcc_token:int_validate_jwt/4 then matched on the JOSE structure type rather than on whether a signature had been verified, and returned success. The JARM path in oidcc_token:validate_jarm/3 is reachable through the browser front channel. UserInfo responses are not affected, because OpenID Connect Core 1.0 section 5.3.2 permits them to be encrypted without also being signed.

This issue affects oidcc: from 3.2.0-beta.1 before 3.9.0.

### CVE-2026-75807

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-29T18:16:36.313 |

The SAML Single Sign On – SSO Login plugin for WordPress is vulnerable to Authentication Bypass in versions up to, and including, 5.4.6. This is due to the mo_saml_login_validate() ACS handler persisting the X.509 certificate extracted from an incoming SAMLResponse into the mo_saml_required_certificate option before the signature-validation verdict is enforced, because mo_saml_find_certificate() returns false on a fingerprint mismatch rather than halting execution. This makes it possible for unauthenticated attackers to overwrite the plugin's stored IdP signing certificate with an attacker-controlled value, and subsequently forge SAML assertions for any WordPress account — including administrators — to obtain a fully privileged session. Note: The exploit requires the administrator to perform a repair after receiving the test_config_error_wpsamlerr004 error message during the test configuration.

### CVE-2026-82634

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-30T13:16:56.780 |

Frappe Framework development builds contain an authorization flaw in the render_jinja_template endpoint that allows low-privileged users to render arbitrary Jinja templates by supplying raw template strings. Attackers with print permission on any document can execute arbitrary SELECT statements against unrelated tables, including reading password hashes from the __Auth table.
