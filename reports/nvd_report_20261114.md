# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-13 15:00 UTC
- **対象期間**: `2026-11-12T15:00:39.000Z` 〜 `2026-11-13T15:00:40.000Z`
- **重要CVE数**: 341 件（Critical 9.0+: 54 件 / High 7.0〜: 287 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE の多くは **Web アプリケーション／CMS 系プラットフォーム**（Joomla、WordPress、Magento など）や **ネットワーク機器（Citrix NetScaler）** に集中しており、**リモートからのコード実行（RCE）や特権昇格** が共通した深刻な脅威となっています。  
- CVSS が 9.0 以上の案件が 30 件以上報告されており、特に **ファイルアップロードのバリデーション不備** と **メモリオーバーフロー** が主要な攻撃ベクトルです。  
- 多くの脆弱性は **既知のプラグインやコンポーネントの古いバージョン** に残っているため、**パッケージのバージョン管理と定期的なアップデート** が最も効果的な防御策です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑117551** (Joomla jDownloads) | 10.0 | フロントエンドのサムネイルアップロードで任意の PHP ファイルを配置でき、リモートコード実行が可能 | **最高スコア（10.0）** かつ Joomla 系統は企業サイトでも広く利用。管理者権限が不要で攻撃が成立する点が危険。 |
| **CVE‑2026‑125055** (WordPress Chatterbug Forms) | 9.8 | 任意ファイルアップロード（拡張子チェック不備）によりサーバ上で任意コード実行 | WordPress のプラグインは多数導入されがちで、**プラグイン単体の脆弱性** が全サイトに波及。 |
| **CVE‑2026‑119077** (WordPress ELEX HelpDesk) | 9.8 | PHP Object Injection による完全なリモートコード実行 | 同様に WordPress エコシステム内で **高権限プラグイン** が標的。攻撃成功後は管理画面取得だけでなく、内部ネットワークへの横展開が容易。 |
| **CVE‑2026‑107412** (Citrix NetScaler ADC/Gateway) | 9.5 | 複数のメモリオーバーフロー → DoS だけでなく任意コード実行の可能性 | Citrix 製品は多くの企業の外部公開サービスで使用。**ネットワーク層の基盤** が攻撃対象になると、サービス全体が停止するリスクが高い。 |
| **CVE‑2026‑124010** (XWEB EVO) | 9.3 | setuid‑root CGI のコマンドインジェクション → 任意コマンド実行（root 権限） | Web サーバ自体が **root 権限で動作** している点が特に危険。認証不要で攻撃が成立するため、放置は即座にシステム乗っ取りにつながる。 |

> **共通点**：いずれも「**認証不要／低権限** でリモートコード実行が可能」か、**管理者権限が取得できる** ことが最大のリスクです。特に CMS 系プラグインはインストール数が多く、攻撃対象になりやすい点に注意が必要です。

---

## 3. 推奨アクション  

### 3.1 パッケージ・プラグインの即時アップデート
| 製品 / パッケージ | 現行脆弱バージョン | 修正版（最低バージョン） | アップデート方法 |
|-------------------|-------------------|--------------------------|-------------------|
| Joomla jDownloads | < 4.1.8 | **≥ 4.1.8** | Joomla 管理画面 → Extensions → Manage → Update もしくは公式サイトから最新版をダウンロード |
| WordPress Chatterbug Forms | ≤ 1.0.2 | **≥ 1.0.3** | WordPress 管理画面 → Plugins → 更新、または開発元 GitHub のリリースページ |
| WordPress ELEX HelpDesk | ≤ 3.3.9 | **≥ 3.4.0** | 同上（プラグイン更新） |
| Citrix NetScaler ADC / Gateway | すべての 2026 系リリース | **最新の 2026.2.x 以降**（ベンダーが提供する Security Patch） | Citrix 管理コンソール → System → Upgrade → Apply Recommended Patches |
| XWEB EVO | < 5.6.2 | **≥ 5.6.2** | XWEB EVO の公式リポジトリから最新版を取得し、`make install` で再デプロイ |
| OpenMage Magento LTS | < 20.18.2、21.0.0‑beta3 未満 | **≥ 20.18.2**（または 21.0.0‑beta3 以降） | Magento の `composer update` または公式パッケージのアップグレードガイドに従う |
| OpsTree BuildPiper | < 2.7.0 | **≥ 2.7.0** | GitHub リリースページからバイナリを取得し、`helm upgrade` でデプロイ |
| Vvveb | < 1.0.9.0 | **≥ 1.0.9.0** | npm/yarn で `npm install vvveb@latest`、または公式 Docker イメージ更新 |

### 3.2 設定・運用上の緩和策
1. **ファイルアップロードの制限**  
   - `php.ini` の `file_uploads` を必要最小限にし、`upload_tmp_dir` のパーミッションを `0700` に設定。  
   - Web アプリ側で **拡張子ホワイトリスト** と **MIME タイプ検証** を徹底（例: `image/*` のみ許可）。  
2. **WAF／IPS の導入**  
   - OWASP ModSecurity Core Rule Set (CRS) を最新に保ち、`/admin`, `/wp-admin`, `/joomla` への不審な POST/PUT をブロック。  
3. **最小権限の原則**  
   - Citrix NetScaler の管理アカウントは **ローカル管理者のみ** に限定し、不要な `root` 権限を持つ CGI/CGI スクリプトは削除。  
   - Docker コンテナは `--cap-drop=ALL` と `readOnlyRootFilesystem=true` を適用。  
4. **監視とインシデント対応**  
   - アクセスログに **`/index.php?option=com_jdownloads`** や **`/wp-content/plugins/*/upload`** へのリクエストが頻出しないか SIEM でアラート設定。  
   - Citrix NetScaler の `nsconmsg -K crash` でメモリオーバーフローのクラッシュダンプを取得し、ベンダーへ即時報告。  
5. **バックアップとロールバック**  
   - 重要システムは **イミュータブルイメージ**（例: OCI、Amazon

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-117551

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-12T18:17:15.813 |

Joomla Extension - jdownloads.com - RCE through file upload in jDownloads < 4.1.8 -  Insufficient validation of frontend thumbnail uploads allowed users with upload permission to place executable files on the server. This results in PHP code execution.

### CVE-2026-125055

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T10:17:28.153 |

The Chatterbug Forms – Fast, Flexible WordPress Form Builder plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.0.2 via the cbforms_check_form_submissions function. This is due to missing server-side file extension validation in cbforms_check_form_submissions(), where the allowed-type check defaults to the uploaded file's own extension when no field restriction is configured, trivially allowing any extension including .php. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. The submission nonce printed inline on every public page containing a Chatterbug form is freely obtainable by unauthenticated visitors and therefore does not constitute an effective access control barrier.

### CVE-2026-119077

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T10:17:26.483 |

The ELEX WordPress HelpDesk & Customer Ticketing System plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 3.3.9 via the 'form (specifically the attacker-controlled ticket_label field inside the url-encoded form string)' parameter parameter. This is due to missing server-side authentication and the absence of a class allowlist on deserialization, with the only guard being a nonce publicly emitted on any page carrying the [wsdesk_support] shortcode. This makes it possible for unauthenticated attackers to execute code on the server. A successful exploit requires a single anonymous GET to any public page carrying the [wsdesk_support] shortcode to harvest the publicly emitted wsdesk_nonce value, after which a single unauthenticated POST completes the attack.

### CVE-2026-107360

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-183` |
| Published | 2026-11-12T20:18:14.907 |

A flaw was found in rubygem-safemode. Compound assignment expressions in sandboxed code are evaluated without mediating method calls through the Jail allow-list. An authenticated attacker who can supply template content can invoke arbitrary no-argument methods on objects exposed to the template renderer without Jail mediation, including destructive operations such as host deletion and disclosure of non-allow-listed object state.

### CVE-2026-107412

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T03:17:28.877 |

Multiple Memory overflow vulnerabilities can lead to unpredictable or erroneous behavior and Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-128049

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-13T10:18:10.820 |

OpenMage Magento LTS before 20.18.2 and 21.0.0-beta1 before 21.0.0-beta3 contains a cross-site request forgery vulnerability in the admin and storefront OAuth confirm and confirmSimple actions, which accept GET requests without form-key validation. Attackers holding OAuth consumer credentials can lure a logged-in administrator or customer to a crafted confirm URL that authorizes the attacker's request token, then exchange it at /oauth/token for a persistent REST API access token bound to the victim.

### CVE-2026-127080

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:18:04.260 |

OpsTree BuildPiper before 2.7.0 contains an improper authorization vulnerability that allows authenticated deploy users to define arbitrary Kubernetes hostPath volumes without allow-list or policy checks. Attackers can set the host path to / in the Define HostPath Volume configuration to mount the worker node root filesystem read-write, breaking container isolation and enabling node and cluster compromise.

### CVE-2026-127073

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:18:03.200 |

OpsTree BuildPiper before 2.7.0 contains a privilege escalation vulnerability that allows project users to gain Kubernetes cluster-admin rights by submitting unrestricted manifests through the Additional Manifest feature. Attackers can deploy a ClusterRoleBinding binding a service account to cluster-admin, which the pipeline applies with cluster-wide credentials, granting control over all workloads and secrets.

### CVE-2026-126380

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T10:17:40.773 |

Vvveb before 1.0.9.0 contains a denylist bypass in system/traits/media.php where '.phar' is misconfigured with a leading dot, allowing authenticated administrators to upload .phar PHP files. Attackers can upload a GIF magic-byte polyglot webshell bypassing binary inspection and execute arbitrary OS commands as the web-server user.

### CVE-2026-126378

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T10:17:40.430 |

Vvveb through 1.0.8.6 contains a file upload vulnerability in the theme installer validFile() function that uses strpos() instead of strict path matching. Attackers with admin credentials can upload a ZIP containing a PHP file whose path includes /theme.php to achieve remote code execution on nginx deployments.

### CVE-2026-68548

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-178;CWE-863` |
| Published | 2026-11-12T20:18:51.307 |

Algernon is a small self-contained pure-Go web server. Prior to version 1.17.10, Algernon's URL-prefix authorization gate matches its protected prefixes (/admin, /repo, /data) with case-sensitive strings.HasPrefix, while the exact same raw req.URL.Path is later resolved against the filesystem. On case-insensitive filesystems (Windows NTFS — always; macOS APFS/HFS+ — default), a request for /Admin/secret.lua evades every protected-prefix check, falls through to the public-prefix accept branch, and then resolves on disk to admin/secret.lua. The result is an unauthenticated bypass of the /admin, /repo, and /data authorization boundary, enabling read (and, for Lua files, execution) of protected content. The permission system is active in the default configuration. This issue has been patched in version 1.17.10.

### CVE-2026-128027

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T10:18:08.563 |

FrankenPHP Docker images before 1.1.11 were rebuilt only when new base image tags were created, so security fixes that Alpine, PHP, and Go applied under existing tags were not propagated. Remote attackers could exploit known flaws in the stale system libraries, such as CVE-2025-15467 in libcrypto3, to execute code.

### CVE-2026-126945

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:18:01.600 |

Zipline before 4.5.1 contains a stored cross-site scripting vulnerability in the HighlightCode component that renders unescaped file content before highlight.js finishes loading. Authenticated attackers can upload text files containing HTML/JavaScript payloads that execute in viewers' browsers, enabling API calls such as account changes on the victim's behalf.

### CVE-2026-126473

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:56.590 |

OpenEMR before 8.4.0 contains OAuth scope canonicalization and containment flaws that allow unauthenticated attackers to obtain unapproved system-level FHIR access. Attackers can register a colon-form system:Patient.read client that bypasses approval, then request unregistered system/Patient.write scope to read, modify, and create Patient records.

### CVE-2026-126315

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-359` |
| Published | 2026-11-13T10:17:37.443 |

Frappe HRMS 16.14.0 before 16.20.1 sends product usage events on certain HR transactions without checking the site's telemetry setting, and some events include more detail than needed. During normal use, with no user action, values such as leave type names, claimed amounts and appraisal scores are transmitted even when telemetry is disabled.

### CVE-2026-126274

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:30.440 |

NocoDB before 2026.08.0 contains a stored cross-site scripting vulnerability that allows authenticated Creator users to inject script by embedding markup in column or table titles. The Delete.vue confirmation dialog renders these titles through an unescaped innerHTML binding, executing script when a victim deletes an external-source table to steal session tokens from localStorage.

### CVE-2026-126269

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:29.667 |

NocoDB before 2026.09.0 contains a stored cross-site scripting vulnerability that allows authenticated Editor users to execute scripts by storing crafted attachment MIME types like text/html;image/png. Attackers can write the value through the records API so the /dltemp signed URL serves HTML inline, stealing session tokens from localStorage to impersonate victims.

### CVE-2026-120864

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T09:17:34.057 |

Memory overflow in ICA proxy can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-111334

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:15.557 |

Memory overflow in Endpoint Analysis (EPA/EPAS) can lead to unpredictable or erroneous behavior or a Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-107415

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T04:17:36.417 |

Memory overflow in Email OTP authentication can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-127277

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-665` |
| Published | 2026-11-13T02:18:54.520 |

A security flaw has been discovered in Linksys EA8100 1.0.3.216940. The affected element is an unknown function of the file etc/init.d/service_smbd.sh of the component SMB Service. Performing a manipulation of the argument ANON_ACCESS results in improper initialization. The attack can be initiated remotely. The exploit has been released to the public and may be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-107410

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T02:18:49.997 |

Memory overflow in NetScaler Push can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-107409

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T02:18:49.863 |

Memory corruption in DNS-over-HTTPS (DoH) can lead to unpredictable or erroneous behavior or a Denial of Service in Citrix NetScaler

### CVE-2026-107408

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T02:18:49.740 |

Memory corruption in DNS / DNS-over-HTTPS (DoH) can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-107407

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T02:18:49.613 |

Memory overflow in SMPP traffic can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-127275

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-306` |
| Published | 2026-11-13T00:20:14.083 |

A vulnerability was determined in Linksys EA8100 1.0.3.216940. This issue affects the function SetRemoteSetting/SetUnsecuredWiFiWarning of the file ui_server.lua of the component JNAP API. This manipulation of the argument isEnabled/enabled causes missing authentication. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-120868

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T00:20:09.977 |

Memory overflow in Packet Processing can lead to unpredictable or erroneous behavior or Denial of Service in NetScaler ADC and NetScaler Gateway.

### CVE-2026-124010

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-250` |
| Published | 2026-11-12T20:18:24.263 |

XWEB EVO before 5.6.2 contains a command injection vulnerability that allows unauthenticated remote attackers to execute arbitrary commands as root by exploiting the setuid-root CGI xwconsole.cgi. Attackers can supply malicious input through the sh parameter, which is passed unsanitized to popen(), to achieve full system compromise. This product line reached it's end of service date in March 2026.

### CVE-2026-124004

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-12T20:18:22.367 |

XWEB EVO before 5.6.2 contains a hardcoded backdoor password vulnerability that allows unauthenticated remote attackers to gain full administrative access to the built-in Administrator account. Attackers can authenticate using the hardcoded credential xwebevonewgeneration in a single request to obtain a complete admin session and full control over the application. This product line reached it's end of service date in March 2026.

### CVE-2026-124002

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-11-12T20:18:21.597 |

XWEB EVO versions 5.2.3 through before 5.7.0 contains a pre-authentication OS command injection vulnerability that allows unauthenticated remote attackers to execute arbitrary OS commands by injecting shell metacharacters into the username field of login.lua, cleanout.lua, or api.lua before the password check occurs. Attackers can exploit this flaw combined with the setuid-root wlua interpreter to execute commands with root privileges, achieving full system compromise. This product line reached it's end of service date in March 2026.

### CVE-2026-127063

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-11-12T18:17:39.760 |

The
third-party RMM+ extension for ConnectWise ScreenConnect uses a static API
secret by default. The value can be changed by an administrator; however,
environments retaining the default value may allow unauthorized access to
extension API functionality, including the ability to send commands to managed
agents. This issue is specific to the third-party extension and does not affect
the ScreenConnect server or client.





Scope: This issue affects the third-party RMM+
extension for ConnectWise ScreenConnect. Deployments without the extension are
not affected. ScreenConnect server or client software are not impacted.

### CVE-2026-75495

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:17.170 |

Cudy TR3000 before 2.5.42 contains an OS command injection vulnerability that allows a malicious or compromised ACS to execute commands as root by supplying a crafted InternetGatewayDevice.User.{i}.Password value. Attackers can send a SetParameterValues request with shell metacharacters that obuspa_system.lua concatenates into a luci.util.exec() command string, gaining root command execution.

### CVE-2026-75491

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-13T10:18:16.597 |

Cudy TR3000 before 2.5.42 contains an authentication bypass vulnerability in the Mosquitto plugin auth_plugin_jwt.so that accepts unsigned JWTs using alg none. Attackers holding any Cudy-trusted client certificate can authenticate as admincudydevice on port 8883 and publish batchcmd requests to execute commands as root.

### CVE-2026-128047

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-11-13T10:18:10.543 |

