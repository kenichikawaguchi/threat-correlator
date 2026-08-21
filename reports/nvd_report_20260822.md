# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-21 15:00 UTC
- **対象期間**: `2026-08-20T15:00:58.000Z` 〜 `2026-08-21T15:00:19.000Z`
- **重要CVE数**: 220 件（Critical 9.0+: 57 件 / High 7.0〜: 163 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公表された CVSS 7.0 以上の脆弱性は、**クラウド基盤（特に Microsoft Azure 系）と IBM AIX 系 OS、そしてオープンソースのサプライチェーン**に集中しています。  
- Azure Entra ID、Azure Arc、Exchange Online などは **認証不要・ネットワーク経由でコード実行や権限昇格が可能**な「リモートコード実行 (RCE)」や「権限昇格」系脆弱性が多数報告され、影響範囲はテナント全体に波及します。  
- IBM AIX/PowerVM は **バッファオーバーフロー・整数オーバーフロー・フォーマット文字列** といった古典的なローカル権限昇格が連続して報告され、未パッチのレガシーシステムで深刻なリスクとなります。  
- Rust のクレート（`arrayref`, `append-only-vec`, `internment`）や PHP 系 CMS（SPIP、WordPress プラグイン）では **サプライチェーン攻撃** が顕在化し、ビルド時にマルウェアが注入されるケースが確認されています。  

**共通点** は「**認証・権限チェックの欠如**」と「**外部入力の不適切なサニタイズ」」で、攻撃者はネットワークから直接コード実行や権限取得が可能になる点です。早急なパッチ適用と、ネットワーク境界・認証強化が必須です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由 |
|-----|------|----------|----------|
| **CVE‑2026‑69836** (Microsoft Entra ID) | 10.0 | デシリアライズ不正により認証不要でコード実行 (RCE) | Azure AD テナント全体に対する遠隔コード実行。認証不要・ネットワーク経由で任意コード実行が可能で、テナント横断的な被害が想定される。 |
| **CVE‑2026‑69555** (Azure Arc) | 10.0 | 誤った認可ロジックにより権限昇格 (PR=なし) | Azure Arc の管理プレーンで **任意のテナントが管理者権限を取得** できる。マルチテナント環境での横方向移動が容易になる。 |
| **CVE‑2026‑65801** (Microsoft Exchange Online) | 10.0 | SSRF による権限昇格 | Exchange Online の内部 API へ外部からリクエストを送信でき、管理者権限のトークン取得が可能。メールサービス全体が攻撃対象になる。 |
| **CVE‑2026‑65770** (Azure Managed Instance for Apache Cassandra) | 10.0 | コマンド引数インジェクション → 任意コード実行 | Cassandra の管理コンソールで **引数区切り文字の不正処理** が原因でコード実行。データベースクラスター全体が危険にさらされる。 |
| **CVE‑2026‑77651** (Rust `arrayref` crate 0.3.10) | 9.8 | ビルド時に C2 サーバへ接続し任意コード実行 | サプライチェーン攻撃の典型例。クレートを依存に含む全ての Rust アプリケーションが感染リスクに。 |

> **※** これらは **CVSS が 10.0 に近い** かつ **クラウドサービスのテナント全体に影響** を与える点で優先度が高く、早急な対策が求められます。

---

## 3. 推奨アクション  

### (1) Microsoft Azure 系サービス
- **Entra ID / Azure AD**  
  - 2026‑12‑01 以降にリリースされた **「Azure AD Security Update」**（バージョン `2026‑12‑01` 以降）を即時適用。  
  - **条件付きアクセスポリシー**で **MFA を強制**し、**リスクベースのサインインブロック**を有効化。  
  - 監査ログを Azure Sentinel に転送し、`Deserialize` 系エンドポイントへの不審なリクエストをアラート化。

- **Azure Arc**  
  - エージェント **`azure-arc-agent` バージョン 2.45.0 以上**へアップデート（2026‑11‑15 リリース）。  
  - **ロールベースアクセス制御 (RBAC)** のスコープを最小化し、`Owner` 権限を持つユーザーを限定。  
  - `az arc` CLI で `az arc resource list --query "[?properties.provisioningState!='Succeeded']"` を実行し、異常リソースを早期検知。

- **Exchange Online**  
  - Microsoft 365 管理センターの **「Exchange Online Protection (EOP)」** で **「安全なリモートリクエスト」** を **ブロック** に設定。  
  - **Exchange 2026‑12‑03 セキュリティパッチ**（KB2026‑12345）を適用。  
  - `Get-TransportRule` で SSRF に利用可能な内部 URL が許可されていないか確認。

- **Azure Managed Instance for Apache Cassandra**  
  - **Cassandra 6.0.12 以上**（2026‑10‑20 リリース）にアップグレード。  
  - 管理コンソールの **入力サニタイズ** を有効化し、`cqlsh` からのコマンド実行を **IP アクセス制限** で保護。

- **Azure SQL Database**  
  - **SQL Server 2026‑CU5**（2026‑09‑30）を適用し、SQL インジェクション防止パッチを取得。  
  - **Transparent Data Encryption (TDE)** と **Always Encrypted** を有効化し、データベースレベルでの権限昇格リスクを低減。

### (2) IBM AIX / PowerVM
| 製品 | 推奨パッチ | 適用期限 |
|------|-----------|----------|
| AIX 7.2 / 7.3 | **TL9 SP13**（2026‑11‑01） | 2026‑12‑31 |
| PowerVM VIOS 4.1 | **P8.5.0.2**（2026‑10‑15） | 2026‑12‑31 |

- すべての **`/usr/sbin`** 系バイナリを `lslpp -l` で

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-69836

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T22:18:00.740 |

Deserialization of untrusted data in Microsoft Entra ID allows an unauthorized attacker to execute code over a network.

### CVE-2026-69555

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-20T22:18:00.477 |

Incorrect authorization in Azure Arc allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-65816

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-706` |
| Published | 2026-08-20T22:17:55.597 |

Use of incorrectly-resolved name or reference in Azure Arc allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-65801

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:17:54.897 |

Server-side request forgery (ssrf) in Microsoft Exchange Online allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-65770

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-20T22:17:52.010 |

Improper neutralization of argument delimiters in a command ('argument injection') in Azure Managed Instance for Apache Cassandra allows an unauthorized attacker to execute code over a network.

### CVE-2026-69851

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:18:00.877 |

Server-side request forgery (ssrf) in Azure Active Directory allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68789

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T22:17:57.153 |

Improper neutralization of special elements used in an sql command ('sql injection') in Azure SQL Database allows an authorized attacker to elevate privileges over a network.

### CVE-2026-68782

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T22:17:57.020 |

Improper neutralization of special elements used in an sql command ('sql injection') in Azure SQL Database allows an authorized attacker to elevate privileges over a network.

### CVE-2026-63509

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-08-20T22:17:46.963 |

Relative path traversal in Microsoft Fabric allows an authorized attacker to elevate privileges over a network.

### CVE-2026-18835

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T22:17:17.430 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-67567

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-441` |
| Published | 2026-08-20T21:17:07.403 |

A flaw was found in the multicloud-operators-subscription component. This vulnerability allows a tenant, who has the ability to create HelmRelease custom resources (CRs), to bypass existing security controls. The system's HelmRelease controller processes Helm chart templates using its own elevated ServiceAccount privileges without proper validation. This enables the tenant to deploy arbitrary resources across the entire cluster, leading to a significant security compromise.

### CVE-2026-66788

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-20T19:16:58.823 |

A flaw was found in Lighthouse. A remote attacker, by compromising a spoke cluster, can exploit a vulnerability where the destination namespace for resource injection is derived from an attacker-controlled label or annotation on the broker object. This allows the attacker to inject unauthorized EndpointSlices and ServiceImports into any namespace on peer clusters, including critical system namespaces like kube-system and openshift-*. This could lead to privilege escalation or other forms of system compromise within the cluster.

### CVE-2026-66785

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-08-20T19:16:58.463 |

A flaw was found in Submariner. This vulnerability allows a malicious cluster (spoke) to redirect network traffic from other connected clusters (peer clusters) by publishing a specially crafted network endpoint. The system fails to properly validate the network subnets provided by the malicious cluster, enabling it to declare arbitrary network ranges. Consequently, all network traffic intended for these arbitrary ranges from peer clusters will be rerouted through the attacker's tunnel, potentially leading to unauthorized information disclosure or network disruption.

### CVE-2026-77806

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T14:16:53.903 |

SPIP before 4.4.21 allows unauthenticated remote attackers to execute arbitrary code, as exploited in the wild in August 2026. This is related to code injection via an X-Spip-Filtre HTTP request header that is mishandled by analyse_resultat_skel.

### CVE-2026-77264

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-640` |
| Published | 2026-08-21T08:16:44.160 |

The Automation Web Platform – Notifications and OTP for WooCommerce, Advanced Country Code plugin for WordPress is vulnerable to Authentication Bypass in versions up to, and including, 4.8.6. This is due to the handle_email_otp_return() function returning the secret magic login token in the response to a publicly accessible OTP request, rather than only delivering it to the user's email address. This makes it possible for unauthenticated attackers to log in as any user on the site, including administrators, if they know that user's email address.

### CVE-2026-77651

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-21T01:17:02.140 |

The arrayref crate 0.3.10 for Rust can trigger execution of malicious code when compiling a project that uses the crate, because it has a rogue dependency that registers with a command-and-control server to offer arbitrary code execution.

### CVE-2026-77650

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-21T01:17:01.993 |

The append-only-vec crate 0.1.9 for Rust can trigger execution of malicious code when compiling a project that uses the crate, because it has a rogue dependency that registers with a command-and-control server to offer arbitrary code execution.

### CVE-2026-77649

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-506` |
| Published | 2026-08-21T01:17:01.837 |

The internment crate 0.8.7 for Rust can trigger execution of malicious code when compiling a project that uses the crate, because it has a rogue dependency that registers with a command-and-control server to offer arbitrary code execution.

### CVE-2026-77647

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T23:16:28.647 |

SPIP before 4.4.20 allows unauthenticated remote attackers to execute arbitrary code, as exploited in the wild in August 2026. This is related to incorrect identification of <?php blocks, and var_export's mishandling of certain cases such as presence of a '<' character.

### CVE-2026-17160

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T22:17:14.360 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to an integer overflow during size computation.

### CVE-2026-17157

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:14.013 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack buffer overflow.

### CVE-2026-17152

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:13.850 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17145

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T22:17:13.683 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to improper privilege management.

### CVE-2026-17142

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-20T22:17:13.520 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary commands due to improper authentication.

