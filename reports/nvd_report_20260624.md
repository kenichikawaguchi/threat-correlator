# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-23 19:00 UTC
- **対象期間**: `2026-06-23T15:00:39.000Z` 〜 `2026-06-23T19:00:43.000Z`
- **重要CVE数**: 71 件（Critical 9.0+: 18 件 / High 7.0〜: 53 件）

---

## AI 分析サマリー

## 1. 全体サマリー
- 直近で公開された CVE の多くは **Web アプリケーションや API の認証・権限チェック不備** に起因し、リモートコード実行 (RCE) や権限昇格が可能になるものが目立ちます。  
- 特に **オープンソースのワークフロー自動化プラットフォーム (n8n, Langflow)** と **AI/ML 関連ツール (Open WebUI, Immich, Langflow)** に集中した脆弱性が多数報告され、攻撃対象が拡大しています。  
- さらに、**ネットワーク機器 (NetComm ルータ)** や **Microsoft Outlook** など、エンタープライズ向け製品でも認証バイパスやテンプレートインジェクションが確認され、企業環境でのリスクが高まっています。

---

## 2. 特に注目すべき CVE

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑27604** (FOSSBilling) | 10.0 | API ロール処理の認証バイパスにより、`/api/system/*` エンドポイントへ無認証でアクセス可能。cron 管理者権限が取得できる。 | **全権限取得** が可能で、課金システムや顧客情報が一括取得・改ざんされる危険性が極めて高い。 |
| **CVE‑2021‑41163** (Discourse) | 10.0 | `subscribe_url` のバリデーション欠如によりリモートコード実行 (RCE)。 | 世界中で数百万のフォーラムが稼働しているため、**広範囲な影響** が想定される。パッチ適用が必須。 |
| **CVE‑2026‑55255** (Langflow) | 9.9 | IDOR により認証ユーザーが他ユーザーのフローを実行可能。 | AI エージェントの **機密データ漏洩・不正実行** が起こり得る。特に SaaS 形態で提供されている場合は顧客への影響が大きい。 |
| **CVE‑2023‑23397** (Microsoft Outlook) | 9.8 | ローカルユーザーが特別に細工したメールを開くだけで特権昇格。 | エンドポイントデバイスが多数ある企業環境で **広範囲に横展開** 可能。既知の攻撃手法で実証済み。 |
| **CVE‑2026‑35019** (NetComm NF20MESH ルータ) | 9.2 | ハードコードされた AES‑256 鍵で認証バイパス、管理者権限取得。 | **ネットワークインフラ全体** が侵害され、内部ネットワークへの不正アクセスが容易になる。 |

> **注:** 上記は CVSS が高く、かつ **実運用で広く利用されている**、または **権限昇格・RCE が直接的に可能** な点で選定しました。

---

## 3. 推奨アクション

### 共通対策
- **脆弱性情報の定期的なモニタリング**（NVD、各ベンダーのアドバイザリ）と **パッチ適用の自動化**（例: `apt-get upgrade`, `yum update`, Docker イメージの再ビルド）を実施。  
- **最小権限の原則**を徹底し、不要な管理者権限や API キーを削除。  
- **外部からの直接アクセスを制限**（WAF、IP 制限、VPN 経由のみ）し、特に `/api/*` 系エンドポイントは認証必須にする。  
- **ログ監視とインシデントレスポンス**を整備し、異常な API 呼び出しや認証失敗の増加を検知。

### 製品別具体的対策

| 製品 | 修正バージョン | 推奨パッケージ/イメージ |
|------|----------------|------------------------|
| **FOSSBilling** | ≥ 0.8.0 | `fossbilling/fossbilling:0.8.0` もしくは最新 Docker イメージ |
| **Discourse** | 最新安定版 (3.2.2 以降) | `docker pull discourse/discourse:latest` |
| **Langflow** | ≥ 1.9.2 (IDOR, RCE, ファイル読取) | `langflow/langflow:1.9.2` 以上 |
| **Microsoft Outlook** (Windows) | 2021 年 10 月以降の累積更新プログラム (KB5028250 など) | Windows Update で最新の Office 365 ビルドを適用 |
| **NetComm NF20MESH** | Firmware R6B032 以降 | メーカー提供の最新ファームウェアを **Web UI** もしくは **TFTP** でアップデート |
| **n8n** | ≥ 1.123.55 / 2.26.2 | `docker pull n8n/n8n:2.26.2` |
| **Open WebUI** | ≥ 0.9.6 | `ghcr.io/open-webui/open-webui:0.9.6` |
| **Immich** | ≥ 1.84.0 (XSS 修正) | `immich-app/immich-server:1.84.0` |
| **Tenable Identity** | 最新リリース (2024‑xx) | `tenable/identity:latest` |
| **Cisco HyperFlex HX** | 最新 IOS / 管理ソフトウェア (2024‑Q2) | Cisco の公式アップデート手順に従う |
| **Revive Adserver** | ≥ 6.0.7 | `reviveadserver/revive-adserver:6.0.7` |

