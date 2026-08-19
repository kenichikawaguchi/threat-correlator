# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-19 15:01 UTC
- **対象期間**: `2026-08-18T15:00:30.000Z` 〜 `2026-08-19T15:01:33.000Z`
- **重要CVE数**: 956 件（Critical 9.0+: 209 件 / High 7.0〜: 747 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件以上** と非常に多く、特に **Joomla 系プラグイン、WordPress プラグイン、IoT デバイス、Oracle Fusion Middleware 系製品** に集中しています。共通する特徴は **認証不要でリモートからコード実行が可能** になる点で、攻撃者は単一の HTTP リクエストだけで管理権限取得や情報漏洩を実現できるケースが目立ちます。  

---

## 2. 特に注目すべき CVE  

| CVE | 製品 / コンポーネント | 主な脆弱性 | 影響範囲・リスク |
|-----|----------------------|------------|-------------------|
| **CVE‑2026‑67364** | Joomla! Extension **Balbooa Forms** (< 2.4.3.2) | 任意コード実行 (PHP `eval()` にカスタム post‑handler がそのまま渡される) | 認証不要で任意 PHP が実行でき、サーバ全体の権限取得が可能。Joomla を利用している多数のサイトが対象。 |
| **CVE‑2026‑74803** | Joomla! Extension **YooTheme Zoo** (< 4.1.64) | 任意ファイルアップロード (MIME 判定バイパス) | 画像アップロード機能を悪用し、任意のスクリプトやシェルを配置できる。Web ルート直下に配置すれば即 RCE。 |
| **CVE‑2026‑73343** | WordPress Plugin **WP Compress** (< 7.20.01) | 未認証リモートコード実行 | プラグインの内部 API が入力を検証せずに `eval()` へ渡すため、任意 PHP が実行できる。WordPress サイト全般に波及。 |
| **CVE‑2026‑76008** | IoT デバイス **Comfast CF‑N1‑S** (ファームウェア 2.6.0.1) | スタックベースバッファオーバーフロー ( `/cgi-bin/mbox-config` の `get_para_from_uri` ) | リモートから任意サイズの `width/height` パラメータでスタック破壊、コード実行が可能。組み込み系デバイスはアップデートが遅れがちで危険度が高い。 |
| **CVE‑2026‑70880** | Oracle Hyperion **Data Relationship Management** (11.2.25.0.000) | 未認証 RCE (TCP/HTTP 経由) | Oracle 製品は企業基幹システムの一部であり、侵入すると財務データ改ざんや内部ネットワーク横移動が容易になる。 |

> **選定理由**  
> - **CVSS が 10.0**（最高評価）で、かつ **認証不要** のリモートコード実行が可能。  
> - **広範な利用者層**（Joomla/WordPress のプラグインは数千サイト、Oracle 製品は大企業の基幹系、IoT デバイスは社内ネットワークに常駐）に影響。  
> - **修正パッチが既に公開** されているか、ベンダーが緊急対応を表明している点で、速やかな対策が求められる。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 | 現行脆弱バージョン | 推奨バージョン | アップデート手順 |
|------|-------------------|----------------|-------------------|
| **Balbooa Forms** (Joomla) | `< 2.4.3.2` | **≥ 2.4.3.2** | Joomla 管理画面 → 「拡張機能」→「インストール」→最新パッケージをアップロード、または Composer (`composer require balbooa/forms:^2.4.3.2`) |
| **YooTheme Zoo** (Joomla) | `< 4.1.64` | **≥ 4.1.64** | 同上、公式サイトから最新版 ZIP を取得し上書きインストール |
| **WP Compress** (WordPress) | `< 7.20.01` | **≥ 7.20.01** | WordPress 管理画面 → 「プラグイン」→「更新」または `wp plugin update wp-compress` |
| **Comfast CF‑N1‑S** (IoT) | 2.6.0.1 | **ベンダー提供の最新ファームウェア** (執筆時点で 2.6.0.3 がリリース) | デバイス管理コンソール → 「ファームウェア更新」→最新イメージをアップロード。更新前に設定バックアップを取得。 |
| **Oracle Hyperion Data Relationship Management** | 11.2.25.0.000 | **≥ 11.2.25.0.001** (Oracle Critical Patch Update) | Oracle My Oracle Support (MOS) から Patch Set Update (PSU) を取得し、`OPatch` で適用。適用後は必ずサービス再起動。 |

### 3.2 直ちに実施すべき防御策
1. **外部からの直接アクセスを遮断**  
   - Joomla / WordPress の管理画面、プラグインのエンドポイント (`/index.php?option=com_zoo…`, `/wp-admin/admin-ajax.php`) への IP 制限または VPN 経由のみ許可。  
   - IoT デバイスは管理用 CGI (`/cgi-bin/mbox-config`) をファイアウォールで内部ネットワーク限定にする。  

2. **Web アプリケーションファイアウォール (WAF) の導入・チューニング**  
   - `Content‑Type` ヘッダーの MIME バイパスや `eval` 呼び出しパラメータを検知するルールを追加。  
   - Oracle 製品は `Oracle Web Application Firewall` で `POST` データのサイズ上限と不正文字列をブロック。  

3. **ログ監視とインシデント対応体

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-74803

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-19T14:17:39.487 |

Joomla Extension - yootheme.com - Unauthenticated arbitrary file upload in Zoo < 4.1.64 - The image element accepts arbitrary files when the client-supplied Content-Type falls within the image MIME group.

### CVE-2026-67364

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T13:17:50.957 |

Joomla Extension - balbooa.com - Pre-auth PHP Code Injection in Balbooa Forms < 2.4.3.2 - CWE-94 / CWE-95 | CVSS 3.1: 9.8 Critical (AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)
The form's optional custom-PHP post-submission handler is executed via eval(). The [URL parameter = X] shortcode is substituted with the raw, unescaped value of a query parameter, letting an unauthenticated attacker inject arbitrary PHP that executes server-side. The CSRF token needed to reach the endpoint is itself disclosed anonymously via a separate task, so it provides no real protection. Exploitability requires the form to have a custom-PHP handler configured (a documented builder feature) referencing that shortcode, and no reCAPTCHA on the submit button.

### CVE-2026-76008

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T03:16:53.077 |

A flaw has been found in Comfast CF-N1-S 2.6.0.1. This affects the function get_para_from_uri of the file /cgi-bin/mbox-config of the component URI Parameter Parsing. This manipulation of the argument width/height causes stack-based buffer overflow. The attack can be initiated remotely.

### CVE-2026-70921

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:49.927 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 10.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70880

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.490 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61241

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.467 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 10.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-73343

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T15:17:02.943 |

Unauthenticated Remote Code Execution (RCE) in WP Compress < 7.20.01 versions.

### CVE-2026-73930

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:26.003 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-71059

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.743 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Service API).  Supported versions that are affected are 8.2.0.0.0 and  26.1.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via SOAP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70920

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:49.810 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62608

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.300 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows low privileged attacker with network access via CORBA to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62588

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.003 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62512

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:04.933 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62452

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:01.840 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-61317

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:59.737 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61248

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.597 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Internet Directory.  While the vulnerability is in Oracle Internet Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61206

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.020 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61066

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:54.043 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via RMI to compromise Oracle Identity Manager.  While the vulnerability is in Oracle Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61021

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.607 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61003

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.760 |

