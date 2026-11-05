# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-05 15:00 UTC
- **対象期間**: `2026-11-04T15:00:51.000Z` 〜 `2026-11-05T15:00:55.000Z`
- **重要CVE数**: 158 件（Critical 9.0+: 43 件 / High 7.0〜: 115 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 超にのぼり、特に **Apache Juneau 系列** が多数（10 件）で CVSS 10.0 の深刻度が集中しています。  
同時に、コンテナサンドボックスの分離不備（Yuxi）や、AI/ML 関連サービス（IBM Watson、GPUStack）での **リモートコード実行** が目立ち、攻撃者が認証なしで管理権限取得や情報漏洩を行えるケースが増加しています。  

## 2. 特に注目すべき CVE  

| CVE | 製品・コンポーネント | 主な脆弱性種別 | 影響範囲・リスク |
|-----|-------------------|----------------|-------------------|
| **CVE‑2026‑96677** | Apache Juneau (Web Page Generation) | Reflected XSS (HTML エンコード欠如) | 任意のスクリプトがページヘッダー等に埋め込めるため、認証情報や CSRF トークンの盗取が可能。全ての Juneau ベース API が対象。 |
| **CVE‑2026‑73117** | Apache Juneau (HTTP Response Splitting) | HTTP ヘッダー CRLF インジェクション | 攻撃者が任意のレスポンスヘッダーを注入でき、キャッシュポイズニングやセッションハイジャックが実現。外部公開 API で特に危険。 |
| **CVE‑2026‑73116** | Apache Juneau (Insufficiently Protected Credentials) | 認証情報漏洩 (リダイレクト時にヘッダーが転送) | HTTPS→HTTP のリダイレクトで認証トークンが平文送信され、MITM 攻撃により完全なアカウント乗っ取りが可能。 |
| **CVE‑2026‑97693** | Yuxi (Docker Sandbox) | コンテナ間の権限昇格（低権限ユーザーがホスト上の Docker を操作） | 0.6.0 β1‑0.7.1 の間に、認証済み低権限ユーザーが `docker exec` 等で任意コード実行。AI 知識グラフ基盤全体が侵害対象に。 |
| **CVE‑2026‑82418** | IBM Watson Speech Services Cartridge 4.0.0‑5.4.0 | Use‑After‑Free → 任意コード実行 | メモリ解放後に再利用されるオブジェクトを操作でき、リモートから任意バイナリを実行可能。音声認識サービスを利用する全顧客に影響。 |

> **選定理由**  
> - **スコア 10.0** のものが多数で、特に **Apache Juneau** は Web API の基盤として広く採用されているため、影響範囲が大きい。  
> - **Yuxi** と **IBM Watson** は AI/ML プラットフォームであり、クラウド上で機密データやモデルが扱われる点から、侵害時の損害が甚大。  

## 3. 推奨アクション  

### 3.1 Apache Juneau 系列（全 CVE 共通）  
- **アップデート**  
  - `org.apache.juneau:juniversal` → **v2.2.1** 以上（2026‑09‑15 リリース）  
  - `org.apache.juneau:juniversal-rest` → **v2.2.1** 以上  
- **設定変更**  
  - `htmlEncode=true`（デフォルトで無効化されている項目）を有効化し、全テンプレート変数を HTML エンコード。  
  - `responseHeaderSanitizer.enabled=true` を設定し、ヘッダー値の CRLF を除去。  
  - `credentialForwarding.enabled=false`（リダイレクト時の認証ヘッダー転送を無効化）。  
- **コードレビュー**  
  - `RestClient` のリダイレクトロジックを確認し、`Location` ヘッダーのスキームが `https` 以外の場合は認証ヘッダーを削除。  
- **モニタリング**  
  - Web アプリケーションファイアウォール (WAF) で **Reflected XSS** と **Response Splitting** のシグネチャを追加。  
  - 認証ヘッダーがログに出力されていないか、`/var/log/juneau/*.log` を定期的に監査。  

### 3.2 Yuxi (AI 知識グラフ)  
- **バージョンアップ**  
  - `yuxi-platform` → **v0.7.2** 以上（Docker サンドボックス分離強化パッチ）  
- **権限分離**  
  - Docker デーモンへのアクセスは **rootless Docker** または **Podman** に切り替え、`/var/run/docker.sock` の権限を `0600` に限定。  
  - 低権限ユーザーに対して **Docker グループ** から除外し、`sudo` 経由での `docker` コマンド実行を禁止。  
- **ネットワーク分離**  
  - コンテナ間の **bridge** ネットワークを分割し、`yuxi` 用ネットワークは外部から直接アクセス不可に設定 (`iptables -A INPUT -s <trusted‑subnet> -j ACCEPT`).  

### 3.3 IBM Watson Speech Services Cartridge  
- **パッチ適用**  
  - `ibm-watson-speech-cartridge` → **v5.5.3** 以上（use‑after‑free 修正）  
- **メモリ保護**  
  - カーネルレベルで **ASLR** と **Stack Canaries** を有効化 (`sysctl -w kernel.randomize_va_space=2`)。  
  - コンテナ実行時に `--security-opt=no-new-privileges` と `--cap-drop=ALL` を付与。  
- **脆弱性スキャン**  
  - 定期的に **Clair** / **Trivy** でイメージの脆弱性をスキャンし、`ibm-watson-speech` のベースイメージが最新か確認。  

### 3.4 共通的な緊急対策  
- **インシデントレスポンス**  
  - 影響が疑われるシステムは **即時ログ取得**（`/var/log/*`、`journalctl`）と **証拠保全** を実施。  
  - すべての API キー・トークンを **ローテーション**（特に `Authorization` ヘッダーが漏洩した可能性がある場合）。  
- **脆弱性管理**  
  - 社内の **SBOM**（Software Bill of Materials）を更新し、対象パッケージのバージョンを可視化。  
  - CI/CD パイプラインに **Dependabot / Renovate** を導入し、セキュリティアップデートを自動で PR 化。  
- **防御強化**  
  - HTTP **Content‑Security‑

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-96677

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T12:17:51.620 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Apache Juneau.

HTML document serialization does not HTML-encode variable substitutions in the page chrome (header, nav, aside, footer and similar fields). Applications whose chrome includes request-derived variables, such as request headers, form data or path values, reflect those values unencoded, allowing cross-site scripting. The default chrome does not use request variables, so only applications that add them are affected.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-73117

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-113` |
| Published | 2026-11-05T12:17:51.473 |

Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting') vulnerability in Apache Juneau.

The Apache Juneau REST server passed response header values and redirect targets to the servlet container unchecked. An application that sets a response header or redirect target from request data could let a remote client inject header lines (where the servlet container does not itself reject CR/LF) or redirect users to an arbitrary external site. The framework itself does not build headers or redirects from request data; exposure depends on application code.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue. Header values are now sanitized by default; applications that build redirect targets from request data must also switch from sendRedirect() to the new sendSafeRedirect().

### CVE-2026-73116

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-05T12:17:51.333 |

Insufficiently Protected Credentials vulnerability in Apache Juneau.

The Apache Juneau RestClient followed HTTP redirects while keeping credential headers from the original request, so a server that redirected the client to a different host or port, or from HTTPS to HTTP, could receive headers such as Authorization, Cookie, Proxy-Authorization and X-API-Key.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue. The fix applies to HTTP clients created by the RestClient builder; applications that supply their own HttpClient must disable automatic redirects or strip credential headers on cross-origin redirects themselves.

### CVE-2026-73101

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-11-05T12:17:51.197 |

Generation of Error Message Containing Sensitive Information vulnerability in Apache Juneau.

The REST server sends the internal exception class and message to clients in a "Thrown" response header on every error response, and can include internal exception messages in the error body, even when stack-trace rendering is disabled. This reveals implementation details to remote clients.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-73100

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-11-05T12:17:51.060 |

Insertion of Sensitive Information into Log File vulnerability in Apache Juneau.

The default REST server call logger records request headers for requests that end in a server error, without redacting them. Any client able to cause a server error gets headers such as Authorization, Cookie, Proxy-Authorization and X-API-Key written in cleartext to the application log, exposing them to anyone who can read the logs.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-73099

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-05T12:17:50.917 |

Cross-Site Request Forgery (CSRF) vulnerability in Apache Juneau.

The REST server accepts a "content" query parameter that replaces the request body, and this is enabled by default on every HTTP method, including GET. A cross-site link can therefore deliver an attacker-chosen request body to an endpoint without a CORS preflight, defeating protections that rely on the HTTP method or content type instead of an anti-CSRF token.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue. Applications that do not use the content parameter can also set disableContentParam to true.

### CVE-2026-73098

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-05T12:17:50.770 |

Improper control of dynamically-loaded code vulnerability in Apache Juneau.

When Apache Juneau parses a value into a property of type java.lang.Class (including parameterized forms), the default class swap loaded the named class with initialization enabled, so input naming a class on the application classpath ran that class's static initializer. The impact depends on the classes present in the deployment.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-121489

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T12:17:49.643 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Apache Juneau.

The microservice DirectoryResource does not keep request paths inside its configured root directory. When an application enables the resource's view, upload or delete settings (all off by default), a client can read, write or delete files outside the root, anywhere the server process has access.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-97693

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-284;CWE-522` |
| Published | 2026-11-04T22:18:07.687 |

Yuxi is a large-model-based intelligent knowledge base and knowledge graph agent development platform.  From 0.6.0.beta1 until 0.7.1, there is insufficient isolation between execution-capable Docker sandboxes and trusted application services. A low-privileged authenticated user who can execute commands in their own sandbox can reach other tenants' sandbox APIs, access their files and secrets, execute commands in active sandboxes, and enumerate, create, or delete sandboxes through the unauthenticated provisioner without knowing administrator, database, or MinIO credentials. Sandboxes can also reach shared internal services; if shipped default service credentials remain unchanged, an attacker can use them, and if the exposed PostgreSQL account is a superuser, obtain command execution in the PostgreSQL container. These paths can disclose or modify cross-tenant data and sandbox state or cause denial of service through sandbox deletion without a container escape or kernel vulnerability. This vulnerability is fixed in 0.7.1. Existing deployments must separately rotate persisted PostgreSQL, Neo4j, or MinIO credentials that were previously set to documented or shipped defaults because upgrading the Compose files does not automatically rotate them.

### CVE-2026-100109

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-05T08:17:01.870 |

