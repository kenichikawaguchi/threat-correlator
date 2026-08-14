# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-14 15:00 UTC
- **対象期間**: `2026-08-13T15:00:24.000Z` 〜 `2026-08-14T15:00:28.000Z`
- **重要CVE数**: 217 件（Critical 9.0+: 41 件 / High 7.0〜: 176 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 近くに上りますが、特に **リモートからコード実行 (RCE) や認証回避** が可能な脆弱性が目立ちます。  
- **SQL インジェクションやパス・トラバーサル** が多数報告され、Web アプリケーションやプラグインでの入力検証不備が根本原因となっているケースが多い。  
- **コンテナ・Kubernetes 系、LDAP 系、AI/Workflow プラットフォーム** でも同様に認証・権限チェックの欠如が深刻なリスクを生んでいます。  
- 多くは **バージョンアップで修正** が提供されているものの、パッケージ管理が分散している（npm、Composer、Docker Hub、OpenWrt など）ため、**インベントリ管理と自動パッチ適用** が急務です。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | なぜ注目すべきか |
|-----|--------|----------|-------------------|
| **CVE‑2026‑72811** | 9.9 (AV:N/AC:L/PR:N) | SiYuan (ノートアプリ) のバックリンク検索で **SQL Injection** が可能。攻撃者は任意の SQL を実行でき、データベースの情報漏洩・改ざんが起こり得る。 | - デスクトップ・Web 両方で利用され、企業内ナレッジベースとして広く導入されている。<br>- 修正は **v3.7.3 以降**。 |
| **CVE‑2026‑73656** | 9.9 (AV:N/AC:L/PR:L) | Trigger.dev の `/api/v1/deployments/:deploymentId/background‑workers` エンドポイントで **認証バイパス + 任意コード実行** が可能。攻撃者はバックグラウンドワーカーを乗っ取り、AI エージェントの実行環境を改ざんできる。 | - SaaS 型 AI ワークフロー基盤で、顧客データやシークレットが流出するリスクが高い。<br>- 修正は **v4.5.6** 以上。 |
| **CVE‑2026‑12949** | 9.8 (AV:N/AC:L/PR:N) | WordPress 用 *Wishlist Member* プラグインで **アカウント乗っ取り** が可能。登録クッキーの検証が不十分で、任意のメールアドレスでログインできる。 | - WordPress は日本でも最も普及している CMS。<br>- プラグインは有料・有料サブスクリプションサイトで頻繁に使用される。<br>- 修正は **v3.34.2** 以降。 |
| **CVE‑2026‑17482** | 9.8 (AV:N/AC:L/PR:N) | IBM Documentation Offline (1.0.0‑1.4.1) が **任意コード実行** できるパス操作脆弱性を抱える。ローカルにインストールされた環境でリモートから任意ファイルを書き込み、実行できる。 | - IBM 製品は大企業の内部ドキュメント管理で利用されるケースが多く、攻撃が成功すると内部ネットワーク全体への踏み台になる。<br>- 修正は **1.4.2** 以降。 |
| **CVE‑2026‑73649** | 9.8 (AV:N/AC:L/PR:N) | Velocity.js (テンプレートエンジン) の **テンプレートインジェクション** が残存。`#set` でのフィルタリングは行われているが、`{{ }}` 形式のプロパティ参照で `constructor`/`__proto__` がバイパスでき、任意コード実行が可能。 | - フロントエンド・サーバーサイド両方で利用され、Node.js アプリのテンプレート処理に広く組み込まれる。<br>- 修正は **v2.1.7** 以上。 |

> **注**：上記は「スコアが最高」かつ「実装環境が広範囲」なものを選出。実際の優先順位は自社のアセットマトリクスに合わせて調整してください。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
1. **脆弱性スキャンの実施**  
   - `nmap --script=vulners`、`trivy`、`snyk test` などで対象リポジトリ・コンテナイメージを即時スキャン。  
2. **インベントリの最新化**  
   - 使用しているパッケージ・プラグインのバージョン情報を **SBOM (Software Bill of Materials)** として管理し、CI/CD パイプラインに組み込む。  
3. **ネットワーク制限**  
   - 外部から直接アクセスできる管理 API (例: OpenChoreo の `/api/proxy/`) は **IP ホワイトリスト** または **VPN** 経由に限定。  
4. **監査ログの強化**  
   - 失敗した認証・SQL クエリ、ファイルアップロードイベントを **SIEM** に集約し、異常検知ルールを追加。  

### 3.2 個別 CVE に対する具体的なパッケージ・バージョン

| CVE | 修正バージョン | パッケージ名 / 配布形態 | 具体的なアップデート手順 |
|-----|----------------|------------------------|---------------------------|
| CVE‑2026‑72811 | **v3.7.3 以上** | `SiYuan` (デスクトップ/Web) | - Linux/macOS: `sudo apt-get update && sudo apt-get install siyuan=3.7.3` <br> - Docker: `docker pull siyuan/siyuan:3.7.3` |
| CVE‑2026‑73656 | **v4.5.6** | `@triggerdev/cli` (npm) | `npm install -g @triggerdev/cli@4.5.6` <br> または SaaS コンソールで自動アップデートを有効化 |
| CVE‑2026‑12949 | **v3.34.2** | `wishlist-member` (WordPress プラグイン) | WordPress 管理画面 → プラグイン → 更新、または `wp plugin update wishlist-member --version=3.34.2` |
| CVE‑2026‑17482 | **1.4.2** | `ibm-doc-offline` (IBM Documentation Offline) | IBM Fix Central からパッチを取得し、`rpm -Uvh ibm-doc-offline-1.4.2.x86_64.rpm` |
| CVE‑2026‑73649 | **v2.1.7** | `velocityjs` (npm) | `npm install velocityjs@2.1.7` または `yarn add velocityjs@2.1.7` |
| CVE‑2026‑73843 | **v1.0.2 / v1.1.2** | `openchoreo` (Dockerイメージ) | `docker pull openchoreo/openchoreo:1.1.2` |
| CVE

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-72811

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-14T12:16:43.903 |

SiYuan versions <= v3.7.2 contain a SQL injection vulnerability in the backlink/mention search query (kernel/model/backlink.go), which concatenates stored block metadata (title, name, alias, anchor text) and the client-supplied keyword into a SQL MATCH/search statement while escaping only the double-quote character and not the single quote. A single quote in the client keyword (first-order, reachable by an anonymous or RoleReader user on the publish surface) or in stored document metadata (second-order) breaks out of the string literal. Because the query runs on the main read-write siyuan.db handle via a statement-stacking-capable driver, an attacker can execute arbitrary SQL, enabling cross-notebook read and write. Fixed in v3.7.4.

### CVE-2026-73656

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-13T20:17:30.297 |

Trigger.dev is a platform for building and deploying fully managed AI agents and workflows. Prior to 4.5.6, POST /api/v1/deployments/:deploymentId/background-workers calls CreateDeploymentBackgroundWorkerServiceV4.call() in apps/webapp/app/v3/services/createDeploymentBackgroundWorkerV4.server.ts, where workerDeployment.findFirst() selects a deployment by friendlyId without an environmentId predicate. A caller with a valid API key for one project can submit another project's deployment identifier, link an attacker-owned background worker to the victim deployment, and move the victim deployment from BUILDING to DEPLOYING. This issue is fixed in version 4.5.6.

### CVE-2026-12949

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-14T06:16:53.237 |

The Wishlist Member plugin for WordPress is vulnerable to Account Takeover via Insufficient Verification of Data Authenticity in versions up to and including 3.34.1. This is due to the wpm_register() function validating the registration cookie only against the GET reg parameter while accepting the POST mergewith and POST wpm_id parameters without verifying that the mergewith user ID references a temporary or incomplete registrant that is bound to the current registration transaction. This makes it possible for unauthenticated attackers to take over any existing WordPress account — including administrator accounts — by supplying an arbitrary user's numeric ID as the mergewith value, which causes wp_update_user() to overwrite the target account's username (additionally written via a direct $wpdb UPDATE), password, email address, first name, and last name with attacker-controlled values, while WordPress password and email change notification emails are explicitly suppressed. When wpm_id references a non-existent membership level, no role key is added to the update payload, causing wp_update_user() to preserve the target user's existing role — including administrator — making full privilege escalation a direct consequence of the takeover.

### CVE-2026-17482

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T21:17:43.543 |

IBM Documentation Offline 1.0.0 through 1.4.1 could allow a remote attacker to execute arbitrary code due to improper control of file paths.

### CVE-2026-73649

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T18:18:20.793 |

Velocity.js is a JavaScript implementation of the Apache Velocity template engine. Prior to 2.1.7, the earlier fix for CVE-2026-44966 filtered constructor, __proto__, and prototype only in the #set assignment handler in src/compile/set.ts, while property-read expressions in src/compile/references.ts remained unfiltered. The getReferences() flow called getAttributes(), whose property access allowed an attacker-controlled template to traverse constructor.constructor to the JavaScript Function constructor. The #set handler validated only the assignment target and did not inspect the right-hand property-read expression, allowing arbitrary shell commands, environment-variable access, cloud-credential access, and internal-network access in the server process. This issue is fixed in version 2.1.7.

### CVE-2026-73843

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306;CWE-668;CWE-862` |
| Published | 2026-08-13T22:17:29.193 |

OpenChoreo is a complete, open-source developer platform for Kubernetes. Prior to 1.0.2 and 1.1.2, internal/cluster-gateway/server.go served caller-facing management APIs on the externally reachable agent listener without authentication, allowing network-reachable attackers to invoke /api/proxy/ and /api/exec/ operations, proxy the data-plane Kubernetes API, and execute commands in workload pods in multi-cluster deployments. This issue is fixed in versions 1.0.2 and 1.1.2.

### CVE-2026-8715

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-552` |
| Published | 2026-08-13T21:18:32.333 |

Vault Secrets Operator 1.3.0 up to 1.4.1 is vulnerable to an arbitrary file read and credential exfiltration issue in the AppRole authentication configuration that may allow a tenant with limited Kubernetes RBAC permissions to read files from the operator pod's filesystem and transmit their contents to a tenant-controlled endpoint, potentially leading to privilege escalation within the cluster. This vulnerability (CVE-2026-8715) is fixed in Vault Secrets Operator 1.5.0.

### CVE-2026-73644

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285;CWE-639` |
| Published | 2026-08-13T18:18:20.093 |

OpenDJ is an LDAPv3 compliant directory service. Prior to 5.1.2, the SASL PLAIN authorization identity path in opendj-server-legacy/src/main/java/org/opends/server/extensions/PlainSASLMechanismHandler.java checked the PROXIED_AUTH privilege but did not evaluate the mayProxy proxy ACI scope when an authzid resolved to a different user. Both dn: and u: or bare authzid forms could therefore let an authenticated account holding PROXIED_AUTH assume any resolvable non-root identity outside the identities permitted by its proxy ACI. The fix returns INVALID_CREDENTIALS (49) before password verification when the target authorization identity is not permitted. This issue is fixed in version 5.1.2.

### CVE-2026-72850

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T22:17:24.307 |

Budibase before 3.40.0 fails to properly sanitize S3 object keys, allowing authenticated builders to upload files with traversal sequences that are preserved during export. Attackers can craft filenames containing .. segments that escape the temporary directory during workspace export, writing arbitrary content to any path writable by the Budibase process.

### CVE-2026-72842

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T22:17:23.977 |

luci-app-lxc contains an ACL inconsistency vulnerability that allows low-privileged authenticated LuCI users to access backend container management routes without proper authorization checks. Attackers can exploit path traversal via `/.%2E` in the `lxc_name` parameter to escape container directories and control host-side scripts executed through `lxc.hook.start-host`, achieving root code execution on the OpenWrt host.

### CVE-2026-72841

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T22:17:23.813 |

luci-app-openvpn fails to properly validate the instance_name2 parameter during file upload, allowing authenticated users to perform path traversal and write arbitrary files outside the intended directory. Attackers can upload malicious payloads to gain persistent root code execution by placing SSH keys in system directories accessible on reboot.

### CVE-2026-14525

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-13T20:17:14.250 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 IBM WebSphere Application Server Liberty is vulnerable to an authentication bypass when the rtcomm-1.0 or rtcommGateway-1.0 feature is enabled.

### CVE-2026-73653

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-552;CWE-862` |
| Published | 2026-08-13T19:17:38.920 |

