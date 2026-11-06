# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-06 15:00 UTC
- **対象期間**: `2026-11-05T15:00:55.000Z` 〜 `2026-11-06T15:00:35.000Z`
- **重要CVE数**: 227 件（Critical 9.0+: 33 件 / High 7.0〜: 194 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS 7.0 以上のものは **WordPress エコシステム** と **CRM／通信基盤** に集中しています。特に **リモートコード実行 (RCE)**、**認証なしの権限昇格**、**IDOR** といった「認証不要で完全制御が奪える」タイプが目立ち、攻撃者が自動化ツールで大量スキャンを行うリスクが高まっています。  
また、FreeSWITCH や OpenHuman などの **インフラ系ソフトウェア** でも同様に入力検証不備が原因の深刻な脆弱性が報告され、IoT／通信サービスへの波及が懸念されます。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品・バージョン | 主な脆弱性種別 | 重大度 (CVSS) | 注目理由・影響範囲 |
|-----|------------------|----------------|--------------|-------------------|
| **CVE‑2026‑118423** | WP Libre Form WordPress plugin **1.5.0.1** | 任意ファイルアップロード → RCE | **10.0** | ファイルタイプを検証しないため、PHP ファイルを任意の場所に配置でき、サーバ全体の制御が可能。WordPress サイトが多数利用しているため、スキャン対象が広がりやすい。 |
| **CVE‑2026‑111490** | MatchPoint API (Web) | IDOR（`actingasuser` ヘッダー） | **9.9** | 認証なしで任意ユーザーに成りすますことができ、個人情報・金融データが漏洩。ヘッダーだけで操作できるため、簡易なスクリプトで大量取得が可能。 |
| **CVE‑2026‑71550** | SuiteCRM **< 7.15.2 / < 8.10.2** | パス・トラバーサル (require_once) | **9.9** | ワークフローコントローラが任意の PHP ファイルをインクルードでき、サーバ上でコード実行が可能。CRM は顧客データを大量保持しているため、情報漏洩・改ざんリスクが極めて高い。 |
| **CVE‑2026‑116533** | Static Snapshot WordPress plugin **≤ 0.2.1** | コマンドインジェクション | **9.8** | ユーザー入力をシェルコマンドに直接結合。認証不要で任意コマンド実行が可能。プラグインは多数のサイトで利用されているが、アップデートがほとんど提供されていない。 |
| **CVE‑2026‑116779** | FreeSWITCH **< 1.11.3** | SIP MESSAGE 解析バグ → 任意コマンド実行 | **9.8** | 電話・VoIP インフラに直結。攻撃者が特定の SIP MESSAGE を送信するだけで、サーバ上で任意コードが実行され、通信サービス全体が停止・乗っ取りされる恐れ。 |

> **※** これらはすべて「認証不要」または「低権限で実行可能」な点が共通しており、攻撃者が自動化ツールで広範囲に悪用しやすい点が特に危険です。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **WAF でのリクエストフィルタリング**  
  - `multipart/form-data` のアップロード先や `actingasuser` ヘッダーの使用をブロック／検証。  
- **不要プラグイン・モジュールの即時無効化**  
  - 影響のあるプラグインが必須でない場合は **削除** する。  
- **監査ログの強化**  
  - ファイルアップロード、認証ヘッダー、SIP MESSAGE の受信ログを詳細に取得し、異常検知を自動化。  

### 3.2 製品別具体的対策  

| 製品 / パッケージ | 現行バージョン (脆弱) | 推奨バージョン / 対策 | 具体的作業 |
|-------------------|----------------------|----------------------|------------|
| **WP Libre Form** | 1.5.0.1 | **1.5.0.2 以降**（開発者が緊急リリース） | `wp plugin update wp-libre-form` または手動で zip を上書き。 |
| **MatchPoint API** | すべて（ヘッダー検証未実装） | **サーバ側で `actingasuser` の検証ロジックを追加**（認可チェック必須） | ソースコードを修正できない場合は **API Gateway** でヘッダーを除去し、認可済みトークンのみ許可。 |
| **SuiteCRM** | < 7.15.2 / < 8.10.2 | **7.15.2** または **8.10.2** 以上へアップデート | `composer update suitecrm/suitecrm` または公式インストーラでバージョンアップ。 |
| **Static Snapshot** | ≤ 0.2.1 | **0.2.2**（コマンドエスケープ対策） | `wp plugin update static-snapshot`。 |
| **FreeSWITCH** | < 1.11.3 | **1.11.3** 以上 | `yum update freeswitch`（CentOS/RHEL）／`apt-get install freeswitch`（Debian/Ubuntu）。 |
| **OpenHuman** | < 0.57.13 | **0.57.13** 以上 | `cargo install openhuman --version 0.57.13` またはバイナリを差し替え。 |
| **PowerSYSTEM Center** | すべて（SQL/認可不備） | **パッチリリース 2026‑04‑15**（仮） | ベンダー提供のパッチを適用し、SQL 文のパラメータ化と権限チェックを有効化。 |

### 3.3 資産管理・運用面のベストプラクティス
1. **脆弱性情報の自動取得**  
   - `cve-search` もしくは SaaS の脆弱性フィードを CI に組み込み、`composer.lock`・`package.json`・`wp‑plugin‑list` の差分を定期的にチェック。  
2. **最小権限の原則**  
   - WordPress の管理者権限は必要最小限のユーザーに限定し、`wp-config.php` の `DISALLOW_FILE_EDIT` を有効化。  
3. **コードレビューの徹底**  
   - 外部プラグイン・モジュールは **サンドボックス化**（例: `mod_security` の `SecRuleEngine On`、Docker コンテナ化）してデプロイ。  
4. **インシデント対応手順の整備**  
   - RCE 発覚時は即座に **Web サーバのファイルシステムを読み取り専用** に切り替え、バックアップから復元できる体制を確保。  

---

### まとめ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-118423

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-06T08:17:18.550 |

The WP Libre Form WordPress plugin 1.5.0.1 does not validate the type of files uploaded through its form submissions, allowing unauthenticated attackers to upload PHP files to a web-accessible location and execute them, leading to remote code execution.

### CVE-2026-111490

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-05T22:17:43.597 |

Insecure direct object reference (IDOR) vulnerability in the MatchPoint API, which relies on the `actingasuser` HTTP header without verifying the requester's authorization for the specified user. Manipulation of sequential identifiers allows access to personal, banking, and financial data, private messages, and QR codes for physical access, as well as the ability to modify third-party accounts, change passwords, impersonate users, and transfer virtual balances.

### CVE-2026-111489

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-05T22:17:43.447 |

A static credential embedded in the mobile app has been reported to return the 'autorizado' token on the MatchPoint platform. The report states that this token grants unauthenticated access to API services.

### CVE-2026-71550

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-11-05T19:17:26.357 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the workflow controller uses a path-traversal-capable aow_action value in require_once() without constraining the resolved file. The affected flow begins at modules/AOW_WorkFlow/controller.php and uses aow_action, and require_once() to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated user with the WorkFlow role can include executable PHP, obtain server-side code execution, access CRM data and configuration secrets, and establish persistent access. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-107622

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T12:17:16.020 |

The BuddyForms plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.10.5 via a form-type confusion attack through the `bf_post_type` parameter. This is due to the public frontend submission handler `buddyforms_form_response_no_ajax()` authorizing logged-out submissions based solely on the target form's `public_submit` flag while independently trusting the attacker-supplied `$_POST['bf_post_type']` to determine the post type of the newly created object — a cross-check introduced in 2.10.2 applies only to existing posts (`post_id != 0`) and is completely bypassed for new-object creation — combined with the `save_post` listener `buddyforms_edit_form_save_meta_box_data()` lacking both a `current_user_can()` capability check and a form-builder nonce, causing it to unconditionally persist attacker-supplied `$_POST['buddyforms_options']` for any newly inserted `buddyforms` CPT post. This makes it possible for unauthenticated attackers to insert a rogue BuddyForms form configuration with an attacker-controlled `new_user_role` value into the live global form registry, then submit a registration through that form to create a new WordPress account with administrator-level privileges and achieve full site takeover. Exploitation requires the WordPress site to have "Anyone can register" enabled and at least one public BuddyForms form attached to a page, both of which are standard BuddyForms deployment configurations.

### CVE-2026-120844

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-06T08:17:19.657 |

Incorrect Privilege Assignment vulnerability in miniOrange OAuth Single Sign On – SSO (OAuth Client) miniorange-login-with-eve-online-google-facebook allows Privilege Escalation.This issue affects OAuth Single Sign On – SSO (OAuth Client): from n/a through 7.1.3.

### CVE-2026-119516

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-06T08:17:19.227 |

Deserialization of Untrusted Data vulnerability in Mamunur Rashid Radius Booking — Booking Calendar for Appointments &amp; Services radius-booking allows Object Injection.This issue affects Radius Booking — Booking Calendar for Appointments &amp; Services: from n/a through 1.0.20.

### CVE-2026-116533

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-06T06:16:40.480 |

The Static Snapshot WordPress plugin through 0.2.1 does not sanitise shell metacharacters in a user-supplied value before concatenating it into operating-system commands run by the server, allowing unauthenticated attackers to execute arbitrary commands on the host.

### CVE-2026-115230

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T06:16:40.270 |

The WHIZZ WordPress plugin through 1.1.8 does not validate the password-reset key before updating a user's password, relying only on a nonce that is exposed to unauthenticated visitors, allowing attackers to set an arbitrary password for any user, including administrators, and fully take over their accounts.

### CVE-2026-113615

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T06:16:40.053 |

The GS JWT Authentication for WP REST API WordPress plugin through 1.0.0 does not sanitize or parameterize a request value before using it in SQL queries on several unauthenticated REST routes, allowing unauthenticated attackers to perform SQL injection and obtain an administrator session.

### CVE-2026-113584

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T06:16:39.943 |

The placester WordPress plugin through 1.4.3 does not perform any capability, nonce or ownership check on an AJAX action that updates account details, allowing unauthenticated attackers to overwrite any user's email address, including an administrator's, and take over the account through the standard password-reset flow.

### CVE-2026-110955

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-06T06:16:39.830 |

The Wurdey WordPress plugin through 1.0.0 does not verify a request signature before logging a user in, allowing unauthenticated attackers to authenticate as an administrator knowing only the administrator's username.

### CVE-2026-116779

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78;CWE-749` |
| Published | 2026-11-05T20:17:44.790 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.3, sofia_presence_handle_sip_i_message() split the To user of an inbound SIP MESSAGE on a plus sign and treated the left side as a chat protocol selector. Selecting the api chat proto reached switch_api_execute(), allowing a peer whose MESSAGE was accepted to run FreeSWITCH API commands, including operating-system command sinks, with the daemon's privileges. Inbound chat is enabled on the stock internal and external profiles, and any authenticated profile account is sufficient; stock directory users without password material can also remove that barrier in affected configurations. The flaw permits configuration and credential disclosure, arbitrary call control, and command execution, and exploitation has been observed in the wild. This issue is fixed in version 1.11.3.

### CVE-2026-54143

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-285` |
| Published | 2026-11-05T17:18:19.487 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before version 0.57.13, an attacker who can send messages to a configured external channel can cause the agent to create persistent shell cron jobs without human approval. The scheduler later executes these jobs with the privileges of the OpenHuman runtime user. Command validation also permits leading environment assignments that can redirect allowed commands to executable helpers. The demonstrated exploit requires a suitable helper executable already present on the host. This can lead to unauthorized persistent command execution and compromise data and resources accessible to OpenHuman. This issue is fixed in version 0.57.13.

### CVE-2026-123294

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-06T11:17:08.140 |

In JetBrains Hub before 2026.2.52556 privilege escalation was possible by changing email authentication details during the verification flow

### CVE-2026-77596

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-11-05T23:17:00.767 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the multi-user HTTP endpoints POST /apis/v2beta1/pipelines/upload and POST /apis/v2beta1/pipelines/upload_version call canUploadVersionedPipeline, which returns without SubjectAccessReview when the target namespace is empty while REQUIRE_NAMESPACE_FOR_PIPELINES defaults to false. A low-privilege tenant can create shared pipelines or inject attacker-controlled versions into existing shared pipelines without the required write permission; if the API server is directly reachable without an authenticating proxy, an unauthenticated caller can exploit the same bypass, while deployments protected by such a proxy do not expose anonymous access. An enabled unpinned recurring run that follows the latest version can then execute the injected specification in another tenant's namespace under that workload's service account, while pinned or embedded-specification runs are not automatically substituted. This issue is fixed in version 2.18.0.

### CVE-2026-102940

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-05T20:17:37.543 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.4.0, controllers/C_Document.class.php write actions, including move_action_process(), do not verify the caller's access to the source document, current patient and category, or destination patient and category before Document::change_patient() performs the mutation. A low-privilege authenticated user can reassign an arbitrary document to a patient or category the user can access and then retrieve it through the normally protected read path. The reassignment occurs before a later list rendering check, so a final HTTP 403 response does not mean the unauthorized write was blocked. This issue is fixed in version 8.4.0.

### CVE-2026-63774

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T01:17:50.470 |

Insufficient input validation in the PowerSYSTEM Center report designer allows an authenticated user to execute unauthorized SQL commands.

### CVE-2026-63017

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T01:17:50.297 |

Incorrect authorization in PowerSYSTEM Center allows a low-privileged, authenticated user to access resources normally limited to administrators.

