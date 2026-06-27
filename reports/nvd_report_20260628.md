# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-06-27 15:00 UTC
- **対象期間**: `2026-06-26T15:00:57.000Z` 〜 `2026-06-27T15:00:22.000Z`
- **重要CVE数**: 150 件（Critical 9.0+: 43 件 / High 7.0〜: 107 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVE のうち **CVSS 7.0 以上** が 30 件を超え、特に **オープンソースの SaaS/CI/CD プラットフォーム**（Kestra、OpenProject、Craft CMS など）や **低コード/WordPress 系プラグイン** に集中しています。  
- **認証バイパス** や **パスサフィックスの不適切な判定** が原因のリモートコード実行 (RCE) が多数。  
- **SQLi / IDOR / 任意ファイルアップロード** が WordPress 系プラグインで頻発し、特権昇格や情報漏洩に直結。  
- **デフォルトシークレットキーやテンプレートエンジンの実行機能** がそのまま利用可能になるケースが目立ち、**攻撃者が認証なしで完全制御を取得** できる深刻度 10.0 の脆弱性が複数報告されています。

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / バージョン | 主な脆弱性種別 | 重大度 (CVSS) | 注目理由・影響範囲 |
|-----|-------------------|----------------|---------------|-------------------|
| **CVE‑2026‑53576** / **CVE‑2026‑49869** | **Kestra** ( < 1.0.45, < 1.3.21 ) | 認証バイパス → 任意 API 呼び出し (RCE) | 10.0 | `@Filter("/api/v1/**")` がパスサフィックス `/configs` だけで認証をスキップ。攻撃者は任意の REST エンドポイントに認証なしでアクセスでき、ジョブ実行やシークレット取得が可能。 |
| **CVE‑2025‑32432** | **Craft CMS** (3.0.0‑RC1〜5.0.0‑RC1, < 5.6.17) | リモートコード実行 (RCE) | 10.0 | Craft のプラグインロードロジックに不適切なシリアライズが残り、任意 PHP オブジェクトを注入できる。公開サイトだけでなく、管理画面が無効化されている環境でも攻撃が成立。 |
| **CVE‑2025‑10035** | **GoAnywhere MFT** (任意バージョン) | デシリアライズ RCE | 10.0 | ライセンスサーブレットで署名付きライセンスレスポンスを偽造し、任意オブジェクトをデシリアライズ。内部コマンド実行やファイル転送機能のフルコントロールが取得できる。 |
| **CVE‑2026‑52785** | **OpenProject** ( < 17.3.3, < 17.4.1 ) | SQL Injection (timestamps パラメータ) | 9.9 | `timestamps` パラメータで任意の SQL を注入可能。プロジェクトの履歴情報取得だけでなく、データベース全体の改ざん・情報漏洩につながる。 |
| **CVE‑2026‑54350** | **Budibase** ( < 3.39.12 ) | 認証なしデータ抽出 (NoAuth) | 10.0 | 公開アプリの任意閲覧でバックエンド MongoDB / DynamoDB 等の全コレクションを取得でき、機密データが丸ごと漏洩。書き込み権限が付与された PUBLIC クエリがある場合は改竄も可能。 |

> **注:** 上記は「CVSS 10.0」または「9.9」かつ **広範囲に影響が及ぶ**（認証不要、RCE、データ全体漏洩）ものを選出。OpenProject 系の複数脆弱性（IDOR、デフォルトシークレットキー、キャッシュ汚染）も深刻ですが、代表例として **CVE‑2026‑52785** を掲載しています。

---

## 3. 推奨アクション  

### 共通対策
- **脆弱性情報の定期的なモニタリング**（GitHub Security Advisories、CVE データベース、各ベンダーのアナウンス）を実施。  
- **インシデントレスポンス手順**を整備し、**影響範囲の即時スキャン**と **緊急パッチ適用** を自動化。  
- **最小権限の原則**を徹底し、外部から直接アクセスできる管理 API・管理画面は IP 制限や VPN 経由に限定。

### 製品別具体的対策

| 製品 | 現行バージョン | 推奨アップデート | 追加設定 / 対策 |
|------|----------------|-------------------|-----------------|
| **Kestra** | < 1.0.45 / < 1.3.21 | **1.0.45** 以上、**1.3.21** 以上へアップデート | `AuthenticationFilter` のパスチェックを **正確なパス** (`/api/v1/configs`) に変更し、**ホワイトリスト方式**から **認証必須** に切り替える。 |
| **Craft CMS** | 3.x‑RC1〜5.x‑RC1 (5.6.16 以前) | **5.6.17** 以上へアップデート | 不要なプラグインは削除し、**シリアライズ設定** (`allow_url_include` 等) を `false` に。 |
| **GoAnywhere MFT** | 任意 | **ベンダー提供のパッチ**（2025‑Q3 リリース）を適用 | ライセンスサーブレットへの **署名検証ロジック** を最新にし、**外部からのライセンスリクエスト** をファイアウォールで遮断。 |
| **OpenProject** | < 17.3.3 / < 17.4.1 | **17.3.3** 以上、**17.4.1** 以上へアップデート | `timestamps` パラメータの入力バリデーションを実装。`SECRET_KEY_BASE` は **環境変数で安全に管理**（`OVERWRITE_ME` は使用禁止）。 |
| **Budibase** | < 3.39.12 | **3.39.12** 以上へアップデート | 公開アプリの **認証設定** を必須にし、`PUBLIC` クエリは **書き込み権限を付与しない**。バックエンド DB の **ネットワーク制限**（IP ホワイトリスト）を設定。 |
| **WordPress プラグイン系** (Uncanny Automator Pro, Dokan Pro, Buddyboss Platform, Paytium, Easy Elements, etc.) | 各プラグイン ≤ 公開バージョン | 各プラグインの **最新安定版**（2026‑05 以降リリース）へ更新 | `wp_ajax_nopriv_*` 系の **権限チェック** を必ず実装。`file_uploads` を必要最小限に制限し、`wp-content/uploads` の **実行権限** を `0755` へ。 |
| **mise** (dev‑tool manager) | < 2026.3.10 | **202

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-53576

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-288` |
| Published | 2026-06-26T22:16:32.840 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.0.45 and 1.3.21, the authentication filter for the REST API (@Filter("/api/v1/**")) treats any request whose path ends in /configs as the public instance-config endpoint and forwards it without a credential check. kestra addresses its resources by URL path segments that the caller chooses (/api/v1/{tenant}/flows/{namespace}, /api/v1/{tenant}/executions/{namespace}/{id}, /api/v1/{tenant}/namespaces/{namespace}/kv/{key}). An anonymous caller picks the literal configs as the final segment, and the request bypasses Basic-Auth entirely. Because the bypass reaches the flow-create and execution-trigger routes, an unauthenticated caller creates a flow containing a Shell or Process task and runs it. The task executes as root inside the kestra container. The official docker-compose.yml mounts /var/run/docker.sock, so root in the container reaches the host Docker daemon. This vulnerability is fixed in 1.0.45 and 1.3.21.

### CVE-2026-49869

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-184;CWE-287;CWE-918` |
| Published | 2026-06-26T22:16:32.113 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.0.45 and 1.3.21, AuthenticationFilter in Kestra OSS uses request.getPath().endsWith("/configs") to whitelist the public configuration endpoint from Basic Auth. Because the check is a suffix match rather than an exact path match, any API path whose last segment is configs bypasses authentication entirely. An unauthenticated remote attacker can exploit this to create and execute arbitrary workflows without credentials. Because Kestra ships with script execution plugins (plugin-script-shell, plugin-script-python, etc.) enabled by default, this directly results in unauthenticated Remote Code Execution as root inside the Kestra worker container.  This vulnerability is fixed in 1.0.45 and 1.3.21.

