# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-19 15:02 UTC
- **対象期間**: `2026-06-18T19:00:20.000Z` 〜 `2026-06-19T15:02:33.000Z`
- **重要CVE数**: 52 件（Critical 9.0+: 19 件 / High 7.0〜: 33 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS 7.0 以上のものは **30 件以上** と非常に多く、特に **認証バイパス・特権昇格・リモートコード実行** が集中しています。  
- JetBrains Hub、Microsoft Dynamics 365、WordPress プラグイン、Microsoft 365 Copilot、Rancher Manager など、**開発・運用プラットフォームとクラウドサービス** が多数対象となっており、企業内部の開発環境だけでなく、外部向け SaaS でも深刻なリスクが顕在化しています。  
- 多くの脆弱性は **デフォルト設定のまま公開** されていることが根本原因で、**設定ミスや不要なサービスの露出** が攻撃者にとって格好の入り口となっています。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑50242** (JetBrains Hub) | 10.0 | 認証バイパス → 管理者権限取得 | JetBrains Hub は社内 SSO・権限管理の中枢。データベース直アクセスで認証を回避できるため、**全社の開発・運用アカウントが乗っ取られる危険**がある。対象バージョンは 2024.2 以降のすべて。 |
| **CVE‑2026‑47647** (Microsoft Dynamics 365) | 9.9 | 特権昇格 (ネットワーク上の認証済み攻撃者) | Dynamics 365 は営業・顧客管理の基幹システム。**認証済みユーザーが管理者権限へ昇格**できるため、機密顧客データや財務情報への不正アクセスが可能になる。 |
| **CVE‑2026‑7515** (BetterDocs Pro – WordPress) | 9.8 | ローカルファイルインクルード (LFI) | WordPress サイトで **未認証のリモートコード実行** が可能。プラグインは多数の企業サイトで利用されており、サーバー全体の乗っ取りリスクが高い。 |
| **CVE‑2026‑54130** (Microsoft 365 Copilot) | 9.8 | 認証なしで情報漏洩 | Copilot の重要機能が認証チェックを欠如しているため、**社内機密情報が外部に流出**する可能性がある。Copilot は多くの企業が業務効率化に導入中。 |
| **CVE‑2026‑44939** (Rancher Manager) | 9.4 | コマンドインジェクション → コンテナ不正実行 | Rancher は Kubernetes 管理のデファクトスタンダード。インポートエンドポイントで **任意のシェルコマンドが実行** でき、クラスタ全体が乗っ取られる危険がある。 |

> **備考**  
> - 同一製品 (JetBrains Hub) に複数の高深刻度脆弱性 (認証バイパス、特権昇格、アカウント乗っ取り) が報告されている点は特に注意が必要です。  
> - SaaS 系サービス (Dynamics 365、M365 Copilot) はベンダー側のパッチ適用が不可欠です。  

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の即時取得**：ベンダーのセキュリティアドバイザリを確認し、パッチが提供されているかを速やかにチェック。  
- **不要サービス・プラグインの無効化**：使用していない機能やプラグインは **アンインストールまたは無効化** する。  
- **ネットワーク境界の強化**：外部から直接アクセスできる管理ポート (例: 8080, 443) は **ファイアウォールで制限** し、IP アクセスリストで信頼できる管理者だけに絞る。  
- **デフォルト認証情報の変更**：全てのコンテナ・イメージ、デバイスでデフォルトユーザー/パスワードが残っていないか確認し、**即座に変更**する。  

### 3.2 製品別具体的対策  

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン / パッチ | 主な対策 |
|-------------------|----------------------|--------------------------|----------|
| **JetBrains Hub** | 2024.2‑2026.1 系列 (例: 2024.3.148430) | **2026.1.13757 以降** (公式パッチ) | - データベース直アクセスを防止するため、DB の外部公開を遮断<br>- 管理コンソールの IP 制限<br>- すべての認証トークンを再発行 |
| **Microsoft Dynamics 365** | 2025.x 系列 (全リリース) | **2026 年 1 月リリースのセキュリティ更新** | - 既存ユーザーの権限レビューと最小権限化<br>- MFA の強制適用<br>- 監査ログの有効化 |
| **BetterDocs Pro (WordPress)** | ≤ 3.8.0 | **3.8.1 以降** (プラグイン作者提供) | - `doc_style` パラメータのサニタイズが実装されたバージョンへ更新<br>- `wp-config.php` で `DISALLOW_FILE_EDIT` を true に設定 |
| **Microsoft 365 Copilot** | 2025.x‑2026.x (全リリース) | **2026 年 2 月のセキュリティパッチ** | - Copilot の API キー管理を見直し、最小権限のスコープに限定<br>- 重要情報へのアクセスは Azure AD 条件付きアクセスポリシーで保護 |
| **Rancher Manager** | < 2.14.2 | **2.14.2 以降** | - インポートエンドポイント `/v3/import/{token}_{clusterId}.yaml` の **YAML パラメータサニタイズ** が追加されたバージョンへアップグレード<br>- 重要操作は RBAC で制限し、`admin` ロールの使用を最小化 |
| **Bitnami Cassandra コンテナ** | 7.x 系列 (cassandra:latest) | **Bitnami Cassandra 7.2.0 以降** | - `CASSANDRA_USER` 環境変数で作成したスーパーユーザーに対し、デフォルト `cassandra` アカウントを **削除** するスクリプトを追加 |
| **NI grpc‑device** (2.17.0 以前) | 2.17.0 | **2.18.0 以降** | - TLS 設定が必須になるようデフォルトで `--bind-address=127.0.0.1` に変更<br>- 不要なポート公開を防止 |
| **PraisonAI** | < 1.5.115 / < 4.5.128 | **1.5.115 以降 / 4.5.128 以降** | - エージェント ID のサニタイズ実装<br>- `PRAISON_APPROVAL_MODE` のデフォルトを `manual` に

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-50242

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-19T13:16:36.987 |

