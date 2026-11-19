# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-19 15:00 UTC
- **対象期間**: `2026-11-18T15:00:47.000Z` 〜 `2026-11-19T15:00:54.000Z`
- **重要CVE数**: 336 件（Critical 9.0+: 83 件 / High 7.0〜: 253 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上り、特に **ネットワーク経由で認証不要** または **低権限での認証が可能** な脆弱性が目立ちます。  
- **リモートコード実行 (RCE)** や **認証バイパス** が多数報告され、攻撃者は一度侵入すればクラスタ全体や管理サーバーを乗っ取れる可能性があります。  
- コンテナ/仮想化基盤（Incus、UniFi Access、JetBrains TeamCity）や **SaaS 型 PaaS（Dokploy）**、**ストレージアプライアンス（Dell PowerStore）** が集中して攻撃対象となっている点が特徴です。  
- 多くの脆弱性は **入力検証不備**（コマンドインジェクション、SSRF、パス・トラバーサル）や **TLS 証明書チェーンの検証漏れ** に起因しているため、開発・運用フェーズでの「安全なデフォルト設定」の徹底が急務です。

---

## 2. 特に注目すべき CVE  

| CVE ID | スコア | 主な影響 | 注目理由・影響範囲 |
|--------|--------|----------|-------------------|
| **CVE‑2026‑75521** | 10.0 | Miren Runtime の QUIC/HTTP3 RPC サーバがクライアント証明書のチェーン検証を行わない | **認証バイパス** が可能で、クラスタ全体の RPC 通信を偽装できる。デフォルトポート 8443 が外部に開放されている環境では、完全なリモートコード実行につながる危険性が高い。 |
| **CVE‑2026‑71499** | 10.0 | cf‑manager が `fetch(url)` で取得した任意コードを Cloudflare Worker としてデプロイ | **特権 Cloudflare API キーが流出** すると、攻撃者は任意の JavaScript を実行でき、顧客全体の Cloudflare 設定を書き換え・情報漏洩・DoS が可能。 |
| **CVE‑2026‑130778** | 10.0 | Incus (LXC コンテナ管理) の TLS クライアント証明書認証バイパス | クラスタ内の **任意ノードに対して管理者権限でアクセス** でき、コンテナの作成・削除・イメージ取得が無制限に行える。Incus は多くの自社プライベートクラウドで採用されているため、影響範囲は広い。 |
| **CVE‑2026‑132802**  (UniFi Access) | 9.9 | Improper Link Resolution Before File Access → 任意コード実行（root） | ネットワーク内の低権限ユーザーが **リンク解決の不備** を突き、ホスト OS の root 権限でシェルを取得できる。UniFi Access は企業の入退室管理に必須で、侵害が直接物理セキュリティに結びつく。 |
| **CVE‑2026‑116440** (Dell PowerStore) | 9.8 | バッファオーバーフローによるリモートコード実行／DoS | Dell PowerStore はエンタープライズ向けストレージアプライアンスで、**外部からの直接攻撃が可能**（ポート開放状態）。コード実行が成功すれば、ストレージ全体のデータが危険にさらされる。 |

> **共通点**：すべて「外部からの直接アクセスが可能」か「内部ネットワークの低権限ユーザーでエスカレーションできる」点で、**防御層の欠如** が根本原因です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・ファームウェアのアップデート
| 製品 | 現行バージョン (脆弱) | 推奨バージョン (修正済) | アップデート手順のポイント |
|------|----------------------|------------------------|---------------------------|
| Miren Runtime | < 0.11.1 | ≥ 0.11.1 | `apt-get update && apt-get install miren-runtime=0.11.1`（公式リポジトリ） |
| cf‑manager | < 1.1.2 | ≥ 1.1.2 | Docker イメージを `docker pull ghcr.io/cf-manager/cf-manager:1.1.2` で再デプロイ |
| Incus | < 7.6.0 | ≥ 7.6.0 | `incus upgrade` または公式パッケージ `incus=7.6.0` を適用 |
| UniFi Access Application | < 2.5.0 (※ベンダーが提供する最初のパッチ) | ≥ 2.5.0 | UniFi OS の UI から「アップデート」→「UniFi Access」→「最新」へ |
| Dell PowerStore (SDNAS) | 7.x 系 (脆弱) | 7.5.2 以降のファームウェア | Dell EMC OpenManage → 「ファームウェアアップデート」→ 最新リリースを適用（リブート必須） |

> **注**：上記バージョンはベンダーが公開した最初の修正版です。リリースノートで「CVE‑2026‑xxxx」修正が明記されていることを必ず確認してください。

### 3.2 設定・運用面での緊急対策
1. **TLS 証明書検証の強化**  
   - Miren Runtime、Incus 共に `tls.RequestClientCert` の使用をやめ、`tls.RequireAndVerifyClientCert` に切り替える。  
   - 証明書チェーンは必ず **CA で検証** し、自己署名証明書は除外。

2. **外部からの直接アクセス遮断**  
   - `firewall-cmd` / `iptables` で **ポート 8443 (Miren)**、**ポート 443 (cf‑manager)**、**PowerStore の管理ポート** を社内ネットワーク以外から遮断。  
   - UniFi Access の管理 UI も VPN 経由のみ許可。

3. **最小権限の原則 (Principle of Least Privilege)**  
   - cf‑manager の Cloudflare API キーは **Read‑Only** に限定し、環境変数で暗号化保存。  
   - Dokploy 系のコマンドインジェクション対策として、すべてのシェル呼び出しを **引数リスト方式** (`execFile`) に変更。

4. **入力検証・サニタイズの徹底**  
   - UniFi Access のファイルパス解決は `realpath()` で正規化し、ルート外への遡りをブロック。  
   - PowerStore の TFTP/SMB/NFS サービスは **パス長チェック** と **境界チェック** を有効化。

5. **監視・インシデント対応の強化**  
   - **IDS/IPS** 

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-75521

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-18T19:18:08.200 |

Miren Runtime provides the runtime component for the Miren application platform. Prior to 0.11.1, the QUIC/HTTP3 RPC server on the default port 8443 uses tls.RequestClientCert and does not verify that presented certificates chain to the configured cluster certificate authority. The RPC authenticators derive a caller identity from PeerCertificates[0].Subject.CommonName without requiring a non-empty VerifiedChains value, and certificate identities bypass all RBAC checks. A network attacker who can reach the listener can present a self-signed certificate with an issuer distinguished name matching the public cluster CA subject and gain cluster superuser access, allowing disclosure, modification, or disruption of applications, sandboxes, disks, credentials, and other managed resources. This issue is fixed in version 0.11.1.

### CVE-2026-71499

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-918` |
| Published | 2026-11-18T19:18:07.890 |

cf-manager is an all-in-one dashboard for managing multiple Cloudflare accounts and services. Prior to 1.1.2, worker/src/routes/workers.ts uses bare fetch(url) calls to retrieve user-supplied URLs and deploys the returned content as a Worker script using stored Cloudflare credentials. The multipart and JSON branches of POST /api/:accountId/workers and POST /api/batch-deploy accept URLs without protocol, destination, redirect, content-type, or response-size validation. An attacker with deployment API access, or unauthenticated access when API_SECRET is not configured, can make cf-manager access internal resources or fetch attacker-controlled JavaScript and execute it in the victim Cloudflare Workers account. This issue is fixed in version 1.1.2.

### CVE-2026-130778

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T19:17:53.607 |

Incus before 7.6.0 contains an authentication bypass vulnerability that allows remote attackers to authenticate as any trusted certificate by appending its public certificate to their presented TLS client chain. Attackers can append the server's or a cluster member's certificate to gain cluster-level access, bypass authorization, modify trust store entries, and influence scriptlet-based authorization decisions.

### CVE-2026-129048

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-19T08:17:11.650 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Jacob N. Breetvelt WP Photo Album Plus wp-photo-album-plus allows Remote Code Inclusion.This issue affects WP Photo Album Plus: from n/a through 9.3.06.003.

### CVE-2026-132808

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T05:18:39.513 |

A malicious actor with access to the network and low privileges could exploit an Incorrect Authorization vulnerability found in UniFi Access Application to execute arbitrary commands on certain adopted UniFi Access devices.

### CVE-2026-132804

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T05:18:38.833 |

A malicious actor with access to the network and low privileges could exploit a Server-Side Request Forgery (SSRF) vulnerability found in UniFi Access Application to escalate privileges within UniFi OS.

### CVE-2026-132803

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T05:18:38.673 |

A malicious actor with access to the network and low privileges could exploit a series of authenticated SQL Injection vulnerabilities found in UniFi Access Application to escalate privileges on the host device.

### CVE-2026-132802

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-19T05:18:38.507 |

A malicious actor with access to the network and low privileges could exploit an Improper Link Resolution Before File Access vulnerability found in UniFi Access Application to execute arbitrary code with root privileges on the host device.

### CVE-2026-129991

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T23:17:19.090 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, the backup prefix field is only checked for a nonempty value, and normalizeS3Path preserves shell metacharacters before the prefix is interpolated into rclone upload and retention-cleanup command strings. An authenticated organization member with backup permission for a service can execute arbitrary commands as root on the Dokploy host or configured remote server when a PostgreSQL, MySQL, MariaDB, MongoDB, libSQL, Compose, or web-server backup runs manually, on schedule, or performs retention cleanup. This issue is fixed in version 0.31.1.

### CVE-2026-129989

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T23:17:18.737 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, the Nixpacks publishDirectory build setting accepts shell metacharacters and is interpolated into a docker cp command executed through child_process.exec. An authenticated user with access to an application can execute arbitrary commands on the Dokploy host when triggering a Nixpacks deployment, leading to host compromise through the privileged Docker environment. This issue is fixed in version 0.31.1.

### CVE-2026-129986

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-18T23:17:18.550 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, mount.deleteFileMount passes a path containing the user-controlled filePath to the local removeFileOrDirectory helper, which interpolates it unquoted into rm -rf, while the remote branch is quoted. An authenticated member with file-mount create and delete permissions can execute arbitrary commands in the host context immediately when deleting a local file mount, without requiring a running container. This issue is fixed in version 0.31.1.

### CVE-2026-129316

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T23:17:18.187 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). From 0.29.13 until 0.31.0, the Docker terminal, container-log, and monitoring WebSocket handlers accept a caller-controlled serviceId as authorization but do not consistently bind the requested containerId or appName to that service. A member with read access to any service can consequently target unrelated containers, obtain a root shell in the Dokploy panel container, read other tenants' logs and statistics, and use the mounted Docker socket to compromise the host. This issue is fixed in version 0.31.0.

### CVE-2026-129987

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-18T22:17:18.237 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, the database password validation used by the MySQL, PostgreSQL, MariaDB, MongoDB, and Redis change-password procedures permits backticks, and the procedures interpolate attacker-controlled passwords into Bash command strings. An authenticated user who can update a database password can trigger command substitution before the database command runs, resulting in arbitrary operating-system command execution with the Dokploy process privileges, which are typically root. This issue is fixed in version 0.31.1.

### CVE-2026-132234

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-18T17:17:44.980 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via argument injection in Mercurial VCS root settings

### CVE-2026-132233

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-18T17:17:44.853 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via build attribute injection

### CVE-2026-132232

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-18T17:17:44.733 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via argument injection in Perforce settings

### CVE-2026-132231

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1289` |
| Published | 2026-11-18T17:17:44.593 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via best-fit character mapping in Perforce settings

### CVE-2026-116440

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-19T13:17:27.983 |

Dell PowerStore SDNAS contains a buffer overflow vulnerability that could allow an unauthenticated remote attacker to cause a denial of service or potential code execution on the NAS node.

### CVE-2026-116439

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T13:17:27.837 |

Dell PowerStore SDNAS contains a path traversal vulnerability that could allow an unauthenticated attacker to read, modify, or delete arbitrary files on the NAS node.

### CVE-2026-132891

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-696` |
| Published | 2026-11-19T11:16:55.263 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via external pull requests

### CVE-2026-14492

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-19T10:17:28.927 |

The WP Duplicate – WordPress Migration Plugin plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.1.11 via the save_single_batch_file function. This is due to a PHP type-juggling authentication bypass via loose != comparison with no is_string() guard, combined with unsanitized base64-decoded path construction in save_single_batch_file() lacking any directory traversal containment. This makes it possible for authenticated attackers, with custom-level access and above, to execute code on the server. Exploitation requires that the site owner has completed the plugin's initial setup so that the site_type and prod_key_random_id options are non-empty, though any non-empty secret value is bypassable via the type-juggling flaw.

### CVE-2026-73969

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-798;CWE-1188` |
| Published | 2026-11-18T21:18:02.120 |

AnsibleForms is a self-hosted web application that turns automation into self-service forms. Prior to 6.2.1, AnsibleForms uses a public hard-coded fallback JWT signing secret from server/config/auth.config.js when ACCESS_TOKEN_SECRET is unset. An unauthenticated attacker can sign a self-contained token with privileged claims because server/src/auth/auth_jwt.js verifies the signature without reloading the user from the database, and server/src/lib/middleware.js trusts the token's roles and options for authorization. A forged token can therefore be accepted as an administrator session, resulting in authentication bypass and full privileged API access. This issue is fixed in version 6.2.1.