### CVE-2026-54350

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89;CWE-943` |
| Published | 2026-06-26T21:16:35.040 |

Budibase is an open-source low-code platform. Prior to 3.39.12,  an unauthenticated visitor of any published Budibase app reads every document of the backing MongoDB, CouchDB, Elasticsearch, DynamoDB-PartiQL, or REST-with-JSON-body collection and, where the builder has published a PUBLIC write query, modifies every document of that collection with one HTTP request. enrichContext at packages/server/src/sdk/workspace/queries/queries.ts:121-138 substitutes parameter values into the raw JSON body of a query, then JSON.parses the result. The validator validateQueryInputs at packages/server/src/api/controllers/query/index.ts:61-71 rejects only Handlebars markers ({{, }}) in user input and does not escape JSON metacharacters (", \, }). A parameter value containing a closing quote and additional keys lifts attacker-controlled fields into the parsed filter object. For Mongo find, the parsed filter passes directly to collection.find() (packages/server/src/integrations/mongodb.ts:506-510). Duplicate-key JSON parsing overrides the builder's {name: "..."} with {name: {$exists: true}} and returns every document. The same primitive against an updateMany query (mongodb.ts:577-585) widens the filter scope to the full collection while the builder-controlled $set body runs against every matched document. The authorized middleware at packages/server/src/middleware/authorized.ts:141-148 short-circuits when the query's role is PUBLIC. CSRF is not enforced on this path. POST /api/v2/queries/:queryId (packages/server/src/api/routes/query.ts:63) accepts the call with no session, only an x-budibase-app-id header that is public from the published-app URL. This vulnerability is fixed in 3.39.12.

### CVE-2025-10035

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-502` |
| Published | 2025-09-18T22:01:51.337Z |

A deserialization vulnerability in the License Servlet of Fortra's GoAnywhere MFT allows an actor with a validly forged license response signature to deserialize an arbitrary actor-controlled object, possibly leading to command injection.

### CVE-2025-32432

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94` |
| Published | 2025-04-25T15:04:06.272Z |

Craft is a flexible, user-friendly CMS for creating custom digital experiences on the web and beyond. Starting from version 3.0.0-RC1 to before 3.9.15, 4.0.0-RC1 to before 4.14.15, and 5.0.0-RC1 to before 5.6.17, Craft is vulnerable to remote code execution. This is a high-impact, low-complexity attack vector. This issue has been patched in versions 3.9.15, 4.14.15, and 5.6.17, and is an additional fix for CVE-2023-41892.

### CVE-2026-52785

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T20:17:19.133 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, there is a SQL injection in timestamps functionality. OpenProject baseline comparison allows callers to request historic work-package attributes using the timestamps parameter. This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-52782

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-26T20:17:18.737 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, there is an IDOR through /projects/<A>/settings/project_storages/<A_ps_id> via PATCH parameter "storages_project_storage[project_folder_id]" leads to Access to Unauthorized Resources. A project-admin in one project can hijack the managed Nextcloud or OneDrive folder of another project on the same storage by writing the victim project's project_folder_id into the attacker's Storages::ProjectStorage row. The next managed-folder sync overwrites the ACL on the referenced folder with the attacker project's user list. This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-46386

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-798;CWE-1188;CWE-1392` |
| Published | 2026-06-26T20:17:13.380 |

OpenProject is open-source, web-based project management software. Prior to , the official openproject/openproject Docker image ships ENV SECRET_KEY_BASE=OVERWRITE_ME as the default Rails master key. Combined with cookies_serializer = :marshal, this gives any logged-in user a deterministic Marshal-deserialization path reachable via the /my/two_factor_devices cookie reader This vulnerability is fixed in .

### CVE-2026-56059

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T15:16:45.273 |

Subscriber Arbitrary File Upload in Travel Booking <= 2.2.5 versions.

### CVE-2026-56058

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T15:16:45.153 |

Subscriber Arbitrary File Upload in Quform <= 2.23.0 versions.

### CVE-2026-56027

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T15:16:42.540 |

Customer Arbitrary File Upload in Booster for WooCommerce <= 8.0.1 versions.

### CVE-2026-12415

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-06-27T05:16:41.620 |

The Invoice Generator plugin for WordPress is vulnerable to privilege escalation due to a missing capability check on the pravel_invoice_edit_account() AJAX action in versions up to, and including, 1.0.0. The handler is exposed via wp_ajax_nopriv_pravel_invoice_edit_account, accepts an attacker-controlled user_id and user_email from POST data, and calls wp_update_user() without verifying authentication, ownership, or a nonce. This makes it possible for unauthenticated attackers to change the email address of any user, including administrators, and then trigger WordPress's password reset flow to gain access to the targeted account.

### CVE-2026-0685

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-06-26T16:16:29.757 |

Server side template inject (SSTI) in the expression evaluation component in Genshi Template Engine version 0.7.9 allows a remote attacker to achieve remote code execution (RCE) via crafted template expressions.

### CVE-2026-56057

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-26T15:16:45.033 |

Subscriber PHP Object Injection in Uncanny Automator Pro <= 7.3.0.6 versions.

### CVE-2026-56033

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-26T15:16:43.260 |

Unauthenticated Privilege Escalation in Dokan Pro <= 5.0.4 versions.

### CVE-2026-56032

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-26T15:16:43.140 |

Subscriber PHP Object Injection in Buddyboss Platform <= 3.0.4 versions.

### CVE-2026-56030

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-26T15:16:42.900 |

Unauthenticated Privilege Escalation in Paytium <= 5.0.2 versions.

### CVE-2026-56028

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-26T15:16:42.660 |

Unauthenticated Privilege Escalation in Easy Elements for Elementor &#8211; Addons &amp; Website Templates <= 1.4.9 versions.

### CVE-2026-54352

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-06-26T21:16:35.293 |

Budibase is an open-source low-code platform. Prior to 3.39.9, `POST /api/pwa/process-zip` at packages/server/src/api/routes/static.ts:24 accepts a builder-uploaded .zip, extracts it with extract-zip@2.0.1 into a temp directory, then for each entry listed in icons.json validates the icon path, opens it, and streams the bytes into MinIO. The resulting object is served back via GET /api/assets/{appId}/pwa/{uuid}.png. extract-zip@2.0.1 preserves absolute symlink targets when restoring symlink entries. The icon-source validator at packages/server/src/api/controllers/static/index.ts:259-268 resolves the icon source string against baseDir (path.resolve), checks resolvedSrc.startsWith(baseDir + path.sep) against that string, and calls fs.existsSync(resolvedSrc) which follows symbolic links to confirm the target exists. None of the three calls reject symbolic-link entries. packages/backend-core/src/objectStore/objectStore.ts:302 then calls (await fsp.open(path)).createReadStream() on the resolved path. fsp.open follows the symlink, the target file's bytes stream into MinIO, and the response of the asset-fetch endpoint returns those bytes verbatim. Result: a workspace-level builder reads any file the server process can open. This vulnerability is fixed in 3.39.9.

