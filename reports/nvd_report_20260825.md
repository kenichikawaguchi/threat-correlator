# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-24 15:00 UTC
- **対象期間**: `2026-08-23T15:00:22.000Z` 〜 `2026-08-24T15:00:18.000Z`
- **重要CVE数**: 80 件（Critical 9.0+: 18 件 / High 7.0〜: 62 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** 登録され、特に **Web アプリケーション・コンテナ基盤・エンタープライズ向けクライアントソフト** に集中しています。  
- **リモートから認証不要でコード実行や権限昇格が可能** な脆弱性が目立ち、攻撃者は最小限の操作で管理者権限取得やシステム全体への侵入が可能です。  
- Joomla、WordPress 系プラグイン、LXD、Zscaler Client Connector など、**広く利用されているオープンソース・商用製品** が多数対象となっており、組織全体の攻撃対象面が拡大しています。  
- 複数の脆弱性は **同一製品で複数の攻撃ベクトル（SQLi、POI、OS コマンドインジェクション、認証バイパス）** を提供しているため、単一のパッチ適用だけでは不十分なケースが増えています。

---

## 2. 特に注目すべき CVE  

| CVE | 製品・バージョン | CVSS | 主な問題点 | 影響範囲・リスク |
|-----|------------------|------|------------|-------------------|
| **CVE‑2026‑77995** | Joomla Extension **miniOrange OAuth Client** `< 3.2.0` | 10.0 | 任意の Cookie 値を書き換えることで **認証なしで任意アカウントにログイン**（管理者含む） | Joomla サイト全体が乗っ取られ、管理画面・プラグイン設定・データベースが完全に制御可能になる。 |
| **CVE‑2026‑66897** | **LXD** (Linux コンテナ管理) – インスタンステンプレート処理 | 9.9 | パス・トラバーサルにより **ホスト上の任意ファイルを書き換え**（root 権限） | コンテナを利用しているすべてのサーバで、攻撃者がホスト OS の完全制御を取得できる。特にマルチテナント環境で深刻。 |
| **CVE‑2026‑66650** | **FreightCo** ≤ 1.1.15 (PHP アプリ) | 9.8 | **Unauthenticated PHP Object Injection** → 任意コード実行 | Web アプリのフロントエンドから直接シェル実行が可能。顧客情報・支払情報が漏洩・改ざんされる危険性。 |
| **CVE‑2026‑59568** | **Zscaler Client Connector** (複数バージョン) | 9.1 | リモートコード実行 (RCE) – 未認証で任意コード実行可能 | エンドポイント保護ソフト自体が攻撃対象になるため、企業ネットワーク全体の防御が失われる。 |
| **CVE‑2026‑78211** | **4MOSAn GCB Doctor** (OS Command Injection) | 9.3 | ADOdb テストページのパラメータ未除去により **任意コマンド実行** | サーバ上で任意シェルが起動し、内部ネットワークへの踏み台化が容易になる。 |

### なぜこれらが重要か
1. **スコアが最高（10.0）または 9.0 以上** で、**認証不要** のリモート攻撃が可能。  
2. **広範囲に展開されているプラットフォーム**（Joomla、LXD、Zscaler）であり、**組織のインフラ全体に波及** するリスクが高い。  
3. **権限昇格・コード実行** が直接的にシステム全体の制御につながり、**データ漏洩・ランサムウェア感染** など二次被害が想定される。  

---

## 3. 推奨アクション  

### 3‑1. 速やかなパッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 推奨バージョン / 対策 |
|------|-------------------|------------------------|
| miniOrange OAuth Client (Joomla) | `< 3.2.0` | **3.2.0 以上** にアップデート。公式パッチが未提供の場合はプラグインの無効化・削除を検討。 |
| LXD | 影響のあるすべてのリリース（詳細は公式アドバイザリ） | **LXD 5.21.0 以降**（パス・トラバーサル修正）へアップグレード。 |
| FreightCo | ≤ 1.1.15 | **1.1.16 以上** に更新。 |
| Zscaler Client Connector | 影響のある全バージョン | **ZCC 6.5.3 以降**（RCE 修正）へ更新。併せて **エンドポイント証明書のローテーション** を実施。 |
| 4MOSAn GCB Doctor | すべてのリリース | **最新版 (≥ 2.3.0)** にアップデートし、**ADOdb テストページ** (`/adodb_test.php` 等) を **Web サーバから削除**、またはアクセス制御 (IP 制限・Basic Auth) を適用。 |

### 3‑2. 侵入検知・防御の強化
- **WAF ルール追加**  
  - `miniOrange OAuth Client` の Cookie 操作パターン（例: `miniOrangeOAuth=...`）をブロック。  
  - LXD のテンプレートパスに対する `../` 系文字列を検知し、リクエストを遮断。  
- **IDS/IPS のシグネチャ更新**  
  - Zscaler Client Connector の RCE ペイロード（CVE‑2026‑59568）を含むシグネチャを導入。  
- **ログ監視**  
  - Joomla の管理画面ログ、LXD の `lxd.log`、FreightCo の PHP エラーログを集中管理し、異常な認証・ファイル書き換えイベントをアラート化。