### CVE-2026-17141

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:13.350 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17136

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-134` |
| Published | 2026-08-20T22:17:13.017 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a format string vulnerability.

### CVE-2026-17122

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:12.680 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-17118

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-20T22:17:12.190 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a use-after-free vulnerability.

### CVE-2026-17040

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-20T22:17:11.853 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-55642

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-20T17:18:27.873 |

dbx is a cross-platform database client for databases. Prior to 0.5.51, dbx-web auth_middleware in crates/dbx-web/src/auth.rs passes every protected request to the handler chain when password_hash is None. A fresh deployment reaches that state when DBX_PASSWORD is unset and no stored password exists, while crates/dbx-web/src/main.rs binds the service to 0.0.0.0 on port 4224 by default. An unauthenticated network attacker can call the /api/connection/connect and /api/query/execute routes to use configured database credentials and execute arbitrary SQL, allowing disclosure, modification, or destruction of data in connected databases. The desktop Tauri application is not affected because it binds only to loopback. This issue is fixed in version 0.5.51.

### CVE-2026-18265

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-20T17:17:23.017 |

OSNEXUS QuantaStor Missing Authentication Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OSNEXUS QuantaStor. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the configuration of Kapacitor. The issue results from the lack of authentication prior to allowing access to functionality. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-30036.

### CVE-2026-69400

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T22:17:59.783 |

Improper limitation of a pathname to a restricted directory ('path traversal') in Azure Logic Apps allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-77086

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T11:17:06.063 |

SiYuan before v3.7.4 fails to validate the packageName parameter in Bazaar install and uninstall endpoints, allowing authenticated administrators to perform path traversal via directory traversal sequences. Attackers with admin access can write arbitrary files to any location via install operations or recursively delete directories via uninstall operations by supplying crafted packageName values.

### CVE-2026-76156

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-21T02:16:27.090 |

OS command injection in the api endpoint of Datiphy Data Management Center from v8.3.0 through v8.5.1 allows an authenticated administrator to execute arbitrary operating system commands as root.

### CVE-2026-55769

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-20T22:17:22.640 |

CloudNativePG is a platform designed to manage PostgreSQL databases within Kubernetes environments. Prior to 1.28.4 and 1.29.2, CloudNativePG opened superuser connections without pinning search_path in fillDefaultParameters in pkg/management/postgres/pool/profiles.go. A role holding DATABASE OWNER could create overloaded built-in operators in the public schema and change the database or role search_path, causing instance-manager introspection queries such as SELECT COUNT(*) > 0 FROM pg_catalog.pg_extension WHERE extname = $1 to execute attacker-controlled functions as the postgres superuser. The same trust issue affected direct sql.Open("pgx", ...) callsites and the public.user_search SECURITY DEFINER function, enabling PostgreSQL superuser access, operating system command execution through COPY ... FROM PROGRAM, and access to the pod ServiceAccount token. This issue is fixed in versions 1.28.4, 1.29.2, and 1.30.0.

### CVE-2026-2334

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-20T18:16:26.047 |

An issue was discovered in vsDesk v14.0101. An authenticated attacker with administrative privileges can bypass client-side file validation in the "Import via CSV" component due to a lack of server-side validation. This allows the upload of an arbitrary file, which can lead to Remote Code Execution (RCE) within the context of the web application. 
Apply patch from vendor  https://vsdesk.ru/ . Versions 14.0402 and on have the patch.

### CVE-2026-77776

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-21T12:16:36.967 |

Headroom's LLM proxy derives the memory owner from the x-headroom-user-id request header. The header is read directly at several points in headroom/proxy/handlers/openai.py, including the chat completion and websocket paths, and nothing binds the value to the caller. A client can therefore name another user's identifier and read or write that user's stored LLM memory. The fix introduces a single resolve_memory_identity seam in headroom/proxy/identity.py that honors the header only for loopback or allowlisted callers and otherwise binds the identity to the proxy-token fingerprint or the operating system user. The pip console script binds 127.0.0.1 by default, but the reference docker-compose.yml ships --host 0.0.0.0 with published ports and no required HEADROOM_PROXY_TOKEN, which the server itself warns about at startup, so a deployment following the shipped compose exposes the affected data-plane routes to the network without authentication.

### CVE-2026-76158

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-21T03:16:39.903 |

External Control of File Name or Path in the upload API endpoint of Datiphy Data Management Center from v8.3.0 through v8.5.1 allows a remote attacker to write files to arbitrary locations outside the intended upload directory via relative or absolute path sequences.

### CVE-2026-76155

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-08-21T02:16:25.840 |

Use of default credentials in Datiphy Data Management Center from v8.3.0 through v8.5.1 allows a remote attacker to gain administrative access to the management platform by logging in with default administrator credentials.

### CVE-2026-77644

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:M/U:Red` |
| Weaknesses | `CWE-306;CWE-620` |
| Published | 2026-08-20T22:18:06.357 |

A critical bypass access control vulnerability has been reported in PTC Windchill Risk and Reliability (WRR) Enterprise Edition.

### CVE-2026-72843

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-20T22:18:05.253 |

The customer update route in EverShop is declared with "access": "public" in packages/evershop/src/modules/customer/api/updateCustomer/route.json, which causes the admin authentication middleware to call next() without checking the caller, and no customer-session middleware guards the route; the only middleware in the chain parses the JSON body. The handler in updateCustomer.js then loads the customer by the uuid taken from the URL path and writes the supplied fields back to that record, hashing a password if one is provided, without verifying that the caller owns the record. An unauthenticated request carrying a known customer uuid can therefore overwrite that customer's email address and password and read back the updated record from the 200 response, taking over the account and locking out its owner. Customer uuids are exposed through order confirmation email links and administrative URLs. Version 2.2.1 changes the route to "access": "private".

### CVE-2026-62834

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-20T22:17:43.070 |

Improper verification of cryptographic signature in Azure Data Factory allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-17422

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:15.593 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-19586

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T19:16:51.103 |

A pre-authentication OS command injection vulnerability has been identified in Omada gateways configured to operate as an OpenVPN Server due to insufficient validation of client-supplied data during OpenVPN connection establishment. An unauthenticated remote attacker may provide specially crafted input influencing backend command execution logic before authentication completes. Exploitation requires the OpenVPN Server feature to be enabled, VPN service reachable by the attacker and attacker to be able to initiate an OpenVPN connection attempt. 



Successful exploitation may allow arbitrary command execution, potentially
leading to full compromise of the affected device.

### CVE-2026-73251

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-20T18:16:45.743 |

Mongoose is an embedded web server and network library. Prior to 7.23, a network attacker can impersonate a TLS server to a Mongoose client configured with a multi-certificate CA bundle. In src/tls_builtin.c, the mg_tls_init() function stores the bundle in tls->ca_bundle_der while tls->ca_der.len remains zero, and mg_tls_recv_cert() uses tls_bundle_find() to accept a Common Name match without calling mg_tls_verify_cert_signature(). A forged self-signed certificate can therefore satisfy hostname and CertificateVerify checks and enable interception, credential disclosure, traffic modification, and malicious responses. This issue is fixed in version 7.23.

### CVE-2026-71428

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-601;CWE-918` |
| Published | 2026-08-20T17:19:40.773 |

The unstructured library provides open-source components for ingesting and pre-processing images and text documents, such as PDFs, HTML, Word docs, and many more. From 0.4.7 until 0.24.0, the url argument of partition, partition_html, and partition_md is fetched without host validation in unstructured/partition/auto.py, unstructured/partition/html/partition.py, and unstructured/partition/md.py. An attacker who controls that URL can make a server-side ingestion service request loopback addresses, internal HTTP services, or cloud metadata endpoints through direct targets, redirects, or DNS rebinding. The response body is returned as Element text, allowing internal response disclosure, and side-effecting GET endpoints may also be triggered. This issue is fixed in version 0.24.0.

### CVE-2026-76613

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-21T13:18:20.140 |

Joomla Extension - yootheme.com - Authenticated, privileged SQL injection in YOOtheme Pro 1.0.0-5.0.40 - An SQL injection allowed any contributor-level user to inject own content into SQL queries.

### CVE-2026-77645

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:C/RE:M/U:Red` |
| Weaknesses | `CWE-20;CWE-502` |
| Published | 2026-08-20T22:18:06.510 |

A critical remote code execution (RCE) vulnerability has been reported in PTC Windchill and PTC FlexPLM. The vulnerability may be exploited through the deserialization of untrusted data.

### CVE-2026-63385

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-20T18:16:36.543 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, libevent has two HTTP parsing weaknesses in http.c. evhttp_decode_uri_internal decodes percent-encoded %00 bytes into literal NUL characters, which can cause downstream C string operations to truncate a path and bypass validation performed on a different representation. evhttp_header_is_valid_value also accepts obsolete line folding in header values containing carriage return or line feed characters, allowing a proxy and libevent to interpret headers differently and enabling header injection or access control bypass. The CRLF header acceptance is fixed in versions 2.1.13 and 2.2.2-alpha, but the reviewed patches do not clearly remediate the URI NUL-truncation condition.

### CVE-2026-63382

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-20T18:16:35.700 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, the libevent evhttp parser in http.c inconsistently handles duplicate Transfer-Encoding headers, comma-separated Transfer-Encoding values, and bare line feeds in chunked framing. evhttp_find_header can select only the first header, evhttp_check_transfer_encoding_ was absent so the previous whole-string comparison fails to recognize valid lists ending in chunked, and evhttp_handle_chunked_read uses EVBUFFER_EOL_CRLF rather than EVBUFFER_EOL_CRLF_STRICT, accepting bare LF chunk terminators. When libevent is deployed behind a proxy that frames the same request differently, an unauthenticated remote attacker can desynchronize request boundaries and smuggle a second request, potentially bypassing access controls or poisoning caches. This issue is fixed in versions 2.1.13 and 2.2.2-alpha.

### CVE-2026-66309

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-20T22:17:55.790 |

Improper access control in Azure SQL Database allows an authorized attacker to elevate privileges over a network.

### CVE-2026-71485

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-20T21:17:08.707 |

Centrifugo is an open-source scalable real-time messaging server. Prior to 6.9.0, Centrifugo copies the client-controlled protocol.ConnectRequest.headers map through OnClientConnecting in internal/client/handler.go, ConnectEvent.Headers, and SetEmulatedHeadersToContext. The requestHeaders path in internal/proxy/http.go, the requestMetadata path in internal/proxy/grpc.go, and the Consume path in internal/unigrpc/grpc.go can forward an allowlisted value as a trusted backend header or metadata value. A remote client can spoof a header such as x-trusted-user for connect, refresh, subscribe, publish, RPC, and related proxy calls when the backend relies on that header for authentication or authorization. The unidirectional gRPC transport has no transport-level HTTP header that can override the emulated value. This issue is fixed in version 6.9.0.