### CVE-2026-52780

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-06-26T20:17:18.490 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, cache store poisoning leads to Remote Code Execution (RCE). This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-33646

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-26T18:16:58.420 |

mise manages dev tools like node, python, cmake, and terraform. Prior to 2026.3.10, mise processes .tool-versions files through the Tera template engine during parsing, with the exec() function registered, enabling arbitrary command execution. Unlike .mise.toml files, .tool-versions files are not subject to trust verification in non-paranoid mode. This means an attacker can place a malicious .tool-versions file in a git repository, and when a victim with mise activated cds into the directory, arbitrary commands execute without any trust prompt. This vulnerability is fixed in 2026.3.10.

### CVE-2025-11919

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-26T16:16:29.193 |

The default JVM can access files and directories under `/tmp/` including the `$TemporaryDirectory` of other users on the same cloud instance (`/tmp/UserTemporaryFiles/`).  The `-init` file for the the JVM initialization exists in the vulnerable directory during the startup of the JVM.  An attacker with access to the shared `/tmp/` space can preemptively create or replace `.jar` files or directories (via the `-init` file) that the victim JVM will resolve first in its classpath.  By strategically placing a malicious version of a commonly used library (e.g., `commons-io`) in a location that is included in the classpath before the legitimate version, an attacker can cause the JVM to load the malicious class during startup, thereby executing the attacker's code.

### CVE-2026-31928

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-06-26T23:17:08.697 |

The DMP-5000 devices are shipped with a default administrative web account with weak authentication controls, which are not required to be changed during initial configuration or operation. Using these accounts provides full system access.

### CVE-2026-28701

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-26T23:17:08.537 |

Various versions of Daktronics Controller Firmware could allow authenticated and unauthenticated remote users to escape the intended directory and enumerate arbitrary file system paths.

### CVE-2026-56070

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:46.940 |

Unauthenticated SQL Injection in Advance Product Search <= 1.4.4 versions.

### CVE-2026-56068

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:46.620 |

Unauthenticated SQL Injection in JetEngine <= 3.8.10.2 versions.

### CVE-2026-56067

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:46.260 |

Unauthenticated SQL Injection in JetSmartFilters <= 3.8.3 versions.

### CVE-2026-56062

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:45.623 |

Unauthenticated SQL Injection in Quotes llama <= 3.1.5 versions.

### CVE-2026-56036

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:43.617 |

Unauthenticated SQL Injection in 워드프레스 결제 심플페이 <= 5.5.6 versions.

### CVE-2026-56034

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:43.380 |

Unauthenticated SQL Injection in Library Management System <= 3.5.7 versions.

### CVE-2026-54831

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:40.587 |

Unauthenticated SQL Injection in GeoDirectory <= 2.8.162 versions.

### CVE-2026-54827

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:40.467 |

Unauthenticated SQL Injection in Real Estate 7 <= 3.5.9 versions.

### CVE-2026-54825

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:40.230 |

Unauthenticated SQL Injection in wpDataTables <= 7.4 versions.

### CVE-2026-54820

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:39.977 |

Unauthenticated SQL Injection in JetBooking <= 4.0.4.1 versions.

### CVE-2025-13188

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-121;CWE-119` |
| Published | 2025-11-14T22:32:06.220Z |

A vulnerability was detected in D-Link DIR-816L 2_06_b09_beta. Affected by this vulnerability is the function authenticationcgi_main of the file /authentication.cgi. Performing manipulation of the argument Password results in stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit is now public and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2025-1316

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` |
| Weaknesses | `CWE-78` |
| Published | 2025-03-04T23:36:59.724Z |

Edimax IC-7100 does not properly neutralize requests. An attacker can create specially crafted requests to achieve remote code execution on the device

### CVE-2026-57658

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T15:16:53.993 |

Administrator Arbitrary File Upload in TemplateSpare <= 4.2.0 versions.

### CVE-2025-12480

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2025-11-10T14:20:40.677Z |

Triofox versions prior to 16.7.10368.56560, are vulnerable to an Improper Access Control flaw that allows access to initial setup pages even after setup is complete.

### CVE-2026-54636

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T17:16:34.083 |

Dokku is a docker-powered PaaS. Prior to 0.38.7, the cron plugin utilizes commands in the app.json file to manage system cron running as the Dokku user. An app.json cron command utilizing special shell characters - including, but not limited to, > or ; - can break out of the Docker container and execute commands on the host as the Dokku user. This vulnerability is fixed in 0.38.7.

### CVE-2026-45408

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T17:16:33.427 |

Dokku is a docker-powered PaaS. Prior to 0.38.2, the app name validation regex (^[a-z0-9][^/:_A-Z]*$) permits shell metacharacters. When an authenticated user pushes to a git remote with a crafted app name, the name is embedded unquoted into a bash pre-receive hook script via an unquoted heredoc (<<EOF instead of <<'EOF') in fn-git-create-hook() at plugins/git/internal-functions:378. On git push, bash interprets the semicolon as a command separator, executing arbitrary commands as the dokku user. This vulnerability is fixed in 0.38.2.

### CVE-2026-45406

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-06-26T17:16:33.150 |

Dokku is a docker-powered PaaS. Prior to 0.38.2, the openresty-vhosts plugin copies files from an app's openresty/http-includes/ git repository directory to the host and then interpolates their filenames, unescaped, into a single-quoted shell string that is later parsed by eval. A filename containing a single quote breaks the quoting and allows command substitution to execute arbitrary commands on the host as the dokku user during the app's next deploy. This vulnerability is fixed in 0.38.2.

### CVE-2026-45405

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-06-26T17:16:33.007 |

Dokku is a docker-powered PaaS. Prior to 0.38.2, the git:from-archive and certs:add commands extract user-supplied tar/zip archives into temporary directories without sanitizing member paths or preventing symlink traversal. GNU tar creates symlinks during extraction and follows them for subsequent entries, allowing an attacker to write arbitrary files anywhere writable by the dokku user — including overwriting ~/.ssh/authorized_keys to gain unrestricted shell access. This vulnerability is fixed in 0.38.2.