### 3‑3. アクセス制御の見直し
- **最小権限の原則** を徹底し、LXD の `container edit` 権限は必要最小限のユーザーに限定。  
- **Zscaler Client Connector** の管理コンソールは **MFA** を必須化し、IP ホワイトリストで保護。  
- **4MOSAn GCB Doctor** のテストページは **外部からのアクセス不可** に設定（`Allow from 127.0.0.1` 等）。

### 3‑4. 緊急対応手順（インシデント発生時）
1. **対象システムのネットワーク切断**（特に LXD ホスト、ZCC エージェント）。  
2. **脆弱バージョンのプロセス停止**、直ちに **

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-77995

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-24T14:17:03.403 |

Joomla Extension - miniorange.com - Arbitrary account takeover in miniOrange OAuth Client < 3.2.0 - The manipulation of a cookie value allows actors to login as arbitrary accounts, including admins.

### CVE-2026-66897

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-23` |
| Published | 2026-08-24T10:16:39.767 |

A path traversal vulnerability in LXD's instance template processing allows an attacker with container edit permissions, or any user launching a crafted image, to overwrite arbitrary files on the host system as root. When processing target template paths specified in metadata.yaml, LXD validates the path against a confined os.Root directory handle but subsequently opens and creates the file using os.Create with an unconfined string path. This discrepancy between path resolution checks and file creation allows an attacker to escape directory confinement, overwrite root-owned host files, and achieve host root code execution.

### CVE-2026-66650

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-24T12:16:53.580 |

Unauthenticated PHP Object Injection in FreightCo <= 1.1.15 versions.

### CVE-2026-66648

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T12:16:53.433 |

Unauthenticated Privilege Escalation in Jawn <= 1.4.2 versions.

### CVE-2026-66587

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T12:16:52.837 |

Unauthenticated Local File Inclusion in WP Cafe Pro < 3.0.15 versions.

### CVE-2026-32558

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T12:16:51.877 |

Unauthenticated Privilege Escalation in Affiliate Pro - Affiliate Program for WooCommerce & WordPress <= 8.9.1 versions.

### CVE-2026-28165

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T12:16:50.600 |

Unauthenticated Privilege Escalation in Digits <= 9.2 versions.

### CVE-2026-67602

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-706` |
| Published | 2026-08-24T14:16:57.347 |

phpIPAM before 1.8.2 contains an authentication bypass vulnerability in the REST API that allows unauthenticated attackers to gain full API access by exploiting an insecure object cache keying mechanism. The cache is keyed by lookup value alone without including the searched column, enabling an entry written during an app_id lookup to satisfy a subsequent app_code lookup, allowing attackers to use the numeric database row identifier as an API token to read, write, and delete all IP address management records.

### CVE-2026-78365

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-24T13:19:19.247 |

Authorization Bypass Through User-Controlled Key in the supplier API in Roskus Prospero Flow CRM 4.0.0 through 5.3.1 allows any authenticated user to read and modify another company's supplier record, and to reassign it to their own company, via a PUT request to /api/supplier/{id} setting company_id in the body.

### CVE-2026-32551

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T12:16:51.733 |

Unauthenticated SQL Injection in Woo Essential <= 4.3.0 versions.

### CVE-2026-77994

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T08:16:33.807 |

Joomla Extension - joomlack.fr - Second order SQL injection in Page Builder CK < 3.6.5 - The Joomla extension Page Builder CK is vulnerable to a SQL injection issue related to the loadStyles method of the frontend page model.

### CVE-2026-78211

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T04:16:59.493 |

4MOSAn GCB Doctor developed by 4MOSAn Security Technology has a OS Command Injection vulnerability. Unauthenticated remote attackers can inject malicious commands through an unremoved ADOdb test page parameter, thereby executing arbitrary system commands on the server.

### CVE-2026-78167

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-24T02:17:04.300 |

A weakness has been identified in EFM ipTIME T16000M 14.20.2. The impacted element is the function httpcon_check_session_url of the component Session Validation Handler. This manipulation causes improper authentication. Remote exploitation of the attack is possible. The exploit has been made available to the public and could be used for attacks. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-78207

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-24T01:16:58.137 |

exceljs-hardened before 5.0.0 contains a prototype pollution vulnerability in the deepMerge helper that fails to reject __proto__, constructor, or prototype keys when merging note objects. Attackers can assign parsed JSON with a malicious __proto__ property to cell notes, modifying Object.prototype and affecting all plain objects created in the process.

### CVE-2026-78372

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T14:17:05.260 |

RansomLook does not consistently 
enforce authorization checks when accessing groups, markets, and ransom 
notes marked as private. An unauthenticated or otherwise unauthorized 
remote attacker can access information associated with private entities 
through several web views and API endpoints.


The affected functionality can 
disclose private group or market names, ransom-note content, and 
metadata associated with private groups. The /compare
 functionality can also be queried directly with the name of a private 
entity, allowing an unauthorized user to retrieve information such as 
post counts, mirror totals, and uptime even when the entity is excluded 
from the normal user interface. The patch explicitly adds a privacy 
check before returning this information. 


Ransom-note views, search results, 
and API endpoints were similarly missing consistent filtering. The fix 
introduces normalized private-group identifiers and alias handling, then
 rejects or filters notes associated with private groups before 
returning them to unauthorized callers.  


An attacker can exploit the issue 
remotely without authentication or user interaction, resulting in 
disclosure of information that was explicitly intended to be restricted 
to authorized users.

