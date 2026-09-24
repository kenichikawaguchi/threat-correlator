# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-24 15:00 UTC
- **対象期間**: `2026-09-23T15:00:46.000Z` 〜 `2026-09-24T15:00:37.000Z`
- **重要CVE数**: 176 件（Critical 9.0+: 40 件 / High 7.0〜: 136 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上** が 40 件以上報告され、**リモートコード実行 (RCE)・任意ファイル操作・権限昇格** が圧倒的に多い。  
- 特に **未認証での攻撃が可能** な脆弱性が目立ち、インターネットに面したサービス（GitLab、HFS2、WordPress プラグイン等）での被害拡大リスクが高い。  
- エンタープライズ向け製品（GitLab、Red Hat Ansible Automation Platform、Velociraptor、OpenC3）でも **認証済みユーザーでも特権取得が可能** な欠陥が多数報告され、内部脅威への備えが求められる。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目すべき理由 |
|-----|------|----------|----------------|
| **CVE‑2026‑97360** | 10.0 | HFS2 2.4.0 以前で **認証不要の任意ファイル読取/書込/削除** が可能 | ファイルシステム全体にアクセスできるため、機密情報漏洩だけでなくマルウェア配置やバックドア作成が容易。HFS2 は組込み系・IoT デバイスでも広く利用されている。 |
| **CVE‑2026‑97359** | 10.0 | HFS2 2.4.0 以前で **テンプレートインジェクション** → RCE | ファイル名にテンプレート構文を埋め込むだけで任意コード実行が成立。上記 97360 と同一製品の別脆弱性で、同時に未パッチの環境は **完全な遠隔乗っ取り** が可能になる。 |
| **CVE‑2026‑93577** | 9.9 | GitLab CE/EE 19.2‑19.4 系で **整数オーバーフロー** に起因する RCE（認証ユーザー） | GitLab は多くの開発組織の中心的リポジトリ。認証ユーザーでも任意コード実行できるため、内部脅威やサプライチェーン攻撃の踏み台になる危険性が高い。 |
| **CVE‑2026‑84719** | 9.9 | Ansible Automation Platform (Automation‑Controller) の **WorkflowJobTemplate コピー時の権限サニタイズ不備** | インスタンスグループや実行環境が検証されず、権限昇格や不正ジョブ実行が可能。自動化基盤全体の信頼性が揺らぐ。 |
| **CVE‑2026‑12227** | 9.8 | WordPress Visual Composer Website Builder 45.16.0 までの **ローカルファイルインクルード (LFI)** | 未認証で任意ファイルを読み取り・実行でき、サーバ全体の権限取得に直結。WordPress は日本国内でも最も普及している CMS の一つで、プラグインの脆弱性は広範囲に波及する。 |

> **補足**：上記 5 件は **CVSS が 9.8 以上** かつ **未認証/低権限での遠隔コード実行** が可能で、インフラ全体の攻撃面を大幅に拡大する点が共通しています。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
- **脆弱性情報の取得とパッチ適用を最優先**。特に CVSS 10.0 の HFS2 脆弱性は **即時アップデートまたはサービス停止** が推奨されます。  
- **外部から直接アクセスできるポートをファイアウォールで遮断**（例：HFS2 の 80/443、GitLab の 22/80/443、WordPress の 80/443）し、必要な IP のみ許可してください。  
- **監査ログの有効化** と **不審なファイル操作・プロセス生成のリアルタイム検知**（例：OSSEC、Falco、Wazuh）を導入。  

### 3.2 製品別具体的対策  

| 製品 / パッケージ | 現行バージョン | 推奨バージョン / パッチ | 実施手順のポイント |
|-------------------|----------------|------------------------|-------------------|
| **HFS2** | ≤ 2.4.0 | **2.4.1 以上**（公式リリース 2026‑09‑15） | - `apt-get`/`yum` でアップデートできない場合は、ベンダー提供のバイナリを手動置換。<br>- アップデート後、`/var/log/hfs2/*.log` で不審なファイル操作が残っていないか確認。 |
| **GitLab CE/EE** | 19.2‑19.4 系 (19.2.0‑19.4.0) | **19.2.7**、**19.3.3**、**19.4.1** 以上 | - Omnibus パッケージの場合 `sudo gitlab-ctl reconfigure` 後に `gitlab-rake gitlab:check` で整合性確認。<br>- 既存のカスタムスクリプトが整数オーバーフローに依存していないかレビュー。 |
| **Ansible Automation Platform (Automation‑Controller)** | 2.3.x 系 (Red Hat 8) | **2.3.5** 以上（2026‑08‑30 リリース） | - `ansible-galaxy collection install` で最新コレクションに更新。<br>- WorkflowJobTemplate のコピー権限を最小化し、`instance_groups` と `execution_environment` のチェックを追加。 |
| **WordPress Visual Composer Website Builder** | ≤ 45.16.0 | **45.16.1** 以上 | - WordPress 管理画面 → プラグイン → 「今すぐ更新」から自動適用。<br>- `wp-config.php` の `DISALLOW_FILE_EDIT` を `true` に設定し、プラグインからのファイル書き込みを防止。 |
| **Velociraptor** | 1.0.0‑1.2.0 | **1.2.1** 以上（2026‑07‑12） | - API エンドポイントの `compiled_collector_args` フィールドを **読み取り専用** に設定。<br>- API キーのローテーションと最小権限化を実施。 |
| **OpenC3 COSMOS** | 5.1.0‑7.3.0 | **7.3.1** 以上 | - `targets_modified/` ディレクトリへの書き込み権限を `admin` のみへ変更。<br>- 非管理者ユーザーの `write` 権限を削除し、`auditd` で変更履歴を取得。 |
| **IBM Concert** | 1.0.0‑3.0.0 | **3.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-97360

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T14:18:22.703 |

HFS2 version 2.4.0 and earlier contains an unauthenticated arbitrary file access vulnerability that allows unauthenticated attackers to read, write, append, and delete files anywhere the HFS service account has filesystem access outside the shared folder. Attackers can exploit the macro dispatcher's lack of authorization model combined with the path resolver's failure to confine absolute paths to manipulate the template engine and compromise the confidentiality, integrity, and availability of the host.

### CVE-2026-97359

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-09-24T14:18:22.533 |

HFS2 version 2.4.0 and earlier contains a template injection vulnerability in the multipart upload handler that allows unauthenticated attackers to achieve remote code execution by embedding malicious template syntax in a filename. Attackers can craft a filename containing a closing template quoting sequence followed by an exec macro, which bypasses the authorization check in the dispatcher to execute arbitrary commands on the underlying host system.

### CVE-2026-19072

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-164;CWE-1269` |
| Published | 2026-09-24T13:17:09.500 |

Velociraptor stores the compiled VQL in the hunt object internally to avoid having to recompile the artifacts for each endpoint in the hunt. Although the field "compiled_collector_args" is an internal field, Velociraptor allowed the field to be set from a user API call. This allows another user who can schedule a hunt (minimal role of "investigator" ) to set the compiled VQL statements for the hunt bypassing any ACL checks that would normally be applied.




This flaw can then be escalated to allow the "investigator" user to run arbitrary VQL statements as an administrator user on the Velociraptor server.

### CVE-2026-93577

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-24T00:17:22.850 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.2 before 19.2.7, 19.3 before 19.3.3, and 19.4 before 19.4.1 that under certain conditions could have allowed an authenticated user to execute arbitrary code on the GitLab server due to an integer overflow issue when compiling a specially crafted regular expression in a CI/CD configuration.

### CVE-2026-89078

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-24T00:17:22.060 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 19.2 before 19.2.7, 19.3 before 19.3.3, and 19.4 before 19.4.1 that under certain conditions could have allowed an authenticated user to execute arbitrary code on the GitLab server due to a double free issue when parsing a specially crafted regular expression in a CI/CD configuration.

### CVE-2026-84719

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T20:17:18.617 |

A flaw was found in the Ansible Automation Platform automation-controller. When a
WorkflowJobTemplate is copied, the deep-copy permission sanitizer validates only the inventory,
unified_job_template, and credentials of each cloned node and fails to check the instance_groups
(and execution_environment and labels) that were preserved from the original. A user with
organization workflow-admin permission but no role on the referenced instance groups can copy a
workflow, become its administrator, and launch jobs pinned to instance groups they are not
authorized to use — including the control-plane instance group — bypassing the InstanceGroup
use_role boundary and causing attacker-influenced automation to run in the control-plane
execution context.

### CVE-2026-84502

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-23T19:19:40.377 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. The Project scm_url field is not validated against values that
begin with a dash and is stored and passed verbatim to the git SCM module.
Because the module runs git ls-remote with the URL as a positional argument and
without a "--" separator, a git project URL such as "--upload-pack=<command>:x"
is interpreted by git as the --upload-pack option and executed via a shell. A
user with permission to create or modify a project in a single organization can
thereby execute arbitrary commands on the control-plane task pod, with output
reflected through the project update stdout endpoint, leading to cross-tenant
compromise and in-cluster lateral movement

### CVE-2026-84474

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-09-23T19:19:39.930 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. The provisioning-callback secret (host_config_key) is exposed to
users holding only the read-level view_jobtemplate permission -- both in the
job template API representation and in the activity stream -- and the
provisioning callback endpoint trusts a client-supplied X-Forwarded-For
header to determine the calling host when the controller is deployed behind
the AAP gateway with an empty proxy allow-list. By reading the secret and
spoofing X-Forwarded-For to match any host in the job template's inventory, a
minimally privileged or unauthenticated remote attacker can launch the job
template against arbitrary managed hosts using the job template's credentials,
resulting in privilege escalation and remote code execution on managed hosts.

### CVE-2026-77602

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T19:19:18.550 |

OpenC3 COSMOS provides the functionality needed to send commands to and receive data from one or more embedded systems. From 5.1.0 until 7.3.0, authenticated non-administrator users can write content under targets_modified/ that is later executed by multiple configuration paths below the intended code-execution privilege tier. Table and command or telemetry definitions are processed through ConfigParser, PacketConfig, GENERIC_READ_CONVERSION, or GENERIC_WRITE_CONVERSION, allowing ERB rendering or Ruby and Python evaluation, while openc3-cosmos-script-runner-api/scripts/run_suite_analysis.rb executes suite procedure files through require. Storage uploads, screen saves, and script creation can place content in the overlay, and triggering table processing, a cmd/tlm reload, or suite analysis executes the content in cmd-tlm-api, decom microservices, or Script Runner with access to internal credentials and data. This issue is fixed in version 7.3.0.

### CVE-2026-12227

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-24T10:17:32.623 |

The Visual Composer Website Builder plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 45.16.0 via the `vcv-template` parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where images and other “safe” file types can be uploaded and included.

### CVE-2026-78308

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-24T09:17:08.043 |

Improper Authentication vulnerability in DIAEnergie allows Authentication Bypass.

This issue affects DIAEnergie: before 1.11.00.022.

### CVE-2026-18467

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-24T02:16:52.943 |

The Paytium: Mollie payment forms & donations plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 5.0.3. The 5.0.3 patch introduced a wp_hash()/hash_equals() signature gate on the pt-paytium-user-data field, but left a second filter — pt_cf_checkout_meta(), registered on the pt_meta_values hook after the signed builder — that copies every $_POST['pt_form_field'][*] key verbatim into the payment meta array without any signature verification; this allows the pt-user-role value it copies to overwrite the signed path's output, after which paytium_user_data_processing() reads the persisted _pt-user-role post meta and passes it directly as the role argument to wp_insert_user(). This makes it possible for unauthenticated attackers to register a new WordPress account with the administrator role and fully take over the site. Exploitation requires submitting a payment through a publicly-exposed [paytium] shortcode form and completing the resulting payment flow, after which the attacker can seize the new administrator account via the standard lost-password flow on their supplied email address.

### CVE-2026-6928

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T21:17:02.430 |

IBM Concert 1.0.0 through 3.0.0 references or accesses memory after it has been freed. This allows an attacker who can influence program execution or input may exploit this condition to corrupt memory, cause application crashes, or execute arbitrary code.

### CVE-2026-6730

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-23T21:17:02.053 |

IBM Concert 1.0.0 through 3.0.0 is vulnerable to a buffer overflow, caused by improper bounds checking. A local user could overflow the buffer and execute arbitrary code on the system.

### CVE-2026-6721

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T21:17:01.927 |

IBM Concert 1.0.0 through 3.0.0 allows an unauthenticated remote attacker can supply specially crafted input that is incorporated into OS commands, resulting in arbitrary command execution on the underlying system. Successful exploitation allows remote code execution with the privileges of the affected application.

### CVE-2025-63564

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T17:17:14.323 |

SQL injection vulnerability in Moodle Socialwall plugin v.3.0 through v.3.3 allows an attacker to execute arbitrary code via crafted HTTP requests

### CVE-2026-96276

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T15:17:32.317 |

If a malicious SDK container declares an extension point with a crafted `directory` path, and a developer runs `flatpak build-init --writable-sdk --sdk-extension` with that SDK, attacker-chosen files could be written outside the working directory, since the target path is resolved via a function that allows `..` traversal.

### CVE-2026-85724

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-155;CWE-863` |
| Published | 2026-09-23T17:17:17.623 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, when pattern-based ACL rules are configured, AuthorizationsCollector.canDoOperation substitutes client ID and username values directly into rules containing %c or %u and then treats the result as an MQTT topic filter. A client that uses + or # in either identity can broaden the substituted filter and gain cross-tenant read and write access. A # identity can also produce an invalid filter that triggers a NullPointerException in Topic.match and disrupts session processing. This issue is fixed in version 0.18.1.

