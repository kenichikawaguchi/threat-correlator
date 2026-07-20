# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-20 15:00 UTC
- **対象期間**: `2026-07-19T15:00:12.000Z` 〜 `2026-07-20T15:00:59.000Z`
- **重要CVE数**: 36 件（Critical 9.0+: 9 件 / High 7.0〜: 27 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 近くに上ります。  
- **リモートからコード実行や認証回避が可能な脆弱性が集中** しており、特に CI/CD パイプラインやクラウドコントロールプレーン、RDP クライアントといったインフラ層での影響が大きいです。  
- **オープンソースの開発ツール・ライブラリ（Meshtastic、FreeRDP、SurrealDB、Crypt::Password など）** が多数対象となっており、アップストリームでの修正が遅れると社内システム全体に波及するリスクがあります。  
- WordPress プラグインや Python/Keras など、**アプリケーション層でも SSRF、SQLi、OS コマンドインジェクション** が報告され、外部からの攻撃者が管理者権限取得や情報漏洩を狙える状況です。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑44359** | 10.0 (CVSS:3.1) | Meshtastic の GitHub Actions `pull_request_target` ワークフローが攻撃者のフォークコードをシークレット付きで実行できる。 | **完全なリモートコード実行 (RCE)** が可能で、CI/CD 環境全体が乗っ取られる危険性がある。GitHub リポジトリを利用している全プロジェクトに波及。 |
| **CVE‑2026‑16235** | 9.8 (CVSS:3.1) | Perl 用 `Crypt::Password` が `rand` を乱数に使用し、予測可能なソルトを生成。 | **パスワードハッシュの衝突・復元** が容易になるため、認証情報が大量に漏洩するリスクが高い。Perl エコシステム全体で広く利用されている。 |
| **CVE‑2026‑16242** | 9.4 (CVSS:3.1) | Kubernetes の Konnectivity プロキシがクライアント証明書を検証せず、認証なしでクラスタ内部へアクセス可能。 | **クラスタ内の機密リソース（etcd、API Server 等）** が外部から取得でき、権限昇格や情報漏洩につながる。K8s のマネージドサービス利用者は必須で対策が必要。 |
| **CVE‑2026‑57309** | 9.3 (CVSS:4.0) | Windu CMS の URL パスに対する Blind SQL Injection。 | **認証不要でデータベース情報取得・改ざん** が可能。CMS が公開されているサイトは即時パッチ適用が求められる。 |
| **CVE‑2026‑64622** | 9.3 (CVSS:4.0) | `network‑ai` (npm) の承認チェックが GET `/approvals` で無効化。 | **機密承認リクエストが無認証で閲覧可能**。npm パッケージは CI/CD パイプラインで頻繁に使用されるため、情報漏洩リスクが高い。 |

> **注**：上記は **CVSS が 9.0 以上** かつ **インフラ層・開発ツール** に関わるものを中心に選出しました。その他の SurrealDB 系や WordPress プラグインの脆弱性も実運用上は無視できませんが、優先度はやや低めです。

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性スキャンの実施**：`trivy`, `snyk`, `OSSIndex` などで対象リポジトリ・コンテナイメージを即時スキャンし、該当パッケージのバージョンを特定。  
- **CI/CD パイプラインの見直し**：`pull_request_target` を使用している GitHub Actions は **`pull_request`** に置き換えるか、シークレットへのアクセスを最小化。  
- **最小権限の原則**：Kubernetes の Konnectivity プロキシは `--cluster-ca-cert` とトークン認証を必ず有効化し、外部からの直接アクセスを防止。  

### 3.2 パッケージ・バージョン別具体的対策  

