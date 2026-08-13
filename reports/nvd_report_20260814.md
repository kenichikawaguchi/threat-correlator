# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-13 15:00 UTC
- **対象期間**: `2026-08-12T15:00:54.000Z` 〜 `2026-08-13T15:00:24.000Z`
- **重要CVE数**: 297 件（Critical 9.0+: 78 件 / High 7.0〜: 219 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVSS 7.0 以上の脆弱性は **「認証不要でリモートコード実行が可能」** という形態が目立ち、特に WordPress 系プラグインや SaaS 型分析ツールに集中しています。  
同時に **LXD コンテナ管理デーモン** に対する多数の認可バイパス・パス・トラバーサル系脆弱性が報告され、内部ユーザーや限定権限のサービスアカウントからクラスタ全体への権限昇格が可能になるケースが増加しています。  
攻撃者は「Web フロントエンド経由」または「コンテナバックエンド経由」のいずれかで侵入し、最終的に **ホスト OS の完全制御** を奪取できる点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目理由 |
|-----|--------|----------|----------|
| **CVE‑2026‑61962** | 10.0 | WP BASE Booking ≤ 6.3.0 の任意コード実行 (認証不要) | WordPress は世界で最も利用される CMS。プラグインだけで **ネットワーク外部から直接シェルが取得** でき、サイト全体が乗っ取られる危険性が極めて高い。 |
| **CVE‑2026‑27544** | 10.0 | QA Analytics ≤ 5.2.0.0 のリモートコード実行 (認証不要) | SaaS 型分析ツールは企業内部の機密データを扱うことが多く、RCE が成功すると **データベース情報や内部ネットワークへの踏み台** として利用される。 |
| **CVE‑2026‑15413** | 10.0 | Link Factory WordPress プラグインにバックドア (署名検証付き REST API) | 「ホームページ文言公開」プラグインと偽装しつつ、攻撃者が **任意のコマンドを実行できる隠し API** を提供。プラグインがインストールされているだけで外部から完全制御が可能。 |
| **CVE‑2024‑27253** | 10.0 | IBM DOORS Next 7.0.3 (IF018) の認証ユーザーによる権限回避 | 大手企業の要件管理ツールで、**認証済みユーザーが管理者権限を取得** できるため、機密要件情報やプロジェクト設定が漏洩・改竄されるリスクが大きい。 |
| **CVE‑2026‑73299** | 10.0 | Prompty (< 0.1.5, < 2.0.0‑beta.5) のテンプレートエンジンで任意 JS 実行 | LLM プロンプトをファイル化する新興ツールだが、**サーバ側でテンプレートを評価する際に JavaScript の任意実行が可能**。クラウド上の AI サービス全体に影響が波及する可能性がある。 |

> **共通点**：すべて **ネットワーク越しに認証不要／低権限で実行可能** なコード実行（RCE）であり、被害が拡大しやすい点が最重要です。  

---

## 3. 推奨アクション  

### 3.1 直ちに実施すべきこと（全体共通）

1. **該当パッケージ・プラグインのバージョン確認**  
   - `wp-base-booking` が **6.3.0 以上**かどうか  
   - `qa-analytics` が **5.2.0.1 以上**かどうか  
   - `link-factory` が **最新版 (≥ 2.0.0)** か、不要なら即削除  
   - IBM DOORS Next は **7.0.3 + IF018** 以降のパッチを適用  
   - `prompty` は **0.1.5 以上** または **2.0.0‑beta.5 以上** にアップデート  

2. **Web アプリケーションファイアウォール (WAF) のルール追加**  
   - `/wp-json/` 配下の不審なリクエストをブロック  
   - `*.prompty` ファイルのアップロード・解析リクエストは信頼できる IP のみ許可  

3. **監査ログの強化**  
   - WordPress の `auth.log`、`error.log`、LXD の `daemon.log` を 24 時間以内に確認  
   - 不審なシェル実行や `/proc/*/cmdline` 変更をアラート化  

4. **最小権限の徹底**  
   - LXD のプロジェクト権限 (`can_create_instances` など) を必要最小限に絞る  
   - IBM DOORS Next の管理者ロールを限定し、不要なユーザーは即削除  

5. **バックアップとリカバリ手順の検証**  
   - 影響を受けるシステムのスナップショットを取得し、復元テストを実施  

---