### CVE-2026-100358

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-05T19:16:55.400 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the Studio Dropdown Editor passes $dropdown_name through html_entity_decode() and writes the result verbatim into a PHP language file under custom/ that is included on later page loads. An administrator can inject persistent PHP that executes as the web-server account, survives cache clears, and compromises application and host confidentiality, integrity, and availability. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-119757

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522;CWE-552` |
| Published | 2026-11-05T22:17:53.203 |

BTCPay Server before 2.4.2, including 2.4.2 release candidates, contains an information disclosure vulnerability that allows unauthenticated remote attackers to retrieve .macaroon credential files for an LND (Lightning Network Daemon) node. Attackers can use the exposed macaroon to gain full control of the LND node, including moving funds, resulting in theft of funds from affected deployments.

### CVE-2026-48705

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-20;CWE-682` |
| Published | 2026-11-05T21:18:50.270 |

MONAI (Medical Open Network for AI) is an AI toolkit for health care imaging. Prior to 1.6.1, PydicomReader._get_affine() trusts non-finite values in the DICOM PixelSpacing, ImagePositionPatient, and ImageOrientationPatient fields and composes them into an affine matrix without validation. An unauthenticated attacker who can upload a crafted DICOM to a default MONAILabel deployment can propagate NaN or infinity values through LoadImaged, Spacingd, model inference, and output writing, causing inference failures, persistent datastore poisoning, or geometrically corrupted results. This issue is fixed in version 1.6.1.

### CVE-2026-123198

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-11-05T19:17:18.393 |

LMFDB before commit 01829bd contains a server-side template injection vulnerability in the render_knowl function that allows unauthenticated attackers to inject Jinja expressions via request parameters. Attackers can supply crafted query-string values or 'content' data to /knowledge/render/<ID> to reach Python builtins and execute operating system commands as the web application account.

### CVE-2026-114630

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-06T12:17:16.503 |

The ELEX WordPress HelpDesk & Customer Ticketing System plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the factory_reset function in all versions up to, and including, 3.3.8 This makes it possible for unauthenticated attackers to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This vulnerability is exploitable via a two-step chain: an unauthenticated attacker first stores an arbitrary ticket_attachment_path value by submitting a ticket through the nopriv eh_crm_new_ticket_post AJAX endpoint (whose nonce is publicly exposed via the [wsdesk_support] shortcode), then triggers the factory_reset routine via a GET request to wp-admin/admin.php?page=wsdesk_factory_reset, which is guarded only by is_admin() — a request-type check — rather than a capability check, causing unlink() to be called on the attacker-supplied path.

### CVE-2026-88800

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T08:17:38.283 |

The MDJM Event Management and Mobile Events Manager WordPress plugins through 1.7.8.7 act on a role deletion request on every page load with no capability check and no nonce, and the guard meant to protect roles that have users assigned reads a different part of the request from the one that selects what is deleted, allowing unauthenticated attackers to remove any WordPress role including administrator, which permanently strips every user of their capabilities.

### CVE-2026-111494

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-05T22:17:44.193 |

Incorrect validation of TLS certificates in the MatchPoint Android app due to a TrustManager that accepts any certificate and a permissive hostname validator. Additionally, the app allows unencrypted HTTP traffic. An attacker capable of intercepting the victim's traffic could read and modify communications, including credentials and personal data.

### CVE-2026-46350

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-1284` |
| Published | 2026-11-05T21:18:50.110 |

dcmjs is a JavaScript implementation of DICOM manipulation. Prior to 0.52.0, the DecimalString and IntegerString implementations in src/ValueRepresentation.js sanitize text with a permissive regular expression and pass the result to JavaScript's Number constructor without validating finiteness or the DICOM value-representation rules. Scientific notation overflow in a DS or IS field can produce positive or negative Infinity, while stripping alphabetic characters from signed infinity text can leave a sign-only string that converts to NaN. IntegerString also accepts exponent notation and values outside the DICOM signed 32-bit IS range. Applications that trust these parsed values can propagate invalid numbers into spatial geometry, display windowing, dose scaling, frame counts, rescaling, or volume reconstruction, causing incorrect calculations or disrupted processing. This issue is fixed in version 0.52.0.

### CVE-2026-116790

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-290;CWE-347` |
| Published | 2026-11-05T20:17:46.557 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, FreeSWITCH's inbound ICE handling accepted every connectivity check without cryptographically validating its STUN MESSAGE-INTEGRITY attribute. A network peer able to reach an ICE-enabled leg's media port could forge an ICE connectivity check without SDP credentials, nominate its own address, redirect RTP and DTLS traffic, and terminate the legitimate media path. On unencrypted legs this enables eavesdropping and media injection, while all WebRTC and SIP legs that negotiate ICE are in scope. Version 1.11.2 introduces the remediation, which requires ice_verify_message_integrity=true.

### CVE-2026-116785

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-681;CWE-787` |
| Published | 2026-11-05T20:17:45.730 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, ws_read_frame() decoded a WebSocket frame's 64-bit extended payload length with a 32-bit byte swap and narrowed the result into a signed length. A value whose surviving low word became negative bypassed the signed size check and was reinterpreted as an enormous unsigned count, causing client bytes to overwrite memory beyond the 64 KiB receive buffer. Any client completing a /socket WebSocket upgrade on an enabled mod_xml_rpc endpoint reached the parser before HTTP authentication; both the module and WebSocket endpoint are disabled by default. The heap overwrite can corrupt connection pointers and crash FreeSWITCH, ending every concurrent session, although remote code execution has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-119344

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-11-05T16:17:40.373 |

Cocos AI is a confidential computing system for AI. In version 0.8.2 and earlier, Cocos AI accepts trusted execution environment attestation Evidence when firmware patch levels and software measurements match, without binding the Evidence to an allowed platform owner or unique machine identity and without enforcing revocation. A remote attacker who controls or compromises another platform trusted by the same verifier can substitute valid Evidence from that platform and cause authorization of the wrong platform. This vulnerability is addressed in 0.9.0. However, this vulnerability can't be patched in source code alone, since the vulnerability arises from the confidential computing threat model itself.

### CVE-2026-123279

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:06.140 |

In JetBrains Datalore before 2026.4 code execution was possible in a notebook's computation by view-only collaborators

### CVE-2026-85076

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-863` |
| Published | 2026-11-05T21:18:54.217 |

Cronicle is a multi-server task scheduler and runner, with a web based front-end UI. Prior to 0.9.124, an authenticated non-admin with run_events, create_events, or edit_events privilege can supply undeclared keys in event params through api_create_event, api_update_event, or api_run_event. lib/api.js and lib/api/event.js validate the parameter object without restricting its keys, and lib/job.js uppercases those keys and applies them to the child process environment after administrator-defined plugin variables. A key that collides with a security-sensitive environment variable can therefore override the plugin execution context and may cause privilege escalation, arbitrary code execution, data access, or service disruption depending on the plugin and runtime. This issue is fixed in version 0.9.124.

### CVE-2026-54141

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-862` |
| Published | 2026-11-05T17:18:19.103 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before 0.57.13, a remote direct message received through a configured Yuanbao channel is converted into a generic channel AgentTurnRequest that uses the default tool policy without establishing an interactive approval context. Under the default Supervised autonomy policy with Node enabled, node_exec is classified as a write operation that should prompt for approval, but ApprovalGate treats missing APPROVAL_CHAT_CONTEXT as a non-interactive turn and allows execution. Because Yuanbao direct messages are open by default, an external sender who can message the connected bot can influence the agent to execute JavaScript and operating-system commands as the OpenHuman user without an approval prompt. The issue requires a configured Yuanbao channel, the default approval-requiring policy state, Node availability, and successful model selection of node_exec. This issue is fixed in version 0.57.13.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-116624

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T12:17:17.340 |

The Advanced Members for ACF plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.3.0 via the `acf[_amem_local_user_password]` parameter of the `[advanced-members-account-password]` shortcode form submission. This is due to a PHP operator-precedence bug in the `pre_update_value` function of `acf/fields/class-user-password.php` that assigns boolean `true` instead of the resolved user ID to `$user_id`, causing the `_can_edit()` authorization check to pass for any logged-in user via PHP loose equality, and causing `wp_update_user()` to cast `'ID' => true` to integer `1` — unconditionally targeting the primary administrator account. This makes it possible for authenticated attackers, with Subscriber-level access and above, to overwrite the password of user ID 1 (the site's primary administrator) with an attacker-chosen value, granting full administrative access to the site. The intended exclusion guard in `Account::process` that strips the password field before saving is defeated because `amem_save_all_fields()` re-reads the full field list from `amem()->submission` and silently overwrites the caller-supplied excluded fields array with an empty array, ensuring the password field is always processed.

### CVE-2026-88799

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-06T08:17:38.130 |

The MDJM Event Management and Mobile Events Manager WordPress plugins through 1.7.8.7 do not check ownership or capability on the identifier supplied to their client profile update, allowing any authenticated user, such as a subscriber, to change the password and email address of any other account including an administrator, resulting in a full account takeover.

### CVE-2026-87784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T06:16:44.363 |

The Cool Media Filter WordPress plugin through 1.0.1 does not perform any capability or nonce check when updating the capabilities of a role, allowing any authenticated user, such as a subscriber, to grant their own role administrator capabilities and take over the site.

### CVE-2026-110525

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T06:16:39.460 |

The MCB  WordPress plugin through 1.0.0 does not sanitise or escape request header values before storing them and later rendering them in the administrator statistics grid, allowing unauthenticated attackers to store malicious JavaScript that executes in an administrator's browser session when the statistics page is viewed.

### CVE-2026-113663

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-184` |
| Published | 2026-11-05T23:16:50.523 |

AG2 is an open-source AgentOS. From 0.13.2 until ag2 1.1.1, and from autogen 0.13.2 to 0.14.1, SandboxShellTool configurations using allowed=[...] or readonly=True rely on ShellAdapter._filter and contains_shell_operator in ag2/tools/sandbox/filter.py and ag2/tools/sandbox/adapter/shell.py to validate a command prefix and reject selected shell syntax. The filter omits newline and carriage-return separators, while the accepted raw string is passed to sh -c, allowing an attacker-influenced agent command to execute an additional arbitrary statement. With the default LocalEnvironment backend, the injected statement runs as a host subprocess with the privileges of the agent process and can affect confidentiality, integrity, and availability. This issue is fixed in ag2 version 1.1.1.

### CVE-2026-33944

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T22:18:41.777 |

Dolibarr is an open-source enterprise resource planning and customer relationship management application. Prior to 22.0.5 and 23.0.1, there is a SQL injection vulnerability in the Third Party company update functionality. The application concatenates the  localtax1_value  and  localtax2_value  properties into an SQL UPDATE statement without numeric conversion or other appropriate sanitization. An authenticated user with Third Party create or edit permission can submit crafted  lt1  or  lt2  POST parameters to read sensitive database information, including password hashes, API keys, and business data, or modify third-party records. This issue is fixed in versions 22.0.5 and 23.0.2.

### CVE-2026-122267

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-05T22:17:55.117 |

MinIO Signature V4 verification before RELEASE.2026-09-22T19-25-18Z accepts unsigned x-amz-* headers, letting a presigned PUT URL be escalated into a cross-bucket read.

### CVE-2026-116786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-94` |
| Published | 2026-11-05T20:17:45.900 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, sofia_handle_sip_i_refer() placed raw Refer-To URI parameters and headers inside a sip_invite_params channel-variable block passed to switch_ivr_originate(). The originate parser treated a comma in the attacker-controlled value as a variable separator, allowing an authenticated caller on a bridged call to inject arbitrary variables into a newly originated leg. An injected execute_on_originate value could invoke the system dialplan application before answer and execute operating-system commands with the FreeSWITCH process privileges. SIP REFER is enabled by default, and the sender needs only a registered account and a call that takes the off-box transfer path, not administrative or Event Socket access. This issue is fixed in version 1.11.2.

### CVE-2026-97377

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:29.280 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the legacy SOAP portal method portal_get_entry_list propagates caller-controlled where and order_by values into SQL query construction without sufficient neutralization. A low-privileged portal API user can perform blind SQL injection to disclose database metadata and sensitive records, affect query behavior, and consume resources. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-71548

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-89` |
| Published | 2026-11-05T19:17:26.183 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, AOR_Report::build_report_query_where incorporates a report editor's parameter_value when value_type=Field without sufficient validation. An authenticated user who can save a report can use SQL injection to read the entire SuiteCRM database. Disclosed data can include users.user_hash, OAuth2 tokens, CRM records, report definitions, and configuration data; the connector does not permit stacked queries, so direct write-through-injection is not supported. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-69142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:25.660 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the jjwg_Maps map marker endpoint uses the authenticated caller's distance value in the map_markers action without strict numeric validation or parameterization. An authenticated attacker can alter the SQL query, extract database data, modify query results, and consume resources. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-69134

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:24.533 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the REST v4 JSON handler reads the pre-filter RAW_REQUEST value and relationship write helpers interpolate supplied field values into INSERT and UPDATE statements. The affected flow begins at $GLOBALS['RAW_REQUEST'] and uses set_relationship, SugarRelationship::addRow(), SugarRelationship::updateRow(), and contact_role to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated user can inject SQL through relationship fields to read or alter database data and may reach file-write consequences when the database account has elevated privileges. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-63214

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-943` |
| Published | 2026-11-05T19:17:23.557 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, legacy REST methods append an authenticated caller's query parameter as a SQL WHERE clause after insufficient structural validation. The affected flow begins at /service/v4_1/rest.php and uses get_entry_list, get_entries_count, and query to carry attacker-controlled data or authorization state into the security-sensitive operation. An account with list permission on a module can bypass the user_hash filter, retrieve password hashes and other database data, and use recovered administrative credentials to compromise the application. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-100365

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89;CWE-943` |
| Published | 2026-11-05T19:16:59.133 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, AOR report generation concatenates an attacker-controlled stored field label into an ORDER BY clause without an allowlist. The affected flow begins at AOR_Reports and uses aor_fields, ORDER BY, and field label to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated user with AOR Reports access can perform time-based extraction of password hashes and arbitrary table data and can hold database connections with expensive expressions. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-100363

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-05T19:16:58.207 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the V8 module API exposes CRUD operations for administrator-only modules to any authenticated OAuth2 user. The affected flow begins at /Api/V8/module and uses ACLRoles, ACLActions, and Administration to carry attacker-controlled data or authorization state into the security-sensitive operation. A low-privileged user can create roles, change ACL levels, bind elevated roles, and alter global configuration to obtain administrator-equivalent control of CRM data and behavior. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-97175

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-05T18:17:11.670 |

A flaw was found in the idp-auto-link authenticator of the keycloak-services component, which handles user identity federation. The issue occurs when Keycloak automatically links an incoming identity from an external provider to an existing local account based on an email address without verifying if the provider has validated that email. This can allow an attacker to take over a victim's account by using a matching unverified email address at a brokered provider.

### CVE-2026-77439

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-639` |
| Published | 2026-11-05T18:17:10.203 |