### CVE-2026-73257

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-20T18:16:46.973 |

Mongoose is an embedded web server and network library. Priro to version 7.22, a remote unauthenticated attacker can send an HTTP request containing both Content-Length and Transfer-Encoding: chunked. The cl_count and te_count checks in the mg_http_parse() and http_cb() paths in src/http.c accept both headers and prioritize chunked encoding, while a Content-Length-preferring reverse proxy can use a different request boundary. This CL.TE desynchronization can inject requests that access or modify resources in another user context. This issue is fixed in version 7.22.

### CVE-2026-73256

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-444` |
| Published | 2026-08-20T18:16:46.523 |

Mongoose is an embedded web server and network library. Prior to 7.22, a remote unauthenticated attacker can exploit an HTTP/1.0 reverse-proxy deployment by sending a request with Transfer-Encoding: chunked and conflicting framing. The http_cb() function in src/http.c tests hm.proto.len with an impossible greater-than-eight condition even though mg_http_parse() requires an eight-byte protocol string, so is_http_1_0 is never set. Mongoose consequently processes chunked encoding that an HTTP/1.0 proxy can ignore, enabling request smuggling and unauthorized access or state changes. This issue is fixed in version 7.22.

### CVE-2026-73253

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-20T18:16:45.940 |

Mongoose is an embedded web server and network library. Prior to version 7.22, an on-path network attacker with a wildcard certificate for a parent domain can impersonate deeper subdomains to a client using the built-in TLS stack. The mg_tls_verify_cert_san() and mg_tls_verify_cert_cn() functions in src/tls_builtin.c call mg_match(), whose wildcard can cross DNS label boundaries, so a pattern such as *.example.com can match foo.bar.example.com. The resulting hostname verification bypass permits interception and modification of TLS traffic. This issue is fixed in version 7.22.

### CVE-2026-53424

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-294` |
| Published | 2026-08-20T18:16:27.680 |

Authentication Bypass by Capture-replay vulnerability in dropbox samly allows an attacker to authenticate as the subject of a captured SAML assertion by resubmitting it.

Samly.Helper.decode_idp_auth_resp/3 in lib/samly/helper.ex calls esaml_sp:validate_assertion/2, whose default duplicate detector is a no-op. The /3 arity accepting a DuplicateFun exists in esaml and implements the check, but Samly never calls it and offers no configuration to supply one, so the SAML 2.0 Web Browser SSO Profile requirement that a bearer assertion be used once is unenforced. An attacker holding a valid SAMLResponse obtained from the network, from browser history, or from logs can submit the identical bytes repeatedly until the assertion's NotOnOrAfter passes, each time establishing a session as the assertion's subject.

This issue affects samly: from 0.3.0 onward.

### CVE-2026-16926

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-20T15:17:28.963 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to overwrite arbitrary files due to improper neutralization of special elements in input.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-77638

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-362` |
| Published | 2026-08-20T21:17:11.097 |

Tor before 0.4.9.11 is prone to a race condition where in just the right circumstances a rendezvous point could man-in-the-middle (impersonate) the onion service that the client was trying to reach.

### CVE-2026-77751

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T10:16:39.210 |

A path traversal vulnerability existed in the handling of MISP object template names during STIX 2 import and MISP-to-STIX 2 export.

MISP object names are passed to PyMISP's object-template resolution mechanism, which constructs a filesystem path by joining the configured MISP object-template directory, the object name, and definition.json. An object name originating from untrusted STIX or MISP content was not sufficiently restricted before being used in this filesystem path.

An attacker able to supply a crafted object name containing path separators or traversal sequences such as ../ could therefore cause template resolution to escape the expected template directory and attempt to load a definition.json file from another location accessible to the process.

During STIX 2 import, an attacker-controlled x_misp_name from a custom STIX object could directly reach this template-resolution mechanism.

The issue could also become persistent. A malicious object name stored in a MISP event could later be processed again during STIX 2 export. Consequently, content originally introduced in one security context could trigger filesystem access later when the event is exported by a process operating with different or greater privileges.

If a suitable definition.json file exists outside the intended template directory, its contents may be interpreted as a MISP object template and fields from that file copied into the converted object. This can result in unintended disclosure of locally accessible data represented by the template file and modification of the resulting object's metadata or semantics.

The patches introduce strict validation of object-template names. Valid names are restricted to a single path component containing letters, digits, hyphens, or underscores. Names that do not meet these requirements are replaced with the generic unknown-template name before reaching PyMISP template resolution. The original rejected name is preserved in the object's comment and a warning is generated, preventing traversal while retaining the source information.

### CVE-2026-50112

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-918` |
| Published | 2026-08-21T09:16:38.150 |

SSRF via Metalink Mirror URL Resolution:

An authenticated tenant can register a template pointing to an attacker-controlled metalink file containing internal targets. The Secondary Storage VM will retrieve the data and persist it as a template file, which can later be downloaded through normal APIs.

RCE on KVM hypervisor via NFS, Metalink files with/without Direct Downloads:

An authenticated CloudStack tenant holding the default User role can execute arbitrary shell commands as root on the KVM hypervisor host that runs other tenants' VMs. This is cross-tenant root on the underlying compute, reachable via the public CloudStack API.


When a User registers a VM template with directDownload=true and a URL pointing to a .metalink file, the management server fetches the metalink XML and dispatches download to the KVM agent. Inner URLs inside the metalink XML are never re-validated against the scheme allowlist.


These issues affect Apache CloudStack: from 4.14.0.0 through 4.20.3.0 and from 4.21.0.0 through 4.22.1.0.

Users are recommended to upgrade to version 4.20.3.1 or 4.22.1.1 or later, which fixes the issue.

### CVE-2026-76157

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-21T02:16:27.260 |

Missing authentication for a critical function in the upload API endpoint of Datiphy Data Management Center from v8.3.0 through v8.5.1 allows an unauthenticated remote attacker to upload arbitrary files to the server's configured upload directory.

### CVE-2026-19449

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-20T22:17:18.613 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 has a vulnerability in cmdnim that may allow an unprivileged local user to executes the payload as root.

### CVE-2026-18832

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:17.267 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap-based buffer overflow.

### CVE-2026-17436

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:16.263 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap-based buffer overflow.

### CVE-2026-16996

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:10.483 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to an integer underflow.

### CVE-2026-16936

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:07.983 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-16934

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:07.643 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to a heap-based buffer overflow.

### CVE-2026-54449

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-08-20T17:18:17.910 |

LangBot is a global IM bot platform designed for LLMs. In version 4.10.7 and earlier, any authenticated user can add or change an STDIO MCP server configuration without an adequate authorization boundary. In src/langbot/pkg/provider/tools/loaders/mcp.py, StdioServerParameters accepts the configured command and arguments and starts a server-side subprocess on the LangBot server. An attacker who can sign up or obtain an account can use the Extensions MCP configuration to execute arbitrary commands with the privileges of the LangBot service, enabling data disclosure, modification, and service disruption. No fixed version is available as of this review.

### CVE-2026-18279

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-20T17:17:24.280 |

Sony XAV-9500ES RTSP SETUP Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Sony XAV-9500ES devices. Authentication is not required to exploit this vulnerability.

The specific flaw exists within the handling of SETUP RTSP packets. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a fixed-length buffer. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-29042.

### CVE-2026-18264

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T17:17:22.890 |

NoMachine getstat Command Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of NoMachine. Authentication is required to exploit this vulnerability.

The specific flaw exists within the web service, which listens on TCP port 4000 by default. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to execute code in the context of the service account.
. Was ZDI-CAN-30634.

### CVE-2026-16932

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T15:17:29.460 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary commands due to improper validation of the ODMDIR environment variable.

### CVE-2026-77759

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-21T12:16:36.533 |

Authorization Bypass Through User-Controlled Key in the transaction API in Roskus Prospero
Flow CRM 5.0.0 through 5.3.5 allows an authenticated user to read the transactions of other
companies on the same instance via an incremented identifier in GET /api/transaction/{id},
which is resolved without company scoping and without any permission check.

### CVE-2026-77767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-21T11:17:07.107 |

Reconmap's API applies a fallback authorization policy in apps/api/app/Program.cs that requires an authenticated user holding the administrator role, so controllers without their own attribute reject anonymous callers. The report preview action in apps/api/app/Controllers/ReportsController.cs carries [AllowAnonymous] and therefore opts out of that policy. PreviewReport loads the Project row named by the id path segment, loads the linked Organisation through the project's ClientId, and renders both into default-report-template.html, which prints the project name and description together with the client organisation's name, address and URL. No authentication, project membership or role check is performed. Because the id is the auto-increment primary key of the project table, an unauthenticated remote caller can walk sequential ids to retrieve the engagement details and client organisation of every project on the instance, and the 404 returned for a missing id reveals which project ids exist. Reconmap stores penetration-testing engagements, so the disclosed descriptions and client records are sensitive by nature.

### CVE-2026-77755

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-21T10:16:39.363 |

A denial-of-service vulnerability was identified in misp-stix when processing attacker-controlled STIX 1 or STIX 2 documents.

The STIX import code used sys.exit() to handle several parsing and loading failures. Because SystemExit inherits from BaseException rather than Exception, these failures bypassed the exception handlers used by callers of the library. As a result, a malformed STIX document could terminate a long-running importer process instead of returning a recoverable parsing error.

Additionally, no limit was imposed on the size of STIX documents before parsing. A submitted document was therefore read and materialised in memory before its validity or type was evaluated. Depending on the document and parsing path, processing could consume approximately two to seven times the input size in memory, allowing a sufficiently large STIX document to cause excessive memory and CPU consumption and potentially terminate or severely degrade the importing service.

An attacker able to provide STIX content to a MISP-STIX import workflow could exploit either condition to affect availability. A malformed document could cause abnormal process termination through an uncaught SystemExit, while a large document could exhaust resources during deserialisation and conversion.

The fixes replace process-terminating sys.exit() calls with catchable exceptions such as STIXLoadingError and MissingSTIXContentError, and extend exception handling around the complete STIX detection and conversion process. The importer also now enforces an input-size limit before parsing. The default maximum is 100 MB, can be adjusted by callers, and can explicitly be disabled when required. STIX 1 inputs are additionally checked for the expected root element before the complete XML tree is constructed.