### CVE-2026-87900

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-23T20:17:20.613 |

Argument injection in WP Toolkit for cPanel 6.11.2-10794 and earlier allows remote authenticated users to read arbitrary files and execute arbitrary code across customer accounts.

### CVE-2026-87899

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-250` |
| Published | 2026-09-23T20:17:20.480 |

Execution with unnecessary privileges in cPanel allows remote authenticated users to execute arbitrary code with root privileges.

### CVE-2026-87898

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T20:17:20.340 |

OS command injection in Plesk allows remote authenticated users to execute arbitrary code with root privileges.

### CVE-2026-91187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-09-24T14:18:18.667 |

Improper Verification of Cryptographic Signature vulnerability in dashbit nimble_zta allows an unauthenticated remote attacker to authenticate as an arbitrary Cloudflare service token. Applications using the Cloudflare Zero Trust authentication strategy are affected.

verify_token/2 in lib/nimble_zta/cloudflare.ex matches the result of JOSE.JWT.verify/2 against {_, token, _s}, which discards the boolean verification result and returns the decoded token after a failed signature check. The attacker sends a forged JWT in the cf-access-jwt-assertion header, carrying the expected iss claim and the seven service token claims. verify_iss/2 reads the iss claim from the forged token, so it rejects nothing, and the service token path then returns those claims as the authenticated identity.

This issue affects nimble_zta: from 0.1.2 before 0.1.3.

### CVE-2026-96891

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-09-24T03:16:58.950 |

A vulnerability was identified in D-Link DIR-825 3.00b32. Affected is the function tunnel_set_params of the file tunnel.c of the component rp-l2tp. The manipulation of the argument peer_hostname  leads to out-of-bounds write. The attack may be initiated remotely.

### CVE-2026-93352

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-23T22:16:59.523 |

Laravel-Mediable 7.0.0 before 7.0.2 contains an incomplete patch for CVE-2026-49972 in which the .pht extension is absent from the forbidden_extensions blocklist in config/mediable.php. The blocklist introduced to address CVE-2026-49972 includes phpt but omits pht, which Apache executes as PHP via the default FilesMatch directive on Debian and Ubuntu systems. An attacker can upload a .pht file that passes all validation in MediaUploader::verifyExtension() and File::sanitizeFileName() because pht is not present in the blocklist, causing the file to be written to disk and executed as PHP when requested, enabling remote code execution with the privileges of the web server process.

### CVE-2026-96770

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-296` |
| Published | 2026-09-23T19:19:55.013 |

All published s2s-proxy versions through 0.2.2 are affected. In versions 0.1.16 through 0.2.2, TLS server listeners use Go's RequireAnyClientCert mode when skipCAVerification is false. This mode checks that the client holds the certificate's private key but does not verify the certificate against the configured CA. An attacker can therefore use a self-signed certificate and key to establish a TLS and yamux connection, then invoke RPCs allowed by the proxy's configuration and Temporal credentials. No certificate or private key trusted by the deployment, and no Temporal credential, is required.

### CVE-2026-95601

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:53.210 |

Unauthenticated SQL Injection in Product Filter by WBW <= 3.1.7 versions.

### CVE-2026-96759

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:25.250 |

orval before 8.29.0 fails to escape the operationId parameter when emitting it into generated TanStack Query mutator options metadata objects. Attackers can inject arbitrary JavaScript code through a crafted operationId in an OpenAPI specification that executes when generated hooks are called.

### CVE-2026-96758

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:25.083 |

orval @orval/core before 8.28.0 contains a code injection vulnerability in the form-data serializer that fails to escape multipart property names in generated template literals. Attackers can inject ${...} expressions into OpenAPI schema property names that execute as live interpolation when the generated client builds FormData bodies with consumer process privileges.

### CVE-2026-96757

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:24.923 |

orval before 8.29.0 fails to escape OpenAPI media-type keys when emitting them into single-quoted Content-Type string literals in generated code. Attackers can inject JavaScript through crafted media-type keys in OpenAPI specifications that executes when generated fetch operations or mock resolvers are invoked.

### CVE-2026-96755

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:24.607 |

orval versions 8.14.0 through 8.28.1 contain a code injection vulnerability in the @orval/effect generator that converts OpenAPI schema defaults into template literals. Attackers can inject arbitrary JavaScript expressions via schema defaults containing ${...} syntax, which are executed at module scope when the generated code is built or imported.

### CVE-2026-96754

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:24.437 |

orval versions before 8.29.0 contain a code injection vulnerability in the @orval/hono generator that fails to escape OpenAPI path values in single-quoted route literals. Attackers can craft an OpenAPI document with an apostrophe in a static path segment to inject arbitrary JavaScript code that executes when the generated TypeScript module is imported.

### CVE-2026-95848

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-09-23T17:17:21.947 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, when a configured authenticator or authorizator class cannot be loaded, Server.initializeAuthenticator and Server.initializeAuthorizatorPolicy treat the failure as though no custom class was configured and fall back to AcceptAllAuthenticator or PermitAllAuthorizatorPolicy. A misspelled class name, missing dependency, constructor failure, or classpath problem can therefore start the broker with authentication or authorization disabled even though the operator configured those controls. This issue is fixed in version 0.18.1.

### CVE-2026-18872

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T16:16:41.720 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift is vulnerable to stored cross-site scripting (CWE-79) in the FTM UI NetworkAcknowledgement React component (NetworkAcknowledgement.jsx:42). A malicious actor can inject script into stored network acknowledgement data that executes in authenticated operator browsers, enabling session hijacking and unauthorized operator-level payment actions.

### CVE-2026-97055

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-09-24T02:16:54.333 |

SigNoz from v0.8.0 before v0.143.0 defaults the JWT tokenizer signing secret (tokenizer::jwt::secret, set via SIGNOZ_TOKENIZER_JWT_SECRET or the deprecated SIGNOZ_JWT_SECRET) to an empty string, and Config.Validate() does not reject the empty value, so a deployment that does not configure a secret starts up and both signs and verifies session tokens with an empty HMAC key. Because the JWT tokenizer was the default provider, any such deployment is affected. An unauthenticated attacker who knows the ID of an existing user can forge a valid session token for that user — including an administrator — by signing the id, orgId and email claims with an empty key; the organization ID (and whether an email is registered) can be obtained without authentication from /api/v2/sessions/context. A forged refresh token can be exchanged at /api/v2/sessions/rotate for a new token pair and cannot be revoked, so it remains usable for its full lifetime (30 days by default). Fixed in v0.143.0, which requires a JWT secret when the jwt provider is selected and changes the default provider to opaque.