| 製品 / パッケージ | 現行脆弱バージョン | **推奨バージョン** | 対策内容 |
|-------------------|-------------------|-------------------|----------|
| **Meshtastic** (GitHub Actions) | < 2.7.21.1370b23 | **≥ 2.7.21.1370b23** | `main_matrix.yml` の `pull_request_target` を `pull_request` に変更し、シークレット使用を制限。 |
| **Crypt::Password (Perl)** | ≤ 0.28 | **≥ 0.29** (または `Crypt::URandom` / `Math::Random::ISAAC::XS` が利用可能な環境へ移行) | `rand` から CSPRNG へ切り替え。`cpan -U Crypt::Password && cpan install Crypt::Password@0.29` |
| **Konnectivity proxy (Kubernetes)** | 1.27 以前のデフォルト設定 | **最新版 (1.28 以降) + `--cluster-ca-cert`** | `--cluster-ca-cert=/path/to/ca.crt --authentication-token-webhook` を必ず設定。 |
| **Windu CMS** | 3.2.1 以前 (脆弱確認版) | **ベンダー提供のパッチ版** (2026‑04‑xx) | ベンダーが公開したアップデートを適用し、`URL` パラメータのサニタイズを実装。 |
| **network‑ai (npm)** | 5.12.2‑5.13.3 | **≥ 5.13.4** | `npm install network-ai@5.13.4` で承認チェックが有効化される。 |
| **FreeRDP** | ≤ 3.27.1 | **≥ 3.28.0** | `apt-get update && apt-get install freerdp=3.28.0-1`（ディストリビューションに合わせ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-44359

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-07-20T00:16:58.210 |

Meshtastic is an open source mesh networking solution. Prior to version 2.7.21.1370b23, the Meshtastic GitHub repository's main_matrix.yml workflow is triggered by pull_request_target  and multiple jobs check out the attacker's fork code and execute it with access to repository secrets and elevated GITHUB_TOKEN permissions. No approval gate exists. Pull requests from external users with author_association: "NONE" triggered the CI workflow automatically. The workflow directly executes attacker-controlled files from the fork checkout. This issue could have resulted in supply chain compromise, self-hosted runner compromise, and/or repository takeover for the repo. This issue is separate from GHSA-6mwm-v2vv-pp96, which addressed a command injection via github.head_ref in the setup job of the same workflow. That fix correctly moved to environment variables. However, the more critical fork checkout vulnerability across the check, build, and build-debian-src jobs was not addressed. Version 2.7.21.1370b23 contains a patch for thie issue.

### CVE-2026-16235

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-07-20T07:16:37.320 |

Crypt::Password versions through 0.28 for Perl generate insecure random values for salts.

These versions use the built-in rand function, which is predictable and unsuitable for cryptography.

### CVE-2026-16242

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-20T08:16:29.833 |

A flaw was found in the Konnectivity proxy-server configuration for hosted control planes. The agent-facing listener was started without --cluster-ca-cert (and without token-based agent authentication), so client certificates were not validated. A remote attacker who can reach the Konnectivity cluster endpoint could connect as an unauthenticated agent, join the routing pool, and potentially proxy, inspect, modify, or drop control-plane-to-node traffic.

### CVE-2026-57309

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-20T13:16:56.367 |

A Blind SQL injection vulnerability has been identified in Windu CMS. A remote unauthenticated attacker is able to inject SQL syntax into URL path in HTTP header resulting in Blind SQL Injection.

Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 4.1 but may also affect other versions.

### CVE-2026-64622

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-20T12:19:47.057 |

Network-AI (npm: network-ai) versions 5.12.2 through 5.13.3 fail to apply the configured authorization check (checkAuth/secret) to the ApprovalInbox GET read routes, so even when an operator configures a secret, unauthenticated actors can access sensitive approval request details. The GET /approvals/?status=all, GET /approvals/:id, GET /approvals/stats, and GET /approvals/sse routes disclose full ApprovalEntry content including action/target shell-command strings, file paths, justifications, and risk levels. All responses also carry a hardcoded Access-Control-Allow-Origin: * header, enabling cross-origin disclosure from any website the operator visits. This is an incomplete fix for GHSA-mxjx-28vx-xjjj.