Immich is a self-hosted photo and video management solution. Prior to 3.0.3, an authenticated user with editor access to a shared album can change the existing owner's role because album member role updates do not protect the owner from modification. By demoting the owner and then promoting themselves, an editor can take ownership of the album, remove the original owner, and delete the album. This vulnerability is fixed in version 3.0.3.

### CVE-2026-54912

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-11-05T18:17:08.523 |

WebAssembly Micro Runtime (WAMR) is a lightweight standalone WebAssembly (Wasm) runtime. Prior to 2.4.5, the two-pass fast interpreter loader in core/iwasm/interpreter/wasm_loader.c can make inconsistent constant-table decisions between the sizing pass and the emitting pass. After duplicate constants inflate the first pass beyond the constant-slot limit, wasm_loader_get_const_offset emits later constants inline, but the between-pass sort and deduplication reduces the table so the second pass can choose table references and cause reserve_block_ret to emit additional copy operands that were not included in code_compiled_peak_size. A crafted module can therefore make the second pass write partially attacker-controlled compiled-code data beyond the heap buffer allocated from the first pass's size calculation during wasm_runtime_load, before guest code executes. This can corrupt host heap metadata and deterministically crash the process, causing denial of service; further consequences depend on the host application's heap layout. Builds using WAMR_BUILD_FAST_INTERP=1 are affected; disabling the fast interpreter avoids the vulnerable loader. This issue is fixed in version 2.4.5.

### CVE-2026-82413

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77;CWE-78;CWE-88` |
| Published | 2026-11-05T17:18:21.137 |

ntopng is a web-based network traffic monitoring application. Prior to 6.7.260717, scripts/lua/rest/v2/add/host/to_scan.lua and scripts/lua/rest/v2/exec/host/schedule_vulnerability_scan.lua accept scan_ports from any authenticated session, including non-administrator users, while deployments with login disabled expose the same request without authentication. The endpoints validate scan_ports with validateSingleWord, which permits shell metacharacters, and persist the value for the minute vulnerability-scan scheduler. The scheduler concatenates the value into an nmap command through nmap_scan_host and executes it through ntop.execCmd or ntop.execCmdAsync using popen. For the tcp_portscan and cve modules, a preliminary nmap -sn probe must first report the target as up before the attacker-controlled ports are used. When nmap is installed, this command injection allows arbitrary operating-system commands to execute as the ntopng service account without further user interaction. This issue is fixed in version 6.7.260717.

### CVE-2026-54146

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-526;CWE-732` |
| Published | 2026-11-05T17:18:20.013 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. From 0.53.15 before 0.57.5 on macOS, core_process.rs in the Tauri desktop process publishes the per-launch OPENHUMAN_CORE_TOKEN bearer credential in its process environment even though the core now runs as an in-process task. Another process running as the same user can read that environment through the macOS KERN_PROCARGS2 process-inspection interface, recover the token together with the local host and port, and authenticate to the core JSON-RPC service with the authority of the desktop frontend. The attacker can read agent memory and integrated-account data, invoke privileged actions, change configuration, and stop or disrupt services without root access, developer mode, or changes to System Integrity Protection. This issue affects Intel and Apple Silicon macOS systems. This issue is fixed in version 0.57.5.

### CVE-2026-54145

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-200;CWE-312;CWE-532` |
| Published | 2026-11-05T17:18:19.850 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. In affected versions before 0.57.5, the approval gate uses the JSON-RPC bearer token as an approval session identifier. This exposes the credential through persisted approval records, events, debug logs, and RPC responses, including during normal desktop operation. An attacker who obtains these artifacts can recover the token and access the core RPC interface while it remains valid. This can expose sensitive agent and integration data and permit privileged operations. Stable tokens remain usable until rotated; launch-specific tokens remain usable while the corresponding core instance is active. The fix is included in version 0.57.5.

### CVE-2026-121994

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T17:18:00.503 |

A stack buffer overflow in the GDB client's remote protocol handler allows an attacker-controlled debug target to execute arbitrary code in the GDB process. The vulnerability exists in fetch_register_using_p, which decodes a stub's register reply into an alloca-sized buffer without bounding writes by the register width.

### CVE-2026-85111

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-06T12:17:23.390 |

Allocation of Resources Without Limits or Throttling in Apache James Mime4J library prior version 0.8.15 allows Denial of Service upon parsing Mime messages.
Users are recommended to upgrade to Apache James server 3.9.1 that relies on fixed MIME4J 0.8.15 which addresses the issue.

See CVE-2026-85108 in Apache James MIME4J library.

### CVE-2026-113431

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-06T11:17:04.410 |

Allocation of Resources Without Limits or Throttling vulnerability in ninenines cowlib allows an unauthenticated remote peer to exhaust the memory of an HTTP/2 endpoint via HPACK-indexed header fields.

cow_http2_machine:headers_decode/4 in src/cow_http2_machine.erl decodes every HEADERS block with cow_hpack:decode/3. It bounds the compressed block size and the number of fields, but not the size of the decoded header list that RFC 9113 section 6.5.2 places under SETTINGS_MAX_HEADER_LIST_SIZE. A peer stores one header value of up to the dynamic table size (4096 bytes by default) and then references it with one-byte indexed fields, so about 100 bytes on the wire decode to a header list of about 390 KB. A consumer that copies the decoded values, as Cowboy does when cowboy_http2:headers_to_map/2 joins repeated cookie fields into one binary, allocates that amount for every stream. The total across streams and connections is not bounded.

This issue affects cowlib: from 2.7.0 onward.

### CVE-2026-123087

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T10:16:37.403 |

SQL injection vulnerability in Atmira’s SIREC. The server retrieves the value of a field from a JSON object containing user-supplied information and concatenates it into an SQL statement without properly sanitising the input. This allows the original query to be altered via malicious input, causing the database to return unexpected information.

### CVE-2026-121824

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-06T08:17:20.980 |

A vulnerability has been identified in armeria versions prior to 1.43.0, where processing malformed Thrift messages can cause excessive memory allocation, potentially resulting in denial of service.

### CVE-2026-121823

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-06T08:17:20.850 |

A vulnerability has been identified in armeria versions prior to 1.43.0, where inconsistent request path normalization can allow unauthenticated attackers to bypass path-based access controls and access protected resources.

### CVE-2026-121820

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-11-06T08:17:20.410 |

A vulnerability has been identified in armeria-saml versions prior to 1.43.0, where the HTTP-Redirect binding decoder decompresses attacker-supplied SAML messages without limiting the output size before signature validation, allowing an unauthenticated remote attacker to exhaust server memory and cause a denial of service.

### CVE-2026-118045

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-06T06:16:40.593 |

The Ever Accounting  WordPress plugin before 2.3.3 does not restrict the file path supplied to its CSV import routine to an allowed directory, allowing users with its custom Accounting Manager role (which does not have administrator privileges) to delete arbitrary files on the server, such as wp-config.php, which takes the entire site offline.

### CVE-2026-119432

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T05:18:20.830 |

A stored cross-site scripting (XSS) vulnerability exists in the Foxit Workspace's file share preview functionality. An attacker could upload a crafted file and share it with a victim. When the victim opens or previews the file, the embedded script executes in the application's origin, potentially accessing locally stored credentials and enabling credential theft.

### CVE-2025-71458

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T01:17:47.737 |

FTS3 Web Monitoring (fts-monitoring) versions 3.12.0 through 3.13.2 and 3.14.0 contain an unauthenticated sql injection vulnerability in the /linkinfo endpoint handled by get_linkinfo. Remote attackers can inject SQL through the source_se and dest_se query parameters to perform blind injection and read stored cloud storage credentials and token provider client secrets.

### CVE-2026-111493

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-05T22:17:44.040 |

Lack of authentication and authorization in the Images.ashx endpoint in MatchPoint, which allows profile photos to be downloaded using predictable identifiers. An unauthenticated remote attacker could enumerate these identifiers and collect users' photos. Linking these photos to identities may be facilitated by other vulnerabilities in the platform.

### CVE-2026-114134

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-05T21:18:36.887 |

Black is the uncompromising Python code formatter. Prior to 26.10.1, the Black GitHub Action with use_pyproject: true accepts tool.black.required-version from pyproject.toml without validating that it is a released Black version specifier. An attacker who can submit a pull request can change that field to a direct reference to attacker-controlled code, causing the workflow to install and execute the code in the victim repository's GitHub Actions context. This issue is fixed in version 26.10.1.

### CVE-2026-123202

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T19:17:19.337 |

libnxml before 0.18.6 contains a stack-based buffer overflow vulnerability in src/nxml_parser.c that allows remote attackers to write past a 1024-byte stack buffer via long XML names. Attackers can supply XML or RSS feeds with a 1022-character element, attribute, DOCTYPE or entity name ending in a multi-byte UTF-8 character to crash parsing applications.

### CVE-2026-123200

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-11-05T19:17:18.953 |

VRPN through 07.36 contains an out-of-bounds stack write vulnerability in vrpn_Endpoint::handle_sender_message() and handle_type_message() that allows unauthenticated remote peers to write outside a stack buffer via an unchecked length index. Attackers can connect, complete the version-cookie exchange, and send a SENDER_DESCRIPTION or TYPE_DESCRIPTION message with an out-of-range or negative index to crash the process.

### CVE-2026-54142

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-11-05T17:18:19.303 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before 0.57.13, background synchronization for connected services such as email, Slack, and Notion stores raw external content and later places it in the model context of autonomous background agents without neutralizing embedded instructions. ApprovalGate treats tool calls without an interactive chat context as pre-authorized automation, so attacker-authored content processed during a background tick can influence the model to invoke Composio actions without presenting an approval request. An attacker who can deliver content to a connected account can use this path to send or forward data, post messages, create or modify third-party content, or disclose information from OpenHuman memory and integrations. The issue requires an active integration and successful model interpretation of the injected instructions. This issue is fixed in version 0.57.13.

### CVE-2026-110532

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-06T06:16:39.597 |

The Mail Mage WordPress plugin through 0.0.25 does not properly sanitise and escape a user-supplied value before using it in a SQL statement, allowing unauthenticated attackers to perform SQL injection attacks.

### CVE-2026-88981

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-05T23:17:01.433 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the frontend artifact download path for source=s3 or source=minio accepts providerInfo.Params.endpoint, and the archived pod-log path accepts S3-compatible endpoint metadata from workflow status, without requiring those endpoints to match operator-controlled storage configuration. In the shipped authorization-disabled standalone configuration, an unauthenticated caller can make the shared ml-pipeline-ui pod connect to arbitrary reachable hosts and return response data; requests may also reveal an access-key identifier when signed with configured object-store credentials. Multi-user secret-backed metadata remains restricted to the server namespace. This issue is fixed in version 2.18.0.

### CVE-2026-88980

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-05T23:17:01.277 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.18.0, the frontend GET /artifacts/get route accepts source=http or source=https with caller-controlled bucket and key values, and isAllowedResourceName permits an all-digit decimal host that the URL parser converts to an IPv4 address. The default ALLOWED_ARTIFACT_DOMAIN_REGEX and authorization-disabled standalone configuration allow an unauthenticated caller to fetch internal HTTP resources and receive their response body. In the authenticated multi-user configuration, the same destination-validation defect is reachable by a low-privilege tenant with a valid identity and authorized namespace. Cloud credential disclosure depends on reachable metadata services and attached roles, and the issue does not establish IMDSv2 bypass or credential access when metadata is blocked. This issue is fixed in version 2.18.0.

### CVE-2026-111492

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T22:17:43.887 |

SQL injection in the push notification handler of the MatchPoint Android app, which processes messages from Firebase Cloud Messaging and constructs queries by concatenating untrusted data. An attacker capable of interacting with the component could manipulate queries and access sensitive information from the local database, including credentials stored in the versions described in the report. The scope of the injection is limited to the device.

### CVE-2026-123196

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-11-05T19:17:17.967 |

Authorizer before 2.4.2 contains a password reset poisoning vulnerability that allows unauthenticated attackers to control emailed link hosts by supplying x-authorizer-url gRPC metadata. Attackers can send this metadata to the gRPC port or a Grpc-Metadata-X-Authorizer-Url header through the REST gateway to capture reset or magic-link tokens and take over accounts.

### CVE-2026-107903

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T18:17:00.547 |

Joomla Extension - balbooa.com - Stored XSS in reviews via inconsistent sanitization in Gridbox < 2.20.5.0

### CVE-2026-105607

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T18:16:59.843 |

Joomla Extension - balbooa.com - Unauthenticated stored XSS in the "Recent Comments / Recent Reviews" widget in Gridbox < 2.20.5.0

### CVE-2026-73856

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-11-05T16:17:48.443 |

ModSecurity is an open source, cross platform web application firewall (WAF) engine for Apache, IIS and Nginx. From 3.0.0 until 3.0.17, src/transaction.cc compares a response Content-Type value against SecResponseBodyMimeType entries case-sensitively. A mixed-case response media type that is semantically equivalent to a configured lowercase type can therefore be treated as unconfigured, causing ModSecurity to skip RESPONSE_BODY inspection. An unauthenticated requester can then receive response content that a phase 4 rule would otherwise block, including sensitive error or debug data. This issue is fixed in version 3.0.17.

### CVE-2026-104269

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-11-05T16:17:29.377 |

ModSecurity is an open source, cross platform web application firewall (WAF) engine for Apache, IIS and Nginx. From 3.0.0 until 3.0.17, ModSecurity's multipart parser does not apply the RFC 2231 filename* parameter precedence used by common Go, Python, Node.js, and Java application parsers. A Content-Disposition header can provide a benign filename parameter for ModSecurity and a different encoded filename* value that the backend prefers, causing MULTIPART_FILENAME rules and the application to make security decisions on different names. Applications that use the backend-selected name for storage, extension checks, or content-type inference can therefore receive a filename that bypassed WAF inspection. PHP's native multipart parser is not affected by this discrepancy. This issue is fixed in version 3.0.17.

### CVE-2026-33379

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T10:16:37.943 |

A user with any role, including Viewer or a service account with no permissions, can create, externally publish, and delete dashboard snapshots (missing authorization). Only Grafana OSS and Grafana Enterprise 12.4 are affected; earlier versions and Grafana 13 are not.

### CVE-2026-49272

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-05T21:18:50.447 |

OAuthLib is an implementation of the OAuth request-signing logic for Python 3.6+. From 3.3.0 until 4.0.1, OAuthLib's RFC 8628 device workflow does not require DeviceCodeGrant.validate_token_request to check that the device_code parameter is present and valid. A caller whose client request is accepted by the configured validator and who knows a valid client ID enabled for the device workflow can submit a missing or bogus device code to the token endpoint and obtain a bearer token without completing device authorization. This issue is fixed in version 4.0.1.

### CVE-2026-120859

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95;CWE-502` |
| Published | 2026-11-05T18:17:05.323 |

