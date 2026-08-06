# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-06 15:01 UTC
- **対象期間**: `2026-08-05T15:00:32.000Z` 〜 `2026-08-06T15:01:39.000Z`
- **重要CVE数**: 122 件（Critical 9.0+: 25 件 / High 7.0〜: 97 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **認証・権限管理の不備**（JWT アルゴリズム混在、トークン横取り、特権昇格）や **コード実行につながる入力検証欠如**（コマンドインジェクション、SQL/ヒープバッファオーバーフロー）に集中しています。  
- CVSS 7.0 以上の脆弱性は **ネットワークから直接攻撃可能 (AV:N)** で、特権が **完全に奪取 (C:H/I:H/A:H)** されるケースが多数。  
- ベンダー別に見ると、**Progress MarkLogic、Cisco、IBM Langflow、WSO2、PraisonAI** が複数件の高リスク脆弱性を抱えており、共通して **パッチ適用が遅延しやすい** ことが懸念材料です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ |
|-----|------|------------|------------------------|
| **CVE‑2026‑5430** | 10.0 | JWT 認証で許可外アルゴリズムが受け入れられる（アルゴリズム混在） | 攻撃者は任意の署名アルゴリズムでトークンを生成でき、認証バイパス → 任意ユーザーとしてシステムにログイン。認証サーバ全体が危殆化。 |
| **CVE‑2026‑48168** | 10.0 | PraisonAI の GitHub Actions ワークフローでブランチ名を直接 Bash に埋め込むコマンドインジェクション | 攻撃者がプルリクエストを作成し、任意のシェルコマンドを実行可能。CI/CD パイプラインが乗っ取り対象となり、コード・シークレット漏洩やインフラ破壊が起こり得る。 |
| **CVE‑2026‑9193** (MarkLogic) | 9.9 | Hadoop 統合で低権限ロールから特権操作が可能な権限昇格 | 認証済みの低権限ユーザーが Security DB に対して管理者権限でクエリを実行でき、データベース全体の改ざん・情報漏洩が発生。 |
| **CVE‑2026‑1728** (WSO2) | 9.8 | 低権限トークンが Admin REST API にアクセスできる設計ミス | 攻撃者は通常ユーザーのトークンだけで管理者 API を呼び出し、設定変更や機密情報取得が可能。WSO2 API Manager / Identity Server 系列全体に波及。 |
| **CVE‑2026‑67873** (lib60870‑C) | 9.8 | FileSegment_encode のバッファ長チェック不備によるヒープオーバーフロー | 悪意ある IEC 60870‑5‑104 クライアントからサーバ側で任意コード実行が可能。産業制御システム (SCADA) 環境での深刻な影響が懸念される。 |

> **選定理由**  
> - **CVSS が 10.0** の 2 件は認証バイパス／コード実行という最上位リスク。  
> - **MarkLogic と WSO2** は企業向け基幹システムで広く採用されており、特権昇格が直接的にデータベースや管理 API の完全取得につながる。  
> - **lib60870‑C** は産業制御向けプロトコル実装で、攻撃が物理設備に波及する可能性があるため、インフラ運用者は特に注意が必要。  

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **脆弱性情報の取得とパッチ適用を即時実施**  
  - ベンダーが提供する **セキュリティパッチ**（または「最新安定版」）をすべての環境に展開。  
- **影響システムのネットワーク分離**  
  - 外部から直接アクセスできるサービスは **ファイアウォールで制限**（IP ホワイトリスト、VPN 経由のみ）し、攻撃面を縮小。  
- **認証トークン・鍵のローテーション**  
  - JWT 鍵、WSO2 のアクセストークン、MarkLogic の内部認証キーは **即時再生成** し、過去のトークンは無効化。  
- **監査ログの強化**  
  - 認証失敗、特権操作、CI/CD ジョブ実行の **詳細ログ** を有効化し、SIEM へリアルタイム転送。  

### 3.2 個別 CVE に対する具体的対策  

| CVE | 推奨パッケージ / バージョン | 具体的作業 |
|-----|---------------------------|------------|
| **CVE‑2026‑5430** (JWT) | すべての JWT ライブラリ（例: `jsonwebtoken`、`java-jwt`）を **最新版 (≥ 9.0.0)** に更新 | - アルゴリズムホワイトリストを明示的に設定 (`alg` = `HS256` など) <br> - 不要な `none` アルゴリズムや `RS256` 以外の受け入れを禁止 |
| **CVE‑2026‑48168** (PraisonAI) | PraisonAI 4.6.40 以降 | - GitHub Actions ワークフローで **ブランチ名をシェルクオート** (`"${{ github.ref }}"`) する <br> - 外部からの PR ビルドは **安全なサンドボックス** (e.g., `pull_request_target` → `pull_request` の使用) |
| **CVE‑2026‑9193** (MarkLogic) | MarkLogic Server **12.0.3** 以上、または **11.3.6** 以上 | - Hadoop 連携設定を見直し、ロールマッピングを最小権限に制限 <br> - 既存トークンを全て失効し、再発行 |
| **CVE‑2026‑1728** (WSO2) | WSO2 **7.0.0** 以降（またはベンダーが提供するパッチ） | - `admin` スコープへのアクセスを **トークン属性で厳格に制御** <br> - API Manager の **OAuth2 スコープポリシー** を更新し、低権限ユーザーの `admin` エンドポイント呼び出しをブロック |
| **CVE‑2026‑67873** (lib60870‑C) | lib60870‑C **2.4.1** 以降 | - ライブラリを最新版にビルドし直す <br> - IEC 60870‑5‑104 の **受信バッファサイズ** を適切に設定し、過大な `FileSegment` を拒否 |
| **CVE

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-5430

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-06T08:16:33.240 |

The JWT authentication mechanism accepts tokens signed with algorithms other than those explicitly configured or supported. This allows an attacker to craft a JWT with an unsupported algorithm, which is then incorrectly validated, leading to unauthorized access.

Successful exploitation of this vulnerability may result in unauthorized access to the system, including the potential compromise of administrative accounts and full account takeover. The CVSS score is adjusted to 9.8 (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H) in single-tenant deployments, reflecting that the impact is contained within a single security authority boundary.

### CVE-2026-48168

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T19:17:31.070 |

PraisonAI is a multi-agent teams system. In versions prior to 4.6.40, the bundled Claude GitHub Actions workflow is vulnerable to command injection because it embeds an attacker-controlled pull request branch name into a Bash run: block without quoting or validation. Additionally, the workflow allows any @claude comment to trigger the job regardless of whether the commenter is a trusted collaborator. An outside contributor can open a pull request from a fork whose branch name contains shell metacharacters and comment @claude, causing Bash to execute arbitrary shell code in the GitHub Actions runner. Because these commands run in a job holding a GitHub App token with write permissions, OIDC access, and gh/git access, the injection can be chained through $GITHUB_PATH to compromise later privileged steps, enabling repository writes, pull request and issue manipulation, or OIDC-token abuse. This issue has been fixed in version 4.6.40.

### CVE-2026-20304

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-05T17:16:50.890 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Catalyst SD-WAN engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20304 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) CWE-284.

### CVE-2026-20303

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-05T17:16:50.513 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Catalyst SD-WAN engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20303 are related to improper input validation issues that are grouped under the Common Weakness Enumeration (CWE) CWE-20.

### CVE-2026-9193

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-05T16:17:10.183 |

An improper privilege management vulnerability in the Hadoop integration of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an authenticated user with a low-privileged Hadoop role to escalate privileges and execute privileged operations against the Security database.

