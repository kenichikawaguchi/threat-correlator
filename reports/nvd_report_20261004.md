# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-03 15:01 UTC
- **対象期間**: `2026-10-02T15:00:43.000Z` 〜 `2026-10-03T15:01:23.000Z`
- **重要CVE数**: 87 件（Critical 9.0+: 18 件 / High 7.0〜: 69 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 40 件**以上に上り、リモートからのコード実行・認証バイパスが目立ちます。  
- **クラウド／コンテナ基盤（AWS Loom、GitLab AI Gateway、NASA AIT‑Core）**、**Web ブラウザ（Chrome）**、**Node.js ライブラリ（Tinypool、Seroval）** が特に集中しており、攻撃者は「認証なし」または「低権限」でも管理者権限取得が可能になるケースが多数です。  
- 多くの脆弱性は **Zero‑day でのリモートコード実行（RCE）**、**認証情報漏洩・改竄**、**プロセス権限昇格** といった **機密性・完全性・可用性** に対する深刻なインパクトを持ち、早急なパッチ適用が求められます。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|------------|------------------------|
| **CVE‑2026‑103956** | 10.0 | **認証なしで super‑admin 権限取得**（Loom for AWS の認証依存モジュールに認証欠如） | 攻撃者はエージェント制御プレーンに対し、ツールサーバ登録、IAM ロールポリシー改竄、保存された統合クレデンシャル取得が可能。AWS 環境全体の権限委譲が危険に。 |
| **CVE‑2026‑103628** | 9.6 | **WebGL のアウト・オブ・バウンズ書き込み**（Chrome < 154.0.8037.97） | 悪意ある HTML ページを閲覧させるだけでサンドボックス外のコード実行が可能。企業内の Web ブラウザ全般が対象。 |
| **CVE‑2026‑104846** | 9.8 | **Seroval の Promise 逆シリアライズ**（fromJSON が任意の thenable をネイティブ Promise に注入） | 攻撃者が制御できる JSON を注入すると、任意コード実行や情報漏洩が起こり得る。Node.js アプリケーションで Seroval 0.12.0‑1.6.2 が使用されている場合に危険。 |
| **CVE‑2026‑90970** | 9.9 | **GitLab AI Gateway の認証バイパス**（特定条件下で Duo Agent Platform ユーザーが権限エスカレーション） | GitLab の AI 機能を利用している全インスタンスが対象。内部ユーザーが意図せず管理者権限を取得でき、コード・シークレットの漏洩リスクが高い。 |
| **CVE‑2026‑105105** | 9.8 | **NASA‑AMMOS AIT‑Core の ZeroMQ バス認証欠如**（ait‑server のコマンドブローカー） | 宇宙ミッションのテレメトリ・コマンド系統に直接介入でき、偽コマンド注入や機密データ抽出が可能。ミッション・クリティカルシステムでの使用は即時対策が必須。 |

> **選定理由**  
> - **スコアが最高（10.0）または 9.5 以上**で、**リモートから直接権限取得やコード実行**が可能。  
> - **インフラ基盤（AWS、GitLab、NASA）や広く使用されるブラウザ・ランタイム**に影響し、組織全体のリスクが拡大する点が共通。  

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンの即時更新
| 製品 / ライブラリ | 修正済みバージョン (最低) | 更新手順のポイント |
|-------------------|--------------------------|---------------------|
| **Loom for AWS** | `>= 1.6.1` | `pip install --upgrade loom-aws` または公式 Docker イメージの再ビルド。 |
| **Google Chrome / Chromium** | `>= 154.0.8037.97` | エンタープライズ管理ツール（Chrome Policy）で自動ロールアウト。 |
| **Seroval** | `>= 1.6.3` | `npm install seroval@^1.6.3` → `package-lock.json` の再生成。 |
| **GitLab AI Gateway** | `>= 19.4.1` (全 AI Gateway バージョン) | GitLab Omnibus の `gitlab-ctl reconfigure` 後、`gitlab-ctl restart`。 |
| **NASA‑AMMOS AIT‑Core** | `>= 3.1.2` | `pip install --upgrade ait-core`、ZeroMQ の認証設定 (`auth` オプション) を再確認。 |
| **Tinypool (Node.js)** | `>= 2.1.2` | `npm install tinypool@^2.1.2`、`Object.prototype` の汚染対策をコードレビューで実装。 |
| **ConvertX** | `>= 0.19.0` | `npm install convertx@^0.19.0`、レシピファイルのサニタイズを追加。 |
| **RouterOS** (MikroTik) | `>= 7.12` (公式パッチ) | Web 管理インタフェースを一時的に無効化し、SSH 経由でアップグレード。 |
| **Microsoft Exchange Server** | `>= 2026‑CU5` (セキュリティ更新) | Exchange 管理シェルで `Get-ExchangeServer | Install-Update` 実行。 |
| **fsspec** | `>= 2026.6.1` | `pip install --upgrade fsspec`、Jinja2 のサンドボックス化設定 (`Environment(autoescape=True)`) を適用。 |

### 3.2 共通的な防御策
- **ネットワーク分離**  
  - ZeroMQ バスや内部 API（AIT‑Core、Tinypool 等）は **内部 VLAN／ファイアウォールで外部からの直接アクセスを遮断**。  
- **最小権限の原則**  
  - IAM ロールや GitLab の API キーは **必要最小限の権限に絞り、定期的にローテーション**。  
- **Web アプリケーションファイアウォール (WAF)**  
  - Chrome の WebGL 攻撃や GitLab AI Gateway の認証バイパスに対し、**不審なリクエストパターン（長大な POST、特定ヘッダー）をブロック**。  
- **コード署名・サプライチェーン検証**  
  - Node.js パッケージは **npm の `npm audit` と `npm ci --production`**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-103956

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-10-02T19:16:39.750 |

Missing authentication for critical function in the authentication dependency in Loom for AWS before 1.6.1 allowed remote actors to obtain super-admin authority over the agent control plane, including registering tool servers, reading stored integration credentials, and rewriting the IAM role policies attached to managed agent roles, via any request to the application API in a deployment where no identity provider is configured.



To remediate this issue, users should upgrade to version 1.6.1 or later.

### CVE-2026-90970

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-02T15:17:12.550 |

GitLab has remediated a vulnerability in the GitLab AI Gateway component affecting all versions of the AI Gateway from 18.1.6 before 19.2.4, 19.3 before 19.3.2, and 19.4 before 19.4.1 that, under certain conditions, could have allowed an authenticated user with Duo Agent Platform access to escape the prompt template sandbox via a specially crafted flow configuration, resulting in arbitrary command execution on the AI Gateway.

### CVE-2026-105105

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-03T12:16:57.183 |

CWE-306: Missing Authentication for Critical Function in the ait.core.server telemetry and command broker (ait-server) in NASA-AMMOS AIT-Core through 3.1.1 allows an unauthenticated remote attacker with network access to the ZeroMQ message bus to inject spacecraft command data, exfiltrate command and telemetry traffic, inject forged telemetry, or disrupt the command and telemetry bus. The ait-server ZeroMQ broker binds its XSUB and XPUB sockets to all network interfaces by default without authentication or transport security. An attacker able to reach TCP port 5559 can publish messages onto internal topics, including the __commands__ command topic. With the shipped default configuration, command messages are forwarded through command_stream and emitted on the command-uplink UDP path. An attacker able to reach TCP port 5560 can subscribe to command and telemetry traffic on the ground bus. AIT-Core 3.1.2 changes the default ZeroMQ bind addresses to loopback.