In JetBrains Hub before 2026.1.13757,
2025.3.148033,
2025.2.148048,
2025.1.148120,
2024.3.148430,
2024.2.148429 authentication bypass via direct database access leading to administrative access was possible

### CVE-2026-49257

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-18T21:16:29.780 |

mcp-pinot is a Python-based Model Context Protocol (MCP) server for interacting with Apache Pinot. In versions 3.0.1 and below, mcp-pinot defaults to running an HTTP MCP server bound to 0.0.0.0:8080 with no authentication enabled. All MCP tools, including SQL query execution, schema creation, and table-config mutation, are reachable by any network-adjacent caller. The server proxies these calls using server-side Pinot credentials, producing a confused-deputy condition that yields full read/write access to the configured Pinot cluster. This issue has been fixed in version 3.1.0

### CVE-2026-56142

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-915` |
| Published | 2026-06-19T13:16:37.313 |

In JetBrains Hub before 2026.1.13757,
2025.3.148033,
2025.2.148048,
2025.1.148120,
2024.3.148430,
2024.2.148429 privilege escalation by attaching authentication details to accounts was possible

### CVE-2026-47647

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-18T22:16:31.747 |

Improper access control in Microsoft Dynamics 365 allows an authorized attacker to elevate privileges over a network.

### CVE-2026-49252

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-18T21:16:29.643 |

deepstream is a server that allows clients and backend services to sync data, send messages and make rpcs at scale. Versions prior to 10.0.5  are vulnerable to Prototype Pollution. Exploitation can lead to potential privilege escalation from any authenticated user with write permission to any record. This issue has been fixed in version 10.0.5.

### CVE-2026-56141

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-338` |
| Published | 2026-06-19T13:16:37.203 |

In JetBrains Hub before 2026.1.13757,
2025.3.148033,
2025.2.148048,
2025.1.148120,
2024.3.148430,
2024.2.148429 account takeover via predictable restore codes was possible

### CVE-2026-7515

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-19T06:17:10.430 |

The BetterDocs Pro plugin for WordPress is vulnerable to Local File Inclusion in versions up to, and including, 3.8.0 via the `doc_style` parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included.

### CVE-2026-54130

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-18T22:16:32.223 |

Missing authentication for critical function in M365 Copilot allows an unauthorized attacker to disclose information over a network.

### CVE-2026-47846

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-18T20:16:13.630 |

Bitnami Cassandra container images are affected by a retained default superuser vulnerability. When a custom administrator account is configured via the CASSANDRA_USER environment variable, the container initialization script creates the new superuser account but fails to drop the built-in cassandra account in certain scenarios. This leaves the default cassandra:cassandra superuser active as an unintended access path.

Affected versions — Container image: 4.0.x prior to 4.0.20-photon-5-r7; 4.1.x prior to 4.1.11-photon-5-r7; 5.0.x prior to 5.0.8-photon-5-r4 / 5.0.8-debian-12-r3.

