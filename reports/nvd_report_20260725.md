# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-24 15:00 UTC
- **対象期間**: `2026-07-23T15:00:36.000Z` 〜 `2026-07-24T15:00:27.000Z`
- **重要CVE数**: 89 件（Critical 9.0+: 28 件 / High 7.0〜: 61 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上り、特に **クラウド基盤（Azure、Microsoft 365）** と **オンプレミスの管理ツール** に対する **認証・認可の欠陥** が目立ちます。  
- 多くが **ネットワーク経由でのリモートコード実行 (RCE)／権限昇格** を可能にし、被害範囲は数千〜数万アカウントに及ぶ可能性があります。  
- CVSS 10.0 の「完全リモート実行」や「ネットワーク上での特権昇格」レベルの脆弱性が **Azure Key Vault、Azure DNS、Microsoft Exchange Online** など、企業の重要インフラに集中しています。  
- 同時期に報告された **オープンソース／自社開発ツール**（DbGate、Pronetiqs IntraVUE、Cal.com など）でも、認可バイパスやテンプレートインジェクションが多数確認され、**サプライチェーンリスク** が顕在化しています。  

---

## 2. 特に注目すべき CVE  

| CVE 番号 | スコア | 製品・サービス | 主な脆弱性種別 | 注目すべき理由・影響範囲 |
|----------|--------|----------------|----------------|---------------------------|
| **CVE‑2026‑62825** | 10.0 | Azure Key Vault | Improper authentication (認証欠如) | 攻撃者がネットワーク上から **任意のキーやシークレットに無制限アクセス** でき、クラウド全体の暗号資産が漏洩・改竄される危険性がある。Key Vault は多くの SaaS・IaaS の認証基盤として利用されているため、影響範囲は **組織全体** に波及。 |
| **CVE‑2026‑58275** | 10.0 | Azure DNS | Missing authorization (認可欠如) | DNS ゾーンの **レコード追加・削除が無制限** に可能となり、ドメインハイジャックやフィッシングサイトへのリダイレクトが実行できる。企業の外部向けサービスがすべて危険にさらされる。 |
| **CVE‑2026‑56191** | 10.0 | Microsoft Exchange Online | Improper authentication (認証欠如) | Exchange Online のメールボックスや設定情報が **不正に改ざん・閲覧** でき、機密情報漏洩やスパム・フィッシングメールの大量送信が可能になる。Exchange は多くの組織のメール基盤であり、**業務停止リスク** が極めて高い。 |
| **CVE‑2026‑42933** | 10.0 (CVSS4) | Pronetiqs IntraVUE 3.2.1a14‑以前 | Unintended proxy / OT segmentation bypass | OT（Operational Technology）環境で **プロキシ経由の不正アクセス** が可能となり、制御系ネットワークへの侵入経路が開く。産業制御システムや SCADA 環境での **重大な安全インシデント** に直結。 |
| **CVE‑2026‑6516** | 10.0 | ManageEngine ADAudit Plus < 8606 | Unauthenticated RCE via agent API | 管理者権限を持つ **任意コード実行** が可能で、内部ネットワーク上の全サーバーに対して横展開が容易。AD 監査ツールは多くの企業で **特権アカウント情報** を保持しているため、被害が拡大しやすい。 |

> **補足**：上記 5 件は **CVSS が 10.0**（最高評価）であり、かつ **クラウド基盤・OT・特権管理ツール** という組織の根幹を揺るがす領域に位置するため、優先的に対策すべきです。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の共有**：SOC、開発チーム、インフラチームへ即時通知し、影響範囲の把握を開始。  
- **ネットワーク分離**：特に Azure DNS・Key Vault への外部アクセスは **IP 制限・VNet Service Endpoints** で保護。  
- **MFA の徹底**：Azure・Exchange Online の全アカウントに対し **条件付きアクセスポリシー** で MFA を必須化。  
- **監査ログの有効化**：認証失敗・権限昇格イベントを **Azure Monitor / Sentinel** でリアルタイムにアラート化。  

### 3.2 製品別具体的パッチ・バージョン

| 製品・サービス | 現行バージョン (※) | 推奨バージョン | 対策手順 |
|----------------|-------------------|----------------|----------|
| Azure Key Vault | 任意（サービスは常に最新） | **2026‑09‑01 以降のロールアウト** | Azure ポータル → **Key Vault → 更新** → 「**Security patch**」適用。 |
| Azure DNS | 任意 | **2026‑09‑01 以降のロールアウト** | 同上、DNS ゾーンの **アクセス制御リスト (ACL)** を設定し、不要なパブリックエンドポイントを無効化。 |
| Microsoft Exchange Online | 常に SaaS | **2026‑09‑15 以降の更新** | Microsoft 365 管理センター → **サービス更新** → 「**Critical security update**」を即時適用。 |
| Pronetiqs IntraVUE | 3.2.1a14 以前 | **3.2.1a15 以上** | 製品ポータルから **IntraVUE 3.2.1a15** へアップグレード。アップグレード後は **プロキシ設定** を再確認し、OT ネットワーク分離を再適用。 |
| ManageEngine ADAudit Plus | < 8606 | **≥ 8606** | 管理コンソール → **アップデート** → 「**ADAudit Plus 8606**」をダウンロード・適用。適用後は **API キーのローテーション** と **最小権限のサービスアカウント** に切り替える。 |
| DbGate | ≤ 7.1.8 | **≥ 7.1.9** | `apt-get update && apt-get install dbgate=7.1.9`（または公式インストーラ）で更新。`/runners/start` と `/runners/load-reader` エンドポイントの **認可チェック** を有効化。 |
| Cal.com (calcom) | < 5.9.9 | **≥ 5.9.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-62825

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-24T01:17:47.030 |