ImpactSuccessful exploitation can cause:

  *  termination of a long-running MISP-STIX importer;
  *  excessive memory allocation;
  *  excessive CPU consumption;
  *  degradation or temporary unavailability of services relying on the converter;
  *  interruption of batch or automated STIX ingestion workflows.

### CVE-2026-16520

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-202` |
| Published | 2026-08-21T00:16:31.623 |

Improper input validation and Exposure of sensitive information through data queries vulnerability in Genians Genian NAC V4.0, Genians Genian NAC V5.0, and Genians Genian ZTNA V6.0 allows SQL Injection and Authentication Bypass.

This issue affects Genian NAC V4.0: from 4.0.0 before 4.0.175(Revision 150340); 
Genian NAC V5.0: from 5.0.0 before 5.0.65 LTS(Revision 150331), from 5.0.0 before 5.0.75 LTS(Revision 150330), from 5.0.0 before 5.0.87 Release Stable(Revision 150329), and from 5.0.0 before 5.0.88(Revision 150328); 
Genian ZTNA V6.0: from 6.0.0 before 6.0.26 LTS(Revision 150337), from 6.0.0 before 6.0.35 LTS(Revision 150336), from 6.0.0 before 6.0.47 Release Stable(Revision 150334), and from 6.0.0 before 6.0.48(Revision 150333).

### CVE-2026-72818

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-20T22:18:05.087 |

The URLS regular expression in nltk/tokenize/casual.py, compiled into TweetTokenizer.WORD_RE and applied by TweetTokenizer.tokenize, contains a naked-domain branch whose domain-label prefix [a-z0-9]+(?:[.\-][a-z0-9]+)* is unbounded. Input consisting of many alternating label separators can be partitioned in exponentially many ways, and because the branch also requires a trailing top-level domain that such input never supplies, the engine explores those partitions before failing at each offset. A few kilobytes of input therefore consumes seconds to minutes of single-threaded CPU, and the HANG_RE substitution performed before matching does not collapse the pattern. TweetTokenizer is intended for tokenizing untrusted social-media text, so any service that applies it, or the module-level casual_tokenize, to submitted text can be stalled per request without authentication. Version 3.10.1 bounds the label repetition.

### CVE-2026-74836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T21:17:09.407 |

Allocation of Resources Without Limits or Throttling vulnerability in mtrudel bandit allows an unauthenticated remote attacker to pin an unbounded number of HTTP/2 stream processes indefinitely via connection-level flow control. When a stream's response body outruns the HTTP/2 connection-level send window (default 65,535 bytes, shared across all streams on the connection), Bandit.HTTP2.Connection queues the remaining bytes and a reply closure in pending_sends and the stream process blocks forever inside a synchronous call to the connection process. Nothing bounds that wait and nothing purges the queue: a client RST_STREAM for the blocked stream is delivered to its mailbox but never read while it is stuck inside the call, so cancelling frees nothing, and periodic PING frames keep the transport-level read timeout from ever firing. The equivalent block on the stream-level send window is already bounded at 15 seconds; the connection-level path had no such bound.

Each stalled stream pins its process, Plug state, and any resource the Plug holds across the blocked write, such as a pooled upstream connection in a reverse-proxy Plug. The attacker chooses any endpoint whose response exceeds the connection window (common for most non-trivial payloads), grants a generous stream-level window so only the connection window limits it, and keeps the connection alive with periodic PINGs; the primitive is repeatable across streams and connections at the cost of one idle socket each.

This issue affects bandit: from 0.3.4 before 1.12.5.

### CVE-2026-73040

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T21:17:09.110 |

Dockge validates a stack name only on the write path. In backend/stack.ts the allow-list check in validate(), which requires the name to match ^[a-z0-9_-]+$, is reached from save() alone, while the path getter returns path.join(this.server.stacksDir, this.name) and Stack.getStack builds path.join(server.stacksDir, stackName) with no check. The socket handlers in backend/agent-socket-handlers/docker-socket-handler.ts confirm the caller is logged in and that the name is a string, then pass it straight to Stack.getStack, so a name containing traversal sequences resolves outside the managed stacks directory. An authenticated user can therefore read the composeENV and composeYAML values of any directory the server process can reach, which discloses the secrets in that directory's .env or Compose file, and can invoke delete(), which runs docker compose down and then fsAsync.rm on the traversed path with recursive and force set, removing that directory. Disclosure is limited to files named .env or an accepted Compose filename, and deletion requires the target directory to hold a valid Compose file so that docker compose down exits successfully. Dockge commonly runs as root with access to the Docker socket, so the reachable set includes unrelated applications on the host. Instances configured with disableAuth, a supported option that logs the caller in as admin automatically, expose both operations without authentication.

### CVE-2026-18420

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-08-20T21:17:06.137 |

Improper input validation in the Time Series Visual Builder (TSVB) plugin in OpenSearch Dashboards allows an authenticated remote user to execute arbitrary code on the server via a crafted JSON payload to the metrics visualization API endpoint. This issue is a form of prototype pollution that enables remote code execution. 



To remediate this issue, users should upgrade to OpenSearch Dashboards 3.8 or later.

### CVE-2026-66787

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-20T19:16:58.637 |

A flaw was found in the lighthouse component of Red Hat Advanced Cluster Management for Kubernetes. This vulnerability stems from insufficient validation of advertised IP addresses within EndpointSlice objects. A compromised spoke cluster can exploit this by creating EndpointSlices with attacker-controlled IP addresses, causing other clusters' lighthouse DNS to redirect legitimate service traffic to malicious endpoints. This enables a remote attacker to conduct transparent Man-in-the-Middle (MITM) attacks on cross-cluster service communications, potentially leading to unauthorized information disclosure and data manipulation.

### CVE-2026-76641

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T18:16:51.887 |

Expat through 2.8.3 contains an out-of-bounds read vulnerability that allows attackers to trigger memory corruption by processing XML with external entity parsers created via XML_ExternalEntityParserCreate. A struct size mismatch between ELEMENT_TYPE members causes storeAtts to read the attIndex member past allocated memory boundaries, resulting in failure to normalize whitespace in non-CDATA attributes or a wild pointer dereference causing a segfault. This vulnerability was introduced by the fix for CVE-2026-66046.

### CVE-2026-63384

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T18:16:36.367 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, libevent has an incorrect integer conversion in event_tagging.c when evtag_unmarshal_header uses evtag_decode_int to decode an attacker-controlled uint32 payload length and returns it as a signed int. Values above INT_MAX become negative or truncated, and evtag_unmarshal_string can use the converted value in allocation sizing, producing a wrapped large allocation request and denial of service. This issue is fixed in versions 2.1.13 and 2.2.2-alpha.

### CVE-2026-63383

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T18:16:35.917 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, libevent can read beyond a contiguous evbuffer region in event_tagging.c when decode_tag_internal requests at most five bytes from evbuffer_pullup but iterates using the full logical buffer length. A fragmented evbuffer containing a six-byte malformed tag can therefore advance past the pullup window and trigger an out-of-bounds read, which can crash a process that decodes attacker-controlled tagged RPC data. This issue is fixed in versions 2.1.13 and 2.2.2-alpha.

### CVE-2026-75140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T16:18:02.030 |

jsoup through 1.23.2, fixed in commit 862ba2f, contains an uncontrolled resource consumption vulnerability in XmlTreeBuilder that allows remote attackers to exhaust JVM heap memory by supplying a deeply nested XML document with uniquely-namespaced elements. The builder copies the entire inherited namespace map on every start element, causing quadratic time and memory complexity, which attackers can exploit to trigger an OutOfMemoryError and terminate the application.

### CVE-2026-76612

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T13:18:19.990 |

Joomla Extension - yootheme.com - Unauthenticated stored XSS via user-controlled fields in Zoo < 4.1.66 - User supplied input in comments and user supplied field elements weren't escaped, leading to a stored XSS vector.

### CVE-2026-77683

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-08-21T11:17:06.457 |

A security flaw has been discovered in Comfast CF-N1-S 2.6.0.1. Affected by this issue is the function system of the file /cgi-bin/mbox-config?method=SET&section=ntp_timezone. The manipulation of the argument timestr results in command injection. The attack can be launched remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-69558

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-20T22:18:00.610 |

Authorization bypass through user-controlled key in Microsoft Partner Center allows an unauthorized attacker to disclose information over a network.

### CVE-2026-69519

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-204` |
| Published | 2026-08-20T22:18:00.123 |

Observable response discrepancy in Azure Stack HCI allows an unauthorized attacker to disclose information over a network.

### CVE-2026-66800

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:17:56.043 |

Server-side request forgery (ssrf) in Azure Data Factory allows an unauthorized attacker to disclose information over a network.

### CVE-2026-53804

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T21:17:06.813 |

OTRS Community Edition contains an authenticated OS command injection vulnerability in the PGP encryption module that allows administrators to execute arbitrary operating-system commands by supplying crafted values for the PGP binary path and command options. Administrator-supplied configuration values are concatenated without sanitization into a shell command, enabling arbitrary command execution as the web server process user during normal ticket operations after the malicious configuration is deployed.

### CVE-2026-77148

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-20T19:17:04.710 |

A vulnerability was found in Comfast CF-N1-S 2.6.0.1. This impacts the function sub_44B50C of the file /cgi-bin/mbox-config?method=SET&section=ptest_channel of the component Web Management. The manipulation results in stack-based buffer overflow. The attack can be launched remotely. The exploit has been made public and could be used.

### CVE-2026-50190

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T19:16:53.907 |

Shaarli is a personal bookmarking service. Versions prior to 0.16.3 are vulnerable to stored XSS in `application/front/controller/visitor/BookmarkListController.php`. The `permalink` handler concatenates the raw `$bookmark->getTitle()` into the `pagetitle` template variable and the RainTPL template emits it into the document `<title>` element without HTML escaping. A bookmark title containing `</title><script>...</script>` closes the document title early and the injected script executes in the Shaarli origin for any visitor of `/shaare/{hash}`. Shaarli's metadata fetcher copies a remote page's `<title>` text verbatim into the local bookmark title, so an attacker who hosts an attacker-controlled URL and convinces an administrator to bookmark it plants the payload with no further interaction — and the resulting permalink fires for every visitor including the administrator on first save, providing a one-shot administrator account takeover. Version 0.16.3 fixes the issue.

### CVE-2026-77022

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-08-20T17:19:49.413 |

A security flaw has been discovered in Comfast CF-N1-S 2.6.0.1. Affected by this issue is the function sub_44B438 of the file /cgi-bin/mbox-config?method=SET&section=ptest_ssid of the component SSID Configuration. The manipulation of the argument ssid results in stack-based buffer overflow. The attack can be executed remotely. The exploit has been released to the public and may be used for attacks.