### CVE-2025-54309

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-420` |
| Published | 2025-07-18T00:00:00.000Z |

CrushFTP 10 before 10.8.5 and 11 before 11.3.4_23, when the DMZ proxy feature is not used, mishandles AS2 validation and consequently allows remote attackers to obtain admin access via HTTPS, as exploited in the wild in July 2025.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-52784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-26T20:17:18.993 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, there is a CSRF on TARGET through /users/:id via POST parameter "user[admin]". This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-57659

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-26T15:16:54.977 |

Unauthenticated Cross Site Request Forgery (CSRF) in Paid Memberships Pro - Add Member From Admin <= 0.7.2 versions.

### CVE-2026-56055

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-26T15:16:44.917 |

Subscriber PHP Object Injection in RealHomes <= 4.5.3 versions.

### CVE-2026-56038

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:43.733 |

Contributor Privilege Escalation in Frisbii Pay <= 1.8.2 versions.

### CVE-2026-56010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-26T15:16:42.057 |

Subscriber Privilege Escalation in Abandoned Cart Pro for WooCommerce <= 10.4.0 versions.

### CVE-2026-56008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-06-26T15:16:41.927 |

Contributor Privilege Escalation in Fusion Builder <= 3.15.4 versions.

### CVE-2025-68052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-26T15:16:35.363 |

Unauthenticated Cross Site Request Forgery (CSRF) in Eagle Booking <= 1.3.4.3 versions.

### CVE-2026-55069

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-916` |
| Published | 2026-06-26T22:16:33.093 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.3.24, this vulnerability exists in the BasicAuth authentication component of the Kestra OSS workflow orchestration platform. An attacker who gains read access to the PostgreSQL database can exploit SHA-512's high computation speed to recover the administrator password offline. In Kubernetes deployments, a successful crack further enables reading of the cluster ServiceAccount Token and all K8s Secrets, achieving vertical privilege escalation. This vulnerability is fixed in 1.3.24.

### CVE-2026-32833

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T20:16:54.583 |

Cudy LT300 3.0 running firmware prior to version 2.5.12 contains an OS command injection vulnerability that allows authenticated attackers to execute arbitrary commands by injecting shell metacharacters into the cbid.system.ntp.current POST parameter in the system time configuration interface. Attackers can submit malicious payloads through the NTP settings endpoint to achieve remote code execution on the underlying system.

### CVE-2026-57518

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T17:16:34.927 |

Pagekit CMS 1.0.18 contains a privilege escalation vulnerability that allows authenticated users with the 'user: manage users' permission to escalate privileges by assigning arbitrary custom roles to themselves due to missing authorization checks in UserApiController::saveAction(). Attackers can assign themselves a custom role with the 'system: manage packages' permission and then upload and install a malicious PHP package through the admin package installer to achieve remote code execution.

### CVE-2026-57527

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-26T15:16:49.587 |

Zed Attack Proxy (ZAP) ViewState add-on before version 4 contains an insecure deserialization vulnerability that allows attackers who control a proxied web server to achieve arbitrary code execution by embedding a malicious serialized Java object in the javax.faces.ViewState HTTP response parameter. The JSFViewState.decode() method base64-decodes the ViewState value and passes it directly to ObjectInputStream.readObject() without a deserialization filter, allowlist, or type restriction, causing the malicious object to be deserialized within the ZAP JVM when the Desktop UI renders the ViewState panel.

### CVE-2026-56773

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:47.410 |

Teable's v2 REST API controller lacks @Permissions metadata on ORPC endpoints, allowing any authenticated user to bypass authorization checks. Attackers can read table schemas, create tables, and modify or delete records across bases and tables via endpoints like GET /api/v2/tables/get and POST /api/v2/tables/updateRecords.

### CVE-2025-10792

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P` |
| Weaknesses | `CWE-120;CWE-119` |
| Published | 2025-09-22T09:32:07.403Z |

A security vulnerability has been detected in D-Link DIR-513 A1FW110. Affected is an unknown function of the file /goform/formWPS. Such manipulation of the argument webpage leads to buffer overflow. The attack may be performed from remote. The exploit has been disclosed publicly and may be used. This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-56414

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T23:17:09.137 |

A vulnerability exists in H.View IP cameras certificate-related upload interfaces allow authenticated users to store arbitrary file content to fixed, persistent filesystem locations without validating file type, structure, or size. This design omission enables the placement of unexpected or malformed data in locations intended for trusted certificate material, which could affect system integrity or behavior even after reboot.

### CVE-2026-55975

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T23:17:08.997 |

A vulnerability exists in H.View IP cameras that could allow an authenticated user to supply unsanitized XML fields to the device's certificate generation interface, which are incorporated into a backend certificate creation command without proper input validation. This may allow for command execution with elevated privileges during certificate generation.

### CVE-2026-49991

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-862` |
| Published | 2026-06-26T20:17:17.817 |

RustFS is a distributed object storage system built in Rust. In 1.0.0-beta.4, authenticated users with only PutObject permission on their own bucket can exploit a path traversal vulnerability in the Snowball auto-extract feature to write arbitrary objects into other users' buckets, completely breaking multi-tenant isolation. The vulnerability chains three flaws: No ../ sanitization in tar entry key normalization; IAM wildcard matching uses raw (uncleaned) paths; and Filesystem path cleaning resolves ../ across bucket boundaries.

### CVE-2026-56876

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-61` |
| Published | 2026-06-26T18:17:03.447 |

extract-zip does not validate symlink targets when extracting zip archives. When processing a malicious zip file containing a symlink with a relative path like '../../../../etc/passwd', extract-zip will extract the symlink without validation, allowing it to point outside the extraction directory. Depending on how extract-zip is used, an attacker could read or write to arbitrary files.

### CVE-2026-55441

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-94;CWE-732` |
| Published | 2026-06-26T18:17:01.190 |

mise manages dev tools like node, python, cmake, and terraform. Prior to 2026.6.4, mise's trust feature gates config files (mise.toml, .tool-versions) through trust_check, but task-include files are loaded on a path that never reaches it. When a directory has a task-include dir (mise-tasks/, .mise/tasks/, …) but no config file, mise falls back to the default includes and renders each task's tera fields — and that tera environment has exec() registered. A {{ exec(command='…') }} in any rendered field runs arbitrary commands the moment the tasks are merely listed. There's no config file to gate on, so no trust prompt ever appears. Read-only commands trigger it: mise tasks, mise task ls, mise run, mise tasks --usage (the query shell completion runs on Tab). The victim only has to cd into a cloned repo and list or tab-complete a task. This vulnerability is fixed in 2026.6.4.

### CVE-2026-56035

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-1284` |
| Published | 2026-06-26T15:16:43.497 |

Unauthenticated Multiple Vulnerabilities in BitFire Security <= 5.0.3 versions.

### CVE-2026-54353

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-367;CWE-918` |
| Published | 2026-06-26T21:16:35.417 |

Budibase is an open-source low-code platform. Prior to 3.39.9, authenticated users with automation permissions can bypass Budibase's SSRF blacklist through DNS rebinding. The outbound fetch flow validates a hostname against the blacklist before the request is sent, but the actual socket connection later performs a separate DNS lookup through node-fetch. Since the validated IPs are never pinned to the connection, an attacker-controlled hostname can return a public IP during validation and a private/internal IP during the real connection. This results in a non-blind SSRF primitive against internal services reachable from the Budibase host, including loopback, RFC1918 ranges, and cloud metadata endpoints. This vulnerability is fixed in 3.39.9.

### CVE-2026-56663

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-06-26T17:16:34.453 |