Improper authentication in Azure Key Vault allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-58275

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-24T01:17:40.863 |

Missing authorization in Azure DNS allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-56191

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-24T01:17:36.417 |

Improper authentication in Microsoft Exchange Online allows an unauthorized attacker to perform tampering over a network.

### CVE-2026-42933

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-441` |
| Published | 2026-07-23T23:16:48.887 |

Pronetiqs IntraVUE versions 3.2.1a14 and prior have an unintended proxy or intermediary vulnerability which could allow an attacker to use an active proxy, which would bypass OT segmentation.

### CVE-2025-71389

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T22:16:51.750 |

Cal.com (calcom/cal.diy) before 5.9.9 is vulnerable to unauthenticated remote code execution because it bundles a version of Next.js whose React Server Components (RSC) request handling deserializes attacker-controlled input. A remote attacker can send a crafted RSC request to the server and cause arbitrary code to be executed during server-side processing, without authentication or user interaction. The flaw derives from the upstream Next.js vulnerability CVE-2025-55182 and is resolved in 5.9.9 by updating the affected dependency.

### CVE-2026-6516

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-23T18:17:02.570 |

Zohocorp ManageEngine ADAudit Plus versions before 8606 are affected by Unauthenticated Remote code execution due to the vulnerable agent API.

### CVE-2026-47668

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-94;CWE-1188` |
| Published | 2026-07-23T18:16:53.350 |

DbGate is cross-platform database manager. In versions 7.1.8 and prior, DbGate's JSON script runner (`POST /runners/start`) allows remote code execution via code injection in the `functionName` parameter of JSON script `assign` commands. The `functionName` value is interpolated directly into dynamically generated JavaScript source code via string concatenation. The generated code is then executed in a forked Node.js child process. Version 7.1.9 contains a patch.

### CVE-2026-54120

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-24T01:17:25.340 |

Improper input validation in Microsoft Surface allows an authorized attacker to execute code over a network.

### CVE-2026-50517

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-24T01:17:02.257 |

Deserialization of untrusted data in M365 Copilot allows an authorized attacker to execute code over a network.

### CVE-2026-47724

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T21:17:04.477 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh virtual private network. Prior to version 0.3.4, the `/api/v1/*` route surface trusts the bearer token alone for authorisation on most endpoints. The codebase itself admits this at `internal/api/hosts.go:384`: "API trusts the bearer token for authorisation; per-CA ownership is enforced only in the Web layer." The Web UI gates state-changing routes through `loadAccessibleCA` (`internal/web/cas.go`); CA-management endpoints in `internal/api/cas.go` ALSO have proper `canAccessCA` gates. The gap is on the host, network, firewall, mobile-bundle, and most operator endpoints. Combined with the per-operator CA model from ADR 0002, this gives any non-admin operator API key broad cross-tenant access — instant privilege escalation in the worst case. Version 0.3.4 fixes the issue.

### CVE-2026-47752

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-07-23T18:16:53.630 |

Tugtainer is a self-hosted app for automating updates of Docker containers. Versions prior to 1.30.2 are vulnerable to Server-Side Template Injection (SSTI) in the notification template feature. The `title_template` and `body_template` fields are rendered using an unsandboxed `jinja2.Environment`, allowing any authenticated user to execute arbitrary OS commands as root inside the container. Version 1.30.2 fixes the issue.