### CVE-2026-12046

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-502` |
| Published | 2026-06-19T00:16:46.873 |

Two state-mutating endpoints in pgAdmin 4's SQL Editor blueprint -- DELETE /sqleditor/close/<trans_id> and POST /sqleditor/initialize/sqleditor/update_connection/<sgid>/<sid>/<did> -- were the only routes in the module missing the @pga_login_required decorator. Both reach a pickle.loads sink on session['gridData'][<trans_id>]['command_obj']: the close endpoint via close_sqleditor_session(), and update_sqleditor_connection via check_transaction_status(). In server mode these endpoints were reachable without any authenticated pgAdmin session.

The defect is a missing-authentication-on-critical-function (CWE-306) wrapper around a deserialization-of-untrusted-data sink (CWE-502). Exploiting it for remote code execution requires the attacker to also forge a server-side session file whose gridData entry contains a malicious pickle payload, which in turn requires both (a) knowledge of pgAdmin's Flask SECRET_KEY (no chain to leak it is described here -- the attacker must already possess it) and (b) write access to pgAdmin's sessions/ directory on the host. Neither precondition is granted by this defect on its own. When those preconditions are met from another channel (misconfigured deployment, prior compromise, leaked configuration), the missing auth gate is the final hop that turns an existing partial compromise into unauthenticated code execution in the pgAdmin process -- and, by extension, on the host under whatever account runs pgAdmin.

Fix is a one-line @pga_login_required decorator on each of the two endpoints, matching the convention used by every other route in the module. The is_authenticated / MFA chain now runs before the trans_id is dereferenced, so an unauthenticated request is rejected before reaching the deserialization path.

The defect is server-mode only. In DESKTOP mode pgAdmin's before_request hook re-authenticates DESKTOP_USER on every request, so no endpoint can be exercised in an unauthenticated state and no auth decorator (or its absence) is meaningful. The accompanying regression test mirrors the attacker's path -- harvests an X-pgA-CSRFToken from GET /login and replays it against both endpoints -- and self-skips outside server mode for that reason; it is wired into the existing server-mode CI workflow alongside the data-isolation tests.

This issue affects pgAdmin 4: from 6.9 before 9.16.

### CVE-2026-44939

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-06-19T13:16:30.583 |

A command injection vulnerability in the Rancher Manager cluster before 2.14.2 import endpoint  /v3/import/{token}_{clusterId}.yaml through unsanitized YAML parameters could allow remote attackers to break out of an image, and execute e.g. malicious containers.

### CVE-2026-12045

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-89` |
| Published | 2026-06-19T00:16:46.703 |

Read-only transaction bypass in the pgAdmin 4 AI Assistant allows an attacker who can influence database content that the assistant reads to execute arbitrary SQL with the privileges of the pgAdmin user's database role.

The AI Assistant's execute_sql_query tool runs LLM-generated SQL inside a BEGIN TRANSACTION READ ONLY wrapper to prevent data modification. The LLM-supplied query was forwarded to the database driver without restriction to a single statement or to read-only verbs, so a multi-statement payload beginning with COMMIT, END, ROLLBACK, or ABORT terminated the read-only transaction and ran subsequent statements in autocommit mode. The trailing ROLLBACK then had no effect.

Delivery is via prompt injection: an attacker who can write content into any object the AI Assistant may inspect (a row, a column value, a comment) can cause the LLM to emit the multi-statement payload as a tool call. With ordinary write privileges on the pgAdmin user's role the attacker can perform unauthorised data modification. When the pgAdmin user's role is a PostgreSQL superuser or holds pg_execute_server_program, the chain extends to remote code execution on the database server host via COPY ... TO PROGRAM.

Fix validates the LLM-supplied query up front: it must parse to exactly one non-empty / non-comment statement whose leading real token (after stripping whitespace, comments, and punctuation) is one of SELECT, WITH, EXPLAIN, SHOW, VALUES, or TABLE. Transaction-control verbs, DML, DDL, CALL, COPY, DO, SET/RESET, and everything else are rejected before any database work happens. PostgreSQL's READ ONLY mode continues to backstop data-modifying CTEs, EXPLAIN ANALYZE on writes, and volatile side effects.

This issue affects pgAdmin 4: from 9.13 before 9.16.

### CVE-2026-9142

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-19T14:16:24.423 |

There is an insecure default credentials vulnerability in NI grpc-device when TLS configuration is not present and the server is bound beyond loopback.  This may allow an unauthenticated user access to the server on the local network.  This affects NI grpc-device 2.17.0 and prior versions.

### CVE-2026-48137

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-822` |
| Published | 2026-06-19T14:16:22.680 |

There is an untrusted pointer dereference vulnerability in the NI grpc-device sideband streaming API that may allow an attacker to cause an arbitrary memory dereference, potentially resulting in remote code execution.  Successful exploitation requires an attacker  to supply a specially crafted Moniker protobuf message.  This affects NI grpc-device 2.17.0 and prior versions.

### CVE-2026-54414

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-434` |
| Published | 2026-06-19T06:17:09.830 |

FileRise before 3.16.0 is vulnerable to path traversal in the shared-folder upload endpoint (/api/folder/uploadToSharedFolder.php), leading to arbitrary file write and administrator account takeover. The upload filename is validated by FolderController with basename() and REGEX_FILE_NAME, which permit URL-encoded sequences (the regex blocks / and \ but not %). The raw filename is then passed to UploadModel::handleUpload, where it is reconstructed as trim(urldecode(basename($fileName))), re-introducing path separators after validation (e.g. ..%2fusers%2fusers.txt becomes ../users/users.txt). UploadNamePolicy::isAllowedForWrite() applies basename() internally and therefore only evaluates the final component (users.txt), allowing the traversal sequence to pass the extension policy. The destination path is then used directly in move_uploaded_file() with no realpath containment check, allowing a write outside the intended upload directory. An attacker who possesses a valid, non-expired, upload-enabled shared-folder link/token (which are designed to be shared publicly) can overwrite users/users.txt to create an administrator account, resulting in unauthenticated admin takeover and, depending on configuration, remote code execution. Exploitation requires possession of a valid, non-expired, upload-enabled shared-folder link/token. This issue is fixed in 3.16.0, which URL-decodes before validation and rejects any path separators in the upload filename.