AutoGPT is a workflow automation platform for creating, deploying, and managing continuous artificial intelligence agents. Prior to 0.6.52, an authenticated user can bypass the SSRF / private-IP protections in SendWebRequestBlock and reach internal network services. _is_ip_blocked() in backend/backend/util/request.py does not normalize IPv4-mapped IPv6 addresses before checking resolved IPs against the blocked IPv4 ranges, and does not block special-use ranges such as 100.64.0.0/10 (CGNAT, RFC 6598). A hostname that resolves to an IPv4-mapped IPv6 address therefore passes validation and the request reaches the embedded internal IPv4 endpoint. This affects all AutoGPT Platform deployments. This vulnerability is fixed in 0.6.52.

### CVE-2026-57667

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:55.810 |

Sales Representative SQL Injection in Groundhogg <= 4.5 versions.

### CVE-2026-57663

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:55.460 |

Contributor SQL Injection in Recipe Maker For Your Food Blog from Zip Recipes <= 8.2.7 versions.

### CVE-2026-57662

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:55.337 |

Contributor SQL Injection in Contest Gallery <= 30.0.0 versions.

### CVE-2026-57653

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:53.400 |

Contributor SQL Injection in WP Job Portal <= 2.5.2 versions.

### CVE-2026-57644

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:52.100 |

Contributor SQL Injection in Restaurant Menu by MotoPress <= 2.4.10 versions.

### CVE-2026-57643

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:51.983 |

Contributor SQL Injection in WP Post Author <= 3.9.1 versions.

### CVE-2026-57642

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:51.857 |

Contributor SQL Injection in Gallery  <= 4.7.8 versions.

### CVE-2026-57636

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:51.153 |

Contributor SQL Injection in wpForo Forum <= 3.0.9 versions.

### CVE-2026-57315

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-06-26T15:16:48.150 |

Contributor Remote Code Execution (RCE) in Blocksy Companion Pro <= 2.1.45 versions.

### CVE-2026-56064

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:45.860 |

Subscriber SQL Injection in Tourfic <= 2.22.5 versions.

### CVE-2026-33560

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:L/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-06-26T23:17:08.847 |

The DMP-5000 file service exposes authenticated arbitrary file upload functionality. There are exposed endpoints which allows authenticated users to upload files of any type without validation. No file extension filtering or content inspection is enforced which allows executable binaries and scripts to be accepted and written directly to the server.

### CVE-2026-12411

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-06-26T16:16:30.117 |

Broken Access Control in the devLXDInstancePatchHandler component of Canonical LXD allows an untrusted guest to mount, read, and overwrite another guest's custom storage volume via a crafted device PATCH request over /dev/lxd when security.devlxd.management.volumes is enabled.

### CVE-2026-56063

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:45.737 |

Unauthenticated Broken Access Control in MailChimp Block <= 1.1.15 versions.

### CVE-2026-54351

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-06-26T21:16:35.170 |

Budibase is an open-source low-code platform. Prior to 3.39.9, the webhook trigger endpoint in Budibase is publicly accessible and passes the full HTTP request body into automation execution parameters. A mass assignment vulnerability in externalTrigger() allows an attacker to overwrite the internal appId property by including it in the webhook POST body. When the automation is processed asynchronously (the default path for webhooks without a collect step), the worker executes the attacker-defined automation in the context of the victim's workspace, granting full read/write access to the victim's database. This vulnerability is fixed in 3.39.9.

### CVE-2026-50137

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T21:16:34.673 |

Budibase is an open-source low-code platform. Prior to 3.39.0, an anonymous attacker who knows or can enumerate a workspace id (app_...) and an S3-source datasource id (ds_...) can call this endpoint with no auth and obtain a 15-minute pre-signed PUT URL minted on the victim's IAM identity. The endpoint also returns the publicUrl so the attacker knows exactly where their PUT lands. Because bucket is attacker-controlled, the attacker can write to any bucket those IAM credentials can write to, not only the bucket the datasource was configured for. The Budibase server route POST /api/attachments/:datasourceId/url (packages/server/src/api/routes/static.ts) is registered with only the recaptcha middleware. There is no authorized(...) middleware in the chain. The controller (packages/server/src/api/controllers/static/index.ts::getSignedUploadURL) looks the requested datasource up, instantiates an AWS S3 client with the datasource's stored accessKeyId / secretAccessKey, and returns an AWS Signature V4 pre-signed PutObjectCommand URL for the caller-supplied bucket and key. The bucket is not pinned to the datasource's configured bucket. The workspace context required by sdk.datasources.get is sourced by getWorkspaceIdFromCtx (packages/backend-core/src/utils/utils.ts) from any of: the x-budibase-app-id header, the JSON body appId, a path segment that begins with the workspace prefix, or ?appId=. auth.buildAuthMiddleware([], { publicAllowed: true }) runs before any of this and explicitly allows anonymous requests. The currentWorkspace middleware's "deny access to dev preview" branch only triggers under isBrowser(ctx) && !isApiKey(ctx); isBrowser checks the parsed User-Agent for a recognised browser, so any non-browser client (curl, the supplied PoC, any tool not setting a browser UA) is neither and reaches dev workspaces too. This vulnerability is fixed in 3.39.0.

### CVE-2026-55188

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-522;CWE-862;CWE-863` |
| Published | 2026-06-26T20:17:26.587 |

RustFS is a distributed object storage system built in Rust. From 1.0.0-alpha.1 until 1.0.0-beta.9, RustFS contains an authorization bypass in the bucket replication admin API. The ListRemoteTargetHandler handler for listing remote replication targets only checks whether request credentials exist, but does not verify that the caller has replication or administrator permissions. As a result, an authenticated user with no effective bucket or admin permissions can list remote replication target configuration for a bucket. Because the returned BucketTarget objects include remote target credentials, this can disclose replication access keys and secret keys. This vulnerability is fixed in 1.0.0-beta.9.

### CVE-2026-52783

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-313` |
| Published | 2026-06-26T20:17:18.860 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, OpenProject's Storages module writes the OneDrive/SharePoint userless OAuth access_token plaintext to Rails.cache under the deterministic key storage.<id>.httpx_access_token, repopulated continuously by an hourly cron and every userless-OAuth call site (see Write cadence). None of the three allowed cache backends (file_store, memcache, redis) encrypts at rest. An attacker with read access to the cache backend recovers the Azure-AD application-tier bearer with an anonymous get over the memcached binary protocol (or the equivalent against Redis). This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-57655

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-06-26T15:16:53.643 |

Unauthenticated Cross Site Request Forgery (CSRF) in Child Theme Wizard <= 1.4 versions.

### CVE-2026-57645

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:52.223 |

newsletters_subscribers Broken Access Control in Newsletters <= 4.13 versions.

### CVE-2026-56031

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-06-26T15:16:43.020 |

Unauthenticated PHP Object Injection in Uncanny Automator <= 7.3.1.2 versions.

### CVE-2025-1094

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-149` |
| Published | 2025-02-13T13:00:02.061Z |

Improper neutralization of quoting syntax in PostgreSQL libpq functions PQescapeLiteral(), PQescapeIdentifier(), PQescapeString(), and PQescapeStringConn() allows a database input provider to achieve SQL injection in certain usage patterns.  Specifically, SQL injection requires the application to use the function result to construct input to psql, the PostgreSQL interactive terminal.  Similarly, improper neutralization of quoting syntax in PostgreSQL command line utility programs allows a source of command line arguments to achieve SQL injection when client_encoding is BIG5 and server_encoding is one of EUC_TW or MULE_INTERNAL.  Versions before PostgreSQL 17.3, 16.7, 15.11, 14.16, and 13.19 are affected.

### CVE-2026-52884

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-42` |
| Published | 2026-06-26T21:16:34.797 |