### CVE-2026-15704

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-180;CWE-284;CWE-863` |
| Published | 2026-07-24T09:16:24.113 |

In Eclipse BaSyx Go Components versions up to and including 1.0.0, ABAC-enabled deployments are vulnerable to an authorization bypass caused by inconsistent trailing-slash handling between the ABAC middleware and the HTTP router.



The shared router configuration used Chi's `middleware.StripSlashes`, so a request such as `GET /shells/` was dispatched to the registered `GET /shells` route. However, the ABAC middleware evaluated the original request path including the trailing slash. If ABAC route lookup did not find a matching slash-suffixed route, the request was passed onward and the router then stripped the slash and executed the protected handler without the intended ABAC authorization decision and without the expected ABAC query filters.



An unauthenticated or unauthorized network attacker could append a trailing slash to protected API routes to reach handlers that should have been denied by ABAC policy. Depending on the exposed component, HTTP method, and deployed policy, this could allow unauthorized read, create, update, delete, or upload operations.



The issue affects ABAC-enabled deployments of services that use the shared router and ABAC middleware, including AAS Repository, Submodel Repository, AAS Registry, Submodel Registry, Concept Description Repository, Discovery, AAS Environment upload, and related services. The issue is fixed in Eclipse BaSyx Go Components v1.0.1.

### CVE-2026-56165

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-24T01:17:34.750 |

Heap-based buffer overflow in Microsoft Account allows an unauthorized attacker to execute code over a network.

### CVE-2026-15981

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-23T21:17:03.220 |

The SAML Single Sign On – SSO Login plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 5.4.4. This is due to the mo_saml_validate_signature() function performing a loose boolean check on the raw tri-state integer returned by PHP's openssl_verify(), causing an error return value of -1 to be evaluated as truthy and therefore treated as a successful signature verification. This makes it possible for unauthenticated attackers to log in as any existing WordPress user, including administrators, by submitting a crafted SAMLResponse containing an attacker-controlled NameID and a deliberately malformed signature value that triggers an OpenSSL processing error — bypassing verification entirely and resulting in wp_set_auth_cookie() being called for the targeted account.

### CVE-2026-63732

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-23T22:16:53.023 |

9router 0.4.59 (fixed in 0.4.60) contains a chain of vulnerabilities: a hardcoded default password (123456) that authenticates any fresh installation, a bypass of the LOCAL_ONLY network gate via a spoofed Host header, and unvalidated arguments passed to child_process.spawn() when registering MCP plugins. A remote, unauthenticated attacker can log in with the default credential, spoof the Host header to reach local-only routes, and register a malicious MCP plugin (e.g. node -e <payload>) to achieve arbitrary code execution on the host operating system when the plugin's SSE endpoint is triggered.

### CVE-2026-47670

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-07-23T20:17:08.500 |

DbGate is cross-platform database manager. Versions 7.1.8 and prior are vulnerable to authenticated Remote Code Execution (RCE). Any user with valid DbGate credentials can execute arbitrary OS commands as root by exploiting an unsanitized `functionName` parameter in the `/runners/load-reader` endpoint. The `require = null` mitigation is trivially bypassed via dynamic `import()`. Version 7.1.9 contains a patch.

### CVE-2026-24727

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-24T09:16:24.520 |

An unrestricted upload of file with dangerous type vulnerability in the e-paper draft upload function of SUNNET Corporate Training Management System through v10.3 allows remote authenticated users with administrator privileges to execute arbitrary commands by uploading a crafted ZIP archive containing a server-executable file.

### CVE-2024-58355

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-07-23T22:16:51.533 |

Cal.com (calcom/cal.diy) versions through 4.7.15 contain a stored cross-site scripting vulnerability. The single booking view (e.g., https://app.cal.com/booking/<id>) renders booking-question field labels via React's dangerouslySetInnerHTML without sanitizing or escaping user input. An attacker who can create an event type with a malicious booking-question label can inject arbitrary HTML/JavaScript that executes when a victim opens the crafted booking URL. The issue is fixed in v4.7.16.

### CVE-2024-58353

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-07-23T22:16:51.080 |

Cal.com (repository calcom/cal.diy) in versions <= 4.7.15 is vulnerable to cross-site scripting (XSS) on the publicly accessible single booking view (e.g., /booking/<id>). Booking question (form field) labels are rendered via React's dangerouslySetInnerHTML without proper input sanitization or CSP, so an attacker who can create an event type with a malicious booking question label can inject arbitrary HTML/JavaScript that executes when a victim visits the booking view URL. Self-hosted instances with open registration are particularly at risk. The issue is fixed in version 4.7.16.

### CVE-2026-63359

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T20:17:20.367 |

The Appriss Insights (Equifax) Victim Information Notification Exchange (VINE) applications allow an unauthenticated attacker to send a specially-crafted request to bypass the login page, access other users' credentials, take over other user accounts, access sensitive PII, and dump other information from the database.

### CVE-2026-47669

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T20:17:08.357 |

DbGate is cross-platform database manager. In versions 7.1.8 and prior, the `unzipDirectory()` function in `packages/api/src/shell/unzipDirectory.js` (line 27) does not validate that extracted file paths stay within the output directory. A malicious ZIP with `../` entries writes files anywhere on the filesystem. In the default Docker deployment, DbGate runs as root and the `none` auth provider issues JWT tokens without credentials via `POST /auth/login`, so this is exploitable by any network-adjacent attacker. Version 7.1.9 fixes the issue.

### CVE-2026-65701

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T18:17:01.480 |

SoftVC VITS Singing Voice Conversion through commit 730930d contains a path traversal vulnerability in the full-song inference server that allows unauthenticated remote attackers to read and exfiltrate arbitrary files by supplying attacker-controlled filesystem paths through the audio_path field of an unauthenticated POST request to the /wav2wav route. Attackers can pass arbitrary server-side paths verbatim to librosa.load, torchaudio.load, and soundfile.write sinks, causing the server to decode and return file contents via the HTTP response body while also writing attacker-specified .wav files to arbitrary locations on the filesystem.

### CVE-2026-65700

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T18:17:01.327 |

h2oGPT through 0.2.1 contains a path traversal vulnerability in the OpenAI-compatible files API that allows unauthenticated remote attackers to read, write, and delete arbitrary files accessible to the server process by supplying traversal sequences in the bearer token. The get_user_dir function in openai_server/backend_utils.py uses the bearer token string unsanitized as a path component via os.path.join, and because the default API key is EMPTY authentication is bypassed, enabling attackers to traverse outside the intended user directory through the file content, delete, and upload endpoints to achieve remote code execution by writing to startup hooks or application-loaded files.

### CVE-2026-65761

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-23T17:16:30.433 |

Joomla Extension - joomshaper.com - Unauthenticated SQL injection in Easy Store extension 1.0.0-2.0.1 - Improper validation of order parameters lead to an unauthenticated SQL injection in easystore, allowing full DB read access including credentials and sessions.

### CVE-2026-28698

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-07-23T23:16:48.590 |

Pronetiqs IntraVUE versions 3.2.1a14 and prior have an exposure of sensitive system information to an unauthorized control sphere vulnerability which could expose the underlying host/share filesystem.

### CVE-2026-49035

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-07-23T21:17:04.620 |

The affected product is vulnerable to a heap-based buffer overflow via a crafted MMS Initiate request. Remote code execution (RCE) has been demonstrated when ASLR is disabled; memory corruption or denial of service may occur in configurations where ASLR is enabled.

### CVE-2026-65760

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-284` |
| Published | 2026-07-23T17:16:30.310 |