### CVE-2026-104846

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-02T16:16:47.230 |

Seroval facilitates JS value stringification, including complex structures beyond JSON.stringify capabilities. From 0.12.0 until 1.6.2, fromJSON deserialization of a fulfilled Promise control node can pass a plugin-produced callable-bearing thenable to a native Promise resolver. ECMAScript thenable assimilation then invokes the callable unexpectedly, allowing attacker-controlled JSON to trigger code in applications using plugin-capable Seroval releases. This path bypasses the Promise resolver type-confusion remediation in version 1.5.3 for CVE-2026-59940 because the unexpected invocation occurs through native Promise settlement after the referenced value is deserialized. This issue is fixed in version 1.6.2.

### CVE-2026-103628

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-02T16:16:43.937 |

Out of bounds write in WebGL in Google Chrome prior to 154.0.8037.97 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-104849

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1321` |
| Published | 2026-10-02T17:17:03.623 |

Tinypool is a minimal Node.js worker thread pool implementation. Prior to 2.1.2, Tinypool reads filename from a caller-supplied options object in pool.run(task, options) without requiring an own property, so a polluted Object.prototype.filename can replace the intended worker module. Applications are affected only when they pass their own second-argument options object to pool.run(); calls without that argument use the trusted default options object. An attacker who can first pollute the prototype can cause the worker pool to load attacker-selected JavaScript and can read or modify task data with the host process's privileges. This issue is fixed in version 2.1.2.

### CVE-2026-104848

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-02T17:17:03.473 |

Tinypool is a minimal Node.js worker thread pool implementation. Prior to 2.1.1, Tinypool constructs ThreadPool.options from a normal options object and reads the execArgv and env worker options in dist/index.js, allowing values inherited from a polluted Object.prototype to be copied into own properties and passed to worker_threads.Worker. An attacker who can first pollute either property can cause each newly spawned worker to load attacker-selected JavaScript through command-line preload arguments or NODE_OPTIONS, resulting in code execution with the host process's privileges and possible access to CI secrets, signing material, or build artifacts. This issue is fixed in version 2.1.1.

### CVE-2026-105080

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-03T01:17:23.650 |

In ConvertX before 0.19.0, converters/calibre.ts does not block recipe files, and instead passes them to the ebook-convert program from Calibre. This affects executable code in a .recipe or .downloaded_recipe file.

### CVE-2026-75937

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-02T21:16:56.337 |

A specially crafted HTTP POST request to the web administration interface allows an unauthenticated attacker to execute arbitrary operating system commands with root privileges on the affected device. Disable the web server when not configuring the device.

### CVE-2026-84411

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-02T23:16:58.417 |

The web management service in affected RouterOS versions contains an integer underflow in its HTTP request body handling that is reachable before authentication. This can be leveraged by an unauthenticated network attacker to achieve arbitrary code execution as root, or to cause a denial of service, using a single crafted request.

### CVE-2026-95102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-02T22:16:56.607 |

WebSocket endpoints lack proper authentication mechanisms, enabling attackers to impersonate charging stations. As a result, attackers can exploit this weakness to gain unauthorized access to sensitive data or perform unauthorized actions. Given that no authentication is required, this can lead to privilege escalation and potentially compromise the security of the entire system.

### CVE-2026-82042

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-02T21:16:56.643 |

UTMStack before 11.2.16 contains an authentication bypass vulnerability that allows remote attackers to gain full administrative API access by presenting a valid Utm-Internal-Key header matching the INTERNAL_KEY environment variable value, which the InternalApiKeyFilter accepts for any endpoint without path restriction, constant-time comparison, rate limiting, or audit logging. Attackers who obtain the key value can authenticate without a user account or JWT to create accounts, manage users, exfiltrate data, and modify security rules.

### CVE-2026-104019

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-02T20:17:00.607 |

OS command injection in the Studio Space startup validation script in Amazon SageMaker Distribution 2.x before 2.14.12, 3.x before 3.9.12, 4.0.x before 4.0.11, 4.1.x before 4.1.11, 4.2.x before 4.2.8, 4.3.x before 4.3.5, and 4.4.x before 4.4.3, as used by Amazon SageMaker Unified Studio, might allow an authenticated remote user with project contributor permissions to execute arbitrary commands in another project member's Studio Space and obtain that member's temporary execution role credentials via a crafted connection resource property that is interpolated into a shell invocation without neutralization.



To remediate this issue, users should upgrade to version 2.14.12, 3.9.12, 4.0.11, 4.1.11, 4.2.8, 4.3.5, or 4.4.3, as applicable to the minor line in use. Users on minor lines that have reached end of support must move to a supported minor line, because no patched version will be released for those lines. In Amazon SageMaker Unified Studio, Studio Spaces adopt the latest patch of their minor line on restart once the patched images are deployed, so no version selection is required.

### CVE-2023-54405

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-02T19:16:38.897 |

H3C CVM, the Cloud Virtualization Management component of the H3C CAS cloud platform, contains an unauthenticated arbitrary file upload vulnerability in the /cas/fileUpload/upload endpoint that allows remote attackers to write arbitrary files by manipulating the caller-supplied token parameter without restricting path traversal or file type. Attackers can exploit the path traversal in the token parameter to upload a malicious JSP file into a web-accessible directory and then request it to achieve remote code execution as the web-server user. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-14.

### CVE-2026-71885

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-287;CWE-295` |
| Published | 2026-10-03T09:17:04.730 |

In Bouncy Castle for Java before 1.86, the Messaging Layer Security (MLS, RFC 9420) implementation did not bind an X.509 credential to a LeafNode's signature_key. LeafNode.verify() checked a leaf's signature against the signature_key carried in the leaf itself, while the credential's X.509 certificate chain was stored but never parsed or validated, so the end-entity certificate's public key was never required to match signature_key as RFC 9420 sec. 5.3 requires. A party could therefore present another party's certificate as its credential while signing the leaf, and the enclosing KeyPackage, with an unrelated key, and be accepted under that other party's identity through KeyPackage.verify() and the Group leaf-validation path. In a deployment that admits external commits without an independent credential-admission check, an unauthenticated attacker could be admitted under a victim's X.509 identity, evict the victim (resynchronization compares whole credentials rather than signing keys), derive the current epoch, decrypt subsequent group messages, and send messages accepted as the victim. TreeKEM.LeafNode now requires the end-entity certificate's subject public key, in the cipher suite's signature encoding, to equal signature_key for an X.509 credential and rejects the leaf otherwise, including an empty chain or a certificate whose key type does not match the cipher suite; certificate-chain and identity validation to a trust anchor remain the application's responsibility per RFC 9420 sec. 5.3.1. Deployments using only basic credentials are unaffected.

### CVE-2026-92084

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-03T08:16:26.990 |

The The Beaver Builder Page Builder – Drag and Drop Website Builder plugin for WordPress is vulnerable to arbitrary shortcode execution in all versions up to, and including, 2.11.0.5. This is due to the software allowing users to execute an action that does not properly validate a value before running do_shortcode. This makes it possible for unauthenticated attackers to execute arbitrary shortcodes. Exploitation requires the target site to have a Beaver Builder page containing the Sidebar module populated with a widget that displays attacker-controllable text, such as the core Recent Comments widget, with comment moderation disabled or the attacker's comment approved.