Notepad++ is a free and open-source source code editor. In v8.9.6.1, isInTrustedDirectory() does NOT canonicalize the path before checking. It uses a prefix-based check (PathIsPrefix() or equivalent) that matches paths starting with trusted directory strings. A path traversal using ..\..\ after a trusted directory prefix passes the check while resolving to an untrusted location. The CVE-2026-48800 patch adds isInTrustedDirectory() validation in Command::run() (RunDlg.cpp) before calling ShellExecute(). This function checks whether the resolved executable path is under a trusted directory.  This vulnerability is fixed in 8.9.6.2.

### CVE-2026-48800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T21:16:34.297 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.6.1, the <Command> tag text content inside <UserDefinedCommands> in shortcuts.xml is read by NppXml::value(aNode) (Parameters.cpp:3658) in the feedUserCmds() function and stored in UserCommand._cmd without any validation. When the user clicks the corresponding entry in the Run menu, NppCommands.cpp:4264 creates a Command object with string2wstring(ucmd.getCmd()) and calls run(), which invokes ShellExecute (RunDlg.cpp:221) with the attacker-controlled string as the executable path. The injected command appears as a normal menu item in the Run menu, making it a viable persistence mechanism.  This vulnerability is fixed in 8.9.6.1.

### CVE-2026-48778

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-06-26T21:16:34.167 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.6.1, the <GUIConfig name="commandLineInterpreter"> tag in config.xml is read by NppXml::value() (Parameters.cpp:6430) and stored in _nppGUI._commandLineInterpreter without any validation, whitelist, or digital signature check. When the user triggers IDM_FILE_OPEN_CMD (File → Open Containing Folder → cmd), NppCommands.cpp:228 creates a Command object with this value and calls run(), which invokes ShellExecute (RunDlg.cpp:221) with the attacker-controlled string as the executable path. This vulnerability is fixed in 8.9.6.1.

### CVE-2026-45195

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-06-26T16:16:30.893 |

Kernel software installed and running inside a Host VM may post improper commands to the GPU Firmware to trigger a memory read or write outside the permitted range of memory for the host kernel.



Addresses passed to the GPU Firmware can be used by the Firmware for more privileged memory accesses than are permitted by the system.

### CVE-2026-45257

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-123` |
| Published | 2026-06-26T15:16:39.280 |

The KTLS receive path decrypted each record in place, assuming that the mbufs holding received data were anonymous and safe to modify.  This assumption does not hold for data placed on a socket by sendfile(2), which can reference file-backed memory directly through non-anonymous M_EXTPG pages or EXT_SFBUF mbufs.  When the sender transmits such data over a loopback connection without enabling KTLS on the transmit side, the file-backed mbufs reach the receiver's decryption path unchanged.  Decrypting a record in place then overwrites the backing file's page cache instead of a private copy of the data.

An unprivileged local user who can read a file can overwrite its contents with data of their choosing by sending the file over a loopback connection on which they have enabled KTLS receive.  The write modifies the page cache directly, so it bypasses file flags such as schg and is written back to disk.  By overwriting a setuid binary or other trusted file, a local user can escalate privileges, potentially gaining full control of the affected system.

### CVE-2023-37524

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1104` |
| Published | 2026-06-27T02:16:27.603 |

HCL Traveler for Microsoft Outlook (HTMO) is susceptible to vulnerabilities due to .NET Framework 4.5 being out of service.  Since .NET Framework 4.5 has reached end-of-life and no longer receives security updates, it may expose the application to publicly known security weaknesses through vulnerable third-party components.

### CVE-2026-49984

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-180;CWE-200` |
| Published | 2026-06-26T22:16:32.243 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.0.45 and 1.3.23, the local internal-storage backend validates user-supplied paths for .. traversal before it converts Windows-style backslashes to forward slashes. An attacker can therefore smuggle a traversal sequence past the guard using backslashes (..\..\..\); the guard sees a harmless string, and the path is only rewritten to ../../../ after validation, immediately before the file is opened. Any authenticated user who can view an execution (the lowest-privilege role) can call GET /api/v1/{tenant}/executions/{executionId}/file?path=… and read any file on the server filesystem readable by the Kestra process, outside the storage sandbox and across every tenant and namespace. This includes the embedded H2 database (all flows, all users, all stored secrets), internal storage of every other tenant/namespace, mounted secret files, and the process environment (/proc/self/environ) which contains configured database and secret-backend credentials. It is a complete breach of Kestra's storage isolation and multi-tenancy boundary. This vulnerability is fixed in 1.0.45 and 1.3.23.

### CVE-2026-45807

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-26T22:16:31.973 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.0.43 and 1.3.19, several Kestra API endpoints accept a kestra:// URI from the client and pass it through StorageInterface.parentTraversalGuard before reading the underlying file from the local storage backend. The guard only inspects the literal URI.toString(), so a URL-encoded .. written as %2E%2E slips through. The downstream code then calls URI.getPath(), which decodes %2E%2E back to .., and the resulting path is handed to Paths.get(...) without normalization. The OS resolves the .. segments at open(2) time, so an authenticated user with a single execution can read any file the Kestra process has access to on the host filesystem (/etc/passwd, mounted secrets, other tenants' execution outputs, etc.). This vulnerability is fixed in 1.0.43 and 1.3.19.

### CVE-2026-55189

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862;CWE-863` |
| Published | 2026-06-26T20:17:26.717 |

RustFS is a distributed object storage system built in Rust. From 1.0.0-alpha.1 until 1.0.0-beta.9, when the FTP frontend is enabled, the FTP read and probe handlers dispatch directly to the storage backend without ever calling the IAM authorization function that the FTP write/list handlers (and the entire HTTP S3 path) use. As a result, any user who can authenticate to the FTP listener — including a user whose IAM policy contains an explicit Deny on s3:GetObject — can read (RETR) and stat (SIZE/MDTM) any object in any bucket, and probe any bucket (CWD), completely regardless of their IAM policy. This vulnerability is fixed in 1.0.0-beta.9.