### CVE-2026-64621

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-20T12:19:46.910 |

FreeRDP before 3.28.0 (affected 3.x through 3.27.1) contains a double-free vulnerability in freerdp_client_rdp_file_apply_to_settings() (client/common/file.c) when parsing the selectedmonitors field of a .rdp connection file. The MonitorIds array is allocated through the settings object, and a raw non-owning pointer to it is freed on the strtoul error path without clearing settings->MonitorIds, leaving it dangling; at teardown freerdp_settings_free() frees the same buffer again. An attacker who convinces a victim to open a crafted .rdp file with oversized monitor tokens can trigger a size-controlled double-free in any FreeRDP CLI client (xfreerdp/sdl-freerdp/wlfreerdp) in the default configuration.

### CVE-2026-64620

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-20T12:19:46.760 |

FreeRDP before 3.28.0 (affected <=3.27.1) contains a heap-based buffer overflow in crypto_rsa_common() (libfreerdp/crypto/crypto.c). The function writes the modular-exponentiation result into the caller's output buffer via BN_bn2bin() and only afterward checks output_length > out_length, so out-of-bounds bytes are written before the bounds check. On the server side, when a client selects RDP Standard Security, the encrypted client random is decrypted into a fixed 32-byte buffer. Because the server publishes its RSA public key, an unauthenticated attacker can forge a ciphertext whose decrypted value is up to the full modulus length (e.g. 256 bytes for RSA-2048), overflowing the 32-byte heap buffer by up to ~224 attacker-controlled bytes pre-authentication, resulting in denial of service.

### CVE-2026-63756

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-07-20T12:19:45.590 |

SurrealDB versions before 3.1.0 contain a time-of-check/time-of-use race condition in the HTTP /rpc endpoint that allows unauthenticated requests to inherit authenticated session state. Unauthenticated attackers can send concurrent requests to the /rpc endpoint while legitimate authenticated traffic is active to execute operations with hijacked user privileges.

### CVE-2026-13147

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-07-20T07:16:35.580 |

The Kirki  WordPress plugin before 6.0.12 does not validate a user-supplied URL before requesting it server-side, allowing unauthenticated attackers to make the site issue HTTP requests to arbitrary hosts (Server-Side Request Forgery).

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-64623

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-20T12:19:47.200 |

Network-AI before 5.13.4 contains an improper cryptographic signature verification vulnerability in APSAdapter where the default local verifier accepts any non-empty string as valid. Unauthenticated attackers can submit forged APS delegation payloads with arbitrary scopes to bypass signature verification and obtain signed permission-grant tokens for sensitive resources including SHELL_EXEC.

### CVE-2026-10081

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T07:16:33.520 |

The Unlimited Elements For Elementor WordPress plugin before 2.0.11 does not sanitize or escape Google review content fetched from the Serp API before rendering it in the Google Reviews widget output, allowing unauthenticated attackers who submit a malicious review on the targeted business's Google listing to deliver Stored XSS to any visitor (including administrators) of any WP page displaying that Place ID's reviews.

### CVE-2026-63760

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-20T12:19:46.187 |

SurrealDB before 3.1.0 fails to enforce the configured recursion depth limit in the value and JSON parser when processing nested braces, brackets, or parentheses. Unauthenticated attackers can send deeply nested JSON payloads to the WebSocket /rpc endpoint to exhaust server memory and crash the process.

### CVE-2026-63757

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-20T12:19:45.747 |

SurrealDB versions before 3.1.0 contain a session hijacking vulnerability where the HTTP /rpc sessions method returns attached session UUIDs without authentication and accepts arbitrary session fields with no ownership verification. Unauthenticated attackers can enumerate session UUIDs and impersonate authenticated sessions to read, write, delete data and escalate privileges.

### CVE-2026-63747

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-07-20T12:19:44.300 |