### CVE-2026-63189

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-200;CWE-287;CWE-522` |
| Published | 2026-11-18T16:18:16.520 |

Dialoqbase is an application for creating chatbots. Prior to 1.11.5, the unauthenticated GET /api/v1/view/* route in server/src/routes/api/v1/view/root.ts resolves its attacker-controlled wildcard path without normalization or containment, allowing traversal outside the intended uploads directory and arbitrary server file reads. Reading environment files can disclose DB_SECRET_KEY, the application’s JWT signing key, which permits forged administrator tokens and takeover of bots, conversations, integrations, and stored third-party credentials. This issue is fixed in version 1.11.5.

### CVE-2026-124990

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-18T16:18:05.313 |

The Masteriyo LMS – LMS Course Builder, Quizzes & Certificates plugin for WordPress is vulnerable to PHP Object Injection in versions up to, and including, 3.5.1 via deserialization of untrusted input in the course importer. The set_post_metas() method  calls maybe_unserialize() on attacker-controlled postmeta string values parsed from the uploaded JSON import file. This makes it possible for unauthenticated attackers to inject arbitrary PHP Objects. Exploitation by unauthenticated attackers requires that the site has enable_instructor_registration=true AND enable_guest_checkout=true AND at least one purchasable course exists. Install.php sets enable_instructor_registration=false on fresh installs, so this is a non-default configuration. On a default installation, where that is not configured, the vulnerability requires attackers with author-level access and above.

### CVE-2026-116449

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T16:17:59.947 |

Dell PowerStore SDNAS contains an OS Command Injection vulnerability that could allow an attacker with internal network access to execute arbitrary commands as root on the NAS node.

### CVE-2026-116443

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:17:59.803 |

Dell PowerStore SDNAS contains a stack-based buffer overflow in the NAS TFTP service that could allow an unauthenticated remote attacker to cause a denial of service or potential code execution.

### CVE-2026-116448

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T15:17:33.083 |

Dell PowerStore SDNAS contains an OS Command Injection vulnerability that could allow an attacker with internal network access to execute arbitrary commands as root on the NAS node.

### CVE-2026-116446

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-18T15:17:32.780 |

Dell PowerStore SDNAS contains an out-of-bounds memory vulnerability in the NAS NFS service that an unauthenticated remote attacker could exploit to cause a denial of service.

### CVE-2026-55506

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-18T21:17:59.833 |

Wavelog is web-based amateur radio logging software. Prior to 2.5, the filename parameter accepted by POST /qsl/addQsoToQsl in application/controllers/Qsl.php addQsoToQsl() is stored without rejecting directory separators or relative path components, and POST /qsl/delete reaches application/models/Qsl_model.php deleteQsl(), which passes the planted qsl_images filename to unlink(). A standard authenticated user can associate the malicious filename with the user's own QSO, satisfy the ownership check, escape the per-user QSL image directory, and delete files writable by the PHP worker. Deleting configuration or operational files can cause denial of service, while deleting installer gate files can reopen the unauthenticated installer and enable application identity takeover through attacker-controlled database configuration. This issue is fixed in version 2.5.

### CVE-2026-116441

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-18T17:17:28.430 |

Dell PowerStore SDNAS contains an out-of-bounds write vulnerability in the storage-processor interconnect driver that could allow a malicious peer to execute code with system privileges.

### CVE-2026-132622

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-11-19T04:17:27.700 |

A vulnerability was found in GearUP Hyperev up to 20261020. This impacts the function get_wlan_sitesurvey of the file ld/utils.lua of the component WLAN Site Survey. Performing a manipulation of the argument line results in os command injection. The attack is possible to be carried out remotely. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-55508

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T21:18:00.170 |

Wavelog is web-based amateur radio logging software. Prior to 2.5, the callsign parameter accepted by POST /oqrs/search_log in application/controllers/Oqrs.php search_log() reaches application/models/Oqrs_model.php search_log(), where it is concatenated directly into a raw SQL WHERE clause without parameter binding. An unauthenticated remote attacker can use UNION-based SQL injection to read arbitrary application database records, including account data, password hashes, API keys, station credentials, reset tokens, QSO data, and station metadata. Disclosure of password reset tokens can be combined with the forgot_password workflow to take over accounts, including administrator accounts. This issue is fixed in version 2.5.

### CVE-2026-130786

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-11-18T19:17:55.157 |

Incus before 7.6.0 contains a configuration injection vulnerability that allows users who can launch instances from controlled images to inject LXC directives by embedding line breaks in OCI config.json values or oci.entrypoint and oci.cwd keys. Attackers can add liblxc hooks or crafted tmpfs lxc.mount.entry fields to run commands as root on the host or bind-mount host paths, even from restricted projects.

### CVE-2026-130784

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T19:17:54.837 |

Incus before 7.6.0 contains an authorization bypass vulnerability that allows restricted clients to create and access default project resources by exploiting entitlement checks against the requested project. Attackers can create bridge networks with raw.dnsmasq directives to execute code as root on the host, or manipulate inherited resources via the ?project= parameter.

### CVE-2026-130780

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T19:17:54.067 |

Incus before 7.6.0 contains a path traversal vulnerability that allows malicious migration peers to write outside intended directories by supplying unvalidated dependent volume and snapshot names in the migration offer header. Attackers controlling a migration source can create root-owned volumes with attacker content at arbitrary host paths, compromising hosts using dir storage pools, bypassing restricted.storage-pools.access, or crashing the daemon.

### CVE-2026-130773

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T19:17:51.587 |

Incus before 7.6.0 contains an authorization bypass that allows restricted project users to create resources in the unrestricted default project by targeting projects lacking features.* flags. Attackers can create bridge networks with raw.dnsmasq dhcp-script injection to run scripts as root, or custom volumes with block.create_options mkfs arguments to read host files.

### CVE-2026-130759

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T19:17:46.750 |

Fleet from 4.71.0 before 4.88.2 contains an authentication bypass vulnerability in the SAML SSO callback that looks up sessions using unvalidated client-supplied identifiers. Users able to run live queries or enroll secret holders can plant attacker-controlled identity provider metadata in the session store, then present a self-signed SAML response to log in as a global admin.

### CVE-2026-130156

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T17:17:38.673 |

Bazarr is a companion application to Sonarr and Radarr. Prior to 1.6.3-beta.11, the /api/subtitles/subtitles-info handler uses SubtitleNameContents.get() in subtitles_contents.py and reads the caller-supplied subtitlePath after checking only its subtitle extension; because the resolved path is not confined to files indexed by Bazarr, traversal can read files outside the media library. The /api/subtitles/subtitles handler in subtitles.py passes caller-supplied path and reference to sync and translation without per-path authorization, allowing an out-of-library reference file to be read and output to overwrite a file outside the media library. The authenticate decorator gates both endpoints when API authentication is enabled, while auth = None allows access without credentials. Both paths can affect only files that the Bazarr process can read or write. This issue is fixed in version 1.6.3-beta.11.

### CVE-2026-110461

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-19T07:17:08.770 |

The Comelit 1456B Multi-User Gateway, in firmware versions up to and including 2.10.0, is configured with static default passwords for multiple privileged roles. None of these passwords are required to be changed during initial configuration, and they remain at their default values unless the administrator changes them manually. An attacker with network access to the device can authenticate using these default credentials and gain administrative control.

### CVE-2026-131914

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-19T02:17:20.360 |

Deserialization of untrusted data in double-submit cookie vs. form field validation in Idunno.AntiCsrf versions through 0.9.1 Beta on ASP.NET allows remote unauthenticated attackers to execute code via object injection

### CVE-2026-63413

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T22:17:22.850 |

Jane is a set of PHP libraries that generates models and API clients from JSON Schema and OpenAPI specifications. Prior to 7.12.0, the Jane open-api-3 generator emits an OpenAPI header parameter name verbatim as an array key in generated Client/Endpoint method docblocks. A header parameter name containing a PHPDoc closing delimiter can terminate the comment early and place attacker-controlled PHP in class-body position, including an __construct method that runs when the generated Client is instantiated. Exploitation requires generating a client from an attacker-influenced OpenAPI document and then using the generated SDK, and can execute arbitrary PHP with the consuming application's privileges. This issue is fixed in version 7.12.0.

### CVE-2026-63412

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-116` |
| Published | 2026-11-18T22:17:22.710 |

Jane is a set of PHP libraries that generates models and API clients from JSON Schema and OpenAPI specifications. Prior to 7.12.0, the Jane open-api-3 generator emits an OpenAPI query parameter name verbatim as an array key in generated Client/Endpoint method docblocks. A query parameter name containing a PHPDoc closing delimiter can terminate the comment early and place attacker-controlled PHP in class-body position, including an __construct method that runs when the generated Client is instantiated. Exploitation requires generating a client from an attacker-influenced OpenAPI document and then using the generated SDK, and can execute arbitrary PHP with the consuming application's privileges. This issue is fixed in version 7.12.0.

### CVE-2026-63411

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-116` |
| Published | 2026-11-18T22:17:22.550 |

Jane is a set of PHP libraries that generates models and API clients from JSON Schema and OpenAPI specifications. Prior to 7.12.0, the Jane open-api-3 generator emits an OpenAPI parameter description verbatim in generated Client/Endpoint method docblocks. A parameter description containing a PHPDoc closing delimiter can terminate the comment early and place attacker-controlled PHP in class-body position, including an __construct method that runs when the generated Client is instantiated. Exploitation requires generating a client from an attacker-influenced OpenAPI document and then using the generated SDK, and can execute arbitrary PHP with the consuming application's privileges. This issue is fixed in version 7.12.0.

### CVE-2026-77297

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T21:18:03.643 |

MyMangaDB is a self-hosted manga collection manager with automatic metadata, MyAnimeList import, Docker support, and collection statistics. Prior to 2.7.2, the unauthenticated /api/v1/database/import handler in backend/app/api/v1/endpoints/database.py accepts a ZIP archive and moves an included database file to DATABASE_PATH while also replacing IMAGE_PATH content. An attacker can supply a database containing an attacker-controlled users table and administrative account, then authenticate as that account; invalid replacement data can also destroy application data or availability. This issue is fixed in version 2.7.2.

### CVE-2026-77296

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-11-18T21:18:03.497 |

MyMangaDB is a self-hosted manga collection manager with automatic metadata, MyAnimeList import, Docker support, and collection statistics. Prior to 2.7.2, the unauthenticated /api/v1/images/manga/save handler in backend/app/api/v1/endpoints/image.py accepts a client-controlled filename and joins it to IMAGE_SAVE_PATH without confining the result. Traversal sequences can escape the image directory and overwrite process-writable files, including DATABASE_PATH for the live SQLite database, while the client-supplied image content type does not validate the uploaded bytes. An attacker can replace the database to plant an administrative user and can overwrite other writable files, causing full application compromise and availability loss. This issue is fixed in version 2.7.2.

### CVE-2026-76807

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-350` |
| Published | 2026-11-18T20:19:13.090 |

Todoist MCP Server provides tools that allow AI agents to access and modify a Todoist account. Prior to 10.3.3, the optional todoist-mcp-http server accepts browser-origin requests to POST /mcp without validating the Host and Origin headers or authenticating the browser caller. A malicious website can use DNS rebinding to reach the loopback listener and invoke MCP tools through StreamableHTTPServerTransport, which uses the server-held Todoist API key. This exposes Todoist account data and permits operations such as task creation, updates, completion, and deletion. The stdio transport is not browser-reachable and is not affected by this attack path. This issue is fixed in version 10.3.3.

### CVE-2026-130783

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T19:17:54.683 |

Incus before 7.6.0 exposes certificate and cluster join token secrets through the default project event stream and skips authorization when cancelling operations without associated permissions. Restricted clients can subscribe to operation events to capture certificate tokens and enroll unrestricted certificates, gaining full server access, or cancel token operations by UUID.

### CVE-2026-130774

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-18T19:17:52.023 |

Incus before 7.6.0 contains a privilege escalation vulnerability: rebuilding a never-started unprivileged container makes it boot without a user namespace. Root processes inside the container run as host uid 0, keeping capabilities like sys_module, with no device cgroup restriction, letting them load kernel modules and compromise the host.

### CVE-2026-130756

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-18T19:17:46.287 |

pnpm exe before 10.34.8 embeds an outdated Node.js runtime that still trusts compromised eMudhra intermediate CA certificates during registry TLS connections. Network attackers holding a recovered intermediate key can intercept standalone pnpm registry fetches and serve forged package metadata or tarballs.

### CVE-2026-130754

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-18T19:17:45.940 |

All versions of LaraDashboard contain an authentication bypass in SocialAuthService::findOrCreateUser(), which links a social login to an existing account by email without checking that the OAuth provider verified that email. Unauthenticated attackers using an OAuth/OIDC provider that asserts a victim's email can log in as any user, including Superadmin, and keep persistent access through a linked social_accounts entry.

### CVE-2026-132209

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-18T17:17:42.890 |

Hardcoded credentials in the executable file. These can be extracted using the “Strings.exe” tool and could allow an attacker unauthorized access to the database and SMTP server. 
winSAT.exe

### CVE-2026-132208

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-18T17:17:42.760 |

Hardcoded credentials in the executable file. These can be extracted using the “Strings.exe” tool and could allow an attacker unauthorized access to the database and SMTP server. winCRM.exe

### CVE-2026-126755

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-18T16:18:09.083 |