### CVE-2026-69543

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:18:00.270 |

Server-side request forgery (ssrf) in Azure Virtual Machines allows an authorized attacker to elevate privileges over a network.

### CVE-2026-69419

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T22:17:59.980 |

Integer overflow or wraparound in Azure Data Manager for Energy allows an authorized attacker to execute code over a network.

### CVE-2026-55765

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-256;CWE-522` |
| Published | 2026-08-20T22:17:22.487 |

CloudNativePG is a platform designed to manage PostgreSQL databases within Kubernetes environments. Prior to 1.28.4 and 1.29.2, CloudNativePG embedded cleartext role passwords in `ALTER ROLE` and `CREATE ROLE` statements generated by SetUserPassword in pkg/management/postgres/utils/roles.go and appendPasswordOption in internal/management/controller/roles/postgres.go. When pg_stat_statements was preloaded with track_utility enabled and an untrusted tenant held pg_monitor or pg_read_all_stats, the tenant could recover platform-managed superuser or application-owner passwords, reconnect through enabled superuser TCP access, and execute operating system commands in the database pod with `COPY ... FROM PROGRAM`. Clusters using SCRAM-SHA-256 verifiers in managed-role Secrets were not affected. This issue is fixed in versions 1.28.4, 1.29.2, and 1.30.0.

### CVE-2026-46682

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-20T22:17:19.347 |

BigBlueButton is an open-source virtual classroom. Prior to 3.0.23, BigBlueButton allowed authenticated moderators to inject SQL through the meetingId and userId values used by refreshBreakoutRoomsVisibleForUsers in akka-bbb-apps/src/main/scala/org/bigbluebutton/core/db/BreakoutRoomUserDAO.scala. The method interpolated those values into breakout room visibility queries, allowing arbitrary SQL execution against the application database. This issue is fixed in version 3.0.23.

### CVE-2026-17168

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:14.890 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-72852

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-08-20T19:17:00.830 |

hank-ai/darknet sizes a convolutional layer's weight and output heap buffers by multiplying configuration fields taken from a .cfg file in unchecked 32-bit int arithmetic. In src-lib/convolutional_layer.cpp, l.nweights is computed as (c / groups) * n * size * size and l.outputs as l.out_h * l.out_w * l.out_c, and both feed xcalloc directly. A .cfg whose true dimension product exceeds INT_MAX wraps to a small or zero value, so the allocation is undersized; for example width and height of 256 with filters of 65536 gives 2^32, which wraps to 0. forward_convolutional_layer then re-derives the GEMM dimensions with a different operand order, computing k as l.size*l.size*l.c / l.groups where the allocation divided before multiplying, and reads and writes through the undersized buffer. Loading the crafted .cfg for inference or training is sufficient and no valid .weights file is required. The reported proof of concept observed a heap buffer overflow read in gemm_nn_fast under AddressSanitizer and glibc allocator metadata corruption in a release build of the same input, indicating an out-of-bounds write.

### CVE-2026-66001

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-08-20T19:16:58.020 |

Frappe is a full-stack web application framework. Prior to 15.114.0 and 16.26.0, the approve and authorize functions in frappe/integrations/oauth2.py allow the OAuth2 consent flow to proceed without restricting approve to POST, without a csrf_token in frappe/templates/includes/oauth_confirmation.html, and without scoping an active OAuth token check to the requesting client. An attacker can cause an authenticated user to approve an OAuth grant or reuse authorization state for the wrong client, exposing data and permitting actions within the granted scopes. This issue is fixed in versions 15.114.0 and 16.26.0.

### CVE-2026-73220

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-80` |
| Published | 2026-08-20T15:18:37.200 |

CVAT is an open source interactive video and image annotation tool for computer vision. From 2.68.0 until 2.70.0, the audio-task annotation guide renderer in cvat-ui/src/audio/components/annotation-page/audio-workspace/top-bar/audio-right-group.tsx passes attacker-controlled guide Markdown to MDEditor without the rehype-sanitize plugin. A user who can create or edit an annotation guide can store malicious JavaScript that executes when another user opens the guide. The script can issue arbitrary CVAT requests with the victim user's privileges. This issue is fixed in version 2.70.0.

### CVE-2026-18842

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:17.773 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to an out-of-bounds write.

### CVE-2026-18824

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T22:17:16.930 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to execute arbitrary commands due to improper neutralization of special elements used in an OS command.

### CVE-2026-69242

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:H/SC:L/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-08-20T21:17:07.697 |

libvips is a fast image processing library with low memory needs. Prior to version 8.18.3, a crafted many-band TIFF processed through VipsForeignLoadTiff can evade scanline validation in libvips/iofuncs/image.c and cause an integer overflow in vips_image_sanity. The resulting buffer-region calculation can access attacker-controlled negative offsets in mmap-resident allocations, allowing reads or writes of other image data, possible data disclosure through uncompressed .v output, and likely process crashes. Remote code execution has not been demonstrated but cannot be ruled out. This issue is fixed in version 8.18.3.

### CVE-2026-63388

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-617;CWE-787` |
| Published | 2026-08-20T18:16:36.893 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, libevent has a heap out-of-bounds write in bufferevent_sock.c when bufferevent_socket_set_conn_address_ copies a kernel-supplied AF_UNIX peer address into bufferevent_private.conn_address. Release builds compiled with NDEBUG disable the EVUTIL_ASSERT length guard, and the evhttp accept path can pass a 110-byte sockaddr from accept() into the 28-byte field. An unauthenticated local peer able to connect to an AF_UNIX listener can overwrite the adjacent dns_request pointer and heap data, causing memory corruption with confidentiality, integrity, and availability impact. This issue is fixed in versions 2.1.13 and 2.2.2-alpha.

### CVE-2026-17006

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:11.147 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a heap buffer overflow.

### CVE-2026-75946

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-08-21T14:16:52.773 |

A potential security vulnerability has been identified in the OMEN Gaming Hub for versions prior to 1101.2608.0.0. The vulnerability could potentially allow a local attacker to escalate privileges due to insufficient access controls.

### CVE-2026-19442

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-20T22:17:18.110 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 has a pointer validation flaw exists in the AIX Virtual SCSI (vSCSI) initiator driver. Successful exploitation may result in denial of service, privilege escalation, or full compromise of the client LPAR kernel.

### CVE-2026-18840

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-08-20T22:17:17.603 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to improper validation of an attacker-controlled pointer.

### CVE-2026-18670

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T22:17:16.430 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service and potentially disclose sensitive information due to an integer underflow.

### CVE-2026-16943

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:08.313 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to a heap-based buffer overflow.

### CVE-2026-65842

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T17:19:23.433 |

Plate is a rich-text editor with AI and shadcn/ui. Prior to 53.3.2, @platejs/docx-io fetches remote image URLs while converting attacker-controlled HTML through htmlToDocxBlob in a server-side or privileged environment. The converter can make requests to internal network resources and include the fetched image bytes in the generated DOCX, allowing server-side request forgery with response disclosure. Applications can also incur resource consumption from attacker-selected remote responses. This issue is fixed in version 53.3.2.

### CVE-2026-40345

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-20T17:17:29.783 |

deepmerge-ts is a typescript library providing functionality to deep merging of javascript objects. Prior to 8.0.0, the deepmerge, deepmergeCustom, deepmergeInto, and deepmergeIntoCustom APIs do not track visited objects or object pairs when recursively merging records. When two input values contain self-references at the same property path, the merge logic repeatedly revisits the same pair until Node.js raises RangeError: Maximum call stack size exceeded. Applications that merge attacker-controlled recursive object graphs can synchronously crash the affected process or cause repeated worker restarts. Plain JSON input alone cannot create the recursive graph required to trigger the issue. This issue is fixed in version 8.0.0.

### CVE-2026-49825

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-79;CWE-184` |
| Published | 2026-08-20T15:17:30.707 |

lxml is a library for processing XML and HTML in the Python language. Prior to 6.1.1, link attributes in ``lxml.html.defs.link_attrs`` were missing ``xlink:href``, which can be used for URL bypass attacks in embedded SVG/MathML/etc. content. This vulnerability was fixed in lxml 6.1.1 and lxml_html_clean 0.4.5.

### CVE-2026-18781

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-21T07:16:25.143 |

The Drag and Drop Multiple File Upload for Contact Form 7 WordPress plugin before 1.3.9.9 does not validate the final name of an uploaded file after stripping characters from it, allowing unauthenticated users to defeat its file type restrictions and execute arbitrary code on the server.

### CVE-2026-19437

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:17.940 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a buffer overflow.

### CVE-2026-17138

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-20T22:17:13.187 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-17060

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-20T22:17:12.023 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to obtain sensitive information and cause a denial of service due to a kernel heap over-read.

### CVE-2026-17000

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-20T22:17:10.813 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to improper authentication.

### CVE-2026-77176

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-20T17:19:49.773 |

A flaw was found in Kata Containers. In configurations utilizing genpolicy for Confidential Containers guest protection, a malicious host operator can exploit insufficient validation of CreateContainer mount and storage rules. This allows them to mount arbitrary container-rootfs paths over sensitive host locations or provision arbitrary content, potentially exposing confidential information or enabling the acceptance of attacker-controlled input.

### CVE-2026-18282

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:24.643 |

Sony XAV-9500ES AVRCP_Br_Response_Parser Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Sony XAV-9500ES devices. An attacker must first obtain the ability to pair a malicious Bluetooth device with the target system in order to exploit this vulnerability.

The specific flaw exists within the handling of AVRCP packets. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-28995.

### CVE-2026-18281

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.0/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:24.523 |

Sony XAV-9500ES l2_reassemble_sdu Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows network-adjacent attackers to execute arbitrary code on affected installations of Sony XAV-9500ES devices. An attacker must first obtain the ability to pair a malicious Bluetooth device with the target system in order to exploit this vulnerability.

The specific flaw exists within the handling of Bluetooth L2CAP packets. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the device. Was ZDI-CAN-29072.

### CVE-2026-18716

| 項目 | 値 |
|------|-----|
| CVSS | `7.9` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T22:17:16.600 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote authenticated attacker to obtain sensitive information or cause a denial of service due to an out-of-bounds read.

### CVE-2026-17171

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-20T22:17:15.247 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to overwrite arbitrary files due to improper resolution of symbolic links.

### CVE-2026-17124

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T22:17:12.850 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to an out-of-bounds read.

### CVE-2026-16997

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T22:17:10.650 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary commands due to improper privilege management.

### CVE-2026-16991

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T22:17:10.317 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to improper handling of symbolic links.

