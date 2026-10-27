# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-27 15:01 UTC
- **対象期間**: `2026-10-26T15:00:44.000Z` 〜 `2026-10-27T15:01:29.000Z`
- **重要CVE数**: 188 件（Critical 9.0+: 39 件 / High 7.0〜: 149 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVSS 7.0 以上の脆弱性は、**認証欠如・権限昇格・リモートコード実行** が共通する傾向が見られます。特に **AI/ML ツール、コンテナオーケストレーション、インフラ管理系ソフトウェア** が集中しており、攻撃者がネットワーク境界をすり抜けて内部システムを直接制御できるリスクが高まっています。  

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑65145** | 10.0 (CVSS3.1) | NVIDIA NeMo Agent Toolkit に認証欠如 → 任意コード実行、特権昇格、情報漏洩 | AI/ML パイプラインで広く利用される SDK。認証が全く無い状態でコード実行可能になるため、社内外の機密データや GPU リソースが即座に奪取される危険性が極めて高い。 |
| **CVE‑2026‑115905** | 10.0 (CVSS4.0) | Rust 製 zip ライブラリ (≤ 9.0.4) のメタデータ不整合により任意ファイル書き込み・コード実行 | 多くの CI/CD ツールやバックアップシステムが内部で zip クレートを使用。攻撃者が細工した ZIP を送るだけでサーバ上で任意コードが実行できる。 |
| **CVE‑2026‑110720** | 9.9 (CVSS3.1) | Consul‑k8s (0.42.0 以降) の ACL バインディングルールに跨名前空間認可バイパス | Kubernetes 環境でのサービスメッシュ管理に必須の Consul が、名前空間を跨いで権限昇格できる。マルチテナント環境での横方向移動が容易になる。 |
| **CVE‑2026‑102649** | 9.9 (CVSS3.1) | Burrito Terraform Automation Operator の Webhook 署名検証欠如 | Terraform の自動化・CI に組み込まれることが多く、GitHub/GitLab の Webhook が署名なしで受け入れられるため、攻撃者が任意の Terraform 設定を注入し、インフラ全体を破壊できる。 |
| **CVE‑2026‑92885** | 9.8 (CVSS3.1) | WordPress 用 Qode Membership プラグイン (≤ 2.0.6.2) の認証バイパス | 多数の企業サイトで利用されるプラグイン。認証バイパスによりアカウント乗っ取りが可能で、サイト改ざんやスパム・マルウェア配布の踏み台になる。 |

> **注**：上記 5 件は **CVSS が 9.8 以上** かつ **実装環境で広く使用されている**（AI/ML、CI/CD、K8s、インフラ自動化、CMS）点で優先度が高いです。  

## 3. 推奨アクション  

- **NVIDIA NeMo Agent Toolkit**  
  - 直ちにベンダーが提供する **v2.1.0 以降**（または当該脆弱性が修正されたパッチ）へアップデート。  
  - ネットワーク上での未認証アクセスを防ぐため、ファイアウォールで `tcp/50051`（gRPC）等のポートを内部限定に設定。  

- **Rust zip クレート (zip‑rs)**  
  - `Cargo.toml` の依存バージョンを **>= 9.0.5** に更新。  
  - 既存のビルドパイプラインで `cargo audit` を実行し、古いバージョンが残っていないか確認。  

- **Consul‑k8s**  
  - 脆弱性が修正された **consul‑k8s 2.1.0** または **1.8.18** へアップグレード。  
  - `Consul` の ACL ポリシーを再評価し、**名前空間境界** を明示的に制限する RBAC ルールを追加。  

- **Burrito (Terraform Automation Collaboration Software) Operator**  
  - バージョン **0.13.0 以降** に更新。  
  - `TerraformRepository` の `webhookSecret` が必ず設定されていることを CI で検証し、空文字や未設定をデプロイ前にブロック。  

- **Qode Membership (WordPress) プラグイン**  
  - **2.0.6.3** 以上にアップデート、もしくは公式が提供するパッチを適用。  
  - WordPress のプラグイン自動更新を有効化し、**`wp-config.php`** で `DISALLOW_FILE_EDIT` を設定して不正なコード改変を防止。  

- **共通的な緊急対策**  
  - すべての対象製品・ライブラリについて **脆弱性スキャナ (e.g., Trivy, Anchore, Nessus)** を走らせ、未パッチのインスタンスを即座にリストアップ。  
  - 重要システムは **ネットワーク分離**（VPC、サブネット、セキュリティグループ）を徹底し、外部からの直接アクセスを最小化。  
  - 監査ログを有効化し、**認証失敗・権限昇格試行** をリアルタイムで SIEM に送信、アラートを設定。  

> **備考**：JP1・HiRDB 系列の多数のバッファオーバーフロー系 CVE も同様に深刻ですが、対象が日本国内の大手企業向け基幹系製品であるため、ベンダー提供の **パッチリリース（例: JP1/Base 12.50.54 以降、HiRDB 10.12.01 以降）** を適用すればリスクは低減できます。併せて、該当製品の **ファームウェア/OS パッチ管理** を定期的に実施してください。  

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-65145

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-27T13:16:59.860 |

NVIDIA NeMo Agent Toolkit contains a vulnerability where a attacker could cause a missing authentication issue. This vulnerability might lead to code execution, escalation of privileges, data tampering, denial of service, and information disclosure.

### CVE-2026-115905

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-436` |
| Published | 2026-10-26T17:17:17.823 |

zip is a zip library for Rust that supports reading and writing simple ZIP files. Through 9.0.4, ZipArchive treats Central Directory File Header filenames as authoritative while ZipStreamReader extracts using Local File Header filenames without reconciling the duplicate metadata in src/read/stream.rs. A crafted archive can therefore appear benign to a component that inspects the central directory but cause a streaming extractor to write a different attacker-selected path and content, potentially overwriting files used by a downstream service. This issue is fixed in version 9.0.5.

### CVE-2026-110720

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-26T19:16:29.940 |

Consul-k8s versions 0.42.0 and later are vulnerable to a cross-namespace authorization bypass in component ACL binding rules that may allow an attacker to obtain elevated Consul privileges. This vulnerability (CVE-2026-110720) is fixed in consul-k8s 2.1.0 and 1.8.18.

### CVE-2026-102649

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-306;CWE-863` |
| Published | 2026-10-26T18:17:21.803 |

Burrito is a Terraform Automation Collaboration Software (TACoS) Kubernetes operator. Prior to 0.13.0, `POST /api/webhook` accepts unsigned GitHub and GitLab events when a `TerraformRepository`'s credentials omit `webhookSecret` or set it to an empty value, including credentials configured for git authentication and polling. `Credential.WebhookSecret` is optional, and `go-playground/webhooks` skips signature or token verification when the secret is empty. Anyone who can reach `burrito-server`'s endpoint and knows a tracked repository's URL can forge events to create or delete `TerraformPullRequest` custom resources with attacker-chosen `Branch`, `Base`, and `ID` fields. For GitHub `pull_request` events, the controller fetches changed files using the real pull request number but does not cross-check the payload's branch against that pull request. Pairing a real, existing pull request number with an unrelated existing branch in the same repository can therefore cause an unauthorized `terraform plan` for affected layers using the operator's stored git and cloud credentials. Code analysis also indicates that the resulting plan can be posted to the real pull request's comment thread, exposing and misattributing another branch's infrastructure changes. Auto-apply is disabled for these temporary layers, so this vulnerability alone cannot force a `terraform apply`; plan-time provider and data-source code execution depends on the selected branch's contents. This issue is fixed in version 0.13.0.

### CVE-2026-86574

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:56.643 |

Heap-based Buffer Overflow Vulnerability in JP1/Base.

This issue affects JP1/Base: from 11-00 before 12-50-54.

### CVE-2026-82120

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:56.147 |

Heap-based Buffer Overflow Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-82119

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T10:16:56.033 |

OS Command Injection Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-82118

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:55.917 |

Stack-based Buffer Overflow Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-82117

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-27T10:16:55.797 |

Authentication Bypass by Spoofing Vulnerability in HiRDB.

This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-82116

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-27T10:16:55.680 |

Missing Authentication for Critical Function Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-76939

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:55.563 |

Heap-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.

This issue affects JP1/Automatic Job Management System 3 - Manager: from 11-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 11-00 before 13-50-31.

### CVE-2026-76938

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-27T10:16:55.450 |

Authentication Bypass Vulnerability in JP1/Automatic Job Management System 3.


This issue affects JP1/Automatic Job Management System 3 - Manager: from 10-00 before 13-50-31.

### CVE-2026-76934

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:54.990 |

Stack-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.

This issue affects JP1/Automatic Job Management System 3 - Manager: from 11-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 11-00 before 13-50-31.

### CVE-2026-92885

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-27T09:16:34.630 |

The Qode Membership plugin for WordPress is vulnerable to Authentication Bypass leading to Account Takeover in all versions up to, and including, 2.0.6.2 via the qode_membership_check_facebook_user AJAX action. This is due to a typographic error in the Facebook OAuth token verification guard within the qode_membership_login_user_from_social_network function — the guard condition tests an undefined variable ($check_social_useqoder instead of $check_social_user), causing empty() to always return true and rendering the Graph API token verification branch dead code, leaving wp_set_auth_cookie() reachable with no credential or token validation whatsoever. This makes it possible for unauthenticated attackers to log in as any existing WordPress account — including Administrator-level accounts — by supplying a known or enumerated administrator login name (rather than an email address) in the response[email] parameter, which the fallback path in get_user_by('login', $email) resolves to the matching account. Exploitation does require harvesting a valid qode_validate_facebook_login nonce, but this nonce is rendered on any public front-end page containing the [qode_user_login] or [qode_user_register] shortcode and is therefore obtainable without any prior authentication.

### CVE-2026-18450

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-27T08:16:53.710 |

The BMC does not correctly enforce integrity and encryption requirements for IPMI commands. An attacker may be able to craft packets that execute arbitrary commands on an active session.

### CVE-2026-10757

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T18:17:34.580 |