### CVE-2026-87115

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-03T07:16:48.347 |

The VikAppointments Services Booking Calendar plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the extract function in all versions up to, and including, 1.2.21. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). Exploitation requires at least one File-type custom field to be published on the confirmation page shortcode, as this field is not created by default during plugin installation.

### CVE-2026-103648

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-02T16:16:44.370 |

Path traversal in image-downloader 4.3.0 allows an attacker who can control the download URL to cause downloaded response data to be written outside the configured destination directory.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-105115

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-03T14:16:38.110 |

OpenAM before 16.1.3 contains an unauthenticated arbitrary class instantiation vulnerability in the legacy JAX-RPC SOAP interface that allows remote attackers to load classes without authentication. Attackers can send SOAP requests to /jaxrpc/* with an unverified session identifier and a chosen class name, crashing the server, probing the classpath, or potentially reaching code execution via gadget chains.

### CVE-2026-18443

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-03T07:16:47.917 |

The Smart Manager – Advanced WooCommerce Bulk Edit & Inventory Management plugin for WordPress is vulnerable to generic SQL Injection via the 'access_privileges' parameter in all versions up to, and including, 8.97.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for authenticated attackers, with subscriber-level access and above, to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This exploit is only possible on installations where an administrator has saved a role-based deny-list Access Privilege configuration that does not explicitly block the internal 'access-privilege' module, as this condition allows the authorization filter to implicitly permit Subscriber-level users to invoke the vulnerable handler.

### CVE-2026-97644

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-03T04:18:04.917 |

The Groundhogg — CRM, Newsletters, and Marketing Automation plugin for WordPress is vulnerable to Privilege Escalation via Contact Identity Rebinding in all versions up to, and including, 4.9 The vulnerability exists because the `create_contact` function in the v3 REST endpoint (`POST /gh/v3/contacts`) is gated solely by the `add_contacts` capability and forwards the full request payload — including the security-bearing `user_id` column — into the upsert path of `Contacts_DB::add()`, which bypasses the ownership guard that `Contacts_DB::update()` enforces, allowing an attacker to rebind any existing contact record to an arbitrary WordPress user ID. This makes it possible for authenticated attackers with Sales Representative-level access and above to upsert their own contact row to point to an Administrator's user ID, then invoke the v4 email-test endpoint (`POST /gh/v4/emails/test`) — also accessible to the Sales Representative role via the `send_emails` capability — to generate an `{auto_login_url}` one-time permissions key bound to the rebound contact, and consume that link to call `wp_set_auth_cookie()` and gain a fully authenticated session as the WordPress Administrator.

### CVE-2026-92536

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-03T04:18:01.853 |

The Paid Membership Plugin, Ecommerce, User Registration Form, Login Form, User Profile & Restrict Content – ProfilePress plugin for WordPress is vulnerable to Sensitive Information Exposure in all versions up to, and including, 4.17.4 via the get_user_profile_structure. This makes it possible for authenticated attackers, with subscriber-level access and above, to extract other users' email addresses, login names, and registration dates via the Member Directory's per-row user rebinding when attacker-controlled base64 payloads in the [pp-custom-html] shortcode invoke [profile-email], [profile-username], and [profile-date-registered]. When the WordPress users_can_register option is enabled, unauthenticated attackers can also exploit this vulnerability by supplying the split shortcode fragments through the plugin's own registration handler, which processes the reg_nickname and reg_bio fields without a nonce requirement.

### CVE-2026-39718

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-02T20:17:02.420 |

Cross-Site Request Forgery (CSRF) vulnerability in Webriti Wallstreet wallstreet allows Cross Site Request Forgery.This issue affects Wallstreet: from n/a through 2.8.6.

### CVE-2026-96940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-02T19:16:43.023 |

Weak authorization in Microsoft Exchange Server allows an authenticated attacker to elevate privileges over a network.

### CVE-2026-104851

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-10-02T17:17:03.763 |

fsspec is a specification and Python implementation framework for filesystem interfaces. From 0.9.0 until 2026.6.0, fsspec.implementations.reference.ReferenceFileSystem evaluates fields from Kerchunk reference JSON documents through unrestricted jinja2.Template(...).render(...) calls in _process_references1._render_jinja, _process_templates, and _process_gen in fsspec/implementations/reference.py. A document supplied inline or fetched from an attacker-controlled URL can provide template expressions that execute Python code when the reference filesystem is opened, including through consumers such as xarray, before referenced data is read. The _process_gen path is reached whenever a document includes a gen array, while the other paths depend on template-related options and values. This issue is fixed in version 2026.6.0.

### CVE-2026-103625

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-02T16:16:43.610 |

Type confusion in V8 in Google Chrome prior to 154.0.8037.97 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-103622

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-02T16:16:43.290 |

Use after free in SVG in Google Chrome prior to 154.0.8037.97 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-71890

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-03T09:17:05.607 |

In Bouncy Castle for Java before 1.86, validation of an MLS (RFC 9420) external commit's proposal list, org.bouncycastle.mls.protocol.Group.validateExternalCachedProposals, counted the proposals by type and bounded the removed leaf index but never established that the removed leaf had anything to do with the joiner. RFC 9420 sec. 12.2 permits at most one Remove proposal in an external commit, with which the joiner removes an old version of themselves, and requires that where one is present the LeafNode in the commit's path field meet the criteria it would have to meet in an Update for the removed leaf, in particular that its credential present identifiers acceptable for the removed participant. The ordinary proposal-list validator's self-remove rule is deliberately not applied on this path, because a resync commit legitimately removes a leaf the joiner owns, but nothing was put in its place. Any party holding the group's public GroupInfo, which is precisely what an external joiner is meant to be given, could therefore commit a Remove naming any member's LeafIndex and have every member apply it, evicting that member and taking over their slot in the ratchet tree. The credential check that should have prevented this existed only in the gRPC interop harness and so protected no other caller of the public Group.externalJoin and Group.handle API. An external commit carrying a Remove is now accepted only when the removed leaf's credential is identical to the one in the joiner's own new leaf, on both the sending and the receiving side.

### CVE-2026-71889

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-03T09:17:05.437 |

In Bouncy Castle for Java before 1.86, neither copy of PKIXCertPathReviewer - org.bouncycastle.pkix.jcajce.PKIXCertPathReviewer nor the legacy org.bouncycastle.x509.PKIXCertPathReviewer - applied X.509 name constraints to the end-entity certificate. checkNameConstraints walked the path with a loop bound of index greater than zero, which is the bound the CA-only steps require, but index zero is the target certificate under the standard CertPath ordering, so the permitted and excluded subtree checks of RFC 5280 sec. 6.1.3 (b) and (c) never ran against the leaf's subject DN or its subjectAltName. A chain whose leaf violated a NameConstraints extension imposed by its own issuing CA therefore reported isValidCertPath() true with an empty error list, while CertPathValidator.getInstance("PKIX", "BC"), which shares no code with the reviewer, rejected the identical chain against the identical trust anchor. An application using the reviewer to make the trust decision rather than for diagnostics alongside a real validation accepted a certificate the constrained CA was never authorised to issue. Both copies now check every certificate in the path including the target, waive the sec. 4.2.1.10 self-issued exemption for the final certificate as sec. 6.1.3 requires, and skip the sec. 6.1.4 (g) constraint-accumulation step for the target. This issue also affects Bouncy Castle for Java LTS before 2.73.13, which carries only the org.bouncycastle.pkix.jcajce copy of the reviewer. It also affects Bouncy Castle for Java FIPS (BC-FJA) before bcpkix-fips 1.0.13 (1.0.X series), 2.0.13 (2.0.X series) and 2.1.13 (2.1.X series).

### CVE-2026-71888

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-354` |
| Published | 2026-10-03T09:17:05.250 |

In Bouncy Castle for Java before 1.86, the streaming CMS AuthenticatedData parser accepted a message whose digestAlgorithm and authAttrs fields disagreed about whether authenticated attributes were present. RFC 5652 sec. 9.1 pairs the two, requiring that authAttrs be present whenever digestAlgorithm is, and sec. 9.2 makes the MAC cover the DER encoding of authAttrs when they are present and the eContent OCTET STRING directly when they are not. CMSAuthenticatedDataParser has to choose between those two in its constructor, before it can reach authAttrs, which comes later in the SEQUENCE, so it chose on digestAlgorithm alone: for a message with digestAlgorithm absent but authAttrs present it verified the content MAC and then returned the attributes through getAuthAttrs() as though they had been authenticated, when the MAC had never covered them. An attacker able to modify a message in transit could insert an authenticated attribute, such as an RFC 2634 ESSSecurityLabel, into an otherwise valid message while holding neither the key-encryption key nor the content-MAC key, and an application taking an authorization, routing or labelling decision from those attributes would act on attacker-chosen values. The content itself remained MAC-bound. asn1.cms.AuthenticatedData now rejects the mismatched pairing when parsing and CMSAuthenticatedDataParser cross-checks the two fields once authAttrs is read. This is a variant of CVE-2026-59642, which bound the content to the MAC for messages that legitimately carry authAttrs, and which does not address this case. This issue also affects Bouncy Castle for Java LTS before 2.73.13, and Bouncy Castle for Java FIPS (BC-FJA) before bcpkix-fips 1.0.13 (1.0.X series), 2.0.13 (2.0.X series) and 2.1.13 (2.1.X series), and bcutil-fips 2.0.8 (2.0.X series) and 2.1.8 (2.1.X series).

### CVE-2026-104433

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-03T00:16:35.253 |

Mooncake transfer engine before 0.3.12 contains an out-of-bounds read vulnerability in the readString function of include/common.h that allows unauthenticated attackers to crash the service by sending a zero-length handshake frame. Attackers can connect to the handshake port listening on all interfaces and send an eight-byte frame to terminate the hosting process, such as an SGLang inference server.

### CVE-2026-97363

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-02T22:16:56.910 |

The WebSocket Application Programming Interface lacks restrictions on the number of authentication requests. This absence of rate limiting may allow an attacker to conduct denial-of-service attacks or brute-force attacks to gain unauthorized access.

### CVE-2026-82039

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T20:17:04.430 |

UTMStack before 11.2.16 contains a SQL injection vulnerability in UtmAssetGroupService.searchQueryBuilder() that allows authenticated attackers to inject arbitrary SQL by supplying malicious assetType and groupName values that are inserted unsanitized into a native PostgreSQL query via String.format(). Attackers can exploit the GET /api/utm-asset-groups/searchGroupsByFilter endpoint to execute arbitrary SQL with DBA privileges, enabling full database read, data modification, and potential filesystem access.

### CVE-2020-37278

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T19:16:38.703 |

Weaver e-Bridge contains an unauthenticated arbitrary file read vulnerability that allows remote attackers to access arbitrary files on the host system by supplying a file: URL to the downloadUrl parameter of the saveYZJFile endpoint. Attackers can exploit this flaw to read sensitive files such as /etc/passwd or configuration and credential files, and the same endpoint's support for http(s) URLs also enables server-side request forgery against internal network resources. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-17.

### CVE-2014-125130

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-02T19:16:37.440 |

CodeArt Google MP3 Audio Player plugin (google-mp3-audio-player) for WordPress through 1.0.11 contains an unauthenticated arbitrary file read vulnerability that allows remote attackers to retrieve sensitive files by supplying a path-traversal payload in the file parameter of direct_download.php. Attackers can request paths ../../wp-config.php without authentication to download configuration files containing database credentials and secret keys, leading to full site compromise. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-19.

### CVE-2026-94592

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-02T22:16:56.187 |

Armatura One's database initialization routine assigns a fixed, vendor-defined password to the database superuser account at creation time, rather than generating a unique password per installation. An individual with access to the server operating system and knowledge of this value can authenticate as the database superuser on a deployment where it has not been changed.

### CVE-2026-94591

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-02T22:16:56.023 |

Armatura One stores database and message-broker credentials in an install configuration file, encrypting them with AES-128-CBC when this protection is enabled. The encryption key and initialization vector are fixed values embedded in the software itself and are identical across every installation. An attacker with a copy of the installation package can recover this key and initialization vector, and can then decrypt the stored credentials of any specific installation to which the attacker separately obtains the encrypted configuration file.

### CVE-2026-94593

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-02T22:16:56.327 |

Armatura One's backup and restore routine records the full database connection command, including the superuser password, in plain text in a log file on the host. Credentials disclosed by this finding can be used to access the database when access to the server operating system is available.

### CVE-2026-104854

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-732` |
| Published | 2026-10-02T17:17:04.070 |

Nx is a monorepo solution for TypeScript and polyglot codebases. From 14.6.0 until 22.7.9 and 23.1.2, Nx creates Unix domain sockets for its daemon and isolated plugin workers in shared temporary locations without owner-only directory and socket permissions. Another unprivileged local account on a shared build server, developer host, or multi-user container can discover and connect to a running socket because the transport performs no authentication and relies on filesystem containment. The daemon's PROCESS_IN_BACKGROUND request accepts a module path and invokes its default export, allowing a caller that controls a file to execute code as the account running Nx; other handlers can expose workspace file contents, project graphs, and task hashes. Disabling the daemon alone does not remove the vulnerable plugin-worker sockets, while single-user machines without another local account are not exposed. This issue is fixed in versions 22.7.9 and 23.1.2.

### CVE-2026-104847

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T16:16:47.410 |

ProseMirror's view component renders and manages the editable browser interface for ProseMirror documents. Prior to 1.42.3, prosemirror-view paste handling accepts attacker-provided HTML whose clipboard slice context contains attributes that are not passed through schema attribute validation. When a user pastes the crafted HTML into an editor, the unvalidated context attributes can construct content that executes attacker-controlled JavaScript in the browser window containing the editor. This issue is fixed in version 1.42.3.

### CVE-2026-103958

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T19:16:40.040 |

Server-side request forgery in the tool server and remote agent connection handling in Loom for AWS before 1.7.0 might allow an authenticated remote user to obtain the credentials of the application's own container role and to read responses from arbitrary internal network locations, via a crafted connection address supplied when registering, updating or testing a tool server or remote agent.



To remediate this issue, users should upgrade to version 1.7.0 or later.

### CVE-2026-94483

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-02T16:16:51.473 |

Next.js is a React framework for building full-stack web applications. From 16.0.0 until 16.3.8, Image Optimization can follow attacker-controlled DNS resolution for a remote URL that matches images.remotePatterns, allowing the optimized image fetch to reach private IP addresses after the URL passes the allow-list check. Applications without images.remotePatterns are not affected. Administrators unable to upgrade should audit allow-listed hosts and avoid entries whose DNS records are not trusted. This issue is fixed in version 16.3.8.

### CVE-2026-85515

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-345;CWE-354` |
| Published | 2026-10-03T09:17:06.073 |

In Bouncy Castle for Java before 1.86, a truncated OpenPGP encrypted message was accepted with no error reported, and on the SEIPD version 1 path with no integrity check performed at all. RFC 9580 sec. 13.7 permits an implementation to release the cleartext of the fully authenticated chunks when streaming but requires it to indicate a clear error as soon as the truncation is detected, and to report suspect integrity when it discovers malleable ciphertext. The truncation was detected and then discarded: when a message is truncated but the length field of the enclosing packet is left unchanged, BCPGInputStream.PartialInputStream raises an EOFException for the missing ciphertext, and BCPGInputStream.nextPacketTag() reports an EOFException as a clean end of message, so the packet stream above it stopped as though no packets remained. On the AEAD path (SEIPD version 2 and the version 5 AEAD packet), when the literal data packet ended on an AEAD chunk boundary and the consumer read in increments smaller than one chunk, the look-ahead for the packet after the literal triggered the truncated chunk read, so BcAEADUtil and JceAEADUtil never reached the trailing message tag of sec. 5.13.2 that authenticates the total plaintext length; the caller received the plaintext of the fully authenticated chunks, every packet following the literal was silently dropped, and no exception was raised, so a signed and encrypted message read back as a well-formed unsigned one. Every byte released on that path remained individually authenticated, making this a missing truncation error rather than a forgery, and it is a residual of CVE-2026-12817, which closed the same outcome for an attacker who corrects the outer packet length. On the SEIPD version 1 path the consequence was more serious: IntegrityProtectedInputStream verifies the modification detection code from close(), and reached close() only by closing itself when a read of it returned -1, which a truncated message never produces, so PGPEncryptedData.verify() never ran and the recipient was handed CFB-decrypted plaintext on which no integrity check of any kind had been performed. Measured on a message truncated into that shape, 136 distinct single-byte modifications of the ciphertext produced accepted, altered plaintext with no exception raised. Reachability is a property of the message rather than of attacker-supplied input: the AEAD shape held for 3 of 131 consecutive payload lengths measured, and the SEIPD version 1 shape for one payload length in sixteen, at a truncation offset that did not move with the payload length. The low-level API is unaffected, a caller that invokes PGPEncryptedData.verify() directly getting the check regardless, as are consumers reading in increments of a whole AEAD chunk or more. The AEAD decryption streams now re-throw such an EOFException as a plain IOException, which nextPacketTag() does not launder; OpenPGPMessageInputStream.close() now closes its layer's integrity-protected stream itself rather than relying on that stream having seen the end of its data; and IntegrityProtectedInputStream.close() was made idempotent, as java.io.Closeable requires, which that depends on, since the stream is genuinely closed twice on the ordinary path and PGPEncryptedData.verify() consumes the digest state behind it and cannot be run a second time. This issue also affects Bouncy Castle for Java LTS before 2.73.13, on the AEAD route only, as that edition does not ship the high-level OpenPGP API the SEIPDv1 route runs through. It also affects Bouncy Castle for Java FIPS (BC-FJA) before bcpg-fips 1.0.14 (1.0.X series), 2.0.14.1 (2.0.X series) and 2.1.14 (2.1.X series), on the AEAD route only, as those editions do not ship the high-level OpenPGP API.

### CVE-2026-71887

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-345;CWE-347` |
| Published | 2026-10-03T09:17:05.067 |

In Bouncy Castle for Java before 1.86, the high-level OpenPGP API accepted a data signature made by a signing subkey whose Subkey Binding signature carried no embedded Primary Key Binding (cross-certification) signature, in the case where that binding omits a Key Flags subpacket. RFC 9580 sec. 5.2.1.8 and sec. 10.1.3 require the embedded Primary Key Binding signature on any subkey that can issue signatures; it is the subkey's own statement that it belongs to the primary key it is bound under. OpenPGPCertificate resolved the subkey's key flags two different ways. isSigningKey() goes through getKeyFlags() and getApplyingSubpacket(), which falls back to the primary key's direct-key or primary User ID self-signature when the binding signature omits the subpacket, so the subkey inherited the primary's SIGN_DATA and counted as signing-capable; verifyEmbeddedPrimaryKeyBinding(), which enforces the requirement, reads the binding signature's own hashed subpackets, found no SIGN_DATA there, and returned early as a non-signing key without ever demanding the back signature. The same subkey was therefore signing-capable - so its signatures were attributed to the certificate and OpenPGPSignature.OpenPGPDocumentSignature.isValid() returned true - while being exempt from cross-certification, where GnuPG refuses the identical certificate and message. An attacker needs only the victim's public signing subkey, which is public material: they bind it to their own primary key with a Subkey Binding signature they are able to make, carrying no Key Flags and no embedded Primary Key Binding signature, which they cannot make without the subkey's private key, and a relying party verifying one of the victim's genuinely signed messages against that certificate is told the signature is valid and given the attacker's certificate as its issuer. Because a certificate's User IDs are self-asserted, a verifier that pins on the subkey's fingerprint or key ID while taking the identity from the enclosing certificate reports a real signature under an attacker-chosen identity. This is misattribution of a genuine signature rather than forgery of a new one: no private key is recovered, and the signature must be one the grafted subkey actually made. The low-level PGPSignature / PGPPublicKeyRing API performs no binding checks by design and is unaffected. Key Flags are a statement about the key the carrying signature refers to (RFC 9580 sec. 5.2.3.29), so a subkey no longer inherits them from the certificate-wide signatures of the primary key: a Subkey Binding signature that omits the subpacket now leaves the subkey with no capabilities rather than the primary's, which makes the flags the cross-certification check consults the same flags every other decision consults. Preferences and the other subpackets a direct-key signature carries are inherited as before, and the primary key itself, whose flags legitimately come from its own direct-key or User ID self-signature, is unaffected.

### CVE-2026-71886

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-10-03T09:17:04.897 |

In Bouncy Castle for Java before 1.86, the high-level OpenPGP certificate API accepted a third-party certification or trust delegation from any component key of the issuing certificate, without requiring that component to have been granted the authority to certify. OpenPGPCertificate.getCertificationBy() and getDelegationBy() resolve a third-party signature by matching its issuer key identifier against every key of the third-party certificate, then verify the issuing component's binding chain and the signature itself; nothing checked that the issuing component carried the RFC 9580 sec. 5.2.3.29 certification key flag (CERTIFY_OTHER) when the signature was created. A subkey bound only with SIGN_DATA - the online signing subkey of exactly the offline-primary arrangement those key flags exist to express - could therefore issue a positive User ID certification over an attacker-controlled identity, or a full-trust depth-one direct-key delegation of introducer trust, and the API returned it as a valid signature chain attributed to the third-party certificate. An application treating getCertificationBy(...).isValid() or getDelegationBy(...) as an identity or trusted-introducer decision would attribute the attacker's assertion to the offline primary key. The same held for a legacy RSA subkey bound only for encryption, whose algorithm is nonetheless able to sign. This does not forge the primary key's signature or recover any private key; it promotes an already-compromised restricted subkey to the primary key's identity-issuing authority, defeating the containment the key-flag separation provides. A third-party certification or delegation is now attributed to the issuing certificate only when the component key that made it is the primary key, or is a subkey holding CERTIFY_OTHER when the signature was created, so certification-capable subkeys continue to be accepted; primary keys are accepted whatever their key flags say, since a primary key is certification-capable by construction and certificates carrying no key flags subpacket at all are common. Third-party revocations are deliberately outside the rule, since declining to honour one would keep trust alive rather than withdraw it.

### CVE-2026-71883

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-03T09:17:04.570 |

In Bouncy Castle for Java LTS before 2.73.13, the one-shot native packet ciphers for AES-CBC, CCM, CFB, CTR, GCM and GCM-SIV released the caller's key, IV and additional authenticated data arrays with JNI's ReleaseByteArrayElements in mode 0, which commits the native copy back into the Java array. Those arrays are read-only to the native code, and on a JVM that returns a copy rather than a pin the copy still holds the input bytes as they were read. The output buffer is taken through a separate critical region and committed first, so where an application passed the same Java array as both an input and the destination - encrypting in place over KeyParameter.getKey(), for example - the later mode-0 release of the key wrote the unchanged key bytes over the ciphertext that had just been produced. The call still returned the correct output length, so an application encrypting in place over its own key array was handed the raw AES key where it expected ciphertext, with nothing in the API to indicate it, and would transmit or store the key in place of the message. The read-only input arrays are now released with JNI_ABORT, freeing the native copy without copying it back, and mode 0 is reserved for arrays the native code wrote. The pure-Java packet ciphers and the streaming native modes are not affected. Bouncy Castle for Java (bcprov) is not affected, as it ships no native implementations.

### CVE-2026-104476

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-03T00:16:35.747 |

Backdrop CMS before 1.35.1 contains an information disclosure vulnerability that allows unauthenticated attackers to retrieve configuration export archives left on the server after transfer. Attackers can download compressed archives generated by users with configuration export permission to obtain the full site configuration, including sensitive settings.

### CVE-2026-103957

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201;CWE-918` |
| Published | 2026-10-02T19:16:39.893 |

Server-side request forgery in the OAuth2 discovery handling in Loom for AWS before 1.7.0 might allow an authenticated remote user to obtain the access token of another user of the deployment and to cause the application to issue requests to arbitrary internal network locations, via a crafted discovery document address supplied when registering a tool server or remote agent configured for delegated authentication.



To remediate this issue, users should upgrade to version 1.7.0 or later.

### CVE-2026-94505

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-03T07:16:49.033 |

The Nelio Content – Editorial Calendar & Social Media Auto-Posting plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 4.5.0 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with contributor-level access and above, to permanently delete any reusable social message (nc_reusable_social post), including those authored by administrators or other privileged users.

### CVE-2026-101923

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-03T06:16:39.603 |

The Photo Reviews for WooCommerce plugin for WordPress is vulnerable to Arbitrary Content Deletion in versions up to, and including, 1.2.30. This is due to the plugin storing attacker-controlled post IDs from the wcpr_image_upload_id parameter of a public review submission into the review's reviews-images comment meta without verifying that the IDs correspond to attachments owned by the submitter, combined with the delete_reviews_image() handler unconditionally calling wp_delete_post( $id, true ) on every stored ID when the review is deleted. This makes it possible for unauthenticated attackers to permanently delete arbitrary posts, pages, products, or media attachments on the site whenever an administrator subsequently deletes the attacker's review (or when WordPress's built-in wp_scheduled_delete cron empties the comment trash after 30 days).

### CVE-2026-104988

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-02T20:17:01.370 |

A flaw was found in Dogtag PKI (pki-core). The CMCAuthForEST authentication plugin fails open when an EST fullcmc enrollment request is submitted via BasicAuth without an end-user TLS client certificate. The SSL_CLIENT_CERT session attribute retains the EST subsystem's agent certificate, which causes downstream authorization checks to treat the request as agent-privileged. An authenticated EST user can exploit this to obtain CA-signed certificates with arbitrary subject names.

### CVE-2026-51907

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-02T16:16:50.320 |

In TaskingAI v0.3.0 in the QR Code Generator plugin save_base64_image function, a path traversal vulnerability allows attackers to write image files to arbitrary locations on the server filesystem by manipulating the project_id parameter.

### CVE-2026-104026

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-150` |
| Published | 2026-10-02T15:17:05.453 |

In Sapling SCM prior to v0.2.20260929-102736, control characters were allowed to be embedded in Git subtree URLs. A maliciously constructed repository, if cloned by a target, could trigger code execution on otherwise read-only actions such as sl log/blame/annotate.

### CVE-2026-105119

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-03T14:16:38.710 |

OpenAM before 16.1.3 applies its OAuth2 Provider PKCE enforcement only to authorization requests whose response_type is exactly code, so codes issued through OpenID Connect hybrid flows (code token, code id_token, code token id_token) carry no bound challenge. An attacker who intercepts such a code can redeem it for a public client's tokens with any non-empty code_verifier.

### CVE-2026-104873

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-02T20:17:01.223 |

LangGraph Python SDK is used to connect to running LangGraph API servers, manage assistants, threads and stream runs from Python applications. From 0.1.45 until 0.4.4, the langgraph-sdk resource-scoped authorization decorators @auth.on.threads, @auth.on.assistants, and @auth.on.crons ignore the actions argument and register the selected handler for every action on the resource. Because that wildcard resource handler is selected before broader fallback handlers, an authenticated user may bypass fallback action, ownership, or permission checks and read, update, or delete another user's resource. Only Python deployments using actions on the affected decorators are vulnerable, and a deployment remains protected when the selected handler independently enforces all required checks for every action it receives. This issue is fixed in version 0.4.4.

### CVE-2026-96267

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-03T07:16:49.200 |

The WP Visitor Statistics (Real Time Traffic) plugin for WordPress is vulnerable to generic SQL Injection via the 'fullRef' parameter in all versions up to, and including, 8.7 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This is a second-order SQL injection: an unauthenticated attacker submits a crafted referrer URL to the wmcTrack tracking endpoint, which persists the raw unescaped value into the wp_logVisit table, and the injection is triggered when an administrator next views the Traffic Sources dashboard.

### CVE-2026-75028

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-03T07:16:48.160 |

The WPCafe – Restaurant Menu, Online Food Ordering & Table Booking System plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 3.0.18 via the (template scope) function. This makes it possible for authenticated attackers, with contributor-level access and above, to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included.

### CVE-2026-97337

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-03T06:16:48.943 |

The Simple Membership plugin for WordPress is vulnerable to unauthorized modification of data and sensitive information disclosure in versions up to, and including, 4.8.3 via the resend-activation and email-activation endpoints. The endpoints are dispatched from SwpmInitTimeTasks::check_and_do_email_activation() on frontend init with no authentication, nonce, capability, or ownership check, and the recipient address used by SwpmRegistration::send_reg_email() is taken from an attacker-controlled $_POST['email'] parameter (overriding the member's registered address). This makes it possible for unauthenticated attackers to redirect an arbitrary pending member's activation email — and the follow-up 'registration complete' email containing the member's username and plaintext password — to an attacker-chosen address, and to then activate that member's account without their consent.

### CVE-2026-103913

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-03T06:16:41.800 |

The GeoDirectory plugin for WordPress is vulnerable to SQL Injection via the stored latitude/longitude coordinates of a listing in versions up to, and including, 2.8.186. This is due to insufficient escaping and the absence of numeric validation on coordinate values when a listing is saved, combined with the direct string interpolation of those values into a distance sub-expression in geodir_gps_query_part() that is later executed by the public wp_ajax_nopriv_geodir_widget_listings handler when a caller supplies set_post=<pending-listing-id> and sort_by=distance_asc. This makes it possible for authenticated attackers, with Subscriber-level access and above, to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-93428

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-03T03:16:37.067 |

The Ultimate Member – User Profile, Registration, Login, Member Directory, Content Restriction & Membership Plugin plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.13.1 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to view privacy-restricted member profile field values — including fields explicitly configured as owner-only, members-only, or role-restricted — by querying the publicly accessible wp_ajax_nopriv_um_get_members endpoint. The nonce required by the endpoint ('um-frontend-nonce') is emitted to all unauthenticated visitors via wp_localize_script, meaning it provides no meaningful access control and any anonymous visitor can satisfy the endpoint's authentication requirements.

### CVE-2026-104861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-10-02T18:17:02.430 |

probe-image-size gets image dimensions without downloading the entire file. Prior to 7.4.0, lib/parse_sync/svg.js and lib/parse_stream/svg.js use the searching regular expression /<[-_.:a-zA-Z0-9][^>]*>/, which repeatedly scans to the end of input when attacker-controlled data contains many less-than characters without a closing greater-than character. The synchronous parser converts and scans the full supplied buffer without an input cap, while the streaming parser reparses the complete accumulated SVG prefix for every received chunk. The probe.sync(), probe(stream), and probe(url) entry points can therefore block the Node.js event loop at full CPU, and attacker-controlled chunking can amplify the streaming cost. This issue is fixed in version 7.4.0.

### CVE-2026-67989

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-02T16:16:51.247 |

crmne/ruby_llm at commit fa6f279847d6d7027814539d9c0dfc3bbdfd2a83 contains a polynomial-time regular expression denial-of-service condition in Mistral model capability matching on Ruby 3.1.x

### CVE-2026-51916

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-02T16:16:50.763 |

TransformerOptimus SuperAGI v0.0.14 contains an incorrect access control vulnerability in delete_user_knowledge in superagi/controllers/knowledges.py. In affected source snapshots, POST /knowledges/delete/{knowledge_id} deletes the selected knowledge object without requiring authentication in the route and without verifying organization ownership of the supplied knowledge_id.

### CVE-2026-104845

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-02T16:16:47.070 |

Seroval facilitates JS value stringification, including complex structures beyond JSON.stringify capabilities. Prior to 1.6.3, deserializeTypedArray in fromJSON and fromCrossJSON trusts a deserialized source value as an ArrayBuffer and does not bound the serialized element count. An attacker can provide a small untrusted JSON object with a large length value, causing the array-like TypedArray constructor to synchronously allocate the selected number of elements and exhaust CPU or memory while starving the event loop. The offset check does not reject the crafted source because source.byteLength is undefined. DataView reaches a similar unchecked cast but throws rather than allocating, and the issue has no identified confidentiality or integrity impact. This issue is fixed in version 1.6.3.

### CVE-2026-104859

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-02T18:17:02.270 |

Nx is a monorepo solution for TypeScript and polyglot codebases. From 21.4.0 until 22.7.8 and from 23.0.0 until 23.1.1, the @nx/docker release pipeline builds docker tag, image lookup, and docker push invocations as shell command strings. The release.docker.repositoryName and registryUrl configuration values are interpolated into those strings and passed to /bin/sh -c, allowing shell syntax in untrusted Nx configuration to execute during nx release version or nx release publish. A pull request or repository configuration change can therefore execute commands with the release job's privileges and expose registry credentials or cloud tokens, and dry-run publishing does not prevent the vulnerable pre-check command from executing. This issue is fixed in versions 22.7.8 and 23.1.1.

### CVE-2026-97660

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T07:16:49.530 |

The WPC Product Options for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via wpcpo-* Array Key via Multipart Field Name in all versions up to, and including, 4.0.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable via guest checkout without authentication because the malicious payload is embedded in a multipart Content-Disposition field name beginning with 'wpcpo-', which PHP's RFC1867 parser preserves byte-for-byte and stores into order item meta.

### CVE-2026-93889

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T07:16:48.680 |

The Mail logging – WP Mail Catcher plugin for WordPress is vulnerable to Stored Cross-Site Scripting via PHPMailer 'wp_mail_failed' Error Message in all versions up to, and including, 2.1.12 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires a separately installed plugin, such as Contact Form 7, that passes unauthenticated user-controlled input into mail fields whose content PHPMailer will include in its failure error message.

### CVE-2026-97341

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:49.323 |

The Visitor Traffic Real Time Statistics plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via 'X-Real-IP' HTTP Header in all versions up to, and including, 8.16 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires no authentication, no nonce, and no capability — the wp_ajax_nopriv_ahcfree_track_visitor endpoint accepts the forged X-Real-IP header from any unauthenticated HTTP request and stores the entity-encoded payload verbatim in the database.

### CVE-2026-96650

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:48.290 |

The Strong Testimonials plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'platform_user_photo' Custom Field in all versions up to, and including, 3.3.11 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has added custom text fields named 'platform' and 'platform_user_photo' to a public testimonial submission form, as the plugin does not reserve those internal metadata keys.

### CVE-2026-96575

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:47.920 |

The Transliterator – Multilingual and Multi-script Text Conversion plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content via Predictable {rstr_keep} Placeholder in all versions up to, and including, 2.5.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload survives WordPress comment save-time sanitization because the tags and attributes used (such as a[title] and code) are permitted by the core comment kses allow-list, and the literal characters comprising the plugin's shortcode markers and placeholder tokens are not stripped.

### CVE-2026-96564

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:47.607 |

The SEOPress – AI SEO Plugin & On-site SEO plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Author Display Name in all versions up to, and including, 10.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires the 'Track Authors' custom dimension to be configured in the plugin's Google Analytics 4 or Matomo settings, and the attacker must be able to publish public singular content (e.g., via bbPress forum topics) so that the injected display name is rendered in the tracking script.

### CVE-2026-93430

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:46.727 |

The GD Rating System plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'title' and 'url' Render Args in gdrts_live_handler AJAX in all versions up to, and including, 3.7.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Although the AJAX action requires a per-item nonce, that nonce is publicly emitted in the page's &lt;script class="gdrts-rating-data"&gt; JSON block on every page rendering the rating item, making it obtainable by any unauthenticated visitor and therefore not an authentication barrier.

### CVE-2026-87091

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:44.260 |

The Welcart e-Commerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Settlement Notification Parameters in all versions up to, and including, 2.12.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The IPN endpoint accepts the 'rel' and 'option' parameters with no authentication, nonce validation, or signature verification, meaning any unauthenticated attacker can directly submit malicious payloads that are stored and later rendered in the administrator's settlement error log view.

### CVE-2026-101928

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T06:16:40.080 |

The Magic Tooltips For Contact Form 7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'author' parameter in all versions up to, and including, 1.0.34 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because the plugin's esc_html filter callback decodes HTML-entity-encoded payloads (e.g. those containing '&lt;tip&gt;') back into live HTML, meaning an entity-encoded script payload submitted as a comment author name — which bypasses sanitize_text_field — is rendered as executable markup when an administrator views wp-admin/edit-comments.php.

### CVE-2026-92977

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T04:18:04.190 |

The Real Cookie Banner: GDPR & ePrivacy Cookie Consent plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment in all versions up to, and including, 5.3.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Malicious script payloads placed in the title attribute of an anchor tag survive WordPress's comment kses filter at save time, as the payload is only promoted to executable HTML attributes when the plugin's page-wide regex strips the closing quote delimiter at render time; exploitability is therefore subject to the standard comment moderation workflow before the comment is publicly displayed.

### CVE-2026-96270

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-03T03:16:37.687 |

The Ultimate Member – User Profile, Registration, Login, Member Directory, Content Restriction & Membership Plugin plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'form_id' parameter in all versions up to, and including, 2.13.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The injected payload is stored in the registering user's 'submitted' usermeta via update_user_meta() and is only triggered when an administrator opens the affected user record in the wp-admin Users modal, which inserts the unescaped output via jQuery .html().

### CVE-2026-102626

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-02T18:16:59.433 |

An authenticated LimeSurvey Community Edition 7.4.0 user with the global Surveys: create permission can store a JavaScript-breaking value in the date_min attribute of a Date/Time question. When another user renders the affected question, LimeSurvey inserts the stored value into a single-quoted inline JavaScript literal without JavaScript-context encoding.

### CVE-2026-105113

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-667` |
| Published | 2026-10-03T14:16:37.823 |

Nezha Dashboard from 1.8.0 before 2.3.13 contains an improper locking vulnerability where a non-deferred mutex unlock leaks on a nil-map panic path. Any authenticated non-admin member can issue four notification API calls to permanently deadlock the alerting subsystem, then exhaust memory with blocking requests.

### CVE-2026-71891

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-03T09:17:05.763 |

In Bouncy Castle for Java before 1.86, BLS12_381BasicScheme.keyValidate, and so BLSPublicKeyParameters and every BasicScheme, MessageAugmentation and ProofOfPossession verify and aggregateVerify that gate on it, accepted a public key built on a foreign ECCurve that merely shares BLS12-381's field characteristic. The prime-order subgroup check trusts a point's own curve to name its cofactor, since ECPoint.satisfiesOrder returns true outright when the curve's cofactor is one, so a point on a curve with a different equation and a cofactor forged to one passed keyValidate despite not being a G1 point at all. In BC's pairing implementation such a point contributes the identity in the target group, so an aggregate signature verified against a set of public keys including it is accepted even though it contains no signature for that key and message pair, admitting a phantom signer. keyValidate now first confirms that the point's curve carries exactly the canonical G1 field, equation, order and cofactor before any subgroup check. The issue is reachable only where an application constructs an ECPoint on an explicit, non-canonical curve and accepts it as an authority-bearing key; the standard 48-byte compressed-point decoder always supplies the canonical curve and was never affected.

### CVE-2026-104478

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-03T00:16:36.083 |

Formwork before 2.3.13 contains a path traversal vulnerability in BackupController that allows authenticated panel users to read or delete arbitrary files. Attackers with backup download or delete permission can supply a base64-encoded backslash-separated traversal payload that bypasses PHP basename on Linux to access files outside the backup directory.

### CVE-2026-105050

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-180` |
| Published | 2026-10-02T23:16:58.093 |

PeaZip before 11.3.0, in a non-default configuration, is vulnerable to OS command injection via a filename in an archive because "quotation character already used in the string" is mishandled.

### CVE-2026-82045

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-02T21:16:57.080 |

UTMStack before 11.2.16 contains a JPQL injection vulnerability that allows authenticated attackers to read arbitrary entity data by exploiting UtmNetworkScanService.searchPropertyValues(), which builds a JPQL query with String.format() and executes it via em.createQuery() without parameter binding. Attackers can inject malicious JPQL through the value parameter in the GET /api/utm-network-scans/searchPropertyValues endpoint to extract sensitive data including credential tables such as jhi_user.

### CVE-2026-104991

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T20:17:01.513 |

Phproject before 1.8.7 contains a missing object-level authorization vulnerability in the REST API issue endpoints (single_get, single_comments, single_comments_post) that allows authenticated API key holders to bypass the security.restrict_access confidentiality control by never invoking the allowAccess() authorization routine. Attackers can use a valid API key to read restricted issue contents and comments, including owner and author email addresses, and post unauthorized comments to issues they should not have access to.

### CVE-2026-96613

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-02T16:16:52.490 |

The Meari IoT Cloud Platform OpenAPI Service is vulnerable to an authorization flaw that allows authenticated users to access the complete device shadow of any device by specifying its device ID. This vulnerability exposes sensitive information, such as device credentials, owner details, network data, and telemetry, without verifying any relationship between the requester and the target device.

### CVE-2026-104912

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-862` |
| Published | 2026-10-02T16:16:49.047 |

MISP contains an authorization flaw in its correlation handling during attribute searches. When a user performs an attribute search that triggers correlation lookups, the system authorized access to correlated attributes and events based on a stale distribution snapshot stored on the correlation row rather than the live event access control list.

Because the correlation row's distribution columns are a point-in-time copy that lacks a published flag, the authorization check becomes incorrect when an event is subsequently restricted (for example, its sharing group is changed or it is unpublished). As a result, an authenticated user could retrieve attributes and event details belonging to events they no longer have permission to view.

Preconditions:

- An authenticated user with at least read access to some events in the instance.

- The existence of correlations between events, at least one of which has been restricted after the correlation was created.

Impact:

- Confidentiality: exposure of attribute values and event metadata that the user is not authorized to access.

Affected versions: MISP prior to v2.5.48.

### CVE-2026-104908

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-915` |
| Published | 2026-10-02T16:16:48.580 |

MISP contains an improper input validation vulnerability in the decaying model import functionality. The import endpoint was intended to create a new decaying model belonging exclusively to the importing user's organisation, with the default flag forced to off.

However, the application stripped only the top-level id and uuid fields and pinned org_id and default on the outer array before saving the data flat. A user with decaying-model permissions could supply a nested model key carrying its own primary key, organisation identifier, and default flag, which bypassed those guards during the save operation.

Impact:

- A user with perm_decaying could overwrite an existing decaying model belonging to another organisation in place, altering its name, formula, parameters, or ownership.

- A user could create or modify a model flagged as the organisation default, affecting scoring behaviour for other users.

- A user could reassign a model's organisation to an arbitrary value.

Preconditions:

- Authenticated user with decaying-model permission (perm_decaying).

- Network access to the MISP instance.

Affected: <2.5.48.

### CVE-2026-102795

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-02T18:16:59.780 |

Improper Access Control vulnerability in Apache Traffic Server.



This issue affects Apache Traffic Server: from 9.0.0 through 9.2.14, from 10.0.0 through 10.1.3.



Users are recommended to upgrade to version 9.2.15 or 10.1.4, which fixes the issue.



This CVE supersedes CVE-2026-41920, whose record listed the affected 9.x versions as 9.0.0 through 9.1.14 and the fixed version as 9.1.15. All 9.2.x releases before 9.2.15 are affected.