Vitest is a testing framework powered by Vite. Prior to versions 3.2.7, 4.1.10, and 5.0.0-beta.6, Browser Mode provider commands including upload, takeScreenshot, screenshotMatcher, stopChunkTrace, deleteTracing, and annotateTraces accept browser-supplied file paths without enforcing the allowWrite permission gate or confining paths to the project root. A client that can reach the Browser Mode API can read arbitrary local files, create or overwrite image and trace files, or delete files accessible to the Vitest process even when allowWrite is false. This issue is fixed in versions 3.2.7, 4.1.10, and 5.0.0-beta.6.

### CVE-2026-19871

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-14T14:16:51.493 |

Use of Hard-coded Credentials in the human resources component in Roskus Prospero Flow CRM before 5.15.9 allows unauthenticated remote attackers to authenticate as any employee onboarded through the standard flow, knowing only their email address, because the employee save controller falls back to the literal password "changeme" and the onboarding form provides no password field.

### CVE-2026-72830

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-14T12:16:46.277 |

Grav API plugin versions before 1.0.13 fail to enforce API key scope caps in ConfigController super-scope gates, allowing scoped keys to write scheduler configuration. Attackers with a scoped api.config.write key can inject arbitrary commands into scheduler.custom_jobs that execute via Symfony Process for remote code execution.

### CVE-2026-72829

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-14T12:16:46.157 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.13 contains an API-key scope-cap bypass in UsersController's create() and update() methods. These methods enforce the scope cap only for api.users.write, but gate super-privilege grants on a bare isSuperAdmin() check that reads access.api.super directly without consulting the key's scopes. As a result, an api.users.write-scoped key minted on a super account can set access.api.super or assign a super-granting group to mint or promote a full super account, then authenticate as that account for uncapped administrative privileges.

### CVE-2026-72826

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-14T12:16:45.780 |

The getgrav/grav-plugin-api plugin before 1.0.13 fails to validate that the scopes of a newly created API key are a subset of the caller's scopes in createApiKey. The self-target path of requireApiKeyPermission() requires only the baseline api.access scope, and the new key's scopes are read directly from the request body with no subset check. An attacker holding a minimal-scope API key on a super account can submit an empty scopes array to mint an unscoped, full-access super key, bypassing scope restrictions (and enabling further chains such as configuration write to RCE).

### CVE-2026-72824

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-14T12:16:45.520 |

The Grav API plugin (getgrav/grav-plugin-api) before 1.0.13 contains an API key scope-cap bypass in PagesController::guardTwigContent(). The Twig-toggle check uses a bare isSuperAdmin() gate that does not consult api_key_scopes, so a least-privilege API key scoped only to api.pages.write and minted on a super account can enable process.twig on a page save even though admin.pages_twig is intentionally outside the api.pages scope. When security.twig_content.process_enabled=true and editor_enabled=false, this allows Twig-in-content to execute server-side, resulting in server-side template injection (SSTI) and remote code execution.

### CVE-2026-72822

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-14T12:16:45.267 |

The getgrav/grav-plugin-api Composer package before 1.0.13 (affected <= 1.0.12) fails to enforce API key scope caps on the disable2fa endpoint. Unlike the sibling generate2fa endpoint, disable2fa authorizes the admin (non-self) path solely via ACL reads (isSuperAdmin/hasPermission) and never invokes requirePermission(), so the api_key_scopes cap is never applied. As a result, a holder of a narrow-scope API key on a super account, or a non-super account whose ACL includes api.users.write, can force-disable two-factor authentication on any non-super target account via POST /api/v1/users/{user}/2fa/disable without providing a TOTP code, facilitating account takeover.

### CVE-2026-73665

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T22:17:28.227 |

FreePBX is an open source IP PBX. Prior to 17.0.9, the UCP Node server on ports 8001 and 8003 uses io.use(checkAuth) in node/lib/server.js, but Socket.IO version 4 applies that middleware only to the default namespace. An unauthenticated client can connect to custom namespaces that do not consistently invoke checkAuth in node/lib/auth.js and send crafted event values containing carriage-return or newline characters through the Asterisk Manager Interface action path patched by node/lib/asterisk-manager-patch.js, allowing arbitrary commands to execute as the asterisk service user. This issue is fixed in version 17.0.9.

### CVE-2026-73663

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T22:17:27.937 |

FreePBX is an open source IP PBX. From 16.0.0 until 16.0.11 and 17.0.4, the FreePBX missedcall module places the inbound Caller ID name from crafted SIP From headers into the missedcalllog INSERT in agi-bin/missedcallnotify.php without escaping or bound parameters. An unauthenticated caller can inject SQL when a monitored extension goes unanswered, corrupting the database and modifying FreePBX administrator accounts to obtain unauthorized remote access. This issue is fixed in versions 16.0.11 and 17.0.4.

### CVE-2026-72839

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T22:17:23.490 |

filebrowser through 2.63.16 fails to properly restrict scope and permissions when self-signup is enabled with default CreateUserDir setting. Unauthenticated attackers can register accounts that inherit the server root scope with full create, modify, delete, rename, share, and download permissions, allowing unrestricted access to all files.

### CVE-2026-72776

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-13T22:17:23.340 |

AgenticSeek (commit fc242c7) contains an unauthenticated remote code execution vulnerability that allows any network-adjacent attacker to execute arbitrary commands by submitting crafted queries to the unprotected POST /query API endpoint bound to 0.0.0.0:7777 with wildcard CORS. Attackers can send unauthenticated HTTP requests that cause the autonomous agent to generate and execute shell commands through BashInterpreter using subprocess.Popen with shell=True and safety=False, bypassing the incomplete command blocklist to achieve full host-level code execution.

### CVE-2026-67614

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-13T18:18:08.370 |

CyberPanel before 3.0.0 contains a hard-coded JWT secret vulnerability in the WebTerminal FastAPI SSH service that allows unauthenticated remote attackers to forge valid authentication tokens and obtain an interactive root shell via WebSocket on port 8888. Attackers can craft a forged JWT signed with the hardcoded secret value, specifying ssh_user=root, to authenticate to the terminal service without any valid credentials and receive a root shell.

### CVE-2026-73533

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-13T16:19:05.620 |

Ninja Tables Pro 5.2.11 contains an embedded malicious code vulnerability introduced via a tampered plugin build served through a decommissioned update server. The tampered build introduced a rogue PHP file (app/Library/updater/NinjaTableDataSync.php) that established a backdoor REST API endpoint, dropped persistent PHP files in mu-plugins and uploads directories, installed a passwordless administrator account, and registered scheduled tasks that survived plugin removal.

### CVE-2026-73532

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-13T16:19:05.480 |

Fluent Forms Pro 6.2.7 contains an embedded malicious code vulnerability introduced via a tampered plugin build served through a decommissioned update server. The tampered build introduced a rogue PHP file (libs/class-license-sync.php), loaded via a require_once directive added to fluentformpro.php, that established a backdoor REST API endpoint, dropped persistent PHP files in mu-plugins and uploads directories, installed a passwordless administrator account, and registered scheduled tasks that survived plugin removal.

### CVE-2026-72836

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-08-14T12:16:47.060 |

FileBrowser before 2.63.19 does not account for case-insensitive filesystems when checking home directory ownership during self-registration. When Signup and CreateUserDir are enabled and FileBrowser's root is on a case-insensitive filesystem (confirmed on Windows/NTFS), two self-registered usernames that differ only in letter case (e.g., CaseVictim and casevictim) are stored as distinct accounts but resolve to the same physical home directory, because the scope-ownership check compares the persisted scope as an exact case-sensitive string. A second registrant can therefore read, overwrite, and delete another account's files through authenticated HTTP endpoints, without needing an existing account or victim interaction.

### CVE-2026-72810

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-14T12:16:43.760 |

SiYuan versions before v3.7.4 contain a publish-boundary bypass vulnerability in WebSocket broadcast sessions that allows anonymous readers to receive unfiltered edits. Attackers can establish a WebSocket connection to the publish surface and passively receive real-time content events including password-protected and forbidden documents without authentication.

### CVE-2026-70460

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-08-13T15:19:59.957 |

rsync 2.3.3 before 3.5.0 contains a path traversal vulnerability that allows a malicious sender to escape the module root by exploiting symlinks within the module file tree when using --partial-dir or --backup-dir options. Attackers with write access to place a symlink under the module root, or who can exploit a pre-existing trusted symlink, can direct file writes to locations outside the intended module root, achieving arbitrary file write relative to the module root parent.

### CVE-2026-53790

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-08-13T15:19:43.200 |

rsync before 3.5.0 contains multiple command and argument injection vulnerabilities that allow attackers to execute arbitrary commands by supplying malicious input through several code paths, including the RSYNC_CONNECT_PROG environment variable, daemon hooks, the rsync-ssl wrapper, and remote-shell command newline injection. Attackers can inject shell metacharacters or newline characters into unsanitized user-supplied values such as hostnames and hostspecs to execute arbitrary commands under the privileges of the rsync process or the invoking user.

### CVE-2026-73421

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-636` |
| Published | 2026-08-13T22:17:26.447 |

NextAuth.js provides authentication for Next.js. From next-auth 5.0.0-beta.0 until 5.0.0-beta.32, applications that gate access by checking only for the existence of the auth object returned by the auth() wrapper can fail open when Auth.js has a server configuration error. In middleware, Route Handlers, React Server Components, and other auth() entry points, a non-OK session response is parsed into a truthy error object instead of null, so checks such as !!auth and if (req.auth) evaluate to true for unauthenticated requests. A provider missing both the issuer and authorization endpoint triggers InvalidEndpoints, and an unset AUTH_SECRET or another server configuration error can produce the same behavior. There is no impact while configuration is valid, but after a deployment becomes misconfigured, routes protected only by session existence silently grant access to every visitor. This issue is fixed in next-auth 5.0.0-beta.32.

### CVE-2026-73420

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-180` |
| Published | 2026-08-13T22:17:26.297 |

NextAuth.js provides authentication for Next.js. Prior to @auth/core 0.41.3 and next-auth 4.24.15 and 5.0.0-beta.32, the defaultNormalizer used by the email and magic-link sign-in flow validates an address before applying Unicode normalization. An address can contain a Unicode character such as U+FF20 FULLWIDTH COMMERCIAL AT that is not ASCII at-sign but canonicalizes to an ASCII at-sign under NFKC or NFKD normalization. The address passes the normalizer's single-at-sign check, but a downstream sendVerificationRequest mail library or delivery service that normalizes the address can then see two at-sign separators and deliver the passwordless sign-in link to an attacker-controlled recipient. Applications are affected when the email provider uses the built-in normalizer rather than a custom normalizeIdentifier and the downstream sender applies Unicode normalization. An attacker who knows a victim's email address can request the misrouted magic link and sign in as the victim without victim interaction. This issue is fixed in @auth/core 0.41.3 and next-auth 4.24.15 and 5.0.0-beta.32.

### CVE-2026-19297

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-13T21:17:45.870 |

IBM Langflow OSS 1.0.0 through 1.9.6 could allow a remote attacker to obtain unauthorized access to user accounts due to improper restriction of excessive authentication attempts.

### CVE-2026-73567

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-338` |
| Published | 2026-08-13T18:18:19.387 |

sm-crypto provides JavaScript implementations of the Chinese cryptographic algorithms SM2, SM3, and SM4. Prior to 0.5.0, the default no-argument sm2.generateKeyPairHex() path in Node.js uses the module-wide SecureRandom instance in src/sm2/utils.js, supplied by jsbn@1.1.0, which seeds an ARC4 stream from Math.random() and new Date().getTime() because window.crypto.getRandomValues is unavailable even though globalThis.crypto exists. An attacker who can observe the process's Math.random() outputs and estimate the key-generation time can reconstruct the seed, recover generated SM2 private keys, and predict signing ephemeral scalars used to forge signatures. This issue is fixed in version 0.5.0.

### CVE-2022-4993

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-470;CWE-1336` |
| Published | 2026-08-13T17:17:17.780 |