### CVE-2026-78370

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T14:17:05.100 |

RansomLook contains an authorization flaw in its legacy database export functionality that can allow unauthenticated remote users to retrieve information intended to remain private.

The /export/<database> endpoint permits selected internal databases to be exported without requiring authentication. While limited filtering is performed for some entity databases, other exportable databases are returned directly without consistently applying the application's private-entity access restrictions. As a result, information associated with groups, markets, posts, or other records marked as private may be included in an export accessible to an unauthenticated requester.

An attacker able to reach the RansomLook web application can request the affected export endpoint and retrieve data that should only be available to authorized users. Depending on the contents of the instance, this may disclose private ransomware intelligence, victim information, internal tracking data, or other information deliberately excluded from public views.

The patch removes the legacy unauthenticated export route and introduces centralized authorization handling that distinguishes ordinary authenticated API access from authorization to view private entries. API keys must now be explicitly granted private-data access, while existing keys do not automatically receive this privilege. The same private-data filtering is also applied consistently across API responses and database exports.

### CVE-2026-59568

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-24T14:16:56.210 |

Multiple vulnerabilities on affected versions of Zscaler Client Connector allow remote code execution, giving an unauthenticated, unprivileged user the ability to execute arbitrary code in the ZCC context.

### CVE-2026-59564

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-304` |
| Published | 2026-08-24T14:16:55.690 |

An authentication bypass issue exists in communications between affected versions of the Zscaler Client Connector and the Zscaler Client Connector Portal.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-19200

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-94;CWE-862` |
| Published | 2026-08-24T04:16:46.557 |

The Velociraptor verify() VQL function allows a user to verify an artifact for syntatic and other issues. Due to an implementation fault in this VQL function, the global artifact repository is used which allows callers to overwrite existing artifacts without the required permissions.  The attacker need only have the NOTEBOOK_EDIT permission (e.g. an analyst role) to be able to call this function.

### CVE-2026-78168

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-24T02:17:04.480 |

A security vulnerability has been detected in EFM ipTIME T24000M up to 14.20.0. This affects the function httpcon_check_session_url of the component Session Validation Handler. Such manipulation leads to improper authentication. The attack can be executed remotely. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-78376

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-24T14:17:05.390 |

A flaw was found in WebKitGTK. Processing malicious web content can cause a use-after-free issue due to improper memory handling and result in memory corruption.

### CVE-2026-78369

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-24T14:17:04.910 |

RansomLook contains a missing authentication vulnerability in the /admin/crypto/group/new endpoint. While the endpoint provides an administrative function for creating new crypto group entries, it was not protected by the application's authentication mechanism.

An unauthenticated remote attacker able to access the RansomLook web interface could therefore submit requests to this endpoint and create crypto group entries without possessing a valid authenticated session or administrative credentials.

Successful exploitation allows an attacker to make unauthorized modifications to data that should only be manageable by authenticated administrators. Depending on how crypto group information is subsequently consumed by RansomLook, malicious or fraudulent entries could also affect the integrity of information presented or processed by the application.

The vulnerability is addressed by applying the flask_login.login_required decorator to the /admin/crypto/group/new route, ensuring that only authenticated users can access the functionality.

### CVE-2026-76842

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T14:17:01.930 |

The Mercado Pago Node.js SDK interpolates caller-supplied identifiers into API request paths without percent-encoding them, so characters that are structural in a URL survive into the outgoing request. The payment (get, capture, cancel), paymentRefund (create, total, list, get), advancedPayment (get, capture, cancel, update, updateReleaseDate) and disbursementRefund (create, createAll, listAll) clients build their path as a template literal, for example RestClient.fetch(`/v1/payments/${id}`, ...) in src/clients/payment/get/index.ts. A dot-dot or slash sequence in the identifier is normalised by the WHATWG URL parser and redirects the request to a different endpoint, and a question mark appends attacker-chosen query parameters, in both cases carrying the merchant's own access token. An application that forwards an identifier influenced by an untrusted party into one of these methods without an ownership check therefore allows that party to reach other resources within the merchant's token scope. The repository already contains the intended helper, encodePathParam in src/utils/path.ts, which pull request 451 applied to roughly 29 other clients while leaving these unchanged.

### CVE-2026-59567

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-280` |
| Published | 2026-08-24T14:16:56.080 |

Multiple vulnerabilities on affected versions of Zscaler Client Connector allow local privilege escalation, giving an unprivileged user the ability to execute arbitrary code in a privileged context.

### CVE-2026-59565

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-229` |
| Published | 2026-08-24T14:16:55.830 |

A remotely exploitable buffer overflow bug can cause a local and kernel denial-of-service attack on affected versions of Zscaler Client Connector on Windows.

### CVE-2026-78317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T10:16:40.810 |

SQL Injection in Delta DIAEnergie v1.11.00.002 allows attacker to 
remote code execution.

### CVE-2026-78316

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T10:16:40.667 |

SQL Injection in Delta DIAEnergie v1.11.00.002 allows attacker to 
remote code execution.

### CVE-2026-78315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T10:16:40.510 |

SQL Injection in Delta DIAEnergie v1.11.00.002 allows attacker to 
remote code execution.

### CVE-2026-78314

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T10:16:40.370 |