Vulnerability in the Oracle Managed File Transfer product of Oracle Fusion Middleware (component: MFT Runtime Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Managed File Transfer.  While the vulnerability is in Oracle Managed File Transfer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Managed File Transfer. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60995

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.153 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via TLS to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60990

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.567 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via TLS to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60916

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:47.590 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  While the vulnerability is in Oracle WebCenter Enterprise Capture, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Enterprise Capture accessible data as well as  unauthorized read access to a subset of Oracle WebCenter Enterprise Capture accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-60730

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.987 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60720

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.140 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  While the vulnerability is in Oracle Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60702

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.660 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.9 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-55166

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-285;CWE-639;CWE-918` |
| Published | 2026-08-18T19:16:58.783 |

Lemur manages TLS certificate creation. Prior to 1.9.2, authenticated users could influence an ACME authority acme_url without an effective server-side destination restriction and trigger AcmeHandler.setup_acme_client to make backend requests. An attacker could target cloud instance metadata or internal services from Lemur network context, potentially obtaining credentials available to the host. The advisory also identifies creator-equality authorization behavior that could preserve access to certificate key material after ownership or role changes, with insufficient export_private_key audit context to distinguish that access path. Together, the acme_url server-side request forgery and authorization weakness could expose cloud credentials and long-lived PKI private-key access. The fix adds ACME_DIRECTORY_HOST_ALLOWLIST validation and enriches key-export audit events with creator and current-owner context. This issue is fixed in version 1.9.2.

### CVE-2026-66780

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T18:19:23.940 |

A flaw was found in the submariner-operator component. The `submariner-k8s-broker-cluster` Role, which is assigned to joined clusters, possesses excessive permissions. This allows a compromised cluster to alter network configurations, specifically by overwriting other clusters' endpoint information. Consequently, an attacker can redirect inter-cluster tunnel traffic, enabling a Man-in-the-Middle (MITM) attack across the entire cluster mesh.

### CVE-2026-66627

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T15:16:57.563 |

Contributor Arbitrary File Upload in GP Premium <= 2.5.5 versions.

### CVE-2026-32474

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T15:16:53.083 |

Contributor Arbitrary File Upload in Templatiq <= 0.2.5 versions.

### CVE-2026-16019

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:27.093 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Faydam Innovation Inc. FAYDAM Datalogger allows SQL Injection.

This issue affects FAYDAM Datalogger: from 2.7.1 before 2.8.0.

### CVE-2026-73390

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-19T13:18:08.417 |

Unauthenticated Privilege Escalation in Total Donations <= 2.0.5 versions.

### CVE-2026-73389

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T13:18:08.283 |

Unauthenticated PHP Object Injection in Kalles Addons <= 1.0.6 versions.

### CVE-2026-73364

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-19T13:18:07.520 |

Customer PHP Object Injection in Flexible Subscriptions <= 1.8.1 versions.

### CVE-2026-73347

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-19T13:18:07.123 |

Unauthenticated Privilege Escalation in TrueBooker <= 1.2.6 versions.

### CVE-2026-66613

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-19T13:17:50.563 |

Unauthenticated Remote Code Execution (RCE) in JetEngine <= 3.8.14 versions.

### CVE-2026-73921

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.087 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 1.4.20. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73912

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:24.027 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-73905

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:23.227 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71164

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:17.703 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71152

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:16.280 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71074

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:07.503 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71040

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.763 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70995

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.540 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70970

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.647 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70954

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.720 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70953

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.607 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70926

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.510 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Workflow Notification Mailer).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via SMTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in takeover of Oracle Workflow. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70905

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.283 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Agent infrastructure).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SAML to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70873

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.607 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70871

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.360 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70817

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.490 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70745

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.337 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70740

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.780 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70739

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.667 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70689

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.887 |

Vulnerability in Oracle Essbase (component: Infrastructure).   The supported version that is affected is 21.8.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Essbase.  Successful attacks of this vulnerability can result in takeover of Oracle Essbase. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70669

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:18.543 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62640

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.963 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62639

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.850 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via CORBA to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62635

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.387 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62634

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.270 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via CORBA to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62633

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.153 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62632

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.043 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62630

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.823 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62626

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.370 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62624

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.143 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62622

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:15.913 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62621

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:15.807 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62617

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:14.370 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via UDP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62614

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:14.017 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62611

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.670 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62609

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.440 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62592

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.460 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62585

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:10.653 |

Vulnerability in the Siebel CRM Administration product of Oracle Siebel CRM (component: Data Archival).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Administration.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Administration. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62544

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.947 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62543

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.837 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62541

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.720 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62539

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.490 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62457

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:02.207 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61318

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:59.847 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61272

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.340 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Web Runtime SEC).  Supported versions that are affected are 9.2.0.0-9.2.26.4. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61258

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.737 |

Vulnerability in the Oracle Internet Directory product of Oracle Fusion Middleware (component: OID LDAP Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Internet Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Internet Directory. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61018

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.480 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60977

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.097 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: WLS Core Components).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60971

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.727 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60970

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.613 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60958

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.157 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60947

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.560 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60946

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.440 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60921

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.710 |

Vulnerability in the Oracle WebCenter Enterprise Capture product of Oracle Fusion Middleware (component: Client Bundle).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebCenter Enterprise Capture.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Enterprise Capture. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60858

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:45.373 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60821

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.280 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Business Interlink).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60782

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.237 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in takeover of Oracle Payments. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60727

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.627 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60721

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.253 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60698

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.430 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60696

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.317 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60672

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.723 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 9.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-47627

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T19:16:51.290 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause path traversal. A successful exploit might lead to denial of service.

### CVE-2026-67271

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-18T17:17:00.973 |

Dell PowerStore SDNAS, contains an Out-of-bounds Write vulnerability in the SMB/CIFS. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Denial of service and Remote execution. This is a Critical vulnerability as a remote user could send a specially crafted SMB packet and cause a crash, that is persistent in case automatic restarts are enabled. Additionally, a more sophisticated attacker could use the same vulnerability for Remote Code execution.

### CVE-2026-45117

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T16:17:06.493 |

MyBB is free and open source forum software. From 1.8.13 until 1.8.40, the installer module does not properly escape user-supplied database configuration values written to the configuration file, resulting in PHP code injection and remote code execution when the installer is available. install/index.php processes the values with addcslashes(), but the $characters argument added in MyBB 1.8.13 does not include the backslash character, allowing crafted input to escape the generated PHP string. The uniquely identifying implementation details include introduced in MyBB 1.8.13. This issue is fixed in version 1.8.40.

### CVE-2026-73996

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T15:17:08.600 |

Unauthenticated Arbitrary File Upload in Masteriyo - LMS <= 2.3.2 versions.

### CVE-2026-73397

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:07.103 |

Unauthenticated Deserialization of untrusted data in Youzify <= 1.3.7 versions.

### CVE-2026-73380

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:06.003 |

Unauthenticated PHP Object Injection in Popup by Supsystic <= 1.13.0 versions.

### CVE-2026-73376

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:05.410 |

Unauthenticated PHP Object Injection in Ultimate Maps by Supsystic < 1.5.0 versions.

### CVE-2026-73366

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:04.960 |

Unauthenticated PHP Object Injection in Easy Google Maps <= 1.13.0 versions.

### CVE-2026-73341

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:02.647 |

Unauthenticated PHP Object Injection in RegistrationMagic <= 6.0.9.7 versions.

### CVE-2026-59940

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502;CWE-843` |
| Published | 2026-08-18T15:16:56.007 |

Seroval facilitates JS value stringification, including complex structures beyond JSON.stringify capabilities. Prior to 1.5.3, seroval.fromJSON() allows attacker-controlled JSON Promise control nodes to operate on values from the general deserialization reference table without verifying genuine internal Promise resolver records, causing deserialization side effects with plugins enabled and potentially unintended server-side invocation or remote code execution when downstream frameworks register callable wrappers. This issue is fixed in version 1.5.3.

### CVE-2026-32470

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:16:52.690 |

Unauthenticated PHP Object Injection in FundEngine <= 1.7.9 versions.

### CVE-2026-76036

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-18T21:18:27.617 |

Buffer overflow in Dawn in Google Chrome on on Android prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-76035

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-18T21:18:27.500 |

Inappropriate implementation in Media in Google Chrome on on Mac prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-71064

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.313 |

Vulnerability in the Portable Clusterware component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Portable Clusterware executes to compromise Portable Clusterware.  While the vulnerability is in Portable Clusterware, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Portable Clusterware. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71063

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.193 |

Vulnerability in the Portable Clusterware component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Portable Clusterware executes to compromise Portable Clusterware.  While the vulnerability is in Portable Clusterware, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Portable Clusterware. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70958

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.273 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-70846

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:40.430 |

Vulnerability in the Oracle Demand Planning product of Oracle Supply Chain (component: Internal Operations).  Supported versions that are affected are 12.1 and  12.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Demand Planning.  While the vulnerability is in Oracle Demand Planning, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Demand Planning accessible data as well as  unauthorized access to critical data or complete access to all Oracle Demand Planning accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70670

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:18.680 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62582

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:10.303 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-62463

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:02.930 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61001

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.523 |

Vulnerability in the Oracle Web Services Manager product of Oracle Fusion Middleware (component: Web Services Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Web Services Manager.  While the vulnerability is in Oracle Web Services Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Web Services Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Web Services Manager accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60905

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:47.003 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 9.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:L).

### CVE-2026-60861

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:45.630 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 14.1.2.0.0 and  12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via Oracle Net to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Service Delivery Platform accessible data as well as  unauthorized access to critical data or complete access to all Service Delivery Platform accessible data. CVSS 3.1 Base Score 9.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-12564

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T16:17:01.917 |

A flaw was found in the AAP Controller's HashiCorp Vault credential plugin. The kubernetes_auth() function in awx_plugins/credentials/hashivault.py reads the controller pod's Kubernetes service account token and sends it to an attacker-controlled URL when a HashiCorp Vault Secret Lookup credential with kubernetes_role authentication is tested. An authenticated attacker with credential-creation privileges can exfiltrate the service account token, gaining Kubernetes API access to the control plane namespaces with full pod CRUD and secret read permissions, including database credentials and the Django SECRET_KEY.

### CVE-2026-73920

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:24.967 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-71167

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:18.050 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-71166

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:17.930 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-62629

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.707 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized read access to a subset of Oracle Reports Developer accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Reports Developer. CVSS 3.1 Base Score 9.4 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-57580

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-08-18T17:16:59.667 |

authentik is an open-source identity provider. Prior to 2026.2.6 and 2026.5.5, an inbound SAML Source configured with the non-default USERNAME_LINK or EMAIL_LINK user-matching mode interprets an XML comment in a NameID differently from the identity provider's signed assertion. An attacker with an account on the source identity provider who can set the account's NameID can inject an XML comment that truncates the value used by authentik to the text before the comment while the signed assertion remains valid. A crafted NameID can therefore truncate to a victim's username or email and bind the attacker's external identity to the victim's existing account. This grants full takeover without the victim's password or the identity provider's private key, and the malicious link persists so later logins succeed without the comment. Sources using the default unique-identifier matching mode and authentik's outbound SAML Provider role are not affected. This issue is fixed in versions 2026.2.6 and 2026.5.5.

### CVE-2026-75917

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T14:17:41.840 |

SiYuan before v3.7.4 contains a cross-site scripting vulnerability in the file-tree picker's hover-tooltip generation (app/src/util/pathName.ts, getLeaf()/movePathTo()) used by the 'move/link to' path-selection dialogs, where document metadata fields (bookmark, alias, memo, and an alternate name field) are concatenated into the aria-label HTML attribute without escaping. A document crafted with a double quote in any of these fields breaks out of the attribute context and injects arbitrary HTML attributes including inline event handlers (e.g., onmouseover). Because every SiYuan Electron BrowserWindow runs with nodeIntegration:true, contextIsolation:false, and no CSP, the injected handler gains require('child_process') access, escalating the XSS to arbitrary OS command execution when a victim merely hovers over the malicious document entry in the path-picker dialog. Malicious documents reach victims via sharing, sync, or import.

### CVE-2026-75916

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T14:17:41.687 |

SiYuan through 3.7.3 contains a cross-site scripting vulnerability in the '((' block-reference autocomplete hint popup. In genHintItemHTML() (app/src/protyle/hint/extend.ts), a candidate block's name, alias, and memo fields are concatenated into the popup's HTML without escaping. An attacker who can set these metadata fields on a block can inject a self-firing payload (e.g. <img src=x onerror=...>) that executes automatically when a victim types '((' followed by a search term that surfaces the crafted block. Because SiYuan's Electron windows run with nodeIntegration enabled, contextIsolation disabled, and no CSP, the injected script gains require('child_process') access, allowing the XSS to escalate to arbitrary OS command execution.

### CVE-2026-74804

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:39.643 |

Joomla Extension - yootheme.com - Unauthenticated SQL injection in ItemController::element() in Zoo < 4.1.64 - The filter_type request value is interpolated into the query as a.type = "..." and the type_filter array as a.type IN ("..."), with no quoting or escaping.

### CVE-2024-58376

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T14:17:16.240 |

Renovate versions 37.158.0 before 37.199.0 contain a command injection vulnerability in the helmv3 manager's registryAliases handling that allows attackers with commit access to execute arbitrary commands. Attackers can manipulate registryAliases keys with unquoted shell metacharacters to inject commands executed during helm repo add operations, gaining full access to Renovate's execution environment.

### CVE-2026-73391

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:18:08.547 |

Unauthenticated SQL Injection in Total Donations <= 2.0.5 versions.

### CVE-2026-73388

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:18:08.160 |

Unauthenticated SQL Injection in Nikstore Core <= 1.5 versions.

### CVE-2026-73185

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:18:06.997 |

Unauthenticated SQL Injection in NGG Smart Image Search < 4.0.0 versions.

### CVE-2026-73183

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:18:06.737 |

Unauthenticated SQL Injection in Maps Marker Pro <= 4.32 versions.

### CVE-2026-19490

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-19T13:17:45.000 |

Vulnerability in NetScaler ADC and NetScaler Gateway.

This issue affects ADC: from 14.1 through 73.32 and from 13.1 through 63.21; Gateway: from 14.1 through 73.32 and from 13.1 through 63.21.

### CVE-2026-21580

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T22:16:50.140 |

This Critical severity Stored XSS, PrivEsc (Privilege Escalation), and Security Misconfiguration vulnerability was introduced in versions 7.1.1, 7.4.0, 7.13.0, 7.17.0, 7.19.0, 8.0.0, 8.5.0, 8.9.0, 9.0.1, 9.1.0, 9.2.0, 9.3.1, 9.4.0, 9.5.1, 10.0.2, 10.1.0 and 10.2.0 of Confluence Data Center and Server.

This Stored XSS, PrivEsc (Privilege Escalation), and Security Misconfiguration vulnerability, with a CVSS Score of 8.6, allows an unauthenticated attacker to execute arbitrary HTML or JavaScript code on a victims browser, perform actions as a higher-privileged user, and to get into the system utilizing loopholes exposed from security best-practices being overlooked.

Atlassian recommends that Confluence Data Center and Server customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
 Confluence Data Center and Server 9.2: Upgrade to a release greater than or equal to 9.2.21

 Confluence Data Center and Server 10.2: Upgrade to a release greater than or equal to 10.2.13

See the release notes ([https://confluence.atlassian.com/doc/confluence-release-notes-327.html]). You can download the latest version of Confluence Data Center and Server from the download center ([https://www.atlassian.com/software/confluence/download-archives]).

This vulnerability was reported via our Bug Bounty program.

### CVE-2026-71065

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.430 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data as well as  unauthorized update, insert or delete access to some of Helidon accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-71037

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.427 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70998

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.883 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-70855

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:41.600 |

Vulnerability in the Siebel Apps - Self Service product of Oracle Siebel CRM (component: Helpdesk/Training).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Self Service.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Siebel Apps - Self Service, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Self Service accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Self Service accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70673

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:19.040 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data as well as  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-62637

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.620 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-62618

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:14.560 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data as well as  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-62613

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.900 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-52735

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-684` |
| Published | 2026-08-18T20:17:17.227 |

ZEBRA is a Zcash node written entirely in Rust. Prior to 4.5.0, Zebra can accept a block that zcashd rejects because the P2SH signature-operation counter undercounts redeem scripts containing a disabled opcode followed by signature opcodes. In zebra-script/src/lib.rs, p2sh_input_sigop_count used the pure-Rust script::Code::sig_op_count path, whose try_fold parser stops at disabled opcodes such as OP_CODESEPARATOR and returns only the partial count accumulated before the error. The zcashd reference implementation continues static signature-operation counting through disabled opcodes, so an attacker can broadcast P2SH spends that Zebra counts below MAX_BLOCK_SIGOPS while zcashd counts above the 20,000-operation limit. If a Zebra miner includes those transactions, Zebra validators accept the block while zcashd validators reject it, creating a consensus chain split that affects network integrity and availability without requiring the attacker to produce a block. This issue is fixed in version 4.5.0.

### CVE-2026-50161

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-08-18T18:17:53.380 |

libre is a generic library for real-time communications with asynchronous input and output support. Prior to 4.8.1, the websock_decode() function in src/websock/websock.c contains an integer overflow when validating a masked WebSocket frame that uses the 64-bit extended length encoding. The expression 4 + hdr->len can wrap when hdr->len is close to UINT64_MAX, causing the mbuf_get_left() bounds check to pass. The subsequent XOR unmasking loop then writes beyond the heap buffer. Applications using websock_accept() or websock_accept_proto() to implement a WebSocket server are affected, and exploitation can cause attacker-controlled heap corruption or denial of service after the HTTP WebSocket upgrade handshake. This issue is fixed in version 4.8.1.

### CVE-2026-75926

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-08-18T16:18:24.443 |

Hugo 0.161.0 placed the Node asset pipelines behind the Node.js permission model so that code running through PostCSS, Babel, or TailwindCSS could not reach the file system outside the project directory. Hugo 0.162.0 added tailwindcss to the AllowChildProcess default in config/security/securityConfig.go, which makes nodePermissionArgs in common/hexec/exec.go append --allow-child-process whenever the tool being launched is named tailwindcss. TailwindCSS loads the site's tailwind.config.js through require at startup, so top-level code in that file executes inside the permitted Node process and can call child_process to spawn a shell. The spawned process is not a Node process and inherits none of the permission flags, so it runs with the full privileges of the account performing the build. Building a site whose theme, module, or starter template supplies the Tailwind configuration therefore yields arbitrary command execution rather than the confined file access the permission model was introduced to enforce. Hugo 0.165.0 removes tailwindcss from the default security.exec.allow list, so the tool is no longer launched under the default configuration.

### CVE-2026-45118

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-83` |
| Published | 2026-08-18T16:17:06.633 |

MyBB is free and open source forum software. Prior to 1.8.40, the Contact module does not validate a redirect URL or protocol correctly, resulting in an open redirect and reflected JavaScript code injection. contact.php accepts the redirect target from the from HTTP parameter in $mybb->input['from'] or the Referer HTTP header in $_SERVER['HTTP_REFERER'] and passes it to redirect() without sufficient verification. A javascript: URI becomes the target of the `Click here if you don't want to wait any longer` link because $force_redirect is true, allowing script execution when a victim selects the link. This issue is fixed in version 1.8.40.

### CVE-2026-75784

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-18T15:17:13.857 |

A vulnerability was detected in TRENDnet TEW-WLC100 1v2.07b01. Affected by this issue is the function FUN_0040da4c of the file /usr/nginx/sbin/nginx of the component HTTP Header Handler. The manipulation of the argument Server results in stack-based buffer overflow. The attack may be launched remotely. The exploit is now public and may be used.

### CVE-2026-74015

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:09.833 |

Unauthenticated SQL Injection in Readabler < 2.0.18 versions.

### CVE-2026-73392

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:06.543 |

Unauthenticated SQL Injection in Super Store Finder <= 7.8 versions.

### CVE-2026-73365

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:04.820 |

Unauthenticated SQL Injection in JetAppointment <= 2.5.2 versions.

### CVE-2026-73355

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:03.780 |

Unauthenticated SQL Injection in Affiliates Manager <= 2.9.53 versions.

### CVE-2026-73339

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:02.480 |

Unauthenticated SQL Injection in Modern Events Calendar < 7.35.0 versions.

### CVE-2026-73187

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:01.930 |

Unauthenticated SQL Injection in Sticky Chat Widget <= 1.4.2 versions.

### CVE-2026-76243

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-19T14:17:56.693 |

stigmem versions before 0.9.0a2 allow unauthenticated access when authentication is disabled on non-loopback deployments. Attackers can perform read, write, and federation operations with anonymous identity when nodes are exposed outside local development environments.

### CVE-2026-67443

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T20:17:22.963 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. In 1.3.2 and earlier, the allowDashboard authorization gate in server/integrations/node-red/index.js calls authJwt.verify for /nodered without inspecting the decoded identity. When nodeRedEnabled is true, secureEnabled is true, and nodeRedAuthMode is secure, a remote unauthenticated attacker can obtain a signed guest token from POST /api/heartbeat and use it to access the RED.httpAdmin editor and flow deployment API. Because the Node-RED configuration has no second adminAuth gate, the attacker can deploy function nodes or invoke fuxa.runScript and runtime.scriptsMgr.runScript, gaining control of FUXA project data, configuration, scripts, filesystem-capable runtime helpers, and potentially operating-system commands when nodeRedUnsafeModules is enabled. This issue is fixed in version 1.3.3.

### CVE-2026-71878

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-18T18:19:32.817 |

Missing authentication in initial setup functionality left exposed after initial setup is completed in GBIF Integrated Publishing Toolkit versions before 3.3.4 allows remote authenticated attackers to gain administrative control via authentication bypass

### CVE-2026-75856

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T16:18:21.133 |

CodeWhale before 0.8.64 contains a server-side request forgery bypass vulnerability in DNS pinning logic that fails to prevent time-of-check-time-of-use attacks. Attackers can manipulate DNS responses to fail initial resolution checks and succeed on secondary requests, allowing requests to internal IP addresses and bypassing SSRF mitigations.

### CVE-2026-76244

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-19T14:17:56.827 |

stigmem-node contains an insecure default configuration vulnerability that allows federation traffic to traverse networks without mTLS protection when non-loopback endpoints are enabled. Operators who explicitly disabled mTLS while binding federation to non-loopback addresses expose federation traffic to cleartext interception and man-in-the-middle attacks.

### CVE-2026-76242

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-19T14:17:56.567 |

stigmem-node 0.9.0a1 accepts federation peer key material during peer registration without a separate administrator out-of-band fingerprint approval step. On nodes that accept federation peer registration over a network where initial registration can be intercepted or misdirected, an attacker can register a malicious peer and gain access to or tamper with federation traffic. Fixed in 0.9.0a2, which introduces a pending approval flow requiring administrator fingerprint verification before peer tokens are accepted.

### CVE-2026-76214

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-19T14:17:47.473 |

phpMyFAQ before 4.1.7 (affected versions <= 4.1.5) fails to persist the WebAuthn login challenge generated by prepareForLogin, because neither WebAuthn controller saves the mutated key objects back to the database. At login the anti-replay comparison is skipped by its own null guard, allowing an attacker who captures a successful WebAuthn assertion to replay it indefinitely and authenticate as the user without any interaction or hardware key.

### CVE-2026-76213

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-08-19T14:17:47.330 |

phpMyFAQ before 4.1.7 contains a brute-force vulnerability in the two-factor authentication step where the failure counter is session-scoped and reset on each successful password re-authentication. Attackers with a valid password can bypass the five-attempt limit by obtaining a fresh session cookie and repeatedly re-authenticating to reset the counter, enabling unbounded TOTP code guessing.

### CVE-2026-11751

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-19T02:16:12.530 |

A vulnerability has been identified in armeria-xds versions prior to 1.41.0, where xDS upstream TLS peer verification may be silently disabled, allowing man-in-the-middle attacks against xDS-managed upstream connections.

### CVE-2026-73924

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.430 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 1.4.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73922

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.200 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 1.4.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73917

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:24.620 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73916

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:24.487 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73866

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:18.763 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-73865

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:18.650 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71102

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.493 |

Vulnerability in the Portable Clusterware component of Oracle Database Server.  Supported versions that are affected are 19.3-19.32, 21.3-21.23 and  23.4.0-23.26.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Portable Clusterware.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Portable Clusterware accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Portable Clusterware. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-71036

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.313 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71026

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:02.160 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71015

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:00.877 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71014

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:00.763 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70997

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.767 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-70994

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.423 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-70984

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:57.293 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70981

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.937 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70979

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.710 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70978

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.587 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70977

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.463 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70976

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.337 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70884

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.963 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70883

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.850 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70876

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.993 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70872

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.487 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70862

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.370 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Application Testing Suite accessible data as well as  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70854

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:41.480 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70741

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.893 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via RMI to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Reporting accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Reporting accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70730

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:25.610 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Profitability and Cost Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70668

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:18.427 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62638

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:17.740 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Reports Developer. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-62610

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.560 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61034

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.220 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61008

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.000 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Sites accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60754

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.043 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel Apps - Marketing accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel Apps - Marketing. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-60737

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.323 |

Vulnerability in the Oracle Web Services Manager product of Oracle Fusion Middleware (component: Web Services Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Web Services Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Web Services Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Web Services Manager accessible data. CVSS 3.1 Base Score 9.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60728

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.743 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Portlet Services).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle WebCenter Portal. CVSS 3.1 Base Score 9.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H).

### CVE-2026-60591

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.483 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10-19.10.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hospitality Simphony accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hospitality Simphony. CVSS 3.1 Base Score 9.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-75625

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-354` |
| Published | 2026-08-18T18:19:34.343 |

Kraken agents fail to verify peer-to-peer downloaded blobs against their requested SHA-256 digest before committing to the content-addressable cache, relying only on CRC32 checksums for piece validation. Attackers on the agent-to-agent path or malicious peers can supply substituted content with forged CRC32 corrections that passes per-piece checks, poisoning the cache with attacker-chosen container image layers or manifests that are re-seeded and executed by other hosts.

### CVE-2026-71879

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T18:19:32.960 |

Missing authentication in initial setup functionality left exposed until first reboot in GBIF Integrated Publishing Toolkit versions before 3.3.4 allows remote authenticated attackers to gain administrative control via authentication bypass

### CVE-2026-52723

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-18T17:16:59.200 |

ePA 3.x Integration implements the authorization workflow and writes Medical Information Objects to Germany's electronic patient record. Prior to 1.3.0, ePA 3.x Integration performs VAU server certificate validation in app/vau/VAUProtokoll.py without anchoring the signed_vau_server_pub_keys and AUT_VAU_CertData certificate path to independent trusted material. A network-positioned attacker between the DiGA backend and the ePA system can intercept the VAU handshake, supply attacker-controlled certificate and key material, and satisfy the circular trust relationship. Because TLS certificate verification is also disabled in affected versions, no independent server-authentication layer prevents the attack. The attacker can impersonate the VAU server, control the negotiated session keys, and read or modify all encrypted VAU traffic. This issue is fixed in version 1.3.0.

### CVE-2026-18963

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-18T17:16:57.083 |

A flaw was found in the reset-credentials flow of the keycloak-services component, which is the core engine for identity and access management in Red Hat Build of Keycloak. The issue allows an unauthenticated attacker to force the password reset process for any user without needing to click the required email verification link. This can result in the attacker gaining full control over target user accounts by directly setting new credentials.

### CVE-2026-73381

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T15:17:06.143 |

Unauthenticated Broken Authentication in Popup by Supsystic <= 1.13.0 versions.

### CVE-2026-70980

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:56.820 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62988

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-18T21:17:18.077 |

Froxlor is open source server administration software. From 2.3.7 until 2.3.8, the Customers.get, Customers.listing, Admins.get, Admins.listing, Ftps.get, and Ftps.listing API commands in lib/Froxlor/Api/Commands/Customers.php, lib/Froxlor/Api/Commands/Admins.php, and lib/Froxlor/Api/Commands/Ftps.php retrieve full database rows and return them without removing password and data_2fa fields. An authenticated API caller with permission to use these endpoints can obtain customer, administrator, and FTP password hashes as well as Base32-encoded TOTP seeds for administrator and customer accounts. Password hashes can be cracked offline, and TOTP seeds can generate valid second-factor codes until two-factor authentication is reset. Exposure of both values for an account can enable takeover of the hosting panel or hosted resources and can defeat both authentication factors. This issue is fixed in version 2.3.8.

### CVE-2026-61029

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.867 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  While the vulnerability is in Oracle WebCenter Sites, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 9.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H).

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-73373

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-18T16:18:17.173 |

Joomla! Core - [20260810] - Unrestricted uploads of SHTML files in Joomla 1.0.0-5.4.7, 6.0.0-6.1.2 - The default list of dangerous files did not include SHTML files. On servers that executed these files, that could lead to code execution.

### CVE-2026-71539

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-18T15:17:01.343 |

n8n is an open source workflow automation platform. Prior to 1.123.64, 2.29.8, and 2.30.1, the Git node clone operation allows an authenticated workflow user to swap a validated directory for a symlink before cloning, planting a crafted repository in the community node directory that loads as a custom JavaScript node after restart and executes arbitrary code on the server. This issue is fixed in versions 1.123.64, 2.29.8, and 2.30.1.

### CVE-2026-76208

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-778` |
| Published | 2026-08-19T14:17:46.220 |

phpMyFAQ versions 3.1.0 through 4.1.6 contain an authentication bypass vulnerability in AuthLdap::create(). When LDAP authentication is enabled, after a successful LDAP bind the code calls User::setStatus('active') unconditionally, which overwrites the account_status column of a pre-existing local account from 'blocked' to 'active'. As a result, a user whose local phpMyFAQ account has been administratively blocked can restore their account and log in by authenticating via LDAP. The state transition is not logged, so administrators cannot detect that the block was overridden. Fixed in 4.1.7.

### CVE-2026-54795

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T14:17:34.200 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-19489

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-19T13:17:44.870 |

Vulnerability in NetScaler ADC and NetScaler Gateway.

This issue affects ADC: from 14.1 through 73.32 and from 13.1 through 63.21; Gateway: from 14.1 through 73.32 and from 13.1 through 63.21.

### CVE-2026-49420

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-19T06:17:40.790 |

The RTSP handler in libalias rewrote outgoing packets into a fixed-length stack buffer without checking whether the rewritten data fit in the buffer, or whether the result fit back in the original packet.

A host sending crafted RTSP traffic from inside a NAT gateway using libalias can overflow a stack buffer, potentially achieving remote code execution in the kernel (when using ipfw(4) NAT) or in the natd(8) process (which generally runs as the root user).

### CVE-2026-66602

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-18T22:17:25.173 |

Cross-Site Request Forgery (CSRF) vulnerability in DevItems HashBar – WordPress Notification Bar allows Cross Site Request Forgery.

This issue affects HashBar – WordPress Notification Bar: from n/a through 2.0.0.

### CVE-2026-52876

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20;CWE-78` |
| Published | 2026-08-18T22:16:54.173 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Prior to version 2.6.0, the open-path-at-time IPC handler in src/ipc/player.js accepts a renderer-controlled filePath without validating its type or location. If the mpv or VLC launch attempts are skipped or fail, the handler passes filePath to Electron's shell.openPath. A compromised renderer can provide the path of a local executable, script, shortcut, or other file with an executing default handler, causing the operating system to launch it with the privileges of the StreamBERT process and enabling escape from the renderer sandbox. This issue is fixed in version 2.6.0.

### CVE-2026-52872

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-08-18T22:16:53.650 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Prior to 2.5.0, the downloadSubtitleFile utility in src/ipc/downloads.js, reached through the run-download IPC channel, accepts a renderer-supplied subtitle url using the file: URI scheme and passes its decoded pathname to fs.copyFileSync. The renderer also controls downloadPath, which determines the destination path. A compromised renderer can therefore copy any file readable by the StreamBERT process into an attacker-chosen writable location, exposing sensitive local data, and can overwrite existing writable files. This vulnerability is fixed in 2.5.0.

### CVE-2026-50191

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-288` |
| Published | 2026-08-18T22:16:52.930 |

4gaBoards is a boards system for realtime project management. Prior to 3.3.8, 4gaBoards is vulnerable to pre-account takeover when registrationEnabled, localRegistrationEnabled, and ssoRegistrationEnabled are enabled and Google, GitHub, Microsoft, or OIDC SSO is configured. The POST /api/register endpoint permits creation of an unverified local account with a victim's email address, and POST /api/access-tokens permits that account to authenticate while isVerified is false. During the victim's first SSO login, server/api/helpers/users/get-create-one-for-github-sso.js, server/api/helpers/users/get-create-one-for-google-sso.js, server/api/helpers/users/get-create-one-for-microsoft-sso.js, and server/api/helpers/users/get-create-one-for-oidc-sso.js find the attacker-controlled account by email and link the verified SSO identity without confirming ownership of the local account. The attacker can retain local-password access to the linked account and obtain the victim's projects, data, and permissions. This issue is fixed in version 3.3.8.

### CVE-2026-50186

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T22:16:52.783 |

4gaBoards is a boards system for realtime project management. Prior to 3.3.8, 4gaBoards allows an authenticated project manager to supply traversal sequences in the filename parameter of GET /exports/:id/:filename. In server/api/controllers/boards/download.js, the decoded inputs.filename value is passed to path.join() beneath private/exports/<user_id>/ without containment validation. A crafted value such as ../ can select an arbitrary file readable by the server process, and the file is returned to the attacker. The fileStream close handler then passes the same path to fs.unlink(), deleting the selected file and potentially causing data loss or denial of service. This issue is fixed in version 3.3.8.

### CVE-2026-21582

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T22:16:50.340 |

This High severity BASM (Broken Authentication & Session Management) vulnerability known as CVE-2026-21582 was introduced in version 7.2.1 of Crowd Data Center.

This BASM (Broken Authentication & Session Management) vulnerability, with a CVSS Score of 8.8, allows an unauthenticated attacker to perform actions as another user.
	
	Atlassian recommends that Crowd Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		Crowd Data Center 7.2: Upgrade to a release greater than or equal to 7.2.2
		
		
	
	See the release notes (https://confluence.atlassian.com/crowd/crowd-release-notes-199094.html). You can download the latest version of Crowd Data Center from the download center (https://www.atlassian.com/software/crowd/download-archive). 
	
	This vulnerability was reported via our Penetration Testing program.

### CVE-2026-76047

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-08-18T21:18:28.863 |

Type confusion in V8 in Google Chrome prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76045

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-18T21:18:28.643 |

Use after free in WebGL in Google Chrome prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76043

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-682` |
| Published | 2026-08-18T21:18:28.407 |

Incorrect calculation in V8 in Google Chrome prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-18T21:18:28.060 |

Use after free in Browser in Google Chrome on on Mac prior to 151.0.7922.169 allowed a remote attacker leveraging social engineering to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76034

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-18T21:18:27.390 |

Buffer overflow in WebGL in Google Chrome prior to 151.0.7922.169 allowed a remote attacker to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-71150

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:16.057 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71106

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.943 |

Vulnerability in the Oracle Hospitality OPERA 5 Property Services product of Oracle Hospitality Applications (component: Opera Servlet).  Supported versions that are affected are 5.6.28.0-5.6.28.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality OPERA 5 Property Services.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Hospitality OPERA 5 Property Services. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-71067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.660 |

Vulnerability in the Oracle Agile PLM MCAD Connector product of Oracle Supply Chain (component: CAX Client).   The supported version that is affected is 3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM MCAD Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM MCAD Connector. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.630 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: Web Service API).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in takeover of Oracle BI Publisher. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71055

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.287 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71052

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.063 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Web Services Security).   The supported version that is affected is 6.2.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Engineering Data Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71051

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.940 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Product Lifecycle Analytics executes to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71046

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.483 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile PLM executes to compromise Oracle Agile PLM.  While the vulnerability is in Oracle Agile PLM, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71045

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.373 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-71044

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.257 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Export).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71039

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.650 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Application Server).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70966

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.190 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70965

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.080 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70956

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.007 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70951

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.383 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Document Management).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in takeover of Siebel CRM End User. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.153 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70948

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.050 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Other issue).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70944

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.587 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via TCP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70941

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.227 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Payroll executes to compromise Oracle Payroll.  While the vulnerability is in Oracle Payroll, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Payroll. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.113 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70928

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.747 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70922

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.043 |

Vulnerability in the Oracle Financial Services Enterprise Case Management product of Oracle Financial Services Applications (component: Web UI).  Supported versions that are affected are 8.0.8.2 and  8.1.2.11. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financial Services Enterprise Case Management.  Successful attacks of this vulnerability can result in takeover of Oracle Financial Services Enterprise Case Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70918

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:49.583 |

Vulnerability in the Oracle Product Hub product of Oracle E-Business Suite (component: Outbound Data).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Hub.  Successful attacks of this vulnerability can result in takeover of Oracle Product Hub. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70899

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.587 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70886

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.207 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70877

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.117 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70874

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.740 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70863

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.490 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker having Load Testing for Web Apps privilege with network access via HTTPS to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70821

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:37.030 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70819

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.760 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70818

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.620 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70813

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.923 |

Vulnerability in the Oracle Call Center Technology product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Call Center Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Call Center Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70812

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.793 |

Vulnerability in the Oracle Call Center Technology product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Call Center Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Call Center Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70792

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:32.960 |

Vulnerability in the Oracle Yard Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Yard Management.  Successful attacks of this vulnerability can result in takeover of Oracle Yard Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70787

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:32.247 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70761

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:28.710 |

Vulnerability in the Oracle Risk Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Risk Management.  Successful attacks of this vulnerability can result in takeover of Oracle Risk Management. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70747

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.560 |

Vulnerability in the Oracle Customers Online product of Oracle E-Business Suite (component: Customer Tab).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customers Online.  Successful attacks of this vulnerability can result in takeover of Oracle Customers Online. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70742

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.007 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70737

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.440 |

Vulnerability in the Oracle Enterprise Manager for Systems Infrastructure product of Oracle Enterprise Manager (component: Storage Server Management).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Manager for Systems Infrastructure.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager for Systems Infrastructure. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:25.490 |

Vulnerability in the Oracle Teleservice product of Oracle E-Business Suite (component: Service Request Form).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Teleservice.  Successful attacks of this vulnerability can result in takeover of Oracle Teleservice. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:23.840 |

Vulnerability in Oracle Autonomous Health Framework (component: Trace File Analyzer).  Supported versions that are affected are 26-26.1.0, 26.2.0, 26.3.1, 26.5.0 and  26.5.2. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Autonomous Health Framework executes to compromise Oracle Autonomous Health Framework.  Successful attacks of this vulnerability can result in takeover of Oracle Autonomous Health Framework. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70710

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:23.260 |

Vulnerability in the Oracle Sales Foundation product of Oracle E-Business Suite (component: Security API).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Foundation.  Successful attacks of this vulnerability can result in takeover of Oracle Sales Foundation. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70707

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.910 |

Vulnerability in the Oracle Sales for Handhelds product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales for Handhelds.  Successful attacks of this vulnerability can result in takeover of Oracle Sales for Handhelds. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70688

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.763 |

Vulnerability in Oracle Essbase (component: Calculator).   The supported version that is affected is 21.8.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Essbase.  Successful attacks of this vulnerability can result in takeover of Oracle Essbase. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70686

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.540 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in takeover of Oracle General Ledger. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70674

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:19.157 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62631

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.930 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62623

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.030 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Reports Developer executes to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62619

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:15.573 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-62612

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.787 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62500

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:04.110 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62462

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:02.807 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in takeover of Oracle Work in Process. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62450

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:01.720 |

Vulnerability in the Oracle Flow Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Flow Manufacturing.  Successful attacks of this vulnerability can result in takeover of Oracle Flow Manufacturing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61341

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.910 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61330

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.323 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61319

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:59.960 |

Vulnerability in the Oracle U.S. Federal Financials product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle U.S. Federal Financials.  Successful attacks of this vulnerability can result in takeover of Oracle U.S. Federal Financials. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61284

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.810 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Application Config Console).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61276

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.570 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61273

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.453 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Installation Security).  Supported versions that are affected are 9.2.0.0-9.2.26.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Tools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61231

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.353 |

Vulnerability in the Oracle Virtual Directory product of Oracle Fusion Middleware (component: Virtual Directory Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Virtual Directory.  Successful attacks of this vulnerability can result in takeover of Oracle Virtual Directory. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61213

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.427 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61118

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:54.177 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61058

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.927 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61042

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.570 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61040

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.457 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61032

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.987 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61022

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.743 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61017

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:52.363 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61002

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.640 |

Vulnerability in the Oracle SOA Suite product of Oracle Fusion Middleware (component: B2B Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle SOA Suite.  Successful attacks of this vulnerability can result in takeover of Oracle SOA Suite. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60976

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.957 |

Vulnerability in the Oracle Scripting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Scripting.  Successful attacks of this vulnerability can result in takeover of Oracle Scripting. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60967

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.387 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: nVision).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60879

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:46.190 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Configuration Manager).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60767

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.753 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60751

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.680 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60731

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.097 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via RMI to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60729

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.873 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60726

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.500 |

Vulnerability in the Oracle Access Manager product of Oracle Fusion Middleware (component: Authentication Engine).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Access Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Access Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60722

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.380 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60716

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:40.017 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60715

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.897 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: OIM Legacy UI).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 8.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-48508

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-18T18:17:41.073 |

Lemur manages TLS certificate creation. Prior to 1.9.1, StrictRolePermission and AuthorityCreatorPermission in lemur/auth/permissions.py call flask_principal.Permission.__init__() with zero Need objects when ADMIN_ONLY_AUTHORITY_CREATION and LEMUR_STRICT_ROLE_ENFORCEMENT are unset because both flags default to False. Flask-Principal Permission.allows() returns True when self.needs is empty, so the .can() authorization gate permits every authenticated identity, including the read-only role. A read-only user can access POST /api/1/authorities, POST /api/1/certificates/upload, POST /api/1/pending_certificates//upload, POST /api/1/notifications, PUT or DELETE /api/1/notifications/, and POST /api/1/domains to create root Certificate Authorities, upload arbitrary certificates, create or edit notifications that reach an SSRF sink, and create domain entries. Explicitly setting either flag to False continues to opt into the permissive behavior. This issue is fixed in version 1.9.1.

### CVE-2026-61574

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-863` |
| Published | 2026-08-18T17:16:59.813 |

authentik is an open-source identity provider. Prior to 2026.2.6 and 2026.5.5, the Remote Access Control endpoint list returns every configured endpoint to any authenticated user regardless of which applications the user may access, and the response includes connection settings that can contain stored credentials. The endpoint listing does not apply the access controls governing the endpoints, and the connection flow does not confirm that an endpoint belongs to the Remote Access Control application through which it was launched. Any authenticated user can therefore read every endpoint together with its host and stored credentials and can open a connection to an endpoint belonging to another application. This exposes stored credentials for managed RDP, SSH, and VNC targets and grants interactive access to systems the user was never authorized to reach. Deployments that do not use the enterprise Remote Access Control provider are not affected. This issue is fixed in versions 2026.2.6 and 2026.5.5.

### CVE-2026-49228

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:58.263 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend product operations allow a low-privileged Vendor to access products owned by another Vendor. The admin/controller/product/products.php controller accepts a caller-controlled product_id for duplicate and delete actions, and admin/sql/sqlite/product.sql loads and mutates products without consistently applying the current admin_id when view_other_products or edit_other_products is absent. An attacker can read product details, duplicate products, or delete products and related catalog data, exposing commercial information and causing unauthorized copies, catalog pollution, data loss, or business disruption. This issue is fixed in version 1.0.8.4.

### CVE-2026-62357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-18T16:18:11.650 |

Dragonfly is an in-memory data store built for modern application workloads. Prior to 1.40.0, CMS.INITBYDIM and CMS.INITBYPROB accept dimensions whose width times depth times sizeof(int64_t) overflows in src/core/cms.cc, allocating an undersized counter buffer while CMS.INCRBY and CMS.QUERY use the unbounded dimensions, which allows an unauthenticated remote client to corrupt or disclose adjacent heap memory and crash the server. This issue is fixed in version 1.40.0.

### CVE-2026-49221

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T16:17:13.357 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend digital asset operations allow a low-privileged Vendor to access digital assets linked to another Vendor's products. The admin/controller/product/digital-asset.php and admin/controller/product/digital-assets.php controllers and the admin/sql/sqlite/digital_asset.sql data queries use a caller-controlled digital_asset_id without consistently enforcing the current admin_id ownership boundary. An attacker can list assets, read asset names and file metadata, edit asset metadata, or delete asset records, which can disclose private product metadata, corrupt resource links, and cause data loss. This issue is fixed in version 1.0.8.4.

### CVE-2026-74012

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:17:09.700 |

Editor PHP Object Injection in TaxoPress <= 3.51.0 versions.

### CVE-2026-66793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-18T15:17:00.140 |

A flaw was found in the governance-policy-addon-controller component of Red Hat Advanced Cluster Management for Kubernetes. A user with permissions to annotate the namespaced ManagedClusterAddOn resource can override the governance-policy container image. This allows an attacker to run a controlled image with cluster-admin privileges on the managed cluster, leading to arbitrary code execution and privilege escalation.

### CVE-2026-63639

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-18T15:16:56.627 |

Valkey is a distributed key-value database. Prior to 7.2.14, 8.0.10, 8.1.9, 9.0.5, and 9.1.1, Valkey's RESTORE command accepts a malformed RDB stream payload that assigns one Pending Entry List NACK to multiple consumers during stream consumer-group deserialization, causing a use-after-free when one consumer is deleted while another still references the shared NACK and potentially allowing remote code execution. This issue is fixed in versions 7.2.14, 8.0.10, 8.1.9, 9.0.5, and 9.1.1.

### CVE-2026-61407

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-698` |
| Published | 2026-08-18T15:16:56.310 |

Dell Watchdog Timer Driver versions prior to 2.0.0.1 contain an Exposed IOCTL with Insufficient Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Privilege Escalation.

### CVE-2026-50187

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T15:16:54.870 |

Oh My Zsh is a community-driven framework for managing Zsh configuration. Prior to 2026-05-28, the dotenv plugin in plugins/dotenv/dotenv.plugin.zsh passes ZSH_DOTENV_FILE to source after a directory change into a folder containing a .env file, allowing syntactically valid shell commands in the file to execute with the current account's privileges, including without a prompt when ZSH_DOTENV_PROMPT=false or after the default prompt accepts an empty Enter response. This issue is fixed in versions released after 2026-05-28.

### CVE-2026-76234

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-19T14:17:52.797 |

libcrux-ecdh and libcrux-ed25519 before 0.0.6, and libcrux-psq before 0.0.7, contain cryptographic implementation bugs. libcrux-ecdh did not properly check length and clamping during X25519 secret validation (and had a broken clamping check for imported X25519 secret keys); libcrux-ed25519 performed a duplicated clamping step during key generation; and libcrux-psq panicked instead of propagating an AEADError. These were fixed in the respective patched releases.

### CVE-2026-76224

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T14:17:48.880 |

ArcadeDB before 26.8.1 (arcadedb-gremlin, affected <= 26.7.3) contains a remote code execution vulnerability in its Gremlin query engine. Although the engine defaults to the documented-secure java (gremlin-lang) engine, ArcadeGremlin.executeStatement() silently falls back to the insecure Groovy engine whenever a request carries any query parameter and the query does not parse as gremlin-lang. An authenticated user with any database role, including a read-only reader, can submit a parameterized Gremlin query to trigger the Groovy fallback and execute arbitrary operating system commands as the ArcadeDB server process user.

### CVE-2026-76221

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74` |
| Published | 2026-08-19T14:17:48.463 |

GitPython before 3.1.58 contains a config-name injection vulnerability in the option-name validator that allows attackers to forge arbitrary git-config directives by injecting equals signs, hash symbols, and whitespace into option names. Attackers can inject malicious option names like 'sshCommand = touch /tmp/RCE #' to execute arbitrary commands via core.sshCommand or core.hooksPath on the next git operation.

### CVE-2026-76220

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-19T14:17:48.323 |

GitPython before 3.1.58 contains a command execution vulnerability in the check_unsafe_options guard that can be bypassed by combining a single-character kwarg with split_single_char_options=False. Attackers can supply a crafted kwargs dictionary to guarded methods like clone_from to emit a joined token parsed as --upload-pack, enabling arbitrary OS command execution at default allow_unsafe_options=False.

### CVE-2026-75918

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-19T14:17:42.053 |

phpMyFAQ before 4.1.7 stores password reset tokens in a publicly accessible tracking file when user tracking is enabled. Unauthenticated attackers can read the tracking file at content/core/data/trackingDDMMYYYY to extract reset tokens and replay them against the password reset API to take over user accounts.

### CVE-2020-37267

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-19T14:17:16.033 |

Renovate versions >=19.180.0 and <23.25.1, when used with Azure DevOps, may expose the bot's authorization token in server or pipeline logs because the git http.extraheader=AUTHORIZATION parameter is logged without redaction. Anyone with access to saved logs could obtain the bot credentials. Fixed in 23.25.1; Azure DevOps users should revoke and regenerate credentials if logs may have been exposed.

### CVE-2019-25766

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-08-19T14:17:14.937 |

Renovate versions >= 13.87.0 and <= 19.38.6 leak temporary repository tokens into pull request comments during certain Go Modules update failure scenarios. The issue is fixed in version 19.38.7. Anyone able to view the affected pull request comments could obtain the exposed tokens.

### CVE-2026-70408

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T05:17:05.820 |

An incorrect authorization vulnerability exists in acmailer, which may allow a user to create a sub-account that has administrative privileges.

### CVE-2026-62292

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-18T22:17:03.023 |

libheif is a HEIF and AVIF file format decoder and encoder. From 1.19.0 until 1.23.1, a crafted uncompressed HEIF image using generic zlib unci full-item compression can crash an application that decodes an advertised tile with heif_image_handle_decode_image_tile(). In libheif/codecs/uncompressed/unc_decoder.cc, unc_decoder::fetch_tile_data() computes a large tile offset and unc_decoder::get_compressed_image_data_uncompressed() validates it with range_start_offset plus range_size. For the last advertised tile (4095, 4095), the addition can wrap to zero, bypass the bounds check, and pass an invalid source pointer and a one-terabyte length to memcpy. The observed result is an out-of-bounds read and process crash; opening the file alone does not trigger the issue because tile decoding is required. This issue is fixed in version 1.23.1.

### CVE-2026-15315

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-18T22:16:49.207 |

Tapo C200 v5
contains an improper authentication vulnerability within the login
authentication verification module. An attacker on the local network can
exploit weaknesses in challenge parameter validation to bypass normal
authentication controls and obtain administrative session tokens. 









Successful
exploitation may allow an attacker to subsequently execute privileged
management actions, enable unauthorized administrative access and temporary
disruption of device services, resulting in a denial-of-service (DoS)
condition.

### CVE-2026-71050

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.830 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows high privileged attacker with network access via Oracle Net to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Product Lifecycle Analytics accessible data as well as  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-71000

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:59.130 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70903

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.050 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70900

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.700 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.730 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70778

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:30.920 |

Vulnerability in the Oracle Customer Care product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Customer Care.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Customer Care, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customer Care accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customer Care accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-62607

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:13.180 |

Vulnerability in the Oracle Customer Care product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Customer Care.  While the vulnerability is in Oracle Customer Care, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Customer Care accessible data as well as  unauthorized access to critical data or complete access to all Oracle Customer Care accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-62589

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.120 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61332

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.557 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-61219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.660 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-61215

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.543 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-61193

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:54.653 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60996

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.277 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Connectors and Connector Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTPS to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60981

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.337 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 14.1.2.0.0 and  12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60980

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.220 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60954

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.783 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.207 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60934

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.087 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60903

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:46.877 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60860

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:45.500 |

Vulnerability in the Service Delivery Platform product of Oracle Fusion Middleware (component: Messaging Enabler).  Supported versions that are affected are 14.1.2.0.0 and  12.2.1.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TCP to compromise Service Delivery Platform.  While the vulnerability is in Service Delivery Platform, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Service Delivery Platform accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Service Delivery Platform. CVSS 3.1 Base Score 8.7 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:H).

### CVE-2026-60707

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.770 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Identity Manager.  While the vulnerability is in Oracle Identity Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager accessible data. CVSS 3.1 Base Score 8.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-54347

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T21:16:36.027 |

Froxlor is open source server administration software. Prior to 2.3.8, DNS TXT record content accepted by lib/Froxlor/Api/Commands/DomainZones.php can contain HTML special characters, lib/Froxlor/UI/Callbacks/Text.php returns the content from Text::wordwrap without HTML escaping, and templates/Froxlor/table/table.html.twig renders the callback result with the raw filter. An authenticated customer with DNS editor access can store JavaScript-bearing content in a TXT record. When an administrator views the affected domain's DNS configuration, the payload executes automatically in the administrator's browser session, which can expose session data or perform privileged panel actions. This issue is fixed in version 2.3.8.

### CVE-2026-53453

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T21:16:34.973 |

Blueprint Studio is a VS Code-like file editor for Home Assistant configuration files. Prior to 2.5.2, Blueprint Studio exposed administrator-intended backend API actions to any authenticated Home Assistant user because the backend did not consistently enforce the panel's admin-only authorization boundary. Affected surfaces included the backend API, upload API, stream routes, terminal WebSocket, Blueprint Studio WebSocket subscriptions, call_service, render_template, global_replace, file and stream access paths, upload handling, and terminal helpers. A non-admin user could invoke arbitrary Home Assistant services, expose Home Assistant state through templates, modify configuration files, access streamed or downloaded configuration content, upload files, or reach terminal-related helpers. These actions could compromise the confidentiality, integrity, and availability of the Home Assistant installation. This issue is fixed in version 2.5.2.

### CVE-2026-75936

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-18T20:17:34.317 |

Improper handling of highly compressed data in the GZIP auto-decompression handler in Amazon ion-java before 1.12.0 might allow remote actors to cause a denial of service via a crafted compressed Ion document that expands to an arbitrarily large size upon decompression.



To remediate this issue, users should upgrade to version 1.12.0 and configure withGzipDecompressionEnabled(false) and/or set an explicit withMaximumBufferSize() when parsing untrusted input.

### CVE-2026-75935

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-18T20:17:34.130 |

Uncontrolled memory allocation in the binary Ion stream cursor in Amazon ion-java before 1.12.0 might allow remote actors to cause a denial of service via a crafted Ion binary document containing a declared-length field that causes excessive heap preallocation.



To remediate this issue, users should upgrade to version 1.12.0.

### CVE-2026-52736

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-08-18T20:17:17.400 |

ZEBRA is a Zcash node written entirely in Rust. Prior to 4.5.0, a remote unauthenticated P2P peer can stall a Zebra node by racing an invalid block body against the valid canonical body for the same block header hash. ZIP-244 permits the attacker to mutate coinbase scriptSig authentication data while retaining the transaction identifiers, merkle root, and block header hash, so the poisoned body fails later commitment validation but shares the canonical hash. In zebra-state/src/service.rs, queue_and_commit_to_non_finalized_state recorded the hash in non_finalized_block_write_sent_hashes before contextual validation completed and did not remove it when the write task rejected the body. When the honest body later arrived, the cached hash caused KnownBlock::WriteChannel duplicate handling to suppress it, leaving the node stuck one height behind until restart or reorganization. This issue is fixed in version 4.5.0.

### CVE-2026-75924

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-18T17:17:03.457 |

A flaw was found in managed-serviceaccount. A compromised addon-manager pod, due to its ClusterRole granting excessive permissions, can read any secret across all namespaces. Additionally, it can approve arbitrary Certificate Signing Requests (CSRs), which could lead to information disclosure and privilege escalation within the cluster.

### CVE-2026-75897

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-08-18T17:17:03.310 |

Improper input validation in the capabilities route handler in OpenSearch Dashboards - the size of the request payload is not bounded - might allow remote attackers to cause a denial of service via a crafted HTTP request.

### CVE-2026-69220

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-18T17:17:01.497 |

The RabbitMQ Java client library allows Java and JVM-based applications to connect to and interact with RabbitMQ nodes. Prior to 5.33.1, src/main/java/com/rabbitmq/client/impl/ValueReader.java permits ValueReader.readTable and ValueReader.readArray to call ValueReader.readFieldValue recursively for AMQP table type F and AMQP array type A values without a nesting-depth limit. A malicious AMQP server or network intermediary can send approximately 580 nested table levels in the pre-authentication connection.start frame, fitting within the default 131072-byte frame maximum, to trigger StackOverflowError. The error terminates the client input processing thread and causes denial of service. This issue is fixed in version 5.33.1.

### CVE-2026-69219

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-789` |
| Published | 2026-08-18T17:17:01.353 |

The RabbitMQ Java client library allows Java and JVM-based applications to connect to and interact with RabbitMQ nodes. Prior to 5.33.1, src/main/java/com/rabbitmq/client/impl/ValueReader.java uses ValueReader.readBytes to accept a wire-declared contentLength below Integer.MAX_VALUE and allocate a byte array before checking the bytes available in the frame. A malicious AMQP peer can send a LongString or byte-array field with type tag S and a declared length such as 0x7FFFFFFE during the pre-authentication connection.start server-properties table, causing an approximately 2 GB allocation and OutOfMemoryError before readFully consumes data. The resulting memory exhaustion can terminate the JVM and cause denial of service. This issue is fixed in version 5.33.1.

### CVE-2026-75915

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-18T16:18:23.970 |

CodeWhale versions before 0.8.64 contain an environment variable exposure vulnerability in the js_execution tool that fails to scrub parent process environment variables before spawning Node.js. Attackers can craft malicious JavaScript code executed by the tool to read process.env and leak API keys, cloud credentials, and authentication tokens back to the model context.

### CVE-2026-75914

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T16:18:23.840 |

CodeWhale versions before 0.8.64 contain a path traversal vulnerability in the image_analyze tool that fails to canonicalize symlinks before reading files. Attackers can create workspace symlinks pointing to external files with image extensions to leak file bytes to the vision endpoint without user approval.

### CVE-2026-75859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T16:18:21.787 |

CodeWhale versions before 0.8.64 fail to validate file paths in the project config instructions field, allowing attackers to read arbitrary files on the victim's system. A malicious .codewhale/config.toml file in a cloned repository can specify paths outside the workspace that are read and injected into the AI system prompt for exfiltration.

### CVE-2026-55839

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T16:17:53.710 |

Kestra is an open-source, event-driven orchestration platform. Prior to 1.3.24, Kestra's custom Markdown parser in ui/src/utils/markdown_plugins/link.ts allows a user with permission to create or update a Flow description to inject JavaScript event-handler attributes through the custom [[link]] syntax, causing stored cross-site scripting when another user opens the description or information panel in the Flow list. This issue is fixed in version 1.3.24.

### CVE-2026-45116

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T16:17:06.347 |

MyBB is free and open source forum software. Prior to 1.8.40, the user datahandler does not properly validate checkbox and multiselect profile field types, resulting in stored JavaScript code injection. UserDataHandler::verify_profile_fields() only performs the specialized validation when is_array($profile_fields[$field]) is true. A non-array profile_fields[fidX] value instead of the expected profile_fields[fidX][] shape falls through to generic text handling and is stored without verification. The affected value is then rendered directly by member.php and inc/functions_post.php rather than processed by the MyCode parser. The uniquely identifying implementation details include inc/datahandlers/user.php. This issue is fixed in version 1.8.40.

### CVE-2026-45115

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T16:17:06.180 |

MyBB is free and open source forum software. Prior to 1.8.40, the Buddy/Ignore component does not sanitize usernames correctly, allowing attackers to perform JavaScript code injection through a specially crafted username. The User CP Buddy/Ignore list and the Select Buddies list in Private Messages pass usernames through htmlspecialchars_uni(), which may leave single quotes unescaped. The payload is triggered when a victim chooses Yes in Please Confirm while removing the username in usercp.php, or selects the username through the onclick handler in the xmlhttp.php Select Buddies popup. The uniquely identifying implementation details include Private Messages Select Buddies list, and unescaped single quotes. This issue is fixed in version 1.8.40.

### CVE-2026-66046

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-407` |
| Published | 2026-08-18T15:16:57.000 |

Expat through 2.8.3 contains a denial of service vulnerability caused by quadratic algorithmic complexity in the storeAtts() function in xmlparse.c, where processing N specified attributes with non-normalized values triggers an O(N^2) linear scan of elementType->defaultAtts to determine CDATA status. A remote unauthenticated attacker can supply a single well-formed XML document of a few megabytes to an application parsing untrusted XML to cause excessive CPU consumption, resulting in denial of service without requiring authentication, external entity resolution, or non-default parser options.

### CVE-2026-76237

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T14:17:55.840 |

stigmem-node before 0.9.0a12 contains a broken object level authorization (cross-tenant BOLA) vulnerability in the quarantine review endpoints. On multi-tenant deployments running the opt-in stigmem-plugin-multi-tenant, the list/count queries and _get_quarantined_fact in routes/quarantine.py lacked a tenant_id predicate and the garden lookup was not tenant-scoped, allowing a tenant administrator with only a plain tenant write capability to list, read, and admit or reject quarantined facts belonging to other tenants via the /v1/quarantine endpoints. Default single-tenant deployments are not affected.

### CVE-2026-76207

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-304` |
| Published | 2026-08-19T14:17:46.073 |

phpMyFAQ before 4.1.7 contains a two-factor authentication bypass vulnerability where remember-me tokens are issued before 2FA verification completes. Attackers with valid credentials can obtain a remember-me cookie, skip the 2FA challenge, and replay the cookie to gain full authenticated access without second-factor verification.

### CVE-2026-76205

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:45.777 |

phpMyFAQ before 4.1.7 contains a SQL injection vulnerability in the glossary create and update endpoints caused by truncating an escaped string before embedding it in a SQL literal. Authenticated users with glossary add or edit permissions can craft a payload with a dangling backslash to escape the closing quote and inject arbitrary SQL commands to read sensitive database information.

### CVE-2026-12983

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T06:17:31.307 |

The Dinatur WordPress plugin through 1.18 does not sanitize and escape user input before using it in a SQL query, allowing unauthenticated users to perform SQL injection attacks. The same handler also performs a database table truncation without any authorization check, allowing any unauthenticated visitor to wipe the Dinatur WordPress plugin through 1.18's data.

### CVE-2026-76004

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T03:16:52.900 |

A security vulnerability has been detected in UTT HiPER 1250GW up to 3.2.7-210907-180535. Affected by this vulnerability is the function strcpy of the file /goform/aspApBasicConfigUrcp of the component HTTP Handler. The manipulation of the argument pvid leads to stack-based buffer overflow. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-76003

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T03:16:52.727 |

A weakness has been identified in UTT HiPER 1200GW up to 2.5.3-170306. Affected is the function strcpy of the file /goform/formGroupConfig. Executing a manipulation of the argument timestart can lead to stack-based buffer overflow. The attack may be performed from remote. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-75976

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-19T00:16:28.510 |

A weakness has been identified in TRENDnet TEW-823DRU 1.1.02b01. Impacted is the function strcpy of the file /cgi-bin/wan.cgi of the component NVRAM. This manipulation of the argument wan_l2tp_password causes stack-based buffer overflow. The attack can be initiated remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-52854

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-79;CWE-80` |
| Published | 2026-08-18T22:16:53.470 |

Maps is a MediaWiki extension that enables visualization of geographic data through dynamic embedded maps. Prior to version 12.1.3, the display_map parser function in the Leaflet service accepts attacker-controlled HTML in the overlays parameter, and resources/leaflet/jquery.leaflet.js uses the overlay name as a Leaflet layer-control label without escaping it. A wiki user with the edit permission can store malicious wikitext that causes script execution when another user previews or views the affected map. The script executes in the viewing user's browser session and can access data or perform actions available to that user. This issue is fixed in version 12.1.3.

### CVE-2026-73939

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:27.023 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.20. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data. CVSS 3.1 Base Score 8.6 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:H/A:N).

### CVE-2026-71131

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:13.967 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H).