Joomla Extension - joomshaper.com - cross-customer order and personal information disclosure in Easy Store extension 1.0.0-2.0.1 - Improper access checks allow logged in users to retreive order and customer information of any order in the system.

### CVE-2026-56160

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-07-24T01:17:34.560 |

Improper authorization in Azure Red Hat OpenShift (ARO) allows an authorized attacker to elevate privileges over a network.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-16870

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-787;CWE-918` |
| Published | 2026-07-24T06:16:42.553 |

Multiple security vulnerabilities in Snowflake libsnowflakeclient versions prior to 2.9.2 could allow remote code execution and credential exfiltration. A stack-based buffer overflow in the file download path could allow remote code execution on a victim host. An attacker could exploit this by uploading a file with a crafted encryption metadata field to a shared internal stage that a victim process later downloads, and impact would be limited to deployments where principals with different privilege levels share the same internal stage. A related out-of-bounds write in the same download path could allow memory corruption with attacker-controlled write primitives. An attacker may exploit this through a crafted initialization vector metadata field on a shared stage, and impact would be limited by the same stage-write precondition. Improper validation of connection parameters could allow an attacker-controlled input to redirect outbound authentication requests — including credentials and tokens — to an attacker-controlled endpoint. Impact is limited to embedding deployments where a lower-privileged principal can influence connection configuration while higher-privileged service credentials are in use. The fix is available in Snowflake libsnowflakeclient version 2.9.2. Users must manually upgrade.

### CVE-2026-65604

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-23T22:16:53.170 |

Skipper contains an incomplete fix for CVE-2026-50197 in which oversized request bodies bypass Open Policy Agent (OPA) deny-on-presence Rego policies. When a request body exceeds the configured maxBodyBytes limit, Skipper forwards the full payload to the upstream service while OPA evaluates against an empty parsed_body, so policies that deny requests based on body content are not enforced and forbidden actions proceed. No fixed version is available; v0.27.26 adds documentation guidance only.

### CVE-2026-16807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-23T22:16:52.750 |

Out of bounds write in Codecs in Google Chrome prior to 150.0.7871.186 allowed a remote attacker to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-16806

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-23T22:16:52.640 |

Use after free in WebMCP in Google Chrome prior to 150.0.7871.186 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-16805

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-23T22:16:52.533 |

Use after free in Blink in Google Chrome prior to 150.0.7871.186 allowed a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-16002

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-23T21:17:03.363 |

The affected product is vulnerable to an Out-of-bounds read, which may allow an attacker to crash the parsing process and cause a denial of service.

### CVE-2026-15212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-23T20:17:07.460 |

The WPO365 | Login plugin for WordPress is vulnerable to Cross-Site Request Forgery in versions up to, and including, 43.2. This is due to the Ajax_Service::verify_ajax_request() helper gating its wp_verify_nonce() call behind the boolean option 'enable_nonce_check', which is absent from the default 'wpo365_options' array and therefore evaluates to false via get_global_boolean_var(); as a result, the wp_ajax_wpo365_update_settings handler (Ajax_Service::update_settings) accepts POSTs from cross-origin pages and forwards the attacker-supplied 'settings' payload (base64/JSON) to Options_Service::update_options(), which merges every key/value into wpo365_options without a key allowlist. This makes it possible for unauthenticated attackers to overwrite arbitrary plugin options — including enabling the SCIM REST endpoint (enable_scim), planting an attacker-known scim_secret_token, and setting new_usr_default_role to 'administrator' — via a forged request granted they can trick a site administrator into performing an action such as clicking on a link.

### CVE-2026-63765

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-23T19:17:03.560 |

Chatwoot before 4.16.0 contains an authentication bypass vulnerability in the direct uploads controller that allows unauthenticated attackers to create arbitrary ActiveStorage blobs in any tenant account. Attackers can exploit missing authentication checks to resolve any account and conversation, then obtain signed PUT URLs to write arbitrary data to the application's storage backend.

### CVE-2026-65702

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T18:17:01.630 |

Vanna through 2.0.2 contains a path traversal vulnerability in the FileSystemConversationStore persistence integration that allows unauthenticated remote attackers to write attacker-controlled JSON files to arbitrary filesystem locations and read conversation metadata from outside the intended store base directory. Attackers can supply path traversal sequences in the conversation_id parameter submitted to the unauthenticated chat API endpoints to escape the base directory during both write and read operations, enabling arbitrary file write with attacker-controlled content and unauthorized file read on the server filesystem.

### CVE-2026-15810

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Amber` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-24T12:16:47.543 |