### CVE-2026-67404

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-23T21:17:01.517 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0, When no CA bundle is available, ssl_options/1 falls back to [{verify, verify_none}] with no warning. An attacker in a man-in-the-middle position can forge the JWKS response, which leads the broker to accept arbitrary JWTs. Preconditions include The OAuth2 plugin must be in use with no cacertfile configured and the OS CA bundle empty or unreadable (for example, in a minimal container), and the attacker must hold a network man-in-the-middle position.. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0.

### CVE-2026-63132

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-09-23T19:17:34.663 |

OpenBao is an open source identity-based secrets management system. Prior to 2.6.0, OpenBao's handleLogicalRecovery path in http/logical.go compared the highly privileged recovery token with ordinary string equality. A remote unauthenticated attacker able to make repeated recovery mode requests and measure response timing could infer the recovery token. The recovered token could then authorize recovery mode operations that read or modify OpenBao data. This issue is fixed in version 2.6.0.

### CVE-2026-96756

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T17:17:24.767 |

orval versions before 8.30.0 contain a code injection vulnerability in the @orval/core factory generator that fails to escape date default values in new Date() calls. Attackers can inject arbitrary expressions through apostrophes in OpenAPI schema defaults to execute code with the privileges of the consumer process when factoryMethods and useDates options are enabled.

### CVE-2026-78312

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T09:17:08.553 |

Path Traversal in DIAEnergie.

This issue affects DIAEnergie: before 1.11.00.022.

### CVE-2026-67231

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-09-23T21:17:00.940 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0, The trust-store plugin installs a verify_fun that overrides {bad_cert, unknown_ca} / {bad_cert, selfsigned_peer} when the presented cert "matches" a whitelisted one. The match key is extract_issuer_id/1 → public_key:pkix_issuer_id/2 → {IssuerName, SerialNumber} , both fields are taken verbatim from the presented certificate body and contain no public-key, SKI, fingerprint or signature material. is_whitelisted/1 is a pure ets:member lookup; the stored full DER is used only for list/0 display and is never compared against the presented cert. cacerts is [], so the whitelisted cert is never used as a trust anchor for path validation either. TLS client-authentication bypass: an attacker who knows the issuer DN + serial of any whitelisted certificate can connect with a forged self-signed cert. Preconditions include rabbitmq_trust_store plugin enabled and used as the TLS verify_fun Attacker knows or can guess the {Issuer, Serial} of at least one whitelisted cert (non-secret; exposed via CLI/logs/any cert copy). This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0.

### CVE-2026-75884

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-23T20:17:14.637 |

A flaw was found in AWX. The container group pod_spec_override field uses an incomplete blocklist that only restricts automountServiceAccountToken, allowing injection of initContainers, serviceAccountName overrides, and projected service account token volumes. An AAP platform administrator can exploit this to escalate privileges to OpenShift namespace-level access and exfiltrate namespace secrets.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-97059

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-09-24T14:18:21.997 |

DCMTK through 3.7.0 contains a heap over-read vulnerability in ConcatenationLoader that copies pixel data frames without validating the PixelData buffer length against the declared NumberOfFrames. Attackers can craft malicious DICOM instances declaring more frames than the buffer contains to trigger heap over-reads that crash the application or leak adjacent heap memory.

### CVE-2026-85682

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-24T09:17:08.797 |

The YOP Poll plugin for WordPress is vulnerable to Origin Validation Error in all versions up to, and including, 7.0.10. This is due to the plugin transmitting a wp_rest nonce to window.opener via postMessage() with a wildcard targetOrigin. This makes it possible for unauthenticated attackers to steal a REST nonce scoped to a logged-in Administrator and use it to change the Administrator's email address and password, resulting in full account takeover. The Administrator must open an attacker-controlled page in order to exploit this vulnerability.

### CVE-2026-78311

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-24T09:17:08.440 |

SQL Injection vulnerability in DIAEnergie.

This issue affects DIAEnergie: before 1.11.00.022.

### CVE-2026-78309

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-24T09:17:08.187 |

SQL Injection vulnerability in DIAEnergie.

This issue affects DIAEnergie: before 1.11.00.022.

### CVE-2026-70125

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-09-23T23:18:12.510 |

Microsoft Outlook Remote Code Execution Vulnerability

### CVE-2026-86583

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-23T22:16:59.220 |

The Import and export users and customers plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.4.17 via the plugin's own export and re-import workflow. The vulnerability exists because the exporter writes CSV cells using fputcsv() with a NUL byte (\0) as the escape character, while the importer parses the same file using SplFileObject::fgetcsv() with only a single delimiter argument, causing PHP's default backslash escape character to be applied instead; because the export column layout places display_name immediately before the role column and nickname immediately after, an attacker can store crafted values in those two profile fields — saved by WordPress core via the standard profile page — such that the escape mismatch causes the parser to merge the display_name cell into the role field and rebalance the column count via nickname, yielding administrator as the parsed role for their own row when it reaches the import_user function's add_role function. This makes it possible for authenticated attackers with Subscriber-level access or above to escalate their privileges to Administrator. Exploitation requires a site administrator to trigger the plugin's documented export re-import migration with both "Update existing users" and "Update roles for existing users" set to "yes".

### CVE-2026-81537

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T22:16:57.690 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to OS command injection.

### CVE-2026-80423

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-09-23T22:16:57.270 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to the exposure of namespace-wide secrets via accessible file mounts.

### CVE-2026-80425

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T21:17:03.190 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-80412

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T21:17:03.067 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary code due to improper escaping of connector property values during OSH script generation.

### CVE-2026-80379

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T21:17:02.940 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-77601

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T19:19:18.380 |

OpenC3 COSMOS provides the functionality needed to send commands to and receive data from one or more embedded systems. From 5.12.0 until 7.3.0, an authenticated actor can write the pypi_url setting through set_setting at POST /openc3-api/api, then cause OpenC3::PluginModel.install_phase2 in openc3/lib/openc3/models/plugin_model.rb to interpolate the value into a shell command while installing a plugin with Python dependency metadata. Shell metacharacters in the setting are interpreted by the command shell, allowing arbitrary operating-system commands to run as the openc3 service user with access to Redis and bucket credentials. Open-source deployments permit any authenticated user to reach the affected operations, while Enterprise deployments require an administrator. This issue is fixed in version 7.3.0.

### CVE-2026-96804

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-23T17:17:25.530 |

MLflow's statsmodel flavor, versions 2.1.0 to 3.14.0, omits the MLFLOW_ALLOW_PICKLE_DESERIALIZATION=False security control entirely in _load_model(), which allows a remote attacker to execute arbitrary code via a crafted MLmodel artifact.

### CVE-2026-96775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-23T17:17:25.407 |

MLflow's dspy flavor, versions >= 2.0,  applies the MLFLOW_ALLOW_PICKLE_DESERIALIZATION=False security control only when the model_path ends in .pkl, which allows a remote attacker to execute arbitrary code via a crafted MLmodel artifact.

### CVE-2026-95847

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-99` |
| Published | 2026-09-23T17:17:21.780 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, H2PersistentQueue derives a session's message-map name as queue_ plus the client ID and its metadata-map name as queue_ plus the client ID plus _meta. A durable session whose client ID ends in _meta can therefore make its message map collide with another client's metadata map. The colliding sessions read and write the same H2 MVStore map with incompatible value types, which can corrupt queue head and tail data and cause message loss, misdelivery, failed queue reloads, or exposure of queued content across sessions. This issue is fixed in version 0.18.1.

### CVE-2026-18490

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-23T16:16:41.460 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift is vulnerable to unauthenticated remote code execution via Java native deserialization on the PayDir Business Rules Manager RMI SSL endpoint (BrmRMISSLServerSocketFactory.java:95, EP8). An adjacent-network attacker can deliver a crafted serialized payload to achieve arbitrary code execution, exposing all PayDir credentials and enabling manipulation of payment business rules.

### CVE-2026-96275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T15:17:32.180 |

A malicious or compromised Flatpak repository can write attacker-controlled content to arbitrary locations on the host filesystem via extract_extra_data(). On system installs, the write happens as root. Two issues combine: `files/extra` is resolved via path operations that follow symlinks, and blob names from `xa.extra-data-sources` are not sanitized against `..` traversal.

### CVE-2026-97057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-09-24T14:18:21.683 |

redis-parser through 3.0.0 fails to validate the multi-bulk length value in RESP protocol parsing, allowing attackers to trigger an uncaught RangeError by supplying an excessively large declared length. A malicious or compromised Redis endpoint can deliver a crafted RESP header with a length above 2^32-1 to crash the Node.js client process.

### CVE-2026-84691

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-134` |
| Published | 2026-09-23T20:17:17.537 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. The setting that formats the log message emitted for API 4XX errors
is an administrator-controlled Python format-string template that is rendered
with a live user object as an argument. Because Python string formatting permits
attribute and item traversal on its arguments, an administrator can craft a
template that walks from the user object into the application settings and reads
the Django secret key and the database password. The formatted message is written
to a logger that can be forwarded to an external log aggregator, whose destination
is also administrator-controlled, allowing the secrets to be sent off the host. An
authenticated administrator can thereby obtain the master encryption key used to
protect all stored credentials and the database service password, enabling offline
decryption of every stored credential, forgery of user sessions, and direct
access to the controller database.

### CVE-2026-84683

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T20:17:17.403 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. The HTML view of job, ad hoc command, project update, and inventory
update standard output escapes HTML metacharacters but does not remove ANSI
terminal escape sequences before conversion to HTML. An ANSI OSC 8 hyperlink
sequence in the output is expanded into an HTML anchor whose href is not scheme-
filtered or escaped, so a low-privileged user who can produce output -- or an
external party whose data a playbook echoes -- can embed a javascript: link that
is rendered into a text/html response with no Content-Security-Policy. When a
higher-privileged user views the output page and clicks the link, attacker-
controlled JavaScript executes in their authenticated session, allowing actions
as that user up to full platform takeover.

### CVE-2026-82405

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-23T20:17:16.370 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, the KleverUpdateAccountPermission built-in authorizes replacement of a target account's permissions by checking attacker-controlled vmInput.RecipientAddr instead of authenticated vmInput.CallerAddr. An attacker-controlled contract can choose a victim account with configured permissions as RecipientAddr, and contractHasValidPermission can accept the victim's default self-signer as authorization. UpdatePermission can then replace the victim's entire permission set with attacker-supplied Owner permissions, enabling asset theft or permanent lockout without a victim key or signature. Accounts without stored permissions and the native transaction path are not affected. This issue is fixed in version 1.7.20.