### CVE-2026-70996

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.657 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70721

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:24.550 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  While the vulnerability is in Oracle Hyperion Profitability and Cost Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62636

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:17.500 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data as well as  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Reports Developer. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-62628

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.597 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62625

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:16.253 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data as well as  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Reports Developer. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-62620

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:15.690 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62599

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.197 |

Vulnerability in the Oracle Trading Community product of Oracle E-Business Suite (component: Third Party Data Integration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Trading Community.  While the vulnerability is in Oracle Trading Community, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Trading Community accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62586

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:10.773 |

Vulnerability in the Siebel CRM Administration product of Oracle Siebel CRM (component: Data Archival).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Administration.  While the vulnerability is in Siebel CRM Administration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Administration accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62535

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.020 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61286

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:57.933 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Event Management).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Enterprise Manager Base Platform accessible data as well as  unauthorized read access to a subset of Oracle Enterprise Manager Base Platform accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-61230

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.240 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61228

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.000 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61045

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:53.690 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Sites accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-61033

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:53.107 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Sites accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-60699

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:39.543 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  While the vulnerability is in Oracle WebLogic Server, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebLogic Server accessible data. CVSS 3.1 Base Score 8.6 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-53455

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-18T21:16:35.280 |

Blueprint Studio is a VS Code-like file editor for Home Assistant configuration files. Prior to 2.5.2, Blueprint Studio generated a shell-based Git credential helper in custom_components/blueprint_studio/backend/git_manager.py by interpolating the configured Git username and token directly into executable helper script content without validating credential values. An attacker able to set Git credentials could include newline characters or shell syntax in a username or token. When Git executed the generated credential helper, the injected shell commands ran with the operating-system privileges of Home Assistant and could access or modify Home Assistant configuration data. This issue is fixed in version 2.5.2.