SurrealDB versions before 3.1.0 contain a denial of service vulnerability in the RPC use handler that panics when db is set without a namespace. Unauthenticated attackers can send a malformed WebSocket message to the /rpc endpoint to crash the server process.

### CVE-2026-63735

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-20T12:19:42.563 |

SurrealDB versions before 3.2.0 fail to validate namespace and database scope in custom API routes, allowing authenticated users to invoke endpoints in different namespaces/databases. Attackers with valid credentials for any namespace/database can access custom API endpoints in other tenants by specifying the target scope in the URL path, reading sensitive data or triggering unintended operations.

### CVE-2026-14448

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-20T12:17:54.707 |

An high privileged remote attacker can exploit an authenticated OS command injection vulnerability in the system_certificates view due to improper neutralization of special elements in an OS command. This can result in a total loss of confidentiality, availability and integrity.

### CVE-2026-11349

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-20T07:16:34.547 |

The Modern Event Calendar Pro WordPress plugin before 7.34.0, Modern Events Calendar Lite WordPress plugin before 7.34.0 do not sanitise and escape a request parameter before using it in a SQL statement, through an AJAX action available to unauthenticated users, leading to an unauthenticated SQL injection vulnerability that allows attackers to extract sensitive data from the database.

### CVE-2026-63739

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-20T12:19:43.143 |

SurrealDB before 3.1.5 contains an arbitrary file read vulnerability in the DEFINE ANALYZER mapper filter that allows database users with EDITOR or OWNER roles to read files accessible to the SurrealDB process. Attackers can specify arbitrary file paths in the mapper filter and retrieve file contents through query error messages when the SURREAL_FILE_ALLOWLIST is empty or not configured.

### CVE-2026-13577

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-338;CWE-340` |
| Published | 2026-07-20T08:16:28.987 |

Dancer2 versions through 2.1.0 for Perl generate insecure session ids when CSPRNG modules are unavailable.

Dancer2::Core::Role::SessionFactory::generate_id silently falls back to a built-in rand-derived session id when both Math::Random::ISAAC::XS and Crypt::URandom are unavailable.

The fallback session id is generated from a SHA-1 hash of a call to the built-in rand function, the absolute path of the Dancer2::Core::Role::SessionFactory module, an internal counter, the process id, the module instance memory address, and a shuffled string of characters (using the List::Util::shuffle function, which also uses the built-in rand function).

These are all low-entropy and easily guessed sources.

The built-in rand() function is seeded with 32-bits and considered unsuitable for security applications.

Predictable session ids could allow an attacker to gain access to systems.

### CVE-2026-12484

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-19T20:16:28.800 |

A vulnerability in keras-team/keras version 3.15.0 allows unsafe deserialization of attacker-controlled PyTorch pickle data through the public `keras.layers.TorchModuleWrapper.from_config` method. This method invokes `torch.load(..., weights_only=False)` without requiring an explicit unsafe opt-in, such as a `safe_mode=False` parameter. When called outside a `SafeModeScope(True)` context, the absence of an ambient safe mode state permits unsafe deserialization by default. This issue can lead to arbitrary code execution if untrusted Keras layer configurations are processed using this method. The vulnerability arises because the method does not enforce safe deserialization practices unless explicitly guarded by Keras safe mode.

### CVE-2026-63763

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-20T12:19:46.623 |

SurrealDB before 2.5.0 and before 3.0.0-beta.3 contains a confused deputy privilege escalation vulnerability. Unprivileged users (e.g., those with the database editor role) can create or modify fields containing futures, functions, or closures. Because these are executed in the context of the invoking/querying user rather than their creator, an attacker can plant malicious logic that executes with a higher-privileged user's permissions when that user reads or writes the affected record. This can lead to full privilege escalation, including creation of a root owner and server takeover.

### CVE-2026-6656

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-208` |
| Published | 2026-07-20T07:16:42.440 |