### CVE-2026-8709

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-05T16:17:09.820 |

An improper privilege management vulnerability in the REST API document patch operation of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an authenticated user with a low-privileged REST role to escalate privileges and execute privileged operations against the Security database.

### CVE-2026-7329

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-05T16:17:09.200 |

An improper privilege management vulnerability in the SQL, SPARQL, and Optic REST query interfaces of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an authenticated user with a low-privileged REST role to escalate privileges to administrator. This enables execution of privileged operations and unauthorized data access.

### CVE-2026-5134

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-06T14:16:36.840 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Loca Software Informatics Technology Ltd. Co. CMS allows SQL Injection.

This issue affects CMS: through 06082026. NOTE: The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-1728

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-06T08:16:31.423 |

Tokens issued to a low-privileged user are not sufficiently restricted, allowing them to be used to access product-level Admin REST APIs.

Exploitation of this vulnerability allows a low-privileged user to invoke the Admin REST APIs of WSO2 products, potentially leading to full administrative account takeover. This requires the attacker to already possess a low-privileged user account and be able to obtain a valid token for it.

### CVE-2026-67873

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-06T00:16:54.380 |

A heap-based buffer overflow exists in lib60870-C 2.4.0 in the server-side FileSegment ASDU encoding path. The issue occurs because FileSegment_encode() validates only the standalone segment length via FileSegment_GetMaxDataSize() and does not verify the residual capacity of the current ASDU frame before encoding object fields and segment data

### CVE-2026-52466

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-06T00:16:53.593 |

Open Library Foundation VuFind v11.0.3 and v4.1 is vulnerable to toInorrect Access Control. The application fails to stop processing an incoming request in VuFind\Controller\AbstractBase::validateAccessPermission after it has found that controller level access permissions do not allow access to the requested function. The requester receives a response indicating that access was denied, but the actual function is executed regardless of that.

### CVE-2026-20272

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-05T17:16:49.053 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20272 are related to issues with improper neutralization of special elements that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-74.

### CVE-2026-9192

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-05T16:17:10.063 |

An authentication bypass vulnerability in the ODBC App Server of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an unauthenticated remote attacker to bypass password verification and execute queries with the privileges of any named user known to the server, including administrators.

### CVE-2026-12605

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-06T14:16:20.887 |

In Eclipse GlassFish versions 8.0.x before 8.0.4, CSRF + SSRF in DownloadServlet ContentSources leaks the admin `gfresttoken` to attacker-controlled host if the victim is authenticated into the Admin Console -\> full unauthenticated takeover of Eclipse GlassFish domain until the token expires.

### CVE-2026-71319

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-306` |
| Published | 2026-08-05T22:17:08.227 |

Nuxt is an open-source web development framework for Vue.js. Prior to 3.3.1, Nuxt DevTools (development mode only) exposes a bidirectional RPC channel over the Vite HMR WebSocket via the nuxt:devtools:rpc plugin. On affected versions the channel has no authentication: any client that can reach the Vite HMR endpoint (ws://<host>:<port>/, subprotocol vite-hmr) can call RPC methods, with no token, handshake, or origin check before the channel is established. The updateOptions(), clearOptions(), and openInEditor() methods do not enforce the ensureDevAuthToken check that the other mutating methods use. openInEditor() reads the persisted behavior.openInEditor value and passes it to the launch-editor package, which spawns it as a child process. That value is settable through the equally unauthenticated updateOptions(). An attacker who can reach the HMR port can therefore chain updateOptions('behavior', { openInEditor: '<command>' }) then openInEditor('<any-existing-file>') to execute an arbitrary program on the developer's machine. This issue is fixed in 3.3.1.

### CVE-2025-15039

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-06T08:16:29.147 |

The Conditional Authentication (Adaptive Authentication) script does not correctly enforce the completion of all required authentication steps when a specific multi-step pattern involving certain authenticators is configured. This allows an attacker to bypass intermediate authentication challenges by exploiting how the script handles callbacks and re-execution of authentication steps.

Successful exploitation allows a malicious actor to gain unauthorized access to a targeted user account. This vulnerability can only be exploited when all of the following conditions are met: the application login flow contains a specific secondary authenticator, the Conditional Authentication script is configured with particular event callbacks and re-executes an authentication step, the targeted user has one of the impacted authenticators enrolled, and the attacker successfully completes any preceding authentication steps.

### CVE-2026-15587

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-05T16:16:51.147 |

Improper Privilege Management in Google SecOps (Chronicle SOAR) versions prior to 6.3.85 on Google Cloud Platform allows an authenticated attacker to escalate privileges to system-level administrative access using a crafted internal authentication header.




This vulnerability was patched with version 6.3.85, and no customer action is needed.

### CVE-2026-67531

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-06T00:16:53.733 |

FrontMCP is a TypeScript-first framework for the Model Context Protocol (MCP). Prior to 1.5.7, the sandboxed codecall:execute tool exposes live host Zod schema instances to the script via getTool(), and because Zod v4 defines _zod as a non-configurable, non-writable own property, the ECMAScript Proxy invariants force the security membrane to hand back the raw host object, letting a script reach _zod.constr.constructor (the host Function constructor) and execute arbitrary code in the server process. A single tools/call is sufficient to escape the sandbox and achieve remote code execution as the server user, exposing everything the process holds such as OAuth client secrets, JWT_SECRET, session keys, database credentials, and cloud instance metadata. Because the framework's DEFAULT_AUTH_OPTIONS is public mode, an unconfigured server serves this to unauthenticated callers, and on authenticated servers an indirect prompt injection in tool output or fetched content can trigger it without a human attackerThis issue is fixed in version 1.5.7.

### CVE-2026-9195

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-79` |
| Published | 2026-08-05T16:17:10.313 |

A cross-site scripting vulnerability in the Query Console of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows a remote attacker who lures an authenticated administrator to a crafted URL to execute arbitrary JavaScript in the administrator's browser session, capture credentials, and perform privileged actions on the administrator's behalf.