SQL Injection in Delta DIAEnergie v1.11.00.002 allows attacker to 
remote code execution.

### CVE-2026-78386

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-24T14:17:06.090 |

RansomLook exposed sensitive operator-side scraping configuration through multiple unauthenticated API responses. Location records associated with ransomware groups and markets were returned largely verbatim to unauthenticated callers whenever the location itself was not marked as private.


These records could contain internal fields such as header, which may include authentication headers, session cookies, or other credentials used to access monitored websites; init_script, which may contain logic used to bypass CAPTCHA, anti-bot protections, or paywalls; and browser, which discloses details about the scraping environment.


An unauthenticated remote attacker could query the affected API endpoints and obtain these values. Leaked authentication material could potentially be replayed against the monitored service, while disclosure of scraping and bypass logic could allow site operators or other attackers to identify and defeat RansomLook's collection mechanisms.


The patch introduces an explicit allowlist of fields permitted in public location records and strips all operator-side fields before returning data to unauthenticated users.


The accompanying change from <string:postname> to <path:postname> appears to be a functional correction allowing legitimate post titles containing / and does not, based on this patch alone, represent the security issue.

### CVE-2026-78380

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T14:17:05.667 |

RansomLook fails to enforce the privacy status of ransomware groups and markets when distributing newly collected victim posts to external notification channels. The post-processing logic checks whether an individual post is marked private but does not verify whether the group or market to which the post belongs is configured as private.

As a result, newly parsed victim information associated with a private group or market may be automatically published through enabled Rocket.Chat, Mastodon, Bluesky, and e-mail notification channels despite the entity being explicitly configured to prevent public disclosure.

A similar issue affects the public MISP feed. The feed previously determined privacy using groupinfo(), which only queries the group database. Consequently, victim information associated with private markets could be added to the public MISP feed because the corresponding market privacy flag was not evaluated.

An attacker or other unauthorized party able to access these public notification channels or the MISP feed may obtain victim information that was intended to remain private. Depending on the collected data, this may disclose victim names, ransomware activity, incident information, or other information associated with privately monitored groups and markets.

The fix introduces a common is_private_entity() check covering both groups and markets and prevents private entity posts from being distributed through external notification channels or the public MISP feed. Internal storage and dashboard alerting remain unaffected.

### CVE-2026-76848

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T14:17:03.013 |

TypeORM's SelectQueryBuilder.distinctOn accepts an array of strings and stores it on the expression map without validation. For PostgreSQL-family drivers, createSelectDistinctExpression in src/query-builder/SelectQueryBuilder.ts joins that array and interpolates the result into the generated statement as SELECT DISTINCT ON (values), with no escaping, quoting, identifier validation or allowlist, and without routing the values through replacePropertyNames or the driver's escape helper. Because the interpolation point is a parenthesized SQL expression list rather than an identifier-only position, a supplied element may carry arbitrary expressions, including correlated subqueries. An application that forwards a client-controlled value into distinctOn, for instance to let a caller choose a deduplication column, allows that client to read data anywhere the application's database role can reach through boolean or time-based inference, independently of the entity being queried. validateOrderByCondition, the allowlist check guarding the orderBy family in the same class, is not applied to this path.