### CVE-2026-21734

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-823` |
| Published | 2026-06-26T16:16:30.557 |

A web page that contains unusual GPU shader code is loaded into the GPU compiler process and can trigger a write out-of-bounds write crash in the GPU shader compiler library. On certain platforms, when the compiler process has system privileges this could enable further exploits on the device.



An edge case using a very small value in GPU shader code can cause a segmentation fault in the GPU shader compiler due to am out-of-bounds write.

### CVE-2026-57631

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:50.560 |

Administrator SQL Injection in Popup box <= 6.0.1 versions.

### CVE-2026-57628

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-06-26T15:16:50.207 |

Administrator SQL Injection in WP All Import <= 4.0.1 versions.

### CVE-2026-54826

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-26T15:16:40.350 |

Subscriber Insecure Direct Object References (IDOR) in SupportCandy <= 3.4.6 versions.

### CVE-2026-52885

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-06-26T21:16:34.920 |

Notepad++ is a free and open-source source code editor. Prior to 8.9.6.4, NppCommands.cpp checks the HMAC of the on-disk shortcuts.xml at the moment a user command fires (Time-of-Check). However, the command payload is taken from the in-memory _userCommands vector, which is populated at application startup and never re-synchronized with the on-disk file (Time-of-Use). Swapping shortcuts.xml between startup and command execution causes the HMAC check to validate a clean file while a malicious command runs. An attacker with write access to shortcuts.xml places a malicious version on disk before launch, then immediately restores the legitimate file. The HMAC check at execution time validates the restored legitimate file (check passes), while the malicious payload executes from memory. This vulnerability is fixed in 8.9.6.4.

### CVE-2026-46710

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-06-26T21:16:33.903 |

Notepad++ is a free and open-source source code editor. From 8.9.4 until 8.9.6, Notepad++ contains a local privilege escalation vulnerability in the installer. During installation, the installer invokes powershell.exe without using an absolute path after setting the working directory to the installation contextMenu directory. If an attacker can pre-place a malicious powershell.exe in a user-writable custom installation directory, and a privileged user later runs the installer and selects that directory, the attacker-controlled executable is launched with the elevated privileges of the installer. This vulnerability is fixed in 8.9.6.

### CVE-2026-47193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-862` |
| Published | 2026-06-26T20:17:13.527 |

OpenProject is open-source, web-based project management software. Prior to 17.3.3 and 17.4.1, the journal diff endpoint discloses hidden historical field values without enforcing object and field visibility. This vulnerability is fixed in 17.3.3 and 17.4.1.

### CVE-2026-47220

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-06-26T19:16:41.173 |

Envoy is an open source edge and service proxy designed for cloud-native applications. From 1.37.0 until 1.37.5 and 1.38.3, when the %REQUESTED_SERVER_NAME(X:Y)% is used in log format and host related options is specified, like HOST_FIRST, SNI_FIRST, it's possible to crash Envoy when the specified host header is missing in the request headers. This vulnerability is fixed in 1.37.5 and 1.38.3.

### CVE-2026-54341

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-06-26T18:17:00.417 |

Dragonfly is an in-memory data store built for modern application workloads. Prior to 1.39.0, a crafted RESTORE payload triggers an out-of-bounds read in DragonflyDB's listpack collection loaders, crashing the entire server process (SIGSEGV). Because DragonflyDB requires no authentication by default and RESTORE is a normal keyspace command, an unauthenticated remote attacker can crash the server with a single ~24-byte command — a remote, repeatable denial of service. This vulnerability is fixed in 1.39.0.

### CVE-2026-48743

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-06-26T18:17:00.173 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.35.11, 1.36.7, 1.37.3, and 1.38.1, Envoy can translate a downstream HTTP/3 request that is complete at the transport layer (HEADERS with FIN / headers-only close) but still carries a nonzero Content-Length into a complete upstream HTTP/1 request with unresolved body debt. In an HTTP/1 upstream deployment where the origin replies before reading the declared body and keeps the connection reusable, the beginning of the next Envoy-generated upstream request can be consumed as the first request's body. The remaining bytes are then parsed by the origin as a new HTTP/1 request. This was reproduced as a route-bypass/desync: direct /pwn was denied by Envoy, but the second downstream H3 stream received the response for backend-parsed GET /pwn HTTP/1.1. This vulnerability is fixed in 1.35.11, 1.36.7, 1.37.3, and 1.38.1.

### CVE-2026-48044

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-06-26T18:16:59.767 |

Envoy is an open source edge and service proxy designed for cloud-native applications. From 1.23.0 until 1.35.11, 1.36.7, 1.37.3, and 1.38.1, a  vulnerability has been identified in Envoy's zstd decompressor implementation (ZstdDecompressorImpl). When zstd decompression is enabled, processing a specially crafted, highly compressed zstd payload can lead to massive memory allocation. An attacker can exploit this to cause severe memory exhaustion, potentially resulting in an Out-Of-Memory (OOM) kill and Denial of Service (DoS) for the Envoy proxy. This vulnerability is fixed in 1.35.11, 1.36.7, 1.37.3, and 1.38.1.

### CVE-2026-48042

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1124` |
| Published | 2026-06-26T18:16:59.630 |

Envoy is an open source edge and service proxy designed for cloud-native applications. Prior to 1.35.11, 1.36.7, 1.37.3, and 1.38.1, destructor of JSON Object results in stack overflow when deeply O(100K) nested objects are present. This vulnerability is fixed in 1.35.11, 1.36.7, 1.37.3, and 1.38.1.

### CVE-2026-57231

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-668` |
| Published | 2026-06-26T17:16:34.697 |

Podman is a tool for managing OCI containers and pods. From 1.8.1 until 5.8.4, a container image that contains a environment variable with just a key and no value can trick podman into passing that variable from the host into the container. This is made worse by the fact that using an asterisk (*) will cause podman to pass all host variables into the container. So essentially a malicious image can exfiltrate all podman environment variables that are set in the session from where the container is launched. This vulnerability is fixed in 5.8.4 and 6.0.0.

### CVE-2026-55677

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-26T17:16:34.203 |

Echo is a Go web framework. Prior to 4.15.3 and 5.2.0, Echo's router and static file handler disagree on URL path decoding. The router matches routes using the raw encoded path (preserving %2F as-is), while StaticDirectoryHandler unescapes %2F to / before resolving filesystem paths. This allows an attacker to bypass route-level access controls and read static files without authorization. This vulnerability is fixed in 4.15.3 and 5.2.0.

### CVE-2026-5757

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-26T16:16:36.917 |

Unauthenticated remote information disclosure vulnerability in Ollama's model quantization engine allows an attacker to read and exfiltrate the server's heap memory, potentially leading to sensitive data exposure, further compromise, and stealthy persistence.

### CVE-2026-0828

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-06-26T16:16:29.860 |

Kernel driver ProcessMonitorDriver.sys in Safetica's endpoint client x64 , versions 10.5.75.0 and 11.11.4.0, allows unprivileged user to abuse IOCTL path and terminate protected system processes.

### CVE-2026-57647

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-26T15:16:52.503 |

Contributor Local File Inclusion in Panorama Viewer – 360 Degree Image + Video Viewer <= 1.6.1 versions.

### CVE-2026-56069

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-26T15:16:46.787 |

Unauthenticated Insecure Direct Object References (IDOR) in Toolset Forms <= 2.6.24 versions.

### CVE-2026-56061

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:45.503 |

Unauthenticated Broken Access Control in Subscriptions for WooCommerce <= 1.9.5 versions.

### CVE-2026-56060

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-06-26T15:16:45.390 |

Unauthenticated Sensitive Data Exposure in Print Invoice & Delivery Notes for WooCommerce <= 7.1.1 versions.

### CVE-2026-56029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-06-26T15:16:42.780 |

Unauthenticated Broken Authentication in CorvusPay WooCommerce Payment Gateway <= 2.7.4 versions.

### CVE-2026-56025

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:42.300 |

Unauthenticated Broken Access Control in Paymob for WooCommerce <= 4.1.2 versions.