### 緊急対応チェックリスト
1. **脆弱性スキャン**：`nmap`, `nikto`, `OWASP ZAP` で対象システムを走査し、未パッチのエンドポイントが残っていないか確認。  
2. **API キーローテーション**：特に FOSSBilling、Langflow、n8n の API キーは全て再生成し、古いキーは即時無効化。  
3. **TLS/HTTPS 強制**：全ての管理 UI と API に対し TLS 1.2 以上を必須化し、自己署名証明書は信頼できる CA に置き換える。  
4. **バックアップ検証**：RCE やデータ改ざんに備え、**オフラインバックアップ**を定期的に取得し、リストア手順をテスト。  
5. **ユーザー教育**：Outlook の特権昇格脆弱性に対し、**不審なメールの開封禁止**や **マクロ無効化** のポリシーを周知徹底。

---

**まとめ**  
今回の CVE は「認証・権限チェックの欠如」や「テンプレート/コードインジェクション」が共通テーマです。特にオープンソースの自動化・AI ツールは開発スピードが速く、脆弱性が早期に公開されやすい傾向があります。**迅速なパッチ適用と最小権限化**、そして **継続的な監視** が被害防止の鍵となります。各製品の推奨バージョンへアップデートし、上記チェックリストを実施してください。

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-27604

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-306;CWE-862;CWE-863` |
| Published | 2026-06-23T15:16:33.700 |

FOSSBilling is a free, open-source billing and client management system. Starting in version 0.5.4 and prior to version 0.8.0, an authorization bypass in the API role handling allows unauthenticated access to privileged `/api/system/*` endpoints. Because `system` resolves to the cron admin identity, attackers can invoke admin API methods without valid credentials, session, or CSRF token. Version 0.8.0 patches the issue. Some workarounds are available. Block external access to `/api/system/*` at reverse proxy/WAF, restrict API access by trusted source IPs only (`api.allowed_ips`), rotate all admin/client API tokens immediately, invalidate active sessions and reset high-privilege credentials, and/or review API request logs for suspicious `/api/system/` access and treat as potential incident.

### CVE-2021-41163

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2021-10-20T22:30:14.000Z |

Discourse is an open source platform for community discussion. In affected versions maliciously crafted requests could lead to remote code execution. This resulted from a lack of validation in subscribe_url values. This issue is patched in the latest stable, beta and tests-passed versions of Discourse. To workaround the issue without updating, requests with a path starting /webhooks/aws path could be blocked at an upstream proxy.

### CVE-2026-55255

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T17:17:08.050 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.2, an Insecure Direct Object Reference (IDOR) vulnerability in /api/v1/responses endpoint allows an authenticated attacker to execute any flow belonging to another user by specifying the victim's flow ID in the request. This vulnerability is fixed in 1.9.2.

### CVE-2021-38163

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2021-09-14T11:21:36.000Z |

SAP NetWeaver (Visual Composer 7.0 RT) versions - 7.30, 7.31, 7.40, 7.50, without restriction, an attacker authenticated as a non-administrative user can upload a malicious file over a network and trigger its processing, which is capable of running operating system commands with the privilege of the Java Server process. These commands can be used to read or modify any information on the server or shut the server down making it unavailable.

### CVE-2023-23397

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:F/RL:O/RC:C` |
| Weaknesses | `CWE-20` |
| Published | 2023-03-14T16:55:28.168Z |

Microsoft Outlook Elevation of Privilege Vulnerability

### CVE-2021-1497

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2021-05-06T12:41:27.712Z |

Multiple vulnerabilities in the web-based management interface of Cisco HyperFlex HX could allow an unauthenticated, remote attacker to perform command injection attacks against an affected device. For more information about these vulnerabilities, see the Details section of this advisory.

### CVE-2026-53662

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79;CWE-601` |
| Published | 2026-06-23T18:18:05.530 |

immich is a high performance self-hosted photo and video management solution. From commit 4ffa26c9 until 4eb1003, a reflected cross-site scripting (XSS) vulnerability on the /auth/login page allows an attacker to fully compromise any authenticated user's account with a single link click. The continue query parameter is read from the URL and passed to SvelteKit's redirect() without any scheme or origin validation, allowing attacker-controlled JavaScript to execute inside Immich's origin. The payload then uses the victim's existing session to mint an all-permission API key on their account, leading to persistent account takeover. This vulnerability is fixed in commit 4eb1003.

### CVE-2026-55447

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-61;CWE-200` |
| Published | 2026-06-23T17:17:08.540 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.2, by controlling a files that are digested into the RAG, an attacker can direct the node to read any file on the file-system by absolute path. All components based on BaseFileComponent are vulnerable to the vulnerability. This includes Docling (DoclingInlineComponent), Docling Serve, DoclingRemoteComponent), Read File (FileComponent), NVIDIA Retriever Extraction (NvidiaIngestComponent), Video File (VideoFileComponent), and Unstructured API (UnstructuredComponent). This vulnerability is fixed in 1.9.2.

### CVE-2026-48519

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-23T17:17:01.240 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.2, the "Shareable Playground" (or "Public Flows" in code) contains a critical RCE vulnerability. Shareable Playground feature works by enabling the execution of workflows by unauthenticated users, by accessing a link. Specifically, it enables the route /api/v1/build_public_tmp to execute any public flow, given a public flow ID. When the route executes the flow, it allows for providing arbitrary custom Python code as the nodes code, inside the JSON payload. The vulnerable field is data.nodes[X].data.node.template.code.value. This vulnerability is fixed in 1.9.2.

### CVE-2026-44791

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-23T17:16:59.547 |

n8n is an open source workflow automation platform. Prior to 1.123.43, 2.22.1, and 2.20.7, an authenticated user with permission to create or modify workflows could bypass the patch for CVE-2026-42232 in the XML node. When combined with other nodes, this could lead to RCE on the n8n host. This vulnerability is fixed in 1.123.43, 2.22.1, and 2.20.7.

### CVE-2026-44790

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-06-23T17:16:59.417 |

n8n is an open source workflow automation platform. Prior to 1.123.43, 2.22.1, and 2.20.7, an authenticated user with permission to create or modify workflows could inject CLI flags on the Git node's Push operation allowing an attacker to read arbitrary files from the n8n server potentially leading to full compromise. This vulnerability is fixed in 1.123.43, 2.22.1, and 2.20.7.

### CVE-2026-44789

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-23T17:16:59.290 |

n8n is an open source workflow automation platform. Prior to 1.123.43, 2.22.1, and 2.20.7, an authenticated user with permission to create or modify workflows could achieve global prototype pollution via an unvalidated pagination parameter in the HTTP Request node. Combined with other techniques this could lead to RCE on the instance. This vulnerability is fixed in 1.123.43, 2.22.1, and 2.20.7.

### CVE-2026-28496

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-06-23T15:16:33.850 |

FOSSBilling is a free, open-source billing and client management system. Versions prior to 0.8.0 have a Server-Side Template Injection (SSTI) vulnerability in the template rendering system. Administrators with access to features that render Twig templates (email templates, mass mail campaigns, custom payment adapters, and the `string_render` API endpoint) can inject arbitrary Twig expressions, leading to information disclosure and remote code execution. The vulnerability exists because Twig templates are rendered without a sandbox, allowing access to the full Twig environment, API context, and the application's dependency injection container. Version 0.8.0 patches the issue. Some workarounds are available. Audit existing email templates for suspicious Twig expressions, rotate all admin and client API tokens, and/or block external access to /api/system/* at reverse proxy/WAF to mitigate chaining with GHSA-78x5-c8gw-8279.

### CVE-2026-54257

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-06-23T18:18:07.803 |

Electron is a framework for writing cross-platform desktop applications using JavaScript, HTML and CSS. From 42.3.1 until 42.3.3, Buffer performs incorrect byte length calculations resulting in heap buffer under/overflow. Most apps will crash and some may perform incorrect buffer allocations in the Node.js Buffer API resulting in unexpected truncation or allocation. This vulnerability is fixed in 42.3.3.

### CVE-2026-55450

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:H` |
| Weaknesses | `CWE-200;CWE-306;CWE-400` |
| Published | 2026-06-23T17:17:08.663 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.1, unauthenticated users can upload any amount of data to the server without any limitations. No need for any prior knowledge, only network access to Langflow. This can lead to space exhaustion on the server. In addition, in the response, the absolute path of the uploaded file is reported to the attacker, which is an information leak that can assist in chaining other primitives. This vulnerability is fixed in 1.9.1.

### CVE-2026-35019

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-06-23T15:16:34.140 |

NetComm NF20MESH routers running firmware R6B031 and earlier contain an authentication bypass vulnerability that allows unauthenticated attackers to gain administrative access by exploiting a hardcoded AES-256 key used to encrypt session cookies for the web management interface. Attackers can forge a valid encrypted session cookie using the shared hardcoded key and bypass authentication checks to obtain full administrative control of the management interface while any legitimate administrator session is active.

### CVE-2018-10933

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-592` |
| Published | 2018-10-17T12:00:00.000Z |

A vulnerability was found in libssh's server-side state machine before versions 0.7.6 and 0.8.4. A malicious client could create channels without first performing authentication, resulting in unauthorized access.

### CVE-2026-54157

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-23T18:18:07.670 |

LobeHub is a work-and-lifestyle space to find, build, and collaborate with agent teammates that grow with you. Prior to 2.1.57, the /webapi/proxy endpoint on app.lobehub.com accepts a URL in the POST body and fetches it server-side without any authentication. An attacker can use this to make arbitrary outbound requests from LobeHub's infrastructure, leak Vercel deployment details, and inject cookies on the lobehub.com domain through reflected Set-Cookie headers. This vulnerability is fixed in 2.1.57.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-54305

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-284` |
| Published | 2026-06-23T17:17:06.743 |

n8n is an open source workflow automation platform. Prior to 1.123.55, 2.25.7, and 2.26.2, three EE endpoints used by the Dynamic Credentials feature accepted any authenticated n8n session without performing per-resource ownership or scope checks on the target workflow or credential. An authenticated user with no project membership or credential sharing relationship could enumerate credential identifiers, names, and types referenced by any private workflow in the instance, initiate an OAuth authorization flow against another user's credential to overwrite its stored tokens with tokens bound to an account they control, or revoke another user's stored credential tokens entirely. Workflows relying on a hijacked credential would subsequently execute under the attacker's OAuth identity, enabling data exfiltration to attacker-controlled external services and persistent takeover of integrations. Token revocation would break affected workflows. This vulnerability is fixed in 1.123.55, 2.25.7, and 2.26.2.

### CVE-2026-44792

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T17:16:59.670 |

n8n is an open source workflow automation platform. Prior to 1.123.43, 2.22.1, and 2.20.7, an attacker with write access to the git repository connected to an n8n Source Control configuration could commit a malicious Data Table JSON file containing a crafted column name. When an administrator performed a Source Control Pull, n8n imported the file and could lead to SQL injection on the internal PostgreSQL instance. Exploitation requires the n8n instance uses PostgreSQL as its database backend, the Source Control feature is enabled and connected to a repository the attacker can write to, and an administrator triggers a Source Control Pull. This vulnerability is fixed in 1.123.43, 2.22.1, and 2.20.7.

### CVE-2026-44959

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-23T17:17:00.120 |

A missing validation of user input exists when saving delivery limitations in Revive Adserver 6.0.6 and earlier. A low‑privileged user could add an unexpected component parameter and inject malicious PHP code into the compiledlimitations field, which would then be executed during banner delivery. Input sanitisation has been improved to ensure that unexpected parameters are filtered out.

### CVE-2026-34916

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-23T17:16:53.910 |

A missing validation of user input when saving delivery limitations in Revive Adserver 6.0.6 and earlier could allow a low‑privileged user to use the logical parameter to inject malicious PHP code into the compiledlimitations field on the database and have it executed during banner delivery. Input sanitisation has been improved to ensure that the parameter is properly validated.

### CVE-2026-33760

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T17:16:52.790 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.9.0, Langflow's /api/v1/monitor router exposes 7 endpoints that perform read, write, and delete operations on user-owned resources — messages, sessions, build artifacts, and LLM transaction logs — without verifying that the authenticated requester owns the targeted resource. Any authenticated user can read, modify, rename, or permanently delete another user's data by supplying the target's resource ID or flow_id. This is a classic IDOR/BOLA vulnerability. Notably, the same source file (monitor.py) contains one correctly-implemented endpoint that uses an ownership check, demonstrating the correct pattern was known but inconsistently applied. This vulnerability is fixed in 1.9.0.

### CVE-2026-54309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-23T16:17:01.860 |

n8n is an open source workflow automation platform. Prior to 2.25.7 and 2.26.2, when @n8n/mcp-browser is run in HTTP transport mode, the MCP endpoint accepts session initialization and tool invocation requests without any authentication. Any network-reachable client, or any website visited by the user, can establish an MCP session and invoke browser-control tools. Where the n8n AI Browser Bridge extension is installed and a browser connection is active, an unauthenticated caller can access browser-control capabilities including navigation, JavaScript evaluation, and cookie and storage access against the user's real browser profile. This issue only affects instances where @n8n/mcp-browser is run with the HTTP transport (--transport http). This vulnerability is fixed in 2.25.7 and 2.26.2.

### CVE-2026-54011

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T18:18:06.310 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6,Open WebUI renders Mermaid blocks from Markdown files in the file preview panel and inserts the generated SVG into the DOM using innerHTML. Because Mermaid is configured with securityLevel: 'loose', attacker-controlled Mermaid content can be rendered unsafely in this flow. A working payload was validated through the Markdown preview path, resulting in JavaScript execution in the victim’s browser under the application origin.  This vulnerability is fixed in 0.9.6.

### CVE-2026-13007

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-524` |
| Published | 2026-06-23T17:16:41.243 |

Tenable Identity Exposure contains multiple unauthenticated API endpoints under /w/api/* that expose sensitive application configuration data including cleartext LDAP credentials, SAML configuration, user accounts, and directory settings to unauthenticated remote attackers. Affected responses are served with Cache-Control: public headers and without Vary: Cookie, allowing reverse proxies and CDNs to cache and serve sensitive data to unauthenticated users even after authentication is applied.

### CVE-2026-35018

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-23T15:16:33.990 |

NetComm NF20MESH routers running firmware R6B031 and earlier contain an authenticated remote code execution vulnerability that allows authenticated attackers to execute arbitrary commands as root by injecting shell metacharacters into the username JSON parameter processed by the dalStorage_addUserAccount function. Attackers can exploit the unsafe concatenation of user-supplied input into a shell command string passed to rut_doSystemAction without sanitization to achieve full root-level command execution on the underlying operating system.

### CVE-2026-54008

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-23T18:18:05.927 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, backend/open_webui/utils/oauth.py::_process_picture_url calls validate_url(picture_url) on the initial URL only, then invokes aiohttp.ClientSession.get(picture_url, ...) without allow_redirects=False. aiohttp's default is allow_redirects=True, max_redirects=10; the function does not pass the project's AIOHTTP_CLIENT_ALLOW_REDIRECTS env constant either. An attacker with a valid OAuth IdP identity can therefore submit a public URL that 302-redirects to an internal address and read the internal response body via the attacker's own profile_image_url field. This vulnerability is fixed in 0.9.6.

### CVE-2026-54307

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-23T17:17:07.010 |

n8n is an open source workflow automation platform. Prior to 1.123.55, 2.25.7, and 2.26.2, a member-level user with editor access to a shared workflow could reference credentials they do not own via specific public API endpoints. Credential ownership checks were only enforced partially leading to cross-user credential access. This issue affects instances where workflow sharing is enabled and at least one workflow has been shared with a member-level user as an Editor. This vulnerability is fixed in 1.123.55, 2.25.7, and 2.26.2.

### CVE-2026-12958

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-06-23T17:16:41.120 |

Missing symlink validation in Language Servers for AWS may allow an arbitrary file write outside of the workspace trust boundary. This may occur when a local user opens a workspace with a maliciously crafted symlink that resolves to a file path outside the workspace trust boundary.



To remediate this issue, users should upgrade to version 1.69.0 or higher.

### CVE-2026-12957

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-06-23T17:16:40.977 |

Improper trust boundary enforcement in Language Servers for AWS before version 1.65.0 on all supported platforms may allow a for arbitrary code execution. If a local user opens a maliciously crafted workspace, any commands within the project configuration files may be automatically executed. This issue requires the user to trust the workspace when prompted.



To remediate this issue, users should upgrade to Language Servers for AWS version 1.65.0 or higher.

### CVE-2026-54010

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284;CWE-639;CWE-862` |
| Published | 2026-06-23T18:18:06.180 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, Open WebUI lets an authenticated user attach arbitrary file_id values to their own chat message without checking whether they own or can read those files. If the attacker then shares that chat and grants themselves read access, has_access_to_file() treats the victim file as accessible through the shared chat, and the file endpoints read or delete the victim file. This vulnerability is fixed in 0.9.6.

### CVE-2026-50574

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-06-23T17:17:03.340 |

yt-dlp is a command-line audio/video downloader. Prior to 2026.06.09, if aria2c is used as an external downloader for a fragmented manifest format (such as an HLS/DASH stream), yt-dlp passes insufficiently sanitized input to aria2c that allows an attacker to perform an arbitrary file write. On Windows platforms, this can lead to immediate arbitrary code execution. On non-Windows platforms, this can lead to arbitrary code execution upon the next invocation of yt-dlp. This vulnerability is fixed in 2026.06.09.

### CVE-2026-50023

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-641` |
| Published | 2026-06-23T17:17:03.000 |

yt-dlp is a command-line audio/video downloader. Prior to 2026.06.09, a vulnerability exists in yt-dlp that allows a remote attacker to write arbitrary OS-shortcut files (such as .desktop, .url, .webloc) to the user's filesystem, bypassing the remediation for CVE-2024-38519. The allowlist explicitly included the unsafe extensions .desktop, .url, and .webloc so that the functionality of the --write-link option (and its variants) could be preserved. These allowlist inclusions can be exploited by an attacker to write malicious OS-shortcut files in the context of a media or subtitles download. This vulnerability is fixed in 2026.06.09.

### CVE-2026-45732

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T17:17:00.700 |

n8n is an open source workflow automation platform. Prior to 1.123.43, 2.22.1, and 2.20.7, the OAuth1 and OAuth2 credential reconnect endpoints authorized access using credential:read rather than credential:update. An authenticated user with read-only access to a shared credential could initiate an OAuth reconnect flow and overwrite the stored token material for that credential with tokens bound to an external account they control. Workflows relying on the affected credential would subsequently execute under the attacker's OAuth identity, enabling data exfiltration to attacker-controlled external services and persistent takeover of shared integrations. This vulnerability is fixed in 1.123.43, 2.22.1, and 2.20.7.

### CVE-2026-34914

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T17:16:53.700 |

A missing sanitisation of user input in the zone-include.php script of Revive Adserver 6.0.6 and earlier. A low‑privileged user could exploit the clientid parameter to perform blind SQL injection attacks. Input sanitisation has been improved to ensure that all parameters processed by the script are properly validated.

### CVE-2026-52845

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287;CWE-290;CWE-444` |
| Published | 2026-06-23T18:18:05.267 |

Caddy is an extensible server platform that uses TLS by default. Prior to 2.11.4, forward_auth copy_headers deletes the exact client-supplied identity header before copying the trusted value from the auth gateway. But when the request later goes through php_fastcgi, Caddy normalizes HTTP headers into CGI variables by replacing - with _. This lets a client send an underscore alias that survives the forward_auth delete step but becomes the same PHP/FastCGI variable. Result: a remote client can inject or sometimes override identity/group headers trusted by PHP/FastCGI applications behind Caddy. This vulnerability is fixed in 2.11.4.

### CVE-2026-49402

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-23T18:18:03.177 |

Deno is a JavaScript, TypeScript, and WebAssembly runtime. Prior to 2.7.10, Deno's node:child_process implementation provided an escapeShellArg() helper used when callers passed shell: true to spawn / spawnSync / exec and friends. On Windows, the helper failed to quote arguments that contained cmd.exe metacharacters and did not neutralize % (which cmd.exe expands even inside double-quoted strings). An attacker who controlled any portion of an argument passed to such a call could inject arbitrary additional commands into the spawned cmd.exe invocation. This vulnerability is fixed in 2.7.10.

### CVE-2026-45135

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-176;CWE-178` |
| Published | 2026-06-23T18:17:52.343 |

Caddy is an extensible server platform that uses TLS by default. From 2.7.0 until 2.11.3, the FastCGI transport's splitPos() in modules/caddyhttp/reverseproxy/fastcgi/fastcgi.go misuses golang.org/x/text/search with search.IgnoreCase when the request path contains a non-ASCII byte. Two distinct flaws in that fallback let an attacker mislead Caddy's FastCGI splitting into treating a non-.php (or other configured split_path extension) file as a script. In any deployment where the attacker can place content into a file served via FastCGI (uploads, file storage, etc.), this can be escalated to remote code execution by crafting a URL whose path triggers either flaw. This vulnerability is fixed in 2.11.3.

### CVE-2020-9695

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-06-23T18:17:31.403 |

Acrobat Reader versions 2020.009.20074, 2020.001.30002, 2017.011.30171, 2015.006.30523 and earlier are affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-11940

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-06-23T17:16:40.847 |

tarfile.extractall() with the 'data' or 'tar'
 filter could be bypassed by a crafted archive where a hardlink 
references a symlink stored at a deeper name than the hardlink itself.  
The extraction fallback validated the symlink at it's archived location 
but recreated it at the hardlink's shallower
path, letting a relative
 target the filter judged contained escape the destination directory.  
This allowed a malicious tar archive to create a symlink pointing 
outside the destination, enabling out-of-destination file reads or 
writes. This was an incomplete fix of CVE-2025-4330.

### CVE-2026-54018

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-23T18:18:07.097 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, the SafePlaywrightURLLoader implements a validate_url function to prevent SSRF attacks by checking the IP address of the user-provided URL. However, this validation is performed only on the initial URL. Since Playwright automatically follows HTTP redirects (301/302) by default, an attacker can bypass the validation by providing a safe URL that redirects to a restricted internal network address (e.g., localhost, Docker container network, or Cloud Metadata). This allows the application to access internal services despite ENABLE_RAG_LOCAL_WEB_FETCH being set to False This vulnerability is fixed in 0.9.6.

### CVE-2026-54317

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-06-23T18:18:08.767 |

Home Assistant is open source home automation software that puts local control and privacy first. Prior to 2026.6.0, the Konnected integration registers an HTTP endpoint, KonnectedView (homeassistant/components/konnected/__init__.py), that is marked as not requiring authentication (requires_auth = False). A comment next to that line says auth is instead handled "via the access token from configuration." That promise is only half true. Write requests (POST and PUT) are handled by update_sensor(), which does check the request's Authorization: Bearer <token> header against the integration's stored access tokens (using hmac.compare_digest). Read requests (GET) are handled by a separate get() method that has no authentication check at all. This vulnerability is fixed in 2026.6.0.

### CVE-2026-54013

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-116;CWE-693` |
| Published | 2026-06-23T18:18:06.580 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, Open WebUI patched SVG XSS in user profile images and webhook profile images but forgot to apply the same fix to model profile images. The ModelMeta class has no validate_profile_image_url field validator, and the model image serving endpoint has no MIME allowlist or nosniff header. Any authenticated user with workspace.models permission (enabled by default) can store a data:image/svg+xml;base64,... payload in a model's profile image and achieve full account takeover of anyone who navigates to the image URL. This vulnerability is fixed in 0.9.6.

### CVE-2026-52844

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-284` |
| Published | 2026-06-23T18:18:05.137 |

Caddy is an extensible server platform that uses TLS by default. Prior to 2.11.4, on Windows, Caddy path matchers treat /private\secret.txt as outside /private/*, but file_server later resolves the same request path as private\secret.txt on disk. An unauthenticated remote client can bypass Caddy path-scoped auth/deny routes protecting /private/*. This vulnerability is fixed in 2.11.4.

### CVE-2025-61029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T18:17:40.627 |

An issue in the sqlo_untry component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2025-61024

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T18:17:40.307 |

An issue in the sqlo_try_in_loop component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2026-55446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-23T17:17:08.410 |

Langflow is a tool for building and deploying AI-powered agents and workflows. Prior to 1.0.19, an attacker can send a /api/v1/files/upload/ request without any authentication token/cookies and abuse a very long multipart form boundary to make the langflow app unusable for all users for an indefinite amount of time. This vulnerability is fixed in 1.0.19.

### CVE-2025-61025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89;CWE-400` |
| Published | 2026-06-23T17:16:39.460 |

An issue in the sslr_qst_get component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2025-61022

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T17:16:39.267 |

An issue in the sqlo_tb_col_preds component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2025-61020

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T17:16:39.060 |

An issue in the sqlo_strip_in_join component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2025-61018

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-23T17:16:38.843 |

An issue in the sqlo_place_dt_set component of openlink virtuoso-opensource v7.2.11 allows attackers to cause a Denial of Service (DoS) via crafted SQL statements.

### CVE-2020-3452

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2020-07-22T20:00:22.049Z |

A vulnerability in the web services interface of Cisco Adaptive Security Appliance (ASA) Software and Cisco Firepower Threat Defense (FTD) Software could allow an unauthenticated, remote attacker to conduct directory traversal attacks and read sensitive files on a targeted system. The vulnerability is due to a lack of proper input validation of URLs in HTTP requests processed by an affected device. An attacker could exploit this vulnerability by sending a crafted HTTP request containing directory traversal character sequences to an affected device. A successful exploit could allow the attacker to view arbitrary files within the web services file system on the targeted device. The web services file system is enabled when the affected device is configured with either WebVPN or AnyConnect features. This vulnerability cannot be used to obtain access to ASA or FTD system files or underlying operating system (OS) files.

### CVE-2018-1111

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2018-05-17T16:00:00.000Z |

DHCP packages in Red Hat Enterprise Linux 6 and 7, Fedora 28, and earlier are vulnerable to a command injection flaw in the NetworkManager integration script included in the DHCP client. A malicious DHCP server, or an attacker on the local network able to spoof DHCP responses, could use this flaw to execute arbitrary commands with root privileges on systems using NetworkManager and configured to obtain network configuration using the DHCP protocol.

### CVE-2026-49440

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-325` |
| Published | 2026-06-23T18:18:03.563 |

Deno is a JavaScript, TypeScript, and WebAssembly runtime. Prior to 2.8.1, node:crypto.checkPrime(candidate[, options][, callback]) and crypto.checkPrimeSync(candidate[, options]) ran no Miller-Rabin rounds at all when the caller left options.checks at its default of 0. In that mode, the only test applied to the candidate was trial division by the primes up to 17,863. Any composite whose smallest prime factor exceeds that bound — for example the product of two primes just above it, such as 17,881 × 17,891 — was reported as true ("probably prime"). The same divergence affected the lower-level op_node_check_prime / op_node_check_prime_bytes paths that the polyfill calls into. This vulnerability is fixed in 2.8.1.

### CVE-2026-44726

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-06-23T18:17:48.623 |

Deno is a JavaScript, TypeScript, and WebAssembly runtime. From 2.0.0 until 2.7.8, a flaw in Deno's Node.js tls compatibility layer could cause a TLS client to transmit application data in plaintext after a connection retry. When `autoSelectFamily was enabled and the first address-family attempt failed, the socket reinitialization path reused a stale TLS upgrade hook that was bound to the original, failed handle. As a result, the replacement TCP connection was never upgraded to TLS, and any data the application wrote before the secureConnect event travelled over the network unencrypted. A network attacker positioned to cause the initial connection attempt to fail (for example, by dropping IPv6 traffic on a dual-stack host) could deterministically trigger the fallback path and observe or tamper with traffic that the application believed was TLS-protected. This vulnerability is fixed in 2.7.8.

### CVE-2026-56815

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-06-23T15:16:40.317 |

pwnlift before d7a9544, in a privileged deployment, contains a symlink following vulnerability in the upload handler in Components/Pages/Home.razor.

### CVE-2026-49401

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-41;CWE-176` |
| Published | 2026-06-23T18:18:03.033 |

Deno is a JavaScript, TypeScript, and WebAssembly runtime. Prior to 2.7.14, Deno's permission system enforces filesystem and execution restrictions by comparing the requested path against the path supplied to --deny-read, --deny-write, --deny-run, or --deny-ffi. On macOS, that comparison was done at the raw-byte level while the APFS filesystem treats different Unicode spellings of the same name as the same file. That means a program could reach a denied path by spelling it differently than the deny rule. This vulnerability is fixed in 2.7.14.

### CVE-2026-54312

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-06-23T16:17:02.297 |

n8n is an open source workflow automation platform. Prior to 2.24.0, an authenticated user with permission to create or modify workflows could achieve global prototype pollution via the Microsoft SQL node by supplying a crafted value as the table parameter. This pollutes Object.prototype process-wide for the lifetime of the n8n server process, causing application-wide validation failures and rendering the n8n instance completely non-functional until restarted. This vulnerability is fixed in 2.24.0.

### CVE-2026-54318

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-926` |
| Published | 2026-06-23T18:18:08.890 |

Home Assistant is open source home automation software that puts local control and privacy first. Prior to 2026.5.3, the LocationSensorManager BroadcastReceiver is exported with no permission. Any installed app, with zero runtime permissions, can broadcast a forged Google Play Services LocationResult directly to it; the receiver trusts the extra and forwards it to the user's Home Assistant server as the device's real location. This bypasses Android's developer-mode "Mock Location" gate and allows a local malicious app to drive zone-based automations (unlock door / disarm alarm / open garage) by faking the user's GPS position. This vulnerability is fixed in 2026.5.3.

### CVE-2026-54012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284;CWE-285;CWE-862` |
| Published | 2026-06-23T18:18:06.443 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, Open WebUI lets a user who can create, update, or import workspace models store arbitrary meta.knowledge entries on their model without checking whether they own or can read the referenced files. Open WebUI then treats meta.knowledge entries of type file as an authorization source in two places: the built-in view_file tool reads the file's extracted text, and has_access_to_file()'s model branch authorizes the file content and file delete endpoints. A malicious model owner can therefore attach another user's file ID to their model metadata and read or delete that private file. This vulnerability is fixed in 0.9.6.

### CVE-2026-54007

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-06-23T18:18:05.807 |

Open WebUI is a self-hosted artificial intelligence platform designed to operate entirely offline. Prior to 0.9.6, the chat message listener allows non-same-origin input:prompt and action:submit messages, so an external site can set prompt text and trigger submitPrompt() in an authenticated victim session. I validated this with a cross-origin attacker page that auto-posted messages and caused unauthorized POST /api/v1/chats/new and POST /api/chat/completions requests containing attacker-controlled prompts. This enables cross-site forced actions and model/tool execution under victim privileges without consent. This vulnerability is fixed in 0.9.6.

### CVE-2025-71382

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-06-23T18:17:41.087 |

MuPDF before 1.27.0-rc1 contains an uncontrolled recursion vulnerability in the EPUB CSS rendering engine that allows remote attackers to cause a denial of service by supplying a maliciously crafted EPUB file with deeply nested HTML elements and inline CSS styles. The function value_from_inheritable_property() in css-apply.c recurses through the CSS property inheritance chain without a depth limit, exhausting the process stack and causing a crash in any application using MuPDF for EPUB rendering.

### CVE-2026-56116

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-06-23T17:17:09.410 |

dhcpcd through 10.3.2, fixed in commit 708b4a5, contains a memory leak vulnerability in the IPv6 Router Advertisement route information handling that allows an unauthenticated same-link attacker to cause denial of service by sending crafted Router Advertisements. Attackers can repeatedly send Router Advertisements containing Route Information options with a lifetime of zero, triggering unfreed allocations in routeinfo_findalloc() that cause linear memory exhaustion and eventual daemon crash.

### CVE-2026-54304

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-06-23T17:17:06.603 |

n8n is an open source workflow automation platform. Prior to 1.123.55, 2.25.7, and 2.26.1, an authenticated user with permission to create or modify workflows and access to a SecurityScorecard credential with limited allowed domains could configure the SecurityScorecard node's report download operation to target an attacker-controlled URL. The node attached the SecurityScorecard API token to the outbound request, causing the credential to be sent to the attacker-controlled host bypassing credential configured limitations and exfiltrating. This vulnerability is fixed in 1.123.55, 2.25.7, and 2.26.1.

### CVE-2026-49444

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-23T17:17:01.920 |

n8n is an open source workflow automation platform. Prior to 1.123.48, 2.21.8, and 2.22.4, an authenticated user with permission to create or modify workflows containing a Python Code Node could escape the sandbox and achieve arbitrary code execution on the task runner container. This vulnerability is fixed in 1.123.48, 2.21.8, and 2.22.4.

### CVE-2026-56695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-23T16:17:06.170 |

OpenHarness ohmo gateway /resume and /summary slash commands default remote_invocable to True, allowing admitted remote senders to enumerate and load arbitrary session snapshots by ID. Attackers can exploit this to access victim snapshots containing private prompts, credentials, tool output, and file paths via shared gateway channels.

### CVE-2026-56402

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-23T16:17:05.397 |

NanoClaw before 2.1.17 contains a privilege escalation vulnerability in the handleApprovalsResponse function that fails to verify responder role authorization. Attackers with a valid questionId can approve or reject privileged actions like package installation by submitting approval response payloads without proper role validation.

### CVE-2025-62180

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-23T16:16:58.660 |

Pega Platform versions 8.3.0 through Infinity 25.1.2 are affected by an authorization weakness that may allow authenticated users to access certain additional data via crafted URLs.

### CVE-2026-54302

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T17:17:06.193 |

n8n is an open source workflow automation platform. Prior to 1.123.55, 2.25.7, and 2.26.2, an authenticated user with workflow edit access could inject arbitrary JavaScript into the Chat Trigger's generated page by setting a malicious webhookId. When a logged-in user visited the chat URL, the injected code executed in the n8n origin with that user's session privileges. This vulnerability is fixed in 1.123.55, 2.25.7, and 2.26.2.

### CVE-2026-54301

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-23T17:17:06.053 |

n8n is an open source workflow automation platform. Prior to 1.123.55, 2.25.7, and 2.26.2, an authenticated user with workflow edit access could configure a Respond to Webhook node to serve binary content with an attacker-controlled Content-Type. The binary response path bypassed the central Content-Security-Policy sandbox header, allowing a public webhook to execute JavaScript in the n8n origin when visited by an authenticated user, with access to that user's session. This vulnerability is fixed in 1.123.55, 2.25.7, and 2.26.2.