### CVE-2026-75877

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-18T20:17:33.340 |

A flaw has been found in TRENDnet TV-IP751WIC 11.03.03. This vulnerability affects the function SystemNetworkChanged/SystemDDNSChanged/SystemEmailChanged/SystemFTPChanged/websCheckRealm/FUN_00432574/FUN_0043372C of the component alphapd. Executing a manipulation can lead to stack-based buffer overflow. It is possible to launch the attack remotely. The exploit has been published and may be used.

### CVE-2026-54730

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-807` |
| Published | 2026-08-18T17:16:59.350 |

authentik is an open-source identity provider. Prior to 2026.2.6 and 2026.5.5, the enterprise Google Chrome device-trust stages advance the flow without confirming that the out-of-band device attestation actually ran. Affected enterprise deployments place either a Google Chrome Endpoint stage with mode set to REQUIRED or the deprecated Google Chrome Device Trust Connector stage in an authentication flow. The device attestation occurs in a verification iframe that calls the Google Verified Access API and records the verified device on success, but the vulnerable stages treat the flow as passed as soon as the stage is submitted. An attacker who can reach such a stage, including after primary username and password authentication, can skip the verification iframe and authenticate from a device that was never verified. Where device trust is the only additional factor, that protection is fully bypassed, while other configured factors remain in force. This issue is fixed in versions 2026.2.6 and 2026.5.5.

### CVE-2026-66668

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:17:50.687 |

Subscriber SQL Injection in Community by PeepSo <= 9.0.5.2 versions.

### CVE-2026-32552

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T13:17:45.137 |

Subscriber SQL Injection in YITH WooCommerce Membership Premium <= 2.33.0 versions.

### CVE-2026-11565

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-19T06:17:27.777 |

The Advanced File Manager  WordPress plugin before 5.4.13 does not perform capability checks in several of its file management AJAX actions, allowing users with any role to which an administrator has granted file-manager access (as low as Subscriber) to read arbitrary files on the server — including sensitive configuration files — and to overwrite existing non-PHP files, which can be leveraged to compromise administrator accounts and the whole site.

### CVE-2026-71155

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:16.617 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data as well as  unauthorized update, insert or delete access to some of Helidon accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-71062

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.080 |

Vulnerability in the RDBMS component of Oracle Database Server.  Supported versions that are affected are 23.4.0-23.26.3. Difficult to exploit vulnerability allows low privileged attacker having Authenticated User privilege with network access via Oracle Net to compromise RDBMS.  While the vulnerability is in RDBMS, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of RDBMS. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71057

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:05.510 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.1.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  While the vulnerability is in Oracle BI Publisher, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.5 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-71049

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.713 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows low privileged attacker with network access via Oracle Net to compromise Oracle Product Lifecycle Analytics.  While the vulnerability is in Oracle Product Lifecycle Analytics, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data as well as  unauthorized update, insert or delete access to some of Oracle Product Lifecycle Analytics accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-71002

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:59.360 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized read access to a subset of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N).

### CVE-2026-70885

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.090 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70859

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.117 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70807

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.107 |

Vulnerability in the Oracle Call Center Technology product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Call Center Technology.  While the vulnerability is in Oracle Call Center Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Call Center Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Call Center Technology accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-70728

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:25.370 |

Vulnerability in Oracle Autonomous Health Framework (component: Trace File Analyzer).  Supported versions that are affected are 26-26.1.0, 26.2.0, 26.3.1, 26.5.0 and  26.5.2. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Autonomous Health Framework.  While the vulnerability is in Oracle Autonomous Health Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Autonomous Health Framework accessible data as well as  unauthorized update, insert or delete access to some of Oracle Autonomous Health Framework accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-70718

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:24.207 |

Vulnerability in the Oracle Bills of Material product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Bills of Material.  While the vulnerability is in Oracle Bills of Material, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Bills of Material. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62615

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:14.137 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62596

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.970 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Integration accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-62590

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.233 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Siebel CRM Integration. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-61326

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.207 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-61212

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.310 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60849

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.877 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60841

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.750 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Unified Directory. CVSS 3.1 Base Score 8.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60798

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.810 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Migration).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Deployment.  While the vulnerability is in Siebel CRM Deployment, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60758

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.273 |

Vulnerability in the Siebel Artificial Intelligence product of Oracle Siebel CRM (component: AI).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Artificial Intelligence.  While the vulnerability is in Siebel Artificial Intelligence, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel Artificial Intelligence accessible data as well as  unauthorized update, insert or delete access to some of Siebel Artificial Intelligence accessible data. CVSS 3.1 Base Score 8.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-75913

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-18T16:18:23.363 |

CodeWhale (codewhale / codewhale-tui) versions >= 0.8.41 and < 0.8.64 contain an argument injection vulnerability in the git_show tool. The model-supplied rev parameter is passed unvalidated into the git show argv without an --end-of-options sentinel, so a value beginning with --output= is interpreted as a git flag. Because the tool is registered as auto-approved and advertised as read-only, an attacker (via a malicious repository combined with prompt injection) can cause an unprompted arbitrary file write at the privilege of the invoking user, targeting sensitive files such as ~/.ssh/authorized_keys, ~/.bashrc, or ~/.gitconfig. Fixed in 0.8.64 by adding rev validation.

### CVE-2026-75911

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T16:18:23.057 |

CodeWhale versions before 0.8.64 fail to properly validate the allow_shell configuration parameter from project config files, allowing attackers to enable arbitrary shell command execution by committing a malicious .codewhale/config.toml file to a repository. When a user clones and opens the repository in CodeWhale, the AI model gains access to exec_shell and task_shell tools, enabling execution of arbitrary shell commands on the victim's machine without explicit user consent.

### CVE-2026-75858

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-18T16:18:21.653 |

CodeWhale (packages codewhale / codewhale-tui) versions >= 0.8.41 and < 0.8.64 contain a remote code execution vulnerability in the rlm_eval tool. The tool's approval_requirement() returns ApprovalRequirement::Auto, which the engine treats as 'never prompt,' causing arbitrary model-supplied Python code to run in a python3 interpreter without consulting the user's configured --approval-policy and without any approval prompt or audit step. An attacker can induce the agent to execute arbitrary code via prompt injection in untrusted content the agent reads (a web page, fetched URL, repository file, or MCP tool result); the companion rlm_open tool can stage such content. Code runs on the user's machine at the user's privilege level. Fixed in 0.8.64.

### CVE-2026-71574

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T16:18:16.457 |

Joomla! Core - [20260803] - Inconsistent ACL checks for mutating webservice endpoints in Joomla 4.0.0-5.4.7, 6.0.0-6.1.2 - An improper access check allows unauthorized users to perform mutation actions in webservice endpoints, where the same mutation was restricted in the backend UI.

### CVE-2026-76233

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T14:17:50.957 |

Renovate versions from 39.53.0 before 40.33.0 contain a command injection vulnerability in the gleam manager where the depName parameter is appended to gleam deps update commands without proper sanitization. Attackers with repository write access can craft malicious gleam.toml files to execute arbitrary commands on the machine running Renovate.

### CVE-2026-76232

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T14:17:50.700 |

Renovate versions from 31.51.0 before 40.33.0 contain a command injection vulnerability in the helmv3 manager where the repository parameter is appended to helm registry login commands without proper sanitization. Attackers with repository write access can craft malicious Chart.yaml files to execute arbitrary commands on the machine running Renovate.

### CVE-2026-76231

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T14:17:50.453 |

Renovate versions from 32.135.0 before 40.33.0 contain a command injection vulnerability in the hermit manager where user-provided dependency names are appended to install and uninstall commands without proper sanitization. Attackers with repository write access can provide maliciously named hermit dependencies to execute arbitrary commands on the machine running Renovate.

### CVE-2026-76230

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T14:17:50.277 |

Renovate versions from 35.63.0 before 40.33.0 contain a command injection vulnerability in the npm manager where user-provided packageName values are appended to npm install commands without proper sanitization. Attackers with repository write access can craft malicious Renovate configuration files to execute arbitrary commands on the machine running Renovate.

### CVE-2026-76229

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-19T14:17:50.133 |

Renovate versions from 39.218.0 before 40.33.0 contain an arbitrary command injection vulnerability in the kustomize manager where user-provided chart names are appended to helm pull commands without proper sanitization. Attackers with repository write access can craft malicious kustomization.yaml files with specially crafted chart names to execute arbitrary commands on the Renovate host machine.

### CVE-2026-76228

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T14:17:49.520 |

Renovate versions >=32.124.0 and before 42.68.5 (and Mend renovate-ce/renovate-ee before 13.3.0) contain a command injection vulnerability in Gradle Wrapper artifact handling. When Renovate processes Gradle Wrapper updates, it invokes a wrapper update command via a shell (e.g. /bin/sh -c ... ./gradlew :wrapper --gradle-distribution-url <value>). If an attacker supplies a malicious gradle-wrapper.properties whose distributionUrl contains shell command substitution syntax such as $(...), the shell evaluates it before Gradle parses the URL, resulting in arbitrary command execution in the Renovate runtime. Exploitation requires the attacker to introduce the malicious file into a repository that Renovate scans; the issue occurs even when allowScripts is disabled.

### CVE-2026-76222

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T14:17:48.603 |

GitPython before 3.1.58 fails to validate submodule names from .gitmodules files, allowing attackers to create Git repositories at arbitrary filesystem paths outside the intended clone directory. Attackers can craft malicious repositories with traversal sequences in submodule names that GitPython processes during submodule initialization, creating attacker-controlled Git repositories at escaped filesystem locations.

### CVE-2026-58083

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-19T08:17:12.470 |

While the kernel was copying knotes during fork, a knote with a timer-based filter could fire and be enqueued on the kqueue's active list before the copy was complete.  The copy routine did not account for this and could enqueue the new knote a second time, corrupting the active list.  In addition, the copy routine did not hold the appropriate locks while reading knote state, allowing further races.

An unprivileged local user can trigger a use-after-free in the kernel, potentially leading to privilege escalation.

### CVE-2026-49422

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-19T06:17:41.447 |

The RACK setsockopt(2) handler drops the connection lock in order to copy option data from userspace, then reacquires the lock.  After reacquiring, it verifies that the TCP stack had not been switched away, but did not reload its pointer to the stack's per-connection control block.  If userspace switches stacks twice during this window, the check will succeed but the saved pointer will refer to freed memory.

The bug may be exploitable by an unprivileged local user to escalate privileges.

### CVE-2026-52875

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-08-18T22:16:54.003 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Prior to 2.6.0, the perform-scheduled-backup IPC handler in src/ipc/storage.js takes settings.path from a renderer-supplied object and uses the resulting directory for fs.mkdirSync, fs.writeFileSync, fs.readdirSync, and fs.unlinkSync operations without checking that it is inside an authorized backup location. A compromised renderer can choose an absolute path or a relative traversal path to create directories and write a streambert-backup-[timestamp].json file containing renderer-controlled data. The pruning loop can also delete files in that directory whose names begin with streambert-backup- and end with .json. This vulnerability is fixed in 2.6.0.

### CVE-2026-76037

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-18T21:18:27.727 |

Link following in CredentialProvider in Google Chrome on on Windows prior to 151.0.7922.169 allowed a local attacker to potentially execute arbitrary code outside the sandbox via a local program. (Chromium security severity: High)

### CVE-2026-70842

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:39.870 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70840

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:39.597 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70731

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:25.730 |

Vulnerability in Oracle Autonomous Health Framework (component: Trace File Analyzer).  Supported versions that are affected are 26-26.1.0, 26.2.0, 26.3.1, 26.5.0 and  26.5.2. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Autonomous Health Framework executes to compromise Oracle Autonomous Health Framework.  While the vulnerability is in Oracle Autonomous Health Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Autonomous Health Framework accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Autonomous Health Framework. CVSS 3.1 Base Score 8.4 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H).

### CVE-2026-60928

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.840 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-75898

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T15:17:15.367 |

RAGFlow before 0.26.3 contains a server-side request forgery vulnerability in the agent workflow "Invoke" component (agent/component/invoke.py). The component builds an outbound request URL from canvas configuration and runtime template variables and passes it to requests.get, requests.post, or requests.put without calling the shared assert_url_is_safe validator or pinning the resolved address, unlike the crawler, SearXNG, file-upload, and RSS fetch paths. A user who can create or trigger an agent can direct the server to fetch loopback, link-local, and RFC 1918 destinations, including cloud instance metadata endpoints and services co-located on the deployment network, and the response body is returned as the component output. Where an agent is configured to interpolate the chat query into the Invoke URL, the destination is chosen by whoever can send that query.

### CVE-2026-76225

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T14:17:49.020 |

ArcadeDB before 26.8.1 contains a server-side request forgery vulnerability in the OpenCypher LOAD CSV implementation that fails to validate HTTP/HTTPS URLs. Authenticated attackers can craft LOAD CSV queries pointing to internal network addresses or cloud metadata endpoints to make the ArcadeDB server fetch and return sensitive data from restricted services.

### CVE-2026-52877

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-20;CWE-749` |
| Published | 2026-08-18T22:16:54.520 |

Streambert is a cross-platform Electron Desktop App to stream and download video content. Prior to version 2.6.0, the open-external IPC handler in src/ipc/downloads.js passes a renderer-supplied url directly to Electron's shell.openExternal without validating its protocol. A compromised renderer can submit file: URIs or operating-system-specific custom schemes, causing the host to open local files, access remote resources through registered handlers, or launch scripts and applications supported by those handlers. This issue is fixed in version 2.6.0.

### CVE-2026-76046

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-18T21:18:28.750 |

Buffer overflow in ANGLE in Google Chrome on on Android prior to 151.0.7922.169 allowed a remote attacker who had compromised the renderer process to execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-76044

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-18T21:18:28.530 |

Race condition in USB in Google Chrome prior to 151.0.7922.169 allowed a remote attacker who had compromised the renderer process to potentially execute arbitrary code outside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-73931

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:26.113 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L).

### CVE-2026-73929

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:25.890 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L).

### CVE-2026-71095

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:09.683 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-70770

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:29.777 |

Vulnerability in the Oracle Warehouse Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Warehouse Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Warehouse Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Warehouse Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Warehouse Management. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-62455

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:02.083 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized read access to a subset of Siebel CRM Cloud Applications accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H).

### CVE-2026-61305

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:59.123 |

Vulnerability in the Oracle BI Publisher product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle BI Publisher.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle BI Publisher accessible data as well as  unauthorized access to critical data or complete access to all Oracle BI Publisher accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle BI Publisher. CVSS 3.1 Base Score 8.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-49225

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:58.117 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend product revision operations allow a low-privileged Vendor to access revisions for products owned by another Vendor. The admin/controller/product/revisions.php route reuses admin/controller/content/revisions.php, while admin/sql/sqlite/product_content_revision.sql trusts caller-controlled product_id, language_id, and created_at values without applying the current admin_id to revision reads, restores, and deletes. An attacker can read historic product content, restore a revision over another Vendor's live product content, or delete revision records, exposing private copy, corrupting product pages, and removing audit history. This issue is fixed in version 1.0.8.4.

### CVE-2026-49224

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:57.977 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend post revision operations allow a low-privileged Author to access revisions for posts owned by another Author. The admin/controller/content/revisions.php controller and admin/sql/sqlite/post_content_revision.sql queries trust caller-controlled post_id, language_id, and created_at values without consistently applying the current admin_id to revision lists, reads, restores, and deletes. An attacker can read historic post content, restore a revision over another Author's live post content, or delete revision records, exposing drafts, corrupting published content, and removing audit history. This issue is fixed in version 1.0.8.4.

### CVE-2026-75912

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-18T16:18:23.220 |

CodeWhale versions before 0.8.64 contain an argument injection vulnerability in the git_blame tool that allows attackers to read arbitrary files by injecting git options into the unvalidated rev parameter. Attackers can supply rev values like --contents=/path/to/file to exfiltrate sensitive files such as SSH keys and credentials through the tool output returned to the model.

### CVE-2026-49226

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T16:17:13.510 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend post operations allow a low-privileged Author to access posts owned by another Author. The admin/controller/content/posts.php controller permits filter[admin_id] to replace the server-selected admin_id restriction and accepts a caller-controlled post_id for duplicate and delete actions, while admin/sql/sqlite/post.sql does not consistently enforce post.admin_id. An attacker can view post metadata, discover post identifiers, duplicate posts, or delete posts and related content, exposing private drafts and causing content pollution, data loss, or business disruption. This issue is fixed in version 1.0.8.4.