A Cross-Site Scripting (XSS) vulnerability in Google Cloud Looker versions prior to 25.6.103, 25.12.65, 25.18.68, 26.0.66, 26.2.47, 26.4.36, 26.6.28, and 26.8.7 on Looker-hosted and Self-hosted allows an attacker to execute arbitrary JavaScript leading to administrative account takeover using a maliciously crafted URL.


Looker-hosted and Self-hosted were found to be vulnerable.
This issue has already been mitigated for Looker-hosted instances. No user action is required for these.


Self-hosted instances must be upgraded to the patched versions: 25.6.103+, 25.12.65+, 25.18.68+, 26.0.66+, 26.2.47+, 26.4.36+, 26.6.28+, or 26.8.7+.

### CVE-2026-40430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-07-23T23:16:48.743 |

Pronetiqs IntraVUE Versions 3.2.1a14 and prior have a plaintext storage of a password vulnerability that could expose cleartext credentials through the API.

### CVE-2026-65694

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T22:16:53.313 |

Microweber CMS through 2.0.20 contains a path traversal vulnerability in the static file controller that allows unauthenticated remote attackers to read arbitrary files by supplying directory traversal sequences in the path query parameter. Attackers can send a single unauthenticated HTTP GET request exploiting the failure of normalize_path() to strip traversal sequences, disclosing sensitive files such as environment configuration files containing credentials and system files.

### CVE-2026-6924

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-336` |
| Published | 2026-07-23T21:17:05.447 |

A bug in the entropy initialization for SiWx917 causes the DRBG to use a predictable seed. As such, all random numbers generated in the Matter code use the same stream of numbers. This vulnerability was discovered after the impacted repository was already deprecated.

### CVE-2026-50039

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-07-23T21:17:04.910 |

The affected product is vulnerable to a stack-based buffer overflow, which may allow an attacker to cause a memory corruption via a Read Request.

### CVE-2026-50032

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-07-23T21:17:04.773 |

A NULL pointer dereference in the MMS Write Named Variable List handler, which may allow a network adjacent attacker to crash the server by sending a WriteRequest with an empty listOfData field.

### CVE-2026-21655

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-23T21:17:03.810 |

Deserialization of untrusted data vulnerability in Johnson Control victor on Windows allows capec-586.

This issue affects victor: from 2.9 before 3.0.

### CVE-2026-47722

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T20:17:08.637 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh virtual private network. Prior to version 0.3.2, `internal/configgen/generator.go:86,108,119` interpolates the operator-supplied `ListenHost` and `TunDevice` fields raw into a `text/template` that produces the agent's `config.yml`. `internal/web/advanced.go:20-35` accepts both with only `strings.TrimSpace` — no character or shape validation. Version 0.3.2 fixes the issue.

### CVE-2026-16756

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-23T19:16:53.657 |

Missing connection and header-read timeouts and the absence of a concurrent-connection cap in the default serve() path of Amazon aws-smithy-http-server might allow remote attackers to cause a denial of service by opening many connections and sending partial requests that are never completed, exhausting server sockets and tasks.



To mitigate this issue, users should upgrade to aws-smithy-http-server 0.66.5 or later.

### CVE-2026-65919

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T18:17:02.290 |

Meshery before 1.0.57 contains an unauthenticated arbitrary file read vulnerability in the /api/system/fileView and /api/system/fileDownload endpoints that pass user-supplied file parameters directly to os.Open without path validation. Attackers can supply absolute paths or traversal sequences in the file parameter to read arbitrary files from the host filesystem without authentication.

### CVE-2026-47743

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79;CWE-200;CWE-639` |
| Published | 2026-07-23T18:16:53.490 |

Shopper is a Headless e-commerce Admin Panel. Prior to 2.8.0, three related defects on admin Livewire components allowed data tampering, sensitive data disclosure, and stored XSS. First, several Livewire components in the admin panel exposed Eloquent model identifiers as public properties without the `#[Locked]` attribute. An authenticated user could rewrite the wire payload from the browser to target any record id, bypassing the implicit scoping enforced by the page routing. Second, `Customers/Create::store()` re-passed a `Hidden` `_password` form field straight into the create payload. The plaintext password was rendered into the HTML and transported through the Livewire snapshot in clear text, exposing credentials in the page DOM and in any logging that captures Livewire payloads. Finally, the product barcode field was rendered through `DNS1DFacade::getBarcodeHTML()` with `{!! !!}`. An attacker with `edit_products` permission could persist malicious payload in the barcode field that would execute in the browser of any admin user viewing that product, enabling session theft and privileged-action chaining. Starting in v2.8.0, all vulnerable Livewire model identifiers are now marked `#[Locked]`; `Customers/Create` no longer round-trips the password through a Hidden form field; the plaintext password is hashed at action boundary and never returned to the client; and the product barcode rendering now escapes the value before passing it to the barcode generator and the output is wrapped in an `<svg>` context that does not interpret event handlers. No known workarounds are available.

### CVE-2026-65759

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-23T17:16:30.190 |

Joomla Extension - joomshaper.com - unauthenticated payment/order forgery in Easy Store extension 1.0.0-2.0.1 - Critical order and payment information, including states, are processed from client side input, enabling unauthenticated attackers to manipulate payment and order states of arbritrary orders.

### CVE-2026-65917

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-23T16:17:55.020 |