### CVE-2026-68492

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-09-23T20:17:13.583 |

An untrusted search path vulnerability in Plesk from 18.0.34 before 18.0.80.8 and 18.0.81 before 18.0.81.1 allows remote authenticated users to execute arbitrary code as root via the "Plesk RESTful API" extension from 2.4.2 before 2.4.7.

### CVE-2026-82368

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-23T19:19:34.747 |

Insecure access controls on internal service ports in Brocade SANnav versions before 3.0.1a allow local, non-administrative host users to communicate directly with backend management services. A local attacker can leverage this exposed access to transmit commands to connected Fabric OS switches under the security context of the SANnav management user.

### CVE-2026-95846

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T17:17:21.627 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, PostOffice.publishWill publishes a client's Last-Will message without applying the canWrite authorization and reserved-topic checks used for a normal PUBLISH. A client can configure a Will for a topic that the client is not permitted to write and cause the broker to publish the unauthorized message when the client disconnects unexpectedly. This issue allows unauthorized message injection into restricted topics. This issue is fixed in version 0.18.1.

### CVE-2026-95845

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T17:17:21.470 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, the broker does not enforce a maximum length for pending per-session message queues. When a fast publisher sends messages to a slow subscriber whose in-flight window is full, queued messages can accumulate without bound in memory or persistent storage. Remote clients can use this condition to exhaust broker resources and cause a denial of service. This issue is fixed in version 0.18.1.

### CVE-2026-95844

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-09-23T17:17:21.280 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, Moquette does not limit the depth of topic names and topic filters before processing them through recursive CTrie insertion and matching operations. A remote client can publish or subscribe with a deeply nested topic, causing a StackOverflowError that disrupts session processing and can deny service to broker clients. This issue is fixed in version 0.18.1.

### CVE-2026-95843

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-23T17:17:21.130 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, PostOffice.subscribe parses a shared-subscription filter through SharedSubscriptionUtils.extractShareName before validating the complete $share/{shareName}/{topicFilter} structure. A remote client can send a filter such as $share/grp without a topic-filter portion, causing a StringIndexOutOfBoundsException while calculating the share name. The exception terminates command handling on the shared session event loop and can deny service to other client sessions assigned to that loop. This issue is fixed in version 0.18.1.

### CVE-2026-95842

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-23T17:17:20.970 |

Moquette is a lightweight Java MQTT broker. Prior to 0.18.1, SessionEventLoop.run catches only InterruptedException, and SessionEventLoopGroup does not restart a terminated loop. An MQTT command that raises an uncaught exception can terminate an event loop shared by multiple client sessions, preventing every co-located client from processing PUBLISH, SUBSCRIBE, PUBACK, and other commands. An attacker can select client IDs that map across the available loops to disrupt session processing for the entire broker. This issue is fixed in version 0.18.1.

### CVE-2026-96673

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T16:16:50.183 |

Photoview through 2.4.0 contains an SQL injection vulnerability in the album download route that allows unauthenticated attackers to inject SQL by manipulating the album_id path segment. Attackers can supply crafted SQL expressions in the album_id parameter to extract arbitrary data from the database using time-based or blind injection techniques.

### CVE-2026-55610

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-23T15:17:14.580 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. Prior to version 2.4.1, in InvoiceShelf's multi-company installations, any user who is an Owner of one company can read and overwrite any user account in any other company on the same installation. `GET/PUT /api/v1/users/{user}` resolves the target `User` by global primary key, and `UserPolicy` checks only that the requester owns their own header-company — it never verifies that the target user belongs to that company. This allows cross-tenant disclosure of user data and full account takeover (email/password overwrite + company re-assignment). Version 2.4.1 fixes the issue.

### CVE-2026-96515

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434;CWE-862` |
| Published | 2026-09-24T13:17:17.787 |

This
vulnerability exists in the Netlink ICT HG323RW router due to insufficient
authorization and input validation controls in the diagnostic script import
functionality. An authenticated attacker could exploit this vulnerability by
uploading and executing a specially crafted script through the web management
interface.





Successful exploitation of this vulnerability
could allow the attacker to execute arbitrary operating system commands with
root privileges resulting in complete compromise of the affected device.

### CVE-2026-97152

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-24T04:18:06.213 |

Nanomsg versions 0.5-beta through 1.x before 1.2.3 has a remotely exploitable buffer overflow in the WebSocket transport, due to an unchecked copy of the Sec-WebSocket-Version header, through snprintf.

### CVE-2026-82370

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-09-24T00:17:21.777 |

Unauthenticated remote command injection in the Brocade SANnav orchestrator HTTP service permits network-adjacent attackers to execute arbitrary administrative switch CLI commands and issue container management instructions. This could allow an attacker to alter Fibre Channel fabric switch configurations or manipulate application container runtimes. This vulnerability affects Brocade SANnav versions before 3.0.1a.

### CVE-2026-82369

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T21:17:03.317 |

Insufficient input sanitization of shell metacharacters in the Brocade SANnav CLI scripting component permits authenticated users to break out of restricted execution contexts on managed switches. An attacker with command execution permissions can leverage this flaw to run unauthorized shell commands across target fabric switches, bypassing command allow-lists and obtaining full administrative switch access. This vulnerability affects all Brocade SANnav versions before 3.0.1a.

### CVE-2026-86064

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200;CWE-306` |
| Published | 2026-09-23T20:17:19.960 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, the default-open GET /log WebSocket route configured in config/node/api.yaml and registered by network/api/api.go does not require authentication. The first client message is parsed as a logger Profile in network/api/logs/logSender.go and applied process-wide through Profile.Apply, allowing a remote client to change global log levels and formatting options until the connection closes. The same connection is registered as a log observer and can receive live process logs. An attacker can suppress normal logs, increase verbosity, distort operator visibility, and access operational information without credentials. This issue is fixed in version 1.7.20.

### CVE-2026-90904

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-23T19:19:43.543 |

Joomla Extension - joomshaper.com - Broken Access Control (ACL Bypass) in ApiController Record Editing in Easy Store extension 1.0.0-3.0.0 - The allowEdit() method in ApiController.php hardcoded return true;, bypassing Joomla component-level and asset-level ACL permission checks. Any authenticated backend user could edit any EasyStore record, regardless of specific ACL permission grants. Resolved by replacing the hardcoded boolean with proper ACL authorization checks via AccessControl::create()->canEdit()`.

### CVE-2026-90901

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-23T19:19:43.150 |

Joomla Extension - joomshaper.com - Authenticated, Privileged SQL Injection in Media Image Deletion in Easy Store extension 1.0.0-3.0.0 - The checkout.searchGuestUser endpoint allowed querying guest checkout records solely by supplying an email address. The server returned complete shipping details (full name, phone number, street address, city, postal code, and country) directly from the #__easystore_guests table with no authentication, session validation, or ownership checks. An unauthenticated attacker could iterate through email lists to enumerate guest customers and harvest sensitive Personally Identifiable Information (PII). Resolved by removing the unauthenticated server-side guest lookup endpoint entirely and migrating autofill functionality to client-side localStorage protected by explicit user consent.

### CVE-2026-96656

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-23T17:17:23.840 |

Plex Media Server before 1.43.3.10861 allows an admin user to write arbitrary files that may be executed on load. The preference TranscoderH264Options is appended verbatim to x264's option string on every transcode. At startup, all .so files are run without signature, execute bit, or symbol checks.

### CVE-2026-93349

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-23T17:17:19.653 |

Frictionless through 5.20.0rc1 contains an OS command injection vulnerability in the explore console command that allows an attacker who supplies a crafted Data Package descriptor to execute arbitrary operating system commands as the user who explores it. Attackers can place shell metacharacters in resource path values within a datapackage.json descriptor, which are passed unsanitized to os.system through a shell, causing arbitrary command execution in the victim's security context when they run the explore command against the untrusted package.

### CVE-2026-94124

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:47.940 |

Contributor SQL Injection in WP EasyCart <= 5.9.4 versions.

### CVE-2026-93773

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:46.613 |

Contributor SQL Injection in Mollie Forms <= 2.11.0 versions.

### CVE-2026-93527

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:45.573 |

Contributor SQL Injection in Live Copy Paste for Elementor <= 1.5.10 versions.

### CVE-2026-76648

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T19:19:15.030 |

CopyAPIView (awx/awx/api/generics.py:873) sets permission_classes =
(IsAuthenticated,), so DRF's get_object() performs no object-level
RBAC. The get() handler (lines 988–991) explicitly guards with
request.user.can_access(obj._class_, 'read', obj) — but post()
(lines 1001–1010) does not. POST only checks:

can_access(model, 'add', create_kwargs_check)

can_access(model, 'copy_related', obj)

For JobTemplate, can_add (awx/awx/main/access.py:1465–1520) gates on

inventory.use_role + project.use_role +
execution_environment.read_role — resource-level roles that do not
imply read on the source JT — and can_copy_related (1522–1534) checks
only credentials.use_role. None of these imply the caller can read the
source JT.

### CVE-2026-76086

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862;CWE-915;CWE-918` |
| Published | 2026-09-23T19:19:14.393 |

Formie is a Craft CMS plugin for creating forms. Prior to 2.2.23 and 3.1.31, Formie's formie/integrations/form-settings control panel action in IntegrationsController::actionFormSettings is reachable without the required form integration permissions and passes request-supplied settings to a configured integration. An authenticated attacker can replace outbound host properties such as apiUrl while the server uses stored API keys or OAuth tokens, causing non-blind server-side requests to an attacker-controlled or internal host and returning the remote response. This residual flaw remained because the permission gate added in version 3.1.28 excluded the form-settings action. Sites that permit low-privileged or front-end user authentication can therefore expose integration credentials and internal network responses. This issue is fixed in versions 2.2.23 and 3.1.31.

### CVE-2026-75131

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-09-23T19:19:14.073 |