Crypt::Password versions through 0.28 for Perl are susceptible to timing attacks.

The check_password method uses the built-in eq operator. This allows discrepancies in timing to be used to guess the underlying hash.

### CVE-2026-12592

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T07:16:34.757 |

The SlimStat Analytics WordPress plugin before 5.5.0 does not escape a visitor-controlled geolocation value before outputting it in its admin analytics reports, allowing unauthenticated visitors to store a cross-site scripting payload that executes in the browser of an administrator who views the reports. Exploitation requires the SlimStat Analytics WordPress plugin before 5.5.0 to be configured to use the Cloudflare geolocation provider.

### CVE-2026-42566

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-20T00:16:58.050 |

Meshtastic is an open source mesh networking solution. Prior to version 2.7.23.b246bcd, a single node advertising a User.long_name that contains a malformed character encoding can render other radios unusable over BLE when managed through the iOS app. The malformed name does not need to be maliciously crafted — it can arise from ordinary buffer truncation and has been observed occurring naturally in the wild. At least one code path could place a null terminator in the middle of a multibyte sequence, leaving a malformed User.long_name in the node database. The problem surfaced downstream: the iOS app enforced encoding validation and therefore cannot parse a node database once it contains a poisoned entry. This caused BLE sync to enter a fail/retry loop, resulting in loss of control over the affected device. For a typical user managing their radio with the iOS app, the device becomes effectively unusable until the poisoned node ages out of the on-device database, or unless they have an alternate management path (e.g., the Python CLI, which can be used to identify and remove the offending entries manually). Because the malformed name propagates through the mesh, the temporary presence of a single affected node can degrade BLE management for iOS users across a wide geographical area for an extended period. Less technical users have no straightforward recovery path. Starting in version 2.7.23.b246bcd, the firmware has added input sanitization and regression tests demonstrating recovery for already-poisoned devices. The apps have also taken steps to ensure more graceful handling of malformed encoding sequences as well.

### CVE-2026-16221

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-07-19T15:16:49.027 |

Impact: fast-uri versions from 2.3.1 through 4.1.0 (including the 3.x line up to 3.1.3 and the 2.x line up to 2.4.2) do not treat a literal backslash character (U+005C) as an authority delimiter. Node's native WHATWG URL parser, used by fetch, undici, and Node's http and https clients, normalizes the backslash to a forward slash for special schemes such as http, https, ws, wss, ftp, and file. As a result, the two parsers extract different hosts from the same input string. Applications that use fast-uri to enforce host-based policy such as allowlists, denylists, loopback or SSRF filtering, redirect validation, or outbound proxy routing before passing the same URL into Node's URL or fetch consumers can be steered to an unintended destination, including cloud metadata endpoints, loopback, or internal hosts. 

Patches: upgrade to fast-uri 4.1.1, 3.1.4, or 2.4.3.

Workarounds: none.

### CVE-2026-16248

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-20T13:16:56.190 |

A vulnerability was found in Tenda AC10 16.03.10.09_multi_TDE01. This issue affects the function fromAdvSetLanip of the file /goform/AdvSetLanip of the component httpd/netctrl. The manipulation of the argument GetValue/SetValue results in stack-based buffer overflow. The attack may be performed from remote. The exploit has been made public and could be used.

### CVE-2026-12080

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-07-20T13:16:55.543 |

A flaw was found in the QEMU Guest Agent (qga). A local unprivileged user can exploit a vulnerability in the guest-ssh-add-authorized-keys command handler by manipulating symbolic links. This can occur either through a deterministic directory-symlink bypass or a Time-of-Check to Time-of-Use (TOCTOU) file-symlink race. Successful exploitation allows the attacker to gain ownership of arbitrary root-owned files or directories, leading to root access. This vulnerability requires an external management layer (e.g., libvirt) to trigger the affected code path.

### CVE-2026-16247

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-20T12:17:56.230 |