### CVE-2026-76847

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321;CWE-862` |
| Published | 2026-08-24T14:17:02.857 |

act starts an HTTP Artifacts V4 backend whenever a workflow uses actions/upload-artifact@v4 or actions/download-artifact@v4. The control-plane RPCs of that backend, including CreateArtifact, GetSignedArtifactURL, ListArtifacts, FinalizeArtifact and DeleteArtifact, accept a caller-supplied workflow_run_backend_id and never check that it belongs to the requester: validateRunIDV4 in pkg/artifacts/artifacts_v4.go parses the value and returns it with the comparison against the requesting task's run ID left commented out. The signed URLs the backend issues are authenticated by an HMAC whose key is hardcoded to the four bytes 0xba 0xdb 0xee 0xf0, identical in every build, computed over a concatenation of endpoint, expiry, artifact name and task ID with no length prefix or delimiter, so signatures are both forgeable and ambiguous between differing artifact name and task ID pairs. The --artifact-server-addr flag defaults to the host's outbound address rather than loopback, leaving the backend reachable from the surrounding network. Any client that can reach it may read, overwrite or delete the artifacts of a concurrently running job with no credentials, exposing build outputs such as secrets and deployment credentials and permitting their replacement before the owning job consumes them.

### CVE-2026-76841

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-24T14:17:01.760 |

Xinference loads models with Hugging Face remote code execution unconditionally enabled, and before version 2.12.0 exposes no setting to disable it. Six loader call sites pass trust_remote_code=True as a literal or as an unconditional default: RerankModel._get_tokenizer in xinference/model/rerank/core.py, SentenceTransformerRerankModel.load in xinference/model/rerank/sentence_transformers/core.py, SentenceTransformerEmbeddingModel.load in xinference/model/embedding/sentence_transformers/core.py, FlagEmbeddingModel.load in xinference/model/embedding/flag/core.py, and two sites in xinference/model/llm/transformers/core.py where PytorchModel._sanitize_model_config and PytorchModel._get_components default the value to True. Because a caller with model launch access can register a model whose type is unknown and supply an arbitrary model path, the server reaches _auto_detect_type and then AutoTokenizer.from_pretrained, which imports and executes Python declared by the model directory's own tokenizer_config.json auto_map, running attacker-supplied code with the privileges of the worker process. Version 2.12.0 gates every site behind allow_trust_remote_code and the XINFERENCE_TRUST_REMOTE_CODE setting, permitting remote code only for bundled built-in models.

### CVE-2026-78255

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-24T08:16:33.967 |

The HTTP media server running on DJI drones serves stored photos and videos through the `/v2` endpoint without authenticating the requesting client. Filenames follow a predictable pattern, allowing an attacker who joins the drone's internal network to enumerate valid filenames and exfiltrate stored photos and videos. The exposed media may reveal sensitive information, including private locations, property, travel history, identifiable individuals, and the operator's routines.

Affected models are DJI Neo until 01.00.0400, DJI Neo 2 until 01.00.0500, DJI Flip until 01.00.1200, DJI Air 3 until 01.00.1600, DJI Air 3S until 01.00.1400, DJI Avata 2 until 01.00.0400, DJI Avata 360 until 01.00.0300, DJI Mavic 3 until 01.00.1400, DJI Mavic 3 Classic until 01.00.0800, DJI Mavic 3 Pro until 01.01.0700, DJI Mavic 4 Pro until 01.00.0500, DJI Mini 2 until 01.07.0200, DJI Mini 3 until 01.00.0500, DJI Mini 3 Pro until 01.00.0900, DJI Mini 4 Pro until 01.00.1100, and DJI Mini 5 Pro until 01.00.0600.

### CVE-2026-78212

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-24T04:16:59.660 |

4MOSAn developed by 4MOSAn Security Technology Co., Ltd. has an Arbitrary File Read vulnerability. Unauthenticated remote attackers can exploit a Relative Path Traversal flaw to download arbitrary system files.

### CVE-2026-78208

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-24T01:16:58.280 |

exceljs-hardened before 5.0.0 contains a path traversal vulnerability in the Workbook.addImage() function that fails to validate file paths. Attackers can supply arbitrary file paths to read any file accessible to the Node.js process and embed it in the generated workbook.

### CVE-2026-78206

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-24T01:16:57.973 |

exceljs-hardened before 5.0.0 decompresses all entries from supplied xlsx archives into memory without limits on entry size, total size, or compression ratio. Attackers can upload highly compressed workbooks that expand to gigabytes in memory, exhausting available resources and causing denial of service.

### CVE-2026-32477

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T12:16:51.473 |

Unauthenticated Arbitrary File Deletion in ShopBuilder Pro – Elementor WooCommerce Builder Addons <= 2.2.0 versions.

### CVE-2026-28171

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T12:16:50.970 |

Unauthenticated Arbitrary File Deletion in WooCommerce File Approval <= 10.7 versions.

### CVE-2026-78169

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-24T02:17:04.650 |

A vulnerability was detected in UTT HiPER 1250GW up to 3.2.7-210907-180535. This impacts the function strcpy of the file /goform/aspRemoteApConfTempSend of the component HTTP Request Handler. Performing a manipulation of the argument Profile results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is now public and may be used.

### CVE-2026-76840

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-787` |
| Published | 2026-08-24T14:17:01.550 |

RustDesk's Windows clipboard redirection copies a peer-supplied length into a fixed-size caller buffer without an upper bound check. When an OLE paste consumer such as explorer.exe calls IStream::Read with a buffer of cb bytes, CliprdrStream_Read in libs/clipboard/src/windows/wf_cliprdr.c requests that many bytes of a remote file through cliprdr_send_request_filecontents and then executes CopyMemory(pv, clipboard->req_fdata, clipboard->req_fsize), where req_fsize is taken verbatim from the peer's CLIPRDR FileContentsResponse by wf_cliprdr_server_file_contents_response (req_fsize = fileContentsResponse->cbRequested) and is never clamped to cb anywhere in the chain. The function's only length comparison, req_fsize < cb, handles the short-read case and is evaluated after the copy has already occurred. A malicious or compromised peer that answers a small file-contents read with an oversized response therefore writes attacker-chosen data past the end of the paste consumer's heap buffer when the local user pastes clipboard file contents offered by the remote side. The file is a fork of FreeRDP's client/Windows/wf_cliprdr.c, where the same defect is CVE-2026-68579, fixed in FreeRDP 3.30.0.

### CVE-2026-32478

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T12:16:51.607 |

Subscriber SQL Injection in WP Project Manager Pro <= 4.0.1 versions.

### CVE-2026-32471

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T12:16:51.210 |

Subscriber SQL Injection in ProLancer Element <= 1.4.8 versions.

### CVE-2025-63080

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-24T12:16:47.937 |

Firmware in KAON PG5298A and PG5298B routers allow an authenticated user to send crafted JSON-RPC requests and perform operations not possible via GUI, e.g. system file read or command execution.   
This vulnerability has been fixed in firmware version: 3.0.82 for PG5298A and 4.0.82 for PG5298B.

### CVE-2026-78306

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-24T09:16:47.200 |