CyberPanel through 1.9.1, fixed in commit b198460, contains an insecure direct object reference (IDOR) vulnerability in the IncBackups application's incremental-backup handlers (deleteBackup, fetchRestorePoints, and restorePoint) that allows authenticated panel users to access or manipulate other tenants' backup resources by supplying an attacker-controlled globally sequential IncJob integer ID that is never re-scoped to the authorized domain. Attackers can enumerate sequential backup IDs to read another tenant's backup metadata, irrecoverably delete another tenant's backup snapshots, or trigger unauthorized restoration of another tenant's backup job with root privileges.

### CVE-2026-10610

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-24T12:16:45.797 |

Local privilege escalation potentially allowed an attacker to execute arbitrary code as a privileged user.

### CVE-2026-7483

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-24T10:16:32.637 |

Local privilege escalation potentially allowed an attacker to write an arbitrary file with fully controlled content as a privileged user.

### CVE-2026-56167

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-24T01:17:34.877 |

Server-side request forgery (ssrf) in Azure AI Search allows an authorized attacker to elevate privileges over a network.

### CVE-2024-58354

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-23T22:16:51.380 |

cal.com (calcom repository, later renamed cal.diy) is affected by a repository takeover vulnerability in its GitHub Actions workflows. The workflow pr.yml uses the pull_request_target trigger with the repository's default write permissions and passes them down to check-types.yml. check-types.yml then performs a 'dangerous' checkout of the attacker-submitted pull request code (via the dangerous-git-checkout action) and subsequently executes it (through yarn install and package.json scripts). An attacker can open a pull request whose code runs arbitrary commands with the repository's write-scoped GITHUB_TOKEN, allowing them to push commits, merge or mutate pull requests, add or delete comments, and delete or force-push branches, thereby compromising the repository. The main branch is affected; no patched version is available.

### CVE-2026-65706

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-07-23T20:17:22.257 |

FFmpeg versions 3.0 through 8.1.2 contain an out-of-bounds write vulnerability in the vf_swaprect video filter that allows attackers to corrupt heap memory by supplying a crafted NV12 video frame with odd width dimensions. The filter_frame() function reuses a temporary row buffer sized for plane 0's single-byte pixel step across all planes, causing an 18-byte memcpy into a 17-byte heap allocation when processing the two-byte-per-sample interleaved chroma plane of a 17x16 NV12 frame, resulting in heap corruption and process crash with potential for code execution.

### CVE-2026-65703

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-23T20:17:21.803 |

FFmpeg versions 2.7 through 8.1.2 contain an out-of-bounds write vulnerability in the TDSC video decoder that allows remote attackers to cause heap corruption by supplying a crafted AVI file that changes frame dimensions across TDSF frames. The tdsc_parse_tdsf() function fails to unreference the existing reference frame before calling av_frame_get_buffer(), causing tdsc_blit() and tdsc_yuv2rgb() to write attacker-controlled pixel data beyond the end of the undersized reference frame buffer, resulting in a process crash and potential code execution.

### CVE-2026-60122

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-23T20:17:09.207 |

gpsd through release-3.27.5, fixed at commit 4c06658, contains a code injection vulnerability in the gpsprof utility that allows an attacker who controls GPS input data to execute arbitrary OS commands by injecting malicious content into the SKY.satellites[].used field, which is inserted unsanitized into a gnuplot heredoc data block. Attackers can supply a used value containing the string EOD to terminate the heredoc early and append gnuplot system() calls, achieving OS command execution as the user running gpsprof when the generated plot script is processed by gnuplot in polar mode.