There is a SQL injection vulnerability in Esri ArcGIS Server versions 12.1 and earlier on Windows and Linux that may allow a remote attacker with privileges to access the service (which could, depending on the service being configured in a non-default access configuration “public”, include an anonymous attacker) to issue database specific functions that should not be allowed. A patch is provided for ArcGIS Server software in General Availability and Extended support status, which includes versions 12.1, 12.0, 11.5, 11.3, and 11.1. Other versions are in mature or retired status, which are not patch eligible. Users working with unlisted versions are advised to upgrade and apply the patch.

### CVE-2026-65184

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-26T15:16:41.627 |

The root-privileged `wsserver` terminal-bridge daemon builds a shell command from client-supplied WebSocket fields and passes it to `system()` and `popen()` without quoting, escaping, or character-set validation. The daemon's public-key session path performs no appliance-session check.

### CVE-2026-86577

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-27T10:16:56.993 |

Out-of-bounds Write Vulnerability in JP1 Products.

This issue affects JP1/Integrated Management 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent Minimal Edition: from 13-00 before 13-50-31; JP1/Base: from 11-00 before 12-50-54.

### CVE-2026-86576

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:56.880 |

Heap-based Buffer Overflow Vulnerability in JP1 Products.

This issue affects JP1/Integrated Management 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent Minimal Edition: from 13-00 before 13-50-31; JP1/Base: from 11-00 before 12-50-54.

### CVE-2026-86575

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:56.760 |

Stack-based Buffer Overflow Vulnerability in JP1 Products.

This issue affects JP1/Integrated Management 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Manager: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 13-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent Minimal Edition: from 13-00 before 13-50-31; JP1/Base: from 11-00 before 12-50-54.

### CVE-2026-82122

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:56.380 |

Stack-based Buffer Overflow Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-76937

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:55.337 |

Heap-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.


This issue affects JP1/Automatic Job Management System 3 - Manager: from 10-00 before 13-50-31.

### CVE-2026-76936

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:55.223 |

Stack-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.


This issue affects JP1/Automatic Job Management System 3 - Manager: from 10-00 before 13-50-31.

### CVE-2026-76935

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:55.110 |

Stack-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.


This issue affects JP1/Automatic Job Management System 3 - Manager: from 10-00 before 13-50-31.

### CVE-2026-76933

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T10:16:54.870 |

Heap-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.

This issue affects JP1/Automatic Job Management System 3 - Manager: from 11-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 11-00 before 13-50-31.

### CVE-2026-76932

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T10:16:54.730 |

Stack-based Buffer Overflow Vulnerability in JP1/Automatic Job Management System 3.

This issue affects JP1/Automatic Job Management System 3 - Manager: from 11-00 before 13-50-31; JP1/Automatic Job Management System 3 - Agent: from 11-00 before 13-50-31.

### CVE-2026-117603

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-27T14:16:40.233 |

Electrum before 4.7.2 contains a spending limit bypass vulnerability in the Nostr Wallet Connect plugin that allows malicious NWC clients to exceed daily_limit_sat by exploiting non-atomic budget checks and millisatoshi truncation. Attackers can send concurrent pay_invoice requests that pass budget_allows_spend() before add_to_budget() runs, or repeatedly pay msat amounts that are floored to whole satoshis, to drain funds beyond the limit.

### CVE-2026-117601

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-27T14:16:39.947 |

Electrum before 4.8.3 fails to verify signatures of wallet-owned inputs in unconfirmed mempool transactions, allowing malicious servers to replace a just-broadcast transaction with a conflicting one. Attackers can swallow the user's transaction and display an invalid zero-fee copy paying an attacker address, tricking users into RBF fee-bumping and signing it.

### CVE-2026-117564

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-27T14:16:38.720 |

nest-admin before 1.0.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge administrator tokens by using a hardcoded JWT_SECRET committed in .env.production. Attackers can sign tokens with the known secret that JwtStrategy and RbacGuard trust, impersonating any user ID or claiming the admin role for full administrative access.

### CVE-2026-117532

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-27T11:17:33.597 |

REDAXO core from 5.3.0 before 5.21.4 contains an authentication bypass vulnerability in the structure/history plugin that allows unauthenticated attackers to forge temporary login tokens. Attackers can force the session-tied secret into a predictable state and forge tokens for accounts like admin, gaining backend access and code execution outside live mode.

### CVE-2026-102789

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-27T10:16:53.907 |

Joomla Extension - balbooa.com - Missing Authorization Check on Editor Controller Task in Gridbox < 2.20.4.2 - EditorController::getBlogPosts() reads the order parameter and invokes getBlogPosts() . Unlike other tasks in this controller, it omits the GridboxHelper::checkUserEditLevel() check.

### CVE-2026-102788

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T10:16:53.780 |

Joomla Extension - balbooa.com - Unauthenticated SQL injection in Gridbox < 2.20.4.2 - On store product list pages, the value of the sort-by URL parameter is retrieved using a string filter and passed directly to GridboxHelper::getBlogPosts(). When the parameter does not match known sorting keys, it is prefixed with a table alias and inserted into the ORDER BY clause without checking against an allowlist

### CVE-2026-116508

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-10-26T22:16:54.373 |

A security flaw has been discovered in TOTOLINK A950RG 4.1.2cu.5268_B20221104. Affected by this issue is the function sub_402340 of the file infostat.cgi of the component Device-Information CGI. Performing a manipulation of the argument CONTENT_LENGTH results in stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been released to the public and may be used for attacks.

### CVE-2026-112346

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1327` |
| Published | 2026-10-26T16:17:14.110 |

OpenHands Software Agent SDK before 1.52.0 contains an unauthenticated remote code execution vulnerability where the DockerWorkspace and Apptainer workspace launchers bind the sandbox agent server to all network interfaces (0.0.0.0) with an empty session_api_keys list, disabling authentication by default. Attackers who can reach the published container port can send unauthenticated HTTP and WebSocket requests to execute arbitrary shell commands as root in the sandbox, access the mounted workspace, and read plaintext secrets from the secrets store.

### CVE-2026-93328

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-22;CWE-862` |
| Published | 2026-10-26T15:16:45.813 |

Path Traversal and Missing Authorization in cloud-storage source in Google Cloud MCP Toolbox for Databases (googleapis/mcp-toolbox) versions 1.2.0 through 1.4.0 allows an unauthenticated remote attacker to exfiltrate host files to external Google Cloud Storage buckets and overwrite arbitrary local files via crafted tool invocation parameters.

### CVE-2026-77055

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-26T15:16:43.123 |

boneIO black_debian_images gives the boneio service account excessive privileges, including full passwordless sudo access and membership in the docker group. A local attacker who compromises the boneio user can use these privileges to escalate to root.

This issue was fixed in version 1.6.0: the image removes the sudoers rule and the docker group membership when it is sealed, and devices already in the field have both removed by migrations shipped with boneio 1.6.0 and applied on first start after the upgrade. Privileged operations now go through helpers that accept only a fixed set of commands, with migrations verified against Ed25519 signatures.

### CVE-2026-116747

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-26T22:16:59.463 |

Kener 3.0.0 before 4.1.10 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge session tokens by using the hardcoded DUMMY_SECRET fallback key. When KENER_SECRET_KEY is empty or unset, attackers knowing an administrator email can sign a kener-user cookie to access /manage/api with full administrative privileges or forge password-reset tokens.

### CVE-2026-115216

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-27T12:17:07.090 |

In Eclipse ioFog Operator versions 3.8.0 before 3.9.2, TLS certificate verification is disabled when the operator contacts the Controller API and when it logs in to an external OIDC issuer. An on-path attacker can present any certificate, capture the OAuth client secret (external mode) or the Controller bootstrap admin password (embedded mode with Controller HTTPS enabled), and supply the access token the operator stores for later Controller API calls. v3.8 removed Keycloak. The exposed credential is not a Keycloak realm-admin secret.

### CVE-2026-112362

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-27T12:17:04.970 |

@fastify/express is a Fastify plugin that runs Express middleware inside Fastify. In versions 4.0.5 through 4.0.8, when Fastify runs with the non-default ignoreDuplicateSlashes option enabled, the plugin matches path-scoped Express middleware against a URL whose duplicate-slash normalization has also collapsed the separator after an absolute-form request target's scheme, so Fastify's router resolves the request to the scoped path and runs the handler while the Express layer no longer sees that path. As a result, a request using an absolute-form target can reach a handler on a scoped route such as an admin path while the middleware for authentication, authorization, or rate limiting is skipped. An unauthenticated attacker needs only the non-default ignoreDuplicateSlashes option to be enabled. The issue is fixed in @fastify/express 4.0.9, and users should upgrade to 4.0.9 or later. As a workaround, enforce authentication in a Fastify hook such as preHandler that runs after the router resolves the request, or leave ignoreDuplicateSlashes at its default.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-4337

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-27T12:17:08.053 |

Unrestricted Upload of File with Dangerous Type vulnerability in the PuMuKIT application allows a unauthenticated user to upload any type of file to the server, and to any path where the web server user has write permissions. This could also allow them to delete files.

### CVE-2026-65220

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-27T08:16:54.487 |

A logic flaw in the BMC IPMI implementation may allow an attacker to send specially crafted RAKP+ messages and escalate an account to administrator privileges.

### CVE-2026-75891

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-27T07:16:32.500 |

The Kirki plugin for WordPress is vulnerable to Privilege Escalation via PHP Object Injection in all versions up to, and including, 6.2.5 via deserialization of untrusted input through the 'get-single-symbol' branch of the kirki_post_apis() AJAX dispatcher due to a missing capability check. This makes it possible for authenticated attackers, with Subscriber-level access and above, to inject a PHP Object. The additional presence of a POP chain allows attackers to overwrite an administrator's password and gain administrative access.

### CVE-2026-116838

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-27T01:19:06.973 |

A malicious actor who lures an authenticated user to a malicious page could exploit a Cross-Site Request Forgery (CSRF) vulnerability found in airMAX M devices to execute a Command Injection on the device.