DJI drones expose an unauthenticated DUML command interface over Bluetooth that allows an attacker within Bluetooth range to modify Wi-Fi configuration parameters, including the SSID, PSK, MAC address, regulatory country code, and wireless channel. An attacker can overwrite the Wi-Fi PSK with a known value and connect to the drone's internal Wi-Fi network, potentially gaining access to the flight control interface and issuing flight commands. Crafted DUML commands can also disable or restart the Wi-Fi and Bluetooth interfaces, disconnect Wi-Fi clients, or reset wireless configuration, resulting in a denial-of-service condition that can disrupt the operator's wireless control, video, and telemetry connections during flight.

Affected models are DJI Neo until 01.00.0400, DJI Neo 2 until 01.00.0500, DJI Flip until 01.00.1200, DJI Air 3 until 01.00.1600, DJI Air 3S until 01.00.1400, DJI Avata 2 until 01.00.0400, DJI Avata 360 until 01.00.0300, DJI Mavic 3 until 01.00.1400, DJI Mavic 3 Classic until 01.00.0800, DJI Mavic 3 Pro until 01.01.0700, DJI Mavic 4 Pro until 01.00.0500, DJI Mini 2 until 01.07.0200, DJI Mini 3 until 01.00.0500, DJI Mini 3 Pro until 01.00.0900, DJI Mini 4 Pro until 01.00.1100, and DJI Mini 5 Pro until 01.00.0600.


Remediation requires a firmware update from the vendor.

### CVE-2026-76843

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-24T14:17:02.087 |

The official Flair wheels for 0.15.0 and 0.15.1 still contain flair/models/clustering.py, whose ClusteringModel.load static method returns pickle.loads(joblib.load(str(model_file))) and so executes arbitrary Python while loading a model file. Loading a model supplied by an attacker therefore runs that attacker's code with the privileges of the loading process. This is the same sink and the same file as CVE-2024-10073, which records 0.15.0 as the fixed version on the basis that clustering support was dropped in that release; the module was removed from the documented API but remains present in the distributed artifact and reachable by importing flair.models.clustering directly, so the earlier record's fixed version does not hold for the shipped package.

### CVE-2026-59566

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-229` |
| Published | 2026-08-24T14:16:55.940 |

A locally exploitable buffer overflow bug can cause a local denial-of-service attack on affected versions of Zscaler Client Connector on Android and ChromeOS.

### CVE-2026-59561

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T05:16:55.090 |

Sakura Editor provided by Sakura Editor Development Community contains an OS command injection vulnerability. If a victim user is directed to edit a file in a crafted directory, arbitrary OS command may be executed on the user's PC when the user invokes "Open Terminal".

### CVE-2026-78209

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1236` |
| Published | 2026-08-24T01:16:58.423 |

exceljs-hardened versions before 5.0.0 fail to neutralize leading equals, plus, minus, or at signs in cell values written to CSV output. Attackers who can influence exported cell values can inject formulas that execute when the CSV file is opened in a spreadsheet application, potentially exfiltrating data or performing other malicious actions.

### CVE-2026-76844

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T14:17:02.250 |

webpack-dev-middleware resolves a request to a local file in getFilenameFromUrl by testing the request pathname against a traversal guard and then slicing it at a fixed character offset. The guard, UP_PATH_REGEXP applied to path.normalize(`./${pathname}`), only matches ".." that stands as a whole path segment, while the containment test is the string comparison pathname.startsWith(publicPathPathname) and the file path is built as path.join(outputPath, pathname.slice(publicPathPathname.length)). When the configured publicPath has no trailing slash, a request such as GET /assets../.env against publicPath /assets yields the pathname /assets../.env, whose only dot-dot sits inside the segment "assets.." and so passes the guard, but the offset slice cuts within that segment and hands "../.env" to path.join, resolving one directory above outputPath. Reading a file from that path requires the middleware to be backed by the physical filesystem, which happens when writeToDisk is true or a custom outputFileSystem is supplied, since the default memfs volume holds only build output. Traversal depth is limited to a single directory because a separately delimited dot-dot segment is collapsed during URL parsing before the guard runs. The default publicPath value of "auto" resolves to "/" and is not affected. This is an incomplete fix for CVE-2024-29180: the guard and offset slice were introduced by that fix and are present in every release from 5.3.4, 6.1.2 and 7.1.0 onward.

### CVE-2026-10582

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-24T11:16:38.233 |

Hugo's security.http.urls allowlist is the only control on outbound fetches made by resources.GetRemote, and it inspects the URL text alone. CheckAllowedHTTPURL in config/security/securityConfig.go applies the configured pattern list and then re-checks a canonicalised form of an integer, hex or octal IPv4 host, but it never resolves the hostname and never inspects the address the HTTP client actually connects to. The client constructed in resources/resource_factories/create/create.go installs no dial-time hook, so no check occurs at connection time either. A hostname that resolves to a loopback, private or cloud-metadata address therefore satisfies the policy, and the response body is embedded in the generated site. An attacker who can supply a URL through content, for example a front-matter field or a CMS field, can make the build fetch an internal endpoint and publish the response in the static output, so the build artifact itself carries the data out.

### CVE-2026-78385

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-24T14:17:05.940 |

RansomLook contains insufficient resource validation in the analysis PDF generation functionality. Analysis documents are converted from Markdown to HTML and passed to WeasyPrint for PDF rendering. Prior to the fix, WeasyPrint used its default URL fetcher, allowing resource references contained in an analysis to be resolved without restrictions.