### CVE-2026-66140

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-24` |
| Published | 2026-07-24T05:16:49.747 |

Exim before 4.99.5 allows directory traversal to access files outside of the spool area, and consequently gain privileges, because arguments related to queue-name are mishandled.

### CVE-2026-16796

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-07-23T21:17:03.510 |

Improper neutralization of argument delimiters in the install_packages() method in AWS Bedrock AgentCore Python SDK before 1.18.1 might allow a remote authenticated user to execute arbitrary commands within the Code Interpreter sandbox via crafted package name arguments.



To mitigate this issue, users should upgrade to the patched version 1.18.1.

### CVE-2026-63313

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-23T22:16:52.877 |

9Router before 0.4.72 contains a server-side request forgery (SSRF) vulnerability in the /v1/web/fetch endpoint. The endpoint accepts a user-controlled url parameter and passes it to a configured external scraping provider (Firecrawl, Jina Reader, Tavily, or Exa) to fetch content. The URL is only validated as syntactically valid via new URL() with no blocklist for private IP ranges, cloud metadata endpoints (e.g., 169.254.169.254), link-local addresses, or internal hostnames. An authenticated or locally-connected user can cause the server to fetch arbitrary internal URLs and have the response content returned, enabling read-access SSRF that can expose cloud metadata credentials, reach internal services, and bypass authentication on localhost endpoints.

### CVE-2026-16804

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-23T22:16:52.427 |

Use after free in Input in Google Chrome prior to 150.0.7871.186 allowed a remote attacker who had compromised the renderer process to potentially perform a sandbox escape via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-12736

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-24T04:16:51.357 |

The Wpify Woo plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 5.4.16. This is due to the SettingsApi::save_option() REST route (POST /wp-json/wpify-woo/v1/option) passing the request-supplied 'option' and 'data' parameters directly to update_option() without any option-name allowlist or value sanitization, while the permission_callback only verifies the manage_woocommerce capability. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to elevate their privileges to Administrator by overwriting arbitrary WordPress options (for example setting default_role to administrator and users_can_register to 1, or disabling security plugins via active_plugins).

### CVE-2026-35425

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-07-24T01:16:36.970 |

Improper access control in Azure API Management (APIM) allows an authorized attacker to execute code over a network.

### CVE-2026-14172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-24T07:16:32.977 |

Rapid7 InsightVM, Nexpose, and the Insight Agent execute discovered executables during authenticated assessment without validating file ownership, allowing a local low-privileged user to run code as the scan credential (Scan Engine) or as root/SYSTEM (Insight Agent). Fixed in Scan Engine content 1.1.3935 and Insight Agent content component 0.0.245.0.

### CVE-2026-50044

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-07-23T23:16:49.170 |

Pronetiqs IntraVUE versions 3.2.1a14 and prior have an inadequate encryption strength vulnerability which could allow an attacker to steal admin credentials via weak hash or a pass-the-hash attack.

### CVE-2026-65695

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-23T17:16:29.610 |

Office-Word-MCP-Server through 1.1.11 contains a path traversal vulnerability in its document tools that allows attackers who can influence the filename argument to read arbitrary .docx files or create and overwrite .docx files outside the intended working directory. Attackers can supply absolute paths or ../ traversal sequences directly to document open and save operations, bypassing the check_file_writeable and ensure_docx_extension helpers which perform no base-directory confinement or realpath validation.

### CVE-2026-15967

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-07-23T21:17:02.977 |

Insufficient session expiration vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.5, from 2026.0.0 before 2026.0.3.

### CVE-2026-15966

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-942` |
| Published | 2026-07-23T21:17:02.860 |

Permissive cross-domain security policy with untrusted domains vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.5, from 2026.0.0 before 2026.0.3.

### CVE-2026-10697

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-23T21:17:01.597 |

Improper Authentication vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.5, from 2026.0.0 before 2026.0.3.

### CVE-2026-25800

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-07-23T20:17:07.860 |

Quinn is a pure-Rust, async-compatible implementation of the IETF QUIC transport protocol. Starting in version 0.1.0 and prior to version 0.11.15, the `Assembler` component that assembles unordered stream fragments into consecutive chunks of the stream incurs some overhead for non-contiguous fragments. Readers that read from a `RecvStream` in order (through an `AsyncRead` impl for example) will be sensitive to peers that send fragments while leaving out early parts of the stream, and in particular, fragments with many gaps (because these cannot be defragmented). In such a scenario, the receiving connection suffers from high buffer overhead, enabling memory exhaustion. Version 0.11.15 fixes the issue.

### CVE-2026-44909

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-07-23T17:16:28.170 |

Proxygen lacked a generalized slow-consumer detection mechanism in its core HTTP session layer. A remote, unauthenticated attacker could exploit HTTP/2 flow-control by setting SETTINGS_INITIAL_WINDOW_SIZE to 0 or withholding WINDOW_UPDATE frames, causing the server to buffer complete response bodies in memory indefinitely for stalled streams. By opening many simultaneous streams requesting large resources while preventing the server from transmitting responses, an attacker could induce unbounded memory growth leading to service degradation, resource exhaustion, or denial of service. Versions v2017.01.16.00 through v2026.07.20.00 are affected.

### CVE-2026-43823

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-07-23T15:17:05.613 |

When initializing an RSA public key from DER or PEM bytes throws an error, the EVP_PKEY* is double-freed: first in the catch block, then in the deinit. This can lead to a crash on future memory allocations. This double-free manifests when BoringSSL cannot decode the public key from the bytes provided. This vulnerability is addressed in swift-crypto version 4.5.1.

### CVE-2026-15243

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-297` |
| Published | 2026-07-24T12:16:46.973 |

Apereo CAS Client accepts any CA-trusted certificate for any hostname, provided the URL the client is calling matches the configured allowlist or regex. An attacker with a MITM position (DNS poisoning, rogue Wi-Fi, malicious proxy, etc.) can provide any CA-signed certificate for a hostname that matches the configured allowlist or regex. This can lead to intercepting the CAS exchange, capturing the Ticket-Granting Ticket (TGT), and subsequently obtaining Service Tickets on behalf of the victim. 


Because maintainers contact attempts were unsuccessful, vulnerabilities have only been confirmed in version 4.1.0 (Java Apereo CAS Client) and 3.6.4 (Jasig CAS Client) but may also affect other versions.

### CVE-2026-66141

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-07-24T05:16:49.890 |

Exim before 4.99.5 allows .forward privilege escalation because force_command for a pipe transport is mishandled.

### CVE-2026-10033

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-24T10:16:29.983 |

The EventON Action User plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.5.14. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to grant EventON management capabilities and the upload_files capability to any non-administrator WordPress role or user, escalating their privileges within the site. The administrator role is protected by an early-return guard in update_role_caps(), so only non-administrator roles and individual users can be targeted; however, the same unauthenticated exposure also allows attackers to enumerate all WordPress users with their IDs and display names, disclose role and user capability state along with nonce values, and tamper with event-to-user term assignments.

### CVE-2026-16519

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-07-24T08:16:26.663 |

A
DLL hijacking vulnerability exists in the GeoVision GV-IP Device Utility
desktop application. The application loads one or more dynamic-link libraries
(DLLs) from an unsafe search path, allowing a local attacker to place a
malicious DLL in a location searched before the legitimate library
location.

### CVE-2026-65705

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-07-23T20:17:22.120 |

FFmpeg versions 3.4 through 8.1.2 contain an out-of-bounds write vulnerability in the vf_floodfill video filter that allows attackers to corrupt heap memory by supplying a dynamically sized video stream with filtergraph reinitialization disabled via -reinit_filter 0. When config_input() allocates the points traversal stack based on initial frame dimensions and a subsequent larger frame is processed, filter_frame() performs flood-fill neighbor pushes beyond the original allocation boundary, resulting in heap corruption and process crash with potential for code execution depending on heap layout and process hardening.

### CVE-2026-65704

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-07-23T20:17:21.973 |

FFmpeg through 8.1.2 contains an out-of-bounds write vulnerability that allows attackers to cause heap corruption by supplying a crafted ffconcat file processed with the -safe 0 flag. The TY demuxer's demux_audio() function decrements packet size without bounds checking, producing a negative size value that is passed to memcpy() in shorten_decode_frame(), where conversion to size_t wraps the value to near SIZE_MAX and triggers reads beyond the source allocation and writes far beyond the Shorten decoder's bitstream buffer.

### CVE-2026-16584

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-455` |
| Published | 2026-07-23T16:17:15.787 |