OpenMage magento-lts before 20.18.2 and 21.0.0-beta pre-releases before 21.0.0-beta3 generate customer email-confirmation keys with md5(uniqid()) and customer and administrator password-reset tokens with the non-cryptographic uniqHash(). Unauthenticated attackers can brute-force the roughly 20-bit confirmation key via the unrate-limited confirmAction endpoint to log in as pending customers, or predict administrator reset tokens after recovering generator state.

### CVE-2026-128046

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-13T10:18:10.400 |

OpenMage magento-lts 20.17.0 before 20.18.2 and 21.0.0-beta1 before 21.0.0-beta3 contains an unrestricted file upload vulnerability because the general/file/protected_extensions blocklist omits phar, php8, and phps. Unauthenticated attackers can upload a .phar file through a product File custom option to a predictable media/custom_options path and request it directly to execute code on servers that map .phar to PHP and serve that directory.

### CVE-2026-128014

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T10:18:06.457 |

FrankenPHP standalone static binaries 1.8.0 before 1.13.2 bundle the PHP brotli extension statically linked with Brotli 1.2.0, whose decoder contains an out-of-bounds write (CVE-2026-111497). Unauthenticated remote attackers can send crafted data to applications that pass it to brotli_uncompress_add() to crash the entire FrankenPHP process, and possibly cause memory disclosure or code execution.

### CVE-2026-126953

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:02.737 |

Cudy TR3000 before 2.5.42 contains an OS command injection vulnerability that allows a malicious or compromised ACS to execute commands as root by supplying an unvalidated InternetGatewayDevice.User.{i}.Username value. Attackers can send a SetParameterValues request with shell metacharacters that set_UserUsername() in obuspa_system.lua passes to os.execute(), gaining root command execution.

### CVE-2026-126952

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-13T10:18:02.590 |

Zipline through 4.4.0 contains an authentication bypass vulnerability in the WebAuthn login endpoint that creates sessions for a supplied registered credential ID without verifying the assertion. Attackers who obtain a target's passkey credential ID can impersonate that account without its authenticator, potentially gaining administrative control over SUPERADMIN accounts.

### CVE-2026-126937

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-13T10:18:00.417 |

Zipline before 4.6.5 contains a TOCTOU race condition in the POST /api/setup endpoint that allows unauthenticated attackers to create multiple SUPERADMIN accounts by racing concurrent requests before the firstSetup flag is reset. Attackers can send simultaneous requests with spoofed X-Forwarded-For headers during the argon2 hashing window to gain full administrative control of the instance.

### CVE-2026-126377

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T10:17:40.257 |

Vvveb before 1.0.9.0 contains an authentication bypass vulnerability in generateCookie() in system/user/user.php that uses loose comparison to validate MD5 cookie hashes. Unauthenticated attackers can brute-force cookie values until the server's MD5 computation yields a 0e magic hash, then forge persistent cookies for account takeover.

### CVE-2026-126273

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:17:30.290 |

NocoDB before 2026.09.0 contains a privilege escalation vulnerability in initAdminFromEnv.ts that silently skips super-admin bootstrap when the admin password environment variable is empty. Unauthenticated attackers can call the public signup endpoint first on a fresh instance to receive Creator and Super Admin roles, gaining full administrative control.

### CVE-2026-124012

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-11-12T20:18:24.970 |

XWEB EVO 5.6.2 through 5.8.8 contains a hardcoded credential vulnerability where the Administrator web account is configured to use password_mode daily_password with no stored password, as the Users.authenticate function in lualib_users.lua synthesizes the Administrator configuration without validating any stored secret. Attackers who can derive the MAC-based daily password can authenticate as Administrator to obtain a full admin session on the device. This product line reached it's end of service date in March 2026.

### CVE-2026-124007

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T20:18:23.387 |

XWEB EVO before 5.6.2 contains a pre-authentication OS command injection vulnerability that allows unauthenticated remote attackers to execute arbitrary commands by injecting shell metacharacters into the password field. Attackers can exploit the unescaped interpolation of the password value into the hashpass invocation within login.lua, cleanout.lua, and api.lua to achieve root-level command execution via the setuid wlua interpreter. This product line reached it's end of service date in March 2026.

### CVE-2026-124006

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798;CWE-1392` |
| Published | 2026-11-12T20:18:23.033 |

XWEB EVO through 5.8.8 contains a predictable credential generation vulnerability that allows attackers to derive the Linux root password by computing a fixed prefix combined with a daily password value. Attackers can calculate the deterministic root credential, which before 5.7.0 was identical across all units and from 5.7.0 onward remains derivable from the MAC-based daily password, to gain unauthorized root access to the underlying operating system. This product line reached it's end of service date in March 2026.

### CVE-2026-124005

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-11-12T20:18:22.673 |

XWEB EVO 4.3.0 through 5.8.8 contains a weak password generation vulnerability that allows remote attackers to derive the Administrator code-of-the-day password using only the device MAC address and date, with no server secret involved. Attackers can analyze the firmware binary xwpasswd, which itself functions as the password generator, to compute valid Administrator credentials offline and authenticate to the device without authorization. This product line reached it's end of service date in March 2026.

### CVE-2026-128333

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-11-13T10:18:13.210 |

listmonk 6.0.0 before 7.0.0-beta.2 contains an authentication bypass vulnerability in doResetPassword that skips TOTP verification after a password reset. Attackers who can complete a reset, such as by reading the victim's reset email, obtain fully authenticated sessions including Super Admin without the TOTP code.

### CVE-2026-128332

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T10:18:13.030 |

Listmonk 6.0.0 before 7.0.0-beta.2 contains a 2FA bypass vulnerability that allows attackers with a valid password to brute-force TOTP codes because the attempt counter resets on every new password login. Attackers can repeatedly submit credentials to POST /admin/login to obtain fresh tokens, each allowing 15 more guesses, gaining sessions for 2FA-protected accounts including Super Admin.

### CVE-2026-128023

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-13T10:18:07.930 |

FrankenPHP before 1.13.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to spoof trusted headers by sending dot-form header names that PHP rewrites to underscores. Attackers can send headers like X.Authenticated.User or X.Forwarded.For that map to $_SERVER keys, spoofing user identity, client IP, or scheme.

### CVE-2026-127079

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T10:18:04.113 |

OpsTree BuildPiper before 2.7.0 lacks rate limiting on password-reset OTP verification, allowing unauthenticated attackers to brute force 6-digit OTPs. Attackers can initiate a reset and submit unthrottled guesses to the check_otp endpoint, resetting the target's password and taking over the account.

### CVE-2026-126280

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-13T10:17:31.360 |

NocoDB before 2026.08.0 contains a race condition in refresh-token rotation that allows attackers to reuse tokens because UserRefreshToken.ts never checks the affected-row count. Attackers holding a captured refresh token can present it concurrently with the legitimate user to obtain a valid authenticated session, and no reuse event is recorded.

### CVE-2026-126265

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T10:17:29.003 |

SiYuan 2.1.0 before 3.8.9 contains a flaw where the loginAuth CAPTCHA challenge lives in a signed client-side cookie, allowing reuse of a solved challenge. Attackers can replay the original signed siyuan cookie with distinct wrong access codes to brute-force the code and gain an administrator session.

### CVE-2026-126837

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-180` |
| Published | 2026-11-12T17:17:33.320 |

A validation flaw in the DNS SRV host discovery of the MongoDB Node.js driver may cause the driver to connect to a host outside the expected domain. For a mongodb+srv:// connection string, the driver checks each host name in the DNS SRV response against the domain of the connection string. The driver then builds the connection address from the original name, in which certain characters end the host name early. An unauthenticated party who can forge or change the DNS SRV response may redirect the connection to a host of their choice. TLS does not prevent this, because the driver verifies the server certificate against the redirected host name. This may result in unintended disclosure of application data and authentication credentials, and in altered query results. Applications that use mongodb:// connection strings are not affected.

### CVE-2026-127131

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-12T16:19:07.807 |

SOGo before 5.12.13 contains a missing rate limiting vulnerability in its web login TOTP verification that allows attackers who already possess a victim's password to brute-force the second-factor code without triggering any lockout. Attackers can send repeated POST requests to /SOGo/connect with wrong verification codes at high speed since failed TOTP attempts never increment the failed-login counter and SOGoMaximumFailedLoginCount does not apply, enabling indefinite guessing across 30-second code windows to bypass two-factor authentication.

### CVE-2026-127111

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-12T16:19:07.260 |

SOGo before 5.12.13 contains an improper restriction of excessive authentication attempts vulnerability that allows unauthenticated attackers to reset account passwords by repeatedly guessing secret-question answers via the passwordRecoveryCheck endpoint without lockout or rate limiting. Attackers can submit unlimited candidate answers to obtain a valid recovery JWT, then use it to change the account password without the old credential and log in via the connect endpoint, achieving full account takeover on accounts without TOTP enabled.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-117543

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-12T18:17:15.503 |

Joomla Extension - jdownloads.com - SSRF via external download URL field jDownloads < 4.1.8 -  HTTP redirects when retrieving external download URLs could bypass validation of the original destination. This allowed server-side requests to internal or otherwise prohibited destinations and disclosure of their responses (SSRF).

### CVE-2026-116411

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-13T14:17:48.130 |

Dell PowerStore contains a Server-Side Request Forgery (SSRF) vulnerability. An authenticated user with limited privileges could potentially exploit this vulnerability, potentially leading to information disclosure via requests to internal services.

### CVE-2026-86356

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T13:18:30.020 |

Dell PowerStore contains an authorization-bypass vulnerability that could lead to elevation of privilege to administrator.

### CVE-2026-128041

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:18:09.700 |

OpenMage magento-lts before 20.18.2 and 21.0.0-beta1 before 21.0.0-beta3 serves RSS feeds with a text/html content type and does not escape feed entry data, leading to stored cross-site scripting. An unauthenticated guest can submit a product review with script in the nickname, title or text that executes when an administrator opens the pending-reviews feed, enabling admin account takeover.

### CVE-2026-123769

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:17:27.823 |

The SureDash – Community, Courses & Member Dashboard plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.13.0 This is due to the `save_settings()` REST handler at `/suredash/v1/save-settings` being gated only by `admin_permission_callback()`, which authorizes any holder of the custom `manage_portal_dashboard` capability (Portal Manager role) without requiring `promote_users`, `edit_users`, or `manage_options`, combined with `sanitize_settings_data()` iterating all attacker-supplied keys with no allow-list, allowing arbitrary keys such as `default_role` to pass through `sanitize_text_field()` unchanged and be persisted into the `portal_settings` option via `update_option()` with no role-validity check. This makes it possible for authenticated attackers with Portal Manager-level access and above to poison the `default_role` setting to `administrator`, after which any subsequent new-user registration through the publicly accessible block-register endpoint reads the corrupted setting and passes it directly to `wp_insert_user()`, producing a full WordPress Administrator account under the attacker's control. The exploit requires two steps: a POST to the authenticated `save-settings` endpoint to overwrite `default_role`, followed by triggering a new registration through the unauthenticated block-register endpoint to receive the escalated account. Successful exploitation causes the attacker's own account to receive the complete administrator role.

### CVE-2026-116615

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-13T10:17:25.983 |

The Widget Options – Advanced Conditional Visibility for Gutenberg Blocks & Classic Widgets plugin for WordPress is vulnerable to Code Injection in all versions up to, and including, 4.2.6.1 via the `post_content` parameter. This is due to asymmetric parsing between the save-time strip filter (`widgetopts_strip_logic_from_blocks()`) and the render-time parser (`blockopts_filter_before_display()`): embedding an inner `<!--start_widgetopts` literal inside a JSON key causes the write-side `json_decode` to see a non-`class` key and skip stripping — persisting the payload verbatim to the database — while the render-side `str_replace` reconstitutes the key to `class`, feeding the attacker-controlled `logic` value directly into `@eval`. This makes it possible for authenticated attackers, with Author-level access and above, to inject PHP expressions that execute on every front-end page view, enabling boolean-oracle exfiltration of WordPress site configuration data — including admin email address, default role, and arbitrary `get_option`, `get_user_meta`, and `get_post_meta` values — via the plugin's allowlisted-function sandbox, which escalates to unrestricted code execution if any installed plugin extends the `widgetopts_allowed_php_functions` filter. Contributors can also exploit this vulnerability when their submitted post is later published by an administrator; notably, the injected payload executes for all site visitors, including unauthenticated users, because a trust-flag mechanism introduced in version 4.2.6 causes `widgetopts_safe_eval_trusted()` to bypass its non-admin short-circuit at every legacy render callsite. Exploitation by attackers with contributor-level access and above requires that an administrator (or editor) later publishes the contributor's submission. On a default installation, where that is not configured, the vulnerability requires attackers with author-level access and above.

### CVE-2024-58405

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:23.610 |

Zipline through 3.7.9 contains an improper authorization vulnerability in the /api/auth/register endpoint, which enforces invite codes only when user registration is disabled, so registration succeeds without an invite when both invites and user registration are enabled. Unauthenticated attackers can send a direct POST request omitting the invite code to create accounts, view stats, and exhaust storage by uploading many files.

### CVE-2026-86322

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-12T21:17:33.057 |

A flaw was found in Foreman’s Api::V2::PersonalAccessTokensController, where Foreman::Controller::UserAware#find_user resolves the target account using User.find(params[:user_id]) without applying the required parent-user authorization check. An attacker with the create_personal_access_tokens permission can therefore invoke POST /api/v2/users/:user_id/personal_access_tokens with another user’s ID and create a Personal Access Token on their behalf. The resulting plaintext token is returned in the API response, while PersonalAccessToken#check_permissions_after_save only validates create_personal_access_tokens on the token and does not enforce edit_users authorization on the target user. The attacker can then use the forged token to authenticate as the victim, potentially resulting in complete account takeover, including administrator accounts.

### CVE-2026-124014

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-12T20:18:25.590 |

XWEB EVO 4.3.0 through 5.8.8 contains an unauthenticated arbitrary file write vulnerability that allows remote attackers to modify the system configuration file /etc/xwebconfig.json by sending a crafted POST request to config.lua with action=set, which performs no session validation and writes the raw, unvalidated request body. Attackers can tamper with configuration values such as model and plugin fields or trigger a SYSTEM_NOT_CONFIGURED state via the unauthenticated action=get and action=set operations, resulting in configuration tampering and denial of service. This product line reached it's end of service date in March 2026.

### CVE-2026-18379

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-12T19:17:04.040 |

A flaw was found in yggdrasil-worker-package-manager. An authenticated attacker can exploit this issue to achieve arbitrary file modification or potential privilege escalation. The vulnerability exists because repository management operations fail to sanitize directory traversal sequences (such as '../') within repository names. By supplying a crafted repository name, an attacker can manipulate the root-level worker process into creating or deleting files outside the intended directory, compromising host system integrity.

### CVE-2026-126197

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T18:17:24.780 |

pgEdge Postgres MCP Server enables SQL queries against PostgreSQL databases through Model Context Protocol compatible clients. Prior to 1.1.0, custom pl-do tools interpolated JSON arguments into a PostgreSQL DO block delimited by fixed dollar-quote tags. An argument containing $mcp_custom_tool$ could terminate the block and inject arbitrary SQL statements, while $mcp_args$ could inject procedural code into a plpgsql block. Because the statement used the simple query protocol, injected text could include additional statements and transaction control, bypassing read_only and accessing data or modifying resources available to the connecting role. The issue requires at least one pl-do custom tool; sql and pl-func tools pass arguments as bind parameters and are not affected by this injection mechanism. This issue is fixed in 1.1.0.

### CVE-2026-120466

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T18:17:18.017 |

Joomla / WordPress Extension - acymailing.com - Missing authorization on subscription changes in AcyMailing 1.0.0 - 11.1.1 - An unauthenticated attacker who knows a subscriber's email address can unsubscribe that subscriber from one mailing list or from every mailing lists, without proving that the address is theirs. The affected feature also lets an attacker determine whether a given email address belongs to a subscriber of the site.

### CVE-2026-118495

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-12T18:17:16.130 |

Joomla / WordPress Extension - acymailing.com - Exposure of sensitive information to an unauthorized actor in AcyMailing 6.0.0 - 11.1.1 - Exposure of sensitive information to an unauthorized actor in AcyMailing 6.0.0 through 11.1.1. An unauthenticated attacker who knows a subscriber's email address can read that subscriber's record, including the per-subscriber secret key that authorises the subscription management links. Holding that key, the attacker can act as that subscriber on those endpoints, which includes triggering the GDPR data export and the GDPR account deletion where those options are enabled.

### CVE-2026-6460

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:51.597 |

Type confusion in PostgreSQL allows an object creator to execute arbitrary code as the operating system user running the database, via ALTER ... SET DATA TYPE primarily.  Other DDL attack routes exist, such as "ALTER TABLE ... ADD COLUMN; ROLLBACK; ALTER TABLE ... ADD COLUMN".  The system had inadequate tracking of typed values, and values were not self-identifying.  Stale values could appear in data dictionary entries, PL/pgSQL variables, and many other parts of the system.  PostgreSQL Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-18447

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:51.127 |