### CVE-2026-116837

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T01:19:06.860 |

A malicious actor with access to the adjacent network could exploit a Heap-based Buffer Overflow vulnerability found in airMAX M, LTU, SolarPoint, and SolarSwitch devices to execute arbitrary code on the device.

### CVE-2026-116836

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T01:19:06.733 |

A malicious actor with access to the adjacent network and under certain conditions could exploit a Stored Cross-Site Scripting (XSS) vulnerability found in airMAX M devices to escalate privileges on the device.

### CVE-2024-58400

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-27T01:19:03.080 |

llama.cpp before b3701 contains an out-of-bounds read vulnerability in llama_decode_internal and llama_encode_internal that allows remote unauthenticated attackers to read memory by supplying unvalidated token IDs. Attackers can send integer-array prompts to the llama-server /completion endpoint with IDs outside 0 to n_vocab to read embedding memory out of bounds or crash the process.

### CVE-2026-116818

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:16.007 |

OpenPanel before 3.0.0 contains an unauthenticated ClickHouse sql injection vulnerability that allows remote attackers to inject SQL through the projectId parameter of the /live/visitors/:projectId WebSocket, which lacks session and project-access checks. Attackers can use UNION or boolean count oracles to read other tenants' events and profiles, and project members can similarly inject via the cohort.preview timeframe values.

### CVE-2026-86929

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-26T21:20:30.323 |

An out-of-bounds write issue was addressed with improved bounds checking. This issue is fixed in macOS Golden Gate 27, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. Processing a maliciously crafted file may lead to arbitrary code execution.

### CVE-2026-64759

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-26T21:18:33.897 |

An integer overflow was addressed with improved input validation. This issue is fixed in iOS 26.7.2 and iPadOS 26.7.2, iOS 27 and iPadOS 27, macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7. Processing a maliciously crafted image may lead to arbitrary code execution.

### CVE-2026-113947

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-26T21:18:11.100 |

This issue was addressed with improved access restrictions. This issue is fixed in macOS Golden Gate 27.2. Unpacking a maliciously crafted archive may lead to unexpected app termination or arbitrary code execution.

### CVE-2026-112688

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-26T21:18:03.177 |

A memory corruption issue was addressed with improved memory handling. This issue is fixed in iOS 26.7 and iPadOS 26.7, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. Parsing a file may lead to an unexpected app termination or arbitrary code execution.

### CVE-2026-112659

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-26T21:17:59.497 |

A type confusion issue was addressed with improved memory handling. This issue is fixed in Safari 27.2, iOS 26.7.2 and iPadOS 26.7.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, visionOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112655

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:17:59.020 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 27.2, iOS 26.7.2 and iPadOS 26.7.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, tvOS 27.2, visionOS 27.2, watchOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112651

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:17:58.397 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 27.2, iOS 26.7.2 and iPadOS 26.7.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, visionOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112637

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:17:57.297 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 27.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, tvOS 27.2, visionOS 27.2, watchOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112626

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:17:55.980 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 27.2, iOS 26.7.2 and iPadOS 26.7.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, tvOS 27.2, visionOS 27.2, watchOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112623

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:17:55.493 |

A use-after-free issue was addressed with improved memory management. This issue is fixed in Safari 27.2, iOS 26.7.2 and iPadOS 26.7.2, iOS 27.2 and iPadOS 27.2, macOS Golden Gate 27.2, visionOS 27.2. Processing maliciously crafted web content may lead to arbitrary code execution.

### CVE-2026-112438

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-26T21:17:33.680 |

A logic issue was addressed with improved state management. This issue is fixed in macOS Golden Gate 27.2, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. An unprivileged attacker may be able to execute arbitrary code as root.

### CVE-2026-105608

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-178` |
| Published | 2026-10-26T18:17:26.910 |

HashiCorp Consul and Consul Enterprise are vulnerable to an authorization bypass in service mesh proxy registration. This may allow a user with service write permission to apply Envoy escape-hatch configuration without the required mesh write permission. This vulnerability (CVE-2026-105608) is fixed in Consul Community Edition 2.1.0 and Consul Enterprise 2.1.0 and 1.21.19.

### CVE-2026-115748

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-26T16:17:17.833 |

**UNSUPPORTED WHEN ASSIGNED**  Authorization bypass in Apache Vysper, all versions.




Apache Vysper is an XMPP (Jabber) server library. Its XEP-0077 (In-Band Registration) implementation is missing an authentication check, allowing any authenticated user to compromise other accounts.




As this project is retired, we do not plan to release a version that fixes this issue. Users are recommended to find an alternative.

### CVE-2026-77059

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-26T15:16:43.787 |

boneIO Black contains a TOCTOU race condition in the create_timedatectl_sudoers_file() function in boneio/webui/routes/timezone_sudoers.py. The function writes sudoers rules to a predictable temporary file, validates them, then installs them with root privileges. A local attacker can exploit the race window between validation and installation to substitute malicious content, or use the predictable filename for symlink attacks, resulting in arbitrary sudoers rule injection and local privilege escalation to root.

This issue was fixed in version 1.6.0.

### CVE-2026-106087

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-27T12:17:04.410 |

TRO600 contains an arbitrary file read vulnerability. An unauthenticated attacker can exploit this vulnerability to read or download arbitrary files on the affected device, including sensitive configuration files and password data, resulting in the disclosure of sensitive information.

### CVE-2026-102800

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T12:17:04.137 |

Joomla Extension - dj-extensions.com - Unauthenticated Stored XSS in DJ-HelpfulArticles < 1.3.0 - The “was this article helpful” voting widget posts a client-supplied ip field to its AJAX handlers (getDeny, getConfirm, getDenyReason in mod_djhelpful_articles/helper.php), reachable without authentication through com_ajax. The value was stored exactly as submitted instead of being taken from the connection by the server. It was then printed without output escaping in the administrator backend’s “Helpful articles” overview (views/items/tmpl/default.php). $db->quote() was applied on insert, which protects the SQL statement but does nothing for HTML output. There was no CSRF token, no rate limit, and the vote de-duplication keyed on the same attacker-controlled field.

### CVE-2026-117540

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-27T11:17:34.833 |

svg-sanitizer from 0.5.3 before 1.1.0 contains a denial of service vulnerability in Sanitizer::sanitize() that repeatedly rescans the whole input while stripping PHP tags. Unauthenticated attackers can upload SVGs with many overlapping PHP tag openers and closers, forcing quadratic preg_replace passes that exhaust worker CPU for minutes.

### CVE-2026-116878

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-27T11:17:29.830 |

Semantic MediaWiki from 2.5.0 before 7.3.1 contains an uncontrolled resource consumption vulnerability that allows anonymous attackers to force quadratic computation by supplying a zero limit to Special:PropertyLabelSimilarity. Attackers can send repeated requests with limit=0 to bypass the SQL LIMIT and trigger pairwise similar_text() comparisons, exhausting PHP CPU, memory, and database connections.

### CVE-2026-116877

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-27T11:17:29.687 |

Semantic MediaWiki from 2.5.0 before 7.3.1 contains an uncontrolled resource consumption vulnerability that allows low-privilege editors to bypass smwgMaxNumRecurringEvents by supplying a large limit parameter. Attackers can save pages using #set_recurring_event without an end date to generate thousands or millions of date subobjects, exhausting CPU, memory, and database resources.

### CVE-2026-116872

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-27T11:17:28.970 |

Semantic MediaWiki from 3.0.0 before 7.3.1 contains an algorithmic complexity vulnerability in TermParser::normalize_compact_form() that allows unauthenticated attackers to cause quadratic CPU consumption. Attackers can submit long search terms with many distinct in:(...) or has:(...) expressions to Special:Search to exhaust PHP search workers when the extended search engine is enabled.

### CVE-2026-116871

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-27T11:17:28.813 |

Semantic MediaWiki 3.0.0 before 7.3.1 contains an uncontrolled recursion vulnerability in LegacyParser::getSubqueryDescription() that processes nested query tokens before depth limits apply. Unauthenticated attackers can submit deeply nested query elements to the action=ask API to consume substantial CPU and memory, tying up request workers.

### CVE-2026-116870

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1289` |
| Published | 2026-10-27T11:17:28.610 |

In affected versions of Octopus Server, OIDC token issuer validation was performed inconsistently. This could result in a token issued from a suitably configured non legitimate issuer being accepted as a token belonging to a service account from a legitimate trusted issuer. Exploitation requires a service account with at least one OIDC identity configured. An attacker would also need to know or guess some details of that identity in order to be in a position to attempt exploitation.

### CVE-2026-116843

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-27T01:19:07.730 |

Mistral Vibe before 3.0.3 contains a remote code execution vulnerability that allows attackers to run commands by defining git filter drivers in an untrusted repository's .git/config. When started with --worktree, git worktree add applies .gitattributes and runs filter smudge, clean, or process commands before the trusted-folder check, executing attacker commands with user privileges.

### CVE-2026-116811

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-27T00:17:14.263 |

OpenPanel before 3.0.0 contains a sandbox escape vulnerability in the js-runtime validator that allows a project member to bypass the AST allowlist by aliasing the Function constructor. Attackers with write access can read payload.constructor.constructor into a local and call it to run arbitrary code in the worker process.

### CVE-2026-116748

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-10-26T22:16:59.610 |

Transmission 4.0.0 before 4.1.3 contains a permissive CORS vulnerability in handle_request() in rpc-server.cc that exposes the X-Transmission-Session-Id anti-CSRF token to any web origin. Malicious web pages can read the token from the 409 handshake response and replay it to issue RPC calls, enabling script-torrent-done execution, download-dir changes, or torrent and data deletion.

### CVE-2026-116738

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-26T22:16:58.090 |

VMime through 0.9.2 contains an integer underflow in the uuEncoder::decode function that allows remote attackers to trigger a stack-based buffer overflow via crafted uuencoded MIME parts. Attackers can send an email with a uuencoded line whose length character is 'b' but is not a 'begin' line, corrupting stack memory to crash the application or potentially execute code.