An authenticated attacker able to create or modify an analysis could embed crafted resource references using schemes such as file:// or http://. When the analysis was subsequently rendered as PDF, WeasyPrint would process these references with the privileges and network access of the RansomLook server.

A malicious file:// reference could cause the renderer to access arbitrary files readable by the RansomLook process, potentially exposing sensitive configuration, credentials, or other local data through rendered resources. Network URLs could cause the server to initiate requests to localhost, internal network services, or external systems, resulting in server-side request forgery (SSRF) and potentially bypassing network-level access restrictions.

The patch introduces a dedicated WeasyPrint URL fetcher that permits only data: resources, the RansomLook report logo, and files contained within the analysis asset directory. Network resources and filesystem paths outside these explicitly permitted locations are rejected.

### CVE-2026-78381

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T14:17:05.807 |

RansomLook contains a path traversal vulnerability in the handling of the screen field associated with group posts. The GroupPost.get API handler concatenates the database-controlled screen value directly with the application's source/ directory and opens the resulting path without verifying that the resolved file remains within the intended directory.

Because the screen field is free-form and can be populated either through the administrative post editor or through data imported from a remote RansomLook instance, a malicious upstream instance can provide traversal sequences such as ../config/generic.json. When the affected post is subsequently retrieved through the API, RansomLook resolves and reads the attacker-controlled path and returns the contents of the referenced file Base64-encoded in the API response.

This can allow an attacker (being admin) controlling imported post data to read arbitrary files accessible to the RansomLook process, potentially exposing sensitive configuration data, API credentials, password hashes, or other application secrets. The attack does not require the malicious upstream to possess an account on the affected RansomLook instance.

The vulnerability is addressed by resolving screen paths with os.path.realpath() and verifying that the resolved path remains beneath the application's source/ directory. Validation is performed both when values are written and immediately before files are read. Using canonical paths also prevents traversal through symbolic links that would bypass purely lexical path normalization checks.

### CVE-2026-66671

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T12:16:53.880 |

Unauthenticated Local File Inclusion in Verdure Core <= 1.2 versions.

### CVE-2026-66670

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T12:16:53.730 |

Unauthenticated Local File Inclusion in Måne <= 1.7 versions.

### CVE-2026-28152

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T12:16:50.220 |

Unauthenticated Local File Inclusion in Tonda Core < 2.6 versions.

### CVE-2026-28151

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T12:16:50.083 |

Unauthenticated Local File Inclusion in Tonda < 2.6 versions.

### CVE-2026-78270

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T12:16:55.043 |

Author SQL Injection in FluentCRM Pro <= 3.1.12 versions.

### CVE-2026-66585

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-24T12:16:52.693 |

Unauthenticated Sensitive Data Exposure in WP Cafe Pro < 3.0.15 versions.

### CVE-2026-28167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T12:16:50.850 |

Unauthenticated Arbitrary File Download in Super Forms <= 6.3.315 versions.

### CVE-2026-28153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T12:16:50.347 |

Unauthenticated Broken Access Control in Notification Master &#8211; Real-Time WordPress Notifications With Email, SMS, Webhooks &amp; More <= 1.7.1 versions.

### CVE-2026-76172

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-177` |
| Published | 2026-08-24T11:16:40.723 |

fast-uri is a URI parser for Node.js. During parsing it runs a legacy decoding pass over the scheme component and never re-escapes the result, and serialization writes the scheme back out verbatim, unlike the host component which is re-escaped. As a result an input whose scheme carries percent-encoded slashes parses as a scheme with no authority, so the parsed host and error are both undefined, yet resolving or normalizing that same input emits a network-path reference whose authority is attacker-chosen and re-parses to that host. An application that allowlists on the parsed host, or treats a reference with no authority as safe to resolve against its base, gets the opposite of what it checked, giving an off-site redirect, server-side request forgery, or address-policy bypass. The legacy decoder also expands non-standard escape forms, widening the issue past upstream filters, and control characters in the scheme can reach the output as raw carriage return and line feed. The affected versions are 2.3.1 up to but not including 2.4.5, 3.0.0 up to but not including 3.1.6, and 4.0.0 up to but not including 4.1.3. The issue is fixed in 2.4.5, 3.1.6, and 4.1.3, which reject a scheme that is not valid after decoding. Users should upgrade to a patched version.

### CVE-2026-75975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-20;CWE-918` |
| Published | 2026-08-24T10:16:40.237 |

fast-uri is a URI parser for Node.js. Its custom parser for bracketed IPv6 literals does not validate the complete IPv6 grammar, so invalid trailing text in an authority can be silently discarded and a malformed attacker-controlled host is turned into a different valid IPv6 destination. For example, a bracketed literal with invalid trailing characters is normalized to the unspecified address, which a Node HTTP client then connects to a local service over loopback, and other malformed literals collapse to private-range addresses. No error is set on the parsed result, so an application checking the error field cannot detect the rewrite. An application that normalizes untrusted URLs before outbound requests, redirects, proxy routing, or address-policy enforcement can be redirected to a local or private IPv6 target, giving a server-side request forgery and address-policy bypass primitive. The affected versions are 2.3.1 up to but not including 2.4.5, 3.0.0 up to but not including 3.1.6, and 4.0.0 up to but not including 4.1.3. The issue is fixed in 2.4.5, 3.1.6, and 4.1.3, which validate bracketed IP literals against the full grammar and mark malformed literals as authority errors. Users should upgrade to a patched version.

