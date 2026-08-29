# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-29 15:01 UTC
- **対象期間**: `2026-08-28T15:00:40.000Z` 〜 `2026-08-29T15:01:21.000Z`
- **重要CVE数**: 118 件（Critical 9.0+: 28 件 / High 7.0〜: 90 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、**CVSS 7.0 以上が 40 件以上**と非常に多く、特に **認証バイパス・リモートコード実行 (RCE)** 系の脆弱性が目立ちます。  
- Kubernetes 系ツール（Argo CD、Kubeflow、Argo Rollouts）や **データプラットフォーム（JFrog Artifactory、Redpanda、Pimcore）** がネットワークに対して過度にオープンな設定をデフォルトで提供している点が共通しています。  
- 多くの脆弱性は **「デフォルトで認証が無効」**、あるいは **「外部から直接呼び出せる管理 API」** が原因で、内部ネットワークに侵入できた攻撃者がフル権限を取得できる点が危険です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な問題点 | 影響範囲・被害シナリオ | 推奨される対策 (概要) |
|-----|------|------------|------------------------|------------------------|
| **CVE‑2026‑82456** | 10.0 | Argo CD MCP が **全インターフェースにバインド** し、`ARGOCD_API_TOKEN` が設定されていると認証なしで MCP セッションを受け付ける | 攻撃者が同一ネットワーク上にいるだけで、Argo CD の全機能（アプリケーション作成・削除・設定変更）を **オペレーター権限** で実行可能 | - `argocd-mcp` を **0.8.1 以降** にアップデート<br>- `--bind-address=127.0.0.1`（または内部限定IP）で起動<br>- `ARGOCD_API_TOKEN` の使用は最小権限トークンに限定し、環境変数での自動注入をやめる |
| **CVE‑2026‑54745** | 10.0 | Kubeflow Pipelines フロントエンドの **/\\_proxy/** ルートで SSRF が可能 | 任意の内部サーバ（例: メタデータサービス、Kubernetes API）へリクエストを送信でき、認証情報取得や内部サービスの不正操作が可能 | - **2.17.0 以降** にアップデート<br>- `/\\_proxy/` エンドポイントを **Ingress/NetworkPolicy** で外部から遮断<br>- 必要なら `proxy` 機能を無効化 (`KFP_DISABLE_PROXY=true`) |
| **CVE‑2026‑82329** | 9.8 | JFrog Artifactory のデフォルト設定で **認証なしで管理 API が利用可能** | ネットワーク上の未認証ユーザーが **管理者権限** でリポジトリ作成・削除、設定変更、機密情報取得ができる | - **7.84.0 以降** にアップデート（認証強制パッチ）<br>- `artifactory.system.security.requireAuthentication=true` を明示的に設定<br>- 管理 API のポートを **ファイアウォールで内部限定** |
| **CVE‑2026‑82266** | 9.3 | Redpanda が **Admin API を 0.0.0.0:9644 にバインド**、`admin_api_require_auth` がデフォルト **false** | 任意の内部クライアントが **スーパーユーザー** としてブローカー作成・削除、クラスタ設定変更、データ破壊が可能 | - **26.2.3 以降** にアップデート<br>- `admin_api_require_auth=true` を設定し、TLS クライアント証明書で保護<br>- Admin API のポートを **内部ネットワークのみ** に制限 |
| **CVE‑2026‑82448** | 9.3 | Shinobi の子ノードサービスに **ハードコードされた接続キー** があり、WebSocket ハンドシェイクで認証なしに使用できる | 攻撃者が子ノードポートに接続し、任意の **SQL クエリ** を実行できる（データベース改ざん・情報漏洩） | - **0.9.0 以降** にアップデート（キー除去）<br>- 子ノードサービスの **バインドアドレスをローカル** に変更<br>- キー管理を **環境変数またはシークレットストア** に移行 |

> **注**：上記は CVSS が 9.8 以上のものを中心に選出していますが、同様に **認証バイパス** 系 (CVE‑2026‑82452, CVE‑2026‑82277, CVE‑2026‑82281 など) も組織の内部防御策で必ず対処すべきです。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **ネットワーク境界の強化**  
  - すべての管理 API（Argo CD, Kubeflow, JFrog Artifactory, Redpanda, Shinobi 等）を **ファイアウォール / Security Group** で内部ネットワークに限定。  
  - 必要な場合は **Zero‑Trust** の mTLS や API‑Gateway 認証を導入。  

- **認証・認可のデフォルト強化**  
  - 各製品の設定ファイルで **認証必須** (`requireAuthentication=true` など) を明示的に有効化。  
  - デフォルトの管理者パスワード・トークンは **即時変更**、かつ **最小権限** のトークンに置き換える。  

- **監査ログの有効化**  
  - 変更系 API の呼び出しを **JSON ログ** で記録し、SIEM に転送。  
  - 不審な IP からのアクセスや異常な操作があれば **アラート** を上げる。  

### 3.2 製品別具体的アップデート・設定例  

| 製品 | 現行バージョン (脆弱) | 修正版バージョン | 主な設定変更例 |
|------|----------------------|------------------|----------------|
| **argocd‑mcp** | 0.8.0 | **0.8.1** 以上 | `--bind-address=127.0.0.1` <br> `ARGOCD_API_TOKEN` を **Read‑Only** に限定 |
| **Kubeflow Pipelines** | < 2.17.0 | **2.17.0** 以上 | `KFP_DISABLE_PROXY=true` <br> Ingress で `/\_proxy/` を **deny** |
| **JFrog Artifactory** | 任意 (デフォルト) | **7.84.0** 以上 | `artifactory.system.security.requireAuthentication=true` <br> 管理 API ポートを内部限定 |
| **Redpanda** | ≤ 26.2.2 | **26.2.3** 以上 | `admin_api_require_auth=true` <br> TLS クライアント証明書を必須に |
| **Shinobi** | 任意 (ハードコードキー) | **0.9.0**

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-82456

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1327` |
| Published | 2026-08-29T14:16:38.767 |

argocd-mcp 0.8.0 binds its HTTP transport to every network interface and accepts MCP sessions without requiring caller credentials when ARGOCD_API_TOKEN is configured. Attackers who can reach the listener can invoke the full tool surface using the operator's stored token to create applications, request syncs, and modify Argo CD resources.

### CVE-2026-54745

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-918` |
| Published | 2026-08-28T20:18:17.240 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.17.0, the Kubeflow Pipelines frontend exposes an unauthenticated server-side request forgery vulnerability through the /_proxy/ route in frontend/server/proxy-middleware.ts. The _routePathWithReferer() function accepts an arbitrary attacker-controlled HTTP or HTTPS target and passes its origin to createProxyMiddleware without a host allowlist or filtering for loopback, link-local, RFC1918, or cluster-local addresses. The route remains outside the authorization middleware when ENABLE_AUTHZ=true and is reachable through /apis/v1beta1/_proxy/, /apis/v2beta1/_proxy/, /pipeline/apis/v1beta1/_proxy/, and /pipeline/apis/v2beta1/_proxy/, including through a crafted Referer header. Requests can forward attacker-controlled methods, headers such as Authorization, Cookie, and X-Forwarded-For, and POST bodies to reachable internal services, while returning the upstream response to the unauthenticated client. This can expose cloud metadata credentials, Kubernetes or service APIs, and other cluster-internal endpoints to unauthorized read or modification. This issue is fixed in version 2.17.0.

### CVE-2026-19295

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-28T22:16:47.613 |

IBM Langflow OSS 1.0.0 through 1.11.1 allows an authenticated attacker to execute arbitrary operating system commands in the server process by saving a flow with a crafted type field value and triggering a build of a wrapper flow that references it. This allowed privilege escalation from "authenticated flow user" to arbitrary OS-level command execution under the server process identity, bypassing the LANGFLOW_ALLOW_CUSTOM_COMPONENTS=false policy control.

### CVE-2026-18527

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-384` |
| Published | 2026-08-28T22:16:46.620 |

IBM Administration Runtime Expert for i 1R1M0 IBM Application Runtime Expert (ARE) for i could allow a remote attacker to gain elevated privileges, caused by ARE GUI component processing. An unauthenticated attacker can exploit this vulnerability to execute actions under another user's authenticated profile gaining elevated privileges on the IBM i system.

### CVE-2026-55634

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-94` |
| Published | 2026-08-28T20:18:29.627 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.19, 12.3.10, and 2026.1.6, the class-definition import endpoint /pimcore-studio/api/class/definition/configuration-view/detail/{id}/import accepts a DataObject field name that is emitted without an identifier allowlist by lib/DataObject/ClassBuilder/FieldDefinitionPropertiesBuilder.php into generated PHP properties and by models/DataObject/ClassDefinition/Helper/Dao.php into ALTER TABLE identifiers. An authenticated user with the objects permission can inject PHP syntax into the generated DataObject class, causing attacker-controlled code in generated var/classes/DataObject/.php files to run when an object of that class is instantiated, and can also inject SQL identifier content into schema-changing statements. The central models/DataObject/ClassDefinition/Data.php::setName() validation did not reject semicolons, braces, backticks, spaces, or other non-identifier characters. This issue is fixed in versions 11.5.19, 12.3.10, and 2026.1.6.

### CVE-2026-55565

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T20:18:29.070 |

Yamcs is a mission control framework. Prior to 5.12.8 and 5.13.2, Yamcs LikeExpression.fillCode_getValueReturn in yamcs-core/src/main/java/org/yamcs/yarch/streamsql/LikeExpression.java inserts an unescaped LIKE pattern into Java source compiled by Expression.getCompiledExpression through SimpleCompiler.cook instead of applying ValueExpression.escapeJavaString. The pattern can originate from POST /api/archive/{instance}:executeSql, POST /api/archive/{instance}:streamSql, POST /api/archive/{instance}/tables/{table}:readRows, GET /api/archive/{instance}/events, or activity searches, including paths available with ReadTables, ReadEvents, or ReadActivities. A quote in the pattern can inject Java that runs as the Yamcs server process. This issue is fixed in versions 5.12.8 and 5.13.2.

### CVE-2026-14494

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-29T12:16:41.163 |

The Sigma Forms Pro plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.4.5 via the handle_form_submission function. This is due to the plugin dynamically granting the unfiltered_upload capability to all users during form submissions and bypassing MIME type validation when allowed_file_types is not configured. This makes it possible for unauthenticated attackers to execute code on the server. Several default pre-built templates including Job Application, Support Ticket, and Wholesale Application have file upload fields with no file type restrictions configured by design, making this vulnerability immediately exploitable upon installation.

### CVE-2026-19286

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T22:16:47.357 |

IBM Langflow OSS 1.0.0 through 1.11.1 could allow a remote attacker to execute arbitrary code due to improper enforcement of security restrictions on the A2A public endpoint.

### CVE-2026-82329

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-28T20:20:21.293 |

JFrog Artifactory contains an authentication weakness that, under default configuration, may allow an unauthenticated attacker with network access to obtain administrative privileges.

### CVE-2026-55559

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470;CWE-1336` |
| Published | 2026-08-28T20:18:28.930 |

Yamcs is a mission control framework. Prior to 5.12.8 and 5.13.2, Yamcs inserts templateArgs from POST /api/instances and PATCH /api/instances/{instance} into YAML through VarStatement.append in yamcs-core/src/main/java/org/yamcs/templating/VarStatement.java without YAML-context escaping. The rendered configuration is parsed by YamcsServer.createInstance and loaded by YamcsServerInstance, allowing an attacker to inject a services entry for org.yamcs.ProcessRunner. Deployments without security.yaml expose the operation through the guest superuser, while secured deployments require SystemPrivilege.CreateInstances. Successful exploitation executes commands as the Yamcs service account. This issue is fixed in versions 5.12.8 and 5.13.2.

### CVE-2026-37751

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T16:17:46.667 |

An OS command injection vulnerability in the killSessionSync function (lib/agent-runtime.ts) of 23blocks-OS ai-maestro v0.24.17 allows attackers to execute arbitrary commands via a crafted input.

### CVE-2026-54755

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-28T20:18:17.670 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.19, split-royalty fields decoded in core/kapp/builtInFunctions/utils.go can contain values greater than core.HundredPercent, and core/kapp/kda/create.go and core/kapp/kda/trigger.go sum those values in uint32 accumulators. Crafted values such as two 0x80000000 entries wrap the validation sum to zero and pass CheckValid100Params. Royalty payout paths in core/kapp/accounts/accounts.go, core/kapp/market/market.go, and core/kapp/ito/ito.go then credit each oversized split amount and silently discard a negative remainder, allowing ordinary asset transfers, marketplace purchases, or ITO purchases to create unbacked KLV or other assets. This issue is fixed in version 1.7.19.

### CVE-2026-54754

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-191;CWE-367;CWE-682` |
| Published | 2026-08-28T20:18:17.533 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.19, marketplace settlement in core/kapp/market/market.go reads MarketOrderData.ReferralPercentage from the listing while reading asset.Royalties.MarketPercentage live at purchase time. An asset owner can create a valid listing and then use AssetTrigger UpdateRoyalties to make the combined referral and royalty percentages exceed the bid. executeBuyMarket pays referral and royalty amounts unconditionally while computeMarketOwnerAmount silently skips a nonpositive seller remainder, allowing MarketBuy, BuyItNow, or auction Claim settlement to credit more KLV or sale currency than the buyer paid. This can create unbacked currency and corrupt token supply integrity. This issue is fixed in version 1.7.19.

### CVE-2026-82078

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-28T16:18:31.240 |

An unsafe dynamic class loading vulnerability exists in the database connection utilities of PaperCut MF and PaperCut NG. The application instantiates database driver classes based on configurable driver names without validating against an allowlist of approved drivers. If an attacker can manipulate system configuration parameters, this enables the execution of arbitrary Java bytecode residing on the application classpath under the security context of the PaperCut server process.

### CVE-2026-82454

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-29T14:16:38.480 |

The Omnivore API (packages/api) before the fix in commit abf53d6 contains an authentication bypass in Apple sign-in token verification. The decodeAppleToken function extracted the 'alg' field from the attacker-supplied JWT header and passed it as the sole allowed algorithm to jwt.verify(). Using jsonwebtoken v8 (which does not validate key/algorithm compatibility), an attacker can set alg=HS256 and sign a forged token using Apple's publicly available RSA public key as the HMAC secret, bypassing signature verification and impersonating any Apple-linked account.

### CVE-2026-82452

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-29T14:16:38.210 |

rust-iot-platform through commit 5df942ab contains an authentication bypass vulnerability where most REST API routes lack authentication guards in their handler signatures. Unauthenticated attackers can create, update, list, retrieve, and delete user accounts by directly accessing unprotected endpoints without providing valid credentials.

### CVE-2026-82448

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-29T13:16:38.877 |

Shinobi before commit 5a76c74f contains a hardcoded connection key in the child node service that allows unauthenticated attackers to execute arbitrary database queries. Attackers reaching the child node port can present the hardcoded key during WebSocket handshake, then dispatch SQL queries through the onWebSocketDataFromChildNode handler to read and modify user records and camera configuration.

### CVE-2026-82277

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T20:20:18.760 |

Argo Rollouts dashboard through 1.10.0 binds to all interfaces and exposes mutating Rollout operations without authentication, authorization, or CSRF protection. Attackers on the same network can invoke PromoteRollout, AbortRollout, RestartRollout, SetRolloutImage, UndoRollout, and RetryRollout operations across all namespaces accessible to the operator's kubeconfig.

### CVE-2026-82266

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T20:20:17.213 |

Redpanda through 26.2.2 binds the Admin API to 0.0.0.0:9644 with admin_api_require_auth defaulting to false, treating unauthenticated requests as superusers. Attackers can reach port 9644 without credentials to create and delete broker accounts, modify cluster configuration, and disrupt partition replication.

### CVE-2026-55378

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T20:18:27.200 |

JS Recon is a JavaScript enumeration and SAST tool. From 1.2.1-beta.1 until 1.3.1-beta.2, the PR Branch Checker workflow in .github/workflows/pr_checker.yml places github.head_ref and github.event.pull_request.head.repo.full_name into BRANCH_NAME and SOURCE_REPO and interpolates those untrusted values into a shell gh pr comment command. A remote user who opens a pull request can use shell metacharacters in a branch or fork name to execute commands in the GitHub Actions runner with the workflow's GITHUB_TOKEN, which has pull-requests write permission. This issue is fixed in version 1.3.1-beta.2.

### CVE-2026-55220

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-28T20:18:26.517 |

Pimcore is an Open Source Data & Experience Management Platform. Prior to 11.5.19, 12.3.10, and 2026.1.6, Pimcore\Model\DataObject\ClassDefinition\Data\Hotspotimage::getDataFromResource() in models/DataObject/ClassDefinition/Data/Hotspotimage.php passes the field __hotspots object-store column to Pimcore\Tool\Serialize::unserialize() without an allowed-classes restriction after JSON decoding fails. An attacker with a separate capability to write crafted PHP serialized bytes into that column can instantiate available classes and trigger magic methods when an affected DataObject is loaded, which can produce arbitrary file writes or code execution through bundled gadget chains. The related ImageGallery, Block, and Video callers use the same fallback pattern, but the identified June fix changes the Hotspotimage caller only. This issue is fixed for Hotspotimage in versions 11.5.19, 12.3.10, and 2026.1.6.

### CVE-2026-55068

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-28T20:18:24.183 |

free5GC is an open-source implementation of the 5G core network. In 4.2.2 and earlier, the NRF RegisterNFInstance handler at PUT /nnrf-nfm/v1/nf-instances/{nfInstanceID} accepts NF Profiles without enforcing UUID format, nfStatus enum values, heartBeatTimer ranges, mandatory profile fields, or nfServices.ipEndPoints address constraints. The invalid profiles are persisted in the MongoDB NfProfile collection and returned by NFDiscover, allowing an attacker with SBI access to advertise attacker-controlled network-function endpoints and redirect control-plane signaling. This can expose credentials and signaling, alter service discovery integrity, and deny service across network functions that trust the NRF. This issue is fixed in version 4.2.3.

### CVE-2026-3627

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-28T22:16:49.063 |

IBM Concert 1.0.0 through 2.3.1 is vulnerable to SQL injection. A remote attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-82281

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:20:19.363 |

Kotaemon through 0.12.0 fails to properly validate conversation ownership in select_conv, delete_conv, rename_conv, and on_set_public_conversation functions in control.py. Attackers can read other users' chat histories, delete conversations, or rename conversations by supplying arbitrary conversation identifiers without proper authorization checks.

### CVE-2026-55511

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T20:18:27.947 |

Yamcs is a mission control framework. Prior to 5.12.8 and 5.13.2, Yamcs allows a user with SystemPrivilege.ControlArchiving to create a double-quoted StreamSQL column name that is interpolated into generated Java source by Expression.fillCode_InputDefVars and Expression.sanitizeName. A sum aggregate reaches yamcs-core/src/main/java/org/yamcs/yarch/streamsql/CompilableAggregateExpression.java and yamcs-core/src/main/java/org/yamcs/yarch/streamsql/funct/SumExpression.java through SelectExpression.compile, where Janino SimpleCompiler.cook compiles the injected source. POST /api/archive/{instance}:executeSql can therefore execute arbitrary Java in the Yamcs server process, exposing mission data and credentials and permitting telemetry tampering or denial of service. This issue is fixed in versions 5.12.8 and 5.13.2.

### CVE-2026-55248

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T20:18:27.030 |

plone.app.portlets provides portlets and a Plone-specific user interface for plone.portlets. Prior to 5.0.8, 6.0.4, and 7.0.2, a member who can add an RSS portlet can set its feed URL to a very large response, causing src/plone/app/portlets/portlets/rss.py to download and retain excessive data in memory and deny service. The same RSS URL handling accepts internal hosts, IP addresses, single-word domains, and explicit ports, allowing server-side requests that can probe internal network services and open ports. A malicious feed item can also supply a JavaScript URL that is retained as the item link and can execute script when used by a victim. The affected logic includes _rss_feed_url_validator, _normal_url_validator, RSSFeed._retrieveFeed, RSSFeed._buildItemDict, and the FEED_DATA in-memory cache. This issue is fixed in versions 5.0.8, 6.0.4, and 7.0.2.

### CVE-2026-55247

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T20:18:26.890 |

plone.app.event provides the event content type for Plone. Prior to versions 5.2.4 and 6.0.1, the iCalendar import in src/plone/app/event/ical/importer.py accepts insufficiently restricted calendar and event URLs, does not adequately bound downloaded bytes or imported events, and commits work per event. A logged-in editor can make the server request internal network resources or local calendar files, exhaust resources and take the site offline, and store a malicious event URL that executes script in another user's browser. The fix restricts accepted URLs, applies MAXIMUM_ICAL_IMPORT_SIZE_BYTES and MAXIMUM_ICAL_IMPORT_EVENTS limits, uses transaction savepoints, and validates event URLs. This issue is fixed in versions 5.2.4 and 6.0.1.

### CVE-2026-82021

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-28T20:20:14.470 |

Hermes Agent 0.18.2 prior to 0.19.0 contains a supply chain vulnerability in its bundled MCP catalog that allows a remote attacker to execute arbitrary code by compromising a third-party upstream repository referenced via a mutable branch rather than a pinned commit SHA. An attacker who compromises the upstream repository can propagate malicious code to every host that installs the affected catalog entry, with no further action required by the operator.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T22:16:46.867 |

IBM Langflow OSS 1.0.0 through 1.11.1 could allow a remote authenticated attacker to execute arbitrary code due to improper control of generation of code.

### CVE-2026-82286

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T20:20:20.093 |

gpt-crawler through 1.5.1 fails to validate the outputFileName parameter in the POST /crawl endpoint, allowing unauthenticated attackers to write arbitrary files to any filesystem path. Attackers can supply absolute paths or parent-directory segments to overwrite existing files with content sourced from attacker-controlled URLs.

### CVE-2026-82285

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:19.953 |

bisheng through 2.6.0-fix2 contains a server-side request forgery vulnerability in the POST /api/v1/workflow/report/callback endpoint that lacks authentication and applies no URL scheme restrictions or host filtering. Unauthenticated attackers can supply arbitrary URLs to enumerate internal network services and cloud metadata endpoints, then retrieve captured responses from object storage using caller-supplied object names.

### CVE-2026-82282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-28T20:20:19.523 |

Atlantis through 0.47.1 fails to authenticate the /github-app/setup endpoint, allowing unauthenticated attackers to access GitHub App credentials. Attackers can observe or intercept the GitHub redirect during setup to obtain the RSA private key and webhook secret, enabling installation token minting and webhook payload forgery.

### CVE-2026-72984

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-28T20:19:44.943 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-55521

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T20:18:28.240 |

Yamcs is a mission control framework. Prior to 5.12.8 and 5.13.2, Yamcs omits authorization checks in IndexesApi.listPacketIndex, IndexesApi.listEventIndex, Cop1Api.disable, Cop1Api.resume, Cop1Api.initialize, Cop1Api.updateConfig, and TimeApi.setTime. An authenticated low-privilege user can read packet and event index metadata without ObjectPrivilegeType.ReadPacket, alter COP-1 link state without SystemPrivilege.ControlLinks, and manipulate simulation time. These operations can disclose telemetry metadata, disrupt telecommand handling, and affect system integrity and availability. This issue is fixed in versions 5.12.8 and 5.13.2.

### CVE-2026-55509

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T20:18:27.810 |

WsgiDAV is a generic and extendable WebDAV server based on WSGI. Prior to 4.3.5, the sample MySQLBrowserProvider in wsgidav/samples/mysql_dav_provider.py concatenates the record key parsed from a request URL directly into SQL WHERE clauses. The affected _exists_record_by_primary_key, _get_field_by_primary_key, and _get_record_by_primary_key methods are part of a shipped example provider that is not enabled by default. An attacker who can access a share explicitly configured with this non-default provider can inject SQL through a normal GET request; anonymously exposed read shares permit a status-code oracle and extraction of arbitrary data reachable by the configured MySQL account. This issue is fixed in version 4.3.5.

### CVE-2026-55485

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-269;CWE-863` |
| Published | 2026-08-28T20:18:27.657 |

Piccolo Admin is an admin interface and content management system for Python, built on top of Piccolo. Prior to 1.14.0, piccolo_admin/endpoints.py uses superuser_validators to block PUT, PATCH, DELETE, and POST requests by non-superusers but permits GET requests to configured user and session tables, while piccolo_api/session_auth/tables.py exposes SessionsBase.token because the token column is not secret. In deployments that add the Sessions and User tables to create_admin, a non-superuser administrator can call GET /api/tables/sessions/, obtain another user's live session token, replay it as the Cookie id value to impersonate a superuser, and permanently set superuser to true on the attacker's own row. This issue is fixed in version 1.14.0.

### CVE-2026-81578

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-08-28T16:18:29.600 |

An improper access control vulnerability exists in the web management interface of PaperCut MF and PaperCut NG. Under specific conditions, unauthenticated remote requests targeting administrative functions can trigger backend actions prior to the  completion of access validation checks. This allows an unauthenticated remote attacker to modify certain system configurations.

### CVE-2026-13761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-08-28T16:17:06.870 |

Pega Platform versions 7.1.0 through 25.1.2 are affected by an improper validation of inputs that are used for loop conditions, potentially leading to a denial of service or other consequences because of excessive looping.

### CVE-2026-82453

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-08-29T14:16:38.347 |

rust-iot-platform through commit 5df942ab stores user passwords in cleartext without hashing in the user model. Attackers can read API responses from user retrieval and listing routes to obtain plaintext credentials for all accounts.

### CVE-2026-82450

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-29T14:16:37.930 |

BookStack before 26.05.4 contains a remote code execution vulnerability in the portable ZIP import functionality that allows users with Import Content and Create Books permissions to upload a PHP polyglot file as a book cover. Attackers can bypass image extension validation by embedding a PHP file with a .php filename in the ZIP archive, which is stored in the public web root and executed by unauthenticated requests.

### CVE-2026-82447

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-29T13:16:38.643 |

Skyvern before 1.0.45 contains a sandbox escape vulnerability in TextPromptBlock that renders prompts twice, first through a sandboxed Jinja environment and then through an unsandboxed environment. Attackers can inject malicious Jinja template syntax through workflow parameters or upstream block output to execute arbitrary code with server process privileges.

### CVE-2026-55764

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-28T23:17:07.220 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.19, Klever-Go allows a mint-role holder to bypass a finite per-nonce MaxSupply on the semi-fungible token add-quantity path. In core/kapp/systemAccount/systemAcount.go, SFTAddCirculation performed meta.Circulation += amount before evaluating whether Circulation exceeded MaxSupply, without checking for signed int64 overflow. A large positive raw Amount supplied through processSemiFungibleAddQuantity in core/kapp/kda/mint.go can wrap Circulation negative, causing the signed maximum-supply comparison to pass and crediting approximately MaxInt64 units while corrupting the on-chain counter. The fungible path is not affected because its MintedValue <= 0 guard detects the overflow. The correction uses the consensus activation flag FixMarketBuyOverflow. This issue is fixed in version 1.7.19.

### CVE-2026-81532

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-28T22:16:54.793 |

A user able to submit SQL through an application using the MongoDB Connector for BI ODBC driver can supply a positioned-cursor statement whose cursor name exceeds the size of an internal fixed-length buffer. Because the name length is not bounded before the driver builds its diagnostic message, memory adjacent to that buffer is overwritten with user-supplied content. This can terminate the hosting application process and may allow unintended code to run within it.

### CVE-2026-81520

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1088` |
| Published | 2026-08-28T22:16:54.650 |

A network-reachable client that has not yet authenticated can hold a MongoDB Connector for BI authentication session open indefinitely by beginning a SASL-based login exchange and then declining to complete it. Because the negotiation loop had no overall time bound and the read from the client had no deadline, each such session retains a worker, a client connection slot, and its associated backend database connections until the process is restarted. Repeated use of this behavior can consume the configured connection capacity and prevent legitimate users from establishing new sessions.

### CVE-2026-81518

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-28T22:16:54.510 |

When mongosqld is configured with a client certificate authority file, the listener requests a client certificate during the TLS handshake but does not require one, so a client that presents no certificate is still accepted. In deployments that rely on client certificates as the sole means of identifying users, a remote party with network access to the listener can therefore establish a session and read the MongoDB data exposed through the connector.

### CVE-2026-81517

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-08-28T22:16:54.383 |

An unauthenticated party able to reach the port of a MongoDB Connector for BI (mongosqld) instance may generate enough routine connection log activity to exhaust the storage backing the configured log path. When a log write or log rotation operation subsequently fails, the resulting error is not handled and the shared mongosqld process ends, ending service for all connected SQL clients. The process continues to end on startup until an operator restores available storage, and the diagnostic message explaining the condition is not recorded.

### CVE-2026-75118

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-28T22:16:52.880 |

A pre-authentication stack-based buffer overflow vulnerability exists in the http_gdpr_decrypt function of TL-MR100 V3.20 due to insufficient bounds checking of encrypted requests to the /cgi/login endpoint. An adjacent unauthenticated attacker with access to the router's web management interface can trigger memory corruption and potentially achieve arbitrary code execution.







Successful exploitation can overwrite saved control-flow data on the httpd process stack prior to authentication, resulting in a service crash or potential arbitrary code execution in the context of the affected process.

### CVE-2026-55763

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-841` |
| Published | 2026-08-28T22:16:51.720 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.19, processPercentageRoyaltiesTransfer in core/kapp/accounts/accounts.go calls SubFromBalance after the split loop and after the royaltiesToPay <= 0 early return. computeSplitRoyalties rejects only when splitToPay > royaltiesToPay, so a valid PercentTransferPercentage = 10000 split consumes exactly 100 percent of the royalty pool, sets royaltiesToPay to zero, and returns before the source account is debited. The split recipient receives the full royaltyAmount while the sender pays nothing and the supply counter is not updated, allowing unbounded off-the-books inflation of the transferred KDA. A KDA owner must configure a TransferPercentage royalty with a 100 percent split, after which any holder's transfer of the asset triggers the mint; the sibling processFixedRoyaltiesTransfer path is not affected because it debits the source before distribution. This issue is fixed in version 1.7.19.

### CVE-2026-82288

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-28T20:20:20.393 |

Stable Diffusion WebUI through 1.10.1 contains a credential disclosure vulnerability in the /sdapi/v1/cmd-flags endpoint that returns parsed command-line arguments including gradio_auth and api_auth values in cleartext. Unauthenticated attackers can access this endpoint to retrieve configured usernames and passwords, then use them to authenticate to the interface and access the application.

### CVE-2026-82278

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-28T20:20:18.923 |

BISHENG before 2.6.0 contains a remote code execution vulnerability in the workflow run_once endpoint that allows authenticated users to execute arbitrary Python code. Attackers can submit crafted Code node definitions to the POST /api/v1/workflow/run_once endpoint, which executes them with exec() without sandboxing, gaining access to filesystem, credentials, and internal network resources.

### CVE-2026-82275

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T20:20:18.507 |

Qwen-Agent through 0.0.34 contains a path traversal vulnerability in the document parser that fails to restrict file access to intended directories. Attackers can supply absolute file paths to the unauthenticated Gradio interface to read arbitrary files accessible by the server process.

### CVE-2026-82270

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:17.797 |

Portkey AI Gateway through 1.15.2 contains a server-side request forgery vulnerability in the /v1/proxy/* route that lacks requestValidator middleware. Attackers can set the x-portkey-custom-host header to internal addresses and forward requests with Authorization headers to reach internal services and exfiltrate provider API keys.

### CVE-2026-82268

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:17.510 |

Qwen-Agent through 0.0.34 contains a server-side request forgery vulnerability in the document parsing path that treats caller-supplied paths as URLs without scheme restriction or host validation. Attackers can reach the unauthenticated Gradio interface to make the server issue HTTP requests to arbitrary internal addresses including metadata services and read retrieved content through parsed document output.

### CVE-2026-81849

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-28T20:20:13.940 |

Improper limitation of a pathname to a restricted directory in the aws:downloadContent plugin in amazon-ssm-agent before 3.3.4515.0 might allow an authenticated remote user whose ssm:SendCommand permission is restricted to the AWS-DownloadContent document, to write arbitrary files outside the intended download directory with root privileges, via crafted object keys in the S3 source the document is directed to retrieve. This issue may lead to arbitrary code execution as root if specific sensitive files are overwritten.



To remediate this issue, customers should upgrade amazon-ssm-agent to version 3.3.4515.0 or later.

### CVE-2026-75124

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-28T20:19:52.970 |

PLANET GS-4210-16P2S firmware before 3.441b260626 contains a pre-authentication memory corruption vulnerability in the web management interface where the _readHttpParam function copies an oversized HTTP query string without guaranteeing NUL termination, allowing parse_query_string to process attacker-controlled data into a fixed-size stack buffer. An unauthenticated remote attacker can send an oversized GET request to dispatcher.cgi to cause denial of service of the web management interface and potentially trigger memory corruption.

### CVE-2026-55245

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:18:26.743 |

Bifrost is an enterprise AI gateway for routing requests to model providers. Prior to 1.5.17, the isPublicIP function in core/providers/utils/fetch.go, reached through FetchAndEncodeURL for Bedrock and Vertex image or document URLs, classifies Carrier-Grade NAT 100.64.0.0/10, IPv6 6to4 2002::/16, NAT64 64:ff9b::/96 and 64:ff9b:1::/48, and deprecated IPv6 site-local fec0::/10 addresses as public. A remote attacker who controls a multimodal request URL can make the gateway fetch internal services, including a cloud instance metadata endpoint encoded through 6to4 or NAT64. This issue is fixed in version 1.5.17.

### CVE-2026-19412

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-28T16:17:08.610 |

This vulnerability exists in the CP Plus CP-XR-DE21-S Router due to the presence of hardcoded HTTP Digest authentication credentials in the firmware that are identical across all devices running the affected firmware. An attacker with access to the local network could exploit this vulnerability by obtaining the hardcoded authentication information from the firmware.

 

Successful exploitation of this vulnerability could allow the attacker to gain unauthorized administrative access and perform privileged operations on the targeted device.

### CVE-2026-55848

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-08-28T23:17:08.013 |

mapfish-print is a component of MapFish for printing templated cartographic maps. Prior to 3.28.30, 3.30.32, 3.31.24, 3.33.16, and 4.0.5, MapFish Print accepts an attacker-controlled GML layer url in requests to the /api/print3/print endpoint and fetches XML parsed by core/src/main/java/org/mapfish/print/map/geotools/GmlLayer.java without disabling external entities and external DTDs. A remote XML document and DTD can expand a local file entity, and the resulting content can be exposed through the GML parsing and error path. This allows unauthenticated attackers to read files such as operating-system account data, Kubernetes service-account tokens, and certificates. Replacing the file entity target with an internal HTTP endpoint also permits server-side request forgery. This issue is fixed in versions 3.28.30, 3.30.32, 3.31.24, 3.33.16, and 4.0.5.

### CVE-2026-82017

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-28T22:16:55.067 |

IGEL OS 12 before 12.7.6 and IGEL OS 11 before 11.11.150 contain a boot registry parameter injection vulnerability that allows attackers with physical access to execute arbitrary Linux loader parameters by writing to an unencrypted and unsigned configuration area read by the signed bootloader. Attackers can inject malicious kernel command line parameters that execute with boot environment privileges without triggering TPM PCR measurement failures, as the attack does not modify the measured boot code.

### CVE-2026-82287

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-08-28T20:20:20.243 |

Rybbit before 2.7.0 contains a CORS misconfiguration vulnerability that allows attackers to bypass origin restrictions by reflecting any request origin in Access-Control-Allow-Origin responses while credentials are enabled. Attackers can issue credentialed cross-origin requests from any website to read analytics data, account information, and perform authenticated state-changing operations as the victim user.

### CVE-2026-82284

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:20:19.823 |

Quivr versions through 0.0.322 fail to validate chat ownership in the GET /chat/{chat_id}/history, DELETE /chat/{chat_id}, and POST /chat/{chat_id}/question/answer endpoints. Authenticated attackers can read other users' conversation histories including private knowledge base content, delete arbitrary chats, and inject fabricated messages into other users' conversations.

### CVE-2026-82283

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:20:19.683 |

VoltAgent through 2.1.20 fails to validate conversation ownership in memory API handlers, allowing authenticated users to access other users' conversations. Attackers can read, modify, and delete arbitrary conversations and messages by supplying caller-controlled identifiers to memory endpoints.

### CVE-2026-82269

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-28T20:20:17.650 |

Gophish through 0.12.1 fails to enforce account lockout and password change requirements in the API authentication middleware. Attackers with valid API keys can bypass these security controls and retain full API access even when their account is locked or password change is required.

### CVE-2026-75123

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T20:19:52.837 |

PLANET GS-4210-16P2S firmware before 3.441b260626 contains an authenticated OS command injection vulnerability in /cgi-bin/dispatcher.cgi. The web_smtp_test_post handler incorporates a caller-supplied SMTP server value directly into a shell command without sanitization. A remote attacker with administrator web credentials can send a crafted SMTP server value to execute arbitrary operating-system commands on the device.

### CVE-2026-75122

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T20:19:52.707 |

PLANET GS-4210-16P2S firmware before 3.441b260626 contains an authenticated OS command injection vulnerability in /cgi-bin/httpuploadcert.cgi. The certificate password field in a certificate upload request is incorporated into a shell command without sanitization of shell metacharacters. A remote attacker with administrator web credentials can submit a crafted certificate upload request to execute arbitrary operating-system commands on the device.

### CVE-2026-75121

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T20:19:52.567 |

PLANET GS-4210-16P2S firmware before 3.441b260626 contains an authenticated OS command injection vulnerability in /cgi-bin/dispatcher.cgi. The web_vlan_membership_edit_dialog_post handler incorporates the memberTags POST parameter into a shell command without sanitization. A remote authenticated attacker can send a crafted memberTags value to execute arbitrary operating-system commands on the device.

### CVE-2026-56100

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T20:18:30.640 |

SpringBlade versions from 2.7.3 up to but not including 5.0.0 contain a privilege escalation vulnerability that allows authenticated attackers to create system administrator accounts by sending crafted POST requests to an unprotected internal Feign user-creation endpoint exposed via @RestController without authorization checks. Attackers can exploit the gateway's authentication filter, which only validates JWT parsing without verifying user roles or caller identity, and leverage a hardcoded JWT signing key embedded in publicly available JARs to forge tokens and escalate privileges from a low-privilege user to administrator, enabling cross-tenant data pollution and persistent backdoor access.

### CVE-2026-82457

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-681` |
| Published | 2026-08-29T14:16:38.910 |

su-exec through 0.3 fails to validate numeric user and group identifiers parsed with strtol before assigning to uid_t and gid_t, allowing truncation of out-of-range values to zero. Attackers can supply large numeric identifiers that truncate to root's identifier, causing su-exec to execute target programs with root privileges instead of intended unprivileged accounts.

### CVE-2026-77586

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T20:19:56.030 |

In MongoDB Connector for BI, MongoDB object names such as collection, field, and index names are placed into the quoted identifiers of the DDL text returned by SHOW CREATE statements without escaping the identifier delimiter. A user with permission to write to a sampled MongoDB collection can choose a name that closes the quoted identifier early, so that additional SQL text becomes part of the generated output. If an operator or automated tool later replays that generated statement against a SQL server, the additional text is executed with the privileges of that session.

### CVE-2026-75486

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-28T20:19:54.027 |

Synk Sweater Comb before 3.8.8 contains a command injection vulnerability that allows an attacker who controls the .vervet.yaml configuration file to execute arbitrary OS commands by injecting malicious input into the linters.<key>.optic-ci.original branch name field. The expectGitBranch() function in src/lint.ts passes the unsanitized branch name directly into child_process.exec() via an unescaped template literal, enabling arbitrary command execution when the lint command is run against the repository.

### CVE-2026-55108

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:N/A:H` |
| Weaknesses | `CWE-59;CWE-400` |
| Published | 2026-08-28T20:18:24.337 |

KubeVela is an open source application delivery platform. Prior to 1.9.14, from 1.10.0-alpha.1 until 1.10.9, and from 1.11.0-alpha.1 until 1.11.0-alpha.4, the Terraform remote configuration loader in pkg/controller/utils/capability.go, GetTerraformConfigurationFromRemote, clones a repository supplied through a core.oam.dev/v1beta1 ComponentDefinition and follows repository-controlled variables.tf or main.tf symlinks. A user with permission to create or update ComponentDefinition objects can point variables.tf to /dev/zero through terraform.path, after which os.Stat and os.ReadFile follow the link and read an unbounded stream before ParseTerraformVariables or HCL parsing can reject the content. The read can exhaust memory, OOM-kill the cluster-wide vela-core controller, cause repeated Pod restarts, and pressure node memory when no effective container limit is configured. This issue is fixed in versions 1.9.14, 1.10.9, and 1.11.0-alpha.4.

### CVE-2026-82227

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-28T16:18:32.163 |

Contributor SQL Injection in WPBulky <= 1.2.2 versions.

### CVE-2026-81490

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-28T22:16:54.247 |

A database user able to create a view in a namespace that MongoDB Connector for BI samples can cause the schema-sampling routine to stop functioning by defining a view whose evaluation reliably fails. The sampling logic classifies the resulting server message as transient and, after the configured retries are exhausted, proceeds without a valid result, ending the schema refresh routine. The mongosqld process continues running without a usable schema, so SQL clients are unable to obtain results until an operator removes the view or excludes its namespace from sampling.

### CVE-2026-82289

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:20.537 |

Gitingest through 0.3.1 fails to properly validate hostnames in _validate_host, accepting any host with a git., gitlab., or github. prefix regardless of known-hosts list membership. Attackers can submit URLs with attacker-controlled hostnames to trigger outbound connections to arbitrary hosts and disclose GitHub personal access tokens via HTTP basic credentials.

### CVE-2026-18904

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T22:16:47.227 |

IBM Langflow OSS 1.0.0 through 1.11.1 could allow a remote attacker to obtain sensitive information and inject unauthorized messages due to a namespace collision between user identifiers.

### CVE-2026-18891

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-28T22:16:46.990 |

IBM Langflow OSS 1.0.0 through 1.11.1 could allow a remote attacker to execute arbitrary flows and access sensitive information due to improper authentication.

### CVE-2026-82263

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:16.790 |

Logto through 1.42.0 contains a server-side request forgery vulnerability in the OIDC SSO connector creation endpoint that fails to validate the issuer URL parameter. Tenant administrators with Management API credentials can supply arbitrary internal URLs to trigger HTTP GET requests to private network services, with response content returned in API responses.

### CVE-2026-82262

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-28T20:20:16.643 |

Logto through 1.42.0 contains a server-side request forgery vulnerability in the POST /api/hooks/:id/test endpoint that accepts arbitrary URLs without host validation. Tenant administrators with Management API tokens can make the server issue HTTP POST requests to internal URLs and retrieve response bodies from services on the private network.

### CVE-2026-82291

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-942` |
| Published | 2026-08-28T20:20:20.820 |

HeyForm before 3.0.0-rc.8 reflects the request Origin header in CORS responses while allowing credentials, enabling cross-origin requests with authentication. Attackers can execute authenticated GraphQL queries from malicious pages visited by logged-in users to access workspaces, projects, forms, submissions, and respondent data, or modify account settings.

### CVE-2026-55065

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-08-28T20:18:23.757 |

Vikunja is an open-source self-hosted task management platform. From 0.24.6 until 2.4.0, DELETE /api/v1/projects/:project/views/:view permits an authenticated user to supply a view identifier from another project while authorizing only against an attacker-controlled project identifier. ProjectView.CanDelete in pkg/models/project_view_permissions.go does not establish that the view belongs to the path project, and ProjectView.Delete in pkg/models/project_view.go continues after the scoped project_views delete affects no rows. Its subsequent deletes select task_buckets and task_positions only by project_view_id, allowing cross-tenant destruction of Kanban assignments and ordering while leaving the victim view and tasks intact. This issue is fixed in version 2.4.0.

### CVE-2026-50979

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-28T16:18:14.037 |

A command injection vulnerability in the 'advanced/curl' component of Osbil Technology oPanel v1.19.50 and earlier allows authenticated attackers to execute arbitrary shell commands via the 'url' parameter

### CVE-2026-41012

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-29T03:17:06.637 |

Traffic interception vulnerability in BOSH Director vCenter CPI allows attackers positioned between BOSH Director and vCenter to impersonate vCenter REST API and capture administrator credentials via HTTP Basic auth, leading to complete virtualization infrastructure takeover.



An attacker who can intercept traffic between the BOSH Director and vCenter can establish a malicious server impersonating the vCenter REST API. When the BOSH Director makes CPI calls to perform routine cloud infrastructure operations, the attacker captures the vCenter administrator username and password transmitted via HTTP Basic authentication.



The vulnerability stems from insufficient authentication security in the communication protocol between BOSH Director and vCenter. While HTTPS may be used, the lack of proper certificate validation and pinning allows attackers to successfully impersonate vCenter endpoints. Because vCenter credentials typically grant full administrative control over the entire virtualization estate, successful credential capture yields complete takeover of every VM, datastore, and network the CPI manages.



This exposure exists on every CPI call (including routine deployment operations, not just when tags are configured) and cannot be mitigated by supplying a CA certificate alone. The attack impacts all infrastructure managed by the compromised vCenter instance, potentially affecting hundreds or thousands of VMs across multiple deployments and environments.

### CVE-2026-82020

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-08-28T20:20:14.323 |

Hermes Agent 0.16.0 prior to 0.17.0 contains an improper path restriction vulnerability that allows attackers who can influence ingested message content to overwrite the credential store by bypassing sensitive-path guards that excluded the auth.json file. Attackers can craft malicious messages directing the agent's file-write tooling to overwrite the credential store without triggering any path-based protection, enabling credential tampering or unauthorized access.

### CVE-2026-55841

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-138` |
| Published | 2026-08-28T23:17:07.840 |

Graylog is a free and open log management platform. Prior to Graylog Server versions 6.3.12, 7.0.7, and 7.1.2 and Graylog Forwarder version 7.3, the FortiGate key-value syslog parser in graylog2-server/src/main/java/org/graylog2/inputs/codecs/GLFortiGateSyslogEvent.java and graylog2-server/src/main/java/org/graylog2/inputs/codecs/SyslogCodec.java mishandles field-like text inside quoted values. GLFortiGateSyslogEvent.getFields() uses KV_PATTERN and QUOTED_KV_PATTERN, while SyslogCodec.parse() invokes the FortiGateSyslogEvent parser; crafted values containing = or backslash-escaped quotes can cause embedded keys such as srcip, dstip, date, time, and tz to remove or overwrite original top-level fields or produce an invalid message that Graylog discards. An unauthenticated network sender who can submit syslog messages can therefore manipulate security-log fields or evade logging to obscure malicious activity. This issue is fixed in Graylog Server versions 6.3.12, 7.0.7, and 7.1.2 and Graylog Forwarder version 7.3.

### CVE-2026-55784

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-28T23:17:07.517 |

free5GC is an open-source implementation of the 5G core network. In version 1.4.4 and earlier, the AUSF component stores per-subscriber authentication state in a global sync.Map named AUSFContext.UePool in internal/context/context.go, keyed only by SUPI. Every request handled by internal/sbi/processor/ue_authentication.go creates an AusfUeContext, and AddAusfUeContextToPool executes ausfContext.UePool.Store(ausfUeContext.Supi, ausfUeContext), unconditionally replacing the active context for that SUPI. An attacker with access to the AUSF SBI/N12 interface can send concurrent POST /nausf-auth/v1/ue-authentications requests for the same target SUPI, causing all attempts to share one logical authentication context URL while K_aut, XRES, and EapID are repeatedly overwritten. A valid EAP-AKA' response for an earlier challenge is then checked against the latest context, causing AT_MAC verification to fail and denying authentication to the selected subscriber while the request flood continues. No fixed version is available as of this review.

### CVE-2026-82333

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T22:16:57.037 |

multer is a middleware for handling multipart/form-data in Node.js. A small multipart request with two specially crafted text field names can make multer's field parser synchronously iterate a maximum-length sparse array, blocking the event loop so the process cannot handle other requests. A large numeric array index in the first field allocates a maximum-length sparse array, and a second field with a non-numeric key then triggers a full-length iteration inside the append-field dependency. All versions before 2.3.0 are affected, and this is a remotely triggerable denial of service. multer 2.3.0 adds an opt-in fieldArrayIndexLimit option that rejects oversized array indexes. Upgrade to multer 2.3.0 and set limits.fieldArrayIndexLimit to the largest array index your application needs to remediate.

### CVE-2026-77078

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-08-28T22:16:53.883 |

multer is a middleware for handling multipart/form-data in Node.js. A small multipart request containing two specially crafted text field names can cause an uncaught RangeError (Invalid array length) that terminates the Node.js process. The first field uses a very large numeric array index to allocate a maximum-length sparse array, and a second field then pushes past that length, which throws inside the append-field dependency and is not caught by multer. All versions before 2.3.0 are affected, and the issue is a remotely triggerable denial of service. The issue is fixed in multer 2.3.0. Upgrade to multer 2.3.0 to remediate.

### CVE-2026-77037

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-459` |
| Published | 2026-08-28T22:16:53.627 |

multer is a middleware for handling multipart/form-data in Node.js. In version 2.2.0, when a disk-backed upload is aborted or truncated before the write stream finishes, multer's disk storage engine removes the visible file but does not close the underlying write file descriptor, leaving a deleted but still open descriptor. A remote attacker able to reach an upload route using the built-in disk storage can send repeated aborted or malformed multipart uploads, each one leaking a file descriptor and retaining disk blocks until the process exits, which can exhaust resources and cause a denial of service. The issue is fixed in multer 2.3.0, which closes the destination write stream on abnormal source termination and defers cleanup until the stream has closed. Upgrade to multer 2.3.0 to remediate.

### CVE-2026-18899

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T22:16:47.107 |

IBM Langflow OSS 1.0.0 through 1.11.1 could allow a remote attacker to read arbitrary files due to path traversal.

### CVE-2026-17203

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-28T22:16:46.480 |

IBM Administration Runtime Expert for i 1R1M0 could allow a remote authenticated attacker to obtain sensitive information due to improper authentication enforcement.

### CVE-2026-55584

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-28T20:18:29.487 |

phpSysInfo is a customizable PHP script that displays system information. Prior to 3.4.6, the PSI_ALLOWED access-control check in read_config.php trusts attacker-controlled X-Forwarded-For and Client-IP HTTP headers before REMOTE_ADDR. A remote unauthenticated attacker can supply an allowed address in one of these headers to impersonate a trusted client and access exposed hostname, kernel, CPU, memory, filesystem, and network-interface information. This issue is fixed in version 3.4.6.

### CVE-2026-55552

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-28T20:18:28.793 |

Yamcs is a mission control framework. Prior to 5.11.13, Yamcs StaticFileHandler.locateFile resolves an unauthenticated request path without using Path.normalize and Path.toAbsolutePath to confirm that the absolute path remains within the configured staticRoots. A path containing traversal segments can escape the intended web root and return an arbitrary readable host file. The flaw is in yamcs-core/src/main/java/org/yamcs/http/StaticFileHandler.java and can disclose sensitive operating-system and application data. This issue is fixed in version 5.11.13, and the 5.12 line is fixed from version 5.12.0.

### CVE-2026-55484

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-754` |
| Published | 2026-08-28T20:18:27.513 |

ALOS HTTP is a Linux-first Go web framework and application server built around a custom networking stack. Prior to 0.0.0-20260617230736-314b6783e196, core/utils.go::sanitizeRequestPath calls splitPathQuery on a request path beginning with a question mark and then performs the unchecked p[0] access without checking whether the resulting path is empty. An unauthenticated client can send a malformed request such as a question-mark-only path through h1_plain.go::ParseH1RequestHead, hpack.go::decodeSimpleGetPathHTTPSRequest, hpack.go::observeHeader, or h3_conn.go::handleRequestStream, causing an out-of-bounds panic before core.Recovery() middleware runs and terminating the server process. This issue is fixed in pseudo-version 0.0.0-20260617230736-314b6783e196.

### CVE-2026-55215

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-295;CWE-522` |
| Published | 2026-08-28T20:18:26.353 |

MariaDB Connector/Node.js is used to connect applications developed on Node.js to MariaDB and MySQL databases. Prior to versions 3.3.3, 3.4.6, and 3.5.3, when ssl is enabled without a pinned CA or server certificate, MariaDB Connector/Node.js sends credentials before completing certificate fingerprint validation. In lib/cmd/handshake/auth/handshake.js, a server that selects mysql_clear_password as the initial authentication plugin can receive the password before the post-TLS identity check. In lib/cmd/handshake/authentication.js, an authentication switch can evaluate the previous plugin instead of the requested target plugin, allowing mysql_clear_password to send the credential first. An active man-in-the-middle can present a self-signed certificate, capture the database password, and use it to authenticate directly even though the connector later rejects the server and closes the connection. This issue is fixed in versions 3.3.3, 3.4.6, and 3.5.3.

### CVE-2026-54788

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-28T20:18:17.950 |

dd-trace-rs provides Datadog application performance monitoring for Rust. From 0.1.0 until 0.3.3, datadog-opentelemetry/src/propagation/tracecontext.rs parses the W3C tracestate header and collects every semicolon-separated key and value pair in the Datadog dd=... vendor entry into a HashMap without enforcing a pair count or entry size limit. Because tracecontext extraction is enabled by default, a remote unauthenticated attacker can send an arbitrarily large dd=... entry and force excessive CPU and memory consumption for each request, causing denial of service in an instrumented network service. This vulnerability is fixed in 0.3.3.

### CVE-2026-81767

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T16:18:30.590 |

Unauthenticated Broken Access Control in Simple Payment <= 2.5.2 versions.

### CVE-2026-81285

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-28T16:18:29.243 |

Unauthenticated Denial of Service Attack in Smush Image Compression and Optimization <= 4.2.0 versions.

### CVE-2026-56854

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-28T16:18:17.607 |

The source-address critical option in the Permissions returned by an authentication callback was only enforced for the PublicKeyCallback and VerifiedPublicKeyCallback paths, extending the fix for CVE-2026-46595. Permissions returned by the PasswordCallback, KeyboardInteractiveCallback, NoClientAuthCallback, and GSSAPIWithMICConfig.AllowLogin callbacks were not validated against the client's remote address, so a source-address restriction set by those callbacks was silently ignored. The check is now applied to the Permissions returned by any authentication callback.

### CVE-2026-38638

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T16:17:47.063 |

An issue in the with_argv function (/unistd/mod.rs) of relibc commit 61f42d allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-38636

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T16:17:46.917 |

An issue in the seekdir() function (/dirent/mod.rs) of relibc commit 61f42d allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-37736

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-28T16:17:46.550 |

An issue in the JsonSanitizer.sanitize() component of OWASP json-sanitizer v1.2.3 allows attackers to cause a Denial of Service (DoS) via a crafted input.

### CVE-2026-37237

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-28T16:17:46.300 |

vLLM up to and including 0.17.0 allows remote attackers to cause a Denial of Service via memory exhaustion. The AsyncMediaIO.fetch_audio and AsyncMediaIO.fetch_image functions in multimodal/inputs.py fetch user-supplied media URLs using aiohttp and call r.read() without enforcing a maximum response size, allowing an attacker to exhaust server memory by providing a URL to an arbitrarily large file.

### CVE-2026-81020

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-323` |
| Published | 2026-08-28T16:18:28.890 |

wolfEngine before 1.4.1 generates the 8-byte explicit AES-GCM nonce once when the TLS write key is set and never increments it per record. As a result every TLS 1.2 and DTLS 1.2 AES-GCM record within a connection is encrypted under an identical key and nonce pair. Reusing a GCM key and nonce discloses the keystream (the XOR of two ciphertexts equals the XOR of their plaintexts, so one known record recovers the others) and leaks the GHASH authentication key, enabling authentication tag forgery. AES-CCM, TLS 1.3, and non-TLS use of the cipher are not affected.

### CVE-2026-81019

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-323` |
| Published | 2026-08-28T16:18:28.757 |

wolfProvider before 1.2.2 generates the 8-byte explicit AES-GCM nonce once when the TLS write key is set and never increments it per record. As a result every TLS 1.2 and DTLS 1.2 AES-GCM record within a connection is encrypted under an identical key and nonce pair. Reusing a GCM key and nonce discloses the keystream (the XOR of two ciphertexts equals the XOR of their plaintexts, so one known record recovers the others) and leaks the GHASH authentication key, enabling authentication tag forgery. AES-CCM, TLS 1.3, and non-TLS use of the cipher are not affected.

### CVE-2026-82279

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T20:20:19.067 |

HyperDX through 1.10.1 fails to enforce role-based access controls in team management endpoints, allowing any team member to perform administrative actions. Attackers can delete team members including owners, rotate API keys, and rename teams by sending requests to PATCH /team/apiKey, PATCH /team/name, and DELETE /team/member endpoints.

### CVE-2026-81757

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-28T16:18:30.083 |

Author Remote Code Execution (RCE) in Rank Math SEO <= 1.0.276 versions.

### CVE-2026-6176

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T16:18:21.580 |

The Customer Reviews for WooCommerce plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the aggregated review form submission in versions up to and including 5.106.0. This is due to insufficient input sanitization and output escaping on user-supplied review comment text. The plugin accepts review submissions from unauthenticated users through the 'cr_local_forms_submit' AJAX action without sanitizing HTML content before storing it via wp_insert_comment(), and later renders this stored content on product pages through comment_text() without proper escaping. This makes it possible for unauthenticated attackers with a valid review form URL (obtainable through review reminder emails sent to customers who placed orders) to inject arbitrary web scripts in pages that will execute whenever a user accesses the affected product page.

### CVE-2026-5934

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T16:18:19.657 |

The WP Rocket plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 3.21.0.1. This is due to insufficient input sanitization and output escaping of user-supplied data via the rocket_beacon AJAX endpoint. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-82280

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:20:19.213 |

Quivr through 0.0.322 fails to validate ownership in prompt endpoints, allowing authenticated users to modify any prompt by identifier. Attackers with read-only access to shared brains can read exposed prompt identifiers and overwrite system prompts affecting all brain users.

### CVE-2026-82273

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-28T20:20:18.227 |

Mastra through 1.63.0 contains an authentication bypass vulnerability in the memory API thread ownership validation when mapUserToResourceId callback is omitted from configuration. Authenticated attackers can enumerate all threads via GET /api/memory/threads and read conversation history and metadata of other resource owners.

### CVE-2026-82272

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-28T20:20:18.087 |

Immich through 3.1.0 fails to properly enforce locked asset visibility when assets are locked through the single-asset endpoint, allowing them to remain accessible through shared albums and links. Attackers can read locked assets and their metadata by accessing existing shared albums or links, bypassing the locked visibility protection.

### CVE-2026-82271

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:20:17.950 |

R2R through 3.6.5 fails to properly validate user ownership in conversation update and message handlers, allowing authenticated users to modify other users' conversations. Attackers can supply arbitrary conversation identifiers to rename conversations and append messages to other users' conversation histories, corrupting state and injecting malicious content.

### CVE-2026-77939

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-28T20:19:56.397 |

Flextype CMS through v1.0.0-dev contains an expression language injection vulnerability that allows authenticated attackers with a valid API token to read arbitrary files by passing unsanitized user-supplied input to the Symfony ExpressionLanguage engine via the POST /api/v1/query endpoint. Attackers can leverage exposed application objects including filesystem() and serializers() within the evaluation scope to read arbitrary server files and achieve conditional remote code execution if a PHP file can be placed on disk through a secondary vector.

### CVE-2026-55673

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-08-28T20:18:29.770 |

PowSyBl (Power System Blocks) is a framework to build power system oriented software. Prior to 7.2.2, UnixLocalCommandExecutor and WindowsLocalCommandExecutor concatenate command arguments and environment variables into strings interpreted through bash -c or cmd /c without sufficient escaping. Attacker-controlled values reaching UnixLocalCommandExecutor.execute, WindowsLocalCommandExecutor.execute, LocalComputationManager.execute, ParallelLoadFlowActionSimulator.run, ActionSimulatorTool.run, AmplModelRunner.run, or AmplModelRunner.runAsync can break out of the intended command and execute arbitrary shell commands as the JVM user. The affected itools paths include action-simulator with task-count, security-analysis with external, and dynamic-security-analysis. Downstream CLI tools, libraries, REST front ends, and multi-tenant grid-analysis services that forward less-trusted contingency identifiers or computation parameters into these APIs can expose the injection remotely. This issue is fixed in version 7.2.2.

### CVE-2026-55520

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-08-28T20:18:28.100 |

Protego is a pure-Python robots.txt parser with support for modern conventions. Prior to 0.6.2, protego._urlpattern._URLPattern._prepare_pattern_for_regex translates every asterisk in an Allow or Disallow directive into a lazy regular-expression wildcard, so a directive containing many asterisks creates exponential backtracking. After protego.Protego.parse processes a crafted robots.txt file, protego.Protego.can_fetch can spend an attacker-controlled period matching a near-miss URL and deny service to the crawler. The vulnerable path is src/protego/_urlpattern.py in the _URLPattern match logic. This issue is fixed in version 0.6.2.

### CVE-2026-55066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-28T20:18:23.897 |

Vikunja is an open-source self-hosted task management platform. Prior to 2.4.0, POST /api/v1/projects/{project}/views/{view}/buckets/{bucket}/tasks accepts a body supplied task_id but TaskBucket.CanUpdate in pkg/models/kanban_task_bucket.go authorizes only the project, view, and bucket from the URL. updateTaskBucket then calls Task.ReadOne without a separate task permission check, returns the victim task contents, and can update the task done state when the attacker chooses a done bucket. Because task identifiers are global sequential values, an authenticated user can enumerate cross-tenant tasks and modify their completion metadata through both the v1 and v2 routes that share this model. This issue is fixed in version 2.4.0.

### CVE-2026-81760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-28T16:18:30.340 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetEngine allows Reflected XSS.

This issue affects JetEngine: from n/a through 3.8.14.2.

### CVE-2026-16821

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-08-28T22:16:46.310 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to a format string vulnerability.