### CVE-2026-39923

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-324` |
| Published | 2026-08-05T16:16:55.980 |

Flarum before 1.8.16 contains a password reset token expiry bypass vulnerability that allows unauthenticated attackers to reuse expired password reset tokens by submitting them directly to the reset processing endpoint. The SavePasswordController::handle() method calls PasswordToken::findOrFail() without performing any expiry validation, allowing attackers to bypass the 24-hour token lifetime enforced only during form rendering and change any account's password to gain an authenticated session.

### CVE-2026-20310

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-05T17:16:51.520 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Catalyst SD-WAN engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20310 are related to improper link resolution before file access issues that are grouped under the Common Weakness Enumeration (CWE) CWE-59.

### CVE-2026-9190

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-05T16:17:09.940 |

An HTTP request smuggling vulnerability in the HTTP App Server of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows a remote attacker to bypass authentication and authorization checks, hijack a legitimate user's session, or capture credentials. The vulnerability occurs when a crafted HTTP request containing both Content-Length and Transfer-Encoding headers causes a reverse proxy and MarkLogic Server to interpret request boundaries differently.

### CVE-2026-7557

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-05T16:17:09.437 |

An improper verification of cryptographic signature vulnerability in the SAML authentication module of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an unauthenticated remote attacker to bypass authentication and impersonate any user, including administrators. This vulnerability affects deployments with SAML single sign-on enabled.

### CVE-2026-70426

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-05T18:17:12.233 |

In Remoting 3384.v60d89463d9e0 and earlier, except 3355.3357.v931d3c992987, included in Jenkins 2.575 and earlier, LTS 2.568.1 and earlier, the JEP-200 class filter is not applied to classes resolved via a fallback path in the Remoting deserialization implementation, allowing agent processes, code running on agents, and attackers with Agent/Connect permission to bypass the JEP-200 deserialization filter for classes on the Jenkins core classpath.

### CVE-2026-20267

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-05T17:16:47.560 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by&nbsp;CVE-2026-20267 are related to improper access control issues that are grouped under the Common Weakness Enumeration (CWE) Pillar&nbsp;CWE-284.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-15991

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T05:16:38.930 |

The File Manager plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the connector function in all versions from 6.0 - 6.9. This makes it possible for authenticated attackers, with subscriber-level access and above, to read and delete arbitrary files on the server, which can lead to remote code execution when the right file is deleted (such as wp-config.php). The bypass is triggered by passing cmd=rm or cmf=file in the URL query string of a POST request: elFinder's bind registration reads the command exclusively from $_POST and therefore never registers the rm.pre permission handler, while the dispatcher reads from the merged $_GET+$_POST superglobal and executes the rm or file command unchecked against a volume that defaults to ABSPATH.

### CVE-2026-17556

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T20:17:06.047 |

A path traversal vulnerability was identified in GitHub Enterprise Server that allowed an unauthenticated attacker to delete arbitrary files and directories on the instance, including the entire user storage directory containing Git LFS objects, release assets, attachments, and avatars. The X-GitHub-Request-Id request header was used without sanitization as a filesystem path segment for the upload buffer directory, so a traversal value pointed the buffer at an arbitrary path and the deferred cleanup routine recursively removed the traversed target. Exploitation required only network reachability to the instance and no authentication, and it worked even when private mode was enabled. This vulnerability affected all versions of GitHub Enterprise Server prior to 3.22 and was fixed in versions 3.21.4, 3.20.6, 3.19.10, 3.18.13 and 3.17.19. This vulnerability was reported via the GitHub Bug Bounty program.

### CVE-2026-9201

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-326` |
| Published | 2026-08-05T19:17:48.657 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow an authenticated attacker to execute arbitrary code due to a cryptographic weakness in the custom component validation mechanism. When the optional hardening mode that restricts execution to trusted component templates is enabled, the application validates component code using a truncated SHA‑256 hash. Because the hash comparison relies on only a portion of the digest, an attacker can craft malicious component code that collides with a trusted template hash and bypasses validation. Successful exploitation allows the attacker to introduce and execute unauthorized Python code within the Langflow process, defeating the intended security control and potentially leading to full compromise of the affected instance.

### CVE-2026-8478

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:45.043 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote attacker to inject arbitrary code on the system, due to the improper control of user input code.

### CVE-2026-8182

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:43.823 |

IBM Langflow OSS 1.0.0 through 1.10.3 installations allow anyone on the internet to execute arbitrary code on the server without any credentials via 2 HTTP requests.

### CVE-2026-17632

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:28.923 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary code due to improper validation of Python code during AST-based security scanning.

### CVE-2026-70432

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-05T18:17:12.903 |

A cross-site request forgery (CSRF) vulnerability in Jenkins Multijob Plugin 669.v9d96a_d9c71b_0 and earlier allows attackers to execute arbitrary code in the context of the Jenkins controller JVM.

### CVE-2026-70431

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T18:17:12.773 |

Jenkins Multijob Plugin 669.v9d96a_d9c71b_0 and earlier provides Groovy scripting features that do not integrate with Script Security Plugin, allowing attackers with Item/Create or Item/Configure permission to execute arbitrary code in the context of the Jenkins controller JVM.

### CVE-2026-20312

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-05T17:16:52.093 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Catalyst SD-WAN engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20312 are related to Cleartext storage of sensitive information issues that are grouped under the Common Weakness Enumeration (CWE) CWE-312.

### CVE-2026-20200

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-141` |
| Published | 2026-08-05T17:16:47.180 |

A vulnerability in the web-based management interface of Cisco IMC could allow an authenticated, remote attacker with low privileges to execute arbitrary commands on the underlying operating system of an affected system and elevate privileges to root.&nbsp;

This vulnerability is due to improper validation of user-supplied input. An attacker could exploit this vulnerability by entering crafted inputs to the web-based management interface of the affected software. A successful exploit could allow the attacker to execute arbitrary commands on the underlying operating system as the root user.&nbsp;

### CVE-2026-17626

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-05T17:16:44.783 |

IBM Langflow OSS 1.0.0 through 1.10.3 Langflow could allow an authenticated attacker to read, modify, or expose sensitive host files via Docker-based MCP servers due to incomplete filtering of dangerous Docker volume-mount and device-mapping arguments.

### CVE-2026-17623

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T17:16:44.663 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper validation of the command field in MCP server configurations.

### CVE-2026-15572

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-05T16:16:50.903 |

A flaw was found in Keycloak's Dynamic Client Registration (DCR) security policy management. The "Allowed Protocol Mapper Types" policy, which restricts which types of data mappers a client can use, fails to re-validate the mapper type during a client update if the mapper's configuration remains unchanged. An attacker with client registration privileges can exploit this by first registering an allowed mapper type with a malicious configuration and then swapping it for a restricted, high-privilege mapper type (such as one that hardcodes administrative roles). This allows the attacker to gain full administrative access to the Keycloak realm.

### CVE-2026-66733

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-06T13:18:21.947 |

Sonic 3 A.I.R. before commit 2492d18 contains an unbounded memory allocation vulnerability in ReceivedPacketCache::enqueuePacket() that allows unauthenticated remote attackers to crash the server process by sending a crafted UDP packet with mUniquePacketID set to the maximum uint32 value. The mUniquePacketID field is read directly from the UDP wire-format packet header without bounds checking, causing the server to allocate one CacheItem per missing packet ID gap, exhausting available host memory and propagating an uncaught std::bad_alloc exception to std::terminate().

### CVE-2026-69111

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T20:17:14.657 |

Milvus through 2.6.22 and 3.0.0 contains an unauthenticated denial of service vulnerability that allows remote attackers to terminate service components by sending a crafted HTTP GET request to the management server on port 9091. Attackers can exploit the unprotected /management/stop endpoint, which bypasses REST API authentication middleware, by supplying a 'role' parameter to shut down the proxy, datanode, or querynode components, resulting in denial of service.

### CVE-2026-71309

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T21:16:58.383 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. From 1.40.0 until 1.75.0, rclone serve restic does not correctly reject URL paths beginning with ../ in cmd/serve/restic/restic.go WithRemote, which accepts a leading parent path and passes it to GET, HEAD, POST, and DELETE handlers for configured backends including WebDAV, FTP, HTTP, Memory, and SFTP. An attacker who can access the REST endpoint may read, create, overwrite, or delete objects outside the path configured by the operator when the operator publishes a backend subdirectory and the backend credential can access parent or sibling objects. This issue is fixed in 1.75.0.

### CVE-2026-70617

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T20:17:17.770 |

Spacebar Server before commit dcfd910 contains a missing authorization vulnerability that allows any authenticated attacker to add themselves to arbitrary group DM channels by sending a PUT request to the channels recipient endpoint without membership verification. Attackers can exploit the unguarded PUT /channels/{channel_id}/recipients/{user_id} handler to join private group DMs, read complete message history, post messages as a participant, and force-add third-party users without their consent.

### CVE-2026-66298

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-05T20:17:12.203 |

Origin Validation Error vulnerability in livebook-dev livebook allows untrusted notebook output JavaScript to trigger session-wide keyboard shortcuts, including forced evaluation of all cells and runtime restart.

Livebook's JS-view feature renders notebook-defined JavaScript inside a sandboxed, cross-origin iframe specifically because that JavaScript is untrusted. The trusted iframe shell in iframe/priv/static/iframe/v5.html forwards every keydown event fired in its own window to the parent page without consulting Event.isTrusted, so an event synthesized by the untrusted script through window.dispatchEvent is forwarded exactly as a genuine keystroke would be. The parent-side relay in assets/js/hooks/js_view.js reconstructs and re-dispatches it on the live page with no further validation, and because assets/js/hooks/session.js registers the global shortcut handler on the document in the capture phase, that handler acts on the replicated event regardless of how it was produced.

Sandboxed output JavaScript can therefore drive Livebook's session-wide keyboard shortcuts. Two of them reach LivebookWeb.SessionLive and execute immediately with no confirmation: the shortcut for queueing full evaluation runs every cell in the notebook, and the shortcut for reconnecting the runtime disconnects and reconnects it, discarding in-memory state. A third shortcut deletes the focused cell behind a confirmation dialog that the user can permanently dismiss, after which it too executes silently.

Forced full evaluation is the significant consequence, because it causes the notebook's own Elixir code to run without the user choosing to evaluate anything. A user who merely opens a notebook obtained from a third party, or reached from published documentation, can have its code executed on their runtime. Livebook also mirrors cell outputs to every connected client, so a malicious output triggers in a collaborator's browser as soon as it renders.

This issue affects livebook: from 0.5.0 before 0.18.7 and from 0.19.0 before 0.19.9.

### CVE-2026-20301

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-606` |
| Published | 2026-08-05T17:16:50.187 |