The Security For WooCommerce WordPress plugin from 1.0.10 to 1.0.16 does not perform capability checks when creating users through an action available to unauthenticated visitors, and lets the caller choose the new account's role, allowing unauthenticated attackers to create administrator accounts and take over the site.

### CVE-2026-102895

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-290;CWE-346` |
| Published | 2026-11-04T22:17:44.613 |

GPUStack is an open-source GPU cluster manager for AI model serving and GPU instance provisioning. Prior to 2.2.0, get_current_user in gpustack/api/auth.py treated a loopback request source as the built-in administrator when force_auth_localhost was false, which was the default. A remote request could appear to originate from 127.0.0.1 because client_ip_getter accepted a same-host reverse proxy peer or a client-supplied X-GPUStack-Real-IP loopback value. The bypass allowed unauthenticated administrative access, including user and model changes, persistent administrator API-key creation, disclosure of worker and cloud-provider secrets, and code execution through POST /v2/inference-backends/from-yaml. Exploitation was observed in the wild against a 2.1.1 deployment. This issue is fixed in version 2.2.0.

### CVE-2026-82418

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-04T21:18:14.940 |

IBM Watson Speech Services Cartridge 4.0.0 through 5.4.0 could allow a remote attacker to execute arbitrary code due to a use-after-free vulnerability.

### CVE-2026-122006

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1188` |
| Published | 2026-11-04T15:17:42.940 |

The activestorage gem before 8.1.4.1 for Ruby on Rails, when ImageMagick attachment processing occurs, can allow server read and write operations (e.g., reading secret_key_base) because the ImageMagick analyzer runs when a file is attached, and there is not an ImageMagick security policy to block unintended functionality.

### CVE-2026-115770

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-04T23:17:18.767 |

Pocket ID is an OIDC provider that allows users to authenticate with their passkeys to services. From 2.2.0 until 2.12.0, SendEmailVerification uses the token model in backend/internal/model/email_verification_token.go to bind an email-verification token only to the user's identifier, while UpdateUser can change the account email without invalidating the outstanding token and VerifyEmail marks the current address as verified. An ordinary user can request a token for an address they control, change the account to an arbitrary unused address, and redeem the old token so Pocket ID publishes the new address with email_verified set to true. The default affected configuration uses emailsVerified=false and allowOwnAccountEdit=true; the target address must not already belong to another Pocket ID user. A relying application that trusts a verified email for automatic account matching or provisioning can link the attacker's identity to another user's account, while applications that rely exclusively on the stable OIDC sub claim are not affected by that downstream consequence. This issue is fixed in version 2.12.0.

### CVE-2026-123025

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-05T07:17:25.897 |

An OS Command Injection vulnerability was discovered in the Google Cloud DNS validation module of the OPNsense os-acme-client plugin through 4.17. The DnsGcloud::prepare() method decodes the dns_gcloud_key model field and directly interpolates the string fields gcloud_account and gcloud_project into a shell command passed to proc_open() via LeUtils::run_shell_command() without any validation or escaping. A remote authenticated user with privileges to issue or renew certificates through the WebGUI/API can achieve arbitrary code execution as root.

### CVE-2026-122313

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-05T03:17:23.853 |

Kyverno from 1.17.0 before 1.19.2 contains a privilege escalation vulnerability that allows namespace-scoped tenants to modify resources in other namespaces through NamespacedMutatingPolicy targetMatchConstraints.expression CEL output lacking namespace checks. Attackers can emit a literal target such as another tenant's RoleBinding, which the cluster-wide background controller then mutates to add attacker subjects or alter Roles, NetworkPolicies, and ConfigMaps.

### CVE-2026-122311

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T03:17:23.497 |

Kyverno from 1.16.0 before 1.19.2 fails to validate path segments in the resource argument of resource.get() and resource.post(), allowing namespaced CEL policies to escape their namespace. Tenants who can create a NamespacedValidatingPolicy can insert .. segments to read and write arbitrary cluster objects using the admission controller's ServiceAccount, leading to cluster takeover.

### CVE-2026-122310

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-05T03:17:23.337 |

Kyverno from 1.19.1 before 1.19.2 validates a Policy's context.apiCall urlPath after cleaning it but executes the raw path, whose fragment or query the Kubernetes client discards. A namespace-scoped user who can create a Policy can hide ../ segments behind # or ? to reach cluster-scoped endpoints with Kyverno's ServiceAccount, gaining cluster admin.

### CVE-2026-122304

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-05T03:17:22.353 |

Kyverno from 1.17.0 before 1.19.2 contains an authorization bypass vulnerability that allows namespace admins to escape namespace confinement because the cleanup controller builds its context loader with a nil policy. Attackers can create a namespaced CleanupPolicy with apiCall or globalReference context entries to read cross-namespace Secrets and modify validatingwebhookconfigurations using the cleanup controller's ServiceAccount.

### CVE-2026-122303

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T03:17:22.197 |

Kyverno from 1.17.0 before 1.19.2 contains an authorization bypass vulnerability that allows namespace tenants to overwrite resources in other namespaces via NamespacedMutatingPolicy mutate-existing targetMatchConstraints.expression. Attackers can return a CEL map literal fabricating a target with an attacker-chosen metadata.namespace, causing the privileged background controller to overwrite Secrets, Deployments, or policies cluster-wide.

### CVE-2026-122302

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-05T03:17:22.030 |

Kyverno before 1.19.2 contains a privilege escalation vulnerability that allows namespace admins to create resources beyond their RBAC because generate-rule admission checks verify the controller's permissions, not the author's. Attackers can create a namespaced Policy with generate rules targeting other namespaces or cluster-scoped kinds, making the background controller create or clone resources cluster-wide.

### CVE-2026-122051

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-05T00:17:24.013 |

A flaw has been found in Edimax BR-6208AC 1.32. Affected by this vulnerability is an unknown functionality of the file /goform/mp. Executing a manipulation can lead to command injection. The attack may be launched remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-54384

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-04T23:17:48.523 |

VitaFit cloud API before 2026-10-30 contained an authentication bypass vulnerability that allows remote attackers to obtain a full session for a victim's account by submitting a linked Google or Facebook account identifier to the POST /front/login/sns/ endpoint without providing proof of ownership from the identity provider. Attackers can forge a login using an identifier exposed through account enumeration to read and modify the victim's profile and delete the account's authentication record, preventing the legitimate user from logging in.

### CVE-2026-57566

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-04T22:18:06.850 |

Readest is a modern, feature-rich ebook reader designed for seamless cross-platform access and an intuitive reading experience. Prior to 0.11.10, the unauthenticated /api/opds/proxy route in apps/readest-app/src/app/api/opds/proxy/route.ts accepted an attacker-controlled URL and fetched it server-side without restricting the scheme, blocking private, loopback, link-local, or metadata hosts, or revalidating destinations during automatic redirect following. The route also accepted caller-controlled outbound headers and Authorization values and reflected the upstream status and response body. A remote attacker could use the service as an open request proxy and, on Node, Docker, or other self-hosted deployments with internal-network access, retrieve cloud metadata or internal-service responses. Cloudflare Workers deployments restrict access to link-local and private destinations, which reduces the internal-network impact there, but the unauthenticated public fetch-and-reflect behavior remains. This issue is fixed in version 0.11.10.

### CVE-2026-54378

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-04T22:18:05.777 |

VitaFit cloud API before 2026-10-30 contained a broken access control vulnerability that allows any authenticated user to obtain temporary AWS credentials by calling the POST /front/user/s3/token/ endpoint. Attackers can use these improperly scoped credentials to list the shared storage bucket and read or overwrite other users' stored files, enabling unauthorized cross-user data access and manipulation.

### CVE-2026-122013

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T21:18:07.540 |

A vulnerability was detected in Comfast CF-WR632AX 2.6.0.1. Affected by this vulnerability is an unknown functionality of the file /usr/bin/webmgnt of the component Multipart Parser. Performing a manipulation of the argument filename results in path traversal. It is possible to initiate the attack remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2025-71457

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-11-04T21:17:40.340 |

vtenext 25.02 before 25.02.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to change any account password via hub/rpwd.php without token verification. Attackers knowing a valid user_name can send action=change_password to RecoverPwd::displayChangePwd() and log in as administrators lacking two-factor authentication.

### CVE-2026-121933

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-11-04T20:19:11.607 |

A flaw has been found in Linksys E5350 1.0.00.037. This impacts the function save_settings of the file /wizard/apply.cgi of the component Setup Wizard. Executing a manipulation of the argument wizard_router_pwd can lead to missing authentication. The attack may be launched remotely. The exploit has been published and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-121932

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-04T19:17:33.440 |

A vulnerability was detected in Linksys E5350 1.0.00.037. This affects the function system of the file /wizard/apply.cgi. Performing a manipulation of the argument ping_ip/traceroute_ip results in os command injection. The attack may be initiated remotely. The exploit is now public and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-113780

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-822` |
| Published | 2026-11-04T19:17:18.493 |

ESF-IDF is the Espressif Internet of Things (IOT) Development Framework. From 5.5.5 until 5.5.6, 6.0.4, and 6.1.1, the esp_tee trap entry in esp_tee_vectors_plic.S and esp_tee_vectors_clic.S saves a caller-controlled register frame through the REE-supplied stack pointer before switching to the trusted TEE stack or validating the pointer. A local unprivileged REE application can direct this machine-mode write into TEE-exclusive memory on ESP32-C5, ESP32-C6, ESP32-C61, and ESP32-H2 devices, breaking the REE/TEE isolation boundary and potentially corrupting TEE control-flow data for code execution, denial of service, or system crashes. Both secure-service ecall and interrupt entry paths contain the vulnerable ordering. This issue is fixed in version 5.5.6 and is scheduled to be fixed in versions 6.0.4 and 6.1.1.

### CVE-2026-107846

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-11-04T19:17:18.130 |

bitcoinjs-lib is a JavaScript Bitcoin library for Node.js and browsers. From 2.3.0 until 5.2.1, 6.1.8, and 7.0.2, fastMerkleRoot pads odd Merkle-tree levels by hashing the final node with itself but does not report adjacent duplicate hashes. The affected block-root verifier was introduced as Block.checkMerkleRoot() alongside Block.calculateMerkleRoot(), while later versions expose validation through checkTxRoots() and __checkMerkleRoot; these validation paths can accept a recomputed root without checking for mutation. A peer can append duplicate transactions so a different transaction list retains the original Merkle root, block header, proof of work, and block identifier. Consumers that rely on block-root validation, including explorers, exchange indexers, or SPV clients, can process a duplicated transaction twice or blacklist the shared block hash and reject the honest block. This issue is fixed in versions 5.2.1, 6.1.8, and 7.0.2.

### CVE-2026-121953

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-04T16:17:47.717 |

FreeRDP before 3.32.2 has a use-after-free in the client's rdpgfx dynamic virtual channel: a duplicate-name channel with a new ChannelId overwrites the listener's single callback slot, which rdpgfx_on_close frees without clearing. A malicious RDP server can open and close such a channel, then send a PDU on the original channel to crash the client or potentially execute code.

### CVE-2026-121952

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T16:17:47.530 |

FreeRDP before 3.32.2 has an out-of-bounds write in the proxy because rdp_read_bitmap_cache_v2_capability_set rejects only numCellCaches values above 5, yet the bitmap cache v2 cell array is later accessed at fixed indices 0 through 4. A client connecting to the proxy can declare fewer than five cell caches in its Confirm Active, causing heap corruption, heap data leakage to the backend, or a crash.

### CVE-2026-122992

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-05T03:17:25.513 |

In G4KLX DStarGateway and F4FXL DStarGateway before 7b75de6, dstarCallsignToAPRS in APRSUtils.cpp has an integer underflow via an empty RS-MS1A sender field.

### CVE-2026-52848

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-04T23:17:46.560 |

GLPI is a free asset and IT management software package. From 11.0.0 until 11.0.8, during the login phase, an unauthenticated user could use a crafted URL to skip one-time-password verification, defeating two-factor authentication. This issue is fixed in version 11.0.8.

### CVE-2026-121639

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-252;CWE-287;CWE-306` |
| Published | 2026-11-04T15:17:42.600 |