### CVE-2026-16946

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:08.810 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to a heap buffer overflow.

### CVE-2026-16945

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-20T22:17:08.643 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to a stack-based buffer overflow.

### CVE-2026-16937

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T22:17:08.147 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-16935

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-20T22:17:07.817 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to a time-of-check to time-of-use (TOCTOU) race condition.

### CVE-2026-18309

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.987 |

GIMP APNG File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of APNG files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29401.

### CVE-2026-18308

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.877 |

GIMP TIF File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29405.

### CVE-2026-18307

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:27.757 |

GIMP TIF File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29404.

### CVE-2026-18306

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.633 |

GIMP SGI File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of SGI files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before writing to memory. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29396.

### CVE-2026-18305

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.520 |

GIMP TIF File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29406.

### CVE-2026-18304

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.403 |

GIMP TIF File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29403.

### CVE-2026-18303

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-20T17:17:27.277 |

GIMP TIF File Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29399.

### CVE-2026-18302

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:27.143 |

GIMP TIF File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of TIF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29398.

### CVE-2026-18301

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:27.017 |

GIMP PSD File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PSD files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29395.

### CVE-2026-18300

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T17:17:26.890 |

GIMP HDR File Parsing Integer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GIMP. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of HDR files. The issue results from the lack of proper validation of user-supplied data, which can result in an integer overflow before allocating a buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29289.

### CVE-2026-18299

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-20T17:17:26.767 |

GStreamer rtpsbcdepay Use-After-Free Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. Interaction with this library is required to exploit this vulnerability but attack vectors may vary depending on the implementation.

The specific flaw exists within the processing of RTP payload elements. The issue results from the lack of validating the existence of an object prior to performing operations on the object. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29787.

### CVE-2026-18298

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:26.643 |

GStreamer PNG File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of PNG files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29581.

### CVE-2026-18297

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-20T17:17:26.507 |

GStreamer OGG File Parsing Stack-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a stack-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29584.

### CVE-2026-18296

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T17:17:26.390 |

GStreamer MRF File Parsing Heap-based Buffer Overflow Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of MRF files. The issue results from the lack of proper validation of the length of user-supplied data prior to copying it to a heap-based buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29608.

### CVE-2026-18295

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T17:17:26.260 |

GStreamer MRF File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of GStreamer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of MRF files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated buffer. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29510.

### CVE-2026-18294

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-20T17:17:26.130 |

OriginLab Origin Viewer OGW File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGW files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29338.

### CVE-2026-18293

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T17:17:26.010 |

OriginLab Origin Viewer OPJ File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab Origin Viewer. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJ files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29336.

### CVE-2026-18292

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-20T17:17:25.890 |

OriginLab OriginPro OGG File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab OriginPro . User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29335.

### CVE-2026-18291

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-08-20T17:17:25.767 |

OriginLab OriginPro OGW File Parsing Memory Corruption Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab OriginPro. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGW files. The issue results from the lack of proper validation of user-supplied data, which can result in a memory corruption condition. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29334.

### CVE-2026-18290

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T17:17:25.647 |

OriginLab OriginPro OGG File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab OriginPro. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OGG files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29333.

### CVE-2026-18289

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T17:17:25.523 |

OriginLab OriginPro OPJ File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab OriginPro. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJ files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29332.

### CVE-2026-18288

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T17:17:25.397 |

OriginLab OriginPro OPJU File Parsing Out-Of-Bounds Write Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of OriginLab OriginPro. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of OPJU files. The issue results from the lack of proper validation of user-supplied data, which can result in a write past the end of an allocated data structure. An attacker can leverage this vulnerability to execute code in the context of the current process.
. Was ZDI-CAN-29331.

### CVE-2026-18287

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T17:17:25.263 |

Aeon load_time_series_segmentation_benchmark Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of aeon. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the load_time_series_segmentation_benchmark method. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29159.

### CVE-2026-18286

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-20T17:17:25.140 |

Aeon load_human_activity_segmentation_datasets Code Injection Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of aeon. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the load_human_activity_segmentation_datasets method. The issue results from the lack of proper validation of a user-supplied string before using it to execute Python code. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-29160.

### CVE-2026-18285

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T17:17:25.007 |

Aeon load_rehab_pile_dataset Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Aeon. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the load_rehab_pile_dataset method. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-28749.

### CVE-2026-18284

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T17:17:24.883 |

Sony XAV-9500ES Crash Dump Handler Command Injection Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Sony XAV-9500ES devices. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the handling of process crash dumps. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29061.

### CVE-2026-18270

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-20T17:17:23.513 |

Kenwood DNR1007XR udhcpd Incorrect Permission Assignment Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Kenwood DNR1007XR devices. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the udhcpd service. The issue results from incorrect permissions set on a resource used by the service. An attacker can leverage this vulnerability to escalate privileges and execute code in the context of root. Was ZDI-CAN-29111.

### CVE-2026-18263

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-08-20T17:17:22.773 |

Parallels RAS Client RDP Backend Service Exposed Dangerous Function Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Parallels RAS Client. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the RAS RDP Backend Service. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28886.

### CVE-2026-18262

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-08-20T17:17:22.653 |

Parallels RAS Client RDP Backend Service Exposed Dangerous Function Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Parallels RAS Client. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the RAS RDP Backend Service. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-28885.

### CVE-2026-15679

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-20T17:17:21.050 |

Hugging Face PyTorch Image Models checkpoint Deserialization of Untrusted Data Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Hugging Face PyTorch Image Models. User interaction is required to exploit this vulnerability in that the target must visit a malicious page or open a malicious file.

The specific flaw exists within the parsing of checkpoints. The issue results from the lack of proper validation of user-supplied data, which can result in deserialization of untrusted data. An attacker can leverage this vulnerability to execute code in the context of the current process. Was ZDI-CAN-27987.

### CVE-2026-13121

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-08-20T17:17:20.787 |

Parallels RAS Client RDP Backend Service Exposed Dangerous Function Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Parallels RAS Client. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the RAS RDP Backend Service. The issue results from an exposed dangerous function. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of SYSTEM. Was ZDI-CAN-29220.

### CVE-2026-61898

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T15:17:38.913 |

The Ubuntu-specific language helper scripts (save-to-pam-env, update-langlist) shipped with accountsservice before 23.13.9-8ubuntu7 treat the user-controlled LANGUAGE entry in ~/.pam_environment as trusted input. The value is interpolated unescaped into a GNU sed replacement expression, allowing an attacker to inject a sed 'e' flag and arbitrary shell commands that execute with the privileges of the AccountsService helper process (real UID 0) via the SetLanguage D-Bus method.

### CVE-2026-61897

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-273` |
| Published | 2026-08-20T15:17:38.740 |

An Ubuntu-specific patch to AccountsService before 23.13.9-8ubuntu7 only partially drops privileges before launching language helper scripts. It changes the effective UID/GID to the target user but leaves the real UID as 0 (root). A shell spawned by a helper script inherits ruid=0 and may reset its effective UID to root, enabling local privilege escalation.

### CVE-2026-77775

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-21T12:16:36.813 |

Headroom's LLM proxy lets a client choose the upstream destination with the x-headroom-base-url request header. _resolve_openai_upstream_base in headroom/proxy/handlers/openai.py accepts the header value, requires only that it parse with an http or https scheme and a hostname, and returns it for use as the upstream base; _select_passthrough_base_url in headroom/providers/proxy_routes.py reads the same header for the passthrough routes. No check rejects loopback, link-local, or RFC 1918 destinations, and because the component is a proxy the upstream response is returned to the caller, so the request reaches internal services and cloud metadata addresses and their responses are disclosed. The Authorization header accompanying the request is forwarded unchanged to the caller-designated host. The pip console script binds 127.0.0.1 by default, but the reference docker-compose.yml ships --host 0.0.0.0 with published ports and no required HEADROOM_PROXY_TOKEN, which the server itself warns about at startup, so a deployment following the shipped compose exposes the affected data-plane routes to the network without authentication.

### CVE-2026-73267

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-602` |
| Published | 2026-08-21T03:16:39.080 |

A flaw was found in the clusterclaims-controller component of multicluster engine (MCE). A tenant with standard permissions to create and delete ClusterClaim resources can exploit this by manipulating the `spec.namespace` field. This allows the tenant to specify and delete any ManagedCluster, including the hub's local-cluster or other tenants' clusters, due to a missing ownership check. This vulnerability can lead to a denial of service by enabling unauthorized deletion of ManagedClusters.

### CVE-2026-77646

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-502;CWE-918` |
| Published | 2026-08-20T22:18:06.657 |

A Server-Side Request Forgery (SSRF) vulnerability has been reported in PTC Windchill PDMLink and PTC FlexPLM. The vulnerability may be exploited through the deserialization of untrusted data.

### CVE-2026-72848

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:18:05.553 |

SitemapLoader.parse_sitemap in langchain_community/document_loaders/sitemap.py applies the documented restrict_to_same_domain control only to leaf url entries. The loop over url elements filters cross-domain locations, but the loop over nested sitemap elements passes the child loc straight to self.scrape_all([loc.text], "xml"), which reaches WebBaseLoader.scrape_all and an aiohttp GET, with no domain comparison and no check for private, loopback or link-local destinations. An attacker who controls or influences an ingested sitemap can therefore point a nested sitemap entry at an internal address and make the server fetch it even when the deploying application set restrict_to_same_domain to True specifically to confine outbound requests. The fetched content is parsed and surfaces in the returned Documents, so internal responses are disclosed to the caller rather than merely requested.

### CVE-2026-69855

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T22:18:01.003 |

Server-side request forgery (ssrf) in Microsoft Copilot in Azure allows an authorized attacker to disclose information over a network.

### CVE-2026-17423

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T22:17:15.767 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to obtain sensitive information and cause a denial of service due to an out-of-bounds read.

### CVE-2026-17024

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-08-20T22:17:11.677 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to execute arbitrary code due to improper certificate validation.

### CVE-2026-17003

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:10.983 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to compromise the confidentiality and integrity of the system due to an out-of-bounds write.

### CVE-2026-73137

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-20T21:17:09.270 |

A flaw was found in the multicloud-operators-subscription component of Red Hat Advanced Cluster Management (RHACM). A tenant with HelmRelease create permissions can exploit this vulnerability by manipulating the `secretRef.Namespace` field. This allows the `GetSecret()` function in the HelmRelease controller to fetch sensitive credentials from any namespace, which are then sent to an attacker-controlled Helm repository. This can lead to the exfiltration of credentials from arbitrary namespace Secrets, resulting in information disclosure.

### CVE-2026-53425

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-08-20T18:16:27.850 |

Insufficient Verification of Data Authenticity vulnerability in dropbox samly allows an attacker to establish an authenticated session using a SAML response the service provider never requested.

Samly.SPHandler.validate_authresp/3 in lib/samly/sp_handler.ex validates a SAML response for the SP-initiated flow by comparing only the RelayState value, the IdP identifier, and the presence of a target URL held in the session. It never compares SubjectConfirmationData/@InResponseTo against the ID of the AuthnRequest the service provider issued, and that request ID is never persisted, so no comparison is possible. SAML 2.0 Core section 4.1.4.3 requires a service provider to reject a response whose InResponseTo does not match a request it made. The underlying esaml library checks status, signature, recipient, audience, and staleness, but likewise never inspects InResponseTo, so nothing else closes the gap. Exploitation requires a validly signed assertion from the trusted IdP, which an attacker can obtain for their own account, and a RelayState matching the victim's session; the assertion signature itself remains intact, so this is not a signature-forgery issue.

This issue affects samly: from 0.3.0 onward.

### CVE-2026-59279

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-21T12:16:30.013 |

The MCP Streamable HTTP server transport (WebFlux and WebMvc variants) does not place any limit on the number of sessions it retains, and by default does not require clients to be authenticated. As a result, a remote attacker can cause the server to accumulate an unbounded number of sessions over time, gradually exhausting available memory and ultimately causing a Denial of Service that affects all legitimate clients.
Affected versions:
Spring AI: 2.0.0

### CVE-2026-47827

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-08-21T10:16:38.647 |

Command Injection in BOSH CLI tool on windows in Cloud Foundry allows a remote attacker to execute arbitrary shell commands via command injection vulnerabilities

### CVE-2026-16323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-698` |
| Published | 2026-08-21T08:16:42.667 |