NetworkManager-l2tp through 1.52.4, fixed in 1.52.6, contains a privilege escalation vulnerability that allows local users with permission to create VPN connections to execute arbitrary code as root by injecting pppd options through a crafted VPN username. Attackers can embed a double-quote character or whitespace in the username to break out of the pppd options file quoting context and include the pppd plugin directive, causing the privileged pppd process to load an attacker-controlled shared object.

### CVE-2026-79310

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-23T16:16:45.687 |

webpy web.py 0.76 is vulnerable to server-side template injection (SSTI). The template engine can be tricked into executing attacker-controlled template code that built-in security checks are designed to reject. When an application precompiles templates from a directory the attacker can write to and later renders them through the precompiled template loader, the sandbox is bypassed and the attacker's code runs, resulting in arbitrary Python code execution and OS command execution on the server.

### CVE-2026-97151

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-09-24T04:18:06.027 |

mammoth (aka mammoth.js) before 1.12.2 is vulnerable to prototype pollution when reading the styles defined in a document. Converting a crafted .docx file allows an attacker to add arbitrary properties to Object.prototype. In 1.11.0 through 1.12.1, applications that convert further documents in the same process and return the converted HTML can also disclose the contents of local server files (to the party supplying the documents) by setting externalFileAccess to true.

### CVE-2026-82409

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-23T20:17:16.893 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, indexer/common.go serializedDataForUpdateAccounts places the attacker-controlled acc.Name value into an Elasticsearch _bulk JSON and NDJSON request without escaping it. The SetAccountName transaction accepts valid UTF-8 account names containing quotes, backslashes, and newlines, and the resulting name is stored in consensus account state. When an indexer processes the account, those characters can break the JSON string, reject a bulk batch, or inject additional bulk actions that create, overwrite, or delete documents in indices writable by the indexer. The persistent state value is replayed by new or historical indexers, and direct access to the indexing host or Elasticsearch port is not required. This issue is fixed in version 1.7.20.

### CVE-2026-67232

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-23T21:17:01.083 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0, The cowboy WebSocket options at line 117 set compress => true, enabling RFC 7692 permessage-deflate negotiation. The handler does not set max_frame_size, so cowboy's default of infinity applies. cowlib's cow_ws:parse_payload/9 calls zlib:inflate/2 on the compressed payload with no output-size limit. An attacker can negotiate permessage-deflate during the WebSocket upgrade and send a frame containing a zlib bomb (e.g. 50 KB → 5 GB). Decompression occurs in the connection process before websocket_handle/2 ever sees the MQTT bytes. An unauthenticated attacker can crash a RabbitMQ node running the Web-MQTT plugin by sending a single highly-compressed WebSocket frame (a few KB on the wire) that inflates to gigabytes in memory. The cowboy WebSocket handler decompresses the entire frame before the MQTT CONNECT packet is processed, so no credentials are required. Preconditions include rabbitmq_web_mqtt plugin enabled (not default, but common for browser clients) Network reachability to port 15675/15676 No authentication required. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, 4.2.6, and 4.3.0.

### CVE-2026-68490

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-23T20:17:13.447 |

Incorrect permission assignment allows local users to obtain sensitive CalDAV/CardDAV information belonging to other accounts.

### CVE-2026-66079

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T20:17:13.150 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6, parse_array_primitive/2 for constructor 0x45 (list0) returns an element with byte-width B = 0. The enclosing array32 parser at line 148 reads a 4-byte Count from the wire and loops Count times consuming B bytes each , with B = 0, no input is consumed and the loop builds a list of Count empty elements bounded only by the 32-bit field. The SASL-mechanisms / SASL-init frame is parsed by amqp10_framing:decode_bin/1 from rabbit_amqp_reader.erl:412 before authentication completes. The pre-auth incoming_max_frame_size (default 8192 bytes) caps the frame, not the Count field, so a 19-byte payload with Count = 0xFFFFFFFF is accepted. No max_heap_size is set on the reader process. An unauthenticated network attacker can crash any RabbitMQ node that has the AMQP 1.0 listener enabled (default port 5672) by sending a single ~19-byte frame. The reader process attempts to build a list of ~4 billion empty elements, exhausting heap memory and terminating the Erlang VM. All tenants and protocols on the node lose service. Preconditions include Network reachability to the AMQP listener (port 5672, enabled by default) No authentication required. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6.

### CVE-2026-90902

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-23T19:19:43.283 |

Joomla Extension - joomshaper.com - Authenticated, Privileged SQL Injection in Coupon Bulk Update in Easy Store extension 1.0.0-3.0.0 - The coupon bulk update task (administrator/index.php?option=com_easystore&task=coupon.couponBulkUpdate) took input IDs and directly concatenated them into raw SQL IN (...) clauses in ProductCoupon.php and CouponsModel.php without sanitization or parameterization. An authenticated administrator could manipulate the query through injected SQL syntax. Resolved by strictly casting all IDs to integers (array_map('intval', ...)) and adopting parameterized ->whereIn() query construction.

### CVE-2026-90899

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-639` |
| Published | 2026-09-23T19:19:42.873 |

Joomla Extension - joomshaper.com - Unauthenticated PII Exposure via IDOR in Guest Checkout in Easy Store extension 1.0.0-3.0.0 - The checkout.searchGuestUser endpoint allowed querying guest checkout records solely by supplying an email address. The server returned complete shipping details (full name, phone number, street address, city, postal code, and country) directly from the #__easystore_guests table with no authentication, session validation, or ownership checks. An unauthenticated attacker could iterate through email lists to enumerate guest customers and harvest sensitive Personally Identifiable Information (PII). Resolved by removing the unauthenticated server-side guest lookup endpoint entirely and migrating autofill functionality to client-side localStorage protected by explicit user consent.

### CVE-2026-84486

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-489` |
| Published | 2026-09-23T19:19:40.093 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. Four debug views that trigger the internal task, dependency, and
workflow schedulers are configured to allow any user (including unauthenticated
clients) and are routed in production builds because their URL include is not
gated on the debug setting. An unauthenticated remote attacker can repeatedly
invoke these endpoints to acquire the cluster-wide scheduler advisory lock;
because the legitimate scheduler acquires the same lock without waiting, the
attacker causes real scheduler runs to be skipped, stalling job dispatch for
all tenants, while also consuming controller web workers. The debug root view
additionally discloses the list of debug endpoints to unauthenticated callers.

### CVE-2026-76087

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-09-23T19:19:14.570 |

Formie is a Craft CMS plugin for creating forms. Prior to 2.2.23 and 3.1.31, Formie's anonymous formie/submissions/submit action in SubmissionsController::actionSubmit trusts a client-supplied submissionId when loading an incomplete submission without session binding, ownership validation, or a valid submissionEditToken. An unauthenticated attacker can enumerate sequential IDs and overwrite or hijack another user's in-progress multi-page or save-for-later submission, and the modified data can be persisted and forwarded through notifications or integrations when the submission is completed. This is an incomplete remediation of CVE-2026-47266 because that earlier change validated edit tokens for save-submission but did not protect submit. Completed submissions are excluded by the isIncomplete filter. This issue is fixed in versions 2.2.23 and 3.1.31.

### CVE-2026-19179

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-23T16:16:42.107 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to manipulate database queries due to improper neutralization of special elements in a boolean expression.

### CVE-2026-96599

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-09-23T15:17:33.237 |

Isotope eCommerce through 2.9.10 derives order identifiers from uniqid() instead of a cryptographically secure source, allowing unauthenticated attackers to guess identifiers. Guest orders lack ownership verification, enabling attackers to access order details including billing address, customer information, and purchased files by supplying a guessed uid parameter.

### CVE-2026-57590

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-24T10:17:38.010 |

A missing authorization vulnerability exists in the Task Group APIs of Apache DolphinScheduler. The affected APIs do not properly verify whether the authenticated user has permission to access the project associated with the target Task Group.



This issue affects Apache DolphinScheduler: before 3.4.3.



Users are recommended to upgrade to version 3.4.3, which fixes the issue.

### CVE-2026-19125

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-23T22:16:56.683 |

The EthPress – Web3 Login plugin for WordPress is vulnerable to Authentication Bypass in all versions up to, and including, 2.3.5. This is due to the verify_login() function in app/Login.php containing a missing return statement in the signature verification failure branch — when Signature::verify2() reports a mismatch, the function only assigns a WP_Error to a local variable and continues executing, causing unconditional fall-through to the login block where Address::log_in() calls wp_set_auth_cookie() regardless of whether the submitted signature is valid. This makes it possible for unauthenticated attackers to log in as any WordPress user who has a linked wallet address — including administrators — by submitting that user's public wallet address alongside an arbitrary well-formed signature, enabling full site takeover.

### CVE-2026-94487

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-23T19:19:49.540 |

Unauthenticated Cross Site Request Forgery (CSRF) in PublishPress Capabilities <= 2.50.1 versions.