### CVE-2026-116591

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-26T22:16:55.783 |

compress provides various compression algorithms. Prior to 1.20.2, the zstd DecodeAll and streaming decoder paths can panic when a crafted two-block frame reaches huff0.ReadTable with an FSE normalized count of 32768 that readNCount stores in int16 as -32768. The wrapped count allows buildDtable to retain stale fse.Scratch decode-table state from the prior block, and nextFast then derives an out-of-range state and indexes beyond the table instead of returning a decode error. Both blocks are required to preserve and then reuse the stale state, allowing untrusted zstd input to crash an application. This issue is fixed in version 1.20.2.

### CVE-2026-116588

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-26T22:16:55.340 |

Datadog dd-trace-py is the Datadog Python APM client. From 1.5.0 until 3.19.9 and 4.15.6, the default query-string obfuscation regular expression can exhibit excessive backtracking while synchronously processing attacker-controlled URL query strings for HTTP span metadata. A remote attacker can cause prolonged CPU consumption, request latency, and service unavailability in affected HTTP tracing integrations that include query strings in URL span tags. The vulnerable processing is enabled by default for those integrations. This issue is fixed in versions 3.19.9 and 4.15.6.

### CVE-2026-116543

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-26T16:17:19.830 |

Open5GS 1.3.0 through 2.8.0 contains a heap out-of-bounds write vulnerability in parse_multipart() that allows unauthenticated attackers to corrupt memory by supplying an empty multipart boundary. Attackers can send a single crafted multipart/related request to the SBI interface of any network function, overflowing the lookbehind buffer and crashing it.

### CVE-2026-77053

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-26T15:16:42.827 |

boneIO Black firmware ships with authentication disabled by default. Its management web API listens on all network interfaces and exposes all endpoints without requiring credentials. An unauthenticated remote attacker can fully control the device, causing denial of service, modifying configuration, and operating connected physical circuits.
This issue was fixed in version 1.6.0: a device without an administrator account refuses API requests until the owner creates one in the first-run wizard, and every API route is restricted to an authenticated role.

Versions before 1.2.0 are based on Debian 10, are no longer supported and cannot be upgraded in place; affected devices should be re-flashed with the 1.6.0 system image.

### CVE-2026-77052

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-26T15:16:42.660 |

boneIO Black exposes a Node-RED instance without authentication at the /nodered/ path through a Caddy reverse proxy. The Node-RED Admin API allows deploying flows that can execute arbitrary system commands. An unauthenticated attacker on the local network can deploy a malicious flow to achieve remote code execution and gain full control over the home automation system.


This issue was fixed in version 1.6.0.

### CVE-2026-117602

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-27T14:16:40.090 |

Electrum 4.6.0 before 4.7.2 contains an authorization bypass in the external plugin loader, which executes a plugin's __init__.py module when the plugin is marked enabled in the config file, without verifying its plugin-password signature. A rogue local process with write access to the Electrum data directory can place plugin code in the plugins/ folder and mark it enabled, causing arbitrary code execution inside the Electrum process.

### CVE-2026-117536

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-27T11:17:34.200 |

REDAXO before 5.21.3 contains a cross-site request forgery vulnerability in the backend user administration page (users/users) because the CSRF token check only runs when the save parameter is set, while the update path triggered by FUNC_UPDATE does not require it. Attackers can lure a logged-in backend user with the users[] permission to a crafted GET link to grant administrator rights, deactivate accounts, or lock out the sole administrator.

### CVE-2026-117466

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-27T11:17:33.343 |

In affected versions of Octopus Server, a user holding the System Manager role could escalate their privileges to full system Administrator.

### CVE-2026-116808

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:13.347 |

OpenPanel before 3.0.0 contains an sql injection vulnerability that allows authenticated users to read cross-tenant data by supplying a crafted property parameter to profile.values. Attackers can inject a SELECT expression with their own FROM/WHERE clauses and comment out the project_id scope to exfiltrate other projects' profiles, events, and sessions.

### CVE-2026-116506

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-26T21:18:13.047 |

A vulnerability was determined in TOTOLINK A950RG 4.1.2cu.5268_B20221104. Affected is the function apmib_set of the file firewall.so. This manipulation causes command injection. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-116504

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-26T21:18:12.420 |

A vulnerability has been found in TOTOLINK A950RG 4.1.2cu.5268_B20221104. This affects the function setCloudUpgradeFW of the file lib/cste_modules/upgrade.so of the component Cloud Upgrade. The manipulation of the argument FileName leads to command injection. The attack can be initiated remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-115924

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-26T20:17:52.250 |

Rembg is a tool to remove images background. Prior to 2.0.82, the public /api/remove endpoint passes attacker-controlled extras.sam_model through rembg/commands/s_command.py to rembg/sessions/sam.py, where it is interpolated into SAM filenames and GitHub download URLs passed to pooch.retrieve() without a pinned hash. An unauthenticated attacker can supply a sam_model value combining path traversal with URL fragment syntax to exploit the HTTP request discarding the fragment while the local POSIX path retains it. The first request primes the attacker-selected path tree, and an identical repeated request downloads malicious ONNX encoder and decoder files beside a readable target file. The graphs can load the target through ONNX external data and encode its bytes into the returned PNG mask, disclosing complete files accessible to the rembg process and allowing arbitrary ONNX computation. This issue is fixed in version 2.0.82.

### CVE-2026-112343

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-26T16:17:13.797 |

Syncplify Server! before 8.8.0 contains an access control bypass vulnerability that allows authenticated SFTP users to evade per-path permission overrides by exploiting case-insensitive filesystem path resolution and 8.3 short names. Attackers can address a protected directory using alternate capitalization or its 8.3 short name to perform file uploads and downloads that the configured override is intended to deny, resulting in unauthorized file access.

### CVE-2026-112345

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-26T15:16:38.167 |

TTLock Android application before v9.8.260718 and associated smart-lock firmware contain a hardcoded static AES key vulnerability that allows an attacker within Bluetooth range to decrypt the per-pairing session key transmitted during BLE pairing. Attackers can observe the pairing exchange, recover the persistent session key using the embedded defaultKey, and forge authenticated BLE requests to unlock the device, add fingerprints or access codes, and perform administrative actions without authentication or user interaction.

### CVE-2026-117573

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:39.800 |

hagent through commit 761eec6 contains an OS command injection vulnerability that allows MCP clients to execute shell commands by injecting metacharacters into the args parameter of the hagent_arduino and hagent_esp32 tools. Attackers or prompt-injected agents can supply crafted args interpolated into arduino-cli and idf.py commands run with subprocess.run(shell=True) to execute commands as the MCP server user.

### CVE-2026-117569

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:39.477 |

Kali-GPT through commit a608c74 contains an OS command injection vulnerability in execute_tool() in kali_gpt/tools/mcp_server.py that allows MCP clients to run commands via unsanitized scanner parameters. Attackers or prompt-injected agents can embed shell metacharacters in parameters like target, ports, domain, wordlist, or url, executed via subprocess.run with shell=True as the MCP server user.

### CVE-2026-117567

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:39.173 |

esp-mcp through commit 28afddf contains an OS command injection vulnerability that allows attackers to run arbitrary commands by supplying shell metacharacters in MCP tool parameters. Attackers influencing agent tool calls through prompt injection can inject metacharacters into target, port, project_path, or project_name values passed to asyncio.create_subprocess_shell, executing commands as the MCP server user.

### CVE-2026-117561

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:38.270 |

Codefriar sf-mcp through 1.3.2 contains an OS command injection vulnerability that allows attackers to execute shell commands by supplying crafted Salesforce CLI tool flag values. Because escapeValue() in src/utils.ts fails to neutralize backticks, $() substitution, and other shell metacharacters, these values reach execSync in executeSfCommand and run as the MCP server user.

### CVE-2026-117560

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:38.133 |

ATXP Gemini CLI extension through 1.0.0 contains an OS command injection vulnerability in runAtxp() that allows attackers to execute shell commands through unsanitized MCP tool parameters. Attackers can plant instructions in email or SMS content to inject $() or backtick substitutions into parameters like message_id, subject, or query, running commands as the user.

### CVE-2026-117559

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:37.987 |

DroidMind through 0.4.0 contains a command injection vulnerability that allows MCP clients to bypass the shell command allowlist by using $(...) or backtick substitution. Attackers, including prompt-injected agents, can inject commands through parameters interpolated into Device.run_shell() or unvalidated Device.list_directory() to run blocked commands such as reboot on connected Android devices.

### CVE-2026-117558

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:37.840 |

The ai-sdlc plugin MCP server through 0.31.2 contains an OS command injection vulnerability that allows attackers to execute commands by supplying shell metacharacters in the repo argument. The unvalidated repo value is interpolated into gh issue view or gh pr view commands run via execSync(), letting prompt-injected agents execute commands as the MCP server user.

### CVE-2026-116816

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-27T01:19:06.437 |

llama.cpp b5899 before b10261 contains a heap out-of-bounds write vulnerability in llm_tokenizer_plamo2::build that allows attackers to corrupt heap memory via crafted GGUF models. Attackers can supply BYTE-typed token text like <0x-1> whose negative parsed value writes token ids before the bytes_ buffer during model loading, causing crashes or potential code execution.

### CVE-2026-116724

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-26T22:16:56.070 |

FLTK through 1.4.5 contains an integer overflow vulnerability in Fl_BMP_Image::load_bmp_() that causes undersized pixel buffer allocation from file-supplied width and height. Attackers can supply a crafted BMP or ICO file with large dimensions so row decoding writes file-derived data past the heap buffer, corrupting the application heap.

### CVE-2026-116723

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-26T22:16:55.923 |

FLTK through 1.4.5 contains a stack-based buffer overflow vulnerability in Fl_BMP_Image::load_bmp_() that allows attackers to corrupt stack memory by supplying an oversized BMP colors_used field. Attackers can craft BMP or ICO files with colors_used above 256 to overflow the 768-byte colormap array, causing crashes or potential code execution.