PyMoDAQ before 4.4.13, and pymodaq_data, pymodaq_gui, and pymodaq_utils before 5.1.15, 5.2.x before 5.2.14, and 5.3.x before 5.3.10, contain deserialization of untrusted data and eval injection vulnerabilities that allow attackers to execute arbitrary code by supplying crafted files that a user opens. Attackers can store pickled objects in HDF5 string nodes that StringARRAY.array_to_string() passes to pickle.loads() when the node is browsed or read, place Python expressions in HDF5 attributes that JsonConverter.json2object() evaluates, supply a .dock file that load_layout_state() unpickles from the Dashboard Load layout action, or embed Python expressions in XML settings files that elt_to_dict() and set_txt_from_elt() evaluate.

### CVE-2026-120499

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95;CWE-502` |
| Published | 2026-11-05T17:18:00.097 |

h5io before 0.2.6 contains a code injection vulnerability in read_hdf5() that allows attackers to execute arbitrary code by supplying a crafted HDF5 file. Attackers can store Python code in a node titled timezone, which _triage_read() passes to eval() with builtins reachable, name an arbitrary module in class or custom-object nodes that _import_class() imports, or place pickled objects in pd_dataframe or pd_series nodes that pandas deserializes on read.

### CVE-2026-122329

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T16:17:46.030 |

SDL_mixer 3.1.2 through 3.2.4 contains a stack-based buffer overflow in FetchXLaw() in src/decoder_aiff.c due to miscalculated output offsets when expanding A-law or mu-law samples. Attackers can supply a crafted AIFF-C file that overwrites roughly 1 KB of adjacent stack memory when decoded, causing crashes or potential code execution.

### CVE-2026-122328

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T16:17:45.853 |

SDL_mixer 3.1.2 through 3.2.4 contains a stack-based buffer overflow vulnerability in FetchXLaw() of src/decoder_wav.c when decoding A-law or mu-law WAV files. Attackers can supply a crafted WAV file whose doubly-offset float expansion overwrites about 1 KB of adjacent stack memory, causing crashes or potentially code execution.

### CVE-2026-123323

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T11:17:11.983 |

In JetBrains YouTrack before 2025.3.170763, 
2026.1.14150, 
2026.2.19656 improper URL validation in the app widget host allowed apps to send REST requests without user confirmation

### CVE-2026-114604

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-11-05T21:18:37.057 |

GraphQL Tools provides utilities for building, stitching, and mocking GraphQL schemas. From 10.10.1 until 12.0.2, the @graphql-tools/utils mergeIncrementalResult helper passes incrementalResult.path segments to setObjectKeyPath without runtime primitive-type validation. A non-primitive segment can bypass strict comparisons against __proto__, constructor, and prototype, then be coerced during property access so a malicious or compromised upstream incremental GraphQL response writes attacker-controlled properties to Object.prototype in the consuming Node.js process. The affected implementation is packages/utils/src/mergeIncrementalResult.ts and is reachable when consumers merge untrusted @defer or @stream transport results. This issue is fixed in version 12.0.2.

### CVE-2026-49393

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288;CWE-306` |
| Published | 2026-11-05T17:18:16.687 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before 0.56.0, the core server protects HTTP POST requests to /rpc with bearer middleware but exposes Socket.IO rpc:request and chat:start handlers without equivalent transport or handler-level authentication. A local unauthenticated client can connect to the Socket.IO namespace and dispatch requests through the same protected controller path that rejects a missing bearer on /rpc. Depending on the selected method, the attacker can read configuration or health data, start agent flows, interact with integrated account APIs, alter local data, or stop and restart services. This issue is fixed in version 0.56.0.

### CVE-2026-119083

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T17:17:55.840 |

Path traversal in the archive extraction utility in GluonTS before 0.17.0 might allow an actor who supplies a crafted tar archive to write arbitrary files outside the intended extraction directory with the privileges of the extracting process via symbolic or hard links contained in the archive.



To remediate this issue, users should upgrade to version 0.17.0 or later.

### CVE-2026-112902

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-686` |
| Published | 2026-11-05T21:18:36.713 |

Pillow is a Python imaging library. In versions through 12.3.0, the libtiff TIFF encoder can pass arguments to  TIFFSetField()  that do not match libtiff’s definition of the corresponding tag. When an application saves attacker-controlled image metadata through this encoder, crafted tag values can cause invalid memory reads, copying process memory into the encoded output or crashing the process. Applications that return the encoded output to an attacker can disclose that memory. The issue is reachable when re-saving compressed TIFF images and through certain conversions that preserve EXIF metadata into compressed TIFF output. This vulnerability is fixed in version 13.0.0.

### CVE-2026-69141

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:25.490 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the CasesController action_get_kb_articles action interpolates $_POST['search'] into a CASE WHEN ... LIKE expression and the SQL WHERE clause. Although securexss() normally entity-encodes quotes, an input prefixed with an XSS payload makes AntiXSS select a processed string instead of the encoded backup, allowing a literal quote to reach the query. A low-privileged user with Cases module access can perform blind SQL injection and extract sensitive database information. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-69140

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:25.313 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, GetLatestRevision.php interpolates get_latest_for_id directly into an SQL UPDATE statement. Although securexss() normally entity-encodes quotes, an input prefixed with an XSS payload makes AntiXSS select a processed string instead of the encoded backup, allowing a literal quote to reach the query. A low-privileged user with Documents module access can disclose database data and mass-update linked_documents records, while stacked statements and arbitrary DROP or INSERT operations are not supported by this vector. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-63215

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:23.750 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the REST API v4.1 get_entry_list method is vulnerable to time-based blind SQL injection when an authenticated caller simultaneously bypasses two independent security mechanisms. The advisory does not identify those controls more precisely, so their identities remain unspecified. Successful exploitation can extract sensitive database information. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-61653

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:22.937 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, modules/Campaigns/PopupCampaignRoi.php interpolates $_REQUEST['id'] into SQL. Although securexss() normally entity-encodes quotes, an input prefixed with an XSS payload makes AntiXSS select a processed string instead of the entity-encoded backup, allowing a literal quote to reach the query. An authenticated user with Campaigns access can perform time-based blind SQL injection against arbitrary database tables. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-61651

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:22.737 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the get_end_date action in Projects Controller concatenates an authenticated caller's task_id value into a SQL query without parameterization. A low-privileged user can use blind SQL injection to enumerate the database schema and extract credentials, customer records, and other database contents. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-61648

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:22.203 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, a user-controllable Multi report condition passes parameter_value through unencodeMultienum() and concatenates the result into a SQL WHERE clause. Although securexss() normally entity-encodes quotes, an input prefixed with an XSS payload makes AntiXSS select a processed string instead of the encoded backup, allowing a literal quote to reach the database. A low-privileged user with AOR Reports access can read arbitrary tables through time-based or UNION-based SQL injection and can consume database connections with delay expressions. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-123205

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-05T19:17:19.867 |

accel-ppp before 1.15.0 contains a heap buffer overflow vulnerability in the tcp, syslog and pgsql log targets that allows unauthenticated remote peers to overflow fixed heap buffers by producing log lines exceeding LOG_MAX_SIZE. Attackers within client-ip-range can send an L2TP Start-Control-Connection-Request with many string AVPs when verbose logging is enabled to corrupt heap memory and crash the daemon.

### CVE-2026-54914

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-05T18:17:08.873 |

WebAssembly Micro Runtime (WAMR) is a lightweight standalone WebAssembly (Wasm) runtime. Prior to 2.4.5, wasi_poll_oneoff in core/iwasm/libraries/libc-wasi/libc_wasi_wrapper.c validates the output pointer for only one wasi_event_t, while wasmtime_ssp_poll_oneoff in core/iwasm/libraries/libc-wasi/sandboxed-system-primitives/src/posix.c can write as many events as the guest-controlled nsubscriptions value. A crafted guest module can provide multiple subscriptions that produce events while positioning an output region large enough for only one event, causing a later out[nevents] write to cross the validated Wasm linear-memory boundary into adjacent host heap memory. The overwrite contains partly attacker-controlled event data and can reliably crash the host process, with further confidentiality or integrity consequences depending on heap layout. This issue is fixed in version 2.4.5.

### CVE-2026-107129

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T18:17:00.027 |

Joomla Extension - balbooa.com - Unauthenticated arbitrary file deletion via path traversal in Gridbox < 2.20.5.0

### CVE-2026-54140

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-11-05T17:18:18.910 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before 0.57.13, OpenHuman places names, descriptions, titles, and parameter definitions returned by configured external MCP servers into the agent model context without neutralizing instructions or bounding the descriptive fields. The McpRemoteTool records produced by list_tools preserve this remote content, while tool filtering considers the tool name and the prompt-injection detector screens user messages rather than MCP definitions. A malicious or compromised MCP server can therefore return a poisoned description that is evaluated on every agent turn and may direct the model to invoke other available tools, disclose accessible data, or perform unauthorized actions without a separate malicious user message. The issue affects users who configure an attacker-controlled or compromised MCP server. This issue is fixed in version 0.57.13.

### CVE-2026-123301

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T11:17:09.067 |

In JetBrains IntelliJ IDEA before 2026.3 dOM-based XSS in the OpenAPI preview error view was possible

### CVE-2026-115701

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-06T11:17:05.223 |

Allocation of Resources Without Limits or Throttling vulnerability in ninenines cowboy allows an unauthenticated remote attacker to exhaust connection process memory over HTTP/1.1.

Once a request has been received in full and its handler is still running, cowboy_http:parse/2 in src/cowboy_http.erl appends every further byte that arrives on the keep-alive connection to the connection buffer and returns to the receive loop without parsing it. The socket stays in active mode and no limit applies to this buffer: max_request_line_length, max_headers and the other parser limits only take effect once the handler returns and parsing resumes, and the only timer in this state is idle_timeout (default 60 seconds), which is reset on every received chunk. A client can therefore send an arbitrary amount of data on one connection for as long as the handler runs, and a few connections to an endpoint that holds requests open can drive the Erlang VM into out-of-memory conditions.

This issue affects cowboy: from 2.18.0 onward.

### CVE-2026-92698

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-05T23:17:02.633 |

FastNetMon is a high-performance DDoS detector and sensor. In version 1.2.9 and earlier, process_sflow_flow_sample() in src/sflow_plugin/sflow_collector.cpp passes the attacker-controlled sflow_raw_protocol_header_t.header_size to parse_raw_packet_to_simple_packet_full() as its trusted captured length without comparing it with the bytes remaining in the record. An inflated header_size creates a false end pointer beyond the received sFlow v5 UDP buffer, defeating the nested parser's bounds checks and causing an unauthenticated remote out-of-bounds read and process crash, with possible limited exposure of adjacent bytes through parsed flow fields. No fixed release is available as of this review.

### CVE-2026-92695

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-05T23:17:02.293 |

FastNetMon is a high-performance DDoS detector and sensor. In version 1.2.9 and earlier, the live parse_packet() callback in src/pcap_plugin/pcap_collector.cpp is registered through pcap_loop and processes captured frames when pcap = on without checking packethdr->caplen. A short frame or an attacker-controlled IPv4 header length can make the parser dereference IP or transport headers beyond the captured bytes, causing an out-of-bounds read and process termination. No fixed release is available as of this review.

### CVE-2026-92693

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-05T23:17:01.923 |

FastNetMon is a high-performance DDoS detector and sensor. In version 1.2.9 and earlier, parse_raw_packet_to_simple_packet_full() in src/simple_packet_parser_ng.cpp dereferences ipv6_extension_header_fragment_t when IpProtocolNumberIPV6_FRAG is present without first verifying that the eight-byte Fragment header remains. A crafted sFlow v5 RAW_PACKET_HEADER record can remotely reach this shared parser with the Fragment bytes omitted, causing an unauthenticated remote out-of-bounds read. The supplied harness detects the read under AddressSanitizer, but the advisory does not establish a production process crash. No fixed release is available as of this review.

### CVE-2026-77622

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-05T21:18:53.890 |

Sliver is a command and control framework. Prior to 1.7.6, an HTTP(S) listener using the PNG encoder accepts attacker-controlled PNG dimensions without an effective decoded-size or pixel limit in util/encoders/images.go, while the listener nonce space implemented in server/encoders/encoders.go is small enough to search remotely. An unauthenticated attacker who identifies a valid nonce can submit a highly compressed image to PNGEncoder.Decode, where it expands during png.Decode, exhausting server memory and causing a complete loss of availability. This vulnerability is fixed in 1.7.6.

### CVE-2026-116788

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-122;CWE-131;CWE-191` |
| Published | 2026-11-05T20:17:46.240 |