### CVE-2026-40624

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-06-19T00:16:47.693 |

Improper input validation in AVer PTC500S, PTC115, PTC500+, and PTC115+ 
cameras may allow a remote, unauthenticated attacker to achieve 
arbitrary code execution via a specially crafted web request.

### CVE-2026-12048

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-06-19T00:16:47.200 |

Stored cross-site scripting in pgAdmin 4's error-rendering and plan-node-rendering paths. Text returned by a PostgreSQL server (ErrorResponse messages, including object names quoted back inside relation-does-not-exist errors and inside EXPLAIN Recheck Cond / Exact Heap Blocks fields) was passed verbatim through html-react-parser at every user-facing sink — the notifier toasts, FormFooterMessage / FormInput help and error areas, FormNote, ModalProvider AlertContent and confirmDelete, ToolErrorView, the Explain visualiser's NodeText panel, the SQL editor confirm dialogs, ConfirmSaveContent, PreferencesHelper modal alerts, and SelectThemes helper text. A PostgreSQL server an attacker controls — or any server returning attacker-influenced text such as a table or column name a low-privilege database user can create — could inject arbitrary HTML (including <iframe>) into the pgAdmin DOM the moment the victim's pgAdmin connected to that server or viewed an Explain plan that referenced the crafted object.

The injected iframe's srcdoc could fetch attacker-served JavaScript and, by writing to parent.location, redirect the victim's top-level pgAdmin browser tab to an attacker-controlled URL. Because the injection originates from inside pgAdmin's own interface, standard anti-clickjacking controls (X-Frame-Options, Content-Security-Policy: frame-ancestors) do not mitigate it. A phishing page rendered inside the legitimate pgAdmin window is indistinguishable from a genuine pgAdmin dialog.

Fix combines three complementary layers. (1) DOMPurify sanitisation is wrapped around every html-react-parser call site reachable from notifier, alert, form-error, Explain, and SQL-editor flows. (2) A new plain-text rendering contract — SafeMessage / SafeHtmlMessage components plus Notifier.errorText / alertText / warningText / infoText / successText helpers — is introduced; around fifty callers across browser, tools, dashboard, debugger, misc, llm, preferences, schema diff, and the SQL editor that previously interpolated backend-derived strings are migrated to the plain-text variants. (3) Backend HTML-escape is applied at the post-connection-SQL handler (execute_post_connection_sql) via a new sanitize_external_text helper, so third-party JSON consumers (audit logs, API clients) never receive raw markup either; the Explain plan-info renderer is also patched to _.escape Recheck Cond and Exact Heap Blocks at construction (matching every sibling field), giving defence in depth even before DOMPurify runs.

This issue affects pgAdmin 4: from 6.0 before 9.16.

### CVE-2026-8713

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-19T06:17:10.917 |

The Avada (Fusion) Builder plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the maybe_delete_files function in all versions up to, and including, 3.15.3. This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The attack requires a published Avada form configured to save entries to the database; an unauthenticated attacker submits a path-traversal payload via the wp_ajax_nopriv_fusion_form_submit_ajax handler while also controlling the fusion_privacy_expiration_interval and privacy_expiration_action fields to force an immediate 'delete' cleanup, causing the planted entry to be automatically processed by the Fusion_Form_DB_Privacy shutdown-hook routine without any administrator interaction.