### CVE-2026-75931

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-436` |
| Published | 2026-08-24T10:16:40.113 |

fast-uri is a URI parser for Node.js. It canonicalizes a host to its ASCII form only when the input carries an explicit scheme, so a scheme-relative reference such as a host preceded by two slashes is returned with its host verbatim and no error set. As a result fast-uri's own entry points disagree with each other: parse, resolve, normalize, and equal can yield different hosts for the same input depending only on whether a scheme is written out, and equal can return opposite verdicts for the same pair of hosts. An application that extracts a host with fast-uri to check it against a policy list and then resolves the same reference can make its decision on one host while the destination is another, enabling host confusion and policy bypass. The affected versions are 2.4.2 up to but not including 2.4.5, 3.1.3 up to but not including 3.1.6, and 4.0.1 up to but not including 4.1.3. The issue is fixed in 2.4.5, 3.1.6, and 4.1.3, which canonicalize the host consistently across the resolve path. Users should upgrade to a patched version.

### CVE-2026-75899

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-174;CWE-918` |
| Published | 2026-08-24T10:16:39.960 |

fast-uri is a URI parser for Node.js. It decodes percent escapes in a hostname during parsing and then decodes the parsed hostname a second time during authority recomposition, so a single call to normalize or resolve can turn nested percent-encoded input into a different network destination such as a loopback hostname or address. For example, a doubly encoded host that spells out a loopback name decodes to that live host in one operation, which contradicts RFC 3986 section 2.4 that an implementation must not decode the same string more than once. An application that normalizes or resolves an untrusted HTTP-family URI before outbound routing, redirect validation, or a host-policy check can receive a destination different from the one the original encoded host represented, giving a server-side request forgery and host-policy bypass primitive. This is an incomplete-fix variant of CVE-2026-6322. The affected versions are 2.4.1 up to but not including 2.4.5, 3.1.2 up to but not including 3.1.6, and 4.0.0 up to but not including 4.1.3. The issue is fixed in 2.4.5, 3.1.6, and 4.1.3, which normalize percent escapes once and preserve encoded percent signs. Users should upgrade to a patched version.

### CVE-2026-21751

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1240` |
| Published | 2026-08-24T14:16:52.170 |

HCL Hive is affected by a cryptographic primitive with a risky implementation which could allow an attacker unauthorized lateral compromise or widespread credential leakage if a single internal component is breached.

### CVE-2026-78170

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-08-24T02:17:04.817 |

A flaw has been found in UTT HiPER 1200GW up to 2.5.3-170306. Affected is the function strcpy of the file /goform/formConfigFastDirectionW. Executing a manipulation of the argument ssid can lead to buffer overflow. The attack may be performed from remote. The exploit has been published and may be used.

### CVE-2026-21756

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T13:17:32.477 |

HCL Hive is affected by a broken access control vulnerability which could allow an attacker or unauthorized user to introduce unverified, malicious, or broken code directly into production environments.

### CVE-2026-6017

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-24T12:16:54.030 |

Firmware in KAON PG5298A and PG5298B routers allow an unauthenticated user to query a specific endpoint and acquire sensitive information such as a password to the administrative portal.   
This vulnerability has been fixed in firmware version: 3.0.82 for PG5298A and 4.0.82 for PG5298B.

### CVE-2026-66623

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:53.270 |

Unauthenticated Cross Site Scripting (XSS) in Social Media & Share Icons <= 2.9.9 versions.

### CVE-2026-66610

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:53.127 |

Unauthenticated Cross Site Scripting (XSS) in Urna <= 2.6.2 versions.

### CVE-2026-66599

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:52.980 |

Unauthenticated Cross Site Scripting (XSS) in WPComplete <= 2.9.5.6 versions.

### CVE-2026-66584

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:52.543 |

Unauthenticated Cross Site Scripting (XSS) in 12 Step Meeting List <= 3.19.16 versions.

### CVE-2026-32476

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:51.340 |

Unauthenticated Cross Site Scripting (XSS) in Brave Conversion Engine (PRO) <= 0.8.6 versions.

### CVE-2026-28190

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T12:16:51.093 |

Subscriber Broken Access Control in ProLancer Element <= 1.4.8 versions.

### CVE-2026-28166

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:50.723 |

Unauthenticated Cross Site Scripting (XSS) in Tourmaster <= 5.4.9 versions.

### CVE-2026-28162

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T12:16:50.473 |

Unauthenticated Cross Site Scripting (XSS) in Events Made Easy <= 3.2.5 versions.

### CVE-2026-78203

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-24T01:16:57.530 |

Ghostwriter before 7.1.2 fails to validate template ownership in the report template swap endpoint, allowing attackers to attach client-scoped templates from other clients to their own reports. Attackers can exploit sequential template primary keys to enumerate and attach foreign templates, then generate reports to disclose template contents including letterhead, boilerplate, and methodology text.

### CVE-2026-78367

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-24T14:17:04.767 |

A flaw was found in rpmbuild. When rpmbuild processes a crafted tarball in tarball mode, a specially designed tar member name can lead to macro injection. This vulnerability allows a remote attacker to execute arbitrary code on the system by convincing a user to build a malicious tarball.