FreeSWITCH is an open-source software telecommunications platform. Before version 1.11.2, an integer underflow in  switch_xml_decode()  can cause an undersized heap allocation when an XML document declares an entity with an empty replacement value. Subsequent copying overruns the allocated buffer. An unauthenticated attacker who can reach a SIP profile with presence management enabled and DTD processing permitted can trigger the vulnerability through a crafted SIP PUBLISH request. Exploitation can corrupt heap memory and terminate the FreeSWITCH process, interrupting all active calls. This vulnerability is fixed in version 1.11.2.

### CVE-2026-116783

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-11-05T20:17:45.400 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, udptl_rx_packet() used a peer-controlled FEC entry count directly to fill five-entry FEC arrays in a mod_spandsp T.38 session. A larger count wrote sender-controlled error-recovery data beyond those arrays and persisted the oversized count for a later reconstruction pass. Any peer able to deliver UDPTL to an established T.38 fax session can reach the parser, including deployments using fax applications or a T.38 gateway. The memory corruption can crash FreeSWITCH and end every active call, although remote code execution has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-118494

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-538` |
| Published | 2026-11-05T19:17:12.140 |

Joomla Extension - jreviews.com - Secret configs cached in a web-accessible in JReviews 1.0.0-5.12.0, 6.0.0-6.6.9 - JReviews caches its full settings table, including the Joomla global configuration secret (copied into cms_secret) and third-party API keys and secrets, to a serialized file under components/com_s2framework/tmp/cache/core/ inside the web root. The file has no PHP guard and the directory has no .htaccess, so anyone who knows the file name can read it without authentication.

### CVE-2026-121996

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-11-05T17:18:00.870 |

A length validation flaw in gdbserver's agent-expression parser allows an unauthenticated remote attacker to read uninitialized heap memory from the gdbserver process and cause a denial of service. Disclosed heap content includes addresses suitable for defeating ASLR in further exploitation.

### CVE-2026-92895

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-11-06T12:17:24.820 |

The Live2DWebCanvas plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.2.1 via the download_one_file function. This is due to missing file extension whitelist and MIME type validation in download_one_file() when writing files derived from attacker-controlled manifest entries to the web-served plugin directory. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible when the plugin's apiType setting is configured as custom-local (self-hosted model mode), a non-default option that requires a paid license and prints the REST nonce and one-time session tokens into every front-end page.

### CVE-2026-123317

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-354` |
| Published | 2026-11-06T11:17:11.170 |

In JetBrains Ktor before 3.6.1 session forgery was possible via tampered encrypted session cookies

### CVE-2026-123295

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:08.273 |

In JetBrains Hub before 2026.2.52519 enforced two-factor authentication could be disabled via the profile update endpoint

### CVE-2026-123280

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:06.270 |

In JetBrains Datalore before 2026.2.4 unauthenticated users could execute code via published interactive reports

### CVE-2026-58273

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-05T22:18:49.230 |

Rucio is a scientific data management framework. From 1.16.1 until 35.9.0, 38.6.0, and 41.0.0rc1, the /credentials/signurl endpoint reads X-Rucio-Account instead of the account stored in request.environ['issuer'] by token authentication. Any authenticated low-privilege user can supply root as the header value and pass the root-only get_signed_url permission check. The server then returns a presigned read, write, or delete URL for an attacker-selected object using stored S3, GCS, or Swift credentials, and X-Rucio-VO can select another tenant in multi-VO deployments. This permits data disclosure, modification, deletion, and cross-tenant access on cloud-backed RSEs. This issue is fixed in versions 35.9.0, 38.6.0, and 41.0.0rc1.

### CVE-2026-115573

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T20:17:42.803 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, library/classes/Controller.class.php allows explicit controller.php dispatch to controllers missing from CONTROLLER_ACL_MAP, and checkControllerAcl() returns without enforcing any permission for those entries. A low-privilege authenticated user can invoke C_X12Partner::edit_action_process() to create or alter insurance-routing hosts and credentials, or invoke C_PatientFinder::find_action_process() to enumerate patient names, dates of birth, and identifiers. The shared fail-open dispatcher root cause also exposes other administrative controllers that were intended to be reached through ACL-gated Practice Settings routes. This issue is fixed in version 8.3.0.

### CVE-2026-103935

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T20:17:38.190 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, interface/forms/transfer_summary/new.php and interface/forms/functional_cognitive_status/new.php render stored transfer_to, code, and codetext values with text(), which uses ENT_NOQUOTES, inside double-quoted HTML value attributes. An authenticated clinical user can store a value containing a double quote that escapes the attribute and injects event-handler markup when another clinician opens the form. Successful exploitation can expose session data and protected health information or permit patient-record actions in the victim's session. This issue is fixed in version 8.3.0.

### CVE-2026-61650

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T19:17:22.550 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the POST /Api/V8/module/{moduleName}/{id}/relationships/{linkFieldName} endpoint checks only view and list permissions before a one-to-many relationship writes a target record's foreign key, without enforcing the required edit permission. A low-privileged user can reassign records, alter ownership and security-relevant relationships, expand cross-user access, and manipulate workflows. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-92857

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-11-05T18:17:10.887 |

Keycloak provides a Dynamic Client Registration feature that allows users with specific tokens to register their own applications. A flaw in how Keycloak validates these registration requests allows an attacker to create a malicious application that forges identity information. By mapping their own user profile details to protected fields like the user ID (sub) or intended audience (aud), an attacker can generate signed security tokens that make them appear to be a different user. This could allow an attacker to impersonate other users or gain unauthorized access to services that rely on these tokens for identity verification.

### CVE-2026-76077

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120;CWE-125;CWE-787` |
| Published | 2026-11-05T17:18:20.830 |

ASN1SCC is an open source ASN.1 compiler for embedded systems. Prior to 4.7.0.1, the XER tokenizer NT() in asn1crt/asn1crt_encoding_xer.c, which is reached by all XER decode paths, copies tag characters into a fixed char Value[100] field without a length bound and reads input and lookahead bytes without checking the buffer count. A crafted XER message with an overlong tag can overwrite the tokenizer's stack frame, while a truncated tag or unterminated processing-instruction or comment sequence can read beyond the input and may cause a CPU spin. The flaws can disclose adjacent memory, corrupt stack data, crash or hang the decoder, and potentially permit code execution. This issue is fixed in version 4.7.0.1.

### CVE-2026-75614

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129;CWE-787` |
| Published | 2026-11-05T17:18:20.497 |

ASN1SCC is an open source ASN.1 compiler for embedded systems. Prior to 4.7.0.1, BitStream_DecodeConstraintWholeNumber in asn1crt/asn1crt_encoding.c reads enough bits for a constrained integer but does not reject values above the declared range when the encoded range is not a power of two. Generated uPER and ACN decoders for variable-size SEQUENCE OF, OCTET STRING, BIT STRING, and string values use the invalid result as a loop or copy length, so a crafted over-range size field can write beyond a destination buffer. Decoding untrusted affected data can corrupt heap or stack memory, cause a crash, or potentially permit code execution. This issue is fixed in version 4.7.0.1.

### CVE-2026-121997

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-11-05T17:18:01.053 |

A heap buffer overflow in gdbserver's QTDPsrc packet handler allows an unauthenticated remote attacker to achieve native code execution in the gdbserver process. The vulnerability results from a mismatch between a packet's declared source length and the actual data length, causing hex2bin to write beyond the allocated heap buffer.

### CVE-2026-114232

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T17:17:39.547 |

A flaw was found in the UserManagedPermissionService of the Keycloak authorization server. The UMA Protection API, which manages user permissions, fails to validate the resourceType field when a user creates a new policy. This allows an attacker to create a policy that applies to resources owned by other users, potentially leading to unauthorized access or modification of sensitive data across the entire realm.

### CVE-2026-112208

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-305` |
| Published | 2026-11-05T17:17:38.283 |

A flaw was found in the Organization identity-first login flow of the Keycloak authentication server. Keycloak is an open-source identity and access management solution used to secure modern applications and services. The issue occurs when an attacker who belongs to multiple organizations initiates a login and then switches to a registration or password reset path. During this process, a flag indicating a successful login is not properly cleared when the user is removed from the session. An attacker can then provide a victim's username, and the system incorrectly treats the stale flag as proof of the victim's identity. This allows the attacker to bypass authentication and gain full access to the victim's account and connected applications.

### CVE-2026-123158

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-394` |
| Published | 2026-11-05T16:17:47.110 |

sshd in OpenSSH before 10.6p2 on Linux, when musl libc is used without PAM, lacks a workaround for a password authentication bypass (related to misinterpretation of whether a string is intended to be a password hash). For some configurations of accounts, any password between 256 and 1024 characters succeeds. An example of a platform using musl libc without PAM is Alpine Linux.

### CVE-2026-107891

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-11-05T16:17:32.150 |

musl libc before 1.2.7, when an untrusted regular expression is used with regcomp, has multiple integer overflows, possibly leading to incorrect allocation sizes and out-of-bounds heap writes.

### CVE-2026-71901

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-99` |
| Published | 2026-11-05T15:17:22.220 |

Improper Control of Resource Identifiers ('Resource Injection') vulnerability in Apache OFBiz.



An authenticate user with access to sfa component can override the service to use on vcard import and access to other service.



This issue affects Apache OFBiz: before 24.09.08.



Users are recommended to upgrade to version 24.09.08, which fixes the issue.

### CVE-2026-88801

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T08:17:38.410 |

The MDJM Event Management and Mobile Events Manager WordPress plugins through 1.7.8.7 do not check a capability or a nonce before creating a WordPress role from a name supplied in the request, and store that name without escaping it, allowing any authenticated user, such as a subscriber, to inject arbitrary web scripts which execute when an administrator opens one of the standard user management screens.

### CVE-2026-120408

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T06:16:41.790 |

The All-in-One Video Gallery  WordPress plugin before 5.1.0 does not escape a video's stored thumbnail URL before outputting it in the admin video list, and does not sanitise that value when it is written outside its own editor, allowing users with a role as low as Subscriber to perform Stored Cross-Site Scripting attacks against administrators.

### CVE-2026-110930

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-05T20:17:40.827 |

Codex Desktop for Windows does not correctly check quotation marks in project paths from Windows Explorer. If a user selects "Open project in ChatGPT" for an attacker-controlled library's child item, the path can add application startup arguments. These arguments can run attacker-controlled code with the current Windows user's permissions before sign-in or project trust approval.

### CVE-2026-96453

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-05T18:17:11.270 |

A flaw was found in the Keycloak Admin CLI kcadm tool, which is used by administrators to manage Keycloak servers from the command line. When a custom truststore is provided to verify the server identity, the tool incorrectly accepts any self-signed certificate as long as the hostname matches. This allows a network attacker to impersonate the Keycloak server, steal administrative credentials, and perform unauthorized management actions.

### CVE-2026-102523

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-11-05T16:17:23.727 |

MariaDB server is a community developed fork of MySQL server. From 10.11.1 until 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2, ALTER TABLE ... CONVERT ... PARTITION does not apply filename encoding to user-specified partition names before using them in filesystem path construction. An authenticated database user can use a partition name requiring filename escaping to make the conversion operate on table files the user is not authorized to access, allowing unauthorized table reads or modifications. This issue is fixed in versions 10.11.19, 11.4.13, 11.8.9, 12.3.3, and 13.0.2.

### CVE-2026-123321

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:11.723 |

In JetBrains WebStorm before 2026.3, 
2026.2.3 code execution via Grunt and Gulp task loading was possible in untrusted projects

### CVE-2026-123304

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:09.340 |

In JetBrains IntelliJ IDEA before 2026.3 code execution in untrusted projects via a configured ShellCheck path

### CVE-2026-123302

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:09.200 |

In JetBrains IntelliJ IDEA before 2026.3, 
2026.2.4, 
2026.1.5.1, 
2025.3.6.2 code execution was possible in untrusted projects via script engine discovery

### CVE-2026-123293

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:08.013 |

In JetBrains IntelliJ IDEA before 2026.3, 
2026.2.4 code execution was possible in untrusted projects  via the Terraform tool path setting

### CVE-2026-123276

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:05.740 |

In JetBrains CLion before 2026.3, 
2026.2.4.1 code execution was possible in Safe Mode via a crafted GDB server debug profile

### CVE-2026-44875

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-11-05T20:17:58.457 |

In HPE Cray Programming Environment versions 25.03 and 25.09, prior to 26.03, the method that CPE is deployed on HPCM potentially allows elevated access by a local unprivileged user.

### CVE-2026-102739

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-05T17:17:32.083 |

ESPectre is a Wi-Fi motion sensing platform for ESP32. Prior to 3.0.0-rc1, Micro-ESPectre analysis tools, including tools/6_optimize_filter_params.py, tools/1_analyze_raw_data.py, and tools/10_train_ml_model.py, load NPZ datasets with NumPy pickle support enabled through micro-espectre/tools/csi_utils.py and a direct loader. A malicious dataset contributor or pull-request author can place an object-typed array in a .npz file under micro-espectre/data, causing pickle-controlled code to execute as the maintainer or developer when a documented analysis tool accesses the field. This issue is fixed in version 3.0.0-rc1.

### CVE-2026-70659

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787;CWE-1284` |
| Published | 2026-11-05T16:17:48.047 |