### CVE-2026-49454

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-347` |
| Published | 2026-06-18T21:16:29.920 |

Relyra is a strict-by-default SAML 2.0 Service Provider library for Elixir and Phoenix. Versions 1.0.0 and 1.1.0 accept forged SAML signatures because SignatureValue was not cryptographically verified before the library returned a successful authentication result. The XMLDSig trust boundary was incomplete as :public_key.verify over the exclusive-C14N canonicalized SignedInfo was not performed against the configured IdP certificate's public key, DigestValue was not recomputed over the canonicalized referenced element, and canonicalize/2 remained an unused passthrough in the signature-verification path. The result was a structure-only acceptance path where document shape and trust-source rejection could succeed without proving the signature bytes. A forged SignatureValue carrying an attacker-controlled NameID could be accepted as {:ok}. This issue has been fixed in version 1.2.0.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-49357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-06-19T14:16:23.667 |

Line Desktop MCP is a project that, while unaffiliated with the official line-bot-mcp-server, allows users to directly operate the LINE Desktop application on Windows or Mac via MCP. `line-desktop-mcp` supports a `--http-mode` Streamable HTTP transport for use with clients such as n8n. In this mode the server binds to `0.0.0.0` and exposes the MCP `/mcp` endpoint without an MCP-layer authentication check. Prior to version 1.1.2, any network client that can reach the port can initialize a session, list tools, and call tools that read LINE Desktop chat history or send LINE messages through the already logged-in desktop application. Version 1.1.2 fixes the issue.

### CVE-2026-4026

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-19T14:16:24.037 |

A security vulnerability has been identified in FlexNet Manager Suite 2025 R1 that could allow an authenticated user with read-only access to account settings to escalate their privileges to Administrator level.

### CVE-2026-48139

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-19T14:16:22.937 |

There is a NULL pointer dereference vulnerability in NI grpc-device in the data moniker service that may allow an attacker to cause a denial of service by triggering a crash.  Successful exploitation requires an attacker to provide an unknown value to the data moniker service. This affects NI grpc-device 2.17.0 and prior versions.

### CVE-2026-48138

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-19T14:16:22.817 |

There is an out-of-bounds read vulnerability in the NI grpc-device streaming API due to a missing bounds check that may result in a denial of service. Successful exploitation requires an attacker to supply a specially crafted write request. This affects NI grpc-device 2.17.0 and prior versions.

### CVE-2026-8806

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-440` |
| Published | 2026-06-19T03:16:15.010 |

Expected Behavior Violation vulnerability in Mitsubishi Electric MELSEC iQ-F Series FX5-ENET/IP Ethernet Module FX5-ENET/IP all versions allows a remote attacker to cause a denial-of-service (DoS) condition in the affected product by continuously sending a large number of communication packets to the Ethernet port of the product in a short period of time, increasing the processing load of the product, preventing the internal anomaly-detection processing from being performed, and causing the communication function to stop.

### CVE-2026-8805

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-06-19T03:16:14.850 |

Integer Overflow or Wraparound vulnerability in the EtherNet/IP function of Mitsubishi Electric MELSEC iQ-F Series FX5-EIP EtherNet/IP module FX5-EIP versions 1.000 and prior allows a remote attacker to cause a denial-of-service (DoS) condition in the affected product by rapidly establishing a large number of TCP connections to it, resulting in an inconsistency in the product's internal connection management process and triggering improper memory access.

### CVE-2026-12044

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-116` |
| Published | 2026-06-19T00:16:46.053 |

SQL injection in pgAdmin 4 across every dialog template that renders ``COMMENT ON ... IS '<description>'`` for a user-supplied description field. The Jinja templates for Domains (and their constraints), Foreign Tables, Languages, and Event Triggers, plus the Views OID-lookup query, interpolated the description directly inside a single-quoted SQL literal -- ``'{{ data.description }}'`` -- instead of passing it through the ``qtLiteral`` escape filter. An authenticated pgAdmin user with permission to create or alter the affected object types could submit a description containing an apostrophe, break out of the literal and chain arbitrary SQL. The injected SQL runs under the PostgreSQL role the user is already authenticated as; for a connected role with ``COPY ... TO/FROM PROGRAM`` (typically PostgreSQL superuser), this chains to OS command execution on the PostgreSQL host. The defect does not cross a privilege boundary -- the user already has direct SQL access to that role through pgAdmin's Query Tool -- so the attacker gains no capability beyond what their database role already grants. The marginal impact captures bypass of any application-layer Query Tool gating an operator may have configured.

The defect was originally reported against the Domain Dialog ``description`` field; a code-wide audit identified sixteen sites of the same pattern across the templates listed above. The same review also surfaced ten related sinks in the pgstattuple/pgstatindex stats templates -- ``pgstattuple('{{schema}}.{{table}}')`` and the matching pgstatindex shape -- where ``qtIdent`` escapes embedded double quotes inside the identifier but not apostrophes, so a user with CREATE privilege on a schema could plant a table or index named ``foo'bar`` and a later stats viewer would render an unbalanced literal.

Fix is layered:

  1. Sites: replace every ``'{{ x.description }}'`` with ``{{ x.description|qtLiteral(conn) }}`` (no surrounding quotes -- the filter wraps the value in escaped quotes itself). Plumb ``conn=self.conn`` through every ``render_template`` call that loads one of these templates. Also corrects a ``{ % elif`` Jinja typo in the foreign-table schema diff (dead branch). Rewrite the ten pgstattuple/pgstatindex stats sites to address the relation via OID + ``::oid::regclass`` cast (e.g. ``pgstattuple({{ tid }}::oid::regclass)``), eliminating the embedded literal-call form entirely so that bug-class can no longer recur there.

  2. Driver hardening: ``qtLiteral`` (in ``utils/driver/psycopg3/__init__.py``) used to silently return the raw unescaped value when its ``conn`` argument was falsy. It now raises ``ValueError`` -- surfacing the entire bug class going forward. The change immediately uncovered eight latent plumbing bugs (in ``schemas/__init__.py``, ``schemas/functions/__init__.py``, ``schemas/tables/utils.py``, ``foreign_servers/__init__.py``, and seven sites in ``roles/__init__.py``) -- all fixed as part of this patch. The inner ``except`` block that swallowed adapter-level failures and returned the raw value is also removed, so unadaptable inputs raise instead of leaking unescaped values.

  3. Regression tests: a per-template behavioural test renders each previously-vulnerable template with an apostrophe-injection payload and asserts the escaped fragment is present and the vulnerable fragment absent; a lint test walks every ``*.sql`` template flagging any ``'{{ ... }}'`` single-quote-wrapped interpolation against an explicit allowlist; unit tests cover the new qtLiteral fail-fast and inner-except raise paths.

This issue affects pgAdmin 4: from 1.0 before 9.16.

### CVE-2026-56078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-18T23:16:19.760 |

PraisonAI before 1.5.115 contains a path traversal vulnerability in MultiAgentMonitor that fails to sanitize agent IDs when building file paths. Attackers can include traversal sequences like ../ in agent IDs to read, write, or overwrite arbitrary files, enabling sensitive disclosure, denial of service, or code execution.

### CVE-2026-56075

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-18T23:16:19.357 |

PraisonAI before 4.5.128 contains an arbitrary shell command execution vulnerability where the UI modules hardcode approval_mode to auto, overriding administrator configuration from PRAISON_APPROVAL_MODE environment variable. Authenticated attackers can instruct the LLM agent to execute arbitrary shell commands via subprocess.run with shell=True, bypassing the manual approval gate and insufficient command sanitization blocklists.

### CVE-2026-48716

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-18T20:16:13.850 |

nanobot is a personal AI assistant. In versions 0.1.5.post3 and prior, the WhatsApp bridge in bridge/src/whatsapp.ts constructs a filesystem path using the fileName field from an incoming WhatsApp document message without sanitization. The WhatsApp bridge downloads media attachments and writes them to disk using a filename derived from the sender's message via documentMessage.fileName, which is concatenated with a prefix and its raw value is passed directly to path.join(mediaDir, outFilename). Node.js path.join resolves .. components, allowing an attacker to escape the intended media/ directory by sending a document with a crafted fileName such as ../../../.ssh/authorized_keys. Because the attacker also controls the file content (the downloaded buffer), this is a write-anywhere primitive — both path and content are attacker-controlled. A fix for this issue is planned for version 0.1.5.post4.

### CVE-2026-12104

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:L/U:Amber` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-19T14:16:21.687 |