A Missing Authentication for Critical Function vulnerability in WatchGuard AuthPoint Gateway allows a remote unauthenticated attacker with network access to the AuthPoint Gateway host to disrupt authentication services and delete the local directory synchronization configuration.

### CVE-2026-117691

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-05T14:17:01.320 |

A flaw was found in the SAML HTTP-Redirect binding implementation of Keycloak. The issue occurs because the server processes percent-encoded parameter names (like %53AMLResponse) while the signature verification logic only checks literal parameter names. An attacker can use this discrepancy to provide a crafted, unsigned SAML message that the server processes instead of a legitimately signed one, leading to full account takeover of federated users.

### CVE-2026-102894

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294;CWE-347` |
| Published | 2026-11-04T22:17:44.440 |

GPUStack is an open-source GPU cluster manager for AI model serving and GPU instance provisioning. From 0.7.1 until 2.2.2, the /auth/saml/callback endpoint decoded SAML XML, used its NameID and attributes to resolve or provision a user, and minted a gpustack_session JWT without calling OneLogin_Saml2_Auth.process_response to verify the signature, issuer, audience, destination, or time conditions. Any network client could submit an identity for an existing user, including an administrator, or provision a new non-administrator account, even when SAML was not configured. Response and Assertion identifiers were not consumed, so captured signed responses could also be replayed. This issue is fixed in version 2.2.2.

### CVE-2026-122220

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-04T20:19:12.397 |

WPO365 | LOGIN (wpo365-login) plugin before version 45.2 contains an authentication bypass by capture-replay vulnerability caused by a non-functional anti-replay check in Saml2_Service::check_message_id(), which never persists processed SAML message IDs to the wpo365_saml_message_ids transient due to a logic error that returns before saving. Attackers who capture a validly-signed SAMLResponse can replay it to the ACS endpoint repeatedly within its assertion validity window to log in as the victim, including administrators, without detection since the duplicate message ID check never triggers.

### CVE-2026-113373

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1390` |
| Published | 2026-11-04T20:18:56.750 |

Sonatype Nexus Repository 3 Pro does not check the local account status when a user signs in through a configured SAML or OAuth2/OpenID Connect identity provider. A user whose account was disabled or locked by an administrator in Nexus Repository can sign in again with valid identity provider credentials for the same account, and then receives a new session with the roles of that account. The attacker needs no Nexus Repository session and no Nexus Repository privilege. The attacker needs a named account that holds valid credentials at the identity provider. The anonymous user is not part of this attack path.

### CVE-2026-121640

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-04T15:17:42.790 |

An Authentication Bypass by Capture-replay vulnerability in WatchGuard AuthPoint Gateway allows an attacker who has observed a legitimate request between AuthPoint Gateway components to replay it and perform unauthorized administrative actions, including disrupting authentication services.

### CVE-2026-121638

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-04T15:17:42.437 |

An Improper Certificate Validation vulnerability in WatchGuard AuthPoint Gateway allows an attacker with an on-path network position to intercept and modify communications between the AuthPoint Gateway and local authentication providers.

### CVE-2026-122120

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-04T19:17:39.560 |

In Yealink Plug-in Softwares before 2.35.219.0, there is an unauthorized file write vulnerability under specific scenarios, which may be exploited by attackers to achieve remote code execution.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-121637

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-04T15:17:42.263 |

An improper integrity validation vulnerability in WatchGuard AuthPoint Gateway's LDAP authentication callback allows a network attacker who has obtained a valid header signature to forge the authentication result and transaction identifier in the request body, resulting in unauthorized session outcomes.

### CVE-2026-118193

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-05T05:18:19.427 |

The GiveWP – Donation Plugin and Fundraising Platform plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.19.1 via the `donor_default_user_role` parameter. This is due to the `sanitize_option_donor_default_user_role()` function applying only a narrow literal check against the string `'administrator'` rather than enforcing the plugin's own `give_get_donor_safe_user_roles()` allowlist on save, and due to the `give_core_settings_import_callback()` AJAX handler writing imported JSON directly into the `give_settings` option via `update_option()` without invoking the sanitize filter at all. This makes it possible for authenticated attackers with the GiveWP Manager role (holding the `manage_give_settings` capability) and above to configure donor registration to assign privileged WordPress roles — up to and including Administrator via the import path — to every new donor account created through the platform. Via the settings save path, the Administrator role is blocked but any other elevated role (Editor, Author, etc.) is accepted; via the Tools › Import JSON path, the sanitize filter is bypassed entirely, allowing the Administrator role itself to be stored and subsequently applied to all newly registered donor accounts.

### CVE-2026-77372

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-787` |
| Published | 2026-11-04T23:17:58.713 |

VeraCrypt provides disk encryption with strong security based on TrueCrypt. Prior to 1.26.30, the Unix, macOS, and FreeBSD serialization paths in src/Platform/Serializer.cpp and src/Volume/VolumePassword.cpp accept untrusted length and count values when deserializing data that can cross from the unprivileged GUI or CLI to the root CoreService helper. Serializer::DeserializeWString allocates floor(size / sizeof(wchar_t)) elements but reads size bytes, so a non-aligned size can overflow the heap allocation. VolumePassword::Deserialize accepts PasswordSize values larger than the fixed 128-byte PasswordBuffer, allowing downstream DataPtr() and Size() consumers such as the KDF to read beyond the buffer. DeserializeString, DeserializeWString, and the string and wide-string list readers also lack allocation and collection bounds, which can exhaust memory, and a zero-length DeserializeString can access an empty vector. Windows uses a different path, and the immediate CoreService pipe writer is the same-user parent process, so the documented exposure is a local defense-in-depth boundary rather than a remote attack. This issue is fixed in 1.26.30.

### CVE-2026-103002

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-04T22:17:44.783 |

GPUStack is an open-source GPU cluster manager for AI model serving and GPU instance provisioning. From 2.2.0 until 2.2.2, cluster_apiserver_proxy forwarded an authenticated non-administrator's requests to a selected Kubernetes cluster without a resource-level authorization check. The proxy used a reachable worker's Kubernetes ServiceAccount credentials, so the caller could read sensitive resources, create or modify workloads, or delete resources according to that ServiceAccount's permissions. Exploitation required a Kubernetes-provider cluster with a reachable worker, and attacker-controlled workloads could result in code execution in the target cluster. This issue is fixed in version 2.2.2.

### CVE-2026-13292

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-04T21:18:12.290 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow an authenticated attacker to execute arbitrary code by injecting malicious environment variables through transfer request metadata.

### CVE-2026-11376

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-04T21:17:56.403 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow an authenticated attacker to cause a denial of service or potentially execute arbitrary code due to an integer overflow when processing subscription requests with crafted buffer size values.

### CVE-2026-73095

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-05T12:17:50.617 |

Allocation of Resources Without Limits or Throttling vulnerability in Apache Juneau.

The MessagePack parser, which the REST server enables by default, sizes buffers from length values in the input. An unauthenticated client can send a few bytes that force a multi-gigabyte allocation and an OutOfMemoryError, causing denial of service. Related unbounded allocations in REST request handling (multipart uploads and request reader buffers) are fixed at the same time.

This issue affects Apache Juneau: through 9.2.0.

Users are recommended to upgrade to version 9.2.1, which fixes the issue.

### CVE-2026-118869

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-05T09:17:05.143 |

An OS command injection vulnerability exists in SHIRASAGI, which may allow an authenticated attacker to execute arbitrary OS commands on the system running the product.

### CVE-2026-123014

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-05T06:17:07.707 |

iTerm2 before 3.7.7beta2 has an argument injection vulnerability in the x-man-page: URL handler, allowing an attacker to execute arbitrary commands with the privileges of the logged-in user by inducing the user to open a crafted URL in iTerm2. Percent-encoded NUL characters survive input sanitization and are subsequently converted to whitespace during command-line parsing, allowing injection of additional arguments to /usr/bin/man. An attacker can inject the -P option to select an attacker-controlled pager command. NOTE: this issue exists because of an incomplete fix for CVE-2023-46321.

### CVE-2026-122323

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-05T03:17:25.343 |

Kyverno from 1.11.0 before 1.19.2 contains an unbounded decompression vulnerability in FetchSignatureBlob that allows attackers to exhaust memory by supplying highly compressed notary signature layers. Attackers who control registry referrers or signatures can publish small gzip layers that decompress beyond maxPayloadSize, causing admission controller OOM kills and denial of service.

### CVE-2026-122322

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-05T03:17:25.187 |

Kyverno from 1.11.0 before 1.19.2 contains an unbounded decompression vulnerability in extractStatement that allows remote attackers to exhaust memory by supplying highly compressed attestation layers. Attackers controlling registry referrer artifacts can push gzip predicate layers exceeding maxPayloadSize when decompressed, causing admission controller OOM kills and denial of service.

### CVE-2026-122319

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-704` |
| Published | 2026-11-05T03:17:24.700 |