A vulnerability in the Extensible Messaging Client Protocol (XMCP), also referred to as the External Client protocol, of Cisco IOS Software and Cisco IOS XE Software could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper handling of malformed XMCP packets. An attacker could exploit this vulnerability by sending a malformed XMCP packet to an affected device. A successful exploit could allow the attacker to cause the affected device to reload unexpectedly, resulting in a DoS condition. The attacker does not need the XMCP client username to exploit this vulnerability.

### CVE-2026-20273

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-05T17:16:49.290 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in a software hardening release that addresses multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20273 are related to improper input validation issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-20.

### CVE-2026-20271

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-691` |
| Published | 2026-08-05T17:16:48.810 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20271 are related to insufficient control flow management issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-691.
&nbsp;

### CVE-2026-20270

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-08-05T17:16:48.340 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20270 are related to incorrect calculation issues that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-682.

### CVE-2026-20269

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-664` |
| Published | 2026-08-05T17:16:48.070 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20269 are related to issues with improper control of a resource through its lifetime that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-664.

### CVE-2026-20268

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-05T17:16:47.830 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco IOS XE Software engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20268 are related to issues with improper restriction of operations within the bounds of a memory buffer that are grouped under the Common Weakness Enumeration (CWE) Pillar CWE-119.

### CVE-2026-20263

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-388` |
| Published | 2026-08-05T17:16:47.310 |

A vulnerability in the Blocks Extensible Exchange Protocol (BEEP) feature of Cisco IOS XE Software could allow an unauthenticated, remote attacker to cause a denial of service (DoS) condition on an affected device.

This vulnerability is due to improper handling when parsing a specific BEEP SOAP request. An attacker could exploit this vulnerability by sending a specific BEEP SOAP request to an affected device. A successful exploit could allow the attacker to cause the device to reload unexpectedly, resulting in a DoS condition.

### CVE-2026-18597

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-06T08:16:29.633 |

The PDF creation feature of Foxit PDF Services API supports referencing external files. Although local file access is restricted, an attacker could trigger an SSRF vulnerability by using URL redirection to bypass validation, leading to information disclosure.

### CVE-2026-70615

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-05T20:17:17.420 |

boringproxy through 0.10.0 contains a newline injection vulnerability that allows authenticated low-privileged users with tunnel-creation permission to inject arbitrary lines into the server account's SSH authorized_keys file by supplying a percent-encoded newline character in the domain parameter of the tunnel creation endpoint. Attackers can insert an unrestricted public key entry into authorized_keys to gain persistent shell access, and subsequently read cleartext credentials from the database file including all user tokens, tunnel private keys, and TLS certificates.

### CVE-2026-18485

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1285` |
| Published | 2026-08-05T19:17:29.170 |

There is a local privilege escalation vulnerability recently discovered in the NI-PAL kernel driver.  This may allow a local, authenticated user to escalate privileges and execute arbitrary code.  This vulnerability affects NI-PAL 26.3.1 and prior versions running on Microsoft Windows.

### CVE-2026-17633

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:29.043 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary code due to code injection.

### CVE-2026-17624

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:27.933 |

IBM Langflow OSS 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, and 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary code due to improper validation of module imports.

### CVE-2026-9077

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-807` |
| Published | 2026-08-05T17:16:57.510 |

IBM Langflow OSS 1.0.0 through 1.10.3 Langflow allows remote authenticated attackers to bypass localhost-only restrictions and write arbitrary MCP server configurations to IDE configuration files on the host system.

### CVE-2026-17617

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T17:16:44.543 |

IBM Application Gateway Operator 22.2 through 26.06 is vulnerable to Server-Side Request Forgery (SSRF) due to insufficient validation of URLs specified in custom resources.

### CVE-2026-9203

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T16:17:10.437 |

A server-side request forgery vulnerability in Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an authenticated user with low-privileged roles to bypass protections for cloud instance metadata endpoints. Successful exploitation can disclose cloud credentials and compromise cloud resources accessible to the host instance.

### CVE-2026-55978

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-06T10:16:43.910 |

An improper access control vulnerability in CatchPulse could allow a non-administrative local attacker to connect to an unrestricted kernel filter communication port and bypass CatchPulse's security policy enforcement.

### CVE-2026-16731

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:H/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:P/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-06T14:16:22.173 |

OMICRON StationScout before version 3.05 contains a cryptographic timing side-channel vulnerability in the backend authentication mechanism that may allow an unauthenticated attacker to forge valid authentication credentials, bypass authentication and authorization, and impersonate legitimate clients.
An attacker can gain full access to the system configuration, allowing modification, reset, or unauthorized alteration of system parameters or injecting network traffic into the connected network.

### CVE-2026-66732

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-06T13:18:21.773 |

Sonic 3 A.I.R. before commit 2492d18 contains a missing source address validation vulnerability in ConnectionManager where established connections are resolved by a two-byte local connection handle alone without verifying that the datagram source address matches the registered remote address for the connection. An on-path attacker who can observe cleartext UDP traffic can inject arbitrary packets into any established session by forging the two-byte connection identifier, enabling session termination via TerminateConnectionPacket, arbitrary channel message forgery, and forged request responses without requiring IP address spoofing.

### CVE-2026-34966

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T21:16:58.187 |

Gitea prior to 1.27.0 contains a server-side request forgery vulnerability that allows authenticated attackers to bypass SSRF protections by exploiting HTTP fetch operations in migration and OAuth avatar code paths that use Go's default http.Get without a custom DialContext. Attackers can supply arbitrary URLs through release asset download URLs, pull-request patch URLs, or OAuth avatar endpoints to reach internal services, cloud instance-metadata endpoints, or read local files such as the application configuration containing database credentials and signing secrets, with exfiltrated content persisted as migration release assets for later retrieval.

### CVE-2026-17583

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-353` |
| Published | 2026-08-05T21:16:57.393 |