### CVE-2026-45733

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79;CWE-83;CWE-693` |
| Published | 2026-08-18T15:16:54.270 |

Trilium Notes is a cross-platform, hierarchical note taking application focused on building large personal knowledge bases. Prior to 0.103.0, the #iconClass label value is returned raw by getNoteIcon() and inserted without HTML attribute encoding into class attributes in apps/client/src/widgets/quick_search.ts and apps/client/src/services/note_autocomplete.ts, allowing a stored payload to execute automatically when a victim opens a new tab or uses Ctrl+J and, because Electron enables nodeIntegration and disables contextIsolation, run operating-system commands as the victim. This issue is fixed in version 0.103.0.

### CVE-2026-73937

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:26.800 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon and  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H).

### CVE-2026-73925

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.547 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 1.4.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-71159

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:17.167 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data as well as  unauthorized update, insert or delete access to some of Helidon accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-71130

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:13.853 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows unauthenticated attacker with network access via RDP to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle VM VirtualBox accessible data as well as  unauthorized update, insert or delete access to some of Oracle VM VirtualBox accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-71129

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:13.737 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71096

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:09.800 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Business Intelligence Enterprise Edition accessible data as well as  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-71024

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:01.927 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-71018

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:01.217 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-71016

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:00.987 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-70993

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.310 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-70964

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.957 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70952

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:53.493 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70909

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:48.747 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70897

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.357 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70893

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:46.060 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70892

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.940 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70887

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.330 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70870

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:43.240 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Web Client - Unicode).   The supported version that is affected is 11.2.23.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70852

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:41.210 |

Vulnerability in the Oracle Demand Planning product of Oracle Supply Chain (component: Internal Operations).  Supported versions that are affected are 12.1 and  12.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Demand Planning.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Demand Planning accessible data as well as  unauthorized update, insert or delete access to some of Oracle Demand Planning accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70773

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:30.173 |

Vulnerability in the Oracle HCM Common Architecture product of Oracle E-Business Suite (component: Knowledge Integration).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle HCM Common Architecture.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle HCM Common Architecture accessible data as well as  unauthorized update, insert or delete access to some of Oracle HCM Common Architecture accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70743

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:27.113 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Reporting accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70722

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:24.670 |

Vulnerability in the Oracle Advanced Inbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Advanced Inbound Telephony.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Advanced Inbound Telephony accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Advanced Inbound Telephony. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-70703

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.460 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile Engineering Data Management.  While the vulnerability is in Oracle Agile Engineering Data Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile Engineering Data Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Agile Engineering Data Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70702

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.347 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payments accessible data as well as  unauthorized update, insert or delete access to some of Oracle Payments accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-62605

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.917 |

Vulnerability in the Oracle Partner Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Partner Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Partner Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Partner Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Partner Management accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-62598

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.083 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via SFTP to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-62485

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.647 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-62448

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:01.490 |

Vulnerability in the Oracle Email Center product of Oracle E-Business Suite (component: Message Component).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Email Center.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Email Center, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Email Center accessible data as well as  unauthorized update, insert or delete access to some of Oracle Email Center accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61340

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.790 |

Vulnerability in the Oracle MES for Process Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle MES for Process Manufacturing.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle MES for Process Manufacturing, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle MES for Process Manufacturing accessible data as well as  unauthorized update, insert or delete access to some of Oracle MES for Process Manufacturing accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61302

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:59.000 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Pod Admin).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-61222

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.777 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61054

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.807 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-61038

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:53.340 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-61016

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:52.247 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Sites accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-61011

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:52.130 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Sites accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Sites. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-60955

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:48.913 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized read access to a subset of Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 8.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-60944

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.320 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-60796

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:43.583 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel CRM Integration. CVSS 3.1 Base Score 8.2 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-60592

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.603 |

Vulnerability in the MySQL Cluster product of Oracle MySQL (component: Cluster: NDB Operator).  Supported versions that are affected are 8.0.0-8.0.47, 8.4.0-8.4.10 and  9.7.0-9.7.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise MySQL Cluster.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of MySQL Cluster as well as  unauthorized update, insert or delete access to some of MySQL Cluster accessible data. CVSS 3.1 Base Score 8.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-47719

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T20:17:15.103 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. Prior to 1.3.2, the DEVICE_WEBAPI_REQUEST and DEVICE_PROPERTY Socket.IO handlers in server/runtime/index.js omit isSocketWriteAuthorized and accept attacker-controlled property.address or endpoint connection data. A remote unauthenticated attacker can make server/runtime/devices/httprequest/index.js call axios.get against arbitrary HTTP or HTTPS destinations, connect to reachable OPC UA or ODBC services, and receive results through the corresponding Socket.IO event. This read SSRF oracle can expose cloud instance metadata, internal administrative services, industrial endpoints, and ODBC data reachable from the FUXA host, including when secureEnabled is true. This issue is fixed in version 1.3.2.

### CVE-2026-66783

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-18T17:17:00.840 |

A flaw was found in the `submariner-operator` component of Red Hat Advanced Cluster Management for Kubernetes. This vulnerability allows a cluster administrator, or any user with permissions to modify the Submariner Custom Resource (CR), to specify an unvalidated image path. This lack of validation enables an attacker to execute arbitrary code with elevated privileges across the entire cluster, including control-plane nodes, by deploying a malicious image.

### CVE-2026-73337

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-18T16:18:16.893 |

Joomla! Core - [20260807] - MFA Authentication Bypass in Joomla 4.0.0-5.4.7 and 6.0.0-6.1.2 - Insufficient state checks lead to a vector that allows to bypass 2FA checks.

### CVE-2026-73356

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T15:17:03.940 |

Unauthenticated Arbitrary Content Deletion in Breeze <= 2.5.12 versions.

### CVE-2026-73350

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-18T15:17:03.377 |

Unauthenticated Broken Authentication in SupportCandy <= 3.5.1 versions.

### CVE-2026-70422

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:38.897 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-73387

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-19T13:18:08.033 |

Unauthenticated Local File Inclusion in Resido <= 1.5 versions.

### CVE-2026-13169

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T06:17:31.677 |

The Eventin  WordPress plugin before 4.1.21 does not properly verify ownership of events before allowing them to be modified, deleted, or reassigned to a different author, allowing users with contributor-level access and above to alter, delete, or take over events created by other users including administrators.

### CVE-2026-19942

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-19T05:17:02.217 |

The Atarim – AI Agency for WordPress: Edit Pages, Fix Code, Update Plugins, SEO & Client Feedback plugin for WordPress is vulnerable to arbitrary file deletion due to insufficient file path validation in the AVCF_Abilities_Media::register (replace-media-file execute_callback) function in all versions up to, and including, 5.1.1. This makes it possible for authenticated attackers, with author-level access and above, to delete arbitrary files on the server, which can easily lead to remote code execution when the right file is deleted (such as wp-config.php). This is exploitable by first using the atarim/update-post-field ability to overwrite the _wp_attached_file meta of an attacker-owned attachment with a directory-traversal path, then invoking atarim/replace-media-file to cause get_attached_file() to resolve and unlink the targeted file.

### CVE-2026-71112

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:11.753 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects product of Oracle PeopleSoft (component: Security).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise FIN Common Objects.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71110

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:11.470 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71068

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.783 |

Vulnerability in the Oracle Agile PLM MCAD Connector product of Oracle Supply Chain (component: CAX Client).   The supported version that is affected is 3.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM MCAD Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM MCAD Connector. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71053

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.173 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Web Services Security).   The supported version that is affected is 6.2.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Engineering Data Management. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71042

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.990 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: PGC / Excel Plugin).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Agile PLM accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Agile PLM. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-71035

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.193 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70999

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.997 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70959

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.387 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70957

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.153 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70943

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.463 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70931

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:51.097 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Workflow Notification Mailer).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Workflow accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Workflow. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70929

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.863 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70925

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.393 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70924

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.280 |

Vulnerability in the Oracle Web Services Manager product of Oracle Fusion Middleware (component: Web Services Security).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Web Services Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Web Services Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70904

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.167 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Data Relationship Management executes to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70901

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.820 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-70881

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.610 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70878

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.247 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70868

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.110 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70835

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.920 |

Vulnerability in the Oracle iRecruitment product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iRecruitment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iRecruitment accessible data as well as  unauthorized access to critical data or complete access to all Oracle iRecruitment accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70830

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.237 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Process Manufacturing Systems accessible data as well as  unauthorized access to critical data or complete access to all Oracle Process Manufacturing Systems accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70815

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.210 |

Vulnerability in the Oracle Internet Procurement Connector product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Internet Procurement Connector.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Internet Procurement Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Internet Procurement Connector accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70814

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.067 |

Vulnerability in the Oracle Call Center Technology product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Call Center Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Call Center Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70811

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.657 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.5-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70805

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:34.813 |

Vulnerability in the Oracle Project Planning and Control product of Oracle E-Business Suite (component: Change Management).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Project Planning and Control.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Project Planning and Control accessible data as well as  unauthorized access to critical data or complete access to all Oracle Project Planning and Control accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70795

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:33.387 |

Vulnerability in the Oracle Applications Platform Engineering product of Oracle E-Business Suite (component: Valid Session).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise Oracle Applications Platform Engineering.  Successful attacks of this vulnerability can result in takeover of Oracle Applications Platform Engineering. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70782

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:31.513 |

Vulnerability in the Oracle Labor Distribution product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Labor Distribution.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Labor Distribution accessible data as well as  unauthorized access to critical data or complete access to all Oracle Labor Distribution accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70762

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:28.833 |

Vulnerability in the Oracle Risk Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Risk Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Risk Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Risk Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70749

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.680 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70746

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.450 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Reporting accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Reporting accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-70744

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.227 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70738

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.553 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Profitability and Cost Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70708

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:23.023 |

Vulnerability in the Oracle Sales Foundation product of Oracle E-Business Suite (component: Security API).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales Foundation.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales Foundation accessible data as well as  unauthorized access to critical data or complete access to all Oracle Sales Foundation accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70704

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.573 |

Vulnerability in the Oracle Trading Community product of Oracle E-Business Suite (component: Party Search UI).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Trading Community.  Successful attacks of this vulnerability can result in takeover of Oracle Trading Community. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70701

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.233 |

Vulnerability in the Oracle Payables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payables.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Payables accessible data as well as  unauthorized access to critical data or complete access to all Oracle Payables accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70684

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.307 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70675

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:19.267 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in takeover of Oracle Reports Developer. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70671

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:18.803 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62600

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.313 |

Vulnerability in the Oracle Sales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Sales accessible data as well as  unauthorized access to critical data or complete access to all Oracle Sales accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62595

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.857 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Integration executes to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62591

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.340 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-62531

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:05.663 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62502

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:04.357 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62501

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:04.227 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62491

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.757 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Purchasing accessible data as well as  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62477

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.410 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62471

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.167 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62442

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:01.260 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61321

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.083 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Cloud Applications accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61307

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:59.370 |

Vulnerability in the PeopleSoft Enterprise CC Common Application Objects product of Oracle PeopleSoft (component: Common Application Objects).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via Oracle Net to compromise PeopleSoft Enterprise CC Common Application Objects.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise CC Common Application Objects. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61293

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.407 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61281

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.683 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N).

### CVE-2026-61270

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.223 |

Vulnerability in the JD Edwards EnterpriseOne Orchestrator product of Oracle JD Edwards (component: E1 IOT Orchestrator Security).  Supported versions that are affected are 9.2.0.0-9.2.26.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Orchestrator.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Orchestrator accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Orchestrator accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61268

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:57.090 |

Vulnerability in the JD Edwards EnterpriseOne Tools product of Oracle JD Edwards (component: Business Logic Infra SEC).  Supported versions that are affected are 9.2.0.0-9.2.26.4. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise JD Edwards EnterpriseOne Tools.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all JD Edwards EnterpriseOne Tools accessible data as well as  unauthorized access to critical data or complete access to all JD Edwards EnterpriseOne Tools accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-61265

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.980 |

Vulnerability in the JD Edwards EnterpriseOne Orchestrator product of Oracle JD Edwards (component: E1 IOT Orchestrator Security).  Supported versions that are affected are 9.2.0.0-9.2.26.4. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise JD Edwards EnterpriseOne Orchestrator.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne Orchestrator. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61229

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:56.130 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Portal. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61177

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:54.537 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60992

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.797 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via TLS to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60831

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.630 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Integration Broker).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60791

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.350 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Application Interface).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60779

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.000 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Marketing accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel Apps - Marketing. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-60757

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.163 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Search).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Siebel CRM End User executes to compromise Siebel CRM End User.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM End User accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data. CVSS 3.1 Base Score 8.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60742

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.440 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: PIA Core Technology).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60680

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:38.967 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebLogic Server accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle WebLogic Server. CVSS 3.1 Base Score 8.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-60415

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.130 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 8.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-52793

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-18T21:16:34.650 |

Froxlor is open source server administration software. Prior to 2.3.7, the API authentication path in lib/Froxlor/Api/FroxlorRPC.php and FroxlorRPC::validateAuth accepts an API key and secret for an administrator or customer account without checking type_2fa, validating a TOTP code, or invoking FroxlorTwoFactorAuth. The web interface requires a second factor for accounts with two-factor authentication enabled, but the API grants access after validating only the API credentials, expiration, API permission, and account status. An attacker who obtains an API key and secret for a protected account can call the available API functions without supplying the configured second factor, which can expose or modify customer data, domains, email and FTP accounts, databases, DNS records, and certificate material. This issue is fixed in version 2.3.7.

### CVE-2026-71308

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-18T20:17:23.740 |

Lemur manages TLS certificate creation. From 0.5.0 until 1.9.3, certificate create, upload, and edit requests accepted replaces[] or replacements identifiers that AssociatedCertificateSchema resolved with fetch_objects without a CertificatePermission check. Assigning those objects to Certificate.replaces invoked an append listener that disabled the victim certificate notifications and marked it as replaced. The victim was then excluded from get_all_pending_reissue, and certificate_rotate could deploy the attacker certificate to endpoints serving the victim. An authenticated non-read-only user could target certificates for which the user had no ownership or role, suppress lifecycle automation, and cause fleet-wide TLS disruption or unauthorized substitution. The fix authorizes every referenced replacement certificate before mutation. This issue is fixed in version 1.9.3.

### CVE-2025-9210

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-18T19:16:43.650 |

Missing signature validation in JSON Web Tokens in Otalio Ship Property Management System versions before 2.22.0 allows authenticated attackers to escalate privileges via tampering with JWTs

### CVE-2026-67262

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T18:19:24.927 |

Dell PowerStore contains a Missing Authorization vulnerability. An attacker with access to a mapped host could exploit this vulnerability to read from or write to LUNs that the host is not authorized to access, bypassing per-initiator LUN access controls and leading to protection mechanism bypass.

### CVE-2026-50143

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T18:17:53.227 |

The Apify MCP server enables AI agents to extract data from websites using ready-made scrapers, crawlers, and automation tools available on the Apify Store. Prior to 0.10.11, getActorMCPServerURL in src/mcp/actors.ts concatenates the trusted Actor standby URL with the attacker-controlled webServerMcpPath from an Actor definition without verifying the resulting origin, allowing a malicious Actor publisher to use a userinfo-style authority value to redirect connectMCPClient to a third-party host. The call-actor, fetch-actor-details, and actor-mcp tool-loading paths pass this URL to transports in src/mcp/client.ts that attach the victim Authorization bearer token, exposing the Apify API token and enabling access to Actors, stored data, and billable compute. A victim must invoke or inspect the attacker-controlled Actor. This issue is fixed in version 0.10.11.

### CVE-2026-44472

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-18T18:17:33.573 |

Saleor is an e-commerce platform. From 2.10.0rc1 until 3.21.67, 3.22.63, and 3.23.22, the account activation flow treats email verification as sufficient proof of account ownership and automatically associates anonymous commerce data with the newly activated account. An attacker can use accountRegister to create an account with a victim's email address before the victim registers. If the victim follows the activation link sent to that mailbox, Saleor activates the attacker-created account and saleor/graphql/account/mutations/account/confirm_account.py can merge anonymous orders and gift-card data for the same email address without requiring the account password or another authentication factor. The attacker can then access the merged order history and personal data, including names, addresses, and phone numbers. The patched supported lines disable automatic merging by default, while the redesigned 3.24.0 flow requires password confirmation before anonymous objects are linked. This issue is fixed in versions 3.21.67, 3.22.63, and 3.23.22.

### CVE-2026-70415

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-18T17:17:01.973 |

Dell PowerStore SDNAS contains a Buffer Copy without Checking Size of Input vulnerability in the NFS/RPC. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Command execution and Denial of service.

### CVE-2026-73400

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-18T15:17:07.530 |

Unauthenticated Local File Inclusion in Restaurant Menu by MotoPress <= 2.4.11 versions.

### CVE-2026-50138

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T15:16:54.580 |

goshs is a SimpleHTTPServer written in Go. Prior to version 2.1.0, when `goshs` is launched with WebDAV enabled (`-w`), the mode-restriction flags `--read-only`, `--upload-only`, and `--no-delete` are enforced only on the primary HTTP port. The WebDAV port is wired straight to `golang.org/x/net/webdav.Handler` with no equivalent guard, so an authenticated WebDAV client can `PUT`, `DELETE`, `MKCOL`, `MOVE`, and `COPY` despite the operator's stated intent. Version 2.1.0 patches the issue.

### CVE-2026-71122

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:12.947 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70802

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:34.383 |

Vulnerability in the Oracle Public Sector Human Resources product of Oracle E-Business Suite (component: Regression Testing).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Human Resources.  While the vulnerability is in Oracle Public Sector Human Resources, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Public Sector Human Resources. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70690

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.990 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: US Payroll - General).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HRMS (US).  While the vulnerability is in Oracle HRMS (US), attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (US). CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-62602

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.560 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Calculation Manager executes to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60998

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.400 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Microsoft Active Directory).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows high privileged attacker with network access via LDAP to compromise Oracle Identity Manager Connector.  While the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 8.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-60961

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.270 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 8.0 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70685

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.427 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Hyperion Calculation Manager executes to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 7.9 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-54552

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-273` |
| Published | 2026-08-18T18:18:23.147 |

sh provides Python process launching. Prior to 2.2.4, the _uid option in sh.py performs an incomplete privilege drop on Linux and Unix-like systems. When sh runs from an elevated process and launches a command with _uid set to an unprivileged user, the child changes its UID but can retain the parent process's supplementary groups because the privilege-drop sequence does not fully establish the target user's UID, primary GID, and supplementary groups. The child can therefore retain access to files or resources granted to privileged groups such as root, docker, disk, shadow, or sudo, violating the expected _uid privilege boundary. This issue is fixed in version 2.2.4.

### CVE-2026-43961

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-19T14:17:31.793 |

A flaw was found in Vim's netrw plugin. A crafted filename containing quote characters and expression fragments can break out of the quoted context during mark/unmark operations, allowing arbitrary Vimscript execution. This can be leveraged to run shell commands with the privileges of the user running Vim.

### CVE-2026-58087

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125;CWE-191;CWE-787` |
| Published | 2026-08-19T08:17:12.877 |

The GETALL and SETALL commands in semctl(2) recorded the number of semaphores in the target set, dropped the lock protecting the set, allocated a buffer sized for that count, and reacquired the lock.  A sequence-number check was used to verify that the set had not been replaced in the interim, but the sequence number wraps after 0x8000 create/destroy cycles.  By rapidly destroying and recreating semaphore sets at the same index, another process can cause the sequence number to wrap, allowing a set with a different number of semaphores to pass validation.  The subsequent copy then reads or writes past the end of the allocated buffer.

An unprivileged local user can trigger out-of-bounds reads and writes on kernel heap memory, potentially leading to privilege escalation.

### CVE-2026-49429

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-19T06:17:42.513 |

The ZFS_IOC_USERSPACE_MANY ioctl, used by zfs-userspace(8), truncated a 64-bit output buffer size to a 32-bit integer for the kernel allocation, but used the original 64-bit size as the buffer limit when writing records.

A local user with the "userused" delegated ZFS permission can trigger a kernel heap overflow via the ZFS_IOC_USERSPACE_MANY ioctl, potentially escalating privileges.

### CVE-2026-71126

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:13.400 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71111

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:11.627 |

Vulnerability in the Oracle Identity Manager product of Oracle Fusion Middleware (component: Installer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Identity Manager executes to compromise Oracle Identity Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71101

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.380 |

Vulnerability in the Oracle HRMS (US) product of Oracle E-Business Suite (component: US Payroll Tax Issues).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle HRMS (US) executes to compromise Oracle HRMS (US).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (US). CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71097

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:09.917 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71028

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:02.383 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71010

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:00.310 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-70879

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:44.370 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Data Relationship Management executes to compromise Oracle Hyperion Data Relationship Management.  While the vulnerability is in Oracle Hyperion Data Relationship Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-70866

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.863 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker having Load Testing for Web Apps privilege with logon to the infrastructure where Oracle Application Testing Suite executes to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70798

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:33.823 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Purchasing executes to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70750

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:27.787 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Reporting executes to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Reporting. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62581

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:10.187 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62454

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:01.963 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Cloud Applications. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61300

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.877 |

Vulnerability in the Oracle Enterprise Manager Base Platform product of Oracle Enterprise Manager (component: Agent Next Gen).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Enterprise Manager Base Platform executes to compromise Oracle Enterprise Manager Base Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager Base Platform. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61291

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.290 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60991

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.683 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60822

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.397 |

Vulnerability in the Oracle Enterprise Manager for Systems Infrastructure product of Oracle Enterprise Manager (component: Agent).  Supported versions that are affected are 13.5 and  24.1. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Enterprise Manager for Systems Infrastructure executes to compromise Oracle Enterprise Manager for Systems Infrastructure.  Successful attacks of this vulnerability can result in takeover of Oracle Enterprise Manager for Systems Infrastructure. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60753

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.927 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Installation).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Deployment executes to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60414

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.013 |

Vulnerability in the Oracle Outside In Technology product of Oracle Fusion Middleware (component: Outside In Core).   The supported version that is affected is 8.5.8. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Outside In Technology executes to compromise Oracle Outside In Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Outside In Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60413

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:37.900 |

Vulnerability in the Oracle Outside In Technology product of Oracle Fusion Middleware (component: Outside In Core).   The supported version that is affected is 8.5.8. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Outside In Technology executes to compromise Oracle Outside In Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Outside In Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60412

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:37.750 |

Vulnerability in the Oracle Outside In Technology product of Oracle Fusion Middleware (component: Outside In Core).   The supported version that is affected is 8.5.8. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Outside In Technology executes to compromise Oracle Outside In Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Outside In Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-60392

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T21:16:37.510 |

Vulnerability in the Oracle Outside In Technology product of Oracle Fusion Middleware (component: Outside In PDF Export SDK).   The supported version that is affected is 8.5.8. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Outside In Technology executes to compromise Oracle Outside In Technology.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Outside In Technology. CVSS 3.1 Base Score 7.8 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-55426

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-18T21:16:36.460 |

linuxfabrik-lib provides Python modules for database access, caching, shell execution, and API integrations, and Linuxfabrik Monitoring Plugins uses those modules to run external monitoring commands. From the earliest affected releases until linuxfabrik-lib 5.0.0 and Linuxfabrik Monitoring Plugins 6.0.0, check plugins embedded user-controlled values in command strings passed to lib.shell.shell_exec(), which split strings at pipe characters and executed the resulting commands. In check-plugins/restic-check/restic-check, the --repo parameter could inject a pipe-delimited command into a constructed restic invocation, and sudo-authorized execution allowed a compromised nagios or icinga account to run that command as root. The shared library also accepted command strings and a shell parameter, while numerous plugins constructed external commands from attacker-influenced arguments. The fixes require argv lists, always use shell=False, remove pipe splitting, and reject option-like positional values through lib.shell.safe_cli_value(). These issues are fixed in linuxfabrik-lib 5.0.0 and Linuxfabrik Monitoring Plugins 6.0.0.

### CVE-2026-24183

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-08-18T19:16:45.520 |

NVIDIA Cumulus Linux contains a vulnerability in the user management component, where an unprivileged user could use improper privilege management on the system. A successful exploit of this vulnerability might lead to escalation of privileges.

### CVE-2026-71551

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-18T18:19:32.483 |

Super Productivity is an advanced todo list app with integrated timeboxing and time tracking capabilities. Prior to 18.13.0, the EXEC IPC handler in electron/ipc-handlers/exec.ts accepts a command string from the renderer through the IPC.EXEC channel and executes it with child_process.exec(). The electron/preload.ts bridge exposes window.ea.exec() to renderer code, including community plugins executed with new Function(), without requiring nodeExecution permission. A confirmation dialog protects only the first execution, its persistence checkbox is selected by default, and approved commands are stored in the ALLOWED_COMMANDS value in simpleSettings for silent later execution with the desktop account's privileges. This issue is fixed in version 18.13.0.

### CVE-2026-66782

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-312` |
| Published | 2026-08-18T17:17:00.710 |

A flaw was found in the Submariner operator. This vulnerability allows for the exposure of a long-lived broker service account (SA) bearer token within the Submariner Custom Resource (CR) specification. An attacker with access to the cluster's etcd database or through `kubectl get` commands could obtain this token. The possession of this token grants full control over the mesh network, enabling unauthorized management of network resources such as endpoints and secrets.

### CVE-2026-76218

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-19T14:17:48.040 |

GitPython before 3.1.58 contains a remote code execution vulnerability in Repo.init that forwards unsafe git options without validation. Attackers can supply a template parameter pointing to a directory with malicious git hooks that execute arbitrary code when git operations are performed on the initialized repository.

### CVE-2026-76216

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T14:17:47.743 |

Vikunja through 2.4.0 contains a principal-type confusion vulnerability where LinkSharing principals with id N are treated as user principals with users.id == N at three permission checks lacking type guards. Attackers with a link-share JWT can remove victims from teams, enumerate and delete victim bot users, or read team rosters by exploiting id collisions in the autoincrement space.

### CVE-2026-67363

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-472;CWE-602` |
| Published | 2026-08-19T13:17:50.820 |

Joomla Extension - balbooa.com - Pre-auth Payment Amount Tampering in Balbooa Forms < 2.4.3.2 - The stripeCharges and payAuthorize endpoints accept the charge total from a client-controlled request parameter and forward it to the payment gateway without recomputing it from the form's configured product prices. Neither endpoint enforces authentication or CSRF checks. An unauthenticated attacker can purchase any priced item for an arbitrary amount (e.g., $0.01), and can additionally forge line items, quantities, and shipping.

### CVE-2026-71141

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:15.017 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle VM VirtualBox accessible data as well as  unauthorized read access to a subset of Oracle VM VirtualBox accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.7 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L).

### CVE-2026-71056

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.400 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Search).  Supported versions that are affected are 8.2.0.0.0, 12.2.1.4.0 and  26.01.0.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  While the vulnerability is in Oracle Business Intelligence Enterprise Edition, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70988

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:57.753 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70945

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.697 |

Vulnerability in the Oracle Payroll product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payroll.  While the vulnerability is in Oracle Payroll, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payroll accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70942

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.347 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70894

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:46.993 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Hyperion Data Relationship Management executes to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70857

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:41.867 |

Vulnerability in the Siebel CRM End User product of Oracle Siebel CRM (component: Open UI).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTPS to compromise Siebel CRM End User.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Siebel CRM End User, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM End User accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM End User accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-70828

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:37.970 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70827

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:37.833 |

Vulnerability in the Oracle MES for Process Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle MES for Process Manufacturing.  While the vulnerability is in Oracle MES for Process Manufacturing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle MES for Process Manufacturing accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70804

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:34.667 |

Vulnerability in the Oracle Public Sector Human Resources product of Oracle E-Business Suite (component: Regression Testing).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Public Sector Human Resources.  While the vulnerability is in Oracle Public Sector Human Resources, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Public Sector Human Resources accessible data as well as  unauthorized access to critical data or complete access to all Oracle Public Sector Human Resources accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70771

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:29.893 |

Vulnerability in the Oracle Warehouse Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTPS to compromise Oracle Warehouse Management.  While the vulnerability is in Oracle Warehouse Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Warehouse Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70723

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:24.790 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  While the vulnerability is in Oracle Hyperion Profitability and Cost Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70717

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:24.083 |

Vulnerability in Oracle Autonomous Health Framework (component: Cluster Health Analyzer).  Supported versions that are affected are 26-26.1.0, 26.2.0, 26.3.1, 26.5.0 and  26.5.2. Difficult to exploit vulnerability allows low privileged attacker with access to the physical communication segment attached to the hardware where the Oracle Autonomous Health Framework executes to compromise Oracle Autonomous Health Framework.  While the vulnerability is in Oracle Autonomous Health Framework, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Autonomous Health Framework accessible data as well as  unauthorized access to critical data or complete access to all Oracle Autonomous Health Framework accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70695

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.563 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Payments.  While the vulnerability is in Oracle Payments, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Payments accessible data as well as  unauthorized access to critical data or complete access to all Oracle Payments accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70694

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.450 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Payments.  While the vulnerability is in Oracle Payments, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Payments accessible data as well as  unauthorized access to critical data or complete access to all Oracle Payments accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70692

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.227 |

Vulnerability in the Oracle Marketing Encyclopedia System product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Marketing Encyclopedia System.  While the vulnerability is in Oracle Marketing Encyclopedia System, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Marketing Encyclopedia System accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70687

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:20.657 |

Vulnerability in the Oracle Marketing product of Oracle E-Business Suite (component: Audience).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Marketing.  While the vulnerability is in Oracle Marketing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Marketing accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62594

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.740 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Siebel CRM Integration. CVSS 3.1 Base Score 7.7 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:N/I:H/A:H).

### CVE-2026-62593

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:11.623 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: Open Integration).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Integration.  While the vulnerability is in Siebel CRM Integration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62571

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:08.953 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-62467

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.050 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61331

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.440 |

Vulnerability in the Oracle Financials Common Modules product of Oracle E-Business Suite (component: Common Components).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials Common Modules.  While the vulnerability is in Oracle Financials Common Modules, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Financials Common Modules accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61199

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:54.893 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).   The supported version that is affected is 14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60983

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.447 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 14.1.2.0.0 and  12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60969

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.503 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows low privileged attacker with network access via LDAP to compromise Oracle Unified Directory.  While the vulnerability is in Oracle Unified Directory, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 7.7 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-60733

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:41.210 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Composer).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  While the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data as well as  unauthorized read access to a subset of Oracle WebCenter Portal accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Portal. CVSS 3.1 Base Score 7.7 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-71307

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T20:17:23.577 |

Lemur manages TLS certificate creation. Prior to 1.9.3, GET /api/1/destinations and GET /api/1/destinations/ relied only on authentication while sibling write handlers required admin_permission. DestinationOutputSchema returned raw options and copied them into pluginOptions without redacting sensitive values. The sftp-destination plugin stored password and privateKeyPass values in plaintext, allowing even a read-only user to retrieve credentials for remote certificate-deployment hosts. The exposed credentials could permit direct access to SFTP systems and TLS material outside the Lemur security boundary. The fix requires administrator permission for destination reads and redacts options marked sensitive. This issue is fixed in version 1.9.3.

### CVE-2026-71303

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T20:17:23.403 |

Lemur manages TLS certificate creation. Prior to 1.9.3, _validate_acme_url enforced ACME_DIRECTORY_HOST_ALLOWLIST when an authority was created, but PUT /api/1/authorities/ passed options to lemur/authorities/service.py without applying the same check. A user holding an authority role could replace the stored acme_url with an internal service or instance-metadata URL such as 169.254.169.254. The next issuance operation loaded that value and passed it to ClientV2.get_directory, causing an outbound request from the Lemur backend. This bypassed the creation-time mitigation for CVE-2026-55166 and could expose internal services or cloud metadata. The fix revalidates acme_url whenever authority options are updated. This issue is fixed in version 1.9.3.

### CVE-2026-71365

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T16:18:16.157 |

A server-side request forgery (SSRF) vulnerability was found in AWX's webhook status callback mechanism. When processing GitHub pull request webhooks, AWX extracts the status callback URL (pull_request.statuses_url) from the incoming webhook payload without validating the target host against the expected Git provider. This URL is persisted in job extra variables and later used to send authenticated status updates. A user with admin role on a webhook-enabled job template can read the template's webhook signing key, forge a signed GitHub webhook payload with an arbitrary statuses_url, and cause AWX to POST status updates to an attacker-controlled or internal URL. The status update request includes the configured Git Personal Access Token (PAT) in the Authorization header, resulting in credential leakage to the attacker-specified endpoint.

### CVE-2026-53958

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287;CWE-915` |
| Published | 2026-08-18T22:16:54.717 |