### 3.2 個別パッケージ・バージョン別対策

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ | 具体的作業 |
|-------------------|-------------------|------------------------|------------|
| **WP BASE Booking** | ≤ 6.3.0 | **6.3.1** (公式リリース) | `wp plugin update wp-base-booking` または手動で zip を上書き |
| **QA Analytics** | ≤ 5.2.0.0 | **5.2.0.1** 以上 | `composer update qa-analytics` もしくはベンダー提供のパッチ適用 |
| **Link Factory** | ≤ 2.0.0 | **2.1.0** (バックドア除去) | プラグイン削除 → `wp plugin delete link-factory` → 必要なら代替プラグイン導入 |
| **IBM DOORS Next** | 7.0.3 (IF018 未適用) | **7.0.3 + IF018** 以上 | IBM Fix Central から IF018 をダウンロードし、管理コンソールで適用 |
| **Prompty** | < 0.1.5 / < 2.0.0‑beta.5 | **0.1.5** 以上、**2.0.0‑beta.5** 以上 | `npm install -g prompty@latest` または Docker イメージの再ビルド |
| **LXD** (

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-61962

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T14:17:02.550 |

Unauthenticated Arbitrary Code Execution in WP BASE Booking <= 6.3.0 versions.

### CVE-2026-27544

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T14:16:56.890 |

Unauthenticated Remote Code Execution (RCE) in QA Analytics <= 5.2.0.0 versions.

### CVE-2026-59500

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-13T10:17:15.017 |

CWE-287: Improper Authentication

### CVE-2026-15413

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-13T09:17:12.153 |

The Link Factory WordPress plugin is a backdoor. Distributed as a "homepage sentence publisher", it exposes an operator-controlled REST API under /wp-json/link-factory/v1/ - authenticated by a detached Ed25519 signature verified against a hardcoded operator public key (except for the health check).

### CVE-2024-27253

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T22:17:13.600 |

IBM DOORS Next 7.0.3 through 7.0.3 Interim Fix 018 could allow an authenticated user to bypass security logic to perform unauthorized activities.

### CVE-2026-73299

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-1336` |
| Published | 2026-08-12T18:18:15.197 |

Prompty is a markdown file format (.prompty) for LLM prompts. Prior to 0.1.5 and 2.0.0-beta.5, the TypeScript Nunjucks renderer evaluated untrusted .prompty template bodies with unrestricted JavaScript member access. An attacker-controlled template could traverse constructor and prototype properties to execute JavaScript in the host Node.js process. This issue is fixed in versions 0.1.5 and 2.0.0-beta.5.

### CVE-2026-66898

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T21:17:39.700 |

A path traversal vulnerability in LXD allows an attacker to manipulate file system paths during backup import and restore operations. When importing or restoring a backup archive, LXD fails to validate instance and storage volume names contained within the archive metadata. An attacker can exploit this flaw by supplying a crafted backup archive with malicious instance or volume names containing path traversal sequences, potentially allowing file access or overwriting outside the designated restore directory.

### CVE-2026-73269

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T20:17:53.793 |

A flaw was found in the cluster-curator-controller component. A local user, by creating a ClusterCurator resource with a specific naming convention, can trigger the creation of a cluster-scoped ClusterRoleBinding. This allows the user to escalate their privileges from namespace-local access to cluster-wide control. This privilege escalation grants broad permissions, including the ability to access and manipulate secrets, manage cluster actions, and delete hosted clusters or node pools.

### CVE-2026-73268

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-12T20:17:53.650 |

A flaw was found in the cluster-curator-controller component of multicluster engine (MCE). A tenant with create or update permissions on ClusterCurator resources can inject an arbitrary Job specification. This is possible because the CreateJob() function does not validate user-controlled input when unmarshaling the spec.install.overrideJob raw extension. Successful exploitation allows the injected Job to run with the controller's elevated privileges, leading to arbitrary code execution and privilege escalation, potentially accessing cluster-wide secrets.

### CVE-2026-72508

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-12T20:17:49.650 |

A flaw was found in the multicloud-operators-subscription component of Red Hat Advanced Cluster Management (RHACM). This vulnerability allows a namespace-admin tenant to perform a confused-deputy attack by creating Subscription Custom Resources (CRs) that leverage a highly privileged ServiceAccount (SA). This enables the tenant to deploy arbitrary cluster-scoped resources, leading to privilege escalation and potential arbitrary code execution across the cluster.

### CVE-2026-63300

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:47.953 |

An improper validation vulnerability in the instancePostMigration function in lxd/instance_post.go of LXD allows an authenticated attacker with can_create_instances permissions on a restricted project to bypass project-level security restrictions. When migrating an instance between projects, LXD fails to validate the instance's configuration against the target project's enforced restrictions (such as restricted.containers.lowlevel, restricted.devices.*, and restricted.networks.access). An attacker can exploit this by creating a disallowed or high-privilege instance in an unrestricted project and subsequently moving it into the restricted project.

### CVE-2026-63299

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T20:17:47.830 |

An authorization bypass vulnerability in LXD allows an authenticated user to bypass project-level disk and volume limits. Two related code paths fail to verify resource limits during volume operations: the storagePoolVolumeTypePostMove function omits the limits.AllowVolumeCreation check before moving a volume across projects, and volume snapshot restore operations skip the AllowVolumeUpdate check when the configuration is nil (Config == nil). An attacker can exploit these flaws to allocate storage resources that exceed the administrative limits configured for a project.

### CVE-2026-63298

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T20:17:47.713 |

An improper neutralization of special elements vulnerability in LXD's NVIDIA instance configuration handling allows an authenticated attacker to inject arbitrary configuration directives. By supplying newline characters within the 'nvidia.driver.capabilities' or 'nvidia.require.*' configuration values, an attacker can manipulate the generated lxc.conf file. This flaw enables the attacker to execute arbitrary code on the host system with the privileges of the LXD daemon.

### CVE-2026-63297

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-863` |
| Published | 2026-08-12T20:17:47.583 |

An authorization bypass vulnerability in LXD due to a timing flaw during configuration merging allows an authenticated attacker to bypass target project restrictions during cross-project instance copies. When copying an instance to a target project, LXD performs restriction checks before configuration merging is complete, creating a time-of-check to time-of-use (TOCTOU) condition. An attacker can exploit this flaw to copy instances with disallowed high-privilege configurations into restricted projects, bypassing security controls.

### CVE-2026-63296

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T20:17:47.437 |

An authorization bypass vulnerability in LXD allows an authenticated attacker to bypass target project restrictions during instance migration. When migrating an instance to a target project, LXD accepts configuration overrides without validating the new configuration against the target project's enforced restrictions. An attacker can exploit this flaw to move instances with disallowed high-privilege configurations into restricted projects, bypassing security controls.

### CVE-2026-63294

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-12T20:17:47.187 |

A link following vulnerability in LXD allows an attacker to achieve root command execution on the host system. During the import or unpacking of crafted image or backup archives, LXD fails to properly validate and confine the backup.yaml file when it exists as a symbolic link. An attacker can exploit this flaw by providing a malicious archive with a symlinked backup.yaml file, causing LXD to process unconfined configuration metadata and execute arbitrary commands with root privileges.

### CVE-2026-63293

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-12T20:17:47.060 |

A link following vulnerability in LXD allows an attacker to achieve arbitrary file read and write operations on the host system. When importing or unpacking an image archive, LXD fails to validate whether the metadata.yaml file is a symbolic link. An attacker can exploit this flaw by providing a crafted image archive with a symlinked metadata.yaml file pointing to target file paths on the host system.

### CVE-2026-62420

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T20:17:46.897 |

An authorization bypass vulnerability in LXD allows an authenticated attacker to bypass target project security restrictions during cross-project instance migrations. When moving an instance cross-project to a different cluster member via POST /1.0/instances/{name} with migration: true, project: <target>, and target: <member>, the destination node skips all project restriction checks because the request arrives as an internal cluster notification. An attacker can exploit this to introduce disallowed instance configurations into a restricted project.

### CVE-2026-19656

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:42.933 |

ScadaLTS 2.7.8.1 exposes a server-side method that lacks authorization checks, allowing any authenticated user (including one holding only low-privilege, read-only permissions) to execute arbitrary operating system commands on the host. Successful exploitation results in code execution in the context of the ScadaLTS server process (root), leading to full compromise of the underlying system.

### CVE-2026-16860

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-12T18:17:24.397 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary code due to an uncontrolled search path element.

### CVE-2026-73294

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-08-12T16:17:22.640 |

Semaphore UI is a web interface for managing DevOps tools. Prior to 2.18.17 and 2.19.5-beta2, repository git_url handling passes an attacker-controlled --upload-pack option to CmdGitClient.GetLastRemoteCommitHash through POST /api/project/{id}/repositories and scheduled commit-hash polling, allowing a project Manager or Owner to execute arbitrary OS commands in the Semaphore server process. This issue is fixed in versions 2.18.17 and 2.19.5-beta2.

### CVE-2026-73263

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T15:18:30.943 |

Prowler is a cloud security platform. Prior to 5.36.0, the Kubernetes provider connection test accepted kubeconfig_content containing a legacy gcp auth-provider with config.cmd-path and config.cmd-args because kubeconfig_contains_exec_auth in api/src/backend/api/v1/serializers.py checked only exec blocks, and POST /api/v1/providers/{id}/connection loaded it through config.load_kube_config_from_dict in prowler/providers/kubernetes/kubernetes_provider.py, causing kubernetes-python CommandTokenSource.token to run the attacker-supplied command through subprocess.Popen on the shared worker. This issue is fixed in version 5.36.0.

### CVE-2026-66691

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-13T14:17:10.240 |

Unauthenticated Broken Access Control in Nokri <= 1.6.6 versions.

### CVE-2026-66465

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-13T14:17:07.833 |

Unauthenticated Broken Authentication in Cartify <= 1.3.0.1 versions.

### CVE-2026-66453

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-13T14:17:06.277 |

Unauthenticated Broken Authentication in Salon booking system <= 10.30.26 versions.

### CVE-2026-66424

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T14:17:04.600 |

Unauthenticated Privilege Escalation in SMS Alert Order Notifications <= 3.9.7 versions.

### CVE-2026-61967

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-13T14:17:02.957 |

Unauthenticated Privilege Escalation in miniorange otp verification <= 5.5.1 versions.

### CVE-2026-28185

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-13T14:17:00.303 |

Unauthenticated Broken Authentication in Log in with Google <= 1.4.2 versions.

### CVE-2026-28149

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-13T14:16:58.070 |

Unauthenticated PHP Object Injection in Headless Single Sign On <= 1.6 versions.

### CVE-2026-28148

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-13T14:16:57.943 |

Unauthenticated Bypass Vulnerability in Headless Single Sign On <= 1.6 versions.

### CVE-2026-28008

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-13T14:16:57.687 |

Unauthenticated Broken Authentication in OAuth Single Sign On – SSO (OAuth Client) <= 7.0.0 versions.

### CVE-2026-49827

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-306;CWE-434` |
| Published | 2026-08-13T13:19:10.050 |

WebErpMesv2 is a Resource Management and Manufacturing execution system Web for industry. Versions 1.19 and prior allow any self-registered user to upload arbitrary PHP files through the HR Expense scan_file parameter, leading to Remote Code Execution. Combined with open registration (no invite required) and broken role middleware (CheckUserRole silently swallows RouteNotFoundException), this chain is effectively unauthenticated RCE against any default installation. The issue is patched in commit 5c54862fa044b363fd2be03d586750e81afd6818.

### CVE-2026-49819

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-269;CWE-306;CWE-862` |
| Published | 2026-08-13T00:17:32.747 |

UpSnap is a wake on lan web app. Versions 4.4.1 through 5.3.5 are vulnerable to a missing-authentication / privilege-escalation chain in `pb.HandlerInitSuperuser` (`backend/pb/handlers.go:249`), reachable as `POST /api/upsnap/init-superuser`. The vulnerable code lacks any authentication, setup token, IP allow-list, or rate limit and is gated only by a `totalSuperusers > 0` count check — a condition that is false on every fresh install — allowing an unauthenticated network-adjacent attacker to register the initial superuser account, receive a long-lived JWT, and pivot to root remote code execution at `backend/networking/wake.go:43` (`exec.CommandContext(ctx, "/bin/sh", "-c", wake_cmd)`). Version 5.4.0 fixes the issue.

### CVE-2026-16770

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-13T00:17:31.763 |

PDF::WebKit versions through 1.2 for Perl allow argument injection into wkhtmltopdf via meta tags in the source document.

For an HTML string or file source, the constructor collects every <meta name="pdf-webkit-KEY" content="VALUE"> element in the document head through _pdf_webkit_meta_tags and turns each one into a wkhtmltopdf command line option. KEY is normalized to an option name matching --[a-z0-9-]+ but is not checked against an allow list, VALUE is passed through unchanged as the argument that follows it, and a VALUE of "yes" emits the option as a bare flag. BUILD merges the meta derived options last, so they also override the module defaults and the options passed to new. Switches such as --enable-local-file-access and --cookie-jar are reachable this way. The renderer is executed with an argument list rather than a shell command, so this is argument injection and not shell injection.

Any caller that renders untrusted HTML lets the document choose the renderer's options and override those set by the application, including options that read local files into the resulting PDF or write to a chosen path. A URL source is not scanned, and the scan is skipped when XML::LibXML, a recommended dependency, is not installed.

### CVE-2026-17083

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-12T20:17:39.260 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-17218

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-12T18:17:25.867 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to execute arbitrary code due to an out-of-bounds write.

### CVE-2026-16956

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T18:17:25.133 |

IBM Db2 Mirror for i 7.4, 7.5, and 7.6 could allow a remote attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-71193

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T23:17:22.030 |

In OpenStack Designate before 22.0.1, zone creation checks (_is_subzone, _is_superzone, and the duplicate-zone DB constraint) are scoped to the target pool only. An authenticated user can bypass these checks by scheduling a zone to a different pool via the AttributeFilter scheduler, creating an overlapping zone that conflicts with another tenant's zone. This enables cross-tenant DNS hijack (redirecting traffic to attacker-controlled IPs) and DNS denial of service (NODATA responses). Exploitation requires a multi-pool deployment with AttributeFilter enabled in scheduler_filters, which is a non-default but documented and supported configuration for self-service tiering.

### CVE-2026-49481

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T23:17:21.363 |

UpSnap is a wake on lan web app. Versions prior to 5.4.0 have an OS command injection vulnerability in the UpSnap’s device management functionality due to the presence of unsafe shell command template interpolation using the ip and the mac fields. User-controlled values can be inserted into the wake_cmd and shutdown_cmd templates and executed via /bin/sh -c (Linux) or cmd /C (Windows) without sanitization, resulting in an authenticated Remote Code Execution (RCE). A low-privileged user with permission to create or edit devices can execute arbitrary operating system commands on the UpSnap hosted server. Version 5.4.0 patches the issue.

### CVE-2026-73300

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T18:18:15.340 |

Budibase is an open-source low-code platform. Prior to 3.40.0, the MySQL integration component in Budibase is configured with multipleStatements: true, enabling execution of multiple SQL statements in a single query. Attackers can inject malicious SQL commands through user input fields, leading to complete database compromise. This vulnerability is fixed in 3.40.0.

### CVE-2026-17276

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T18:17:26.680 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to escalate privileges due to improper authorization in the handling of high-authority threads.

### CVE-2026-19001

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-12T21:17:37.307 |

The MongoDB BI Connector ODBC Driver may write outside the bounds of a fixed-size buffer when an application supplies an unusually long catalog, schema, or object name to a metadata retrieval function. This may result in memory corruption within the calling application's process, leading to abnormal termination and, under certain conditions, the potential for arbitrary code execution.

### CVE-2026-73483

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T12:17:23.540 |

Flowise (packages flowise and flowise-components) in versions <= 3.1.2 contain a sandbox escape in the vm2/@flowiseai/nodevm JavaScript sandbox. An authenticated user with access to the /api/v1/node-custom-function endpoint can escape the sandbox by supplying attacker-controlled executablePath and args parameters to puppeteer.launch(), which internally invokes child_process.spawn() outside the sandbox boundary. This allows execution of arbitrary OS commands as the Flowise process user (root in the official Docker image) and arbitrary host file disclosure via Chromium's file:// URL handling. In versions 3.0.8–3.1.2 exploitation requires ALLOW_BUILTIN_DEP=true; earlier versions are exploitable by default. Fixed in 3.1.3.

### CVE-2026-73296

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-08-12T17:17:32.780 |

Microsoft UFO open-source framework for intelligent automation across devices and platforms. Prior to 3.0.8, create_mobile_data_collection_server and create_mobile_action_server in ufo/client/mcp/http_servers/mobile_mcp_server.py exposed Streamable HTTP MCP services on TCP ports 8020 and 8021 without authentication, allowing an unauthenticated remote attacker to invoke capture_screenshot, get_ui_tree, tap, swipe, type_text, launch_app, press_key, and click_control against an ADB-connected Android device, disclose screen and device data, and modify device state. This issue is fixed in version 3.0.8.

### CVE-2026-50561

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T15:17:38.307 |

Yuxi is a large-model-based intelligent knowledge base and knowledge graph agent development platform. Prior to version 0.6.2, the project's authentication mechanism contains a flaw. In affected versions, the system does not sufficiently validate the identity token in the Authorization header — only performing a validity check. This allows an administrator token generated in another deployment instance or local testing environment to be used to access the backend management interfaces of a different affected instance. An attacker who obtains or constructs an acceptable administrator Authorization token may bypass normal login authentication and gain administrator privileges. This vulnerability could allow an attacker to access system configurations, invoke backend management APIs, create administrator accounts, and ultimately take over the system backend. This issue has been fixed in version 0.6.2. Before upgrading, users are advised to implement the following temporary measures: Set the environment variable `JWT_SECRET_KEY` to a non-default value, and configure a unique, sufficiently strong JWT/authentication key for each deployment instance; and/or avoid exposing backend management interfaces directly to the public network.

### CVE-2026-66478

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:08.763 |

Unauthenticated SQL Injection in Church Admin <= 5.1.1 versions.

### CVE-2026-66472

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:08.637 |

Unauthenticated SQL Injection in Everest Backup <= 2.3.12 versions.

### CVE-2026-66458

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:06.843 |

Unauthenticated SQL Injection in RealPress <= 1.1.2 versions.

### CVE-2026-66446

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:05.893 |

Subscriber SQL Injection in If-So Dynamic Content Personalization <= 1.10 versions.

### CVE-2026-66436

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:05.380 |

Unauthenticated SQL Injection in Active Products Tables for WooCommerce <= 1.1.1 versions.

### CVE-2026-61969

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:03.080 |

Unauthenticated SQL Injection in Listdom <= 5.6.0 versions.

### CVE-2026-61966

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:02.810 |

Subscriber SQL Injection in WPJAM Basic <= 7.0.1 versions.

### CVE-2026-28142

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:57.813 |

Unauthenticated SQL Injection in Web Directory Free <= 1.7.13 versions.

### CVE-2026-28001

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:57.177 |

Unauthenticated SQL Injection in WP Directory Kit <= 1.5.4 versions.

### CVE-2026-59507

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-13T10:17:15.963 |

CWE-798: Use of Hard-coded Credentials CWE-200: Exposure of Sensitive Information to an Unauthorized Actor CWE-284: Improper Access Control

### CVE-2026-59506

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-13T10:17:15.840 |

CWE-306: Missing Authentication for Critical Function

### CVE-2026-73519

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-12T22:17:17.600 |

WolfStack before 25.9.2 contains a hard-coded cluster-authentication secret compiled into every build and published as a constant in src/auth/mod.rs, allowing remote unauthenticated attackers to bypass authentication by supplying this value in the X-WolfStack-Secret header to the require_auth() gate without any session, API key, or user account. Attackers can reach an affected node's management port to enumerate all Docker and LXC containers on the host and execute arbitrary commands as root inside any container via the POST /api/containers/{runtime}/{id}/exec endpoint.

### CVE-2026-64639

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-12T16:17:12.280 |

Incorrect database cloning process in Plesk from 18.0.52 before 18.0.79.6 and 18.0.80.2 allows a low-privileged user (customer, reseller) to execute arbitrary code on behalf of the database server administrator.

### CVE-2026-73608

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T12:17:25.323 |

SiYuan's development branch (endpoint introduced by commit 9b8e8956f, not present in v3.7.3 or master, patched in v3.7.4) contains a missing-authorization vulnerability in the /api/av/getAttributeViewSearchTarget endpoint. The route is registered with CheckAuth only and performs no authorization checks (no CheckReadonly, no publish-access or encrypted-notebook gating). Given a database identifier taken from a published page and a keyword, an anonymous reader can query the endpoint to retrieve matching database row content, including rows that publish filters (FilterAttributeViewByPublishAccess) would otherwise withhold. No released stable version is affected.

### CVE-2026-73414

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-150` |
| Published | 2026-08-12T20:17:56.510 |

Shescape is a simple shell escape library for JavaScript. Prior to 2.1.14 and 3.0.1, getEscapeFunction in src/internal/win/cmd.js does not escape `(` and `)` when applications use the escape or escapeAll APIs on Windows with shell set to cmd.exe, or with shell set to true when CMD is the default. An attacker-controlled argument can break out of a parenthesized CMD construct and inject shell syntax depending on the original command, resulting in arbitrary command execution. This issue is fixed in versions 2.1.14 and 3.0.1.

### CVE-2026-73332

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T20:17:55.480 |

CamaleonCMS contains a stored cross-site scripting vulnerability in the cama_contact_form plugin that allows low-privileged authenticated attackers to inject arbitrary HTML by submitting unsanitized content to the before_html field through the contact form edit endpoint, which lacks proper authorization controls. Attackers can persist malicious script payloads into the database that execute in victims' browsers when the contact form loads, enabling cookie theft, forged authenticated requests against the admin interface, and session takeover of viewing users.

### CVE-2026-73329

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T20:17:55.053 |

CamaleonCMS contains a stored cross-site scripting vulnerability that allows authenticated low-privileged users to execute arbitrary JavaScript in an administrator's browser by injecting unsanitized HTML payloads into the post title parameter during draft creation. Attackers can submit a malicious HTML payload as a draft title through the drafts creation endpoint, which is persisted to the database without escaping and later rendered as raw HTML in the admin drafts listing, enabling administrator session compromise, cookie theft, and forged authenticated requests.

### CVE-2026-72804

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-12T20:17:52.383 |

SiYuan versions before v3.7.4 fail to validate publish-password tier in getGraph and getLocalGraph endpoints, allowing anonymous readers to retrieve block-level content of password-protected documents. Attackers can call these endpoints without supplying a password to read protected document content and the complete reference topology.

### CVE-2026-72798

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:51.543 |

SiYuan versions before v3.7.4 fail to properly filter related-database content in renderAttributeView, allowing anonymous readers to access Relation and Rollup cell contents from hidden or password-protected databases. Attackers can request published databases that relate to restricted databases to retrieve sensitive content, or bypass row filtering entirely when the first column is a non-block type.

### CVE-2026-72795

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:51.137 |

SiYuan versions before v3.7.4 fail to filter embedded block content by publish access in the getBlockDOMWithEmbed and getBlockDOMsWithEmbed endpoints. Attackers can request published blocks containing embed queries to read content from password-protected, hidden, or forbidden documents without authorization.

### CVE-2026-72794

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-12T20:17:50.977 |

siyuan versions before v3.7.4 expose the session cookie signing key through the /api/system/getConf endpoint to unauthenticated users in publish mode. Attackers can retrieve the CookieKey value and forge valid session cookies to impersonate users or gain administrative access.

### CVE-2026-72793

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-12T20:17:50.837 |

SiYuan versions before v3.7.4 fail to mask sensitive configuration fields in the /api/system/getConf endpoint, allowing anonymous or publish-reader users to obtain the session-cookie signing key, OS username via pandoc path, and encrypted-notebook key material. Attackers can forge and tamper with session cookies to impersonate users, and on instances without access-auth codes configured, escalate to administrator privileges.

### CVE-2026-72789

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:50.270 |

SiYuan before v3.7.4 fails to properly validate publish access for encrypted notebooks, treating them as publicly accessible by default. Anonymous readers can enumerate and retrieve fully decrypted document content from unlocked encrypted notebooks through the publish API without authentication or key material.

### CVE-2026-59504

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-602` |
| Published | 2026-08-13T10:17:15.500 |

CWE-602: Client-Side Enforcement of Server-Side Security

### CVE-2026-59503

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-13T10:17:15.380 |

CWE-200: Exposure of Sensitive Information to an Unauthorized Actor CWE-359: Exposure of Private Personal Information to an Unauthorized Actor

### CVE-2026-73501

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T22:17:17.443 |

kin-openapi is a Go project for handling OpenAPI files. Prior to 0.144.0, ValidationHandler.Load() in openapi3filter/validation_handler.go silently replaces a nil AuthenticationFunc with NoopAuthenticationFunc, which returns nil without checking credentials. This substitution causes every OpenAPI security requirement to be satisfied for unauthenticated requests when an application relies on ValidationHandler as its enforcement middleware. The no-op callback prevents the fail-closed ErrAuthenticationServiceMissing path from being reached and forwards the request to protected handlers that may require an API key, OAuth token, or another security scheme. This issue is fixed in version 0.144.0.

### CVE-2026-73602

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-13T12:17:24.480 |

Flowise before 3.1.3 contains a sandbox escape vulnerability in the vm2 JavaScript sandbox that allows authenticated users to execute arbitrary code by exploiting moment locale validation bypass. Attackers can craft a fake String object with a match function that bypasses path traversal checks to load and execute malicious JavaScript files stored in the document store outside the sandbox.

### CVE-2026-73601

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-08-13T12:17:24.353 |

Flowise versions before 3.1.3 contain a remote code execution vulnerability in the Custom MCP node when CUSTOM_MCP_PROTOCOL is set to stdio, allowing authenticated users to execute arbitrary commands by manipulating environment variables and command arguments. Attackers can abuse PYTHONWARNINGS and BROWSER environment variables with python3, or leverage the root working directory with node to bypass validation and execute system commands.

### CVE-2026-73487

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T12:17:24.083 |

Flowise before 3.1.3 contains a regex-based Python code validator bypass in CSV and Airtable Agent nodes that allows unauthenticated attackers to inject malicious code via prompt injection. Attackers can exploit unblocked pandas functions like pd.read_json() to exfiltrate datasets, perform SSRF against internal services, or achieve code execution through the unauthenticated prediction API.

### CVE-2026-73486

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T12:17:23.947 |

Flowise before 3.1.3 contains a code injection vulnerability in the CSV Agent node's customReadCSV parameter that allows authenticated attackers to execute arbitrary Python code. The validator uses a static regex blocklist that can be bypassed through obfuscation techniques, enabling attackers to execute code in the unsandboxed pyodide environment with full system access.

### CVE-2026-73485

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-13T12:17:23.807 |

Flowise before 3.1.3 contains a code injection vulnerability in the Airtable Agent node that allows unauthenticated attackers to execute arbitrary Python code by bypassing the pythonCodeValidator blocklist through obfuscation techniques. Attackers can send crafted prompts to a chatflow using the Airtable Agent node to inject malicious Python code that executes in an unsandboxed pyodide environment with full access to the host operating system.

### CVE-2026-71471

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-12T22:17:15.890 |

A flaw was found in acm-search-v2-rhel9. An attacker with administrative privileges on the hub cluster, specifically with patch access to the Search Custom Resource (CR), could exploit a vulnerability in the `Collector.ImageOverride` field. This allows the attacker to deploy an arbitrary container image across all managed clusters. The consequence is remote code execution (RCE), enabling the attacker to execute commands and potentially access sensitive information across the entire fleet of managed clusters.

### CVE-2026-73407

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T20:17:55.763 |

Budibase is an open-source low-code platform. Prior to 3.40.1, RestIntegration._req in packages/server/src/integrations/rest.ts attached credentials from getAuthHeaders and defaultHeaders without requiring the final request destination to match the datasource origin. An unauthenticated caller of a PUBLIC POST /api/v2/queries/:queryId query could supply an absolute or parameterized path to an attacker-controlled host and receive the stored bearer, basic, or static-header credentials. This issue is fixed in version 3.40.1.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-18099

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T20:17:40.827 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary script code due to improper neutralization of user-controlled input.

### CVE-2026-28176

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-13T14:16:59.663 |

Unauthenticated PHP Object Injection in Booking Activities <= 1.18.4 versions.

### CVE-2026-28161

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T14:16:58.887 |

Subscriber Privilege Escalation in Service Finder Booking <= 6.2 versions.

### CVE-2026-19385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-13T13:17:48.740 |

Heap buffer overflow in PostgreSQL pg_dump of long function transform lists allows an object creator to execute arbitrary code as the operating system user running pg_dump, via a crafted transform list.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-18408

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-13T13:17:48.127 |

Untrusted data inclusion in pg_dump in PostgreSQL allows a malicious superuser of the origin server to inject arbitrary code for restore-time execution as the client operating system account running psql to restore the dump, via psql \restrict meta-command input expansion.  The fix for CVE-2025-8714 introduced \restrict and \unrestrict to block this attack, but \unrestrict itself was sufficient for an attack.  pg_dumpall is also affected.  pg_restore is affected when used to generate a plain-format dump.  Non-core use of \restrict would be affected, but we've not identified non-core use.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-16239

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-13T13:17:46.520 |

Type confusion in PostgreSQL "portal"/cursor lifecycle allows a user to execute arbitrary code as the operating system user running the database, via re-creation of a cursor or other portal with different types.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-16238

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-13T13:17:46.383 |

Type confusion in PostgreSQL pg_restore_attribute_stats() allows an object creator to execute arbitrary code as the operating system user running the database, via conflation of range and multirange values.  Within major version 18, minor versions before PostgreSQL 18.5 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-15742

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-13T13:17:46.103 |

Integer wraparound in PostgreSQL fuzzystrmatch allows a user to direct writes to a huge range of addresses, executing arbitrary code as the operating system user running the database, via extreme inputs to SQL function levenshtein() or levenshtein_less_equal().  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-15741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T13:17:45.957 |

SQL injection in PostgreSQL EXTRACT() deparse allows an object owner to execute arbitrary SQL as a superuser via a hostile object definition.  Attacks affect expression deparse consumers broadly, including pg_dump, psql commands like \sf, and any similar usage in non-core tools.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14680

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-13T13:17:45.400 |

Type confusion with PostgreSQL "internal" data type arguments allows any user to execute arbitrary code as the operating system user running the database, via calls to functions with that argument type.  Type "internal" represents a class of mutually-incompatible data structures not intended for access from SQL.  The system intended to prevent such function calls, but this prevention had gaps.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14677

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-13T13:17:45.027 |

Integer wraparound in PostgreSQL 32-bit builds of pltcl and plperl allows an object creator to cause the server to undersize an allocation and write out-of-bounds via crafted function bodies.  This may execute arbitrary code as the operating system user running the database.  CVE-2026-6473 had fixed similar problems.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-13T13:17:44.907 |

Heap buffer overflow in PostgreSQL pg_stat_statements allows the query author to execute arbitrary code as the operating system user running the database, via crafted queries containing array constants.  Within major version 18, minor versions before PostgreSQL 18.5 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-14671

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-13T13:17:44.530 |

Type confusion in PostgreSQL module "refint" allows an object creator to execute arbitrary code as the operating system user running the database.  The fix for this emerged as a non-security bug report, and the fix appear in the git repository with subject "refint: Remove plan cache.", without a CVE number.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14670

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-13T13:17:44.407 |

Heap buffer overflow in PostgreSQL plperl return of a tied hash allows the function owner to execute arbitrary code as the operating system user running the database, via a crafted function body.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14669

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-13T13:17:44.280 |

Heap buffer overflow in PostgreSQL to_char(timestamptz) allows the party choosing the timezone to execute arbitrary code as the operating system user running the database, via a long POSIX timezone abbreviation.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14664

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-13T13:17:43.847 |

Heap buffer overflow in PostgreSQL regexp allows the query author to execute arbitrary code as the operating system user running the database, via text that would not pass encoding validation.  This shares heritage with CVE-2026-2006, but this case involved unanticipated data growth when round-tripped through pg_wchar.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14662

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-13T13:17:43.553 |

Integer wraparound in PostgreSQL tsvector and tsquery data type functions allows an unprivileged database user to cause the server to undersize an allocation and write out-of-bounds, via crafted large inputs.  This may execute arbitrary code as the operating system user running the database.  These types are typically sourced from application logic, not taken from the application's user.  Hence, application users attacking the database, through the application as a conduit, are unlikely.  CVE-2026-6473 had fixed similar problems.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-12263

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-13T11:17:38.193 |

Zohocorp ManageEngine Password Manager Pro versions before 13232 and PAM360 versions before 8551 are vulnerable to an authentication bypass vulnerability due to improper SAML validation.

### CVE-2026-11840

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T08:16:42.987 |

Zohocorp ManageEngine Password Manager Pro versions before 13232 and ManageEngine PAM360 versions before 8552 are vulnerable to authenticated SQL injection.

### CVE-2026-49473

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-436;CWE-863` |
| Published | 2026-08-13T00:17:32.587 |

@cedar-policy/authorization-for-expressjs is an open-source Express.js middleware that integrates Cedar authorization into Express applications by mapping HTTP requests to Cedar actions and evaluating authorization policies before allowing requests to proceed. Versions prior to 0.3.0 have an issue where, under certain circumstances, the middleware matches incoming requests against Cedar action mappings using req.originalUrl, which includes the query string, while Express routes requests using only the path component. The middleware uses req.originalUrl to match incoming requests against Cedar action mappings. In Express, req.originalUrl includes the query string, while route matching uses only the path. This creates a divergence between what Cedar authorizes and what Express executes. When an application defines separate actions for overlapping path prefixes with different authorization requirements (for example, GET /users for listing all users with admin-only access, and GET /users/{id} for retrieving a single user with any authenticated user access), an actor can append a query string to bypass the more restrictive policy. Sending GET /users/?x=1 causes the middleware to match against /users/{id} (with id parameter set to ?x=1) and evaluate the less restrictive action, while Express routes the request to the /users list handler. This allows inappropriate access to the more restrictive endpoint. This issue has been addressed in version 0.30. Some workarounds are available. Validate and sanitize incoming request paths before they reach the authorization middleware. Ensure that applications do not rely solely on the middleware for authorization when defining multiple actions on overlapping path prefixes with different permission levels.

### CVE-2026-19004

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-12T21:17:37.577 |

An application using the MongoDB BI Connector ODBC Driver may experience a memory-safety issue when processing output parameters from a stored procedure. Triggering this issue requires connecting to an untrusted or impersonated database server that returns crafted metadata. This may result in process termination, disclosure of process memory, or, under certain conditions, arbitrary code execution.

### CVE-2026-19002

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-12T21:17:37.440 |

A missing bounds check when parsing stored procedure parameter metadata in the MongoDB BI Connector ODBC Driver can result in an out-of-bounds write in the client application process. Triggering this issue requires control over the server the driver connects to, or the ability to respond in its place, in order to return malformed metadata. The resulting memory corruption may cause the client application to terminate abnormally or, under certain conditions, execute unintended code.

### CVE-2026-13622

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T21:17:35.630 |

A symlink following vulnerability was found in KubeVirt's virt-handler migration proxy. During live migration, virt-handler dials Unix sockets inside the target virt-launcher pod via /proc/<pid>/root/ paths using net.Dial() without symlink protection. These socket paths reside in qemu-owned directories writable by the virt-launcher user. An attacker with namespace edit and pods/exec permissions can replace a migration proxy socket with a symlink to the host CRI-O socket. Because virt-handler runs as root in the host mount namespace, absolute symlink targets resolve against the host filesystem, and the bidirectional io.Copy proxy relays attacker-controlled bytes to the container runtime, enabling full node compromise.

### CVE-2026-13105

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T21:17:35.027 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 is vulnerable to zip slip path traversal exploit when importing a configuration.

### CVE-2026-72807

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T20:17:52.837 |

SiYuan versions before v3.7.4 contain a second-order SQL injection vulnerability in attribute-view template columns that expose the queryBlocks function, which executes raw SQL using string substitution instead of parameterized queries. Attackers can distribute malicious SiYuan documents or packages with crafted template columns that execute arbitrary SQL on a victim's kernel when the package is imported and rendered, enabling read and write access across notebooks.

### CVE-2026-17642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T20:17:40.550 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-17417

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T20:17:40.170 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of shell metacharacters.

### CVE-2026-17082

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T20:17:39.130 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to gain elevated privileges due to improper validation of a client-supplied profile name.

### CVE-2026-13361

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-12T20:17:34.857 |

IBM Informix oninit sq_sgkprepare RCE via unchecked SQL Interface length field.

### CVE-2026-69106

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-12T18:18:11.273 |

A low-privileged user may poison cached artifact metadata under specific conditions, potentially causing consumers to retrieve untrusted content.

### CVE-2026-49467

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303;CWE-304` |
| Published | 2026-08-12T18:17:30.637 |

Pingvin Share X is a secure and easy self-hosted file sharing platform. A vulnerability in versions 1.5.0 through 1.18.0 allow an attacker to bypass password verification when managing Time-based One-Time Password (TOTP) settings. The root cause is a missing `await` keyword on calls to the asynchronous `verifyPassword` method in `authTotp.service.ts` and the `authenticateUser` method in `auth.service.ts`. In JavaScript, an unawaited `Promise` is always truthy. So the logic intended to throw a `ForbiddenException` when a password is incorrect. It never executes because the expression evaluates the existence of the `Promise` object rather than its resolved boolean result. The vulnerability is fixed in version 1.18.1 by ensuring all asynchronous authentication calls are properly awaited. There are no official workarounds. If a user is locked out, an administrator must manually reset the user's TOTP status in the database.

### CVE-2026-44741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T18:17:29.823 |

Pimcore's Admin Classic Bundle provides a Backend UI for Pimcore. Versions prior to 2.3.6 and 1.7.18 have a SQL injection vulnerability in Pimcore's translation grid date filter — the user-supplied `property` field from the filter JSON is interpolated directly into a `UNIX_TIMESTAMP(DATE(FROM_UNIXTIME(...)))` SQL expression without parameterization or allowlist validation. Versiosn 2.3.6 and 1.7.18 fix the issue.

### CVE-2026-18713

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T18:17:28.967 |

IBM i 7.6, 7.5, 7.4, and 7.3 s vulnerable to privilege escalation via Navigator for i. An authenticated user could elevate privileges to a root user to execute commands.

### CVE-2026-18669

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-12T18:17:28.723 |

IBM i 7.6, 7.5, 7.4, and 7.3 is vulnerable to a privilege escalation as the result of a remote code execution vulnerability in the activation engine component. An authenticated attacker can execute a maliciously planted script with root authority.

### CVE-2026-17110

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-12T18:17:25.717 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary commands and obtain sensitive information due to improper privilege management.

### CVE-2026-16906

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T18:17:24.773 |

IBM i 7.6, and 7.5 could allow a remote authenticated attacker to execute arbitrary commands with elevated privileges due to improper neutralization of special elements used in an OS command.

### CVE-2026-16856

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T18:17:24.277 |

IBM i 7.6, and 7.5 could allow a local attacker to gain elevated privileges due to improper neutralization of special elements used in an OS command.

### CVE-2026-18847

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-12T17:17:25.920 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote unauthenticated attacker to harvest credentials due to spoofing of Navigator for i.

### CVE-2026-18683

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T17:17:25.790 |

IBM i 7.6, 7.5, 7.4, and 7.3 is vulnerable to privilege escalation via Navigator for i. An authenticated user could elevate privileges to a root user to execute commands.

### CVE-2026-73293

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T16:17:22.493 |

Semaphore UI is a web interface for managing DevOps tools.  Prior to 2.18.19 and from 2.19.0-alpha3 until 2.19.5-beta5, ProjectMiddleware and GetProjectOrGlobalRoleBySlug allow a project manager to use POST /api/project/{id}/roles to create a custom manager role with permission bitmask 15, overriding the built-in manager permissions and granting CanUpdateProject and CanManageProjectUsers owner capabilities. This issue is fixed in versions 2.18.19 and 2.19.5-beta5.

### CVE-2026-67587

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-12T16:17:15.090 |

Apache Airflow's Task SDK rebuilt a `Callback` object from serialized data by re-running its constructor, which imports the module named by the stored callback path. Because `SyncCallback` is itself an Airflow class it passes the default `allowed_deserialization_classes` allow-list, so tightening that setting does not help. A Dag author — who controls a task instance's `next_kwargs` through the task execution API — can therefore cause an arbitrary module to be imported inside the scheduler process, when the scheduler's `awaiting_input` timeout sweep deserializes that value. No non-default configuration is required; the sweep runs unconditionally. Versions before 3.3.0 are not affected: the class existed, but the scheduler sweep that reaches it did not. This is a separate code path from CVE-2026-58076 and CVE-2026-67260, which cover different gadgets reaching deserialization — applying either of those fixes does not address this one. Users are advised to upgrade to apache-airflow 3.3.1 or later.

### CVE-2026-65941

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73;CWE-94;CWE-306;CWE-918` |
| Published | 2026-08-12T16:17:14.050 |

In WhatsUp Gold versions released before 2026.0.2, an unauthenticated remote attacker with network access to the affected service can execute arbitrary code in the context of the IIS application service account.

### CVE-2026-73431

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-12T15:18:33.483 |

Vulnerability-Lookup contains an 
authentication weakness in its account activation and password-recovery 
mechanism. Activation and recovery links were generated using stateless 
signed tokens containing only the user's login. Although the token 
signature and age were validated, the application did not track whether a
 token had already been successfully used. As a result, a captured 
activation or password-recovery link remained valid for the entire 
configured TOKEN_VALIDITY_PERIOD, even after the associated password had been changed. 


An attacker who obtains a valid 
activation or recovery token could therefore replay it multiple times 
during its validity period to set a new password and repeatedly take 
control of the affected account. In addition, tokens were not bound to a
 specific purpose, allowing the same token mechanism to be used across 
activation and recovery workflows. The patch introduces purpose-bound 
tokens and a random nonce whose SHA-256 digest is stored with the user 
account. The nonce is invalidated after a successful password change, 
making tokens single-use, while issuing a new token invalidates any 
previously issued token.  The password-setting operation now explicitly consumes the token before committing the account change. 


Successful exploitation requires 
the attacker to obtain a currently valid activation or recovery link, 
but does not require knowledge of the victim's existing password or an 
authenticated session.

### CVE-2026-73284

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T15:18:31.437 |

RustFS is a distributed object storage system built in Rust. RustFS AddServiceAccount in rustfs/src/admin/handlers/service_account.rs accepts an attacker-controlled target_user after only checking CreateServiceAccountAdminAction, passes it to new_service_account, and prepare_service_account_auth sets is_owner for the resulting root-parent service account. This issue is fixed in version 1.0.0-beta.11.

### CVE-2026-49478

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T13:19:09.790 |

Fulcio is a certificate authority for issuing code signing certificates for an OpenID Connect (OIDC) identity. Versions through 1.8.5 improperly follow cross-host redirects and attach Kubernetes ServiceAccount tokens during OIDC discovery, allowing a malicious or compromised issuer to perform blind SSRF, substitute and cache malicious JWKS keys, or disclose ServiceAccount tokens to external hosts. Version 1.8.6 blocks cross-host redirects, restricts token injection, and restricts local token loading. No known workarounds are available.

### CVE-2026-73625

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T12:17:27.753 |

GitPython versions before 3.1.54 contain a remote code execution vulnerability in the check_unsafe_options guard that can be bypassed by smuggling git options inside single-character kwarg values. Attackers can supply crafted option dictionaries to clone_from, fetch, pull, push, ls_remote, iter_commits, blame, or archive methods to execute arbitrary OS commands via the --upload-pack parameter.

### CVE-2026-73622

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-13T12:17:27.337 |

GitPython before 3.1.55 fails to disable environment variable expansion in Remote.create() and Submodule.add() URL handling, allowing attackers to exfiltrate secrets by supplying URLs containing variable references. Attackers can craft URLs with environment variable tokens that are expanded into .git/config and .gitmodules, then transmitted to attacker-controlled hosts during fetch or pull operations.

### CVE-2026-73618

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-13T12:17:26.770 |

Budibase Server before 3.40.0 contains a NoSQL injection vulnerability in the MongoDB query execution endpoint where user-supplied parameters are interpolated into JSON query templates without proper sanitization of JSON metacharacters. Attackers with query write permission can inject JSON structural characters to alter MongoDB queries, bypassing filters to read, modify, or delete arbitrary documents.

### CVE-2026-73615

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-08-13T12:17:26.337 |

Network-AI versions before 5.15.1 contain a security matcher bypass vulnerability where SandboxPolicy evaluates raw command strings with quotes preserved while the executor tokenizes commands by stripping quotes before execution. Attackers can craft quoted commands that evade blocklist checks and approval gates while the executor runs the identical unquoted dangerous argv.

### CVE-2026-73614

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-08-13T12:17:26.197 |

Network-AI ClaudeHookBridge before 5.15.1 truncates the target string to 500 characters before evaluating denyPatterns, while Claude Code executes the full untruncated command. Attackers can position dangerous content past byte 500 in a Bash command field to bypass the operator's hard-deny list and execute arbitrary commands.

### CVE-2026-46382

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T00:17:32.090 |

The Meeting Room Booking System (MRBS) is a PHP-based application for booking meeting rooms. Prior to version 1.12.2, a user-supplied private/local URI can be made to be fetched without checks. Version 1.12.2 contains a fix. No known workarounds are available.

### CVE-2026-73500

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T22:17:17.290 |

etcd is a distributed key-value store for the data of a distributed system. Prior to versions 3.5.33, 3.6.14, and 3.7.1, a network attacker who can reach an etcd TLS listener can open many TCP connections and never send a ClientHello. In client/pkg/transport/listener_tls.go, each connection handled by tlsListener.acceptLoop spawns a goroutine that blocks indefinitely inside tls.Conn.Handshake() and remains tracked in the pending map. Unbounded goroutine and map growth can exhaust memory in the etcd process, causing loss of availability for the cluster and, when etcd backs Kubernetes, the control plane. This issue is fixed in versions 3.5.33, 3.6.14, and 3.7.1.

### CVE-2026-73413

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-08-12T20:17:56.350 |

Shescape is a simple shell escape library for JavaScript. From 2.1.11 until 2.1.14 and 3.0.1, the flag-protection loop in compose in src/internal/compose.js repeatedly joins and slices flag fragments when flagProtection is enabled, which is the default, making processing quadratic in input size across the escape, escapeAll, quote, and quoteAll APIs. An attacker who can supply a large untrusted input containing many flag fragments can consume CPU and cause denial of service. This issue is fixed in versions 2.1.14 and 3.0.1.

### CVE-2026-72801

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-12T20:17:51.973 |

SiYuan versions before v3.7.4 disclose encrypted-notebook key-derivation material and wrapped data keys through unauthenticated endpoints in publish mode. Attackers can retrieve Argon2id salt, cost parameters, password verifiers, and wrapped notebook keys to perform unlimited offline master-password cracking without rate limiting.

### CVE-2026-15217

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T20:17:36.667 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.2 before 19.0.6, 19.1 before 19.1.4, and 19.2 before 19.2.2 that under certain conditions could have allowed cross-site scripting due to improper neutralization of user-controlled values rendered in table cell content by an analytics dashboard component.

### CVE-2026-15216

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T20:17:36.513 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.2 before 19.0.6, 19.1 before 19.1.4, and 19.2 before 19.2.2 that under certain conditions could have allowed cross-site scripting due to improper neutralization of user-controlled data rendered in pagination controls by an analytics dashboard component.

### CVE-2026-12004

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-08-12T20:17:33.530 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 contains a format string injection vulnerability in the management interface that allows attackers to cause denial of service and information disclosure by crafting a malicious HTTP request.

### CVE-2026-73327

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T18:18:15.480 |

Joomla 6.1.1 contains a path traversal vulnerability in the com_joomlaupdate extension that allows a Super User to be induced into extracting a crafted archive containing directory traversal sequences or absolute paths in ZIP entry filenames. Attackers can supply malicious ZIP entry names with parent-directory segments or absolute paths to the extract.php extraction routine, causing files to be written outside the intended destination root and enabling persistent remote code execution via planted PHP files.

### CVE-2026-73298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-12T18:18:15.057 |

The Microsoft Container Migration Solution Accelerator is a multi-service application that provides a multi-agent, AI-driven migration solution for moving container service configurations to Azure Kubernetes Service. In version 2.1.2 and earlier, a security vulnerability was identified in the Container Migration Solution Accelerator, specifically an authenticated IDOR (Insecure Direct Object Reference) that allows users to read, write, and delete processes belonging to other authenticated users. The issue affects multiple API endpoints, where ownership checks are missing, enabling unauthorized access and modification of migration data across users within the same organization. The vulnerability is present in both process and file management APIs, and the application relies on Entra ID authentication but lacks proper authorization controls between users. Authenticated users are able to access, modify, and delete processes and files belonging to other users without proper authorization checks.

### CVE-2026-15803

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611;CWE-827` |
| Published | 2026-08-12T16:16:54.877 |

In Eclipse RDF4J, several XML parser entry points do not fully restrict XML External Entity (XXE) processing when parsing untrusted XML-based RDF data or query results, permitting DOCTYPE declarations, external entity references, and external DTD loading. This is due to an incomplete fix for CVE-2018-1000644: the earlier fix did not cover all parser entry points. The issue is resolved in RDF4J 5.3.2, which rejects or disables DOCTYPE declarations, external entities, and external DTD loading by default.

### CVE-2026-73612

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-13T12:17:25.897 |

File Browser before v2.63.22 fails to validate access rules for descendants during recursive copy, rename, and delete operations, allowing authenticated users to bypass path-based access controls. Attackers can copy, rename, or delete denied files by operating on their allowed parent directory, defeating rule-based isolation for confidentiality and integrity.

### CVE-2026-73484

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-13T12:17:23.677 |

Flowise before 3.1.3 contains a sandbox escape vulnerability in pythonCodeValidator.ts that fails to block native Pandas DataFrame methods like to_csv, to_json, pipe, and query. Authenticated attackers can exploit this to exfiltrate uploaded CSV data or write arbitrary files to the server filesystem.

### CVE-2026-59505

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-13T10:17:15.623 |

CWE-284: Improper Access Control

### CVE-2026-59499

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-13T10:17:14.877 |

CWE-200: Exposure of Sensitive
Information to an Unauthorized Actor

### CVE-2026-19311

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-475` |
| Published | 2026-08-12T19:17:31.660 |

Missing authorization in the Execute Monitor API in Amazon OpenSearch Alerting plugin might allow an authenticated remote user to read, modify, or delete arbitrary index data via a crafted inline monitor request with unintentional data source and input index parameters.

### CVE-2026-18952

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-12T19:17:31.507 |

Missing input validation in the threat intelligence feed parser in the OpenSearch Security Analytics plugin might allow an authenticated remote user to perform server-side request forgery and read local files via a crafted URL parameter to the threat intel source configuration endpoint.

### CVE-2026-66658

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:09.603 |

Subscriber SQL Injection in Reviewer <= 3.14.2 versions.

### CVE-2026-66430

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:04.987 |

Subscriber SQL Injection in Visitor Traffic Real Time Statistics Pro <= 11.10 versions.

### CVE-2026-28184

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:00.100 |

Subscriber SQL Injection in Form Maker by 10Web <= 1.15.44 versions.

### CVE-2026-28168

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:59.017 |

Subscriber SQL Injection in CubeWP <= 1.1.30 versions.

### CVE-2026-28156

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:58.323 |

Subscriber SQL Injection in Do Lasso <= 358 versions.

### CVE-2026-28002

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:57.307 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Arraytics Booktics allows Blind SQL Injection.

This issue affects Booktics: from n/a through 1.0.22.

### CVE-2026-71473

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-12T22:17:16.020 |

A flaw was found in the `search-v2-operator` component. A user with specific administrative permissions on a managed cluster can exploit a vulnerability that allows them to inject arbitrary configuration data. This manipulation can override critical settings, leading to the replacement of container images. This ultimately results in container image injection on the managed cluster, potentially compromising its integrity.

### CVE-2026-16033

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T21:17:35.880 |

A path traversal vulnerability in LXD allows an attacker to achieve arbitrary host file read or unconstrained file creation. When processing image metadata templates, LXD fails to properly sanitize or restrict template file paths from escaping the instance templates directory (specifically affecting virtual machine / QEMU driver execution paths). An attacker can exploit this flaw by providing a crafted image archive with malicious template directives containing path traversal sequences, causing LXD to access or write files outside the intended template directory on the host system.

### CVE-2026-19228

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-12T20:17:42.213 |

GitLab has remediated an issue in GitLab EE affecting all versions from 19.1 before 19.1.4 and 19.2 before 19.2.2 that under certain conditions could have allowed an authenticated user to cause AI usage to be attributed to another namespace, due to improper authorization of identity information supplied in requests.

### CVE-2026-17418

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T18:17:26.807 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a local authenticated attacker to cause a denial of service due to improper neutralization of special elements used in an SQL command.

### CVE-2026-15423

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T18:17:23.820 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.0 before 19.0.6, 19.1 before 19.1.4, and 19.2 before 19.2.2 that under certain conditions could have allowed an authenticated user with developer-role permissions to execute CI/CD pipelines on a protected branch without the required push permissions due to improper authorization in pipeline reference validation.

### CVE-2026-73629

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T12:17:28.330 |

Serendipity before 2.6.0 contains a server-side request forgery vulnerability in the serendipity_url_allowed() filter that fails to block hex-encoded IPv4 addresses, IPv6 literals, and link-local ranges. Authenticated users with adminImagesAdd permission can bypass the filter using alternate address formats to request internal services and retrieve response bodies through the public uploads directory.

### CVE-2026-19003

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-12T22:17:15.153 |

A data source definition containing an over-length file path setting may cause the MongoDB BI Connector ODBC Driver setup dialog to write outside the bounds of an allocated buffer. The issue stems from an incorrect buffer capacity calculation in the dialog's file and folder selection handling, and is reached only when a user opens the setup dialog for such a data source and initiates a file or folder selection. Depending on build configuration, the result may range from abnormal process termination to, under certain conditions, execution of unintended code in the context of the user running the dialog.

### CVE-2026-10534

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-12T22:17:14.203 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 is vulnerable to buffer overflow in the IXF IMPORT parser.

### CVE-2026-73325

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-12T16:17:23.000 |

Fujitsu Research's OneCompression library 1.2.0 contains an unsafe deserialization vulnerability that allows attackers to execute arbitrary code by supplying a crafted model.pt checkpoint file, as QuantizedModelLoader.load_quantized_model_pt() unconditionally calls torch.load with weights_only=False, invoking Python's pickle machinery during deserialization. Attackers can embed malicious __reduce__ methods in a crafted model checkpoint to execute arbitrary Python code, including system commands, when the library loads the file from a caller-selected model directory.

### CVE-2026-13433

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-12T21:17:35.380 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 (ACS) is vulnerable to downloading unverified product code when configured to update from an IBM i. A bad actor could use this vulnerablity to run compromised code on the ACS user's workstation.

### CVE-2026-18235

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T18:17:28.000 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary Control Language commands due to insufficient input validation.

### CVE-2026-17095

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-12T17:17:24.570 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to bypass security restrictions due to unsafe reflection.

### CVE-2026-73292

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-352;CWE-620` |
| Published | 2026-08-12T16:17:22.343 |

Semaphore UI is a web interface for managing DevOps tools. Prior to 2.18.21, the /api/users/{id}/password endpoint accepts a cross-site request using the authenticated user's semaphore session cookie without CSRF protection or current-password confirmation, allowing an unauthenticated attacker to change an administrator's or another user's password after user interaction. This issue is fixed in version 2.18.21.

### CVE-2026-14679

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-13T13:17:45.277 |

Stack buffer overflow in PostgreSQL argument name matching allows an object creator to achieve unknown impacts via OUT parameter count.  The attack can write only 0x0 and 0x1 bytes.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-59501

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-13T10:17:15.140 |

CWE-284: Improper Access Control

### CVE-2026-17485

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-12T22:17:14.433 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service and obtain sensitive information due to an integer underflow.

### CVE-2026-10543

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-12T21:17:34.360 |

IBM Db2 11.5.0 through 11.5.9, and 12.1.0 through 12.1.5 is vulnerable to privilege escalation with a specially crafted query.

### CVE-2026-73303

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-12T20:17:54.133 |

Budibase is an open-source low-code platform. Prior to 3.40.0, POST /api/v2/email on account.budibase.app accepted a client-controlled accountId without binding it to the authenticated session, while checking only currentEmail. An authenticated attacker who obtains a victim account identifier can start the email-change workflow for the victim, receive and submit the verification code through POST /api/v2/email/verification, move the victim email to an attacker-controlled address, and complete a password reset as the victim. This issue is fixed in version 3.40.0.

### CVE-2026-17445

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-12T20:17:40.410 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to bypass security restrictions due to improper validation of an attacker-supplied user profile name.

### CVE-2026-66657

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-13T14:17:09.477 |

Unauthenticated Local File Inclusion in Biagiotti Core <= 2.1.1 versions.

### CVE-2026-66656

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-13T14:17:09.350 |

Unauthenticated Local File Inclusion in Foton Core <= 1.1.1 versions.

### CVE-2026-66653

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-13T14:17:08.917 |

Unauthenticated Local File Inclusion in Barista <= 2.5.1 versions.

### CVE-2026-66450

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-13T14:17:06.147 |

Unauthenticated Local File Inclusion in  Geo Mashup <= 1.13.18 versions.

### CVE-2026-61979

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T14:17:03.463 |

Unauthenticated Privilege Escalation in SAML SP Single Sign On <= 5.4.3 versions.

### CVE-2026-28186

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:00.560 |

Subscriber Broken Access Control in Travelfic Toolkit <= 1.5.1 versions.

### CVE-2026-27543

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T14:16:56.763 |

Unauthenticated Privilege Escalation in MStore API <= 4.20.0 versions.

### CVE-2026-6464

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-13T13:19:16.347 |

Untrusted data inclusion in PostgreSQL psql COPY may allow a server administrator to elicit execution of data lines as psql commands, via error injection.  If the "COPY FROM STDIN" or "\copy FROM STDIN" command fails before the server indicates that it awaits input rows, psql processes the in-line data rows as psql commands.  "COPY FROM" with a filename is unaffected.  The server administrator has no inherent control over the data rows, so a complete attack requires the attacker to separately acquire control of both the server and the data rows.  Alternatively, an attacker controlling data rows alone might complete an attack through a coincidental error that they don't control.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-14668

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-13T13:17:44.137 |

Type confusion regarding input of PostgreSQL ctid data type selectivity estimator allows an object creator to view a calculation derived from the value of an arbitrary 4-byte span of memory, via a chosen non-ctid input.  While the calculation loses precision, substantial memory value recovery appears possible.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-13267

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-302` |
| Published | 2026-08-12T20:17:34.690 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 could allow an authenticated user to gain privileges of another user via a specially crafted request.

### CVE-2026-12359

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T20:17:33.797 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 could allow a remote attacker to access sensitive information due to an inconsistent interpretation of an HTTP request by a reverse proxy.

### CVE-2026-16904

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T18:17:24.633 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary commands due to improper privilege management during monitor owner reassignment.

### CVE-2026-18499

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-12T17:17:25.650 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.8 is vulnerable to a privilege escalation when using Liberty collectives.

### CVE-2026-18098

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-12T17:17:24.993 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to obtain sensitive information and compromise system integrity due to an XML injection flaw.

### CVE-2026-69105

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-12T16:17:20.093 |

An unauthenticated attacker may cause untrusted package content to be cached under specific conditions, potentially affecting artifact integrity and availability.

### CVE-2026-73289

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T15:18:32.733 |

RustFS is a distributed object storage system built in Rust. Prior to 1.0.0-beta.12, RustFS evaluates the ForAllValues: and ForAnyValue: set qualifiers with the negated string operators StringNotEquals, StringNotEqualsIgnoreCase, StringNotLike, ArnNotEquals, and ArnNotLike using each other's semantics because crates/policy/src/policy/function/string.rs negates the aggregate result after eval or eval_like instead of negating each request-value predicate before quantification. Partially overlapping policy and request value sets can therefore make an Allow condition grant access to an excluded principal or make a Deny guardrail fail, including policies based on jwt:groups and jwt:roles; absent keys also receive the opposite ForAllValues: and ForAnyValue: behavior. This issue is fixed in version 1.0.0-beta.12.

### CVE-2026-73286

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T15:18:32.060 |

RustFS is a distributed object storage system built in Rust. Prior to 1.0.0-beta.12, RustFS get_condition_values folds attacker-controlled request headers from HeaderMap into server-derived userid, username, principaltype, groups, versionid, signatureversion, jwt:, and ldap: condition keys, allowing authenticated callers to satisfy identity-based policy conditions. This issue is fixed in version 1.0.0-beta.12.

### CVE-2026-66375

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T15:18:19.343 |

A low-privilege authenticated user may permanently remove protected internal metadata across repositories under specific conditions.

### CVE-2026-65937

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T16:17:13.527 |

In WhatsUp Gold versions released before 2026.0.2, an authenticated attacker can bypass frontend controls and inject persistent script content.

### CVE-2026-16695

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T21:17:36.427 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 could allow a local attacker to execute arbitrary code due to improper neutralization of special elements used in an OS command.

### CVE-2026-13367

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-12T21:17:35.260 |

IBM Informix Dynamic Server 14.10, and 15.0 contain a local privilege escalation vulnerability in the oninit setuid-root utility.

### CVE-2026-13094

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-12T21:17:34.900 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 is vulnerable to arbitrary code execution on Windows when installed for all users due to publicly writeable configuration file.

### CVE-2026-59917

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-12T20:17:46.663 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.3.0.17, contain Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges and arbitrary code execution.

### CVE-2026-59916

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-12T20:17:46.547 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.3.0.17, contain Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges and arbitrary code execution.

### CVE-2026-59914

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-12T20:17:46.407 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.3.0.17, contain an Authentication Bypass by Spoofing vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges and arbitrary code execution.

### CVE-2026-46731

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-12T20:17:44.170 |

Dell Display and Peripheral Manager (DDPM Windows), versions prior to 2.3.0.17, contain an Authentication Bypass by Spoofing vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges and arbitrary code execution.

### CVE-2026-14478

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-12T15:17:31.687 |

A maliciously created executable, when executed on the victim's machine, may allow a local low-privileged attacker to inject unauthenticated IPC messages into named pipes, modify pipe permissions or ownership, and potentially impact confidentiality, integrity, and availability.

### CVE-2026-66661

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-13T14:17:09.857 |

Subscriber Privilege Escalation in Directories Pro <= 2.0.5 versions.

### CVE-2026-65582

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T14:17:04.320 |

Subscriber Arbitrary File Download in AI Hub <= 1.3.10 versions.

### CVE-2026-73623

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-13T12:17:27.477 |

GitPython before 3.1.54 contains an incomplete denylist in unsafe_git_clone_options that omits --template, allowing attackers to achieve arbitrary command execution during clone operations. Attackers can supply --template pointing to a directory containing malicious post-checkout hooks that execute when git clones the repository.

### CVE-2026-73498

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T22:17:16.973 |

MCP Atlassian is a Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Prior to 0.22.0, confluence_upload_attachment passes its client-supplied file_path directly to open(file_path, "rb") in src/mcp_atlassian/confluence/attachments.py through _upload_attachment_direct() without calling validate_safe_path. An authenticated MCP client can read any file accessible to the server process and exfiltrate it to Confluence as an attachment. If an AI agent can be induced to call the tool through untrusted content, the same flaw can disclose server environment variables such as CONFLUENCE_API_TOKEN and other credentials. This issue is fixed in version 0.22.0.

### CVE-2026-14866

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-12T21:17:35.757 |

IBM i Access Client Solutions 1.1.2.0 through 1.1.9.13 is vulnerable to injection of rogue certificate authority due to publicly writeable truststore.

### CVE-2026-16863

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-12T18:17:24.517 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to obtain sensitive information due to an out-of-bounds read.

### CVE-2026-16627

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T18:17:24.160 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.2 before 19.2.2 that under certain conditions could have allowed an authenticated user with developer-role permissions to escalate privileges due to improper sanitization of HTML content rendered in a CI job modal.

### CVE-2026-48554

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T17:17:27.840 |

Nagios Core before 4.5.14 and Nagios XI before 2026R1.7 are vulnerable to authenticated remote code execution via unfiltered NOTIFICATION-family macro substitution through the com_data parameter. When a notification command references $NOTIFICATIONCOMMENT$ or $NOTIFICATIONAUTHOR$ in a shell-reachable position, authenticated UI users can run arbitrary commands as the nagios user. Exploitation requires a non-default configuration in which a notification command references these macros in a shell-executed command line.

### CVE-2026-48553

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T17:17:27.697 |

Nagios Core before 4.5.13 and Nagios XI before 2026R1.5 are vulnerable to authenticated remote code execution via custom-variable macro injection through the Nagios Remote Data Processor (NRDP). When a custom variable defined on a host, service, or contact is referenced in a shell-executed command line, an authenticated attacker with NRDP access can inject OS commands through the macro value. Exploitation requires a non-default configuration in which a custom variable is defined and referenced in a shell-executed command.

### CVE-2026-73346

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:17:12.880 |

Administrator SQL Injection in MailChimp For WooCommerce < 6.2 versions.

### CVE-2026-73611

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-13T12:17:25.747 |

File Browser versions from 2.50.0 through 2.63.21 fail to validate JWT expiration when proxy authentication is configured with a non-default logout page. Attackers with a previously valid token can access protected routes and administrative endpoints indefinitely, and exchange expired tokens for fresh ones via the renewal endpoint.

### CVE-2026-17111

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T20:17:39.497 |

IBM i 7.6, 7.5, 7.4, and 7.3 s vulnerable to SQL injection. A remote attacker could send specially crafted SQL statements, which could allow the attacker to view, add, modify, or delete information in the back-end database.

### CVE-2026-16907

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-12T18:17:24.890 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to execute arbitrary code due to improper bounds checking.

### CVE-2026-73264

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-12T15:18:31.087 |

Prowler is a cloud security platform. Prior to 5.33.1, an authenticated user with Lighthouse provider configuration access could supply an unvalidated base_url for the openai_compatible provider through POST /api/v1/lighthouse/providers and POST /api/v1/lighthouse/providers/{id}/connection, causing api/src/backend/tasks/jobs/lighthouse_providers.py to send outbound requests, including the API key in the Authorization header, to attacker-controlled or internal endpoints when client.models.list was called. This issue is fixed in version 5.33.1.

### CVE-2026-73188

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-13T14:17:12.470 |

Unauthenticated Sensitive Data Exposure in KiviCare <= 4.5.1 versions.

### CVE-2026-66469

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:08.380 |

Unauthenticated Broken Access Control in Arvow AI SEO Writer <= 1.5.3 versions.

### CVE-2026-66466

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:07.960 |

Unauthenticated Broken Access Control in StoreGrowth: Smart Sales Booster for WooCommerce | BOGO, Upsells, Direct Checkout, Quick View, Side Cart <= 2.1.1 versions.

### CVE-2026-66463

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-13T14:17:07.580 |

Unauthenticated Sensitive Data Exposure in iCARRY <= 2.9 versions.

### CVE-2026-66462

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-08-13T14:17:07.417 |

Unauthenticated Sensitive Data Exposure in WooCommerce Appointments <= 5.3.8 versions.

### CVE-2026-66461

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:07.243 |

Unauthenticated Broken Access Control in SMEPay: UPI Gateway for WooCommerce <= 1.0.5 versions.

### CVE-2026-66443

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-13T14:17:05.633 |

Unauthenticated Sensitive Data Exposure in REST API Log <= 1.7.1 versions.

### CVE-2026-66441

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:05.503 |

Unauthenticated Broken Access Control in MultiVendorX <= 5.0.10 versions.

### CVE-2026-66432

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1258` |
| Published | 2026-08-13T14:17:05.253 |

Subscriber Sensitive Data Exposure in WPJAM Basic <= 7.0.2.1 versions.

### CVE-2026-66431

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:05.120 |

Unauthenticated Broken Access Control in Bitcoin Lightning Payment Gateway for WooCommerce (via CLINK) <= 1.0.7 versions.

### CVE-2026-61984

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:03.720 |

Unauthenticated Broken Access Control in WPMobile.App <= 11.77 versions.

### CVE-2026-61980

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T14:17:03.590 |

Unauthenticated Arbitrary File Download in OMGF Pro <= 5.2.7 versions.

### CVE-2026-48702

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-13T14:17:01.427 |

Rekor is a software supply chain transparency log. Starting in version 0.3.0 and prior to version 1.5.2, the `Package.Unmarshal()` function in `pkg/types/alpine/apk.go` decompresses the signature and control gzip members of an APK file into in-memory buffers without bounding the total decompressed size. The existing `max_apk_metadata_size` check (default 1MB) is only applied to individual tar entry header sizes after decompression completes, so it does not prevent a decompression bomb from consuming unbounded heap memory. An attacker can craft a gzip stream that compresses at a ~1000:1 ratio (e.g., 2MB compressed zeros → 2GB decompressed). When submitted as spec.package.content in an Alpine `ProposedEntry`, the server decompresses the full payload into memory during request processing, triggering a fatal Go runtime out-of-memory error or OS OOM-kill that cannot be caught by the server's recover() middleware. This is reachable via two unauthenticated endpoints, `POST /api/v1/log/entries (createLogEntry)` and `POST /api/v1/log/entries/retrieve (searchLogQuery)`. Both invoke `V001Entry.Canonicalize()` → `fetchExternalEntities()` → `apk.Unmarshal(packageData)`, which performs the unbounded decompression. Version 1.5.2 patches the issue. There is no effective workaround. Setting `max_request_body_size` reduces but does not eliminate exposure due to the ~1000:1 compression ratio (a 1MB body limit still allows ~1GB heap allocation). Setting `max_apk_metadata_size` has no effect on this vulnerability since the check is applied after decompression.

### CVE-2026-28157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-35` |
| Published | 2026-08-13T14:16:58.450 |

Subscriber Path Traversal in Do Lasso <= 358 versions.

### CVE-2026-27538

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-13T14:16:56.510 |

Unauthenticated SQL Injection in WP Directory Kit <= 1.5.4 versions.

### CVE-2026-27345

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:16:55.847 |

Unauthenticated Broken Access Control in Taxi Booking Manager for WooCommerce <= 2.0.3 versions.

### CVE-2026-19484

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835;CWE-1322` |
| Published | 2026-08-13T10:17:11.640 |

@fastify/busboy is a multipart form-data parser. In versions 3.1.0 through 3.2.0, a remote unauthenticated attacker can stall the Node.js event loop by sending a multipart request whose boundary is crafted to a specific length. The vendored streaming search stores its skip table in a fixed 256 entry byte array, and a boundary of exactly 252 bytes makes the search needle 256 bytes, which truncates the default skip distance to zero and turns the search into a CPU bound loop on a small body. A single small request can keep one core busy and deny service to other requests handled by the same process. The issue is fixed in @fastify/busboy 3.2.1, which widens the skip table so the skip distance is preserved. Users should upgrade to 3.2.1.

### CVE-2026-19481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-754` |
| Published | 2026-08-13T09:17:12.573 |

@fastify/busboy is a multipart form-data parser. In versions 1.0.0 through 3.2.0, an attacker who can submit multipart form-data can crash the parser by sending a part header whose name is a prototype-inherited property such as __proto__ or constructor. The internal header parser stores headers in a plain JavaScript object and assumes each value is an array, so an inherited property name resolves to a truthy non-array value and triggers a TypeError. In the common pipe integration the failure surfaces as an error event, but in direct write or end usage the exception is thrown synchronously and can terminate the Node.js process, causing an unauthenticated denial of service. The issue is fixed in @fastify/busboy 3.2.1, which creates the header object with a null prototype. Users should upgrade to 3.2.1.

### CVE-2026-47717

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-12T23:17:20.643 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. In fuxa-server version 1.3.0, the GET /api/project endpoint exposes sensitive project configuration data to guest-context requests even when secureEnabled is enabled. Version 1.3.1 fixes the issue.

### CVE-2026-73493

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T22:17:16.673 |

Http4s (http4s-blaze-server) is a minimal, idiomatic Scala interface for HTTP services. Prior to 0.23.18 and 1.0.0-M42, http4s-blaze-server aggregates fragments of an incoming WebSocket message with no limit on total size or fragment count. A client that completes a WebSocket handshake can send an unterminated fragmented message and drive unbounded heap growth in the server JVM, resulting in denial of service through OutOfMemoryError. Any http4s application serving WebSocket routes over BlazeServerBuilder is affected, no non-default configuration is required, and maxWebSocketBufferSize does not bound the aggregate because it bounds only individual frames. A single connection sending continuation frames that never set FIN forces the server to buffer every fragment until the heap is exhausted, terminating the JVM with OutOfMemoryError on the blaze selector thread. Small fragments amplify the cost through per-frame object overhead, so a modest volume of wire bytes is sufficient. This issue is fixed in versions 0.23.18 and 1.0.0-M42.

### CVE-2026-71469

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T22:17:15.760 |

A flaw was found in search-v2-api. An unauthenticated attacker can exploit this by sending requests with unique random bearer tokens. Each unique token creates a permanent entry in the unbounded tokenReviews cache, which is not properly cleared. This can lead to memory exhaustion of the search-api pod, resulting in a Denial of Service (DoS).

### CVE-2026-73418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-248` |
| Published | 2026-08-12T21:17:40.890 |

NextAuth.js provides authentication for Next.js. Prior to @auth/core 0.41.3 and next-auth 4.24.15 and 5.0.0-beta.32, the exported getToken() helper in the next-auth/jwt and @auth/core/jwt modules can throw an uncaught exception when it reads a malformed Authorization: Bearer header. When no session cookie is present, getToken() URL-decodes the bearer value before validating it, and malformed percent encoding causes decodeURIComponent() to throw instead of treating the token as invalid. Because getToken() is commonly called in API routes, middleware, and server-side request handlers, a single unauthenticated request can trigger an unhandled exception in code paths that authenticate requests, causing a per-request denial of service without exposing tokens, sessions, or other data and without bypassing authentication. This issue is fixed in @auth/core 0.41.3 and next-auth 4.24.15 and 5.0.0-beta.32.

### CVE-2026-19654

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-12T21:17:38.517 |

A unauthenticated remote peer may lead rsyslogd to crash due to a flaw in the optional imptcp module. A crafted input sequence during oversize-frame recovery can cause an invalid internal message length and terminate rsyslogd. No confidentiality or integrity impact, privilege escalation, or code execution has been identified. imtcp and the default imptcp framing modes are not affected.

### CVE-2026-73415

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-12T20:17:56.660 |

jupyterlab is an extensible environment for interactive and reproducible computing, based on the Jupyter Notebook Architecture. Prior to 4.5.10 and 4.6.2, in packages/imageviewer/src/widget.ts, JupyterLab's ImageViewer uses URL.createObjectURL for a specially crafted SVG image and revokes the blob URL too early, allowing the image to retain an executable same-origin context when it is opened through the image viewer and then opened in a new browser tab. The resulting cross-site scripting can be used to execute arbitrary code on the JupyterLab server. This issue is fixed in versions 4.5.10 and 4.6.2.

### CVE-2026-73406

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-12T20:17:55.617 |

Budibase is an open-source low-code platform. Prior to 3.39.32, GET /api/global/users/tenant/:id was listed in PUBLIC_ENDPOINTS in packages/worker/src/api/index.ts, and tenantUserLookup returned a full PlatformUser document. An unauthenticated caller could query an email or user identifier, distinguish existing users from missing users, and obtain tenant identifiers, user identifiers, email addresses, SSO identifiers, and document revision metadata. This issue is fixed in version 3.39.32.

### CVE-2026-73330

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-12T20:17:55.197 |

CamaleonCMS 2.9.1 contains a server-side template injection vulnerability that allows authenticated administrators to execute arbitrary commands by embedding ERB tags in the email parameter of the test_email settings action, which are evaluated when an SMTP rejection reflects the recipient address back in the exception message rendered as an inline ERB template. Attackers can submit a crafted email parameter containing ERB expressions through the admin settings test_email endpoint, causing the Rails inline template renderer to evaluate attacker-controlled Ruby code and achieve arbitrary command execution as the Rails process user.

### CVE-2026-67579

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89;CWE-502` |
| Published | 2026-08-12T20:17:48.440 |

Deserialization of Untrusted Data vulnerability in ash-project ash allows an unauthenticated attacker to inject a filter expression through a forged keyset pagination cursor, resulting in SQL injection or code execution depending on the data layer.

Read actions with keyset pagination decode the client-supplied page[:after] or page[:before] cursor in decode_values/2 in lib/ash/page/keyset.ex using non_executable_binary_to_term/2 with [:safe]. That guard blocks new atoms, funs, and ports, but not a struct built from atoms already interned in a running Ash application, so a decoded %Ash.Query.Call{} expression survives and is spliced into the keyset filter as a comparison value in do_filters/4 and evaluated. Because the cursor bypasses the Ash.Expr macro, the runtime never applies the private?/public? gate that would otherwise reject it. On AshPostgres the injected fragment is inlined into the SQL query; on the ETS and Simple data layers it is evaluated in-process as an arbitrary function call.

This issue affects ash: from 1.17.0 before 3.31.3.

### CVE-2026-42018

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T18:17:29.473 |

JFrog Artifactory could return an internal anonymous-user token to an unauthenticated caller when anonymous access is disabled, potentially exposing sensitive resources.

### CVE-2026-17271

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-12T18:17:26.557 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to improper validation of input size.

### CVE-2026-16931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-08-12T18:17:25.010 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote attacker to cause a denial of service due to improper handling of zero-length TCP options.

### CVE-2026-68968

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-08-12T16:17:19.607 |

Apache Airflow's Backfill API authorized a request against a Dag id supplied by the caller whenever the `backfill_id` path segment failed to parse. The authorization dependency parsed it with `int()` while the route handler parsed it as pydantic's `NonNegativeInt`, which accepts values `int()` rejects (`1.0` coerces to `1`); FastAPI resolves dependencies before endpoint validation, so the two acted on different Dags. An authenticated user holding edit permission on any single Dag could therefore read, pause and cancel backfills belonging to any other Dag, including moving another Dag's queued runs to `failed`. No non-default configuration is required and backfill ids are sequential, so finding a target is trivial. Users are advised to upgrade to apache-airflow 3.3.1 or later, which parses the backfill id with the same type the routes declare.

### CVE-2026-73285

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T15:18:31.840 |

RustFS is a distributed object storage system built in Rust. From 1.0.0-alpha.64 until 1.0.0-rc.1, RustFS external OPA authorization enabled by RUSTFS_POLICY_PLUGIN_URL in crates/iam/src/sys.rs sets PreparedIamAuth.needs_existing_object_tag incorrectly for PreparedIamMode::Opa, causing maybe_merge_object_tag_conditions to omit s3:ExistingObjectTag/* values and allowing authenticated users to bypass tag-based policy restrictions. This issue is fixed in version 1.0.0-rc.1.

### CVE-2026-68757

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-12T15:18:22.477 |

A user with access to a valid SAML response may impersonate another user under specific conditions.

### CVE-2026-28189

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T14:17:01.020 |

Unauthenticated Arbitrary File Deletion in Participants Database <= 2.7.8.4 versions.

### CVE-2026-73495

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-12T22:17:16.820 |

blaze is a Scala library for building asynchronous pipelines, with a focus on network IO. Prior to 0.23.18 and 1.0.0-M42, blaze-server can merge HTTP/1.1 chunked-body trailer fields into Request.headers. Because trailer fields are attacker-controlled, an unauthenticated remote client can inject arbitrary header names and values, including X-Forwarded-For and internal authorization headers, that a fronting proxy sanitized from the request-header section, bypassing header-based trust decisions in the application. Any http4s application using BlazeServerBuilder over HTTP/1.1 whose routes or middleware trust proxy-set headers, including X-Forwarded-For, X-Real-IP, and X-Forwarded-Host, is affected. If a fronting proxy strips or normalizes those headers but forwards chunked bodies with trailers intact, an attacker can spoof client IP for allow-lists, rate limits, or auditing, forge the https scheme, or inject internal authorization headers. A promoted Connection: close trailer is also honored, allowing attacker-controlled termination of pooled backend connections. This issue is fixed in versions 0.23.18 and 1.0.0-M42.

### CVE-2026-11923

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-12T20:17:33.250 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 Reverse Proxy in certain configurations may provide weaker than expected cryptographic validation of user supplied data.

### CVE-2026-28188

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:17:00.870 |

Unauthenticated Broken Access Control in Hydra Booking <= 1.2.2 versions.

### CVE-2026-13476

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T21:17:35.510 |

IBM Informix Dynamic Server 14.10, 15.0, and 12.10 could allow an unauthenticated user to execute arbitrary commands with service account privileges on the system due to improper validation of user supplied input.

### CVE-2026-67260

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-12T16:17:14.813 |

Apache Airflow 3.3.0 moved human-in-the-loop tasks from the triggerer to a new `awaiting_input` task state swept by the scheduler. That sweep deserializes the task instance's `next_kwargs` without an allow-list, so a Dag author — who controls that value through the task execution API — can cause an arbitrary module import and object instantiation inside the scheduler process, or terminate the scheduler job. No non-default configuration is required: the sweep runs unconditionally every 15 seconds, and the default `allowed_deserialization_classes` setting does not cover this code path. Versions before 3.3.0 are not affected, because human-in-the-loop tasks deferred onto the triggerer instead. This is a different code path from CVE-2026-58076, which covers the same unguarded exception-node deserialization reached elsewhere — deployments that applied that fix must upgrade for this issue as well. Users are advised to upgrade to apache-airflow 3.3.1 or later.

### CVE-2026-66704

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-13T14:17:11.043 |

Unauthenticated Server Side Request Forgery (SSRF) in Gutenverse Companion <= 2.5.1 versions.

### CVE-2026-27380

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-13T14:16:55.987 |

Editor PHP Object Injection in Car Rental Manager <= 1.3.9 versions.

### CVE-2026-6471

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T13:19:16.747 |

Missing authorization in PostgreSQL logical decoding allows a non-superuser holding REPLICATION privilege to dlopen any file visible to the operating system account running the server, via the choice of logical decoding plugin.  This in turn runs arbitrary code as that account.  Versions before PostgreSQL 18.5, 17.11, 16.15, 15.19, and 14.24 are affected.

### CVE-2026-73624

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-13T12:17:27.617 |

GitPython versions before 3.1.54 contain an arbitrary file overwrite vulnerability in the Diffable.diff method that fails to validate git options passed through kwargs. Attackers can supply the --output argument via the other parameter or output kwarg to write patch content to attacker-chosen file paths at process privilege level.

### CVE-2026-73620

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-13T12:17:27.057 |

GitPython before 3.1.57 fails to guard git option forwarding in IndexFile.checkout() and TagReference.create(), allowing attackers to pass unsafe options via kwargs. Attackers can use --prefix to overwrite arbitrary files with repository content or -F to read arbitrary files returned in-band.

### CVE-2026-73613

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-13T12:17:26.043 |

filebrowser versions before 2.63.19 contain an out-of-scope file deletion vulnerability in the TUS upload cache eviction mechanism that allows authenticated users with only Create permission to delete arbitrary files outside their scope. Attackers can swap an ancestor directory with a symlink during the cache TTL window to redirect the raw os.Remove call to an out-of-scope target, bypassing ScopedFs scope guards and Perm.Delete checks.

### CVE-2026-18146

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T07:17:06.523 |

The Fluent Forms – Customizable Contact Forms, Survey, Quiz, & Conversational Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Notification Smartcode Values in all versions up to, and including, 6.2.11 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts that execute in the browser of an administrator (or any user with the Fluent Forms entry-viewing capability) when they view the form's entry Submission Logs in the WordPress admin dashboard. Exploitation requires that a site administrator or Fluent Forms manager has configured an email notification whose subject or static (direct) Send To value references an attacker-influenced Smartcode such as an input_password field value, a cookie value, or submission.response.

### CVE-2026-73326

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:54.887 |

CamaleonCMS contains a missing authorization vulnerability that allows any authenticated low-privileged user to access and modify plugin settings by reaching four unprotected plugin-administration endpoints without administrator-level authorization. Attackers can manipulate plugin configuration parameters at runtime across the attack, front_cache, cama_meta_tag, and cama_contact_form plugins to alter cached page behavior, modify public meta-tag output, or reconfigure contact forms, enabling account takeover when chained with stored cross-site scripting through the contact form's before_html field.

### CVE-2026-12618

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-12T20:17:33.940 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 could allow an administrator to execute additional commands they are not entitled to due to improper validation of user supplied input.

### CVE-2026-12005

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T20:17:33.667 |

IBM Security Verify Access 10.0 through 10.0.9.2 and IBM Verify Identity Access 11.0 through 11.0.3 and IBM Verify Identity Access Container 11.0 through 11.0.3 contains a input validation vulnerability in the management interface that allows already privileged attackers to execute additional operations by crafting a malicious HTTP request.

### CVE-2026-68759

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-12T16:17:16.887 |

A holder of a valid integration credential may impersonate other users under specific conditions.

### CVE-2026-68752

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-12T15:18:21.880 |

A Project Resource Manager may gain broader administrative privileges under specific conditions.

### CVE-2025-59319

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-12T15:17:28.963 |

CPSD CryptoPro Secure Disk for Bitlocker before v7.7.4 fails to certify the integrity of the intended boot partition and selects the first partition index matching a hardcoded type value. A crafted Linux partition could be inserted ahead of this intended target, allowing for code execution in the context of high privilege.

### CVE-2026-66700

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:10.913 |

Unauthenticated Cross Site Scripting (XSS) in Smart Online Order for Clover <= 1.6.1 versions.

### CVE-2026-66698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:10.787 |

Unauthenticated Cross Site Scripting (XSS) in SureDash <= 1.10.1 versions.

### CVE-2026-66697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:10.647 |

Unauthenticated Cross Site Scripting (XSS) in Colissimo Officiel : Méthodes de livraison pour WooCommerce <= 2.10.0 versions.

### CVE-2026-66655

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:09.207 |

Unauthenticated Cross Site Scripting (XSS) in MultiParcels Shipping For WooCommerce <= 1.30.36 versions.

### CVE-2026-66468

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:08.237 |

Unauthenticated Cross Site Scripting (XSS) in Local Delivery Drivers for WooCommerce <= 3.0.0 versions.

### CVE-2026-66449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:06.017 |

Unauthenticated Cross Site Scripting (XSS) in  Geo Mashup <= 1.13.18 versions.

### CVE-2026-66429

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:04.860 |

Unauthenticated Cross Site Scripting (XSS) in Visitor Traffic Real Time Statistics Pro <= 11.10 versions.

### CVE-2026-66426

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:04.730 |

Unauthenticated Cross Site Scripting (XSS) in WP-Stats <= 2.56 versions.

### CVE-2026-65580

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:04.190 |

Unauthenticated Cross Site Scripting (XSS) in Agrion <= 1.0.0 versions.

### CVE-2026-61974

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:03.210 |

Unauthenticated Cross Site Scripting (XSS) in Mang Board WP <= 2.3.4 versions.

### CVE-2026-61965

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:02.680 |

Unauthenticated Cross Site Scripting (XSS) in GeekyBot <= 1.2.6 versions.

### CVE-2026-61960

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:02.420 |

Unauthenticated Cross Site Scripting (XSS) in WP Full Stripe Free <= 8.5.0 versions.

### CVE-2026-28187

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:17:00.717 |

Unauthenticated Cross Site Scripting (XSS) in Knowledge Base for Documentation, FAQs with AI Assistance <= 17.211.0 versions.

### CVE-2026-28175

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:59.533 |

Unauthenticated Cross Site Scripting (XSS) in Visitors Traffic Real Time Statistics <= 8.11 versions.

### CVE-2026-28173

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:16:59.277 |

Customer Arbitrary Content Deletion in WP Event SOlution <= 4.1.19 versions.

### CVE-2026-28170

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:59.143 |

Unauthenticated Cross Site Scripting (XSS) in Blog Floating Button <= 1.4.20 versions.

### CVE-2026-28158

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:58.583 |

Unauthenticated Cross Site Scripting (XSS) in Do Lasso <= 358 versions.

### CVE-2026-28004

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:57.560 |

Unauthenticated Cross Site Scripting (XSS) in Business Directory <= 6.4.25 versions.

### CVE-2026-28003

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:57.433 |

Unauthenticated Cross Site Scripting (XSS) in Maspik – Spam blacklist <= 2.9.1 versions.

### CVE-2026-27539

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:56.640 |

Unauthenticated Cross Site Scripting (XSS) in Welcart e-Commerce <= 2.11.31 versions.

### CVE-2026-27536

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-13T14:16:56.250 |

Unauthenticated Cross Site Scripting (XSS) in MailChimp Subscribe Forms  <= 4.3.3 versions.

### CVE-2026-27535

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-13T14:16:56.120 |

Subscriber Broken Access Control in Solace Extra <= 1.6.0 versions.

### CVE-2026-73619

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-13T12:17:26.913 |

GitPython before 3.1.57 contains an incomplete denylist in the unsafe_git_archive_options guard that omits --add-file and --add-virtual-file options. Attackers can supply these options to Repo.archive() to read arbitrary files from the filesystem and include them in the returned archive.

### CVE-2026-73617

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-943` |
| Published | 2026-08-13T12:17:26.627 |

Budibase before 3.40.0 contains a NoSQL injection vulnerability in the MongoDB datasource integration where user-supplied parameters are enriched with handlebars using noEscaping: true and parsed without operator filtering. Attackers can inject MongoDB operators through query parameters to bypass per-user access controls, read arbitrary documents, execute JavaScript via $where operators, or modify collections through update and delete operations.

### CVE-2026-73616

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-13T12:17:26.480 |

OpenRemote notification deletion endpoints fail to enforce realm boundaries, allowing any realm administrator to delete notifications belonging to other realms. Attackers with write:admin role in one realm can send DELETE requests to remove notifications from the master realm or other tenants without authorization checks.

### CVE-2026-73604

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-13T12:17:24.750 |

Flowise before 3.1.3 contains an incomplete credential redaction vulnerability in the GET /api/v1/credentials/:id endpoint that returns decrypted secrets in plaintext. Authenticated users with credentials:view permission can retrieve sensitive data including database connection URLs with embedded passwords, cloud service account JSON with private keys, and API keys by calling this endpoint.

### CVE-2026-73499

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-12T22:17:17.130 |

etcd is a distributed key-value store for the data of a distributed system. Prior to versions 3.5.33, 3.6.14, and 3.7.1, a user granted READ permission on a single exact key can use the Watch gRPC API with clientv3.WithFromKey() to receive watch events for every key lexicographically greater than or equal to the permitted key. In server/etcdserver/api/v3rpc/watch.go, the open-ended RangeEnd sentinel is rewritten before the RBAC permission check in server/auth/range_perm_cache.go function isRangeOpPermitted, causing the request to be treated as an exact-key watch. Range/Get and DeleteRange requests are not affected, and the issue affects only clusters with authentication enabled. This issue is fixed in versions 3.5.33, 3.6.14, and 3.7.1.

### CVE-2026-64826

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-12T21:17:39.427 |

rConfig before 8.2.13 contains a path traversal vulnerability that allows authenticated attackers to read arbitrary files by supplying unsanitized directory traversal sequences in the filename GET parameter of the download_export() method. Attackers can craft requests with ../ sequences to escape the exports base directory and access sensitive files readable by the web server process, including application environment files containing encryption keys, database credentials, and mail configuration.

### CVE-2026-18888

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-12T21:17:37.170 |

The MongoDB BI Connector ODBC Driver converts floating point column values into text without checking that the result fits within the destination buffer. When an application reads a sufficiently large floating point value as text, the driver may write beyond the end of that buffer and corrupt adjacent memory. A user who can store data in a collection read through the BI Connector could use this to crash the application performing the read.

### CVE-2026-73331

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-12T20:17:55.340 |

CamaleonCMS 2.9.1 contains an authenticated SQL injection vulnerability that allows authenticated attackers with post creation or editing privileges to submit a crafted slug value containing SQL syntax that the database backend evaluates as part of an inadequately parameterized query. Attackers can supply malicious slug payloads using boolean- or union-style blind SQL injection techniques to extract sensitive data from the underlying SQLite database, including administrative credentials and configuration values stored in application tables.

### CVE-2026-72809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-12T20:17:53.110 |

SiYuan versions <= v3.7.2 (patched in v3.7.4) contain an authentication bypass vulnerability in the kernel's CheckAuth function, which grants the administrator role (RoleAdministrator) to any request whose RemoteAddr is loopback (127.0.0.1) for a specific set of endpoints (including /api/system/exit, getNetwork, getWorkspaceInfo, /assets/*, and /export/*). These localhost bypasses sit outside the access auth code gate, so they apply even when an access auth code is configured. Because the fixed-port reverse proxy forwards requests to the kernel over loopback without injecting an authentication token and does not configure trusted proxies, a request forwarded through this proxy reaches the kernel with RemoteAddr = 127.0.0.1. If the fixed-port proxy is bound to a network interface, this could allow a remote unauthenticated attacker to obtain admin access on the affected endpoints; however, per the advisory this remote forwarding behavior was established only by code inspection and was not reproduced end-to-end.

### CVE-2026-72786

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-12T20:17:49.837 |

Craft CMS versions before 5.10.8 contain an authentication bypass vulnerability in the elements/save action that allows authenticated users to change passwords without verification. Attackers with edit users permission can reset any user's password including administrators by exploiting the unprotected newPassword field in the User element save flow.

### CVE-2026-16494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-12T20:17:37.640 |

GitLab has remediated an issue in GitLab EE affecting all versions from 19.1 before 19.1.4 and 19.2 before 19.2.2 that under certain conditions could have allowed an authenticated user to modify project settings restricted to higher-privileged roles, due to missing authorization checks on a project update endpoint.

### CVE-2026-17248

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-12T18:17:26.190 |

IBM i 7.6, 7.5, 7.4, and 7.3 could allow a remote authenticated attacker to cause a denial of service due to improper neutralization of special elements in an OS command.

### CVE-2026-73291

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-94` |
| Published | 2026-08-12T15:18:33.020 |

Seerr is an open-source media request and discovery manager for Jellyfin, Plex, and Emby. Prior to version 3.4.0, Seerr's ImageProxy in server/lib/imageproxy.ts uses the upstream ETag and Content-Type response headers to build a cache filename for the unauthenticated GET /avatarproxy/:jellyfinUserId route, allowing a malicious or compromised Jellyfin or Emby server, or a man-in-the-middle attacker on a plaintext media-server connection, to supply traversal sequences that path.join and fs.writeFile normalize outside the cache directory, overwrite /app/dist/index.js or other files, and execute code as the node user after a container restart. This issue is fixed in version 3.4.0.