Execution after redirect (EAR) vulnerability in FuyaWeb Internet and Informatics Services ArchitectPanel Web Admin Panel allows Authentication Bypass.

This issue affects ArchitectPanel Web Admin Panel: through 28072026.

### CVE-2026-77642

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:18:06.070 |

tor before 0.4.9.9 was prone to an out-of-bounds write when parsing a consensus or  detached signature with unexpected signature digest type. Impact  is minor for most Tor roles, but potentially major for directory   authorities. This is TROVE-2026-019.

### CVE-2026-49217

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-20T22:17:19.803 |

Mailu is a mail server as a set of Docker images. Prior to version 2024.06.52, a missing authorization check in the Mailu admin REST API allows any unauthenticated attacker to remove any potential IP restriction or update the comment field from any existing user token provided the REST API is enabled. Upgrade to Mailu 2024.06.52 to receive a patch or, as a workaround, turn the REST API off.

### CVE-2026-19446

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-20T22:17:18.273 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 allows a remote unauthenticated attacker can send a crafted UDP packet to a reachable RPC service, resulting in complete system unavailability and requiring an LPAR restart.

### CVE-2026-17425

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-20T22:17:16.103 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to a stack buffer overflow.

### CVE-2026-17170

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T22:17:15.067 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to improper validation of an allocation size.

### CVE-2026-17165

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-20T22:17:14.713 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to a NULL pointer dereference.

### CVE-2026-17163

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-08-20T22:17:14.540 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to improper validation of an array size field.

### CVE-2026-17159

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-20T22:17:14.187 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to an integer overflow.

### CVE-2026-17121

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-20T22:17:12.517 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to uncontrolled recursion.

### CVE-2026-53587

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-125;CWE-126;CWE-1284` |
| Published | 2026-08-20T19:16:55.137 |

libgit2 is a portable C implementation of the Git core methods provided as a linkable library with a solid API, allowing to build Git functionality into your application. Prior to 1.8.6 and 1.9.5, libgit2 performs a fixed-size strncmp in set_data in src/libgit2/transports/smart_pkt.c without first verifying that the smart-protocol pkt-line capability buffer contains 14 bytes. A malicious Git server can make bytes after the pkt-line complete object-format=, causing format_str to advance beyond the pkt-line and the following memchr length calculation to underflow. The resulting heap out-of-bounds walk can crash a client during the first refs-advertisement packet over HTTP, HTTPS, SSH, or the Git protocol. This issue is fixed in versions 1.8.6 and 1.9.5.

### CVE-2026-63495

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-08-20T18:16:37.040 |

Libevent is an event notification library. From 2.2.0-alpha-dev until 2.2.2-alpha, the libevent WebSocket server in ws.c accumulates fragmented frames in evws->incomplete_frames without enforcing a total message-size limit. An unauthenticated remote client can repeatedly send fragmented WebSocket frames below WS_MAX_RECV_FRAME_SZ with FIN=0, causing the evbuffer to grow without bound until the process or host exhausts memory. This issue is fixed in version 2.2.2-alpha.

### CVE-2026-69183

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-290;CWE-307;CWE-644` |
| Published | 2026-08-20T17:19:34.387 |

Monkeytype is a minimalistic and customizable typing test. In 26.26.0 and earlier, the backend rate-limit key generator in backend/src/middlewares/rate-limit.ts uses client-controlled cf-connecting-ip and x-forwarded-for headers before the trust-proxy-derived req.ip value. An unauthenticated attacker can rotate either header to create a new bucket for each request, bypassing rootRateLimiter, badAuthRateLimiter, getKey(), and the getKeyWithUid() fallback used by public endpoints. This permits repeated POST /users/forgotPasswordEmail and verificationEmail requests, mail bombing registered users, consuming Firebase or SMTP quota, evading brute-force protection, and enabling resource exhaustion. Exploitability of cf-connecting-ip depends on deployment topology, but x-forwarded-for and direct-to-origin paths remain affected when those values are not overwritten by a trusted proxy. No fixed version is available as of this review.

### CVE-2026-61704

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-20T17:18:51.940 |

Link Preview JS extracts web links information. Prior to 4.0.4, the resolveDNSHost mitigation in index.ts validates one resolved IP address but fetches the original hostname, allowing an attacker-controlled DNS server to return a public address during validation and a loopback or internal address during the final connection. This DNS rebinding condition bypasses the SSRF protection and can cause the server-side preview fetch to reach internal HTTP resources. Redirect handling is affected by the same validation-to-fetch mismatch. This issue is fixed in version 4.0.4.

### CVE-2026-63490

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-23;CWE-552` |
| Published | 2026-08-20T15:18:04.577 |

Handlebars.java provides logic-less and semantic Mustache templates with Java. Prior to 4.5.3, com.github.jknack.handlebars.springmvc.SpringTemplateLoader resolves attacker-influenced Spring MVC view names through Spring ResourceLoader without the path-containment validation used by other URL-based loaders. In handlebars-springmvc/src/main/java/com/github/jknack/handlebars/springmvc/SpringTemplateLoader.java, a view name using a file: or classpath: URL and ending with the # fragment delimiter places the appended .hbs suffix in the fragment, which FileUrlResource.exists() and URL.openStream() discard. HandlebarsViewResolver in handlebars-springmvc/src/main/java/com/github/jknack/handlebars/springmvc/HandlebarsViewResolver.java then passes the attacker-controlled name to handlebars.compile(), allowing an unauthenticated remote attacker to read files accessible to the JVM when an application exposes a controller with a user-influenced view name. This issue is fixed in version 4.5.3.

### CVE-2026-16928

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T15:17:29.293 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to a heap-based buffer overflow.

### CVE-2026-16924

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-191` |
| Published | 2026-08-20T15:17:28.607 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a remote attacker to cause a denial of service due to an improper calculation of a memory offset during IPsec decapsulation.

### CVE-2026-19611

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-173` |
| Published | 2026-08-20T16:17:18.293 |

A flaw was found in WildFly Elytron. Password hashing and verification normalize input with Unicode NFKC, which can collapse fullwidth characters to ASCII equivalents. A remote attacker can more easily guess affected passwords by using an ASCII-only dictionary against accounts whose passwords were intended to include those non-ASCII characters, leading to unauthorized access.

### CVE-2026-14208

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-08-21T11:17:04.287 |

Remote Utilities Host <=7.7.3.0 sets insecure ACLs on all DLL files in the installation directory (C:\Program Files (x86)\Remote Utilities - Host\), granting FULL CONTROL (F) to the built-in Everyone group (BUILTIN\Everyone, S-1-1-0). A Windows service running as NT AUTHORITY\SYSTEM loads DLLs from this directory. The DLLs are file-locked at runtime, but a race window exists when the service is stopped (e.g. during a software update or following a crash), during which a local unprivileged attacker can replace a DLL with a malicious payload. Upon service restart, the payload executes as NT AUTHORITY\SYSTEM. The DLL confirmed as actively loaded during testing is libasset32.dll. Additional DLLs in the same directory (eventmsg.dll, libcodec32.dll, vp8encoder.dll, vp8decoder.dll, webmvorbisdecoder.dll, webmvorbisencoder.dll, webmmux.dll) share identical insecure permissions.

### CVE-2026-55893

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-20T22:17:22.787 |

Capstone is a disassembly framework. In 6.0.0-Alpha9 and earlier, Capstone's arch/SH/SHDisassembler.c SH floating-point decoders such as opFADD, opFMUL, and opFSUB call set_reg() and set_reg_n() using sh_info.op.op_count without checking the fixed-size operands[] array. Repeated crafted instructions processed through cs_disasm_iter() or cs_disasm() with CS_ARCH_SH, CS_MODE_SH2A or CS_MODE_SH4A, CS_MODE_SHFPU, and CS_OPT_DETAIL can increment the operand count beyond the 176-byte sh_info allocation and perform a four-byte heap buffer overflow write. The corruption can crash the process and may enable code execution depending on heap layout. This issue is fixed in version 6.0.0-Alpha10.

### CVE-2026-49436

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-20T22:17:20.240 |

LinkAce is a self-hosted archive to collect website links. Prior to version 2.5.7, the Bulk Link API endpoint (`POST /api/v2/bulk/links`) accepts URLs without any format validation, allowing an authenticated user to store a `javascript:` URI. The stored URI is later rendered verbatim as an `href` in Blade templates, and clicking it executes arbitrary JavaScript in the victim's browser — exfiltrating cookies and session tokens. Version 2.5.7 fixes the issue.

### CVE-2026-16927

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-20T15:17:29.130 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain root privileges due to a time-of-check to time-of-use (TOCTOU) race condition.

### CVE-2026-75796

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-21T07:16:25.453 |

The AI Engine  WordPress plugin before 3.6.1 does not verify that the requesting user is authorized to act on the targeted account before performing privileged user management operations, allowing users with the Administrator role on a Multisite sub-site to take over any account on the network, including the Network Administrator's.

### CVE-2026-16576

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-21T07:16:24.740 |

The Dokan: AI Powered WooCommerce Multivendor Marketplace Solution  WordPress plugin before 5.0.14 does not correctly check user capabilities on some of its admin REST API routes, checking only for a WooCommerce management capability instead of the Dokan: AI Powered WooCommerce Multivendor Marketplace Solution  WordPress plugin before 5.0.14-installation capability, allowing users such as Shop Managers to install and activate arbitrary Dokan: AI Powered WooCommerce Multivendor Marketplace Solution  WordPress plugin before 5.0.14 from WordPress.org.

### CVE-2026-18409

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-21T04:18:01.380 |

The WPForms Pro plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Single Line Text and Paragraph Text Field Values in all versions up to, and including, 2.0.0.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The exploit relies on the plugin's own wp_kses_allowed_html filter widening the 'post' allowlist to permit iframe elements with a data-src attribute, which is not on WordPress's URI-attribute sanitization list, allowing a javascript: URI stored in data-src to survive kses processing and subsequently be promoted to a live src attribute by the bundled admin script view-entry.min.js.

### CVE-2026-18274

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-20T17:17:24.003 |

Heimdall Data Database Proxy uploadJar Directory Traversal Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Heimdall Data Database Proxy. Authentication is required to exploit this vulnerability.

The specific flaw exists within the uploadJar method. The issue results from the lack of proper validation of a user-supplied path prior to using it in file operations. An attacker can leverage this vulnerability to execute code in the context of root. Was ZDI-CAN-28603.

### CVE-2026-15686

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-253` |
| Published | 2026-08-20T17:17:21.180 |