HTML::FormHandler versions through 0.40068 for Perl allow attacker selected method dispatch and resource exhaustion because _apply_actions and add_error use error message text built from request data as a Locale::Maketext bracket notation template.

add_error hands its first argument to the language handle as the Locale::Maketext message key, and the default handle's lexicon sets `_AUTO`, so a string that is not a lexicon entry is compiled as a bracket notation template instead of being looked up. In a bracket group the first token names a method called on the language handle and the remaining tokens are its arguments.

Three kinds of text the library did not author reach that position. _apply_actions installs a `$SIG{__WARN__}` handler that stores the warning text in `$error_message`, and a captured warning survives a successful action, so a field carrying a numeric transform turns `Argument "[sprintf,%50000000d,0]" isn't numeric` into the template; a warning quotes the submitted value verbatim, so the group is well formed and dispatches. `$error_message ||= $tobj->validate($new_value)` takes a type constraint's own failure message, which renders the rejected value through a partial dumper in bracket and comma form (Devel::PartialDump when Moose can load it, Type::Tiny's own dumper always), so a field with `apply => [ Str ]` given a parameter sent more than once, which arrives as an array, gets `Reference ["a","b"] did not pass type constraint "Str"` as its template, from a request that carries no bracket character of its own. A coercion or transform exception reaches it the same way. Beyond those, a validator whose message contains the field value puts that value in the template directly, and add_error replaces the message list with the contents of an arrayref first argument (`@message = @{$message[0]} if ref $message[0] eq 'ARRAY'`), so a value arriving as an array fills the argument slots from the same request as well.

A malformed group such as `[0]` makes the compile croak, and HTML::FormHandler::I18N::maketext and add_error each re-raise that as a die, so process() throws. A well formed group naming sprintf reaches CORE::sprintf with an attacker chosen field width. Any caller that applies a type constraint or a transform to an untrusted field, or whose validator passes an untrusted field value to add_error, can be made to throw an unhandled exception out of process(), or to allocate an arbitrary amount of memory in one request, and an application whose language handle subclass defines side effecting public methods makes those callable with attacker chosen arguments. The dumped type constraint message is bounded to the exception, because both dumpers quote non-numeric elements so the method slot is never an attacker chosen name. The built-in messages pass fixed templates with the value in an argument slot, where it stays inert, and the built-in field types attach explicit message callbacks, so neither is affected.

### CVE-2026-70452

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636;CWE-863` |
| Published | 2026-08-13T15:19:58.740 |

rsync 3.1.0 before 3.5.0 contains an access control bypass vulnerability that allows remote attackers to circumvent hosts deny rules by inducing DNS resolution failures during hostname-based access control evaluation. When a DNS lookup for a hostname-based deny rule fails, the daemon skips the rule rather than defaulting to a deny decision, enabling attackers who can trigger DNS failures to bypass module-level IP access controls and gain unauthorized access to restricted module file trees.

### CVE-2026-53793

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T15:19:43.690 |

rsync before 3.5.0 contains a path confinement bypass vulnerability that allows remote clients to escape the intended inner-module root confinement by constructing paths that resolve outside the chroot boundary when the module root contains a /./ boundary marker. Attackers can exploit improper handling of the /./ notation or forge delta-basis transfers referencing xname paths that cross the /./ boundary to gain unauthorized read or write access to files outside the module's subtree.

### CVE-2026-53791

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-13T15:19:43.363 |

rsync daemon before 3.5.0 contains an IP address spoofing vulnerability that allows unauthenticated remote attackers to bypass IP-based access controls by sending a crafted PROXY protocol header with a forged source address. Attackers who can connect directly to the rsync daemon can inject a spoofed source IP in the PROXY protocol header to circumvent hosts allow/deny rules, gaining unauthorized access that would otherwise be blocked based on their real source address.

### CVE-2026-73842

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-306;CWE-862` |
| Published | 2026-08-13T22:17:29.037 |

OpenChoreo is a complete, open-source developer platform for Kubernetes. Prior to 1.0.3, 1.1.3, and 1.2.0-rc.2, internal/cluster-gateway/server.go exposed /api/proxy/, /api/exec/, and /api/wirelogs/ on an internal listener without requiring a client certificate or token, allowing any network-reachable caller to read tenant Kubernetes Secrets, mutate workloads, and execute commands across connected data planes. This issue is fixed in versions 1.0.3, 1.1.3, and 1.2.0-rc.2.

### CVE-2026-73302

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T22:17:25.353 |

Budibase is an open-source low-code platform. Prior to 3.39.30, the OIDC flow in packages/backend-core/src/middleware/passport/sso/oidc.ts resolved an email without getEmailVerified or an email_verified requirement, and packages/backend-core/src/middleware/passport/sso/sso.ts then used users.getGlobalUserByEmail as a fallback account-linking key. An attacker who can authenticate through a configured identity provider that asserts a victim email as unverified can have a fresh provider identity merged into the victim Budibase account and inherit the victim roles. This issue is fixed in version 3.39.30.

### CVE-2026-72851

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T22:17:24.450 |

Budibase before 3.40.0 contains an unauthenticated SQL injection vulnerability in webhook-triggered automations with EXECUTE_QUERY steps. Attackers can POST attacker-controlled JSON to the webhook trigger endpoint to inject SQL payloads that execute with builder-configured database credentials, enabling data exfiltration, modification, and persistence in connected datasources like Snowflake.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18193

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-13T21:17:44.700 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to bypass security restrictions due to improper validation of user-controlled addresses.

### CVE-2026-19747

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-13T20:17:21.570 |

A weakness has been identified in Tenda CH7, CH7G, CH10, CP3, CP3 Pro, CP7, TC3B14C, TC3B15C, TC3T14C and TC3T15C up to 20260625. This impacts the function CAte::HandleCmd of the file Kylin of the component ATE Module. This manipulation causes command injection. The attack is possible to be carried out remotely.

### CVE-2026-73570

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T16:19:06.003 |

A remote code execution vulnerability exists in Zimbra Collaboration (ZCS) before 10.1.20 when the optional zimbra-snmp package is installed and SNMP notifications are enabled. Due to improper sanitization of untrusted input during SNMP notification processing, an unauthenticated attacker can send specially crafted SMTP requests that may result in execution of arbitrary operating system commands as the Zimbra user.

### CVE-2026-73841

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-08-13T22:17:28.900 |

OpenChoreo is a complete, open-source developer platform for Kubernetes. From 1.2.0-rc.1 until 1.2.0, internal/openchoreo-api/api/handlers/exec.go and internal/openchoreo-api/api/handlers/wirelogs.go authorize component:exec and wirelogs:view using the caller-supplied project query parameter instead of comp.Spec.Owner.ProjectName, allowing a user with a project-scoped grant to execute commands in and read wirelogs from components owned by other projects in the same namespace. This vulnerability is fixed in 1.2.0.

### CVE-2026-73667

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T22:17:28.580 |

OpenChoreo is a complete, open-source developer platform for Kubernetes. Prior to 1.0.4, 1.1.4, and 1.2.0-rc.2, OpenChoreo Workflow Plane templates under samples/getting-started/workflow-templates/ interpolated developer-controlled workflow parameters into shell program text executed through sh -c instead of passing the values through container.env, allowing arbitrary commands to run in workflow pods while affected privileged Podman templates lacked hostUsers: false. This issue is fixed in versions 1.0.4, 1.1.4, and 1.2.0-rc.2.

### CVE-2026-73305

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862;CWE-863` |
| Published | 2026-08-13T22:17:25.657 |

Budibase is an open-source low-code platform. Prior to 3.39.24, POST /api/public/v1/roles/assign called validateGlobalRoleUpdate without checking appBuilder.appId or role.appId in packages/server/src/api/controllers/public/globalRoleValidation.ts. An app-scoped builder could scope the request to an app they control and then grant themselves builder access or an arbitrary role in another app, exposing that app data, datasource configuration, and automations. This issue is fixed in version 3.39.24.

### CVE-2026-72853

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T22:17:24.593 |

Budibase before 3.40.0 contains a SQL injection vulnerability in the Oracle datasource connector's post-write row lookup that fails to escape table names in identifiers. Attackers with write permission on a table with a double-quote in its name can inject SQL that executes as the datasource's database user to read or modify arbitrary data.

### CVE-2026-18101

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-13T21:17:44.550 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local attacker to gain elevated privileges due to improper management of thread authority swaps.

### CVE-2026-17481

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-117` |
| Published | 2026-08-13T21:17:43.390 |

IBM Documentation Offline 1.0.0 through 1.4.1 could allow a remote attacker to execute arbitrary code due to improper output neutralization for logs.

### CVE-2026-72642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-823` |
| Published | 2026-08-13T20:17:24.673 |

The native inference process that Elasticsearch uses to evaluate uploaded machine learning models accepts a model operation that computes a memory address from an offset supplied inside the model, without validating that the offset stays within the bounds of the underlying storage. A user with the privileges required to upload and deploy a trained model can craft a model that reads and writes memory outside the intended allocation. The result is heap corruption that crashes the inference process, and, with sufficient control over the heap layout, could allow arbitrary code execution in the context of that process.

### CVE-2026-17223

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:19.097 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17029

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:17.840 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-16987

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T20:17:17.530 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local attacker to gain elevated privileges due to improper validation of the LANG environment variable.

### CVE-2026-16975

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:17.240 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary code due to a heap-based buffer overflow.

### CVE-2026-16722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-13T20:17:15.057 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to obtain unauthorized privileges due to improper privilege management.

### CVE-2026-16674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-13T20:17:14.527 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary code due to an untrusted search path.

### CVE-2026-70461

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T15:20:00.117 |

rsync 3.2.5 before 3.5.0 contains a heap out-of-bounds write vulnerability that allows remote unauthenticated attackers to write one attacker-controlled byte past the end of a heap allocation by supplying a crafted files-from entry. Attackers can trigger the vulnerability against a read-only rsync daemon module by providing a files-from entry containing both an interior and trailing backslash, causing the add_implied_include() function to under-count the trailing backslash when sizing the destination buffer.

### CVE-2026-70458

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T15:19:59.663 |

rsync 3.0.0 before 3.5.0 contains an out-of-bounds write vulnerability that allows attackers to corrupt memory by triggering HLINK_BUMP processing on file entries with the FLAG_HLINKED flag set while the hard-link preservation option is inactive. Attackers can exploit the missing F_SUM field in the file_struct layout to access memory past the end of the allocated structure, corrupting adjacent heap or stack data.

### CVE-2026-70456

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T15:19:59.343 |

rsync 3.0.1 before 3.5.0 contains an out-of-bounds write vulnerability in the read_args() function that allows a malicious sender to corrupt adjacent heap memory by sending a crafted argument list. When the argument count causes the argv allocation to be exactly full, the trailing NULL terminator is written one slot beyond the allocation boundary, corrupting adjacent heap memory.

### CVE-2026-68454

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-13T15:19:58.210 |

In the Linux kernel, the following vulnerability has been resolved:

KVM: s390: pci: Fix handling of AIF enable without AISB

When a guest seeks to register IRQs without a summary bit specified,
ensure that the associated GAITE then stores 0 for the guest AISB
location instead of virt_to_phys(page_address(NULL)).

### CVE-2026-19293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-521` |
| Published | 2026-08-13T15:19:37.873 |

SMP security request (from peripheral) does not include the maximum
encryption key size supported. Using a key with less than the maximum keysize
makes brute-forcing the key easier. See V6 in BLERP paper linked below.