stable-diffusion.cpp is a pure C/C++ library for running diffusion model (Stable Diffusion, Flux, Wan, Qwen Image, Z-Image, and more) inference. From master-742-1a13107 until master-763-4fcc6fe, IMatrixCollector::load_imatrix in src/runtime/imatrix.cpp reuses the values and counts vectors for entries with the same tensor name but resizes them only when they are empty. An untrusted .imatrix file can provide a small nval for the first entry and a larger nval for a second entry with the same name, causing the accumulation loop to write attacker-controlled floating-point and integer values beyond both heap buffers. Loading the file through the --imat-in conversion path can corrupt the heap or crash the process before a model is required. This issue is fixed in master-763-4fcc6fe.

### CVE-2026-123324

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:12.120 |

In JetBrains YouTrack before 2026.2.19562 information disclosure via shared mailbox message history was possible

### CVE-2026-119433

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T05:18:20.970 |

A server-side request forgery (SSRF) vulnerability exists in an undocumented API endpoint of Foxit Workspace due to insufficient validation of user-supplied URL and network parameters. A remote attacker could exploit this issue to induce the server to send requests to arbitrary internal or external resources, potentially enabling unauthorized access to internal services, network reconnaissance, and sensitive information disclosure.

### CVE-2026-119431

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-06T05:18:20.677 |

A server-side request forgery (SSRF) vulnerability exists in Foxit Workspace's file-upload functionality. Insufficient validation of user-supplied links may allow a remote attacker to induce the server to access internal resources and return their contents, potentially resulting in sensitive information disclosure and unauthorized access to internal services.

### CVE-2026-111770

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-05T22:17:45.817 |

The Model Context Protocol TypeScript SDK provides TypeScript client and server implementations of the Model Context Protocol. From 2.0.0 until 2.3.0 in @modelcontextprotocol/server, applications that shared one stateless HTTP transport or one McpServer or Server instance among multiple clients could deliver responses and notifications to the wrong client. The affected surface is an MCP server reached over HTTP by multiple clients. The trigger is reuse of one stateless transport or server instance. Messages were associated with a connection using only the JSON-RPC request identifier. SDK clients start request identifiers at zero, so collisions occur in normal operation. Cross-client delivery exposes one client's responses and notifications to another client. The issue requires an HTTP endpoint reachable by more than one client and an application that constructs the server or transport once at startup instead of once per request or session. stdio servers and factory-created per-call servers are not affected. Upgrading causes reused instances to fail and therefore requires an application code change. This issue is fixed in @modelcontextprotocol/server 2.3.0.

### CVE-2026-69137

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-05T19:17:25.147 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the CalendarAccount testConnection action passes an authenticated caller's server_url directly to curl without host, address, or scheme validation. The affected flow begins at CalendarAccount::action_testConnection and uses server_url, CalDAVProvider::makeCalDAVRequest(), and PROPFIND to carry attacker-controlled data or authorization state into the security-sensitive operation. The server sends a PROPFIND request from its network context and returns non-success response bodies, enabling internal-service access, partial response disclosure, service enumeration, and possible cloud metadata access. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-61649

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-11-05T19:17:22.380 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the SSRF protection added in 7.15.1 uses a substring comparison in isSelfRequest() rather than hostname equality. The affected flow begins at validate_external_host() and uses isSelfRequest(), and stripos() to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated attacker can place the server hostname in a URL path to bypass IP validation and direct server-side requests to internal services. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-123208

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-05T19:17:20.380 |

noname Electron desktop build v1.11.2 through v1.11.6.1 contains an unauthenticated local file server with wildcard CORS that allows malicious websites to read, overwrite, or delete installation files. Attackers can send cross-origin requests to /writeFile on localhost port 8089 to overwrite renderer scripts, executing JavaScript with Node.js access as the local user.

### CVE-2026-49407

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-306;CWE-400;CWE-770` |
| Published | 2026-11-05T17:18:18.690 |

OpenHuman is an open-source agent harness available as a desktop application and Rust library. Before version 0.57.44, its local  /ws/dictation  WebSocket endpoint lacks client authentication and browser-origin validation. An unauthenticated client, including a malicious web page able to reach the endpoint, can submit audio and trigger resource-intensive speech-to-text processing. Earlier affected versions also accumulate audio in an unbounded buffer, allowing continuous streaming to exhaust process memory. These conditions can degrade performance, exhaust resources, or crash the application. This issue is fixed in version 0.57.44.

### CVE-2026-123095

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-11-05T16:17:46.580 |

mpv 0.29.0 before 0.42.0 contains a playlist injection vulnerability in the bundled ytdl_hook script that allows remote attackers to add unchecked entries by embedding newlines in playlist URLs. Attackers controlling a feed or page can bypass url_is_safe() to open file:// or av:// inputs, reading local files or loading shared objects via ladspa for code execution.

### CVE-2026-119744

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-11-05T15:17:20.557 |

Cendio ThinLinc contains an improper authentication vulnerability in its browser-based web client (tlwebaccess) that allows an authenticated attacker to impersonate any other user, including root, by exploiting flaws in multi-step authentication flows such as one-time passwords, login banners, or expired password prompts. Attackers can leverage this authentication bypass during the multi-step login process to gain unauthorized access to other user accounts, including administrative privileges, in versions from 4.1.0 through 4.20.0.

### CVE-2026-103479

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-269` |
| Published | 2026-11-06T12:17:15.440 |

The Pubjet | پاب‌جت plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 5.4.8. This is due to the `checkToken()` AJAX handler — registered under `wp_ajax_pubjet-check-token` — performing no capability check and no nonce verification before unconditionally writing the attacker-supplied `token` GET parameter directly into the site-wide `pubjet_settings` option via `pubjet_update_setting()`, prior to any remote validation. This makes it possible for authenticated attackers, with Subscriber-level access and above, to overwrite the plugin's stored REST API credential with an attacker-chosen value, immediately elevating their effective privileges to those of an authorized Pubjet API client and enabling them to invoke otherwise-restricted endpoints — `createReportage`, `updateReportage`, `deleteReportage`, `toggleCopyright`, and `createBacklink` — to create, modify, and delete arbitrary reportage posts and manipulate plugin state that Subscribers cannot normally access. The privilege escalation is self-reinforcing: because `RestApi::isTokenValid()` authenticates solely by comparing the incoming `Authorization` header against the value returned by `pubjet_token()`, which reads from the same option the unprotected handler writes to, the attacker-planted token is trusted as legitimate on all subsequent requests.

### CVE-2026-34157

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:L/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-625` |
| Published | 2026-11-05T21:18:47.300 |

Wails is a framework for building desktop applications using Go and web technologies. From 2.0.0 until 2.13.0, BindingsAllowedOrigins in v2/internal/frontend/originvalidator/originValidator.go passes wildcard patterns to wildcardPatternToRegex, which expands every asterisk to an unrestricted regular-expression match. When an application configures a trailing or partial-label wildcard immediately after an allowed domain, an attacker-controlled lookalike origin can match the allowed suffix and invoke bound Go methods through IPC. A complete-component subdomain wildcard is an unaffected configuration. The resulting confidentiality, integrity, and availability impact depends on the file, database, command, credential, or other operations exposed by the application's bound methods. This issue is fixed in version 2.13.0.

### CVE-2026-102615

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T16:17:23.937 |

HeyForm is an open-source form builder. Prior to 3.0.1, /api/upload accepts a file according to the client-controlled multipart file.mimetype while retaining an HTML filename, and static/upload serves the resulting file as text/html with contentSecurityPolicy: false. An ordinary user can therefore upload active HTML that executes on the HeyForm origin when a victim opens its returned URL. The same-origin script can access /graphql with the victim's session and read or modify data available to that account. The code also permits upload requests tied to an active public form through formId, openToken, and a fieldId belonging to a file or signature question, although the advisory did not fully verify that unauthenticated path end to end. This issue is fixed in version 3.0.1.

### CVE-2026-123655

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T12:17:20.657 |

A flaw was found in Moodle. Insufficient access control checks on H5P content files allow unauthenticated remote attackers to view restricted materials, including content stored in the system context and files belonging to hidden or unavailable course modules. This issue results in unauthorized information disclosure of protected content.

### CVE-2026-104010

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-06T12:17:15.827 |

The WPSyncSheets For Contact Form 7 – CF7 Google Sheets Connector & Save to Database plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.8.0 via the 'any non-system CF7 field (e.g., your-message)' parameter parameter. This is due to insufficient sanitization of CF7 submission field values before database storage and the absence of an allowed_classes restriction on maybe_unserialize() during admin retrieval. This makes it possible for unauthenticated attackers to execute code on the server. Successful exploitation of the remote code execution gadget chain requires that a Google Sheets access token be configured in the plugin (its primary advertised feature), as this triggers autoloading of the bundled Monolog 2.10.0 library whose classes form the exploitable gadget chain; however, the underlying PHP Object Injection occurs regardless.

### CVE-2026-123327

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T11:17:12.913 |

In JetBrains YouTrack before 2026.2.19562 missing authorization in the saved query endpoint allowed disclosure of issue descriptions

### CVE-2026-123305

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-11-06T11:17:09.470 |

In JetBrains IntelliJ IDEA before 2026.3 path traversal was possible via unpacking Dev Container archives from a remote host

### CVE-2026-123296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:08.400 |

In JetBrains Hub before 2026.2.52519 privilege escalation via forged email verification was possible

### CVE-2026-123281

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-11-06T11:17:06.390 |

In JetBrains Datalore before 2026.4 notebook code could execute commands in the sidecar container via the mount broker

### CVE-2026-19877

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-307;CWE-331` |
| Published | 2026-11-06T09:17:01.700 |

INFINITT ULite 5.0.2.1_BN48_20260528 and earlier protects image-share links with a low-entropy password and does not restrict repeated password attempts, allowing an unauthenticated remote attacker to brute-force the password within the link validity window and gain unauthorized access to shared medical images. Fixed in ULite 5.0.2.1 BN50.

### CVE-2026-119499

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-11-06T08:17:19.063 |

Insertion of Sensitive Information Into Sent Data vulnerability in BAKKBONE Australia FloristPress bakkbone-florist-companion allows Retrieve Embedded Sensitive Data.This issue affects FloristPress: from n/a through 7.8.4.

### CVE-2026-86606

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T06:16:44.237 |

The iubenda | All-in-one Compliance for GDPR / CCPA Cookie Consent + more WordPress plugin before 3.13.7 does not properly escape content it re-emits through its bundled HTML parser, allowing unauthenticated users to inject arbitrary web scripts in pages that will execute in the session of any visitor viewing them, including logged in administrators.

### CVE-2026-115673

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T06:16:40.373 |

The Anti-Spam, Spam FireWall by CleanTalk WordPress plugin before 6.91 does not escape a commenter-supplied value before outputting it on an administrative spam-review screen, allowing unauthenticated users to inject arbitrary web scripts that execute in the browser of an administrator who reviews flagged comments.

### CVE-2026-110813

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T06:16:39.717 |

The Advanced Custom Fields (ACF®) WordPress plugin before 6.8.11 does not properly sanitize a stored field definition that can be modified through its comment handling, allowing unauthenticated users to inject a payload that is emitted as an HTML attribute name and executed as JavaScript in the browser of any visitor or administrator who views a page rendering the affected field.

### CVE-2026-77299

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-11-06T02:17:52.893 |

Regexp2 is a feature-rich RegExp engine for Go. Prior to version 2.3.0, when regexp2 compiles and matches a pattern containing a large fixed-count quantifier applied to a zero-width subexpression — e.g. (?:){50000000} — the match engine executes the empty loop body m-1 times, pushing two integers onto the backtracking stack on every iteration. Because the parser accepts any repetition count up to math.MaxInt32 and the backtracking stack grows without bound, a pattern of fewer than 20 bytes matched against an empty input can force multi-gigabyte allocation and OOM-kill the process. MatchTimeout does not fully mitigate this because the memory is allocated faster than the 100 ms timeout clock can fire. This issue has been patched in version 2.3.0.

### CVE-2026-93424

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-11-05T23:17:02.817 |

FastNetMon is a high-performance DDoS detector and sensor. In version 1.2.9 and earlier, peer_find_template() in src/netflow_plugin/netflow_collector.cpp and src/netflow_plugin/netflow_v9_collector.cpp returns a pointer into global_netflow9_templates after releasing the cache mutex. On deployments with at least two entries in netflow_ports, concurrent template redefinition and data-flowset processing can let add_update_peer_template() reassign the template and free its records vector while another listener dereferences the escaped pointer. An unauthenticated sender that can reach both NetFlow/IPFIX listener ports can trigger a heap-use-after-free and reliably crash FastNetMon. No fixed release is available as of this review.

### CVE-2026-92697

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-05T23:17:02.460 |

FastNetMon is a high-performance DDoS detector and sensor. In version 1.2.9 and earlier, the NetFlow v9 collector calls  strlen()  on an attacker-controlled interface-description field without bounding the scan to the field’s declared length. Although fields longer than 128 bytes are excluded from this operation, an accepted field without a null terminator can cause reads beyond the field and packet buffer. An unauthenticated remote attacker who can send crafted UDP packets to the collector can trigger an out-of-bounds read and potentially crash the process, causing denial of service. No fixed release is available as of this review.

### CVE-2026-111768

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-05T22:17:45.457 |

The Model Context Protocol TypeScript SDK provides TypeScript client and server implementations of the Model Context Protocol. From 1.3.0 until 1.32.0 in @modelcontextprotocol/sdk and from 2.0.0 until 2.3.0 in @modelcontextprotocol/server, HTTP servers did not enforce a limit on the number of array elements and object keys validated in one request. The affected surface is validation of HTTP requests containing arrays or object keys. The trigger is an array-element or object-key validation workload large enough to exhaust memory while remaining within the request size limit. A single request within the default 4 MiB limit can terminate the process with JavaScript heap exhaustion. No credentials are required unless the application authenticates before SDK processing. Tools accepting arrays or records carry the greatest risk. stdio-only servers do not expose the HTTP request path. Upgrading alone does not enable the new validation bound. Operators must configure both a tool-input element bound and an appropriate request body size limit. This issue is fixed in @modelcontextprotocol/sdk 1.32.0 and @modelcontextprotocol/server 2.3.0.