The affected

Thermo Fisher Applied Biosystems Genetic Analyzers are vulnerable because .fsa/.hid output files can be edited. An attacker could tamper with these files, altering DNA data and resulting in inaccurate DNA test outcomes.

### CVE-2026-19024

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-05T23:16:53.343 |

NULL pointer dereference in H5Pget_fill_value in HDF5 before 2.1.1 allows attackers to cause a denial of service via a dataset whose version 1 or 2 fill value message has the "defined" flag set together with a negative size field, which is not normalized to the library's "undefined" sentinel and reaches H5T_path_find with a NULL datatype.

### CVE-2026-71315

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-178;CWE-863` |
| Published | 2026-08-05T21:16:59.297 |

Nuxt is an open-source web development framework for Vue.js. From 3.21.7 until 3.21.10 and 4.5.1, mixed-case routeRules keys can fail to match case-folded lookups when router.options.sensitive is false and drop appMiddleware authorization gates. This is caused by an incomplete fix for CVE-2026-53721. This issue is fixed in 3.21.10 and 4.5.1.

### CVE-2026-10025

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-05T16:16:49.197 |

IBM QRadar 7.6.0.0 through 7.6.0.1, and 7.5.0 through 7.5.0 UP 15 Interim Fix 005 has an XML External Entity (XXE) injection vulnerability. The vulnerability resides in the parseXmlPayload() function within the event processing pipeline ( q1labs_core.jar ). When at least one log source type is configured to use XML-format property autodetection, the system processes XML-formatted syslog events sent to port 514 (UDP/TCP) without authentication.

### CVE-2026-16315

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:U/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-06T14:16:21.840 |

OMICRON StationGuard before version 4.10 contains a cryptographic timing side-channel vulnerability in the backend authentication mechanism that may allow an unauthenticated attacker to forge valid authentication credentials, bypass authentication and authorization, and impersonate legitimate clients.
An attacker can gain full access to the system configuration, allowing modification, reset, or unauthorized alteration of system parameters.

### CVE-2026-15459

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-06T06:16:30.950 |

The WPMU DEV Dashboard plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 5.0.0. On sites not yet connected to the WPMU DEV Hub — the default state after installation — the site API key that keys the WDP-AUTH request signature is empty, making the signature verified by validate_hash() trivially forgeable; version 5.0.0 additionally removed the replay check in validate_nonce(), and the remote handler is bound to the public init hook with no capability check. This makes it possible for unauthenticated attackers to invoke privileged Hub actions — including installing and activating a plugin from an attacker-supplied URL (resulting in remote code execution), deleting plugins and themes, upgrading WordPress core, or logging in as an administrator via SSO. Sites connected to a WPMU DEV account, which have a non-empty 64-character API key, are not affected.

### CVE-2026-71320

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74;CWE-94` |
| Published | 2026-08-05T22:17:08.367 |

Nuxt is an open-source web development framework for Vue.js. From 3.4.0 until 3.21.10 and 4.5.1, an attacker can inject a template key through /__nuxt_island/ props into a dynamic component when `vue.runtimeCompiler: true` is enabled, causing template execution in the Nitro process. This issue is fixed in 3.21.10 and 4.5.1.

### CVE-2026-9196

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-05T19:17:48.523 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow an authenticated attacker to execute unintended code during Agentic Assistant validation due to improper handling of LLM‑generated components. The application executes model‑generated Python code in the backend during validation prior to user approval, which may allow an attacker to trigger side effects such as outbound network access, file system interaction, or data exfiltration with the privileges of the Langflow backend process.

### CVE-2026-8400

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-05T16:17:09.657 |

IBM WebSphere Application Server 8.5, and 9.0 and IBM WebSphere Application Server - Liberty Continuous delivery has a flaw in the ORB component in IBM SDK, Java Technology Edition, may allow a malicious IIOP server to induce loading and instantation of arbitrary classes.

### CVE-2026-7327

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-05T16:17:09.077 |

An improper privilege management vulnerability in the REST API document processing pipeline of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows an authenticated user with an administrative REST role to escalate privileges. This can result in unauthorized disclosure of sensitive server-side data when it is accessed by a higher-privileged user.

### CVE-2026-16102

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-05T15:16:37.703 |

A flaw was found in the Dynamic Client Registration (DCR) component of Keycloak, an identity and access management solution. The default DCR policy fails to properly validate the claim path for User Property mappers, allowing them to write values to sensitive internal claim locations. An attacker with a standard user account and a limited Initial Access Token can exploit this to forge administrative roles in their access token. This allows the attacker to take over other clients, steal confidential secrets, and potentially gain full administrative control over the realm.

### CVE-2026-15573

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-08-05T15:16:36.397 |

A flaw was found in Keycloak's Authorization Services. The component responsible for matching request paths to security policies (PathMatcher) does not properly normalize URIs before comparison. By adding extra characters like a trailing slash or matrix parameters to a URL, an attacker can trick the system into applying a less restrictive security policy than intended. This allows an authenticated user to access administrative or restricted areas they should not have permission to see.

### CVE-2026-71312

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T21:16:58.867 |

rclone is a command-line program to sync files and directories to and from different cloud storage providers. Prior to v1.75.0, rclone interpolates remote SFTP paths into PowerShell hash commands in backend/sftp/sftp.go, and quoteOrEscapeShellPath escapes only ASCII apostrophe even though PowerShell treats U+2018, U+2019, U+201A, and U+201B as single-quote delimiters, allowing an attacker-controlled filename to terminate the intended path literal and append PowerShell statements that execute as the victim SSH account when server-side hashing is invoked. This issue is fixed in v1.75.0.