In _connect.BRAIN versions prior to 5.06,
the application LogPathConfig.exe is executed during setup. During this
process, existing permissions on %ProgramData% are deleted and replaced,
granting the Windows group Everyone full control instead of restricting
access to %ProgramData%\Bizerba\_connect.BRAIN or %ProgramData%\Bizerba\BCT.









Starting with _connect.BRAIN 5.06,
the setup no longer executes this tool.

### CVE-2026-16246

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-276` |
| Published | 2026-07-20T12:17:56.087 |

In BRAIN2 versions prior to 3.09, the
application LogPathConfig.exe is executed during setup. As a result, the
Windows group Everyone is granted full control over %ProgramData% instead of
being restricted to %ProgramData%\Bizerba\BRAIN2\.





Starting with BRAIN2 3.09, the setup no
longer executes this tool.

However, the optional component Bizerba ScriptService still executes it.





Bizerba ScriptService is being
deprecated and will no longer be included starting with BRAIN2 version 3.11.

### CVE-2026-63759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-20T12:19:46.047 |

SurrealDB before 3.1.0 fails to enforce recursion depth limits in the type/kind parser when processing nested type annotations. Authenticated attackers can send queries with deeply nested type annotations to exhaust server memory and crash the process.

### CVE-2026-63755

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-20T12:19:45.433 |

SurrealDB before 3.1.0 evaluates user-supplied WHERE clauses in SELECT statements (and SET/MERGE/CONTENT/PATCH clauses in UPDATE, UPSERT, INSERT ON DUPLICATE KEY UPDATE, and RELATE update-variant statements) against full record data before enforcing PERMISSIONS FOR SELECT WHERE restrictions. An authenticated user — including Record and Scope users — can exploit this ordering flaw to read the full contents of any table in the database they are authenticated against, bypassing table-level permission checks. Exfiltration is most direct when scripting functions are enabled (--allow-scripting), but is also possible via SurrealQL's THROW statement and timing-based side channels without scripting. The vulnerability is confined to the attacker's current database and does not cross namespace or database isolation boundaries.

### CVE-2026-63754

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-07-20T12:19:45.293 |

SurrealDB versions before 3.1.0 contain a denial of service vulnerability where malicious LIVE queries with WHERE clauses that evaluate to errors cause all CREATE, UPDATE, and DELETE operations on the watched table to fail. An authenticated user with only select permission can prevent write operations on a table for any user, including root, by registering a LIVE query that triggers evaluation errors until the query is killed or the session ends.

### CVE-2026-63746

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-07-20T12:19:44.143 |

SurrealDB versions before 3.1.0 fail to enforce table SELECT permissions when traversing graph edges or back-references. Authenticated users can read records from any table reachable through graph edges regardless of the target table's PERMISSIONS FOR select clause.

### CVE-2026-63740

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-07-20T12:19:43.287 |

SurrealDB versions before 3.1.4 fail to properly enforce SELECT permissions on array elements (field.*) for record users, leaking denied array elements instead of hiding them. Attackers with record scope access can read array elements that element-level permissions should deny by exploiting incorrect index handling during permission filtering.

### CVE-2026-63737

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-07-20T12:19:42.857 |

SurrealDB versions before 3.1.5 contain a denial of service vulnerability where authenticated users can crash the server with queries containing long chains of operators. Attackers can submit queries with tens of thousands of chained operators that create unbounded expression trees, causing stack overflow during query processing and aborting the entire process.

### CVE-2026-9833

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-20T07:16:42.657 |

The Tag Groups is the Advanced Way to Display Your Taxonomy Terms WordPress plugin before 2.2.0 does not properly escape one of its AJAX parameters before reflecting it in the response body served with an HTML content type, allowing unauthenticated attackers to execute arbitrary JavaScript in the browser of a logged-in user with `edit_pages` capability (Editor or higher) who is tricked into following a crafted link.