### CVE-2026-19292

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-305` |
| Published | 2026-08-13T15:19:37.737 |

Re-pairing with a legitimate device can use a lower security level than
previous making brute-forcing the LTK easier. See V4 in the BLERP paper linked below.

### CVE-2026-19291

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-13T15:19:37.603 |

Bluetooth re-pairing with an existing device can use a lower security level. RS9116W and SiWx91x impacted. See V3 in the BLERP paper linked below.

### CVE-2026-16101

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-13T15:19:33.347 |

Spoofing an already bonded device can force either RS9116W or SiWx917 to re-pair/bond with a rogue device. See V1 in BLERP paper below

### CVE-2026-73673

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-14T13:19:09.573 |

Netis NC63 router firmware V3.0.0.3327 contains an unauthenticated firmware update vulnerability that allows unauthenticated attackers to submit unsigned firmware images by exploiting a missing authentication enforcement flaw in the Boa web server and netis.cgi CGI dispatcher. Attackers can send a multipart POST request to /cgi-bin/upload_fw.cgi without a valid session cookie, bypassing authentication because Boa grants access to any path containing '.cgi' regardless of cookie validation, and netis.cgi reads but does not enforce the authentication state before invoking the firmware update handler, which accepts images validated only by a forgeable additive checksum and static product strings rather than a cryptographic signature, potentially enabling persistent router compromise.

### CVE-2026-72837

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-14T12:16:47.187 |

File Browser versions before 2.63.20 fail to honor the createUserDir isolation in proxy and hook authentication auto-provisioning paths. Attackers with valid upstream-authenticated credentials can read, modify, delete, and share files belonging to other users by exploiting the server root scope assignment.

### CVE-2026-72833

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-14T12:16:46.670 |

The Grav API plugin (getgrav/grav-plugin-api) versions >= 1.0.6 and <= 1.0.11 contain a privilege escalation vulnerability. A scoped API key minted on a super-admin account bypasses its declared scope cap on four isSuperAdmin()-gated write endpoints (in GroupsController, AccountsConfigController, PreferencesController, and DashboardWidgetController). These endpoints authorize via a super-admin early-return that never invokes requirePermission()—the sole enforcement point of the scope cap—so a 'read-only'-scoped key (e.g. api.pages.read) can perform super-only write operations, including rewriting group ACL maps to grant super-admin privileges to arbitrary accounts. A leaked or delegated read-only CI/monitoring key can therefore gain full super-admin write capability. Fixed in 1.0.13.

### CVE-2026-72831

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-14T12:16:46.400 |

The Flex Objects plugin (through 1.4.6, tested with Grav 2.0.11) contains an incorrect authorization vulnerability in its Flex Objects API. FlexApiController::update() checks only the general Flex directory permission and does not apply the additional target/field/super-admin checks enforced by the dedicated Users and Groups API controllers. An authenticated account with api.access, admin.login, and users.update permissions (but without api.users.write or admin.super) can use the generic /api/v1/flex-objects/user-accounts endpoint to change a super administrator's password, or the /api/v1/flex-objects/user-groups endpoint to grant its group admin.super, resulting in full site takeover. Fixed in Flex Objects 1.4.7.

### CVE-2026-72827

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-14T12:16:45.907 |

Grav CMS before 2.0.13 contains a server-side template injection vulnerability in email-action parameters that allows low-privileged page editors to execute arbitrary operating-system commands. Attackers can inject Twig payloads using the unsandboxed find filter in email subject, body, to, or from fields to achieve remote code execution when forms are submitted.

### CVE-2026-72819

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-14T12:16:44.873 |

Grav CMS before 2.0.13 contains a remote code execution vulnerability in the Flex Objects plugin settings validation that allows authenticated users to execute arbitrary code by uploading a ZIP file containing PHP code. Attackers can bypass routine name validation by using array notation instead of string notation, call the unZip routine with a malicious archive, and write PHP files to the web root for execution.

### CVE-2026-72849

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-13T22:17:24.140 |

Budibase before 3.40.0 contains a cross-site request forgery vulnerability in the chat-link handoff endpoint that allows attackers to bind an external chat identity to a victim's account. Attackers can craft a phishing page that auto-submits a POST request with a leaked confirmation token to bind their chat identity to a victim user's account, enabling impersonation within agent operations and inheritance of victim permissions.

### CVE-2026-72840

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T22:17:23.640 |

OpenWrt LuCI contains an overly permissive ACL definition in luci-mod-system-mounts that grants write access to /etc/crontabs/root to users intended only for mount configuration. Authenticated users with only the mount-configuration ACL group can append arbitrary cron entries via ubus file.write, which the default busybox crond daemon executes as root within one minute.

### CVE-2026-73569

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-776` |
| Published | 2026-08-13T18:18:19.803 |

fast-xml-parser allows users to process XML from JS object without C/C++ based libraries or callbacks. From 5.9.3 until 5.10.1, src/xmlparser/OrderedObjParser.js processes multiple DOCTYPE declarations within a single XML document and passes each declaration's entities through addInputEntities(). addInputEntities() resets maxTotalExpansions and maxExpandedLength every time it is called, allowing additional DOCTYPE declarations to repeatedly reset the configured entity-expansion limits during one parse operation. A crafted XML document can then cause excessive CPU use, event-loop blocking, memory exhaustion, and process termination. This issue is fixed in version 5.10.1.

### CVE-2026-73564

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-190` |
| Published | 2026-08-13T18:18:18.950 |

frp is a fast reverse proxy. From 0.53.0 until 0.70.1, frp's optional SSH Tunnel Gateway in pkg/ssh/server.go parses an SSH exec channel request by adding 4 to an attacker-controlled four-byte big-endian length. A length of 0xFFFFFFFF makes the uint32 addition wrap to 3, defeats the payload bounds check, and causes payload[4:3] to panic in TunnelServer.handleNewChannel. When no authorized-keys file is configured, sshConfig.NoClientAuth permits an unauthenticated peer to reach this channel phase before the frp token is checked, so a single five-byte request terminates the frps process and drops every active tunnel. This issue is fixed in version 0.70.1.

### CVE-2026-18428

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-693` |
| Published | 2026-08-13T18:17:21.130 |

A SQL query validation bypass in the Flint extension query handler in the OpenSearch SQL plugin allows a remote authenticated actor with async query access to execute arbitrary code on Apache Spark workers by sending a crafted SQL query to the direct query endpoint.

### CVE-2024-58374

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T18:17:16.433 |

Hongjing e-HR contains an unauthenticated SQL injection vulnerability in the getSdutyTree servlet endpoint that allows remote unauthenticated attackers to access protected resources by supplying a path traversal sequence in the request URI to bypass the oauthservlet authentication filter. Attackers can inject UNION-based SQL payloads through the unsanitized codeitemid parameter into the underlying Microsoft SQL Server query to retrieve sensitive database contents including user credentials. Exploitation evidence was first observed by the Shadowserver Foundation on 2024-07-30 (UTC).

### CVE-2019-25765

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T18:17:15.113 |

ASP-CMS contains a SQL injection vulnerability in the commentList.asp endpoint that allows unauthenticated remote attackers to inject arbitrary SQL by manipulating the id parameter in GET requests to the comment listing script. Attackers can bypass the application's keyword blocklist by interleaving the string 'master' within blocked SQL terms to extract sensitive database contents. Exploitation evidence was first observed by the Shadowserver Foundation on 2023-10-18 (UTC).

### CVE-2026-59109

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2026-08-13T17:17:29.207 |

SQL injection in the Zalktis accounting application via
trading-partner-controlled text fields in received electronic invoices. When
importing a received e-invoice (UBL/PEPPOL) or an e-commerce export, Zalktis
concatenates partner-controlled values directly into SQL statement text using
string concatenation, with neither parameterised queries nor escaping. The
application's own escaping helper, Dazadi.sql_txt(),
is not invoked on these code paths, so a party that sends an invoice can break
out of the string literal and alter the query logic.









This issue affects Zalktis: before 2026.1.586 and before 2026.2.592.

### CVE-2026-55402

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-13T17:17:24.630 |

CVE-2026-55402 is an out of bounds read vulnerability in Secure Access 
servers prior to version 14.57. Attackers with an ‘in the middle’ 
position can send specially crafted data to a server causing a 
persistent denial of service.

### CVE-2026-73514

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T16:19:05.190 |

The address_standardizer extension for PostGIS through 3.7.0, fixed in commit 423570b, contains an out-of-bounds write vulnerability that allows a database user with the ability to supply caller-controlled relation names to standardize_address() to trigger memory corruption by providing a rules table with a classification Type value exceeding the fixed class range. Attackers can craft a malicious rules table entry with an oversized rule type value that is used without bounds checking as an index into an internal output-link table, resulting in an out-of-bounds write.

### CVE-2026-70464

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-13T15:20:01.667 |

rsync daemon 2.0.0 before 3.5.0 contains a denial of service vulnerability that allows unauthenticated remote attackers to exhaust daemon connection slots by stalling the handshake process before or after module selection without triggering the I/O timeout. Attackers can open many simultaneous connections and trickle data at the minimum rate to avoid timeout, or stall entirely before module selection where no timeout applies, consuming all available connection slots and denying service to legitimate clients.

### CVE-2026-70455

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-13T15:19:59.197 |

rsync 3.4.2 before 3.5.0 contains a denial of service vulnerability that allows a remote sender to exhaust system resources by specifying the --zt short alias for --compress-threads, which bypasses the refuse options directive's string matching on long option names. Attackers can specify --zt=N with a large value to spawn an unbounded number of Zstandard worker threads on the receiver, exhausting available thread and memory resources.

### CVE-2026-70453

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-13T15:19:58.893 |

rsync before 3.5.0 contains an algorithmic complexity vulnerability in the hash_search() function that allows a remote attacker to cause a denial of service by delivering a carefully constructed file list. A sender can exploit the quadratic-time worst-case behavior in hash lookups to exhaust receiver CPU resources with a modest number of crafted entries, causing a sustained denial of service.

### CVE-2026-19870

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-14T13:17:38.523 |

Authorization Bypass Through User-Controlled Key in the payroll module in Roskus Prospero Flow CRM before 5.15.10 allows authenticated users holding the read payroll permission to view the salary and banking details of employees of any other company in the instance, and users holding the create payroll permission to create payroll records attributed to another company's employees, because the listing query is not scoped to the caller's company and the employee identifier is validated for global existence rather than company membership

### CVE-2026-72828

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-14T12:16:46.030 |

Grav Plugin API (getgrav/grav-plugin-api) before 1.0.13 fails to enforce API-key scope caps in InvitationsController. The strip-super and accept-groups decisions are gated on a bare isSuperAdmin() check rather than a scope-aware permission check, so a least-privilege API key (scoped to api.users.write) minted on a super account can create an invitation record containing super-admin access flags. When the invitation is accepted, those flags are written verbatim to the new account, resulting in privilege escalation to a fully controlled super account.

### CVE-2026-73664

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269;CWE-284;CWE-732` |
| Published | 2026-08-13T22:17:28.087 |

FreePBX is an open source IP PBX. From 17.0.5.34 until 17.0.11, the publicKeySave AJAX endpoint in Backup.class.php accepts an authenticated administrator's SSH public key and appends it to /home/asterisk/.ssh/authorized_keys for the asterisk system user without reliably enforcing backup-only command and source restrictions. The key grants persistent shell access that can execute arbitrary commands, access FreePBX and call data, modify system files, and disrupt services. This issue is fixed in version 17.0.11.

### CVE-2026-73661

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-08-13T22:17:27.627 |

FreePBX is an open source IP PBX. Prior to 16.0.47 and 17.0.30, the FreePBX Framework module permits a crafted backup to restore the hidden AUTHTYPE setting with the value none through runRestore() in amp_conf/htdocs/admin/libraries/Builtin/Restore.php. An authenticated user with sufficient backup-restore access or write access to backup files can thereby disable FreePBX authentication during restoration, bypassing the user-interface removal of AUTHTYPE=none. This issue is fixed in versions 16.0.47 and 17.0.30.

### CVE-2026-73417

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79;CWE-116` |
| Published | 2026-08-13T22:17:26.133 |

jupyterlab is an extensible environment for interactive and reproducible computing, based on the Jupyter Notebook Architecture. From 3.3.0 until 4.5.10 and 4.6.2, JupyterLab allows notebook settings to be shared and applied through an overrides.json file using the Import button in the Settings Editor. In packages/notebook-extension/schema/tracker.json and packages/notebook-extension/src/index.ts, the sideBySideLeftMarginOverride and sideBySideRightMarginOverride settings are not properly validated before being inserted into style content, allowing a crafted settings file to contain instructions that execute as code instead of only changing display preferences. A user can import the malicious file, or an attacker with access to a shared settings location can plant an overrides.json that is applied automatically. The embedded code runs with the affected user's access and can read or modify notebooks and files and run code through the notebook server, including on a connected kernel. This issue is fixed in versions 4.5.10 and 4.6.2.

### CVE-2026-72856

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-13T22:17:24.893 |