### CVE-2026-54847

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:41.790 |

Unauthenticated Broken Access Control in Stylish Cost Calculator <= 8.3.9 versions.

### CVE-2026-54846

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:41.650 |

Unauthenticated Broken Access Control in Syncee Premium Dropshipping &amp; Wholesale <= 1.0.27 versions.

### CVE-2026-54839

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-06-26T15:16:41.373 |

Unauthenticated Sensitive Data Exposure in Trinity Backup &#8211; Backup, Migrate, Restore, Clone &amp; Schedule Backups <= 2.0.9 versions.

### CVE-2026-54837

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:41.240 |

Unauthenticated Broken Access Control in Intranet &amp; Private Site &#8211; All-In-One Intranet <= 1.8.1 versions.

### CVE-2026-54835

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:41.093 |

Unauthenticated Broken Access Control in Five Star Restaurant Menu <= 2.5.2 versions.

### CVE-2026-54834

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-06-26T15:16:40.947 |

Unauthenticated Sensitive Data Exposure in Object Cache 4 everyone <= 2.3.2 versions.

### CVE-2026-54832

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:40.703 |

Unauthenticated Broken Access Control in Gutenverse Companion <= 2.5.0 versions.

### CVE-2026-54824

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-06-26T15:16:40.110 |

Unauthenticated Sensitive Data Exposure in Ads by WPQuads <= 3.0.3 versions.

### CVE-2026-30041

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-06-26T15:16:37.683 |

An integer overflow in the PSD parser compnent of FastStone Image Viewer v8.3 allows attackers to execute arbitrary code or cause a Denial of Service (DoS) via supplying a crafted PSD file.

### CVE-2025-68064

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-26T15:16:35.617 |

Contributor Local File Inclusion in Goya Core < 1.0.9.4 versions.

### CVE-2025-68063

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-06-26T15:16:35.490 |

Contributor Local File Inclusion in Splash - Sport Club WordPress Theme for Basketball, Football, Hockey <= 4.4.3 versions.

### CVE-2026-50136

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-06-26T21:16:34.547 |

Budibase is an open-source low-code platform. Prior to 3.39.3, the application server exposes an unauthenticated endpoint that generates S3 PutObject presigned URLs using credentials stored in a workspace datasource. The route is protected only by the recaptcha middleware and does not require authentication, table permission, datasource permission, or builder access. A public caller who knows a workspace ID and S3 datasource ID can request a signed upload URL for attacker-controlled bucket and key values. This vulnerability is fixed in 3.39.3.

### CVE-2026-54833

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-06-26T15:16:40.823 |

Unauthenticated Backdoor in Enable CORS <= 2.0.3 versions.

### CVE-2026-50132

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284;CWE-352` |
| Published | 2026-06-26T21:16:34.420 |

Budibase is an open-source low-code platform. Prior to 3.39.0, `GET /api/chat-links/:instance/:token/handoff` is a public endpoint (no auth required) that performs a permanent, state-changing operation: it binds an external chat identity (Slack/Discord/MS Teams) to an authenticated Budibase user account, with no consent UI and no CSRF protection. The session token in the URL is created by the attacker (from their own /link slash command) and embeds the attacker's externalUserId. When an authenticated Budibase victim visits the URL, their account is silently and permanently linked to the attacker's Slack/Discord identity. The server responds with "Authentication succeeded." — no indication of what was linked. This vulnerability is fixed in 3.39.0.

### CVE-2026-54840

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-06-26T15:16:41.507 |

Unauthenticated Broken Access Control in Newsletters <= 4.13 versions.

### CVE-2026-13372

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-06-26T19:16:39.897 |

Incorrect link resolution by display name in the custom PowerShell VPN editor in Devolutions Remote Desktop Manager 2026.2.5 through 2026.2.11 allows an authenticated attacker with write access to a shared workspace to execute a PowerShell script in another user's context via a display name collision with an existing VPN script link.

### CVE-2026-9640

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-06-26T16:16:37.250 |

A privilege escalation vulnerability exists in LXD from 6.0 before 6.9, 5.21.0 before 5.21.5, and 5.0.0 before 5.0.7 regarding the handling of project-restriction policies during snapshot restoration.. An authenticated project operator in a restricted multi-tenant environment can bypass policy restrictions by importing a maliciously crafted instance backup containing restricted configuration keys within a snapshot. When the snapshot is restored, these restricted keys are applied to the live instance without policy validation. Starting the modified instance grants the operator unauthorized host root access.

### CVE-2026-47214

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-73;CWE-400` |
| Published | 2026-06-26T16:16:31.373 |

Docling simplifies document processing by parsing diverse formats and providing integrations with the generative AI ecosystem. Prior to 2.94.0, the HTML backend has unsafe URI and path handling. This vulnerability is fixed in 2.94.0.

### CVE-2026-57325

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:49.220 |

Unauthenticated Cross Site Scripting (XSS) in NanoMag <= 1.8 versions.

### CVE-2026-57322

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:48.860 |

Unauthenticated Cross Site Scripting (XSS) in weMail <= 2.1.2 versions.

### CVE-2026-57321

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-06-26T15:16:48.743 |

Contributor Arbitrary File Deletion in H5P <= 1.17.7 versions.

### CVE-2026-57319

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:48.627 |

Unauthenticated Cross Site Scripting (XSS) in FOX <= 1.4.8 versions.

### CVE-2026-57317

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:48.387 |

Unauthenticated Cross Site Scripting (XSS) in Simply Schedule Appointments <= 1.6.12.2 versions.

### CVE-2026-57314

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:48.037 |

Unauthenticated Cross Site Scripting (XSS) in SureCart <= 4.3.2 versions.

### CVE-2026-57312

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:47.563 |

Unauthenticated Cross Site Scripting (XSS) in Everest Forms <= 3.4.8 versions.

### CVE-2026-56072

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:47.250 |

Unauthenticated Cross Site Scripting (XSS) in WoodMart <= 8.5.3 versions.

### CVE-2026-56047

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:44.677 |

Unauthenticated Cross Site Scripting (XSS) in perfmatters <= 2.6.3 versions.

### CVE-2026-56045

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:44.443 |

Unauthenticated Cross Site Scripting (XSS) in Automatic < 3.135.1 versions.

### CVE-2026-56044

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:44.327 |

Unauthenticated Cross Site Scripting (XSS) in Blog2Social <= 8.9.2 versions.

### CVE-2026-56043

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:44.207 |

Unauthenticated Cross Site Scripting (XSS) in Customer Reviews for WooCommerce <= 5.110.1 versions.

### CVE-2026-56041

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:44.087 |

Unauthenticated Cross Site Scripting (XSS) in Responsive Lightbox <= 2.7.6 versions.

### CVE-2026-56040

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:43.967 |

Unauthenticated Cross Site Scripting (XSS) in Gutenverse Form <= 2.4.7 versions.

### CVE-2026-56039

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:43.850 |

Unauthenticated Cross Site Scripting (XSS) in Quick Interest Slider <= 3.1.6 versions.

### CVE-2026-56011

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-06-26T15:16:42.180 |

Unauthenticated Cross Site Scripting (XSS) in MapPress Maps for WordPress <= 2.97.3 versions.