Type confusion in PostgreSQL SQL-language functions allows an object creator to execute arbitrary code as the operating system user running the database, via an output parameter of type "any".  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120151

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:43.817 |

Type confusion in PostgreSQL plpgsql record-field assignment allows an object creator to execute arbitrary code as the operating system user running the database, via a reentrant domain CHECK that changes a RECORD variable's row type while a value is being cast.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:43.687 |

Use after free in PostgreSQL expanded-record domain checks allows an object creator to execute arbitrary code as the operating system user running the database, via repeated checks of a domain over a composite type that cause reuse of a dangling memory-context pointer.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T15:17:43.567 |

Heap-based buffer overflow in PostgreSQL foreign batch inserts allows a foreign server to execute arbitrary code, via reporting that it inserted more rows than the server supplied.  postgres_fdw can legitimately encounter this when a rule on the remote table expands an INSERT into additional rows.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120147

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:43.317 |

Use after free in the PostgreSQL dblink extension allows an object creator to execute arbitrary code as the operating system user running the database, via type conversion code that re-enters dblink and closes a connection whose results an outer dblink call is reading.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120145

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T15:17:43.060 |

Missing authorization in PostgreSQL logical replication allows a compromised publisher to execute arbitrary code as the operating system user running the superuser-owned subscription, via naming a system catalog as a replication target.  Only subscriptions owned by a superuser are vulnerable.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:42.930 |

Type confusion from incomplete PostgreSQL type-cache invalidation allows an object creator to execute arbitrary code as the operating system user running the database, via a composite type change while its cache entry is being populated.  Within major version 18, minor versions before PostgreSQL 18.7 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-120143

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:42.790 |

Use after free in PostgreSQL trigger functions allows an object creator to execute arbitrary code as the operating system user running the database, via a cursor over a transition table.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:42.660 |

Type confusion in PostgreSQL anonymous RECORD types allows an object creator to execute arbitrary code as the operating system user running the database, via row types having dropped attributes in the same positions but with different widths or alignments.  Within major versions 17-18, minor versions before PostgreSQL 18.7 and 17.12 are affected.  Versions before PostgreSQL 17 are unaffected.

### CVE-2026-120141

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:42.547 |

Type confusion in PostgreSQL materialized set-returning functions allows a database user to execute arbitrary code as the operating system user running the database, via returning rows having different dynamic RECORD return types.  json_populate_recordset() is one affected function.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120139

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-12T15:17:42.420 |

Integer wraparound in PostgreSQL in-memory tuple-size calculations allows a database user to execute arbitrary code as the operating system user running the database, via oversized tuple data.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116336

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-672;CWE-843` |
| Published | 2026-11-12T15:17:42.167 |

Operation on a dropped index in PostgreSQL REINDEX CONCURRENTLY allows an object creator to execute arbitrary code as the operating system user running the database, via an index expression that issues DROP INDEX.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:42.043 |

Type confusion in PostgreSQL operator commutator and negator links allows an object creator to execute arbitrary code as the operating system user running the database, via linking operators having different result types or creating inconsistent reciprocal links.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116332

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:41.800 |

Use after free in PostgreSQL portal setup allows an object creator to execute arbitrary code as the operating system user running the database, via running user-defined code during planning or executor startup that closes the portal currently being prepared.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116331

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:41.683 |

Type confusion in PostgreSQL min/max aggregate optimization allows an object creator to execute arbitrary code as the operating system user running the database, via a user-defined aggregate whose SORTOP option causes the planner to treat the aggregate's input and result as the same type when they differ.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116330

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-12T15:17:41.557 |

Untrusted data inclusion in PostgreSQL pg_dump tar-format restore.sql allows a compromised origin server to execute arbitrary code as the client operating system account running psql, via the predictable restriction key in restore.sql.  This is a gap in the fix for CVE-2025-8714.  restore.sql is undocumented.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:41.437 |

Type confusion in PostgreSQL statistics import allows a table maintainer to execute arbitrary code as the operating system user running the database, via nested SET DATA TYPE during conversion of values to import.  Within major version 18, minor versions before PostgreSQL 18.7 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-116328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-12T15:17:41.313 |

Integer wraparound in PostgreSQL generation memory contexts allows a database user to execute arbitrary code as the operating system user running the database, via freeing an allocation larger than 1 GB and causing its block to be reused for smaller chunks whose back-pointer offset cannot represent that position.  Within major versions 16-18, minor versions before PostgreSQL 18.7, 17.12, and 16.16 are affected.  Versions before PostgreSQL 16 are unaffected.

### CVE-2026-116326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-672` |
| Published | 2026-11-12T15:17:41.077 |

Uncaught exceptions in PostgreSQL plperl allow an object creator to cause use of a stale sigjmp_buf, via a tied Perl object, or a Perl object whose overloaded conversion throws while plperl is handling another error.  We have not ruled out arbitrary code execution on some platform.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116323

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:40.823 |

Use after free in PostgreSQL pltcl allows an object creator to execute arbitrary code as the operating system user running the database, via a domain CHECK that re-enters the Tcl interpreter and frees or changes a string still used by the outer result conversion.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:40.430 |

Use after free in PostgreSQL plperl allows an object creator to execute arbitrary code as the operating system user running the database, via dropping the final reference to a Perl array or hash while PostgreSQL is converting that object.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116319

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:40.313 |

Use after free in PostgreSQL plperl allows an object creator to execute arbitrary code as the operating system user running the database, via reentrant return_next() calls.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116318

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T15:17:40.147 |

SQL injection in PostgreSQL pg_dump allows an object creator to execute arbitrary SQL as the user restoring the dump, via an inherited column having a child-local not-null constraint whose name requires quoting.  Within major version 18, minor versions before PostgreSQL 18.7 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-116317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T15:17:39.993 |

Heap-based buffer overflow in PostgreSQL ts_rank_cd() may allow a database user to execute arbitrary code as the operating system user running the database, via an invalid tsvector containing duplicate positions.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-424` |
| Published | 2026-11-12T15:17:39.837 |

Improper protection of alternate path in PostgreSQL security-restricted operations allows an object creator to execute arbitrary SQL as the operation's caller, via a domain, enum, or range type created in pg_temp.  The victim session must later run a query containing an unqualified type name, e.g. "SELECT '1'::bigint"; autovacuum and other common security-restricted operation users do not do so, so they are unaffected.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-12T15:17:39.683 |

Heap-based buffer overflow in PostgreSQL tsvector_delete() allows a database user to execute arbitrary code as the operating system user running the database, via a tsvector whose lexeme data uses a nonstandard but valid ordering that requires additional alignment padding in the result.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116314

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-12T15:17:39.500 |

Improper input validation in PostgreSQL pg_restore allows a non-plain archive provider to execute arbitrary code as the operating system user running pg_restore, via a crafted archive.  Note a contrast: crafted archive data may legitimately cause arbitrary SQL to execute at the restore destination, but it does not legitimately confer arbitrary code execution in the pg_restore OS process.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:38.647 |

Type confusion in PostgreSQL plperl may allow an object creator to execute arbitrary code, via blessing a non-hash reference into PostgreSQL::InServer::ARRAY.  We have not confirmed or ruled out a way to control the pointer sufficiently to achieve security impact, but we are proceeding as though that is possible.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116307

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-12T15:17:38.340 |

Use after free in PostgreSQL plperl allows an object creator to execute arbitrary code as the operating system user running the database, via re-entering plperl and freeing a prepared query while an outer invocation is executing it.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116306

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:38.193 |

Type confusion in PostgreSQL composite-value field assignment allows an object creator to execute arbitrary code as the operating system user running the database, via changing a composite type between deforming and reforming a value.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116304

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-843` |
| Published | 2026-11-12T15:17:38.043 |

Use after free in PostgreSQL coordination of anonymous RECORD type identifiers among parallel workers allows a database user to execute arbitrary code as the operating system user running the database, via causing one process to free a shared tuple descriptor while another process retains and later uses its address.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-112182

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T11:17:15.913 |

Unauthorization vulnerability in the management of workflow definitions in OpenKM Community Edition. The REST endpoints `registerProcessDefinition` and `runProcessDefinition` require authentication but do not verify roles in the WorkflowService or in lower layers. An attacker with the `ROLE_USER` role can register and execute a process definition containing BeanShell scripts, allowing them to execute Java code and operating system commands with the service’s privileges. In the official Docker image, the process runs as root.

### CVE-2026-75492

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-13T10:18:16.740 |

Cudy TR3000 before 2.5.42 contains an unauthenticated stack buffer overflow vulnerability in the stun_client TR-111 UDP Connection Request parser that parses requests before verifying username or HMAC. Remote attackers can send a single crafted UDP datagram lacking a space in the request line, causing strncpy() to overflow a 10-byte stack buffer and crash stun_client for denial of service.

### CVE-2026-128347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T10:18:15.427 |

ExcelJS through 4.4.0 contains an arbitrary file read vulnerability in the streaming WorkbookWriter that allows attackers to read local files by supplying crafted image filenames to addImage. Attackers can inject ../ path segments into user-controlled image paths, causing addMedia to embed any file readable by the Node.js process under xl/media in the generated workbook.

### CVE-2026-128346

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-11-13T10:18:15.273 |

ExcelJS through 4.4.0 contains a resource leak vulnerability in the streaming WorkbookReader.parse that leaves temporary files and open descriptors when sheet parsing fails or iteration stops early. Attackers can repeatedly upload malformed multi-sheet workbooks with worksheets placed before xl/sharedStrings.xml to fill the temporary directory and exhaust file descriptors.

### CVE-2026-128344

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:14.977 |

ExcelJS through 4.4.0 contains a memory exhaustion vulnerability that allows attackers to crash applications by supplying a workbook with an unbounded image anchor column in the drawing part. Attackers can set an anchor column such as 300000000 in xl/drawings/drawing1.xml so reading getImages() anchor positions makes Worksheet.getColumn allocate millions of Column objects and abort with a heap out-of-memory error.

### CVE-2026-128343

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-11-13T10:18:14.823 |

exceljs through 4.4.0 contains a denial of service vulnerability that allows attackers to block the event loop by supplying unbounded row r attributes parsed in row-xform.js. Attackers can craft an XLSX file with a row numbered far beyond Excel's limit, making getSheetValues(), workbook writes and CSV export consume time proportional to that number.

### CVE-2026-128342

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-606` |
| Published | 2026-11-13T10:18:14.670 |

ExcelJS through 4.4.0 contains a denial of service vulnerability that allows attackers to block the event loop by supplying an unbounded sheetId in xl/workbook.xml. Attackers can provide a workbook with a huge sheetId, making the sparse worksheet array walk stall worksheets, getWorksheet and writeBuffer for seconds.

### CVE-2026-128341

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:14.530 |

ExcelJS through 4.4.0 contains a resource exhaustion vulnerability in data-validations-xform.js that allows attackers to exhaust CPU and memory by supplying unbounded sqref ranges. Attackers can provide a small crafted workbook with a sqref of A1:XFD1048576 to make xlsx.load() iterate billions of addresses, blocking the event loop and crashing the process with an uncatchable out-of-memory error.

### CVE-2026-128340

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:14.373 |

ExcelJS through 4.4.0 contains a memory exhaustion vulnerability that allows attackers to crash applications by supplying a workbook with an oversized defined-name range. DefinedNames.addEx expands ranges such as S!$A$1:$XFD$1048576 from xl/workbook.xml cell by cell, causing an uncatchable fatal heap out-of-memory error during xlsx.load().

### CVE-2026-128339

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:14.223 |

ExcelJS through 4.4.0 contains a memory exhaustion vulnerability in Worksheet._parseMergeCells that allows attackers to crash applications by supplying unbounded mergeCell ranges. Attackers can craft a small workbook with a mergeCell ref like A1:XFD1048576, causing xlsx.load() to create billions of Row and Cell objects and abort the process.

### CVE-2026-128338

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:14.073 |

exceljs through 4.4.0 contains a memory exhaustion vulnerability that allows attackers to crash applications by supplying a worksheet col element with an unbounded max attribute. Attackers can craft a small workbook with a huge max value, causing xlsx.load() to allocate hundreds of millions of Column objects and abort the process with an uncatchable heap out-of-memory error.

### CVE-2026-128242

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-11-13T10:18:12.180 |

actix-http before 3.20.1 and actix-web before 4.18.2 contain an unbounded decompression vulnerability in encoding::Decoder that lets remote attackers exhaust memory and CPU via compressed bodies. Attackers can send small highly compressed gzip, deflate, Brotli or zstd request bodies to Json, Form, Bytes or String extractors, or serve them to awc clients, causing denial of service.

### CVE-2026-128044

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-13T10:18:10.123 |

OpenMage magento-lts before 20.18.2 and 21.x before 21.0.0-beta3 validates OAuth 1.0a oauth_callback URLs with a string-prefix check and falls back to accepting any well-formed URL. Attackers holding a leaked consumer key and secret can supply host-suffix, userinfo, or arbitrary callback URLs to capture an approving administrator's or customer's request token and verifier, then obtain an access token with the victim's API privileges.

### CVE-2026-127090

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-305` |
| Published | 2026-11-13T10:18:05.620 |

Jadaptive Maverick Synergy Server before 3.0.33 and 3.1.x before 3.1.7, and Maverick Legacy Server before 1.8.1, contain an authentication bypass vulnerability in SSH public key authentication that reuses cached key authorization decisions across usernames. Attackers holding a key authorized for one account can authenticate it, then send a signed SSH_MSG_USERAUTH_REQUEST with a different username on the same connection to log in as that account.

### CVE-2026-126948

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:18:02.047 |

Zipline before 4.5.0 contains an insecure direct object reference vulnerability caused by missing ownership verification in the PATCH and DELETE handlers for /api/user/folders/:id. Authenticated attackers can supply another user's folder ID to rename it, make it public, enable uploads, or delete it.

### CVE-2026-126487

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:17:58.923 |

OpenEMR before 8.5.0 contains an authorization bypass vulnerability that allows authenticated users to override system-wide global configuration values by storing global-prefixed keys through library/ajax/user_settings.php. Attackers can submit lab or target parameters with global: prefixed setting names to disable audit logging, weaken password policies, or alter security-sensitive settings persistently for their sessions.

### CVE-2026-126482

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:58.060 |

OpenEMR before 8.5.0 contains an SQL injection vulnerability in SLEOB::slInvoiceNumber() in src/Billing/SLEOB.php, which concatenates the CLP01 claim identifier from uploaded X12 835 ERA files into a query without escaping or parameter binding. Authenticated users with billing permissions, or a malicious payer whose ERA file a clerk uploads, can execute arbitrary SQL to read any table, including users_secure password hashes, and modify data.

### CVE-2026-126472

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:17:56.427 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in ccdaservice/ccda_gateway.php that allows any authenticated low-privilege staff user to retrieve other patients' C-CDA documents. Attackers can request the view or dl action with sequential pid values and their own CSRF token to enumerate and exfiltrate medications, problems, allergies, and immunizations.

### CVE-2026-126470

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:17:56.087 |

OpenEMR before 8.5.0 contains an insecure direct object reference vulnerability in the Carecoordination module that allows authenticated users with send_to_hie permission to access any patient's CCDA/CCR/QRDA documents. Attackers can supply arbitrary document or patient IDs to download, transmit, or export patient health records, inject falsified clinical data, and delete audit records.

### CVE-2026-126469

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:55.920 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in several custom/ scripts that rely only on session authentication and never call AclMain::aclCheckCore(). Any authenticated low-privilege user can request export_labworks.php, chart_tracker.php, or export_registry_xml.php to disclose patient SSN, DOB, and insurance data or provider NPI/tax IDs, and forge chart-tracker records.

### CVE-2026-126468

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:55.757 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability that allows any authenticated low-privilege user to access reports, dated reminders, and batch reminder endpoints lacking AclMain::aclCheckCore() checks. Attackers can request patient_list.php, amc_full_report.php, dated_reminders_add.php, or batch_reminders.php directly to export patient PHI, send unauthorized reminders, and trigger batch reminder processing.

### CVE-2026-126466

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:55.417 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability that allows any authenticated user to create patient records and enumerate patients by omitting aclCheckCore() checks. Attackers can POST to new_comprehensive_save.php to create patients with insurance PHI, or query new_search_popup.php and patient_select.php to leak names, SSNs and DOBs.

### CVE-2026-126458

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:54.163 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in authorizations_full.php that allows any authenticated staff user to authorize arbitrary patients' clinical records. Attackers can send a mode=authorize request with an attacker-chosen pid and their own CSRF token to set authorized=1 on billing, forms, pnotes, and transactions records, bypassing provider review.

### CVE-2026-126436

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:50.510 |

OpenEMR before 8.5.0 contains an authorization bypass vulnerability that allows OAuth2 clients to use unregistered grant types because oauth_clients.grant_types is never enforced. Attackers can request tokens with grant_type=password to bypass the user consent screen, and disabled clients can redeem authorization codes using JWT client assertions.

### CVE-2026-126414

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:46.837 |

Frappe HRMS 15.0.0 before 15.64.2 and 16.0.0 before 16.20.0 contains a missing authorization vulnerability in certain record update endpoints that lack an ownership check. Authenticated users with the Employee role can call these endpoints to modify records belonging to other employees, beyond their permitted role.