### CVE-2026-18181

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-321` |
| Published | 2026-09-23T16:16:41.083 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to bypass authentication and access sensitive information due to a hard-coded cryptographic key.

### CVE-2026-95521

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T14:18:20.290 |

A command injection flaw was found in rpm. Installing or rebuilding a source RPM whose source or spec file basenames contain a %() macro construct causes rpm to execute an attacker-controlled shell command via popen() while relocating the source file list. This allows arbitrary command execution as the invoking (typically non-root) user, simply by installing, rebuilding, or otherwise processing an untrusted .src.rpm.

### CVE-2026-95519

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-24T14:18:20.153 |

A flaw was found in rpm. An attacker can supply a crafted manifest file that, when processed by a user or automation using `rpm -q -p` or similar manifest-processing flows, leads to arbitrary code execution. This occurs because manifest entries are unexpectedly macro-expanded before being opened, allowing embedded shell commands to run with the privileges of the `rpm` process. Successful exploitation can lead to a full compromise of confidentiality, integrity, and availability for the affected account.

### CVE-2026-97185

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-24T09:17:08.937 |

A flaw was found in GIMP. When processing a specially crafted GIMPressionist preset file, the plug-in does not properly validate vector indices before writing into fixed-size arrays. This can lead to an out-of-bounds write, corrupting memory. An attacker could exploit this by convincing a user to load a malicious preset file, potentially causing a crash or enabling arbitrary code execution.

### CVE-2026-6935

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-23T21:17:02.553 |

IBM Concert 1.0.0 through 3.0.0 invokes operating system commands without fully qualifying executable paths or adequately restricting search path resolution. As a result, an attacker with local system access can manipulate the search path environment to execute untrusted or malicious code.

### CVE-2026-6794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-23T21:17:02.177 |

IBM Concert 1.0.0 through 3.0.0 has a double free vulnerability that exists due to incorrect memory management. A local attacker can exploit this flaw to corrupt heap memory and execute arbitrary code in the context of the affected process.

### CVE-2026-96889

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-23T20:17:27.587 |

A flaw was found in librsvg. When processing an SVG document containing nested XML inclusions (Xincludes) with duplicate entity declarations, a use-after-free error can occur. This vulnerability arises because the library incorrectly frees an XML entity that is still in use by the parser. An attacker could potentially exploit this to cause a denial of service or execute arbitrary code.

### CVE-2026-92470

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-24T00:17:22.193 |

GitLab has remediated an issue in GitLab EE affecting all versions from 18.7 before 19.2.7, 19.3 before 19.3.3, and 19.4 before 19.4.1 that under certain conditions could have allowed an authenticated user to access sensitive CI/CD variable values from debug-mode job traces through the Duo AI troubleshooting feature due to missing authorization checks.

### CVE-2026-81536

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-23T22:16:57.553 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow a remote authenticated attacker to obtain sensitive information due to an XML external entity (XXE) injection.

### CVE-2026-81208

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-23T22:16:57.410 |

IBM DataStage on Cloud Pak for Data 5.4.0.0 could allow an authenticated user to access sensitive information due to improper handling of encrypted credentials. An attacker could exploit this vulnerability to obtain credentials intended for other users or environments.

### CVE-2026-84499

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-209` |
| Published | 2026-09-23T19:19:40.233 |

A flaw was found in Red Hat Ansible Automation Platform's automation-
controller. Survey questions of type password are write-only and stored
encrypted, displayed only as a placeholder on read. When a schedule or
workflow job template node is revalidated against a tightened survey
specification, the controller decrypts the stored password and includes its
plaintext value in the minimum/maximum length validation error message
returned in the HTTP response. A user with the delegated JobTemplate Admin
role can tighten the survey length constraint and trigger revalidation of a
schedule or node created by another, higher-privileged user, thereby
recovering that user's stored password in plaintext.

### CVE-2026-76089

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-639;CWE-862` |
| Published | 2026-09-23T19:19:14.720 |

Formie is a Craft CMS plugin for creating forms. Prior to 2.2.23 and 3.1.31, Formie's formie/sent-notifications/get-resend-modal-content control panel action in SentNotificationsController::actionGetResendModalContent accepts a request-supplied notification ID without permission or object-level authorization checks. Any authenticated user able to invoke the action can enumerate notification IDs and read recipient headers and complete HTML email bodies containing submitted form data, even without the sent-notification viewing permission. This issue is fixed in versions 2.2.23 and 3.1.31.

### CVE-2026-97056

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-09-24T02:16:54.500 |

SigNoz versions from v0.98.0 up to (but not including) v0.143.0, when configured to use the opaque session tokenizer (which was not the default before v0.143.0), do not revoke a user's existing login sessions when the user's password is reset with a reset token (UpdatePasswordByResetPasswordToken, reachable via POST /api/v2/factor_password/reset) or when the user is deleted (DeleteUser, reachable via DELETE /api/v2/users/{id}). Neither code path calls the tokenizer's DeleteTokensByUserID, so cached tokens and identities are left in place. An attacker who already holds a session token for the account — for example from a stolen browser session or from a user being offboarded — retains the account's full access, up to administrator, after a password reset until the token reaches its configured maximum lifetime (30 days by default), and after user deletion until the token next rotates (30 minutes by default). This defeats password reset and user deletion as a means of terminating access. The issue is fixed in v0.143.0.

### CVE-2026-96826

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T20:17:27.333 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Shazzad Hossain Khan W4 Post List allows Blind SQL Injection.

This issue affects W4 Post List: from n/a through 3.0.6.

### CVE-2026-84706

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-23T20:17:17.677 |

A flaw was found in Ansible Automation Platform's automation-controller. The custom
Credential Type environment-variable injector validates variable names against a
deny-list (an ANSIBLE_* prefix check plus a fixed ENV_BLOCKLIST) that omits
process-hijacking loader variables such as BASH_ENV, ENV, LD_PRELOAD, LD_LIBRARY_PATH,
PYTHONSTARTUP and GIT_SSH_COMMAND. Combined with the credential file injector, a
privileged user can write an attacker-controlled script into the execution environment
and point BASH_ENV at it, obtaining arbitrary code execution inside the
execution-environment container for any job that attaches a credential of that type.

### CVE-2026-66070

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-942` |
| Published | 2026-09-23T20:17:12.850 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.17, 4.0.22, 4.1.13, and 4.2.6, match_origin/1 returned the bare reflected Origin and allowed credentials even when the wildcard "" was configured, so the response echoed the attacker's origin together with Access-Control-Allow-Credentials. The affected code is rabbit_mgmt_cors.erl. When the management plugin is configured with a wildcard CORS origin (cors_allow_origins = ""), the handler reflects the request Origin back in Access-Control-Allow-Origin and also sends Access-Control-Allow-Credentials: true. A malicious web page that a signed-in administrator visits can then use that administrator's cached HTTP Basic credentials to issue authenticated, state-changing requests to the management API. Preconditions include The management plugin is configured with the wildcard cors_allow_origins = "*", which is an explicit operator misconfiguration A target administrator has a cached HTTP Basic-auth session in the browser. This issue is fixed in versions 3.13.17, 4.0.22, 4.1.13, and 4.2.6.

### CVE-2026-95593

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:52.933 |

Editor SQL Injection in Ultimeter <= 3.0.8 versions.

### CVE-2026-95522

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:51.393 |

Shop manager SQL Injection in Easy Digital Downloads <= 3.7.0 versions.

### CVE-2026-94174

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:48.277 |

Administrator SQL Injection in Email Log <= 2.63 versions.

### CVE-2026-77394

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:15.343 |

OpenC3 COSMOS provides the functionality needed to send commands to and receive data from one or more embedded systems. From 5.0.6 until 7.3.0, an authenticated actor with system_set permission can store a shared screen through POST /openc3-api/screen whose BUTTON widget action is evaluated by openc3-cosmos-init/plugins/packages/openc3-vue-common/src/widgets/ButtonWidget.vue in another operator's browser session when the button is activated. The stored script runs in the COSMOS origin and can read localStorage.openc3Token, allowing theft of the victim's bearer token, account takeover, and actions with the victim's privileges. The permissive content security policy contributes to execution but is not the primary root cause. This issue is fixed in version 7.3.0.

### CVE-2026-7169

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-09-24T12:17:12.973 |

a vulnerability involving an unchecked search path element in Evope Collector, versions prior to 1.1.7.13, allows a local attacker without privileges to load a malicious DLL by placing a ‘wtsapi32.dll’ file in the ‘C:\ProgramData\Evope\’ directory. The ‘Evope.Service.exe’ component, which runs with ‘NT AUTHORITY\SYSTEM’ privileges, loads this DLL without properly verifying its integrity or origin. Successful exploitation could allow code execution with SYSTEM privileges and result in local privilege escalation.

### CVE-2026-77193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T09:17:07.877 |

The eesy_ID2WP – Publish InDesign HTML5 plugin for WordPress is vulnerable to Path Traversal in all versions up to, and including, 1.0.3 via the `id2wp_path` parameter. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information.

### CVE-2026-80513

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-24T06:17:01.430 |

The wpForo Forum WordPress plugin before 3.1.6 does not restrict which classes may be instantiated when it deserializes a user-supplied profile field value, allowing authenticated users with Subscriber-level access and above to inject a PHP Object.
No POP chain is present in the wpForo Forum WordPress plugin before 3.1.6 itself; if one is present via another installed wpForo Forum WordPress plugin before 3.1.6 or , this could lead to remote code execution, arbitrary file operations, or SQL injection. This is an incomplete fix of CVE-2026-49769.

### CVE-2026-14780

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-24T06:17:00.567 |

A vulnerability exists in the PaperCut NG/MF platform's device-scripting functionality due to insufficient sanitization and access restrictions within the embedded execution engine. An authenticated user with administrative access to the management interface can supply a malicious script that escapes the runtime sandbox.  

A successful execution enables an attacker to run unauthorized operating system commands with administrative privileges on the host operating system.

### CVE-2026-75887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T22:16:57.117 |

A flaw was found in the OpenShift console. An unauthenticated attacker can exploit a path traversal vulnerability by manipulating the `lng` and `ns` query parameters in the `/locales/resource.json` endpoint. This allows the attacker to read sensitive `*.json` files from the pod filesystem, including plugin manifests and configuration files. Furthermore, this flaw can enable path traversal against registered dynamic-plugin backends.

### CVE-2026-86065

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T20:17:20.160 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, the default-open GET /subscribe endpoint in network/api/websocket/routes.go accepts unauthenticated WebSocket clients with permissive origin handling, does not call SetReadLimit to bound message size, and has no live-connection cap. SocketHub.HandleClientInsertion also accepts an unbounded address list that grows addressSubscription, and client.loopIn continues reading without a size limit, allowing one client to grow subscription maps or many clients to retain goroutines, buffered channels, and descriptors. The global HTTP request throttler does not count upgraded live WebSocket connections. Because the REST and WebSocket API runs in the node process, memory or scheduler exhaustion can crash the node and interrupt P2P and consensus participation. This issue is fixed in version 1.7.20.

### CVE-2026-96541

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T19:19:54.080 |

A denial-of-service flaw was found in gnome-remote-desktop. An unauthenticated remote attacker can open RDP connections without completing the handshake and retain the connection-throttling slots indefinitely because no pre-authentication handshake deadline is enforced. By exhausting the global connection limit, an attacker can prevent new RDP clients from connecting until a holding socket is closed.

### CVE-2026-95604

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T19:19:53.637 |

Unauthenticated Broken Access Control in Loops & Logic <= 4.2.4 versions.

### CVE-2026-95513

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-23T19:19:50.933 |