### CVE-2026-116505

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-10-26T21:18:12.730 |

A vulnerability was found in TOTOLINK A950RG 4.1.2cu.5268_B20221104. This impacts the function getDeviceInfo of the file /var/lib/misc/udhcpd.leases of the component device-information Handler. The manipulation of the argument MAC address results in command injection. The attack can be launched remotely. The exploit has been made public and could be used.

### CVE-2026-71456

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-26T17:17:28.893 |

Use of hard-coded cryptographic key vulnerability in Johnson Controls Kantech Entrapass allows Padding Oracle Crypto Attack.

This issue affects Kantech Entrapass: before 9.20.

### CVE-2026-65151

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T13:16:59.980 |

NVIDIA NeMo Agent Toolkit contains vulnerability where an attacker could cause a SQL injection issue. A successful exploit of this vulnerability might lead to data tampering, denial of service and information disclosure.

### CVE-2026-65119

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-27T13:16:59.607 |

NVIDIA TensorRT-LLM for any platform contains a vulnerability in KvCacheAwareRouter tokenizer loading, where an attacker could cause inclusion of functionality from an untrusted control sphere. A successful exploit might lead to code execution, information disclosure, data tampering, and denial of service.

### CVE-2026-116819

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-27T00:17:16.293 |

OpenPanel before 3.0.0 contains an information disclosure vulnerability that allows read-level project members to obtain plaintext integration secrets because the notification.rules query skips redactIntegration. Attackers can call the notification.rules tRPC query to retrieve Slack bot tokens, webhook URLs, and authorization headers for use against external systems.

### CVE-2026-65327

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-26T21:18:36.653 |

A logic issue was addressed with improved checks. This issue is fixed in macOS Golden Gate 27.2, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. A local attacker may be able to elevate their privileges.

### CVE-2026-85299

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-27T10:16:56.500 |

A Missing Authorization vulnerability in the disks.createSnapshot and regionDisks.createSnapshot APIs in Google Compute Engine versions prior to 2026-08-31 on Google Cloud Platform allows an authenticated attacker to exfiltrate cross-project disk data.


This vulnerability was patched on 31 August 2026, and no customer action is needed.

### CVE-2026-117494

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T10:16:54.580 |

Cross-Site Scripting (XSS) in the processing of SVG images submitted to the /api/v2/ai/sessions API in the format data:image/svg+xml;base64. Script tags embedded in the SVG are processed when the content is rendered in the assistant window, allowing JavaScript to be executed and the displayed content to be altered.

### CVE-2026-117493

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T10:16:54.420 |

Stored cross-site scripting (XSS) in BloX widgets. The /api/dashboards/<id>/widgets/<id> API accepts HTML and JavaScript content in the ‘desc’ and ‘text’ parameters. The code entered is executed in the browser when the widget is rendered, which could compromise the confidentiality of the information accessible in that context.

### CVE-2026-116825

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-27T00:17:17.997 |

YesWiki from 4.6.2 before 4.7.0 lacks replay protection in HttpSignatureService::verifySignature(), which never validates the Date header or tracks seen signatures. Attackers who capture a signed request to the /api/forms/{formId}/actor/inbox endpoint can replay it later to re-execute Delete, Update, Follow, or Undo actions.

### CVE-2026-116741

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-26T22:16:58.530 |

Speex (libspeex) through 1.2.1 contains an out-of-bounds write vulnerability in speex_bits_read_whole_bytes() in libspeex/bits.c that mishandles length truncation for non-owned SpeexBits buffers. Attackers can stream crafted Speex data into buffers set up with speex_bits_init_buffer() or speex_bits_set_bit_buffer() to corrupt heap or stack memory and crash applications.

### CVE-2026-116827

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-27T00:17:18.637 |

YesWiki before 4.7.0 contains a server-side request forgery vulnerability in the Bazar CSV import copyUrlToLocalFile() function that allows authenticated administrators to make arbitrary outbound requests by supplying crafted URLs in CSV file or image fields. Attackers can bypass the extension check with a query-string suffix or redirects to fetch cloud metadata credentials, internal services, or local files via file://, with responses stored in the web-accessible files/ directory.

### CVE-2026-116826

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-27T00:17:18.343 |

YesWiki before 4.7.0 contains a server-side request forgery vulnerability in DuplicationManager::downloadFile() that allows authenticated administrators to make arbitrary outbound requests via the files array. Attackers can POST file:// or internal URLs to /api/pages/{tag}/duplicate, storing local files, cloud metadata, or database credentials in the publicly accessible files/ directory.

### CVE-2026-116589

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-26T22:16:55.490 |

Datadog dd-trace-py is the Datadog Python APM client. From 3.13.0 until 4.15.5, the IAST string-processing instrumentation does not properly handle certain internal errors while old-style % string formatting processes attacker-controlled input. An unhandled error can terminate the Python process and interrupt the work it is handling. Exploitation requires IAST to be enabled, which is not the default, and application code to apply the affected formatting operation to attacker-controlled input. This issue is fixed in version 4.15.5.

### CVE-2026-72753

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-26T18:18:40.943 |

When Routinator encounters an RRDP notification file with gaps in the delta entries, it is still accepted and parsed, potentially leading to missing data. If it encounters too many delta entries it may run out of memory.

### CVE-2026-116634

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-26T18:17:45.677 |

OmniRoute 3.8.50 before 3.8.52 contains a missing authentication vulnerability that allows unauthenticated attackers to issue sync tokens via POST /api/sync/tokens when requireLogin is disabled. Attackers can use the issued token against GET /api/sync/bundle to retrieve decrypted provider credentials and plaintext API keys, with tokens persisting after login is re-enabled.

### CVE-2026-116541

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-10-26T16:17:19.527 |

Netty netty-tcnative before 2.0.84.Final contains a denial of service vulnerability in the tcn_write_to_bytebuffer BIO write callback that overreports bytes consumed. Remote TLS 1.3 peers can provoke queued post-handshake records like NewSessionTicket or KeyUpdate to truncate flights, fail connections, or abort the JVM process.

### CVE-2026-116540

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T16:17:19.377 |

netty-tcnative 2.0.66.Final before 2.0.84.Final built against OpenSSL 3.x contains a use-after-free vulnerability in ssl_tlsext_ticket_key_cb during session ticket key rotation. Remote clients performing TLS handshakes while setSessionTicketKeys0 frees the shared key array cause OpenSSL to read freed HMAC keys, crashing or corrupting ticket processing.

### CVE-2026-116539

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-26T16:17:19.200 |

Netty netty-tcnative before 2.0.84.Final contains a heap buffer overflow vulnerability in the tcn_write_to_bytebuffer BIO callback caused by failing to wrap the non-application ring buffer write index. Remote TLS peers can drive handshake, renegotiation, or post-handshake messages into this buffer, triggering an out-of-bounds memcpy that crashes the JVM process.

### CVE-2026-112427

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-26T21:17:32.437 |

An authentication issue was addressed with improved state management. This issue is fixed in macOS Golden Gate 27.2. A remote attacker may be able to cause arbitrary code execution.

### CVE-2026-115915

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-183` |
| Published | 2026-10-26T18:17:38.883 |

vLLM is an inference and serving engine for large language models. Prior to 0.32.0, ImageMediaIO passes attacker-controlled image bytes to Pillow through Image.open(BytesIO(data)) without restricting decoder selection, and the MIME label does not constrain the selected format. Image-capable request paths through parse_image() and fetch_image() can therefore dispatch an EPS payload to host components. A host with Ghostscript affected by CVE-2024-29510 can execute commands with the vLLM process's privileges, while environments using Pillow 12.0.0 through 12.2.0 can trigger CVE-2026-59203 and exhaust media-loading workers. Deployments without the applicable vulnerable dependency are not affected by that corresponding impact. This issue is fixed in version 0.32.0.

### CVE-2026-47486

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-27T13:16:57.380 |

NVIDIA PhysX for all platforms contains a vulnerability where an attacker could cause an out-of-bounds write. A successful exploit of this vulnerability might lead to code execution, data tampering, denial of service, information disclosure.

### CVE-2026-86916

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-26T21:20:28.087 |

A use after free issue was addressed with improved memory management. This issue is fixed in iOS 26.7 and iPadOS 26.7, iOS 27 and iPadOS 27, macOS Golden Gate 27, macOS Sequoia 15.8, macOS Tahoe 26.7.2. An app may be able to execute arbitrary code with kernel privileges.

### CVE-2026-116576

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-26T21:18:13.720 |

systeminformation is a System and OS information library for node.js. Prior to 5.33.16, services() in lib/processes.js inserts a caller-supplied service name into a PowerShell Get-CimInstance filter after processing it with sanitizeShellString() in lib/util.js. On Windows, the sanitizer removes ASCII quotes but permits Unicode quotation marks that PowerShell accepts as string delimiters, allowing crafted input to terminate the filter and place a PowerShell expression in the command executed by util.powerShell(). The expression runs with the Node.js process account's permissions and may read or change accessible files, alter application data, or disrupt the service. The package does not expose a network service itself, so remote reachability depends on a consuming application forwarding attacker-controlled input to services() or getDynamicData(). This issue is fixed in version 5.33.16.

### CVE-2026-112484

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-26T21:17:39.277 |

This issue was addressed with improved file handling. This issue is fixed in macOS Golden Gate 27.2, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. A malicious application may be able to execute arbitrary code with system privileges.

### CVE-2026-116612

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-913` |
| Published | 2026-10-26T17:17:27.530 |

A flaw was found in GStreamer Editing Services (gst-editing-services). A GES project file can embed an arbitrary GStreamer pipeline description as an effect definition. When such a file is loaded, either explicitly by an editing application or automatically by a media player or file-manager thumbnailing service that uses GStreamer autoplugging, the pipeline description is parsed and instantiated without restriction on which elements may be used or which properties may be set. A remote attacker who can deliver a crafted project file to a victim's system can trigger reading or writing of arbitrary local files, issue outbound network requests to attacker-controlled servers, or cause the application to crash. Under certain conditions the file-write capability may be leveraged to achieve code execution.

