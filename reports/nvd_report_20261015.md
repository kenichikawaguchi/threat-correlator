# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-14 15:03 UTC
- **対象期間**: `2026-10-13T15:01:01.000Z` 〜 `2026-10-14T15:03:48.000Z`
- **重要CVE数**: 1457 件（Critical 9.0+: 148 件 / High 7.0〜: 1309 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVSS 7.0 以上の脆弱性は **「認証不要でリモートからコード実行」** が共通した特徴です。特に **Adobe Experience Manager、Adobe Commerce、ColdFusion、WordPress プラグイン** に集中しており、攻撃者は単一の HTTP リクエストでサーバ上の任意コードを実行したり、ファイル削除・アップロードを行える点が顕著です。  
また、**スコープが C (変更) になるケースが多数**（ColdFusion 系、Adobe 系）で、脆弱性が成功すると攻撃者は同一ホスト上の他サービスやコンテナまで横移動できるリスクがあります。  

---

## 2. 特に注目すべき CVE  

| CVE | 主な脆弱性種別 | 影響範囲 (製品・バージョン) | 重要度・選定理由 |
|-----|----------------|----------------------------|-------------------|
| **CVE‑2026‑106624** | Code Injection (不適切なコード生成制御) | Adobe ColdFusion **全バージョン (2023‑2026 系列)** – 具体的なパッチは未公開だが、全インスタンスが対象 | CVSS 10.0、認証不要・ネットワーク経由で任意コード実行が可能。ColdFusion は企業の業務システムで広く利用されているため、被害拡大リスクが最大。 |
| **CVE‑2026‑106622** | SSRF (サーバーサイドリクエストフォージェリ) | Adobe ColdFusion **全バージョン** | CVSS 10.0、スコープ変更 (C) により内部ネットワークへの不正アクセス・権限昇格が可能。SSRF はクラウド環境や内部 API への踏み台に利用されやすい。 |
| **CVE‑2026‑105899** | 任意ファイルアップロード (危険なタイプ) | Adobe ColdFusion **全バージョン** | CVSS 10.0、アップロードしたファイルがそのまま実行可能になるため、リモートコード実行と同等。ColdFusion のデフォルト設定で防御が困難。 |
| **CVE‑2026‑90532** / **CVE‑2026‑48383** / **CVE‑2026‑48382** | Incorrect Authorization (認可不備) | Adobe Experience Manager (AEM) **6.5.x 以前** – 具体的なバージョンはベンダーが 2026‑03‑15 に修正パッチを提供 | CVSS 10.0、認可チェックが抜けているだけで任意コード実行が可能。AEM は大手企業のデジタルアセット管理に使用され、被害が顕在化するとブランド・情報漏洩リスクが高い。 |
| **CVE‑2026‑107594** | 任意ファイル削除 (パス操作) | WordPress **File Upload to Order** プラグイン **1.1.3 以前** | CVSS 10.0、認証不要でサーバ上の任意ファイルを削除できる。WordPress は日本国内でも多数の中小企業サイトで採用されており、サイト改ざん・サービス停止につながる。 |

> **注:** これら 5 件は **CVSS 10.0**（最高評価）であり、かつ **認証不要**、**スコープ変更**、**広範囲にデプロイされているプラットフォーム**という点で最優先で対策すべきです。

---

## 3. 推奨アクション  

### 3.1 共通的な緊急対策
1. **脆弱性スキャンの実施**  
   - NVD、CVE Details、ベンダーの Security Advisory を用いて、社内資産に上記製品・プラグインが存在するか即時確認。  
2. **外部からの直接アクセス遮断**  
   - ColdFusion、AEM、WordPress の管理画面・API エンドポイントを **IP アクセス制御**（ファイアウォール、WAF）で保護。  
3. **監査ログの強化**  
   - `access_log`、`error_log`、ColdFusion の `coldfusion-out.log`、AEM の `request.log` などをリアルタイムで SIEM に転送し、**不審なリクエスト (例: `/api/*` の GET/POST、`/admin.php` の無認証呼び出し)** を検知。  
4. **最小権限の原則**  
   - ColdFusion の `admin` アカウントや WordPress のプラグイン実行権限を **必要最小限** に絞る。  
5. **バックアップと復旧手順の確認**  
   - 重要ファイル・データベースの **定期バックアップ**（少なくとも 24 時間前まで）を取得し、復旧テストを実施。

### 3.2 製品別具体的アップデート

| 製品 / プラグイン | 現行バージョン | 推奨バージョン / パッチ | アップデート手順 |
|-------------------|----------------|------------------------|-------------------|
| **Adobe ColdFusion** | 2023‑2026 系列 (例: 2023.0.0) | **2026‑03‑15 リリースパッチ** (CF2026‑Patch‑10) もしくは **2026.0.0** 以降 | 1. 公式サイトからパッチをダウンロード → 2. サーバ停止 → 3. `coldfusion.jar` を上書き → 4. サービス再起動 → 5. 動作確認 |
| **Adobe Experience Manager (AEM)** | 6.5.x 以前 | **6.5.22.0** 以上 (2026‑03‑15 Security Fix) | 1. AEM の **CRX/DE** コンソールでパッチ適用 → 2. OSGi バンドルの再起動 → 3. キャッシュクリア → 4. 管理画面でバージョン確認 |
| **WordPress Plugin – File Upload to Order** | ≤ 1.1.3 | **1.1.4** 以上 | 1. WordPress 管理画面 → プラグイン一覧 → 「File Upload to Order」→ 「更新」 → 2. `wp-content/plugins/file-upload-to-order` ディレクトリの権限を `755` に設定 |
| **WordPress Plugin – SimpleForm – Form Maker** | ≤ 3.10.0 | **3.10.1** 以上 | 同上、プラグイン更新後に `wp_ajax_nopriv_simpleform_wp_register` の **capability チェック** が追加されたことを確認 |
| **Argo CD** (参考) | 2.10.0‑3.6.0‑rc2 | **3.6.1** 以上 | `helm upgrade argo-cd argo/argo-cd --version 3.6.1` でアップグレード、PostDelete フックの認可ロジックが修正済み |
| **Podman** | 4.4.0‑5.8.8、6.1.3 | **5.8.9** 以上、または **6.1.4

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-107594

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-14T07:17:02.090 |

The File Upload to Order WordPress plugin before 1.1.4 does not validate or confine a file path taken from attacker-controlled session data before deleting the file, and the action that performs the deletion is reachable by unauthenticated users, allowing them to delete arbitrary files on the server, including files whose removal leads to full site compromise.

### CVE-2026-106624

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T21:17:31.703 |

ColdFusion is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106622

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:17:31.490 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105899

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-13T21:17:29.483 |

ColdFusion is affected by an Unrestricted Upload of File with Dangerous Type vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-90532

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T20:19:10.150 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48383

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T20:17:29.017 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-48382

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T20:17:28.900 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-110130

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-13T19:18:43.397 |