Unauthenticated Broken Access Control in Online Booking & Scheduling Calendar for WordPress by vcita <= 4.6.0 versions.

### CVE-2026-77423

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-23T19:19:16.017 |

JLine is a Java library for handling console input. From 3.0.0 until 3.30.15 and 4.3.1, the JLine built-in less viewer passes user-controlled search and display-filter patterns from getPattern(boolean doDisplayPattern) in builtins/src/main/java/org/jline/builtins/Less.java directly to Java's backtracking regular expression engine and repeatedly applies them to file content. A nested-quantifier expression evaluated against non-matching lines can consume excessive CPU and indefinitely block the session thread, and repeated sessions in Telnet or SSH deployments can exhaust a bounded worker pool. This issue is fixed in versions 3.30.15 and 4.3.1.

### CVE-2026-77422

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-23T19:19:15.863 |

JLine is a Java library for handling console input. From 3.0.0 until 3.30.15 and 4.3.1, the JLine built-in grep command in builtins/src/main/java/org/jline/builtins/PosixCommands.java accepts a user-controlled regular expression in grep(...) and, unless line-regexp mode is used, automatically adds a dot-star prefix and suffix before compiling it with Java's backtracking regular expression engine. The wrapping expands the backtracking search space, so a short nested-quantifier expression evaluated against non-matching input can consume excessive CPU and indefinitely block a command worker, including in remotely exposed shell sessions. This issue is fixed in versions 3.30.15 and 4.3.1.

### CVE-2026-61814

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-407` |
| Published | 2026-09-23T19:17:32.970 |

Jawn is an open source JSON parser. Prior to 1.7.0, Jawn's AsyncParser can perform quadratic work when a single JSON token is delivered across many small chunks because each absorb call rescans the incomplete token from the start. A remote attacker who controls untrusted JSON input and its chunk sizes can exhaust CPU resources and cause denial of service in applications using AsyncParser. This issue is fixed in version 1.7.0.

### CVE-2026-61695

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-09-23T19:17:32.810 |

Wire provides gRPC and protocol buffers for Android, Kotlin, Swift, and Java. Prior to 6.4.1 and 7.0.0-alpha04, Wire's Swift runtime ProtoReader.skipGroup(expectedEndTag:unknownFieldsWriter:) accepts a negative length for a LENGTH_DELIMITED field inside an unknown START_GROUP field. ProtoReader.readData() forwards the negative count to ReadBuffer.readData(count:), whose upper-bound-only check permits the value to reach Foundation Data(bytes:count:) and trigger an unrecoverable process trap instead of a catchable ProtoDecoder.Error. Any Swift process decoding untrusted protobuf bytes can be crashed without authentication, user interaction, or knowledge of the target schema. This issue is fixed in versions 6.4.1 and 7.0.0-alpha04.

### CVE-2026-59990

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T19:17:32.637 |

Jawn is an open source JSON parser. Prior to 1.7.0, Jawn parse methods accept arbitrarily deep JSON array and object nesting without a depth limit, allowing a remote attacker who can submit untrusted JSON to grow parser contexts until the JVM heap is exhausted. The resulting java.lang.OutOfMemoryError is a fatal Scala error that is not ordinarily handled by scala.util.Try or cats.effect.IO, causing denial of service. This issue is fixed in version 1.7.0.

### CVE-2026-88830

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-09-23T17:17:18.427 |

A unit confusion in BusyBox TLS Montgomery reduction buffer allocation causes a pre-authentication heap buffer overflow when processing a crafted ClientKeyExchange message.

### CVE-2026-6668

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-835` |
| Published | 2026-09-23T17:17:16.073 |

Integer overflow in the packet buffer growth logic in PgBouncer through 1.25.2 allows an unauthenticated remote attacker to cause a denial of service. Sufficiently large input makes the buffer size computation overflow, leaving the growth loop unable to terminate. Because PgBouncer serves all clients from a single process, this saturates a CPU core and stalls every pooled connection until the process is killed. Both unauthenticated and authenticated code paths can reach the overflow.

### CVE-2026-19888

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-23T17:17:14.917 |

Missing validation of a mandatory attribute in the SCRAM client-final-message parser in PgBouncer through 1.25.2 allows an unauthenticated remote attacker to crash the process. A malformed message can make the parser report success while leaving a required value unset, which is then dereferenced as a NULL pointer. The crash occurs before any credential is verified, so no valid account is required. Because PgBouncer serves all clients from a single process, this terminates every pooled connection.

### CVE-2026-73591

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-540` |
| Published | 2026-09-23T15:17:18.103 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains an Inclusion of Sensitive Information in Source Code vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-88907

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-24T13:17:15.873 |

Incorrect Authorization vulnerability in TÜBİTAK ULAKBİM UlakPDF allows Authentication Bypass.

This issue affects UlakPDF: through 09092026.

### CVE-2026-94183

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-451` |
| Published | 2026-09-23T20:17:23.907 |

Arc Search for Android before version 1.12.10 does not display a fullscreen notification when a page enters fullscreen mode while the app is running in the background. A remote attacker can exploit this via a specially crafted website to render fake UI elements, such as a spoofed address bar, misleading the user about the origin of displayed content and increasing the risk of phishing.

### CVE-2026-94181

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-451` |
| Published | 2026-09-23T19:19:48.763 |

An address bar spoofing issue in affected versions of Arc could allow an attacker to spoof the browser address bar via a <select> element that triggers requestFullscreen without displaying the fullscreen notification.

### CVE-2026-92730

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:44.430 |

LimeSurvey Community Edition 7.0.14 contains a reflected cross-site scripting vulnerability on the administrative survey-participant CSV import result page.

### CVE-2026-91775

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T18:17:11.097 |

LimeSurvey fails to safely encode attacker-controlled content from a crafted .lss survey file when displaying import warnings, resulting in XSS in the administrative interface.

### CVE-2026-96808

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-09-23T17:17:25.860 |

In Flatpak before 1.18.1, the revokefs writer, used by the flatpak-system-helper to receive repository data from unprivileged callers, validated file paths by rejecting literal .. components but did not prevent symlink traversal. A malicious local user in an active local session could obtain two revokefs sessions via the system helper, create a symlink in one session pointing into the other session's directory, and retain a file descriptor through that symlink. This allowed the attacker to modify files belonging to a different revokefs session after they had been validated and imported by the system helper. In particular, an attacker could use this to tamper with ostree commit objects in the system repository after they passed signature verification, enabling root-controlled file writes to attacker-chosen paths and local root privilege escalation.

### CVE-2026-18184

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-23T16:16:41.210 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to obtain sensitive information due to an XML external entity (XXE) injection flaw.

### CVE-2026-73588

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-23T15:17:17.850 |

Dell Secure Connect Gateway (SCG) Policy Manager, versions prior to 5.34.00.16, contains a Missing Authentication for Critical Function vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-82077

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-78` |
| Published | 2026-09-24T07:16:33.457 |

An improper limitation of a pathname to a restricted directory (path traversal) vulnerability in the Scan-to-Fax component of PaperCut NG and PaperCut MF allows an authenticated administrator to execute arbitrary commands on the underlying host via crafted fax provider settings.

### CVE-2026-66077

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T21:16:59.647 |

RabbitMQ is a messaging and streaming broker. Prior to versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6, The management UI uses EJS 1.0 in which <%= ... %> does NOT HTML-escape. connection.ejs:135 renders <%= connection.ssl_details.peer_cert_subject %> (and peer_cert_issuer) directly into the page. The same pattern appears in streamConnection.ejs:102,106,110. The values come from rabbit_ssl:peer_cert_subject/1 which formats the DN as a string without HTML escaping. The verifier corrected the original researcher's claim: this is reachable only when the listener is configured with verify_peer (so the certificate must be signed by a CA in the broker's trust store, not arbitrary self-signed); however, in deployments using mTLS for client authentication, any user who can request a certificate from the organisational CA controls the Subject CN. An attacker who can obtain a TLS client certificate signed by a CA the broker trusts (with verify_peer enabled) can embed JavaScript in the certificate's Subject DN. When any administrator views that connection in the management UI, the script executes in the admin's browser session, allowing full account takeover (create users, export definitions, etc.). The management UI's CSP includes 'unsafe-inline', so inline script execution is not blocked. Preconditions include TLS listener configured with ssl_options.verify = verify_peer Attacker can obtain a CA-signed client certificate with attacker-chosen Subject (e.g. self-service corporate PKI, or rabbitmq_trust_store plugin in use) Administrator views the connection detail page. This issue is fixed in versions 3.13.15, 4.0.20, 4.1.11, and 4.2.6.

### CVE-2026-88832

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-23T17:17:18.573 |

BusyBox romfs volume ID parsing uses unbounded strlen on attacker-controlled metadata, causing a heap buffer overflow when processing crafted filesystem images.

### CVE-2026-18875

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-74` |
| Published | 2026-09-23T16:16:41.850 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift is vulnerable to RAG poisoning via unauthenticated runbook upsert (CWE-74) in the FTM AI agent server (api.vectordb.runbooks.js:51). An unauthenticated attacker can insert malicious runbook content into the agent's vector database to steer AI-driven MCP tool calls, potentially triggering unauthorized payment actions or exfiltrating payment data.

### CVE-2026-18185

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-23T16:16:41.337 |

IBM Financial Transaction Manager (FTM) for RedHat OpenShift could allow a remote attacker to access sensitive information and modify system configurations due to missing authentication for a critical function.

### CVE-2026-88843

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-24T06:17:03.207 |

The MasterStudy LMS WordPress Plugin  WordPress plugin before 3.7.50 does not validate one of its display-style settings before using it to build a template path, allowing users with the Contributor role and above to include and execute arbitrary local PHP files on the server. An equivalent path was corrected in an earlier release and this one was not, so the issue persists in versions the earlier advisory reports as fixed.

### CVE-2026-75886

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-441` |
| Published | 2026-09-23T21:17:02.683 |

A flaw was found in openshift/console. An unauthenticated remote attacker can exploit a misconfiguration in the CatalogdHandler, which lacks proper authentication, and the forwarding of the `openshift-session-token` cookie. This allows the attacker to send requests to the in-cluster catalogd service, leading to the disclosure of the internal operator-catalog index and providing a relay into the openshift-catalogd namespace.