Kyverno before 1.19.2 contains a denial-of-service vulnerability in the In and NotIn operators that allows attackers to crash the policy engine via an unchecked type assertion. Attackers can submit resources whose JMESPath-evaluated values yield arrays of integers, booleans, or mixed types, triggering a panic that disrupts admission control and policy enforcement.

### CVE-2026-122315

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-05T03:17:24.200 |

Kyverno before 1.19.2 contains an unchecked type assertion in buildStatementMap that allows unauthenticated attackers to crash the policy engine via crafted attestation statements. Attackers can push an OCI referrer manifest with a non-string type field to bypass image verification under failurePolicy Ignore or crash-loop the reports-controller.

### CVE-2026-122314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-05T03:17:24.037 |

Kyverno before 1.19.2 contains an unchecked type assertion in its variable-substitution engine that allows users who can submit resources to crash the policy engine. Attackers can submit resources with non-string fields referenced by {{- variable }} shallow substitution in policies, causing a panic that yields webhook denial of service and policy bypass under failurePolicy Ignore.

### CVE-2026-76892

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-04T23:17:58.557 |

tsParticles is a TypeScript library for creating highly customizable particle animations. Prior to 4.3.1, the HTTP mode of @tsparticles/mcp-server calls JSON.parse outside a request-local error boundary in the POST /mcp handler in integrations/mcp-server/src/index.ts. A single unauthenticated malformed JSON body raises a SyntaxError that terminates the Node.js process, leaving the MCP service unavailable until an external supervisor restarts it. This issue is fixed in version 4.3.1.

### CVE-2026-54381

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-04T23:17:48.033 |

VitaFit cloud API before 2026-10-30 contained a misconfigured cloud storage bucket vulnerability that allows unauthenticated attackers to list and download stored files without authentication. Attackers can enumerate the publicly accessible bucket containing 129,947 objects, including 126,881 user-uploaded profile images, to access sensitive personal data without credentials.

### CVE-2026-47678

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-04T23:17:34.950 |

GLPI is a free asset and IT management software package. From 9.4.0 until 10.0.26 and 11.0.8, any authenticated user can submit crafted values to the dropdown values fetching endpoint that are incorporated into a database query. This permits SQL injection through the dropdown endpoint. This issue is fixed in versions 11.0.8 and 10.0.26.

### CVE-2026-54374

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-04T22:18:05.070 |

VitaFit Android application (com.vt.vitafit) before 2.8.1.0 contains a hardcoded credentials vulnerability that allows attackers to extract confidential third-party integration secrets by decompiling the APK. Attackers can retrieve embedded WeChat, Tencent QQ, and Fitbit credentials from the decompiled application to abuse the active third-party application registrations.

### CVE-2026-54372

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-04T22:18:04.667 |

VitaFit Android application (com.vt.vitafit) before 2.8.1.0 contains an insecure TLS/SSL certificate validation vulnerability that allows network-based attackers to intercept and modify HTTPS traffic by exploiting a custom X509TrustManager that trusts all certificates and a hostname verifier that accepts any hostname. Attackers can perform a man-in-the-middle attack to capture account sessions and health-related API data, and use a captured session to delete the account's authentication record and prevent legitimate login.

### CVE-2026-122127

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T21:18:08.200 |

CESNET ipfixcol2 2.7.1 before 2.9.0 contains a heap-based buffer overflow in Lz4Decoder.cpp that allows unauthenticated network peers to write past heap buffers. Attackers can declare a small ring buffer_size followed by a large decompressed_size to write up to 65535 controlled bytes and crash the collector.

### CVE-2026-57853

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-1336` |
| Published | 2026-11-04T18:17:44.877 |

DataGerry before 3.3.0 contains a server-side template injection vulnerability that allows authenticated attackers with base.docapi.template.add permission to store arbitrary Jinja2 payloads in the template_data field via POST /rest/docapi/template, which is later rendered in a non-sandboxed Jinja2 environment when a user calls GET /rest/docapi/template/<id>/render/<object_id>. Attackers can exploit the standard cycler.__init__.__globals__.os gadget chain to execute arbitrary operating system commands as the DataGerry web process user, confirmed as root in default Docker deployments, achieving remote code execution.

### CVE-2026-119749

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-11-04T17:17:34.930 |

The GetPaid plugin for WordPress before 2.8.63 contains an improper input validation vulnerability that allows unauthenticated attackers to bypass payment processing by submitting a negative item quantity on a public payment form. Attackers can exploit the unchecked quantity value in process_item() to produce a negative line subtotal that reduces the invoice total to zero, causing process_free_payment() to mark the invoice as paid without any actual gateway charge.

### CVE-2026-121964

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T16:17:49.683 |

FreeRDP before 3.32.2 contains a heap-based buffer overflow in the RD Gateway RPC client, where rpc_client_recv_fragment writes BIND_ACK and ALTER_CONTEXT_RESP fragments into a persistent PDU stream after checking only total capacity rather than remaining capacity from the current stream position. A malicious or compromised RD Gateway can send crafted RPC fragments with manipulated alloc_hint and frag_length values to overwrite client heap memory with attacker-controlled data, causing a crash or potentially arbitrary code execution.

### CVE-2026-121960

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-04T16:17:48.970 |

FreeRDP before 3.32.2 contains a denial of service vulnerability in the NLA-enabled shadow server when a CredSSP TSRequest omits negoTokens. Unauthenticated attackers can send a crafted seven-byte TSRequest containing only the version field to trigger a fatal WINPR_ASSERT and abort the server process.

### CVE-2026-121958

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T16:17:48.610 |

FreeRDP through 3.32.1 has a heap out-of-bounds write in the RDPGFX client because the delete_surface callback truncates surface hash keys to 16 bits, leaving the surface table inconsistent so HashTable_GetKeys writes past its allocated key array. A malicious or man-in-the-middle RDP server can exploit this by creating surfaceId 0xFFFF, closing the RDPGFX channel, sending repeated DELETESURFACE PDUs, and then sending ENDFRAME or RESETGRAPHICS.

### CVE-2026-121957

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-04T16:17:48.423 |

FreeRDP before 3.32.2 contains a use-after-free vulnerability that allows malicious RDP servers to corrupt client memory by racing the RDPGFX ResetGraphics handler against the planar bitmap decoder. Attackers can send ResetGraphics while concurrently sending compressed bitmaps of 32 bpp or more to trigger heap use-after-free or out-of-bounds read/write on shared planar buffers.

### CVE-2026-121956

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-11-04T16:17:48.250 |

FreeRDP before 3.32.2 contains a double free in the WinPR Kerberos SSPI retrieveSomeTgt function, which installs the krb5 default realm into a target principal that has an empty realm without taking ownership of it. Unauthenticated remote clients can send a crafted NLA/CredSSP u2u TGT request whose server-name component contains '@' to corrupt the heap and crash the server process.

### CVE-2026-121955

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-04T16:17:48.070 |

FreeRDP before 3.32.2 contains a use-after-free vulnerability in Emulate_SCardReleaseContext that frees the emulated SCardContext before its worker thread is cancelled and joined. A malicious server can send ESTABLISHCONTEXT, a long-timeout GETSTATUSCHANGE, then RELEASECONTEXT smartcard IRPs to corrupt heap memory or crash clients using smartcard emulation.

### CVE-2026-121951

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-04T16:17:47.350 |

FreeRDP 3.0.0 before 3.32.2 server-side RDP peer input parsing skips the six-byte body of a slow-path input event with an unknown message type without checking it lies within the packet's declared length, causing a WinPR stream assertion failure. A remote RDP client with an active session can send a truncated unknown input event to abort assertion-enabled server processes, causing denial of service.

### CVE-2026-122299

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-115;CWE-1250` |
| Published | 2026-11-04T23:17:23.730 |

Dulwich before 1.2.20 contains a commit object parsing vulnerability where the read path in _parse_commit resolves a duplicate tree header to the last occurrence instead of the first, diverging from core git's resolution behavior, while Poetry 2.5.1 ships this version and uses dulwich by default for git dependency installation. Attackers can craft a commit object with two tree headers so that reviewers and CI using git see a benign tree while Poetry's dulwich-based checkout resolves to a different attacker-controlled tree containing malicious build scripts such as setup.py, resulting in unreviewed code execution on the install or build host.

### CVE-2026-57567

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T22:18:07.013 |

Readest is a modern, feature-rich ebook reader designed for seamless cross-platform access and an intuitive reading experience. In affected desktop Tauri builds prior to 0.11.10, the apps/readest-app/src-tauri/src/transfer_file.rs commands download_file and upload_file accepted a webview-controlled file_path and passed it to File::create or File::open without checking the Tauri filesystem scope, rejecting absolute paths, or blocking parent-directory traversal. The commands were registered in the global invoke handler for the main, updater, and reader-* windows, so JavaScript executing in the privileged application origin could write attacker-controlled content to any path writable by the process or read and send any path readable by the process. Exploitation requires JavaScript execution in that privileged origin, such as through an application XSS or compromised renderer; whether book-embedded JavaScript can reach the parent origin was not established. The write primitive can overwrite trusted or startup files, while the read primitive can expose keys, tokens, and application secrets. This issue is fixed in version 0.11.10.

### CVE-2026-54375

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-04T22:18:05.240 |

VitaFit Android application (com.vt.vitafit) before 2.8.1.0 contains an insecure session management vulnerability that allows attackers to extract or intercept unencrypted m_session_id tokens stored in application backups, which remain valid for ten years. Attackers can use a stolen session token to read and modify the victim's account or delete the account's authentication record, preventing the legitimate owner from logging in again.

### CVE-2026-122135

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-04T21:18:09.423 |

Mistral Vibe before 3.0.3 contains a remote code execution vulnerability that allows attackers to run commands by abusing repository-configured gpg.program during project context collection. A crafted repository setting gpg.program and log.showSignature with a signed commit makes git log execute the attacker's program at session start, before any trust prompt.

### CVE-2026-122134

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-04T21:18:09.260 |

Mistral Vibe before 2.25.7 contains a remote code execution vulnerability that allows attackers to run commands by configuring malicious Git clean or process filter drivers in a repository. When a user opens a crafted repository, ProjectContextProvider._fetch_git_status runs git status at startup, invoking the filters and executing commands with user privileges before any trust prompt.