### CVE-2026-55522

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-426;CWE-829` |
| Published | 2026-08-05T20:17:10.453 |

PraisonAI is a multi-agent teams system. In versions 3.9.26 through 4.6.57 of praiseonai and 0.12.12 through 1.6.57 of praiseonaiagents, the workflow "include" feature is vulnerable to code execution. Workflow._execute_include() implicitly imports and runs an included recipe's tools.py via a raw importlib.util.spec_from_file_location() and spec.loader.exec_module() call, without honoring the PRAISONAI_ALLOW_TEMPLATE_TOOLS/PRAISONAI_ALLOW_LOCAL_TOOLS autoload opt-in gates or routing through the centralized safe loader that protects the other tools.py autoload paths. As a result, a workflow that includes an attacker-controlled local recipe directory executes arbitrary module-level Python code during include setup, before any child workflow parsing or model call, and the same sink is reachable through the higher-level praisonai.recipe.run() recipe API. An attacker who can cause a victim process to run a workflow or recipe that includes an untrusted local recipe achieves arbitrary Python code execution as the PraisonAI process user, a variant that bypasses the hardening applied to the previously disclosed automatic tools.py RCE advisory family. This issue has been fixed in version 4.6.58 of praisonai and 1.6.58 of praisonaiagents.

### CVE-2026-12410

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-05T15:16:35.833 |

Link following vulnerability in the Uninstaller component in CCleaner prior to 7.10.1464 on Windows allows a local, low-privileged attacker to escalate privileges to SYSTEM via a symlink/junction created during application uninstallation, which CCleaner follows when deleting the application's data folder with elevated integrity.

### CVE-2026-68746

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-08-05T20:17:14.393 |

Not Failing Securely ('Failing Open') vulnerability in livebook-dev livebook allows an unauthenticated network client to obtain full access to a Livebook server that enforces identity through Livebook Teams.

A Livebook Agent or App Server connected to Livebook Teams caches the identifier of the deployment group it belongs to, and resolves that identifier against a locally cached list of deployment groups on every request in order to decide whether Teams identity enforcement is active. Livebook.Hubs.TeamClient.handle_call/3 in lib/livebook/hubs/team_client.ex does not distinguish a deployment group that could not be resolved from one that was resolved with identity enforcement switched off: the clause matches only the case where a group was found with enforcement enabled, and falls through to a catch-all that reports enforcement as switched off for everything else. The two neighbouring functions that decide user and application access resolve the same identifier and treat the same unresolved result as a denial.

When the identity status is reported as switched off, Livebook.ZTA.LivebookTeams.authenticate/3 in lib/livebook/zta/livebook_teams.ex returns empty identity metadata and allows the request to continue instead of halting it. LivebookWeb.UserPlug.build_current_user/3 merges that empty metadata into a newly built user, whose access type defaults to full access, and LivebookWeb.AuthPlug.authorized?/1 grants access to any user holding full access.

The cached identifier becomes unresolvable when the deployment group it refers to is deleted while the agent is not connected to receive the change, most concretely when a deployment group is deleted during the window in which an agent is disconnected or reconnecting. The client removes the group from its cached list without clearing the identifier that refers to it. Any client able to reach the affected server over the network is then granted the same access as a fully privileged member of the organisation, including the ability to read notebooks and configured secrets, execute code on the server's runtime, and disrupt its operation.

This issue affects livebook: from 0.19.7 before 0.19.9.

### CVE-2026-55523

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T20:17:10.690 |

PraisonAI is a multi-agent teams system. In versions 1.5.128 through 1.6.57, the praisonaiagents.tools.web_crawl_tools.web_crawl() function is vulnerable to server-side request forgery. While it validates the initially supplied URL and blocks direct loopback and private destinations, its default httpx fallback uses httpx.Client(follow_redirects=True) and does not revalidate intermediate or final redirect targets. An attacker who can influence a URL passed to web_crawl(), directly or through an agent or tool workflow, can supply an attacker-controlled public URL that passes the initial host check and then redirects to loopback, private-network, or cloud metadata endpoints reachable from the host, with the redirected response body returned in the web_crawl() result. This constitutes an incomplete fix and patch bypass for the previously disclosed web_crawl SSRF class (GHSA-qq9r-63f6-v542 / CVE-2026-40160 and GHSA-8f4v-xfm9-3244), since the guard validates only the requested URL and not the destination actually fetched after redirection. This issue has been fixed in version 1.6.58.

### CVE-2026-8183

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-05T19:17:43.943 |

IBM Langflow OSS 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, and 1.0.0 through 1.10.3 could allow a remote attacker to traverse directories on the system. An attacker could send a specially crafted URL request containing "dot dot " sequences ( /.. /) to v i ew arbitrary files on the system.

### CVE-2026-20313

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-1284` |
| Published | 2026-08-05T17:16:52.437 |

As part of Cisco's ongoing commitment to proactive security and product quality, the Cisco Catalyst SD-WAN engineering team has conducted a comprehensive internal security review. This review resulted in software hardening releases that address multiple internally discovered vulnerabilities.

The vulnerabilities tracked by CVE-2026-20313 are related to Improper link resolution before file access issues that are grouped under the Common Weakness Enumeration (CWE) CWE-1284.

### CVE-2026-20124

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-772` |
| Published | 2026-08-05T17:16:46.643 |

A vulnerability in the Simple Network Management Protocol (SNMP) subsystem of Cisco IOS XE Software could allow an authenticated, remote attacker to cause an affected device to reload, resulting in a denial of service (DoS) condition.

This vulnerability is due to improper error handling when parsing SNMP requests. This vulnerability affects all versions of SNMP &mdash; Versions 1, 2c, and 3. An attacker could exploit this vulnerability by sending a malformed SNMP request to an affected device. A successful exploit could allow the attacker to cause the device to reload unexpectedly. The attacker must have the SNMPv1 or v2c read-only or read-write community string or valid SNMPv3 user credentials on the affected device.

### CVE-2026-39924

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-05T16:16:56.137 |

Flarum before 1.8.16 contains an improper session invalidation vulnerability that allows attackers who hold a valid session token to retain full account access after a victim changes their password, because the access_tokens table is never cleared on password change events. The TokensClearer::clearPasswordTokens() function only removes rows from the password_tokens table while leaving all active session cookies and API bearer tokens intact, including long-lived RememberAccessToken entries, and administrator-forced password resets via the user update endpoint are equally ineffective at revoking attacker-held sessions.

### CVE-2026-65551

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-06T13:18:21.417 |

Missing Authorization vulnerability in Soflyy Breakdance allows Exploiting Incorrectly Configured Access Control Security Levels.

This issue affects Breakdance: from n/a before 2.7.

### CVE-2026-18649

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-06T08:16:29.780 |

A flaw was found in the GStreamer gst-plugins-good package. The rtph264depay and rtph265depay RTP depayloader elements do not enforce a maximum size limit on the reassembly buffer used during fragmented RTP packet processing. A remote, unauthenticated attacker can send a continuous stream of RTP fragments without ever transmitting an end-of-fragment marker, causing the reassembly buffer to grow without bound until process memory is exhausted. This results in a denial of service through process termination.

### CVE-2026-67872

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-06T00:16:54.267 |

An issue in Systerel S2OPC 1.7.3 allows a remote attacker to cause a denial of service via the event monitored-item queue resize handling

### CVE-2026-67871

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-06T00:16:54.160 |

Buffer Overflow vulnerability in Systerel S2OPC 1.7.3 allows a remote attacker to cause a denial of service via the AddNodes, address_space_bs.c, sopc_node_mgt_helper_internal.c, and toolkit_test_server

### CVE-2026-67869

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-06T00:16:53.900 |

Buffer Overflow vulnerability in open62541 v1.5.5 allows a remote attacker to cause a denial of service via the Service_Call validates input arguments against runtime-resolved InputArguments metadata

### CVE-2026-67867

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-05T23:16:53.997 |

Buffer Overflow vulnerability in Systerel S2OPC 1.7.3 allows a remote attacker to cause a denial of service via the Alarm/Conditions wrapper when processing PublishResponse EventNotificationList data

### CVE-2026-67866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-05T23:16:53.887 |

Buffer Overflow vulnerability in Systerel S2OPC 1.7.3 allows a remote attacker to cause a denial of service via the LockedStaMac_ProcessMsg_DeleteMonitoredItemsResponse and SOPC_StaMac_NewDeleteMonitoredItems in the client wrapper DeleteMonitoredItems path

### CVE-2026-67863

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-05T23:16:53.753 |

In open62541 1.5.5, a server-side use-after-free exists in the local MonitoredItem callback path. The issue occurs when UA_Subscription_localPublish continues to use the current UA_Notification after a callback invokes UA_Server_deleteMonitoredItem for the current local MonitoredItem. This allows a remote attacker to cause a denial of service.

### CVE-2026-71321

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-770` |
| Published | 2026-08-05T22:17:08.507 |

Nuxt is an open-source web development framework for Vue.js. From 3.1.0 until 3.21.10 and 4.5.1, the internal island renderer endpoint `/__nuxt_island/...` decodes and hashes attacker-controlled JSON body input with destr and ohash before validating the URL-resident hash. An unauthenticated `POST /__nuxt_island/_.json` with a large JSON body is fully read, parsed, hashed, and then rejected, which wastes CPU on Nitro single event loop and delays concurrent requests. No valid hash and no authentication are required. This issue is fixed in 3.21.10 and 4.5.1.