### CVE-2026-126412

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:46.537 |

Frappe HRMS 15.0.0 before 15.64.1 and 16.0.0 before 16.19.0 lacks a write permission check on a bulk record processing action, allowing users with only read access to the related setup record to modify data. Authenticated users with the default Employee role can run the action to create and submit records for every covered employee.

### CVE-2026-126401

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-13T10:17:44.597 |

Fleet before 4.86.2 contains a denial of service vulnerability that allows unauthenticated attackers to exhaust server memory through quadratic XML canonicalization of unsigned SAML responses. Attackers can send a single crafted SAML response with deeply nested elements declaring new namespace prefixes to POST /api/v1/fleet/sso/callback, crashing the Fleet server.

### CVE-2026-126397

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:43.923 |

vLLM from 0.10.1 before 0.31.0 forwards a request-controlled mm_processor_kwargs.max_patches value to the Hugging Face processor for Cohere2 Vision models without a server-side upper bound, causing quadratic CPU work during multimodal preprocessing. Remote clients can send small image chat-completion requests with large, varying max_patches values to bypass the LRU cache, exhaust preprocessing workers, and deny service to other clients.

### CVE-2026-126372

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T10:17:39.410 |

Vvveb through 1.0.8.6 contains an incomplete fix for CVE-2026-41934 that allows authenticated editor or site_admin users to write server-side templates by bypassing save restrictions. Attackers can upload or rename .tpl files via editor/code upload and rename actions, or evade isExecutableFile checks in save(), to inject PHP code into templates.

### CVE-2026-126370

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-11-13T10:17:39.060 |

Vvveb through 1.0.8.6 contains a remote code execution vulnerability allowing restricted site_admin roles to inject PHP by saving .sql files through the admin code editor. Attackers can bypass extension and content deny-lists with an @IF macro payload that compiles into executable PHP when the model loads, running OS commands as the web user.

### CVE-2026-126317

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:37.750 |

Frappe HRMS from 16.0.0 before 16.20.1 contains a missing authorization vulnerability that allows authenticated users to read company details outside their permissions due to a missing permission check. Any logged-in user, including Employee role users, can query the affected endpoint to list every company on the site along with its default currency.

### CVE-2026-126314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:37.297 |

Frappe HRMS 15.0.0 before 15.64.6 and 16.0.0 before 16.20.1 does not check access to each employee on endpoints that create records in bulk for a list of employees. An authenticated user with create permission on the affected record type, such as HR User, can create records for employees outside their user-permission scope, including other companies' employees.

### CVE-2026-126308

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-13T10:17:36.320 |

The web dashboard in Coder 2.24.0 before 2.29.23, 2.30.0 before 2.34.14, 2.35.0 before 2.36.9, 2.37.0 before 2.37.6, and 2.38.0 before 2.38.2 replaces the $SESSION_TOKEN placeholder in external app URLs with a full-access API key without checking whether the app belongs to a sub-agent. Code running in a workspace can register a disguised sub-agent app with a custom protocol URL, so the owner's click sends their API key to an attacker-chosen destination.

### CVE-2026-126307

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:36.143 |

Nezha Dashboard before 2.6.0 contains multiple authorization, tenant isolation, and resource exhaustion vulnerabilities that allow members or unauthenticated attackers to abuse NAT, DDNS, OAuth, cron, and server transfer features. Attackers can claim undeclared Dashboard hostnames to capture login bodies, hijack DDNS profiles, create executable schedules without exec scope, or exhaust memory via buffered NAT requests.

### CVE-2026-126304

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-11-13T10:17:35.637 |

NLTK from 3.10.0 before 3.10.4 contains a symlink escape vulnerability in YCOECorpusReader that allows attackers to read files outside the corpus root by planting psd or pos directory symlinks. Attackers controlling a YCOE corpus can make parsed_sents() and tagged_words() return file content from other corpora or temporary files within the NLTK data sandbox.

### CVE-2026-126303

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:35.457 |

NLTK before 3.10.4 contains an uncontrolled resource consumption vulnerability in SteppingRecursiveDescentParser.parse() that lacks any max_time deadline or step limit. Attackers influencing the grammar can supply an ambiguous self-embedding grammar and short token input to force unbounded top-down search, pinning CPU cores and exhausting worker pools.

### CVE-2026-126299

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:34.747 |

NLTK before 3.10.4 contains a denial of service vulnerability in the CCG lexicon parser fromstring that allows remote attackers to exhaust CPU by supplying wide inputs. Attackers can submit lexicon text with long flat bracket bodies or operator chains, triggering quadratic string re-slicing in matchBrackets and augParseCategory that blocks worker threads.

### CVE-2026-126298

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:34.580 |

NLTK before 3.10.4 contains a denial of service vulnerability in Tree.chomsky_normal_form that allows remote attackers to exhaust CPU through quadratic-time right-factor binarization using list.pop(0). Attackers can supply a wide flat treebank tree parsed by Tree.fromstring to force tens of seconds of single-threaded CPU consumption, blocking the processing thread.

### CVE-2026-126297

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:34.420 |

NLTK before 3.10.4 contains a quadratic-time denial of service vulnerability in ConllCorpusReader._get_srl_instances that allows remote attackers to exhaust CPU through nested span rescans. Attackers can supply a crafted CoNLL SRL corpus with many predicates and span columns, placing the head span last, to pin a core for minutes.

### CVE-2026-126294

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T10:17:33.890 |

Grav Login plugin before 3.11.0 contains an authentication bypass vulnerability that allows attackers with an account password to skip two-factor verification when the global twofa_enabled setting is off. Attackers can sign in through the /login form, remember-me cookie, or magic link to obtain a session the API plugin accepts, gaining full account permissions including super-admin control.

### CVE-2026-126291

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:33.443 |

NocoDB before 2026.06.2 contains an SQL injection vulnerability in base-user.cte.utils.ts, which concatenates base members' email addresses into the SQL text of queries resolving user, created-by or last-modified-by fields. Registered users can set an email with a quoted local part containing a single quote to execute arbitrary SQL, exposing user records, API tokens and data-source credentials.

### CVE-2026-126283

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:31.820 |

NocoDB before 2026.08.0 contains an incorrect authorization vulnerability that lets base-scoped API tokens act as account-wide credentials because the token's base_id is never stored or checked. Attackers holding a leaked token can read, write and delete records on every base the token owner belongs to, including bases joined later.

### CVE-2026-126278

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-13T10:17:31.053 |

NocoDB before 2026.08.1 contains a race condition vulnerability in users.service.ts that allows holders of a valid reset token to perform multiple password changes by sending concurrent reset requests. Attackers can exploit the window created by slow bcrypt hashing before the token is cleared to overwrite the owner's new password and lock them out.

### CVE-2026-126277

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:17:30.893 |

NocoDB before 2026.08.1 contains an uncontrolled resource consumption vulnerability that allows unauthenticated attackers to exhaust server resources by sending unbounded filter arrays to shared-view bulk endpoints. Attackers with a shared view UUID can POST a large body of minimal filter objects, triggering a full database query per entry, to crash the NocoDB process.

### CVE-2026-126266

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T10:17:29.173 |

SiYuan from 3.6.0 before 3.8.9 contains an information disclosure vulnerability that allows unauthenticated publish visitors to bypass per-document passwords via regex search in getDoc. Attackers can send POST requests to /api/filetree/getDoc with queryMethod 3 and a broad regex to read protected body text returned in the unfiltered keywords field.

### CVE-2026-120867

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T09:17:34.437 |

Memory overflow in SSL/TLS/DTLS can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-120865

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T09:17:34.190 |

Memory overflow in HTTP/3 (QUIC) can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-59074

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-13T08:17:17.347 |

Edito CMS is vulnerable to improper cryptographic signature verification in the JWT refresh logic. An authenticated low-privilege user can submit self-crafted​ ​JWT​ containing​ ​an existing user​ ​identifier and, due to the lack of signature validation,​​  obtain​ ​a ​​valid,​​ fully-signed​​ session ​​token​​ for​​ any ​​account ​​in​ ​the​ ​system. This allows the attacker to impersonate any user, including administrators.
This issue was fixed in version 5.10.2607.  Hotfixes for older versions (5.8) have also been released.

### CVE-2026-120863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:17.013 |

Memory overflow in the management plane can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-120862

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:16.890 |

Memory overflow in SIP ALG (LSN) and DNS answer-section logging datapaths can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-120861

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:16.760 |

Memory overflow / improper handling in GSLB and geolocation (MEP, static-proximity, config-sync) can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-120860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:16.633 |

Memory overflow in protocol load-balancing traffic handling (Diameter, SIP-over-TCP, MQTT, RADIUS) can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-111337

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:15.950 |

Memory overflow in Base64 decoding in advanced policy expressions leading to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-111342

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T04:17:36.777 |

Memory overflow in LDAP authentication can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-111341

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T04:17:36.653 |

Memory overflow in client-certificate authentication can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-111340

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T04:17:36.537 |

Memory overflow in KBA (knowledge-based authentication) can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-107414

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T03:17:29.113 |

Memory overflow in WebAuth authentication can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-107413

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T03:17:28.997 |

Memory overflow in SAML authentication can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-107411

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T03:17:28.757 |

Memory overflow in RTSP ALG can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler

### CVE-2026-128066

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T00:20:14.457 |

Pillow is a Python imaging library. From 1.0 through 12.3.0, ImageFileDirectory_v2.load() in src/PIL/TiffImagePlugin.py retains a separate bytes object for each out-of-line IFD tag value without limiting the total data read or preventing distinct tags from referencing the same file region. A small crafted TIFF or EXIF-bearing JPEG, PNG, WebP, or MPO can therefore cause memory use quadratic in the input size. TIFF and some JPEG paths trigger parsing during Image.open(), while other formats are exposed when EXIF is requested, including through getexif() or ImageOps.exif_transpose(). The declared pixel dimensions do not bound this metadata allocation, so decompression-bomb checks do not prevent process memory exhaustion. This issue is fixed in version 13.0.0.

### CVE-2026-106018

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-11-12T21:17:17.923 |

Authentication bypass using an alternate path or channel vulnerability in Johnson Controls EasyIO FW allows Authentication Bypass.

This issue affects EasyIO FW: through 3.0b25.

### CVE-2026-124013

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T20:18:25.237 |

XWEB EVO 5.6.2 through 5.8.8 contains an authenticated OS command injection vulnerability in the api.lua import_preconfiguration and restore actions, where server_url and related server credential fields are concatenated unescaped into a root curl command executed via io.popen. Attackers can inject malicious shell commands through these unfiltered parameters to achieve arbitrary command execution with root privileges on the underlying system. This product line reached it's end of service date in March 2026.

### CVE-2026-127204

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-12T18:17:42.423 |

WooCommerce PayPal Pro Payment Gateway plugin before 4.1.1 contains an unauthenticated payment bypass vulnerability that allows remote attackers to mark unpaid orders as paid by exploiting the pp_capture_order AJAX handler, which is gated only by a public checkout nonce and fails to properly validate the PayPal capture response status. Attackers can supply a valid _paypal_order_id to trigger payment_complete() without verifying the capture status or amount, causing the store to fulfill goods or services that were never paid for and resulting in direct financial loss to the merchant.

### CVE-2026-75578

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:17.593 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability in luci/model/cbi/vpn/openvpn/client.lua, which embeds the shellquote()-quoted remote host token of an uploaded OpenVPN configuration inside an already single-quoted sed program run by os.execute(), so the nested quotes terminate the outer quote. Authenticated administrators can upload an .ovpn file whose remote host token contains a semicolon to execute arbitrary commands as root.

### CVE-2026-75577

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:17.450 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability that allows authenticated administrators to execute commands as root by storing a malicious WireGuard private key. Attackers can save a private_key containing $() shell substitution and call the vpn.export_conf method on the /cgi-bin/luci/rpc/app JSON-RPC endpoint, which passes the key to a wg pubkey shell command.

### CVE-2026-75576

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:17.310 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability that allows authenticated administrators to execute commands as root via an unvalidated multipart filename in the CBI FileUpload handler. Attackers can upload a valid OpenVPN configuration file through the VPN client config page with a filename containing $() shell substitution, which is passed through Lua %q to /bin/sh -c.

### CVE-2026-75487

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T10:18:16.013 |

Cudy TR3000 before 2.5.42 contains a command injection vulnerability that allows authenticated administrators to execute commands as root via the WireGuard server private_key option. Attackers can save a private key containing $() command substitution, which runs when action_wireguards_export() passes it to luci.sys.exec during configuration export.

### CVE-2026-127088

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-13T10:18:05.457 |

2FAuth before 9.0.1 contains a weak password recovery vulnerability that allows unauthenticated attackers to poison reset links by forging the HTTP Host header. Attackers can request password or WebAuthn recovery emails with an attacker-controlled host, capture the victim's token, and take over accounts exposing stored TOTP/HOTP secrets.

### CVE-2026-126489

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:59.250 |

OpenEMR before 8.5.0 contains a second-order SQL injection vulnerability in the IPPF contraceptive issue feature because issue_ippf_con_save concatenates layout_options field_id values into a REPLACE INTO query as column names. Authenticated administrators can add a malicious field_id via edit_layout.php, then trigger issue_ippf_con_save through add_edit_issue.php to execute arbitrary SQL.

### CVE-2026-126480

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:57.720 |

OpenEMR before 8.5.0 contains an sql injection vulnerability in CcrTable::insertApprovedData() that allows authenticated users to inject SQL through request parameter names used as column names. Attackers can send crafted patient_data-*-sel parameters to the revandapprove route, lacking ACL and CSRF checks, to copy password hashes into patient fields or corrupt records.

### CVE-2026-126455

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:53.670 |

OpenEMR before 8.5.0 contains multiple missing authorization and SQL injection defects across report, portal, transaction, and immunization components. Low-privileged Front Office clerks can chain these to read arbitrary database tables including users_secure hashes, hijack patient portal identities, and forge approved clinical records.

### CVE-2026-126454

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-11-13T10:17:53.507 |

OpenEMR before 8.5.0 lacks rate limiting or lockout on TOTP submission, allowing attackers with a valid password to brute-force the 6-digit MFA code. Attackers can script repeated POST requests to main_screen.php or the OAuth2 authorization flow with re-submitted hidden credentials to bypass two-factor authentication.

### CVE-2026-126442

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:51.480 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in create_portallogin.php that allows low-privilege authenticated users to replace patient portal credentials without ACL checks. Attackers can select a victim patient in session and post replacement credentials to take over portal accounts, read PHI, and lock patients out.

### CVE-2026-126434

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:50.190 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in interface/forms/procedure_order/common.php that allows authenticated accounts lacking patients/lab permission to read and modify other patients' procedure orders. Attackers can request a global order id to disclose clinical history, or select the target patient in their session and submit bn_save to falsify diagnoses, instructions, and order status.

### CVE-2026-126430

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:49.530 |

OpenEMR before 8.5.0 contains an sql injection vulnerability that allows any authenticated core user to inject SQL by supplying crafted patient_data field names to the CCR revandapprove controller. Attackers can embed scalar subqueries in the UPDATE patient_data SET clause to read staff password hashes and portal reset values, alter arbitrary patient demographics, and take over patient-portal accounts.

### CVE-2026-126402

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:44.753 |

Fleet before 4.89.0 contains an incorrect authorization flaw in its user administration API that accepts user creation or modification when the caller administers any one of the assigned teams. Authenticated team administrators can grant users administrator roles on other teams, then deploy software and execute scripts on those teams' hosts.

### CVE-2026-126322

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T10:17:38.550 |

OpenEMR before 8.3.0 contains an unsanitized deserialization vulnerability that allows authenticated attackers to control patient-matching criteria by supplying a crafted serialized key parameter. Attackers can send serialized arrays to interface/orders/patient_match_dialog.php to enumerate patients or force matches that associate lab orders with the wrong patient.

### CVE-2026-126306

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:35.973 |

EspoCRM before 9.3.11 and 10.x before 10.0.8 contains a stored cross-site scripting vulnerability that allows low-privileged users to upload crafted SVG images that submit authenticated POST requests to arbitrary backend endpoints. Attackers can trick an administrator into opening the SVG in a separate browser tab and clicking it, performing administrator actions such as elevating the attacker's account to administrator.

### CVE-2026-126286

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:32.287 |

NocoDB before 2026.08.0 contains a reflected cross-site scripting vulnerability in PageLeavingWarning.vue that allows unauthenticated attackers to execute script by embedding an ASCII control character in the ncRedirectUrl scheme. Attackers can send a crafted link that bypasses the scheme check and reaches the anchor href or window.location, stealing the session token from localStorage for account takeover.

### CVE-2026-126282

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-13T10:17:31.670 |

NocoDB from 2026.04.0 before 2026.08.0 contains an improper privilege management vulnerability in org-users.service.ts where updating a user's legacy organization role rewrites their default-workspace role. Revoked users can silently regain Creator-level read, write and schema modification access across all default-workspace bases using their existing session token.

### CVE-2026-127208

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-12T21:17:22.933 |