4gaBoards is a boards system for realtime project management. Prior to 3.3.9, 4gaBoards allows an authenticated user to modify ssoGoogleId, ssoGoogleEmail, ssoGithubId, ssoGithubUsername, ssoGithubEmail, ssoMicrosoftId, ssoMicrosoftEmail, ssoOidcId, and ssoOidcEmail through PATCH /api/users/:id. The whitelist in server/api/controllers/users/update.js mass assigns these backend-managed identity attributes from user input. An attacker can place a victim's provider identifier on an attacker-controlled account, causing the default lookup in helpers such as server/api/helpers/users/get-create-one-for-github-sso.js to match the victim's first SSO login to the attacker's account before the email-linkage flow runs. The victim is logged into the attacker-controlled account, and projects, boards, or data the victim creates remain accessible through the attacker's original local credentials. This issue is fixed in version 3.3.9.

### CVE-2026-21584

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T22:16:50.460 |

This High severity Improper Authorization vulnerability was introduced in versions 10.0.0, 10.1.0, 10.2.0, 11.0.0, 12.0.0, and 12.1.0 of Bamboo Data Center. 
	
	This Improper Authorization vulnerability, with a CVSS Score of 7.6, allows an authenticated attacker to gain unintended access and can lead to the exposure of resources or functionality, possibly providing attackers with sensitive information or even execute arbitrary code. 
	
	Atlassian recommends that Bamboo Data Center customers upgrade to latest version, if you are unable to do so, upgrade your instance to one of the specified supported fixed versions:
		
		* Bamboo Data Center 10.2: Upgrade to a release greater than or equal to 10.2.22
		
		* Bamboo Data Center 12.1: Upgrade to a release greater than or equal to 12.1.10
		
		
	
	See the release notes (https://confluence.atlassian.com/bambooreleases/bamboo-release-notes-1189793869.html). You can download the latest version of Bamboo Data Center from the download center (https://www.atlassian.com/software/bamboo/download-archives). 
	
	This vulnerability was reported via our Penetration Testing program.

### CVE-2026-71048

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:04.600 |

Vulnerability in the Oracle Product Lifecycle Analytics product of Oracle Supply Chain (component: Installation Issues).   The supported version that is affected is 3.6.1. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Product Lifecycle Analytics.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Product Lifecycle Analytics accessible data as well as  unauthorized update, insert or delete access to some of Oracle Product Lifecycle Analytics accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Product Lifecycle Analytics. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-71027

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:02.270 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-71022

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:01.690 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Workbench).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-71021

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:01.567 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-71020

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:01.447 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-70960

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:54.503 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-70864

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.620 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows low privileged attacker having Load Testing for Web Apps privilege with network access via HTTP to compromise Oracle Application Testing Suite.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Application Testing Suite, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data as well as  unauthorized update, insert or delete access to some of Oracle Application Testing Suite accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-70803

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:34.523 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle General Ledger accessible data as well as  unauthorized read access to a subset of Oracle General Ledger accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle General Ledger. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-70791

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:32.820 |

Vulnerability in the Oracle Transportation Execution product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Transportation Execution.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Transportation Execution, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Transportation Execution accessible data as well as  unauthorized read access to a subset of Oracle Transportation Execution accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:H/A:N).

### CVE-2026-70786

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:32.100 |

Vulnerability in the Oracle Service Fulfillment Manager product of Oracle E-Business Suite (component: Fulfillment Engine).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Service Fulfillment Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Service Fulfillment Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Service Fulfillment Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Service Fulfillment Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-70764

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:29.060 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle General Ledger accessible data as well as  unauthorized update, insert or delete access to some of Oracle General Ledger accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle General Ledger. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-70725

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:25.023 |

Vulnerability in the Oracle Advanced Inbound Telephony product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Advanced Inbound Telephony.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Advanced Inbound Telephony accessible data as well as  unauthorized update, insert or delete access to some of Oracle Advanced Inbound Telephony accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Advanced Inbound Telephony. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-70678

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:19.610 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61296

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.640 |

Vulnerability in the Oracle Enterprise Asset Management product of Oracle E-Business Suite (component: Linear Asset Management).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Enterprise Asset Management.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Enterprise Asset Management, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Enterprise Asset Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Enterprise Asset Management accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61227

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:55.883 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Portal, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-61208

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:55.160 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Portal accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Portal accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Portal. CVSS 3.1 Base Score 7.6 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L).

### CVE-2026-60909

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.230 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:L/A:N).

### CVE-2026-60748

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:41.567 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle General Ledger.  While the vulnerability is in Oracle General Ledger, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle General Ledger accessible data as well as  unauthorized update, insert or delete access to some of Oracle General Ledger accessible data. CVSS 3.1 Base Score 7.6 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-71880

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-18T18:19:33.097 |

Interpretation of untrusted input in template engine in GBIF Integrated Publishing Toolkit versions before 3.3.4 allows remote authenticated attackers to access server-side files and state via template injection

### CVE-2026-49223

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:57.830 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend product review operations allow a low-privileged Vendor to manage reviews under another Vendor's products. The admin/sql/sqlite/product_review.sql queries accept a caller-controlled product_review_id and do not verify product_review.product_id against product.admin_id for the current admin_id. An attacker can read pending review content, ratings, author information, and moderation state, change review status, edit review content, or delete reviews, manipulating product review visibility and integrity. This issue is fixed in version 1.0.8.4.

### CVE-2026-49222

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:57.687 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend product question operations allow a low-privileged Vendor to manage questions under another Vendor's products. The admin/sql/sqlite/product_question.sql queries accept a caller-controlled product_question_id and do not verify product_question.product_id against product.admin_id for the current admin_id. An attacker can read pending question content and moderation data, change question status, edit question content, or delete questions, manipulating product Q&A visibility and integrity. This issue is fixed in version 1.0.8.4.

### CVE-2026-19869

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T17:16:57.227 |

@neo4j/graphql from 5.2.0 until the patched versions fails to enforce field-level @authentication rules on root custom-resolver fields when a type-level @authentication rule is also present on the same operation type. When both a type-level @authentication (on Query/Mutation) and a field-level @authentication (on a root custom-resolver field within that type) are declared, only the type-level rule is evaluated and the field-level rule is silently discarded. As a result a stricter per-field requirement — such as an admin-role JWT claim (jwt: { roles_INCLUDES: "admin" }) — is never checked, and any client that satisfies the coarser type-level requirement can invoke the more-restricted field. No token forgery is involved: a legitimately issued, correctly signed non-admin token (e.g. roles: ["user"]) is sufficient.

### CVE-2026-49227

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T16:17:13.653 |

Vvveb is a powerful and easy to use CMS with page builder to build websites, blogs or ecommerce stores. Prior to 1.0.8.4, Vvveb backend comment operations allow a low-privileged Author to manage comments under another Author's posts. The admin/controller/content/comment.php and admin/controller/content/comments.php controllers and the admin/sql/sqlite/comment.sql queries accept a caller-controlled comment_id without verifying comment.post_id against post.admin_id for the current admin_id. An attacker can read pending comment content and commenter email addresses, change moderation status, edit comment content, or delete comments, breaking author and moderation boundaries. This issue is fixed in version 1.0.8.4.

### CVE-2026-69189

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-200;CWE-639;CWE-862` |
| Published | 2026-08-18T15:17:00.930 |

Hoppscotch is an open source API development ecosystem. Prior to 2026.6.0, the team, teamMembers.user, RESTHistory, GQLHistory, currentRESTSession, currentGQLSession, environments, globalEnvironments, and settings GraphQL paths expose another workspace member's private User data, while toggleHistoryStarStatus and removeRequestFromHistory in the UserHistory service accept another user's history identifier without enforcing userUid ownership, allowing an authenticated workspace member to read private request history, session data, request contents, authorization headers, environment values, and settings and to modify or delete the victim's private history entries. This issue is fixed in version 2026.6.0.

### CVE-2026-76240

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:56.300 |

stigmem-node 0.9.0a1 interpolates Postgres backend schema identifiers into SQL strings without defensive quoting. In the affected code path the schema value is operator-controlled, but the unsafe pattern could allow SQL injection if a schema name were derived from tenant, request, or user input. Fixed in 0.9.0a2, which adds identifier quoting and validation. As a workaround, only configure schema names from trusted deployment configuration.

### CVE-2026-76235

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-08-19T13:18:11.637 |

A memory leak flaw was found in cockpit-ws. The login page handler leaks a heap allocation on every unauthenticated request that carries a CockpitLang cookie, allowing a remote unauthenticated attacker to exhaust memory on the host and cause a denial of service.

### CVE-2026-73394

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T13:18:08.670 |

Unauthenticated Broken Access Control in Stitch Express <= 1.9.0 versions.

### CVE-2026-73386

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-19T13:18:07.910 |

Unauthenticated Sensitive Data Exposure in Track Geolocation Of Users Using Contact Form 7 <= 3.0.2 versions.

### CVE-2026-73385

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T13:18:07.777 |

Unauthenticated Broken Access Control in Outranking Plugin Options <= 1.1.3 versions.

### CVE-2026-73384

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-08-19T13:18:07.650 |

Unauthenticated Sensitive Data Exposure in Pay with Contact Form 7 <= 1.0.4 versions.

### CVE-2026-14861

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T06:17:34.067 |

The User Verification by PickPlugins WordPress plugin through 2.0.47 does not verify that a request to resend a verification email is authorized to act on the supplied user, nor bind the protecting token to that user, allowing unauthenticated attackers to reset arbitrary users' email-verification status and lock them, including administrators, out of their accounts.

### CVE-2026-50142

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-770` |
| Published | 2026-08-18T22:16:52.633 |

libheif is a HEIF and AVIF file format decoder and encoder. From 1.19.0 until 1.23.0, a crafted HEIF sequence accepted by heif_context_read_from_memory() with the msf1 sequence brand can cause unbounded heap allocation. In libheif/sequences/seq_boxes.cc, Box_stsz::parse() applies max_sequence_frames only to variable-size samples, so fixed-size mode accepts an attacker-controlled sample_count without a bound. In libheif/sequences/track.cc, Track::load() also adds current_sample_idx and samples_per_chunk in 32-bit arithmetic, allowing the consistency check to be bypassed by wraparound. The resulting values reach the Chunk::Chunk() allocation path, which can consume gigabytes of memory and crash or stall the process through memory exhaustion. This issue is fixed in version 1.23.0.

### CVE-2026-73938

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:26.913 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73936

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:26.680 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73935

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:26.570 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73934

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:26.453 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73927

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.663 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.20. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73915

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:24.370 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73908

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:23.573 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:23.460 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73903

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:23.000 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-73902

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:22.883 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73890

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:21.533 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73887

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:21.180 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP/2 to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73884

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.843 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73883

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.733 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-73882

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.620 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-73879

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.277 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-73878

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.163 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71160

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:17.330 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in takeover of Helidon. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:17.050 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71153

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:16.393 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 1.4.20. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-71142

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:15.140 |

Vulnerability in the Oracle Communications Unified Inventory Management product of Oracle Communications (component: Security Component).  Supported versions that are affected are 7.5.0-7.5.1, 7.6.0-7.8.0 and  8.0.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Communications Unified Inventory Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Communications Unified Inventory Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71117

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:12.350 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  While the vulnerability is in Oracle Hyperion Financial Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71116

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:12.223 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in takeover of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H).

### CVE-2026-71113

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:11.870 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows unauthenticated attacker with network access via RDP to compromise Oracle VM VirtualBox.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-71107

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:11.060 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Server).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71092

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:09.450 |

Vulnerability in the PeopleSoft Enterprise FIN Lease Administration product of Oracle PeopleSoft (component: Lease Administration).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise FIN Lease Administration executes to compromise PeopleSoft Enterprise FIN Lease Administration.  While the vulnerability is in PeopleSoft Enterprise FIN Lease Administration, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise FIN Lease Administration accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise FIN Lease Administration accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-71069

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:06.917 |

Vulnerability in the Oracle Agile PLM MCAD Connector product of Oracle Supply Chain (component: CAX Client).   The supported version that is affected is 3.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Agile PLM MCAD Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM MCAD Connector. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71061

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:05.967 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: BI Platform Security).  Supported versions that are affected are 8.2.0.0.0 and  26.01.0.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Business Intelligence Enterprise Edition accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71043

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:04.110 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Security).   The supported version that is affected is 9.3.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Agile PLM accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71038

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.543 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71034

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.080 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Forge).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SOAP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71023

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:01.810 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N).

### CVE-2026-70987

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:57.637 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70986

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:57.530 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70985

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:57.410 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70973

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.983 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70955

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.840 |

Vulnerability in the Oracle Commerce Platform product of Oracle Commerce (component: Dynamo Application Framework).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Commerce Platform executes to compromise Oracle Commerce Platform.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Platform. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70947

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.930 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Other issue).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Purchasing accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70946

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:52.817 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70937

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:51.777 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70930

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.983 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  Successful attacks of this vulnerability can result in takeover of Oracle Order Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70927

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:50.630 |

Vulnerability in the Oracle Workflow product of Oracle E-Business Suite (component: Workflow Notification Mailer).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Workflow.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Workflow. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-70910

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.870 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70908

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.633 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Helidon. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-70906

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:48.393 |

Vulnerability in Oracle Java SE (component: 2D).  Supported versions that are affected are Oracle Java SE: 25.0.4 and  26.0.2. Easily exploitable vulnerability allows unauthenticated attacker with network access via multiple protocols to compromise Oracle Java SE.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Java SE. Note: This vulnerability can be exploited by using APIs in the specified Component, e.g., through a web service which supplies data to the APIs. This vulnerability also applies to Java deployments, typically in clients running sandboxed Java Web Start applications or sandboxed Java applets, that load and run untrusted code (e.g., code that comes from the internet) and rely on the Java sandbox for security. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-70896

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.237 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.817 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70890

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.693 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70889

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:45.570 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70875

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:43.867 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Data Relationship Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70865

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.743 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Difficult to exploit vulnerability allows low privileged attacker having Load Testing for Web Apps privilege with network access via HTTPS to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in takeover of Oracle Application Testing Suite. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70856

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:41.737 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Migration).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Siebel CRM Deployment. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-70832

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.507 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70829

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.100 |

Vulnerability in the Oracle Process Manufacturing Systems product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Process Manufacturing Systems.  Successful attacks of this vulnerability can result in takeover of Oracle Process Manufacturing Systems. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70822

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:37.167 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70810

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.517 |

Vulnerability in the Oracle Scripting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Scripting.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Scripting accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:33.960 |

Vulnerability in the Oracle SDP Number Portability product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle SDP Number Portability.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle SDP Number Portability accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70777

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:30.767 |

Vulnerability in the Oracle iSupplier Portal product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iSupplier Portal.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle iSupplier Portal accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70772

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:30.017 |

Vulnerability in the Oracle Warehouse Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Warehouse Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Warehouse Management accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70763

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:28.943 |

Vulnerability in the Oracle Operations Intelligence product of Oracle E-Business Suite (component: Daily Business Intelligence).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Operations Intelligence.  Successful attacks of this vulnerability can result in takeover of Oracle Operations Intelligence. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70752

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:28.007 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Reporting accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70724

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:24.900 |

Vulnerability in the MySQL Cluster product of Oracle MySQL (component: Cluster: General).  Supported versions that are affected are 8.0.0-8.0.48, 8.4.0-8.4.11 and  9.7.0-9.7.2. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise MySQL Cluster.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of MySQL Cluster. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-70713

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:23.610 |

Vulnerability in the Oracle iSetup product of Oracle E-Business Suite (component: General Ledger Update Transform, Reports).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle iSetup.  Successful attacks of this vulnerability can result in takeover of Oracle iSetup. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70706

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.800 |

Vulnerability in the Oracle Sales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales.  Successful attacks of this vulnerability can result in takeover of Oracle Sales. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70700

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.130 |

Vulnerability in the Oracle Payables product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Payables.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Payables. CVSS 3.1 Base Score 7.5 (Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H).

### CVE-2026-70696

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.673 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via TCP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payments accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-70691

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.110 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Engineering Data Management. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70681

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:19.953 |

Vulnerability in the Oracle Applications DBA product of Oracle E-Business Suite (component: JRI and other Java utils).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Applications DBA.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Applications DBA. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-62554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:07.847 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-62552

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:07.600 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-62550

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:07.300 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-62545

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:07.067 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.530 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Events).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via SQL to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-61007

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.887 |

Vulnerability in the Oracle WebCenter Sites product of Oracle Fusion Middleware (component: WebCenter Sites).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Sites.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Sites accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60993

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:50.910 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  Successful attacks of this vulnerability can result in takeover of Oracle Identity Manager Connector. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60975

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.840 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Security).  Supported versions that are affected are 8.61 and  8.62. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  While the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60956

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:49.037 |

Vulnerability in the JD Edwards EnterpriseOne US Payroll product of Oracle JD Edwards (component: Payroll).   The supported version that is affected is 9.2. Difficult to exploit vulnerability allows low privileged attacker with network access via JDENET to compromise JD Edwards EnterpriseOne US Payroll.  Successful attacks of this vulnerability can result in takeover of JD Edwards EnterpriseOne US Payroll. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60914

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.347 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60906

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.117 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60889

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:46.527 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60850

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:45.010 |

Vulnerability in the Oracle Unified Directory product of Oracle Fusion Middleware (component: OUD Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via LDAP to compromise Oracle Unified Directory.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Unified Directory accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60808

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.050 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Email Marketing).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Siebel Apps - Marketing executes to compromise Siebel Apps - Marketing.  While the vulnerability is in Siebel Apps - Marketing, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Marketing accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Marketing accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-60769

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.880 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in takeover of Oracle General Ledger. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.523 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in takeover of Siebel Apps - Marketing. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60679

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-18T21:16:38.850 |

Vulnerability in the Oracle WebLogic Server product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0, 14.1.1.0.0, 14.1.2.0.0 and  15.1.1.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via T3, IIOP to compromise Oracle WebLogic Server.  Successful attacks of this vulnerability can result in takeover of Oracle WebLogic Server. CVSS 3.1 Base Score 7.5 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60590

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:38.367 |

Vulnerability in the Oracle Hospitality Simphony product of Oracle Food and Beverage Applications (component: POS).  Supported versions that are affected are 19.8-19.8.5, 19.9-19.9.3 and  19.10-19.10.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hospitality Simphony.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hospitality Simphony accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60393

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:37.633 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Lifecycle Management).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-60391

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:37.370 |

Vulnerability in the Oracle Hyperion Financial Reporting product of Oracle Hyperion (component: Server).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Financial Reporting.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Reporting accessible data. CVSS 3.1 Base Score 7.5 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N).

### CVE-2026-71676

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-18T20:17:24.917 |

Buffer Overflow vulnerability in Open5GS v.2.7.0 allows a remote attacker to cause a denial of service via the NAS 5GS decoder chain, triggered when the message type byte of a NAS PDU is mutated

### CVE-2026-71675

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-401` |
| Published | 2026-08-18T20:17:24.790 |

An issue in Open5GS v.2.7.0 allows a remote attacker to cause a denial of service via the ngap_send_to_nas() function in src/amf/ngap-path.c

### CVE-2026-65984

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-18T20:17:20.557 |

FUXA is a web-based Process Visualization (SCADA/HMI/Dashboard) software. In 1.3.2 and earlier, POST /api/refresh in server/api/auth/index.js falls back from current user data to decoded.groups, including when the user is deleted or groups is zero, and POST /api/heartbeat in server/api/index.js re-signs inbound JWT claims without validating the current database record. An attacker who possesses a previously issued privileged refresh cookie or access token can continue minting privileged JWTs after account deletion, disablement, role removal, or demotion. Continued refresh-cookie rotation can extend the stale session and preserve unauthorized access to user management, project manipulation, runtime configuration, scripts, and backdoor-account creation. This issue is fixed in version 1.3.3.

### CVE-2026-52829

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617;CWE-843` |
| Published | 2026-08-18T20:17:18.330 |

ZEBRA is a Zcash node written entirely in Rust. Prior to 4.5.0, an unauthenticated IPv4 peer can deterministically terminate a synced Zebra node using the default Linux dual-stack listener configuration. The handshake path canonicalized an IPv4-mapped IPv6 PeerSocketAddr such as ::ffff:127.0.0.1 to plain IPv4 before storing it through MetaAddr::new_connected, but the mempool misbehavior path forwarded the raw transient address to MetaAddrChange::UpdateMisbehavior. In zebra-network/src/meta_addr.rs, apply_to_meta_addr then compared the canonical address-book entry with the raw update address and reached its unexpected address mismatch assertion. After the misbehavior batch flush, panic equals abort terminated zebrad; the peer only needed to complete a P2P handshake and advertise an invalid mempool transaction. This issue is fixed in version 4.5.0.

### CVE-2026-52481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-18T20:17:16.383 |

An issue in SJRC F11 SJ-GPS-PRO firmware build 2019-09-17 allows a remote attacker to obtain sensitive information via the tcp_actions() function

### CVE-2026-47629

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-18T19:16:52.217 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause improper input validation. A successful exploit might lead to denial of service.

### CVE-2026-47628

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-18T19:16:51.740 |

NVIDIA Triton Inference Server for Linux contains a vulnerability where an attacker could cause an allocation of resources without limits. A successful exploit might lead to denial of service.

### CVE-2026-24184

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-18T19:16:45.980 |

NVIDIA Cumulus Linux contains a vulnerability in the Link Layer Discovery Protocol (LLDP) daemon component, where an unauthenticated attacker on an adjacent network could cause buffer overflow by sending crafted LLDP frames. A successful exploit of this vulnerability might lead to code execution.