### CVE-2026-71316

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-524;CWE-862` |
| Published | 2026-08-05T22:17:07.917 |

Nuxt is an open-source web development framework for Vue.js. From 4.4.0 until 4.5.1, runtime cache:nuxt:payload entries for /<page>/_payload.json can be returned before route middleware and page guards because import.meta.prerender is not enforced, disclosing another user's SSR data. This issue is fixed in 4.5.1.

### CVE-2026-67865

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-05T22:17:07.797 |

S2OPC 1.7.3 contains an out-of-bounds read in RepublishResponse handling. This allows a remote attacker to cause a denial of service

### CVE-2026-71314

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770;CWE-789;CWE-1284` |
| Published | 2026-08-05T21:16:59.150 |

Nuxt is an open-source web development framework for Vue.js. From 3.1.0 until 3.21.10 and 4.5.1, an unauthenticated attacker can use a server island v-for prop, including vforToArray and , to trigger unbounded SSR memory allocation until MAX_VFOR_LENGTH = 100000 and crash the Nuxt process. This issue is fixed in 3.21.10 and 4.5.1.

### CVE-2026-55524

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-08-05T20:17:10.847 |

PraisonAI is a multi-agent teams system. In versions prior to 1.6.58, the web_crawl tool performs its SSRF check only on the initially supplied URL, allowing the protection to be bypassed so the tool connects to attacker-chosen internal destinations. The check resolves the hostname once with socket.gethostbyname and rejects private/loopback/link-local results, but then passes the URL to a fetcher using httpx.Client(follow_redirects=True) (or urllib.request.urlopen when httpx is absent, which also follows redirects) that re-resolves the hostname at connect time with no further validation. This validate-here/fetch-there gap is exploitable through both HTTP redirects and DNS rebinding. If an attacker can influence URLs passed to web_crawl(), directly or through an agent/tool workflow, they can cause the PraisonAI host to fetch loopback, private-network, or cloud metadata endpoints reachable from that host, with the response body returned in the web_crawl() result. This issue has been fixed in version 1.6.58.

### CVE-2026-10716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-05T18:16:52.410 |

Directus contains an authenticated SQL injection vulnerability in the collection creation flow when the instance uses PostgreSQL with PostGIS enabled. An administrator can create a collection with a geometry field whose fields[].type value starts with geometry but contains attacker-controlled SQL syntax after the geometry subtype.This issue affects Directus: before 12.1.0.

### CVE-2026-8446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-05T17:16:55.983 |

IBM Langflow OSS 1.0.0 through 1.10.3 contain an authentication bypass vulnerability in the Model Context Protocol (MCP) composer endpoint when mcp_composer_enabled=true (default) and projects are configured with auth_type=oauth .

### CVE-2026-7326

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-05T16:17:08.930 |

A cross-site request forgery vulnerability in the Admin UI of Progress MarkLogic Server before 11.3.6 and 12.0.3 allows a remote attacker who lures an authenticated administrator to a malicious web page to perform administrative actions on the administrator's behalf. This can result in unauthorized changes to security configuration.

### CVE-2026-70601

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-05T16:17:04.203 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 39.8.9, 40.9.2, 41.2.2, and 42.0.0-beta.5, apps that expose Promise-returning functions to web content via contextBridge may be vulnerable to a context isolation bypass. Untrusted web content could obtain access to the isolated preload world and, through it, every capability the preload script has. In renderers without a sandbox, or with nodeIntegration enabled, this may escalate to Node.js access. Apps are affected if they expose Promise-returning functions via contextBridge, the standard pattern for wrapping ipcRenderer.invoke, in windows that load untrusted content. This issue is fixed in versions 39.8.9, 40.9.2, 41.2.2, and 42.0.0-beta.5.

### CVE-2026-54876

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-08-05T15:16:53.487 |

Issue summary: A malicious TLS server can cause a memory leak in a TLS
client that has enabled OCSP response checking by sending an OCSP
response that contains no single response entries.

Impact summary: An attacker can leak an attacker-tunable amount of memory
per TLS handshake in a victim client application. A long-running client
that repeatedly connects to a malicious server can have its memory
exhausted, resulting in a Denial of Service.

CWE: CWE-401: Missing Release of Memory after Effective Lifetime

Description: The affected function is called during X.509 certificate
chain verification when OCSP response checking is enabled
with the X509_V_FLAG_OCSP_RESP_CHECK or X509_V_FLAG_OCSP_RESP_CHECK_ALL
verification flags, for example when a TLS client verifies an OCSP
response stapled into the TLS handshake by the server.

When the received BasicOCSPResponse contains an empty SEQUENCE OF
SingleResponse, which is permitted on the wire and accepted by the
OpenSSL decoder, the OCSP_BASICRESP structure allocated by
OCSP_response_get1_basic() was not freed because an early return
bypassed the cleanup code at the end of the function.

The amount of memory leaked per handshake can be amplified by the
attacker by padding the certs field of the BasicOCSPResponse with
bogus certificates, which are parsed and stored in the leaked
structure before the empty response check triggers the early return.
A long-running TLS client that repeatedly connects to a malicious
server can have its memory exhausted over time.

OCSP response checking is not enabled by default. Only client
applications that explicitly enable the OCSP response check
verification flags are affected.

FIPS impact: no

The FIPS modules in 4.0 and 3.6 are not affected by this issue as the
affected code is outside the OpenSSL FIPS module boundary.

### CVE-2026-17613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-05T15:16:40.003 |

Penpot’s ::import-binfile RPC command lacks authorization on the optional file-id parameter, allowing any authenticated user to overwrite any files on the target server and subscribe to WebSocket events, enabling full data exfiltration and data poisoning.

### CVE-2026-9205

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-338` |
| Published | 2026-08-05T19:17:49.193 |

IBM Langflow OSS contains a weak cryptographic key derivation vulnerability in the ensure_fernet_key() function.

### CVE-2026-8470

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-327` |
| Published | 2026-08-05T19:17:44.823 |

IBM Langflow OSS 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, and 1.0.0 through 1.10.3 use Python's non-cryptographic random module for generating Fernet encryption keys from user secrets under 32 characters. The deterministic Mersenne Twister PRNG produces identical keys for identical seeds, allowing attackers to reproduce encryption keys and decrypt stored API keys and authentication tokens.