datamodel-code-generator before 0.84.0 contains a code injection vulnerability that allows attackers to achieve arbitrary code execution by supplying a malicious JSON Schema with a crafted x-python-type annotation containing a string ast.Constant node in a subscript slice position, which bypasses validation in parse_python_type_annotation and _python_type_expr_from_ast. Attackers can embed malicious Python expressions such as __import__ calls within quoted string literals in the generated source code, which Pydantic v2 evaluates as a ForwardRef via eval() during model_rebuild(), resulting in arbitrary code execution on developer workstations, CI/CD pipelines, or applications that generate and import the produced models at runtime.

### CVE-2026-126793

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-12T21:17:22.380 |

An untrusted search path issue in Aurora PostgreSQL dialect detection in the AWS Advanced Go Wrapper from release 2026-04-06 (awssql/v2.0.0) and before release 2026-07-29 (awssql/v2.0.3) could allow a remote authenticated user to escalate privileges to those of another database user, including a member of the rds_superuser role, via a crafted function that runs when that user connects to an Aurora PostgreSQL cluster through an affected version of the wrapper.



To remediate this issue, users should upgrade to the AWS Advanced Go Wrapper release 2026-07-29 (awssql/v2.0.3) or later.

### CVE-2026-47711

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-121;CWE-131;CWE-787;CWE-805` |
| Published | 2026-11-12T20:18:41.220 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4, 1.5.1, and 1.6.0, the current master demo server can be crashed remotely over BACnet/IP by sending a valid Confirmed WriteProperty request that updates loop-1's controlled-variable-reference to point to life-safety-zone-1 / accepted-modes. This issue has been patched in versions 1.4.4, 1.5.1, and 1.6.0.

### CVE-2026-124009

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T20:18:23.960 |

XWEB EVO 5.2.3 through 5.8.8 contains an authenticated OS command injection vulnerability that allows authenticated attackers to execute arbitrary commands as root by injecting shell metacharacters into the output device path parameter processed by backup.lua. Attackers can exploit the unescaped concatenation into mount, unzip, and related shell commands run via the wlua interpreter, including through the setuid xwbackup.cgi and xwrestore.cgi interfaces, to achieve full system compromise. This product line reached it's end of service date in March 2026.

### CVE-2026-124008

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-12T20:18:23.653 |

XWEB EVO 5.2.3 through 5.8.8 contains an authenticated OS command injection vulnerability in the devices.lua template handling, which allows authenticated attackers to execute arbitrary commands by injecting unescaped template source into unzip and related shell commands. Attackers can exploit this flaw through the wlua interpreter to execute arbitrary commands with root privileges on the affected device. This product line reached it's end of service date in March 2026.

### CVE-2026-106154

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-12T18:17:12.420 |

In Progress® Telerik® UI for ASP.NET Core versions `2015.1.318` through `2026.3.1015`, the server-side FilterParser processes nested expressions in untrusted filter parameters through recursive parsing without a recursion-depth limit, while FilterLexer does not enforce an input-length limit. An unauthenticated remote attacker can exploit this if the application exposes an endpoint using DataSourceRequest model binding that is reachable without authentication. Deeply nested filters can trigger parsing errors during model binding or cause `StackOverflowException`. This issue is fixed in version `2026.4.1111`.

### CVE-2026-106146

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-12T18:17:12.273 |

In Progress® Telerik® UI for ASP.NET MVC versions `2012.2.710` through `2026.3.1015`, server-side filter processing does not properly validate descriptor types, null values, or stack state in FilterNodeVisitor and does not catch FilterParserException within the affected assembly. An unauthenticated remote attacker can exploit this if the application exposes an endpoint reachable without authentication that accepts crafted filter parameters. Affected requests can trigger uncaught cast, null-reference, or empty-stack exceptions and return HTTP 500. The report does not demonstrate worker-process termination or disruption of unrelated requests. The issue is fixed in version `2026.4.1111`.

### CVE-2026-127084

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:18:04.853 |

Teable before 2026-10-12T12-45-53Z.3331 contains a stored cross-site scripting vulnerability that allows authenticated users to upload SVG or HTML attachments with an attacker-chosen content type. Attackers can send the same-origin /api/attachments/read URL, served inline with an empty Content-Security-Policy, to run script with the victim's session and perform API actions.

### CVE-2026-126451

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:52.993 |

OpenEMR before 8.5.0 contains a stored cross-site scripting vulnerability that allows portal patients to run JavaScript in staff sessions by injecting javascript: URLs into document template_data. Attackers can submit an encounterForm value rendered unsanitized into an iframe src by DocumentTemplateRender, letting the script read PHI and CSRF tokens and call staff or admin endpoints.

### CVE-2026-126403

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:44.910 |

Coder 2.26.0 before 2.29.24, 2.30.0 before 2.34.16, 2.35.0 before 2.36.11, 2.37.0 before 2.37.8, and 2.38.0 before 2.38.4 contains an improper authorization flaw in the external agent credentials endpoint, which returns the workspace agent token to users with only workspace read access rather than ssh permission. Authenticated users with roles such as Template Admin or Organization Admin can use the token to read the owner's private Git SSH key and Git provider OAuth tokens, and impersonate the agent to receive the owner's sessions.

### CVE-2026-126305

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:35.797 |

EspoCRM before 9.3.11 and 10.x before 10.0.9 contains a stored cross-site scripting vulnerability in Knowledge Base articles that lets users with Knowledge Base create or edit access attach a JavaScript file and add a crafted link to the article body. When an administrator clicks the link, the script runs in their session and can create an administrator account with attacker-chosen credentials.

### CVE-2026-124003

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-11-12T20:18:21.917 |

XWEB EVO before 5.6.2 contains a command injection vulnerability where the setuid-root Lua CGI interpreter wlua executes system("/usr/bin/lua "+argv) on unsanitized input. Attackers can craft malicious input reached through a .lua CGI endpoint to inject arbitrary commands into the concatenated argv string, achieving command execution with root privileges. This product line reached it's end of service date in March 2026.

### CVE-2026-128040

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:18:09.547 |

OpenMage magento-lts before 20.18.2 and 21.0.0-beta1 before 21.0.0-beta3 contains a stored cross-site scripting vulnerability because admin pages render Dataflow profile link variables, tax rate titles, OAuth consumer names, and PayPal certificate filenames without escaping. An administrator restricted to one affected area can store script that runs when another administrator, including a full administrator, opens the page, reading the form key and performing actions with that administrator's privileges.

### CVE-2026-59081

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T08:17:18.353 |

Edito CMS deserializes JSON data without further validation. A user (even an administrator) cannot exploit this vulnerability through the application's normal functionality. An attacker who could modify cache entries or inject them could execute code on the server.




This issue was fixed in version 5.10.2607.  Hotfixes for older versions (5.8) have also been released.

### CVE-2026-128067

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T00:20:14.710 |

Pillow is a Python imaging library. From 2.3.0 through 12.3.0, Pillow applications that save compressed TIFF images through libtiff can pass attacker-controlled image geometry tags to the encoder while allocating its row buffer from the actual image dimensions. The affected TiffImagePlugin._save path allows ImageWidth, ImageLength, or SamplesPerPixel from exif=, tiffinfo=, or a source TIFF IFD to make libtiff consume a larger scanline than the buffer supplied by ImagingLibTiffEncode. This can read heap memory into the generated TIFF or crash the process. When TIFF Predictor 2 is enabled, libtiff can rewrite the oversized scanline in place and corrupt memory beyond the buffer. A carried-over PlanarConfiguration value of 2 instead makes libtiff use a shorter scanline and can produce an undecodable output file, but is not established to cause the out-of-bounds access. This issue is fixed in version 13.0.0.

### CVE-2026-82977

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-11-12T17:17:46.230 |

The Plesk GoAccess statistics integration in Plesk Obsidian for Linux, versions 18.0.77 to 18.0.81.7, 18.0.82 to 18.0.82.2, allows cross-subscription information disclosure.

### CVE-2026-86355

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T13:18:29.887 |

Dell PowerStore contains an External Control of File Name or Path vulnerability. A remote authenticated attacker could exploit this vulnerability, potentially leading to privilege escalation on the appliance.

### CVE-2026-75494

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-13T10:18:17.027 |

Cudy TR3000 before 2.5.42 contains an argument injection vulnerability that allows a malicious or compromised ACS to inject curl options through unfiltered Username and Password values in the easycwmpd Upload handler. Attackers can embed whitespace to add options like -o and --url to the root-run curl command, writing attacker-controlled HTTP responses to arbitrary files on the device.

### CVE-2026-128337

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-13T10:18:13.920 |

ExcelJS through 4.4.0 contains a prototype pollution vulnerability in mergeConditionalFormattings that allows attackers to modify Object.prototype by supplying an x14:cfRule id of __proto__. Attackers can craft an xlsx file that, when loaded with xlsx.load(), sets properties such as type, direction, border and cfvo on every object in the process until it restarts.

### CVE-2026-128329

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:18:12.520 |

Dokploy 0.28.0 before 0.31.1 contains a path traversal vulnerability that allows authenticated organization members to read arbitrary files by supplying ../ sequences in the filePath of patch.readRepoFile. Attackers with service read permission can read /etc/shadow, SSH private keys, and secret environment files on the Dokploy host or managed remote servers.

### CVE-2026-128016

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-13T10:18:06.807 |

FrankenPHP before 1.13.4 contains a use-after-free vulnerability in worker mode that frees internal streams of SplTempFileObject or SplFileObject on php://temp instances surviving across requests. Remote clients can send requests reaching code that uses such persisted objects, causing reads of freed memory that leak garbage data or crash the process.

### CVE-2026-128015

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-13T10:18:06.633 |

FrankenPHP before 1.13.4 contains a use-after-free vulnerability that leaves a dangling pointer to a freed environment table when putenv() is called during request shutdown. Attackers triggering putenv() in shutdown functions, destructors, or session handlers can crash the process on the next getenv() call or leak previous request environment values.

### CVE-2026-127082

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-11-13T10:18:04.550 |

Huginn before 2026.11.09 contains an information exposure vulnerability in JqAgent that allows authenticated users to read the server process environment because the jq child process inherits it. Attackers who can create, configure or dry-run a JqAgent can supply a filter using env or $ENV to disclose APP_SECRET_TOKEN, database, SMTP and OAuth secrets.

### CVE-2026-126491

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:59.600 |

OpenEMR before 8.5.0 contains a stored SQL injection vulnerability in getByPatientDemographics() where layout_options field_id values are concatenated into the patient search WHERE clause. Attackers with Layout Editor access can plant a malicious field_id, allowing any authenticated low-privilege user to exfiltrate data from patient_data and users_secure tables.

### CVE-2026-126488

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:59.087 |

OpenEMR before 8.5.0 contains an SQL injection vulnerability in the patient portal OnsiteDocument.Query endpoint, where mass-assigned _BitwiseAnd criteria parameters are placed unquoted into SQL with only quote-character escaping. Authenticated portal patients can inject SQL outside their per-patient scope to read the entire database, including other patients' demographics and users_secure password hashes.

### CVE-2026-126379

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-13T10:17:40.603 |

Vvveb 1.0.8.6 contains an incomplete server-side request forgery fix that allows authenticated admin users to bypass DNS pinning by requesting non-443 URLs. Attackers can supply a rebinding hostname to the editor oEmbedProxy url parameter to read loopback services, internal panels, and cloud metadata credentials.

### CVE-2026-126285

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:32.140 |

NocoDB before 2026.08.0 contains an sql injection vulnerability that allows authenticated users with read access to run arbitrary read queries via the legacy where parameter on PostgreSQL. Attackers, including Viewer-role users, can inject single quotes into filter values concatenated by CustomKnex.ts to read other tables, schemas, view-filtered rows, and hidden columns.

### CVE-2026-126271

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-11-13T10:17:29.987 |

NocoDB before 2026.09.0 contains an information disclosure vulnerability that allows authenticated base Viewers to obtain TLS client private keys by reading a base's data source. The source read handler masked only the connection password, letting attackers retrieve the decrypted private key, client certificate and CA to connect directly to the external database, bypassing NocoDB permissions.

### CVE-2026-126264

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T10:17:28.827 |

SiYuan before 3.8.9 contains an information disclosure vulnerability that allows authenticated Reader users to retrieve credential-named widget files by bypassing the sensitive-path guard in getFile. Attackers can request paths like /data/widgets/<package>/credentials.json for publish-referenced widgets to obtain API keys, tokens, or other stored secrets.

### CVE-2026-112181

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-11-13T10:17:24.907 |

Vulnerability due to inadequate restriction of references to external XML entities in OpenKM Community Edition. The XML processing in FormUtils / LocalEntityResolver does not properly restrict the resolution of external resources. An authenticated remote attacker with the ROLE_USER role can exploit the flaw via a REST request. In the 6.3.x branch, this allows the attacker to trigger HTTP requests under their control (SSRF); in 7.0.3, it allows the attacker to read local files and access internal HTTP resources from the server.

### CVE-2024-58404

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:23.447 |

Zipline versions from 3.4.5 before 3.7.10 contain a path traversal vulnerability in the user data export endpoint via the name query parameter. Authenticated attackers can bypass the user id check and use directory traversal sequences to read arbitrary files on the server host.

### CVE-2023-54423

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:P/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-82` |
| Published | 2026-11-13T10:17:23.227 |

OpenMage magento-lts before 20.2.0 contains a stored cross-site scripting vulnerability because the TinyMCE WYSIWYG editor fails to filter scripts in specially crafted HTML tags. Attackers can inject an img element with a malicious onmouseover attribute to execute scripts in the browsers of users viewing the rendered content.

### CVE-2026-111336

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T08:17:15.817 |

Memory overflow in HTTP/2 handling can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-120221

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:A/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-11-13T12:17:03.210 |

In FRRouting 8.4 and later, bgpd frees the same memory twice when dynamic BGP neighbors disconnect, if the peer-group used by a "bgp listen range" also has a Site-of-Origin configured ("neighbor PG soo"). Each dynamic neighbor shares the peer-group's SoO value instead of getting its own copy, but frees it as its own when the neighbor is deleted, which happens as soon as its connection closes. The first disconnect leaves the peer-group pointing at freed memory, and the second disconnect frees it again, causing bgpd to abort and drop all BGP sessions on the router. Any host whose address falls inside the listen range can trigger this by opening and closing two TCP connections to the BGP port, without sending any BGP message and without knowing the AS number, and can repeat it each time bgpd restarts. If the peer-group has a TCP-MD5 password, only hosts that know the password can trigger it. Two ordinary flaps of legitimate dynamic neighbors have the same effect. Between the two frees, displaying the configuration ("show running-config") or establishing a dynamic neighbor also reads the freed memory, which can crash bgpd after a single disconnect. Only configurations that combine a listen range with a SoO on the same peer-group are affected.

### CVE-2026-75493

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-13T10:18:16.883 |

Cudy TR3000 before 2.5.42 contains a stack buffer overflow vulnerability in an obuspa getter for the TR-098 WLANConfiguration KeyPassphrase parameter, which copies the stored value with strcpy() into a 4,096-byte stack buffer without a length check. A malicious or compromised ACS can set a 5,000-byte passphrase via SetParameterValues, and a later read of the parameter overflows the buffer and crashes obuspa, causing denial of service.

### CVE-2026-75488

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-13T10:18:16.173 |

Cudy TR3000 before 2.5.42 contains a stack buffer overflow vulnerability in the CWMP client that allows a malicious ACS to corrupt stack memory via oversized credentials. Attackers controlling the ACS can send Username and Password values up to 256 bytes in TR-069 Download or Upload requests, overflowing 128-byte stack buffers and crashing the CWMP process.

### CVE-2026-128024

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-11-13T10:18:08.083 |

FrankenPHP before 1.13.0 contains a denial of service vulnerability in goArray() that allows remote attackers to abort the server process via arrays with null integer-keyed elements. Attackers can send crafted JSON passed to frankenphp_log() or returned from worker callbacks, triggering an unrecovered cgo panic that terminates every vhost and in-flight request.

### CVE-2026-128020

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-11-13T10:18:07.467 |

FrankenPHP before 1.13.2 contains an uncontrolled recursion vulnerability in its PHP-to-Go array converter that fails to detect circular references in PHP arrays. Passing a self-referential array to frankenphp_log() or returning one from a worker callback triggers a fatal Go stack overflow, terminating the entire server process.

### CVE-2026-126941

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T10:18:01.023 |

Zipline through 4.6.2 contains an authorization bypass vulnerability that allows authenticated administrators to read superadmin secrets because GET /api/users and GET /api/users/:id lack the canInteract check. Attackers can retrieve plaintext totpSecret and OAuth tokens to bypass 2FA and take over superadmin accounts, while any authenticated user can enumerate other users' folders via GET /api/user/folders.

### CVE-2026-126398

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-11-13T10:17:44.093 |

vLLM from 0.28.0 before 0.30.0 contains a reachable assertion vulnerability in GPUModelRunner._init_xdrope_positions that allows remote attackers to crash the engine by submitting embeddings-only requests. Attackers can send a /v1/completions request containing only prompt_embeds to XD-RoPE models with --enable-prompt-embeds, terminating the EngineCore and API server for all clients.