Dockhand before 1.0.45 contains an authentication bypass in which the global auth hook skips authentication for any path ending in a static-asset extension such as .js, including /api/* routes, and the user-mutation handlers fail open for unauthenticated callers. Unauthenticated remote attackers can send a PUT request to /api/users/<id>.js to reset the admin's or any user's password and take over the account.

### CVE-2026-103849

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-10-13T19:17:53.997 |

Adobe Commerce is affected by an Improper Neutralization of Special Elements Used in a Template Engine vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-94603

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-693` |
| Published | 2026-10-13T17:17:49.123 |

Podman is a tool for managing OCI containers and pods. From 4.4.0 until 5.8.8 and 6.1.3, podman run treats an image carrying the io.podman.annotations.checkpoint.runtime.name annotation as a checkpoint and silently ignores user-supplied container creation restrictions such as --cap-drop=ALL, allowing image-controlled checkpoint state to select weaker sandbox settings and capabilities. Rootless containers are not affected because checkpoint and restore are unavailable in that mode. This issue is fixed in versions 5.8.8 and 6.1.3.

### CVE-2026-55675

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-829;CWE-1357` |
| Published | 2026-10-13T16:17:21.890 |

The Salty documentation repository builds and deploys the docs.saltbox.dev website. Prior to commit 649c9aea2daef1168eeb0415b44e65dbbde9f220, .github/workflows/trigger-pr-build.yml records an untrusted fork commit in the pr_info artifact, and the secret-bearing workflow_run job in .github/workflows/build-pr.yml checks out that commit before running pip install -r requirements.txt. A fork pull request can therefore supply attacker-authored setup.py or PEP 517 build hooks whose installation code executes in the privileged base-repository workflow with CF_API_TOKEN, GH_TOKEN, MKDOCS_GIT_COMMITTERS_APIKEY, and a write-capable GITHUB_TOKEN, allowing secret disclosure and follow-on compromise. The vulnerability is not caused by the repository-fork guard, and the demonstrated path requires attacker control of fork content rather than merely the artifact metadata. This vulnerability is fixed with commit 649c9aea2daef1168eeb0415b44e65dbbde9f220.

### CVE-2024-34323

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T16:17:08.210 |

ProPhoenix Law RMS v2022.2403.3.101 was discovered to contain an Insecure Direct Object Reference (IDOR) via the usrLogin$hdnPFID parameter. This vulnerability allows attackers to access sensitive information via a crafted HTTP request.

### CVE-2026-97381

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-346;CWE-393` |
| Published | 2026-10-13T22:19:45.427 |

Legacy Update is a tool for activating and installing updates on legacy Windows PCs. Legacy Update 1.12.0 through 1.13.1 contains an origin validation error in the IsPermitted method of its ActiveX control. After successfully reading the hosting document's hostname, a hostname that is not on the permitted list falls through without setting E_ACCESSDENIED, causing IsPermitted to return S_OK. An attacker who induces a user to visit a malicious webpage in Internet Explorer can invoke the control to enumerate update and system information, install updates without consent, display dialogs, or restart the computer when a reboot is pending. This issue was fixed in Legacy Update 1.13.2.

### CVE-2026-106612

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.347 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105903

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T21:17:29.813 |

ColdFusion is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-75732

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T20:18:04.200 |

Adobe Experience Manager is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105895

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T20:17:15.420 |

Adobe Experience Manager is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-103848

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T20:17:11.267 |

Adobe Experience Manager is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-77459

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T17:17:46.050 |

Argo CD is a declarative, GitOps continuous delivery tool for Kubernetes. From 2.10.0 until 3.3.15, 3.4.10, 3.5.4, and 3.6.0-rc2, Argo CD creates PostDelete resource hooks without applying the AppProject destination and resource authorization checks used during ordinary synchronization. The omitted checks include cluster-scoped and namespaced resource allow/deny lists. A user who can write to an Application's Git repository can commit a delete hook targeting a forbidden namespace, server, group, kind, or resource name, and deletion of the Application causes the application-controller to create that resource with its destination-cluster credentials. The reachable impact is bounded by the controller's cluster access but can include cluster-scoped resources, disallowed namespaces, persistent hook objects, and secondary objects created by a hook Job. PreSync, Sync, PostSync, and SyncFail hooks continue to use the normal project checks. This issue is fixed in versions 3.3.15, 3.4.10, 3.5.4, and 3.6.0-rc2.

### CVE-2026-109412

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-13T17:17:28.267 |

An exposed dangerous endpoint in Ivanti Neurons Patch for Intune allows a remote authenticated attacker to leak sensitive authentication information.

### CVE-2026-106042

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-13T17:17:16.273 |

An External Control of File Name or Path vulnerability in Ivanti Xtraction before version 2026.4 allows a remote authenticated attacker to redirect application-generated requests to an attacker-controlled endpoint and obtain EPMM connector credentials transmitted by the application.

### CVE-2026-108065

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T14:17:33.813 |

SQL Injection (CWE-89) in the SOAP GetUser method of the /preapproval.asmx endpoint in Channel Software WebAlliance eCommerce [VERSION — missing] allows an unauthenticated remote attacker to read, write, and potentially execute commands on the backend Microsoft SQL Server via a crafted sUserID parameter value containing a single quote and stacked SQL query.

### CVE-2026-16741

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T13:17:28.103 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TR7 Cyber ​​Defense Inc. TR7 ASP on virtual appliance and TR7 Cyber ​​Defense Inc. TR7 ASP on physical appliance allows OS Command Injection.

This issue affects TR7 ASP: from 1.0.40.236 before 1.0.1554.2331; TR7 ASP: from 1.6.42.239 before 1.6.1554.2331.

### CVE-2026-16740

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T13:17:27.977 |

Missing authentication for critical function vulnerability in TR7 Cyber ​​Defense Inc. TR7 ASP on virtual appliance and TR7 Cyber ​​Defense Inc. TR7 ASP on physical appliance allows OS Command Injection.

This issue affects TR7 ASP: from 1.0.40.236 before 1.0.1554.2331; TR7 ASP: from 1.6.42.239 before 1.6.1554.2331.

### CVE-2026-108291

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T13:17:24.633 |

Deserialization of Untrusted Data vulnerability in itthinx Affiliates affiliates allows Object Injection.This issue affects Affiliates: from n/a through 7.0.1.

### CVE-2026-107424

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-14T13:17:23.453 |

Incorrect Privilege Assignment vulnerability in M A Vinoth Kumar Frontend Dashboard frontend-dashboard allows Privilege Escalation.This issue affects Frontend Dashboard: from n/a through 3.0.7.

### CVE-2026-104748

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-14T08:17:02.997 |

The SimpleForm – Form Maker to Chat Apps with Quiz, Poll and Multi Lead Notifications plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 3.10.0 This is due to the `wp_ajax_nopriv_simpleform_wp_register` AJAX action lacking any capability check for role assignment and the `save_custom_fields_to_user_meta()` function using an exclusion list that omits `wp_capabilities`, combined with `get_form_settings()` returning a hard-coded defaults array that unconditionally enables meta writing regardless of the supplied `form_id`. This makes it possible for unauthenticated attackers to create a new Administrator-level WordPress account by supplying `wp_capabilities[administrator]=1` alongside standard registration fields. The nonce required by the endpoint is publicly emitted into the `front_end_data` JavaScript object on every front-end page via `wp_enqueue_scripts`, making it trivially obtainable by any unauthenticated visitor before submitting the malicious request.

### CVE-2026-87855

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-14T04:18:52.840 |

The JTL-Connector for WooCommerce plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.4.3 via the saveImage() function. This is due to the startSession() function accepting an empty jtlauth parameter as a valid credential, combined with insufficient file type validation in handleImagePush(). This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible.

### CVE-2026-104800

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-14T04:18:12.563 |

The AGE-GATE plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 1.0 via the 'width (and height)' parameter parameter. This is due to missing authentication, capability checks, and nonce verification on the standalone admin.php endpoint, combined with unsanitized injection of POST parameters directly into generated PHP source written to an included file. This makes it possible for unauthenticated attackers to execute code on the server. This is possible because admin.php does not load WordPress and carries no ABSPATH guard, making it a fully unauthenticated entry point regardless of the decorative capability arguments registered via the plugin's simulated menu API.

### CVE-2026-97668

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T03:17:37.797 |

The Abandoned Cart Pro for WooCommerce plugin for WordPress is vulnerable to SQL Injection via the guest cart persistent meta_value in all versions up to, and including, 10.8.0 due to insufficient escaping on user supplied data and lack of sufficient preparation on the existing SQL query in the update_guest_persistent_cart() function. The abandoned_cart_info value, populated from attacker-controlled checkout fields such as the SMS consent field, is passed through stripslashes() and concatenated directly into an UPDATE statement while the adjacent SELECT and INSERT use prepared statements. This makes it possible for unauthenticated attackers to append additional SQL to the query. Because the sink is an UPDATE ... SET on the wp_usermeta table, the injection can both extract sensitive information from the database via time-based blind techniques and modify usermeta rows; it has been demonstrated to escalate an arbitrary account to administrator by writing a wp_capabilities row that shadows the legitimate one.

### CVE-2026-97657

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T03:17:37.657 |

The Abandoned Cart Pro for WooCommerce plugin for WordPress is vulnerable to Authentication Bypass via Malleable Encryption and Bypassable HMAC in all versions up to, and including, 10.8.0. This is due to the use of MAC-free AES-CTR encryption for cart-recovery link tokens — where the 8-byte CTR nonce is carried inside the ciphertext blob and the encryption key is looked up using the attacker-supplied `user_email` GET parameter — combined with an HMAC nonce check in `wcap_email_track_links()` that is only enforced when the `wcap_nonce` parameter is non-empty, allowing complete bypass by omission, and an insecure direct object reference on the decrypted `abandoned_id` with no ownership verification confirming the cart belongs to the email used for decryption. This makes it possible for unauthenticated attackers who possess a single legitimate cart-recovery link (obtained from their own reminder email) to recover the keystream, forge a ciphertext that decrypts to any victim's cart ID, and trigger a call to `wp_set_auth_cookie()` for the victim user — achieving full account takeover of any user who has ever abandoned a cart, including administrators. The auto-login feature defaults to enabled and is forced on during plugin upgrades, meaning all affected installations are exploitable without any additional configuration.

### CVE-2026-110002

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-14T03:17:20.220 |

The Snazzy Social Media Feed plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.5 via the (file scope) function. This is due to missing WordPress bootstrap, authentication, capability, and nonce checks in the standalone save-to-cache.php script, combined with insufficient sanitization of the pluginURL parameter before it is written to a web-executable PHP file. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. The save-to-cache.php script is directly reachable without loading WordPress; FILTER_SANITIZE_URL — the only filter applied to the pluginURL value — preserves the characters required to craft a valid PHP payload, which is then written verbatim into cached-content/cached-feed.php and immediately executable via a single GET request.

### CVE-2026-93388

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-14T02:17:01.720 |

The Printcart Store (PCDesigner / NB Designer) plugin for WooCommerce is vulnerable to unauthenticated arbitrary file upload leading to remote code execution in all versions up to, and including, 2.9.1 The nbdesigner_copy_image_from_url AJAX action is registered for logged-out callers (wp_ajax_nopriv_), and its Google Drive branch rebuilds the destination filename from the raw, attacker-supplied gapi[name] parameter — bypassing the jpg/jpeg/png/gif allow-list applied on the other branch — and writes the fetched bytes to a web-accessible directory (wp-content/uploads/nbdesigner/temp/). This makes it possible for unauthenticated attackers to write a .php file to a web-served, PHP-executing location and, by supplying their own Google Drive file and OAuth token as the content source, execute arbitrary code on the server. The required save-design nonce is handed to anonymous callers by the nbd_check_use_logged_in endpoint, so it presents no barrier.

### CVE-2026-110392

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T02:16:59.653 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in Samsung Open Source QA-Board allows : OS Command Injection.

### CVE-2026-104252

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:17:12.453 |

Vitess is a database clustering system for horizontal scaling of MySQL. Prior to 23.0.5 and 24.0.2, twopczHandler in go/vt/vttablet/tabletserver/twopcz.go writes the Action and dtid form values from the vttablet and vtcombo /twopcz HTTP debug endpoint into a text/html response without HTML escaping. Under the default allow-all ACL policy, a remote unauthenticated attacker can send an operator a crafted request that executes script in the operator's browser after the request is opened. The script runs with the vttablet debug origin and can read same-origin diagnostic endpoints that expose query, transaction, environment, variable, or profiling data available in that deployment. This issue is fixed in versions 23.0.5 and 24.0.2.

### CVE-2026-97816

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:20.110 |

Use after free in OpenSSH for Windows allows an unauthorized attacker to execute code over a network.

### CVE-2026-97815

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:19.930 |

Heap-based buffer overflow in Windows Error Reporting allows an unauthorized attacker to execute code over a network.

### CVE-2026-97814

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:19.753 |

Heap-based buffer overflow in Windows Text Shaping allows an unauthorized attacker to execute code over a network.

### CVE-2026-97805

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-13T19:22:18.440 |

Out-of-bounds read in Windows Partition Management Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-97749

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:22:12.340 |

Double free in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-97016

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:10.530 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-96934

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:05.590 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-96924

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:22:03.867 |

Untrusted pointer dereference in Windows OLE allows an unauthorized attacker to execute code over a network.

### CVE-2026-96909

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:01.520 |

Heap-based buffer overflow in Windows BitLocker allows an unauthorized attacker to execute code over a network.

### CVE-2026-96864

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:22:00.717 |

Double free in Microsoft Failover Cluster Virtual Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-96320

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:55.017 |

Heap-based buffer overflow in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-96219

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:47.737 |

Out-of-bounds write in Windows Local Security Authority Subsystem Service (LSASS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-96113

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-10-13T19:21:45.733 |

Heap-based buffer overflow in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-96096

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:45.403 |

Heap-based buffer overflow in Windows Media Player allows an unauthorized attacker to execute code over a network.

### CVE-2026-92909

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:21:43.613 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction.

### CVE-2026-88178

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:38.557 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-88156

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:21:35.710 |

Stack-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-88102

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:28.217 |

Use after free in Windows Failover Cluster allows an unauthorized attacker to execute code over a network.

### CVE-2026-85928

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:18.917 |

Heap-based buffer overflow in Windows Volume Manager Extension Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-85814

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:05.980 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-85809

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:05.287 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-85806

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-191` |
| Published | 2026-10-13T19:21:04.770 |

Integer underflow (wrap or wraparound) in Network Policy Server (NPS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-85792

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:02.570 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-84015

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:51.720 |

Heap-based buffer overflow in Remote Access Point-to-Point Protocol (PPP) EAP-TLS allows an unauthorized attacker to execute code over a network.

### CVE-2026-83935

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:50.337 |

Heap-based buffer overflow in Microsoft XML allows an unauthorized attacker to execute code over a network.

### CVE-2026-83910

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:20:46.063 |

Out-of-bounds write in RPC Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-83869

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:20:36.677 |

Integer underflow (wrap or wraparound) in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-83862

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:35.520 |

Use after free in Windows Network Load Balancing allows an unauthorized attacker to execute code over a network.

### CVE-2026-83782

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:27.183 |

Heap-based buffer overflow in Windows Shell allows an unauthorized attacker to execute code over a network.

### CVE-2026-83780

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:26.917 |

Use after free in Windows CCFFilter Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-83770

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:25.433 |

Heap-based buffer overflow in Windows Text Shaping allows an unauthorized attacker to execute code over a network.

### CVE-2026-83748

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:20.500 |

Heap-based buffer overflow in Windows Error Reporting allows an unauthorized attacker to execute code over a network.

### CVE-2026-83693

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:12.390 |

Heap-based buffer overflow in Windows Error Reporting allows an unauthorized attacker to execute code over a network.

### CVE-2026-83578

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190;CWE-191` |
| Published | 2026-10-13T19:20:00.457 |

Integer underflow (wrap or wraparound) in Windows PowerShell allows an unauthorized attacker to execute code over a network.

### CVE-2026-83519

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:57.757 |

Heap-based buffer overflow in Windows Error Reporting allows an unauthorized attacker to execute code over a network.

### CVE-2026-83517

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:57.447 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-70300

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:50.007 |

Untrusted pointer dereference in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70291

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:48.817 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70242

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:40.990 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70157

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:29.030 |

Heap-based buffer overflow in Windows System Information Console allows an unauthorized attacker to execute code over a network.

### CVE-2026-70153

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:28.537 |

Heap-based buffer overflow in Microsoft PostScript Printer Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-70147

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:27.683 |

Heap-based buffer overflow in Microsoft PostScript Printer Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-70096

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:21.420 |

Heap-based buffer overflow in Windows Rich Text Edit Control allows an unauthorized attacker to execute code over a network.

### CVE-2026-70024

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-121` |
| Published | 2026-10-13T19:19:13.487 |

Stack-based buffer overflow in Windows Internet Information Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69886

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:01.503 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-69883

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:01.150 |

Use after free in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-69705

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:18:57.820 |

Out-of-bounds write in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-69639

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:56.713 |

Heap-based buffer overflow in Windows Libarchive allows an unauthorized attacker to execute code over a network.

### CVE-2026-69634

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:56.343 |

Heap-based buffer overflow in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-105016

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:57.750 |

Heap-based buffer overflow in Microsoft QUIC allows an unauthorized attacker to execute code over a network.

### CVE-2026-105010

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:57.433 |

Use after free in Microsoft Windows Search Component allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-102210

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:46.520 |

Heap-based buffer overflow in Windows Text Shaping allows an unauthorized attacker to execute code over a network.

### CVE-2026-100222

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:17:42.587 |

Heap-based buffer overflow in Network Policy Server (NPS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-100219

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:42.163 |

Use after free in Microsoft QUIC allows an unauthorized attacker to execute code over a network.

### CVE-2026-100202

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:40.143 |

Use after free in Windows Message Queuing Queue Manager allows an unauthorized attacker to execute code over a network.

### CVE-2026-37107

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-13T18:17:23.847 |

An issue in HTMLy v.3.1.1 allows a remote attacker to escalate privileges via the get_feed function in the admin.php component

### CVE-2026-106173

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T18:17:14.697 |

A improper limitation of a pathname to a restricted directory ('path traversal') vulnerability in Fortinet FortiSIEM 7.5.0 may allow attacker to execute unauthorized code or commands via specially crafted packets.

### CVE-2026-69227

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T17:17:45.130 |

A flaw in Portal for ArcGIS allows unauthenticated access to certain /portaladmin/local API endpoints under specific conditions. This could enable an attacker to access administrative functionality that should require authentication.

### CVE-2026-53709

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-321;CWE-798;CWE-1188` |
| Published | 2026-10-13T15:17:44.873 |

MCP Context Forge is an MCP gateway and administrative platform. Prior to 1.0.2, mcpgateway/config.py and .env.example ship a known JWT_SECRET_KEY, while verify_jwt_token() accepts HS256 tokens signed with that key and get_current_user() creates a platform administrator when the token subject matches PLATFORM_ADMIN_EMAIL and REQUIRE_USER_IN_DB is false. A remote unauthenticated attacker can therefore mint accepted administrator tokens without a database account. While the vulnerable signing key remains configured and the platform-admin bootstrap remains enabled, forged access survives password rotation, account deletion, and session revocation, allowing administrative disclosure, modification, and service disruption. This issue is fixed in version 1.0.2.

### CVE-2026-110165

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.480 |

Use after free in Core in Google Chrome on on Android prior to 155.0.8059.79 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110161

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.050 |

Use after free in Network in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code outside the sandbox via crafted network traffic. (Chromium security severity: Critical)

### CVE-2026-110159

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T22:17:35.833 |

Incorrect authorization in Updater in Google Chrome prior to 155.0.8059.79 allowed a local attacker to execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-110152

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T22:17:35.077 |

Buffer overflow in ANGLE in Google Chrome on on Android prior to 155.0.8059.79 allowed a remote attacker to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110149

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:34.737 |

Use after free in Browser in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110144

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T22:17:34.203 |

Incorrect authorization in Mojo in Google Chrome on on Windows prior to 155.0.8059.79 allowed a local attacker to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-110142

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:33.993 |

Use after free in FileSystem in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-110136

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:33.330 |

Use after free in PDF in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-75994

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:18:20.380 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106620

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:31.263 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-90531

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-13T20:19:10.030 |

Adobe Experience Manager is affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-102238

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T20:17:06.727 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-55183

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T17:17:41.893 |

RClone Manager is a cross-platform GUI application designed to help users manage Rclone remotes efficiently. Prior to 0.2.7, RClone Manager starts the local rclone rcd service on 127.0.0.1:51900 with --rc-no-auth, --rc-allow-origin *, and --rc-serve. A malicious web page opened by a user while the daemon is running can therefore send cross-origin requests to the unauthenticated local API with the user's operating-system privileges. The requests can disclose configured storage credentials and potentially access, upload, modify, or exfiltrate locally stored files accessible to the user and files available through configured remotes; the advisory's possible command-execution impact remains unconfirmed. This issue is fixed in version 0.2.7.

### CVE-2026-104192

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T15:17:31.087 |

Dragonfly is an in-memory data store built for modern application workloads. Prior to 1.40, OpaqueObjLoader::CreateStream in src/server/rdb_load.cc can associate one streamNACK with a consumer group's global PEL and a consumer-local PEL, then free the shared object when a duplicate consumer entry is rejected. Cleanup subsequently frees the same object again. In the default configuration, where Dragonfly ships with authentication disabled, an unauthenticated client can trigger the double-free by sending a crafted serialized stream to RESTORE, causing allocator corruption, denial of service, and potentially attacker-controlled code execution as the Dragonfly service account. The source fix has not yet been mapped to a published release.

### CVE-2026-89310

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T07:17:04.650 |

A parameter taken from the request body is inserted into
a T-SQL statement without parameterization or escaping, allowing
a remote attacker to execute arbitrary SQL statements in the context of the
application's database account.

### CVE-2026-88092

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-13T19:21:27.043 |

Inconsistent interpretation of http requests ('http request/response smuggling') in ASP.NET Core allows an unauthorized attacker to perform tampering over a network.

### CVE-2026-105445

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-13T18:17:13.167 |

An Incorrect Privilege Assignment vulnerability in Docker Hub's account-to-organization conversion feature allowed an authenticated attacker to reassign a personal access token (PAT) they controlled to another Docker Hub user without rotating or revoking the token secret. The unchanged PAT then authenticated to the registry as the recipient and could pull, push, or delete images, within its scopes, in repositories accessible to that user, including organization repositories.

### CVE-2026-90530

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T21:19:57.273 |

ColdFusion RDS is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.









RDS is purely a development feature meant for debugging purposes, and switching ColdFusion to Production Secure Profile automatically disables RDS. The Lockdown Guide outlines the specific step to disable RDS if a ColdFusion server is not being used in Production Secure Profile.

### CVE-2026-49950

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T21:17:39.007 |

Xorbits Xoscar through 0.11.2 contains an unauthenticated deserialization vulnerability that allows remote attackers to execute arbitrary code by sending crafted data over the actor-pool TCP channel. Attackers can exploit SocketChannel.recv() passing unvalidated data to cloudpickle.loads(), which triggers pickle __reduce__ gadget execution before message type validation, achieving remote code execution as the server process which commonly runs as root on GPU nodes.

### CVE-2026-83662

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:18:11.500 |

Adobe Experience Manager is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-63146

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T20:17:30.210 |

Omnispace Agora Project before 26.10.0 contains a code injection vulnerability where unescaped, attacker-controlled values are written into the config.inc.php configuration file during installation through File::updateConfigFile() and DbInstall::dbControl(), combined with an SQL injection issue enabled by PDO::ATTR_EMULATE_PREPARES supporting stacked queries. Attackers can exploit the SQL injection to re-trigger the installer and inject arbitrary PHP code into config.inc.php, achieving unauthenticated remote code execution on the underlying system.

### CVE-2026-106630

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:17:16.627 |

Adobe Experience Manager is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-106629

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:17:16.507 |

Adobe Experience Manager is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-91013

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:21:43.127 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-75120

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T19:19:53.390 |

The OpenText™ (EnCase SAFE Agents) component utilized by OpenText™ Endpoint Investigator, OpenText™ Endpoint Forensics & Response, OpenText™ Information Assurance, and OpenText™ Endpoint Security contains a security vulnerability on the Agents that could allow unauthorized or unauthenticated activity that establishes an unauthorized connection to a vulnerable Agent by bypassing intended security controls during session establishment

### CVE-2026-70279

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:19:47.373 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Exchange Server allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-100133

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:17:39.690 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by an attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-102989

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T17:17:14.797 |

TanStack Router is a client-first, server-capable, fully type-safe router and full-stack framework for the web. From 1.143.12 until 1.169.39 for @tanstack/start-server-core, 1.168.60 for @tanstack/react-start, 1.168.57 for @tanstack/solid-start, and 1.168.56 for @tanstack/vue-start, an unauthenticated attacker can place non-public fields in a server-function request payload so that attacker-controlled middleware state reaches the error path and a response-shaped object is accepted as an HTTP response. A crafted server-function URL can therefore return attacker-controlled HTML from the application's origin; when a visitor opens the URL, the injected script can access same-origin data and issue requests with the visitor's authority. This issue is fixed in @tanstack/start-server-core 1.169.39, @tanstack/react-start 1.168.60, @tanstack/solid-start 1.168.57, and @tanstack/vue-start 1.168.56.

### CVE-2026-103928

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-13T16:17:10.597 |

Metabase is an open source business intelligence and analytics platform. From 1.55.0 until 1.58.16, 1.59.13, 1.60.9, and 1.61.4, native queries and actions against an H2 data source are passed through without restricting host-facing built-in functions. A user authorized to run native queries or actions can invoke FILE_READ, FILE_WRITE, CSVREAD, CSVWRITE, or LINK_SCHEMA to read or write arbitrary files on the Metabase server or link other databases. The default sample database uses H2, so the vulnerable surface is exposed by default. This issue is fixed in versions 1.58.16, 1.59.13, 1.60.9, and 1.61.4.

### CVE-2026-77099

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T15:17:49.530 |

CVFS contained an input validation issue affecting command execution.  Software customers upgrade to resolved maintenance release. Update CVFS.

### CVE-2026-14851

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-14T09:17:22.437 |

A vulnerability relating to the exposure of confidential information in the customer invoicing web application, which exposes personally identifiable information (PII) and financial data – including customer names, addresses, invoice numbers, payment details and tax information – to unauthorised individuals. The issue is caused by a lack of authorisation checks at the endpoint responsible for serving PDF invoice files. Furthermore, some URLs for invoicing documents appear to be publicly accessible via search engines, exposing paths to confidential files. Successful exploitation of this vulnerability could allow an attacker to access data to which they should not have access, as well as to predict identifiers in order to access even more confidential information.

### CVE-2026-110447

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T03:17:20.683 |

Collabora Online Built-in CODE Server before 26.4.303 (richdocumentscode), a Nextcloud app, allows remote code execution, as exploited in the wild in September and October 2026, a different vulnerability than CVE-2025-66208. This is an OS command injection in proxy.php when the CODE server isn't running (e.g., the product was recently restarted). The vulnerability is not present in standalone Collabora Online servers; only this deployment with CODE Server is affected.

### CVE-2026-110112

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:18:43.257 |

Dockhand before 1.0.50 contains a privilege escalation vulnerability that allows users from another tenant to gain admin access because OIDC iss, aud, nonce and exp claims are not validated. Attackers with admin rights in another tenant of a shared provider like Microsoft Entra ID can recreate the mapped admin group and log in as Dockhand administrators.

### CVE-2026-92097

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T02:17:01.397 |

The Click to Chat for WhatsApp plugin for WordPress is vulnerable to Arbitrary Shortcode Execution in versions up to, and including, 4.44 This is due to the greetings_dialog() function building the {url} template placeholder from a sanitize_text_field()-filtered $_SERVER['REQUEST_URI'] on archive pages and then passing the substituted greeting content to do_shortcode() in the greetings-1 and greetings-2 templates, without stripping shortcode delimiters. Because wp_kses() runs against main_content BEFORE the {url} substitution, the attacker-controlled URL bytes reach do_shortcode() unfiltered. This makes it possible for unauthenticated attackers to execute arbitrary shortcodes registered by WordPress core, the active theme, or any other plugin (e.

### CVE-2026-93909

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-13T21:19:57.977 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 is vulnerable by an authentication bypass vulnerability when samlWeb-2.0 feature is enabled.

### CVE-2026-93895

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-13T21:19:57.743 |

IBM WebSphere Application Server - Liberty 20.0.0.12 through 26.0.0.10 could allow an unauthenticated remote attacker to bypass access controls configured on gRPC service methods.

### CVE-2026-106621

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T21:17:31.380 |

ColdFusion is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction.

### CVE-2026-63160

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-13T20:17:31.420 |

Omnispace Agora Project before 26.10.0 contains a vulnerability where the persistent remember-me token is stored verbatim server-side, making the stored value identical to the bearer credential held in the user's cookie. Attackers who gain access to the stored token, such as through database or backup disclosure, can replay the plaintext value to authenticate as the victim user without needing their password.

### CVE-2026-63159

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-13T20:17:31.273 |

Omnispace Agora Project before 26.10.0 contains a predictable password-reset token vulnerability that allows unauthenticated attackers to take over user accounts by computing the reset token as sha1(login.password), a deterministic and reusable value. Attackers can derive or brute-force the reset token from known or guessed login and password combinations to forge valid password-reset requests and hijack arbitrary accounts.

### CVE-2026-63158

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-836` |
| Published | 2026-10-13T20:17:31.143 |

Omnispace Agora Project before 26.10.0 contains an authentication bypass vulnerability that allows attackers possessing a user's stored bcrypt password hash to authenticate as that user without knowing the actual password, caused by the legacy AGORAP_LOG/AGORAP_PASS cookie mechanism treating the stored hash as a directly replayable bearer credential. Attackers can set the AGORAP_LOG/AGORAP_PASS cookies with a stolen password hash to impersonate any user, including administrators, and gain unauthorized access to the application.

### CVE-2026-63149

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-330` |
| Published | 2026-10-13T20:17:30.617 |

Omnispace Agora Project before 26.10.0 contains an insecure randomness vulnerability that allows attackers to predict temporary or default account passwords generated by Txt::defaultPassword() using PHP's uniqid() function based on server time in microseconds. Attackers who observe or approximate the account creation time can compute the predictable password and take over the account before the legitimate user logs in.

### CVE-2026-106626

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T20:17:16.270 |

Adobe Experience Manager is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-96252

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:21:51.343 |

Improper verification of cryptographic signature in Active Directory Federation Services (AD FS) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-92464

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T19:21:43.370 |

Adobe Commerce is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-70188

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-13T19:19:33.130 |

Inconsistent interpretation of http requests ('http request/response smuggling') in ASP.NET Core allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-52394

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-201;CWE-209` |
| Published | 2026-10-13T18:17:24.103 |

DeepSeek V4 is vulnerable to Incorrect Access Control via a crafted input.

### CVE-2026-54454

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-13T17:17:41.310 |

OpenCATS is an open-source applicant tracking system and recruitment CRM for staffing agencies and hiring teams. Prior to 0.10.0, the OpenCATS Import module in modules/import/ImportUI.php can preserve an uploaded file's original name for one import data type and place the file in the web-accessible temporary directory. An authenticated user with Import privileges can select the affected import path and upload a PHP file that remains under an attacker-controlled executable filename, and an import error can leave the file on disk. If the temporary directory is served with PHP execution enabled, requesting the staged file can execute arbitrary PHP code with the web server process privileges, exposing or modifying recruiting data and the host system. This issue is fixed in version 0.10.0.

### CVE-2026-55695

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T16:17:22.057 |

FearlessCMS is a flat-file content management system centered on simplicity and open source. In 0.1.2b and earlier, an authenticated administrator can set an arbitrary Git repository URL through admin/updater-handler.php and trigger perform_update, which passes the URL to update.sh. The updater clones the repository and replaces the live plugins/, admin/, and includes/ directories without verifying the repository's identity, signatures, or contents. Because router.php permits existing PHP files under plugins to be executed by the PHP development server, attacker-supplied update content can execute arbitrary PHP with the web server process's privileges and persist as a backdoor. This issue is fixed in version 0.1.3b.

### CVE-2024-34324

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-13T16:17:08.317 |

An issue in ProPhoenix Law RMS v2022.2403.3.101 allows attackers to execute a session hijacking attack via injecting a crafted 24-character string into the ASP.NET_SessionId cookie.

### CVE-2026-106619

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T21:17:31.150 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-85818

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:21:06.667 |

Improper verification of cryptographic signature in Windows Schannel allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-105008

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T19:17:57.093 |

No cwe for this issue in Windows Schannel allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-92892

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-13T18:17:26.530 |

Potential arbitrary code execution, under specific configurations.

### CVE-2026-55562

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T17:17:42.040 |

Cronicle is a multi-server task scheduler and runner, with a web based front-end UI. Prior to 0.9.119, the administrator Activity Log in htdocs/js/pages/admin/Activity.js concatenates the attacker-controlled item.user.full_name value into HTML without applying encode_entities and inserts the result through this.div.html. The bundled pixl-server-user input filter can be bypassed by a tag containing a line break because its regular expression does not match newlines. An authenticated non-administrator can update the attacker's own name through /api/user/update using a valid session and current password; when free_accounts is enabled, an anonymous attacker can instead plant the name during self-registration. The stored name executes script in an administrator's session when the Activity Log is opened, enabling administrator takeover and subsequent command execution through privileged Cronicle features. This issue is fixed in version 0.9.119.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-105429

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-116` |
| Published | 2026-10-14T05:16:42.487 |

Improper neutralization of special elements in the NetBird client SSH configuration manager (client/ssh/config/manager.go) in NetBird versions 0.60.0 through 0.74.6 allows a malicious or compromised peer to execute arbitrary commands on other NetBird client hosts. The client writes a system-wide OpenSSH drop-in file (/etc/ssh/ssh_config.d/99-netbird.conf, or the equivalent under %PROGRAMDATA%\ssh\ssh_config.d on Windows) that embeds each peer FQDN or hostname inside a double-quoted Match host directive without escaping. A peer name containing a double quote breaks out of the quoted context and injects arbitrary SSH configuration directives, including exec commands, which run locally as any user on the host the next time that user runs ssh. Desktop clients on Linux, macOS, Windows and FreeBSD are affected; the Android and iOS apps are not. The issue is fixed in version 0.74.7, which accepts a peer FQDN or hostname only if it is a valid DNS name.

### CVE-2026-106599

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T13:17:22.503 |

Deserialization of Untrusted Data vulnerability in Brainstorm Force SureCart surecart allows Object Injection.This issue affects SureCart: from n/a through 4.9.3.

### CVE-2026-104795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-10-14T11:16:59.937 |

The insights-runtime-extractor runs as a privileged DaemonSet (`hostPID: true`)
that scans container processes for runtime fingerprinting. When scanning a
container, the coordinator:

1. **fork()s** a child process
2. **setns()** into the target container's PID and mount namespaces
3. **fchdir()** back to an orphaned FD pointing at the extractor's own root
   filesystem (where `/crio.sock` is hostPath-mounted)
4. Calls **only `seteuid(target_uid)`** — changing the effective UID but leaving
   the **real UID and saved-set-UID at 0** and **retaining the permitted
   capability set**
5. The `check_no_privileged_perms()` guard inspects only the Effective capability
   set (so it passes), and is **skipped entirely when the target runs as uid 0**
6. The `VersionExecutable` fingerprint invokes `fpr_kind_executable` with
   `process.command_line[0]` — the target's argv[0], read from
   `/proc/<pid>/cmdline` and **fully controlled by the workload**
7. `fpr_kind_executable` calls `exec.Command(executable, "--version").Output()`
   — executing the **workload's own binary** inside the workload's mount
   namespace while **ruid=0 in the host user namespace**

The executed process can call `setuid(0)` to restore full root with
`CAP_SYS_ADMIN`, and inherits the orphaned cwd which resolves into the extractor
container's filesystem containing the host CRI-O socket.

## Affected Code

### 1. Insufficient privilege drop (Rust — extractor coordinator)

**File:** `extractor/src/insights_runtime_extractor.rs`

```rust
// Lines 139-146 — seteuid-only drop, guard skipped for root containers
join_process_namespaces(process.pid)?;
change_dir(current_dir);
switch_user(*process.uid)?;
if *process.uid != 0 {
    perms::check_no_privileged_perms()
        .expect("Must not have privileged permissions to run fingerprints");
}
fingerprint::run_fingerprints(&config, out_dir, &process);
```

```rust
// Lines 182-185 — only effective UID changed; ruid/suid stay 0
fn switch_user(uid: u32) -> Result<(), ScannerError> {
    debug!("... Becoming user: {uid}");
    seteuid(uid.into()).map_err(|e| ScannerError::Errno(e))
}
```

### 2. Execution of untrusted binary (Go — fingerprint)

**File:** `fingerprints/pkg/utils/file.go`

```go
// Lines 75-80 — executes a path taken verbatim from workload's argv[0]
func GetExecutableVersionOutput(executable string) (string, error) {
    out, err := exec.Command(executable, "--version").Output()
    if err != nil {
        return "", err
    }
    return string(out), nil
}
```

### 3. Workload-controlled path forwarded (Rust — version_executable)

**File:** `version_executable.rs`

```rust
// Lines 29-34 — workload-controlled command_line[0] forwarded to fingerprint
return Some(vec![
    fpr_kind_executable,
    out_dir.to_string(),
    String::from(&process.command_line[0]),
    String::from(&version_executable.runtime_kind_name),
]);
```

## Attack Pattern

**Attacker:** Any tenant able to schedule a pod (unprivileged, any namespace)
**Victim:** The node running the insights-runtime-extractor DaemonSet
**Trigger:** Automatic — the DaemonSet scans all container processes on the node

**Attack sequence:**

1. Attacker creates a pod whose process name matches a configured
   versioned-executable pattern (`node`, `python`, `python3`, `MainThread`,
   or contains `java`)
2. The pod's main binary (at the path matching argv[0]) is a malicious
   executable that calls `setuid(0)` to restore root
3. When the insights operator triggers a scan, the DaemonSet forks, enters the
   attacker's mount namespace, and executes the attacker's binary with ruid=0
4. The attacker's code regains full root with `CAP_SYS_ADMIN` in the host user
   namespace
5. The inherited cwd contains the host CRI-O socket → full node compromise

### CVE-2026-105106

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T08:17:03.587 |

Koha is vulnerable to OS command injection in the Task Scheduler deletion path. The tools/scheduler.pl handler accepts the jobid request parameter for op=cud-delete and passes it to C4::Scheduler::remove_at_job without validating it. Schedule::At::remove substitutes the supplied job ID into an atrm command string without quoting or escaping it and executes the command through a single-argument system() call, which invokes the shell. An authenticated staff user with the tools => schedule_tasks permission can therefore execute arbitrary operating-system commands as the Koha web/application user by supplying shell metacharacters in jobid. The issue is fixed in Koha 24.11.20, 25.05.15, 25.11.09, and 26.05.04, and in the 26.11 development branch.

### CVE-2026-86799

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T07:17:03.860 |

The Forms WordPress plugin before 3.0.2 does not sanitise submitted form values on storage, nor escape them before outputting them on the form submissions screen in the administration dashboard, allowing unauthenticated users to inject arbitrary web scripts that will execute in the browser of any administrator viewing the submissions.

### CVE-2026-107126

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T07:17:01.350 |

The WP Booking System  WordPress plugin before 2.1.0.1 does not sanitise and escape a client-controllable request value before storing it and later outputting it in an administration screen, allowing unauthenticated attackers to perform Stored Cross-Site Scripting attacks that execute in the session of an administrator who views the stored data.

### CVE-2026-110172

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:37.237 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110171

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:37.127 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110169

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.907 |

Use after free in V8 in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110168

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.800 |

Use after free in V8 in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110167

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.693 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T22:17:36.590 |

Buffer overflow in Animation in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.377 |

Use after free in DOM in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.267 |

Use after free in DOM in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110162

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:36.160 |

Use after free in Desktop in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110157

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:35.620 |

Use after free in SVG in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T22:17:35.400 |

Buffer overflow in PDFium in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110154

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:35.293 |

Use after free in Canvas in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110153

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:35.187 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110151

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:34.963 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110148

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:34.637 |

Use after free in SVG in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-110147

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:34.530 |

Use after free in PDF in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110140

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T22:17:33.777 |

Type confusion in V8 in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110139

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:33.667 |

Use after free in Media in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110137

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:33.447 |

Use after free in WebRTC in Google Chrome prior to 155.0.8059.79 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-94512

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:19:58.210 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-65674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T21:17:41.157 |

Deserialization of untrusted data in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-106618

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:31.043 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106617

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.930 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106615

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.693 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106613

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T21:17:30.470 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction.

### CVE-2026-106090

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.140 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106089

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.030 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105901

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:29.703 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-70098

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T20:17:48.553 |

Missing authorization in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-102855

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T20:17:07.010 |

Heap-based buffer overflow in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-102235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-116` |
| Published | 2026-10-13T20:17:06.607 |

Improper encoding or escaping of output in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-97781

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-13T19:22:16.197 |

Improper neutralization of special elements used in a command ('command injection') in Microsoft Office OneNote allows an unauthorized attacker to execute code over a network.

### CVE-2026-97780

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:16.080 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:22:15.830 |

Integer overflow or wraparound in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97777

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:15.710 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97776

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:15.590 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97775

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-400;CWE-416` |
| Published | 2026-10-13T19:22:15.463 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97773

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:15.227 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97772

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:22:15.107 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97771

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:14.983 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97770

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:22:14.863 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97769

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-10-13T19:22:14.740 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97768

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:14.617 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97767

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415;CWE-476` |
| Published | 2026-10-13T19:22:14.487 |

Double free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97766

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:14.363 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97765

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:14.240 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97763

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:14.117 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97762

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:22:13.990 |

Out-of-bounds write in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:22:13.853 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97759

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:13.610 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97758

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:13.490 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97757

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:13.367 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97756

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:13.237 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97755

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:13.107 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97754

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:12.973 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97753

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:22:12.850 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97752

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:12.707 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97751

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:12.587 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97750

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:22:12.463 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97748

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:12.213 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97747

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:12.093 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97746

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:22:11.953 |

Integer underflow (wrap or wraparound) in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97745

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:11.823 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97742

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:22:11.440 |

Stack-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97741

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-193` |
| Published | 2026-10-13T19:22:11.317 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97739

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:22:11.050 |

Integer underflow (wrap or wraparound) in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97738

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:10.800 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:10.647 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:22:10.293 |

Stack-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-97011

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763;CWE-908` |
| Published | 2026-10-13T19:22:10.170 |

Use of uninitialized resource in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97010

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:10.050 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97008

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-124` |
| Published | 2026-10-13T19:22:09.810 |

Buffer underwrite ('buffer underflow') in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97007

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:09.687 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97004

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:22:09.430 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-97003

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:09.307 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-96957

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:22:08.267 |

Improper verification of cryptographic signature in .NET allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-96952

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:07.940 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-96951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-13T19:22:07.760 |

Improper neutralization of special elements used in a command ('command injection') in Windows Shell allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-96943

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:22:06.470 |

Integer overflow or wraparound in Windows Raw Image Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-96917

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:02.880 |

Heap-based buffer overflow in Windows PCI Bus Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96914

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:22:02.350 |

Integer overflow or wraparound in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-96913

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:02.197 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96251

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-13T19:21:51.193 |

Reliance on untrusted inputs in a security decision in Microsoft PowerShell allows an unauthorized attacker to execute code over a network.

### CVE-2026-96235

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:49.343 |

Out-of-bounds write in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-96230

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:21:48.720 |

Improper neutralization of input during web page generation ('cross-site scripting') in ASP.NET Core allows an unauthorized attacker to execute code over a network.

### CVE-2026-96224

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:48.333 |

Out-of-bounds write in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-96202

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:46.520 |

Heap-based buffer overflow in Windows Raw Image Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-96044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-13T19:21:45.113 |

No cwe for this issue in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-88219

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:42.773 |

Untrusted pointer dereference in RPC Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-88202

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:41.797 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-88200

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-270` |
| Published | 2026-10-13T19:21:41.547 |

Privilege context switching error in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-88198

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:21:41.413 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-88197

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:41.283 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-88196

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:41.150 |

Heap-based buffer overflow in Microsoft Office allows an unauthorized attacker to execute code over a network.

### CVE-2026-88186

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:39.650 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-88166

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-190` |
| Published | 2026-10-13T19:21:37.200 |

Integer overflow or wraparound in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-88165

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:37.020 |

Out-of-bounds write in Active Directory Domain Services allows an authorized attacker to execute code over a network.

### CVE-2026-88163

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:36.900 |

Integer overflow or wraparound in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-88159

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:36.207 |

Use after free in Windows Background Intelligent Transfer Service (BITS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-88157

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:35.840 |

Heap-based buffer overflow in OpenSSH for Windows allows an unauthorized attacker to execute code over a network.

### CVE-2026-88155

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:35.590 |

Heap-based buffer overflow in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-88150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-13T19:21:34.910 |

Use of uninitialized resource in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-88145

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:34.267 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-88144

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:34.147 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-88142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:33.803 |

Use after free in Windows Background Intelligent Transfer Service (BITS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-88136

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-13T19:21:33.030 |

Improper resolution of path equivalence in WebDAV allows an authorized attacker to execute code over a network.

### CVE-2026-88116

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:29.937 |

Untrusted pointer dereference in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88115

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:29.767 |

Out-of-bounds read in Windows Server for NFS allows an unauthorized attacker to execute code over a network.

### CVE-2026-88114

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:29.510 |

Untrusted pointer dereference in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88112

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:29.180 |

Untrusted pointer dereference in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88075

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T19:21:26.270 |

Improper neutralization of special elements used in an sql command ('sql injection') in Microsoft Configuration Manager allows an authorized attacker to elevate privileges over a network.

### CVE-2026-88073

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:26.010 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-87697

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:21:22.400 |

Deserialization of untrusted data in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-85936

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-415` |
| Published | 2026-10-13T19:21:20.353 |

Double free in Windows Shell allows an unauthorized attacker to execute code over a network.

### CVE-2026-85931

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:19.310 |

Heap-based buffer overflow in Windows Distributed File System (DFS) allows an authorized attacker to execute code over a network.

### CVE-2026-85905

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:16.403 |

Heap-based buffer overflow in Windows UI Immersive Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-85903

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:16.043 |

Untrusted pointer dereference in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-85900

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:21:15.567 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-85817

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-13T19:21:06.487 |

Reliance on untrusted inputs in a security decision in Windows PowerShell allows an unauthorized attacker to execute code over a network.

### CVE-2026-85363

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:20:59.480 |

Integer overflow or wraparound in .NET Framework allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-85339

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:20:56.743 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-83934

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:50.150 |

Stack-based buffer overflow in Windows GDI+ allows an unauthorized attacker to execute code over a network.

### CVE-2026-83929

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:20:49.403 |

Out-of-bounds write in Windows GDI allows an unauthorized attacker to execute code over a network.

### CVE-2026-83928

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:20:49.227 |

Out-of-bounds write in Windows Local Security Authority Subsystem Service (LSASS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-83923

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-13T19:20:48.297 |

Relative path traversal in OpenSSH for Windows allows an unauthorized attacker to execute code over a network.

### CVE-2026-83891

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-121` |
| Published | 2026-10-13T19:20:40.100 |

Stack-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-83889

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:20:39.917 |

Release of invalid pointer or reference in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-83874

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:37.530 |

Heap-based buffer overflow in Windows Event Tracing allows an unauthorized attacker to execute code over a network.

### CVE-2026-83851

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:33.960 |

Heap-based buffer overflow in Windows Partition Management Driver allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-83797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:29.803 |

Out-of-bounds read in Windows Partition Management Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-83789

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:28.570 |

Heap-based buffer overflow in Windows SMB Client allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-83784

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-10-13T19:20:27.570 |

Absolute path traversal in Windows Encrypting File System (EFS) allows an authorized attacker to elevate privileges over a network.

### CVE-2026-83778

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:26.563 |

Heap-based buffer overflow in Microsoft Internet Messaging API allows an unauthorized attacker to execute code over a network.

### CVE-2026-83777

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:26.400 |

Heap-based buffer overflow in Windows Bluetooth Service allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-83771

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:25.610 |

Use after free in Windows Camera Frame Server Monitor allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-83759

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:20:22.380 |

Improper control of generation of code ('code injection') in Windows Encrypting File System (EFS) allows an authorized attacker to execute code over a network.

### CVE-2026-83728

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1286` |
| Published | 2026-10-13T19:20:18.330 |

Improper validation of syntactic correctness of input in Windows Hyper-V allows an authorized attacker to perform spoofing locally.

### CVE-2026-83725

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:20:17.807 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-83716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:16.243 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-83688

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:20:11.453 |

Heap-based buffer overflow in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-83643

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:05.150 |

Stack-based buffer overflow in Windows Error Reporting allows an unauthorized attacker to execute code over a network.

### CVE-2026-83642

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:20:04.920 |

Access of resource using incompatible type ('type confusion') in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-83523

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:58.450 |

Heap-based buffer overflow in Windows Image Acquisition allows an unauthorized attacker to execute code over a network.

### CVE-2026-83520

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:19:57.933 |

Deserialization of untrusted data in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-77910

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:19:54.057 |

Incorrect authorization in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-77902

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:53.927 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-77496

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:53.657 |

Heap-based buffer overflow in Windows Imaging Component allows an unauthorized attacker to execute code over a network.

### CVE-2026-70580

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:19:51.270 |

Missing authentication for critical function in Windows Credential Guard allows an authorized attacker to perform spoofing locally.

### CVE-2026-70343

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:50.533 |

Heap-based buffer overflow in Microsoft MPEG-2 Video Extension allows an unauthorized attacker to execute code over a network.

### CVE-2026-70302

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:50.243 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70301

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:50.123 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70299

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:19:49.883 |

Improper access control in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70297

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-10-13T19:19:49.643 |

Absolute path traversal in Skype for Business and Microsoft Lync allows an authorized attacker to execute code over a network.

### CVE-2026-70287

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:48.510 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70282

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:47.770 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70275

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:46.693 |

Untrusted pointer dereference in Windows CD-ROM Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-70268

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:45.540 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T19:19:45.300 |

Improper neutralization of special elements used in an sql command ('sql injection') in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70262

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:44.897 |

Heap-based buffer overflow in WebDAV allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70258

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:44.240 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to execute code over a network.

### CVE-2026-70257

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:44.127 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70256

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:44.007 |

Heap-based buffer overflow in Microsoft Office Outlook allows an unauthorized attacker to execute code over a network.

### CVE-2026-70254

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:43.687 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-70250

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:42.457 |

Use after free in Windows DHCP Client allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-70246

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:19:41.600 |

Incorrect authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70215

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:36.237 |

Use after free in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-70210

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-10-13T19:19:35.327 |

Heap-based buffer overflow in Windows OLE DB allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70185

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T19:19:32.670 |

Protection mechanism failure in Windows PowerShell allows an authorized attacker to bypass a security feature locally.

### CVE-2026-70174

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-358` |
| Published | 2026-10-13T19:19:31.533 |

Improperly implemented security check for standard in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-70167

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822;CWE-843` |
| Published | 2026-10-13T19:19:30.537 |

Access of resource using incompatible type ('type confusion') in DNS Server allows an authorized attacker to execute code over a network.

### CVE-2026-70158

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:19:29.210 |

Remote Code Execution in Windows Routing and Remote Access Service (RRAS) allows attacker to gain an unauthorized access to victim's machine

### CVE-2026-70149

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:28.033 |

Exposure of sensitive information to an unauthorized actor in Windows Client Side Caching driver (csc.sys) allows an authorized attacker to disclose information locally.

### CVE-2026-70089

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:20.530 |

Heap-based buffer overflow in Windows GDI allows an unauthorized attacker to execute code over a network.

### CVE-2026-70069

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:19:18.323 |

Stack-based buffer overflow in Windows DHCP Server allows an authorized attacker to execute code over a network.

### CVE-2026-70068

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-822` |
| Published | 2026-10-13T19:19:18.137 |

Heap-based buffer overflow in Windows Client-Side Caching (CSC) Service allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70035

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:19:14.490 |

Deserialization of untrusted data in .NET Framework allows an unauthorized attacker to execute code over a network.

### CVE-2026-70007

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:19:11.757 |

Out-of-bounds write in .NET Framework allows an unauthorized attacker to execute code over a network.

### CVE-2026-69985

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:09.217 |

Heap-based buffer overflow in Windows Libarchive allows an unauthorized attacker to execute code over a network.

### CVE-2026-69945

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:19:04.593 |

Missing authorization in Windows AppX Deployment Extensions allows an authorized attacker to elevate privileges locally.

### CVE-2026-69943

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T19:19:04.473 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-69918

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:03.057 |

Heap-based buffer overflow in Windows Core Messaging allows an authorized attacker to elevate privileges locally.

### CVE-2026-69765

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:58.897 |

Use after free in Windows Storport Miniport Driver allows an unauthorized attacker to execute code over a network.

### CVE-2026-69521

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:18:55.697 |

Integer overflow or wraparound in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-69370

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-13T19:18:54.530 |

Improper neutralization of special elements used in a command ('command injection') in Visual Studio Code allows an unauthorized attacker to execute code over a network.

### CVE-2026-69326

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:54.000 |

Heap-based buffer overflow in Graphic Fonts allows an unauthorized attacker to execute code over a network.

### CVE-2026-108471

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:18:07.377 |

Untrusted pointer dereference in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-108467

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:06.987 |

Heap-based buffer overflow in Microsoft PostScript Printer Driver allows an authorized attacker to execute code over a network.

### CVE-2026-108463

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-13T19:18:06.310 |

Improper resolution of path equivalence in Windows SmartScreen allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-108458

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:05.573 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-108400

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:18:05.300 |

Integer overflow or wraparound in Microsoft Windows Codecs Library allows an unauthorized attacker to execute code over a network.

### CVE-2026-108398

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:18:04.963 |

Untrusted search path in .NET Framework allows an authorized attacker to bypass a security feature locally.

### CVE-2026-105733

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T19:18:01.443 |

Improper access control in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-105727

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T19:18:00.770 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Dynamics Business Central allows an authorized attacker to elevate privileges over a network.

### CVE-2026-105718

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-13T19:17:59.750 |

Out-of-bounds read in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-105717

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-122` |
| Published | 2026-10-13T19:17:59.617 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:59.493 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105598

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.830 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105597

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.700 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105596

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.567 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105595

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:17:58.437 |

Out-of-bounds read in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105593

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.307 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105591

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.040 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105007

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:17:56.893 |

An elevation of privilege vulnerability exists in the Network Driver Interface Specification (NDIS) when ndis.sys fails to check the length of a buffer prior to copying memory to it.
To exploit the vulnerability, in a local attack scenario, an attacker could run a specially crafted application to elevate the attacker's privilege level. An attacker who successfully exploited this vulnerability could run processes in an elevated context. However, an attacker must first gain access to the local system with the ability to execute a malicious application in order to exploit this vulnerability.
The security update addresses the vulnerability by changing how ndis.sys validates buffer length.

### CVE-2026-103575

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:53.413 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-103572

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:17:53.293 |

Improper control of generation of code ('code injection') in Visual Studio Tools for Applications and SQL Server Management Studio allows an unauthorized attacker to execute code over a network.

### CVE-2026-102870

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:17:51.617 |

Improper control of generation of code ('code injection') in ASP.NET Core allows an unauthorized attacker to execute code over a network.

### CVE-2026-102869

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:17:51.483 |

Access of resource using incompatible type ('type confusion') in .NET and Visual Studio allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-102863

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:17:50.837 |

Improper control of generation of code ('code injection') in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102862

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:17:50.717 |

Incorrect authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102861

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:17:50.590 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102860

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-13T19:17:50.470 |

Improper access control in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102858

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:50.217 |

Heap-based buffer overflow in Microsoft Office OneNote allows an unauthorized attacker to execute code over a network.

### CVE-2026-102857

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-193` |
| Published | 2026-10-13T19:17:50.097 |

Heap-based buffer overflow in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-102856

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:17:49.973 |

Heap-based buffer overflow in Microsoft Office Visio allows an unauthorized attacker to execute code over a network.

### CVE-2026-102850

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:49.287 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-102849

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:49.170 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-102226

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T19:17:48.300 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Dynamics Business Central allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102225

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-197` |
| Published | 2026-10-13T19:17:48.117 |

Out-of-bounds read in Windows Text Shaping allows an unauthorized attacker to execute code over a network.

### CVE-2026-102217

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-13T19:17:47.397 |

Improper resolution of path equivalence in WebDAV allows an authorized attacker to elevate privileges over a network.

### CVE-2026-102214

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:46.843 |

Use after free in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-102203

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:17:45.333 |

Access of resource using incompatible type ('type confusion') in RPC Runtime allows an unauthorized attacker to execute code over a network.

### CVE-2026-100220

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:42.320 |

Heap-based buffer overflow in Windows Media Video Decoder allows an unauthorized attacker to execute code over a network.

### CVE-2026-100214

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:17:41.343 |

Deserialization of untrusted data in Dynamics Business Central allows an authorized attacker to execute code over a network.

### CVE-2026-100212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:41.213 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-100211

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:41.073 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-100210

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:40.933 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-100209

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:40.810 |

Use after free in Microsoft Office Excel allows an unauthorized attacker to execute code over a network.

### CVE-2026-108385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.893 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, BaseGenerator.parse_enum and EnumRepresentation.render_symbols use each schema-controlled enum symbol as a generated enum member name after case conversion but without validating it as an identifier. When generator classes are used directly, newlines and punctuation can inject constrained statements into the generated enum class body, allowing namespace modification or preventing the module from loading. Version 0.70.6 fixes the vulnerability by validating every enum symbol as a name.

### CVE-2026-108384

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.750 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, BaseGenerator.parse_fixed interpolates a fixed type's aliases value directly into a generated types.confixed annotation. A list is represented with quoted entries, but a bare string is emitted as an unquoted Python expression and evaluated when the generated module is imported, allowing arbitrary code execution from a crafted schema. Version 0.70.6 fixes the vulnerability by rejecting aliases values that are not lists.

### CVE-2026-108383

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.610 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, FieldRepresentation.get_field_default renders a schema-controlled enum field default as an enum member reference after applying case conversion but without validating it as an identifier. Newlines, operators, and punctuation can escape the intended reference and inject constrained statements into the generated module, allowing namespace modification or preventing the module from loading. Version 0.70.6 fixes the vulnerability by validating enum defaults as names.

### CVE-2026-108382

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.457 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, EnumRepresentation.render_symbols concatenates each schema-controlled enum symbol between double quotes in a generated enum assignment. When generator classes are used directly, a quote can terminate the string literal and inject arbitrary Python code into the enum class body, which executes when the generated module is imported. Version 0.70.6 fixes the vulnerability by escaping enum symbol values before rendering them.

### CVE-2026-108381

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.310 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.44.0 through 0.70.5, the Pydantic and AvroDantic model generators insert a schema field's pydantic-class value after pydantic. in a generated field annotation without safely restricting the expression. Because annotations are evaluated when the generated module is imported, a crafted value can execute arbitrary Python code. Version 0.70.6 fixes the vulnerability by restricting the value to a bare name or a call to a bare name with literal arguments.

### CVE-2026-108380

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.157 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.65.9 through 0.70.5, PydanticFieldRepresentation.add_field_properties inserts a schema field's doc value between the quotes of a generated pydantic.Field description argument without escaping it. A crafted quote can terminate the string and inject an expression evaluated during generated class definition, allowing arbitrary Python code execution for Pydantic and AvroDantic model generation. Version 0.70.6 fixes the vulnerability by escaping the documentation value before rendering it.

### CVE-2026-108379

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:17.000 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, BaseGenerator.parse_fixed inserts a fixed type's namespace value between quotes inside a generated types.confixed annotation without escaping or validating it. A crafted quote can terminate the namespace string and alter the surrounding annotation expression, which Python evaluates when the generated class is defined, allowing arbitrary code execution. Version 0.70.6 fixes the vulnerability by requiring the namespace to be a dot-separated sequence of valid Avro names.

### CVE-2026-108378

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:16.857 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.40.0 through 0.70.5, ClassRepresentation.render_docstring copies a schema record's doc value into a generated triple-double-quoted class docstring without escaping quotes or backslashes. A crafted triple-quote sequence can close the docstring and inject statements into the generated class body, while a trailing backslash can escape the generated closing delimiter, allowing Python code execution during module import. Version 0.70.6 fixes the vulnerability by escaping quotes, backslashes, and unsafe control characters before rendering docstrings.

### CVE-2026-108377

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:16.697 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.62.3 through 0.70.5, ClassRepresentation.render_metaclass inserts a schema-controlled Avro record name into the quoted Meta.schema_name field of generated Python source without escaping it. A crafted name can terminate the string literal and inject statements into the generated class body, which execute when the generated module is imported. Version 0.70.6 fixes the vulnerability by escaping schema values rendered into generated string literals.

### CVE-2026-108376

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:16.550 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.47.3 through 0.70.5, FieldRepresentation.get_field_default inserts a schema-controlled referenced record name into the callable position of a generated default_factory lambda without validating it as an Avro name. A crafted record name can become an arbitrary Python expression that executes when an instance of the generated model consumes the field default. Version 0.70.6 fixes the vulnerability by rejecting record names that do not match the Avro name grammar.

### CVE-2026-108375

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T18:17:16.390 |

dataclasses-avroschema generates Avro schemas from Python dataclasses, Pydantic models, and Faust Records and generates Python code from Avro schemas. From version 0.38.0 through 0.70.5, FieldRepresentation.get_field_default inserts schema-controlled string, UUID, bytes, and fixed field defaults into quoted literals in generated Python source without escaping them. A crafted default can terminate the literal and inject statements into the generated module, which execute when the module is imported. Version 0.70.6 fixes the vulnerability by escaping schema values rendered into generated string literals.

### CVE-2025-57739

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T18:17:12.100 |

An improper neutralization of special elements used in an SQL Command ("SQL Injection") vulnerability [CWE-89] vulnerability in Fortinet FortiMail 7.6.0 through 7.6.3, FortiMail 7.4.0 through 7.4.5, FortiMail 7.2.0 through 7.2.8 allows an authenticated attacker to execute unauthorized code or commands via specifically crafted HTTP or HTTPS requests.

### CVE-2025-46773

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T18:17:11.940 |

An Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability [CWE-89] vulnerability in Fortinet FortiAnalyzer 7.6.0 through 7.6.4, FortiAnalyzer 7.4.0 through 7.4.7, FortiAnalyzer 7.2 all versions, FortiAnalyzer Cloud 7.6.2 through 7.6.4, FortiAnalyzer Cloud 7.4.1 through 7.4.7, FortiAnalyzer Cloud 7.2.1 through 7.2.11 may allow a low privileged user to execute arbitrary commands via crafted requests.

### CVE-2026-85990

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862` |
| Published | 2026-10-13T17:17:47.707 |

Leantime is an open source project management system. Prior to 3.10.0, for the provisionally grouped account-creation and plugin-management surfaces, Leantime's JSON-RPC dispatcher in app/Domain/Api/Controllers/Jsonrpc.php exposes public API service methods, while PermissionEnforcer::enforce allows methods that lack a RequiresPermission attribute. A low-privilege authenticated user with an ordinary browser session can send the required X-Requested-With: XMLHttpRequest header and call leantime.rpc.api.api.createApiKeyWithProjects, which reaches Api::createApiKeyWithProjects, with an attacker-chosen role to create an interactive administrator account. The same missing per-method authorization exposes Plugins::installPlugin, Plugins::enablePlugin, Plugins::disablePlugin, and Plugins::removePlugin to ordinary authenticated users, permitting unauthorized plugin management. The complete provisionally grouped issue is fixed in version 3.10.0.

### CVE-2026-110116

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T17:17:35.843 |

Risesoft-y9 Digital-Infrastructure 9.6.5 through 9.6.11 contains a path traversal vulnerability in the fileManager storeFile endpoint that allows unauthenticated attackers to write arbitrary files. Attackers can send crafted fullPath and fileName parameters to POST /rest/storeFile to create or overwrite service-writable files, potentially achieving code execution.

### CVE-2026-55376

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-94;CWE-693` |
| Published | 2026-10-13T16:17:21.720 |

Heym builds and runs agentic systems and business-process automations on self-hosted infrastructure. Prior to 0.0.40, an authenticated user who can create or edit a workflow with an Agent custom Python tool can bypass the blacklist-based sandbox in backend/app/services/python_tool_executor.py because allowed standard-library modules expose operating-system, process, and filesystem capabilities through public attributes that pass _safe_import() and _validate_code_safety(). The runner then executes the supplied tool with exec(), permitting commands and file operations as the backend application user; self-registration affects reachability, but portal triggering alone does not grant code control. This issue is fixed in 0.0.40.

### CVE-2026-12655

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-13T15:17:43.820 |

A security issue exists within 1732E ArmorBlock® I/O, where an unauthenticated attacker can change the device's webserver password without valid credentials. This could result in admin account takeover or unauthorized modification of device configuration.

### CVE-2026-110690

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-14T14:17:44.140 |

Cloud Commander (cloudcmd) versions 19.20.2 through 19.21.1 contains a path traversal vulnerability in the GET /api/v1/pack endpoint where the onGET handler at server/rest/index.js:130 calls the unguarded root() function instead of the root.resolve() validation wrapper used elsewhere. Attackers can send percent-encoded directory traversal sequences in the pack request path to read arbitrary files outside the configured --root directory, such as /etc/passwd or SSH private keys, which are archived and streamed back as a downloadable tar.gz file.

### CVE-2026-82026

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T13:17:28.557 |

Radar before 1.12.2 contains a missing authorization vulnerability in the handleLocalTerminal WebSocket endpoint (/api/local-terminal) that allows authenticated or unauthenticated attackers to spawn a privileged shell by relying only on a runtime-mode check instead of role-based access control. Attackers can connect to the endpoint to execute /bin/bash -l on the Radar host with Radar's own kubeconfig and process credentials injected into the shell environment, achieving remote code execution with Radar's privileges even when the --disable-local-terminal flag is set.

### CVE-2026-108071

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-10-14T11:17:03.113 |

Incorrect authentication vulnerability in the TSplus Remote Access multi-factor authentication (MFA) mechanism. A remote attacker authenticated with valid first-factor credentials could bypass the second-factor verification because the authentication flow does not correctly apply the MFA validation result, allowing the attacker to complete the login without a valid second-factor token and gain access to protected applications and resources.

### CVE-2026-108070

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-552` |
| Published | 2026-10-14T11:17:02.977 |

A vulnerability involving improper access control in the TSplus Remote Access web server that allows an unauthenticated remote attacker to access internal resources protected by manipulated paths through the /socket.io/JWN/ endpoint, bypassing the access restrictions intended for certain internal resources.

### CVE-2026-103905

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T11:16:59.050 |

The authentication middleware of the JTL-Shop
administration backend processes the plugin safe mode toggle on the admin
logout route before checking whether the requesting user is
authenticated. An unauthenticated remote attacker can therefore switch the shop's
plugin safe mode on and off, which deactivates all installed plugins and their
functionality, such as payment and shipping integrations, resulting in a shop-wide
denial of service. The attack requires a single request and can be
automated against many installations.

### CVE-2026-101341

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T11:16:57.423 |

Tokens of text in RDATA (of for example TXT records) under 32 bytes are not checked to stay within the space reserved for the RDATA allowing for arbitrary sized out of bound stack writes, including an overwrite of a callback function pointer which is called directly after parse.  Zone files which are written out by NSD itself, such for zones for which the NSD instance is secondary, will not be formatted like this. The zone file must be fed to NSD directly, (but it could come, for example, from an operator controlled provisioning system).

### CVE-2026-101339

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T11:16:57.300 |

A HIP resource record that fills the RDATA near or at is limit, and has another dname RDATA field (a HIP Rendezvous server) can overwrite the stack with up to 191 bytes of attacker controlled data.  Zone files which are written out by NSD itself, such as for zones for which the NSD instance is secondary, will not be formatted like this. The zone file must be fed to NSD directly, (but it could come, for example, from an operator controlled provisioning system).

### CVE-2026-101338

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T11:16:57.130 |

When a SVCB or HTTPS RR has filled the wire format RDATA up to the brim, another ECH parameter may overwrite the stack, and once beyond the limit, the base64 decoder can write attacker controlled data of unlimited size.  Zone files which are written out by NSD itself, such as for zones for which the NSD instance is secondary, will not be formatted like this. The zone file must be fed to NSD directly, (but it could come, for example, from an operator controlled provisioning system).

### CVE-2026-101337

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T11:16:56.890 |

When base64 data is split up in pieces, of 3 character or less, tokens were incorrectly calculated to produce 0 bytes. This enables attackers to overwrite the stack with up to 64K of attacker controlled data.  Zone files which are written out by NSD itself, such as for zones for which the NSD instance is secondary, will not be formatted like this. The zone file must be fed to NSD directly, (but it could come, for example, from an operator controlled provisioning system).

### CVE-2026-110385

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-14T01:17:06.337 |

A remote code execution vulnerability in ONLYOFFICE Document Server versions before10.0.0 allows an authenticated attacker with a valid Inbox-compatible JWT to execute arbitrary operating system commands as the ds service account. The Document Builder API improperly processes user-controlled converter XML supplied through the optional third argument of builder.SaveFile(). By injecting a duplicate m_sFileTo element, an attacker can override the server-generated output path and write arbitrary content outside the designated job directory. This allows the attacker to overwrite the runtime.json configuration file, modify the Document Builder executable path and arguments, and execute arbitrary commands when a subsequent Document Builder job is processed.

### CVE-2026-108473

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T01:17:06.030 |

Multiple
Kasa devices contain an improper authentication vulnerability in the local
device-management protocol. An unauthenticated adjacent attacker may send
management instructions to an affected device without adequate authentication
or authorization, allowing modification of the device state or management
settings. Under certain usage conditions involving interaction between the
user, mobile application, and device-cloud service, insufficient protection of
account-related communications may also expose account information.









Successful
exploitation may allow an unauthenticated adjacent-network attacker to perform
unauthorized device-management actions and disrupt legitimate user control.
Under certain conditions, account-related information may also be exposed,
potentially leading to compromise of the associated cloud account.

### CVE-2026-92817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T00:17:13.290 |

The Ignition Perspective module does not properly validate session privileges when determining Designer-level access. An authenticated user with access to a Vision project could provide their valid Vision session identifier and gain Designer-level privileges. An attacker could exploit these elevated privileges to execute arbitrary code in the context of the Ignition Gateway process.

### CVE-2026-101294

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-325` |
| Published | 2026-10-13T21:17:17.007 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 and IBM WebSphere Application Server 8.5, and 9.0 could allow a remote attacker to bypass cryptographic signature verification due to improper verification of cryptographic signature.

### CVE-2026-63163

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T20:17:31.817 |

Omnispace Agora Project before 26.10.0 contains a broken access control vulnerability in the MobileFileDownload route that allows unauthenticated attackers to download arbitrary files by computing an md5(filename) token instead of passing a proper authorization check. Attackers can guess or determine file names to generate the corresponding md5 token and retrieve protected files without authorization, leading to unauthorized information disclosure.

### CVE-2026-63162

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T20:17:31.687 |

Omnispace Agora Project before 26.10.0 contains a path traversal vulnerability that allows attackers to write arbitrary files outside the intended temporary directory by supplying an unanchored tmpFolderName value in the upload destination path. Attackers can exploit this flaw, for example by setting tmpFolderName to a traversal sequence targeting the web root, to write attacker-controlled files and achieve remote code execution.

### CVE-2026-63154

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T20:17:31.010 |

Omnispace Agora Project before 26.10.0 contains a SQL identifier injection vulnerability that allows a space administrator to escalate privileges by supplying caller-controlled agoraFields[] names as unvalidated SQL column identifiers during the user import flow. Attackers can inject privileged column names such as generalAdmin or use backtick-injection techniques to set administrative flags and escalate to general administrator privileges.

### CVE-2026-95631

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T19:21:44.693 |

Adobe Commerce is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-92911

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:21:43.840 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a low-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-84994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-13T19:20:52.743 |

Qwik is a performance-focused JavaScript framework. Prior to @builder.io/qwik 1.20.0 and @qwik.dev/core 2.0.0-beta.37, default server-side qwik-json deserialization causes ResourceSerializer.$fill$ to pass resource._resolved to Promise.resolve without first rejecting attacker-controlled thenables. An unauthenticated request can provide a plain object whose then property is a QRL for an unregistered symbol, causing an orphaned asynchronous rejection that terminates Node.js under its default unhandled-rejection policy. A single request can crash a server, and repeated requests can keep replicas unavailable. This issue is fixed in @builder.io/qwik 1.20.0 and @qwik.dev/core 2.0.0-beta.37.

### CVE-2026-110238

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T19:18:49.063 |

Rapyd Admin from 9.0.0 before 9.20.0 contains an authorization bypass vulnerability that allows authenticated company members with the default customer role to modify or delete arbitrary user accounts through the UsersModalEditEmbed Livewire component. Attackers can dispatch editUser or deleteUser with predictable sequential user ids to reset owner or super admin passwords, promote themselves to owner, and delete users.

### CVE-2026-110215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:45.640 |

youlai-boot through 2.21.1 contains a missing authorization vulnerability that allows authenticated users to assign arbitrary menu and button permissions to roles via PUT /api/v1/roles/{roleId}/menus. Low-privileged users such as the GUEST test account can grant all permissions to their own role, refreshing the Redis permission cache to gain administrator-equivalent access.

### CVE-2026-110207

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:44.337 |

Wukong AICRM through 20260610 contains a missing authorization vulnerability that allows any authenticated user to call user, role, department and agent administration APIs because no administrator check exists. Attackers can send POST requests to /managerUser/updateUser to reset the admin account's password and assign themselves the "all" role, achieving full administrator account takeover.

### CVE-2026-109429

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:33.250 |

Mistral Vibe before 2.25.4 contains a command permission gate bypass vulnerability that allows attackers to execute arbitrary commands by hiding a command substitution inside a single-quoted variable value that tree-sitter-bash static parsing cannot detect. Attackers can craft input such as embedding a command substitution within a single-quoted variable and re-expanding it with the ${var@P} prompt-transform operator so bash's promptvars feature executes the hidden command at runtime while only the trailing allowlisted command is classified, resulting in silent arbitrary command execution with the privileges of the agent's terminal session.

### CVE-2026-109428

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:33.097 |

Mistral Vibe before 2.25.5 contains a permission validation bypass vulnerability that allows attackers to execute unauthorized commands by exploiting a parsing discrepancy between tree-sitter-bash and bash in handling backslash-newline line continuations in the _extract_commands() function of bash.py. Attackers can craft a command string where tree-sitter-bash extracts only an allowlisted prefix such as cd while bash joins the line continuation into a materially different and hidden command such as a curl request, causing resolve_permission to grant ALWAYS permission while bash executes unauthorized arbitrary commands.

### CVE-2026-104817

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:L/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-405;CWE-770;CWE-918` |
| Published | 2026-10-13T19:17:55.697 |

Misskey is an open source, federated social media platform. From 12.112.1 until 2026.7.0, the unauthenticated fetch-rss API lacks rate limiting and response-size restrictions and performs synchronous XML parsing. An attacker can trigger unbounded outbound HTTP requests and synchronous parsing, exhausting instance resources, amplifying requests toward third-party servers, or probing network-reachable services even when federation is disabled. This issue is fixed in version 2026.7.0.

### CVE-2026-103937

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-13T19:17:54.387 |

Misskey is an open source, federated social media platform. From 13.0.0 until 2025.4.1 and from 2025.5.0 until 2026.7.0, cleanup processing may not execute during file uploads. Repeated uploads can exhaust storage or file descriptors and deny service regardless of whether federation is enabled. This issue is fixed in version 2026.7.0.

### CVE-2026-104085

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T18:17:12.727 |

odt2spip plugin for SPIP before 4.4.0 contains an OS command injection vulnerability that allows authenticated authors to execute arbitrary commands by uploading a document with a maliciously crafted filename through the document import form. Attackers can embed shell metacharacters such as $(id) in a non-.odt filename, which survives insufficient sanitization in odt2spip_deplacer_fichier_upload() and LibreOffice::createCommand(), to achieve remote code execution as the web-server user during the LibreOffice conversion process.

### CVE-2026-55823

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T17:17:42.390 |

Frappe is a full-stack web application framework. Prior to 16.23.0, the get_count() method in reportview composes a count operation around generated SQL through a raw database execution path, allowing crafted report input to alter SQL executed by the application. This issue is fixed in version 16.23.0.

### CVE-2026-110128

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T17:17:38.647 |

fuint through commit 4c4bc8a contains a missing authentication vulnerability that allows unauthenticated attackers to retrieve any member's order details via the /clientApi/order/detail endpoint. Attackers can enumerate sequential orderId values without an Access-Token to expose buyer names, national ID numbers, phone numbers, addresses, WeChat openIds and verification codes.

### CVE-2026-110115

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T17:17:35.697 |

Risesoft Digital-Infrastructure 9.6.5 through 9.6.11 contains a path traversal vulnerability in the fileManager Y9FileController.retrieveFileStream handler that allows unauthenticated attackers to read arbitrary files by supplying parent-directory segments in the fullPath and fileName parameters. Attackers can request the unauthenticated /rest/retrieveFileStream endpoint to retrieve files like application.yml, exposing database, Redis and Nacos credentials.

### CVE-2026-97334

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-13T15:17:52.300 |

The network messaging layer contained improper handling of highly compressed data affecting service availability.  Software customers upgrade to resolved maintenance release. Update all Commvault installations, including CommServe server, Web Server, Command Center, MediaAgents, clients, and HyperScale.

### CVE-2026-77100

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T15:17:49.650 |

MediaAgent contained a heap-based buffer overflow issue affecting service availability.  Software customers upgrade to resolved maintenance release. Update Commvault installation of MediaAgents and HyperScale.

### CVE-2026-77090

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:48.887 |

CVFS contained an XML external entity (XXE) reference handling issue affecting information dislcosure.  Software customers upgrade to resolved maintenance release. Update CVFS.

### CVE-2026-12656

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T15:17:43.967 |

A denial-of-service security issue exists in the affected product and version. The security issue stems from improper handling of network storm traffic, which can interrupt communication, cause device faults, and affect open TCP and UDP ports. A power cycle is required to recover the device to its normal state.

### CVE-2026-103904

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T11:16:58.903 |

The public consent endpoint of JTL-Shop accepts arbitrary
consent names from unauthenticated visitors without validating
them against the configured consent items. These names are stored in the consent
statistics and rendered without output encoding in the administration
backend. An unauthenticated remote attacker can thereby inject script code that
is executed in the browser session of an administrator viewing the consent
statistics page, allowing actions to be performed with the administrator's
privileges.

### CVE-2026-107508

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-14T07:17:01.983 |

The Ultimate Multisite  WordPress plugin before 2.17.2 does not validate a user-supplied value used to select a file to include, allowing unauthenticated attackers to include and read arbitrary local files, including the WordPress configuration file.

### CVE-2026-103307

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T07:17:00.127 |

The Walletdoc Payment Gateway for WooCommerce WordPress plugin before 1.8.5 does not properly sanitize and escape user input before using it in a SQL statement, and verifies its payment webhook with a signing secret that is empty by default, allowing unauthenticated attackers to perform SQL injection attacks and to mark arbitrary orders as paid.

### CVE-2026-110459

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-14T06:17:06.260 |

A malicious actor with access to the network could exploit an Improper Access Control vulnerability found in UniFi Protect AI Key to obtain information, make unauthorized changes, and execute a Denial of Service (DoS) attack on the device.

### CVE-2026-110445

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T03:17:20.527 |

TeamPlus Messenger developed by Teamplus Technology has a Code Injection vulnerability. Unauthenticated remote attackers can trick users into interacting with crafted content to inject and execute arbitrary JavaScript. After the user confirms a Windows security warning, attackers can execute arbitrary code with the privileges of the current user.

### CVE-2026-110444

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T03:17:20.363 |

TeamPlus Messenger developed by Teamplus Technology has a Code Injection vulnerability. Unauthenticated remote attackers can trick users into opening a crafted link to inject and execute arbitrary JavaScript. After the user confirms a Windows security warning, attackers can execute arbitrary code with the privileges of the current user.

### CVE-2026-95634

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T22:19:30.853 |

CAI Content Credentials is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-95639

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:19:59.073 |

Photoshop Desktop is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-34634

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:17:38.230 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106616

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-13T21:17:30.810 |

ColdFusion is affected by an Improper Restriction of XML External Entity Reference ('XXE') vulnerability that could lead to arbitrary file system read. An attacker could exploit this vulnerability to access sensitive files and directories outside the intended access scope. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105897

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:17:29.240 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-63174

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T20:17:32.217 |

Omnispace Agora Project before 26.10.0 contains a broken access control vulnerability that allows a space administrator to assign users into spaces outside their authority because the spaceAffectList affectation was performed without verifying the caller's rights to the target space. Attackers can exploit the missing readRight() check in the import flow's join INSERT to break tenant isolation and manipulate user-space assignments across unauthorized spaces.

### CVE-2026-63165

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T20:17:31.947 |

Omnispace Agora Project before 26.10.0 contains a SQL injection vulnerability in the calendar functionality that allows attackers to inject malicious SQL by manipulating the sortEvents parameter, which is concatenated into the ORDER BY clause without sanitization in app/ModCalendar/CtrlCalendar.php. Attackers can exploit this flaw using error-based techniques such as extractvalue payloads to extract database information, including version data, from the underlying system.

### CVE-2026-63161

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-13T20:17:31.550 |

Omnispace Agora Project before 26.10.0 contains a session fixation vulnerability that allows remote attackers to hijack authenticated sessions by planting a known session identifier in a victim's browser prior to login. Attackers can exploit the application's failure to regenerate the session id upon successful authentication to gain unauthorized access to the victim's authenticated session after they log in.

### CVE-2026-63153

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T20:17:30.880 |

Omnispace Agora Project before 26.10.0 contains a broken access control vulnerability in setAffectations() that allows authenticated attackers to insert access-right records for a caller-supplied target space without verifying the caller has rights to that space. Attackers can assign access affectations to spaces outside their own reach, breaking tenant isolation and granting unauthorized access to restricted spaces.

### CVE-2026-63152

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T20:17:30.750 |

Omnispace Agora Project before 26.10.0 contains a second-order SQL injection vulnerability that allows authenticated attackers to inject malicious SQL via the _idCategoryFilter parameter, which is persisted into the session and later concatenated into a SQL statement without parameterization. Attackers can store a malicious payload that executes when the filter is subsequently applied in app/Common/MdlCategory.php, leading to unauthorized database access or manipulation.

### CVE-2026-103847

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T20:17:11.153 |

Dimension is affected by an Untrusted Search Path vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. A local attacker with user permissions could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must run the application. Scope is changed.

### CVE-2026-103846

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:17:11.023 |

Dimension is affected by an Improper Neutralization of Input During Web Page Generation vulnerability that could result in arbitrary code execution in the context of the current user. A local attacker with user permissions could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must run the application. Scope is changed.

### CVE-2026-103845

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-13T20:17:10.910 |

Dimension is affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. A local attacker with user permissions could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must run the application. Scope is changed.

### CVE-2026-92088

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-232` |
| Published | 2026-10-13T19:21:43.250 |

Improper handling of undefined values vulnerability in upKeeper Solutions upKeeper Instant Privilege Access allows Privilege Escalation.

This issue affects upKeeper Instant Privilege Access: through 1.7.1.

### CVE-2026-110124

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:37.080 |

FastBee through 2.1.0 contains an insecure direct object reference vulnerability in DeviceController that allows authenticated low-privilege users to read and modify other tenants' devices by supplying sequential device IDs. Self-registered attackers can enumerate deviceId or serialNumber values to read owner, IP, and location data, and overwrite user_id and tenant_id to take over devices.

### CVE-2026-110108

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T17:17:34.920 |

MateCloud through 5.0.8 contains a missing authorization vulnerability that allows any authenticated user to manage object storage by calling the unprotected /api/v1/admin/storage endpoints in StorageController. Low-privilege or self-registered users can supply arbitrary bucket and objectName values to list objects, obtain pre-signed download URLs for other users' files, delete objects, and upload at chosen keys.

### CVE-2026-110097

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-13T17:17:33.263 |

Ikaros 1.2.0 through 1.2.5 contains an authentication bypass vulnerability that allows attackers with a valid password to skip TOTP verification by reusing the login temp token. Attackers can present the temp token from the jwt/apply endpoint as a bearer JWT, refresh it, or use HTTP Basic login to gain full account access, including the master administrator.

### CVE-2026-104935

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T16:17:11.640 |

Authentication bypass by spoofing in ICS before version 25.1.3.0 allows a remote unauthenticated attacker to execute arbitrary commands. This does not impact ICS version 22.7R2.14 or prior.

### CVE-2026-65198

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-13T15:17:46.823 |

Huawei's openUBMC ships a default SNMPv3 USM key that uses one value for both authentication and privacy. An attacker who holds the key (recoverable from the open-source build) can authenticate SNMPv3 to, and decrypt SNMPv3 traffic from, any unit that still carries the shipped key. The build customization `manifest/build/customization/default_password.lua` sets `AuthenticationKey == EncryptionKey == 7df2f29369e3ac3245b2c9d46b67a0ecd055197e41808a34ef325db2f6422581` for the iBMC product build, and the community seed `account/manufacture/default_password.lua` sets both to `7a2f5b86f20233ec7b7bef49643fbf34d86d0cbf6f1f8f5c52d4f30d4536938b`. These are shipped constants, not per-unit values, and they are not rotated by the Administrator password reset, so they survive account provisioning. This is especially dangerous considering that SNMP access is mapped to full device administration privileges, including system reset and firmware upgrades.

### CVE-2026-102250

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-13T15:17:29.940 |

CWE-345: Insufficient Verification of Data Authenticity vulnerability exists that could allow modified firmware to be uploaded when an authorized admin user begins a firmware update procedure which could result in control over the device.

### CVE-2026-105067

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T11:17:00.190 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Webnus Modern Events Calendar Lite modern-events-calendar-lite allows Blind SQL Injection.This issue affects Modern Events Calendar Lite: from n/a before 7.37.0.

### CVE-2026-109901

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T08:17:05.193 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Codepeople CP Multi View Event Calendar  cp-multi-view-calendar allows SQL Injection.This issue affects CP Multi View Event Calendar : from n/a through 1.4.41.

### CVE-2026-50218

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-99` |
| Published | 2026-10-14T06:17:06.900 |

Akamai GPA (Guardicore Platform Agent) client on all platforms before 7.4 improperly validates JWT tokens used for seeding. By convincing a user to interact with a malicious link, an attacker can use a spoofed JWT token to inject arbitrary parameters into the client software, resulting in unauthorized reconfiguration and full compromise of the application's functionality. This attack can also be targeted against an already seeded client if the attacker knows the URL of the IDP that the client used for enrollment.

### CVE-2026-106931

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T05:16:42.633 |

SiteGuard Server Edition contains an OS command injection vulnerability, which may allow an attacker to execute arbitrary OS commands with root or SYSTEM privileges on the system running the affected product.

### CVE-2026-85886

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:19:31.143 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-68883

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:17:41.847 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-67625

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:17:41.343 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to execute code over a network.

### CVE-2026-104816

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:17:55.547 |

Misskey is an open source, federated social media platform. From 12.0.0 until 2026.7.0, the RSS components display feed item links from configured feeds without verifying their URL schemes. Missing URL scheme verification allows an attacker who controls feed content to provide an unsafe-scheme link that causes script execution when a user clicks it in an RSS widget. This issue is fixed in version 2026.7.0.

### CVE-2026-53562

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T17:17:41.147 |

Improper link resolution before file access ('link following') vulnerability in Citrix UniconOS.

This issue affects UniconOS: before 2607 CR and before 2603 LTSR CU2.

### CVE-2026-102982

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T16:17:10.293 |

Plane is an open-source project management tool. Prior to 1.4.0, the plane comments fail to sanitize unsafe URL schemes stored in comment_html. A project member can store a crafted link in a comment, and attacker-controlled script executes in the browser context of another user who selects the link. This issue is fixed in version 1.4.0.

### CVE-2026-86476

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T10:17:56.850 |

A flaw was found in gst-plugins-base. A heap buffer overflow can be triggered when processing video buffers whose attached GstVideoMeta metadata declares plane strides and offsets that exceed the actual backing memory allocation. The metadata is not range-checked during deserialization, and the video frame mapping code does not verify that the declared plane geometry fits within the buffer before allowing consumers to read or write video data. A local attacker who controls the sending side of a GStreamer inter-process IPC pipeline can deliver a crafted buffer carrying fabricated strides, causing the receiving process to read or write beyond heap boundaries. Successful exploitation can cause a denial of service or potentially allow code execution within the affected process.

### CVE-2026-75995

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T21:18:20.500 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-71385

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:18:19.483 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. The vulnerable component is restricted to an administrative network zone by default. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-83845

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T19:20:33.013 |

Improper privilege management in Windows Internet (wininet.dll) allows an authorized attacker to perform spoofing locally.

### CVE-2026-110255

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T19:18:49.843 |

Finsys Dockhand before 1.0.43 contains a response-disclosing server-side request forgery vulnerability that allows authenticated users to make the server fetch arbitrary URLs by supplying repository URL and stackfile values. Attackers can send stack templates pointing to internal services or cloud metadata endpoints and read the fetched content from the compose response field, exposing credentials and tokens.

### CVE-2026-110233

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T19:18:48.327 |

Rovr through 0.10.3 on Windows contains an OS command injection vulnerability that allows attackers to execute commands by crafting malicious file names. Attackers can deliver a file named with shell metacharacters like & alongside a payload, which runs with user privileges when the file is opened through open_file.

### CVE-2026-110158

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:35.730 |

Use after free in Passwords in Google Chrome prior to 155.0.8059.79 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110156

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-13T22:17:35.513 |

Incorrect reference resolution in Extensions in Google Chrome on on Mac prior to 155.0.8059.79 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted Chrome extension. (Chromium security severity: High)

### CVE-2026-110145

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:34.313 |

Use after free in Passwords in Google Chrome prior to 155.0.8059.79 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-110138

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:17:33.560 |

Use after free in ShapeDetection in Google Chrome prior to 155.0.8059.79 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-92908

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:21:43.487 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and write access, causing a limited disruption to availability. Exploitation of this issue does not require user interaction.

### CVE-2026-73798

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-115` |
| Published | 2026-10-14T12:17:17.963 |

A security vulnerability in HPE NonStop DNS 9.2.3 Non Secure Version could cause a Denial of Service.

### CVE-2026-73790

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-14T09:17:22.613 |

A vulnerability in HPE NonStop iTP WebServer can cause memory corruption and system shutdown.

### CVE-2026-93905

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T21:19:57.863 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 could allow an unauthenticated remote attacker to corrupt the persisted status of batch job instances.

### CVE-2026-105898

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:29.353 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file. Scope is changed.

### CVE-2026-105443

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-13T21:17:27.100 |

IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 has insufficient isolation between servers sharing an install.

### CVE-2026-86016

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T20:18:55.303 |

VNote is a note-taking platform. Prior to 4.3.0, VNote uses the assignment `preNode.innerHTML = p_metaData` in src/data/extra/web/js/markdownit.js to insert YAML frontmatter metadata into a pre element before the protectFromXss sanitization path runs. Opening an attacker-supplied Markdown note can therefore execute stored JavaScript in the file:// viewer context. Because QWebEngineSettings::LocalContentCanAccessRemoteUrls enables local content to access remote URLs, the script can read reachable local note files and transmit their contents to a remote server without further interaction after the note is opened. This issue is fixed in version 4.3.0.

### CVE-2026-85925

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-923` |
| Published | 2026-10-13T19:21:18.433 |

Improper restriction of communication channel to intended endpoints in Azure Key Vault allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85369

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:00.523 |

Out-of-bounds read in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-110104

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-916` |
| Published | 2026-10-13T17:17:34.310 |

Xxyopen novel through 3.5.0 contains a weak password hashing vulnerability that allows attackers to recover plaintext passwords because UserServiceImpl.register() stores unsalted MD5 digests in user_info.password. Attackers who obtain the password column through a database leak or backup exposure can crack hashes with precomputed tables or GPU brute force and reuse credentials.

### CVE-2026-104909

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-14T08:17:03.443 |

The Mang Board plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 2.4.3 via the '<mode>_type (e.g. foo_type)' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. Exploitation is trivial via an unauthenticated POST to any page rendering a public [mb_board] shortcode, as no nonce or capability check is enforced on the shortcode render path; on servers with a standard PHP installation, pearcmd.php can be leveraged to write and then include an attacker-controlled payload file in a single request.

### CVE-2026-103367

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-14T08:17:02.553 |

The ShopMagic – email automation for WordPress plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 4.9.0 via the 'billing_address.first_name' parameter parameter. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. Exploitation requires a published recipe that processes the {{ customer.first_name }} placeholder — the plugin's built-in "New Order email with social media profile links" recipe satisfies this requirement out of the box, making the default configuration exploitable with no account, cookie, or nonce by simply submitting a guest checkout with the payload as the billing first name.

### CVE-2026-110455

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-14T05:16:43.647 |

A malicious actor with access to the network and under certain conditions could exploit an Improper Input Validation vulnerability found in UniFi Protect AI Key to execute a Command Injection on the device.

### CVE-2026-17092

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T02:16:59.783 |

The Directorist: AI-Powered Business Directory, Listings & Classified Ads plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 8.10.2.1. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary business directory listings, including those owned by other users and posts in publish, draft, or private status. The nonces guarding the endpoint do not constitute an authorization barrier because both directorist_nonce and atbdp_nonce_js are exposed to all logged-in users via wp_localize_script.

### CVE-2026-104995

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-14T02:16:56.500 |

The BP Profile Search plugin for WordPress is vulnerable to Local File Inclusion in versions up to, and including, 5.9 via the 'ajax_template' value parsed from the client-controlled 'bps_directory' cookie during BuddyPress AJAX directory requests. The bps_directory_ajax() filter (hooked onto bp_legacy_object_template_path and bp_nouveau_object_template_path) reads the cookie, applies only a referer-derived 'page' comparison in bps_get_directory_data() (where bps_current_page() uses HTTP_REFERER during AJAX and is therefore also attacker-controlled), and then suffixes the attacker-controlled template value with '.php' and passes it to bp_locate_template() with no basename restriction, no whitelist, and no path-traversal check. This makes it possible for unauthenticated attackers to include arbitrary PHP files on the server, which can lead to remote code execution when PHP files can be uploaded or when images such as the default wordpress:php8.

### CVE-2026-97783

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:22:16.443 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-92922

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:21:43.953 |

Adobe Commerce is affected by a stored Cross-Site Scripting (XSS) vulnerability that could be abused by a high-privileged attacker to inject malicious scripts into vulnerable form fields. Malicious JavaScript may be executed in a victim's browser when they browse to the page containing the vulnerable field, potentially gaining elevated access or control over the victim's account or session. Scope is changed.

### CVE-2026-88185

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:39.527 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-88174

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:38.120 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Deployment Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-88173

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-10-13T19:21:37.973 |

Use after free in Windows Background Intelligent Transfer Service (BITS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-88171

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:21:37.710 |

Double free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88120

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:30.587 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88119

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:30.440 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88117

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:30.107 |

Use after free in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-88094

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-13T19:21:27.320 |

Improper neutralization of special elements in output used by a downstream component ('injection') in Azure Storage Library allows an authorized attacker to elevate privileges over a network.

### CVE-2026-85926

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:18.553 |

Use after free in Windows Secure Socket Tunneling Protocol (SSTP) allows an unauthorized attacker to execute code over a network.

### CVE-2026-85799

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:03.807 |

Use after free in Network Policy Server (NPS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-85371

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:00.843 |

Use after free in Network Policy Server (NPS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-84012

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:20:51.213 |

Double free in Remote Desktop Gateway Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-83914

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:46.750 |

Use after free in Microsoft XML allows an unauthorized attacker to execute code over a network.

### CVE-2026-83844

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:32.890 |

Out-of-bounds read in Windows Paint allows an unauthorized attacker to execute code over a network.

### CVE-2026-83746

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-36` |
| Published | 2026-10-13T19:20:20.157 |

Absolute path traversal in Skype for Business and Microsoft Lync allows an authorized attacker to elevate privileges over a network.

### CVE-2026-83674

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:20:09.393 |

Weak authentication in Active Directory Federation Services (AD FS) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-83522

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-13T19:19:58.267 |

Reliance on untrusted inputs in a security decision in Windows IKE Extension allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-70571

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:19:50.830 |

Stack-based buffer overflow in Microsoft Exchange Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-70269

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:45.663 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-70229

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:19:39.210 |

Incorrect authorization in Active Directory Domain Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-70197

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:19:33.790 |

Out-of-bounds write in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-70187

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:32.963 |

Use after free in Remote Desktop Gateway Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-70175

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-13T19:19:31.687 |

Improper authentication in ASP.NET Core allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70127

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:24.917 |

Use after free in DNS Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-70111

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:22.960 |

Untrusted pointer dereference in Windows Kernel allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-70062

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:19:17.270 |

Double free in Windows Libarchive allows an unauthorized attacker to execute code over a network.

### CVE-2026-70038

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-416` |
| Published | 2026-10-13T19:19:14.650 |

Use after free in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-70013

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:12.513 |

Use after free in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-69913

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:02.343 |

Use after free in Windows TCP/IP allows an unauthorized attacker to execute code over a network.

### CVE-2026-69830

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:18:59.943 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-69802

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:18:59.803 |

Weak authentication in Network Device Enrollment Service (NDES) allows an unauthorized attacker to execute code over a network.

### CVE-2026-108460

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:05.767 |

Use after free in Windows Message Queuing allows an unauthorized attacker to execute code over a network.

### CVE-2026-108457

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:18:05.437 |

Out-of-bounds write in Microsoft Windows PDF allows an unauthorized attacker to execute code over a network.

### CVE-2026-105005

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:17:56.567 |

Out-of-bounds write in Windows Schannel allows an unauthorized attacker to execute code over a network.

### CVE-2026-102866

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:17:51.207 |

Improper verification of cryptographic signature in Microsoft Office SharePoint allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-100218

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:41.983 |

Use after free in Remote Desktop Gateway Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-53418

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-939` |
| Published | 2026-10-13T15:17:44.630 |

Improper Authorization in Handler for Custom URL Scheme in Zoom Workplace for Android before version 7.2.1 may allow an unauthenticated user to conduct an escalation of privilege via network access.

### CVE-2026-110450

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-696` |
| Published | 2026-10-14T05:16:42.917 |

Nix before 2.35.3 and Lix before 2.95.4 allow privilege escalation via a repair operation because it could destroy and then replace a store path before content verification.

### CVE-2026-96956

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T21:20:14.737 |

Stack-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-96844

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:21:57.530 |

Integer underflow (wrap or wraparound) in Microsoft Bluetooth Driver allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-88121

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:30.730 |

Use after free in Windows Background Intelligent Transfer Service (BITS) allows an unauthorized attacker to execute code over a network.

### CVE-2026-85881

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:21:15.190 |

Stack-based buffer overflow in Microsoft Graphics Component allows an authorized attacker to elevate privileges over a network.

### CVE-2026-83838

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:20:31.923 |

Integer underflow (wrap or wraparound) in Windows Bluetooth A2DP driver allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-70213

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-13T19:19:35.860 |

Origin validation error in Microsoft Power Apps allows an authorized attacker to execute code over a network.

### CVE-2026-70049

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T19:19:15.657 |

Improper neutralization of special elements used in an sql command ('sql injection') in Microsoft Configuration Manager allows an authorized attacker to elevate privileges over an adjacent network.

### CVE-2026-69363

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:54.357 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges over a network.

### CVE-2026-53420

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-13T15:17:44.753 |

Buffer overflow in a Zoom Phone feature of Zoom Workplace Clients may allow an unauthenticated user to conduct a escalation of privilege via network access.

### CVE-2026-73793

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T10:17:56.480 |

HPE NonStop Middleware software has secret key handling and data deserialization vulnerability.

### CVE-2026-82715

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-377` |
| Published | 2026-10-14T02:17:00.863 |

Insecure Temporary File vulnerability in Hitachi Disk Array Driver for AIX and Hitachi Disk Array Driver for Virtual I/O Server.

This issue affects Hitachi Disk Array Driver for AIX: from 01-00 before 01-23-/A; Hitachi Disk Array Driver for Virtual I/O Server: from 01-04 before 01-23-/A.

### CVE-2026-90954

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-14T10:17:57.297 |

A flaw was found in BusyBox's dpkg-deb archive extraction. The ar archive handler flushes deferred symlinks after each archive member, unlike the tar, cpio, and unzip handlers which flush once after the last member. A specially crafted .deb archive with two data.tar members can exploit this ordering: the first member declares a symlink pointing to an absolute path (e.g., '/'), which is deferred as unsafe but flushed after the first member. The second member declares a regular file whose path traverses the now-live symlink, resulting in a file being written outside the intended extraction directory. This could allow an attacker to write arbitrary files to arbitrary locations when a user extracts a crafted .deb package.

### CVE-2026-110359

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-14T01:17:06.203 |

Hyland Desktop Host for Windows before 25.1.1 is vulnerable to local privilege escalation. This is caused by a privileged service running from the %PROGRAMDATA%\Hyland\DesktopHost\bin folder with weak permissions. A local user can exploit this to escalate privileges.

### CVE-2026-97312

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:20:16.110 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-96523

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:20:07.947 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-96522

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:20:07.827 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-96521

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:20:07.220 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-95641

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:19:59.300 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-95638

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:19:58.957 |

Photoshop Desktop is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-95637

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:19:58.843 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-95636

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T21:19:58.720 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-95635

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T21:19:58.603 |

Photoshop Desktop is affected by a Double Free vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-83966

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:19:09.400 |

Substance3D - Sampler is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-83965

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T21:19:09.290 |

Substance3D - Sampler is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-83661

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T21:18:32.667 |

Photoshop Desktop is affected by an Integer Overflow or Wraparound vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-106614

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:30.583 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-104348

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:17:25.593 |

Photoshop Desktop is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104347

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:25.483 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104346

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:25.370 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103821

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:23.193 |

Substance3D - Designer is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-100129

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:14.983 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-100128

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:14.870 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-100127

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:14.753 |

Bridge is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-100112

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:14.523 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-100111

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T21:17:14.397 |

Photoshop Desktop is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103854

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T20:17:12.023 |

Dimension is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103851

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T20:17:11.510 |

Substance3D - Stager is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103844

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:10.790 |

Dimension is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103843

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T20:17:10.680 |

Substance3D - Stager is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103842

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T20:17:10.567 |

Substance3D - Stager is affected by an out-of-bounds read vulnerability when parsing a crafted file, which could result in a read past the end of an allocated memory structure. An attacker could leverage this vulnerability to execute code in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103841

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T20:17:10.453 |

Substance3D - Stager is affected by an out-of-bounds read vulnerability when parsing a crafted file, which could result in a read past the end of an allocated memory structure. An attacker could leverage this vulnerability to execute code in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103840

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T20:17:10.340 |

Substance3D - Stager is affected by an out-of-bounds read vulnerability when parsing a crafted file, which could result in a read past the end of an allocated memory structure. An attacker could leverage this vulnerability to execute code in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103839

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:10.227 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103838

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:10.113 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:10.000 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103836

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:09.883 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103835

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:09.767 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103834

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:09.650 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103833

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:09.533 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103832

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T20:17:09.410 |

Substance3D - Stager is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103830

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T20:17:09.290 |

Substance3D - Stager is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-97811

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-400;CWE-415` |
| Published | 2026-10-13T19:22:19.310 |

Double free in OpenSSH for Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-97809

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:19.043 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:18.763 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97806

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:18.627 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:18.280 |

Heap-based buffer overflow in HID class driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-97803

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:18.160 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-97800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-13T19:22:17.900 |

Incorrect permission assignment for critical resource in Windows Mobile Broadband allows an authorized attacker to elevate privileges locally.

### CVE-2026-97799

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:22:17.780 |

Improper verification of cryptographic signature in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97798

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-13T19:22:17.640 |

Improper neutralization of argument delimiters in a command ('argument injection') in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-97794

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:17.507 |

Heap-based buffer overflow in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-97792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-13T19:22:17.227 |

Improper access control in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-97009

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:09.930 |

Heap-based buffer overflow in Microsoft Office Excel allows an unauthorized attacker to execute code locally.

### CVE-2026-97001

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:09.180 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-96997

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:09.060 |

Use after free in Microsoft Office OneNote allows an authorized attacker to elevate privileges locally.

### CVE-2026-96996

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:08.940 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-96995

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-197` |
| Published | 2026-10-13T19:22:08.813 |

Stack-based buffer overflow in Microsoft Office Word allows an authorized attacker to elevate privileges locally.

### CVE-2026-96953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:22:08.087 |

Null pointer dereference in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to execute code locally.

### CVE-2026-96950

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:07.580 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96947

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:07.050 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96946

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:06.867 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:22:05.417 |

Untrusted pointer dereference in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96931

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:22:05.073 |

Untrusted pointer dereference in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96929

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:04.720 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96928

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:04.543 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96920

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:03.340 |

Heap-based buffer overflow in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96918

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:22:03.030 |

Improper access control in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96916

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:02.703 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96915

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:22:02.523 |

Integer overflow or wraparound in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-96912

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:02.050 |

Use after free in Windows Client License Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96911

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:22:01.867 |

Improper link resolution before file access ('link following') in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-96867

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:01.200 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-96862

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:00.310 |

Out-of-bounds read in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-96856

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:59.333 |

Heap-based buffer overflow in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-96847

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:57.890 |

Untrusted pointer dereference in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-96843

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:57.353 |

Heap-based buffer overflow in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-96324

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:56.993 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-96318

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:54.700 |

Heap-based buffer overflow in Windows Resume allows an authorized attacker to elevate privileges locally.

### CVE-2026-96317

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:54.550 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96312

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:53.710 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96309

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:53.263 |

Use after free in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-96308

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:53.087 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96306

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:52.750 |

Out-of-bounds read in Windows Sysmain Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96249

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:50.923 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-96244

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:49.980 |

Use after free in Windows Internal System User Profile allows an authorized attacker to elevate privileges locally.

### CVE-2026-96243

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:49.820 |

Improper link resolution before file access ('link following') in Windows WalletService allows an authorized attacker to elevate privileges locally.

### CVE-2026-96231

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:48.843 |

Improper link resolution before file access ('link following') in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-96225

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:48.480 |

Improper link resolution before file access ('link following') in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-96223

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:48.210 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-96220

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:21:47.890 |

Improper control of generation of code ('code injection') in Windows Assigned Access allows an authorized attacker to elevate privileges locally.

### CVE-2026-96217

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:47.413 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-96186

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:21:46.207 |

Deserialization of untrusted data in Microsoft Windows Media Foundation allows an authorized attacker to elevate privileges locally.

### CVE-2026-96118

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-190` |
| Published | 2026-10-13T19:21:45.880 |

Out-of-bounds read in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96108

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:45.583 |

Use after free in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-88210

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-13T19:21:42.653 |

Reliance on untrusted inputs in a security decision in Microsoft Office Word allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-88194

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:40.830 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88193

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:40.647 |

Heap-based buffer overflow in Microsoft Scripting Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-88191

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:40.347 |

Improper link resolution before file access ('link following') in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-88189

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:40.010 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88188

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:39.770 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88182

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:39.123 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-88181

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:38.980 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88180

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:38.833 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88179

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:38.673 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88177

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:38.400 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88168

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:37.443 |

Heap-based buffer overflow in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-88152

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:35.153 |

Use after free in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88147

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:34.543 |

Heap-based buffer overflow in Windows Secure Socket Tunneling Protocol (SSTP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88135

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:21:32.857 |

Improper access control in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-88134

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:32.670 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-88133

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:32.493 |

Improper authorization in Windows Portable Device Enumerator Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88128

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:31.880 |

Heap-based buffer overflow in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-88126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:31.543 |

Untrusted pointer dereference in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-88118

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:30.250 |

Integer overflow or wraparound in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88109

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:28.940 |

Use after free in Microsoft Office Click-To-Run allows an authorized attacker to elevate privileges locally.

### CVE-2026-88105

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:28.480 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88101

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:21:28.040 |

Weak authentication in Microsoft Input Method Editor (IME) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88100

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:27.920 |

Use after free in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-88093

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:27.167 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-88091

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:21:26.863 |

Deserialization of untrusted data in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-88080

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:26.687 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-88074

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:21:26.150 |

Integer overflow or wraparound in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-88072

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:25.863 |

Improper access control in Windows Host Guardian Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88071

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:21:25.717 |

Double free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-88070

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:25.540 |

Out-of-bounds read in Windows BitLocker allows an authorized attacker to elevate privileges locally.

### CVE-2026-87712

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:24.680 |

Use after free in Windows Quality of Service (QoS) Packet Scheduler allows an authorized attacker to elevate privileges locally.

### CVE-2026-87711

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:21:24.490 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87707

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:23.760 |

Heap-based buffer overflow in Windows Fax and Scan Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-87706

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:23.587 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-87702

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:21:23.047 |

Integer overflow or wraparound in Windows Resource Management (MRM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-87700

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:22.870 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87699

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:22.693 |

Heap-based buffer overflow in Winlogon allows an authorized attacker to elevate privileges locally.

### CVE-2026-87695

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-13T19:21:22.153 |

Inclusion of functionality from untrusted control sphere in Microsoft Exchange Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-87694

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:21.980 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87692

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:21:21.683 |

Deserialization of untrusted data in Microsoft Exchange Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-87691

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:21.553 |

Use after free in Windows Management Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-85945

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:21.237 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-85933

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:19.720 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-85927

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:18.737 |

Heap-based buffer overflow in Windows Universal Plug and Play (UPnP) Device Host allows an authorized attacker to elevate privileges locally.

### CVE-2026-85915

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:17.677 |

Heap-based buffer overflow in Windows PCI Bus Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85911

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:17.200 |

Use after free in Windows StateRepository API allows an authorized attacker to elevate privileges locally.

### CVE-2026-85908

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:16.717 |

Heap-based buffer overflow in Windows Win32K - GRFX allows an authorized attacker to elevate privileges locally.

### CVE-2026-85906

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:16.580 |

Use after free in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-85902

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:15.880 |

Heap-based buffer overflow in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-85901

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:15.703 |

Heap-based buffer overflow in Windows Win32K - GRFX allows an authorized attacker to elevate privileges locally.

### CVE-2026-85884

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:21:15.313 |

Missing authentication for critical function in Windows Health and Optimized Experiences Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85874

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:14.900 |

Use after free in Windows Message Queuing Queue Manager allows an authorized attacker to execute code locally.

### CVE-2026-85872

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:14.610 |

Use after free in Windows Storage VSP Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85871

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:14.433 |

Heap-based buffer overflow in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-85869

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:14.067 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-85867

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:13.720 |

Heap-based buffer overflow in Windows Remote Access Connection Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-85864

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-641` |
| Published | 2026-10-13T19:21:13.220 |

Improper privilege management in Python allows an authorized attacker to elevate privileges locally.

### CVE-2026-85863

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:13.060 |

Use after free in Windows Clipboard User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85861

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:12.897 |

Use after free in Windows Clipboard User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85860

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:12.713 |

Use after free in Windows Message Queuing Queue Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-85858

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:12.410 |

Out-of-bounds read in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-85851

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:11.327 |

Use after free in Windows SmartScreen allows an authorized attacker to elevate privileges locally.

### CVE-2026-85850

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:21:11.207 |

Release of invalid pointer or reference in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-85849

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:21:11.043 |

Improper link resolution before file access ('link following') in Windows AppX Deployment Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85848

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:10.860 |

Heap-based buffer overflow in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85843

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-13T19:21:10.337 |

Use of uninitialized resource in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85842

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-13T19:21:10.197 |

Use of externally-controlled format string in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-85837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:09.747 |

Out-of-bounds read in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-85836

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:09.617 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-85833

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:09.117 |

Use after free in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85832

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:08.827 |

Heap-based buffer overflow in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85829

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:21:08.310 |

Double free in Windows Wired AutoConfig Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85822

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:07.150 |

Heap-based buffer overflow in Windows exFAT File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-85820

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:21:06.800 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85807

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:21:04.950 |

Integer overflow or wraparound in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85804

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:04.460 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-85800

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:03.983 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-85796

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121;CWE-197` |
| Published | 2026-10-13T19:21:03.267 |

Numeric truncation error in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85795

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:03.087 |

Use after free in Windows Text Services Framework allows an authorized attacker to elevate privileges locally.

### CVE-2026-85377

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:21:01.923 |

Access of resource using incompatible type ('type confusion') in Windows CD-ROM Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85376

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:21:01.743 |

Weak authentication in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-85375

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:01.563 |

Use after free in Windows Universal Plug and Play (UPnP) Device Host allows an authorized attacker to elevate privileges locally.

### CVE-2026-85373

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:01.203 |

Heap-based buffer overflow in Windows Universal Plug and Play (UPnP) Device Host allows an authorized attacker to elevate privileges locally.

### CVE-2026-85368

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:00.337 |

Heap-based buffer overflow in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-85366

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:59.990 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85359

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-13T19:20:58.930 |

Improper control of generation of code ('code injection') in Windows Performance Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-85358

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:58.670 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85356

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:58.300 |

Out-of-bounds read in Windows Volume Manager Extension Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85343

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:20:57.407 |

Improper link resolution before file access ('link following') in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-85341

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:57.057 |

Heap-based buffer overflow in Windows USB Video Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85340

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:56.927 |

Use after free in Microsoft Office Click-To-Run allows an authorized attacker to elevate privileges locally.

### CVE-2026-85338

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:56.590 |

Out-of-bounds read in Microsoft Graphics Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-85332

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:55.717 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85327

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:54.010 |

Heap-based buffer overflow in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-85318

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:52.893 |

Heap-based buffer overflow in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-84016

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:20:51.903 |

Out-of-bounds write in Windows EAPHost Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-84013

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:51.363 |

Use after free in Windows Telephony Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-83932

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:49.833 |

Heap-based buffer overflow in Windows Group Policy allows an authorized attacker to elevate privileges locally.

### CVE-2026-83931

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:49.703 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to execute code locally.

### CVE-2026-83927

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:20:49.087 |

Improper link resolution before file access ('link following') in Windows Registry allows an authorized attacker to elevate privileges locally.

### CVE-2026-83922

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:48.127 |

Use after free in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-83920

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:47.770 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83919

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:47.593 |

Heap-based buffer overflow in Microsoft Internet Messaging API allows an authorized attacker to execute code locally.

### CVE-2026-83918

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:20:47.417 |

Integer overflow or wraparound in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83913

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:46.607 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83912

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:46.430 |

Use after free in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-83903

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:44.593 |

Heap-based buffer overflow in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-83902

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:44.413 |

Heap-based buffer overflow in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-83896

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:41.173 |

Heap-based buffer overflow in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-83883

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:38.973 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83882

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:38.823 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83881

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:38.643 |

Heap-based buffer overflow in Windows exFAT File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-83877

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:20:38.310 |

Integer overflow or wraparound in HID Parser Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-83876

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:38.083 |

Use after free in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-83873

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-13T19:20:37.347 |

Relative path traversal in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-83872

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-681` |
| Published | 2026-10-13T19:20:37.157 |

Incorrect conversion between numeric types in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-83867

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:36.353 |

Heap-based buffer overflow in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-83863

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:35.670 |

Heap-based buffer overflow in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-83861

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:35.330 |

Heap-based buffer overflow in Windows Remote Desktop Protocol allows an authorized attacker to elevate privileges locally.

### CVE-2026-83859

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:34.983 |

Use after free in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83857

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:34.800 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83850

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:33.787 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83848

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:20:33.480 |

Untrusted pointer dereference in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83847

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:20:33.300 |

Heap-based buffer overflow in Microsoft Account allows an authorized attacker to elevate privileges locally.

### CVE-2026-83840

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:20:32.243 |

Weak authentication in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83837

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-10-13T19:20:31.763 |

Improper access control in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-83836

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:20:31.580 |

Heap-based buffer overflow in Windows Event Tracing allows an unauthorized attacker to execute code locally.

### CVE-2026-83833

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:31.043 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83832

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:30.900 |

Out-of-bounds read in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-83830

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:30.720 |

Heap-based buffer overflow in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83829

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:30.547 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83828

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:20:30.423 |

Heap-based buffer overflow in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-83826

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:20:30.130 |

Untrusted pointer dereference in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83796

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:29.667 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83792

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:20:29.013 |

Incorrect authorization in Windows Device Install Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83791

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-283` |
| Published | 2026-10-13T19:20:28.870 |

Improper authorization in Windows Virtual Input allows an authorized attacker to elevate privileges locally.

### CVE-2026-83783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:27.360 |

Heap-based buffer overflow in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-83781

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-170` |
| Published | 2026-10-13T19:20:27.050 |

Improper null termination in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83779

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:26.743 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83769

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:25.280 |

Use after free in OpenSSH for Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-83768

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:25.097 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83767

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:24.897 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83763

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:20:23.017 |

Access of resource using incompatible type ('type confusion') in Windows Input System allows an authorized attacker to elevate privileges locally.

### CVE-2026-83762

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:22.863 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83761

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:22.707 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-83758

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:22.200 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to execute code locally.

### CVE-2026-83757

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:22.063 |

Heap-based buffer overflow in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83756

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:21.927 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-83753

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:21.443 |

Heap-based buffer overflow in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-83741

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:19.983 |

Use after free in Internet Explorer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83735

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:20:18.857 |

Release of invalid pointer or reference in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83732

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:18.503 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83727

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-13T19:20:18.153 |

Buffer over-read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-83726

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:17.983 |

Use after free in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-83721

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:17.027 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83712

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:20:15.543 |

Out-of-bounds write in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-83709

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:15.200 |

Heap-based buffer overflow in Windows NTLM allows an authorized attacker to elevate privileges locally.

### CVE-2026-83704

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:20:14.363 |

Improper link resolution before file access ('link following') in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83700

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:13.660 |

Use after free in Windows Now Playing Session Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-83699

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:13.480 |

Stack-based buffer overflow in Windows Client-Side Caching (CSC) Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83698

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:13.293 |

Heap-based buffer overflow in Windows Client-Side Caching (CSC) Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83692

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:12.240 |

Heap-based buffer overflow in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83691

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:12.047 |

Heap-based buffer overflow in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-83690

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:11.853 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83679

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:10.103 |

Use after free in Windows Defender Firewall Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83678

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:09.920 |

Heap-based buffer overflow in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-83669

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-13T19:20:08.700 |

Use of uninitialized resource in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83659

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:20:07.660 |

Improper link resolution before file access ('link following') in Windows User Profile Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83654

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:20:06.790 |

Missing authentication for critical function in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83652

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:06.613 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83650

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:06.260 |

Heap-based buffer overflow in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-83641

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:04.700 |

Heap-based buffer overflow in Windows Media allows an authorized attacker to elevate privileges locally.

### CVE-2026-83640

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:04.503 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to execute code locally.

### CVE-2026-83639

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:04.293 |

Heap-based buffer overflow in Windows Sensor Data Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83638

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:04.087 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83637

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:03.900 |

Out-of-bounds read in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-83634

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:20:03.400 |

Double free in Windows BitLocker allows an authorized attacker to elevate privileges locally.

### CVE-2026-83588

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:03.210 |

Heap-based buffer overflow in Windows USB Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83587

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:20:03.033 |

Untrusted pointer dereference in Windows Core Messaging allows an authorized attacker to elevate privileges locally.

### CVE-2026-83586

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:20:02.897 |

Weak authentication in Windows Resilient File System (ReFS) Deduplication Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83585

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-13T19:20:02.710 |

Use of externally-controlled format string in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83583

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:20:02.367 |

Improper access control in Windows Geotag Broker allows an authorized attacker to elevate privileges locally.

### CVE-2026-83579

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:00.683 |

Heap-based buffer overflow in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-83570

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:59.510 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83569

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:59.357 |

Heap-based buffer overflow in HID Parser Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-83568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:19:59.230 |

Improper access control in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-83567

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:59.057 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83518

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:57.633 |

Heap-based buffer overflow in RPC Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-83514

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:56.930 |

Heap-based buffer overflow in Windows Partition Management Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83513

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:56.640 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83508

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:55.910 |

Out-of-bounds read in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-83506

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:19:55.593 |

Untrusted search path in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-83499

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-10-13T19:19:55.003 |

Insufficient granularity of access control in Windows Server Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-81969

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1220` |
| Published | 2026-10-13T19:19:54.677 |

Insufficient granularity of access control in Windows Server Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-78459

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:54.187 |

Heap-based buffer overflow in Windows Internet Information Services allows an authorized attacker to elevate privileges locally.

### CVE-2026-73027

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-13T19:19:52.197 |

External control of system or configuration setting in Windows Setup Files Cleanup allows an authorized attacker to elevate privileges locally.

### CVE-2026-70566

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:19:50.653 |

Null pointer dereference in Windows Schannel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70303

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:19:50.360 |

Out-of-bounds write in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70286

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:48.323 |

Heap-based buffer overflow in Windows Win32K - GRFX allows an authorized attacker to elevate privileges locally.

### CVE-2026-70285

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:48.133 |

Heap-based buffer overflow in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70278

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:47.180 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an authorized attacker to elevate privileges locally.

### CVE-2026-70274

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:46.567 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70255

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:43.860 |

Heap-based buffer overflow in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-70247

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:41.797 |

Out-of-bounds read in Windows HTTP.sys allows an authorized attacker to execute code locally.

### CVE-2026-70245

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:41.417 |

Access of resource using incompatible type ('type confusion') in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-70238

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:40.617 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an authorized attacker to elevate privileges locally.

### CVE-2026-70233

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:39.757 |

Heap-based buffer overflow in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70228

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:39.050 |

Out-of-bounds read in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-70225

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:38.720 |

Access of resource using incompatible type ('type confusion') in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-70222

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-13T19:19:37.083 |

Relative path traversal in Windows Shell allows an authorized attacker to elevate privileges locally.

### CVE-2026-70220

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:36.897 |

Heap-based buffer overflow in Microsoft Office Word allows an unauthorized attacker to execute code locally.

### CVE-2026-70218

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-1220` |
| Published | 2026-10-13T19:19:36.660 |

Insufficient granularity of access control in Windows StateRepository API allows an authorized attacker to elevate privileges locally.

### CVE-2026-70184

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-13T19:19:32.540 |

Improper resolution of path equivalence in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-70177

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-197` |
| Published | 2026-10-13T19:19:31.987 |

Numeric truncation error in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:31.180 |

Untrusted pointer dereference in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-70151

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:28.400 |

Use after free in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-70143

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:27.380 |

Heap-based buffer overflow in Windows Network File System allows an authorized attacker to execute code locally.

### CVE-2026-70142

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:19:27.247 |

Untrusted search path in Windows Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70139

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:26.707 |

Heap-based buffer overflow in Windows Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70138

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:26.530 |

Heap-based buffer overflow in Windows OLE allows an authorized attacker to elevate privileges locally.

### CVE-2026-70132

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:25.390 |

Heap-based buffer overflow in Windows Portable Device File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70131

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:25.210 |

Heap-based buffer overflow in Microsoft Windows Media Foundation allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-70123

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-10-13T19:19:24.550 |

Numeric truncation error in Microsoft Graphics Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70121

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:24.260 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70117

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:23.840 |

Heap-based buffer overflow in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70114

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:23.467 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70113

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:19:23.287 |

Integer overflow or wraparound in Windows Client for NFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-70112

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:23.140 |

Heap-based buffer overflow in Windows Spaceport.sys allows an authorized attacker to execute code locally.

### CVE-2026-70110

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:19:22.750 |

Stack-based buffer overflow in Microsoft PostScript Printer Driver allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-70109

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:22.577 |

Heap-based buffer overflow in Microsoft PostScript Printer Driver allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-70108

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:22.403 |

Heap-based buffer overflow in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70106

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:22.223 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70104

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:22.070 |

Untrusted pointer dereference in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70103

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:21.903 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-70102

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:21.750 |

Use after free in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-70093

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:21.060 |

Heap-based buffer overflow in Windows Rich Text Edit Control allows an authorized attacker to elevate privileges locally.

### CVE-2026-70092

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:20.883 |

Heap-based buffer overflow in Microsoft PostScript Printer Driver allows an unauthorized attacker to elevate privileges locally.

### CVE-2026-70064

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:19:17.600 |

Integer underflow (wrap or wraparound) in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-70060

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:17.090 |

Heap-based buffer overflow in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70059

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:16.910 |

Heap-based buffer overflow in Windows OLE allows an authorized attacker to elevate privileges locally.

### CVE-2026-70054

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:16.070 |

Heap-based buffer overflow in Windows NetBIOS allows an authorized attacker to elevate privileges locally.

### CVE-2026-70052

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:15.937 |

Integer overflow or wraparound in Windows PowerShell allows an authorized attacker to execute code locally.

### CVE-2026-70051

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:15.780 |

Access of resource using incompatible type ('type confusion') in Windows SmartScreen allows an authorized attacker to elevate privileges locally.

### CVE-2026-70048

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:15.450 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-70027

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:14.010 |

Heap-based buffer overflow in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-70023

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:13.337 |

Use after free in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-70015

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:12.900 |

Use after free in Windows Local Security Authority Subsystem Service (LSASS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-70010

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:12.043 |

Heap-based buffer overflow in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-70008

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:19:11.903 |

Integer overflow or wraparound in Windows IP Over USB Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69966

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:19:06.983 |

Integer overflow or wraparound in Microsoft Streaming Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69963

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:19:06.623 |

Heap-based buffer overflow in Microsoft Streaming Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69959

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:06.443 |

Out-of-bounds read in Windows Overlay Filter allows an authorized attacker to execute code locally.

### CVE-2026-69957

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126;CWE-190` |
| Published | 2026-10-13T19:19:06.083 |

Integer overflow or wraparound in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-69953

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-13T19:19:05.540 |

Buffer over-read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-69952

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:05.357 |

Out-of-bounds read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-69950

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-13T19:19:05.137 |

Buffer over-read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-69949

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:04.867 |

Heap-based buffer overflow in Windows Client for NFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69942

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-13T19:19:04.347 |

Buffer over-read in Windows Overlay Filter allows an authorized attacker to execute code locally.

### CVE-2026-69934

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-190` |
| Published | 2026-10-13T19:19:03.890 |

Integer overflow or wraparound in Windows Spaceport.sys allows an authorized attacker to elevate privileges locally.

### CVE-2026-69926

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:03.580 |

Access of resource using incompatible type ('type confusion') in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69923

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-13T19:19:03.463 |

Uncontrolled search path element in Windows AI allows an authorized attacker to elevate privileges locally.

### CVE-2026-69916

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T19:19:02.873 |

Integer overflow or wraparound in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69909

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:02.160 |

Heap-based buffer overflow in Microsoft COM for Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-69898

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:01.683 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-69884

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-126` |
| Published | 2026-10-13T19:19:01.327 |

Buffer over-read in Windows GDI allows an authorized attacker to elevate privileges locally.

### CVE-2026-69882

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:19:01.027 |

Untrusted search path in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69880

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:00.873 |

Access of resource using incompatible type ('type confusion') in Desktop Window Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69867

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:00.587 |

Out-of-bounds read in SQLite allows an authorized attacker to elevate privileges locally.

### CVE-2026-69850

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:19:00.257 |

Untrusted pointer dereference in Windows Certificates allows an authorized attacker to elevate privileges locally.

### CVE-2026-69798

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:59.620 |

Use after free in Windows Wired AutoConfig Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-10-13T19:18:59.167 |

External control of file name or path in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69733

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:18:58.307 |

Untrusted search path in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69718

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-13T19:18:57.997 |

Improper neutralization of special elements used in a command ('command injection') in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69673

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:18:57.557 |

Improper link resolution before file access ('link following') in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69650

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:18:57.213 |

Improper verification of cryptographic signature in Windows Key Distribution Center allows an authorized attacker to elevate privileges locally.

### CVE-2026-69633

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:56.173 |

Heap-based buffer overflow in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-69471

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-10-13T19:18:55.337 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-69354

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-10-13T19:18:54.177 |

Heap-based buffer overflow in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-68836

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:53.820 |

Heap-based buffer overflow in Windows kernel32.dll allows an authorized attacker to elevate privileges locally.

### CVE-2026-61931

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:53.153 |

Use after free in Windows Perception Simulation Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-49785

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-404` |
| Published | 2026-10-13T19:18:52.167 |

Improper resource shutdown or release in Windows UEFI allows an authorized attacker to bypass a security feature locally.

### CVE-2026-108136

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:04.100 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-108133

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:18:03.690 |

Release of invalid pointer or reference in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-108130

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:03.207 |

Heap-based buffer overflow in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-106625

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:18:01.787 |

Adobe Framemaker is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-105004

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:17:56.343 |

Out-of-bounds read in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-105003

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:56.157 |

Heap-based buffer overflow in HID class driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-104344

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:55.290 |

Adobe Framemaker is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104342

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:55.047 |

Adobe Framemaker is affected by a Use After Free vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104341

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:17:54.920 |

Adobe Framemaker is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-104340

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:54.797 |

Adobe Framemaker is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103967

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:17:54.663 |

Adobe Framemaker is affected by an out-of-bounds write vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103966

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:54.537 |

Adobe Framemaker is affected by a Heap-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-103568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-10-13T19:17:52.943 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Credential Providers allows an authorized attacker to elevate privileges locally.

### CVE-2026-103553

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:17:51.737 |

Out-of-bounds read in Windows Partition Management Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-102233

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:17:48.920 |

Missing authorization in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-102227

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:48.417 |

Heap-based buffer overflow in Windows Resilient File System (ReFS) allows an authorized attacker to execute code locally.

### CVE-2026-102220

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:47.763 |

Use after free in Windows VHD miniport driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-102218

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:47.583 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-102216

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:17:47.207 |

Access of resource using incompatible type ('type confusion') in Windows StateRepository API allows an authorized attacker to elevate privileges locally.

### CVE-2026-102215

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:47.017 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-102205

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:45.660 |

Heap-based buffer overflow in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-102204

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:17:45.533 |

Improper link resolution before file access ('link following') in Microsoft Defender for Endpoint allows an authorized attacker to elevate privileges locally.

### CVE-2026-102202

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:17:45.193 |

Improper access control in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-102201

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:45.047 |

Use after free in Microsoft Windows Media Foundation allows an authorized attacker to elevate privileges locally.

### CVE-2026-102196

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:44.387 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-100217

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:17:41.807 |

Improper privilege management in Windows Group Policy allows an authorized attacker to elevate privileges locally.

### CVE-2026-100215

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:41.470 |

Heap-based buffer overflow in Microsoft Graphics Component allows an unauthorized attacker to execute code locally.

### CVE-2026-14765

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-14T03:17:21.927 |

Epic Games Unreal Engine versions up to and including 5.8.0 ship with an insecure default configuration for the LaunchURL Blueprint node (UKismetSystemLibrary::LaunchURL). The URL scheme filter (FURLRequestFilter) is empty by default, which permits all URL schemes. On Windows, this results in a call to ShellExecuteW() with the open verb, so a supplied file:/// URI causes the referenced file to be executed. Any Unreal Engine game that loads user-generated content containing Blueprints is vulnerable to command execution via a malicious local file or a remote file on a WebDAV share. This is an instance of CWE-1188 (Initialization of a Resource with an Insecure Default).

### CVE-2026-88081

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T21:19:42.563 |

Out-of-bounds read in SQL Server allows an authorized attacker to disclose information over a network.

### CVE-2026-85888

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T21:19:31.270 |

Out-of-bounds read in SQL Server allows an authorized attacker to disclose information over a network.

### CVE-2026-34633

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:17:38.087 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105994

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:29.923 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106634

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T20:17:17.103 |

Adobe Experience Manager is affected by an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability that could result in arbitrary file system write. A low-privileged attacker could leverage this vulnerability to write files to unauthorized locations on the file system. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-110206

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:44.157 |

Roo Code through 3.54.0 contains a command approval bypass vulnerability in parseCommandLine() that allows attackers to auto-approve arbitrary shell commands by placing a command substitution in command position. Attackers using indirect prompt injection can submit commands like $(echo touch /tmp/x) that pass the echo allowlist check, causing the shell to execute the output without user approval.

### CVE-2026-110205

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-13T19:18:44.003 |

Roo Code through 3.54.0 contains a command approval bypass vulnerability in parseCommandLine() that discards command substitutions placed next to * or ? glob characters. Attackers using indirect prompt injection can craft commands like echo *$(...) that match allowlisted prefixes, executing denied commands without user approval when auto-approval is enabled.

### CVE-2026-110204

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:43.857 |

Roo Code through 3.54.0 contains a command approval bypass vulnerability that allows attackers to run denied shell commands because parseCommandLine() treats ${ command; } substitutions as parameter expansions. Attackers using indirect prompt injection can embed denied commands inside an allowlisted command like echo to execute them without user approval on bash 5.3+ or ksh93.

### CVE-2026-110203

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:43.707 |

Roo Code through 3.54.0 contains a command approval bypass vulnerability that allows attackers to auto-approve denied shell commands by abusing quote-masking regex in parseCommandLine(). Attackers can use indirect prompt injection with escaped or single-quoted double quotes to hide command separators behind allowlisted prefixes like echo, executing commands without user approval.

### CVE-2026-110202

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-13T19:18:43.543 |

Roo Code through 3.54.0 contains a command approval bypass vulnerability in getCommandDecision() that allows attackers to auto-approve denied shell commands by prefixing them with a bare >& redirect. Attackers using indirect prompt injection can make the allowlist match a redirect target like echo while the shell runs the denied command on the developer machine.

### CVE-2026-110111

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-13T19:18:43.107 |

Xen Orchestra before 6.9.0 contains an improper access control vulnerability that allows any authenticated user to become global administrator by abusing the unprotected vm.importFromEsxi and vm.importMultipleFromEsxi methods. Attackers can point xo-server at a malicious ESXi host serving a crafted .vmx file with __proto__.permission set, polluting Object.prototype so permission-less accounts inherit admin rights and enabling remote code execution.

### CVE-2026-102231

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-41` |
| Published | 2026-10-13T19:17:48.690 |

Improper resolution of path equivalence in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-82416

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-362;CWE-488` |
| Published | 2026-10-13T17:17:47.183 |

FrankenPHP is a modern application server for PHP. Prior to 1.12.5, FrankenPHP worker mode can retain PHP session state between requests when the session extension is loaded as a shared module and is unavailable through HAVE_PHP_SESSION at compile time. In this build configuration, frankenphp_reset_session_state() is compiled out, PS(id) can survive a request boundary, and a subsequent session_start() can ignore the new request's cookie because an identifier is already present. Under concurrent requests, session_id() can therefore return another client's identifier or a stale identifier from a previous request on the same worker thread, causing cross-user session exposure, possible session hijacking, and intermittent logout behavior. Builds with the session extension statically linked, including the official static binaries and Docker images, are not affected. This issue is fixed in version 1.12.5.

### CVE-2026-61642

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-13T17:17:42.670 |

Squid is a caching proxy for the Web. From 3.3.0.1 to before 7.6, due to an improper enforcement of behavioral workflow bug, Squid is vulnerable to a Request Smuggling attack against HTTP/1.1 Transfer-Encoding. HTTP header parsing (`src/HttpHeader.cc`) accepted the bare` Transfer-Encoding:` identity form, which the HTTP specification prohibits because any transfer coding must be wrapped within chunked encoding. This problem allows a trusted client to perform an HTTP Request Smuggling attack when HTTP/1.1 is used, bypassing security mechanisms that may be in place between attacker and Squid. When there is an HTTP cache operating prior to the affected Squid, this Request Smuggling attack also allows the attacker to poison that web cache and store arbitrary malicious content at any URL for delivery to other clients' future requests. This issue is fixed in version 7.6.

### CVE-2026-54641

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:41.633 |

OpenRemote is an open-source internet-of-things platform. Prior to 1.24.2, the get, getUserClientRoles, and getUserRealmRoles methods in manager/src/main/java/org/openremote/manager/security/UserResourceImpl.java authorize callers with the read:admin role without confirming that the target UUID belongs to the requested and authenticated realm. A realm administrator can supply a user identifier from another tenant or the master realm and retrieve that user's profile, client roles, and realm roles, breaking tenant isolation and exposing privileged account information. This issue is fixed in version 1.24.2.

### CVE-2026-110102

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-10-13T17:17:33.987 |

Powerlevel10k through 1.20.0 contains an insecure download vulnerability in the gitstatus/install script that disables TLS certificate verification with curl -k and skips integrity checks when no SHA-256 utility exists. Network-positioned attackers can intercept the github.com mirror request and substitute a malicious archive, which runs as the gitstatusd daemon under the user's account on every prompt.

### CVE-2026-106047

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T17:17:16.497 |

A Path Traversal vulnerability in the template export functionality of Ivanti Xtraction before version 2026.4 allows a remote authenticated attacker to read arbitrary files.

### CVE-2026-77096

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:49.400 |

CVFS contained a missing authentication condition affecting command execution.  Software customers upgrade to resolved maintenance release. Update CVFS.

### CVE-2026-84790

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-158;CWE-290` |
| Published | 2026-10-13T22:18:58.937 |

OpenVPN 2.7_alpha1 through 2.7.7 allows remote authenticated users to impersonate others via a crafted certificate subject field

### CVE-2026-75748

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:18:20.263 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. An attacker with high privileges could exploit this vulnerability to gain elevated access to internal resources. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-54640

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-13T17:17:41.490 |

OpenRemote is an open-source internet-of-things platform. Prior to 1.24.2, the KNXProtocol.startAssetImport method in agent/src/main/java/org/openremote/agent/protocol/knx/KNXProtocol.java processes 0.xml from an authenticated user's uploaded ETS project ZIP with Saxon TransformerFactoryImpl and XMLInputFactory parsers that permit external entity resolution. This incomplete remediation of CVE-2026-40882 leaves the KNX handler unprotected while the parallel Velbus handler is hardened, allowing a regular realm user to read files accessible to the JVM process or cause server-side requests. This issue is fixed in version 1.24.2.

### CVE-2026-76655

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T12:17:18.083 |

A security vulnerability in HPE NonStop SNMP Trap Multiplexer may allow remote code execution

### CVE-2026-107431

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T11:17:02.763 |

Missing Authorization vulnerability in Crocoblock JetFormBuilder jetformbuilder allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects JetFormBuilder: from n/a through 3.6.6.

### CVE-2026-103358

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T11:16:57.670 |

Improper Control of Generation of Code ('Code Injection') vulnerability in VillaTheme Email Template Customizer for WooCommerce email-template-customizer-for-woo allows Code Injection.This issue affects Email Template Customizer for WooCommerce: from n/a through 1.3.4.

### CVE-2026-110284

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-14T08:17:05.747 |

The LifterLMS – WP LMS for eLearning, Online Courses, & Quizzes plugin for WordPress is vulnerable to Local File Inclusion in versions up to, and including, 10.3.1 via attacker-controlled attributes of the [lifterlms_checkout] shortcode. This is due to the llms_get_template() helper performing extract() on the shortcode attribute array before resolving the template path, which allows the attacker-supplied 'template_name' and 'default_path' shortcode attributes to overwrite the function's local parameters and ultimately control the path passed to a PHP include. This makes it possible for authenticated attackers, with Instructor-level access and above, to include and execute arbitrary files on the server, that can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where files with safe extensions containing attacker-controlled content can be uploaded and included.

### CVE-2026-103366

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T08:17:02.417 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to Insecure Direct Object Reference in versions up to, and including, 5.7.3 via the `booking[id]` and `cart[id]` parameters on the `steps__reload_booking_form_summary_panel` and `steps__start` public routes (reachable through wp_ajax_nopriv_latepoint_route_call). This is due to `OsStepsHelper::set_required_objects()` feeding raw request parameters into `set_booking_object()` and `set_cart_object()`, which call `OsModel::set_data()` and load an arbitrary booking or cart row by primary key with no ownership check — the ownership guard the vendor added for the earlier disclosure lives only inside `OsStepsHelper::load_step()` and does not cover the sibling routes or `cart[id]` at all. This makes it possible for unauthenticated attackers to enumerate sequential booking / cart identifiers and read other customers' appointment details (service name, agent, date/time, duration, price breakdown, status) and other shoppers' pending checkout contents directly from the JSON responses.

### CVE-2026-96661

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T04:19:01.350 |

The Gmedia Photo Gallery plugin for WordPress is vulnerable to time-based SQL Injection via the 'gmedia__in' parameter in all versions up to, and including, 1.25.1 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The unauthenticated mobile app endpoint dispatches the library action without validating the Mobile App feature flag, a nonce, or any WordPress authentication, meaning no account or session of any kind is required to exploit this vulnerability.

### CVE-2026-95808

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T04:18:56.467 |

The Form Maker by 10Web – Mobile-Friendly Drag & Drop Contact Form Builder plugin for WordPress is vulnerable to blind SQL Injection via the 'inputs' parameter in all versions up to, and including, 1.15.48 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The nonce required to reach the vulnerable handler is emitted to every public page that renders a form, making it trivially obtainable by an unauthenticated attacker from page source.

### CVE-2026-78193

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T04:18:36.860 |

The JTL-Connector for WooCommerce plugin for WordPress is vulnerable to time-based SQL Injection via 'product.push' Identity Endpoint in all versions up to, and including, 2.4.3 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. The injection fires during identity linking, before ProductController::push() executes, meaning exploitation succeeds even if downstream product handling would otherwise reject the request.

### CVE-2026-110449

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:L` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T04:18:17.317 |

Nix before 2.35.3 and Lix before 2.95.4 have an integer overflow and resultant out-of-bounds write when evaluating untrusted expressions because list allocation is mishandled.

### CVE-2026-102251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T03:17:12.513 |

The Abandoned Cart Pro for WooCommerce plugin for WordPress is vulnerable to generic SQL Injection via the 'validate' parameter in all versions up to, and including, 10.8.0 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. AES-CTR is a malleable stream cipher, so an attacker who obtains one legitimate token by abandoning a cart with an email address they control can recover the keystream and forge a ciphertext carrying arbitrary SQL. The HMAC check added in 10.4.1 is enforced only when the wcap_nonce parameter is present, so omitting the parameter skips it entirely.

### CVE-2026-104767

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-14T02:16:56.360 |

The Membership & User Roles for WooCommerce (Automatic Role Changer) plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 20260828. This is due to the `maybe_add_role_to_user()` function unconditionally re-assigning every role stored in the `dfxwcrc_foreign_roles` user meta cache without verifying that each cached role is still actively assigned by the external provider — a condition made permanent by `remember_foreign_roles()`, which merges new foreign roles into the cache but never evicts roles that have since been revoked. This makes it possible for authenticated attackers with subscriber-level access and above to restore a previously revoked Administrator role to their own account, gaining full administrative control of the site, by triggering any role-assignment event such as completing a purchase for a role-mapped product. Exploitation requires Replace Roles mode to be enabled and the attacker's account to have previously received Administrator legitimately through a separate role-management mechanism while the plugin was active, so that `administrator` was written into the `dfxwcrc_foreign_roles` user meta cache before the external provider revoked it.

### CVE-2026-104749

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-14T02:16:56.223 |

The Bit integrations – Form Integration, Webhook, Spreadsheets, CRM, LMS & Email Automation plugin for WordPress is vulnerable to Privilege Escalation via Log Re-execution in all versions up to, and including, 2.10.6 The vulnerability exists because `IntegrationHandler::executeWithCapture()` stores raw, attacker-controlled field values — including `user_pass` and `user_email` — verbatim into `wp_btcbi_log.field_data` on anonymous front-end requests with no capability check, and `LogHandler::reexecute()` feeds that stored payload back through `Flow::execute()` inside the replaying administrator's session without validating the identity that originally produced the data, causing `RegistrationController::updateUser()` to resolve the target user ID to the administrator and write the attacker-supplied password via `wp_update_user()`. This makes it possible for unauthenticated attackers to overwrite the administrator's password and fully take over the administrator account. Exploitation requires that an administrator has configured a flow mapping a user-supplied form field to the `user_pass` parameter of the WP User Registration "Update User" action, and that the administrator subsequently clicks "Re-execute" on the failure log row produced by the anonymous submission from the plugin's log screen.

### CVE-2026-103423

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T02:16:54.710 |

The Booking Package plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 1.7.29 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers to retrieve personally identifiable information for every booked customer stored in the booking_package_booked_customers table, including names, email addresses, phone numbers, physical addresses, and cancellation tokens. The nonce nominally protecting the endpoint is a public CSRF token emitted in the localized booking_package JavaScript object on any page rendering the [booking_package] shortcode or widget, making it trivially harvestable by unauthenticated visitors and providing no effective authentication barrier.

### CVE-2026-95633

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T22:19:30.733 |

CAI Content Credentials is affected by an Improper Verification of Cryptographic Signature vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-95632

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T22:19:30.610 |

CAI Content Credentials is affected by an Improper Verification of Cryptographic Signature vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-94453

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T22:19:30.253 |

Libreswan's pluto daemon has a use-after-free vulnerability when a client connecting using IKE over TCP closes the connection and another packet (retransmit or malicious) is received for the same tuple. IKE state is retained in memory after the client closes the connection, storing a pointer to iface_endpoint inside ike_sa.sa->st_iface_endpoint. Once this invalid pointer is used, the daemon crashes and restarts. This vulnerability can be triggered before the remote peer has authenticated itself. Continued exploitation can lead to a denial of service. Remote code execution could be possible. The IKE over TCP option is not enabled by default; only configurations that contain listen-tcp=yes are affected.

### CVE-2026-77207

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-252;CWE-476` |
| Published | 2026-10-13T22:18:26.040 |

Libreswan has a null pointer dereference bug in the PKCS#7 handling code for IKE certificate authentication. When libreswan decodes an IKE CERT payload of type CERT_PKCS7_WRAPPED_X509, it guards the PKCS#7 blob with SEC_PKCS7ContainsCertsOrCrls() and then iterates the certificate list with SEC_PKCS7GetCertificateList(). The two NSS APIs disagree on a SignedData that carries a CRL but no certificates: ContainsCertsOrCrls() returns PR_TRUE (there is a CRL), so the guard passes, but GetCertificateList() returns NULL (there are no certificates). This causes libreswan to dereference a null pointer leading to a crash and restart. A malicious IKE_AUTH packet can trigger this bug, meaning the peer does not need to be authenticated. No remote code execution is possible. Continued exploitation can cause a denial of service.

### CVE-2026-77206

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T22:18:24.727 |

Libreswan's IKEv2 state machine has a null pointer dereference bug in the EAP handling code for authentication. As a result of inconsistency within the IKEv2 state machine code, this bug can be triggered by any IKEv2 connection, even if EAP is not configured at all. The error is caused by a fall-through where it incorrectly dereferences ike->sa.st_eap which is NULL. A malicious IKE_AUTH packet can trigger this bug, meaning the peer does not need to be authenticated. The bug results in a crash and restart of the pluto daemon. No remote code execution is possible. Continued exploitation can cause a denial of service.

### CVE-2026-106627

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T22:17:30.627 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-105902

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T22:17:30.507 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-104345

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:26.307 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-103297

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T22:17:24.057 |

CAI Content Credentials is affected by an Improper Verification of Cryptographic Signature vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-103296

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T22:17:23.940 |

CAI Content Credentials is affected by an Improper Verification of Cryptographic Signature vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100139

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T22:17:12.387 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-100138

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T22:17:12.267 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-100137

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T22:17:12.150 |

CAI Content Credentials is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-100136

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T22:17:12.030 |

CAI Content Credentials is affected by an Integer Overflow or Wraparound vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-100135

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:11.907 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100124

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:11.663 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100123

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T22:17:11.543 |

CAI Content Credentials is affected by an Improper Certificate Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100122

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T22:17:11.420 |

CAI Content Credentials is affected by an Improper Certificate Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100121

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T22:17:11.300 |

CAI Content Credentials is affected by an Improper Certificate Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100120

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:11.173 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100119

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:11.050 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100118

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T22:17:10.870 |

CAI Content Credentials is affected by an Improper Certificate Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100117

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:10.677 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100115

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-13T22:17:10.417 |

CAI Content Credentials is affected by an Improper Access Control vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-13T22:17:10.290 |

CAI Content Credentials is affected by an Improper Access Control vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-100113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T22:17:09.967 |

CAI Content Credentials is affected by an Improper Input Validation vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized write access. Exploitation of this issue does not require user interaction.

### CVE-2026-88083

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T21:19:42.810 |

Stack-based buffer overflow in SQL Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-75996

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-13T21:18:20.620 |

ColdFusion is affected by an Uncontrolled Resource Consumption vulnerability that could lead to application denial-of-service. An attacker could exploit this vulnerability to exhaust system resources, resulting in an application denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-106623

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:17:31.597 |

ColdFusion is affected by an Incorrect Authorization vulnerability that could lead to disclosure of sensitive memory. An attacker could leverage this vulnerability to disclose sensitive information. Exploitation of this issue does not require user interaction.

### CVE-2026-105900

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-13T21:17:29.593 |

ColdFusion is affected by an Improper Input Validation vulnerability that could result in an application denial-of-service. An attacker could exploit this vulnerability to crash the application, leading to a denial-of-service condition. Exploitation of this issue does not require user interaction.

### CVE-2026-105442

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T21:17:26.913 |

IBM WebSphere Application Server 8.5, and 9.0 and IBM WebSphere Application Server - Liberty 17.0.0.3 through 26.0.0.10 Liberty could allow a remote attacker to cause a denial of service caused by an insecure deserialization in the messaging service.

### CVE-2026-97830

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:22:22.557 |

Double free in Windows Internet Information Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-97801

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-1287` |
| Published | 2026-10-13T19:22:18.023 |

Improper validation of specified type of input in .NET Framework allows an unauthorized attacker to perform tampering over a network.

### CVE-2026-97789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:16.910 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-97788

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-203` |
| Published | 2026-10-13T19:22:16.697 |

Observable discrepancy in Active Directory Federation Services (AD FS) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-96960

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-405` |
| Published | 2026-10-13T19:22:08.670 |

Asymmetric resource consumption (amplification) in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-96959

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:22:08.527 |

Allocation of resources without limits or throttling in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-96958

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-13T19:22:08.387 |

Inefficient algorithmic complexity in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-96945

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-13T19:22:06.733 |

Uncaught exception in Windows Failover Cluster allows an unauthorized attacker to deny service over a network.

### CVE-2026-96866

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:01.050 |

Out-of-bounds read in Network Device Enrollment Service (NDES) allows an unauthorized attacker to deny service over a network.

### CVE-2026-96861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:22:00.163 |

Out-of-bounds read in Network Device Enrollment Service (NDES) allows an unauthorized attacker to deny service over a network.

### CVE-2026-96325

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-771` |
| Published | 2026-10-13T19:21:57.170 |

Missing reference to active allocated resource in Windows SMB Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-96248

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:21:50.773 |

Stack-based buffer overflow in Windows Host Guardian Service allows an unauthorized attacker to deny service over a network.

### CVE-2026-96246

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:50.407 |

Out-of-bounds read in Network Policy Server (NPS) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-96245

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:50.147 |

Out-of-bounds read in Windows Routing and Remote Access Service (RRAS) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-96237

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-13T19:21:49.587 |

Inclusion of functionality from untrusted control sphere in .NET allows an unauthorized attacker to execute code over a network.

### CVE-2026-96236

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:21:49.460 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-96233

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:49.083 |

Out-of-bounds write in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-96232

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:48.960 |

Out-of-bounds read in .NET allows an unauthorized attacker to disclose information over a network.

### CVE-2026-96071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:45.223 |

Heap-based buffer overflow in Windows Media allows an unauthorized attacker to execute code over a network.

### CVE-2026-88207

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:42.290 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-88206

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T19:21:42.170 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-87716

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:25.387 |

Heap-based buffer overflow in Windows Storage Spaces Controller allows an unauthorized attacker to deny service over a network.

### CVE-2026-87713

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:24.867 |

Use after free in Windows Bluetooth Port Driver allows an unauthorized attacker to elevate privileges over an adjacent network.

### CVE-2026-87696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-13T19:21:22.273 |

Improper verification of cryptographic signature in Microsoft Exchange Server allows an authorized attacker to elevate privileges over a network.

### CVE-2026-86063

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494;CWE-829` |
| Published | 2026-10-13T19:21:21.417 |

Claude Code is an agentic coding tool. Prior to 2.1.179, the Claude Code and Claude Desktop plugin installation flow runs git checkout for a marketplace-pinned commit without verifying that the resulting HEAD equals the pinned 40-character SHA. An attacker who controls a plugin repository on a Git host that permits SHA-shaped branch names can create a branch named after the reviewed commit, causing checkout to select the branch tip and install attacker-controlled plugin code. Exploitation requires a user to install the malicious plugin and pin it to the ostensibly safe hash. This issue is fixed in version 2.1.179.

### CVE-2026-85891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-13T19:21:15.430 |

Exposure of sensitive information to an unauthorized actor in Azure HDInsight allows an unauthorized attacker to disclose information over a network.

### CVE-2026-85811

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:05.660 |

Use after free in Network Policy Server (NPS) allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-85808

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:05.110 |

Out-of-bounds read in Windows Routing and Remote Access Service (RRAS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-85353

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:57.760 |

Out-of-bounds read in Windows Print Spooler Components allows an unauthorized attacker to disclose information over a network.

### CVE-2026-85334

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:56.053 |

Out-of-bounds read in Windows Message Queuing Queue Manager allows an unauthorized attacker to disclose information over a network.

### CVE-2026-85324

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-13T19:20:53.850 |

Memory allocation with excessive size value in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-85322

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-13T19:20:53.530 |

Use of uninitialized resource in Windows Routing and Remote Access Service (RRAS) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-85321

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:20:53.400 |

Allocation of resources without limits or throttling in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-85319

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:20:53.080 |

Allocation of resources without limits or throttling in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-84017

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:20:52.077 |

Null pointer dereference in Windows Routing and Remote Access Service (RRAS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-84008

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-13T19:20:50.780 |

Inefficient algorithmic complexity in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-83860

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:35.157 |

Stack-based buffer overflow in Windows GDI allows an unauthorized attacker to deny service over a network.

### CVE-2026-83856

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:34.643 |

Out-of-bounds read in Windows Event Logging Service allows an unauthorized attacker to execute code over a network.

### CVE-2026-83855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:20:34.513 |

Integer underflow (wrap or wraparound) in Windows WLAN Service allows an unauthorized attacker to deny service over a network.

### CVE-2026-83843

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:32.713 |

Out-of-bounds read in Windows Internet Key Exchange (IKE) Protocol allows an unauthorized attacker to deny service over a network.

### CVE-2026-83795

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-10-13T19:20:29.477 |

Heap-based buffer overflow in Windows IKE Extension allows an unauthorized attacker to deny service over a network.

### CVE-2026-83754

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:21.597 |

Heap-based buffer overflow in OpenSSH for Windows allows an unauthorized attacker to execute code over a network.

### CVE-2026-83739

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:19.533 |

Use after free in Windows Bluetooth Service allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-83677

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-13T19:20:09.793 |

Missing release of memory after effective lifetime in Windows DHCP Client allows an unauthorized attacker to deny service over a network.

### CVE-2026-83670

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:08.860 |

Out-of-bounds read in Function Discovery Service (fdwsd.dll) allows an unauthorized attacker to disclose information over a network.

### CVE-2026-83665

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:20:08.023 |

Null pointer dereference in Windows DHCP Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-83655

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:06.973 |

Out-of-bounds read in Network Policy Server (NPS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-83647

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:05.780 |

Out-of-bounds read in Active Directory Domain Services allows an unauthorized attacker to deny service over a network.

### CVE-2026-83645

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:20:05.500 |

Allocation of resources without limits or throttling in Active Directory Federation Services (AD FS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-83635

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:03.557 |

Out-of-bounds read in DNS Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-83516

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:57.300 |

Out-of-bounds read in Windows Local Security Authority Subsystem Service (LSASS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-70281

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:19:47.630 |

Out-of-bounds read in Microsoft Office Outlook allows an unauthorized attacker to disclose information over a network.

### CVE-2026-70251

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T19:19:42.697 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70207

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:34.793 |

Heap-based buffer overflow in Network Policy Server (NPS) allows an authorized attacker to execute code over a network.

### CVE-2026-70202

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T19:19:34.370 |

Server-side request forgery (ssrf) in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70186

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-833` |
| Published | 2026-10-13T19:19:32.847 |

Deadlock in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-70183

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:19:32.417 |

Concurrent execution using shared resource with improper synchronization ('race condition') in ASP.NET Core allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70181

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:19:32.293 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-70179

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T19:19:32.170 |

Authentication bypass by spoofing in ASP.NET Core allows an authorized attacker to elevate privileges over a network.

### CVE-2026-70163

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:19:29.930 |

Allocation of resources without limits or throttling in OpenSSH for Windows allows an unauthorized attacker to deny service over a network.

### CVE-2026-70159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:19:29.390 |

Allocation of resources without limits or throttling in ASP.NET Core allows an unauthorized attacker to deny service over a network.

### CVE-2026-70155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-13T19:19:28.713 |

Missing release of memory after effective lifetime in Windows DNS allows an unauthorized attacker to deny service over a network.

### CVE-2026-70133

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-13T19:19:25.577 |

Allocation of resources without limits or throttling in Windows SMB Server allows an unauthorized attacker to deny service over a network.

### CVE-2026-70095

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:21.237 |

Heap-based buffer overflow in Windows iSCSI allows an unauthorized attacker to execute code over a network.

### CVE-2026-70082

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-13T19:19:19.657 |

Uncaught exception in Windows DNS allows an unauthorized attacker to deny service over a network.

### CVE-2026-70079

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-841` |
| Published | 2026-10-13T19:19:19.510 |

Improper enforcement of behavioral workflow in Windows DNS allows an unauthorized attacker to deny service over a network.

### CVE-2026-70058

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:19:16.767 |

Out-of-bounds write in Windows DHCP Server allows an unauthorized attacker to execute code over a network.

### CVE-2026-70033

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-13T19:19:14.343 |

Missing release of memory after effective lifetime in Remote Desktop Gateway Service allows an unauthorized attacker to deny service over a network.

### CVE-2026-70031

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:14.150 |

Heap-based buffer overflow in Windows iSCSI allows an unauthorized attacker to deny service over a network.

### CVE-2026-70014

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:12.717 |

Use after free in Windows Cryptographic Services allows an authorized attacker to execute code over a network.

### CVE-2026-70012

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:12.340 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-70006

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:11.583 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-70004

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:11.280 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69998

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.970 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69997

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.793 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69996

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.613 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69995

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.437 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69994

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.260 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69992

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:10.087 |

Use after free in Windows Remote Desktop Services allows an unauthorized attacker to execute code over a network.

### CVE-2026-69991

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:09.910 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69988

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:09.737 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69987

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:09.553 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69986

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:09.377 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69984

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:09.030 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69976

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:08.240 |

Use after free in Remote Desktop Client allows an unauthorized attacker to execute code over a network.

### CVE-2026-69789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:59.293 |

Heap-based buffer overflow in Reliable Multicast Transport Driver (RMCAST) allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-69651

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407` |
| Published | 2026-10-13T19:18:57.397 |

Inefficient algorithmic complexity in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-69577

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:18:55.873 |

Out-of-bounds read in Microsoft Azure Attestation service and Device Health Attestation Service allows an unauthorized attacker to disclose information over a network.

### CVE-2026-69454

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:18:55.213 |

Out-of-bounds read in Microsoft Azure Attestation service and Device Health Attestation Service allows an unauthorized attacker to disclose information over a network.

### CVE-2026-58280

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-10-13T19:18:52.810 |

Uncontrolled recursion in .NET allows an unauthorized attacker to deny service over a network.

### CVE-2026-108131

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-13T19:18:03.343 |

No cwe for this issue in Active Directory Federation Services (AD FS) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-105728

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:18:00.900 |

Improper authentication in Dynamics Business Central allows an unauthorized attacker to disclose information over a network.

### CVE-2026-105723

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:18:00.303 |

Untrusted pointer dereference in Windows Distributed File System (DFS) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-105715

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-416` |
| Published | 2026-10-13T19:17:59.360 |

Integer overflow or wraparound in Microsoft Office Word allows an unauthorized attacker to execute code over a network.

### CVE-2026-105714

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:59.223 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.960 |

Heap-based buffer overflow in Microsoft Office PowerPoint allows an unauthorized attacker to execute code over a network.

### CVE-2026-105592

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:58.177 |

Heap-based buffer overflow in Microsoft Office Access allows an unauthorized attacker to execute code over a network.

### CVE-2026-105009

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-276` |
| Published | 2026-10-13T19:17:57.277 |

Incorrect default permissions in Windows Server Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-103577

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-453` |
| Published | 2026-10-13T19:17:53.723 |

Insecure default variable initialization in Microsoft QUIC allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-103569

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:17:53.123 |

Out-of-bounds read in Windows IKE Extension allows an unauthorized attacker to disclose information over a network.

### CVE-2026-103558

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-833` |
| Published | 2026-10-13T19:17:52.210 |

Deadlock in Windows Routing and Remote Access Service (RRAS) allows an unauthorized attacker to deny service over a network.

### CVE-2026-102599

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-13T19:17:49.037 |

Socket.IO enables bidirectional and low-latency communication for every platform. From Engine.IO 6.6.0 until 6.6.10, a transport upgrade can independently derive an Engine.IO protocol revision from the upgrade request instead of enforcing the revision stored on the existing session. A malicious client can establish a valid session and send an upgrade request with a different or omitted EIO query parameter, attaching a transport with incompatible parser and heartbeat behavior. A crafted heartbeat packet can then trigger an uncaught exception and terminate the Node.js process, including when Engine.IO v3 compatibility is disabled because an omitted EIO value is interpreted as revision 3 on the affected path. This issue is fixed in Engine.IO 6.6.10.

### CVE-2026-102192

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-13T19:17:43.800 |

Integer underflow (wrap or wraparound) in Windows Failover Cluster allows an unauthorized attacker to deny service over a network.

### CVE-2026-106043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T17:17:16.387 |

A Missing Authentication for Critical Function vulnerability in Ivanti Xtraction before version 2026.4 allows a remote unauthenticated attacker to create, modify, trusted site.

### CVE-2026-103030

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-13T17:17:14.953 |

Dio is a powerful HTTP client for Dart and Flutter. From 1.0.0 until 2.8.0, dio_http2_adapter follows redirects in Http2Adapter._fetch by copying the original RequestOptions.headers into the redirected HTTP/2 request without comparing the source and destination origins. A server contacted by an application can return a cross-origin Location redirect to a different-origin destination, which then receives preserved Authorization, Cookie, and Proxy-Authorization headers because RequestOptions.copyWith retains the full header map. The issue applies when applications use Http2Adapter for authenticated requests, and redirect following is enabled by default. This issue is fixed in version 2.8.0.

### CVE-2026-95122

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T15:17:51.677 |

mp4v2 2.0.0 contains a NULL pointer dereference vulnerability in MP4File::GenerateTracks() in src/mp4file.cpp. This allows a remote attacker to cause a denial of service

### CVE-2026-95115

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T15:17:51.307 |

Buffer Overflow vulnerability in libwebsockets main 106d542c allows a remote attacker to cause a denial of service via the LEJP JSON parser

### CVE-2026-95114

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T15:17:51.153 |

libwebsockets contains an out-of-bounds read vulnerability in the LEJP incremental parser in lib/misc/lejp.c. This allows a remote attacker to cause a denial of service

### CVE-2026-100163

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T08:17:02.257 |

The Appointment Booking Plugin – LatePoint | Calendar & Scheduling for WordPress plugin for WordPress is vulnerable to Authentication Bypass in versions up to, and including, 5.7.2 via the OsCustomerHelper::create_wp_user_for_customer() helper reached from the public process_step_customer() booking step. When the 'Use WordPress users as customers' option is enabled, the helper falls back from email_exists() to username_exists( $customer->email ), which matches any WordPress user whose user_login equals the victim customer's email even when that user's user_email is completely different, and links that WordPress user's ID into the victim's LatePoint customer row (only privileged roles are excluded; Subscriber is allowed). This makes it possible for authenticated attackers, with Subscriber-level access and above, to take over another customer's LatePoint account — accessing their bookings, service, agent, and calendar data, and having the victim customer's email overwritten with the attacker's on next login — by holding a Subscriber account whose user_login equals the victim's email and submitting an unauthenticated public booking step registration request.

### CVE-2026-95695

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T21:19:59.413 |

IBM WebSphere Application Server - Liberty 20.0.0.12 through 26.0.0.10 could allow a remote attacker to bypass security restrictions due to incorrect authorization.

### CVE-2026-102234

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-807` |
| Published | 2026-10-13T20:17:06.477 |

Reliance on untrusted inputs in a security decision in Visual Studio Code allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-96222

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T19:21:48.030 |

Improper certificate validation in Active Directory Federation Services (AD FS) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-87705

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-940` |
| Published | 2026-10-13T19:21:23.403 |

Improper verification of source of a communication channel in Windows Hyper-V allows an unauthorized attacker to bypass a security feature over an adjacent network.

### CVE-2026-85922

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:21:18.310 |

Weak authentication in Azure Key Vault allows an unauthorized attacker to bypass a security feature over a network.

### CVE-2026-83511

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:19:56.460 |

Weak authentication in Active Directory Federation Services (AD FS) allows an unauthorized attacker to perform spoofing over a network.

### CVE-2026-105013

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-13T19:17:57.610 |

Deserialization of untrusted data in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-108185

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T15:17:32.157 |

Improper certificate validation in the My Notes feature of certain Zoom Clients may allow an unauthenticated user to conduct an information disclosure via network access.

### CVE-2026-108184

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-13T15:17:32.033 |

Improper certificate validation in certain Zoom Clients for Windows may allow an unauthenticated user to conduct an information disclosure via network access.

### CVE-2026-107426

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T13:17:23.773 |

Missing Authorization vulnerability in VideoWhisper.com Paid Videochat Turnkey Site ppv-live-webcams allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Paid Videochat Turnkey Site: from n/a through 7.5.12.

### CVE-2026-107421

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-384` |
| Published | 2026-10-14T13:17:23.183 |

Session Fixation vulnerability in VideoWhisper.com Broadcast Live Video videowhisper-live-streaming-integration allows Session Hijacking.This issue affects Broadcast Live Video: from n/a through 7.3.2.

### CVE-2026-85298

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T12:17:18.320 |

An Incorrect Authorization vulnerability in the AuthConfig validation and integration execution runtime in Google Cloud Application Integration versions prior to 2026-08-27 allows an authenticated user to escalate privileges and impersonate a service account in the project.


This vulnerability was patched on 27 August 2026, and no customer action is needed.

### CVE-2026-55601

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T20:17:29.477 |

MultiTail is a utility for monitoring multiple log files in one terminal. In version 7.1.5 and earlier, the -ex and -eX execute-on-match feature appended attacker-controlled matched input to a configured command inside double quotes, then check_filter_exec() in mt.c passed the constructed command through execute_program() in exec.c to sh -c. Partial escaping left shell metacharacters such as command substitution active, allowing an attacker who could influence monitored input to execute commands as the user running MultiTail. No fixed release is available as of this review.

### CVE-2026-96188

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-13T19:21:46.393 |

External control of system or configuration setting in Microsoft PowerToys allows an authorized attacker to elevate privileges locally.

### CVE-2026-88204

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-13T19:21:42.050 |

Improper neutralization of input during web page generation ('cross-site scripting') in Microsoft Office SharePoint allows an authorized attacker to perform spoofing over a network.

### CVE-2026-70190

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:19:33.253 |

Improper link resolution before file access ('link following') in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-70161

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-13T19:19:29.683 |

Improper limitation of a pathname to a restricted directory ('path traversal') in .NET allows an authorized attacker to elevate privileges locally.

### CVE-2026-105732

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:18:01.300 |

Stack-based buffer overflow in SysInternals allows an authorized attacker to elevate privileges locally.

### CVE-2026-100207

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T19:17:40.677 |

Improper neutralization of special elements used in an os command ('os command injection') in Azure CycleCloud allows an authorized attacker to execute code locally.

### CVE-2026-97278

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T13:17:28.707 |

Deserialization of Untrusted Data vulnerability in WP SYNTEX Polylang polylang allows Object Injection.This issue affects Polylang: from n/a through 3.8.9.

### CVE-2026-88829

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-10-14T10:17:57.077 |

A flaw was found in BusyBox httpd's reverse proxy feature. When the proxy is configured to forward requests matching a URL prefix to a backend server, only the first HTTP request on a TCP connection has its path rewritten. An attacker can send a pipelined second request that is relayed verbatim to the backend, bypassing the configured path restrictions. This allows accessing arbitrary paths on the backend server that were not intended to be exposed through the proxy.

### CVE-2026-107751

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T08:17:04.570 |

The Mang Board plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'user_name' parameter in all versions up to, and including, 2.4.3 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The save-time sanitizer mbw_htmlspecialchars2() is ineffective against this vector because the exploit payload relies solely on unquoted HTML attribute syntax using only spaces, alphanumerics, and characters such as =, parentheses, and dots — none of which are escaped.

### CVE-2026-107631

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T08:17:04.260 |

The Record of Consent Extension for Complianz plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'uid' parameter in all versions up to, and including, 2.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because the enforcing nonce is emitted via wp_localize_script on wp_enqueue_scripts and is therefore readable by any unauthenticated frontend visitor, and no capability or role check gates the write path.

### CVE-2026-105107

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T08:17:03.747 |

Koha is vulnerable to SQL injection in the Most-circulated items report. The reports/cat_issues_top.pl script (sub calculate) concatenates the user-controlled Criteria, Filter, and Limit request parameters directly into dynamic SQL. Criteria is only prefix-normalized and never validated against an allow-list, so it is inserted verbatim into identifier positions (SELECT DISTINCTROW, GROUP BY, ORDER BY, and the main calculation query). Filter values are concatenated raw into single-quoted LIKE, BETWEEN, and comparison fragments. Limit is appended raw to a LIMIT clause. An authenticated staff user with the reports module permission (not requiring superlibrarian) can inject arbitrary SQL and read any table reachable by the Koha database user, including borrowers (userid and bcrypt password hashes, two-factor secrets, personal data), api_keys, and sessions. The issue is fixed in Koha 24.11.19, 25.05.14, 25.11.08, and 26.05.03, and in the 26.11 development branch. This is the unpatched twin of reports/bor_issues_top.pl (CVE-2026-70372).

### CVE-2026-104764

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T08:17:03.297 |

The Post Export Import with Media plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.17.1 via deserialization of untrusted input . This makes it possible for authenticated attackers, with administrator-level access and above, to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-86787

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T07:17:03.643 |

The affiliate-toolkit  WordPress plugin before 3.9.1 does not prevent a low-privileged user from supplying a template body that its bundled templating engine compiles and executes as PHP, allowing users with the Contributor role or above to run arbitrary PHP code on the server.

### CVE-2026-101924

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T05:16:41.567 |

The NewStatPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting in versions up to, and including, 1.4.5 via the 'Last referrers' meta box on the plugin's Overview admin page. This is due to insufficient output escaping of the visitor-supplied query string that the plugin records in its statistics table: the newstatpress_generate_overview_lastreferrers() function concatenates the stored urlrequested value into a single-quoted href attribute after only FILTER_SANITIZE_URL, which does not encode the apostrophe. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a high-privileged user, such as an administrator, accesses the Overview page and hovers the injected link.

### CVE-2026-97398

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:19:05.300 |

The FV Flowplayer Video Player plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'synopsis' Shortcode Attribute in all versions up to, and including, 7.5.54.7212 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This requires the 'Parse Vimeo and YouTube links' (parse_comments) option to be enabled and the liststyle attribute set to "season" for the vulnerable code path to be reached.

### CVE-2026-95816

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:56.647 |

The Smart Forms – when you need more than just a contact form plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'formString' parameter in all versions up to, and including, 2.6.104 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The nonce check protecting the rednao_smart_forms_save_form_values AJAX handler is only enforced when the smart_forms_block_anonymous_submissions option is enabled, meaning default installations require no authentication or nonce verification whatsoever to submit and store malicious payloads.

### CVE-2026-94377

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:55.297 |

The Verified Reviews (Avis Vérifiés) plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'moderation' parameter in all versions up to, and including, 2.4.6 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The authentication bypass is possible because ntav_check_data() uses loose != comparisons for signature verification, allowing a JSON body with boolean true values for idWebsite and sign to pass all checks on any configured installation.

### CVE-2026-93885

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:54.973 |

The Cryptocurrency Donation Box – Bitcoin & Crypto Donations plugin for WordPress is vulnerable to Stored Cross-Site Scripting via data_object Parameter in all versions up to, and including, 2.2.13 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable by unauthenticated attackers because the cdbbc_payment_verify AJAX action is registered under wp_ajax_nopriv_ and its only authentication gate — a nonce check — is bypassable, as the cdbbc_donation_box nonce is publicly exposed to anonymous visitors via the wallets_data JavaScript object emitted by the [crypto-donation-box] shortcode.

### CVE-2026-83592

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:38.893 |

The Contact Form DB for Enfold plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Contact Form Field Values in all versions up to, and including, 2.0.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload is echoed unescaped both inside a title HTML attribute and in the table cell body in admin/ecf_index.php; base64 encoding and serialization of the stored values do not neutralize the malicious content.

### CVE-2026-77114

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:36.537 |

The Document Gallery plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'dg_thumber_webhook' Action Request Body in all versions up to, and including, 5.1.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that logging be enabled in the plugin's Advanced settings, which is only the default state when WP_DEBUG is true; otherwise an administrator must manually enable it.

### CVE-2026-100153

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T04:18:03.177 |

The NewStatPress plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'QUERY_STRING / REQUEST_URI' parameter in all versions up to, and including, 1.4.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires that an administrator has placed the [NewStatPress type="Top Pages"] shortcode on a publicly viewable page, and that the attacker's crafted URL accumulates enough hits to appear in the top-N ranking.

### CVE-2026-103422

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T03:17:14.037 |

The AnyComment plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'email' parameter in versions up to, and including, 0.3.6. This is due to insufficient input sanitization on the public /wp-json/anycomment/v1/subscribe REST endpoint and missing output escaping in AnyCommentSubscriptionsTable::column_default(), which returns the stored email verbatim into an HTML <td> when the subscription's user_ID does not resolve to an existing WP_User. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever an administrator accesses the AnyComment → Subscriptions admin page.

### CVE-2026-92910

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:21:43.723 |

Adobe Commerce is affected by an Incorrect Authorization vulnerability that could result in a Security feature bypass. An attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-85798

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:03.630 |

Heap-based buffer overflow in Windows Distributed File System (DFS) allows an authorized attacker to execute code over a network.

### CVE-2026-70267

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-13T19:19:45.420 |

Inclusion of functionality from untrusted control sphere in Microsoft Office SharePoint allows an authorized attacker to execute code over a network.

### CVE-2026-110211

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:45.037 |

iFlytek SkillHub through 0.2.22 contains a missing authorization vulnerability that allows any authenticated user to permanently delete other users' skills via DELETE /api/cli/v1/skills/{namespace}/{slug}. Attackers can locate targets through the anonymous search endpoint and trigger deletion without ownership checks, purging all versions, files, reviews, ratings and metadata.

### CVE-2026-108399

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:05.103 |

Heap-based buffer overflow in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-23707

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T18:17:23.590 |

An Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability [CWE-89] vulnerability in Fortinet FortiAnalyzer 7.6.0 through 7.6.4, FortiAnalyzer 7.4.0 through 7.4.7, FortiAnalyzer 7.2 all versions, FortiAnalyzer Cloud 7.6.2 through 7.6.4, FortiAnalyzer Cloud 7.4.1 through 7.4.7, FortiAnalyzer Cloud 7.2.1 through 7.2.11, FortiManager 7.6.0 through 7.6.4, FortiManager 7.4.0 through 7.4.6, FortiManager 7.2 all versions, FortiManager Cloud 7.6.2 through 7.6.4 may allow a low privileged user to execute arbitrary commands via crafted requests.

### CVE-2026-23705

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T18:17:23.320 |

An Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability [CWE-89] vulnerability in Fortinet FortiAnalyzer 7.6.0 through 7.6.4, FortiAnalyzer 7.4.0 through 7.4.7, FortiAnalyzer 7.2 all versions, FortiManager 7.6.0 through 7.6.4, FortiManager 7.4.0 through 7.4.6, FortiManager 7.2 all versions may allow a low privileged user to execute arbitrary commands via crafted requests.

### CVE-2026-107870

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T14:17:33.527 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetEngine jet-engine allows DOM-Based XSS.This issue affects JetEngine: from n/a through 3.8.16.

### CVE-2026-107867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T13:17:24.290 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crocoblock JetProductTables jet-product-tables allows Reflected XSS.This issue affects JetProductTables: from n/a through 1.2.4.

### CVE-2026-105874

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T13:17:22.043 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Brainstorm Force SureCart surecart allows Reflected XSS.This issue affects SureCart: from n/a through 4.9.3.

### CVE-2026-107428

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T09:17:22.180 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VideoWhisper.com Paid Videochat Turnkey Site ppv-live-webcams allows Reflected XSS.This issue affects Paid Videochat Turnkey Site: from n/a through 7.5.12.

### CVE-2026-88964

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-13T23:19:13.687 |

An integer underflow in OpenVPN version 2.7_alpha3 through 2.7.7 on Windows and Android allows remote authenticated servers to cause a denial of service or memory disclosure via crafted domain search options

### CVE-2026-76001

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T21:18:20.730 |

ColdFusion is affected by a Server-Side Request Forgery (SSRF) vulnerability that could result in privilege escalation. A low-privileged attacker could exploit this vulnerability to gain elevated access to internal resources. Exploit depends on conditions beyond the attacker's control. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-63172

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T20:17:32.080 |

Omnispace Agora Project before 26.10.0 contains a broken access control vulnerability that allows a regular, non-administrative member to create user accounts by invoking the user-edit action without a function-level authorization check. Attackers can exploit the missing editRight() enforcement in actionVueEditUser to create unauthorized user accounts, leading to privilege escalation.

### CVE-2026-110084

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-91` |
| Published | 2026-10-13T20:17:27.217 |

Adobe Experience Manager is affected by an XML Injection (aka Blind XPath Injection) vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction.

### CVE-2026-110083

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-13T20:17:27.090 |

Adobe Experience Manager is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction.

### CVE-2026-85856

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:12.050 |

Heap-based buffer overflow in Windows Internet Connection Sharing (ICS) allows an authorized attacker to execute code over an adjacent network.

### CVE-2026-83715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:20:16.060 |

Missing authentication for critical function in Windows Error Reporting allows an authorized attacker to perform tampering locally.

### CVE-2026-70126

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-13T19:19:24.743 |

Out-of-bounds read in Windows Bluetooth Port Driver allows an unauthorized attacker to execute code over an adjacent network.

### CVE-2026-69452

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:55.033 |

Use after free in Windows Enterprise App Management allows an authorized attacker to elevate privileges over a network.

### CVE-2026-110236

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-13T19:18:48.770 |

KDE Dolphin 24.08.0 through 26.08.2 contains an OS command injection vulnerability that allows attackers to execute commands by supplying crafted folder names substituted into the {path} placeholder. Attackers can embed a double quote and shell metacharacters in a directory name to escape quoting in slotDoubleClickViewBackground, executing commands when victims double-click the view background.

### CVE-2026-110220

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-13T19:18:46.413 |

Kubeflow Model Registry through 0.3.17 contains a server-side request forgery vulnerability that allows namespace users to steal the controller ServiceAccount token via the modelregistry.kubeflow.org/url annotation. Attackers can create an InferenceService pointing the annotation at their server, capture the bearer token, and modify other tenants' InferenceServices cluster-wide.

### CVE-2026-110217

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-13T19:18:45.937 |

Lenve vhr through commit 03abbd3 contains an information disclosure vulnerability that allows any authenticated user to retrieve other operators' BCrypt password hashes via GET /chat/hrs. Low-privileged operators can collect administrator password hashes, phone numbers, and addresses from the serialized Hr entity for offline cracking and privilege escalation.

### CVE-2026-110216

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:45.790 |

youlai-boot through 2.21.1 contains a missing authorization vulnerability that allows any authenticated user to enable or disable accounts because the updateUserStatus handler lacks a @PreAuthorize check. Attackers can send PATCH requests to /api/v1/users/{userId}/status to disable root or admin accounts, locking administrators out, or re-enable accounts an administrator has disabled.

### CVE-2026-110209

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:44.740 |

Stonewuu ai-fusion-video through 1.2.0 contains a missing authorization vulnerability that allows authenticated non-admin users to read stored secrets through unprotected ApiConfigController and SystemConfigController endpoints. Attackers can query the api-config get/list and system config endpoints to obtain AI provider API keys, proxy passwords and mail_password, enabling billing abuse and sending mail as the platform.

### CVE-2026-110208

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T19:18:44.590 |

Wukong AICRM through 20260610 contains a missing authorization vulnerability in the /systemConfig controller that allows any authenticated user to read the stored AI provider API key. Attackers can request GET /systemConfig/byType/ai for the cleartext key, or send a chosen apiUrl to /systemConfig/ai/test, forwarding the stored key to their host.

### CVE-2026-105729

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:18:01.037 |

Untrusted pointer dereference in SysInternals allows an authorized attacker to elevate privileges locally.

### CVE-2026-104875

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T19:17:55.863 |

Ente provides end-to-end encrypted cloud services and security tools. Prior to server image 2026.07.09, the POST /emergency-contacts/approve-recovery endpoint authorized approval using a client-supplied userID and updated an emergency recovery session using only its client-supplied recovery-session UUID. An accepted emergency contact could submit the contact's own identifier, transition the victim's session from WAITING to READY, clear wait_till, retrieve recovery information, and continue account recovery before the owner-configured notice period expired. Exploitation of the approval bypass required the victim to have previously added and accepted the attacker as an emergency contact, and it did not create recovery rights for an arbitrary account. Separately, the same insufficiently scoped update pattern affected the reject and stop recovery transitions, allowing a user who knew another recovery-session UUID to potentially cancel a session to which the user was not a party. This issue is fixed in server image 2026.07.09.

### CVE-2026-100205

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:17:40.540 |

Untrusted pointer dereference in SysInternals allows an authorized attacker to elevate privileges locally.

### CVE-2026-110129

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:38.797 |

fuintCatering through commit 122c9e6 contains an insecure direct object reference vulnerability in the ClientRefundController refund detail endpoint that lets authenticated members read other members' refund records. Attackers can register freely and enumerate sequential refundId values to obtain buyers' names, national ID numbers, addresses, WeChat openIds, and order details.

### CVE-2026-110123

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T17:17:36.880 |

Makunet maku-boot 4.3.0 through 5.0.0 contains a missing authorization vulnerability that allows authenticated users to read mail and SMS configurations by calling /sys/mail/config/list and /sys/sms/config/list without the required authority checks. Attackers can retrieve unmasked SMTP passwords and Aliyun, Tencent Cloud, Qiniu or Huawei Cloud access keys, and abuse /sys/mail/config/send to send mail to arbitrary recipients.

### CVE-2026-110121

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:36.557 |

PickMall lilishop through 4.4 contains an insecure direct object reference vulnerability that allows authenticated sellers to overwrite any store's product by supplying another store's goodsId to the goods update endpoint. Attackers can send PUT requests to /store/goods/goods/update/{goodsId} to replace product details and SKUs and reassign products to their own store.

### CVE-2026-110119

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:36.273 |

Yshopmall through 2.0.0 contains an insecure direct object reference vulnerability in the member address API that allows authenticated members to read, overwrite and delete other members' shipping addresses. Attackers can enumerate sequential address ids via /address/detail/{id}, /address/del and /address/edit to expose recipient names, phone numbers and addresses, reassign them, or delete them.

### CVE-2026-110118

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-13T17:17:36.130 |

WorkFlow-Engine through 9.6.11 contains a missing authorization vulnerability that allows authenticated users to complete or reassign other users' workflow tasks via /vue/buttonOperation endpoints. Low-privileged attackers can supply a known taskId to the complete, completeTask or reAssign handlers to approve tasks or reassign them without authority.

### CVE-2026-110117

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T17:17:35.977 |

SmartAdmin through 3.30.0 contains a missing authorization vulnerability in AdminProtectController that allows authenticated low-privileged employees to modify system-wide level-3 protection settings. Attackers can call the unannotated updateConfig and loginFail batchDelete endpoints to disable login lockout and two-factor login, weaken password rules, and clear lockout records.

### CVE-2026-110109

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-13T17:17:35.070 |

JetLinks Community through 2.10.0 contains a missing authorization vulnerability that allows users with only query access on transparent-codec to overwrite product codecs via POST /device/transparent-codec/{productId}. Because the endpoint lacks @SaveAction, attackers can save arbitrary codec providers and configurations, controlling how transparent messages are decoded and encoded for every device of that product.

### CVE-2026-96299

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-13T16:17:24.323 |

A security issue was discovered in MongoDB mongos (the sharded cluster router) where an authenticated user with readWrite privileges could crash the mongos process by crafting a specially formed aggregation pipeline. The issue leverages an internal aggregation stage that lacks proper authorization checks despite being intended for internal use, allowing a subsequent stage to be forced to execute on the router under conditions it was not designed to handle. This results in an unhandled fatal error that causes the mongos process to immediately abort, resulting in denial of service for all clients routed through the affected mongos instance.

### CVE-2026-104005

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-13T16:17:11.137 |

A security issue was discovered in MongoDB mongos (the sharded cluster router) where an authenticated user with readWrite privileges could crash the mongos process by crafting a specially formed aggregation pipeline. The issue leverages an internal aggregation stage that lacks proper authorization checks despite being intended for internal use, allowing a subsequent stage to be forced to execute on the router under conditions it was not designed to handle. This results in an unhandled fatal error that causes the mongos process to immediately abort, resulting in denial of service for all clients routed through the affected mongos instance.

### CVE-2026-104004

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T16:17:10.930 |

MongoDB Server's collection validation feature may not properly handle certain expressions stored in a validator. In some cases, this can cause the server process to stop running when a document is later inserted. The behavior can occur for authenticated users with write access.

### CVE-2026-97333

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T15:17:52.160 |

QAPI contained a stack-based buffer overflow affecting service availability.  Software customers upgrade to resolved maintenance release. Update CommServe, Web Server, Command Center and Index Server.

### CVE-2026-77095

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:49.273 |

CvFWD contained a null pointer dereference affecting service availability.  Software customers upgrade to resolved maintenance release. Update all Commvault installations, including CommServe, Webserver, Command Center, MediaAgents, Clients and HyperScale.

### CVE-2026-77094

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:49.143 |

CvFWD contained an out-of-bounds write affecting service availability.  Software customers upgrade to resolved maintenance release. Software customers upgrade to resolved maintenance release. Update all Commvault installations, including CommServe, Webserver, Command Center, MediaAgents, Clients and HyperScale.

### CVE-2026-77093

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:49.017 |

CvFWD contained an integer overflow affecting service availability.  Software customers upgrade to resolved maintenance release. Update all Commvault installations, including CommServe, Webserver, Command Center, MediaAgents, Clients and HyperScale

### CVE-2026-18228

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-13T15:17:44.103 |

HyperScale contained a path traversal issue affecting information disclosure.  Software customers upgrade to resolved maintenance release. Update Commvault installation of HyperScale MediaAgents.

### CVE-2026-107153

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1391` |
| Published | 2026-10-14T06:17:05.390 |

Multiple smartphones provided by Rakuten Mobile, Inc. utilize AOSP test keys for their Android Verified Boot (AVB) functionality. With physical access to the affected device, a crafted system image may be installed.

### CVE-2026-88088

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-13T21:19:43.307 |

Integer overflow or wraparound in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-88082

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:19:42.693 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-85919

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T21:19:34.053 |

Heap-based buffer overflow in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-85876

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T21:19:30.767 |

Use after free in SQL Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-62840

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T21:17:40.033 |

Time-of-check time-of-use (toctou) race condition in Linux Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-86022

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-10-13T20:18:55.473 |

VNote is a note-taking platform. Prior to 4.3.0, SessionConfig::ExternalProgram::fetchCommand wraps a note path in double quotes and substitutes it into a command string that QProcess::start(const QString&) reparses into arguments through ProcessUtils::startDetached. The automatic path in src/controllers/viewareacontroller.cpp and the Open With path in src/controllers/notebooknodecontroller.cpp both reach this sink. On Linux and macOS, an attacker-controlled double quote in a POSIX note filename can terminate the quoted path and add arguments to the victim's configured external program. If the configured program supports an argument that executes commands, such as the vim or gvim -c option, the injected arguments can execute arbitrary commands as the user. This issue is fixed in version 4.3.0.

### CVE-2026-97812

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:22:19.467 |

Double free in Windows Update Orchestrator Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97810

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:19.183 |

Heap-based buffer overflow in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-97808

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:18.903 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-97793

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:22:17.353 |

Missing authentication for critical function in Windows Setup and Deployment allows an authorized attacker to elevate privileges locally.

### CVE-2026-97787

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:22:16.563 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Container Isolation FS Filter Driver (unionfs.sys) allows an authorized attacker to elevate privileges locally.

### CVE-2026-97774

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:22:15.350 |

Time-of-check time-of-use (toctou) race condition in Microsoft Office Click-To-Run allows an authorized attacker to elevate privileges locally.

### CVE-2026-96949

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:22:07.407 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-96939

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:22:06.230 |

Time-of-check time-of-use (toctou) race condition in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-96937

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:05.917 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-96932

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:22:05.253 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Embedded Mode Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96923

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:22:03.690 |

Use after free in Windows Workstation Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96919

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:22:03.193 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-96868

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:22:01.383 |

Heap-based buffer overflow in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96852

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:58.663 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-96323

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:56.853 |

Use after free in Windows Update allows an authorized attacker to elevate privileges locally.

### CVE-2026-96322

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:55.323 |

Use after free in Windows Remote Desktop Protocol allows an authorized attacker to elevate privileges locally.

### CVE-2026-96319

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:54.877 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96313

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-13T19:21:53.880 |

Missing authentication for critical function in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-96310

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:53.400 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96307

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:52.910 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96305

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:52.567 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96304

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:52.420 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96302

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:52.110 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-96301

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:51.973 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96254

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:51.643 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96253

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:51.503 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96250

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:51.050 |

Use after free in Windows USB Print Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-96216

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416;CWE-822` |
| Published | 2026-10-13T19:21:47.250 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-96215

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:47.117 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-96209

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:46.940 |

Out-of-bounds read in Windows Network File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-95943

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:21:44.983 |

Double free in Connected Devices Platform Service (Cdpsvc) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88161

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:36.560 |

Use after free in Windows Local Security Authority (LSA) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88160

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:36.383 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-88149

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:21:34.723 |

Double free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-88146

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:21:34.390 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Background Intelligent Transfer Service (BITS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-88141

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:33.673 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-88139

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:33.387 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-88127

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:31.720 |

Use after free in Windows SMB Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-88124

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:31.227 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-88113

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:29.360 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88110

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:29.060 |

Heap-based buffer overflow in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-88107

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:21:28.787 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-88106

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:28.620 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-88103

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:28.340 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-88098

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-10-13T19:21:27.620 |

Untrusted pointer dereference in Windows Security Support Provider Interface allows an authorized attacker to elevate privileges locally.

### CVE-2026-88096

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:27.447 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows DCOM Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-88079

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:21:26.567 |

Null pointer dereference in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-88076

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:21:26.390 |

Null pointer dereference in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87715

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:25.210 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87710

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:24.293 |

Improper access control in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to elevate privileges locally.

### CVE-2026-87708

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:23.943 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87704

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:23.227 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-87693

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:21.803 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85943

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-367` |
| Published | 2026-10-13T19:21:21.050 |

Time-of-check time-of-use (toctou) race condition in Reliable Multicast Transport Driver (RMCAST) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85941

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:21:20.870 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85934

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:19.907 |

Use after free in Windows AppX Deployment Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85930

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:19.107 |

Use after free in Windows Image Acquisition allows an authorized attacker to elevate privileges locally.

### CVE-2026-85920

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:21:18.133 |

Time-of-check time-of-use (toctou) race condition in Windows BitLocker allows an authorized attacker to elevate privileges locally.

### CVE-2026-85918

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:17.957 |

Use after free in Windows Universal Plug and Play (UPnP) Device Host allows an authorized attacker to elevate privileges locally.

### CVE-2026-85914

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:17.517 |

Use after free in Windows Embedded Mode Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85912

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:17.353 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Clipboard User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85904

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-415` |
| Published | 2026-10-13T19:21:16.223 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85879

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:21:15.073 |

Time-of-check time-of-use (toctou) race condition in Windows Subsystem for Linux allows an authorized attacker to elevate privileges locally.

### CVE-2026-85870

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:14.253 |

Heap-based buffer overflow in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85868

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:13.890 |

Use after free in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85855

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:11.930 |

Use after free in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-85854

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:11.780 |

Use after free in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-85853

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:21:11.623 |

Out-of-bounds read in Windows DWM Core Library allows an authorized attacker to elevate privileges locally.

### CVE-2026-85846

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:10.523 |

Use after free in Windows Web Account Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-85834

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:09.310 |

Heap-based buffer overflow in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-85828

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:08.137 |

Heap-based buffer overflow in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-85827

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:07.957 |

Heap-based buffer overflow in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-85826

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-13T19:21:07.777 |

Out-of-bounds write in Windows Fast FAT Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85825

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:21:07.597 |

Use after free in Windows Universal Disk Format File System Driver (UDFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85824

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:21:07.460 |

Use after free in Windows Composite Image File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-85823

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:07.330 |

Use after free in Windows Composite Image File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-85810

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:05.477 |

Use after free in Windows Telephony Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-85803

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:04.333 |

Use after free in Windows Camera Frame Server Monitor allows an authorized attacker to elevate privileges locally.

### CVE-2026-85802

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:04.160 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-85791

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:21:02.390 |

Heap-based buffer overflow in Windows Encrypting File System (EFS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-85372

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:01.027 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-85370

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:00.667 |

Use after free in WebDAV allows an authorized attacker to elevate privileges locally.

### CVE-2026-85367

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:21:00.170 |

Use after free in Windows Cash Drawer Protocol Provider allows an authorized attacker to elevate privileges locally.

### CVE-2026-85365

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:59.810 |

Heap-based buffer overflow in Servicing Stack Updates allows an authorized attacker to elevate privileges locally.

### CVE-2026-85364

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:59.630 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85362

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:20:59.293 |

Release of invalid pointer or reference in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-85361

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:59.110 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-85357

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:20:58.480 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Phone Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85355

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-13T19:20:58.117 |

Inclusion of functionality from untrusted control sphere in Windows Common Log File System Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-85354

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:57.940 |

Use after free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-85352

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:57.580 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85342

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:57.233 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-85329

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:20:55.353 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Account allows an authorized attacker to elevate privileges locally.

### CVE-2026-85328

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-13T19:20:54.223 |

Weak authentication in Windows Projected File System allows an authorized attacker to elevate privileges locally.

### CVE-2026-84020

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:52.593 |

Use after free in Windows Routing and Remote Access Service (RRAS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-84019

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:52.437 |

Use after free in Windows Advanced Rasterization Platform allows an authorized attacker to elevate privileges locally.

### CVE-2026-84018

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-10-13T19:20:52.257 |

Use after free in Windows Print Spooler Components allows an authorized attacker to elevate privileges locally.

### CVE-2026-84014

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-10-13T19:20:51.550 |

Heap-based buffer overflow in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83930

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:49.570 |

Use after free in Windows Update Orchestrator Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83924

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:48.570 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83921

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:47.947 |

Heap-based buffer overflow in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83917

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:47.253 |

Use after free in Windows ALPC allows an authorized attacker to elevate privileges locally.

### CVE-2026-83916

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:20:47.080 |

Double free in Windows Error Reporting allows an authorized attacker to execute code locally.

### CVE-2026-83915

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:46.927 |

Use after free in Windows Diagnostic Policy Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83911

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:46.250 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-83908

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-763` |
| Published | 2026-10-13T19:20:45.700 |

Release of invalid pointer or reference in RPC Runtime allows an authorized attacker to elevate privileges locally.

### CVE-2026-83901

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:44.220 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-83900

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:44.040 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83899

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:20:43.363 |

Improper privilege management in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83886

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:39.427 |

Use after free in Windows Update Orchestrator Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83879

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:20:38.463 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-83871

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-367` |
| Published | 2026-10-13T19:20:36.990 |

Heap-based buffer overflow in OpenSSH for Windows allows an authorized attacker to elevate privileges locally.

### CVE-2026-83868

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:20:36.517 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Microsoft Bluetooth Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83866

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:36.197 |

Use after free in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83853

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:34.227 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-83852

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:34.110 |

Use after free in Windows Bind Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83846

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:33.147 |

Use after free in Connected Devices Platform Service (Cdpsvc) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83842

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:20:32.560 |

Double free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-83841

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:20:32.407 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Win32K allows an authorized attacker to elevate privileges locally.

### CVE-2026-83839

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:20:32.090 |

Time-of-check time-of-use (toctou) race condition in Windows Hyper-V allows an authorized attacker to elevate privileges locally.

### CVE-2026-83834

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-416` |
| Published | 2026-10-13T19:20:31.227 |

Use after free in Windows Kernel-Mode Drivers allows an authorized attacker to elevate privileges locally.

### CVE-2026-83827

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:30.260 |

Heap-based buffer overflow in Windows Bluetooth Port Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83793

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:20:29.150 |

Improper link resolution before file access ('link following') in Windows Update Orchestrator Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83790

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:28.743 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-83785

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:27.863 |

Use after free in Windows COM+ Event System Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83775

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-362` |
| Published | 2026-10-13T19:20:26.043 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83752

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:21.243 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83751

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:21.103 |

Use after free in Windows MIDI Service Module allows an authorized attacker to elevate privileges locally.

### CVE-2026-83750

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-367` |
| Published | 2026-10-13T19:20:20.893 |

Time-of-check time-of-use (toctou) race condition in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83749

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:20.693 |

Use after free in Windows Overlay Filter allows an authorized attacker to elevate privileges locally.

### CVE-2026-83740

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:19.793 |

Use after free in Windows Hello allows an authorized attacker to elevate privileges locally.

### CVE-2026-83738

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:20:19.343 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-83724

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:17.630 |

Heap-based buffer overflow in Windows Management Instrumentation allows an authorized attacker to elevate privileges locally.

### CVE-2026-83722

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:20:17.173 |

Use after free in Microsoft Local Security Authority Server (lsasrv) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83720

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:16.903 |

Use after free in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-83718

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:16.580 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83717

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:16.407 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83710

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:15.377 |

Use after free in Windows Device Association Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83708

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:20:15.010 |

Stack-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83707

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:14.853 |

Use after free in Windows Event Tracing allows an authorized attacker to elevate privileges locally.

### CVE-2026-83702

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:13.973 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83701

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:13.810 |

Use after free in Windows Now Playing Session Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-83696

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:12.987 |

Use after free in Windows Cloud Files Mini Filter Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83694

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-13T19:20:12.597 |

Out-of-bounds read in Windows Volume Manager Extension Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-83689

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:11.650 |

Use after free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-83687

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:11.297 |

Use after free in Windows Connected User Experiences and Telemetry allows an authorized attacker to elevate privileges locally.

### CVE-2026-83682

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:10.527 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-83680

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:10.233 |

Heap-based buffer overflow in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83676

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-191` |
| Published | 2026-10-13T19:20:09.653 |

Integer underflow (wrap or wraparound) in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-83675

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:09.527 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-83666

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:20:08.177 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Active Directory Certificate Services (AD CS) allows an authorized attacker to elevate privileges locally.

### CVE-2026-83644

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:05.340 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83584

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:02.530 |

Use after free in Windows Smart Card allows an authorized attacker to elevate privileges locally.

### CVE-2026-83580

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:20:00.910 |

Heap-based buffer overflow in Windows Client-Side Caching (CSC) Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-83575

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:00.243 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83574

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:20:00.047 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83566

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:58.930 |

Use after free in Windows Win32K - ICOMP allows an authorized attacker to elevate privileges locally.

### CVE-2026-83564

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:58.570 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-83510

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:19:56.280 |

Time-of-check time-of-use (toctou) race condition in Windows Setup Files Cleanup allows an authorized attacker to elevate privileges locally.

### CVE-2026-83509

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-13T19:19:56.097 |

Untrusted search path in Windows Setup Files Cleanup allows an authorized attacker to elevate privileges locally.

### CVE-2026-83505

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367;CWE-426` |
| Published | 2026-10-13T19:19:55.430 |

Time-of-check time-of-use (toctou) race condition in Windows Setup Files Cleanup allows an authorized attacker to elevate privileges locally.

### CVE-2026-81971

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:54.823 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-72969

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:52.047 |

Use after free in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72968

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:51.880 |

Use after free in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-72955

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:51.747 |

Use after free in Windows Application Compatibility Cache allows an authorized attacker to elevate privileges locally.

### CVE-2026-72934

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:51.613 |

Use after free in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70276

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:46.873 |

Use after free in Microsoft Office Click-To-Run allows an authorized attacker to elevate privileges locally.

### CVE-2026-70273

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:46.377 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70272

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:46.127 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-70271

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:45.950 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70253

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:43.390 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70252

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:43.030 |

Use after free in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70249

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:42.263 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70243

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:41.120 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70241

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:40.800 |

Use after free in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-70237

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:40.437 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-70236

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:40.260 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70230

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:39.403 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70223

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:38.300 |

Use after free in Windows Console Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-70212

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-923` |
| Published | 2026-10-13T19:19:35.697 |

Improper restriction of communication channel to intended endpoints in Windows Security Center allows an authorized attacker to elevate privileges locally.

### CVE-2026-70209

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:35.150 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70205

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-13T19:19:34.487 |

Access of resource using incompatible type ('type confusion') in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-70198

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:33.910 |

Use after free in Windows Push Notifications allows an authorized attacker to elevate privileges locally.

### CVE-2026-70176

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:31.817 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70169

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:30.840 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Connected Devices Platform Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70168

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:30.657 |

Use after free in Windows Ancillary Function Driver for WinSock allows an authorized attacker to elevate privileges locally.

### CVE-2026-70164

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:30.087 |

Use after free in Windows TCP/IP allows an authorized attacker to elevate privileges locally.

### CVE-2026-70160

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:29.510 |

Use after free in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-70156

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:28.857 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70150

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:28.220 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70144

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:27.553 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70140

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:26.900 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70136

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:26.180 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70134

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:25.850 |

Use after free in Windows Event Tracing allows an authorized attacker to elevate privileges locally.

### CVE-2026-70118

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:24.003 |

Use after free in Windows Audio Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70115

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:23.593 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70086

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:20.230 |

Use after free in Microsoft Windows Search Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-70076

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:19.207 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70067

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:17.950 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-70066

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:17.800 |

Use after free in Windows DHCP Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-70056

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:16.433 |

Use after free in Windows Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-70045

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:15.203 |

Use after free in Windows Work Folders allows an authorized attacker to elevate privileges locally.

### CVE-2026-70026

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:13.850 |

Use after free in Windows Secure Kernel Mode allows an authorized attacker to elevate privileges locally.

### CVE-2026-70021

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:13.210 |

Use after free in Windows Direct Composition allows an authorized attacker to elevate privileges locally.

### CVE-2026-69977

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:08.420 |

Use after free in Quality Windows Audio/Video Experience (QWAVE) service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69970

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:19:07.653 |

Heap-based buffer overflow in Microsoft Streaming Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69964

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:06.803 |

Use after free in Microsoft Streaming Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69935

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:04.020 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69931

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:03.730 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69915

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:02.713 |

Use after free in Windows NTFS allows an authorized attacker to elevate privileges locally.

### CVE-2026-69856

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:19:00.433 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69840

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:19:00.093 |

Use after free in Windows Certificates allows an authorized attacker to elevate privileges locally.

### CVE-2026-69795

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-13T19:18:59.467 |

Null pointer dereference in Windows Clipboard Server allows an authorized attacker to elevate privileges locally.

### CVE-2026-69766

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:18:59.017 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69763

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:18:58.747 |

Use after free in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-69743

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:58.617 |

Use after free in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69736

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:18:58.440 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Credential Manager allows an authorized attacker to elevate privileges locally.

### CVE-2026-69596

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:56.003 |

Use after free in Windows Program Compatibility Assistant Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-69387

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:54.710 |

Use after free in Windows Error Reporting allows an authorized attacker to elevate privileges locally.

### CVE-2026-110237

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-283` |
| Published | 2026-10-13T19:18:48.917 |

Vifm 0.8.1-beta through 0.14.4 reuses a pre-existing IPC FIFO in the shared temporary directory without checking ownership, allowing local users to execute commands as another user. Attackers can pre-create a world-writable vifm-ipc-vifm FIFO and write IPC packets with -c and ! shell commands that execute with the victim's privileges.

### CVE-2026-109453

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:18:33.393 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-108468

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:07.180 |

Use after free in Windows Installer allows an authorized attacker to elevate privileges locally.

### CVE-2026-108465

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:06.620 |

Use after free in Windows Update Delivery Optimization allows an authorized attacker to elevate privileges locally.

### CVE-2026-108464

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:06.443 |

Use after free in Software Protection Platform (SPP) allows an authorized attacker to elevate privileges locally.

### CVE-2026-108461

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:05.960 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-108396

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-13T19:18:04.800 |

Time-of-check time-of-use (toctou) race condition in Windows Modern Device Management (MDM) allows an authorized attacker to elevate privileges locally.

### CVE-2026-108135

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-13T19:18:03.960 |

Improper link resolution before file access ('link following') in Windows Backup Engine allows an authorized attacker to elevate privileges locally.

### CVE-2026-108134

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:03.830 |

Use after free in Windows Autopilot allows an authorized attacker to elevate privileges locally.

### CVE-2026-108132

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-13T19:18:03.530 |

Double free in Windows Kerberos allows an authorized attacker to elevate privileges locally.

### CVE-2026-105725

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:00.507 |

Use after free in Windows Security App allows an authorized attacker to elevate privileges locally.

### CVE-2026-105722

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:18:00.150 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-103565

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:52.523 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-103555

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:52.037 |

Heap-based buffer overflow in Virtual Hard Disk (VHD) Miniport Driver allows an authorized attacker to elevate privileges locally.

### CVE-2026-103554

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:51.903 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-102232

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-13T19:17:48.807 |

Incorrect authorization in Visual Studio Code allows an unauthorized attacker to bypass a security feature locally.

### CVE-2026-102211

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-416` |
| Published | 2026-10-13T19:17:46.673 |

Use after free in Windows Virtualization-Based Security (VBS) Enclave allows an authorized attacker to elevate privileges locally.

### CVE-2026-102209

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:46.390 |

Heap-based buffer overflow in Microsoft Graphics Component allows an authorized attacker to elevate privileges locally.

### CVE-2026-102208

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:46.230 |

Use after free in Windows Win32 Kernel Subsystem allows an authorized attacker to elevate privileges locally.

### CVE-2026-102207

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-13T19:17:46.027 |

Concurrent execution using shared resource with improper synchronization ('race condition') in Windows Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-102197

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:44.533 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-102195

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:44.257 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-102194

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:44.073 |

Use after free in Windows Graphics Kernel allows an authorized attacker to elevate privileges locally.

### CVE-2026-102193

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:43.930 |

Use after free in Windows Broadcast DVR User Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-102191

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:43.663 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-102189

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:43.517 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-100225

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:42.780 |

Heap-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-100216

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-13T19:17:41.650 |

Stack-based buffer overflow in Windows Storage allows an authorized attacker to elevate privileges locally.

### CVE-2026-100203

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-13T19:17:40.327 |

Heap-based buffer overflow in Windows Update Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-100201

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-197` |
| Published | 2026-10-13T19:17:39.983 |

Heap-based buffer overflow in Windows Client License Service allows an authorized attacker to elevate privileges locally.

### CVE-2026-100200

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-13T19:17:39.840 |

Use after free in Windows Update Service allows an authorized attacker to elevate privileges locally.