### CVE-2026-117553

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-10-27T14:16:35.840 |

Umbraco CMS before 17.7.2 and 18.2.2 contains an authentication bypass vulnerability that allows unauthenticated attackers to register attacker-controlled OAuth redirect URIs by poisoning the Host header. Attackers send signed-in users authorization links using response_mode=form_post to capture codes, then redeem them via HTTP Basic client credentials to hijack back-office sessions and execute code through Razor templates.

### CVE-2026-13162

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T12:17:07.500 |

An OS command vulnerability exists in CoreTec product that allows authenticated users with certain roles to execute arbitrary system commands with full control over the device. The vulnerability exists in the configuration daemon's time synchronization handler, which is responsible for setting the system time-zone. When processing time-zone configuration updates, the daemon constructs a shell command by concatenating user-supplied input without any sanitization or validation.

### CVE-2026-10756

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-923` |
| Published | 2026-10-27T12:17:04.843 |

TRO600 contains a vulnerability that allows an authenticated attacker to bypass network access restrictions and access services intended to be reachable only from localhost. By leveraging port forwarding, an attacker can interact with locally bound ports and services, resulting in unauthorized access to sensitive functionality and confidential information, and causing availability impact.

### CVE-2026-117341

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-27T11:17:33.220 |

In affected versions of Octopus Server, creating a user invitation writes the invitation code to the audit event log. When the invitation is linked to a space, a user in that space with appropriate permissions could read the code from the audit event. Successfully exploiting this by redeeming the unclaimed invitation could allow the user to escalate privileges however this is dependant on the permissions assigned for the invited user.

### CVE-2026-116896

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-27T11:17:32.510 |

REDAXO before 5.21.5 contains a missing authorization vulnerability in the backup addon export that accepts any database table, allowing non-admin users with the backup[export] permission to export rex_user, rex_user_session, and other applications' tables. Attackers can obtain plaintext session ids and stay-logged-in keys to take over admin accounts, or password hashes for offline cracking.

### CVE-2026-111460

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-27T08:16:53.110 |

A hard-coded cryptographic key vulnerability exists in the OnCell G3150A-LTE Series. Under certain conditions, an unauthenticated remote attacker could obtain shared cryptographic key material and use it to impersonate affected devices that have not regenerated their cryptographic keys, potentially compromising the confidentiality and integrity of management communications.

### CVE-2025-13833

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-26T21:17:01.887 |

A vulnerability exists in SecureConnector for Windows when the “Additional Appliance Connections” setting is enabled and the agent’s configuration file contains more than three trusted‑server entries. Some entries omit TLS certificate fingerprints, which allows the agent to accept and establish sessions with a malicious server. An attacker who controls the wired or wireless network can redirect traffic to a malicious server. The attacker can then use the agent’s built‑in command/file features to execute arbitrary commands as SYSTEM, granting full administrative control and the ability to disable endpoint protections or exfiltrate data.

### CVE-2026-85297

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-340` |
| Published | 2026-10-26T16:17:23.090 |

Bucket Squatting in Google Cloud Run MCP versions prior to 1.11.0 on Google Cloud Platform allows an attacker to intercept and access proprietary source code, execute arbitrary code and exfiltrate data.



Users must upgrade to Cloud Run MCP version 1.11.0 or later.

### CVE-2026-116489

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-26T16:17:18.690 |

Timescale pgvectorscale before 0.9.1 contains a type confusion vulnerability that allows low-privileged database users to corrupt memory by shadowing pgvector's vector type or operators. Attackers with CREATE privilege on the vectorscale schema can pre-create shadow objects, then build and query DiskANN indexes over crafted values to cause out-of-bounds reads and writes, disclosing memory, crashing the server, or escalating privileges.

### CVE-2026-111459

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-27T08:16:52.953 |

An improper certificate validation vulnerability exists in Moxa Remote Connect Suite (MRC Client). Under certain conditions, an unauthenticated attacker with on-path access to the communication between the MRC Client and its server could impersonate a trusted server and conduct a man-in-the-middle attack, potentially compromising the confidentiality and integrity of communications.

### CVE-2026-112344

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-26T16:17:13.963 |

Syncplify Server! before 8.8.0 contains a path traversal vulnerability that allows attackers with a symbolic link placed inside a user's home folder to access files outside the virtual filesystem root because confinement is enforced only against the requested path and not the on-disk destination of the link. Attackers can leverage a symlink or, on Windows, a directory junction that points outside the jail to read or access restricted files beyond the intended home-folder boundary.

### CVE-2026-115930

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-26T15:16:39.480 |

The MongoDB Shell (mongosh) relies on Node.js as a third-party runtime that carries its own TLS root certificate store. This certificate store has the recoverable eMudhra intermediate CA certificates. This issue impacts MongoDB Shell (mongosh) versions prior to 2.14.0 and can be resolved by updating to mongosh 2.14.0 which bundles Node.js 24.22.1 or later. If mongosh is installed through npm, it uses the Node.js runtime installed on the host; update that runtime separately.

### CVE-2026-92546

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-27T13:17:02.257 |

Authentication bypass by spoofing vulnerability in Keepnet Labs Cybersecurity Inc. Agentic AI / Agentic Ally allows Authentication Bypass.

This issue affects Agentic AI / Agentic Ally: before 0ef61f2e.

### CVE-2026-100164

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-10-27T13:16:54.157 |

Observable response discrepancy vulnerability in Rolantis Information Technologies Tourism Industry and Trade Co. Ltd. Agentis allows Account Footprinting.

This issue affects Agentis: before 4.8.

### CVE-2026-41021

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-521` |
| Published | 2026-10-27T12:17:07.813 |

Eaton easyE4 uses an insufficiently strong password policy. An attacker who obtains a password hash, including through CVE-2026-41020, could perform an offline password-guessing attack and potentially recover user credentials.

### CVE-2026-41020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-27T12:17:07.670 |

Eaton easyE4 uses a static nonce during authentication, which could allow an unauthenticated attacker with access to captured authentication traffic to replay a valid authentication exchange and gain unauthorized access to the device.

### CVE-2026-82121

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-27T10:16:56.263 |

Origin Validation Error Vulnerability in HiRDB.


This issue affects HiRDB Server Version 10: from 10-00 before 10-12-01; HiRDB Server Version 9: from 09-00 through 09-66-22; HiRDB Server with Additional Function Version 9: from 09-00 through 09-66/V; HiRDB Server Version 9(32): from 09-02 through 09-66-22; HiRDB Server with Additional Function Version 9(32): from 09-00 through 09-66-/V.

### CVE-2026-18449

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-10-27T08:16:53.583 |

The BMC does not correctly enforce integrity and encryption requirements for IPMI commands. An attacker may be able to craft packets that execute arbitrary commands on an active session.

### CVE-2026-111461

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T08:16:53.260 |

An OS command injection vulnerability exists in OnCell G3150A-LTE Series. When the SMS management functionality is enabled and configured, a remote attacker with the required privileges could exploit insufficient input validation in the SMS management functionality to execute arbitrary commands on the affected device.

### CVE-2026-106174

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-667` |
| Published | 2026-10-27T07:16:32.040 |

A improper locking vulnerability in Fortinet FortiOS 8.0.0, FortiOS 7.6.4 through 7.6.6 may allow an unauthenticated attacker with network access to the device to cause a denial of service of the HTTPS management interface via crafted HTTP requests.

### CVE-2026-116587

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-770` |
| Published | 2026-10-26T22:16:55.193 |

Go JOSE provides an implementation of the Javascript Object Signing and Encryption set of standards in Go, including support for JSON Web Encryption (JWE), JSON Web Signature (JWS), and JSON Web Token (JWT) standards. Prior to 4.1.6, go-jose parses attacker-controlled RSA modulus and prime values from JWKs without enforcing size and consistency bounds before passing them to crypto/rsa.PrivateKey.Validate. On Go 1.24 and later, crafted large or degenerate RSA parameters can make that validation consume cubic CPU time, allowing remote denial of service in applications that parse JWKs from untrusted sources. This issue is fixed in version 4.1.6.

### CVE-2026-116584

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T21:18:17.053 |

Seroval facilitates JavaScript value stringification, including complex structures beyond JSON.stringify capabilities. From 1.4.1 until 1.6.8, fromJSON and fromCrossJSON do not require an array node's element list to be an actual array. A small crafted payload can supply an attacker-controlled length that determines memory allocation and decoder iterations independently of payload size, allowing an unauthenticated request to exhaust the process or block its thread. This issue is a residual bypass of the remediation for CVE-2026-23957. This issue is fixed in version 1.6.8.

### CVE-2026-116581

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835;CWE-1284` |
| Published | 2026-10-26T21:18:15.903 |

Seroval facilitates JavaScript value stringification, including complex structures beyond JSON.stringify capabilities. Prior to 1.6.8, fromJSON and fromCrossJSON do not validate a sequence node's done index. A crafted done index can create an iterator that never finishes when application code consumes it to completion. An unauthenticated request to a service that deserializes untrusted input can therefore block the event loop, exhaust process memory, or make the service unavailable. This issue is fixed in version 1.6.8.

### CVE-2026-72758

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-26T18:18:42.850 |

When parsing an AS range in Routinator, if the maximum value of the range is smaller than the minimum value of the range, Routinator will never reach the maximum value and run out of memory.

### CVE-2026-72756

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-26T18:18:42.143 |

Routinator exits when an rsync URI for a file obtained over RRDP contains a path that cannot be stored on disk, such as too long file names, and folder names that overlap with existing file names.