### CVE-2026-63337

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-470` |
| Published | 2026-08-18T17:17:00.423 |

The RabbitMQ Java client library allows Java and JVM-based applications to connect to and interact with RabbitMQ nodes. Prior to 5.33.0, com.rabbitmq.tools.jsonrpc.ProcedureDescription receives a javaReturnType value in an untrusted system.describe response and passes it through JSONUtil.tryFill, setJavaReturnType, and computeReturnTypeAsJavaClass to Class.forName(javaReturnType) with initialization enabled. An attacker able to answer the JsonRpcClient request through a shared broker or network interception can select a class already present in the victim JVM and trigger its static initializer, while JsonRpcClient.java later passes getReturnType output to mapper.parse and may also create type confusion. Successful exploitation can affect confidentiality, integrity, and availability in the client process. This issue is fixed in version 5.33.0.

### CVE-2026-50578

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-18T17:16:58.933 |

ePA 3.x Integration implements the authorization workflow and writes Medical Information Objects to Germany's electronic patient record. Prior to 1.3.0, ePA 3.x Integration disables TLS certificate verification for both ePA connections in app/vau/VAUProtokoll.py and Konnektor connections in app/konnektor/Konnektor.py. A network-positioned attacker can present an arbitrary certificate, terminate the TLS connection, and intercept ePA traffic. The VAU protocol does not provide an effective fallback because its application-layer certificate validation is also broken in affected versions. The Konnektor session uses self.session.verify set to False while the client authenticates with self.session.cert, so an attacker impersonating the Konnektor can receive the client's mutual TLS certificate exchange and observe smartcard operations. This issue is fixed in version 1.3.0.

### CVE-2026-19500

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-18T16:17:02.647 |

The Entries component in Brainstorm Force SureForms version, less than 2.12.3, does not enforce adequate limits on user-controlled form fields or submitted content during processing and rendering, which allows a remote attacker to exhaust server resources, prevent administrators from accessing the Entries interface, and trigger HTTP 500 errors via crafted form submissions.

### CVE-2026-73997

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-18T15:17:08.747 |

Unauthenticated Denial of Service Attack in Starter Templates by Kadence WP <= 2.3.3 versions.

### CVE-2026-73994

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T15:17:08.320 |

Unauthenticated Broken Access Control in Charitable <= 1.8.11.3 versions.

### CVE-2026-73377

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T15:17:05.550 |

Unauthenticated Broken Access Control in Ultimate Maps by Supsystic < 1.5.0 versions.

### CVE-2026-73181

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T15:17:01.790 |

Unauthenticated Arbitrary File Download in Extra Product Options & Add-Ons for WooCommerce < 7.6 versions.

### CVE-2026-66622

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:16:57.430 |

Unauthenticated SQL Injection in Depicter Slider <= 4.8.0 versions.

### CVE-2026-56684

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-18T15:16:55.463 |

Valkey is a distributed key-value database. Prior to 7.2.14, 8.0.10, 8.1.9, 9.0.5, and 9.1.1, Valkey's tlsProcessPendingData function iterates pending_list while an authenticated client can trigger CLIENT KILL, causing connTLSClose to delete the iterator's cached next node and producing a use-after-free that can crash the server or potentially allow remote code execution when TLS is enabled. This issue is fixed in versions 7.2.14, 8.0.10, 8.1.9, 9.0.5, and 9.1.1.

### CVE-2026-32549

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T15:16:53.487 |

Unauthenticated Broken Access Control in ThumbPress < 6.5 versions.

### CVE-2026-32481

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T15:16:53.210 |

Unauthenticated Broken Authentication in Ezoic <= 2.22.11 versions.

### CVE-2026-32472

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-18T15:16:52.817 |

Unauthenticated Broken Access Control in Online Contact Widget <= 1.3.0 versions.

### CVE-2026-58088

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362;CWE-787` |
| Published | 2026-08-19T08:17:12.983 |

The ELF core dump code counted the number of dumpable VM map entries, allocated a buffer for the corresponding program headers, then iterated over the map a second time to populate them.  A process sharing the address space via rfork(2) can mutate the map between the two passes, causing the second pass to write program headers past the end of the buffer.

An unprivileged local user sharing an address space with a process that dumps core can trigger an out-of-bounds write on the kernel heap, potentially leading to privilege escalation.

### CVE-2026-71143

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:15.253 |

Vulnerability in the Oracle Communications Unified Inventory Management product of Oracle Communications (component: Third Party).  Supported versions that are affected are 7.5.0, 7.5.1, 7.6.0-7.8.0 and  8.0.1. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Communications Unified Inventory Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Communications Unified Inventory Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Communications Unified Inventory Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-71009

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:00.190 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70898

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.470 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70823

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:37.303 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70790

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:32.673 |

Vulnerability in the Oracle Telecommunications Billing Integrator product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Telecommunications Billing Integrator.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Telecommunications Billing Integrator, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Telecommunications Billing Integrator accessible data. CVSS 3.1 Base Score 7.4 (Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N).

### CVE-2026-70783

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:31.660 |

Vulnerability in the Oracle Service Contracts product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Service Contracts.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Service Contracts accessible data as well as  unauthorized access to critical data or complete access to all Oracle Service Contracts accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70779

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:31.073 |

Vulnerability in the Oracle iSupplier Portal product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle iSupplier Portal.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle iSupplier Portal accessible data as well as  unauthorized access to critical data or complete access to all Oracle iSupplier Portal accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70734

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.087 |

Vulnerability in Oracle Autonomous Health Framework (component: Trace File Analyzer).  Supported versions that are affected are 26-26.1.0, 26.2.0, 26.3.1, 26.5.0 and  26.5.2. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Autonomous Health Framework executes to compromise Oracle Autonomous Health Framework.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Autonomous Health Framework, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Autonomous Health Framework accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Autonomous Health Framework. CVSS 3.1 Base Score 7.4 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:R/S:C/C:N/I:H/A:H).

### CVE-2026-70699

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.013 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Payments accessible data as well as  unauthorized access to critical data or complete access to all Oracle Payments accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70672

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:18.927 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Reports Developer.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Reports Developer accessible data as well as  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62538

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.377 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62492

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:03.877 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60933

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.973 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Content accessible data as well as  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60915

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:47.460 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Helidon accessible data as well as  unauthorized access to critical data or complete access to all Helidon accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60856

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:45.260 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Install and Packaging).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60820

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:44.163 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60803

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.930 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel Apps - Marketing accessible data as well as  unauthorized access to critical data or complete access to all Siebel Apps - Marketing accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60797

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.697 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60792

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.467 |

Vulnerability in the Siebel CRM Deployment product of Oracle Siebel CRM (component: Server Infrastructure).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Siebel CRM Deployment.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Deployment accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Deployment accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60766

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.640 |

Vulnerability in the Siebel CRM Integration product of Oracle Siebel CRM (component: REST).  Supported versions that are affected are 17.0-26.6. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTPS to compromise Siebel CRM Integration.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Siebel CRM Integration accessible data as well as  unauthorized access to critical data or complete access to all Siebel CRM Integration accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-60759

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:42.390 |

Vulnerability in the Oracle Internet Procurement Connector product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Internet Procurement Connector.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Internet Procurement Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Internet Procurement Connector accessible data. CVSS 3.1 Base Score 7.4 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70666

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T20:17:23.237 |

Lemur manages TLS certificate creation. Prior to 1.9.3, an authority-role member could update acme_url through PUT /api/1/authorities/ without revalidation and direct setup_acme_client_no_retry to an attacker-controlled ACME server. ACME directory and order responses contain newNonce, newOrder, authorizations, and finalize URLs chosen by that server. The Lemur ClientV2 followed those URLs without requiring their host to match the configured directory host, allowing JWS-signed requests to internal services or cloud metadata endpoints. The issue required an ACME authority and a user authorized for that authority, but did not require global administrator privileges. The fix revalidates updates and introduces _PinnedClientNetwork to enforce a single allowed host for the complete ACME flow. This issue is fixed in version 1.9.3.

### CVE-2026-50577

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-323` |
| Published | 2026-08-18T17:16:58.790 |

ePA 3.x Integration implements the authorization workflow and writes Medical Information Objects to Germany's electronic patient record. Prior to 1.3.0, ePA 3.x Integration leaves request_counter unchanged in app/vau/VAUProtokoll.py while constructing VAU messages. The frozen client request counter causes the server side to reuse AES-GCM nonce and key combinations across responses. A network attacker who collects repeated ciphertexts can recover the XOR of plaintexts and use predictable inner HTTP headers and JSON fields to recover sensitive data, including patient health records. Repeated nonces can also enable recovery of the GHASH authentication key through the Joux forbidden attack, allowing forged AES-GCM messages and injection of malicious responses. The response-counter check also fails to maintain last_response_counter, weakening replay and ordering validation. This issue is fixed in version 1.3.0.

### CVE-2026-66635

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-18T15:16:58.087 |

Unauthenticated Cross Site Request Forgery (CSRF) in Slider by 10Web <= 1.2.62 versions.

### CVE-2026-59825

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-18T15:16:55.623 |

Mastodon is a free, open-source social network server based on ActivityPub. Prior to 4.4.19 and from 4.5.0 until 4.5.12, Mastodon's app/models/concerns/user/ldap_authenticable.rb mutates OpenSSL::SSL::SSLContext::DEFAULT_PARAMS when LDAP authentication uses LDAP_TLS_NO_VERIFY=true, disabling SSL and TLS certificate verification globally for requests made by puma web processes while sidekiq background jobs remain unaffected. This issue is fixed in versions 4.4.19 and 4.5.12.

### CVE-2026-18534

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-1021` |
| Published | 2026-08-18T15:16:49.667 |

ArcSearch for iOS versions prior to 1.48.0 could keep the address bar hidden after a page-initiated scroll, allowing attacker-controlled content to imitate browser interface elements and increasing spoofing risk.

### CVE-2026-76241

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-494` |
| Published | 2026-08-19T14:17:56.430 |

stigmem-node 0.9.0a1 allows plugin signature enforcement to be disabled via a single configuration flag without a second explicit acknowledgment. If that setting is carried into an environment where plugin directories are writable by less-trusted users, unsigned (potentially malicious) plugin code could be loaded and executed, resulting in arbitrary code execution. Fixed in 0.9.0a2, which requires a second explicit acknowledgment to disable signature enforcement.

### CVE-2026-73933

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:26.340 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-73918

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:24.743 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-73894

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:21.983 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-73891

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:21.650 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Helidon. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-71138

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:14.677 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox as well as  unauthorized update, insert or delete access to some of Oracle VM VirtualBox accessible data and  unauthorized read access to a subset of Oracle VM VirtualBox accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H).

### CVE-2026-71136

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:14.440 |

Vulnerability in the Oracle VM VirtualBox product of Oracle Virtualization (component: Core).   The supported version that is affected is 7.2.14. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle VM VirtualBox executes to compromise Oracle VM VirtualBox.  While the vulnerability is in Oracle VM VirtualBox, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle VM VirtualBox as well as  unauthorized update, insert or delete access to some of Oracle VM VirtualBox accessible data and  unauthorized read access to a subset of Oracle VM VirtualBox accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:H).

### CVE-2026-71094

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:09.563 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Presentation Services).   The supported version that is affected is 12.2.1.4.0. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-70800

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:34.103 |

Vulnerability in the Oracle SDP Number Portability product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with logon to the infrastructure where Oracle SDP Number Portability executes to compromise Oracle SDP Number Portability.  While the vulnerability is in Oracle SDP Number Portability, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle SDP Number Portability accessible data as well as  unauthorized read access to a subset of Oracle SDP Number Portability accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle SDP Number Portability. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:H/A:L).

### CVE-2026-62551

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:07.457 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Infrastructure Technology accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Infrastructure Technology. CVSS 3.1 Base Score 7.3 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L).

### CVE-2026-61339

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:00.673 |

Vulnerability in the Siebel CRM Cloud Applications product of Oracle Siebel CRM (component: Siebel Cloud Manager).  Supported versions that are affected are 22.3-26.6. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Siebel CRM Cloud Applications executes to compromise Siebel CRM Cloud Applications.  While the vulnerability is in Siebel CRM Cloud Applications, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Cloud Applications accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Cloud Applications accessible data. CVSS 3.1 Base Score 7.3 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-15571

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-341` |
| Published | 2026-08-18T21:16:33.910 |

A flaw was found in the legacy client-initiated account-linking endpoint of Keycloak, a widely used open-source identity and access management solution. The mechanism used to protect the account-linking process from unauthorized requests relies on a hash that can be predicted by a malicious OIDC client. By tricking a user into authenticating, an attacker-controlled client can forge a valid linking URL to connect the victim's account to an attacker's external identity. This results in a full account takeover, allowing the attacker to log in as the victim.

### CVE-2026-71417

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-18T20:17:24.237 |

Lemur manages TLS certificate creation. Prior to 1.9.3, POST /api/1/certificates/upload allowed a non-read-only user to create a duplicate row using another certificate body, authority_id, serial, or external_id without requiring permission on the underlying authority. PUT /api/1/certificates//revoke authorized the caller against only the selected Lemur row, so the creator of the duplicate bypassed CertificatePermission. The duplicate had no cert.endpoints, which also bypassed the safeguard that prevents revocation of deployed certificates. Issuer plugins then revoked the real CA-side certificate using certificate.body or external_id under the stored authority credentials. An attacker could therefore revoke arbitrary managed certificates and cause fleet-wide TLS denial of service. The fix rejects duplicate authority_id and serial identities, requires authority access on upload, and checks every matching row during revocation. This issue is fixed in version 1.9.3.

### CVE-2026-59915

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-272` |
| Published | 2026-08-18T20:17:19.880 |

Dell Alienware Command Center (AWCC), versions prior to 6.14.20.0, contain a Least Privilege Violation vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of Privileges.

### CVE-2026-32657

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-61` |
| Published | 2026-08-18T18:17:28.573 |

Dell AppSync Version 4.6.0.0, Dell Metro Node Version 8.0.0, Dell UCC Edge Version 3.0.1, Dell VxRail Version 8.0.322, Dell PowerMax Version 10.3.0, Dell Unity Version 5.4, Dell PowerFlex Manager Version 4.5.4, Dell PowerFlex Intelligent Catalog Versions 46.377.00 and 46.382.00 and Dell PowerFlex Rack version 4.5.4 and prior versions, contain(s) an UNIX Symbolic Link (Symlink) Following vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-75857

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-18T16:18:21.520 |

CodeWhale versions >= 0.8.41 and < 0.8.64 contain a vulnerability in the exec_shell_interact (alias exec_interact) tool, whose approval_requirement returns ApprovalRequirement::Auto. This overrides the default Required approval for code-executing tools, so LLM-controlled stdin is written into an already-approved long-running interactive shell (e.g., a python3 -i REPL, mysql, ssh, or sudo -i session) without any approval prompt. An attacker who can inject instructions via untrusted content the agent ingests (a fetched page, MCP result, or repo file) can cause commands to run at the privilege level of that approved process. Fixed in 0.8.64.

### CVE-2026-76238

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-19T14:17:56.013 |

stigmem versions before 0.9.0a12 contain a broken object level authorization vulnerability in the decay sweep endpoint that allows authenticated attackers with write credentials for one tenant to execute decay operations affecting all tenants. Attackers can submit POST requests to the decay sweep endpoint with ttl_seconds=0 to expire facts across all tenants, or use dry_run to obtain cross-tenant fact counts and existence information.

### CVE-2026-76236

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-19T14:17:54.810 |

stigmem-node before 0.9.0a12 contains a cross-tenant broken object level authorization (BOLA) flaw in the RTBF (right-to-be-forgotten) tombstone mechanism. issue_tombstone defaulted the tenant to "default" instead of the caller's tenant, allowing deletion records to be written to the wrong tenant, and the read-suppression path (_get_tombstone_filter and the tombstone scope cache) lacked a tenant_id predicate, so tombstone suppression was applied tenant-blind across fact queries and provenance reads. As a result, a tenant's deletion could be attributed to the wrong tenant and tombstone suppression could either hide facts belonging to other tenants or fail to hide facts within the correct tenant, undermining data isolation and RTBF guarantees. The issue is exploitable only on multi-tenant deployments running the opt-in stigmem-plugin-multi-tenant; single-tenant deployments are unaffected. Fixed in 0.9.0a12.

### CVE-2026-76219

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-19T14:17:48.187 |

GitPython versions before 3.1.58 contain an arbitrary file overwrite vulnerability in IndexFile.from_tree, IndexFile.reset, and IndexFile.merge_tree methods that append caller-influenced treeish strings to git read-tree without option validation or argument separation. Attackers can inject the --index-output option to overwrite arbitrary files with a valid git-index blob, destroying existing file content at attacker-controlled writable paths.

### CVE-2026-70421

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-19T14:17:38.743 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Privilege Management vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-54796

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-19T14:17:34.360 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-54794

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T14:17:34.040 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains a Server-Side Request Forgery (SSRF) vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to Information exposure.

### CVE-2026-75981

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T07:16:59.907 |

The TranslatePress – Translate Multilingual sites with AI Translation plugin for WordPress is vulnerable to unauthenticated Stored Cross-Site Scripting in versions up to and including 3.2.5. The special gettext markers '#!trpst#' and '#!trpen#' are unconditionally rewritten to '<' and '>' by translate_page() in includes/class-translation-render.php (lines 538-539). Because those markers are plain text with no HTML-special characters, an unauthenticated attacker can embed them in a comment; the markers survive wp_kses, and when the post is viewed in a secondary language the substitution turns the attacker's '#!trpst#img ... #!trpen#' into a real <img> tag. remove_tags_from_output() only strips <script>/<style>, so an <img onerror=...> executes in the visitor's browser.

### CVE-2026-15780

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T07:16:27.773 |

The WP Statistics – Simple, privacy-friendly Google Analytics alternative plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'utm_campaign' parameter in all versions up to, and including, 14.16.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The payload can be planted without authentication via the public /wp-statistics/v2/hit REST endpoint, because the required signature is exposed on the public homepage and a base64-encoded page_uri POST parameter overrides the previously sanitized REQUEST_URI, allowing the malicious utm_campaign value to bypass sanitization and be stored in the database.

### CVE-2026-13174

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-19T06:17:32.200 |

The Eventin  WordPress plugin before 4.1.21 does not verify ownership or capability before deleting user accounts, allowing users with contributor-level access and above to permanently delete other users' accounts.

### CVE-2026-73928

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:25.773 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.3. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-73886

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:21.067 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-73885

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:20.957 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.18. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-73876

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:19.923 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 4.5.1. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-73875

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:19.807 |

Vulnerability in the Helidon product of Oracle Fusion Middleware (component: Imperative Web Server).   The supported version that is affected is 3.2.19. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Helidon.  While the vulnerability is in Helidon, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Helidon accessible data as well as  unauthorized read access to a subset of Helidon accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-71104

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.720 |

Vulnerability in the Oracle HRMS (Netherlands) product of Oracle E-Business Suite (component: Netherlands Payroll).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle HRMS (Netherlands).  Successful attacks of this vulnerability can result in takeover of Oracle HRMS (Netherlands). CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71099

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.150 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Analytics Web Answers).   The supported version that is affected is 26.01.0.0.0. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71032

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:02.840 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized read access to a subset of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-71030

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:02.610 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Endeca Application Controller).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  While the vulnerability is in Oracle Commerce Guided Search / Oracle Commerce Experience Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data as well as  unauthorized read access to a subset of Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N).

### CVE-2026-70950

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:53.270 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70939

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:51.997 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70932

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:51.213 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle Order Management executes to compromise Oracle Order Management.  While the vulnerability is in Oracle Order Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Order Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Order Management accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70861

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.243 |

Vulnerability in the PeopleSoft Enterprise FIN Common Objects Brazil product of Oracle PeopleSoft (component: Common Objects).   The supported version that is affected is 9.1. Easily exploitable vulnerability allows high privileged attacker with network access via T3, IIOP to compromise PeopleSoft Enterprise FIN Common Objects Brazil.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise FIN Common Objects Brazil. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70834

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.790 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70820

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.897 |

Vulnerability in the Oracle Call Center Technology product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Call Center Technology.  Successful attacks of this vulnerability can result in takeover of Oracle Call Center Technology. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70797

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:33.690 |

Vulnerability in the Oracle Purchasing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Purchasing.  Successful attacks of this vulnerability can result in takeover of Oracle Purchasing. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70796

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:33.547 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where Oracle General Ledger executes to compromise Oracle General Ledger.  While the vulnerability is in Oracle General Ledger, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle General Ledger accessible data as well as  unauthorized access to critical data or complete access to all Oracle General Ledger accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:N).

### CVE-2026-70781

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:31.370 |

Vulnerability in the Oracle Proposals product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Proposals.  Successful attacks of this vulnerability can result in takeover of Oracle Proposals. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70735

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.213 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Profitability and Cost Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62616

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:14.253 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via SMTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Reports Developer. CVSS 3.1 Base Score 7.2 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:L).

### CVE-2026-62540

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.603 |

Vulnerability in the Oracle Cost Management product of Oracle E-Business Suite (component: Cost Planning).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Cost Management.  Successful attacks of this vulnerability can result in takeover of Oracle Cost Management. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-62459

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:02.450 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows high privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Calculation Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:L/A:L).

### CVE-2026-60994

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:51.030 |

Vulnerability in the Oracle Identity Manager Connector product of Oracle Fusion Middleware (component: Core).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.1.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Identity Manager Connector executes to compromise Oracle Identity Manager Connector.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle Identity Manager Connector, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Identity Manager Connector accessible data as well as  unauthorized access to critical data or complete access to all Oracle Identity Manager Connector accessible data. CVSS 3.1 Base Score 7.2 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N).

### CVE-2026-60883

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:46.303 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: PeopleCode).  Supported versions that are affected are 8.61-8.63. Easily exploitable vulnerability allows high privileged attacker with network access via HTTP to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60873

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:46.070 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Data Mover).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows high privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in PeopleSoft Enterprise PeopleTools, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all PeopleSoft Enterprise PeopleTools accessible data as well as  unauthorized access to critical data or complete access to all PeopleSoft Enterprise PeopleTools accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.2 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:L).

### CVE-2026-54348

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T21:16:36.170 |

Froxlor is open source server administration software. Prior to 2.3.8, the Admins.add and Admins.update endpoints in lib/Froxlor/Api/Commands/Admins.php accept an attacker-controlled ipaddress array and store it as JSON in panel_admins.ip without enforcing numeric element types. When the poisoned account later calls IpsAndPorts.listing, lib/Froxlor/Api/Commands/IpsAndPorts.php decodes the array and concatenates its elements into a SQL IN clause without casting or parameterization; the same unsafe pattern is present in lib/Froxlor/Api/Commands/Domains.php. An authenticated administrator with change_serversettings permission can store a UNION-based payload and trigger it through the poisoned account to retrieve arbitrary database data, including administrator login names and bcrypt password hashes, with potential privilege escalation and broader database impact. This issue is fixed in version 2.3.8.