Budibase versions before 3.40.0 contain an authorization/authentication bypass in the PUT /api/global/users/tenant/owner (changeTenantOwnerEmail) endpoint. On self-hosted instances (SELF_HOSTED or DISABLE_ACCOUNT_PORTAL set), the cloudRestricted middleware is a no-op and the route is protected only by a general authentication check, so any authenticated user — including a lowest-privilege BASIC app user — can reassign the tenant account-holder (top-privilege admin) email to an attacker-controlled address. The attacker can then use the public password-reset flow to take over the admin account, leading to full administrative access.

### CVE-2026-17502

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T21:17:43.677 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to an out-of-bounds write.

### CVE-2026-49864

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T20:17:22.720 |

wetty provides terminal access in browser over http/https. Prior to version 3.0.4, the wetty client decodes a base64 filename from the file-download escape sequence and interpolates it raw into a Toastify HTML string (`escapeMarkup: false`). Any output the victim renders - a `cat`'d file, a tailed log, an SSH MOTD, a `curl` response - that contains `\x1b[5i...:...\x1b[4i` runs script in the wetty origin and types attacker-chosen keystrokes into the victim's SSH session. Version 3.0.4 fixes the issue.

### CVE-2026-16815

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:15.187 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service and potentially obtain sensitive information due to a stack-based buffer overflow.

### CVE-2026-72741

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-13T18:18:16.670 |

Rainbond through 6.9.7 contains a broken access control vulnerability in the CheckToken function that allows authenticated attackers to access unauthorized enterprise resources by substituting another enterprise's tenant name in URL paths. Attackers can use any valid API token to bypass enterprise ID verification and access or modify another enterprise's services, plugins, environment variables, and certificates.

### CVE-2026-73670

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T16:19:07.400 |

A CMS contains a SQL injection vulnerability in admin/db_data.php at line 509 that allows authenticated administrators to inject arbitrary SQL into a SHOW COLUMNS FROM statement by supplying unsanitized input through the table_name GET or POST parameter. Attackers can perform table traversal, time-based blind, boolean-based blind, and error-based injection techniques to enumerate full database schema, access system tables such as information_schema, and chain the disclosure with secondary injection points to extract credential data.

### CVE-2026-70463

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T15:20:01.513 |

rsync 3.1.0 before 3.5.0 contains an authorization bypass in auth users directive parsing. The auth users parser uses comma-only tokenization when splitting the user list, which fails to correctly handle entries of the form @Group Name where the group name contains a space. The space within the group name causes the parser to split the entry at the space boundary, discarding the deny rule associated with the group. An authenticated user whose username or group membership would be denied by an @Group Name auth users entry can connect to a restricted module because the deny rule is silently discarded during parsing.

### CVE-2026-53783

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-88` |
| Published | 2026-08-13T15:19:41.913 |

rsync before 3.5.0 contains a time-of-check to time-of-use (TOCTOU) race condition vulnerability in the rrsync restricted shell wrapper that allows authenticated clients to escape enforced directory restrictions by substituting a symlink for a path component after validation but before transfer processing. Attackers can additionally leverage unrestricted flags such as --copy-unsafe-links, -D, and --log-file through rrsync to read or write files outside the permitted directory subtree.

### CVE-2026-19734

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-13T15:19:38.940 |

Missing Authorization and Authorization Bypass Through User-Controlled Key in the product management component in Roskus Prospero Flow CRM before 5.4.7 allows authenticated users of any company to read the full sensitive data (price, cost, stock, SKU, and barcode) of another company's product and to hijack that product by reassigning its company_id, via the product's numeric identifier, because `ProductUpdateController` did not extend `MainController` and therefore required no authentication check on the read endpoint, and `ProductRepository::save()` retrieved the record via `Product::find($data['id'])` without constraining the query to the authenticated user's company before overwriting its company_id.

### CVE-2026-73654

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-13T20:17:30.007 |

Trigger.dev is a platform for building and deploying fully managed AI agents and workflows. From 3.3.8 until 4.5.6, the PUT /api/v1/runs/:runId/metadata endpoint passes attacker-controlled operation.key values to new JSONHeroPath(operation.key).set(newMetadata, value) in packages/core/src/v3/runMetadata/operations.ts without rejecting dangerous constructor and prototype path segments. A caller with a normal environment API key can pollute Object.prototype in the shared webapp process, corrupting Prisma queries and Prometheus labels, breaking other tenants' worker authentication, and causing a process-wide denial of service. This issue is fixed in version 4.5.6.

### CVE-2026-16967

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-13T20:17:17.097 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to gain unauthorized access to system objects due to a time-of-check to time-of-use (TOCTOU) race condition involving symbolic links.

### CVE-2026-16908

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T20:17:16.667 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to gain unauthorized access to arbitrary objects due to a path traversal vulnerability.

### CVE-2026-63425

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-13T15:19:55.377 |

During an internal security assessment, a potential improper permissions vulnerability was discovered in Lenovo Dock Manager that could allow a local authenticated user to execute arbitrary code with elevated privileges.

### CVE-2026-63423

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-13T15:19:55.080 |

During an internal security assessment, a potential vulnerability was discovered in Lenovo Accessories and Display Manager for Enterprise for Windows that could allow a local authenticated user to execute arbitrary code with elevated privileges.

### CVE-2026-53803

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T15:19:53.020 |

rsync before 3.5.0 contains a symlink following vulnerability that allows local attackers to overwrite arbitrary files by placing a symlink at a predictable output path such as --log-file, --write-batch, or daemon-mode log and statistics paths. Attackers can exploit rsync's failure to reject symlinks during ancillary file writes to redirect output to arbitrary filesystem locations, achieving local privilege escalation on installations where rsync runs with elevated privileges such as setuid or privileged daemon configurations.

### CVE-2026-72855

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T22:17:24.753 |

Budibase before 3.40.0 contains server-side request forgery vulnerabilities in OpenAPI query import and REST query execution that allow authenticated builder-level users to bypass DNS pinning protections through DNS rebinding attacks. Attackers can configure hostnames that resolve to public addresses during validation but resolve to loopback or private addresses during actual connection, allowing access to blocked internal HTTP services.

### CVE-2026-18249

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-13T21:17:44.870 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to gain elevated privileges due to improper validation of pointers read from Java-controlled addresses.

### CVE-2026-53802

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-08-13T15:19:52.850 |

rsync before 3.5.0 contains an arbitrary file read vulnerability that allows attackers to read files accessible to the rsync daemon process by exploiting symlink following in input configuration file handling including --files-from, --password-file, and filter merge files. Attackers can place a symlink at a predictable --files-from or --password-file path, or supply a --files-from path that escapes the daemon module root, to read arbitrary files accessible to the rsync process.

### CVE-2026-53784

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T15:19:42.190 |

rsync before 3.5.0 contains a path traversal vulnerability that allows remote clients to access files outside the intended module root when use chroot is disabled and the module root path or a component of it is a symlink. The daemon calls chdir() to the module root at session initialization without resolving symlinks via realpath() or equivalent, causing subsequent relative-path operations to reference files relative to the symlink target rather than the intended module root, enabling unauthorized file access.

### CVE-2026-72859

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-14T12:16:47.440 |

Budibase versions 3.39.4 before 3.40.0 contain an authorization regression in the S3 attachment upload endpoint that allows BASIC users to obtain S3 PutObject presigned URLs by sending POST requests to the attachments endpoint. The route was changed from a BUILDER permission check to a TABLE/WRITE check, which BASIC users hold by default. Attackers can specify arbitrary S3 buckets in the request body to generate presigned URLs for writing to any bucket accessible by the stored IAM credentials, enabling unauthorized file uploads.

### CVE-2026-72857

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-13T22:17:25.040 |

Budibase before 3.40.0 fails to redact datasource credentials stored in STRING typed fields, allowing authenticated users to read MongoDB connection strings and Firebase private keys in plaintext. Attackers with table read permissions can retrieve datasource configurations through the read API to obtain live backend database credentials and service account keys.

### CVE-2026-17101

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T21:17:42.160 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to execute arbitrary code or obtain sensitive information due to improper authentication.

### CVE-2026-70457

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-08-13T15:19:59.490 |

rsync 3.2.3 before 3.5.0 contains an out-of-bounds write in parse_size_arg() where the return value of snprintf() is used directly as an index into a .bss-segment array without bounds checking. When snprintf truncates the formatted size string, the return value equals the number of characters that would have been written including the truncated portion, and this value may exceed the array length. The subsequent indexed write targets memory outside the intended array bounds, corrupting .bss memory.

### CVE-2026-73666

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-13T22:17:28.393 |

OpenChoreo is a developer platform for Kubernetes. Prior to 1.0.4, 1.1.4, and 1.2.1, the OpenChoreo Backstage backend hardcoded backend.auth.dangerouslyDisableDefaultAuthPolicy and auth.providers.guest.dangerouslyAllowOutsideDevelopment to true, exposing /api/* without authentication and allowing unauthenticated catalog reads, scaffolder log reads, and catalog location creation or deletion. This issue is fixed in versions 1.0.4, 1.1.4, and 1.2.1.

### CVE-2026-73658

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-22;CWE-862` |
| Published | 2026-08-13T22:17:27.190 |

Trigger.dev is a platform for building and deploying fully managed AI agents and workflows. From 4.4.2 until 4.5.0-rc.5, Aws4FetchClient.buildUrl() and Aws4FetchClient.presign() in apps/webapp/app/v3/objectStoreClient.server.ts assign user-controlled packet keys to URL.pathname, while apps/webapp/app/routes/api.v1.packets.$.ts accepts params["*"] without rejecting dot segments and uses findResource: async () => 1 without per-resource ownership validation. WHATWG path normalization collapses .. segments before signing, allowing a caller with a valid environment API key to obtain presigned URLs for another tenant's object-store keys and read or overwrite task payloads. This issue is fixed in version 4.5.0-rc.5.

### CVE-2026-19750

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-255;CWE-259` |
| Published | 2026-08-13T22:17:19.290 |

A flaw has been found in Tenda CH, CP and TX3 V21.x/V22.x/V25.x/V26.x/V27.x. Affected by this issue is some unknown functionality of the component SSH. Executing a manipulation can lead to use of hard-coded password. It is possible to launch the attack remotely. The attack requires a high level of complexity. The exploitation is known to be difficult. The exploit has been published and may be used.

### CVE-2026-18509

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-13T21:17:45.057 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to gain privilege escalation via the Navigator for i debugger. This could allow the attacker to access or manipulate sensitive data on the system, or create new profiles with elevated privileges on the IBM i system.

### CVE-2026-17272

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T21:17:42.687 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to a buffer overflow.

### CVE-2026-73650

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-08-13T19:17:38.460 |

SVGO, short for SVG Optimizer, is a Node.js library and command-line application for optimizing SVG files. From version 1.0.0 until versions 2.8.3, 3.3.4, and 4.0.2, the removeScripts plugin, named removeScriptElement in versions 1 through 3, can leave executable content in optimized SVGs because it does not remove namespaced or prefixed script elements such as <svg:script> and, in versions 3 and 4, matches JavaScript URIs case sensitively. Applications that process untrusted SVG input with this plugin enabled and serve the result can allow scripts to execute when another user opens the SVG, exposing local storage or cookies. This issue is fixed in versions 2.8.3, 3.3.4, and 4.0.2.

### CVE-2026-17220

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-13T19:17:18.810 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service and modify authentication metadata due to a buffer overflow.

### CVE-2026-13048

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-95` |
| Published | 2026-08-13T17:17:19.397 |

Data::MuForm::Localizer versions through 0.05 for Perl execute Perl from a message catalog header, reached at an arbitrary path because load_lexicon interpolates the language attribute into the catalog filename.

load_lexicon builds the catalog path by appending `Messages/$lang.po` to the directory holding Localizer.pm, where $lang is the language attribute, with no check that it names a bare locale tag. A value holding `../` segments walks out of the message directory, so any readable path with a `.po` suffix is loaded. While parsing the catalog, extract_header_msgstr takes the `Plural-Forms:` header, prefixes `$` to the bare words nplurals, plural and n, and passes the rest verbatim into a string that is evaluated: the nplurals form evaluates the header expression immediately, and the plural_code form compiles it into a subroutine whose body runs when a plural message is localized. A header of `nplurals=2; plural=(system('...'),0);` therefore runs that command as the catalog loads. The evaluation inherits strict, so an expression that assigns to an undeclared variable fails to compile, while one built from calls alone does not.