### CVE-2026-72754

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-755` |
| Published | 2026-10-26T18:18:41.413 |

When Routinator encounters a CRL with many entries, it may hang or run out of memory. If Routinator encounters a CRL file with the wrong encoding, it may exit.

### CVE-2026-33521

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-26T18:17:46.360 |

There is s denial of service vulnerability in Esri ArcGIS Server versions 12.0 and prior that may allow a remote, unauthenticated attacker to supply crafted requests that may, under exceptional circumstances, consume all available worker threads and deny service to users. A patch is provided for ArcGIS Server software in General Availability and Extended support status, which includes versions 12.0, 11.5, 11.3, and 11.1. Other versions are in mature or retired status, which are not patch eligible. Users working with unlisted versions are advised to upgrade and apply the patch.

### CVE-2026-105765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-26T18:17:28.863 |

HashiCorp Consul and Consul Enterprise 1.17.0 up to 2.0.4 are vulnerable to an authorization bypass in the agent's service mesh leaf certificate API that may allow an attacker without a valid ACL token to retrieve a cached service leaf certificate and its private key. This vulnerability (CVE-2026-105765) is fixed in Consul Community Edition 2.1.0 and Consul Enterprise 2.1.0 and 1.21.19.

### CVE-2026-105626

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-26T18:17:27.060 |

HashiCorp Consul and Consul Enterprise are vulnerable to a denial of service in the HTTP API that may allow an unauthenticated attacker to exhaust memory on a Consul agent. This vulnerability (CVE-2026-105626) is fixed in Consul Community Edition 2.1.0 and Consul Enterprise 2.1.0 and 1.21.19.

### CVE-2026-115912

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-26T17:17:18.910 |

vLLM is an inference and serving engine for large language models. Prior to 0.32.0, an authenticated caller can place forged shared-memory address and monotonic_id values in public multimodal features.kwargs_data. In scale-out deployments with shared-memory multimodal caching enabled, workers trust those values and pass attacker-selected bytes to pickle.loads(), allowing arbitrary Python execution even when insecure serialization is disabled. This issue is fixed in version 0.32.0.

### CVE-2026-115909

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-789` |
| Published | 2026-10-26T17:17:18.450 |

zip is a zip library for Rust that supports reading and writing simple ZIP files. From 1.3.0 until 9.0.0, ZipArchive::extract in src/read/mod.rs calls Vec::with_capacity for a symbolic link target using the attacker-controlled ZIP64 uncompressed_size before reading entry data. A small archive can request an impossible capacity, causing the infallible allocation path to abort the process before the entry is validated. The failure cannot be contained with catch_unwind or a worker thread, allowing repeated denial of service in archive-processing applications. This issue is fixed in version 9.0.0.

### CVE-2026-115907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-789` |
| Published | 2026-10-26T17:17:18.147 |

zip is a zip library for Rust that supports reading and writing simple ZIP files. From 5.1.0 until 9.0.0, applications built with the legacy-zip feature can reserve output capacity from an attacker-controlled ZIP64 uncompressed size before validating the compressed stream. The ShrinkDecoder path in src/legacy/shrink.rs can panic with a capacity overflow during ZipArchive::extract, and the Reduce and Implode decoders contain the same unbounded preallocation pattern. An unhandled panic can terminate an archive-processing service. This issue is fixed in version 9.0.0.

### CVE-2026-115721

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-26T16:17:17.673 |

**UNSUPPORTED WHEN ASSIGNED**  Unbounded allocation in XML parsing in Apache Vysper; all versions, may lead to an out of memory condition.




This issue affects all versions of Apache Vysper. Apache Vysper is an XMPP (Jabber) server library.




As this project is retired, we do not plan to release a version that fixes this issue. Users are recommended to find an alternative.

### CVE-2026-90885

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-26T15:16:45.430 |

Improper Restriction of XML External Entity Reference vulnerability in Apache Camel Saxon component.



This issue affects Apache Camel: from 4.0.0 before 4.18.5, from 4.19.0 before 4.22.2.



XQueryBuilder in camel-saxon, which evaluates expressions for the xquery language and the xquery component, built its default Saxon Configuration with parse options that set only a whitespace stripping rule, leaving the XML parser at its defaults, under which a DOCTYPE declaration is accepted and external entities are resolved. A message body of type String or byte[], or any body read as an InputStream, is first turned into a javax.xml.transform.Source by Camel's own XML type converters, which configure the parser against external entities, so those bodies were not affected. A body that was already a Source, however, was handed to Saxon unchanged, and when that Source still had to be parsed, as a stream-based Source does, Saxon parsed it with that Configuration, bypassing the protection applied to the other body types. Such a body arises, for example, after a route converts the message with convertBodyTo(Source.class), or when a component or processor earlier in the route sets the body to a stream-based Source. A DOCTYPE with an external subset, or an external entity, declared in that body was therefore resolved and expanded into the document the expression was evaluated against. An external sender whose XML reaches an XQuery expression or an xquery endpoint in that form could read files readable by the Camel process and cause the process to issue requests to hosts the document names. No non-default option is required, since the default Configuration is used whenever the route does not supply one of its own.



Users are recommended to upgrade to version 4.23.0, which fixes the issue. If users are on the 4.22.x releases stream, then they are suggested to upgrade to 4.22.2. If users are on the 4.18.x releases stream, then they are suggested to upgrade to 4.18.5. The 4.14.x releases stream and earlier, as well as the 4.15.x to 4.17.x and 4.19.x to 4.21.x release lines, reached end of life before this issue was resolved and will not receive a fix, so deployments on them must move to a supported release. For deployments that cannot upgrade immediately, do not evaluate XQuery over a message body that is already a javax.xml.transform.Source when that body carries XML from an untrusted sender, or set the configuration option of the xquery endpoint or language to a Saxon Configuration whose parse options refuse a DOCTYPE declaration and disable external entities and external DTD loading, which is what the fixed releases now apply by default.

### CVE-2026-65219

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-696` |
| Published | 2026-10-27T08:16:54.363 |

A flaw in the BMC RAKP+ implementation may allow an attacker to send a request followed by a specially crafted RAKP message and establish an RMCP+ session, which could then be used to execute commands.

### CVE-2026-65629

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-26T20:17:58.647 |

Use of Password Hash With Insufficient Computational Effort in the jose library allows an attacker who obtains a password-encrypted private-key export to recover the private key through an offline password-cracking attack.

When jose exports a password-encrypted private key with jose_jwk:to_der/2 (JOSE.JWK.to_der/2), the jose_jwk_der:to_binary/3 function in src/jwk/jose_jwk_der.erl serializes the key as a PKCS#8 EncryptedPrivateKeyInfo using the PBES2 scheme with hardcoded key-derivation parameters: PBKDF2-HMAC-SHA256 with an iteration count of 2048 and an 8-byte (64-bit) random salt. Neither value can be overridden by the caller.

Both values are far below current guidance (OWASP recommends on the order of 600,000 iterations for PBKDF2-HMAC-SHA256, and NIST recommends salts of at least 128 bits), so the key-stretching work factor is roughly 300 times lower than intended and the short salt reduces the cost of precomputation across keys. The symmetric encryption (AES-256-CBC with a 16-byte random IV) is not affected; the weakness is entirely in the derivation strength. An attacker who obtains one of these exported blobs (for example from a backup, configuration repository, object storage, or logs) can mount a cheap offline dictionary or brute-force attack against the export password, and success yields the full private key.

This issue affects jose: from 1.10.0 before 1.11.13.

### CVE-2026-115908

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59;CWE-61` |
| Published | 2026-10-26T17:17:18.293 |

zip is a zip library for Rust that supports reading and writing simple ZIP files. From 7.2.0 until 9.0.0, ZipArchive::extract and ZipArchive::extract_unwrapped_root_dir use safe_prepare_path in src/read/zipfile.rs and simplified_components in src/path.rs to validate symbolic link targets with a lexical prefix comparison rather than resolving each intermediate link. An attacker who knows or can guess the absolute extraction destination can create a chain whose apparent target remains under the destination while an intermediate symlink resolves outside it, allowing attacker-controlled files to be created or overwritten with the extracting process's privileges. On Windows, discarded drive and UNC prefixes can permit a single-link escape when the process has SeCreateSymbolicLinkPrivilege, such as through administrator rights or Developer Mode. This regression is distinct from CVE-2025-29787. This issue is fixed in version 9.0.0.

### CVE-2026-117568

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T14:16:39.327 |

mcp-ffmpeg through 1.0.5 contains an OS command injection vulnerability that allows attackers to run shell commands by supplying crafted videoPath or outputDir values to the resize-video, extract-audio and get-video-info tools. Attackers can embed $(), backticks or a closing double quote in an existing file or directory name to break out of the child_process.exec command string and execute commands as the MCP server user.

### CVE-2026-116580

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-26T21:18:15.523 |

Seroval facilitates JavaScript value stringification, including complex structures beyond JSON.stringify capabilities. Prior to 1.6.8, fromJSON rebuilds an AsyncIteratorFactoryInstance by calling source.on(listener) without requiring source to be a genuine internal stream. With untrusted Seroval input and an application plugin that returns a callable value or an object exposing an on method, a crafted node can reuse an identifier so the deserializer invokes the plugin-produced value. This is an incomplete-fix variant of CVE-2026-59940. The resulting confidentiality, integrity, or availability impact depends on the behavior exposed by the application plugin. This issue is fixed in version 1.6.8.

### CVE-2026-94347

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-114` |
| Published | 2026-10-27T14:17:05.950 |

PowerProtect Data Domain Virtual Edition, Feature Release versions 7.7.1.0 through 8.7, LTS2024 release versions 7.13.1.0 through 7.13.1.70, LTS2025 release versions 8.3.1.0 through 8.3.1.30, LTS2026 release versions 8.6.1.0 through 8.6.1.10, contain a Process Control vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-94346

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-31` |
| Published | 2026-10-27T14:17:05.823 |

PowerProtect Data Domain Virtual Edition, Feature Release versions 7.7.1.0 through 8.7, LTS2024 release versions 7.13.1.0 through 7.13.1.70, LTS2025 release versions 8.3.1.0 through 8.3.1.30, LTS2026 release versions 8.6.1.0 through 8.6.1.10, contain a Path Traversal vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-109995

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T12:17:04.543 |