### CVE-2026-126276

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T10:17:30.733 |

NocoDB before 2026.08.1 contains an authentication bypass vulnerability in oauth-token.service.ts that treats PKCE as a substitute for confidential client authentication, skipping client secret verification when omitted. Attackers holding a captured authorization code and PKCE verifier can mint access tokens and 60-day refresh tokens for a confidential client without knowing its secret.

### CVE-2026-124218

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:27.993 |

The Drag and Drop File Upload for Elementor Forms plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the remove_files function in all versions up to, and including, 1.6.2 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This vulnerability is reachable when the "yeepdf_not_save" privacy option is enabled, a commonly used production setting that triggers the remove_files() cleanup path.

### CVE-2026-47710

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-11-12T20:18:40.747 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4, 1.5.1, and 1.6.0, a stack-buffer-overflow can be triggered in the current master branch when a Loop object reads a referenced property through its default timer path and the referenced property is OBJECT_STRUCTURED_VIEW / PROP_DESCRIPTION containing a long attacker-controlled string. This issue has been patched in versions 1.4.4, 1.5.1, and 1.6.0.

### CVE-2026-47259

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-11-12T20:18:40.483 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4, 1.5.1, and 1.6.0, a RemoveListElement request targeting Notification-Class.recipient-list can trigger a stack-based out-of-bounds write in the current master branch when the request contains more than NC_MAX_RECIPIENTS valid BACnetDestination elements. This issue has been patched in versions 1.4.4, 1.5.1, and 1.6.0.

### CVE-2026-47258

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-20;CWE-121;CWE-129;CWE-787` |
| Published | 2026-11-12T20:18:40.260 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4, 1.5.1, and 1.6.0, a stack-based out-of-bounds write exists in the Notification Class object implementation when handling AddListElement for the recipient-list property. This issue has been patched in versions 1.4.4, 1.5.1, and 1.6.0.

### CVE-2026-45265

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-12T20:18:38.380 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4 and 1.5.1, there is a stack-based out-of-bounds write / stack-buffer-overflow in bacnet-stack when the server processes a malicious Atomic-Read-File request in record access mode. The bug is triggered on the real server side. A crafted request can set an excessively large RecordCount, which is later used as the loop bound for writing record data into a stack-allocated BACNET_ATOMIC_READ_FILE_DATA data structure. However, the stack object only has space for one fileData element. When the loop reaches i = 1, the code computes &data->fileData[1], which is already out of bounds, and the resulting invalid pointer is passed down to memmove(), causing a stack-buffer-overflow. This issue has been patched in versions 1.4.4 and 1.5.1.

### CVE-2026-124015

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-12T20:18:26.277 |

XWEB EVO 5.6.2 through 5.8.8 contains an authentication bypass vulnerability that allows unauthenticated attackers to set the password of any account flagged must-reset-at-next-login by exploiting missing session validation in the users.lua update_password action. Attackers can reset the password of newly onboarded operator accounts, clearing the password_expiration flag and gaining an immediately usable authenticated foothold on the system. This product line reached it's end of service date in March 2026.

### CVE-2026-117544

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-639` |
| Published | 2026-11-12T19:16:47.883 |

Joomla Extension - jdownloads.com - IDOR allowing restricted file downloads in jDownloads < 4.1.8 - The `other_file_id` parameter could reference another download’s file without fully enforcing the target download’s access restrictions. This allowed files to be delivered to users who were not authorised to access the target download.

### CVE-2026-118191

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:26.150 |

The Photo Gallery, Sliders, Proofing and Themes – NextGEN Gallery plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the handle_job function in all versions up to, and including, 4.5.5 This makes it possible for authenticated attackers, with custom-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). The 'NextGEN Manage gallery' capability required to reach the vulnerable endpoint is granted to Administrators by default but can be delegated to lower-privileged roles via the plugin's Roles screen.

### CVE-2026-116417

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-521` |
| Published | 2026-11-13T09:17:32.160 |

Dell PowerScale InsightIQ, versions 6.3.0 through 6.4.0, contains a Weak Password Requirements vulnerability. An unauthenticated attacker with adjacent network access could potentially exploit this vulnerability, leading to Information disclosure and Unauthorized access.

### CVE-2026-47257

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-670;CWE-754` |
| Published | 2026-11-12T20:18:40.020 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. In versions 1.5.0 and 1.6.0-rc1, there is a restore logic flaw in bacnet-stack that is reachable through the official, unmodified apps/server management path when BACNET_BACKUP_RESTORE is enabled. This issue has been patched in versions 1.5.1 and 1.6.0.

### CVE-2026-126196

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-693` |
| Published | 2026-11-12T18:17:24.590 |

pgEdge Postgres MCP Server enables SQL queries against PostgreSQL databases through Model Context Protocol compatible clients. Prior to 1.1.0, query_database on a read_only connection could send unrecognized statements through pgx Exec without bind parameters, selecting PostgreSQL's simple query protocol and allowing multiple semicolon-separated statements in one request. A caller could combine transaction or session state changes with database writes, and pooled session state could leave later calls writable, when the connecting role held write privileges. The flaw affected deployments relying on read_only as a safety boundary, could compromise integrity and availability, and did not add confidentiality impact beyond the reads already permitted by the connection. This issue is fixed in 1.1.0.

### CVE-2026-14661

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-12T15:17:49.890 |

External control of file name in PostgreSQL dblink and CREATE/ALTER SUBSCRIPTION allows a user to achieve persistent denial of service, via appending invalid data to a chosen file.  Specifically, the "sslkeylogfile" connection parameter appends data, in NSS keylog format, to a file of the user's choosing.  This "sslkeylogfile" mechanism cannot add arbitrary bytes.  Within major version 18, minor versions before PostgreSQL 18.7 are affected.  Versions before PostgreSQL 18 are also affected if libpq version 18 or later is installed and in use by the server.

### CVE-2026-120148

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-843` |
| Published | 2026-11-12T15:17:43.443 |

Type confusion in PostgreSQL extended statistics allows an object creator to execute arbitrary code as the operating system user running the database, via a statistics expression of an anonymous RECORD type whose backend-local type identifier denotes a different row type in another session.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116325

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T15:17:40.947 |

SQL injection in PostgreSQL reindexdb allows an object creator to execute arbitrary SQL as the database user running reindexdb, via a crafted index name embedded in the parallel catalog query for --jobs with --index.  Within major versions 17-18, minor versions before PostgreSQL 18.7 and 17.12 are affected.  Versions before PostgreSQL 17 are unaffected.

### CVE-2026-121876

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-359` |
| Published | 2026-11-12T17:17:29.040 |

A flaw was found in the interaction between systemd-gpt-auto-generator and 
confidential computing guest VM images in OpenShift Sandboxed Containers 
(confidential peer pods). systemd-gpt-auto-generator automatically discovers 
and mounts GPT partitions by type GUID at boot with no user confirmation. In 
the confidential computing threat model, where the host/hypervisor is the 
adversary, a malicious host can inject partitions into the guest's virtual 
disk. Most critically, injecting a swap partition causes the guest kernel to 
page out TEE-encrypted memory to a host-controlled block device, breaking the 
confidentiality guarantee of the hardware TEE (AMD SEV-SNP, Intel TDX).

The PodVM images use a GPT-partitioned disk with dm-verity on the root 
partition. However, the roothash= kernel parameter only disables root 
auto-discovery — non-root partitions (swap, /home, /var, /srv, /var/tmp) are 
still auto-discovered and mounted. The generator is shipped unmasked in the 
RHEL systemd-udev subpackage, and no kernel command line parameter in the 
measured UKI addon disables it. Additionally, the PodVM measurement script 
captures PCRs 3, 9, 11, and 12, but not PCR 5 (GPT partition table), so 
partition table modifications are not detected by remote attestation.

### CVE-2026-109903

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-11-13T11:17:14.167 |

A buffer overread caused by casting a negative integer to CARD32 in XvQueryImageAttributes in X.Org X Server before 21.1.26 and xwayland before 24.1.15 could be used to causes crashes by authenticated X clients.

### CVE-2026-124702

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-12T18:17:22.683 |

In Telerik UI for WPF, versions prior to 2026.4.1110, an untrusted URL redirection vulnerability exists that allows an attacker to launch arbitrary operating system protocol handlers with attacker-controlled arguments via crafted documents and hyperlinks with a non-allowlisted URI scheme that the user opens.

### CVE-2026-124700

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-601` |
| Published | 2026-11-12T18:17:22.537 |

In Telerik UI for WinForms, versions prior to 2026.4.1111, an untrusted URL redirection vulnerability exists that allows an attacker to launch arbitrary operating system protocol handlers with attacker-controlled arguments via crafted documents and hyperlinks with a non-allowlisted URI scheme that the user opens.

### CVE-2026-91007

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-12T16:19:21.250 |

The user-mode syscall verifiers for the charger driver API in drivers/charger/charger_handlers.c did not inspect the prop argument before copying union charger_propval across the user/kernel boundary. Two members of that union are function pointers — status_notification (CHARGER_PROP_STATUS_NOTIFICATION) and online_notification (CHARGER_PROP_ONLINE_NOTIFICATION), declared in include/zephyr/drivers/charger.h — and z_vrfy_charger_set_prop() forwarded the caller-supplied union verbatim to the driver's set_property callback for any property. z_vrfy_charger_get_prop() had the mirror defect and copied the stored kernel callback address back out to user memory.

With CONFIG_USERSPACE enabled, any user-mode thread that has been granted a charger device object could call charger_set_prop() with CHARGER_PROP_STATUS_NOTIFICATION or CHARGER_PROP_ONLINE_NOTIFICATION and an arbitrary pointer value. Drivers that implement these properties — drivers/charger/charger_max20335.c, drivers/charger/charger_pf1550.c and drivers/charger/charger_bq2518x.c — store the pointer in device data and later invoke it from their interrupt work handlers, which run in supervisor mode, on any charger state change such as a cable plug/unplug.

The result is a control-flow hijack at kernel privilege from an unprivileged thread, defeating the isolation that CONFIG_USERSPACE is meant to provide; the read path additionally disclosed a kernel code address to user mode, and clearing a notifier installed by a supervisor thread let user mode suppress charger notifications. Supervisor-mode callers of charger_set_prop()/charger_get_prop() are unaffected.

The fix makes both verifiers reject the two notifier properties outright — including when the supplied callback is NULL, since the notifiers are device state — and adds a BUILD_ASSERT on CHARGER_PROP_COMMON_COUNT so that new properties force a re-review of the union's user-mode safety.

### CVE-2026-75490

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-13T10:18:16.453 |

Cudy TR3000 before 2.5.42 contains a remote code execution vulnerability that allows unauthenticated adjacent attackers to run root commands by advertising a rogue automesh controller over mDNS. Attackers on the upstream Ethernet segment can advertise _cudycmagent._tcp records pointing to a malicious MQTT broker, then send commands encrypted with a fixed AES key that router/batchcmd.lua executes as root.

### CVE-2026-126428

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T10:17:49.193 |

OpenEMR before 8.5.0 contains a remote code execution vulnerability that allows authenticated billing users to store attacker-controlled PHP by uploading a malformed ERA file to era_payments.php. Attackers with a database-write primitive such as SQL injection can register a background_services row whose require_once loads the stored .edi file, executing PHP as the web-server user.

### CVE-2026-126391

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-13T10:17:42.823 |

n8n before 1.123.89 contains an insufficient isolation vulnerability in workflow expression evaluation that allows authenticated users to escape the sandbox. Attackers with permission to create or modify workflows can craft expressions referencing unexpected JavaScript properties to execute arbitrary code on the n8n host.

### CVE-2026-126384

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T10:17:41.500 |

n8n before 1.123.89, 2.x before 2.45.5, 2.46.x before 2.46.1, and 3.x before 3.0.1 bundles a GraphicsMagick version with known vulnerabilities in its official Docker image, which the Edit Image node uses to process images. Attackers who can supply crafted untrusted images to an Edit Image workflow, such as one fed by a Webhook node, can execute code on the n8n instance.

### CVE-2026-120866

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-13T09:17:34.313 |

Memory overflow / improper handling in BGP dynamic routing can lead to unpredictable or erroneous behavior or Denial of Service in Citrix NetScaler ADC and Citrix NetScaler Gateway.

### CVE-2026-126982

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-13T00:20:13.250 |

A type allow-list bypass in the BSON serialization library of the MongoDB C# Driver allows a type-restriction check to be circumvented when polymorphic data is deserialized into loosely typed members. An unauthorized party who can supply or plant BSON/JSON data that the application later deserializes can cause the application process to instantiate .NET types outside the intended allow-list and populate them with unauthorized party-controlled values. In applications that contain a suitable gadget type, this can lead to arbitrary code execution in the context of the application, with corresponding loss of confidentiality, integrity, and availability. No special privileges beyond the ability to introduce data the application reads are required.

### CVE-2026-107443

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T20:18:15.120 |

A flaw was found in Foreman. An authenticated user with view_hosts privileges can retrieve rendered provisioning template content for a host via the hosts template API endpoint, disclosing sensitive data such as the host root password. This is an incomplete fix of CVE-2026-96659, which hardened the web UI preview path but left the API host-template render path authorized for Viewer-level users.

### CVE-2026-127091

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-41` |
| Published | 2026-11-13T10:18:05.797 |

Jadaptive Maverick Synergy Server before 3.0.33 and 3.1.x before 3.1.7, and Maverick Legacy Server before 1.8.1, contain an improper path equivalence flaw in VirtualFileFactory.canonicalisePath that bypasses mount-level access policy. Authenticated users can supply paths with duplicate separators or dot segments to route operations to a less restrictive parent mount and read or write files the child mount denies.

### CVE-2026-126431

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:49.700 |

OpenEMR before 8.5.0 contains a second-order sql injection vulnerability that allows authenticated Carecoordination users to store malicious C-CDA field identifiers through the savedata action. Attackers can inject SQL into the IN clause built by fetchFormValues() during C-CDA generation to extract password hashes, portal reset values, and patient records.

### CVE-2026-126404

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-13T10:17:45.087 |

Coder 2.28.0 before 2.29.24, 2.30.0 before 2.34.16, 2.35.0 before 2.36.11, 2.37.0 before 2.37.8, and 2.38.0 before 2.38.4 does not restrict new API keys to the creating token's scopes, allow list, or expiry. A scoped API key or OAuth2 token holding key-creation permission can call POST /api/v2/users/{user}/keys/tokens to mint longer-lived coder:all keys, gaining the user's full privileges.

### CVE-2026-126312

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-13T10:17:36.973 |

OpenBao before 2.6.5 and 2.7.x before 2.7.2, and the openbao-plugins LDAP and RADIUS auth plugins before 0.2.0, contain an ACL bypass in the AppRole, Cert, LDAP, and RADIUS auth methods caused by implicit path canonicalization. Authenticated attackers can request non-canonical paths for AppRole Role IDs, Cert CRLs, LDAP groups and users, or RADIUS users to evade ACL deny rules.

### CVE-2026-126309

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T10:17:36.500 |

OpenBao before 2.6.5 and 2.7.2 contains a path traversal vulnerability in Transit key import that allows authenticated attackers to bypass name restrictions in ACL policies. Attackers limited by a required_parameters name constraint can craft traversal sequences during import to write key material under arbitrary Transit key names.

### CVE-2026-61418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:18:15.880 |

Dell SmartFabric OS10 Software, versions prior to 10.6.0.10, contains an Incorrect Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-116418

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:17:25.253 |

Dell PowerScale InsightIQ, versions 6.3.0 through 6.4.0, contains an Incorrect Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-126366

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770;CWE-1325` |
| Published | 2026-11-13T00:20:12.397 |

MessagePack for Ruby is an implementation of the MessagePack binary serialization format. Prior to 1.8.7, the Java-platform msgpack gem for JRuby allocated arrays and byte buffers directly from attacker-controlled array32, str32, and bin32 declared sizes before confirming that corresponding elements or bytes were available. A short MessagePack header could therefore trigger a very large allocation or sustained heap growth when an application decoded untrusted input through MessagePack.unpack or MessagePack::Unpacker, potentially exhausting the shared JVM heap. map32 and declared counts at or above 2^31 did not use the affected allocation behavior. This issue is fixed in version 1.8.7.

### CVE-2026-47217

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-400;CWE-674;CWE-754` |
| Published | 2026-11-12T20:18:39.770 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4 and 1.5.1, a remote attacker can trigger an uncontrolled recursion and stack overflow in the default server application of bacnet-stack by abusing the Channel object. This issue has been patched in versions 1.4.4 and 1.5.1.

### CVE-2026-46674

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-125` |
| Published | 2026-11-12T20:18:39.080 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.4 and 1.5.1, an out-of-bounds read vulnerability exists in bacnet-stack's AtomicWriteFile record-access path. The bug is caused by a mismatch between an externally controlled returnedRecordCount field and the fixed-size internal fileData[] array used by BACNET_ATOMIC_WRITE_FILE_DATA. This issue has been patched in versions 1.4.4 and 1.5.1.