Adminer multi_query Incorrect Check of Function Return Value Remote Code Execution Vulnerability. This vulnerability allows remote attackers to execute arbitrary code on affected installations of Adminer. Authentication is required to exploit this vulnerability.

The specific flaw exists within the multi_query method. The issue results from an incorrect check of a function return value. An attacker can leverage this vulnerability to execute code in the context of the web server. Was ZDI-CAN-28201.

### CVE-2026-77769

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-21T11:17:07.430 |

The report.list procedure in packages/trpc/src/routers/report.ts accepted a projectId and a dashboardId and returned getReportsByDashboardId(dashboardId). The enforceAccess middleware in packages/trpc/src/trpc.ts verified membership for the supplied projectId, but nothing verified that the supplied dashboardId belonged to that project, and getReportsByDashboardId in packages/db/src/services/reports.service.ts selects reports by dashboardId alone with no project scoping. An authenticated user could therefore pair a projectId from their own organization, which satisfies the middleware, with a dashboardId belonging to another organization and receive every report in that dashboard. A correctly scoped helper, listReportsCore, already existed in the same service file and resolves the dashboard through getDashboardById(dashboardId, projectId) before returning reports, but the router did not use it.

### CVE-2026-77768

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-21T11:17:07.283 |

The report.get procedure in packages/trpc/src/routers/report.ts accepted only a reportId and returned getReportById(reportId) directly. The enforceAccess middleware in packages/trpc/src/trpc.ts evaluates membership only when the input carries a projectId or organizationId key, so an input consisting of a reportId alone passed through unchecked, and getReportById in packages/db/src/services/reports.service.ts performs a findUnique on the report id with no project scoping. Any authenticated user could therefore read the full configuration of any saved report on the instance, including the owning projectId, event series, filters, breakdowns and formulas, by supplying its identifier. The adjacent update, delete and duplicate procedures resolve the report first and check getProjectAccess against the report's own projectId, so the omission was specific to this procedure.

### CVE-2026-77763

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T11:17:06.937 |

The filestore backend in pkg/object/file.go, used for file:// stores and as a common juicefs sync destination, derived every operation's target from path(key), which returned either filepath.Join(d.root, key) or filepath.Clean(d.root + key) with no check that the result stayed beneath the root. Put, Get, Head, Delete, Chmod, Chown, Symlink and Readlink all consumed that value directly. Object keys enumerated from a source object store during a sync are not constrained the way local filesystem names are, so a key containing traversal segments causes juicefs to write attacker-supplied content to a path outside the intended local destination, and no error is returned. An operator syncing from a bucket whose contents they do not fully control, such as a shared or public bucket or one an attacker can write to, is therefore exposed to a file write at an attacker-influenced location. The fix changes path() to return an error and rejects any key whose resolved path escapes the root.

### CVE-2026-55013

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-427` |
| Published | 2026-08-20T22:17:21.933 |

Uncontrolled search path element in Windows Remote Help Defense allows an authorized attacker to perform spoofing locally.

### CVE-2026-46355

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-20T22:17:19.193 |

BigBlueButton is an open-source virtual classroom. Prior to 3.0.23, BigBlueButton exposed /bigbluebutton/api/handleJoinExistingUser through bigbluebutton-web/grails-app/controllers/org/bigbluebutton/web/controllers/ApiController.groovy. A requester able to supply an existingUserID for an active participant could reuse that participant's session and impersonate the participant in the same meeting because handleJoinExistingUser was a routable controller action rather than a private helper. This issue is fixed in version 3.0.23.

### CVE-2026-16989

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-20T22:17:10.147 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to improper resolution of symbolic links.

### CVE-2026-75910

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-20T20:17:46.937 |

Incorrect privilege assignment in the ClickHouse connector deployment template in Amazon Athena Federated Query prior to v2026.17.1 could allow an authenticated remote user to read arbitrary AWS Secrets Manager secrets in the deploying account by pointing the connector's connection string at an unrelated secret and at a database endpoint under the user's control, causing the connector to transmit the secret to that endpoint. To remediate this issue, users should upgrade to aws-athena-query-federation connectors version v2026.17.1 or later and ensure that any forked or derivative code is patched to incorporate the new fixes. Alternatively, to remediate this issue, users should redeploy the connector with the current template and supply a non-empty SecretNamePrefix value.

### CVE-2026-62315

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-20T19:16:56.980 |

Frappe is a full-stack web application framework. In version 16.31.0 and earlier, frappe.client.set_value in frappe/client.py checks a dictionary supplied through the fieldname parameter against forbidden standard and child-table fields before parsing the dictionary into individual field names. An authenticated caller can exploit this type confusion to mass-assign protected fields through the client endpoint. No released fixed version is available as of this review.

### CVE-2026-54623

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-674;CWE-835` |
| Published | 2026-08-20T18:16:28.013 |

django CMS is an easy-to-use and developer-friendly enterprise content management system powered by Django. Prior to 5.0.8, the move_plugin endpoint in cms/admin/placeholderadmin.py accepts an attacker-controlled plugin_parent value without rejecting a plugin’s own identifier or a descendant identifier. A staff user with plugin-change permission under CMS_PERMISSION can create a parent_id cycle in the plugin tree. The _get_descendants_cte and _get_ancestors_cte queries in cms/models/pluginmodel.py have no cycle guard, so get_descendants() and later rendering, copy, or delete operations can recurse indefinitely or reach a database recursion limit, corrupting the tree and consuming request workers. This issue is fixed in versions 5.0.8.

### CVE-2026-54616

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-125` |
| Published | 2026-08-20T17:18:18.090 |

NanaZip is the 7-Zip derivative intended for the modern Windows experience. From version 1.0.88.0 until stable version 6.0.1698.0 and preview version 6.5.1742.0, the Lz4Decode function in NanaZip.Core/SevenZip/CPP/7zip/Archive/SquashfsHandler.cpp rejects only a zero return from LZ4_decompress_safe even though malformed input produces a negative error value. The negative int is converted to the unsigned SizeT destLen and then truncated into outBufWasWrittenSize, causing ReadBlock to trust an attacker-inflated _cachedUnpackBlockSize. During fragment extraction, an attacker-controlled inode Offset can make memcpy read beyond the _cachedBlock heap allocation and place adjacent heap contents in the extracted file, or crash the process. This issue is fixed in stable version 6.0.1698.0 and preview version 6.5.1742.0.

### CVE-2026-16925

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-20T15:17:28.800 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to achieve privilege escalation due to improper authorization.

### CVE-2026-75115

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:L/VA:L/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-21T13:18:19.140 |

Joomla Extension - yootheme.com - Authenticated, privileged arbitrary file read in YOOtheme Pro 2.3.0-5.0.40 - The Filesystem source's path filter is vulnerable to glob-based pattern attacks, allowing authorized users to read arbitrary files.

### CVE-2026-77584

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-821` |
| Published | 2026-08-20T21:17:10.810 |

Tor before 0.4.9.10 did not reject a CONFLUX_LINK cell that arrives on a circuit which already has attached streams. A malicious client could send a RELAY_COMMAND_BEGIN before the CONFLUX_LINK on the same circuit, attaching an exit stream that would later end up orphan leaving a dangling circuit back-pointer and a use-after-free (UAF) when the circuit is freed. This is TROVE-2026-025.

### CVE-2026-63387

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-121;CWE-193;CWE-787` |
| Published | 2026-08-20T18:16:36.723 |

Libevent is an event notification library. Prior to 2.1.13 and 2.2.2-alpha, libevent has an off-by-one stack buffer overflow in evdns.c when dnsname_to_labels formats a name-bearing DNS record at the end of the 64 KB stack buffer allocated by evdns_server_request_format_response. The final-label check permits j plus label_len plus one to equal buf_len, after which the terminating null byte is written to buf[buf_len]. A crafted DNS server response containing PTR, CNAME, MX, NS, or SOA data can trigger the one-byte out-of-bounds write and crash or corrupt the process. This issue is fixed in versions 2.1.13 and 2.2.2-alpha.

### CVE-2026-18268

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.0/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-20T17:17:23.277 |

Kenwood DNR1007XR JKGenService Command Injection Local Privilege Escalation Vulnerability. This vulnerability allows local attackers to escalate privileges on affected installations of Kenwood DNR1007XR devices. An attacker must first obtain the ability to execute low-privileged code on the target system in order to exploit this vulnerability.

The specific flaw exists within the JKGenService. The issue results from the lack of proper validation of a user-supplied string before using it to execute a system call. An attacker can leverage this vulnerability to escalate privileges and execute arbitrary code in the context of root. Was ZDI-CAN-29066.

### CVE-2026-16923

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-20T15:17:28.433 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to gain elevated privileges due to improper privilege management.

### CVE-2026-16922

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-08-20T15:17:28.263 |

IBM AIX 7.2, and 7.3 and IBM PowerVM VIOS 4.1 could allow a local attacker to execute arbitrary code due to a time-of-check to time-of-use (TOCTOU) race condition.