OS command injection in the environment and tunnel configuration functionality in SIMA GmbH Bondix through version 1.25.7.5 on Linux allows an authenticated attacker with configuration write access to execute arbitrary operating-system commands via crafted configuration values passed to server-side scripts.

### CVE-2025-7737

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-06-19T06:16:58.920 |

DoS Vulnerability in 10G iSCSI Interface of Hitachi Virtual Storage Platform.



This issue affects Hitachi Virtual Storage Platform E990, E1090, E1090H: before DKCMAIN Ver.93-07-21-80/00-05, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-07-01-80/00-07, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-06-82-80/00-06, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-06-63-80/00-04, CHB(iSCSI) Ver.88-01-02-04; Hitachi Virtual Storage Platform E390, E590, E790, E390H, E590H, E790H: before DKCMAIN Ver.93-07-21-x0/00-05, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-07-01-x0/00-07, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-06-82-x0/00-06, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-06-63-x0/00-04, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-07-24-x0/00-02, CHB(iSCSI) Ver.88-01-02-04, before DKCMAIN Ver.93-07-02-x0/00-02, CHB(iSCSI) Ver.88-01-02-04; Hitachi Virtual Storage Platform G130, G150, G350, G370, G700, G900, F350, F370, F700, F900: before DKCMAIN Ver.88-08-10-x0/00-05, CHB(iSCSI) Ver.88-01-02-04; Hitachi Virtual Storage Platform G100, G200, G400, G600, G800, F400, F600, F800: before DKCMAIN Ver.83-06-20-x0/00-05, CHB(iSCSI) Ver.83-01-01-29; Hitachi Virtual Storage Platform VX8, 5100, 5500, 5100H, 5500H, 5200, 5600, 5200H, 5600H: before DKCMAIN Ver.90-09-01-00/01-01, CHB(iSCSI) Ver.90-01-01-07, before DKCMAIN Ver.90-08-83-00/01-01, CHB(iSCSI) Ver.90-01-01-07, before DKCMAIN Ver.90-08-63-00/01-01, CHB(iSCSI) Ver.90-01-01-07; Hitachi Virtual Storage Platform VX7, G1000, G1500, F1500: before DKCMAIN Ver.80-06-93-00/00-04, ISFC Ver.80-01-17.

### CVE-2026-56076

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-06-18T23:16:19.490 |