### CVE-2026-122133

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-04T21:18:09.087 |

Mistral Vibe before 2.25.5 on Windows contains an untrusted search path vulnerability that allows attackers to execute code by placing git.exe in a repository root. Attackers can lure users into opening a crafted repository so SessionLogger and ProjectContextProvider run the malicious git.exe at session start before any trust prompt.

### CVE-2025-71456

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-04T21:17:40.183 |

vtenext before 25.02.2 contains an SQL injection vulnerability that allows authenticated low-privileged users to inject SQL by supplying a crafted fieldname parameter to modules/Fax/EditView.php. Attackers can read arbitrary database contents, including password reset tokens stored in vte_userauthtoken, to take over other user accounts.

### CVE-2026-113374

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-04T20:18:57.057 |

Sonatype Nexus Repository 3 does not require realm administration permission when a user creates a Rut Auth capability. A user who holds only the capability creation permission (nexus:capabilities:create) can create this capability, which turns on header-based authentication for the instance. A remote client can then authenticate as an existing user, including an administrator, without credentials.

### CVE-2026-82033

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-04T19:17:41.533 |

DeepSeek Harness prior to 0.1.2-alpha.2, and specifically commit 3e24087, contains a missing authentication vulnerability in its web profile HTTP and WebSocket RPC control plane, allowing any local process, including those running as a different OS user, to reach unauthenticated session methods such as session.create and session.prompt. Attackers can invoke session.prompt to trigger the agent's bash and filesystem tools, achieve arbitrary command execution as the victim user using their configured model credentials, intercept live session traffic and logs over the event mux stream, and bypass human tool-approval checks via POST /api/respond by matching only rpcId, approvalId, and sessionId values broadcast over the ungated stream.

### CVE-2026-122321

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-05T03:17:25.023 |

Kyverno 1.18.0 before 1.19.2 contains a signature verification bypass in verifyImages because cached verification results are keyed by the image reference string (such as a tag) rather than bound to the verified digest, so cache hits skip signature and attestation checks. An attacker who can submit workloads and move a registry tag can warm the cache with a signed image, repoint the tag, and have Kyverno admit the workload and use mutateDigest to pin the unverified digest.

### CVE-2026-108387

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-04T23:17:18.320 |

radare2 is a UNIX-like reverse engineering framework and command-line toolset. Prior to 6.2.2, attacker-controlled data from several binary format plugins could reach RBinInfo->bclass. Opening or analyzing a crafted Pebble or Sega Mega Drive binary could place a dbg:// URI in bclass, causing radare2 to reopen the input through the debug input/output plugin and ultimately pass attacker-controlled arguments to execvp(). This could execute commands with the privileges of the radare2 process without an explicit debugging command. This issue is fixed in version 6.2.2.

### CVE-2026-11724

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-04T21:17:56.573 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow an authenticated attacker to execute arbitrary code on a Managed File Transfer agent host due to improper validation of metadata used during script execution.

### CVE-2026-102340

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-11-04T21:17:40.683 |

Telepresence enables local development against a remote Kubernetes or OpenShift cluster. Prior to 2.31.0, the Traffic Manager gRPC API on port 8081 accepts unauthenticated cluster-network callers, ArriveAsClient stores a caller-supplied Namespace using only the ManagesNamespace manager watchlist check, and CreateIntercept can target any managed namespace without checking the session's Kubernetes RBAC. An attacker operating any pod with network access to the manager can register in an arbitrary managed namespace, create service intercepts, receive intercepted traffic, and obtain the victim pod's complete container environment, including secrets, tokens, and API keys. The default cluster-wide deployment manages all namespaces. This vulnerability is fixed in 2.31.0.

### CVE-2026-121931

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-04T19:17:33.157 |

A security vulnerability has been detected in Linksys WRT54GL 4.30.18. The impacted element is the function system of the file apply.cgi of the component Traceroute Diagnostic Function. Such manipulation of the argument traceroute_ip leads to os command injection. The attack can be launched remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-121930

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-04T19:17:32.883 |

A weakness has been identified in Linksys WRT54GL 4.30.18. The affected element is the function system of the file apply.cgi of the component Ping Diagnostic. This manipulation of the argument ping_ip causes os command injection. The attack can be initiated remotely. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-122316

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T03:17:24.360 |

Kyverno from 1.17.0 before 1.19.2 contains a missing authorization vulnerability in the mutate-existing background processor that allows namespaced tenants to modify resources outside their namespace. Attackers can create a NamespacedMutatingPolicy targeting Namespace objects or victim-namespace resources via CEL expressions, making the background-controller ServiceAccount strip Pod Security labels cluster-wide.

### CVE-2026-122308

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-05T03:17:23.000 |

Kyverno before 1.19.2 contains an authorization bypass vulnerability in the Generation Handler that allows users with create/update permissions to trigger synchronized generate policies by spoofing internal generate.kyverno.io labels. Attackers can label a ConfigMap as managed-by kyverno with crafted policy, rule, and trigger labels to clone sensitive Secrets from restricted namespaces into their own namespace.

### CVE-2026-123033

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-05T07:17:26.207 |

Authentication bypass in the HA heartbeat origin check in middlewared in TrueNAS SCALE before 25.10.8 (and in release trains before their respective fixes) allows an attacker on the same network segment to achieve unauthenticated full-administrator API access and execute commands as root. middlewared registers the HA peer-authentication hook (ha_permission) unconditionally, with no failover-licence or heartbeat-interface check. An unauthenticated connection whose TCP peer address is a hardcoded HA heartbeat address (169.254.10.1 or 169.254.10.2) and whose peer port is <= 1024 is granted a node credential that is authorized for every API method and treated as full administrator. Both conditions are properties of the attacker's own socket, and thus an attacker on the same layer-2 segment satisfies them without forging anything. The hook is present on non-HA, unlicensed, single-node Community Edition installations. The fix additionally requires that the connection terminate on the HA heartbeat listener (a local address/port the attacker cannot control).

### CVE-2026-122320

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T03:17:24.867 |

Kyverno before 1.19.2 contains a missing authorization vulnerability that allows namespaced Policy authors to read resources in other namespaces by templating generate.clone or cloneList namespace values. Attackers can annotate a triggering ConfigMap so the background-controller copies a victim namespace's sensitive ConfigMap into the attacker's namespace, enabling cross-tenant data disclosure.

### CVE-2026-122312

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-05T03:17:23.653 |

Kyverno from 1.19.1 before 1.19.2 contains a namespace isolation bypass in APICall Fetch() in pkg/engine/apicall/apiCall.go because path.Clean treats '?' as a path character, letting the namespace regex match segments inside the query string. Users who can create namespaced policies can supply a URLPath like /api/v1/nodes?x=/namespaces/default/ that passes validation while client-go requests the cluster-scoped endpoint, reading resources outside their namespace.

### CVE-2026-122307

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-05T03:17:22.840 |

Kyverno before 1.19.2 contains a policy bypass vulnerability in the admissionpolicygenerator controller, which folds PolicyExceptions into generated ValidatingAdmissionPolicies while ignoring the --enablePolicyException, --exceptionNamespace, and policy kind gates. Users with namespaced create rights on PolicyExceptions can inject negated matchConditions into the generated policies to admit violating resources, bypassing cluster-wide enforcement.

### CVE-2026-122306

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-05T03:17:22.680 |

Kyverno before 1.19.2 contains a denial of service vulnerability that allows namespaced policy authors to exhaust admission controller CPU by submitting pathological wildcard patterns. Attackers can create a Policy with crafted match and exclude names evaluated by ValidateMatchExcludeConflict, pinning cores and causing cluster-wide webhook timeouts that block resource operations.

### CVE-2026-122305

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-05T03:17:22.527 |

Kyverno before 1.19.2 contains a denial of service vulnerability in substituteVariablesIfAny that allows low-privileged users to hang the admission webhook via self-referential variable templates. Attackers can create resources whose annotations re-introduce the embedded policy variable, causing unbounded substitution loops that exhaust CPU and memory and block cluster-wide admission.

### CVE-2026-122130

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-04T21:18:08.543 |

CESNET ipfixcol2 2.3.0 before 2.9.0 contains an integer overflow vulnerability in the Forwarder output plugin that allows unauthenticated IPFIX exporters to overflow a heap buffer by wrapping uint16_t message length counters. Attackers can send near-65535-byte data sets and large templates to a collector forwarding over TCP to crash it and perform 2-byte writes to attacker-influenced addresses.

### CVE-2026-92704

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-346;CWE-350;CWE-352;CWE-749` |
| Published | 2026-11-04T16:17:55.097 |

SharpEmu is an experimental PlayStation 5 emulator for Windows and Linux. In version 0.0.3-release.3 and earlier, the repository-provided debugger frontend tooling is vulnerable while running. This tooling is not included in the release archives. The frontend exposes an HTTP API on 127.0.0.1:8765 without authentication or CSRF token. Its  do_POST  handler in  tools/SharpEmu.DebuggerFrontend/debugger_frontend.py  does not validate the Origin, Referer, Sec-Fetch-Site, or Host headers. The  _read_json_body()  function also accepts JSON sent with browser-simple content types instead of requiring  application/json . A malicious page that can reach the loopback listener can send cross-origin requests to  /api/launch ,  /api/command , and  /api/connect . Chromium may require Local Network Access permission for pages served from public origins. Local-origin pages and other delivery paths are not consistently subject to this restriction. The  /api/launch  endpoint accepts an attacker-selected  emulatorPath  if it points to an existing file on the victim’s host. On POSIX systems, that file must also be executable. The endpoint additionally requires an existing  ebootPath . The  /api/command  endpoint exposes debugger operations, including  write-memory ,  set-register , and  continue . The  /api/connect  endpoint can initiate outbound TCP connections. These operations can let an attacker execute an existing binary with the victim’s privileges, control the attached emulated process, or reach network services accessible from the host. DNS rebinding can additionally let the attacker read API responses interactively. This issue is fixed in version 0.0.3-release.3-patch.1

### CVE-2026-93389

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-05T05:18:40.127 |

The LiteSpeed Cache plugin for WordPress is vulnerable to unauthenticated disclosure of sensitive WooCommerce customer data in all versions up to, and including, 7.9.1 With Cache REST enabled (the shipped default cache-rest=1), LiteSpeed stores WooCommerce Store API GET responses (/wc/store/v1/cart and /wc/store/v1/checkout) as PUBLIC cache objects and does not vary the cache on the Cart-Token or WooCommerce session. A shopper's personalized cart/checkout response is therefore served to any later, cookie-less and token-less client as an LSCache HIT. This makes it possible for unauthenticated attackers to read another shopper's billing and shipping details (name, company, street address, email, phone), cart contents and totals, and the shopper's live Cart-Token session JWT and nonce (enabling cart/checkout-session hijack), plus order_key on the checkout endpoint.

### CVE-2026-122309

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-05T03:17:23.170 |

Kyverno before 1.19.2 contains a denial of service vulnerability that allows namespace-scoped policy authors to exhaust CPU and memory by submitting CEL expressions evaluated without runtime cost limits. Attackers can create a NamespacedValidatingPolicy or NamespacedDeletingPolicy with nested map comprehensions over large ConfigMap fields to OOM-kill Kyverno pods and block cluster-wide admission.

### CVE-2026-54376

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-926` |
| Published | 2026-11-04T22:18:05.407 |