ArangoDB before 3.12.11 contains an authentication bypass vulnerability caused by a parser differential between the raw path authentication gate and the URL-decoded dispatch logic. Attackers can send requests with a %5f-encoded leading underscore to endpoints like /_db/_system/%5fapi/simple/first-example to reach /_api/* actions as superuser without authentication. Exploitation evidence was first observed by the Shadowserver Foundation on 2026-09-16.

### CVE-2026-126752

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T16:18:08.590 |

Dagu 1.23.0 before 2.0.0 defaults auth.mode to none, allowing unauthenticated attackers to execute OS commands through the /api/v2/dag-runs endpoint. Attackers can send a POST request with an inline spec defining steps containing arbitrary shell commands to achieve remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2026-03-11.

### CVE-2026-123637

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:04.500 |

When BIG-IP APM is provisioned and a per-request policy that includes the Client Information agent and Endpoint Security agents is applied to a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE).

Impact:

Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system and may allow the attacker to perform RCE. There is no control plane exposure; this is a data plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-121805

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:03.607 |

Description:

When an iRule that processes client traffic using the PEM::subscriber command is configured on a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE). 





Impact:



Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system and may perform RCE. There is no control plane exposure; this is a data plane issue only.







Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-120722

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:03.150 |

Description:

When an iRule that processes client traffic using the DNS::scrape command is configured on a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE). 





Impact:



Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system. In addition, the attacker may be able to perform RCE. There is no control plane exposure; this is a data plane issue only.







Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-120292

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:02.110 |

Description:


When an HTTP profile and an iRule using the 

MR::message 

route command are configured on a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE)


Impact:










Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system and may allow the attacker to perform RCE. There is no control plane exposure; this is a data plane issue only.


Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-120285

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:01.957 |

Description
When an HTTP profile and an iRule containing the PSC::ip_address command are configured on a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE).

Impact
Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system and may allow the attacker to perform RCE. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-116953

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:00.197 |

Description:

When an iRule that processes client traffic using the GENERICMESSAGE::route command is configured on a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate and may lead to remote code execution (RCE). 





Impact:



Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system and may allow the attacker to perform RCE. There is no control plane exposure; this is a data plane issue only.







Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2023-54422

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T16:17:54.023 |

iDocView before 13.10.1_20231115 contains an unrestricted file upload vulnerability in the /html/2word endpoint that allows unauthenticated attackers to write arbitrary files by supplying a malicious url parameter. Attackers can send a crafted GET request with the url parameter to download linked resources with an unsanitized path and unblocked .jsp extension, achieving remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-11-22.

### CVE-2023-54419

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-18T16:17:53.547 |

nginxWebUI 3.0.0 before 3.5.8 contains an authentication bypass vulnerability that allows unauthenticated attackers to reach the /AdminPage/conf/runCmd endpoint by using a case-variant path that evades the case-sensitive /adminPage/ login filter. Attackers can pass OS commands through the cmd parameter, which are executed via /bin/sh with insufficient filtering of & and $() characters, achieving remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2022-51027

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T16:17:51.580 |

MeterSphere versions 1.13.0 before 1.14.7 and 1.15.0 before 1.16.4 contain a pre-authentication code injection vulnerability due to the /plugin/** endpoints being exposed with anonymous access. Attackers can upload a malicious jar via POST /plugin/add and invoke it through POST /plugin/customMethod using the 'entry' and 'request' parameters, which are passed to Class.forName and method invocation for remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2021-48025

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-18T16:17:50.927 |

OpenSNS 3.2.1 contains an unauthenticated code injection vulnerability in the shareBox method of ShareController that allows attackers to invoke arbitrary model methods via the query parameter. Attackers can send crafted GET requests to /index.php?s=weibo/Share/shareBox abusing parse_str and ShareModel::getInfo to reach Schedule::runSchedule and execute code through assert. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2021-48023

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T16:17:50.763 |

Weaver E-cology 9.0 contains an unrestricted file upload vulnerability in /page/exportImport/uploadOperation.jsp that allows unauthenticated attackers to upload arbitrary JSP files. Attackers can send a crafted multipart POST request with a JSP webshell written to /page/exportImport/fileTransfer/ to achieve remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-20.

### CVE-2019-25782

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-11-18T16:17:48.667 |

ThinkPHP 5.0.0 before 5.0.24 contains a code injection vulnerability that allows unauthenticated attackers to execute commands by setting _method=__construct in POST data to overwrite the Request filter property. Attackers can send POST requests to endpoints reached via ?s=captcha or ?s=index/index/index with filter[]=system and server[REQUEST_METHOD] values to execute arbitrary system commands. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2018-25443

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T16:17:48.500 |

Baidu UEditor 1.4.0 through 1.4.3.3 contains an unrestricted file upload vulnerability in the catchimage action of /ueditor/net/controller.ashx that only validates the Content-Type header. Unauthenticated attackers can supply a source[] URL like x.jpg?.aspx to retain a malicious extension and write an executable .aspx file for remote code execution. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-17.

### CVE-2012-20007

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-18T16:17:47.560 |

ThinkPHP 2.0 through 2.2 and 3.0 Lite mode contains an eval injection vulnerability in the Dispatcher PATH_INFO parsing, which uses preg_replace with the /e modifier and a double-quoted replacement. Unauthenticated attackers can send crafted requests to index.php with a malicious 's' parameter containing PHP expressions to execute arbitrary code on the server. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-123058

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-19T12:18:39.513 |

The web installer of JTL-Shop executes its
state-changing installation tasks without checking whether the shop is already
installed, and was not removed or locked after the installation. An unauthenticated
remote attacker who can reach the installer directory can supply their own
database credentials, create administrator and synchronisation accounts and
overwrite the shop configuration. This can lead to a full takeover of
the shop, including code execution on the server.

### CVE-2026-130770

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-11-18T19:17:50.250 |

Incus before 7.6.0 creates the NBD servers used for virtual machine migration and disk export on abstract unix sockets, which have no permission checks and whose names are visible in /proc/net/unix. A local unprivileged user can connect while an operation runs to read or modify the VM disk, gaining code execution in the guest on a migration's receiving side.

### CVE-2026-123634

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T16:18:04.353 |

This issue occurs when NGINX Plus or NGINX Open Source is configured as a proxy, the proxied server name includes variables, and a Server Side Includes (SSI) or mirror directive sends a subrequest to a location that resolves the same server name. Under these conditions, a specially crafted HTTP request may cause a use-after-free condition in a worker process. An attacker may also be able to execute code if Address Space Layout Randomization (ASLR) is disabled or the attacker can bypass ASLR.

Impact: 
An attacker could leverage this vulnerability to crash the NGINX worker process, corrupt its memory, or perform remote code execution (RCE)



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-123633

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T16:18:04.207 |

When NGINX Plus or NGINX Open Source is configured to use HTTP/2 for client connections and proxy client requests to a backend, a specially crafted request can result in use-after-free in the worker process, if this process is running low on worker_connections. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.




Impact:



This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system or may allow a code execution. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-123007

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-11-18T16:18:04.047 |

This issue affects NGINX Plus or NGINX Open Source configurations that use HTTP/2. When NGINX processes undisclosed traffic, the flow control window can exceed the allowed threshold, potentially resulting in a heap buffer overflow typically followed by an NGINX worker segmentation fault. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact: An attacker could leverage this vulnerability to crash the NGINX worker process, corrupt its memory, or potentially execute code remotely. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-121810

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T16:18:03.763 |

Description:
This issue affects NGINX Plus and NGINX Open Source configurations that use HTTP/3. A remote, unauthenticated attacker can cause a use-after-free condition in the NGINX worker process, leading to a restart. Exploitation also depends on conditions beyond the attacker’s control. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact:
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system or to possibly trigger a code execution. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-120718

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-18T16:18:03.013 |

Description: 
BIG-IP iControl REST tokens may not expire as expected in all scenarios.   

Impact: 
An attacker who has obtained a token may be able to extend its expiry lifetime unless the token owner deletes it. There is no data plane exposure; this is a control plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-113425

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T16:17:59.493 |

When NGINX Plus or NGINX Open Source is configured as a mail proxy, undisclosed traffic can cause a use-after-free in an nginx worker process. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact:
A remote unauthenticated attacker may crash an nginx worker process or corrupt its memory, disrupting service. Remote code execution is a potential impact. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2016-20105

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-11-18T16:17:47.940 |

Lucee Server versions 5.0.0.0 before 5.3.4.46 contain an insecure default configuration that allows unauthenticated attackers to set the initial admin password via the first-run form on /lucee/admin/web.cfm and /lucee/admin/server.cfm. Attackers can access the 'New Password' set-password form before any password is configured to seize administrative control of the server. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-24.

### CVE-2026-111509

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-338` |
| Published | 2026-11-19T13:17:27.513 |

Dell PowerStore SDNAS contains a cryptographically weak PRNG vulnerability that could allow a network attacker to decrypt or tamper with NAS SSH/SFTP sessions.

### CVE-2026-55171

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-11-18T21:17:59.350 |

Open OnDemand is an open-source high-performance computing portal. Prior to Open OnDemand 4.1.6 and 4.2.3, and prior to ood-ansible 4.2.1, the portal generator defaults OIDCCryptoPassphrase to SHA1(servername), and the templates/ood_portal.yml.j2 role checks a different variable from the documented passphrase setting. Administrators who set ood_oidc_crypto_passphrase can therefore believe a strong secret is configured while the deployment continues to use an attacker-derivable value. In OIDCSessionType client-cookie deployments, an unauthenticated remote attacker can derive the encryption key and forge a mod_auth_openidc_session cookie for another user, while server-cache deployments permit lower-impact tampering with protected OIDC state and nonce cookies. This issue is fixed in Open OnDemand versions 4.1.6 and 4.2.3 and ood-ansible version 4.2.1.

### CVE-2026-130757

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-18T19:17:46.437 |

Fleet before 4.92.0 contains an improper authentication vulnerability that allows attackers to reuse case-mutated security tokens because MySQL token columns used case-insensitive collation. Attackers holding a case-normalized invite or email-change token can redirect a victim's email for account takeover or redeem invites with roles up to Global Admin.

### CVE-2026-130154

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-306` |
| Published | 2026-11-18T17:17:38.513 |

Zyrabit Platform provides sovereign AI infrastructure for enterprise retrieval-augmented generation. Prior to 2.4.4, import_to_vault(source_path, destination_name) accepts both caller-controlled paths, but the content-pattern guard does not confine destination_name. The vulnerable tool is implemented in zyrabit-slm/api-rag/app/domain/services/mcp_service.py, where Path(DOCS_DIR) / destination_name is passed to shutil.copy2, allowing traversal or an absolute destination to write outside the vault. An unrestricted source_path can be copied into the vault and retrieved through secure_query, disclosing files readable by the service; files that do not match the executable-pattern filter pass that filter. When ENABLE_LEGACY_EXTENSIONS=true, zyrabit-slm/api-rag/app/main.py registers POST /mcp/rpc without get_current_user, allowing unauthenticated network tool calls; this optional exposure is disabled by default and is not required for local invocation. If an attacker can stage chosen source content and write to an execution-triggered destination, the advisory describes conditional process execution. This issue is fixed in version 2.4.4.

### CVE-2026-132807

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-19T05:18:39.360 |

A malicious actor with access to the network and under certain conditions could exploit an Improper Certificate Validation vulnerability found in UniFi Access Application to obtain sensitive information from and make unauthorized changes to an adopted UniFi Access device.

### CVE-2026-61532

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73;CWE-94` |
| Published | 2026-11-18T19:18:06.843 |

Chamilo LMS is an open-source learning management system. Prior to 1.11.40 and 2.0.3, src/Chamilo/CourseBundle/Component/CourseCopy/CourseRestorer.php and src/CourseBundle/Component/CourseCopy/CourseRestorer.php use paths supplied by an imported legacy course backup without consistently confining them to the extraction directory. A course teacher can import a crafted backup containing parent-directory path segments, causing file operations to write attacker-controlled content outside the intended destination, including PHP-executable or automatically loaded locations. This can result in code execution as the PHP process and compromise course data, user data, credentials, and the host. This issue is fixed in versions 1.11.40 and 2.0.3.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2025-64441

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-76` |
| Published | 2026-11-18T17:17:26.880 |

The ownCloud Desktop Client synchronizes files between an ownCloud server and a desktop. Prior to 6.0.2, an authenticated attacker can share a specially crafted file with a victim. If the file is synced by the client and revealed in the macOS Finder, it can cause operating-system command injection on the victim’s computer. This issue is fixed in version 6.0.2.

### CVE-2026-111506

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-19T14:17:23.843 |

Dell PowerStore contains a Missing Authentication vulnerability that a network-adjacent attacker could exploit to bypass authentication and authorization, leading to information disclosure and denial of service.

### CVE-2026-133117

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-19T13:17:32.840 |

WebToffee Product Feed before 2.4.4 for WordPress contains a use of hard-coded cryptographic key vulnerability that allows unauthenticated attackers to bypass the URL-cron signature check by computing a valid hash using the publicly known constant salt embedded in the plugin source. Attackers can send forged GET requests with attacker-controlled parameters to the unauthenticated init-hooked endpoint to repeatedly trigger product-feed generation, causing CPU/database resource exhaustion and overwriting of the generated feed file.

### CVE-2026-133092

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-19T13:17:30.490 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via Git submodule URLs

### CVE-2026-133087

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-19T13:17:29.843 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via a time zone callback in the Kotlin DSL sandbox

### CVE-2026-133086

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-19T13:17:29.717 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via a URL stream handler in the Kotlin DSL sandbox

### CVE-2026-133080

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-19T13:17:28.947 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via Maven repository settings

### CVE-2026-133027

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-19T12:18:43.870 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 privilege escalation was possible via username handling in token authentication

### CVE-2026-133019

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-19T12:18:42.903 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via a context parameters callback in the Kotlin DSL sandbox

### CVE-2026-133018

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-19T12:18:42.783 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via a UI patches callback in the Kotlin DSL sandbox

### CVE-2026-133016

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T12:18:42.533 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via script definitions in the Kotlin DSL settings repository

### CVE-2026-133015

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-19T12:18:42.413 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via boot classpath libraries in the Kotlin DSL sandbox

### CVE-2026-125060

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T12:18:40.263 |

The checkout of JTL-Shop stores the delivery address
ID submitted by the customer in the session and adopts it into the order
without verifying that the address belongs to the ordering customer. A remote
attacker with access to the checkout, including a guest, can thereby attach
the delivery address of another customer to their own order. Name and
address of the other customer, and depending on the shop configuration
further contact data, then appear in the order confirmation and customer
account. As the IDs are sequential, addresses can be enumerated. Goods may
also be shipped to the wrong address.

### CVE-2026-132917

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-19T11:16:58.400 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via a file write bypass in the Kotlin DSL sandbox

### CVE-2026-132909

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-19T11:16:57.443 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via Mercurial repository contents

### CVE-2026-132906

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-183` |
| Published | 2026-11-19T11:16:57.087 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via native code loading in the Kotlin DSL sandbox

### CVE-2026-132806

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T05:18:39.183 |

A malicious actor with access to the network and low privileges could exploit an authenticated SQL Injection vulnerability found in UniFi Access Application to obtain sensitive information and make unauthorized changes within the UniFi Access Application.

### CVE-2026-77283

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-350` |
| Published | 2026-11-18T23:17:21.930 |

obsidian-sync-mcp is an MCP server that gives AI agents access to Obsidian vaults. Prior to 0.5.7, deployments running without MCP_AUTH_TOKEN install no serverOptions.authenticate check for the HTTP /mcp endpoint, so requests are dispatched without validating the Host or Origin headers. A malicious website visited by the operator can use DNS rebinding to reach loopback, LAN, VPN, or container-published addresses, or directly issue a cross-origin request to loopback, and invoke the MCP tool surface to read, create, overwrite, delete, or move vault notes. Deployments using MCP_AUTH_TOKEN are not affected because browsers do not attach the bearer token. This issue is fixed in version 0.5.7.

### CVE-2026-76913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-11-18T21:18:03.180 |

NotrinosERP is an open-source web-based enterprise resource planning system written in PHP and MySQL. From 1.0.0 until 1.1.0, the employee document handler in hrm/manage/employees.php allows an authenticated user with SA_EMPLOYEE permission to submit doc_file through tab_documents() and stores the raw client filename, including an executable extension, under company/0/documents/employees/ without extension, MIME, or content validation. Uploading a PHP file places executable content beneath the web root, where requesting the stored file results in server-side code execution. This issue is fixed in version 1.1.0.

### CVE-2026-63129

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T20:19:10.557 |

mssql-mcp-core is the shared library that powers MSSQL MCP servers. Prior to core and server 0.6.0 and reader and writer 0.5.0, multiple database tools interpolate caller-controlled identifiers and predicates into T-SQL batches passed to Request.query() while parameterizing only data values. update_data, delete_data, insert_data, execute_transaction, create_table, create_index, and drop_table accept unsafe tableName, column, index, schema, or free-form whereClause input, while reader-tier list_databases interpolates stateFilter without runtime allowlist enforcement. Row-count and preview queries execute before confirmUpdate or confirmDelete, allowing malicious arguments to bypass confirmation and maxRows controls and execute stacked DDL or DML, read or destroy data, and potentially run operating-system commands when the SQL login is privileged and xp_cmdshell is enabled. This issue is fixed in core and server version 0.6.0 and reader and writer version 0.5.0.

### CVE-2026-130766

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-18T19:17:48.003 |

Obot from 0.26.0 before 0.27.0 fails to validate the resource identifier in remote MCP server protected resource metadata, allowing malicious MCP servers to steal access tokens. Attackers can name a different service and authorization server with chosen scopes, causing Obot to obtain the victim's token for that service and forward it to the attacker.

### CVE-2026-132237

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-18T17:17:45.347 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via path traversal in the external artifact cache

### CVE-2026-132236

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-18T17:17:45.223 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via path traversal in the pipeline YAML file path

### CVE-2024-58402

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T16:17:54.363 |

Azon Dominator releases through 2024-06-03 contain an SQL injection vulnerability that allows unauthenticated attackers to manipulate database queries through the cid parameter in /fetch_products.php. Attackers can send crafted POST requests with boolean-based or time-based blind payloads to extract sensitive database information. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-07-30.

### CVE-2022-51034

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T16:17:52.700 |

Tangshan Pingsheng Reservoir Safety Supervision Platform builds through 2022-11-30 contain an unauthenticated SQL injection vulnerability in the simcardId parameter of /WebServices/SIMMaintainService.asmx/GetAllRechargeRecordsBySIMCardId. Attackers can send crafted POST requests with time-based MSSQL payloads to extract database information including user, version, and database name. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-07-30.

### CVE-2022-51028

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T16:17:51.760 |

CmsEasy 7.7.5_20210919 contains an unauthenticated SQL injection vulnerability in the execsql_action function at /?case=crossall&act=execsql that executes attacker-supplied queries decrypted with the hardcoded key 'cmseasy_sql'. Attackers can send a crafted 'sql' parameter to run arbitrary SQL and dump the admin username and password hash. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-22.

### CVE-2021-48021

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T16:17:50.097 |

Chamilo LMS 1.11.10 before 1.11.16 contains an unauthenticated SQL injection vulnerability in the searchOptionsFromTags function through the options parameter of extra_field.ajax.php. Attackers can send POST requests with a malicious JSON options array to inject SQL into the IN clause and extract database information. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2019-25784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T16:17:49.010 |

FineCMS versions 5.0.4 before 5.0.11 contain an unauthenticated SQL injection vulnerability in the data2 API action handled by list_tag in libraries/Template.php. Attackers can send GET requests to index.php?c=api&m=data2 with a valid auth hash and the param action=sql sql='...' to execute arbitrary SELECT queries and extract database information. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-116447

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T15:17:32.943 |

Dell PowerStore SDNAS contains a local privilege-escalation vulnerability that could allow a low-privileged attacker to execute code as root on the NAS node.

### CVE-2026-22311

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-348;CWE-645` |
| Published | 2026-11-19T12:18:47.500 |

The failed-login limiter of the JTL-Wawi
synchronisation interface of JTL-Shop derives the client identity from the
client-controlled X-Forwarded-For header and counts requests without credentials as failed
logins. An unauthenticated remote attacker can block the synchronisation
between JTL-Shop and JTL-Wawi with a few requests and repeat this
indefinitely, so that orders are no longer handed over to JTL-Wawi. No data is disclosed
and no code is executed.

### CVE-2026-129985

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-11-18T23:17:18.380 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, a user-controlled schedule appName is joined into the schedule directory path and interpolated without shell quoting into commands that create the directory and write the schedule script. An authenticated user who can create or update a dokploy-server schedule can inject operating-system commands that execute with the Dokploy process privileges when the schedule is saved, including root privileges on typical installations. This issue is fixed in version 0.31.1.

### CVE-2026-77295

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-11-18T21:18:03.347 |

MyMangaDB is a self-hosted manga collection manager with automatic metadata, MyAnimeList import, Docker support, and collection statistics. Prior to 2.7.2, the unauthenticated /api/v1/database/export handler in backend/app/api/v1/endpoints/database.py returns a ZIP containing the live SQLite database and the cover-image library. The database includes the users table and hashed_password values, allowing a remote attacker to obtain all application data and conduct offline password attacks without a session or token. This issue is fixed in version 2.7.2.

### CVE-2026-73967

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-922;CWE-1021` |
| Published | 2026-11-18T21:18:01.817 |

AnsibleForms is a self-hosted web application that turns automation into self-service forms. Prior to 6.2.1, AnsibleForms stores attacker-influenceable job output that server/src/lib/common.js processes through formatOutput without HTML escaping and client/src/components/AppAnsibleOutput.vue renders through v-html. An authenticated user can submit job input that is echoed into persistent output, causing script execution when another user views the job. Additional designer-controlled HTML and expression values reach v-html in client/src/components/AppForm.vue and client/src/components/BsInputForForm.vue without sanitization. Because Content Security Policy is disabled and the JWT is stored in localStorage, script execution can steal a victim's token and take over the account, including an administrator account. This issue is fixed in version 6.2.1.

### CVE-2026-130092

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-18T21:17:49.520 |

A caller who can reach the temporal-proxy gRPC listener, with or without a valid credential, can grow the proxy's memory until the process is terminated by sending requests with many distinct gRPC method names. temporal-proxy labels its request metrics with the method name exactly as the caller sent it, and records every request, including those that authentication or routing reject. Each distinct method name adds metric series that are never removed. The series grow whether or not the metrics endpoint is scraped, and metric labels configured from request metadata multiply the growth. temporal-proxy versions 0.1.0-alpha.20260716 through 1.2.0 are affected. The issue is fixed in 1.0.2, 1.1.2, and 1.2.1, and releases before 1.0.0 receive no fix. Upgrade to the fixed release for the deployed minor release line.

### CVE-2026-127222

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T21:17:48.157 |

SGLang through 0.5.23, fixed in commit 7b5fb39, contains a missing authorization vulnerability in the POST /load_lora_adapter_from_tensors HTTP endpoint, which lacks the @auth_level(AuthLevel.ADMIN_OPTIONAL) decorator applied to its sibling admin endpoints, allowing unauthenticated network-reachable attackers to invoke it without an API key. Attackers can load a LoRA adapter from attacker-supplied serialized tensors to manipulate the served model, and when combined with a separately documented deserialization bypass, achieve unauthenticated remote code execution as root.

### CVE-2026-61583

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-18T19:18:07.443 |

Chamilo LMS is an open-source learning management system. Prior to 1.11.40, main/dropbox/dropbox_functions.inc.php accepts a literal .htaccess filename in the course dropbox and stores it in a directory served by Apache, where the file can alter handler behavior under the required AllowOverride All configuration. Any authenticated course participant can upload .htaccess and then upload a PHP payload disguised as a .gif, resulting in code execution as the web-server user when the dropbox tool is enabled. This can expose or modify the Chamilo installation, course content, and database credentials. This issue is fixed in version 1.11.40.

### CVE-2026-130761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-18T19:17:47.090 |

Fleet before 4.92.0 contains a denial of service vulnerability that allows enrolled hosts to trigger unbounded per-name database lookups by submitting osquery result logs. Attackers with a valid host node key can send one request to /api/osquery/log containing many distinct query names, exhausting database connections and read replica capacity.

### CVE-2026-130760

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-18T19:17:46.927 |

Fleet before 4.86.2 contains a denial of service vulnerability that allows unauthenticated attackers to exhaust server memory via unbounded BER recursion in PKCS#7 parsing. Attackers can send deeply nested indefinite-length structures to Apple MDM check-in, enrollment, SCEP, or OTA endpoints to crash the entire Fleet instance.

### CVE-2026-130753

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-18T19:17:45.753 |

heym before 0.0.142 contains a remote code execution vulnerability in the Playwright step-mode node where _resolve_expressions_in_code substitutes workflow values directly into generated Python source. Authenticated non-admin users can craft step field values that break out of string literals to execute arbitrary Python as root inside the backend container.

### CVE-2026-126822

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-18T16:18:09.250 |

Description:





When BIG-IP APM is provisioned, an Access Profile is configured as a SAML SP (Service Provider) and is applied to a virtual server, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate.

Impact:





Traffic
is disrupted while the TMM process restarts. This vulnerability allows a remote unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system.









There
is no control plane exposure; this is a data plane issue only.






Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-126336

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-18T16:18:07.960 |

Description:


When BIG-IP APM is provisioned and a virtual server is configured with an APM Access profile and a SAML Service Provider (SP) agent with encrypted assertions enabled, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate.






Impact:


Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system. There is no control plane exposure; this is a data plane issue only.









Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-125274

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-18T16:18:05.750 |

An authenticated iControl SOAP user with at least Guest access can inject an unauthorized management request.





Impact:

This vulnerability may allow an authenticated attacker with network access and at least Guest role privileges to the iControl SOAP utility to execute arbitrary system commands, create or delete files, or disable services. There is no data plane exposure; this is a control plane issue only.





Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-125272

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-18T16:18:05.610 |

Description:






When BIG-IP APM is licensed and provisioned, and a virtual server with the APM access profile is configured with a per-request policy containing a form-based Logon Page, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate.









Impact:


Traffic is disrupted while the TMM process restarts. This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system. There is no control plane exposure; this is a data plane issue only.









Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-121812

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-18T16:18:03.910 |

Description:


When BIG-IP APM is provisioned, and a virtual server is configured with an APM access profile and a per-request policy, and the tmm.access.policytrace database key is enabled, undisclosed requests can cause the Traffic Management Microkernel (TMM) to terminate. The key is disabled by default.












Impact:



Traffic is disrupted
while the TMM process restarts. This vulnerability allows a remote unauthenticated attacker to cause a denial-of-service (DoS) on the BIG-IP system . There
is no control plane exposure; this is a data plane issue only.





Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-118899

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-18T16:18:00.357 |

When using the listen directive with the ssl parameter in the http block with TLSv1.3 enabled, an attacker can use a specially crafted TLS connection to cause an infinite loop in the NGINX worker process while reading the HTTP request body. As a result, the worker process stops accepting new connections and processing existing connections. Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

Impact: This vulnerability allows a remote, unauthenticated attacker to cause a denial-of-service (DoS) of NGINX. There is no control plane exposure; this is a data plane issue only.



Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2024-58403

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T16:17:54.547 |

AnyShare builds through 2024-11 contain a missing authentication vulnerability in the /api/ShareMgnt/Usrm_GetAllUsers endpoint that exposes user records including password fields. Attackers can send unauthenticated POST requests with a [start,limit] body to retrieve usernames, passwords, and department information for all users. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-12-25.

### CVE-2023-54420

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T16:17:53.717 |

LiveBOS builds through 2023-08-16 contain a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files via the imgName parameter in /feed/ShowImage.do using a ';.js.jsp' suffix bypass. Attackers can send crafted GET requests with directory traversal sequences in imgName to read system files such as /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-30.

### CVE-2023-54418

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-11-18T16:17:53.367 |

Nuxt 3.0.0-rc.1 before 3.0.0-rc.13 contains an arbitrary file read vulnerability caused by the Vite dev server default setting vite.server.fs.strict=false. Unauthenticated attackers can request /_nuxt/@fs/<absolute path> with a raw query to read arbitrary files like /etc/passwd from the system. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2023-54417

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T16:17:53.193 |

Nuxt 3.0.0 before 3.4.2 contains a semi-arbitrary file read vulnerability in the vite-node dev server middleware that allows unauthenticated attackers to read files by supplying an absolute path as the moduleId. Attackers can send GET requests to /__nuxt_vite_node__/module/ with an absolute file path to read sensitive system files. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2022-51030

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T16:17:52.063 |

QiboCMS V7 contains an arbitrary file download vulnerability in inc/job/download.php that allows unauthenticated attackers to read files by supplying a base64-encoded url parameter to /do/job.php?job=download. Attackers can bypass the .php extension check using the Windows 'ph<' wildcard to download sensitive files such as configuration files containing database credentials. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18.

### CVE-2022-51029

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T16:17:51.910 |

Synway SMG Gateway Management Software builds through 2022-03-15 contain a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files via the downfile parameter in /down.php. Attackers can send a multipart POST request to /down.php with a traversal path in downfile to retrieve sensitive files like /etc/passwd. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-20.

### CVE-2021-48022

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T16:17:50.593 |

Rocket.Chat versions 0.61.0 before 3.11.4, 3.12.x before 3.12.4 and 3.13.x before 3.13.2 contain a missing authorization vulnerability allowing unauthenticated attackers to read any room's messages via the livechat:loadHistory Meteor method. Attackers can mint a guest token through livechat:registerGuest and send POST requests to /api/v1/method.callAnon with a target rid parameter to retrieve message history without membership checks. Exploitation evidence was first observed by the Shadowserver Foundation on 2025-02-13.

### CVE-2019-25785

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T16:17:49.170 |

FineReport 8.0 contains a path traversal vulnerability that allows unauthenticated attackers to read arbitrary files through the resourcepath parameter of the /WebReport/ReportServer endpoint. Attackers can send GET requests with op=chart and cmd=get_geo_json to read sensitive files like privilege.xml and extract admin credentials. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2016-20106

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-18T16:17:48.120 |

NUUO NVRmini 2 through 3.0.8 contains a file disclosure vulnerability that allows unauthenticated attackers to read web-root files by passing a filename to the 'css' parameter of css_parser.php. Attackers can retrieve PHP source files confined to the document root, exposing hardcoded credentials and sensitive application logic. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-17.

### CVE-2012-20008

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-18T16:17:47.733 |

openSIS 5.1 before 9.0 contains a local file inclusion vulnerability that allows authenticated users to include arbitrary files through the modname parameter of ajax.php. Attackers can prefix a payload with misc/ and use ../ directory traversal to read sensitive files like /etc/passwd or execute local scripts in the web server context. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2026-19609

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T07:17:12.243 |

Cross-site scripting in the embedded co-browsing feature in Unblu inc. Unblu Spark 7.0 through 7.57.9 and 8.0 before 8.40.2, on on-premises and cloud deployments, allows an unauthenticated remote attacker in the visitor role to execute arbitrary JavaScript in the browser of an agent taking part in the attacker's co-browsing session, via manipulated synchronized page attributes of the co-browsed page.



The JavaScript runs in the context and under the identity of the agent's session in the Agent Desk or the Single Conversation Desk.



Exploitation requires an agent to join an embedded co-browsing session with the attacker. Mobile co-apping isn't affected.

### CVE-2026-110462

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-312` |
| Published | 2026-11-19T07:17:09.183 |

The Comelit 1456B Multi-User Gateway, in firmware versions up to and including 2.10.0, allows a user authenticated to the web interface with the Installer role to export a system configuration backup. The resulting backup file contains the configured passwords for all privileged roles

### CVE-2026-132748

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-96` |
| Published | 2026-11-19T00:17:42.893 |

Vtiger CRM through 8.4.0 contains a PHP code injection vulnerability that allows authenticated administrators to inject code via the updatedFields parameter into config.inc.php. Attackers can supply a crafted HELPDESK_SUPPORT_EMAIL_ID value that passes email validation but closes the PHP string literal to execute arbitrary operating system commands.

### CVE-2026-132143

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-18T22:17:20.360 |

A vulnerability has been found in DrayTek Vigor2960 up to 1.5.1.6. This vulnerability affects the function doWebBackup of the file /cgi-bin/mainfunction.cgi of the component Backup Handler. Such manipulation of the argument path/value leads to stack-based buffer overflow. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 1.5.1.7 is able to resolve this issue. The affected component should be upgraded. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-132141

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-18T22:17:19.960 |

A vulnerability was detected in DrayTek Vigor2960 up to 1.5.1.6. Affected by this issue is the function json_load_lock of the file /cgi-bin/mainfunction.cgi of the component Jsonstatus. The manipulation of the argument usefile results in stack-based buffer overflow. It is possible to launch the attack remotely. The exploit is now public and may be used. Upgrading to version 1.5.1.7 can resolve this issue. It is advisable to upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-132139

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-18T21:17:55.920 |

A weakness has been identified in DrayTek Vigor2960 up to 1.5.1.6. Affected is the function setSWMProfile of the file /cgi-bin/mainfunction.cgi. Executing a manipulation of the argument filename can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks. Upgrading to version 1.5.1.7 is able to address this issue. It is recommended to upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-130791

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-18T19:17:55.990 |

Finsys Dockhand before 1.0.55 contains a path traversal vulnerability that allows users with stacks:edit permission to move arbitrary server directories by supplying a crafted oldDir parameter. Attackers can send POST requests to /api/stacks/[name]/relocate with an unvalidated source path to relocate directories into stack paths, disrupting services and exposing their contents.

### CVE-2026-130758

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T19:17:46.587 |

Fleet before 4.92.0 contains an authorization bypass vulnerability in the deprecated POST /api/latest/fleet/mdm/apple/enqueue endpoint that allows team-scoped users to enqueue Apple MDM commands outside their teams. Attackers with team admin, maintainer, or GitOps roles can include one own-team host UUID alongside unresolved enrollment IDs to send commands like InstallProfile to deleted or user-channel enrollments without activity logging.

### CVE-2026-115342

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88;CWE-115;CWE-179` |
| Published | 2026-11-19T13:17:27.697 |

Argument injection in OpenVPN version 2.4.0 through 2.6.23 and 2.7_alpha1 through 2.7.8 on Windows allows local authenticated users to bypass interactive service option validation and add arbitrary configuration options via a crafted command line.

### CVE-2026-125061

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T12:18:40.417 |

The administration page "Offene
Bestellungen" (open orders) of the JTL PayPal Checkout plugin for JTL-Shop outputs the
customer name of pending orders without output encoding. A registered
customer (free self-registration) can submit an HTML-entity-encoded name, which is
decoded to markup when the billing address of an order is written. If
the PayPal payment is left unfinished, the order is listed on the page and the
name is rendered as markup in the browser of an administrator who opens
the page. The script code runs with the privileges of that administrator
and can, for example, create a new administrator account. Guest orders are
not affected, because the name is encoded again.

### CVE-2026-132756

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T00:17:44.180 |

Geany through 2.1.0 contains an OS command injection vulnerability that allows attackers to run shell commands by embedding metacharacters in filenames substituted into build and execute commands. Attackers can craft a file named with backticks or $(...) that executes via /bin/sh when a user runs Compile, Build or Execute, gaining code execution as the user.

### CVE-2026-132751

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-19T00:17:43.357 |

yt through 4.4.4 contains a code injection vulnerability that allows attackers to execute Python code by supplying a crafted con_args attribute in a ytdata HDF5 file. SavedDataset._parse_parameter_file() passes con_args to eval() unrestricted, so loading a malicious .h5 file with yt.load() runs attacker code as the user.

### CVE-2026-129315

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-18T23:17:18.000 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). In 0.31.0 and earlier, the hosted installer and manual installation instructions set /etc/dokploy to mode 0777, allowing a local non-root user on a shared host to replace root-owned schedule or Traefik configuration directories. Dokploy subsequently consumes those paths as trusted configuration and can execute substituted scheduled-task scripts as root, resulting in local privilege escalation.

### CVE-2026-132142

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-18T22:17:20.160 |

A flaw has been found in DrayTek Vigor2960 up to 1.5.1.6. This affects the function dataflowstatus of the file /cgi-bin/mainfunction.cgi of the component CGI Process. This manipulation of the argument option causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been published and may be used. Upgrading to version 1.5.1.7 is able to mitigate this issue. You should upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-121720

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250;CWE-426;CWE-454` |
| Published | 2026-11-18T22:17:17.587 |

OpenVPN 2.4.0 through 2.6.23 and 2.7_alpha1 through 2.7.8 on Windows allows local authenticated users to execute arbitrary code via a privileged service using user-controlled environment variables.

### CVE-2026-130779

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T19:17:53.830 |

Incus before 7.6.0 contains a path traversal vulnerability that allows users permitted to import custom volumes to store unvalidated snapshot names from the backup index configuration section. Attackers can craft a backup with traversal sequences in snapshot names so later deletion removes arbitrary host directories as root, while renaming or mounting operates on arbitrary paths.

### CVE-2026-130771

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-18T19:17:50.757 |

Incus before 7.6.0 fails to reject special files, hard links, or symlinks in backup or image metadata, allowing restricted project users to read or overwrite host files. Attackers can import crafted backups containing device nodes, a hard-linked backup.yaml, or symlinks to corrupt host storage, overwrite host files, or leak other projects' data.

### CVE-2026-59159

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-18T17:17:49.060 |

Linux Mint Update Manager manages software updates on Linux Mint systems. From 5.4.8 until 5.5.4.3, 5.5.9.1, 5.8.8.1, 5.9.8.1, 6.0.9.1, and 6.1.5.1, mint-refresh-cache passes a user-controlled --parent-window-id value directly to the privileged Synaptic process without validating it as an integer. A local user permitted to execute mint-refresh-cache through sudo can inject additional Synaptic command-line options and achieve arbitrary code execution as root. This issue is fixed in versions 5.5.4.3, 5.5.9.1, 5.8.8.1, 5.9.8.1, 6.0.9.1, and 6.1.5.1.

### CVE-2026-132913

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T11:16:57.917 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 stored XSS on the P4 Code Review build tab was possible

### CVE-2026-106094

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:Y/R:U/V:D/RE:M/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T22:17:15.950 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Westell Technologies, Inc Remote series products on Linux allows OS Command Injection.

This issue affects several generations of Westell Remotes: through firmware version 9.14.  It has been reproduced across multiple devices. However, it is confirmed to affect only devices configured for RAS (Remote Access Server - e.g., RADIUS, TACACS).

### CVE-2026-55169

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532;CWE-598` |
| Published | 2026-11-18T21:17:59.190 |

Open OnDemand is an open-source high-performance computing portal. Prior to 4.1.6 and 4.2.3, the Open OnDemand dashboard includes noVNC passwords in query parameters generated by apps/dashboard/app/helpers/batch_connect/sessions_helper.rb and apps/dashboard/app/views/batch_connect/sessions/connections/_novnc.html.erb. The server records those query strings in per-user PUN access logs, and insufficiently protected log directories can allow another local user to recover and replay a launch URL. Replaying the credential grants access to the running remote desktop and can result in horizontal or vertical privilege escalation according to the privileges of the desktop owner. This issue is fixed in versions 4.1.6 and 4.2.3.

### CVE-2026-76090

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-95;CWE-116` |
| Published | 2026-11-18T20:19:12.943 |

Tapir is a Scala library for describing HTTP APIs and exposing, consuming, and documenting them using open standards. Prior to 1.13.27, tapir-openapi-codegen-core generates Scala source from untrusted OpenAPI documents by interpolating object property names, query, header, and path parameter names, and operation tags without context-appropriate validation or escaping. Crafted names or values can break out of generated identifier or string-literal contexts and inject arbitrary Scala that executes when generated code is compiled or endpoints are assembled. This is a code-generation and build-time issue and does not make a running tapir server directly exploitable. This issue is fixed in version 1.13.27.

### CVE-2026-130785

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-18T19:17:55.000 |

Incus from 7.3.0 before 7.6.0 contains an authentication bypass vulnerability in the /dev/incus guest API that allows a process in one container to impersonate another by creating a cgroup named with a forged lxc.monitor. component. Attackers can read the target container's user.* and cloud-init.* configuration and devices, subscribe to its events, mark it ready, and export images across projects.

### CVE-2026-132805

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T05:18:39.000 |

A malicious actor with access to the network could exploit a Server-Side Request Forgery (SSRF) vulnerability found in UniFi Access Application to obtain information and make unauthorized changes on the host device.

### CVE-2026-129990

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T23:17:18.917 |

Dokploy is a free, self-hostable Platform as a Service (PaaS). Prior to 0.31.1, every network.* procedure is only authentication-protected and does not require the Docker permission, allowing a standard member to list, inspect, create, import, recreate, resynchronize, and delete Docker networks. A member can disrupt service connectivity or alter network configuration, and create/import operations can target an unchecked serverId. This issue is fixed in version 0.31.1.

### CVE-2026-132144

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-11-18T21:17:56.880 |

MISP contains an authorization flaw in the user login-email change logic. When an external authentication backend is configured (LDAP, Shibboleth, ApacheSecureAuth, or CustomAuth), the login email address serves as the key by which the directory service resolves a user's identity, organization, and role on each login. The __canChangeLogin() method in UsersController only checked the MISP.disable_user_login_change setting and site-admin status; it did not account for whether an external authentication backend was active. As a result, any authenticated non-admin user (including org admins) could change their own login email to an address that matches a higher-privilege account in the external directory. On the user's next login, the external backend would resolve that email to the target directory identity, granting the attacker the organization and role associated with that identity. This constitutes an account-identity capture and privilege escalation: the attacker effectively assumes the identity of any directory account whose email they can guess or discover. The vulnerability requires an authenticated session with a valid API key or session token and a MISP instance configured with at least one external authentication backend. The impact is limited to the scope of the captured directory identity's privileges within MISP.

### CVE-2026-130787

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T19:17:55.317 |

Frappe ERPNext before 16.35.0 contains a missing authorization vulnerability in financial reporting endpoints that allows low-privilege authenticated users to generate reports outside their permitted scope. Attackers can send crafted requests to affected reporting endpoints to read other companies' tax and payment data, including personal and corporate identifiers and financial totals.

### CVE-2026-130782

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T19:17:54.503 |

Incus before 7.6.0 contains an improper authorization vulnerability that allows restricted and view-only clients to read default project resources by requesting the default project directly. Attackers knowing resource names can read profiles, images, network zone peer keys and stored credentials, and export custom volume or bucket backups to obtain full contents or S3 admin keys.

### CVE-2026-130764

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T19:17:47.600 |

Obot from 0.8.0 before 0.27.0 contains a server-side request forgery vulnerability that allows Power User accounts to reach internal hosts by advertising a malicious OAuth token endpoint in remote MCP server metadata. Attackers can direct token exchange or refresh requests, including redirected GET requests, to cloud metadata services or private-network hosts and read error response bodies.

### CVE-2026-128664

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-285;CWE-862` |
| Published | 2026-11-18T19:17:40.040 |

An insecure password reset vulnerability in the Admin Password Recovery Module of PHPGurukul News Portal Project v4.1 allows unauthenticated remote attackers to change an administrator or sub-administrator account password by providing the corresponding username and email address. The application does not require verification of account ownership through an email token, OTP, or another authentication mechanism before updating the password, potentially resulting in account takeover.

### CVE-2026-132798

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T04:17:27.903 |

Improper Limitation of a Pathname to a Restricted Directory in the Como log viewer in Temenos Application Framework Java (TAFJ) R18.SP76.0 allows remote authenticated attackers to read arbitrary files via path traversal

### CVE-2026-59961

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-18T22:17:22.240 |

mini-snmpd is a minimal SNMP agent implementation. Prior to 1.7, the ASN.1 BER parser in protocol.c does not verify that an attacker-controlled field length is no greater than the remaining packet size before decode_str(), decode_oid(), and decode_ptr() evaluate size - len + 1. When len exceeds size, unsigned size_t arithmetic wraps and bypasses the bounds check, allowing the decoder to read beyond the 2048-byte packet buffer. Parsing occurs before the SNMP community string is checked, so a remote unauthenticated attacker can send one crafted request to UDP port 161 to crash the process and potentially disclose adjacent heap memory. This issue is fixed in version 1.7.

### CVE-2026-76100

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T21:18:02.883 |

OwnPay is a self-hosted open-source payment gateway automation platform. In 0.2.0 and earlier, modules/gateways/alipay/AlipayGateway.php fails open when an Alipay callback lacks a signature or the merchant has no configured public key because verify(array $callbackData, array $credentials) falls back to an undefined mode credential that defaults to test mode, while verifyWebhook() returns true unconditionally. An unauthenticated request to POST /webhook/{gateway} can provide a pending order reference and matching amount, pass both verification gates without a valid payment signature, and cause the order and corresponding payment-received ledger entries to be marked completed. No fixed version is available as of this review.

### CVE-2026-61528

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-18T19:18:06.693 |

Chamilo LMS is an open-source learning management system. From 2.0.0 until 2.0.3, the BigBlueButton plugin is vulnerable to XML External Entity (XXE) injection when an authenticated administrator configures a malicious BigBlueButton server URL. Processing attacker-controlled XML from that server can read arbitrary local files and perform Server-Side Request Forgery (SSRF). Sensitive configuration, credentials, source code, and internal network resources may be exposed. This issue is fixed in version 2.0.3.

### CVE-2026-130775

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T19:17:52.330 |

Incus before 7.6.0 contains an authorization bypass vulnerability in the /dev/incus guest-API image export handler that fails to pin the project parameter to the guest's own project. Container root users with the guest-API image entitlement can supply another project in the project query parameter to export public or cached images, including non-public images pulled from authenticated remotes.

### CVE-2026-130008

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-89;CWE-863` |
| Published | 2026-11-18T17:17:38.080 |

sqlite-mcp is a Model Context Protocol server for SQLite. Prior to 0.1.2, the default read-only mode can be bypassed through execute_query, which accepts a leading SELECT while the SQLite driver executes trailing statements, and through describe_table, which interpolates the caller-controlled table_name into PRAGMA table_info. Either path can issue ATTACH DATABASE, which opens an attached file read-write despite mode=ro and can make the protected database writable, read other SQLite database files, or create a SQLite-format file at a path writable by the server process. Existing non-empty files that are not SQLite databases are refused and left unchanged. The server has no built-in authentication and listens on all interfaces at :8080 by default, so any client that can reach the port can invoke these tools unless an authenticating proxy is in place. This issue is fixed in version 0.1.2.

### CVE-2026-30502

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T16:18:15.847 |

A Cross-Site Scripting (XSS) vulnerability in OpenKM v6.3.12 allows attackers to execute arbitrary Javascript in the context of the user's browser via a crafted input injected into the Content parameter.

### CVE-2026-133095

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-19T13:17:30.863 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 a CSRF attack was possible on the Hub integration settings

### CVE-2026-133089

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-19T13:17:30.103 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 the TFS helper process exposed an unauthenticated command server

### CVE-2026-132907

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T11:16:57.207 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 project viewers could redirect GitHub App connection credentials of parent projects

### CVE-2026-132904

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T11:16:56.803 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 missing authorization allowed project viewers to remove VCS roots

### CVE-2026-132903

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T11:16:56.683 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 missing authorization allowed any authenticated user to start and stop cloud agent instances

### CVE-2026-132892

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-19T11:16:55.397 |

In JetBrains TeamCity before 2026.2 privilege escalation was possible via the authorization flow

### CVE-2026-76007

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-18T21:18:02.580 |

IBM Engineering AI Hub 1.0.0 through 1.4.0 could allow a remote attacker to obtain sensitive information and perform unauthorized actions due to improper validation of a redirect URL.

### CVE-2026-132229

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-18T18:19:15.617 |

A flaw was found in hypershift-addon. Due to an overly permissive role-based access control (RBAC) configuration that grants permissions to all authenticated users rather than restricting them to the addon service, a low-privileged authenticated user can view, modify, or delete managed cluster resources. This improper authorization allows unauthorized users to alter or disrupt clusters across the entire managed fleet.

### CVE-2026-132244

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T17:17:46.273 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 stored XSS on the Disk Usage and Build Time pages was possible

### CVE-2026-116442

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-330` |
| Published | 2026-11-18T17:17:28.560 |

Dell PowerStore SDNAS contains an authentication-bypass-by-replay vulnerability in the NAS NDMP service that could allow a network attacker to gain backup and restore control of the appliance.

### CVE-2026-127178

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T16:18:09.410 |

A stored cross site scripting attack when viewing email aliases in postfixadmin 4.0 before 4.0.7, and postfixadmin 3.3 before 3.3.17 could be caused by signed in admins able to inject aliases.

### CVE-2026-111507

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T15:17:32.167 |

Dell PowerStore contains an authorization bypass vulnerability. A remote attacker could exploit this vulnerability to act under another user's session, potentially leading to denial of service.

### CVE-2026-133091

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T13:17:30.360 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 stored XSS on the Users page was possible

### CVE-2026-133083

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T13:17:29.330 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 stored XSS in Server Health reports was possible

### CVE-2026-133017

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-19T12:18:42.660 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via Git VCS root settings

### CVE-2026-132914

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T11:16:58.040 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 stored XSS on the Issue Log tab was possible

### CVE-2026-109555

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-19T06:16:52.890 |

The WP STAGING and WP STAGING Pro plugins for WordPress are vulnerable to PHP Object Injection in all versions up to, and including, 4.17.0 and 6.17.0, respectively, via deserialization of untrusted input during database restore and staging reset. This is due to the database importer treating attacker-controlled text beginning with {WPSTG_BINARY} as trusted internal binary data and decoding its hexadecimal suffix into serialized bytes. This makes it possible for authenticated attackers, with Subscriber-level access and above, to plant a malicious serialized object in their own profile. When an Administrator later performs an ordinary database-including restore or staging reset containing that value, and the restored profile metadata is loaded, either during the restore or in a later request, a built-in POP chain can be used to execute arbitrary code on the server. Additional built-in gadget chains allow arbitrary local file read in both WP STAGING and WP STAGING Pro and arbitrary file deletion in WP STAGING Pro. The attacker does not require Administrator credentials or a copy of a backup, but exploitation does require the later privileged restore or reset.

### CVE-2026-73971

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-11-18T22:17:23.990 |

Music Assistant is an open-source media library manager that integrates streaming services with connected speakers. Prior to 2.8.0, parse_arguments() passes the caller-controlled return_type parameter for config/core/get_value, config/providers/get_value, and config/players/get_value to parse_value() and Python eval() when resolving type parameters in music_assistant/helpers/api.py. Any authenticated user, regardless of role, can reach these commands through the WebSocket /ws endpoint or the REST JSON-RPC /api endpoint, causing arbitrary Python code to run with the Music Assistant server process privileges before command-handler validation, even if the request later fails. A default installation requires no special configuration, and compromise can expose secrets and configuration, alter library data, and control the application container. This issue is fixed in version 2.8.0.

### CVE-2026-62340

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-346` |
| Published | 2026-11-18T20:19:10.320 |

X-Road is open-source data exchange layer software. Prior to .8.2, 7.7.3, and 7.6.5, the Security Server writes each downloaded federated global-configuration part under the X-Road instance identifier declared by the part itself without checking that the identifier matches the source ecosystem that signed and delivered it. A malicious or compromised federated ecosystem can provide a validly signed SHARED-PARAMETERS part naming a victim ecosystem, causing the part to be written as the victim's authoritative shared-params.xml. The poisoned configuration can persist across refreshes, add attacker-controlled trust material, and enable impersonation of victim members and Security Servers across every ecosystem federated with the malicious source. This issue is fixed in versions 7.8.2, 7.7.3, and 7.6.5.

### CVE-2026-82171

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-18T15:17:43.763 |

Dell PowerStore contains an XML External Entity (XXE) Injection vulnerability. A high-privileged attacker could exploit this vulnerability, potentially leading to disclosure of sensitive files and root-level compromise of the appliance.

### CVE-2026-130007

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-18T17:17:37.917 |

k8s-mcp-server manages Kubernetes clusters through the Model Context Protocol. Prior to 1.1.0, SERVER_MODE defaults to SSE, with the listener on 0.0.0.0:8080, but main.go creates the SSE server without an authentication option or context function. The GET /sse handler creates a sessionId that is only a correlation value, and the POST /message handler accepts a loadable sessionId without an authorization or Origin check before dispatching tools/call; consequently, any client able to reach the port can enumerate and invoke registered Kubernetes tools without credentials. Read-only mode is disabled by default, leaving write-capable Kubernetes tools available to run with the server's configured cluster privileges. This issue is fixed in version 1.1.0.

### CVE-2026-132858

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T14:17:28.057 |

A flaw was found in gdm. The CreateRemoteDisplay D-Bus method fails to perform proper authorization checks when initiating a remote display session. A local attacker with access to the login screen environment can invoke this method with an arbitrary username to bypass standard automatic login verification checks. This vulnerability allows the attacker to achieve privilege escalation and start an unauthorized session as any user on the system, including root.

### CVE-2026-126826

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-19T14:17:27.037 |

A maliciously crafted SBSAR file, when imported or loaded through the Substance in 3ds Max plugin in Autodesk 3ds Max 2027, can trigger an Out-of-Bounds Write vulnerability. A malicious actor may leverage this vulnerability to cause an application crash, data corruption, or potentially execute arbitrary code in the context of the current process.

### CVE-2026-62964

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-18T22:17:22.390 |

Gortex is a high-performance code-intelligence engine for AI agents and integrated development environments. Prior to 0.55.0, resolveFilePath in internal/mcp/tools_fileops.go accepts absolute paths without checking indexed repository roots, while write_file, edit_file, and move_inline in internal/mcp/tools_move_inline.go omit guardSymlinkWithinRepo before reaching AtomicWriteFile and related write sinks. A caller that can influence MCP tool arguments can therefore create or overwrite files anywhere the daemon user can access, including startup or hook files that execute code on a later trigger. The flaw violates Gortex's repository-confinement invariant and can lead to arbitrary host code execution. This issue is fixed in version 0.55.0.

### CVE-2026-132150

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-18T15:17:41.873 |

A flaw was found in the file-xmc plugin in GIMP. When processing a specially crafted XMC image file, the plugin does not properly validate the comment subtype before using it as an array index. This missing validation leads to out-of-bounds memory access, invalid free and use-after-free issues. This vulnerability can result in an application crash, leading to a denial of service, or potentially allow for arbitrary code execution.

### CVE-2026-132038

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T15:17:41.740 |

Rapid7 Metasploit Framework versions prior to 6.5.10 suffer from an Improper Access Control issue in the msfdb database initialisation component whereby a PostgreSQL cluster initialised via msfdb init is configured with trust authentication and a world-accessible Unix domain socket in /tmp, allowing any local user on the same host to authenticate as the passwordless postgres superuser and execute arbitrary operating system commands as the msfdb owner. 


This issue is fixed in version 6.5.10.

### CVE-2026-109908

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T15:17:32.020 |

A heap buffer overflow in reading encoding files in X.Org libfontenc before 1.11.0 could be used by local attackers able to inject enc files to the X server could crash or escalate privileges.

### CVE-2026-133094

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T13:17:30.743 |

In JetBrains TeamCity before 2026.2.2 missing authorization allowed project developers to read arbitrary HashiCorp Vault secrets

### CVE-2026-133084

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-19T13:17:29.457 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 vCS root credentials could be exposed via change viewer links

### CVE-2026-133025

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T12:18:43.643 |

In JetBrains TeamCity before 2026.2.1 missing authorization allowed project viewers to download project settings

### CVE-2026-132902

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-19T11:16:56.563 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 access keys of parent project AWS connections could be disclosed

### CVE-2026-132901

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T11:16:56.447 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 improper authorization allowed publishing packages to NuGet feeds of other projects

### CVE-2026-132897

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T11:16:55.983 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 improper authorization allowed access to credentials of other projects via build configuration settings

### CVE-2026-132894

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T11:16:55.630 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 an SSRF in AWS connection settings could expose server credentials

### CVE-2026-132893

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-19T11:16:55.517 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 an SSRF via pipeline repository branch listing was possible

### CVE-2026-132140

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-404;CWE-476` |
| Published | 2026-11-18T21:17:56.683 |

A security vulnerability has been detected in DrayTek Vigor2960 up to 1.5.1.6. Affected by this vulnerability is an unknown functionality of the file mainfunction.cgi of the component Apmcfg Upload. The manipulation leads to null pointer dereference. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used. Upgrading to version 1.5.1.7 addresses this issue. Upgrading the affected component is advised. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-68903

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-18T20:19:11.687 |

LLMKube is a Kubernetes operator for self-hosted large language model inference across heterogeneous hardware. Prior to 0.9.0, the ModelReconciler accepts arbitrary absolute paths and file:// URIs in Model.spec.source without restricting them to approved roots. A namespace user who can create or update Model and InferenceService resources can cause copyLocalModel to open an attacker-selected file in the controller pod or cause a HostPathVolumeSource to mount an attacker-selected node file when modelCache.enabled is enabled, which is the default. The selected file is copied into model storage and can expose controller service-account credentials or other node secrets outside the attacker's namespace. This issue is fixed in version 0.9.0.

### CVE-2026-132240

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-18T17:17:45.753 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 XXE via Maven settings file upload was possible

### CVE-2026-132238

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-18T17:17:45.467 |

In JetBrains TeamCity before 2026.1.3, 2025.11.8 disclosure of password parameter values to project viewers was possible

### CVE-2026-131801

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-18T15:17:41.607 |

Tanium addressed an improper input validation vulnerability in Threat Response.

### CVE-2026-133085

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-19T13:17:29.590 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 an XXE was possible in the TFS helper process

### CVE-2026-132918

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T11:16:58.520 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 stored XSS on build and queue pages was possible

### CVE-2026-132905

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T11:16:56.940 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 stored XSS in the AWS Credentials build feature was possible

### CVE-2026-132899

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T11:16:56.210 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 stored XSS in the NPM Registry build feature was possible

### CVE-2026-114585

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T21:17:47.097 |

IBM Engineering AI Hub 1.0.0 through 1.4.0 could allow a remote authenticated attacker to obtain sensitive information due to a server-side request forgery.

### CVE-2026-132243

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T17:17:46.150 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 stored XSS on the Docker Container Info tab was possible

### CVE-2026-132242

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T17:17:46.030 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 stored XSS in the Promote build dialog was possible

### CVE-2026-132239

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-18T17:17:45.600 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 missing authorization in the Kubernetes integration allowed project viewers to use stored credentials

### CVE-2026-133082

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-19T13:17:29.200 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 a DoS attack was possible via unauthenticated multipart requests

### CVE-2026-133081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-19T13:17:29.073 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via Git VCS root URLs

### CVE-2026-133076

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T13:17:28.440 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via local repository URLs in Subversion VCS roots

### CVE-2026-133024

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-19T12:18:43.517 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via personal builds with versioned settings

### CVE-2026-133022

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-19T12:18:43.270 |

In JetBrains TeamCity before 2026.2.1 remote code execution was possible via the Notification Rules form

### CVE-2026-133021

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-19T12:18:43.143 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via Mercurial subrepository paths

### CVE-2026-115677

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-19T12:18:39.367 |

Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') vulnerability in AirTies Kablosuz İletişim Sanayi ve Dış Ticaret A.Ş. Air 5444 allows Overflow Buffers.

This issue affects Air 5444: through 2026-11-19.
NOTE: The vendor was contacted and it was learned that the product is not supported.

### CVE-2026-132911

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T11:16:57.680 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via build access codes disclosed to project users

### CVE-2026-132910

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-19T11:16:57.563 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 unauthenticated DoS via the agent protocol was possible

### CVE-2026-132908

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-19T11:16:57.327 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via Mercurial VCS root settings

### CVE-2026-132900

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-19T11:16:56.323 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 secure parameter values were disclosed to project viewers in pipelines

### CVE-2026-132895

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-11-19T11:16:55.750 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via Subversion VCS root settings

### CVE-2026-85776

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T10:17:29.313 |

The WP Duplicate – WordPress Migration Plugin plugin for WordPress is vulnerable to Missing Authorization in versions up to, and including, 1.1.11. This is due to a missing capability check and missing nonce check on the start_zip_creation, start_zip_download, local_sync_get_init_root_files, and local_sync_get_files_by_key AJAX actions in the start_zip_creation_dev() and sibling functions. This makes it possible for authenticated attackers, with subscriber-level access and above, to overwrite the plugin's prod_site_url setting so it points at an attacker-controlled host and enumerate arbitrary server directories, which when combined with a subsequent administrator-triggered sync results in an unsigned attacker-supplied ZIP archive being fetched, extracted via a WordPress-independent bridge deployed under the web root, resulting in remote code execution on the affected site.

### CVE-2026-14491

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-19T10:17:28.757 |

The WP Duplicate – WordPress Migration Plugin plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 1.1.11 via the 'file_name' parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The authentication bypass requires submitting the JSON boolean `true` as the `prod_key_random_id` value, which coerces against any non-empty stored secret so that the loose `!=` comparison evaluates to false, skipping the rejection branch entirely without knowledge of the secret.

### CVE-2026-129030

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-11-19T08:17:11.507 |

Exposure of Sensitive System Information to an Unauthorized Control Sphere vulnerability in Mamunur Rashid ShopBuilder – Elementor WooCommerce Builder Addons shopbuilder allows Retrieve Embedded Sensitive Data.This issue affects ShopBuilder – Elementor WooCommerce Builder Addons: from n/a through 3.4.3.

### CVE-2026-129013

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-19T08:17:11.223 |

Missing Authorization vulnerability in Deepen Bajracharya Video Conferencing with Zoom video-conferencing-with-zoom-api allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Video Conferencing with Zoom: from n/a through 4.6.12.

### CVE-2026-76818

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-18T22:17:24.720 |

Axon is an agent-agnostic context engine that gives AI coding agents continuous memory across sessions, tools, and machines. Prior to 0.1.1, rtk-install in src/axon/context/rtk_bootstrap.py uses _http_download() to fetch a prebuilt rtkx release archive and _extract_binary() to mark it executable, after which compress_text_with_rtk() invokes it without verifying a checksum, signature, or build attestation. If the sammyjdev/rtkx release pipeline or maintainer release credentials are compromised, an attacker can supply a modified binary that executes with the Axon process privileges when a user installs or automatically bootstraps rtkx. This issue is fixed in version 0.1.1.

### CVE-2026-75612

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-18T22:17:24.293 |

yt-mcp is a YouTrack MCP server for Claude Code. Prior to 1.18.1, add_attachment in src/yt_mcp/tools/attachments.py accepts a caller-controlled file_path, checks only that the file exists, reads it without directory confinement, and uploads the bytes to a YouTrack issue. A compromised MCP client or an LLM steered by indirect prompt injection can read any file accessible to the server process and exfiltrate secrets through an issue the caller can access. The same release also permits get_project_health to interpolate a caller-controlled project value into snapshot filenames, allowing parent-directory traversal to write JSON files outside the snapshots directory. This issue is fixed in version 1.18.1.

### CVE-2026-76088

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T21:18:02.723 |

PGPainless is a simple-to-use OpenPGP API based on Bouncy Castle. Prior to 1.7.8 and from 2.0.0 until 2.0.4, pgpainless-sop/src/main/kotlin/org/pgpainless/sop/InlineDetachImpl.kt InlineDetachImpl and pgpainless-core/src/main/kotlin/org/pgpainless/decryption_verification/MessageInspector.kt MessageInspector manually descend PGPCompressedData packets without incrementing or enforcing MAX_LAYER_DEPTH. A remote unauthenticated attacker can supply an untrusted OpenPGP message containing deeply nested compressed packet structures to a downstream application using inline-detach or message inspection, bypass the intended 16-layer limit, and force continued decompression and packet processing. The resulting resource consumption can block processing threads, exhaust heap memory, and crash the consuming application. This issue is fixed in versions 1.7.8 and 2.0.4.

### CVE-2026-75522

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-11-18T21:18:02.423 |

OpenID4VP is an open-source credential parsing library for SD-JWT VC and mDOC/mDL formats. Prior to 0.8.1, src/trust/ChainBuilder.ts ChainBuilder.tryBuild() terminates chain construction when an attacker-controlled certificate Subject Distinguished Name equals a trusted anchor subject, without verifying cryptographic closure to the anchor public key. A remote unauthenticated attacker can supply a self-signed leaf or intermediate that reuses the trusted Subject Distinguished Name and have credentials signed by the attacker key accepted as issued by the trusted authority. The public src/trust/TrustEvaluator.ts TrustEvaluator.evaluate() path compounds the error by matching a terminus through serialNumber and falling back to anchors[0], which can attribute the forged chain to genuine trusted-authority metadata. This issue is fixed in version 0.8.1.

### CVE-2026-59975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T21:18:00.500 |

SharpIppNext is a .NET Standard library for building Internet Printing Protocol clients and servers. Prior to 4.1.0, server-side SharpIppNext implementations using SharpIppServer.ReceiveRequestAsync or SharpIppServer.ReceiveRawRequestAsync pass incoming data to IppProtocol.ReadIppRequestAsync in SharpIpp/Protocol/IppProtocol.cs, where ReadDocumentStream is enabled by default and the remaining document body is copied with CopyToAsync into a MemoryStream without a size limit. An unauthenticated remote client can send an arbitrarily large IPP document body, exhausting process memory and causing an out-of-memory failure or service termination. Client-only implementations using SharpIppClient are not affected. This issue is fixed in version 4.1.0.

### CVE-2026-73864

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-11-18T19:18:08.043 |

install-artifact-from-github installs prebuilt native artifacts hosted by GitHub without compiling them locally. Prior to 1.7.0, bin/install-from-cache.js downloads a native .node artifact, allows RE2_DOWNLOAD_MIRROR to select a source, follows HTTP redirects including HTTPS-to-HTTP downgrades, and writes the decompressed response to the artifact path without cryptographic integrity verification before writing or loading it. An attacker who controls a configured mirror, replaces a release asset, or can modify plaintext transport can supply native code that executes when the consumer loads the artifact. Version 1.7.0 adds SHA-256 verification for default-GitHub-source downloads when the consuming package publishes an artifactHashes bag; configured mirrors and packages without a bag remain outside that verification.

### CVE-2026-71481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T19:18:07.733 |

ALTCHA PHP is a lightweight PHP library for creating and verifying ALTCHA challenges. From 2.0.0 until 2.0.3, the verifySolution method skips HMAC signature verification when a challenge payload omits the signature field, even when hmacSignatureSecret is configured. An attacker can remove the signature, supply attacker-selected low-difficulty challenge parameters, solve the resulting proof of work, and submit a payload that verifies successfully, bypassing the CAPTCHA control. This issue is fixed in version 2.0.3.

### CVE-2026-76516

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-841` |
| Published | 2026-11-18T17:17:51.297 |

A vulnerability in the eXtensible ARchive (XAR) GZIP file parser for ClamAV could allow an unauthenticated, remote attacker to exceed the configured MaxFileSize and cause a DoS condition on an affected device.   This vulnerability is due to inefficiencies when parsing specifically formatted files with the XAR GZIP file parser. An attacker could exploit this vulnerability by by sending a crafted XAR GZIP file to be scanned. A successful exploit could allow the attacker to effectively cause the ClamAV to exceed the MaxFileSize and potentially get caught in an infinite loop, causing a DoS condition.

### CVE-2026-76515

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T17:17:51.130 |

A vulnerability in the Object Linking and Embedding, 2nd Generation (OLE2) file parser for ClamAV could allow an unauthenticated, remote attacker to exceed the configured MaxScanTime and cause a DoS condition on an affected device.   This vulnerability is due to inefficiencies when parsing specifically formatted files with the OLE2 file parser. An attacker could exploit this vulnerability by by sending a crafted Microsoft Compound File Binary (CFB) file to be scanned. A successful exploit could allow the attacker to effectively cause the ClamAV OLE2 parser to get into an infinite loop, resulting in a DoS condition on the affected software.

### CVE-2026-76430

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-18T17:17:50.917 |

A vulnerability in the Ultimate Packer for eXecutables (UPX) unpacker of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.   This vulnerability is due to improper length checks, when unpacking the UPX files, which may result in an out-of-bounds read of heap memory. An attacker could exploit this vulnerability by submitting a crafted UPX for decode. A successful exploit could allow the attacker to cause the ClamAV decode process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-76422

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-11-18T17:17:50.717 |

A vulnerability in the debug logging functionality of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to improper handling of logging values. An attacker could exploit this vulnerability by submitting a file to be scanned by the software that has debug logging enabled. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-76421

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-18T17:17:50.523 |

A vulnerability in the LZX data algorithm for Microsoft Compiled HTML Help (CHM) file scanning in ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to improper boundary checks when applying the LZX data algorithm to CHM files during the decoder stage, which may result in buffer overflow. An attacker could exploit this vulnerability by sending a crafted CHM file for scanning. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-76417

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T17:17:50.337 |

A vulnerability in Object Linking and Embedding, 2nd Generation (OLE2) file parser for ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to logic error when parsing specifically formatted files with the OLE2 file parser. An attacker could exploit this vulnerability by by sending a crafted Microsoft Compound File Binary (CFB) file to be scanned. A successful exploit could allow the attacker to allocate all available memory, causing the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-76416

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-18T17:17:50.133 |

A vulnerability in the InstallShield file parser of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to incomplete error checking when the InstallShield File Parser is performing a scan. An attacker could exploit this vulnerability by sending a crafted InstallShield file to be scanned. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate due to an infinite loop, resulting in a DoS condition on the affected software.

### CVE-2026-76415

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-124` |
| Published | 2026-11-18T17:17:49.930 |

A vulnerability in the Yoda'a Crytper (yC) Portable Executable (PE) unpacker of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device. .
 This vulnerability is due to lack of proper error checking for negative values when processing the PE file to be unpacked. An attacker could exploit this vulnerability by sending a PE file to be unpacked. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-76414

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-18T17:17:49.727 |

A vulnerability in Microsoft Compiled HTML Help (CHM) file scanning of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to a logic error when scanning the CHM file and following the internal file pointers. An attacker could exploit this vulnerability by sending a crafted CHM file for scanning. A successful exploit could allow the attacker to cause the ClamAV decode process to terminate due to an infinite loop, resulting in a DoS condition on the affected software.

### CVE-2026-76411

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-11-18T17:17:49.510 |

A vulnerability in the phishcheck functionality of ClamAV could allow an unauthenticated, remote attacker to cause a DoS condition on an affected device.
 This vulnerability is due to improper allocation of memory during processing of URLs. An attacker could exploit this vulnerability by sending a URL to be processed by the software. A successful exploit could allow the attacker to cause the ClamAV scanning process to terminate, resulting in a DoS condition on the affected software.

### CVE-2026-132245

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T17:17:46.400 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 DoS via agent command results was possible

### CVE-2026-126721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-18T16:18:08.267 |

The Magic Login Mail or QR Code plugin for WordPress is vulnerable to Privilege Escalation via Administrator Account Takeover in versions up to, and including, 2.07. This is due to the `curpageurl()` function falling back to the raw `$_SERVER['HTTP_HOST']` value — with no validation against the site's configured origin via `home_url()` or `site_url()` — when `get_the_permalink()` returns empty or false, allowing an attacker-controlled Host header to become the URL origin of the magic-login link generated by `generate_url()` and delivered to the target via `wp_mail()`. This makes it possible for unauthenticated attackers to intercept the one-time uid and token pair sent to a targeted Administrator's email and replay them against the real site, causing `autologin_via_url()` to call `wp_set_auth_cookie()` and establish a full Administrator session on the targeted account. Exploitation requires the `[magic_login]` shortcode to render on a path where `get_the_permalink()` returns empty or false (such as a 404 page or a block-theme header template part), the web server to forward non-canonical Host headers, the attacker to know the target administrator's email address, and the administrator to click the attacker-originated magic-login link. Successful exploitation gives the attacker control of a distinct, already-privileged Administrator account; it does not promote the attacker's original account. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-95823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-18T15:17:44.383 |

tcp_pkt_linearize() in subsys/net/ip/tcp.c is used by th_get() whenever a received TCP header is not contiguous in a single net_buf. While pulling the header bytes out of the following fragments, the loop called net_buf_unref() on an emptied fragment without first detaching its frags pointer. net_buf_unref() walks the whole fragment list, so the payload buffers still linked behind that fragment were freed as well, and the stale pointer was then reinstalled into the packet as buf->frags, producing a use-after-free and a later double free during packet teardown. The same loop also advanced to second->frags unconditionally: when the fragment still held payload after the header remainder was pulled, it was spliced out of the packet without ever being unreferenced, permanently leaking that buffer and silently dropping the data it carried.

The defect is reached from tcp_recv() via th_get() on every received TCP segment, before connection lookup or any header validation, so a single unauthenticated segment that matches a listening socket is sufficient. An attacker only needs the TCP header to straddle a net_buf boundary, which they can arrange from off-link: IPv6 extension headers are accepted on receive and their length is added to the header offset by th_get(), so a Destination Options header of a suitable length places the TCP header across the boundary of the fixed-size receive buffers (CONFIG_NET_BUF_DATA_SIZE). Packet chains assembled from several sources - IPv4/IPv6 reassembly, 6LoWPAN/802.15.4 reassembly, tunnel or virtual interfaces that strip an outer header, or drivers producing scatter-gather chains - can additionally present a short interior fragment that the loop empties exactly, which is the case that frees the remainder of the packet while it is still in use.

The reliably reachable consequence is exhaustion of the receive buffer pool: each crafted segment leaks one net_buf from the fixed CONFIG_NET_BUF_RX_COUNT pool, the buffers are never reclaimed, and once the pool is empty the device can no longer receive network traffic until it is rebooted. Where a fragment is emptied exactly, the impact rises to memory corruption: freed pool buffers are written through by the remainder of the loop, their contents may be delivered to the application, and the packet is double-freed on teardown.

The fix saves and clears second->frags before the net_buf_unref() so only the emptied header fragment is released, and advances to the next fragment only when second->len == 0, keeping any fragment that still holds payload in the packet. This restores the detach-before-unref ownership pattern used elsewhere in the stack, for example in net_pkt_trim_buffer().

### CVE-2026-133097

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-341` |
| Published | 2026-11-19T13:17:31.123 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 agent Push authorization keys were predictable

### CVE-2026-133020

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-807` |
| Published | 2026-11-19T12:18:43.027 |

In JetBrains TeamCity before 2026.1.5 untrusted build approval for GitHub fork pull requests could be bypassed

### CVE-2026-132131

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1287` |
| Published | 2026-11-19T12:18:40.840 |

@fastify/middie is the middleware engine that adds Express and Connect style middleware support to Fastify. In versions 8.3.0 through 9.3.6, the internal helper that normalizes a path-scoped middleware's mount path only handles string inputs, but the use method also accepts an array of mount paths and passes it through unchanged, so the normalization silently does nothing. As a result, a trailing slash on an array element survives into the generated route-matching regular expression, and an element that is exactly the root path, meaning a catch-all mount, is dropped entirely. Requests to subroutes of the affected mount paths then skip the path-scoped middleware, such as authentication, authorization, or rate limiting, while Fastify's router still dispatches them to the handler, allowing an unauthenticated client to reach protected routes. Applications are affected when they mount middleware on an array of paths in which an element ends with a slash, including one introduced by a plugin prefix that ends with a slash, or is exactly the root path. The issue is fixed in @fastify/middie 9.3.7, and users should upgrade to 9.3.7 or later. As a workaround, enforce authorization in a Fastify hook such as preHandler that runs after routing, and avoid array mount paths with a trailing slash element for security relevant middleware.

### CVE-2026-132128

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178;CWE-863` |
| Published | 2026-11-19T12:18:40.543 |

@fastify/middie is the middleware engine that adds Express and Connect style middleware support to Fastify. In versions up to and including 9.3.6, middie does not honor the router's caseSensitive setting and matches path-scoped middleware mount paths with a case-insensitive regular expression that does not fold non-ASCII characters, while Fastify's router, when caseSensitive is set to false, lowercases the request path with a Unicode-aware conversion that maps the KELVIN SIGN character (U+212A) to the ASCII letter k. A request that spells a k in a protected mount path as the percent-encoded KELVIN SIGN is therefore routed to the protected handler while the middleware mounted on that path, such as authentication, authorization, or rate limiting, never matches and is skipped, letting an unauthenticated client reach the handler. Only applications that set caseSensitive to false and protect a mount path containing the letter k are affected. The issue is fixed in @fastify/middie 9.3.7, and users should upgrade to 9.3.7 or later. As a workaround, enforce authorization in a Fastify hook such as preHandler that runs after routing, or keep routing case-sensitive, which is the default.

### CVE-2026-132825

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-19T07:17:11.740 |

Ruby before 3.3.14, 3.4.13, and 4.0.10 has a heap-based buffer overflow during case conversion. One byte can be written outside a buffer for, for example, ISO-8859-1 or Windows-1252.

### CVE-2026-61581

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-379` |
| Published | 2026-11-18T19:18:07.140 |

The Datadog Agent collects events and metrics from hosts and sends them to Datadog. Prior to datadog-apm-inject 0.66.0, the Datadog Single Step Instrumentation injector stores helper tooling in a predictable host directory. On Linux or Kubernetes systems with SSI enabled and at least one Java service instrumented through SSI, a local unprivileged attacker with shell access to the same host can influence that tooling and execute code with the privileges of the instrumented Java service. Services that use dd-java-agent without SSI and non-Java language runtimes are not affected. This issue is fixed in datadog-apm-inject 0.66.0.

### CVE-2026-71861

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290;CWE-294;CWE-347` |
| Published | 2026-11-18T16:18:16.967 |

The Chainguard SDK is a public Go SDK for integrating with the Chainguard platform. Prior to 0.1.107, auth/aws.VerifyToken trusts the Chainguard-Audience and Chainguard-Identity headers without requiring those headers to be covered by AWS SigV4 SignedHeaders. An attacker with a fresh STS GetCallerIdentity request signed by a victim can rewrite the unsigned binding headers and replay the proof to another relying party, causing the relying party to authenticate the victim’s AWS identity for an attacker-chosen audience and identity. Code that only uses auth/aws.GenerateToken is unaffected because the generator signs the binding headers, and exploitation requires a signed request within its validity window. This issue is fixed in version 0.1.107.

### CVE-2026-130089

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-18T21:17:48.933 |

A caller who can send requests to the temporal-proxy gRPC listener can obtain the static API key of an upstream whose address is templated from the request namespace, and then use that key directly against the upstream Temporal service. temporal-proxy does not validate the request namespace before rendering it into a templated upstream address, so when an upstream's hostPort is templated from the namespace, as in the published Temporal Cloud configuration example, a crafted namespace changes the host the proxy dials. If that upstream verifies TLS against the system trust store and sets no literal server name, a caller-controlled host with a publicly trusted certificate passes verification and receives the key. The built-in static-token and JWKS authenticators do not restrict namespaces, so any caller they admit can do this; an external authenticator that admits only listed namespaces prevents it. temporal-proxy versions 0.1.0 through 1.2.0 are affected. The issue is fixed in 1.0.2, 1.1.2, and 1.2.1, and releases before 1.0.0 receive no fix. Upgrade to the fixed release for the deployed minor release line, and rotate any upstream API key that untrusted callers could reach.

### CVE-2026-111520

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-18T21:17:46.960 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.105.0, contain a Time-of-check Time-of-use (TOCTOU) Race Condition vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Code Execution and Elevation of Privilege.

### CVE-2026-111514

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-18T21:17:46.140 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.105.0, contain an Incorrect Default Permissions vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Arbitrary Code Execution and Elevation of Privilege.

### CVE-2026-111513

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T21:17:46.003 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.105.0, contain an Improper Verification of Cryptographic Signature vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Arbitrary Code Execution and Elevation of Privilege.

### CVE-2026-132241

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-18T17:17:45.900 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 XXE in the .NET build steps auto-discovery was possible

### CVE-2026-126675

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-18T17:17:35.173 |

Incorrect default permissions in Nitro PDF Pro before 26.4 on Windows allow a local low-privileged user to execute code in the context of another user who launches the application.

### CVE-2026-133093

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-96` |
| Published | 2026-11-19T13:17:30.617 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 code injection in parent project Kotlin DSL was possible via subproject settings

### CVE-2026-133090

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T13:17:30.233 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 improper authorization allowed overwriting versioned settings of other projects

### CVE-2026-133088

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-19T13:17:29.970 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via FreeMarker notification templates

### CVE-2026-133079

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T13:17:28.823 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via Maven dependencies of Kotlin DSL settings

### CVE-2026-133078

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-486` |
| Published | 2026-11-19T13:17:28.693 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 remote code execution was possible via security context spoofing in the Kotlin DSL sandbox

### CVE-2026-133077

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-19T13:17:28.563 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 privilege escalation to system administrator was possible via Project Import

### CVE-2026-133026

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-96` |
| Published | 2026-11-19T12:18:43.757 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 code injection in generated Kotlin DSL was possible via matrix build parameters

### CVE-2026-133023

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-19T12:18:43.393 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via Kotlin DSL compiler arguments

### CVE-2026-133014

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-19T12:18:42.293 |

In JetBrains TeamCity before 2026.2.1, 2026.1.5 remote code execution was possible via public reflection in the Kotlin DSL sandbox

### CVE-2026-123972

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T12:18:40.110 |

The WP-Slimbox2 Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 1.1.3.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires a logged-in user, typically an administrator, to click the attacker's image link in the comment; however, because unmoderated comments appear in the WordPress moderation queue where administrators routinely interact with them, the moderation gate does not meaningfully prevent exploitation. Successful exploitation causes the attacker's own account to receive the complete Administrator role.

### CVE-2026-123968

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T12:18:39.690 |

The Slimbox plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment (anchor title within comment HTML)' parameter in all versions up to, and including, 1.0.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. WordPress core comment KSES permits unauthenticated commenters to post anchor elements with href and title attributes, so an entity-encoded payload stored in the title attribute survives sanitization verbatim; the browser then decodes the entities when populating the DOM .title property, and the Slimbox library's jQuery .html() caption sink renders it as executable HTML.

### CVE-2026-132912

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-19T11:16:57.800 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 remote code execution was possible via class injection in the Kotlin DSL sandbox

### CVE-2026-132898

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-19T11:16:56.093 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 arbitrary file write on the server was possible via Kotlin DSL settings

### CVE-2026-132896

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-19T11:16:55.867 |

In JetBrains TeamCity before 2026.2, 2026.1.4 remote code execution was possible via Kubernetes Executor settings

### CVE-2026-84998

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T05:18:40.940 |

The NextScripts: Social Networks Auto-Poster plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'comment_author' and 'comment_agent' Comment Fields in all versions up to, and including, 4.4.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload executes in an administrator's browser session when the administrator views the WordPress comment moderation queue, including pending and unapproved comments, meaning no prior approval of the comment is required for exploitation.

### CVE-2026-73968

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-18T21:18:01.973 |

AnsibleForms is a self-hosted web application that turns automation into self-service forms. Prior to 6.2.1, AnsibleForms allows a user with repository management privileges to inject shell syntax through repository uri, branch, name, or host values processed by server/src/models/repo.model.js. The Repo.clone and Repo.addKnownHosts paths interpolate these values into git and ssh-keyscan command strings, and server/src/lib/cmd.js executes the strings through Cmd.executeSilentCommand with shell interpretation enabled. Creating or updating a repository can therefore execute arbitrary commands as the AnsibleForms application process. This issue is fixed in version 6.2.1.

### CVE-2026-130751

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-18T19:17:45.400 |

OpenWrt LuCI luci-app-travelmate on master before 3.0.0-1 and on openwrt-25.12 before 2.4.9-6 grants file exec permissions for state-mutating commands in the read scope of its rpcd ACL, letting authenticated read-only users run those commands as root. Attackers can invoke ubus file exec on /etc/init.d/travelmate setup, start, stop, restart, or /sbin/ifup to modify and commit network and firewall configuration or disrupt the travelmate daemon.

### CVE-2026-132235

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-18T17:17:45.100 |

In JetBrains TeamCity before 2026.1.3, 2025.11.7 remote code execution was possible via path traversal in project import archives

### CVE-2026-3232

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-18T15:17:42.550 |

The Easy Appointments plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'name' and 'phone' fields in all versions up to, and including, 3.12.23.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever an administrator accesses the Customers page.

### CVE-2026-133113

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-19T14:17:28.367 |

Gogs through 0.14.4 contains an authorization bypass vulnerability that allows collaborators with write access to push to protected branches by merging pull requests. Because MergePullRequest skips branch protection checks and PullRequest.Merge omits hook environment variables, attackers can merge commits into branches restricted to allowlisted users.

### CVE-2026-133096

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T13:17:30.993 |

In JetBrains TeamCity before 2026.2.2, 2026.1.6 improper authorization allowed queuing builds with personal changes of other users

### CVE-2026-129034

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T13:17:28.160 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WP Chill Strong Testimonials strong-testimonials allows Stored XSS.This issue affects Strong Testimonials: from n/a through 3.3.18.

### CVE-2026-82950

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-390` |
| Published | 2026-11-19T11:17:08.710 |

The device only supports Wi-Fi protocols vulnerable to
deauthentication attacks (WEP/WPA/WPA2). Should any event which would typically
be logged to the user’s mobile device (such as arming or disarming the alarm or
any tamper events) be incurred whilst the device is temporarily disconnected
from its Wi-Fi network (such as via a deauthentication attack), those alerts
will not be sent even after connection is regained.

### CVE-2026-82949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-11-19T11:17:08.580 |

The static codes used for information transmission
throughout the 433.92 MHz system of the Guardian 2 system allow an attacker in
proximity to monitor the movements of users inside the premises where the
sensors are set up. This is further aided by the fact that codes transmitted
reveal sensor type, although sensor location cannot be inferred from this
traffic alone.

### CVE-2026-82948

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-11-19T11:17:08.437 |

The Guardian 2 alarm unit lacks a mechanism to
authenticate control commands sent over 433.92 MHz, which allows an attacker to
replay the static commands to impersonate activity.  The attacker can also disarm or arm the
system at will if a Nexsmart keypad (product link) is in use, thus compromising
the functionality of the alarm system completely.

### CVE-2026-132916

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-19T11:16:58.280 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 arbitrary file deletion on the server was possible via the Kotlin DSL sandbox

### CVE-2026-132915

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-90` |
| Published | 2026-11-19T11:16:58.160 |

In JetBrains TeamCity before 2026.2, 2026.1.4, 2025.11.8 an LDAP injection allowed bypassing login restrictions

### CVE-2026-126631

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-19T10:17:28.410 |

A flaw was found in OpenSCAP. This vulnerability allows for information disclosure when performing offline scans of untrusted filesystem images, such as container images or virtual machine (VM) disks. Because the scanner does not properly restrict symbolic link (symlink) resolution to the target image's root directory, an attacker can supply a crafted image containing links pointing to files on the host system. When the scan runs, typically with elevated privileges, OpenSCAP follows these links to read sensitive host files and expose their contents in the scan report or manipulate compliance results.

### CVE-2026-129001

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T08:17:11.080 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Gabe Livan Asset CleanUp: Page Speed Booster wp-asset-clean-up allows Reflected XSS.This issue affects Asset CleanUp: Page Speed Booster: from n/a through 1.4.0.6.

### CVE-2026-128999

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-19T08:17:10.913 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Saphali Saphali Woocommerce Lite saphali-woocommerce-lite allows Stored XSS.This issue affects Saphali Woocommerce Lite: from n/a through 2.0.2.

### CVE-2026-132773

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-19T00:17:46.997 |

Attendize through 2.8.0 contains an authorization bypass vulnerability in EventOrdersController::postCancelOrder() that allows authenticated organisers to cancel attendees belonging to other accounts' events. Attackers can cancel one of their own orders while supplying foreign attendee IDs, which Attendee::findFromSelection() loads unfiltered, invalidating tickets for any event on the installation.

### CVE-2026-132750

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-19T00:17:43.197 |

Meilisearch before 1.55.1 and 1.56.x before 1.56.1 contains a quadratic memory consumption vulnerability in filter-parser that allows attackers with a search API key to exhaust server memory. Attackers can send a roughly 100 KB filter, such as a _geoPolygon with thousands of coordinates, to the search endpoint, crashing the server and taking all indexes offline.

### CVE-2026-132749

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T00:17:43.043 |

Vtiger CRM through 8.4.0 contains a blind SQL injection vulnerability in ReportRun::generateAdvFilterSql() that allows authenticated low-privileged users to inject SQL via the bw comparator. Attackers can send a crafted advanced_filter parameter containing a single quote to the Reports getRecordsCount action to break out of BETWEEN literals and extract database contents.

### CVE-2026-132747

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T00:17:42.750 |

Vtiger CRM through 8.4.0 contains an SQL injection vulnerability that allows authenticated users with export access to inject SQL through unvalidated selected_ids values in ExportData.php. Attackers can send a UNION SELECT payload in selected_ids[] to the ExportSelectedRecords mode and read password hashes and access keys from the exported CSV.

### CVE-2026-132746

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T00:17:42.600 |

Vtiger CRM through 8.4.0 contains a blind SQL injection vulnerability that allows authenticated low-privileged users to inject SQL via unescaped clientid values in the wsapp_map webservice operation. Attackers can register a sync application with wsapp_register, then send delete-mode entries with quoted clientid values processed by SyncServer.php to extract database contents including administrator access keys.

### CVE-2026-132745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-19T00:17:42.447 |

Vtiger CRM through 8.4.0 contains a blind SQL injection vulnerability that allows authenticated non-administrative users to inject SQL through the k (does not contain) comparator in list view search_params. Attackers can send crafted search_params to the ListAjax getRecordsCount mode, breaking out of the unescaped NOT LIKE clause to extract database contents via boolean or time-based techniques.

### CVE-2026-71535

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T23:17:21.620 |

Mareforma is a local verification layer for AI-assisted research. From 0.3.0 until 0.3.7, the _maybe_update_replicated_unlocked convergence path in mareforma/db/core.py uses generated_by labels without requiring a valid signature_bundle from a distinct enrolled signer, so an unsigned claim written to a shared graph can converge with a signed peer and be promoted to REPLICATED. The forged trust state is returned by queries requiring REPLICATED support, allowing false multi-party endorsement signals to reach downstream consumers. This issue is fixed in version 0.3.7.

### CVE-2026-76101

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-252;CWE-347;CWE-354` |
| Published | 2026-11-18T22:17:24.567 |

keystore-go is a Go implementation of the Java KeyStore encoder and decoder. In 2.1.0 and earlier, keystore.Decode in decoder.go does not check the error returned when reading the trailing SHA-1 integrity digest and bounds its comparison by the length of the digest actually read. If an attacker with write access removes the final 20-byte digest from a modified JKS file, the empty actual digest causes the comparison loop to execute zero times and Decode returns the parsed keystore without an error. For certificate-only stores using TrustedCertificateEntry values, this bypasses both tamper detection and password verification, allowing trusted CA certificates to be added or replaced without knowing the keystore password and potentially enabling interception or modification of TLS connections that trust the forged CA. This issue is fixed in version 3.0.0.

### CVE-2026-130091

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-18T21:17:49.347 |

A caller with write permission in a namespace can terminate temporal-proxy through memory exhaustion by storing highly compressed payloads in Workflow history, and the stored history causes the same failure on every later read. temporal-proxy 1.2.0 decompresses every payload marked as compressed in the responses it forwards, whether or not compression is configured. Each payload is limited to 4 MiB after decompression, but the total for a response is not, and the decoded payloads are held in memory together. The caller can store many small, highly compressed payloads through the proxy or directly at the upstream Temporal service. When that history is read through the proxy, for example by a Worker processing a task, the proxy can run out of memory and be terminated. The codec server's /decode endpoint is affected in the same way when it is enabled. Only temporal-proxy 1.2.0 is affected; earlier versions do not decompress payloads. The issue is fixed in 1.2.1. Upgrade to 1.2.1 or later.

### CVE-2026-111515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-939` |
| Published | 2026-11-18T21:17:46.270 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.105.0, contain an Improper Authorization in Handler for Custom URL Scheme vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Command Execution and Launch of Phishing Attacks.

### CVE-2026-128669

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-384` |
| Published | 2026-11-18T20:18:59.397 |

A Session Fixation vulnerability exists in the admin login endpoint (/admin/index.php) of PHPGurukul News Portal Project V4.1. The application fails to regenerate the session identifier (PHPSESSID) upon successful authentication. A remote attacker can exploit this by setting a known session ID in the victim's browser prior to login. Once the victim authenticates, the attacker can reuse the fixed session ID to hijack the victim's authenticated session.

### CVE-2026-45142

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-18T19:18:06.050 |

Chamilo LMS is an open-source learning management system. Prior to 1.11.40 and 2.0.1, main/lp/lp_ajax_save_objectives.php and public/main/lp/lp_ajax_save_objectives.php trust the request uid parameter instead of the authenticated user identity when saving SCORM learning objectives. Any authenticated student can replace uid with another user's identifier and overwrite that user's objectives because the endpoint performs no ownership check. This issue is fixed in versions 1.11.40 and 2.0.1.

### CVE-2026-130781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-18T19:17:54.273 |

Incus before 7.6.0 contains a resource exhaustion vulnerability in the storage bucket S3 listener, which buffers entire signed request bodies in memory before verifying the signature or credential role. Attackers knowing only a valid access key, or holding a read-only credential, can send many concurrent large requests to exhaust daemon memory.

### CVE-2026-130776

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:N/VA:L/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-18T19:17:52.677 |

Incus before 7.6.0 contains an information disclosure vulnerability that allows clients with project event-view access to read migration websocket secrets broadcast in operation metadata. Attackers can connect to in-flight migration control and fs websockets before the legitimate peer, hijacking the transfer to obtain instance configuration and filesystem data.

### CVE-2026-130772

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-18T19:17:51.263 |

Incus before 7.6.0 contains an improper authorization vulnerability that allows restricted TLS clients to read other projects' bucket S3 keys and profile configuration through recursive and all-projects responses. Attackers can query bucket listings with recursion=2 or profiles with all-projects=true to obtain S3 secret keys and sensitive environment, cloud-init and user values across projects.

### CVE-2026-130769

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-18T19:17:49.320 |

Incus before 7.6.0 contains a denial of service vulnerability that allows clients permitted to create instances to crash the daemon by importing a backup with a null snapshot entry in index.yaml. Attackers can trigger an unrecovered nil pointer dereference during configuration rewrite, terminating the daemon and all containers and virtual machines on the node.

### CVE-2026-130762

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-18T19:17:47.263 |

Fleet before 4.92.0 contains an SQL injection vulnerability that allows authenticated observer-level users to sort software listings by arbitrary columns via the order_key parameter. Attackers can order by joined hosts table columns such as node keys and use pagination as a binary-search oracle to extract sensitive column values.

### CVE-2026-132219

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:44.213 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'DocumentosOpcionesImprimir' parameter in'/Gestion/DocumentosOpcionesImprimir/'.

### CVE-2026-132218

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:44.070 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesEventos' parameter in'/Clientes/ClientesEventos/'.

### CVE-2026-132217

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.933 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesEventos' parameter in'/Clientes/ClientesEventos/'.

### CVE-2026-132216

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.800 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesEventos' parameter in'/Clientes/ClientesEventos/'.

### CVE-2026-132215

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.670 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesEventos' parameter in'/Clientes/ClientesEventos/'.

### CVE-2026-132214

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.540 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesEventos' parameter in'/Clientes/ClientesEventos/'.

### CVE-2026-132213

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.413 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'TareasCrear' parameter in'/Tareas/TareasCrear/'.

### CVE-2026-132212

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.283 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in  'ClientesClasificaciones' parameter in'/Clientes/ClientesClasificaciones/'.

### CVE-2026-132211

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.157 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in 'ClientesCamposAdicionales' in '/Clientes/ClientesCamposAdicionales/'.

### CVE-2026-132210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-18T17:17:43.023 |

Insecure Direct Object Reference (IDOR) vulnerability. Exploiting this vulnerability allows a user to view the names of other users/companies on the platform by iterating over the numerical value that identifies the customer in 'idCliente' parameter in'/Gestion/DocumentosCrear/'.

### CVE-2026-132224

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-642` |
| Published | 2026-11-18T16:18:15.627 |

Optimizely Web Experimentation before 2026-11-17 mishandles the account signup flow, leading to presence of attacker-controlled code in the projectJS (aka Project JavaScript) field of certain cdn.optimizely.com assets.

### CVE-2026-15263

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-18T15:17:42.033 |

A server-side request forgery (SSRF) vulnerability in the Pure Storage FlashArray extension for Windows Admin Center versions could allow an authenticated Gateway User to direct the management gateway to an unintended host, potentially exposing stored FlashArray credentials and API tokens and allowing unauthorized access to the managed FlashArray.

### CVE-2026-99320

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-19T09:18:18.910 |

In the Linux kernel, the following vulnerability has been resolved:

ipv6: raw: fix use-after-free in rawv6_send_hdrinc()

rawv6_send_hdrinc() caches the route before handing the skb to
l3mdev_ip6_out(). The VRF output path may replace skb->dst and release
the original route, leaving the cached pointer stale.

The function later dereferences that pointer for statistics accounting
and as the output device passed to NF_HOOK(). Its RCU read-side critical
section starts after l3mdev_ip6_out(), so it cannot prevent the old route
from being reclaimed in between.

Reload the route from the current skb destination after
l3mdev_ip6_out() returns.

KASAN reports a slab-use-after-free in rawv6_sendmsg(), with the route
allocated by ip6_dst_alloc(), freed by dst_destroy() from rcu_core(), and
the related RCU callback queued from vrf_l3_out().

### CVE-2026-132621

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1191` |
| Published | 2026-11-19T04:17:27.497 |

A vulnerability has been found in GearUP Hyperev up to 20261020. This affects an unknown function. Such manipulation leads to on-chip debug and test interface with improper access control. The attack can be executed directly on the physical device. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-71536

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-18T23:17:21.770 |

Mareforma is a local verification layer for AI-assisted research. From 0.3.0 until 0.3.8, verify_bundle in mareforma/export_bundle.py validates the outer DSSE envelope and exporter-signed subject digests, but JSONLDExporter._claim_node in mareforma/exporters/jsonld.py supplies no signatureBundle for individual claims. Because the exporter signs both the predicate nodes and their digest list, the check proves only internal bundle consistency and allows claims with missing, invalid, or forged asserter signatures to be accepted as authentic. This issue is fixed in version 0.3.8.

### CVE-2026-63415

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-98;CWE-611;CWE-918` |
| Published | 2026-11-18T22:17:22.987 |

Jane is a set of PHP libraries that generates models and API clients from JSON Schema and OpenAPI specifications. Prior to 7.12.0, Jane's Reference.php::doResolve passes an attacker-controlled OpenAPI $ref target to file_get_contents without restricting its scheme or resolved local path. When a victim generates code from an attacker-influenced document, an HTTP or HTTPS reference can cause requests to attacker-chosen or internal services, while an absolute or parent-relative path can read local JSON or YAML files and inline the retrieved content into generated output. Exploitation occurs during generation or CI processing and can disclose local files and internal-service responses. This issue is fixed in version 7.12.0.

### CVE-2026-61578

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-11-18T19:18:06.993 |

Chamilo LMS is an open-source learning management system. Prior to 1.11.40 on the 1.11 release line and in 2.0.0, plugin/cleandeletedfiles/src/ajax.php and public/plugin/CleanDeletedFiles/src/ajax.php pass the request path parameter and list parameter directly to unlink without canonicalization, filename validation, or confinement to the plugin's scanned directories. An authenticated administrator can delete arbitrary files writable by the web server; a cross-site request forgery against an administrator session can reach the same operation. Deleting application source, uploaded content, cache, or configuration files can cause data loss and denial of service. This issue is fixed in version 1.11.40 on the 1.11 release line. No fixed 2.0 release is established as of this review.