PraisonAI before 1.5.128 contains a cross-origin agent execution vulnerability in the AGUI endpoint that allows remote attackers to trigger arbitrary agent execution. The POST /agui endpoint lacks authentication and hardcodes Access-Control-Allow-Origin: * headers, combined with Starlette's Content-Type-agnostic JSON parsing, enabling attackers to bypass CORS preflight checks via simple requests and exfiltrate sensitive agent responses including tool execution results and environment data.

### CVE-2026-8100

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:X/V:X/RE:M/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-06-18T22:16:32.353 |

Impact

A security issue has been identified in Chef 360 that could allow unauthorized access to protected API endpoints under specific conditions. This issue is due to improper handling of URL-encoded paths during request processing. In certain scenarios, an authenticated request may bypass standard access controls gaining additional privileges, potentially allowing access to API endpoints that are intended to be restricted to higher-permissioned roles. The impact is limited to environments where the affected request patterns can be triggered and depends on specific deployment configuration and access controls in place.
Resolution
The issue has been addressed through product updates that improve request validation and enforce strict path normalization before authorization checks.  Customers are advised to update to the latest available version containing the fix, version 1.7.1 or later.

### CVE-2026-25865

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-428` |
| Published | 2026-06-18T20:16:12.923 |

Punto Switcher through 4.5.0.583 contains an unquoted search path element vulnerability that allows local attackers to execute arbitrary code by exploiting the application's call to WinExec without a fully qualified path for RunDll32.exe when invoking shell32.dll Control_RunDLL input.dll. Attackers can place a malicious executable earlier in the search order to achieve arbitrary code execution in the context of the affected user.

### CVE-2026-12390

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-06-18T19:16:22.130 |

In AzeoTech DAQFactory versions 21.1 and prior, a Type Confusion vulnerability can be exploited by an attacker using specially crafted .ctl files which can result in code execution.

### CVE-2026-49248

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-06-18T21:16:29.500 |

OneDev is a Git server with CI/CD, kanban, and packages. In versions 15.0.6 and below, TarUtils.untar() creates symbolic links verbatim from TAR entry getLinkName() without validating whether the target is an absolute path. A subsequent file entry in the same archive traverses the symlink, writing to arbitrary server-side locations. This is exploitable by any authenticated user with CI Job write access — no admin interaction required. This is an incomplete fix bypass of CVE-2021-21251 (GHSA-2w6j-wc8c-9mq2): that patch blocked .. path segments but did not address absolute symlink targets. This issue has been fixed in version 15.0.7.

### CVE-2026-45696

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-06-18T21:16:28.917 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. In versions 3.4.0 through 3.4.11, the HTJ2K (High-Throughput JPEG 2000) decoder, ht_undo_impl() in OpenEXRCore is vulnerable to a heap-buffer-overflow READ. The  ht_undo_imp function copies decoded pixels out of a per-line OpenJPH buffer using the EXR channel's declared width as the iteration count. The codestream embedded in the EXR chunk can declare different (smaller) tile/line dimensions than the EXR header advertises, but ht_undo_impl() does not validate this — it pulls width 32-bit samples from cur_line->i32[] without checking the OpenJPH line buffer's actual length. A crafted EXR file produces a 4-byte heap-buffer-overflow READ immediately after a buffer allocated by ojph::local::codestream::finalize_alloc(). The bug is reachable through the standard scanline-decode entry point used by every consumer of exr_decoding_run/Imf::checkOpenEXRFile, including thumbnailers, asset pipelines, and the exrcheck utility — i.e. any application that opens untrusted EXR files. The result is a deterministic crash (DoS) and potential adjacent-heap leak. This issue has been fixed in version 3.4.12.

### CVE-2025-15661

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-18T21:16:27.143 |

libssh2 through 1.11.1, fixed in commit 2dae302, contains an out-of-bounds heap read vulnerability in the sftp_symlink() function in src/sftp.c that allows a malicious SSH server or man-in-the-middle attacker to disclose heap memory contents or cause a crash by sending a crafted SSH_FXP_NAME response. Attackers can supply a link_len value larger than the actual packet data in SSH_FXP_NAME responses for SFTP READLINK and REALPATH operations, triggering a heap buffer over-read of up to target_len minus one bytes due to the missing validation of available packet buffer size before the memcpy operation.

### CVE-2026-43994

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-18T21:16:28.630 |

Coturn is a free open source implementation of TURN and STUN Server. Versions prior to 4.10.0 contain a stack buffer overflow in decode_oauth_token_gcm(). A uint16_t nonce_len field read from an attacker-supplied OAuth access token (0-65535) is passed directly to memcpy() as the copy length into a 256-byte stack buffer (oauth_encrypted_block.nonce[256]) without bounds checking. The overflow occurs before AES-GCM authentication is verified, the attacker does not need to know the OAuth key or produce a valid AES-GCM token. Up to 735 bytes of attacker-controlled data are written past the buffer, may corrupt adjacent stack data, including control-flow data depending on compiler, ABI, and mitigations. Requires --oauth mode (non-default). This may provide a plausible RCE primitive depending on exploit mitigations; because coturn is widely deployed for WebRTC TURN/STUN and --oauth is commonly recommended, impact can be broad. This issue has been fixed in version 4.10.0.

### CVE-2026-46461

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-19T08:16:16.840 |

Dell Server Hardware Manager, versions prior to 3.2.2, contains an Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-54017

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-918` |
| Published | 2026-06-18T22:16:32.080 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, the terminal-server reverse proxy in `backend/open_webui/routers/terminals.py` does not fully confine the user-controlled `path` segment before forwarding it to an admin-configured terminal server. An authenticated user who has been granted access to a terminal server can craft `path` values containing encoded `../` traversal sequences that escape the intended path (or policy) scope on that server, reaching unintended endpoints and files on the terminal-server host. Where the terminal server fans requests out to internal services, this also gives SSRF-style reach into those services. This is a separate code path from the `/api/v1/retrieval/process/web` SSRF (GHSA-c6xv-rcvw-v685), with its own input. Two distinct vectors are consolidated here: first, raw path forwarding / single-encoded traversal (original report); and second, a bypass of the subsequently-added `_sanitize_proxy_path` mitigation using double-encoded dots (`%252e%252e`). The attacker-controlled input is the request `path`, supplied by the non-admin user, not anything an administrator configures, so this is not an admin-trust / Rule-9 situation. Version 0.9.6 fixes the issue.