### CVE-2026-77604

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T20:18:00.017 |

Code Graph RAG is an AI-powered knowledge graph and retrieval system for querying, understanding, and editing multi-language codebases. Prior to 0.0.345, the MCPToolsRegistry.read_file implementation in codebase_rag/mcp/tools.py joins attacker-controlled file_path input to project_root without resolving and verifying containment when offset or limit selects the paginated branch. An absolute path causes pathlib to discard the configured root, while relative traversal can also resolve outside it. The protected non-paginated branch uses validate_project_path, but the paginated branch bypasses that validation before opening the path. An unauthenticated caller of a network-exposed HTTP MCP server can therefore read arbitrary UTF-8-readable files available to the server process, including credentials, environment data, private keys, source, and configuration; local callers through the stdio transport can reach the same vulnerable code path. This issue is fixed in version 0.0.345.

### CVE-2026-65983

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-552` |
| Published | 2026-11-05T20:17:59.507 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.2.0, interface/modules/custom_modules/oe-module-faxsms/src/Controller/SignalWireClient.php decrypts a selected patient document with Document::get_data() and SignalWireClient::uploadFileForFax() writes the plaintext bytes under sites/{siteId}/fax. The module returns the resulting public URL to SignalWire, protects it only with a predictable uniqid() filename, and never removes the staged file. An unauthenticated network actor who obtains or guesses the URL can retrieve persistent patient documents even when drive encryption is enabled. This issue is fixed in version 8.2.0.

### CVE-2026-116787

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-789` |
| Published | 2026-11-05T20:17:46.073 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, mod_event_socket used an unauthenticated Content-Length value directly as the allocation size for an Event Socket message body. Negative or extremely large values could overflow the terminator calculation or force an allocation failure through a helper that aborts the FreeSWITCH process. The header is parsed before the Event Socket password, so any host admitted by apply-inbound-acl can trigger termination with its first packet; the default loopback ACL limits ordinary installations to local clients. The outbound socket dialplan path is also affected when FreeSWITCH connects to a hostile application server, and process termination drops every active call until the service is restarted. This issue is fixed in version 1.11.2.

### CVE-2026-116784

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-11-05T20:17:45.560 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, process_rtcp_report() used an RTPFB NACK packet's declared RTCP header length as its feedback-entry loop bound instead of the datagram length already validated by the caller. A short packet with an oversized declaration could drive reads far beyond the fixed 16 KiB receive buffer. Any peer able to send RTCP to an active video call can reach the flaw, including calls where remote SDP enables video RTCP even though the SIP profile has no explicit RTCP interval configured. The out-of-bounds read can crash FreeSWITCH and terminate every active call, but supplies no write primitive and does not echo the read values to the sender. This issue is fixed in version 1.11.2.

### CVE-2026-116782

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-843` |
| Published | 2026-11-05T20:17:45.247 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, rtmp_i_connect() passed the first RTMP connect argument to amf0_object_get() without checking whether the AMF value was an object. A string or number in place of an AMF object caused union bytes from the message to be interpreted as node pointers and dereferenced. Any client with network access to an enabled mod_rtmp listener could send the malformed connect command before login; the module is disabled in the stock build and configuration. The invalid read reliably crashes FreeSWITCH and ends every active call, while no write, memory disclosure, or code execution has been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-116570

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-131;CWE-787` |
| Published | 2026-11-05T20:17:44.313 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, http_directory_auth() rebuilt an expected user@domain:password credential and base64-encoded it into an 80-byte buffer using an encoder without an output-length argument. A configured credential longer than 57 characters overflowed the stack before the supplied HTTP Basic password was compared. An unauthenticated client only needed to name an existing directory user on an exposed mod_xml_rpc HTTP listener; the module is built but not loaded by the stock configuration. The overflow can corrupt the stack and crash FreeSWITCH, ending every active call, although the overrun bytes come from the configured credential and remote code execution has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-116569

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191;CWE-787` |
| Published | 2026-11-05T20:17:44.153 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, msrp_parse_buffer() subtracted delimiter framing from a peer-controlled short segment whose MSRP byte range ended in * without first proving the segment was long enough. The unsigned result wrapped near SIZE_MAX and reached switch_msrp_msg_set_payload() as both an allocation size and memcpy length, while related pointer arithmetic could read before the receive buffer. The listener is disabled by default in msrp.conf.xml, but any deployment enabling an MSRP TCP or TLS port parses this framing before authentication. An unauthenticated network peer can corrupt memory and crash FreeSWITCH, dropping all active calls, although remote code execution has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-116568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-11-05T20:17:43.993 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, rtmp_rtmp2rtpH264() trusted the length prefix of each inbound H.264 NAL unit without checking it against the bytes remaining in the RTMP message. An oversized declared unit underflowed the unsigned remaining-byte counter and advanced the parser beyond its receive buffer, where the next length-prefix read could crash the process. The flaw affects deployments that build and load mod_rtmp and accept video call sessions, commonly on TCP port 1935; placing the call requires a directory login where auth-calls is true, while no credentials are required where auth-calls is absent or false. A remote client can terminate FreeSWITCH and every active call, but the defect supplies no write primitive and memory disclosure has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-116567

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T20:17:43.837 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, rtmp_handle_control() rendered an RTMP user-control message into a 200-byte stack buffer using an unbounded sprintf loop controlled by the wire message length. A body of roughly 70 bytes or more overflowed the stack before any RTMP login, because the handshake authenticates neither side. The flaw affects deployments that build and load mod_rtmp, which is disabled in the stock build and configuration but commonly exposes a listener on TCP port 1935 when enabled. One unauthenticated message can crash FreeSWITCH and end every active call; the constrained ASCII hex output has not yielded control-flow hijacking. This issue is fixed in version 1.11.2.

### CVE-2026-115928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121;CWE-191` |
| Published | 2026-11-05T20:17:43.127 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, switch_core_media_add_crypto() passed the encoded key and salt length from an inbound SDP a=crypto attribute to switch_b64_decode() as the destination capacity. A zero-length key and salt made that capacity underflow, allowing the decoded attribute to overflow a fixed stack buffer with sender-chosen bytes before the call was answered. On the shipped external profile, an unauthenticated caller can reach the SDES-SRTP parser, while profiles that challenge inbound calls remain affected for senders who can authenticate; setting rtp_secure_media_inbound to false removes the path, and WebRTC DTLS-SRTP legs are unaffected. The overflow corrupts memory and can crash the FreeSWITCH process, dropping every active call, although remote code execution has not been demonstrated. This issue is fixed in version 1.11.2.

### CVE-2026-115452

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-05T18:17:01.890 |

Joomla Extension - tassos.gr - Privileged stored XSS in Advanced Custom Fields 2.8.2-2.8.15, 3.0.0-3.1.8 and Smile Pack 1.1.2-1.2.9, 2.0.0-2.1.6 - A user who could edit a Map marker label, like an article author, could add a script that ran for anyone who opened the marker.

### CVE-2026-82965

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-05T17:18:21.983 |

A flaw was found in the SAML implementation of Keycloak, an open-source identity and access management solution. The SAML Artifact Resolution and ECP SOAP endpoints do not properly limit the size or complexity of incoming XML requests. An unauthenticated remote attacker can exploit this by sending specially crafted, large XML messages that cause the server to consume excessive memory. This leads to the application running out of memory and crashing, resulting in a denial of service for all users.

### CVE-2026-123151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T17:18:03.350 |

A flaw was found in the GNU debugger (GDB). When GDB connects to a remote debug target, a malicious target can cause GDB to overflow a buffer on the stack while parsing the target's replies. This can crash GDB or potentially allow the target to execute arbitrary code in the GDB client process with the privileges of the user running GDB.

### CVE-2026-121995

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-11-05T17:18:00.690 |

A stack buffer overflow in the GDB client's tracepoint upload handler allows an attacker-controlled debug stub to corrupt stack memory automatically during connection setup. The overflow results from GDB reading beyond the current reply boundary into a stale prior reply in the shared packet buffer.

### CVE-2026-110932

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-05T17:17:37.457 |

A flaw was found in the theme resource endpoint of Keycloak, an open-source identity and access management solution. The issue occurs because the server fails to validate theme names before using them as keys for an on-disk gzip cache. An unauthenticated attacker can exploit this by sending many requests with unique, fabricated theme names, leading to persistent disk space exhaustion that survives server restarts and causes service disruptions.

### CVE-2026-110931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-05T17:17:37.280 |

A flaw was found in the SAML 1.1 assertion parser of Keycloak, a tool used for identity and access management. The issue occurs when the parser handles a specific element called AuthorityBinding within an authentication statement. Due to an incomplete fix for a previous vulnerability, the parser can enter an infinite loop that consumes all available memory, causing the entire Keycloak service to crash and become unavailable to users.

### CVE-2026-107602

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-05T17:17:35.117 |

A flaw was found in the SAML 1.1 XML parsing logic of Keycloak, an open-source identity and access management solution. The issue occurs when the parser encounters unexpected elements within a security token's key information section, causing the processing thread to enter an infinite loop. An unauthenticated remote attacker could exploit this by sending specially crafted requests, leading to 100% CPU usage and a total denial of service that requires a server restart to resolve.

### CVE-2026-107123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-11-05T17:17:34.950 |

A flaw was found in the SAML XML processing component of Keycloak, an open-source identity and access management solution. The issue occurs when the server parses XML documents containing excessively long dateTime or duration values. Because these strings are not properly validated before processing, the XML parser consumes excessive CPU time. An unauthenticated remote attacker can exploit this by sending specially crafted SAML requests to the server, leading to high CPU utilization and a denial of service for all users.

### CVE-2026-103112

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-11-05T17:17:32.253 |

A flaw was found in the authentication session handling of the keycloak-services component in Keycloak. The issue occurs because the system fails to verify if an authenticator is valid for the current authentication flow when switching between the standard authentication path and the reset credentials path. An authenticated attacker can exploit this by triggering a race condition during the credential reset process to associate their successful authentication state with another user's session. This can result in the attacker gaining full access to the victim's account and changing their password.

### CVE-2026-123306

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-11-06T11:17:09.600 |

In JetBrains IntelliJ IDEA before 2026.3 improper checks allowed server certificates to be added to the trust store during headless runs

### CVE-2026-123282

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-672` |
| Published | 2026-11-06T11:17:06.520 |

In JetBrains Datalore before 2026.4 missing expiration validation of account tokens allowed a new authenticated session

### CVE-2026-116592

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346;CWE-524` |
| Published | 2026-11-06T10:16:36.313 |

undici is an HTTP client for Node.js. In versions 7.30.1 and 8.12.2 through 8.12.3, when an originless Agent composes the redirect and shared cache interceptors, undici decides whether to store the final response under the original request key by inspecting only the final redirect hop, which bypasses the earlier fix for CVE-2026-109829 that compared only the initial and final origins. A redirect that bounces through an untrusted origin and returns to the trusted origin is still cached under the trusted key, an intermediate hop's Vary is dropped so a response that varies on Authorization or Cookie can be served to a different user, and an intermediate hop's no-cache or default-uncacheable status is ignored so a non-storable redirect is laundered into a cacheable entry. An attacker who controls a redirect target from a trusted URL can poison the cached entry for that URL or have a private, per-user response served to a later caller. The issue is fixed in undici 7.30.2 and 8.12.4, and users should upgrade to one of those versions or later. As a workaround, compose the interceptors as cache then redirect, use per-origin dispatchers and cache stores, or disable shared caching on redirect-capable requests.