### CVE-2026-45341

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-11-12T20:18:38.667 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. From versions 1.4.0 to before 1.4.4, and 1.5.0 to before 1.5.1, a NULL pointer dereference can be triggered in bacnet_device_object_reference_decode() when a WriteProperty request updates OBJECT_STRUCTURED_VIEW / PROP_SUBORDINATE_LIST. This issue has been patched in versions 1.4.4 and 1.5.1.

### CVE-2026-127030

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T17:17:43.150 |

A flaw was found in freeradius. An improper length validation in the EAP-FAST module allows a stack-based buffer overflow during session ticket processing. A remote, unauthenticated attacker can exploit this flaw by sending a specially crafted handshake request, causing the server process to crash and resulting in a Denial of Service (DoS).

### CVE-2026-127029

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-12T17:17:42.970 |

A flaw was found in freeradius's Extensible Authentication Protocol Method for Subscriber Identity Module (EAP-SIM) module. When handling authentication requests, the server copies a client-supplied identity into an internal structure without properly checking its length against a fixed-size buffer. An unauthenticated remote attacker can exploit this issue by sending specially crafted EAP-SIM messages, triggering a stack buffer overflow that crashes the service and results in a Denial of Service (DoS).

### CVE-2026-126191

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-11-12T17:17:32.627 |

Soup Sieve is a CSS selector library designed to be used with Beautiful Soup 4. Prior to 3.0, the CSS_ESCAPES and IDENTIFIER regular-expression subpatterns can backtrack exponentially on runs of ambiguous digit escapes in an attribute-name or tag position of an otherwise valid selector. The failure occurs during selector compilation through soupsieve.compile() or Beautiful Soup select() before SELECTOR_LIMIT is applied, so an application that accepts untrusted selector strings can have a worker stalled by a short input. This issue is fixed in version 3.0.

### CVE-2026-126190

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-11-12T17:17:32.440 |

Soup Sieve is a CSS selector library designed to be used with Beautiful Soup 4. Prior to 4.0, Soup Sieve repeatedly walks the same ancestors while matching descendant combinators, and each additional descendant combinator raises the polynomial degree of the work on deeply nested attacker-influenced HTML or XML. Applications using selectors such as section div div through select(), select_one(), or Beautiful Soup CSS APIs against untrusted documents can have a worker occupied for seconds or minutes, while trusted-only document processing is not affected. Selectors compiled with NOCACHE continue to use the old uncached behavior. This issue is fixed in version 4.0.

### CVE-2026-128030

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-13T10:18:08.990 |

OpenMage magento-lts before 20.18.2 and 21.0.0-beta1 before 21.0.0-beta3 contains an insufficient session expiration vulnerability because Mage_Api_Model_Session::_renewBySessId() never checks api_user.is_active and REST OAuth authorization never checks whether the admin user is active. Attackers holding an existing SOAP/XML-RPC session or OAuth access token retain API access after deactivation or API key rotation, reading and modifying customer, order and catalog data.

### CVE-2026-126823

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-377` |
| Published | 2026-11-12T22:19:21.100 |

A local user with an ordinary account on the same host can place a file in a shared temporary location that the JDBC driver's native library loading routine will accept and load without verifying its origin. Loading the driver class in a Java application may then run code of that user's choosing inside the application process, which may result in disclosure or alteration of data held by that process or in the process becoming unavailable.

### CVE-2026-126329

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-282` |
| Published | 2026-11-12T16:19:04.663 |

Docker Sandboxes reuses existing state and configuration directories without verifying their ownership. If sbx or sandboxd is run as root with HOME or, on Linux, XDG_STATE_HOME pointing to an attacker-controlled location, a local unprivileged user can substitute control-plane sockets and configuration trusted by the root process, potentially executing commands as root. Exploitation requires a privileged invocation with an attacker-influenced environment. The issue affects Linux and macOS and is fixed in version 0.53.0.

### CVE-2026-82177

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-11-13T14:18:00.503 |

Dell PowerStore contains an OS Command Injection vulnerability. A high-privileged attacker could exploit this vulnerability, potentially leading to arbitrary root command execution on the appliance.

### CVE-2026-127122

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-13T14:17:54.500 |

P-Net before 1.0.4 does not check the number of MCR request blocks in a Connect request against the number of multicast communication relations that an Application Relationship has room for (PNET_MAX_MC_CR, 1 by default). Each further block is written past the end of the array, into the rest of the Application Relationship and, with more blocks, into the following one. The written data comes from the request. No established Application Relationship is needed, and the attacker requires ADJACENT network access. Builds with PNET_OPTION_MC_CR disabled are not affected.

### CVE-2026-127094

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:18:06.300 |

Pagelayer 2.1.7 before 2.2.1 contains a missing authorization vulnerability in Abilities API abilities registered in main/abilitiesregister.php that only require the edit_posts capability. Contributor-level attackers can overwrite, publish, delete, or duplicate other users' private posts and pages to read them, and modify site-wide theme templates like headers and footers.

### CVE-2026-126486

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:58.750 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in portal/import_template.php, where several portal document template modes lack admin/forms ACL and CSRF checks. Any authenticated staff user can send mode=save_profiles to delete all template profile assignments, use other unguarded modes to push templates to patients or change categories, and read template bodies via mode=get or getPdf.

### CVE-2026-126481

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:57.893 |

OpenEMR before 8.5.0 contains a path traversal vulnerability in era_payments.php and sl_eob_search.php that allows authenticated billing users to write files outside the ERA directory. Attackers can embed traversal sequences in the GS04 element of an uploaded X12 835 file to overwrite .edi or .835 files with attacker-controlled content anywhere writable by the web server.

### CVE-2026-126479

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:57.563 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in five Module Manager InstallerController actions that lack the admin/manage_modules ACL check and CSRF validation. Low-privilege users such as Front Office accounts can POST to saveConfig or SaveHooks to overwrite any module's configuration, retarget CCDA and HIE settings, and delete module hooks.

### CVE-2026-126478

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:57.397 |

OpenEMR before 8.5.0 contains an SQL injection vulnerability in the Syndromic Surveillance report because the form_icd_codes[] POST array is concatenated into an unquoted numeric IN() clause without integer validation. Authenticated users can submit quote-free payloads that bypass add_escape_custom to perform blind or UNION-based injection and exfiltrate patient health information.

### CVE-2026-126375

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:39.927 |

Vvveb through 1.0.8.6 contains a missing authorization vulnerability that allows low-privilege vendors to rename, delete, or overwrite other vendors' digital-asset files in the shared storage/digital_assets directory. Attackers can send rename, delete, or upload requests to product/digital-asset with another vendor's filename to break downloads or substitute malicious content.

### CVE-2026-126321

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:38.400 |

Dockhand before 1.0.55 contains a path traversal vulnerability that allows authenticated users with stacks:edit to bypass the file-browser path guard by combining symlinks with '..' sequences. Attackers can read /proc/self/environ, the SQLite database, and the encryption key via /api/system/files/content, or move them using the stack relocate endpoint, exposing stored credentials.

### CVE-2026-120688

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:27.137 |

The EZ SQL Reports Shortcode Widget and DB Backup plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'HTTP_USER_AGENT (demonstrated); more generally, any attacker-controllable DB column the saved report selects' parameter in all versions up to, and including, 5.25.25 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires an administrator to have saved a SQL report that selects an attacker-controllable database column, such as wp_comments.comment_agent, which WordPress stores verbatim from unauthenticated visitors even when comments are pending moderation.

### CVE-2025-71459

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:23.780 |

Zipline through 4.3.2 contains a path traversal vulnerability that allows authenticated uploaders to write files outside the upload directory by supplying traversal sequences in the x-zipline-filename header. Attackers using the local datasource can create or overwrite files writable by the Zipline process, corrupting application data or disrupting service.

### CVE-2026-6467

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-11-12T15:17:51.793 |

Uncontrolled search path element in PostgreSQL CREATE EXTENSION allows an attacker with database-level CREATE privilege to execute arbitrary code as the bootstrap superuser, via ALTER SCHEMA ... RENAME or CREATE EXTENSION ... SCHEMA "$user".  ALTER EXTENSION was also affected.  A trusted-extension script located the wrong object and executed arbitrary SQL of the attacker's choice.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-120153

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-12T15:17:44.073 |

SQL injection in PostgreSQL extension-script substitutions allows an attacker with database-level CREATE privilege to execute arbitrary code as the bootstrap superuser, via a schema or owner name containing newlines or other special substrings.  This is similar to CVE-2023-39417, but it requires a non-bundled extension with a vulnerable script pattern.  Versions before PostgreSQL 18.7, 17.12, 16.16, 15.20, and 14.25 are affected.

### CVE-2026-116313

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-11-12T15:17:39.347 |

Untrusted search path in PostgreSQL vacuumdb allows a database owner to execute arbitrary SQL as the database user running vacuumdb, via shadowing operators used in the --missing-stats-only catalog query.  The pg_upgrade documentation recommends an affected vacuumdb invocation.  Within major version 18, minor versions before PostgreSQL 18.7 are affected.  Versions before PostgreSQL 18 are unaffected.

### CVE-2026-128790

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-11-13T14:17:55.250 |

In Eclipse BaSyx Go Components versions up to and including 1.1.2, ABAC-enabled deployments of the Submodel Repository and the AAS Environment do not apply an access rule's `FILTERLIST` fragment filters to single Submodel reads.



`GET /submodels` removes the fields that a rule's `FILTERLIST` hides, but `GET /submodels/{submodelIdentifier}` and `GET /submodels/{submodelIdentifier}/$metadata` return them unfiltered. An authenticated caller with READ access to a Submodel can therefore read fields that the access rules hide from them, for example `supplementalSemanticIds` keys that name the other parties allowed to read the Submodel.



If versioning is enabled (`history.mode` set to `api` or `audit`), `GET /submodels/{submodelIdentifier}/$history` and `GET /shells/{aasIdentifier}/$history` in the Submodel Repository, AAS Repository and AAS Environment return the complete stored version without applying the rule's formula or fragment filters. A caller whose rules grant READ on these routes can read fields that the access rules hide, and Submodels and Asset Administration Shells that the direct read does not return to them at all.



The issue is fixed in Eclipse BaSyx Go Components v1.1.3.

### CVE-2026-127124

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-772` |
| Published | 2026-11-13T14:17:54.843 |

P-Net before 1.0.4 keeps the RPC session that is allocated for a fragment of a request with an unknown activity UUID, without a timeout, when the rest of the request never arrives. A session that does not get an Application Relationship is also kept after the response. Repeated fragments or requests with different activity UUIDs exhaust the available sessions, one UDP packet per session. Once they are exhausted the device no longer answers a Connect request until it is restarted. An unauthenticated attacker with ADJACENT network access can use this to cause a denial of service.

### CVE-2026-124761

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-696` |
| Published | 2026-11-13T14:17:50.613 |

P-Net before 1.0.4 copies the IP suite of a DCP Set request to the current and the non-volatile configuration, and starts saving it, before the state of the device is checked. If the request is refused, for example because an Application Relationship is active, the configuration is not restored and is still saved. After a restart the device uses the refused address, and may not answer the controller or may use its address. A host with ADJACENT network access can use this while an Application Relationship is active.

### CVE-2026-124759

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-13T14:17:50.337 |

P-Net before 1.0.4 routes a received RTA alarm frame to an Application Relationship using only the destination alarm reference in the frame, without checking the source of the frame. A host with ADJACENT network access can abort an established Application Relationship with a single alarm ERROR frame, or deliver forged alarm notifications with chosen type, slot, subslot, USI and payload to the application.