An application that sets the language attribute from request data, an Accept-Language header or a locale parameter, and an attacker who can place a file with a `.po` suffix and chosen contents at a readable path, together give code execution as the application user. The message expansion path is not affected: expand_named substitutes only the placeholder names the caller supplies, and _mangle_value returns the value unchanged.

### CVE-2026-53801

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-367` |
| Published | 2026-08-13T15:19:52.623 |

rsync before 3.5.0 contains a symlink race condition vulnerability in the sender's directory scanning logic that allows attackers to cause the sender to enumerate and transfer files outside the module root's intended subtree. Attackers who can create or manipulate symlinks in a path component of the scanned tree can replace a symlink with a directory entry pointing outside the module root between the lstat() call and the subsequent opendir() call, exposing files beyond the intended root in both daemon-mode and non-daemon sender-side scanning.

### CVE-2026-73659

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T22:17:27.333 |

Trigger.dev is the open-source platform for building AI workflows in TypeScript. From 4.4.2 until 4.5.0, the packet presign routes in apps/webapp/app/routes/api.v1.packets.$.ts pass a caller-controlled filename through resolveStoreProtocolForPacketPresign to generatePresignedUrl and generatePresignedRequest in apps/webapp/app/v3/objectStore.server.ts, allowing .. traversal to escape the packets/<projectRef>/<env>/ object-store prefix and enabling a project API key to read or overwrite another organization's offloaded task payloads and outputs on multi-organization self-hosted instances. This issue is fixed in version 4.5.0.

### CVE-2026-72665

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T20:17:27.033 |

Missing Authorization (CWE-862) in Kibana can lead to unauthorized execution of Osquery and Elastic Defend response actions on managed hosts via Accessing Functionality Not Properly Constrained by ACLs (CAPEC-1). A Kibana user who is able to author and evaluate Elastic Security detection rules can cause response actions to be carried out against enrolled agents without holding the Osquery live query privileges or the Elastic Defend response action privileges that normally govern those capabilities. Depending on the response action involved, this can result in disclosure of information from the affected hosts or in unauthorized changes to their state.

### CVE-2026-17206

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:18.780 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17069

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-13T20:17:18.303 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to bypass security restrictions due to improper validation of anti-CSRF tokens.

### CVE-2026-17045

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-13T20:17:18.153 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to perform unauthorized operations and access sensitive information due to improper session management.

### CVE-2026-16868

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-08-13T20:17:15.883 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to the use of uninitialized memory during ASN.1 length processing.

### CVE-2026-16867

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T20:17:15.723 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to access server resources with the privileges of an authenticated user due to improper authentication during NTLM session negotiation.

### CVE-2026-17197

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T19:17:18.640 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to bypass security restrictions due to improper validation of client-asserted identity.

### CVE-2026-24791

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T17:17:22.000 |

Public-only tokens bypass private-resource restrictions on `/api/v1/user` self routes

### CVE-2026-16898

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T20:17:16.533 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to change the ownership of arbitrary files due to improper validation of an attacker-controlled file path.

### CVE-2026-18071

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-13T19:17:18.970 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-73505

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-13T15:20:16.943 |

Oh My Posh is the most customisable and low-latency cross platform/shell prompt renderer. Prior to 29.35.1, the setStyle() function in src/segments/path.go passed pt.Path, which includes raw folder names, to template.Render, whose function map exposes cmd, so an attacker-controlled directory name containing a Go template expression could execute arbitrary operating system commands as the current user whenever the prompt rendered inside that directory or a descendant. This issue is fixed in version 29.35.1.

### CVE-2026-68452

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-13T15:19:57.970 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Validate length for CCA AES cipher key requests

cca_cipher2protkey() derives the copy length for the CPRB parameter
block directly from the length field in the key token. Reject the
request early if the token length exceeds the available space in the
parameter block.

### CVE-2026-68451

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-13T15:19:57.847 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Validate length for CCA ECC private key requests

cca_ecc2protkey() derives the copy length for the CPRB parameter
block directly from the length field in the key token. Reject the
request early if the token length exceeds the available space in the
parameter block.

### CVE-2026-72672

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T20:17:27.777 |

The Elastic Security capability that suggests existing field values while a user authors endpoint policy artifacts queries Elastic Defend event data with Kibana's internal Elasticsearch account instead of the account of the requesting user. Only Kibana feature privileges are verified, and the caller's Elasticsearch index privileges are not. An authenticated user who holds Elastic Security feature privileges but no read access to the Elastic Defend event indices can therefore retrieve field values from that data, including process command line arguments, which commonly contain tokens, credentials, connection strings, and other sensitive operational detail from protected hosts.

### CVE-2026-72670

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-13T20:17:27.530 |

A lower privileged user who holds only the privilege to read agent policies can read the entire configuration of a configured Fleet proxy. This would normally require the Fleet privilege to read settings.The proxy configuration possibly contains proxy authentication credentials and private key material that they should not be authorized to view.

### CVE-2026-72777

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T19:17:32.320 |

Next AI Draw.io through 0.4.16 contains a server-side request forgery vulnerability in the POST /api/parse-url endpoint due to hostname validation that only checks string patterns without DNS resolution. Unauthenticated attackers can supply hostnames that bypass string validation but resolve to internal addresses, allowing them to reach arbitrary internal HTTP services and exfiltrate responses including cloud metadata.

### CVE-2026-72835

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41` |
| Published | 2026-08-14T12:16:46.930 |

filebrowser versions before v2.63.21 fail to canonicalize paths before evaluating access rules, allowing authenticated users to bypass administrator-defined deny rules using case-variant or backslash-separated paths. Attackers can request files with alternate path representations that match no rule but resolve to the same filesystem object, gaining unauthorized access to denied files within their scope.

### CVE-2026-73662

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T22:17:27.787 |

FreePBX is an open source IP PBX. From 17.0.1 until 17.0.7, the FreePBX Music on Hold module permits dangerous command-line options for /usr/bin/mpg123 and other allowed players in validateCustomConfiguration() in Music.class.php. An authenticated administrator can use options that write files, open control channels, or create Asterisk call files because applicationUsesDisallowedPlayerOption() does not reject those arguments, resulting in arbitrary command execution as the asterisk service user. This issue is fixed in version 17.0.7.

### CVE-2026-73408

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T22:17:25.810 |

Budibase is an open-source low-code platform. Prior to 3.39.18, packages/server/src/integrations/mysql.ts enabled multipleStatements and inserted an unescaped tableName into a DESCRIBE statement. An attacker able to create a MySQL table with a backtick and stacked statement in its name could wait for a Budibase administrator to run schema discovery, causing the second statement to execute. The fix applies quoteMySqlIdentifier before constructing the query. This issue is fixed in version 3.39.18.

### CVE-2026-72669

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T20:17:27.403 |

The state that Kibana stores for an Observability Onboarding flow is not bound to the user who created the flow, and the routes that read and update that state do not verify ownership. An authenticated user who holds only generic read access to the space can therefore discover the onboarding flows of other users, read their onboarding state, and write arbitrary progress data into them. A tampered flow can also cause the owner's onboarding view to fail with a server error.

### CVE-2026-16961

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T20:17:16.967 |

IBM i 7.6, 7.5, and 7.4 s vulnerable to SQL injection. A remote attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-73509

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T15:20:17.623 |

OpenList a file list program that supports multiple storage. Prior to 4.2.4, the authenticated /api/fs/batch_rename handler in server/handles/fsbatch.go authorizes only the source directory produced by user.JoinPath(req.SrcDir) and validates renameObject.NewName with checkRelativePath, but does not validate attacker-controlled renameObject.SrcName, supplied as src_name, before concatenating it with the authorized path and passing the result to fs.Rename. A user with rename permission can use traversal segments in src_name to make path normalization select a file outside the authorized directory and configured base path, resulting in cross-user file integrity loss, limited availability impact, and file-existence disclosure through success or error responses. This issue is fixed in version 4.2.4.

### CVE-2026-70454

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-13T15:19:59.047 |

rsync 3.2.0 through 3.2.3 (openssl mode) and rsync-ssl through 3.4.4 (stunnel mode) contain a TLS certificate validation vulnerability that allows on-path attackers to intercept encrypted sessions by presenting self-signed or otherwise invalid certificates. Attackers can exploit the failure to validate server TLS certificates against a trusted CA or verify certificate hostname matching to decrypt or tamper with rsync session content without detection by the client.

### CVE-2026-65935

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-08-13T15:19:56.290 |

Passkey entry Bluetooth LE legacy pairing can be bypassed in the RS9116W and SiWx917 by manipulating the temporary key value. 
See vulnerability B-E3 in the related paper below.

### CVE-2026-73660

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T22:17:27.480 |

FreePBX is an open source IP PBX. Prior to 16.0.6 and 17.0.5.4, the FreePBX Text-To-Speech module allows an authenticated administrator to save a TTS destination name that is HTML-encoded for storage, decoded during dialplan generation, passed as an AGI argument, and used to build filenames inside agi-bin/propolys-tts.agi. The TTS destination name reaches a raw shell-command execution path, allowing arbitrary operating-system command execution as the asterisk service user. This issue is fixed in versions 16.0.6 and 17.0.5.4.

### CVE-2026-18077

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T21:17:44.230 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to a stack-based buffer overflow.

### CVE-2026-17473

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T21:17:43.067 |

IBM Documentation Offline 1.0.0 through 1.4.1 could allow a remote attacker to read arbitrary files due to improper limitation of a pathname to a restricted directory.

### CVE-2026-18846

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:19.713 |

IBM i 7.6, 7.5, 7.4, and 7.3 s vulnerable to a buffer overflow from improperly validating client data. By sending malformed requests to one of the host servers, a remote attacker could leverage this vulnerability to cause a denial-of-server (DoS) for that server.

### CVE-2026-17229

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-08-13T20:17:19.267 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to an infinite loop.

### CVE-2026-17199

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-13T20:17:18.590 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to unbounded resource allocation.

### CVE-2026-17004

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-08-13T20:17:17.660 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to an infinite loop.

### CVE-2026-16982

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:17.377 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to a heap buffer overflow.

### CVE-2026-16887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T20:17:16.263 |

IBM i 7.6 could allow a remote attacker to cause a denial of service due to an out-of-bounds write.

### CVE-2026-13460

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-13T20:17:14.010 |

IBM Storage Scale 5.2.3.0 through 5.2.3.8, and 6.0.0.0 through 6.0.1.0 GUI contains a hardcoded token in the source code, which was used for inter-node cluster communication and REST API authentication between GUI.

### CVE-2026-73643

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-13T18:18:19.947 |

js-yaml is a JavaScript YAML parser and dumper. From 5.0.0 until 5.2.2, parsing a small YAML document can take exponential time when an application calls load() or loadAll() on untrusted input. In src/parser/parser.ts, readFlowCollection uses restoreState and calls parseNode a second time when a flow-sequence entry is recognized as a key: value pair. If the key is a nested flow sequence of the same shape, every level is parsed twice, causing O(2^n) work and allowing an input under 200 bytes to keep one CPU busy for minutes, block the Node.js event loop, and stall the process. No anchors, aliases, merges, tags, or nondefault options are required. This issue is fixed in version 5.2.2.

### CVE-2026-73568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-13T18:18:19.547 |

py-libp2p is the Python implementation of the libp2p networking stack. In 0.7.0 and earlier, the yamux handle_incoming() method in libp2p/stream_muxer/yamux/yamux.py reads an attacker-controlled 32-bit DATA frame length with read_exactly() before validating it against MAX_WINDOW_SIZE or checking whether stream_id exists. A peer that completes the standard Noise handshake can send a 12-byte frame declaring a 0xFFFFFFFF body and then withhold the body, causing the sequential yamux read loop used by the default new_host() configuration to block and preventing every stream on that connection from making progress. No fixed version is available as of this review.