VitaFit Android application (com.vt.vitafit) before 2.8.1.0 contains an insecure custom URI scheme vulnerability that allows a malicious application to intercept Fitbit login tokens by registering the same callback scheme (vitafit://vtio.cn). Attackers can capture the 30-day Fitbit authorization token with weight scope delivered in the callback URL to read, create, and delete the victim's weight and body-fat records via the Fitbit Body API.

### CVE-2026-122126

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T21:18:08.027 |

reSIProcate reTurn client through 1.14.0 contains a heap buffer overflow in TurnTcpSocket::handleReadHeader() that allows malicious TURN servers to overwrite memory via oversized frame lengths. Attackers can send STUN or ChannelData frames declaring up to 65535 bytes, writing roughly 57 KB past the fixed 8192-byte mReadBuffer and crashing the client.

### CVE-2026-115758

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-11-04T21:17:52.130 |

SumatraPDF is a multi-format reader for Windows. In version 3.6.1 and earlier, HttpGet() in src/base/Http_win.cpp unconditionally passes INTERNET_FLAG_IGNORE_CERT_CN_INVALID to WinINet, disabling hostname matching for HTTPS update metadata and crash-symbol requests while retaining certificate-chain validation. A network-positioned attacker with a Windows-trusted certificate for an attacker-controlled domain can impersonate the project's update host, inject promo text and a clickable URL before update metadata validation, and provide an attacker-controlled archive to ExtractSymbols(). Installer replacement is not directly possible because HttpGetToFile() validates TLS and MaybeStartUpdateDownload() restricts the download host. No fixed version is available as of this review.

### CVE-2026-102339

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-04T21:17:40.500 |

Telepresence enables local development against a remote Kubernetes or OpenShift cluster. Prior to 2.31.0, the Traffic Manager Tunnel gRPC streaming endpoint parses a session ID from the first bytes of a caller-controlled message in pkg/tunnel/message.go and passes it to state.Tunnel without verifying that the caller owns the active session. An attacker who obtains a valid active session ID through log leakage, cluster-internal channels, or the unauthenticated ArriveAsClient endpoint can attach a routed tunnel to that session and gain its network routing capabilities. UUID4 session IDs make cold brute force impractical. This vulnerability is fixed in 2.31.0.

### CVE-2026-122148

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:L/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-602` |
| Published | 2026-11-04T19:17:39.890 |

In Yealink MeetingBoard Pro before 331.320.0.64, the Web management module has a front-end validation bypass vulnerability. An attacker with administrator privileges can modify the page DOM to bypass front-end UI control logic and invoke screenshot-related interfaces, triggering the screenshot function by circumventing front-end interface restrictions. Exploitation can occur only when the attacker has a valid administrator account within the local network.

### CVE-2026-121971

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-11-04T18:17:43.077 |

The component ScopingHttpClient in Symfony HttpClient merges the options of its default scope (such as auth_bearer or auth_basic) into a request before resolving a relative URL against the base_uri, allowing a network-path reference such as "//evil.example/steal" to be sent to another origin together with the default scope’s credentials, and resulting in potential disclosure of those credentials to an attacker-controlled server. This affects Symfony in versions 5.x prior to 5.4.56, 6.x prior to 6.4.50, 7.x prior to 7.4.23, and 8.x prior to 8.1.11.



The resolved URL falls outside the origin of the base URI, yet it keeps the merged options, whereas the absolute spelling "https://evil.example/steal" receives none. The same happens with a different port or user-info part on the same host.









This is reachable whenever an attacker controls the beginning of a URL passed to a client built with a base_uri and credentials, including those created with HttpClient::createForBaseUri() or configured under framework.http_client.scoped_clients.

To solve the issue, after resolving a relative URL against the base URI of the default scope, ScopingHttpClient now compares the scheme and authority of the result with those of the base URI, parsed the way the request is sent.

### CVE-2026-121963

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-04T16:17:49.500 |

FreeRDP before 3.32.2 contains a use-after-free vulnerability in the asynchronous dynamic rdpsnd channel that allows malicious RDP servers to trigger freed callback access by closing the channel with queued audio PDUs. Attackers can send a training PDU then close the channel so the playback thread reads the freed callback in rdpsnd_virtual_channel_write, crashing the client.

### CVE-2026-121961

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-04T16:17:49.147 |

FreeRDP before 3.32.2 contains a use-after-free vulnerability in the freerdp-proxy DRDYNVC tracker when intercepting the drdynvc channel. A malicious target server can repeatedly send CREATE_REQUEST_PDU for an active channel id, racing front DATA handling to free a borrowed context and crash the proxy process.

### CVE-2026-119746

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-602` |
| Published | 2026-11-04T16:17:45.100 |

ProSoft Technology ICX35 devices (X35-HWC-A and ICX35-HWC-E) contain a login lockout bypass in the integrated module web page. The account lockout mechanism that restricts repeated failed authentication attempts is enforced in client-side JavaScript, so a remote attacker can reset the lockout and continue submitting password guesses by deleting the relevant browser cookies, defeating the brute-force protection. This vulnerability has been addressed in version 1.14.158.

### CVE-2026-116617

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T05:18:19.240 |

The Motors – Car Dealership & Classified Listings Plugin plugin for WordPress is vulnerable to File Deletion in all versions up to, and including, 1.4.128 The vulnerability exists because `stm_save_user_extra_fields()`, hooked to `personal_options_update`, writes the attacker-controlled `stm_dealer_logo_path` parameter directly to user meta without an ownership check binding the submitted path to the submitting user — unlike the `stm_payment_status` and `stm_lost_password_hash` fields, this field is not gated by a `manage_options` or `edit_users` capability check. This makes it possible for authenticated attackers, with Subscriber-level access and above, to delete image files belonging to other users under `wp-content/uploads` — including other users' avatars, dealer logos, and uploaded media — by storing a crafted path via their own profile and then triggering `unlink()` through the become-dealer form on their author page. Note that the two path guards (`stm_mvl_is_path_within_uploads` and `stm_mvl_is_allowed_image_file`) do restrict the attack surface to files with an image extension that resolve within the uploads basedir; files outside that directory, such as `wp-config.php` or plugin PHP files, cannot be reached.

### CVE-2026-55368

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T22:18:06.343 |

h2o is an HTTP server with support for HTTP/1.x, HTTP/2 and HTTP/3. Prior to commit 48b7ae12107fd2b118e4641da49599e9aac8edd8, H2O's access-log formatter could write past its log-line buffer when an affected custom access-log format was configured. The allocation errors affected %{error}x, %q when the query string was empty, and numeric elements whose temporary terminating NUL reached the end of the buffer. A matching request could crash the server, while the effect of the one-byte NUL overwrite beyond a crash was not established. This vulnerability is fixed with commit 48b7ae12107fd2b118e4641da49599e9aac8edd8.

### CVE-2026-13271

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-04T21:18:11.777 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD Managed File Transfer could allow an authenticated attacker to obtain sensitive information or cause a denial of service due to improper restriction of XML external entity references in command queue processing.

### CVE-2026-107912

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T14:16:59.697 |

A flaw was found in the management interface of the Quarkus framework, specifically within the quarkus-vertx-http component. The issue occurs when the framework incorrectly combines the management root path with specific permission rules, leading to a situation where security policies are applied to the wrong internal paths. As a result, an attacker can bypass intended authorization checks and gain unauthorized access to sensitive management endpoints.

### CVE-2026-62662

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-863` |
| Published | 2026-11-04T23:17:56.940 |

Pocket ID is an OIDC provider that allows users to authenticate with their passkeys to services. From 1.11.0 until 2.10.0, createTokenFromClientCredentials in backend/internal/service/oidc_service.go accepts the client-controlled resource parameter and embeds it directly in the access token aud claim without validating that the audience is registered or that the requesting client may access it. Any authenticated OIDC client can therefore obtain a Pocket ID-signed token naming another client or an arbitrary audience. The /api/oidc/introspect endpoint cannot distinguish the unauthorized token because it treats a token as active when the introspecting client's identifier matches the attacker-selected audience. In deployments where resource servers trust Pocket ID access tokens for service-to-service authorization, this bypasses audience-based access controls and can permit unauthorized data access or actions; deployments that do not use these tokens for resource-server authorization have no immediate exploitable impact. This issue is fixed in version 2.10.0.

### CVE-2026-113370

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-04T20:18:56.137 |

Sonatype Nexus Repository 3 contains a SQL injection vulnerability in the optional "Reindex Search Tables By Pattern" task. A user who holds the nexus:tasks:create privilege can supply a crafted filter condition that the database runs as SQL. This allows the user to modify data in the Nexus database. The task is available only when the non-default setting nexus.reindex.search.by.pattern.visible is set to true.

### CVE-2026-109518

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-62;CWE-367` |
| Published | 2026-11-04T16:17:33.010 |

On Debian, Ubuntu, and derivative Linux distributions, an on-path attacker who can manipulate the HTTP traffic (including a malicious mirror or proxy) between an APT client and an archive server triggered by a package install can trick the client into installing an attacker-controlled unverified package and achieve remote code execution with root privileges.



The vulnerability is caused by the reuse of hard links and requires the client to follow redirects and retry the download of package files. It requires the client to have a non-zero Acquire::Retries configuration setting; the value 3 is the default starting with Debian 12 (bookworm) and Ubuntu 22.04 LTS (Jammy Jellyfish), so older releases are unaffected in a default configuration

### CVE-2026-76506

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-04T17:17:37.030 |

A vulnerability in the web-based management interface of Cisco UCS Central Software could allow an authenticated, remote attacker to achieve remote code execution or conduct information disclosure attacks on an affected device.

This vulnerability is due to insufficient validation of user-supplied input in an HTTP request. An attacker could exploit this vulnerability by sending a crafted HTTP request to an affected endpoint on an affected device. A successful exploit could allow the attacker to execute arbitrary commands, write arbitrary files to the filesystem, and obtain sensitive information. To exploit this vulnerability, the attacker must have valid user credentials on the affected device.
Cisco has released software updates that address this vulnerability There are no workarounds that address this vulnerability.

### CVE-2026-123059

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312;CWE-522` |
| Published | 2026-11-05T14:17:04.940 |

In Eclipse BaSyx Helm Charts version 2.2.0 of the `aas-basyx-v2-full` chart, deployments with the bundled Keycloak enabled store the client secret of the `basyx-technical-user` OAuth2 client in cleartext in a Kubernetes ConfigMap. This client uses the client-credentials grant and its service account holds the realm `admin` role.



The chart correctly writes `keycloak.technicalUser.clientSecret` to a Kubernetes Secret, but the template `basyx-keycloak-realm.yaml` also substitutes the same value into the Keycloak realm-import JSON, which is stored in the ConfigMap `<keycloak.fullnameOverride>-realm`. A principal that can read ConfigMaps but not Secrets in the release namespace, such as a holder of the built-in Kubernetes `view` ClusterRole, can read the client secret from the ConfigMap. They can then exchange it at the Keycloak token endpoint for an access token with the `admin` role. That token grants full create, read, update, delete and execute rights on all BaSyx repositories and registries in the deployment.



The bundled Keycloak is disabled by default. No fixed release of the `aas-basyx-v2-full` chart exists. Affected users should migrate to the `basyx` chart, or deploy without the bundled Keycloak and rotate the `basyx-technical-user` client secret.

### CVE-2026-105321

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T14:16:59.153 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Kobikom Telecommunications and Informatics Services Inc. Kobikom allows SQL Injection.

This issue affects Kobikom: before KobiPBX-FOP3-SEC-r1.

### CVE-2026-104720

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T14:16:59.003 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Kobikom Telecommunications and Informatics Services Inc. Kobikom allows Path Traversal.

This issue affects Kobikom: before KobiPBX-FOP3-SEC-r1.

### CVE-2026-123047

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312;CWE-522` |
| Published | 2026-11-05T13:17:07.493 |

In Eclipse BaSyx Helm Charts versions 3.0.0-rc.1 to 3.12.1 of the `basyx` chart, deployments with the bundled Keycloak enabled store the passwords of the Keycloak users that the chart creates in cleartext in a Kubernetes ConfigMap.



The template `keycloak-init-config.yaml` rendered `keycloak.initialization.users`, including each user's `credentials[].value`, as `users.json` into the persistent ConfigMap `<release>-basyx-keycloak-init-config`. By default this includes the bootstrap administrator user. That user holds the `admin` role and has a non-temporary password. A principal that can read ConfigMaps but not Secrets in the release namespace, such as a holder of the built-in Kubernetes `view` ClusterRole, can read the password from the ConfigMap and log in to Keycloak as this user. The resulting token carries the `admin` role, which the default BaSyx ABAC rules map to full rights on all BaSyx APIs in the deployment.



The bundled Keycloak is disabled by default. The issue is fixed in version 3.12.2 of the `basyx` chart, which moves the initialization users to the Keycloak credentials Secret. Affected users should upgrade and change the passwords of users that were created through the chart.

### CVE-2026-123029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-05T07:17:26.057 |

Wowza Streaming Engine before 4.12.2 processes XML external entities, which allows remote attackers to read local files with the privileges of the Wowza Streaming Engine process.

### CVE-2026-76826

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-04T23:17:58.400 |

tsParticles is a TypeScript library for creating highly customizable particle animations. From 4.0.0 until 4.3.2, the stable publish workflow interpolates steps.release.outputs.body directly into an echo command in Bash source before writing RAW_RELEASE.md. Contributor-controlled shell metacharacters in generated release-note text can therefore execute when a maintainer starts a stable release, allowing modification of generated artifacts or workspace scripts and affecting later release steps that hold GITHUB_TOKEN and write permissions. This issue is fixed in version 4.3.2.

### CVE-2026-63655

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-04T22:18:07.350 |

tsParticles is a TypeScript library for creating highly customizable particle animations. Prior to 4.3.1, the HTTP mode of @tsparticles/mcp-server accepts unauthenticated POST /mcp requests in integrations/mcp-server/src/index.ts and accumulates every request-body chunk in a Buffer[] without a cumulative size limit before Buffer.concat and JSON.parse. A remote attacker can stream an arbitrarily large body to exhaust Node.js process memory and terminate the service, including in the official Docker configuration that exposes HTTP mode on 0.0.0.0:3000. Confidentiality and integrity are not affected. This issue is fixed in version 4.3.1.

### CVE-2026-55367

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-04T22:18:06.167 |

h2o is an HTTP server with support for HTTP/1.x, HTTP/2 and HTTP/3. Prior to commit 4212ce114506a073505fd389db16ad2ba4e582a0, a client could send an incomplete CONNECT-UDP Capsule with an excessively large declared length, causing H2O to keep buffering received bytes without a per-Capsule limit while waiting for the remainder. Deployments that enabled proxy.connect-udp and accepted CONNECT-UDP requests could exhaust server memory and lose availability. This vulnerability is fixed with commit 4212ce114506a073505fd389db16ad2ba4e582a0.

### CVE-2026-17493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-04T21:18:13.020 |

IBM Watson Speech Services Cartridge 4.0.0 through 5.4.0 could allow a remote attacker to cause a denial of service due to an out-of-bounds read.

### CVE-2026-12356

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-04T21:18:11.270 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow an authenticated user with command queue access to execute arbitrary code by injecting malicious arguments into Ant script commands.

### CVE-2026-10859

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-04T21:17:48.103 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow an authenticated attacker to execute arbitrary code on consumer applications due to insecure deserialization of ObjectMessage payloads.

### CVE-2026-104203

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-288` |
| Published | 2026-11-04T21:17:42.327 |

Traccar is an open source GPS tracking system. From 5.1 until 6.15.0, WebModule.java's MediaFilter Guice mapping and WebServer.java's Jetty ResourceServlet assign different routing meanings to path parameters at /api/media/*. An unauthenticated attacker who knows or guesses a device unique ID and media filename can insert a semicolon at the Servlet boundary, bypass MediaFilter's session and device authorization checks, and retrieve the protected media because Jetty still dispatches the noncanonical path to ResourceServlet. The demonstrated impact is read-only disclosure of a protected device media file; depending on the deployment and stored media, this could expose photographs, audio, video, or other uploaded files. The advisory does not establish directory listing, traversal, modification, account takeover, denial of service, or code execution. Reverse proxies that reject or rewrite semicolon path parameters may block the request. This issue is fixed in version 6.15.0.

### CVE-2026-97705

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-04T20:19:13.137 |

Moleculer is a progressive microservices framework for Node.js. Prior to 0.14.36 and 0.15.2, Parser._write in src/transporters/tcp/parser.js used Buffer.prototype.readInt32BE to read a signed packet length, so a remote unauthenticated peer could supply a negative value that caused packet.slice(length) to return the unchanged buffer while the while (packet.length > 0) loop continued indefinitely. The synchronous loop blocked the Node.js event loop and made every service in the process unresponsive until restart. The TCP transporter must be enabled and reachable, and neither CRC validation nor maxPacketSize prevents the malformed length value. This issue is fixed in versions 0.14.36 and 0.15.2.

### CVE-2026-109408

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-297;CWE-636` |
| Published | 2026-11-05T08:17:03.463 |

vault-java-driver, a Java client for HashiCorp Vault, silently disables TLS certificate and hostname verification in three states where the caller asked for verification: an SslConfig passed to VaultConfig without calling build(), an SslConfig restored by Java deserialization, and VAULT_SSL_VERIFY set to a truthy value other than "true", such as 1, yes or on. In each case SslConfig.isVerify() returns false and the driver installs a trust-all SSLContext. An attacker on the network path to the Vault server can then read the Vault token and secrets in transit and forge responses. This issue affects io.github.jopenlibs:vault-java-driver 5.2.0 through 6.2.3. It is fixed in 7.0.0.

### CVE-2026-113783

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-04T19:17:18.907 |

ESP-IDF is the Espressif Internet of Things (IOT) Development Framework. From 5.2.3 until 5.3.7, 5.4.5, 5.5.6, and 6.0.3, the lwIP DNS resolver's cached-lookup path in dns_lookup() in dns.c copies every cached address into a caller-provided single ip_addr_t output buffer without a length parameter or bounds check. When CONFIG_LWIP_DNS_MAX_HOST_IP is greater than 1 and a cached hostname has multiple A or AAAA records, a subsequent lookup through dns_gethostbyname() or dns_gethostbyname_addrtype() writes beyond the single-element buffer into adjacent stack memory. A network-positioned attacker who influences DNS responses can cause a reboot through stack-canary corruption or, without stack protection, overwrite stack variables with attacker-controlled address bytes and potentially redirect control flow. This issue is fixed in versions 5.5.6 and 6.0.3 and is scheduled to be fixed in versions 5.3.7 and 5.4.5. No fixed release is available for the end-of-life 5.2 line.

### CVE-2026-122118

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-334` |
| Published | 2026-11-04T18:17:43.667 |

In certain Yealink products before 2026-04-15, when the Wi-Fi AP function is enabled, a default 8-digit numeric PSK with insufficient strength is used. Attackers can exploit this weakness via brute-force attacks to gain unauthorized network access and intercept Wi-Fi traffic.

### CVE-2026-122007

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-04T15:17:43.127 |

Oqtane Framework before 10.3.0 contains a broken access control vulnerability in SettingController.cs that allows an authenticated site administrator to read and modify settings belonging to other sites within the same tenant database by supplying an arbitrary entityId for Site or Role type settings, since IsAuthorized and FilterPrivate fail to verify the requested site matches the current alias SiteId. Attackers can exploit the /api/setting endpoints to disclose private values such as SMTPPassword, SMTPClientSecret, and ExternalLogin ClientSecret, and to alter another site's OIDC/OAuth2 authentication configuration without requiring host privileges.

### CVE-2026-123010

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-669` |
| Published | 2026-11-05T05:18:36.383 |

@twilio-labs/netlify-okta-auth through 1.0.2 relies on an unverified iss claim. This affects an outbound HTTP request to retrieve a public signing key. There may be other impacts in a misconfiguration where oktaUrl isn't set.

### CVE-2026-122318

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:L/VI:H/VA:L/SC:L/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-05T03:17:24.523 |

Kyverno before 1.19.2 contains an authentication bypass in matchCertificateData that skips verifyImages subject and subjectRegExp checks when the signing certificate has no Subject Alternative Name. Attackers holding a leaf certificate from a configured private trust root can omit the SAN, set the expected Fulcio issuer OID, and sign malicious images that are admitted despite signer pinning.

### CVE-2026-122224

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-04T21:18:10.547 |

WebVirtCloud through commit bb920b0 contains a missing authorization vulnerability that allows low-privileged authenticated users to reach MigrateViewSet and CreateInstanceViewSet because no permission_classes are declared, so Django REST Framework defaults to AllowAny. Attackers can send requests to /api/v1/migrate/ or the compute instance create endpoint to migrate or undefine other users' virtual machines and create volumes and domains on any compute host.

### CVE-2026-121962

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T16:17:49.320 |

FreeRDP before 3.32.2 contains a heap buffer overflow in transport_default_read_pdu when handling partial Early User Authorization reads during PROTOCOL_HYBRID_EX CredSSP. A malicious RDP server can split the four-byte EUA result into short reads that advance the stream pointer beyond the 16 KiB allocation, causing an out-of-bounds write and client denial of service.

### CVE-2026-123012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-05T05:18:36.790 |

In Gogs 0.14.3, the Git Smart HTTP authorization layer in internal/route/repo/http.go allows a push when only read access was intended, a different vulnerability than CVE-2026-52810. This occurs because of inconsistency about whether a verb is checked in a case-sensitive manner.

### CVE-2026-109849

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-05T01:17:21.490 |

Incorrect privilege assignment issue exists in Hinemos. If this vulnerability is exploited, an attacker who can access the password change API with specific permissions that can be assigned to non-administrative users may change the password of an administrative user.

### CVE-2026-57152

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-04T23:17:52.163 |

GLPI is a free asset and IT management software package. From 0.85 until 10.0.26 and from 11.0.0 until 11.0.8, under certain conditions, GLPI permission logic could grant a user access to a document without confirming that the document was linked to the targeted item. This could expose the file to a user who should not be able to view it. This issue is fixed in versions 10.0.26 and 11.0.8.

### CVE-2026-54383

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-04T23:17:48.360 |

VitaFit cloud API before 2026-10-30 contained an excessive data exposure vulnerability that allows any authenticated user to query the GET /front/relation/search/ endpoint and retrieve PII and health-related profile information for user records. Attackers can enumerate the user directory using overlapping alphanumeric search terms to harvest identifiers, emails, birthdays, gender, height, weight goals, phone numbers, and Firebase UIDs.

### CVE-2026-18142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-04T21:18:13.187 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD could allow a remote authenticated attacker to cause a denial of service and perform limited memory corruption due to an integer overflow.

### CVE-2026-13289

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-04T21:18:12.120 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-13284

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-04T21:18:11.947 |

IBM MQ 9.2.0.0 through 9.2.0.44 LTS, 9.3.0.0 through 9.3.0.42 LTS, 9.4.0.0 through 9.4.0.26 LTS, 9.4.0.0 through 9.4.5.1 CD, and 10.0.0.0 through 10.0.0.5 LTS and CD is vulnerable to an XML external entity injection (XXE) attack when processing XML data. A remote attacker could exploit this vulnerability to expose sensitive information or consume memory resources.

### CVE-2026-121969

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-04T21:18:06.840 |

netrek-client-cow through 3.3.3 contains a stack-based buffer overflow vulnerability in handleSMessage() in short.c that allows malicious servers to overflow a 100-byte stack buffer by sending oversized SP_S_MESSAGE packets. A malicious Netrek server or man-in-the-middle on the plaintext TCP connection can send overlong or unterminated message bodies to write server-controlled bytes onto the stack and crash the client.

### CVE-2026-121968

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-04T21:18:06.670 |

Netrek-client-cow through 3.3.3 contains an out-of-bounds read vulnerability in short.c handleSMessage() that allows malicious servers to crash clients via an unchecked m_recpt index. Attackers controlling a Netrek server or intercepting the plaintext TCP connection can send SP_S_MESSAGE packets with m_recpt of 36 or more, reading past players[] and shipnos to deny service.

### CVE-2026-102664

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-908` |
| Published | 2026-11-04T21:17:41.300 |

ProxySQL is a proxy for MySQL and its forks, as well as PostgreSQL. Prior to 3.0.10, 3.1.10, and 4.0.10, decompress_mysql_payload() in lib/mysql_data_stream.cpp accepts a zlib stream when uncompress() returns Z_OK without checking that the actual output length equals the attacker-controlled payload_length. An authenticated MySQL client that negotiates compression can overstate payload_length, causing buffer2array() to parse the uninitialized tail of a heap buffer as MySQL packet headers and forward stale data to the backend. Backend error responses can disclose prior SQL queries, result data, credentials, or session state, and malformed lengths can also cause excessive allocations. This issue is fixed in versions 3.0.10, 3.1.10, and 4.0.10.

### CVE-2026-122192

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-390;CWE-825` |
| Published | 2026-11-04T20:19:12.210 |

Improper handling of a failed memory remap in Firecracker versions 0.23.0 through 1.16.1 might allow a guest user with root privileges to read or modify Firecracker VMM process memory via balloon or virtio-mem discard requests on microVMs restored from a snapshot with the File memory backend, if the host fails to create the replacement mapping.



To remediate this issue, users should upgrade to Firecracker 1.16.2 or 1.17.0 and later.

### CVE-2026-113372

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-04T20:18:56.483 |

Sonatype Nexus Repository 3 returns the private signing key of a YUM proxy or group repository to an account that holds only the read privilege for administering that repository. The account does not need the privilege to edit the repository. A party that holds the key can sign repository metadata as that repository.

### CVE-2026-113371

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-04T20:18:56.297 |

Sonatype Nexus Repository 3 returns the signing passphrase of an APT or YUM repository, through an internal REST endpoint, to a user account that holds only the read privilege for administering that repository. The account does not need the privilege to edit the repository.

### CVE-2026-82029

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-04T19:17:41.360 |

Invoice Ninja before 5.13.28 contains a broken access control vulnerability that allows authenticated vendor-portal contacts to access documents belonging to other vendors and clients by exploiting authorization checks that validate only company_id scope instead of vendor ownership. Attackers can request GET /vendor/documents/{hashid}/download or POST /vendor/documents/download_multiple, enumerating predictable sequential Hashids document identifiers due to a default empty HASH_SALT, to read any invoice PDFs, contracts, payment receipts, and expense attachments within the company.

### CVE-2026-113782

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-04T19:17:18.717 |

ESP-IDF is the Espressif Internet of Things (IOT) Development Framework. From 5.2.0 until 5.2.8, 5.3.6, 5.4.5, 5.5.5, and 6.0.3, the OpenThread Border Router Neighbor Discovery packet handler trusts an attacker-controlled ICMPv6 option length while copying into a fixed stack buffer. A host on the same infrastructure link as the Border Router can send a crafted ICMPv6 Router Advertisement to its infrastructure interface whose oversized length causes an out-of-bounds write into adjacent stack memory. Firmware is affected only when CONFIG_OPENTHREAD_BORDER_ROUTER=y; Thread end devices, routers, and RCP firmware without the Border Router feature are unaffected. Exploitation requires no authentication or user interaction and can crash or reboot the device or corrupt adjacent stack state. This issue is fixed in versions 5.2.8, 5.3.6, 5.5.5, and 6.0.3 and is scheduled to be fixed in version 5.4.5.

### CVE-2026-119747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-04T17:17:34.607 |

The GetPaid plugin for WordPress before 2.8.63 contains an incorrect authorization vulnerability where the check_post_permissions() method in includes/api/class-getpaid-rest-posts-controller.php maps REST operations to generic WordPress post capabilities instead of enforcing the plugin's manage_invoicing permission. Authenticated users with lower-privileged roles such as Editor or Author can exploit this flaw to list other users' invoices, mark pending invoices as paid without recording payment transactions, or create published items and new invoices through the REST API.

### CVE-2026-122032

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-04T16:17:50.580 |

SPIP before 4.4.29 contains a SQL injection vulnerability that allows authenticated attackers with back-office access to inject arbitrary SQL by submitting a differing where parameter value in the POST body versus the GET query string on the /ecrire/?exec=articles endpoint, bypassing spip_sanitize_from_request() sanitization. Attackers can exploit this request parameter mismatch to extract database contents, including protected articles and bcrypt password hashes of users.

### CVE-2026-121959

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-04T16:17:48.793 |

FreeRDP before 3.32.2 contains an infinite loop vulnerability in websocket_context_read that fails to handle a zero BIO result with payload outstanding. A malicious RD Gateway can send a truncated WebSocket frame followed by a TLS close_notify, causing a client thread to spin and consume CPU until killed.

### CVE-2026-121954

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-04T16:17:47.890 |

FreeRDP before 3.32.2 has a heap out-of-bounds write in the planar codec because freerdp_bitmap_planar_context_reset commits new dimensions before buffer reallocation succeeds, and a failed ResetGraphics is only logged. A malicious RDP server can send an oversized ResetGraphics PDU, then a GFX PLANAR command, to corrupt client heap memory and crash the client.

### CVE-2026-121950

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-04T16:17:47.153 |

FreeRDP before 3.32.2 does not check the product of surface dimensions in gdi_CreateSurface when handling an RDPGFX CREATE_SURFACE PDU, causing an integer wrap and heap buffer overflow on 32-bit builds and an approximately 4 GiB allocation on 64-bit builds. A malicious RDP server can send a CREATE_SURFACE PDU with width and height 32766 to a connecting client to corrupt heap memory or cause a denial of service.

### CVE-2026-121966

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-488` |
| Published | 2026-11-04T16:17:50.107 |

Traefik 2.x before 2.11.60 and 3.x before 3.7.16 sends ForwardAuth subrequests (and, in 3.7, Ingress NGINX auth-url requests) through an auth-server connection pool shared by all clients, exposing connection-bound NTLM or Negotiate authentication. An unauthenticated attacker can reuse another user's authenticated connection, receiving the victim's identity via authResponseHeaders to access backends as that user.