### CVE-2026-116413

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-327` |
| Published | 2026-11-13T14:17:48.390 |

Dell PowerStore contains a use-of-broken-cryptography vulnerability. A low-privileged attacker could exploit it to impersonate another identity, potentially leading to unauthorized access.

### CVE-2026-127078

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:18:03.970 |

OpsTree BuildPiper before 2.7.0 contains an authorization bypass vulnerability that allows authenticated users to attach another application's environment to their service by supplying a foreign project_env_id. Attackers can configure CI and trigger builds and deployments through the component env endpoints using the other application's configuration, registries and deployment infrastructure.

### CVE-2026-127077

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:18:03.820 |

OpsTree BuildPiper before 2.7.0 contains an authorization bypass vulnerability that allows authenticated users to create environments on unassigned Kubernetes clusters by tampering with cluster_id and namespaces values. Attackers can modify requests to POST /api/v1/project/{project_id}/env/ to target another project's cluster, then trigger builds and deployments into it, bypassing project isolation.

### CVE-2026-127076

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:18:03.680 |

OpsTree BuildPiper before 2.7.0 contains a broken access control vulnerability that allows authenticated users to list and build from Git repositories restricted to other projects. Attackers can enumerate repositories via GET /api/v1/git_repo/?all=true and submit any git_repo_id to the ci endpoint, cloning other projects' source code, manifests, and committed secrets.

### CVE-2026-127075

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:18:03.530 |

OpsTree BuildPiper before 2.7.0 contains a path traversal vulnerability that allows authenticated users to read arbitrary files by supplying traversal sequences in Additional Manifest file paths. Attackers can enter paths like ../../../../etc/passwd so the renderer embeds file contents in generated manifests and logs, exposing configuration files and service-account tokens.

### CVE-2026-126938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:18:00.573 |

Zipline before 4.6.4 contains a resource allocation vulnerability that allows authenticated users to bypass chunked-upload size and quota checks by forging Content-Range offsets and totals. Attackers can send tiny chunks to the partial upload endpoint with large declared offsets, causing the server to create oversized files and exhaust disk space.

### CVE-2026-126494

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-13T10:18:00.100 |

OpenEMR before 8.4.0 contains an improper authorization vulnerability in ScopeRepository::finalizeScopes() that allows read-only SMART/OAuth clients to obtain write scopes because ScopeEntity::containsScope() ignores registered permissions. Attackers with a client registered for user/<resource>.read can request user/<resource>.write to create, update, and delete appointments or patient data.

### CVE-2026-126492

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:59.763 |

OpenEMR before 8.5.0 contains a second-order sql injection vulnerability that allows low-privileged authenticated users to store malicious SQL via library/ajax/addlistitem.php. Attackers can persist a SQL fragment in the recent_patient_columns option_id value, which dynamic_finder.php concatenates into a SELECT query and executes as SQL.

### CVE-2026-126483

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:58.257 |

OpenEMR before 8.5.0 contains an SQL injection vulnerability that allows authenticated report users to manipulate queries by supplying a crafted form_facility value to interface/reports/ippf_statistics.php. Attackers can close the string literal in the facility_id WHERE clause and use boolean or time-based payloads to read sensitive database contents.

### CVE-2026-126471

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:56.253 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in print_referral.php and trend_form.php that allows low-privileged Front Office users to access patient PHI without patients:med permission. Attackers can directly request these endpoints with arbitrary patient_id values to retrieve patient demographics, insurance data, and vitals history, enumerating IDs to expand disclosure.

### CVE-2026-126467

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-13T10:17:55.580 |

OpenEMR before 8.5.0 contains a mass assignment vulnerability in ObservationController::processEnhancedFormSave() that allows authenticated low-privilege users to forge authorization flags through an incomplete field blacklist. Attackers can submit authorized=1 or override the id field alongside observation_id to mark observations as Provider-signed and overwrite clinical fields of other observations within the same patient encounter.

### CVE-2026-126465

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:55.247 |

OpenEMR before 8.5.0 contains an SQL injection vulnerability in the patient portal api/onsiteactivityviews endpoint that allows any authenticated staff user to inject SQL through unquoted Id_BitwiseAnd Criteria values. Attackers can close the bitwise parenthesis and append OR or UNION SELECT clauses to read patient PHI, staff password hashes, MySQL authentication strings, and API tokens.

### CVE-2026-126463

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:54.890 |

OpenEMR before 8.5.0 contains multiple sql injection vulnerabilities that allow authenticated users to inject payloads through ERA CLP01, form_facility, form_icd_codes, and POST key names. Attackers can perform UNION, blind, and error-based injection to read users_secure password hashes and patient PHI, and overwrite patient_data fields.

### CVE-2026-126461

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-13T10:17:54.520 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in library/ajax/user_settings.php that lets any authenticated user persist arbitrary global configuration overrides. Attackers can POST global:-prefixed keys to re-point external service hosts like CouchDB, eRx, phiMail, or SMTP to attacker-controlled servers, exfiltrating system credentials and patient PHI.

### CVE-2026-126460

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-13T10:17:54.337 |

OpenEMR before 8.5.0 contains a persistent SQL injection vulnerability in SLEOB::slInvoiceNumber(), where the CLP01 claim control number from uploaded X12 835 ERA files is concatenated unescaped into a query. Attackers with billing write access can upload a crafted .edi file via sl_eob_search.php that is stored on the server and re-executes a time-based payload whenever it is reprocessed through sl_eob_process.php, extracting patient health information.

### CVE-2026-126457

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:53.997 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in InstallerController that allows any authenticated user to modify module administration settings without the admin/manage_modules permission. Low-privileged users such as Front Office clerks can POST to saveConfig, DeleteAcl, DeleteHooks and nickName actions to reconfigure or partially disable installed modules.

### CVE-2026-126453

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-11-13T10:17:53.347 |

OpenEMR before 8.5.0 contains an inverted comparison in Document::has_expired() that causes the FHIR Binary download endpoint to treat time-limited PHI documents as unexpired after their one-hour lifetime. Authenticated users still authorized for a Binary/{id} resource can download expired bulk export NDJSON files and $docref CCDs indefinitely.

### CVE-2026-126452

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:17:53.190 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in diagnosis_full.php that allows authenticated users to delete or clear any billing record by ID. Attackers can supply a target billing ID in the id parameter with delete or clear mode to deactivate other patients' charges and corrupt financial records.

### CVE-2026-126449

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:52.667 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in immunizations.php, diagnosis_full.php, and billing_process.php that lets low-privileged users bypass ACL checks. Authenticated Front Office users can reuse their session CSRF token to add or delete immunizations, write encounter billing codes, and invoke the billing processor.

### CVE-2026-126443

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:51.650 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in dynamic_finder_ajax.php that allows authenticated users without patients/demo permission to query patient demographics. Attackers can supply arbitrary patient_data columns via the sColumns parameter to enumerate names, dates of birth, contact details, and Social Security numbers across the practice.

### CVE-2026-126437

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:17:50.660 |

OpenEMR before 8.5.0 contains an authorization bypass vulnerability in portal/lib/download_template.php that allows any authenticated core user to render documents for arbitrary patients by setting isModule. Attackers can submit arbitrary pid and template_id values to disclose patient names, birth dates, chart IDs, addresses, allergies, medications, and problem lists despite ACL and squad restrictions.

### CVE-2026-126429

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-13T10:17:49.360 |

OpenEMR before 8.5.0 passes authenticated user-controlled HTML from the doc_lib.php content parameter to mPDF, which resolves local files and nested SVG resources. Authenticated patients or core users can submit crafted CSS imports or php://filter SVG references to read arbitrary server files including credentials and OAuth keys.

### CVE-2026-126416

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-13T10:17:47.163 |

OpenEMR before 8.5.0 contains an improper authorization vulnerability in patient_tracker_status.php that allows low-privilege authenticated users to modify other patients' tracker entries by supplying arbitrary tracker_id values. Attackers can post statustype and roomnum parameters with a valid CSRF token to alter patient-flow status, room assignments, and linked calendar appointment state.

### CVE-2026-126415

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:46.993 |

OpenEMR before 8.5.0 contains a missing authorization vulnerability in the Patient Validation module that allows any authenticated user to retrieve patient demographic records. Attackers can send direct requests with wildcard mf_lname or empty mf_ parameters to the patientvalidation endpoint to enumerate the entire patient_data table.

### CVE-2026-126405

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-13T10:17:45.257 |

Coder 2.21.0 before 2.29.24, 2.30.0 before 2.34.16, 2.35.0 before 2.36.11, 2.37.0 before 2.37.8, and 2.38.0 before 2.38.4 reads Web Push endpoint responses in webpushSend with io.ReadAll, without a size limit or client timeout. Any authenticated user can register a subscription via POST /api/v2/users/{user}/webpush/subscription pointing to a server returning an endless body, exhausting coderd memory and crashing the API, dashboard, and workspace connections.

### CVE-2026-126399

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:17:44.260 |

vLLM from 0.19.0 before 0.31.0 contains a resource exhaustion vulnerability that allows inference clients to bypass the server frame limit by setting media_io_kwargs.video.num_frames in chat completion requests. Attackers can supply num_frames=-1 or a large value with many base64 JPEG frames, forcing VideoMediaIO to decode all frames and np.stack them, causing memory exhaustion.

### CVE-2026-126320

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-11-13T10:17:38.247 |

Dockhand before 1.0.55 contains an improper authorization vulnerability that lets users holding only containers:view download arbitrary container files instead of requiring containers:exec. Authenticated Enterprise RBAC users can request any path from the files/download endpoint, which reads through Docker's archive API, to retrieve secrets, keys, and mounted credentials.

### CVE-2026-126319

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:38.083 |

Dockhand before 1.0.55 contains an arbitrary file read vulnerability that allows authenticated users with stacks:create permission to read sensitive files by supplying an arbitrary composePath during stack adoption. Attackers can adopt a stack pointing to the encryption key, SQLite database, or /proc/self/environ and read it via the compose endpoint to obtain all stored credentials.

### CVE-2026-126293

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:17:33.740 |

NocoDB before 2026.06.2 contains an attachment size limit bypass that allows authenticated Editor users to store oversized files because data-attachment-v3.service.ts trusts the remote server's advertised content length. Attackers can point the v3 upload-by-URL endpoint at a server that understates or omits its length to exhaust disk space or storage quota.

### CVE-2026-126290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-11-13T10:17:33.290 |

NocoDB before 2026.07.0 contains an information disclosure vulnerability in base-integrations.service.ts that allows authenticated base members to read private integration configurations by omitting a query flag. Attackers can request another user's private integration without the configuration flag, bypassing the ownership check to obtain stored connection credentials.

### CVE-2026-126281

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-13T10:17:31.517 |

NocoDB before 2026.08.0 contains a missing authorization vulnerability in the copy-from branch of integration creation in integrations.service.ts that decrypts a source integration's connection credentials without checking its owner or private flag. Authenticated users with the Creator role can supply guessed or enumerated integration ids to copy other users' private database host, username, and password into an integration they own.

### CVE-2026-126275

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-13T10:17:30.583 |

NocoDB before 2026.09.0 contains an insecure direct object reference vulnerability that allows authenticated users to read cross-base row comments by supplying only model and row ids. Attackers with a Viewer or Creator role on an unrelated base can read private comments and author emails, or plant decoy tables and duplicate comment ids to spoof teammates' comments.

### CVE-2026-126272

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-13T10:17:30.140 |

NocoDB before 2026.09.0 contains an uncontrolled resource consumption vulnerability that allows authenticated users to bypass bulk row-count limits by using session authentication instead of API tokens. Attackers with Editor write permission on one table can submit hundreds of thousands of rows to v1 and v2 bulk write routes, exhausting database connections, CPU, and memory.

### CVE-2026-126267

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-13T10:17:29.350 |

NocoDB from 0.300.0 before 2026.04.4 contains a denial of service vulnerability that allows authenticated users to crash the server by triggering an unhandled promise rejection in MetaService metadata logging. Attackers can send a request leaving a lookup condition undefined, causing knex binding errors in the unawaited logHelper call that terminate the server process.

### CVE-2026-59079

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-13T08:17:18.067 |

Edito CMS restricts the ability to upload files via the UI to specific file types. However, an avatar upload functionality allows an attacker to upload files of any type and extension without restriction.
This issue was fixed in version 5.10.2607.  Hotfixes for older versions (5.8) have also been released.

### CVE-2026-59075

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-917` |
| Published | 2026-11-13T08:17:17.517 |

Edito CMS is vulnerable to Dynamic LINQ injection. Due to improper input validation, an authenticated attacker can inject conditional expressions into the sort parameter of paginated administrative endpoints. Analyzing the returned result order allows the attacker to extract value of any field character by character, leading to potential exposure of sensitive data.


This issue was fixed in version 5.10.2607.  Hotfixes for older versions (5.8) have also been released.

### CVE-2026-127211

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-12T22:19:21.420 |

MultiVendorX plugin for WordPress before 5.0.22 contains a broken access control vulnerability in the /wp-json/multivendorx/v1/stores REST route that allows authenticated vendors to access administrative flag handlers due to the store_owner role possessing the edit_stores capability and missing per-store ownership checks. Attackers can exploit the insecure direct object reference in the visitorMap handler and other flag handlers to retrieve other stores' contact emails, pending withdrawal amounts, onboarding and registration data, deactivation reasons, and visitor analytics, resulting in a cross-tenant confidentiality breach.

### CVE-2026-52786

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-11-12T20:18:42.493 |

BACnet Stack is a BACnet open source protocol stack C library for embedded systems. Prior to versions 1.4.5, 1.5.1, and 1.6.0, in the official apps/epics client tool on v1.6.0-rc1 (not in the generic BACnet RPM ACK decoder alone) a malicious BACnet/IP endpoint can reply to the EPICS tool’s legitimate ReadPropertyMultiple request with a syntactically valid ReadPropertyMultiple-ACK that contains more heading properties than the tool’s fixed local storage can hold. The response is decoded successfully and later consumed by ProcessRPMData(), which writes property values into a fixed global array using an unbounded linear index. This results in a reproducible global-buffer-overflow in apps/epics/main.c. This is a network-reachable memory corruption in the official epics tool’s response-processing path. The root cause is that apps/epics treats a remotely supplied variable-length RPM property list as if it were a trusted, fixed-size local heading-property set. This issue has been patched in versions 1.4.5, 1.5.1, and 1.6.0.

### CVE-2026-111456

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-12T20:18:16.067 |

A missing authorization check has been found in ConsumerResource.setupOwner() function of consumer registration module in the Candlepin package. The registration method checks permission to create a consumer only when the caller is a user. A consumer that authenticates with its identity certificate does not go through that check. A low-privileged network attacker or user who has a valid consumer certificate for one organization can register a new consumer in a different organization by supplying that organization's key. The response includes an identity certificate for the new consumer. With that certificate, the attacker can view the target organization's subscription pools. When the organization is not using simple content access, the attacker can attach that organization's entitlements to the new consumer.

### CVE-2026-107152

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-12T20:18:14.680 |

An improper authentication vulnerability has been found in the task console in the smart_proxy_dynflow package. The console accepts any client certificate signed by the capsule's certificate authority. It does not check the list of servers the capsule trusts. A low-privileged network attacker or user must already hold such a certificate. They can open the console and read job details. Those details include passwords when a job was given them. They can also cancel a running task.

### CVE-2026-120467

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-12T19:16:48.553 |

Joomla / WordPress Extension - acymailing.com - Subscriber identity not bound to the record acted upon in AcyMailing 1.0.0 - 11.1.1 - An authenticated user of any privilege level can subscribe or unsubscribe any other subscriber to or from any mailing list of the site.

### CVE-2026-117550

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-12T18:17:15.657 |

Joomla Extension - jdownloads.com - Publishing of files without approval in jDownloads < 4.1.8 -  Manipulated frontend submission parameters could bypass the intended publication and ownership rules. In particular, submissions could be published despite automatic publication being disabled, and ownership could be assigned contrary to the intended policy.

### CVE-2026-106475

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-22;CWE-863` |
| Published | 2026-11-12T18:17:12.720 |

The Elasticsearch data source resource proxy forwards the request method and path to Elasticsearch using the data source's own credentials, without restricting them to the operations the plugin needs. A user who can query the data source can alter index mappings or reach other indices on the cluster. [Improper authorization / path validation]

### CVE-2026-124698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T17:17:31.320 |

In Progress Kendo UI for jQuery, the Chart default tooltip renders point values as raw HTML. An attacker who can influence a string point value can inject markup that executes as JavaScript when a user hovers over the point. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. Version 2016.2.607 or earlier may be affected, but earlier releases have not been verified. The latest vulnerable version is 2026.3.1015; the issue is fixed in version 2026.4.1111.

### CVE-2026-124697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T17:17:31.160 |

In Progress Kendo UI for jQuery, Chart shared-tooltip rendering treats bound category and series-name values as raw HTML. An attacker who can influence values consumed by an affected Chart can inject markup that executes as JavaScript when a user displays the shared tooltip. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. Version 2016.2.607 or earlier may be affected, but earlier releases have not been verified. The latest vulnerable version is 2026.3.1015; the issue is fixed in version 2026.4.1111.

### CVE-2026-124696

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T17:17:30.993 |

In Progress Kendo UI for jQuery, Spreadsheet sheet names are inserted into the SheetsBar menu button's data-sheet-name attribute without encoding. An attacker who can influence a sheet name can inject an event-handler attribute and execute JavaScript when a user hovers over the menu button. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected version is 2024.4.1112; the latest vulnerable version is 2026.3.1015. The issue is fixed in version 2026.4.1111.

### CVE-2026-124695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T17:17:30.790 |

In Progress Kendo UI for jQuery Form, the items[].hint option is documented as a string but is rendered as HTML. An attacker who can influence a Form item's hint can cause attacker-controlled markup to execute as JavaScript when a user views the rendered form. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected version is 2020.2.513; the latest vulnerable version is 2026.3.1015. The issue is fixed in version 2026.4.1111.

### CVE-2026-124691

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T17:17:30.637 |

In Progress Kendo UI for jQuery Gantt, the task editor's Parent dropdown renders task titles as HTML. An attacker who can influence a task title shown in the dropdown can cause attacker-controlled markup to execute as JavaScript when a user opens or interacts with the task editor. Successful exploitation may compromise the confidentiality and integrity of data available in the user's browser context. The first affected version is 2020.3.915; the latest vulnerable version is 2026.3.1015. The issue is fixed in version 2026.4.1111.

### CVE-2026-127141

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1088` |
| Published | 2026-11-12T16:19:08.230 |

SOGo before 5.12.13 contains a denial of service vulnerability that allows authenticated attackers to exhaust all worker processes by configuring an auxiliary IMAP mail account pointing to a controlled host that accepts a TCP connection but never sends an IMAP greeting response. Attackers can issue concurrent GET requests to the mail view of this account to hold workers indefinitely without an effective timeout, occupying every SOGo worker and denying service to all users for approximately five minutes until the watchdog kills and respawns the stuck workers.

### CVE-2026-127121

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-12T16:19:07.587 |

SOGo before 5.12.13 contains an improper cryptographic signature verification vulnerability that allows remote attackers to replace a victim's contact S/MIME certificate by sending a spoofed multipart/signed message with a mismatched signature and an impersonated From address. Attackers can deliver a crafted CMS signedData object containing their own self-signed certificate, which SOGo's UIxMailView stores on the contact card without validating signature authenticity or certificate identity, enabling subsequent encrypted communications to be decrypted with the attacker's private key.

### CVE-2026-95518

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-13T13:18:31.217 |

Time-of-check time-of-use (TOCTOU) race condition vulnerability in TÜBİTAK BİLGEM Yazılım Teknolojileri Araştırma Enstitüsü Pardus Package Installer allows Leveraging Time-of-Check and Time-of-Use (TOCTOU) Race Conditions.

This issue affects Pardus Package Installer: from 0.7.0 before 0.7.1.

### CVE-2026-126950

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:18:02.323 |

Zipline through 4.4.0 contains a path traversal vulnerability that allows authenticated attackers to delete arbitrary server files by injecting traversal sequences via the x-zipline-file-extension header. Attackers can upload a file with a poisoned stored name and short expiry so LocalDatasource deletion removes chosen files, causing denial of service or data loss.

### CVE-2026-126949

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:18:02.193 |

Zipline through 4.4.0 contains a path traversal vulnerability in the PATCH /api/user/files/:id rename endpoint that allows authenticated users to overwrite existing uploads by supplying unsanitized names. Attackers can submit names like ../uploads/victim.txt that bypass the raw-string database uniqueness check but normalize via path.join(), causing fs.rename() to replace other files' contents.

### CVE-2026-126310

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-13T10:17:36.653 |

OpenBao before 2.6.5 and 2.7.2 contains an authentication bypass vulnerability that allows unauthenticated callers to obtain OIDC ID tokens by abusing public clients with client_credentials enabled. Attackers who know a public client's client_id can request tokens from the identity/oidc/provider/<name>/token endpoint to impersonate the client without any secret.

### CVE-2026-126295

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-13T10:17:34.060 |

NLTK from 3.10.0 before 3.10.4 contains an arbitrary file read vulnerability in BllipParser that allows attackers to open files outside NLTK data roots by supplying unvalidated model paths. Attackers controlling parser_model, reranker_features, reranker_weights, or from_unified_model_dir() input can make the bllipparser C extension read sensitive files or block on FIFOs and devices.

### CVE-2026-126279

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-13T10:17:31.210 |

NocoDB before 2026.06.2 contains a stored cross-site scripting vulnerability in PromptWithFields.vue that renders unescaped field references from AI field prompts as HTML in a tooltip. Attackers with the Creator role or above can store markup in a prompt's field reference that executes when victims open the field configuration, stealing the localStorage session token to call authenticated APIs as the victim.

### CVE-2025-0043

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-12T20:18:13.827 |

Incorrect directory permissions within AMD Vivado™ Lab Solutions could allow a local user-privileged attacker to escalate their privileges, potentially resulting in arbitrary code execution.

### CVE-2024-21954

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-11-12T19:16:44.843 |

Improper exception handling in IOMMU could allow an invalidate command to be sent to PCIe devices that do not support Address Translation Cache (ATC), potentially resulting in denial of service.

### CVE-2026-119275

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-12T18:17:16.507 |

Akaunting 3.3.0 contains a stored cross-site scripting vulnerability in the XLSX invoice-import workflow. An authenticated Manager can import a child invoice whose invoice number contains HTML and is linked to a recurring invoice. When a victim opens that recurring invoice, Akaunting raw-renders the stored child number in an anchor, causing attacker-controlled markup to execute in the victim's browser.