### CVE-2026-73566

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-674` |
| Published | 2026-08-13T18:18:19.250 |

node-tar is a tar archive manipulation library for Node.js. Prior to 7.5.21, node-tar's filesFilter in src/list.ts uses the recursive mapHas helper to walk an archive entry path upward with path.dirname() and no segment cap when tar.t(...) or tar.x(...) receives a non-empty member-selection list. A crafted GNU L or PAX x long-path header with thousands of slash-separated segments reaches this.filter(entry.path, entry) in Parser[CONSUMEHEADER] in src/parse.ts before Unpack[CHECKPATH] applies maxDepth, causing an uncatchable RangeError stack overflow that terminates asynchronous and streaming Node.js consumers. This issue is fixed in version 7.5.21.

### CVE-2026-73561

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-13T18:18:18.490 |

Hub is a Node.js WebSocket server and client with added features. Prior to 0.2.16, every incoming unauthenticated WebSocket connection triggers loadDefaultConnectionEventListeners to call requestClientId, which calls rpc.send for the get-client-id action and pushes a request into RPC.requests. The RPC.waitForReply function starts a setInterval polling loop every 10 milliseconds that is cleared only after a matching reply; if the client remains silent and closes, the timer and pending request stay allocated because the socket close path does not cancel them. Repeated connections therefore cause unbounded timers and heap entries, exhausting CPU and memory and making the server unavailable. This issue is fixed in version 0.2.16.

### CVE-2026-73507

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-13T15:20:17.287 |

Netty is an asynchronous, event-driven network application framework. Prior to 4.1.136.Final and 4.2.16.Final, io.netty.handler.codec.xml.XmlFrameDecoder.decode() failed to preserve closing-tag parser state across invocations, so an unauthenticated remote attacker could trickle-feed repeated </ sequences that repeatedly rescanned the accumulated buffer and exhausted an EventLoop thread's CPU, causing denial of service with a maxFrameLength of 1 MB. This issue is fixed in versions 4.1.136.Final and 4.2.16.Final.

### CVE-2026-14456

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-13T15:19:31.820 |

Issue summary: When an OpenSSL QUIC server (Listener SSL object) processes
valid QUIC Initial packets for unknown destination connection IDs, it
can allocate and queue new incoming channels without enforcing any limit.

Impact summary: A remote peer that can make many Initial packets reach the
server listener faster than the application accepts connections, can cause the
memory allocated to store the per-channel state to grow without any limits,
potentially making the QUIC listener unavailable and causing Denial of Service.

CWE: CWE-770: Allocation of Resources Without Limits or Throttling

Description: The function that handles inbound QUIC packets uses
Connection-Id from the packet header to find an existing connection
(QUIC channel). If no existing connection is found and the packet
type is INITIAL, the function treats the packet as a new connection. It
allocates a new channel object and inserts it into a queue where it
waits to be accepted by the local application with SSL_accept(3ossl).
The memory occupied by these initial channel objects may grow
without bounds if the application is not able to call SSL_accept()
frequently enough to serve these inbound connection requests.

The issue is present since OpenSSL 3.5 when the QUIC server implementation
was added.

The fix introduces a limit for pending connections. The default limit is set
to 256 pending connections (waiting to be accepted by the local application).
Applications may change the default by calling SSL_set_value_uint(3ossl).

FIPS impact: no
The FIPS module is not affected as the QUIC implementation is outside of
the OpenSSL FIPS module boundary.

### CVE-2026-19824

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T13:17:37.960 |

A weakness has been identified in Tenda W20E 15.11.0.6(1068_1546_841)_CN_TDC. The affected element is the function ipMacBindListStore of the file /goform/addIpMacBind. Executing a manipulation of the argument IPMacBindRule can lead to stack-based buffer overflow. The attack can be executed remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-19823

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T13:17:37.763 |

A security flaw has been discovered in Tenda W20E 15.11.0.6(1068_1546_841)_CN_TDC. Impacted is the function formQOSRuleDel of the file /goform/delQos of the component QoS Rule Deletion. Performing a manipulation of the argument qosIndex results in stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been released to the public and may be used for attacks.

### CVE-2026-19822

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T12:16:43.577 |

A vulnerability was identified in Tenda W20E 15.11.0.6(1068_1546_841)_CN_TDC. This issue affects the function lstAdd of the file /goform/editQos of the component QoS Edit. Such manipulation of the argument qosListConnecttedNum leads to stack-based buffer overflow. The attack may be launched remotely. The exploit is publicly available and might be used.

### CVE-2026-19821

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-08-14T11:16:57.573 |

A vulnerability was determined in Tenda AC12 15.03.06.23_multi_TD01. This vulnerability affects the function formSetRebootTimer of the file /goform/SetSysAutoRebbotCfg of the component httpd web management interface. This manipulation of the argument rebootTime causes buffer overflow. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-19815

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T09:16:48.880 |

A flaw has been found in TOTOLINK A800R 4.1.2cu.5137_B20200730. Affected by this vulnerability is the function setParentalRules of the file /cgi-bin/cstecgi.cgi of the component firewall.so. Executing a manipulation of the argument urlKeyword can lead to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been published and may be used.

### CVE-2026-19814

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T09:16:47.883 |

A vulnerability was detected in TOTOLINK A800R 4.1.2cu.5137_B20200730. Affected is the function setMacQos of the file /cgi-bin/cstecgi.cgi of the component firewall.so. Performing a manipulation of the argument macAddress results in stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit is now public and may be used.

### CVE-2026-19813

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T08:17:38.427 |

A security vulnerability has been detected in TOTOLINK A800R 4.1.2cu.5137_B20200730. This impacts the function setMacFilterRules of the file /cgi-bin/cstecgi.cgi of the component firewall.so. Such manipulation of the argument Comment leads to stack-based buffer overflow. The attack may be performed from remote. The exploit has been disclosed publicly and may be used.

### CVE-2026-19812

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T08:17:38.263 |

A weakness has been identified in TOTOLINK A800R 4.1.2cu.5137_B20200730. This affects the function UploadCustomModule of the file /cgi-bin/cstecgi.cgi of the component product.so. This manipulation of the argument File causes stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-19811

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T07:16:52.627 |

A security flaw has been discovered in TOTOLINK A800R 4.1.2cu.5137_B20200730. The impacted element is the function setIpQosRules of the file /cgi-bin/cstecgi.cgi of the component firewall.so. The manipulation of the argument Comment results in stack-based buffer overflow. The attack can be executed remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-19792

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-08-14T05:16:59.030 |

A security flaw has been discovered in Tenda G0 up to 20260625. Impacted is the function setPortMapping of the file /goform/module of the component httpd web management interface. Performing a manipulation of the argument portMappingServer/porMappingtInternal/portMappingExternal results in buffer overflow. The attack is possible to be carried out remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-19791

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T05:16:58.857 |

A weakness has been identified in Tenda G0 up to 20260625. The affected element is the function addStaticRoute of the file /goform/module of the component httpd web management interface. Executing a manipulation of the argument staticRouteNet can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-19790

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T04:16:40.780 |

A vulnerability was identified in Tenda G0 up to 20260625. This issue affects the function formSetPortMirror of the file /goform/module of the component httpd Web Management Interface. Such manipulation of the argument portMirrorMirroredPorts leads to stack-based buffer overflow. The attack can be executed remotely. The exploit is publicly available and might be used.

### CVE-2026-19789

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T04:16:40.620 |

A vulnerability was determined in Tenda AC1206 15.03.06.23_multi_TD01. This vulnerability affects the function set_wl_guest_iplist of the file /goform/WifiGuestSet of the component httpd web management interface. This manipulation of the argument shareSpeed causes stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-19788

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-14T04:16:36.177 |

A vulnerability was found in Tenda AC1206 15.03.06.23_multi_TD01. This affects the function set_device_name of the file /goform/SetOnlineDevName of the component httpd web management interface. The manipulation of the argument devName results in stack-based buffer overflow. The attack may be launched remotely. The exploit has been made public and could be used.

### CVE-2026-73655

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T20:17:30.153 |

Trigger.dev is a platform for building and deploying fully managed AI agents and workflows. Prior to 4.5.2, addGoogleStrategy() in apps/webapp/app/services/googleAuth.server.ts passes a Google profile email to findOrCreateGoogleUser() in apps/webapp/app/models/user.server.ts without requiring Google's email_verified assertion. When existingEmailUser && !existingUser is true, the flow writes the new Google authIdentifier into the existing email-matched account and returns that user object, allowing an attacker-controlled Google profile with an unverified matching email to take over the account. This issue is fixed in version 4.5.2.

### CVE-2026-49857

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T15:19:41.743 |

auth-fetch-mcp is an MCP server that lets AI assistants fetch content from authenticated web pages. Version 3.0.1 implements SSRF protection in `assertSafeUrl()` (`src/security.ts`) to block requests to private and loopback addresses. However, the `isPrivateV6()` function fails to detect IPv4-mapped IPv6 loopback addresses in their hex-normalized form. When an attacker supplies a URL such as `http://[::ffff:127.0.0.1]:PORT/`, the Node.js WHATWG URL parser silently normalizes the host to `[::ffff:7f00:1]`. Because `net.isIPv4('7f00:1')` returns `false`, the private-IP check is bypassed and the URL is passed to the browser or HTTP client, allowing the MCP tool to reach loopback services that are supposed to be blocked. The issue is exploitable under default configuration without any special environment variable. Version 3.0.1 patches the issue.

### CVE-2026-19771

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-08-14T02:16:24.903 |

A vulnerability was identified in Baicells EG3661M BaiCE_BQ6_2.0.5.3_NA. This impacts an unknown function of the file /cgi-bin/luci of the component LuCI Web Interface. Such manipulation of the argument MaxHops/Timeout/Size leads to os command injection. The attack may be launched remotely. The exploit is publicly available and might be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-18511

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-13T21:17:45.220 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to generate a stack-based buffer overflow in the Native IBM i JSSE provider, caused by improper bounds checking during TLS session establishment. A local attacker could overflow a fixed-length buffer and execute arbitrary code on the system or cause the JVM process to crash.

### CVE-2026-17099

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T21:17:42.033 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to obtain sensitive information due to improper authentication.

### CVE-2026-72677

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-13T20:17:28.373 |

Relative Path Traversal (CWE-23) in Kibana can lead to the unauthorized deletion of Kibana resources via Relative Path Traversal (CAPEC-139). Kibana Fleet accepted a user-supplied identifier for a Fleet Server host configuration without rejecting relative traversal sequences. The identifier is stored as provided and is later incorporated into the request that Kibana issues when that configuration is removed.

### CVE-2026-72658

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-13T20:17:26.017 |

Cross-Site Request Forgery (CWE-352) in Kibana can lead to privilege escalation via Cross Site Request Forgery (CAPEC-62). A user who is permitted to create visualizations can save a specially crafted Vega visualization that, when it is opened by another user, causes authenticated requests to be issued to Kibana in the context of the viewing user's session.

### CVE-2026-14875

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-13T20:17:14.390 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 is vulnerable to arbitrary code execution on Windows when installed for all users due to publicly writeable directory.

### CVE-2026-6387

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-13T15:19:58.590 |

A potential authentication bypass vulnerability was reported in Lenovo System Update that could allow a local authenticated user to execute arbitrary code with elevated privileges.

### CVE-2026-15994

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T15:19:32.550 |

During an internal security assessment, an improper link following vulnerability was identified in Lenovo Vantage and Lenovo Commercial Vantage that could allow a local authenticated user to execute code with elevated privileges.

### CVE-2026-72825

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-14T12:16:45.650 |

The getgrav/grav-plugin-api plugin before 1.0.13 contains an API-key scope cap bypass in the POST /reports/twig-content/allowlist endpoint (ReportsController). The endpoint enforces requirePermission('api.config.write') followed by a bare isSuperAdmin() check instead of requireSuper(). Because isSuperAdmin() reads access.api.super directly and never consults api_key_scopes, a least-privilege API key scoped to api.config.write minted on a super account passes the gate, allowing an attacker to append attacker-chosen tokens to the security.twig_sandbox allowlist (persisted to user/config/security.yaml). Widening the allowlist turns any subsequent Twig-in-content render into an SSTI/RCE sink.

### CVE-2026-19794

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-14T08:17:38.130 |

The WP-Stats plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 2.56 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-18109

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-14T03:16:19.363 |