### CVE-2026-32174

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-06-18T22:16:30.290 |

Improper authentication in Azure Bot Service allows an authorized attacker to elevate privileges over a network.

### CVE-2026-46699

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-18T21:16:29.053 |

conda-smithy is a tool for combining a conda recipe with configurations to build using freely hosted CI services into a single repository. Prior to version 3.61.0, a vulnerability in the conda-forge automated webservices allowed unintended write access to feedstock repositories through GitHub username takeover. The root cause is the use of mutable GitHub usernames as identifiers for repository invitation routing, rather than stable, immutable GitHub user IDs. Version 3.61.0 fixes the issue.

### CVE-2026-11576

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415;CWE-459;CWE-908` |
| Published | 2026-06-19T10:16:09.743 |

The security fix for CVE-2025-0728 in eclipse-threadx NetX Duo refactors error handling in the HTTP server PUT process to use a shared cleanup label, but this unified cleanup path unconditionally calls fx_file_close() even when the file was never successfully opened. Multiple error branches jump to the shared cleanup label before any file open operation has occurred, causing fx_file_close() to operate on an uninitialized file handle, leading to undefined behavior, double-close issues, or memory corruption.

### CVE-2026-47633

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-18T22:16:31.613 |

Exposure of sensitive information to an unauthorized actor in Cost Management Interactive Experiences allows an unauthorized attacker to disclose information over a network.

### CVE-2026-4027

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-06-19T14:16:24.157 |

A security vulnerability has been identified in FlexNet Manager Suite 2025 R1 and R2 that could allow unauthorized access to attachment files due to insufficient access control.

### CVE-2026-48140

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-704` |
| Published | 2026-06-19T14:16:23.063 |

There is an unchecked enum cast vulnerability in NI grpc-device BeginSidebandStream that may allow an attacker to trigger invalid enum states and undefined behavior, potentially resulting in a denial of service. Successful exploitation requires an attacker to supply a specially crafted message containing an out-of-range value. This affects NI grpc-device 2.17.0 and prior versions.

### CVE-2026-53915

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-73` |
| Published | 2026-06-19T13:16:37.100 |

In JetBrains GoLand before 2026.1.3 remote code execution was possible via untrusted project configuration

### CVE-2026-52866

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-19T00:16:48.123 |

An attacker within BLE communication range can monopolize the device's 
only available BLE connection slot, preventing legitimate users or 
applications from establishing a connection.

### CVE-2026-50034

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-06-19T00:16:47.980 |

An attacker within BLE communication range can passively intercept 
wireless traffic and obtain sensitive health-related information, 
including glucose measurement values.

### CVE-2026-56077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-668` |
| Published | 2026-06-18T23:16:19.623 |

PraisonAI before 1.5.115 contains an information disclosure vulnerability in the MultiAgentLedger component that allows attackers to access sensitive data by registering agents with duplicate IDs. Attackers can exploit the lack of agent ID uniqueness enforcement to share ledger instances and expose system prompts and conversation history between agents.

### CVE-2026-39999

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-06-19T14:16:21.950 |

Authentication Bypass by Spoofing vulnerability in Apache APISIX.

The attacker can completely bypass authentication capitalising on certain configurations of jwt-auth plugin.
This issue affects Apache APISIX: from v2.2 through v3.16.0.

Users are recommended to upgrade to version v3.17.0, which fixes the issue.