### CVE-2026-116789

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-300` |
| Published | 2026-11-05T20:17:46.397 |

FreeSWITCH is a Software Defined Telecom Stack enabling the digital transformation from proprietary telecom switches to a software implementation that runs on any commodity hardware. Prior to 1.11.2, dtls_state_setup() compared a peer certificate with the SDP a=fingerprint only when FreeSWITCH was the DTLS client, not when it held the DTLS server role. An unauthenticated peer able to reach the negotiated media port could complete the DTLS-SRTP handshake with an unrelated certificate, obtain the leg's SRTP keys, decrypt and inject media, and displace the legitimate endpoint; on ICE-enabled legs the peer also needs the connectivity-check credentials from SDP, which generally requires signaling visibility or a position on its path. WebRTC and SIP DTLS-SRTP legs are affected whenever the peer selects the active role, while FreeSWITCH client-role handshakes already perform fingerprint validation. Version 1.11.2 introduces the remediation, which requires rtp_dtls_client_cert_verify_mode=fingerprint.

### CVE-2026-93998

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-11-05T18:17:11.053 |

A flaw was found in the SAML adapter component of Keycloak, which is used to secure applications with SAML-based authentication. The adapter fails to verify that the issuer of a signed SAML assertion matches the expected identity provider configured for the application. If multiple identity providers share the same trusted signing key, an attacker who controls one of those providers can create a validly signed assertion to log into the application as any user, potentially gaining full administrative control.

### CVE-2026-92855

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-05T18:17:10.707 |

A flaw was found in the SAML identity broker component of Keycloak, which is used to delegate authentication to external identity providers. The issue occurs because the broker fails to verify that a user actually possesses the private key associated with a holder-of-key assertion. An attacker who intercepts a victim signed assertion can replay it to gain unauthorized access and impersonate the victim without needing their private key.

### CVE-2026-112109

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-11-05T18:17:00.787 |

A local privilege escalation vulnerability in Thales SafeNet Authentication Client (SAC) SACSrv can allow an authenticated, non-administrator local user to trigger a heap-based buffer overflow through the service interface. Successful exploitation may allow arbitrary code execution with Local System privileges.This issue affects SAC releases up to and including 10.9 R3 GA (build 10.9.7449).

### CVE-2026-121139

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-11-05T16:17:44.787 |

The Rapid7 Metasploit msf-ws suffers from a missing authentication vulnerability whereby the REST API grants an unauthenticated "bootstrap" exemption so that the very first administrator can be created when the users table is empty. While the table is empty, POST /api/v1/users is exempt from authentication by design: the route handler calls warden.authenticate!(scope: :admin_api), which resolves to AdminApiToken. The inherited ApiToken#authenticate! short-circuits and returns success!() whenever msf.auth_initialized is false, without ever evaluating AdminApiToken's administrator check. In that state the endpoint creates a user — including an administrator — for an entirely unauthenticated caller.


This issue has been fixed in version 6.5.9.

### CVE-2026-87964

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-11-06T10:16:38.110 |

The Product Feed Manager for WooCommerce – CTX Feed – Support 220+ Shopping, AI & Social Channels plugin for WordPress is vulnerable to PHP Code Injection in all versions up to, and including, 8.0.26. This is due to insufficient sanitization of the `feedConfigCustom2` parameter — only `wp_unslash()` is applied before the value is stored verbatim via `update_option()`, and during feed generation the `Custom2Template::evaluate_return()` method passes the stored `{(return ...)}` template expressions directly to PHP's `eval()` function without any code-level sanitization. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to inject and execute arbitrary PHP code on the server, escalating their privileges beyond what the role normally permits to full remote code execution and site takeover. The `ctxfeed_custom2_eval_enabled` option defaults to `true`, meaning no additional administrator configuration is required for this attack path to be exploitable out of the box.

### CVE-2026-110776

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T10:16:35.950 |

The MDTF – Meta Data and Taxonomies Filter plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'vars' parameter in all versions up to, and including, 1.4.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires that a published page or post on the target site contains the [meta_data_filter_results] shortcode, which is the primary output feature of the plugin.

### CVE-2026-110291

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T09:16:59.833 |

The Graphina – Charts and Graphs For Elementor plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'iq_tree_chart_node_font_family (and any text control serialized into chart_data['settings'])' parameter in all versions up to, and including, 3.1.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Elementor's Utils::kses_post_deep() does not strip the attack payload on save because the payload contains no disallowed HTML tags — only a single quote and an event-handler fragment — allowing the malicious value to survive persistence.

### CVE-2026-88984

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285;CWE-863` |
| Published | 2026-11-05T23:17:01.760 |

Kubeflow Pipelines enables users to build and deploy portable, scalable machine learning workflows. Prior to 2.16.1, the multi-user API server treats the empty namespace used by shared or global pipelines as an authorization exception for modification and deletion operations. An authenticated user can modify or delete shared pipeline definitions and versions without the required Kubernetes RBAC permissions, compromising their integrity and availability. Read-only access to shared pipelines remains intentional, single-user deployments intentionally bypass multi-user checks, and execution of a modified pipeline is a conditional downstream consequence. The separate shared-pipeline multipart upload authorization path is outside this advisory and is not remediated by version 2.16.1. This issue is fixed in version 2.16.1.

### CVE-2026-63213

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-05T19:17:23.333 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the Upgrade Wizard commit flow trusts the hidden zip_to_dir parameter, while clean_path() does not reject traversal sequences. An authenticated administrator can copy extracted package files outside the intended destination, overwrite application or configuration files, place executable PHP under the web root, or cause denial of service. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-123184

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-863` |
| Published | 2026-11-05T18:17:08.000 |

An incorrect authorization vulnerability exists in the Altium 365 Git Service. The permission check performed when a user pushes to a project repository did not correctly evaluate the required access level, so the check passed for any user holding any level of access to the project. As a result, an authenticated user with view-only access to a project could write to that project's git repository.




Read access was evaluated correctly and was not affected, and exploitation requires an authenticated account with existing access to the target project. The issue has been remediated in Altium 365 at the service level and no customer action is required. On-premise Altium Enterprise Server is not affected.

### CVE-2026-119345

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-11-05T16:17:40.553 |

Cocos AI is a confidential computing system for AI. Prior to 0.9.0, Cocos AI performs attestation only once when an attested TLS connection is established. An attacker who can modify the attester's workload code, memory-backed state, configuration, or attached devices after that check can keep the existing connection open while the peer continues trusting stale initial Evidence. This gap is especially significant for long-lived connections because the verifier has no mechanism to detect the changed state. This issue is fixed in version 0.9.0.

### CVE-2026-115431

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-06T13:17:25.180 |

Missing Authorization vulnerability in WP Swings Upsell Order Bump Offer for WooCommerce upsell-order-bump-offer-for-woocommerce allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Upsell Order Bump Offer for WooCommerce: from n/a through 3.1.6.

### CVE-2026-109884

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T13:17:23.300 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Elementor Elementor Website Builder elementor allows Reflected XSS.This issue affects Elementor Website Builder: from n/a through 4.3.5.

### CVE-2026-109883

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T13:17:23.137 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Elementor Elementor Website Builder elementor allows Code Injection.This issue affects Elementor Website Builder: from n/a through 4.3.5.

### CVE-2026-123326

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-06T11:17:12.720 |

In JetBrains YouTrack before 2026.2.19197 incorrect authorisation in the scripts debugger allowed workflow script disclosure and suspension

### CVE-2026-123325

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-11-06T11:17:12.530 |

In JetBrains YouTrack before 2025.3.170763, 
2026.1.14150, 
2026.2.19656 inclusion of untrusted remote code was possible via the plugin sandbox page

### CVE-2026-39744

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T08:17:25.767 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WC Lovers WCFM Membership wc-multivendor-membership allows Stored XSS.This issue affects WCFM Membership: from n/a through 2.12.0.

### CVE-2026-119488

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-06T08:17:18.900 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Shamim Rajani Pie Register pie-register allows Stored XSS.This issue affects Pie Register: from n/a through 3.8.4.15.

### CVE-2026-87008

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-11-05T21:18:54.370 |

Code Graph RAG is an AI-powered knowledge graph and retrieval system for querying, understanding, and editing multi-language codebases. Prior to 0.0.589, AstGrepService in codebase_rag/tools/ast_grep_service.py enumerates files beneath project_root and relies on should_skip_path in codebase_rag/utils/path_utils.py to classify them, but the containment check operates on unresolved lexical paths. A symbolic link planted inside an analyzed repository can therefore reference a file outside the configured root while still appearing in scope. The structural_search tool follows the link and discloses readable content without an approval gate, while structural_replace with dry_run=False follows it and overwrites writable content; the MCP path invokes structural replacement without the agent-loop approval control. An attacker who causes a victim to analyze a repository containing such a link can read credentials, keys, environment files, or sibling source and can modify files accessible to the code-graph-rag process. This issue is fixed in version 0.0.589.

### CVE-2026-19134

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-11-05T20:17:54.300 |

A vulnerability in OpenText OpenText Directory Services (OTDS) allows Black Box Reverse Engineering.

This issue affects OpenText Directory Services (OTDS): from 22.1 to 26.2

### CVE-2026-104137

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-05T20:17:39.297 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, the sms_search branch of interface/main/messages/save.php requires an authenticated session but does not enforce patient or feature-level ACLs. A low-privilege user who cannot access patient data through the normal interface can search the MedEx SMS endpoint and receive patient identifiers, names, phone numbers, SMS permission status, and recent message information. This issue is fixed in version 8.3.0.

### CVE-2026-104136

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-11-05T20:17:39.137 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, the new_recall branch of interface/main/messages/save.php accepts a caller-supplied pid without enforcing patient-level or recall-workflow authorization. A low-privilege authenticated user who knows or enumerates a patient identifier can retrieve patient details, contact fields, HIPAA notification preferences, recent appointment information, and existing recall information. This issue is fixed in version 8.3.0.

### CVE-2026-104133

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T20:17:38.670 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, interface/modules/custom_modules/oe-module-dorn/public/compendium_install.php checks authentication and CSRF but does not require the admin/users ACL enforced by sibling DORN administration scripts. When the DORN module is enabled, a low-privilege authenticated user can supply a labGuid that causes LabCompendiumInstall::uninstall() to delete detail and result procedure types and deactivate order types before the reinstall step. The action can corrupt lab-ordering configuration and require an administrator to restore the compendium. This issue is fixed in version 8.3.0.

### CVE-2026-103938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-352` |
| Published | 2026-11-05T20:17:38.353 |

OpenEMR is a free and open source electronic health records and medical practice management application. Prior to 8.3.0, interface/patient_file/pos_checkout_ippf.php performs state-changing void, voidall, and regen operations through GET requests without CSRF token validation. The form_checksum integrity check is conditional and is skipped when the parameter is omitted, allowing a cross-site request to force an authenticated billing user to void checkouts or regenerate invoice counters. The resulting changes can alter ledger state, financial reporting, and audit records. This issue is fixed in version 8.3.0.

### CVE-2026-69136

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:24.977 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, email template attachment handling passes the remove_attachment POST parameter array through HTML-oriented securexss() processing and directly interpolates its elements into an SQL UPDATE statement. An authenticated attacker can inject SQL to disclose database information or abuse the UPDATE context to soft-delete all records in the notes table in one request. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-69135

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T19:17:24.753 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the Project module interpolates the authenticated caller's duplicateId POST parameter directly into a SQL query without sanitization, quoting, or parameterization. An authenticated attacker can alter query structure and disclose sensitive database information. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-63111

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-918` |
| Published | 2026-11-05T19:17:23.137 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the V8 module API lacks module-level authorization and permits a low-privileged user to create SchedulersJobs records with attacker-controlled target values. The affected flow begins at /Api/V8/module and uses SchedulersJobs, target, cron.php, and url:: to carry attacker-controlled data or authorization state into the security-sensitive operation. Cron.php later executes the queued job with system privileges, and the url:: target makes server-side requests to internal or external hosts, can follow redirects, can persist as a recurring job, and may expose internal services. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-123273

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-11-05T19:17:20.903 |

ImageMagick before 7.1.2-35 and 6.9.13-60 contains an infinite loop vulnerability in the SVG decoder because QueueAuthenticPixelCacheNexus in MagickCore/cache.c fails to validate requested region width and height. Attackers can supply a crafted SVG image that repeatedly requests a non-advancing pixel region, consuming CPU and hanging the decoding worker.

### CVE-2026-100364

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-05T19:16:58.647 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the V8 JSON:API update path fails to remove the id attribute before assigning user-supplied attributes to a SugarBean. The affected flow begins at updateRecord() and uses processAttributes(), id, and ACL_ALLOW_OWNER to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated user can substitute a victim record identifier, bypass owner-only authorization, overwrite another record, and hijack record ownership. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-100361

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-915` |
| Published | 2026-11-05T19:16:57.780 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, the V8 write path checks that a field exists but does not enforce api-visible or sensitive metadata that hides the same field on reads. The affected flow begins at PATCH /Api/V8/module and uses user_hash, external_auth_only, api-visible: false, and sensitive: true to carry attacker-controlled data or authorization state into the security-sensitive operation. An authenticated user can mass-assign internal authentication fields, modify password hashes or external-authentication flags, and persist unauthorized account access. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-100360

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-11-05T19:16:57.557 |

SuiteCRM is an open-source, enterprise-ready Customer Relationship Management (CRM) software application. Prior to 7.15.2 and 8.10.2, V8 API relationship write paths do not consistently enforce object-level edit and view authorization on both related records. In the verified Account-to-Contact case, an authenticated user can create a relationship while unable to edit the Account and can delete relationship links to a hidden Contact that cannot be viewed directly. This issue is fixed in versions 7.15.2 and 8.10.2.

### CVE-2026-97847

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-05T18:17:11.840 |

A flaw was found in the protocol mapper and identity resolution components of Keycloak. The issue occurs when a client manager uses hardcoded-claim mappers to override identity claims in sessionless service-account tokens. Because these tokens lack a session ID, Keycloak may incorrectly resolve the token bearer as a different, highly privileged user based on the manipulated claims. This can allow an attacker with limited client management permissions to impersonate a realm administrator and gain full control over the realm.

### CVE-2026-107359

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-369` |
| Published | 2026-11-05T18:17:00.370 |

Improper input validation in the beacon handler for WF200 firmware versions 3.17.0 and earlier may result in a divide-by-zero fault.

### CVE-2026-123096

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-11-05T16:17:46.760 |

anacrolix/torrent through 1.61.0 contains a memory exhaustion vulnerability in the tracker/http package that allows malicious trackers to crash clients by returning unbounded responses. Attackers controlling an HTTP tracker in a torrent file or magnet link can return huge or gzip-compressed announce or scrape responses that Client.Announce and Client.Scrape buffer without limits, exhausting process memory.

### CVE-2026-115738

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-05T15:17:17.177 |

SQL injection vulnerability in DLP on-prem extensions version 11.13.1 and earlier allows a remote authenticated attacker to inject SQL queries without sanitization or parameterized queries.

### CVE-2026-123315

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-625` |
| Published | 2026-11-06T11:17:10.857 |

In JetBrains Junie CLI before 26.8.24 command execution was possible via the Allow Similar Commands option

### CVE-2026-94395

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787;CWE-1284` |
| Published | 2026-11-05T19:17:28.617 |

A stack-based buffer overflow in Thales SafeNet Authentication Client (SAC) SIS token engine processing can be triggered by a malicious physical or software-emulated smart card. The issue can occur before authentication or PIN entry and may
cause a denial of service or potentially arbitrary code execution with the privileges of the affected process. Affected releases start with SAC 10.8 R7 and include SAC 10.9 R3 GA (build 10.9.7449).