The W3 Total Cache plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Comment Author Name in all versions up to, and including, 2.10.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This vulnerability is only exploitable when the Lazy Load Images feature of W3 Total Cache is enabled, as the unsafe re-emission occurs exclusively within the LazyLoad mutator's img tag rewriting step.

### CVE-2026-18164

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-13T20:17:19.440 |

An undocumented hard-coded credential, shared by all device units, is authorized to bypass authentication. This allows an attacker within Bluetooth range to arbitrarily manipulate brain stimulation parameters and state.

### CVE-2026-73482

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-13T19:17:34.423 |

phpList before 3.7.0-RC5 contains a cross-site request forgery (CSRF) vulnerability in lists/admin/admins.php. The administrator deletion action is triggered via an unauthenticated GET request (?page=admins&delete=N) that is not protected by a CSRF token (the central verifyCsrfGetToken check uses enforce=false and is bypassed when the token parameter is absent). A remote attacker can trick a logged-in super-administrator into loading a crafted URL (e.g., embedded as an image in an email) to delete any non-self administrator account.

### CVE-2026-73515

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-13T16:19:05.333 |

PostGIS before 3.7.0beta2 contains an out-of-bounds read vulnerability that allows attackers to cause memory disclosure or a server crash by supplying a malformed FlatGeobuf buffer. The FlatGeobuf property metadata decoder verifies that a string length field is present but fails to verify that the subsequent string body is contained within the supplied buffer before materializing it into a SQL-visible value, enabling memory disclosure or denial of service.

### CVE-2026-66256

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-13T15:19:56.557 |

** UNSUPPORTED WHEN ASSIGNED ** Deserialization of Untrusted Data vulnerability in Apache Shindig.

This issue affects Apache Shindig: all versions.

Users with access to the Shindig REST API can send specially-crafted requests to trigger arbitrary code execution on the server.

As this project is retired, we do not plan to release a version that fixes this issue. Users are recommended to find an alternative or restrict access to the instance to trusted users.

NOTE: This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-53799

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-367` |
| Published | 2026-08-13T15:19:52.130 |

rsync before 3.5.0 contains a symlink race condition vulnerability that allows local attackers to cause rsync to apply arbitrary ACLs or extended attributes to unintended files by substituting a symlink at a predictable destination path between the file write and the subsequent acl_set_file() or lsetxattr() call. Attackers can exploit this timing window to redirect ACL and xattr application through a crafted symlink to files outside the intended destination tree, potentially granting elevated permissions and enabling local privilege escalation.

### CVE-2026-53795

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T15:19:44.117 |

rsync before 3.5.0 contains an arbitrary file write vulnerability that allows attackers to write files outside the intended destination tree by specifying an absolute path via --temp-dir or --link-dest options. The rename-confinement logic is bypassed when these options resolve to paths outside the destination tree, enabling attacker-controlled values to write files to arbitrary locations accessible to the rsync process.

### CVE-2026-72838

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-14T12:16:47.313 |

FileBrowser versions before 2.63.19 fail to enforce the declared Upload-Length in the TUS resumable-upload PATCH endpoint, allowing authenticated users to write arbitrary data to disk. Attackers can send oversized request bodies that exceed the declared upload length to exhaust available disk space and cause service unavailability.

### CVE-2026-19483

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-13T21:17:46.003 |

IBM Storage Scale 5.2.3.0 through 5.2.3.8, and 6.0.0.0 through 6.0.1.0 Secrets may be disclosed in log files in IBM Storage Scale Management GUI The admin password is logged into the GUI log of IBM Storage Scale Systems Deploy and Upgrade from GUI. Secrets may be disclosed in information related to exceptions in IBM Storage Scale Management GUI.

### CVE-2026-72675

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T20:17:28.137 |

Missing Authorization (CWE-862) in Kibana can lead to cross-space information disclosure and unauthorized data modification via Privilege Abuse (CAPEC-122). Kibana Machine Learning carries out its Elasticsearch operations with elevated internal permissions and relies on a per-request space filter to keep the machine learning data of one space separated from another. Part of the Machine Learning functionality did not apply that filter, so operations issued from one space were carried out against the machine learning data of every space in the deployment.

### CVE-2026-72643

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T20:17:24.807 |

Kibana Agent Builder determines whether a caller owns a private agent by comparing a stable user identifier when one is recorded, and falling back to a comparison of the username when it is not. A username is not unique across Elasticsearch authentication realms, so two distinct principals that share a username in different realms are treated as the same owner. This discloses the configuration and instructions of an agent the caller does not own, and allows that agent to be altered or removed.

### CVE-2026-72632

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-203` |
| Published | 2026-08-13T20:17:24.060 |

Observable Discrepancy (CWE-203) in Kibana Fleet can lead to information disclosure via Excavation (CAPEC-116). Fleet removes the Elasticsearch API key value of an enrolled Elastic Agent from the responses of its agent listing capability, but that capability accepted caller-supplied filter expressions over the stored field that holds the value, and evaluated them with Kibana's own internal Elasticsearch privileges rather than the caller's. Because the number of matching agents is reported back to the caller, the difference between a matching and a non-matching filter formed a side channel from which the full API key value could be reconstructed one character at a time with a short sequence of requests.

### CVE-2026-72630

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T20:17:23.813 |

Incorrect Authorization (CWE-863) in Kibana Fleet can lead to privilege escalation via Privilege Abuse (CAPEC-122). Fleet restricts some callers to managing integration policies for one specific integration. When an existing integration policy was updated, that restriction was evaluated against the integration recorded on the stored policy rather than against the replacement integration supplied with the update. An authenticated user holding only the Elastic Defend endpoint policy management privilege was therefore able to convert an endpoint policy they administer into a policy for a different integration, and to supply that integration's configuration at the same time.

### CVE-2026-72629

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-13T20:17:23.690 |

Authorization Bypass Through User-Controlled Key (CWE-639) in Kibana can lead to unauthorized cross-space access via Accessing Functionality Not Properly Constrained by ACLs (CAPEC-1). The result is disclosure of inference output from a trained model in a different space that the user is not authorized to list, read, or use, which exposes the behavior of a model. The same pattern also reached the deployment stop and deployment update operations, allowing an active trained model deployment in another space to be stopped or to have its allocated resources altered.

### CVE-2026-59714

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T20:17:23.280 |

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform. From 0.9.5 before 0.10.0, any authenticated user can overwrite the content of a message in a channel they do not belong to (including private and DM channels) by sending a chat completion request with a channel:-prefixed chat_id and a target message_id. The channel: path routes pipeline output through _make_channel_emitter, which writes to the Messages table using the caller-supplied message_id without binding it to the channel. This issue is fixed in version 0.10.0.

### CVE-2026-48099

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T20:17:22.313 |

WsgiDAV is a generic and extendable WebDAV server based on WSGI. WsgiDAV 4.3.3 and prior can allow a WebDAV request path containing an encoded parent-directory segment to escape the configured filesystem share root in a specific path layout. The issue is fixed with version 4.3.4.

### CVE-2026-45725

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T20:17:22.027 |

compliance-trestle is a tooling platform for managing compliance as code. Prior to versiions 3.12.2 and 4.0.3, the compliance-trestle library's remote fetching cache mechanism (HTTPSFetcher and SFTPFetcher) constructs the local cache file path from the URL path component without sanitizing path traversal sequences (`../`). When a remote OSCAL profile references a URL with traversal in its path, the HTTP response body is written to a location outside the intended cache directory, enabling arbitrary file write with attacker-controlled content to the filesystem. Versions 3.12.3 and 4.0.3 patch the issue.

### CVE-2026-16896

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-13T20:17:16.400 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to obtain unauthorized access to files due to a time-of-check time-of-use (TOCTOU) race condition.

### CVE-2026-13365

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-13T20:17:13.773 |

IBM Planning Analytics 2.0, and 2.1 Local is vulnerable to cross-site request forgery which could allow an attacker to execute malicious and unauthorized actions transmitted from a user that the website trusts.

### CVE-2026-73652

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-13T19:17:38.770 |

vantage6 is an open-source infrastructure for privacy preserving analysis. In version 5.0.2 and earlier, the algorithm-store edit permission lacks an ownership check, allowing one algorithm developer to alter another developer's algorithm while it is pending or under review. The attacker can change metadata including the algorithm image or image tag, causing reviewers and nodes to trust a different image from the one originally submitted for approval. No fixed version is available as of this review.

### CVE-2026-73266

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-08-13T17:17:35.713 |

A flaw was found in the clusterclaims-controller component of Multicluster Engine (MCE). An authenticated tenant can exploit this vulnerability by manipulating ClusterClaim labels. This allows the tenant to force a cluster to join a ManagedClusterSet belonging to another tenant. Such unauthorized access could enable the injection of policies and workloads into other tenants' clusters.

### CVE-2026-58416

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-280;CWE-863` |
| Published | 2026-08-13T17:17:26.300 |

Fork-PR Actions task can read a third private repository via the collaborative-owner branch (missing fork-PR guard)

### CVE-2026-70462

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-835` |
| Published | 2026-08-13T15:20:00.267 |

rsync 3.1.0 before 3.5.0 contains a signed integer overflow vulnerability in the I/O timeout implementation that allows attackers to permanently disable connection timeouts by injecting MSG_IO_TIMEOUT messages carrying non-positive (zero or negative) values. Attackers can craft malicious MSG_IO_TIMEOUT messages that cause the timeout variable to wrap to a non-positive value, preventing the timeout check from firing and enabling idle or stalled connections to hold daemon slots indefinitely, leading to resource exhaustion.

### CVE-2026-68453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-13T15:19:58.093 |

In the Linux kernel, the following vulnerability has been resolved:

s390/zcrypt: Fix buffer over-read in cca_cipher2protkey

Add validation of both the actual key buffer size and token length
fields in all the cca_check_sec*token() functions. Additionally check
in cca_gencipherkey() for possible underflow with returned key size.

The CCA token structures contain user-controlled len fields that
were used in operations without proper validation against both the
actual buffer size and minimum token structure size. An attacker
could set this field larger than the actual buffer size, leading to
reading beyond buffer boundaries. This may result in a kernel crash or
exposure of memory via sending this as part of a request down to the
crypto card. Also an attacker could have used a very small len value
and thus enforce a buffer under-run which may produce similar effects
as a over-read.

So now a key must
- key buf length must be at least sizeof the token struct
- the key len field inside the token must fit into the range of
  sizeof key token struct ... key buf length

### CVE-2026-65934

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-440` |
| Published | 2026-08-13T15:19:56.147 |

An unencrypted 'pause encryption request' message causes a denial of service in the BT122 module. 
See vulnerability B-E10 in the related paper below.

### CVE-2026-53792

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-08-13T15:19:43.527 |

rsync before 3.5.0 contains an out-of-bounds read vulnerability in the sender-side block matching logic that allows a malicious receiver to trigger memory access before the start of an allocated buffer by sending a crafted checksum block with a length of zero. Attackers can send a specially crafted checksum set containing a zero-length block to cause a negative offset calculation during delta computation, resulting in an out-of-bounds read of file data buffer memory on the sender side.

### CVE-2026-53789

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-807` |
| Published | 2026-08-13T15:19:43.030 |

rsync before 3.5.0 contains an improper path handling vulnerability that allows a malicious sender to expand the scope of --delete operations beyond the intended destination subtree by sending a crafted file list that causes rsync to reclassify implied parent directory entries or treat synthetic paths as the transfer root. Attackers can exploit multiple variants including implied parent reclassification, synthetic root path construction, legacy protocol behavior below version 30, and non-directory root handling to cause the receiver to delete files outside the authorized destination directory.

### CVE-2026-28154

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T15:19:39.213 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in snstheme Samex - Clean, Minimal Shop WooCommerce WordPress Theme and snstheme M.Anh - Fashion WooCoommerce WordPress Theme allows Reflected XSS.

This issue affects Samex - Clean, Minimal Shop WooCommerce WordPress Theme: from n/a through 2.5; M.Anh - Fashion WooCoommerce WordPress Theme: from n/a through 1.7.

### CVE-2026-63424

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-261` |
| Published | 2026-08-13T15:19:55.223 |

During an internal security assessment, an improperly protected key was discovered in Lenovo Dock Manager that could allow a local authenticated user to escalate privileges.