### CVE-2026-70604

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-942` |
| Published | 2026-08-05T16:17:04.617 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 39.8.10, 40.9.3, 41.4.0, and 42.0.0, a custom scheme registered with supportFetchAPI: true but without corsEnabled: true was not subject to CORS enforcement. A page loaded from a remote origin could therefore fetch() or XMLHttpRequest that scheme cross-origin and read the full response body, rather than the read being blocked. Apps that serve sensitive data from such a scheme and load remote or untrusted content in a renderer are affected. This issue is fixed in versions 39.8.10, 40.9.3, 41.4.0, and 42.0.0.

### CVE-2026-16442

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-05T16:16:52.027 |

A flaw was found in the SAML broker component of Keycloak, which is used to manage identity federation and user authentication. The issue occurs because the IdP-initiated Single Sign-On endpoint fails to check if a provider is restricted to account linking only. This allows an attacker with control over a linked upstream identity to bypass login restrictions and gain full access to a local user account.

### CVE-2026-19036

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-06T13:17:27.457 |

A security flaw has been discovered in Shibby Tomato 1.28.0000. This affects the function sub_40F88C of the file /tmp/ppp/wanoptions. The manipulation of the argument ppp_custom results in os command injection. The attack may be launched remotely. The exploit has been released to the public and may be used for attacks. This project is superseded by FreshTomato.

### CVE-2026-19035

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-06T12:16:27.103 |

A vulnerability was identified in Shibby Tomato 1.28.0000. Affected by this issue is the function new_qoslimit_start of the file /etc/qoslimit. The manipulation of the argument new_qoslimit_enable leads to os command injection. The attack may be initiated remotely. The exploit is publicly available and might be used. This project is superseded by FreshTomato.

### CVE-2026-19034

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-06T11:16:29.777 |

A vulnerability was determined in Shibby Tomato 1.28.0000. Affected by this vulnerability is the function new_qoslimit_stop of the file /tmp/qoslimittc_stop.sh. Executing a manipulation of the argument wan_iface can lead to os command injection. The attack can be launched remotely. The exploit has been publicly disclosed and may be utilized. This project is superseded by FreshTomato.

### CVE-2025-15028

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T12:16:26.523 |

The FormGent – Next-Gen AI Form Builder for WordPress with Multi-Step, Quizzes, Payments & More plugin for WordPress is vulnerable to Stored Cross-Site Scripting via form submission fields in all versions up to, and including, 1.9.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-18510

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T07:16:29.270 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Content (URL-encoded gettext markers) in all versions up to, and including, 3.2.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Comment moderation may delay exploitation for first-time commenters, but does not prevent it, as the payload uses only WordPress-permitted tags and attributes with percent-encoded characters that pass wp_kses URL validation unmodified.

### CVE-2026-18325

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T05:16:40.593 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Forged Upload Record via Select Field in all versions up to, and including, 1.56.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit is possible because Forminator_Core::sanitize_array() skips all filtering for keys prefixed with 'select-', and set_field_data() treats a submitted 'return' member as a trusted internal flag — allowing an unauthenticated attacker to forge and persist a complete upload field record with an arbitrary file_url value without any sanitization or validation.

### CVE-2026-16636

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-06T05:16:39.140 |

The FluentSMTP – WP SMTP Plugin with Amazon SES, SendGrid, MailGun, Postmark, Google and Any SMTP Provider plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Recipient Display Name (to.name) in Email Logs in all versions up to, and including, 2.2.95 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is delivered via an attacker-controlled recipient display name (to.name) in a wp_mail() call and does not fire in the log list view — only in the detail view when an administrator uses the Prev/Next navigation controls, as that path bypasses the escapeHtml pipeline used by the list view.

### CVE-2026-18411

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-05T21:16:57.563 |

The KARR Security System and SWDS dealer-installed automotive anti-theft systems use a shared Bluetooth authentication key across affected devices. An attacker within Bluetooth range can leverage this weakness to issue unauthorized commands to the vehicle, potentially allowing unauthorized access to vehicle functions, including door unlocking and engine immobilization.

### CVE-2026-70608

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-693;CWE-1021` |
| Published | 2026-08-05T18:17:15.160 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. Prior to 39.8.10, 41.10.3, and 42.0.1, a sandboxed iframe without the allow-popups keyword could still open a new window or trigger setWindowOpenHandler with no user interaction because new-window navigations taking the OpenURL path did not apply the iframe sandbox popup restriction. Apps that embed untrusted content in sandboxed iframes and rely on the absence of allow-popups to prevent window creation are affected, while apps that deny window creation in setWindowOpenHandler or do not embed untrusted content in sandboxed iframes are not affected. This issue is fixed in 39.8.10, 41.10.3, and 42.0.1.

### CVE-2026-17625

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-05T18:16:54.877 |

IBM Langflow OSS 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, 1.0.0 through 1.10.3, and 1.0.0 through 1.10.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-17630

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-05T17:16:44.923 |

IBM Langflow OSS 1.0.0 through 1.10.3 could allow a remote attacker to execute arbitrary code due to improper validation of configuration parameters.

### CVE-2026-70616

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-833` |
| Published | 2026-08-05T20:17:17.600 |

boringproxy through 0.10.0 contains a resource exhaustion vulnerability that allows any authenticated user to permanently exhaust server file descriptors, goroutines, and memory by sending requests to the GET /loading endpoint with attacker-supplied id query parameter values. Because the handler performs no map-lookup validity check and receives on a nil channel that blocks forever, with no timeout, no context cancellation, and no server-side reclamation due to absent HTTP server timeouts, each malicious request permanently holds one goroutine, one file descriptor, and approximately 50 kB of memory until the server's file descriptor limit is reached and listener Accept calls fail, halting all tunnel traffic forwarding for all users.

### CVE-2026-9130

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-05T19:17:46.797 |

IBM Langflow OSS 1.0.0 through 1.10.3 contain an authorization bypass vulnerability in the MemoryComponent that allows authenticated users to access chat history of other users via session_id collision. The MemoryComponent.retrieve_messages and store_message methods filter on session_id without validating flow_id or user_id ownership, enabling cross-user information disclosure through multiple authenticated API endpoints including /api/v1/run/*, /api/v1/responses, and /api/v2/workflow/*. This vulnerability only affects multi-user deployments with LANGFLOW_AUTO_LOGIN=False.

### CVE-2026-9081

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-05T18:17:16.130 |

IBM Langflow OSS 1.0.0 through 1.10.3, and 1.0.0 through 1.10.3 contains a Server-Side Request Forgery (SSRF) vulnerability in the validate_model_provider_key() function for the Ollama provider. The function accepts a user-supplied OLLAMA_BASE_URL parameter and passes it directly to requests.get() without validation, scheme/host allowlisting, or filtering of private IP ranges (loopback, RFC1918, link-local addresses).

### CVE-2026-70448

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-05T18:17:14.687 |

Jenkins Ivy Report Plugin 1.2 and earlier does not configure its XML parser to prevent XML external entity (XXE) attacks when processing Ivy report files.

### CVE-2026-66881

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-05T20:17:12.600 |

Relative Path Traversal vulnerability in livebook-dev livebook allows an attacker-authored notebook to write a file with attacker-controlled content to an arbitrary path.

A .livemd notebook can declare file_entries metadata, each entry carrying a name. Every path that creates a file entry through the user interface validates that name with Livebook.Notebook.validate_file_entry_name/2, which requires a flat filename of alphanumerics, dashes, underscores and dots, ending in an extension. The import path does not: Livebook.LiveMarkdown.Import.file_entry_metadata_to_attrs/1 in lib/livebook/live_markdown/import.ex takes the name verbatim from the notebook source.

For a URL-type file entry, Livebook.Session.file_entry_cache_file/2 in lib/livebook/session.ex resolves that name beneath the session's temporary directory without checking that the result stays inside it, and Livebook.FileSystem.Utils.resolve_unix_like_path/2 collapses parent-directory segments while clamping only at the filesystem root. When the entry's content is requested and no cached copy exists, Livebook fetches the entry's URL and writes the response body to the resolved path, creating parent directories as needed. The attacker therefore controls both the destination and the contents of the written file, which may land anywhere the Livebook process can write. The same missing containment check is present in Livebook.Session.to_attachment_file_entry/2.

A victim who opens an attacker-supplied notebook and causes the entry to be fetched triggers the write within their own authenticated session; the attacker needs no account on the target instance. URL-type entries are also not placed under notebook stamping quarantine on import, so no warning is shown.

This issue affects livebook: from 0.11.0 before 0.18.7 and from 0.19.0 before 0.19.9.