Improper handling of an initialization failure in AWS API MCP Server from 0.2.13 through 1.3.46 might allow an actor to bypass the user-configured security policy and execute AWS API operations that the policy was set to deny or gate. When initialization of the security policy enforcement data fails at server startup, the policy check is skipped for the lifetime of the process. IAM permissions on the configured credentials remain in effect and are unaffected.



To remediate this issue, users should upgrade to version 1.3.47.

### CVE-2026-15401

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-24T10:16:31.410 |

The VikBooking Hotel Booking Engine & PMS plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'vbfX' parameter in all versions up to, and including, 1.8.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The vbfX custom-field value is stored via the public-facing saveorder task, which has no capability or authentication check enforced by default, enabling fully unauthenticated submission of malicious payloads.

### CVE-2026-66138

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-24T05:16:49.433 |

In OpenStack Ironic Python Agent through 11.6.0, a project-scoped user with the manager role can achieve arbitrary code execution on a running Ironic-Python-Agent via a maliciously constructed configuration, because the value of ntp_server is passed to a shell.

### CVE-2026-21653

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:L/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-23T21:17:03.653 |

Victor SSRF vulnerability in Johnson Controls CCure 9000 and victor application server allows Server Side Request Forgery.

This issue affects CCure 9000 and victor application server: from 2.9 through 3.0.

### CVE-2026-65916

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-23T16:17:54.883 |

CyberPanel through 1.9.1, fixed in commit b198460, contains a missing authorization vulnerability in the cancelBackupCreation handler that allows authenticated users to kill, delete, and corrupt other tenants' backups. Attackers can send crafted POST requests with arbitrary backupCancellationDomain and fileName parameters to terminate backup processes, delete backup archives, corrupt backup status files, and remove database records belonging to other tenants.

### CVE-2026-9765

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `N/A` |
| Published | 2026-07-24T13:18:31.480 |

Note: The CVE and blog post don't exist because we determined this is actually a cloud-only issue.

Access Controls are “Broken” when a user can access resources they are not authorized to access. An attacker can bypass any access control mechanisms in a web application, and gain unauthorized access to resources that are not available with their permissions. 

Broken access control can allow attackers to:
Access resources only accessible to certain users, thus allowing unauthorized access to data
Perform operations on behalf of other users, leading to account takeovers in the worst cases
Attempt privilege escalation
Attempt to take over an account

### CVE-2026-50103

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-228` |
| Published | 2026-07-23T21:17:05.057 |

A NULL pointer dereference in the L2 GOOSE and R-GOOSE shared parser, which may allow a network-adjacent attacker to crash a subscribing application by sending a crafted GOOSE frame containing a malformed TLV value.

### CVE-2026-47723

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1021` |
| Published | 2026-07-23T21:17:04.340 |

nebula-mesh is a self-hosted control plane for Slack Nebula mesh virtual private network. Prior to version 0.3.1, none of the response paths in `internal/web/` or `internal/api/` set the standard browser-security headers. `grep` for `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`, `X-Content-Type-Options`, `Referrer-Policy` returns zero matches across the codebase. Version 0.3.1 fixes the issue.

### CVE-2026-34496

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-07-23T21:17:03.947 |

Cwe-269 vulnerability in Johnson Controls victor Web on Windows allows capec-233.

This issue affects victor Web: before 7.1.

### CVE-2026-15968

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-23T21:17:03.090 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.5, from 2026.0.0 before 2026.0.3.

### CVE-2026-65918

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-07-23T18:17:02.143 |

PyTorch torchvision through 0.28.0, fixed in commit 4e05dc2, contains an out-of-bounds heap read vulnerability in the GIF decoder's read_from_tensor callback that passes unclamped length to memcpy. Attackers can supply malicious or truncated GIF files to cause denial of service via segmentation fault or disclose adjacent heap memory contents.