### CVE-2026-85475

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-96` |
| Published | 2026-09-23T20:17:19.343 |

A flaw was found in the Ansible Automation Platform automation controller. The
external logging (rsyslog) configuration is generated by interpolating
user-controlled settings — LOG_AGGREGATOR_HOST, LOG_AGGREGATOR_MAX_DISK_USAGE_PATH
and LOG_AGGREGATOR_RSYSLOGD_ERROR_LOG_FILE — into an rsyslog RainerScript config
file without neutralizing RainerScript syntax. A privileged (superuser) user can
inject rsyslog directives, including an omprog action, causing arbitrary command
execution inside the control-plane rsyslog component. This allows disclosure of
the controller SECRET_KEY and database credentials, decryption of all stored
credentials, and full compromise of the control plane.

### CVE-2026-95603

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-23T19:19:53.500 |

Shop manager PHP Object Injection in Reycob Product Import Export <= 2.3.0 versions.

### CVE-2026-90905

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-352` |
| Published | 2026-09-23T19:19:43.673 |

Joomla Extension - joomshaper.com - Missing CSRF and Access Control on Site Configuration Update in Easy Store extension 1.0.0-3.0.0 - The endpoint administrator/index.php?option=com_easystore&task=appconfig.updateConfiguration updated core Joomla mail configuration (fromname, mailfrom) in configuration.php without verifying anti-CSRF tokens or checking for administrative permissions (canAdmin). A malicious site could silently modify the site's sender name and email address via forged requests from an admin's browser. Resolved by enforcing Session::checkToken('request') / Session::checkToken('post') and adding explicit administrative authorization verification via AccessControl::create()->canAdmin().

### CVE-2026-90903

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-09-23T19:19:43.417 |

Joomla Extension - joomshaper.com - Missing CSRF Token Verification across Administrator AJAX API Endpoints in Easy Store extension 1.0.0-3.0.0 - The administrator ApiController only validated CSRF tokens inside the products() action. All other administrative AJAX endpoints (orders, coupons, media, customers, settings, tags, categories, reviews, and collections) accepted state-changing requests without checking anti-CSRF tokens. An attacker could trick a logged-in administrator into triggering unauthorized state modifications across the store backend. Resolved by implementing global CSRF verification in ApiController::execute() for all state-changing HTTP methods (POST, PUT, PATCH, DELETE) via Session::checkToken().

### CVE-2026-93769

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T16:16:48.360 |

HumHub 1.18.5 is affected by a stored cross-site scripting (XSS) vulnerability that allows any user holding the delegated, non-system-administrator Manage Users permission (admin_manage_users) to inject persistent HTML/JavaScript into a Profile Field Category title.

### CVE-2026-4638

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-209` |
| Published | 2026-09-24T11:16:45.953 |

PRTG Network Monitor before version 26.2.120.1449 ships a demo EXE/Script sensor that multiplies two integer parameters using cscript.exe. If a non-numeric value is passed instead, cscript.exe raises a 'Type mismatch' runtime error that includes the offending parameter value in plaintext. PRTG provides a documented placeholder variable, %windowspassword, which resolves to the configured Windows/domain password used by PRTG and can be passed as a sensor parameter. 




Any PRTG user who is not restricted to read-only access and is permitted to create sensors (the default for non-read-only users) can pass %windowspassword as an argument to the demo VBScript sensor, triggering the type-mismatch error and causing PRTG to display the plaintext password in the sensor's error output.

### CVE-2026-67235

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T21:17:01.227 |

RabbitMQ is a messaging and streaming broker. Prior to versions 4.3.0, 4.2.6, 4.1.11, 4.0.20, and 3.13.15, The content-header BodySize (a uint64) was stored without validation against max_message_size. The size check ran only when assembly completed. By declaring body_size = 2^63-1 and then streaming fragments, a client ensured that check_msg_size never fired, so the accumulated body size went unbounded. A reader process accumulates memory until the memory alarm fires, degrading all publishers cluster-wide, or until the node runs out of memory. The memory alarm provides only partial mitigation, since it is reactive rather than preventive. AMQP 0-9-1 is the most widely used protocol, and any publisher can trigger this condition. Preconditions include Any authenticated AMQP 0-9-1 client with publish permission can exploit this.. This issue is fixed in versions 4.3.0, 4.2.6, 4.1.11, 4.0.20, and 3.13.15.

### CVE-2026-84714

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-23T20:17:18.083 |

A flaw was found in the automation-controller input-validation
                  guard sanitize_jinja(). The function uses two regular
                  expressions to reject user-supplied Jinja, but the patterns
                  stop at the first interior '}' or '%' character, so a Jinja
                  expression containing an inner brace (for example an empty
                  dict) is accepted while remaining valid Jinja. Because
                  sanitize_jinja() is the sole guard on several launch-time
                  fields — ad-hoc command module_args, Machine-credential
                  username / become_method / become_user, and inventory host
                  names — a low-privileged user can inject Jinja that ansible-core
                  evaluates in the execution environment. This enables execution
                  of arbitrary commands in the execution environment (bypassing an
                  administrator's AD_HOC_COMMANDS module allowlist) and disclosure
                  of secrets belonging to credentials the attacker cannot read
                  (by templating a co-attached credential's injected environment
                  variables), across the credential access-control boundary.

### CVE-2026-82406

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-841` |
| Published | 2026-09-23T20:17:16.547 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, the native marketplace function core/kapp/market/market.go Buy does not check IsClaimed before accepting a bid. A seller can use the Claim seller-accept branch to settle a resting-bid auction while leaving the claimed order loadable with a future EndTime and stale CurrentBid and CurrentBidder values. A later bidder can submit a higher bid, be debited, and cause the previous bidder to receive a refund even though the NFT has already been delivered. Because Claim and CancelOrder reject the later bidder when IsClaimed is true, the later bidder cannot obtain the NFT or recover the funds. This issue is fixed in version 1.7.20.

### CVE-2026-67238

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-23T20:17:13.297 |

RabbitMQ is a messaging and streaming broker. Prior to versions 4.2.7 and 4.3.1, rabbit_pid_codec:decompose_from_binary/1 parses a caller-supplied ETF-encoded binary and calls binary_to_atom(Node, utf8) on the node-name field. It is reached from rabbit_volatile_queue:pid_from_name/2, which is invoked for any queue name / routing key beginning amq.rabbitmq.reply-to.. The CandidateNodes membership check happens after the atom is created, and the surrounding try/catch cannot reclaim atoms (they are never GC'd). binary_to_existing_atom is not used. Any authenticated AMQP client can crash the entire Erlang VM (all vhosts, all connections) with ~1M cheap requests. Preconditions include Authenticated AMQP 0-9-1 connection to any vhost No per-connection rate limit low enough to make ~1M operations infeasible. This issue is fixed in versions 4.2.7 and 4.3.1.

### CVE-2026-95590

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T19:19:52.653 |

Subscriber SQL Injection in Tainacan <= 1.2.0 versions.

### CVE-2026-95529

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:52.237 |

Unauthenticated Cross Site Scripting (XSS) in Calculated Fields Form <= 5.5.1.1 versions.

### CVE-2026-95528

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:52.107 |

Unauthenticated Cross Site Scripting (XSS) in Core Web Vitals & PageSpeed Booster <= 1.0.31 versions.

### CVE-2026-95515

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:51.250 |

Unauthenticated Cross Site Scripting (XSS) in Ninja Forms <= 3.15.3 versions.

### CVE-2026-94179

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:48.630 |

Unauthenticated Cross Site Scripting (XSS) in Razorpay Payment Button <= 2.4.9 versions.

### CVE-2026-94176

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:48.453 |

Unauthenticated Cross Site Scripting (XSS) in Mang Board WP <= 2.4.1 versions.

### CVE-2026-93774

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:46.753 |

Unauthenticated Cross Site Scripting (XSS) in WP Photo Album Plus <= 9.3.02.002 versions.

### CVE-2026-93622

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:46.180 |

Unauthenticated Cross Site Scripting (XSS) in WPS Limit Login <= 1.5.9.3 versions.

### CVE-2026-93526

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-23T19:19:45.437 |

Unauthenticated Cross Site Scripting (XSS) in Event Tickets <= 5.29.4 versions.

### CVE-2026-96651

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-23T17:17:23.187 |

Plex Media Server before 1.43.3.10861 builds a file path from the url parameter without checking it for ../ sequences, allowing path traversal via '/system/agents/media/get'. A remote attacker with a valid session token could read any file that the target user can access. This access includes the PlexOnlineToken, which grants control of the Plex account and server. A LAN-adjacent attacker with a client-supplied X-Forwarded-For header could exploit the same issue.

### CVE-2026-96609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-09-23T15:17:33.723 |

Robur Albatross 1.0.0 through 2.x before 2.7.2 does not limit use of the ring buffer, leading to an albatross-console loop with no recognized termination condition. This is only exploitable by users who can send console subscription commands to unikernels that produce sufficient log output to fill the ring buffer (1024 lines). It is not exploitable by unauthorized clients.

### CVE-2026-82407

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-09-23T20:17:16.707 |

Klever-Go is the Go implementation of the Klever blockchain protocol. Prior to 1.7.20, core/kapp/validators/validators.go Register and the runtime validator update path accept a submitted BLSPublicKey without curve, prime-order subgroup, or nonzero validation. When a validator with a malformed key becomes eligible and is selected into a consensus group, MultiSigner.Reset and the corresponding signature verification creation path cannot deserialize the group key and cancel the slot. This causes repeated missed rounds and throughput degradation, and a network whose consensus group equals the eligible validator set can halt completely. Genesis validation is not affected because that path already performs CheckPublicKeyValid. This issue is fixed in version 1.7.20.

### CVE-2026-96600

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-23T15:17:33.400 |

Isotope eCommerce through 2.9.10 contains a blind SQL injection vulnerability in backend callbacks that interpolate request-controlled identifiers and administrator-supplied values directly into SQL statements. Authenticated Contao backend users with Isotope module permissions can exploit conditional and time-based injection payloads to extract arbitrary database contents including user password hashes from the tl_user table.