### CVE-2026-73367

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-829` |
| Published | 2026-08-18T15:17:05.123 |

Unauthenticated Remote File Inclusion in Easy Google Maps < 1.14.2 versions.

### CVE-2026-66620

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-18T15:16:57.153 |

Editor PHP Object Injection in OptionTree <= 2.7.3 versions.

### CVE-2026-32553

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T15:16:53.623 |

Unauthenticated Server Side Request Forgery (SSRF) in OttoKit <= 1.1.35 versions.

### CVE-2026-32473

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-18T15:16:52.953 |

Unauthenticated Server Side Request Forgery (SSRF) in PDF Smart Viewer for Elementor <= 1.0.4 versions.

### CVE-2026-76245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-19T14:17:56.957 |

stigmem (pip package stigmem-node) version 0.9.0a1 contains a timestamp-handling mismatch in federation peer-token validation that can cause valid peer tokens to be incorrectly treated as expired. This affects the availability and reliability of authenticated federation flows on nodes using federation peer authentication paths. The issue is fixed in 0.9.0a2, which uses the canonical millisecond-based validation path.

### CVE-2026-76223

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-19T14:17:48.740 |

ArcadeDB (com.arcadedb) versions 26.7.3 and earlier fail to enforce the UPDATE_SCHEMA permission check when a DEFINE FUNCTION statement targets an already-existing function library. A user with only database access can add or overwrite SQL or Cypher functions in an existing library and persist the change, enabling tampering with admin-defined function logic. The issue is fixed in 26.8.1. (JavaScript functions still trigger the UPDATE_SECURITY check and are not affected.)

### CVE-2026-76217

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-19T14:17:47.903 |

GitPython versions before 3.1.58 fail to validate options passed to git rm and git checkout commands in IndexFile.remove() and Head.checkout(). Attackers can supply --pathspec-from-file and --pathspec-file-nul parameters to read arbitrary files accessible to the process, with full file contents returned in GitCommandError.stderr.

### CVE-2026-76210

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-19T14:17:46.510 |

phpMyFAQ before 4.1.7 does not adequately sanitize HTML in FAQ answers before generating PDFs via TCPDF. An attacker with permission to create or edit FAQ content can embed an <img> tag whose src references a local file under the web root's content/ directory (e.g., content/core/config/database.php). When the PDF is generated, phpMyFAQ attempts to read the referenced file; because it is not a valid image the resulting error is converted into an uncaught exception whose stack trace discloses part of the file's contents to any user who triggers the PDF export. By default the disclosed portion is truncated (zend.exception_string_param_max_len), but a larger configured value can result in disclosure of entire files, including database credentials.

### CVE-2026-56088

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-19T14:17:34.517 |

Dell OpenManage Enterprise, versions prior to 4.7.0, contains an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Script injection.

### CVE-2026-73354

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T13:18:07.250 |

Unauthenticated Cross Site Scripting (XSS) in SimplyRETS Real Estate IDX <= 3.2.8 versions.

### CVE-2026-73184

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T13:18:06.863 |

Unauthenticated Cross Site Scripting (XSS) in Global Gallery <= 11.1.2 versions.

### CVE-2026-73182

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T13:18:06.607 |

Unauthenticated Cross Site Scripting (XSS) in BBQ Pro <= 3.9 versions.

### CVE-2026-66596

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T13:17:50.430 |

Unauthenticated Cross Site Scripting (XSS) in Newsletter <= 9.3.3 versions.

### CVE-2026-61986

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T13:17:49.090 |

Unauthenticated Cross Site Scripting (XSS) in Contest Gallery <= 30.0.5 versions.

### CVE-2026-76164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-19T09:17:36.830 |

AIL Framework contains a server-side request forgery (SSRF) vulnerability in its crawler submission functionality. A low-privileged authenticated user with access to the crawler interface can submit an arbitrary URL for crawling without adequate validation of the destination host.


The crawler can therefore be instructed to make direct HTTP(S) requests to addresses that should not be reachable by application users, including loopback addresses, RFC1918 private networks, link-local addresses, and cloud metadata services such as 169.254.169.254.


Manual crawler tasks bypass the existing domain blacklist because they are assigned a non-zero priority, and ordinary IP literals are classified as web targets and fetched directly rather than through Tor or another proxy. Consequently, an attacker can use the AIL server as a network pivot to access services available from the server's network context.


Responses generated by these requests, including captured HTML, screenshots, and HAR data, can subsequently be accessed through the crawler interface. This makes the SSRF non-blind and may allow an attacker to disclose sensitive internal application data, service information, or cloud instance metadata and credentials.


The patch introduces validation that resolves crawler destinations and rejects URLs resolving to non-global IP addresses, addressing localhost, private-network, and link-local targets.

### CVE-2026-16570

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-19T06:17:34.940 |

The NextScripts: Social Networks Auto-Poster WordPress plugin before 4.4.8 does not escape some of the query-string parameters it reflects back on one of its admin pages, allowing attackers to perform Reflected Cross-Site Scripting attacks against logged-in users such as administrators who are tricked into opening a crafted link.

### CVE-2026-15316

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-18T22:16:49.367 |

An improper input
validation vulnerability in the configuration service for processing encrypted
credential data has been identified in Tapo C200 v5.  An attacker can send oversized crypted
ciphertext values that may trigger exception handling failures, due to insufficient
validation, causing the affected device to crash or restart.





Successful
exploitation may temporarily disrupt HTTPS management and monitoring
functionality, resulting in a denial-of-service (DoS) condition until the
service recovers.

### CVE-2026-71012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:18:00.537 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-71003

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:59.473 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Experience Manager).   The supported version that is affected is 11.4.0. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Commerce Guided Search / Oracle Commerce Experience Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.757 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70967

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:55.307 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70936

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:51.663 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Financial Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70935

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:51.550 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70934

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:51.443 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70933

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:51.330 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Financial Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Financial Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70902

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:47.933 |

Vulnerability in the Oracle Hyperion Data Relationship Management product of Oracle Hyperion (component: Access and security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Data Relationship Management executes to compromise Oracle Hyperion Data Relationship Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Data Relationship Management accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Data Relationship Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-70867

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:42.990 |

Vulnerability in Oracle Application Testing Suite.   The supported version that is affected is 13.3.0.1. Easily exploitable vulnerability allows unauthenticated attacker with access to the physical communication segment attached to the hardware where the Oracle Application Testing Suite executes to compromise Oracle Application Testing Suite.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Application Testing Suite accessible data as well as  unauthorized update, insert or delete access to some of Oracle Application Testing Suite accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70858

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:41.987 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker and while the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change). Successful attacks of this vulnerability can result in  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data as well as  unauthorized read access to a subset of Oracle WebCenter Content accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Content. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L).

### CVE-2026-70845

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:40.297 |

Vulnerability in the Oracle Loans product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Loans.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Loans accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Loans. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-70844

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:40.153 |

Vulnerability in the Oracle Loans product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Loans.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Loans accessible data as well as  unauthorized update, insert or delete access to some of Oracle Loans accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:39.463 |

Vulnerability in the Oracle Financials for EMEA product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials for EMEA.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Financials for EMEA accessible data as well as  unauthorized update, insert or delete access to some of Oracle Financials for EMEA accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70837

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:39.197 |

Vulnerability in the Oracle Financials for Asia/Pacific product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials for Asia/Pacific.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Financials for Asia/Pacific accessible data as well as  unauthorized read access to a subset of Oracle Financials for Asia/Pacific accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N).

### CVE-2026-70833

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:38.660 |

Vulnerability in the Oracle Landed Cost Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Landed Cost Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Landed Cost Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Landed Cost Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:36.347 |

Vulnerability in the Oracle Financials for EMEA product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Financials for EMEA.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Financials for EMEA accessible data as well as  unauthorized update, insert or delete access to some of Oracle Financials for EMEA accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70809

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:35.377 |

Vulnerability in the Oracle Scripting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Scripting.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Scripting accessible data as well as  unauthorized access to critical data or complete access to all Oracle Scripting accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Scripting. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-70808

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:35.247 |

Vulnerability in the Oracle Scripting product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Scripting.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Scripting accessible data as well as  unauthorized update, insert or delete access to some of Oracle Scripting accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70806

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:34.960 |

Vulnerability in the Oracle E-Business Tax product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle E-Business Tax executes to compromise Oracle E-Business Tax.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle E-Business Tax accessible data and unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle E-Business Tax. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H).

### CVE-2026-70801

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:34.240 |

Vulnerability in the Oracle Flow Manufacturing product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Flow Manufacturing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Flow Manufacturing accessible data as well as  unauthorized update, insert or delete access to some of Oracle Flow Manufacturing accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70774

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:30.320 |

Vulnerability in the Oracle Warehouse Management product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Warehouse Management.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Warehouse Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Warehouse Management. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L).

### CVE-2026-70760

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:28.593 |

Vulnerability in the Oracle Order Management product of Oracle E-Business Suite (component: Product Diagnostic Tools).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Order Management.  While the vulnerability is in Oracle Order Management, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Order Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Order Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-70736

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:26.330 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Profitability and Cost Management accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-70733

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:25.977 |

Vulnerability in the Oracle Hyperion Profitability and Cost Management product of Oracle Hyperion (component: Deployment).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Profitability and Cost Management.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Profitability and Cost Management accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Profitability and Cost Management. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-70705

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:22.687 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Hyperion Calculation Manager executes to compromise Oracle Hyperion Calculation Manager.  While the vulnerability is in Oracle Hyperion Calculation Manager, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-70680

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:19.833 |

Vulnerability in the Oracle Applications DBA product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Applications DBA.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Applications DBA accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Applications DBA. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-62627

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:16.480 |

Vulnerability in the Oracle Reports Developer product of Oracle Fusion Middleware (component: Security and Authentication).   The supported version that is affected is 12.2.1.19.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Reports Developer.  While the vulnerability is in Oracle Reports Developer, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Reports Developer accessible data as well as  unauthorized update, insert or delete access to some of Oracle Reports Developer accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-62601

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:12.440 |

Vulnerability in the Oracle Sales product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Sales.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Sales accessible data as well as  unauthorized update, insert or delete access to some of Oracle Sales accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-62587

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:10.890 |

Vulnerability in the Siebel CRM Administration product of Oracle Siebel CRM (component: Data Archival).  Supported versions that are affected are 25.12-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel CRM Administration.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel CRM Administration accessible data as well as  unauthorized update, insert or delete access to some of Siebel CRM Administration accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-62537

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.247 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62536

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:06.130 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Installation and Configuration).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Hyperion Infrastructure Technology executes to compromise Oracle Hyperion Infrastructure Technology.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N).

### CVE-2026-62522

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:05.170 |

Vulnerability in the Oracle Hyperion Infrastructure Technology product of Oracle Hyperion (component: Common Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Infrastructure Technology.  While the vulnerability is in Oracle Hyperion Infrastructure Technology, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Infrastructure Technology accessible data as well as  unauthorized update, insert or delete access to some of Oracle Hyperion Infrastructure Technology accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-62458

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:02.337 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in unauthorized ability to cause a hang or frequently repeatable crash (complete DOS) of Oracle Work in Process as well as  unauthorized update, insert or delete access to some of Oracle Work in Process accessible data. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H).

### CVE-2026-61306

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:59.250 |

Vulnerability in the Oracle Complex Maintenance, Repair and Overhaul product of Oracle E-Business Suite (component: Production).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Complex Maintenance, Repair and Overhaul.  While the vulnerability is in Oracle Complex Maintenance, Repair and Overhaul, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Complex Maintenance, Repair and Overhaul accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Complex Maintenance, Repair and Overhaul. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L).

### CVE-2026-61295

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.523 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle WebCenter Content executes to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N).

### CVE-2026-61290

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.173 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle WebCenter Content. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-61288

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:58.050 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Content.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:L/A:N).

### CVE-2026-61259

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:56.860 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Hyperion Calculation Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-61124

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:54.297 |

Vulnerability in the Oracle WebCenter Portal product of Oracle Fusion Middleware (component: Runtime Tools).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Easily exploitable vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle WebCenter Portal.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle WebCenter Portal accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle WebCenter Portal. CVSS 3.1 Base Score 7.1 (Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L).

### CVE-2026-60949

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:48.667 |

Vulnerability in the Oracle WebCenter Content product of Oracle Fusion Middleware (component: Content Server).  Supported versions that are affected are 12.2.1.4.0 and  14.1.2.0.0. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle WebCenter Content.  While the vulnerability is in Oracle WebCenter Content, attacks may significantly impact additional products (scope change).  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle WebCenter Content accessible data as well as  unauthorized update, insert or delete access to some of Oracle WebCenter Content accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N).

### CVE-2026-60781

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:43.117 |

Vulnerability in the Oracle Payments product of Oracle E-Business Suite (component: File Transmission).  Supported versions that are affected are 12.2.3-12.2.15. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle Payments.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Oracle Payments accessible data as well as  unauthorized update, insert or delete access to some of Oracle Payments accessible data. CVSS 3.1 Base Score 7.1 (Confidentiality and Integrity impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N).

### CVE-2026-60752

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:41.803 |

Vulnerability in the Siebel Apps - Marketing product of Oracle Siebel CRM (component: Marketing).  Supported versions that are affected are 17.0-26.6. Easily exploitable vulnerability allows low privileged attacker with network access via HTTP to compromise Siebel Apps - Marketing.  Successful attacks of this vulnerability can result in  unauthorized access to critical data or complete access to all Siebel Apps - Marketing accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Siebel Apps - Marketing. CVSS 3.1 Base Score 7.1 (Confidentiality and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L).

### CVE-2026-60693

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:16:39.197 |

Vulnerability in the Oracle General Ledger product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with network access via HTTP to compromise Oracle General Ledger.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle General Ledger accessible data as well as  unauthorized access to critical data or complete access to all Oracle General Ledger accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle General Ledger. CVSS 3.1 Base Score 7.1 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L).

### CVE-2026-19671

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-08-18T20:17:13.660 |

Malcolm's upload-processing pipeline (scripts/safe-extract.py) enforces entry-count, nesting-depth, and total-uncompressed-byte limits when extracting container archives (zip/tar/rar/7z via libarchive), but those limits are not applied when the uploaded file is a single-stream compressed format (.gz, .bz2, .xz, .lzma, .lz) that isn't a .tar.*-style archive. Any authenticated user permitted to upload PCAP/log files can upload a small, highly compressible file (e.g. a gzip bomb) that decompresses to an effectively unbounded size on disk, exhausting the shared Docker volume used by OpenSearch, Logstash, Arkime, and Zeek, and disrupting the platform for all users.

### CVE-2026-24185

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T19:16:46.410 |

NVIDIA NVOS for network switches contains a vulnerability in the secure shell (SSH) server configuration component while PKA-only mode is enabled, where an administrator could inadvertently enable an alternative authentication path. If best practices for replacing the default password as recommended by NVIDIA are not followed, this alternative authentication path might lead to unauthorized access. A successful exploit of this vulnerability might lead to escalation of privileges.

### CVE-2026-17106

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-18T19:16:45.030 |

The tar extraction routines in moby/go-archive (Unpack, UnpackLayer, Untar/UntarUncompressed, and the ApplyLayer helpers) do not confine filesystem operations to the destination directory. The extractor decides where each archive entry lands using lexical string checks and then performs the filesystem operation on a path that is resolved by the OS, so links introduced by the archive can be followed out of the destination directory. An attacker who controls the contents of an archive can create or overwrite files at arbitrary paths writable by the extracting process.

### CVE-2026-74039

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770;CWE-1333` |
| Published | 2026-08-18T18:19:33.760 |

Wazuh 4.0.0 before 4.14.7 and 5.0.0-beta2 contain a denial of service vulnerability that allows authenticated attackers with allow_run_as enabled to exhaust CPU resources by submitting arbitrarily deeply nested JSON structures to the POST /security/user/authenticate/run_as endpoint. Attackers can repeatedly submit malformed auth_context bodies with unlimited nesting depth to cause the API framework to consume excessive CPU, denying service to all other API consumers.

### CVE-2026-73073

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-829` |
| Published | 2026-08-18T16:18:16.730 |

Vim is an open source, command line text editor. Prior to 9.2.0845, StructMembers() in runtime/autoload/ccomplete.vim constructs and executes a vimgrep command using an insufficiently escaped typeref: or typename: value from a tags file, allowing an unterminated collection followed by a command separator to execute arbitrary Ex and operating-system commands when a user invokes C omni-completion with CTRL-X CTRL-O on a member access whose type is resolved from that tags file. This issue is fixed in version 9.2.0845.

### CVE-2026-73396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-18T15:17:06.963 |

Subscriber Broken Authentication in MWB HubSpot for WooCommerce <= 1.6.7 versions.

### CVE-2026-73393

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:06.687 |

Unauthenticated Cross Site Scripting (XSS) in Subscribe2 <= 10.46 versions.

### CVE-2026-73382

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:06.280 |

Unauthenticated Cross Site Scripting (XSS) in Site Reviews <= 8.2.0 versions.

### CVE-2026-73378

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:05.713 |

Unauthenticated Cross Site Scripting (XSS) in Contact Form by Supsystic < 1.10.0 versions.

### CVE-2026-73375

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:05.270 |

Unauthenticated Cross Site Scripting (XSS) in Ultimate Maps by Supsystic < 1.5.0 versions.

### CVE-2026-73362

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:04.670 |

Unauthenticated Cross Site Scripting (XSS) in URL Shortify <= 2.5.0 versions.

### CVE-2026-73361

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:04.503 |

Unauthenticated Cross Site Scripting (XSS) in Recipe Card Blocks for Gutenberg & Elementor <= 3.4.18 versions.

### CVE-2026-73360

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:04.360 |

Unauthenticated Cross Site Scripting (XSS) in Chaty Pro <= 3.5.8 versions.

### CVE-2026-73358

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:04.083 |

Unauthenticated Cross Site Scripting (XSS) in Affiliates Manager <= 2.9.53 versions.

### CVE-2026-73351

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:03.503 |

Unauthenticated Cross Site Scripting (XSS) in WordPress Social Login and Register <= 7.8.1 versions.

### CVE-2026-73345

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-18T15:17:03.097 |

Customer SQL Injection in License Manager for WooCommerce <= 3.0.18 versions.

### CVE-2026-73342

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:02.790 |

Unauthenticated Cross Site Scripting (XSS) in WP Multilang <= 2.4.31 versions.

### CVE-2026-73338

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:02.340 |

Unauthenticated Cross Site Scripting (XSS) in Autopay <= 5.0.0 versions.

### CVE-2026-73190

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:02.203 |

Unauthenticated Cross Site Scripting (XSS) in WPDM – Premium Packages <= 7.0.5 versions.

### CVE-2026-68567

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:17:00.527 |

Unauthenticated Cross Site Scripting (XSS) in Convert Pro <= 1.0.1 versions.

### CVE-2026-66667

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:16:59.693 |

Unauthenticated Cross Site Scripting (XSS) in Templately <= 3.7.1 versions.

### CVE-2026-66633

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:16:57.823 |

Unauthenticated Cross Site Scripting (XSS) in Fluent Forms Pro Add On Pack < 6.2.12 versions.

### CVE-2026-66629

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:16:57.700 |

Unauthenticated Cross Site Scripting (XSS) in Kirki <= 6.2.3 versions.

### CVE-2026-66621

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:16:57.290 |

Unauthenticated Cross Site Scripting (XSS) in Ultimate Dashboard <= 3.11.2 versions.

### CVE-2026-48798

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-08-18T15:16:54.427 |

SSH.NET is a Secure Shell (SSH) library for .NET. In 2025.1.0 and earlier, ScpClient.Download(string directoryName, DirectoryInfo directoryInfo) trusts file and directory names returned by a remote SCP server and combines them with the requested local directory without containment validation, allowing a malicious, compromised, or man-in-the-middle server to use ../ sequences or absolute paths to create or overwrite files anywhere writable by the client process. This issue is fixed in version 2026.0.0.

### CVE-2026-32547

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-18T15:16:53.347 |

Unauthenticated Cross Site Scripting (XSS) in BP Better Messages <= 2.15.22 versions.

### CVE-2026-71098

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:10.030 |

Vulnerability in the Oracle Business Intelligence Enterprise Edition product of Oracle Analytics (component: Platform Security).   The supported version that is affected is 26.01.0.0.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Business Intelligence Enterprise Edition executes to compromise Oracle Business Intelligence Enterprise Edition.  Successful attacks of this vulnerability can result in takeover of Oracle Business Intelligence Enterprise Edition. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-71041

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:18:03.877 |

Vulnerability in the Oracle Agile PLM product of Oracle Supply Chain (component: Gantt Chart).   The supported version that is affected is 9.3.6. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile PLM executes to compromise Oracle Agile PLM.  Successful attacks of this vulnerability can result in takeover of Oracle Agile PLM. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70992

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:58.200 |

Vulnerability in the Oracle Commerce Guided Search / Oracle Commerce Experience Manager product of Oracle Commerce (component: Content Acquisition System).   The supported version that is affected is 11.4.0. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Commerce Guided Search / Oracle Commerce Experience Manager executes to compromise Oracle Commerce Guided Search / Oracle Commerce Experience Manager.  Successful attacks of this vulnerability can result in takeover of Oracle Commerce Guided Search / Oracle Commerce Experience Manager. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70914

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:49.223 |

Vulnerability in the Oracle Hyperion Financial Management product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with logon to the infrastructure where Oracle Hyperion Financial Management executes to compromise Oracle Hyperion Financial Management.  Successful attacks require human interaction from a person other than the attacker. Successful attacks of this vulnerability can result in takeover of Oracle Hyperion Financial Management. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H).

### CVE-2026-70697

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:21.790 |

Vulnerability in the Oracle Agile Engineering Data Management product of Oracle Supply Chain (component: Engineering Communication Interface).   The supported version that is affected is 6.2.1. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Agile Engineering Data Management executes to compromise Oracle Agile Engineering Data Management.  Successful attacks of this vulnerability can result in takeover of Oracle Agile Engineering Data Management. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-70676

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-18T21:17:19.383 |

Vulnerability in the Oracle Hyperion Calculation Manager product of Oracle Hyperion (component: Security).   The supported version that is affected is 11.2.25.0.000. Difficult to exploit vulnerability allows unauthenticated attacker with network access via HTTP to compromise Oracle Hyperion Calculation Manager.  Successful attacks of this vulnerability can result in  unauthorized creation, deletion or modification access to critical data or all Oracle Hyperion Calculation Manager accessible data as well as  unauthorized read access to a subset of Oracle Hyperion Calculation Manager accessible data and unauthorized ability to cause a partial denial of service (partial DOS) of Oracle Hyperion Calculation Manager. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L).

### CVE-2026-62449

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:17:01.607 |

Vulnerability in the Oracle Work in Process product of Oracle E-Business Suite (component: Internal Operations).  Supported versions that are affected are 12.2.3-12.2.15. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where Oracle Work in Process executes to compromise Oracle Work in Process.  Successful attacks of this vulnerability can result in takeover of Oracle Work in Process. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-60902

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-18T21:16:46.760 |

Vulnerability in the PeopleSoft Enterprise PeopleTools product of Oracle PeopleSoft (component: Tuxedo).  Supported versions that are affected are 8.61-8.63. Difficult to exploit vulnerability allows low privileged attacker with logon to the infrastructure where PeopleSoft Enterprise PeopleTools executes to compromise PeopleSoft Enterprise PeopleTools.  Successful attacks of this vulnerability can result in takeover of PeopleSoft Enterprise PeopleTools. CVSS 3.1 Base Score 7.0 (Confidentiality, Integrity and Availability impacts).  CVSS Vector: (CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H).

### CVE-2026-52817

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-18T21:16:34.820 |

Linuxfabrik Monitoring Plugins provides monitoring plugins for Icinga, Nagios, and related systems. Prior to version 5.1.0, the shipped assets/sudoers/Debian.sudoers policy allowed the nagios or icinga account to execute /usr/bin/apt-get as root without restricting its arguments. An attacker who already controls that monitoring account can supply the APT::Update::Pre-Invoke option to execute an arbitrary command while apt-get runs with root privileges, resulting in a root shell and complete compromise of the host. The vulnerable rule supports the check-plugins/deb-updates/deb-updates plugin, but it authorized arbitrary apt-get argument sequences rather than only the required apt-get update --quiet 2 command. This issue is fixed in version 5.1.0.

### CVE-2026-74044

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T18:19:33.907 |

Wazuh 4.0.0 before 4.14.6 contains a path traversal vulnerability that allows authenticated cluster peers to delete arbitrary directory contents by supplying a traversal-shaped node name in the cluster hello payload without validation. Attackers holding a valid cluster Fernet key can craft a malicious node name and disconnect, triggering the master's peer cleanup routine to remove the contents of arbitrary directories within the Wazuh installation path writable by the wazuh user.

### CVE-2026-74038

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-18T18:19:33.610 |

Wazuh 4.0.0 before 4.14.6 contains a path traversal vulnerability that allows unauthenticated remote attackers to cause denial of service by enrolling an agent with a dot-sequence name such as ".." through the enrollment port. Attackers exploit insufficient validation in OS_IsValidName() and unsafe path concatenation in delete_diff() to resolve the traversal to the parent queue directory, causing its subdirectories to be removed and stopping all Wazuh services requiring manual recovery.