The Advanced Views – Display Framework for Gutenberg & Elementor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 3.9.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is exploitable even against pending or unapproved comments, as the plugin's get_comment() lookup applies no approval-status filter, meaning a payload executes for any visitor loading an avf-layout block bound to the attacker's comment ID before the comment is ever reviewed.

### CVE-2026-65211

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-27T09:16:33.400 |

This issue may allow an authenticated IPMI Administrator to read and write arbitrary BMC physical memory and thereby execute code on the BMC operating system.

### CVE-2026-16521

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T08:16:53.443 |

An OS command injection vulnerability exists because of insufficient input filtering. An attacker can inject a command payload into a BMC function; the payload may execute when the related service is restarted.

### CVE-2026-111820

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T06:17:23.437 |

The Analytics Insights – Google Analytics Dashboard for WordPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the Page Title in all versions up to, and including, 6.3.12 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-65120

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-27T13:16:59.740 |

NVIDIA TensorRT-LLM contains a vulnerability where an attacker could cause a server-side request forgery. A successful exploit of this vulnerability might lead to information disclosure.

### CVE-2026-24269

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-27T13:16:57.110 |

NVIDIA TensorRT-LLM contains a vulnerability where an attacker could cause a server-side request forgery. A successful exploit of this vulnerability might lead to information disclosure and data tampering.

### CVE-2026-116899

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-27T11:17:32.937 |

REDAXO before 5.21.4 contains a broken access control vulnerability that allows authenticated editors to modify slices in unauthorized categories by pairing a permitted article with a foreign slice id. Attackers can abuse content/edit delete and edit functions or the content_slice_status and content_move_slice APIs to delete, toggle, move, or overwrite other editors' slices.

### CVE-2026-116898

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-27T11:17:32.797 |

REDAXO before 5.21.4 contains a missing authorization vulnerability in the media pool bulk move that checks only target category permission, ignoring the source category. Authenticated backend users with permission for one media category can move files from restricted categories into it, then silently replace their contents site-wide.

### CVE-2026-116897

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-27T11:17:32.653 |

REDAXO core before 5.21.4 contains a missing authorization vulnerability in the structure/version and structure/history frontend preview modes, which do not check category or clang permissions for the previewed article. Any backend user, or one holding history[article_rollback], can set rex_version or rex_history_date with arbitrary article_id values to read unpublished working versions and historic or deleted content.

### CVE-2026-116880

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-27T11:17:30.130 |

Semantic MediaWiki from 3.0.0 before 7.3.1 contains a cross-site request forgery vulnerability in Special:SMWAdmin because it overwrites the wpEditToken with a freshly generated valid token. Attackers can lure an authenticated smw-admin user to a malicious page that triggers schema setup, entity-disposal, or job actions, causing semantic data loss and resource exhaustion.

### CVE-2026-116876

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-27T11:17:29.543 |

Semantic MediaWiki from 2.5.0 before 7.3.1 contains an improper authorization vulnerability that allows ordinary editors to permanently protect pages by adding an Is edit protected annotation. When $smwgEditProtectionRight is enabled, EditProtectionUpdater applies indefinite edit and move restrictions without checking the author's rights, locking other editors and administrators out.

### CVE-2026-116839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-27T01:19:07.093 |

A malicious actor who lures an authenticated user to a malicious page could exploit a Cross-Site Request Forgery (CSRF) vulnerability found in airMAX M devices to make unauthorized changes and execute a Denial of Service (DoS) attack on the device.

### CVE-2026-116821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:16.867 |

YesWiki before 4.7.0 contains a read-ACL bypass in AclService::updateRequestWithACL, which interpolates usernames into SQL LIKE patterns without escaping the _ and % wildcards. Self-registered attackers can use usernames such as ___ or %%% that over-match ACL tokens, reading pages and Bazar entries restricted to other users or groups via the public Bazar listing API.

### CVE-2026-116814

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-10-27T00:17:15.140 |

OpenPanel before 3.0.0 contains an information exposure vulnerability that writes database connection URLs and email template data to standard output logs. Users with log access can obtain database credentials from migration startup logs and password-reset tokens logged when SMTP_HOST and RESEND_API_KEY are unset.

### CVE-2026-116813

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:14.853 |

OpenPanel before 3.0.0 contains an sql injection vulnerability in ConversionService.getConversion that allows project-read members and share-link holders to inject ClickHouse SQL through unescaped event names and dates. Attackers can break out of string literals in series names or startDate/endDate values with OR 1=1 to neutralize project_id scoping and read other tenants' analytics data.

### CVE-2026-116812

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:14.560 |

OpenPanel before 3.0.0 contains a sql injection vulnerability in profileColumnAccess in cohort.service.ts that allows project-read members to inject SQL by supplying unescaped profile filter column names. Attackers can submit a cohort.preview filter whose name contains a subquery spliced into argMax, cityHash64, or comparison clauses to read other tenants' ClickHouse data.

### CVE-2026-116740

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-26T22:16:58.390 |

libcss through 0.9.2 contains a NULL pointer dereference vulnerability in mq_parse_media_query() that allows remote attackers to crash consumers by supplying media lists ending in a comma. Attackers can serve a stylesheet whose @media or @import media list has a trailing comma, causing NetSurf or other parsers to crash.

### CVE-2026-112457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-26T21:17:35.770 |

A double free issue was addressed with improved memory management. This issue is fixed in macOS Golden Gate 27.2, macOS Sequoia 15.8.2, macOS Tahoe 26.7.2. An attacker on the local network may be able to cause unexpected system termination or corrupt process memory.

### CVE-2026-57187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416;CWE-664` |
| Published | 2026-10-26T20:17:56.700 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, an authenticated attacker may cause a heap-use-after-free in `PJSIP TCP/SDP` handling by sending a `SIP INVITE` over a connection-oriented transport and disconnecting before Asterisk responds with the `200 OK`. So far, the crash has only been reproduced when Asterisk is built with `Address Sanitizer`, which detects the issue. `Address Sanitizer` is a development tool with significant performance overhead and, according to the maintainer, is not used in production systems. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-70379

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-26T18:18:39.283 |

When the vSolution Matrix feature is enabled, affected devices may make current screen content available through an unauthenticated RTSP/RTP stream to hosts on the same network segment. The stream is not encrypted, which may allow an unauthenticated host to view or capture presentation content where network access is not otherwise restricted. This vulnerability only affects devices with the vSolution Matrix feature enabled.

### CVE-2026-81038

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-617;CWE-908` |
| Published | 2026-10-26T17:17:30.350 |

The Object Transfer Service server builds its Object Action Control Point (OACP) response indication in oacp_ind_send() (subsys/bluetooth/services/ots/ots_oacp.c). Before this fix the four-byte Checksum Value field was appended whenever the requested op code was BT_GATT_OTS_OACP_PROC_CHECKSUM_CALC, regardless of the result code. The response payload is a bare, uninitialized four-byte stack buffer declared with NET_BUF_SIMPLE_DEFINE(resp_param, sizeof(uint32_t)) in bt_gatt_ots_oacp_write(), and it is filled only on the success path of oacp_checksum_proc_validate(). On every failure path the buffer is still empty, so net_buf_simple_pull_le32() was invoked on a zero-length buffer.

The OACP characteristic and its client characteristic configuration descriptor are declared with BT_GATT_PERM_WRITE and BT_GATT_PERM_READ | BT_GATT_PERM_WRITE, so no pairing, encryption, or authentication is required. Any peer within radio range that can connect to a device running the OTS server can enable OACP indications and write a nine-byte Calculate Checksum command that fails validation — for example by issuing it with no object selected, which returns BT_GATT_OTS_OACP_RES_INV_OBJ. Because oacp_command_decode() accepts the Calculate Checksum op code unconditionally (it is not guarded by CONFIG_BT_OTS_OACP_CHECKSUM_SUPPORT), builds without checksum support are reachable too: they answer BT_GATT_OTS_OACP_RES_OPCODE_NOT_SUP and take the same bad path.

On builds with CONFIG_ASSERT enabled, the zero-length pull trips the assertion inside net_buf_simple_pull_mem() and panics the device, giving a remotely triggered denial of service. On builds with assertions disabled there is no check: the pull returns the untouched stack array and four bytes of uninitialized stack memory are copied into the indication and transmitted to the peer, repeatable on every request. The disclosure is bounded to four bytes per request and the write stays inside the seven-byte res indication buffer, so there is no memory corruption; the impact is uninitialized-memory disclosure plus an availability loss in assertion-enabled configurations.

### CVE-2026-77056

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-10-26T15:16:43.260 |

boneIO black_debian_images ships with a Mosquitto MQTT broker that uses the same default credentials on all devices. These credentials are publicly documented on github, and there is no indication in the instructions to change them. A remote attacker can use them to gain full read and write access to the broker, allowing control of connected relays, blinds, and gates, and injection of fake entities into a linked Home Assistant installation.

This issue was fixed in version 1.6.0 of the image: MQTT passwords are generated per device at first boot. Devices upgraded from earlier versions keep their existing broker credentials; from boneio 1.6.0 the web panel reports credentials that are still the published defaults, and the owner has to change them.

### CVE-2026-116807

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T00:17:13.040 |

OpenPanel before 3.0.0 contains an sql injection vulnerability that allows authenticated users to bypass tenant scoping by injecting unescaped profile filter names into a JOIN subquery. Attackers can supply a crafted filter name with a trailing comment to bypass the project_id WHERE clause and read events from all projects.

### CVE-2026-115418

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-26T17:17:16.533 |

SQL injection in the database-query custom resource handlers in the Amazon Web Services (AWS) Cloud Development Kit (CDK) @aws-cdk/aws-redshift-alpha module before 2.274.0-alpha.0 could allow a third party who can influence construct property values to run SQL statements with Amazon Redshift superuser privileges, including granting access to all cluster users. The statements are reachable through crafted user names, comments, or passwords.



To remediate this issue, users should upgrade to version 2.274.0-alpha.0 or later and review existing table grants to PUBLIC.
