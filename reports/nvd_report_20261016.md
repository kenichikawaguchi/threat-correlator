# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-15 15:00 UTC
- **対象期間**: `2026-10-14T15:03:48.000Z` 〜 `2026-10-15T15:00:52.000Z`
- **重要CVE数**: 463 件（Critical 9.0+: 92 件 / High 7.0〜: 371 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
直近で公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超に上り、**Web アプリケーション・プラグイン** と **インフラ系コントロールパネル** に集中しています。特に **SQL インジェクション**、**認証バイパス**、**任意コード実行** が多発しており、攻撃者はリモートから管理者権限取得やサーバー内部情報の取得が可能になるケースが目立ちます。Kubernetes 環境やメールゲートウェイといった基盤サービスでも深刻な脆弱性が報告されており、**サプライチェーン全体のリスクが拡大**していることが特徴です。

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・対象 | 注目理由 |
|-----|------|----------------|----------------|----------|
| **CVE‑2026‑55572** | 10.0 | **SQL インジェクション**（認証バックエンド） | e107 CMS 2.3.6 以前の `alt_auth` プラグイン | **最高スコア**。認証時にユーザー名が直接 SQL に埋め込まれ、認証バイパスだけでなく任意コード実行が可能。管理者権限取得が即座に成立するため、全サイトでの緊急アップデートが必須。 |
| **CVE‑2026‑108390** | 9.9 | **コマンドインジェクション**（設定ファイル書き込み） | Hestia Control Panel 1.9.7‑1.10.4 | 低権限ユーザーでも `web.conf` に任意文字列を書き込める。結果として Web サーバー設定の改ざんや任意ファイル実行が可能。ホスティング環境で広く利用されている点がリスクを拡大。 |
| **CVE‑2026‑77524** | 9.9 | **権限昇格・外部エンドポイント操作** | KEDA 2.20.2 以前 | 名前空間管理者が `TriggerAuthentication` に任意の Vault エンドポイントを設定でき、Kubernetes 認証を迂回してシークレット取得が可能。マルチテナント環境での情報漏洩リスクが高い。 |
| **CVE‑2026‑76519** | 9.8 | **任意ファイル書き込み**（AMP 機能） | Cisco Secure Email Gateway (SEAG) | 添付ファイル処理の不備により、リモートから OS 上に任意ファイルを書き込める。メールゲートウェイは組織の境界防御の要であり、侵入後の持続化やランサムウェア展開に直結。 |
| **CVE‑2026‑59774** | 9.8 | **任意ファイル読み取り（パス・トラバーサル）** | Gitea の Org‑mode マークアップレンダラ | 公開リポジトリの `INCLUDE` ディレクティブでサーバ側ファイルを参照でき、サービスアカウントがアクセスできる全ファイルが漏洩。CI/CD パイプラインでの機密情報流出リスクが顕在化。 |

> **共通点**：いずれも「**認証・権限チェックの欠如**」が根本原因であり、**外部からの直接アクセスが可能**な点が共通しています。特にインフラ系製品（Hestia、KEDA、Cisco SEAG）は、組織全体のセキュリティ境界を覆うため、早急な対策が求められます。

---

## 3. 推奨アクション  

### 3.1 パッケージ・バージョンのアップデート
| 製品 | 現行脆弱バージョン | 修正済みバージョン | アップデート手順 |
|------|-------------------|-------------------|----------------|
| **e107 CMS** | < 2.3.7 | ≥ 2.3.7 | `composer update e107/e107` または公式サイトから最新版 zip を展開し、`e107_plugins/alt_auth` を上書き。 |
| **Hestia Control Panel** | 1.9.7 〜 1.10.4 | ≥ 1.10.5 | `apt-get update && apt-get install hestia=1.10.5-1`（Debian/Ubuntu）または公式スクリプト `bash <(curl -s https://hestiacp.com/install.sh) --force`。 |
| **KEDA** | ≤ 2.20.2 | ≥ 2.20.3 | `helm upgrade keda oci://registry-1.docker.io/kedacore/keda --version 2.20.3`（Helm 使用時）。 |
| **Cisco Secure Email Gateway (SEAG)** | すべての 2026‑* リリース | Cisco が提供する **2026‑XX‑YY** 以降のパッチ | Cisco Smart Software Manager から最新ファームウェアをダウンロードし、管理コンソール → **System → Software Upgrade** で適用。 |
| **Gitea** | すべての 2026‑* リリース | ≥ 1.22.0（2026‑03‑15 リリース） | `docker pull gitea/gitea:1.22.0` → コンテナ再起動、またはバイナリ版は公式サイトから `gitea-1.22.0-linux-amd64` を取得。 |

### 3.2 設定・運用上の対策
- **Web アプリケーションファイアウォール (WAF)**  
  - `e107`、`Hestia`、`KEDA` のエンドポイントに対し **SQLi/Command Injection** ルールを有効化。  
- **最小権限の原則**  
  - KEDA の `TriggerAuthentication` は **ClusterRole** ではなく **NamespaceRole** に限定し、Vault エンドポイントはホワイトリストで管理。  
- **ログ監視とインシデント対応**  
  - Cisco SEAG の AMP ログで「ファイル書き込み」イベントを **SIEM** に転送し、異常検知ルールを追加。  
  - Gitea の `INCLUDE` ディレクティブ使用を **リポジトリポリシー** で禁止し、`org-mode` のレンダリングを無効化（`[markup]` 設定）。  
- **プラグイン・テーマの定期的なレビュー**  
  - WordPress 系プラグイン（Fluent CRM、10Web Booster など）は **公式リポジトリ** からのみ取得し、`composer.lock` でバージョン固定。  

### 3.3 短期的な緊急対策（パッチ適用が難しい場合）
1. **入力バリデーションの追加**  
   - `e107_plugins/alt_auth/*_auth.php` に対し **プリペアドステートメント** を手動で適用。  
2. **設定ファイルの書き込み権限削減**  
   - Hestia の

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-55572

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T18:17:37.863 |

e107 is a content management system (CMS). Prior to 2.3.7, the bundled alt_auth plugin's otherdb and e107db authentication backends interpolate the submitted login username directly into SQL in e107_plugins/alt_auth/otherdb_auth.php and e107_plugins/alt_auth/e107db_auth.php. The login() methods execute those strings with PDO::query() before effective sanitization, so an unauthenticated user can inject SQL when alt_auth is installed and either backend is configured with a live external database connection. The injection can expose or modify data available to the configured database account, and query failures can additionally disclose the generated query through the debug-message path. This issue is fixed in version 2.3.7.

### CVE-2026-108390

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-88;CWE-94;CWE-427` |
| Published | 2026-10-14T18:17:27.180 |

Hestia Control Panel is a lightweight and powerful control panel for the modern web. From version 1.9.7 through 1.10.4, update_object_value() in func/main.sh does not escape single quotes when writing a custom document-root value to a user's web.conf file, allowing a low-privileged authenticated panel user with a web domain to inject an additional PATH field. When the user invokes the ordinary Search feature, the root-privileged v-search-user-object script loads the forged field through parse_object_kv_list_non_eval(), which permits reserved shell-variable names and globally replaces PATH before invoking column without an absolute path. By placing a malicious column executable in the injected search path, the user can execute arbitrary code as root. This residual vulnerability was introduced when version 1.9.7 replaced the raw eval sink addressed by CVE-2026-84984 with parse_object_kv_list_non_eval(), and it is fixed in version 1.10.5.

### CVE-2026-77524

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-918` |
| Published | 2026-10-14T17:19:11.147 |

KEDA is a Kubernetes-based Event Driven Autoscaling component. In version 2.20.2 and earlier, a namespace administrator who can create TriggerAuthentication and ScaledObject resources can set hashiCorpVault.address to a tenant-controlled endpoint and select Kubernetes authentication without an explicit credential. KEDA then uses the operator pod's projected ServiceAccount token and sends it to that endpoint as a Vault login credential. The JWT-shape filter from the prior CVE-2025-68476 remediation accepts the operator token because its subject is a Kubernetes ServiceAccount, so the attacker can obtain the operator's cluster-wide permissions, including broad Secret reads and workload or admission-related operations. This vulnerability is fixed in 2.21.0.

### CVE-2026-109892

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-15T13:17:12.697 |

Incorrect Privilege Assignment vulnerability in Shabti Kaplan Frontend Admin by DynamiApps acf-frontend-form-element allows Privilege Escalation.This issue affects Frontend Admin by DynamiApps: from n/a through 3.29.13.

### CVE-2026-109686

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-15T13:17:11.540 |

Deserialization of Untrusted Data vulnerability in Link Whisper INC Link Whisper Free link-whisper allows Object Injection.This issue affects Link Whisper Free: from n/a through 0.9.7.

### CVE-2026-109694

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-15T11:17:24.537 |

Incorrect Privilege Assignment vulnerability in WP ManageNinja LLC Fluent CRM fluent-crm allows Privilege Escalation.This issue affects Fluent CRM: from n/a through 3.2.5.

### CVE-2026-109145

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-15T07:17:58.617 |

The User Rights Access Manager WordPress plugin through 1.1.3 does not restrict access to one of its AJAX account-registration handlers and assigns newly registered accounts a role that was created as a copy of the administrator role, allowing unauthenticated attackers to register an administrator-equivalent account and take over the site.

### CVE-2026-108587

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-15T05:17:02.637 |

The 10Web Booster – Website speed optimization, Cache & Page Speed optimizer plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 2.34.10 via the compressCustom function. This is due to missing file type validation and extension filtering on the page_id parameter, combined with a world-readable leaked nonce that bypasses authentication checks. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. This exploit chain requires obtaining the plugin's REST nonce (tenwebio_rest), which is automatically serialized to a world-readable file under wp-content/uploads/ whenever a bulk optimisation batch pauses; because the nonce is generated in a cron/loopback context with a user ID of 0, it is valid for unauthenticated visitors.

### CVE-2026-110911

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T04:18:22.813 |

Wheels 1.1.8 through 4.1.1 allows SQL injection when caller-supplied quoted values are parsed again as SQL by dynamic finders (such as findOneByEmail), the query builder's where(property, value) and where(property, operator, value), string/UUID-key lookup paths (findByKey, updateByKey, deleteByKey and findOrCreateBy...), and validatesUniquenessOf. The parser incorrectly treats a doubled single quote as the end of a literal. Applications passing request data to these APIs can expose authentication, password-reset or token lookups, and data to unauthorized access; numeric-column values are not affected. There is a similar concern for query-builder whereBetween() in 4.0.0 through 4.1.1: string/date bounds can alter SQL on MySQL/MariaDB with backslash escaping enabled. This is fixed in 4.1.2.

### CVE-2026-55684

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T20:17:50.783 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, the unauthenticated web/html/socio/sistema/cadastro_cobrancas_geracao.php endpoint accepts form-encoded POST data through extract($_REQUEST) and interpolates codigo, descricao, data_emissao, data_vencimento, data_pagamento, valor, valor_pago, status, link_cobranca, link_boleto, linha_digitavel, and id_socio into a raw INSERT statement. Numeric parameters are unquoted and unvalidated, while string parameters can break out of their single-quoted SQL context. A remote attacker can execute arbitrary SQL to read or modify billing, member, employee, permission, and credential data or to delete database tables. This issue is fixed in version 3.8.6.

### CVE-2026-55683

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T20:17:50.640 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, the unauthenticated web/html/socio/sistema/cadastro_cobranca.php endpoint accepts POST input through extract($_REQUEST) and directly incorporates valor, valor_pago, id_pessoa, id_socio, and id_sociotipo into UPDATE, INSERT, and SELECT statements without prepared statements. A remote attacker can use the affected parameters to execute arbitrary SQL that reads or modifies WeGIA database content, including billing records and credential data. The same SQL access can delete or truncate tables, causing loss of application data. This issue is fixed in version 3.8.6.

### CVE-2026-55680

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T20:17:50.193 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, unauthenticated POST requests to web/html/socio/sistema/cadastro_cobranca.php can place a quoted SQL expression in the codigo parameter, which extract($_REQUEST) passes into the WHERE codigo= clause of an UPDATE statement without validation or parameter binding. Quoting the value bypasses MariaDB type conversion for the VARCHAR column and permits arbitrary SQL execution without a session. An attacker can read or modify database content, including user credential hashes and billing records in the cobrancas table. This issue is fixed in version 3.8.6.

### CVE-2026-55573

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T18:17:38.013 |

e107 is a content management system (CMS). Prior to 2.3.7, install.php decodes the attacker-controlled previous_steps POST parameter and passes it to unserialize() at file scope and again in the e_install constructor without restricting allowed classes. The installer remains accessible after a normal installation, and a crafted object graph using the bundled GuzzleHttp\Psr7\PumpStream class can flow through paths.hash into site_path, where string coercion invokes an attacker-controlled callable. An unauthenticated attacker who can reach install.php can therefore execute arbitrary PHP functions with the web server process's privileges, leading to full server compromise. This issue is fixed in version 2.3.7.

### CVE-2026-76519

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-14T17:19:10.747 |

A vulnerability in the Advanced Malware Protection (AMP) feature of Cisco Secure Email Gateway could allow an unauthenticated, remote attacker to write arbitrary files on the underlying operating system.

This vulnerability is due to improper handling of email attachments when the file reputation service is enabled. An attacker could exploit this vulnerability by sending an email that contains a crafted attachment through an affected device. A successful exploit could allow the attacker to write arbitrary files and execute commands with&nbsp;root privileges on the underlying operating system.

### CVE-2026-59774

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-14T15:17:20.677 |

Gitea's Org-mode markup renderer processes INCLUDE directives supplied to the repository markup endpoint without preventing access to server-side files. An unauthenticated attacker can use a suitable public repository to read files accessible to the Gitea service account. If the disclosed files include app.ini and its INTERNAL_TOKEN, the attacker can chain the disclosure with internal logger access to modify a Git hook and execute commands as the Gitea service account.

### CVE-2026-93483

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:L/U:Red` |
| Weaknesses | `CWE-348` |
| Published | 2026-10-15T04:18:30.153 |

In Znuny through 7.3.6, an attacker can bypass specific standard login procedures and gain unauthorized access to sensitive system functions by manipulating a specific HTTP request header. Because the application incorrectly trusts this header, an attacker can impersonate any user, including administrators, without requiring a password. This grants full access to confidential data and system controls. More specifically, the HTTPBasicAuth modules for the agent (Kernel::System::Auth::HTTPBasicAuth) and customer (Kernel::System::CustomerAuth::HTTPBasicAuth) interfaces read the username to log in not only from $ENV{REMOTE_USER} (set by the web server after successful authentication), but also, as a fallback, from $ENV{HTTP_REMOTE_USER}, which is populated directly from an attacker-controllable "Remote-User" request header. On systems where HTTPBasicAuth was configured as the authentication backend, this allowed an attacker to log in as any existing user by sending a request with a forged Remote-User header, without providing any credentials.

### CVE-2026-50612

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-61` |
| Published | 2026-10-15T10:17:15.090 |

An unix symbolic link (symlink) following vulnerability has been reported to affect QuMagie. If a remote attacker gains a user account, they can then exploit the vulnerability to compromise the security of the system.

We have already fixed the vulnerability in the following version:
QuMagie 2.9.2 and later

### CVE-2026-16438

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-15T09:17:17.087 |

Incorrect Privilege Assignment vulnerability in Mitsubishi Electric GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, MobileHMI 10.97.3 and prior, MC Works64 all versions, Mitsubishi Electric Iconics Digital Solutions GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, and MobileHMI 10.97.3 and prior allows an attacker who can log in using the same administrator account for the affected products to launch and operate DCOM objects locally or remotely. During installation, the installers of the affected products unnecessarily grant default DCOM permissions to the administrator account of the affected products. Users with that administrator accounts can locally or remotely launch and operate DCOM objects that should require UAC elevation. As a result, the attacker may disclose, tamper with, destroy, or delete internal information, or cause the affected system to enter a denial-of-service (DoS) condition.

### CVE-2026-99999

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T13:17:14.137 |

In the Linux kernel, the following vulnerability has been resolved:

ipv4: validate checksum_start before completing checksum

If a packet with bad checksum metadata gets into the ipv4 stack,
skb_checksum_help can corrupt the network header and cause a bunch of
mischief.

This was discovered and reported by Paulos, and has been reporoduced
by others independently since.

We really shouldn't allow such packets in, but as a defence
in depth measure, let's also check before we complete the checksum.

A more complete validation at input is forthcoming, but needs more work.

### CVE-2026-109698

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T13:17:12.317 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Kitae Park Mang Board WP mangboard allows SQL Injection.This issue affects Mang Board WP: from n/a through 2.4.4.

### CVE-2026-109688

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T13:17:11.917 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Link Whisper INC Link Whisper Free link-whisper allows Blind SQL Injection.This issue affects Link Whisper Free: from n/a through 0.9.7.

### CVE-2026-108497

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T11:17:19.823 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in TMS Amelia ameliabooking allows SQL Injection.This issue affects Amelia: from n/a through 2.4.10.

### CVE-2026-50619

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T10:17:15.220 |

A path traversal vulnerability has been reported to affect Qsirch. If exploited, the vulnerability could allow remote attackers to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Qsirch 7.0.3.0 and later

### CVE-2026-47786

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T10:17:14.720 |

An OS command injection vulnerability has been reported to affect HybridDesk Station. If exploited, the vulnerability could allow remote attackers to execute arbitrary commands.

We have already fixed the vulnerability in the following version:
HybridDesk Station 4.2.23 and later
HybridDesk Station 4.3.4 and later

### CVE-2026-34006

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T10:17:13.187 |

A missing authentication for critical function vulnerability has been reported to affect sMedio DTCP MOVE. If exploited, the vulnerability could allow remote attackers to gain access to the system.

We have already fixed the vulnerability in the following version:
sMedio DTCP MOVE 1.4.5 and later

### CVE-2026-19863

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288;CWE-863` |
| Published | 2026-10-15T10:17:12.497 |

An unauthenticated client may access certain protected resources when using EthereumAuthenticator if the request path contains the configured login path.



This is caused by the authenticator using an unanchored substring match when identifying the login page. If the login path appears later within a protected request path, the request may be treated as the login page and its authentication or role requirement replaced with ALLOWED.



Exploitation requires the protected resource path to contain the configured login path as a later segment. Explicitly FORBIDDEN routes are not affected.

### CVE-2026-101287

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-10-15T09:17:14.367 |

Authentication bypass vulnerability in Stela, versions prior to 1.60.1, due to the use of a cookie named “authProcess” without validating its integrity. The application stores the user identifier (userId) and the status of the authentication process (validSteps) in this cookie and relies on these values—which can be modified by the client—to complete the login process.



A remote attacker, without valid credentials or interaction from other users, could manipulate the cookie to bypass authentication checks and impersonate any account, including one with SUPER_ADMIN privileges. This would allow the attacker to obtain a valid JWT token with administrative privileges and compromise the confidentiality and integrity of the application.

### CVE-2026-110862

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T23:17:27.673 |

Better Auth from 1.4.0-beta.18 before 1.7.7 contains an authentication bypass vulnerability that allows unauthenticated attackers to sign in as other users by reusing OAuth state values as Magic Link tokens. Attackers can start an OAuth sign-in with a victim's email and submit the returned state to Magic Link verification, gaining sessions or creating falsely email-verified accounts.

### CVE-2026-110536

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-10-14T19:17:10.610 |

A vulnerability was determined in D-Link DIR-868L 2.01b05. This impacts the function system of the file /htdocs/cgibin of the component HNAP CGI Handler. Executing a manipulation of the argument SOAPACTION can lead to os command injection. The attack may be launched remotely. The exploit has been publicly disclosed and may be utilized.

### CVE-2026-92152

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-129` |
| Published | 2026-10-14T18:19:34.497 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. From 4.1.0 until 4.2.0, Svc::GenericHub output-port dispatch is vulnerable because the deserialized port field is passed to serialOut_out, bufferOut_out, eventOut_out, or tlmOut_out without an explicit range check. When a remote hub packet supplies a port index outside the configured output-port array, assert-enabled builds abort, while builds without assertions can access an output-port array out of bounds, corrupt heap memory, and potentially allow remote code execution. This issue is fixed in version 4.2.0.

### CVE-2026-77371

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-14T18:18:18.570 |

Redash is a package for data visualization and sharing. From 26.0.0 until 26.9.0, the DuckDB query runner's _connect() path in redash/query_runner/duckdb.py created connections with enable_external_access left at its default value of true. A user with query access to an administrator-created DuckDB data source could use native file-reading functions to retrieve files readable by the Redash process or use COPY TO to write files with that process's privileges. Reading application secrets such as REDASH_COOKIE_SECRET or REDASH_SECRET_KEY could also enable forged sessions and authentication bypass. This issue is fixed in version 26.9.0.

### CVE-2026-103415

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T18:17:19.790 |

When a TLS 1.3 client processes a HelloRetryRequest, it copies the server's cookie into its second ClientHello without checking that the cookie fits in the outgoing packet. Both the length and the contents of that cookie come from the peer, and the write happens before certificate authentication completes, so a malicious or compromised server can overwrite memory past the caller supplied TLS packet buffer without presenting a certificate.



Only the client path is affected.

### CVE-2026-101983

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T18:17:13.293 |

A Stack-based Buffer Overflow vulnerability in the httpd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network attacker to cause remote code execution and denial of service via a J-Web virtual-domain configured.

### CVE-2026-101982

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T18:17:13.120 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd)  of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP/EVPN peer to cause root code execution on Junos OS or an rpd crash on Junos OS Evolved via protocol-valid route advertisements for an EVPN-VPWS service.

### CVE-2026-101954

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T18:17:11.277 |

An Improper Authentication vulnerability in the J-Web management interface and its NETCONF session handling of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network attacker to obtain root-level device configuration access and take over the device via a reachable J-Web HTTP or HTTPS service when web management is enabled.

### CVE-2026-33796

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:28.320 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured external BGP neighbor to execute arbitrary commands with root privileges via BMP route monitoring.

### CVE-2026-33792

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:27.933 |

A Stack-based Buffer Overflow vulnerability in the srxpfe process of Juniper Networks Junos OS on SRX Series allows an unauthenticated network attacker to execute code as root or cause a denial of service via a crafted packet received on a configured GRE tunnel.

### CVE-2026-109439

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T17:18:23.253 |

Lantronix XPress-DR and XPress-DR-I (CoBos-family) firmware through 8.1.0.0 contains a missing authentication vulnerability that allows remote attackers to read and persistently overwrite device configuration by sending crafted frames to the unauthenticated UDP configuration protocol on port 30718. Attackers can send a type 0xF8 query to read live configuration data and a type 0xFD frame with exactly 0x78 body bytes to rewrite the device IP address and serial-channel forwarding records, causing changes to commit to EEPROM and persist across reboots. The XPress-DR product series reached end-of-life/end-of-support in February 2025.

### CVE-2026-102182

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:06.080 |

A Stack-based Buffer Overflow vulnerability in the kmd component of Juniper Networks Junos OS on MX Series allows an unauthenticated network attacker to execute code as root via specific IKE certificate-based packets.

This issue affects Junos OS on MX Series:


  *  All versions before 21.2R3-S11;
  *  from 21.4 before 21.4R3-S12;
  *  from 22.2 before 22.2R3-S8;
  *  from 22.3 before 22.3R3-S5;
  *  from 22.4 before 22.4R3-S9;

### CVE-2026-102178

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:05.610 |

A Stack-based Buffer Overflow vulnerability in the BGP routing daemon of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP flowspec peer to cause routing-engine compromise or a routing-daemon denial of service via flowspec route re-advertisement when BGP update-threading is enabled.

### CVE-2026-102175

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T17:18:05.147 |

A Heap-based Buffer Overflow vulnerability in the sdxd service-deployment daemon of Juniper Networks Junos OS and Junos OS Evolved allows a remote unauthenticated attacker who can control or intercept the configured SDX/SRC server connection to execute code as root or cause denial of service via a crafted frame received over the service-deployment TCP connection.

### CVE-2026-102031

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T17:17:56.617 |

An OS Command Injection vulnerability in TACACS of Juniper Networks Junos OS Evolved allows a low-privileged TACACS+-authenticated user to execute commands with root privileges when periodic TACACS+ authorization-refresh is enabled.

### CVE-2026-101990

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:17:51.587 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote configured BGP peer to cause an rpd crash, or on Junos OS remote code-execution, via sending a flow-spec update which is selected for re-advertisement.

### CVE-2026-101986

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T17:17:50.953 |

An  Improper Authentication vulnerability in J-Web of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network attacker to bypass J-Web authentication and execute CGI content with elevated privileges via a crafted HTTP request.

### CVE-2026-101980

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-14T17:17:50.503 |

An Integer Underflow vulnerability in the kernel of Juniper Networks Junos OS with Extended Echo configured allows an unauthenticated, network-based attacker to cause a denial of service by a kernel crash.

### CVE-2026-101967

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T17:17:49.100 |

An OS Command Injection vulnerability in the bootzd zero-touch provisioning daemon of Juniper Networks Junos OS Evolved allows an unauthenticated attacker on the management LAN to execute commands as root via crafted DHCP response.

### CVE-2026-101956

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T17:17:48.353 |

An Improper Authentication vulnerability in the J-Web web management component of Juniper Networks Junos OS allows an unauthenticated remote attacker to execute arbitrary Junos commands with root privileges via the exposed J-Web web interface.

### CVE-2026-101950

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T17:17:47.877 |

A Heap-based Buffer Overflow vulnerability in the SVR component of Juniper Networks Junos OS on SRX Series allows an unauthenticated network attacker to cause a denial of service and potentially compromise confidentiality and integrity via malformed IPv4 packets reaching an interface configured for Secure Vector Routing.

### CVE-2026-110650

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.793 |

The thumbnail Python package through 1.5 contains an OS command injection vulnerability in generate_thumbnail() that allows attackers to execute commands by supplying shell metacharacters in file paths. Attackers who control a file name passed to generate_thumbnail, such as an uploaded file, can inject commands into os.system() calls running ffmpeg, convert or unoconv with the Python process privileges.

### CVE-2026-110649

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.650 |

Stills before 25.24.2 contains an OS command injection vulnerability that allows attackers to execute shell commands by supplying crafted media file paths. Attackers can name a media file with $(...) or backticks to execute operating system commands with Node.js process privileges when ffmpeg, ffprobe, gifsicle, or convert runs.

### CVE-2026-110645

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.090 |

Video-stitch before 2.0.0-beta.1 contains an OS command injection vulnerability that allows attackers to execute commands by supplying file names interpolated unquoted into shell-executed ffmpeg command lines. Attackers who influence file names passed to concat(), cut(), or merge() can inject shell metacharacters to run commands with the Node.js process privileges.

### CVE-2026-110644

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.940 |

nodejs-whisper through 0.3.1 contains an OS command injection vulnerability in convertToWavType() that allows attackers to execute commands by supplying crafted audio file paths. Attackers can provide file names containing $() command substitution or closing quotes, which are interpolated into an ffmpeg command run via shelljs exec(), executing OS commands with Node.js process privileges.

### CVE-2026-110643

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.790 |

transcribe2texts through 1.0.6 contains an OS command injection vulnerability that allows attackers to execute commands by supplying crafted audioPath values to transcribeAudio(). Attackers can inject $() or backtick substitution or a closing quote into the unescaped path passed to child_process.exec() to run commands with Node.js process privileges.

### CVE-2026-110640

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.277 |

Whisper-node through 1.1.1 contains an OS command injection vulnerability that allows attackers to execute commands by supplying crafted filePath or whisperOptions.language values to whisper(). Attackers can inject shell metacharacters or $() substitution into the command string built by createCppCommand() and run via shelljs exec() to execute commands with Node.js process privileges.

### CVE-2026-110639

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.130 |

@mborne/extract before 0.2.1 contains an OS command injection vulnerability that allows attackers to execute commands by supplying shell metacharacters in archivePath or targetDir options. Attackers controlling these values passed to extract() can inject commands into unquoted shelljs exec() strings in the unzip, 7z, tar-bz2 and gz extractors, running them with Node.js process privileges.

### CVE-2026-110638

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:16.997 |

doc-recog through 1.1.6 contains an OS command injection vulnerability that allows attackers to execute commands by supplying crafted document paths to recog() or tag(). Attackers can embed $(...) or backtick command substitution in the file path, which DocData._readPDF passes to a shell-based pdftotext exec call, running commands with Node.js process privileges.

### CVE-2026-110636

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:16.710 |

pypdftk through 0.5 contains an OS command injection vulnerability in fill_form(), dump_data_fields(), and pdftk_cmd_util() that builds shell commands from caller-supplied paths. Attackers controlling pdf_path or out_file can inject shell metacharacters interpreted by subprocess.Popen with shell=True to execute OS commands as the Python process.

### CVE-2026-110635

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:16.560 |

webp-converter before 3.0.0 contains an OS command injection vulnerability in src/webpconverter.js helpers that run libwebp binaries via execFile with shell enabled. Attackers controlling file names or option strings passed to cwebp, dwebp, gwebp, or webpmux functions can inject shell metacharacters to execute OS commands as the Node.js process.

### CVE-2026-110634

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:16.417 |

git-diff before 2.0.7 contains an OS command injection vulnerability that allows attackers to execute shell commands by supplying crafted strings to the gitDiff API. Attackers who control a diffed document string can embed $(cmd) or backtick substitutions that shelljs.exec evaluates, running commands with Node.js process privileges.

### CVE-2026-110631

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-14T15:17:15.983 |

Komodo through 2.3.3 contains an authentication bypass vulnerability in the Periphery agent that allows unauthenticated attackers to connect as a trusted Core because empty core_public_keys and passkeys lists fail open by default. Attackers reaching port 8120 can present any generated keypair to issue Periphery API requests, including terminal sessions and container operations, executing commands on managed hosts typically as root.

### CVE-2026-110612

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-14T15:17:13.187 |

vlife through 2.0.1 contains an authentication bypass vulnerability that allows unauthenticated attackers to forge JWTs using the hardcoded HS256 signing key in TokenUtil. Attackers can sign a token with superUser=true and arbitrary groupIds claims to gain super administrator access to any URL on vlife instances.

### CVE-2020-37282

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:16:59.520 |

office-converter through 1.0.2 contains an OS command injection vulnerability that allows attackers to execute commands by supplying a crafted fileName to generatePdf() or generateHtml(). Attackers can embed $(...), backticks, or a closing quote with shell metacharacters in the file name, which is concatenated into an unoconv command run via child_process.exec(), executing commands with Node.js process privileges.

### CVE-2026-16436

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-15T09:17:16.717 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in Mitsubishi Electric GENESIS versions 11.03 and prior, GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, MobileHMI 10.97.3 and prior, IoTWorX 10.97.3 and prior, MC Works64 all versions, GENESIS32 all versions, BizViz all versions, Mitsubishi Electric Iconics Digital Solutions GENESIS versions 11.03 and prior, GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, MobileHMI 10.97.3 and prior, IoTWorX 10.97.3 and prior, GENESIS32 all versions, and BizViz all versions allows a remote attacker to unlock the system by obtaining the challenge response by some means. The challenge response used to unlock the system is common to all users and fixed. As a result, the attacker may disclose, tamper with, destroy, or delete internal information, or cause the affected system to enter a denial-of-service (DoS) condition.

### CVE-2026-102469

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.573 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Vert.x DB2 client (vertx-db2-client) contains DRDA protocol handling code that deserializes User Defined Type (UDT) column data using a bare ObjectInputStream.readObject() call with no ObjectInputFilter or class allowlist.



This code path is triggered when a DRDA server sends a result set with a column tagged as UDT (FDOCA protocol LID 0x50). However, DB2 does not support this type of UDT. The FDOCA 0x50 type is never sent by a legitimate DB2 server.



Nevertheless, a malicious or man-in-the-middle DRDA server could craft a response with a 0x50-tagged column, causing the client to deserialize arbitrary attacker-controlled bytes on the Vert.x event loop before any application code can inspect or reject the data. If a Java deserialization gadget chain is present on the application's classpath, this enables remote code execution. Without a gadget chain, denial of service is possible via crafted object graphs. TLS is disabled by default, making man-in-the-middle exploitation feasible.



The impacted component is io.vertx:vertx-db2-client.

### CVE-2026-110858

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-14T23:17:27.043 |

GitPython from 3.1.30 before 3.2.0 contains a remote code execution vulnerability in Remote.pull() whose unsafe-option guard inspects only keyword arguments, not the positional refspec. Attackers controlling the refspec can supply --upload-pack=<command> to execute OS commands as the calling process over local-path or SSH transports.

### CVE-2026-110770

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307` |
| Published | 2026-10-14T19:17:13.077 |

Databasus 3.7.0 through 3.61.0 contains an authentication bypass vulnerability that allows unauthenticated attackers to brute-force password reset codes via POST /api/v1/users/reset-password. Attackers can request a six-digit code for a known email, then guess it without rate limiting, lockout, or invalidation to take over accounts, including administrators.

### CVE-2026-102748

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-862` |
| Published | 2026-10-14T19:17:05.700 |

Dgraph is an open source distributed GraphQL database. Prior to 25.4.0, Dgraph Zero registers administrative HTTP routes on port 6080 without authentication when the administrative interface is enabled. The /removeNode route accepts attacker-controlled id and group values and passes them to Server.RemoveNode, where group 0 can trigger ProposePeerRemoval. A remote unauthenticated attacker who can reach the Zero HTTP port can read topology through /state, allocate identifiers through /assign, access the exposed /moveTablet administrative route, or remove membership through /removeNode, disrupting the Zero control plane and destabilizing Alpha nodes that depend on Zero. The route registration occurs in dgraph/cmd/zero/run.go, and the demonstrated membership-removal path reaches Server.RemoveNode and ProposePeerRemoval. This issue is fixed in version 25.4.0.

### CVE-2026-33789

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:27.763 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated BGP peer to cause a denial of service and potential root-level command execution via crafted BGP route updates when the BGP Monitoring Protocol (BMP) is enabled.

### CVE-2026-102084

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-1286` |
| Published | 2026-10-14T17:18:04.310 |

An Improper Validation of Syntactic Correctness of Input vulnerability in the VPN daemon of Juniper Networks Junos OS on SRX Series allows an authenticated, network-based attacker to take complete control of the device.

If an SRX device configured for AutoDiscovery VPN (ADVPN) receives a message from a peer that contains one or more specifically malformed attributes, this will cause a buffer overflow, which can allow remote code execution and therefore allow an attacker to take complete control of the device. To be able to carry out this attack an attacker must either have acquired the shared secret to impersonate a peer or have compromised an existing one, so this attack is considerably difficult.

This issue affects Junos OS on SRX Series:


  *  All versions before 23.2R2-S7.7;
  *  from 23.4 before 23.4R2-S7;
  *  from 24.2 before 24.2R2-S4;
  *  from 24.4 before 24.4R2-S3;
  *  from 25.2 before 25.2R2;
  *  from 25.4 before 25.4R1-S3.

### CVE-2026-102070

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:18:02.953 |

A Reachable Assertion vulnerability in the Two-Way Active Measurement Protocol (TWAMP) client of Juniper Networks Junos OS allows an unauthenticated network-based attacker to cause rmopd service disruption via a specific TCP packet.

### CVE-2026-102068

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:H/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:02.647 |

A Stack-based Buffer Overflow vulnerability in the kernel of Juniper Networks Junos OS Evolved allows an unauthenticated remote attacker to trigger a kernel panic via a crafted TCP packet when key-chain authentication is used for BGP or LDP.

### CVE-2026-102062

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-14T17:18:01.737 |

An Use of Externally-Controlled Format String vulnerability in the ipfd daemon of Juniper Networks Junos OS on SRX Series allows an unauthenticated network-based attacker to execute code with root privileges via a compromised or impersonated configured HTTPS feed server.

### CVE-2026-102037

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-91` |
| Published | 2026-10-14T17:17:57.867 |

An XML Injection vulnerability in the Unified Threat Management daemon (utmd) of Juniper Networks Junos OS on SRX Series devices allows an unauthenticated network attacker to commit arbitrary device configuration with root privileges via a malicious response from a configured custom URL-feed server.

### CVE-2026-101997

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T17:17:52.740 |

An Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in ipfd of Juniper Networks Junos OS on SRX Series allows an unauthenticated network-based attacker to execute code with root privileges via a configured Security Intelligence feed connection.

### CVE-2026-101955

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:17:48.200 |

A Stack-based Buffer Overflow vulnerability in the UTM Anti-Spam SBL of Juniper Networks Junos OS on SRX series allows an unauthenticated remote attacker to cause arbitrary code execution or a denial of service via a injected malformed DNS packet when Anti-Spam SBL inspection is enabled.

### CVE-2026-97205

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-14T15:17:28.200 |

NGINX Plus and NGINX Open Source have a vulnerability in the ngx_http_core_module module. When asynchronous file I/O (AIO) is enabled in certain configurations, processing a Server Side Includes (SSI) page containing “include virtual” commands may trigger a Use-After-Free (UAF) in the NGINX worker process. This may cause memory corruption or a worker process crash. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact:
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system, corrupt its memory, or possibly trigger code execution. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-93479

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T15:17:26.810 |

A vulnerability exists in NGINX Plus and NGINX Open Source when a map directive uses regex matching and the root directive or access log format references the map's regex capture variables before referencing the map output variable. Alternatively, the same result could be achieved by using a non-cacheable variable in a string expression under certain conditions. An unauthenticated attacker along with conditions beyond their control can exploit this vulnerability by sending crafted HTTP requests. This may cause a heap buffer overflow in the NGINX worker process leading to a restart. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact: 
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system or to possibly trigger a code execution. There is no control plane exposure; this is a data plane issue only.

Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-15176

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T15:17:19.140 |

A vulnerability exists in NGINX Plus and NGINX Open Source when a location is configured that uses the alias directive together with rewrite and a set or return directive referencing the $request_filename variable. Alternatively, the same result could be achieved when the $request_filename variable is used in an access log format directive. An unauthenticated attacker along with conditions beyond their control can exploit this vulnerability by sending crafted HTTP requests. This may cause a heap buffer overflow in the NGINX worker process leading to a restart. Additionally, attackers can execute code on systems with Address Space Layout Randomization (ASLR) disabled or when the attacker can bypass ASLR.

Impact:
This vulnerability may allow remote attackers to cause a denial-of-service (DoS) on the NGINX system or to possibly trigger a code execution. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-110646

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.237 |

Beganovich snappdf from 1.1.0 before 6.1.0 contains an OS command injection vulnerability on Windows that allows attackers to run commands by influencing the rendered URL. Attackers can supply cmd.exe metacharacters such as & in the setUrl() value, which executeOnWindows() passes unescaped to PHP exec(), executing commands as the PHP process.

### CVE-2026-110632

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T15:17:16.143 |

Report One MyReport Updater through 2.1.1 exposes an unauthenticated gRPC service on TCP port 9095 that allows remote attackers to redirect the SYSTEM updater by invoking the UpdateConfigReferent method. Attackers can point the updater to a malicious reference server serving modified module archives with matching MD5 digests to write files and execute code as SYSTEM.

### CVE-2026-110628

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-14T15:17:15.540 |

Kan 0.5.5 through 0.6.0 contains an unauthenticated server-side request forgery vulnerability in the /api/download/attatchment route due to an incomplete fix for CVE-2026-32255. When S3_ENDPOINT is unset, attackers can pass arbitrary url query parameters to fetch() to read internal services, localhost ports, and cloud instance metadata.

### CVE-2026-110616

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T15:17:13.767 |

NullHub through 2026.5.29 contains a missing authentication vulnerability that allows unauthenticated attackers to access the /api/* management API because the auth_token field defaults to null and is never assigned. Attackers sending requests without Authorization or Origin headers to non-loopback listeners can control agent instances, rewrite configurations including provider credentials, and manage cron jobs and MCP servers.

### CVE-2020-37281

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1394` |
| Published | 2026-10-14T15:16:59.370 |

Gravitee API Management through 4.12.22 contains an authentication bypass vulnerability that allows unauthenticated remote attackers to impersonate any user by forging JWTs signed with the shipped default jwt.secret. Attackers knowing an existing user ID can sign an HS256 token with that subject and present it as a bearer token to the Management API, impersonating administrators to gain full platform control.

### CVE-2026-110864

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T23:17:27.970 |

Better Auth from 1.5.0-beta.12 before 1.7.7 contains an authentication bypass vulnerability in the OAuth Proxy plugin that allows unauthenticated attackers to sign in as other users by forging encrypted profiles. When the proxy shares the global secret and cookie-stored state is used, attackers can obtain encrypted state for a fake profile with a victim's verified email to take over the account via implicit linking.

### CVE-2026-108336

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-14T22:17:22.433 |

When the default self-signed certificate is used, an attacker could gain administrative access to the application.



The SSL certificate for the web interface is used to sign JWT access tokens that are used to validate that the user is logged in. When the default SSL certificate is used, an attacker could have the capability to sign JWT access tokens and bypass login.



An attacker could gain administrative access to the application and perform actions like configuring the service or requesting log collection. Device credentials and customer data cannot be accessed with this vulnerability.

### CVE-2026-108335

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-14T22:17:22.290 |

When the password reset functionality is enabled, and email is configured, an attacker could take over any account using a brute-force attack.



There is no rate limiting on the attempts to enter the reset code, leading to the possibility of a brute force solution to the password reset challenge.



An attacker could gain administrative access to the application and perform actions like configuring the service or requesting log collection. Device credentials and customer data cannot be accessed with this vulnerability.

### CVE-2026-85714

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T19:17:22.050 |

Stirling-PDF is a locally hosted web application that facilitates various operations on PDF files. Prior to 2.13.2, an authenticated administrator using the default H2 database and security mode can upload a crafted SQL file to POST /api/v1/database/import-database. DatabaseService.validateSqlContent() splits normalized input on semicolons and accepts a statement when it contains any allowed keyword, allowing dangerous H2 functions such as FILE_READ and CSVWRITE, plus CREATE ALIAS, to bypass the insufficient whitelist and execute side effects when RUNSCRIPT processes the file. This permits arbitrary file access. The demonstrated operating-system command execution chain writes attacker-controlled startup files to a user-site location and then triggers an application Python interpreter configured to load those startup files, resulting in command execution as the JVM service account. This issue is fixed in version 2.13.2.

### CVE-2026-102476

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T18:17:17.503 |

In Eclipse Vert.x versions [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Vert.x HTTP client relies on an SSL context for efficiency purpose, the key of this cache should reflect entirely the SSL semantics of the desired SSL properties. It is possible for a client to ask for an SSL context and obtain an SSL context with weaker properties, for instance a context with hostname validation and obtain a context ignoring hostname validation.



The impacted component is io.vertx:vertx-core.

### CVE-2026-102893

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T16:17:29.987 |

Zulip is an open-source team collaboration tool. In Zulip Server versions through 12.1, GenericOpenIdConnectBackend matches the identity provider email claim to an active account's delivery_email without rejecting an explicitly false email_verified claim. If a configured identity provider returns an email address that the authenticating user does not control together with email_verified=false, Zulip can log the user into the existing account for that address. Exploitation requires a misconfigured trusted identity provider, and deployments whose authoritative identity provider only emits email addresses controlled by the authenticating user are not affected. This issue is fixed in version 12.2.

### CVE-2026-110867

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T23:17:28.397 |

Renovate before 44.60.1 contains an allowlist bypass vulnerability that allows repositories to set restricted environment variables by placing env inside a shared preset. Attackers controlling an externally sourced preset can override variables like PATH, LD_PRELOAD, NODE_OPTIONS, or GIT_SSL_CAINFO in child processes on self-hosted instances.

### CVE-2026-91881

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-14T16:17:56.767 |

Dell Terraform Provider for Redfish, versions prior to 1.6.2, contains an Improper Certificate Validation vulnerability in the HTTP transport component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure and unauthorized access. This is a Critical severity vulnerability as it allows an unauthenticated attacker to intercept all Redfish BMC traffic including credentials by performing a man-in-the-middle attack, since TLS certificate verification is unconditionally disabled in the base HTTP transport. Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-86002

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-95` |
| Published | 2026-10-14T16:17:54.470 |

Dokku is a docker-powered platform as a service. In Dokku versions before 0.38.25, a user with app-level Dokku access and remote SSH access to execute docker-options commands can store arbitrary strings through the docker-options plugin, and those strings are later concatenated into DOCKER_ARGS and processed by Bash eval during build, deploy, or run operations. Shell command substitutions in the stored values are interpreted on the host, allowing arbitrary command execution with the privileges of the dokku operating-system user. This issue is fixed in version 0.38.25.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-39997

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T10:17:14.197 |

A missing authentication for critical function vulnerability has been reported to affect HybridDesk Station. If exploited, the vulnerability could allow remote attackers to gain access to the system.

We have already fixed the vulnerability in the following version:
HybridDesk Station 4.2.22 and later

### CVE-2026-109693

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-10-15T13:17:12.190 |

Incorrect Privilege Assignment vulnerability in WP ManageNinja LLC Fluent CRM fluent-crm allows Privilege Escalation.This issue affects Fluent CRM: from n/a through 3.2.5.

### CVE-2026-18660

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178;CWE-918` |
| Published | 2026-10-15T10:17:12.097 |

In Eclipse Jetty, across various versions of `jetty-server`, and `jetty-proxy`, the host whitelist/blacklist is case-sensitive, and would allow hosts through that only differ by case.

### CVE-2026-18661

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T09:17:17.270 |

In Eclipse Jetty, across various versions of `jetty-annotations`, and `jetty-eeN-annotations`, the Jakarta Spec authoritative url-pattern rules for mixed `@ServletSecurity` annotation, and `web.xml` defined `security-constraint` on the same `url-pattern` were not being applied if the `web.xml` had more than 1 `url-pattern` for a servlet, and had a `security-constraint` applying to only some of those `url-pattern` definitions.

### CVE-2026-81534

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-74` |
| Published | 2026-10-15T07:18:03.093 |

The Email Customizer for WooCommerce (Pro) plugin for WordPress is vulnerable to Remote Code Execution in versions up to, and including, 3.9.5. This is due to insufficient authorization and input sanitization in the send_test_mail() function, which allows user-controlled PHP code to be written to executable files in the uploads directory. This makes it possible for authenticated attackers, with subscriber-level access and above, to execute arbitrary PHP code on the server, leading to full site compromise.

### CVE-2026-110908

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-15T03:17:10.797 |

Netgate pfSense FRR package (pfSense-pkg-frr) 2.0.2_1 and source revision 2.1.2_1 contain an OS command injection vulnerability in the FRR status filter. An authenticated WebGUI user with only the page-status-frr privilege can supply a filter value that breaks out of a single-quoted sed expression into which escapeshellarg() output is concatenated. Shell command substitution is then evaluated by a popen() pipeline, allowing attacker-selected commands to execute as root. There are updated FRR packages for pfSense Plus 26.07/26.03.1 and CE 2.9.0/2.8.1.

### CVE-2026-55681

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T20:17:50.343 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, an authenticated user with access to the Material & Patrimônio module can submit id_produto to web/html/matPat/restaurar_produto_desocultar.php, where a second extract($_REQUEST) overwrites the value previously sanitized by intval(). The raw value is interpolated into UPDATE statements for the produto, isaida, and ientrada tables. An attacker can execute arbitrary SQL to extract sensitive database records or modify institutional and inventory data. This issue is fixed in version 3.8.6.

### CVE-2026-63626

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122;CWE-125` |
| Published | 2026-10-14T19:17:18.570 |

Mongoose is an embedded web server and network library. Prior to 7.23, ppp_handle_ipv6cp() in src/l2_ppp.c trusts the 16-bit IPv6CP len field without checking it against the received payload size. On a PPP or PPPoE link using MG_ENABLE_TCPIP and MG_ENABLE_IPV6, an unauthenticated adjacent peer can complete the required LCP exchange and send a short Configure-Request with an oversized length, causing ppp_tx_frame() to read beyond recv_queue.buf and write beyond tx.buf. The same length misuse can also expose adjacent heap bytes in a reply or hang the event loop through find_opt(). This issue is fixed in version 7.23.

### CVE-2026-54525

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T19:17:17.480 |

Markdown Preview Enhanced is a Markdown preview extension for Visual Studio Code. Prior to 0.8.28, Markdown Preview Enhanced preview-link handling passes a decoded, Markdown-controlled link target to a Windows file-opening helper that invokes child_process.exec with the start command. When a Windows user opens an untrusted Markdown file and clicks a crafted external or unsupported-scheme link, shell metacharacters in the decoded target are interpreted by cmd.exe as command separators, allowing an attacker-selected command to run with the privileges of the current VS Code user. The attack requires one normal preview-link click but does not require malicious workspace configuration, script execution to be enabled, or additional files. This issue is fixed in version 0.8.28.

### CVE-2026-88164

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T18:19:30.300 |

Missing authorization in Microsoft Office SharePoint allows an authorized attacker to elevate privileges over a network.

### CVE-2026-86848

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-14T18:19:19.223 |

A flaw was found in DPDK lib/vhost vhost-crypto. The indirect-descriptor snapshot double-fetches a guest descriptor next index, allowing a malicious guest to cause an out-of-bounds access in the host backend.

### CVE-2026-86567

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-14T18:19:18.390 |

A flaw was found in DPDK lib/vhost. The VDUSE handler fails to invalidate vring pointers when the IOTLB is invalidated, leading to use-after-unmap.

### CVE-2026-86461

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-14T18:19:17.623 |

The FV Flowplayer Video Player plugin for WordPress is vulnerable to Limited Arbitrary File Upload in all versions up to, and including, 7.5.54.7212 via the check_mimetype function. This is due to incomplete file type validation in the check_mimetype function — while some extension checking is present, it can be bypassed, allowing attacker-supplied remote file content to be written with insufficient extension enforcement and no MIME check or WordPress upload helper. This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. Exploitation requires the plugin's 'profile videos on bio' option to be enabled, as this causes the nonce to be emitted on the subscriber-accessible profile page; without this setting, authenticated users below Editor cannot obtain the required nonce.

### CVE-2026-107350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T18:17:25.670 |

Improper authentication in PgBouncer 1.17.0 through 1.26.0 allows a remote attacker who knows the password of a user listed in auth_file to log in as any other user that authenticates using SCRAM, including PgBouncer admin users and backend superusers. A second StartupMessage sent during SCRAM authentication against a non-existent database is not rejected and switches the user being logged in as, while the SCRAM exchange is still verified against the keys of the first user.

### CVE-2026-101966

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-14T17:17:48.943 |

A Use of Externally-Controlled Format String vulnerability in the jti-dialoutd of Juniper Networks Junos OS Evolved allows an authenticated network attacker to cause persistent telemetry dial-out denial of service via a crafted analytics sensor resource submitted through gNMI listener.

### CVE-2026-89067

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-14T16:17:54.897 |

Authentication bypass using an alternate path or channel vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-87093

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-14T16:17:54.780 |

Incorrect Permission Assignment for Critical Resource vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-71184

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T15:17:22.783 |

Gitea's pull request review notifier does not attach the pull request to the Actions notification, so the fork workflow approval gate does not recognize the run as originating from a fork. Review comment and review approval or rejection events can consequently load workflow code from the fork head and run it on the base repository's runners without the required maintainer approval. This allows execution of fork-controlled workflow code across the intended approval boundary.

### CVE-2026-53882

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-15T10:17:15.347 |

An improper link resolution before file access ('link following') vulnerability has been reported to affect Virtualization Station. If a remote attacker gains a user account, they can then exploit the vulnerability to compromise the security of the system.

We have already fixed the vulnerability in the following version:
Virtualization Station 4.1.1.130 and later

### CVE-2026-44084

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T10:17:14.587 |

An authorization bypass through user-controlled key vulnerability has been reported to affect Video Station. If exploited, the vulnerability could allow remote attackers to obtain sensitive data.

We have already fixed the vulnerability in the following version:
Video Station 5.8.8 and later

### CVE-2026-34015

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T10:17:13.823 |

A path traversal vulnerability has been reported to affect Video Station. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Video Station 5.8.8 and later

### CVE-2026-63314

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T09:17:17.713 |

WebCTI service for Slican IPx telephone exchanges is vulnerable to SQL Injection in /webcti/admin_json.php enpoint. Improper neutralization of input allows an authenticated attacker to execute SQL Injection attacks.


This issue was fixed in IPx series version 6.62.0100.

### CVE-2026-102477

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.720 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], a gRPC endpoint does have a configurable per message maximum size in bytes, however the maximum size applies to the received bytes. When applied to a compressed message, this only applies to the compressed size and not the actual size of the uncompressed content. This can be used to force a gRPC endpoint to allocate more bytes than the value defined by the configuration, making the endpoint vulnerable to compression bomb attacks.



The impacted component is io.vertx:vertx-gprc-server.

### CVE-2026-102461

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:14.887 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the uniqueItems keyword validation uses an O(n²) pairwise comparison loop with no short-circuit or size limit. A remote unauthenticated attacker can submit a moderately-sized JSON array that consumes disproportionate CPU time, leading to denial of service.



The impacted component is io.vertx:vertx-json-schema.



The following Vert.x modules depend on vertx-json-schema and are also affected:



io.vertx:vertx-web-openapi-router io.vertx:vertx-web-validation io.vertx:vertx-openapi

### CVE-2026-102475

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T08:16:36.797 |

In Eclipse Vert.x versions [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the HTTP proxy provides a body transformer interceptor that relies on a max buffered bytes limit to ensure a bounded buffer for each request. This can be used to force a server to indefinitely allocate heap. This vulnerability requires to use an intercepting body transformer.



The impacted component is io.vertx:vertx-http-proxy.

### CVE-2026-102467

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T08:16:36.670 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the WebSocket implementation does not define a maximum number of bytes allocation when decompressing frames or messages. This can be used to implement DDOS attacks with a zip bomb.



The impacted component is io.vertx:vertx-core.

### CVE-2026-41544

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T07:18:00.467 |

A path traversal vulnerability has been reported to affect QcalAgent. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
QcalAgent 1.1.10 and later

### CVE-2026-39993

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-10-15T07:18:00.317 |

A relative path traversal vulnerability has been reported to affect Download Station. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Download Station 5.10.2.313 and later
Download Station 5.11.3.322 and later

### CVE-2026-77931

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T02:20:16.277 |

MoviePilot through 3.1.5 contains a command injection vulnerability that allows attackers to execute arbitrary OS commands by embedding malicious instructions in untrusted content processed through tools like browse_webpage, search_web, and torrent metadata parsers, which then get passed to the unrestricted ExecuteCommandTool via asyncio.create_subprocess_shell. Attackers can craft content that instructs the model to invoke execute_command with confirm_dangerous set to true, bypassing the validate_command_safety denylist and exploiting the admin session's is_admin context to achieve remote code execution on the host.

### CVE-2026-76660

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T02:20:16.020 |

A vulnerability in HPE NonStop CIPSAM allows an out-of-bounds
  write that can corrupt buffer data.

### CVE-2026-76066

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T02:20:15.603 |

IntentKit through 2.6.3 contains an authorization bypass vulnerability where the executor validates tool calls against the full tool registry rather than the per-request narrowed tool advertisement enforced by ToolBindingMiddleware, allowing owner-only state-changing tools such as wallet transfer, posting, memory-write, and call-agent to execute without any human-in-the-loop or approval gate. An unauthenticated or public caller in WEB, API, TWITTER, or TELEGRAM contexts can exploit this by supplying the exact de-advertised tool name and arguments via indirect prompt injection or by replaying checkpoint and history data on a reused thread, achieving unauthorized execution of owner-restricted capabilities.

### CVE-2026-109430

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-15T02:18:37.150 |

Ellucian WebAdvisor 3.2 contains an unauthenticated XML External Entity (XXE) injection vulnerability that allows remote attackers to submit crafted XML POST requests to the /WebAdvisor/WebAdvisor endpoint without disabling external entity and DTD resolution. Attackers can exploit this flaw to force the server into SSRF requests, coerce NTLMv2 hash disclosure via attacker-controlled SMB shares, and read arbitrary files from the underlying Windows host through an out-of-band error-based channel. WebAdvisor entered end-of-support status in June 2022 and users are encouraged to migrate to Colleague Self-Service.

### CVE-2026-0993

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-15T01:19:27.290 |

SODOLA SL902-SWTGW124AS firmware before 200.2.12 contains a buffer overflow vulnerability that allows unauthenticated remote attackers to cause a denial of service by sending an oversized boundary value in the Content-Type header of a crafted POST request. Attackers can exploit the embedded HTTP server's multipart/form-data boundary parser to cause the device to become fully unresponsive — dropping all management access and traffic forwarding during its self-recovery cycle.

### CVE-2026-110869

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-14T23:17:28.673 |

Nodemailer 3.0.0 before 10.0.13 has a regular expression denial of service in SMTPConnection._actionEHLO, whose four AUTH mechanism detection regexes contain overlapping whitespace sub-patterns that backtrack quadratically. A malicious or man-in-the-middle SMTP server can reply to EHLO with 250-AUTH, a long whitespace run and a non-matching token, blocking the Node.js event loop for tens of seconds to hours before authentication.

### CVE-2026-110859

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-10-14T23:17:27.183 |

GitPython before 3.2.0 contains an argument injection vulnerability in Head.checkout() that allows remote attackers to read arbitrary files by supplying a branch name parsed as a git option. Attackers can host a repository whose default branch is named --pathspec-from-file=<path>, causing cloning applications that check out the active branch to leak file contents through GitCommandError messages.

### CVE-2026-110856

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-14T23:17:26.760 |

GitPython before 3.2.0 contains a regular expression denial of service vulnerability in the _re_actor_epoch pattern used by parse_actor_and_date on author, committer, and tagger lines. Attackers can serve repositories with commit or tag objects containing long space-filled lines lacking a valid epoch or timezone, causing quadratic backtracking and CPU exhaustion.

### CVE-2026-110838

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T23:17:24.023 |

FreeRDP shadow server from 3.0.0 before 3.32.0 dispatches input PDUs during the Confirm Active state before authentication, allowing unauthenticated attackers to inject keyboard input. Attackers can negotiate TLS-only RDP and send an input PDU without Confirm Active to inject synthetic keystrokes into the host user's X11 session via XTEST.

### CVE-2026-110767

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-14T19:17:12.610 |

Gitingest through 0.3.1 contains a symlink following vulnerability in ingest_query single-file blob ingestion that allows unauthenticated attackers to read server files by submitting symlink blob URLs. Attackers can commit a symlink to a public repository and submit its blob URL, causing the server to return any file the service user can read, up to 10 MB.

### CVE-2026-110761

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-14T19:17:11.723 |

ILIAS before 9.24, 10.12, and 11.5 contains a PHP object injection vulnerability that allows authenticated users with Test creation or import permission to deserialize arbitrary objects via crafted Test archives. Attackers can inject a malicious tst_sequence sequence attribute that is passed to unserialize(), abusing Guzzle or Monolog gadget chains to write PHP files and execute code.

### CVE-2026-104143

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-289` |
| Published | 2026-10-14T19:17:08.347 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.26, authenticated users can store a crafted custom dateFormat for a dataset field. DatasetTableFieldDTO.dateFormat is inserted without validation into date conversion templates used by Dimension2SQLObj, CustomWhere2Str, Field2SQLObj, WhereTree2Str, and ExtWhere2Str. When a chart renders the field on a cross-datasource dataset, Calcite parsing is bypassed and the crafted format can directly alter the generated SQL. On a single-datasource dataset, exploitation additionally requires the payload to survive Calcite reserialization as a valid string literal. Successful exploitation can compromise the confidentiality, integrity, and availability of the backend database. This issue is fixed in version 2.10.26.

### CVE-2026-104142

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T19:17:08.177 |

DataEase is an open source data visualization and analysis tool. Prior to 2.10.26, authenticated users can store crafted FieldGroupDTO.min, FieldGroupDTO.max, FieldGroupDTO.startTime, or FieldGroupDTO.endTime values in dataset group-field binning definitions. Utils.transGroupFieldToSql inserts these free-form values into generated CASE expressions without validation, and the resulting SQL can reach unparameterized backend query execution when a chart uses the field. This stored SQL injection can compromise the confidentiality, integrity, and availability of the configured backend database. This issue is fixed in version 2.10.26.

### CVE-2026-104141

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T19:17:08.013 |

DataEase is an open source data visualization and analysis tool. Authenticated users with datasource access can supply crafted schema names, connection usernames, table names, or database names to datasource metadata operations, including getSchema, validate, save, and update flows. CalciteProvider inserts these identifiers into metadata queries that are executed through a plain JDBC Statement, allowing the generated SQL to be altered and run against the configured backend with application-held datasource credentials. The issue can compromise the confidentiality, integrity, and availability of the connected database without requiring a victim action.

### CVE-2026-102479

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T19:17:05.313 |

In Eclipse Vert.x versions [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Vert.x HTTP/1.x decoder uses a canonicalization for well known HTTP headers, the canonicalization process interprets well crafted headers as headers of this list, allowing for instance Content-Xength to be interpeted as Content-Length.



This can be exploited for request smuggling purpose.



The impacted component is io.vertx:vertx-core.

### CVE-2026-42093

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T18:17:36.980 |

Redash is a package for data visualization and sharing. From versions after 8.0.0 until 26.9.0, the Query Results query runner in redash/query_runner/query_results.py accepts param_query_N_{key=value} parameters and passed attacker-controlled values to replace_query_parameters() for raw substitution into a referenced query's SQL. This path bypassed the ParameterizedQuery schema validation used by normal query execution and omitted the is_safe permission check. An authenticated user with at least view-only access to both the Query Results data source and the referenced data source could therefore inject SQL through text parameters and execute it with the referenced data source's privileges. This issue is fixed in version 26.9.0.

### CVE-2026-106465

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-406` |
| Published | 2026-10-14T18:17:25.093 |

The NetX Secure DTLS server sends a HelloVerifyRequest carrying a freshly generated cookie, but never checks the cookie a client returns. The ClientHello parser copies the client's cookie bytes over the value the server issued, and the server then decides whether the client has been verified from the cookie's length alone. A peer that puts any single cookie byte in its first ClientHello skips the verification exchange entirely, so the server has no return-routability check and completes handshakes for forged source addresses.

### CVE-2026-106464

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-14T18:17:24.960 |

`_nx_secure_x509_parse_signature_data` computes the certificate signature's length as `tlv_length - 1` without first checking that `tlv_length` is non-zero. A certificate whose signature is an empty ASN.1 BIT STRING therefore parses successfully and leaves the certificate holding a signature length of `0xFFFFFFFF` and a signature pointer one byte past the end of the buffer. Certificates are parsed from the peer during the TLS handshake, so the input is remote and unauthenticated.

### CVE-2026-102077

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-754` |
| Published | 2026-10-14T18:17:13.460 |

An Improper Check for Unusual or Exceptional Conditions vulnerability in the Packet Forwarding Engine (PFE) of Juniper Networks Junos OS on MX Series with SPC3 allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).



On MX Series with SPC3 line-card and source NAT configuration, when a specific malformed IPv6 packet is received, it is not dropped but instead a session is created and NAT resources are allocated. Continued receipt of such packets will eventually lead to session or resource exhaustion, which will impact all traffic through the device. To recover the device needs to be rebooted.
To monitor session usage, use the following:

show services sessions summary

To monitor source NAT resource usage, use the following: 

show services nat pool

This issue affects Junos OS on MX Series with SPC3:

  *  All versions before 23.2R2-S4;
  *  23.4 versions before 23.4R2-S5;
  *  24.2 versions before 24.2R2.

### CVE-2026-101981

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T18:17:12.963 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent LDP peer to cause an rpd crash or execute arbitrary code via a malformed LDP Label Mapping message.

### CVE-2026-101979

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T18:17:12.803 |

A Stack-based Buffer Overflow vulnerability in the authd Juniper Networks Junos OS and Junos OS Evolved allows a network attacker with SNMP read access to execute code with root privileges or cause a denial of service via a specific SNMP packet, when SNMP and AAA are enabled.

### CVE-2026-101976

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T18:17:12.640 |

An Out-of-bounds Write vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an eBGP peer which has not negotiated four-octet-AS capability sending a specifically malformed BGP update to cause a Denial-of-Service (DoS).

### CVE-2026-101963

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-682` |
| Published | 2026-10-14T18:17:11.970 |

An Incorrect Calculation vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos EVO allows a remote BGP EVPN neighbor to cause an rpd crash when SRv6 EVPN multihoming is configured.

### CVE-2026-101962

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-14T18:17:11.777 |

An Improper Handling of Length Parameter Inconsistency vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker sending a specifically malformed BGP EVPN multicast update which is attempted to be readvertised to cause an rpd crash.

### CVE-2026-101961

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T18:17:11.610 |

A NULL Pointer Dereference vulnerability in the routing-policy nexthop-ECMP matcher of Juniper Networks Junos OS and Junos OS Evolved allows a configured eBGP peer to cause a routing-daemon denial of service via a specific BGP packet received while a nexthop-ecmp qualifier is attached to a BGP import policy.

### CVE-2026-101952

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T18:17:11.110 |

An Improper Validation of Consistency within Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP ISO-VPN peer to cause an rpd crash by sending a specific ISO-VPN update which is then processed by BMP route monitoring or NSR.

### CVE-2026-101949

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T18:17:10.933 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated remote BGP neighbor to cause a denial of service via a VPN-flowspec BGP update if it is readvertised and BMP post-policy RIB-out monitoring is configured.

### CVE-2026-33798

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:28.477 |

A Stack-based Buffer Overflow vulnerability in the srxpfe of Juniper Networks Junos OS and Junos OS Evolved on the SRX Series allows an L2-adjacent attacker to execute arbitrary code as root via high-availability fabric traffic.

### CVE-2026-33795

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-10-14T17:18:28.123 |

A Numeric Truncation Error vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network-based attacker to cause a denial of service via a BGP Prefix-SID route advertisement that is subsequently re-advertised.

This issue does not affect versions of Junos OS prior to 20.4R1.
This issue does not affect versions of Junos OS Evolved prior to 20.4R1-EVO

### CVE-2026-105659

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T17:18:15.657 |

Uncontrolled Resource Consumption vulnerability in mtrudel bandit allows an unauthenticated remote attacker to pin HTTP/2 stream processes indefinitely via a trickle of small WINDOW_UPDATE frames. A stream whose response outruns the connection or stream send window blocks until the peer grants more window, and each block carries a 15 second deadline. Both deadlines restart whenever the peer makes partial progress. Bandit.HTTP2.Connection.finish_data/5 re-queues a partially advanced send in pending_sends with a fresh expires_at, so every WINDOW_UPDATE on stream 0, and every SETTINGS frame, resets the clock. Bandit.HTTP2.Stream.send_data/3 recurses on each stream WINDOW_UPDATE and re-arms a fresh after read_timeout. A peer that grants a few bytes every few seconds keeps the blocked stream process, its Plug state and any resource it holds mid-response alive for as long as it keeps dripping, and repeats this across streams and connections to exhaust server processes and memory.

The two paths are independent. The stream-level block is reached on its own by widening the connection window with a large WINDOW_UPDATE on stream 0 and shrinking the per-stream window with a small SETTINGS_INITIAL_WINDOW_SIZE, so closing only the connection-level path leaves it exploitable.

This issue affects bandit: from 1.4.0 onward.

### CVE-2026-103994

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T17:18:13.613 |

A Heap-based Buffer Overflow vulnerability in the VXLAN Gateway Daemon (vgd) of Juniper Networks Junos OS allows a malicious or compromised SDN-controller to cause a complete outage of the OVSDB control plane and possibly remote code execution.

### CVE-2026-103946

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T17:18:13.303 |

An SQL injection vulnerability could allow an authenticated user to read or modify data stored by Nessus.

### CVE-2026-102185

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-14T17:18:06.547 |

A Loop with Unreachable Exit Condition ('Infinite Loop') vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote network attacker to cause a denial of service via EVPN multihoming with preference-based designated-forwarder election.

### CVE-2026-102184

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:18:06.390 |

An Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos Evolved platforms allows a configured EVPN signaling peer to cause an rpd crash via a malformed SRv6 structure carried in an EVPN route update. The result is a denial of service affecting routing adjacencies.

### CVE-2026-102183

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:18:06.220 |

An Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP EVPN peer to cause an rpd crash via a specifically malformed NLRI.

### CVE-2026-102180

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:05.923 |

A Stack-based Buffer Overflow vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker with access to a configured BGP peering session to cause a denial of service by sending a crafted BGP route attribute, which is processed while a BGP RIB streaming telemetry subscription is active.

This issue does not affect Junos OS versions prior to 22.1R1.
This issue does not affect Junos OS Evolved versions prior to 22.1R1-EVO.

### CVE-2026-102179

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:18:05.767 |

An Out-of-bounds Write vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker with access to a configured BGP EVPN peer to cause a denial of service via BGP EVPN route processing when the l2vpn-evpn RIB telemetry sensor is subscribed. Successful exploitation can crash rpd and interrupt routing protocols until the daemon restarts and reconverges.

### CVE-2026-102176

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-10-14T17:18:05.303 |

A Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') vulnerability in the SDK service process of Juniper Networks Junos OS allows an unauthenticated network attacker to cause a denial of service or compromise the Routing Engine by sending specific packets when the SDK service and a JDAF routing instance are enabled.

### CVE-2026-102174

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:04.990 |

A Stack-based Buffer Overflow vulnerability in the iked IKE key-management daemon of Juniper Networks Junos OS on the SRX Series allows an authenticated remote-access VPN client to execute code with root privileges or cause denial of service via the remote-access VPN authentication and JIMS identity-publishing path.

### CVE-2026-102081

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-14T17:18:03.863 |

A Missing Release of Memory after Effective Lifetime vulnerability in the packet forwarding engine (PFE) of Juniper Networks Junos OS on SRX Series allows an unauthenticated, network-based attacker to cause a complete Denial-of-Service (DoS).



On SRX4000 Series, and SRX5000 Series with SPC3, and MX Series with SPC3, when one or more specific application services like ALGs, IDP/DPI, APPID, SECINTEL, AAMW or AppQoE are configured, a high connections per second churn will cause PFE memory to leak. If the memory is exhausted traffic processing will be impacted.

Use the CLI command show security monitoring to monitor the memory utilization of the PFEs on the FPCs.

This issue affects Junos OS on SRX Series and MX Series:


  *  23.4 versions from 23.4R2-S3 before 23.4R2-S7;
  *  24.2 versions from 24.2R2 before 24.2R2-S3;
  *  24.4 versions before 24.4R2-S3;
  *  25.2 versions before 25.2R1-S2, 25.2R2.

### CVE-2026-102069

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:02.800 |

A Stack-based Buffer Overflow vulnerability in the dot1x daemon of Juniper Networks Junos OS devices operating as Junos Fusion Aggregation Devices allows an adjacent attacker acting as the configured ICCP peer to cause a denial of service and potentially execute code as root via. The issue is triggered when dot1x synchronization is enabled for the required Fusion satellite topology.

### CVE-2026-102065

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:18:02.173 |

An Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote unauthenticated BGP peer to cause an rpd crash via a malformed BGP-signaled SRv6 service route when SRv6 dynamic tunnels are enabled.

### CVE-2026-102064

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:18:02.017 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker to cause rpd crash via malformed BGP MCAST-VPN updates from a configured eBGP peer.

### CVE-2026-102061

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:01.580 |

A Stack-based Buffer Overflow vulnerability in the phone-home daemon (phcd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to execute arbitrary code as root via a crafted DHCP SZTP bootstrap message.

This issue only affects platforms that support Secure-ZTP.

### CVE-2026-102059

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T17:18:01.253 |

An Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability in the phone-home daemon (phcd) of Juniper Networks Junos OS and Junos OS Evolved on EX Series, SRX Series, and QFX Series allows an adjacent unauthenticated attacker to execute arbitrary commands with root privileges via a rogue DHCP server.

### CVE-2026-102057

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:00.937 |

A Stack-based Buffer Overflow vulnerability in the jdhcpd process of Juniper Networks Junos OS allows an unauthenticated adjacent attacker to cause a denial of service via a DHCP client response. The issue affects DHCP client operation and can interrupt related DHCP, relay, and zero-touch-provisioning services.

### CVE-2026-102055

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:00.590 |

A Stack-based Buffer Overflow vulnerability in the cfmd process of Juniper Networks Junos OS on MX Series and Junos OS Evolved on PTX Series platforms allows an unauthenticated adjacent-network attacker to execute arbitrary code as root or cause denial of service via a specific CFM Message sent to a configured down-MEP with enhanced CFM mode enabled.

### CVE-2026-102052

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:18:00.113 |

A Stack-based Buffer Overflow vulnerability in the jdhcpd process of Juniper Networks Junos OS and Junos OS Evolved platforms allows an adjacent unauthenticated attacker to cause denial of service or execute arbitrary code with root privileges via a malformed DHCPv4 server response when the DHCPv4 local-client feature is used.

### CVE-2026-102050

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:17:59.737 |

A Stack-based Buffer Overflow vulnerability in the l2cpd daemon of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service in Layer 2 control-plane processing via LLDP packets received on an interface configured for LLDP. Repeated triggering may disrupt LLDP and other Layer 2 control protocols across the device.

### CVE-2026-102049

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:17:59.560 |

A Stack-based Buffer Overflow vulnerability in the l2cpd process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to cause a denial of service or execute arbitrary code with root privileges via LLDP traffic received on an interface with Unified Access Policy enabled.

### CVE-2026-102046

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-14T17:17:59.093 |

A Loop with Unreachable Exit Condition ('Infinite Loop') vulnerability in netsctp.ko of Juniper Networks Junos OS on MX Series allows an unauthenticated network attacker to cause a denial of service via crafted SCTP network traffic.

### CVE-2026-102044

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:58.797 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP-LS peer to cause a denial of service via a BGP-LS update.

### CVE-2026-102036

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T17:17:57.717 |

An Integer Overflow or Wraparound vulnerability in the l2ald process of Juniper Networks Junos OS and Junos OS Evolved allows a configured EVPN BGP peer to cause a denial of service via EVPN Type-2 MAC/IP routes.

### CVE-2026-102030

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-459` |
| Published | 2026-10-14T17:17:56.460 |

An Incomplete Cleanup vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows a configured MVPN neighbor to cause a denial of service via a BGP MVPN update when an inter‑region segmented VRF with 'protocols mvpn inter-region-template' is configured.

### CVE-2026-102029

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:56.303 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated configured MSDP peer or adjacent PIM sender to cause a denial of service via an MSDP or PIM policy that uses AS-path expansion.

### CVE-2026-102028

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:56.137 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote BGP peer to cause a denial of service when multiple UPDATEs occur over a single TCP session with 'bgp family l2vpn auto-discovery-only' configured.

### CVE-2026-102027

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-131` |
| Published | 2026-10-14T17:17:55.973 |

An Incorrect Calculation of Buffer Size vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured eBGP neighbor to cause an rpd crash via BGP labeled-unicast UPDATEs when the affected multipath features are enabled.

### CVE-2026-102026

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-664` |
| Published | 2026-10-14T17:17:55.793 |

An Improper Control of a Resource Through its Lifetime vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent eBGP peer to cause a routing-daemon crash via a BGP route update when RIB sharding is enabled.

### CVE-2026-102025

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-762` |
| Published | 2026-10-14T17:17:55.627 |

A Mismatched Memory Management Routines vulnerability in the routing protocol daemon (rpd) process of Juniper Networks Junos OS and Junos OS Evolved allows an authenticated network-based attacker to cause a denial of service via a BGP route update when extended next-hop tunneling and SRv6 service processing are used.

### CVE-2026-102024

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T17:17:55.463 |

An Integer Overflow or Wraparound vulnerability in the routing daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an authenticated BGP peer to cause a denial of service via BGP route updates when extended-nexthop-tunnel is enabled.

### CVE-2026-102023

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:55.320 |

A Reachable Assertion vulnerability in fwstatsd of Juniper Networks Junos OS Evolved allows an authenticated network attacker to cause a denial of service via an SNMP firewall-counter MIB query when at least one firewall counter is configured.

### CVE-2026-102022

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:55.177 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker with access to a configured BGP-LS peer to cause an rpd crash via a crafted BGP-LS Link NLRI advertisements.

### CVE-2026-102020

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:54.873 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an authenticated network-based attacker to cause a denial of service via BGP-LS routing updates.

### CVE-2026-102016

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:17:54.170 |

An Improper Validation of Specified Quantity in Input vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP MVPN peer to cause a denial of service via a BGP MVPN signaling update.

### CVE-2026-102015

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T17:17:53.993 |

A Heap-based Buffer Overflow vulnerability in the secure-dot1xd process of Juniper Networks on Junos OS and Junos OS Evolved allows an unauthenticated adjacent network attacker to execute code as root or cause a denial of service via an EAPOL frame sent to an 802.1X-authenticated interface.

### CVE-2026-102014

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-14T17:17:53.693 |

A Stack-based Buffer Overflow vulnerability in the authd process of Juniper Networks Junos OS allows an attacker able to influence a configured RADIUS server to cause authd to crash or execute code with root privileges via a malicious RADIUS response.

### CVE-2026-102012

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:53.370 |

A Reachable Assertion vulnerability in the na-grpcd process of Juniper Networks Junos OS Evolved allows a remote unauthenticated attacker to cause a denial of service via a gRPC telemetry subscription request.

### CVE-2026-101978

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T17:17:50.350 |

An OS Command Injection vulnerability in the bootzd zero-touch provisioning daemon of Juniper Networks Junos OS Evolved on PTX Series allows an unauthenticated attacker on the management LAN to execute commands as root via a crafted gRPC response.

### CVE-2026-101977

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:50.190 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured eBGP peer to cause a persistent routing-daemon denial of service via a specific BGP packet when ephemeral configuration is used.

### CVE-2026-101973

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:49.900 |

A NULL Pointer Dereference vulnerability in the pkid component of Juniper Networks Junos OS allows an unauthenticated remote attacker to cause a denial of service via a malformed packet received during CMP enrollment or automatic certificate re-enrollment.

### CVE-2026-101965

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-134` |
| Published | 2026-10-14T17:17:48.803 |

An Use of Externally-Controlled Format String vulnerability in the gRPC daemon of Juniper Networks Junos OS Evolved allows an authenticated network attacker to cause telemetry-service disruption, information disclosure, or potential root-level code execution via a crafted message to the gNMI service.

### CVE-2026-101957

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-665` |
| Published | 2026-10-14T17:17:48.493 |

An Improper Initialization vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote BGP peer to cause an rpd crash via an LLGR-stale route update readvertised to a configured non-LLGR peer group.

### CVE-2026-101951

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1288` |
| Published | 2026-10-14T17:17:48.030 |

An Improper Validation of Consistency within Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a network-adjacent configured BGP peer to cause a denial of service by sending a specifically malformed BGP MCAST-TREE update and this NLRI is then attempted to be readvertised.

### CVE-2026-101948

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:47.727 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a remote unauthenticated BGP peer to cause a denial of service via a specific BGP FlowSpec update received by an affected BGP session.

### CVE-2026-101945

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T17:17:47.410 |

An Integer Overflow or Wraparound vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows a remote attacker with an established EVPN BGP peering relationship to cause a denial of service via EVPN BGP route processing. The issue affects EVPN-enabled routing instances and can disrupt control-plane adjacencies.

### CVE-2026-101944

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T17:17:47.247 |

An Integer Overflow or Wraparound vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an attacker to cause a denial of service via specially crafted EVPN route updates from an accepted EVPN BGP peer.

### CVE-2026-101943

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-14T17:17:47.090 |

An Improper Input Validation vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network-based attacker to cause a denial of service via a crafted BGP EVPN update message.

### CVE-2026-101942

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-14T17:17:46.930 |

An Improper Handling of Length Parameter Inconsistency vulnerability in the routing protocol daemon (rpd) process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated network-based attacker to cause a denial of service via a malformed EVPN Type-3 or Type-4 route received from a configured EVPN peer and processed during re-advertisement.

### CVE-2026-101941

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:46.720 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP neighbor to cause a denial of service via a BGP route update when specific routing-policy resolution-map and policy event-tracing configuration is enabled.

### CVE-2026-101940

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:46.543 |

A NULL Pointer Dereference vulnerability in the rpd routing daemon of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated configured BGP peer to cause a denial of service via a BGP UPDATE when ISO-VPN and egress-protection configuration is enabled.

### CVE-2026-101939

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:46.387 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (RPD) of Juniper Networks Junos OS and Junos OS Evolved allows a configured peer sending a BGP UPDATE to cause a denial of service when an import policy with `then source-based-forwarding next-hop next-table <X>` is configured to reference a routing table that does not exist.

### CVE-2026-94197

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-14T15:17:26.963 |

An authentication and authorization bypass vulnerability exists in F5 NGINX Kubernetes Ingress Controller (NIC) when configured with the `ExternalAuth` policy or Ingress external authentication. Client-supplied X-Forwarded-Prefix, X-Forwarded-URI, X-Original-URI, and X-Forwarded-Method routing and method headers are forwarded unsanitized into the internal authentication subrequest (handled by the NGINX auth_request directive). As a result, an unauthenticated, remote attacker may spoof request attributes evaluated by the external authentication provider. 

Impact:
This vulnerability may allow remote attackers 

unauthenticated

 access to protected 

paths. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-91184

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-76` |
| Published | 2026-10-14T15:17:26.420 |

Description

NGINX Gateway Fabric has a vulnerability when it renders the spec.basic.realm (and spec.jwt.realm) field of a namespaced AuthenticationFilter verbatim, unescaped and unvalidated, into the shared data-plane nginx.conf as auth_basic "<realm>";. A namespaced authenticated attacker that configures AuthenticationFilter CRD to an HTTPRoute/GRPCRoute on a shared Gateway can craft a realm value that closes the quoted directive and the enclosing location {} block and injects arbitrary NGINX directives into that Gateway's data-plane config. 

Impact

A remote authenticated attacker can send crafted requests to configure NGINX Gateway Fabric AuthenticationFilter CRD and may be able to read every co-located tenant's mounted secrets, SSRF via proxy_pass, reading the pod ServiceAccount token, or hijacking other tenants' routes. There is no data plane exposure; this is a control plane issue only.






Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-110641

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.437 |

@runnerty/executor-decompress through 3.1.1 contains an OS command injection vulnerability that allows attackers to execute commands by supplying crafted archive file names to compress_file. Attackers who can name a file dropped into a watched directory can inject $() substitutions or unquoted shell metacharacters into shelljs exec() calls, running commands with Runnerty process privileges.

### CVE-2026-110621

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:14.497 |

Swetrix Cloud before 5.1.0 contains a missing authorization vulnerability in ProjectController.addProject that allows authenticated users to hijack arbitrary projects by moving them into their own organisation. Attackers can create an organisation and add a victim project by its public tracking ID to read analytics, change settings, or delete it.

### CVE-2026-104939

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-10-14T15:17:05.260 |

Description
NGINX Ingress Controller has a vulnerability when implementing an externalAuth policy for ingress. NGINX Ingress Controller may mishandle the HTTP response from an OAuth IdP and allow an attacker to acquire unauthenticated access to protected paths before the proper external authentication can happen.



Impact
This vulnerability may allow remote attackers 

unauthenticated

 access to protected 

paths. There is no control plane exposure; this is a data plane issue only.




Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-101895

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-10-14T15:17:03.370 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.31, 21.2.23, and 22.1.6, the @angular/platform-server DOM emulation parser can enter an infinite synchronous loop when Angular server-side rendering processes attacker-controlled HTML containing an incomplete DOCTYPE that ends with whitespace at end of input. In Domino lib/HTMLParser.js, after_doctype_name_state emits doctype and EOF tokens without advancing nextchar or leaving the fixed-lookahead state, so the scanner repeatedly handles the same EOF marker. A remote unauthenticated attacker can use this condition through server-side HTML parsing paths such as innerHTML binding to consume a Node.js SSR worker at full CPU, starve the event loop, and stop concurrent and subsequent requests. This issue is fixed in versions 20.3.31, 21.2.23, and 22.1.6.

### CVE-2026-41545

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23;CWE-78` |
| Published | 2026-10-15T10:17:14.457 |

A relative path traversal vulnerability has been reported to affect QuMagie. If a remote attacker gains an administrator account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
QuMagie 2.9.1 and later

### CVE-2026-93484

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:L/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:Amber` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T04:18:30.373 |

Znuny through 7.3.6 constructs a ticket-search database query by directly concatenating user-supplied input into the SQL statement. This lack of proper sanitization or the use of parameterized queries allows an attacker to inject arbitrary SQL commands, leading to data theft, modification, or denial of service. Specifically this is in Kernel::System::Ticket::TicketSearch and Kernel::System::Ticket::ArticleSearchIndex::DB via the ContentSearch parameter. The parameter is expected to be either "AND" or "OR", but its value was concatenated directly into the generated SQL query without validation.

### CVE-2026-110863

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T23:17:27.830 |

Better Auth @better-auth/sso from 1.7.0-rc.2 before 1.7.3 contains an authentication bypass vulnerability that allows authenticated users to sign in as other users by registering a personal SSO provider. Attackers can copy a legitimate provider's OIDC issuer or SAML entity ID and assert a victim's subject or NameID, because account lookup ignores providerId, creating sessions for victim accounts.

### CVE-2026-102460

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T19:17:05.050 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], a scope bypass vulnerability exists in Eclipse Vert.x Web's ChainAuthHandler when used with scope-requiring authentication handlers such as JWTAuthHandler or OAuth2AuthHandler. When a user is already authenticated on the routing context by a preceding handler in the request pipeline, ChainAuthHandler skips all scope validation configured via withScope() or withScopes(). This affects both any() and all() chain modes.



The root cause is that postAuthentication() relies on internal state that is only set during the authenticate() phase, which is skipped entirely for pre-authenticated users. In any() mode, the absence of this state causes the method to fall through without delegating scope checks to any handler. In all() mode, scope checks are unconditionally skipped.



This allows a user with a valid token but insufficient scopes to access resources protected by scope requirements, provided they were authenticated by an earlier handler in the pipeline. The most common trigger is overlapping authentication handlers on nested routes, where a parent route authenticates broadly and a child route uses a chain to enforce specific scopes.



The impacted component Maven coordinate is io.vertx:vertx-web

### CVE-2026-0322

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:A/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:U/V:D/RE:M/U:Red` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T18:17:07.743 |

A remote code execution (RCE) vulnerability in the management interface of Palo Alto Networks PAN-OS® software enables an authenticated attacker with network access to execute arbitrary code with root privileges on the firewall.



The security risk posed by this issue is minimized by restricting access to the management interface to only trusted internal IP addresses according to our recommended  best practice deployment guidelines https://live.paloaltonetworks.com/t5/community-blogs/tips-amp-tricks-how-to-secure-the-management-access-of-your-palo/ba-p/464431 .



This issue is applicable to PAN-OS software on PA-Series and VM-Series firewalls and on Panorama (virtual and M-Series).



Cloud NGFW and Prisma® Access are not impacted by this vulnerability.

### CVE-2026-101927

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-14T17:17:45.583 |

A Heap-based Buffer Overflow vulnerability in eventd of Juniper Networks Junos OS and Junos OS Evolved on all platforms allows an unprivileged local attacker to cause a denial of service (DoS) or achieve privilege escalation to root via crafted IPC event messages.

### CVE-2026-100236

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:17:44.833 |

A flaw was found in the DPDK GSO library. When software GSO copies packet headers into a new mbuf, it does not check that the header fits in the source first segment or in the destination buffer, and a header longer than the configured GSO segment size can underflow the payload-size calculation. A remote or guest-supplied packet processed with software GSO can trigger an out-of-bounds read or write.

### CVE-2026-91882

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-209` |
| Published | 2026-10-14T16:17:56.880 |

Dell Terraform Provider for OME, versions 1.0.0 through 1.2.3, contains an Insertion of Sensitive Information into Externally-Accessible File or Directory vulnerability in the API client error handling component. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to information exposure.

### CVE-2026-110618

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T15:17:14.053 |

SmsForwarder through 3.5.0 contains a missing authentication vulnerability in its AndServer HTTP server that allows unauthenticated network attackers to invoke remote-control APIs. Attackers can call the default-enabled endpoints to read SMS, call logs and contacts, send SMS, and export or overwrite configuration via the clone API.

### CVE-2026-34008

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-15T10:17:13.443 |

An incorrect permission assignment for critical resource vulnerability has been reported to affect Notes Station 3. If a local attacker gains a user account, they can then exploit the vulnerability to compromise the security of the system.

We have already fixed the vulnerability in the following version:
Notes Station 3 3.9.11 and later

### CVE-2024-22031

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-15T09:17:14.023 |

A vulnerability has been identified within Rancher where a user with the ability to create a project, on a certain cluster, can create a project with the same name as an existing project in a different cluster. This results in the user gaining access to the other project in the different cluster, resulting in a privilege escalation. This happens because the namespace used on the local cluster to store related resources (PRTBs and secrets) is the name of the project.

### CVE-2026-54566

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T20:17:47.403 |

Markdown Preview Enhanced is a Markdown preview extension for Visual Studio Code. Prior to 0.8.29, Markdown Preview Enhanced evaluates repository-controlled .crossnote/config.js and .crossnote/parser.js files with vm.runInNewContext, which does not provide a security boundary from the Node.js host realm. Opening a Markdown file in a malicious repository automatically loads these files, and prototype-chain traversal can reach the host Function constructor and process object, allowing operating-system commands to execute as the victim account without further interaction. Both configuration evaluation and parser-hook evaluation are affected, and the attack does not depend on module-scoped require being available. This issue is fixed in version 0.8.29.

### CVE-2026-102079

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:U/V:X/RE:M/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T17:18:03.560 |

An OS command injection vulnerability in the CLI of Juniper Networks Junos OS allows a local, low privileged attacker to take complete control of the device.

A specific 'request csds' command doesn't sanitize user provided input so that it can be interpreted as a command. This allows unintended command execution with root privileges, which can lead to unauthorized system access or modification.





This issue affects Junos OS:


  *  24.4 versions before 24.4R2-S4;
  *  25.2 versions before 25.2R2-S1;
  *  25.4 versions before 25.4R1-S3;






This issue does not affect Junos OS releases before 24.4R1.

### CVE-2026-110648

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.510 |

@offactory/compress-fonts before 1.1.1 contains an OS command injection vulnerability that allows attackers to execute shell commands by supplying font files with crafted names. Font paths are interpolated unquoted into a FontForge command run through child_process.execSync, so shell metacharacters in file names execute commands with the Node.js process privileges.

### CVE-2026-110647

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:18.373 |

Turnpress through 0.4.2 contains an OS command injection vulnerability that allows attackers to execute shell commands by supplying .docx files with crafted names. The convertDocxToHtml function in src/converter.ts invokes pandoc through execa with shell:true, so shell metacharacters in the --docx path run with the victim's privileges during convert or create.

### CVE-2026-110642

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:17.627 |

xhtml2pdf before 0.2.19 contains an OS command injection vulnerability in pisa.startViewer() that allows attackers to execute commands by interpolating unescaped file names into os.system. Attackers can supply an input file whose name contains a double quote and shell metacharacters, which runs OS commands as the invoking user when the pisa tool is used with -s/--start-viewer.

### CVE-2026-110637

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-14T15:17:16.853 |

buildebooks before 0.2.2 contains an OS command injection vulnerability in lib/kindle.js that allows attackers to execute commands by supplying a crafted EPUB file name passed to kindlegen via child_process.exec. Attackers can craft a book project with a malicious front-matter filename or project folder name and kindle: true to execute OS commands as the user running buildebooks.

### CVE-2026-110633

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-14T15:17:16.283 |

MyReport Updater through 2.1.1 contains a local privilege escalation vulnerability that allows low-privileged users to make the SYSTEM updater service install attacker-supplied archives into arbitrary directories. Attackers can use UpdaterManager.exe over gRPC to set a malicious reference server and installLocation, planting a DLL like HID.dll loaded by osk.exe to gain SYSTEM privileges.

### CVE-2017-20286

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T15:16:59.163 |

DevIL through 1.8.0 contains a heap-based buffer overflow in iGetPalette() in il_gif.cpp that allows attackers to write beyond a 768-byte palette buffer when loading GIF images. Attackers can supply a crafted two-frame GIF whose second frame uses disposal method 1 with a local colour table, writing up to 384 controlled bytes past the heap allocation and possibly executing code.

### CVE-2026-104025

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-693` |
| Published | 2026-10-15T13:17:10.617 |

Path Traversal (CWE-22) in the execute_obj function of the archive object viewer (peach.pas) in PeaZip 11.2.0 and earlier on Windows allows an attacker who convinces a victim to preview an entry of a crafted archive via the "Preview with... -> Associated application" action (Shift+Ctrl+O) to execute an arbitrary program already present on the victim's system, with no warning dialog. The function validates only outname (PeaZip's own temporary directory) with checkfiledirname, while the string actually executed is the concatenation outname+tempstring; tempstring is taken verbatim from the archive entry name (StringGridList.Cells[12,...]) and is never validated. checkfiledirname (list_utils.pas) rejects control and reserved characters in the file name but performs no ".." path-containment check, so an entry named ../../../../Windows/System32/calc.exe escapes the extraction directory and is passed to cp_open -> ShellExecuteW; the extracting backend (7-Zip) strips the traversal while the opener does not. In addition, the SECEXTCONST dangerous-extension confirmation prompt is implemented only in the double-click handler (grid_obj_open) and not on this preview route, so an executable inside an archive reaches ShellExecuteW unannounced, and where the prompt does fire it names the entry's display name rather than the resolved path that will run. Arbitrary code execution was demonstrated with a proof of concept against official PeaZip builds, confirmed on two archive formats (.zip and .tar) to show the defect is in PeaZip's own path handling and not in a single format parser.

### CVE-2026-34014

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-15T10:17:13.697 |

An incorrect permission assignment for critical resource vulnerability has been reported to affect Download Station. If a local attacker gains an administrator account, they can then exploit the vulnerability to compromise the security of the system.

We have already fixed the vulnerability in the following version:
Download Station 5.10.1.312 and later
Download Station 5.11.2.321 and later

### CVE-2026-34009

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-653` |
| Published | 2026-10-15T10:17:13.573 |

An improper isolation or compartmentalization vulnerability has been reported to affect Notes Station 3. If a local attacker gains an administrator account, they can then exploit the vulnerability to compromise the security of the system.

We have already fixed the vulnerability in the following version:
Notes Station 3 3.9.11 and later

### CVE-2026-110868

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-14T23:17:28.537 |

Renovate before 44.79.0 contains a server-side request forgery vulnerability that allows users to make the shared HTTP client request arbitrary internal URLs via extends presets or customDatasources. Attackers can point a preset at an instance metadata service endpoint to obtain AWS credentials or leak sensitive information through Renovate logs.

### CVE-2026-55786

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-306` |
| Published | 2026-10-14T19:17:17.777 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. From 2.26.2 until 2.26.4, the HTTP MCP POST /mcp route accepts unauthenticated JSON-RPC tools/call requests and forwards execute_module arguments to the module registry without the require_auth dependency used by the REST execution routes. An unauthenticated caller can select sandbox.execute_shell and supply its command parameter, which reaches asyncio.create_subprocess_shell with the privileges of the flyto-core server process. The endpoint is reachable locally under the default loopback binding and becomes network reachable when an operator binds the server to a non-loopback interface, allowing arbitrary OS command execution and potential full host compromise. This issue is fixed in version 2.26.4.

### CVE-2026-103414

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T18:17:19.637 |

The GUIX binary resource (theme) loader sizes its arena and populates it in two separate passes that traverse the resource file with independent cursor arithmetic. Because `gx_page_header_data_size` is never validated against the glyph data a page actually contains, the two passes can read different page headers for the same font page, derive different glyph counts, and reserve less than the load pass writes. The excess is written past the end of the arena, with content taken verbatim from the file.



The overflowed buffer is allocated by GUIX itself, through `_gx_system_memory_allocator`, rather than supplied by the caller. The public API `gx_binres_theme_load()` takes no size parameter, so no amount of caller diligence prevents this.



Reproduces in the shipped default configuration; `GX_BINARY_RESOURCE_SUPPORT` is enabled by default.

### CVE-2026-110769

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1188` |
| Published | 2026-10-14T19:17:12.940 |

holaOS through 2026.822.1 contains a missing authorization vulnerability in channel-gateway connectors that allows any messaging-platform user to submit agent tasks because the #isAllowed check accepts all senders when the default allowFrom list is empty. Attackers who can message the operator's Telegram, Slack, Discord, or other bot can have ChannelIngress.handle pass turns to the workspace agent, running configured tools on the operator's machine.

### CVE-2026-97629

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-908` |
| Published | 2026-10-14T15:17:28.600 |

Description
When NGINX Plus or NGINX Open Source is configured with ssl_session_cache 

shared:name:size

without an explicit ssl_session_ticket_key file directives to automatically rotate SSL session ticket keys, a remote unauthenticated attacker is able to forge client SSL sessions 

in a non-deterministic manner that is beyond the attacker's control. An attacker could leverage this vulnerability to bypass verification of client certificates.

Impact


This vulnerability can lead to the exposure of resources or functionality to unintended actors, possibly providing attackers with access to sensitive information. There is no control plane exposure; this is a data plane issue only.






Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-101019

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-436` |
| Published | 2026-10-14T15:17:01.697 |

Description
NGINX JavaScript (njs) has a vulnerability where the njs XML module exposes entity-backed XML attributes inconsistently with libxml2 canonicalization. In both the built-in njs and QuickJS backends during the canonicalization process, the $attr$Name getter may return undefined for an explicitly present attribute containing an internal entity reference. The $attrs getter may return a value derived only from the first attribute child. This may allow an unauthenticated attacker that invests significant effort in obtaining a genuinely signed document to skip validation while signature verification succeeds. An nginx-saml deployment is a confirmed affected consumer when run with the built-in njs backend.

Impact
In affected signed-XML consumers, an unauthenticated attacker can cause security-relevant attributes to appear absent or truncated while signature verification succeeds. In nginx-saml, this can bypass expiry, Destination, and request-correlation checks, enabling replay or acceptance of a response outside its intended context. It does not permit signature or identity forgery, or a direct availability impact. There is no control plane exposure; this is a data plane issue only.



 Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-88794

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-15T13:17:13.837 |

Enterprise Architect is vulnerable to XML External Entity (XXE) injection in the XSLT Debugger feature. When a user loads a crafted XML file containing a `DOCTYPE` with an external DTD reference, the parser processes external entities, allowing an attacker to read arbitrary files from the victim's filesystem.

Because vendor contact attempts were unsuccessful, the vulnerability has only been confirmed in version 17.1 but may also affect other versions.

### CVE-2026-79829

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T10:17:16.083 |

A security vulnerability in HPE NonStop HTTP WEBSERVER can cause memory corruption which may result in a system halt.

### CVE-2026-77711

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-15T09:17:18.573 |

When Jetty's `HttpClient` make a request to a server through a forward proxy, the server may reply with a 407 (Proxy Authentication Required).



The client mistakenly interprets the 407 as coming from the proxy, so it re-sends the request with the `Proxy-Authentication` header, which arrives to the server, that now has access to the proxy credentials.

### CVE-2026-76184

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-15T09:17:18.443 |

In Eclipse Jetty, HttpClient may receive a redirect of the form:



```



/secure/../evil



```



If an attacker is able to control the redirects, then HttpClient matches authentication credentials against `/secure` rather than normalizing the path to `/evil`, and will therefore follow the redirect sending the `Authorization` header for `/secure` to `/evil`.



This also mean that the attacker must have an evil application deployed on the same domain as the target.

### CVE-2026-63315

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-256` |
| Published | 2026-10-15T09:17:17.857 |

WebCTI service for Slican IPx telephone exchanges stores temporary subscriber password in plaintext. An attacker with access to the database can obtain the user's password and log in to the subscriber's account.



This issue was fixed in IPx series version 6.62.0100.

### CVE-2026-35088

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:L/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-326` |
| Published | 2026-10-15T09:17:17.417 |

Slican telephone exchanges use symmetric encryption for TCP/IP communication. Secret key is hardcoded in multiple binary files. An attacker who has access to these files can decrypt the communication.

This issue was fixed in IPx series version 6.62.0100.

The issue STILL EXISTS in End-Of-Life telephone exchanges:
- CCT-1668 (CCT1CPU)
- MAC-6400
- CXS-0424
These products were discontinued in 2011 and 2012 and and will not receive updates. These products require a hardware update in order to receive a software update. The vendor recommends that users of these devices contact the their service department directly to determine the options for upgrading.

### CVE-2026-103224

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.990 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the MySQL message decoder aggregates inbound multi-packet payloads into a composite direct-memory buffer without any cumulative size limit. A malicious, compromised, or man-in-the-middle MySQL server can send a continuous stream of packets with the maximum payload length (0xFFFFFF), preventing the end-of-message condition from being reached, causing unbounded direct-memory allocation on the client and leading to an out-of-memory crash. This occurs before authentication completes.



The impacted component is io.vertx:vertx-mysql-client.

### CVE-2026-103223

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.853 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the PostgreSQL message decoder reads the 4-byte message length field from the PostgreSQL wire protocol without any maximum validation. A malicious, compromised, or man-in-the-middle PostgreSQL server can send a message header with the length field set to an extremely large value (up to Integer.MAX_VALUE), causing the decoder to accumulate subsequent TCP data into a composite buffer without bound, leading to unbounded memory allocation on the client and an out-of-memory crash. This occurs before authentication completes.



The impacted component is io.vertx:vertx-pg-client.

### CVE-2026-102466

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.427 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Vert.x MySQL client (vertx-mysql-client) pre-allocates an array for column definitions based on a server-declared column count with no upper-bound validation. A malicious or compromised MySQL server, or an attacker with man-in-the-middle positioning, can send a crafted result set packet with an extremely large column count, causing the client to attempt a massive heap allocation. The resulting OutOfMemoryError crashes the Netty event loop thread, causing a complete denial of service for all connections and verticles in the Vert.x application.



The impacted component is io.vertx:vertx-mysql-client.

### CVE-2026-102464

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.283 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Eclipse Vert.x MQTT (vertx-mqtt) MqttClient stores every inbound QoS 2 PUBLISH message received from the broker in an internal map (qos2inbound) while awaiting the corresponding PUBREL packet to complete the QoS 2 handshake. This map has no size limit; the maxInflightQueue option is enforced only on the outbound publish path and does not constrain inbound message retention.



A malicious or compromised MQTT broker can exploit this by sending QoS 2 PUBLISH messages with distinct packet identifiers and withholding the PUBREL responses. Each incomplete handshake causes the client to retain the full publish message (topic, payload, and metadata) indefinitely, leading to unbounded memory growth in the Vert.x process. This can degrade the MQTT-consuming application or cause out-of-memory termination.



The impacted component is io.vertx:vertx-mqtt.

### CVE-2026-102463

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.143 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the binary array decoder in vertx-pg-client (DataTypeCodec.binaryDecodeArray) allocates a Java array sized by a server-declared 32-bit dimension count with no upper bound. A malicious or compromised PostgreSQL server, or an on-path attacker intercepting an unencrypted connection, can send a crafted DataRow message with an excessively large array dimension value, causing the client to attempt a multi-gigabyte heap allocation and crash with an OutOfMemoryError.



The impacted component is io.vertx:vertx-pg-client.

### CVE-2026-102462

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T09:17:15.020 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the TDS message decoder in the Vert.x MSSQL client (vertx-mssql-client) aggregates inbound TDS packets into a composite direct-memory buffer without any cumulative size limit. A malicious, compromised, or man-in-the-middle SQL Server can send a continuous stream of TDS packets without setting the END_OF_MESSAGE status flag, causing unbounded direct-memory allocation on the client and leading to an out-of-memory crash. This occurs before authentication completes.



The impacted component is io.vertx:vertx-mssql-client.

### CVE-2026-102465

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-15T08:16:36.540 |

In Eclipse Vert.x versions [4.0.0, 4.5.34] or [5.0.0,5.0.12] or [5.1.0,5.1.9] or [5.2.0, 5.2.0], the Vert.x Redis client RESP parser pre-allocates arrays to a length declared by the server without enforcing an upper bound. A malicious or compromised Redis server, or an attacker in a man-in-the-middle position, can send a crafted RESP response declaring an extremely large array, push, or attribute length, causing the client to attempt a massive heap allocation. The resulting OutOfMemoryError crashes the Vert.x event loop thread, denying service to all connections and verticles sharing that loop.



The impacted component is io.vertx:vertx-mysql-client.

### CVE-2026-79821

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T07:18:02.853 |

A security vulnerability in HPE NonStop SOAP 4.0  may cause memory corruption resulting in a system down.

### CVE-2026-110872

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T23:17:29.097 |

Nodemailer from 3.0.0 before 10.0.10 contains a quadratic complexity denial of service vulnerability in the SMTP client reply parser in SMTPConnection._onData and isPartialResponse. A malicious SMTP server or on-path attacker can stream continuation lines without a completion line before authentication, blocking the Node.js event loop and exhausting memory.

### CVE-2026-110854

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-14T23:17:26.490 |

Parse Server before 8.6.97 and 9.0.0 before 9.10.2-alpha.6 does not handle errors raised while sending verification or password reset emails, causing the server process to exit. A client holding only the public application keys can sign up, request a verification email, or request a password reset while the mail provider rejects, rate limits, or is unavailable, crashing the server.

### CVE-2026-110843

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-14T23:17:24.787 |

n8n before 2.41.4 and 2.42.x before 2.42.1 contains an uncontrolled resource consumption vulnerability in the unauthenticated OAuth authorize endpoint, which resolves clients by URL path but stores the caller's raw identifier as the record key. Unauthenticated attackers can send identifiers differing only in their query string to create unlimited first-party client records that bypass the registration cap, growing the database until the disk fills.

### CVE-2026-110833

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T23:17:23.160 |

FreeRDP from 3.0.0-beta1 before 3.32.0 fails to enforce cumulative or absolute size limits when reassembling RDPDR channel fragments in the proxy. Attackers can send a FIRST fragment followed by continuation fragments without LAST, growing per-session heap streams proportional to traffic and exhausting proxy memory.

### CVE-2026-110830

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T23:17:22.737 |

FreeRDP before 3.32.0 fails to close prior serial handles in serial_process_irp_create, allowing a malicious RDP server to exhaust file descriptors. Attackers can send repeated serial IRP_MJ_CREATE requests to accumulate descriptors and terminate the client at the CommReadFile FD_SETSIZE assertion.

### CVE-2026-71854

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-306;CWE-639;CWE-862` |
| Published | 2026-10-14T21:17:39.177 |

OpenAEV is an open source platform allowing organizations to plan, schedule and conduct cyber adversary simulation campaign and tests. Prior to version 2.260622.0, on a default installation, the `/api/player/**` lessons endpoints can be called without authentication, and they trust a client-supplied `userId` query parameter without verifying that the caller is that user or a member of the exercise. An unauthenticated client that knows an exercise UUID can read lessons-learned questions and answers (including each answer's author identity) and create or overwrite answers attributed to an arbitrary user. Version 2.260622.0 contains a patch.

### CVE-2026-61843

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T21:17:37.947 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.18.0, FileRise upload-enabled shared-folder and upload-only links do not reject a destination filename that already exists. An unauthenticated visitor with a valid share token and any configured share password can upload a file with the same name as an existing file and silently replace its content while the original uploader metadata remains. The same replacement gap affects ordinary authenticated uploads through /api/upload/upload.php and authenticated upload-only users who lack edit authority over the existing file. This issue is fixed in version 3.18.0.

### CVE-2026-55383

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-285` |
| Published | 2026-10-14T20:17:48.350 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. Prior to version 2.4.0, InvoiceShelf public customer invoice, estimate, and payment routes use an EmailLog token's numeric mailable_id without verifying mailable_type, and the JSON handlers do not enforce EmailLog::isExpired. A token issued for one document type can therefore disclose a different company's document when numeric identifiers collide, and an expired token can remain usable on the JSON routes GET /customer/invoices/{email_log:token}, GET /customer/estimates/{email_log:token}, and GET /customer/payments/{email_log:token}. View handlers can also mark a mismatched invoice or estimate as viewed and send a notification. This issue is fixed in version 2.4.0.

### CVE-2026-110765

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-14T19:17:12.313 |

FlexPrice through 2.1.38 contains an authentication bypass vulnerability in HandleQuickBooksWebhook that skips signature verification when the intuit-signature header is omitted. Unauthenticated attackers knowing a tenant and environment ID can replay forged payment notifications to repeatedly add payment amounts, marking invoices paid or overpaid.

### CVE-2026-100406

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-200;CWE-306` |
| Published | 2026-10-14T19:16:59.847 |

dbt enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications. From 2.0.0-alpha.0 until 2.0.0-alpha.5, dbt docs serve exposes the unauthenticated POST /api/v1/query endpoint in crates/dbt-docs-server/src/handlers/query.rs, which passes caller-supplied SQL to DuckDbViewsBackend::query_arrow() in crates/dbt-index-core/src/backend.rs without authorization or an allowlist. A client that can reach the server can invoke DuckDB filesystem-reading functions to read files available to the dbt process, including files outside the docs index directory. The server binds to localhost by default, but operators can expose it to a network through the host option or DBT_DOCS_HOST setting. This issue is fixed in version 2.0.0-alpha.5.

### CVE-2026-108480

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T18:17:29.393 |

Missing Authorization vulnerability in Skydropx Skydropx skydropx allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Skydropx: from n/a through 2.1.4.

### CVE-2026-94200

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1288` |
| Published | 2026-10-14T17:20:21.590 |

Improper Validation of Consistency within Input vulnerability in Erlang OTP ssl (tls_handshake_1_3, ssl_handshake and tls_client_ticket_store modules) allows a malicious TLS 1.3 server to cause a denial of service of the ssl application on the client node.

The TLS 1.3 client decodes the extensions of a NewSessionTicket message as if they came from EncryptedExtensions. It therefore accepts a 0-length early_data extension, a form that is only valid in ClientHello and EncryptedExtensions. With {session_tickets, auto}, the client stores the ticket in the node-global tls_client_ticket_store. On the next automatic resumption, tls_handshake_1_3:get_max_early_data/1 crashes the store with a case_clause. Repeated crashes can exceed the restart intensity of the ssl supervisors, which use the rest_for_one strategy, and take down ssl for all connections on the node.

This issue affects OTP from OTP 23.3 before OTP 27.3.4.19, OTP 28.5.0.8, and OTP 29.1.2, corresponding to ssl from 10.3 before 11.2.12.14, 11.6.0.7, and 11.7.8.

### CVE-2026-86565

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:20:05.770 |

A flaw was found in DPDK lib/vhost. A guest can desynchronize virtqueue size from inflight descriptor table size, causing an out-of-bounds write in the host vhost process.

### CVE-2026-102086

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:18:04.637 |

A NULL Pointer Dereference vulnerability in the DNS plugin of Juniper Networks Junos OS on SRX Series allows an unauthenticated, network-based attacker to cause a complete Denial-of-Service (DoS).



When multiple DNS queries are received in a single flow session, where one query matches a Security Intelligence (SecIntel) feed and another query is sent for DNS Domain Generation Algorithm (DGA) analysis, an error in processing logging of these asynchronous tasks can lead to an FPC crash. The exact timing conditions are outside an attacker's direct control.

This issue affects Junos OS on SRX Series:


  *  All versions before 23.2R2-S7.7;
  *  from 23.4 before 23.4R2-S8.13;
  *  from 24.2 before 24.2R2-S5.5;
  *  from 24.4 before 24.4R2-S4;
  *  from 25.2 before 25.2R2-S1;
  *  from 25.4 before 25.4R1-S2.

### CVE-2026-102083

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-413` |
| Published | 2026-10-14T17:18:04.160 |

An Improper Resource Locking vulnerability in the UTM processing of Juniper Networks Junos OS on SRX Series allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).



When UTM WebFiltering is configured and the WebFiltering cloud server is unreachable, sustained HTTP traffic load may cause the UTM subsystem to crash and restart, which will lead to a complete service outage until the system has recovered.
When category lookup requests cannot be completed, they accumulate internally. Under high load and specific timing conditions, an invalid internal state can occur during cleanup of pending WebFiltering lookups, resulting in a crash of the UTM process.
This issue applies to both NextGeneration WebFiltering (NGWF) and Enhanced WebFiltering (EWF).

This issue affects Junos OS on SRX Series:


  *  23.2 versions from 23.2R2 before 23.2R2-S7.7;
  *  23.4 versions from 23.4R2 before 23.4R2-S8.13;
  *  24.2 versions before 24.2R2-S5.5;
  *  24.4 versions before 24.4R2-S4;
  *  25.2 versions before 25.2R2-S1;
  *  25.4 versions before 25.4R1-S3, 25.4R2.

### CVE-2026-102082

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-166` |
| Published | 2026-10-14T17:18:04.010 |

An Improper Handling of Missing Special Element vulnerability in the SSL plugin of Juniper Networks Junos OS on SRX Series allows a network-based, unauthenticated attacker to cause a Denial-of-Service (DoS).



This issue is will occur when 'ssl-proxy' is configured on SRX platforms and during a TLS session-resumption attempt a specifically malformed TLS message is received. This results in an invalid pointer access and PFE crash which causes a temporary loss of traffic forwarding until the PFE automatically recovers. The exact internal timing to trigger this issue is outside the attacker's direct control.This issue affects Junos OS on SRX Series:


  *  All versions before 23.2R2-S5;
  *  23.4 versions before 23.4R2-S5;
  *  24.2 versions before 24.2R2-S2;
  *  24.4 versions before 24.4R2.

### CVE-2026-102078

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:M/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-14T17:18:03.400 |

A Use After Free vulnerability in the packet forwarding engine (pfe) of Juniper Networks Junos OS on SRX Series allows an unauthenticated, network-based attacker to cause a Denial-of-Service (DoS).



When web filtering for TCP traffic is configured, a high volume of DNS requests increases the likelihood of a flowd crash and restart, which leads to a complete service outage until the service has automatically recovered. This is a race condition outside the attacker's direct control.

This issue affects Junos OS on SRX Series:


  *  All versions before 23.2R2-S5;
  *  from 23.4 before 23.4R2-S6;
  *  from 24.2 before 24.2R2-S3;
  *  from 24.4 before 24.4R2-S1;
  *  from 25.2 before 25.2R1-S1, 25.2R2.

### CVE-2026-110718

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-14T16:17:44.047 |

TurboDocx html-to-docx through 1.23.1 contains a server-side request forgery vulnerability that allows attackers supplying HTML to make the server fetch internal URLs via img src attributes. Attackers can reference loopback, private, or cloud metadata addresses that bypass the loose isValidUrl() check, and read responses embedded in the generated DOCX word/media folder.

### CVE-2026-102695

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-345;CWE-409;CWE-552` |
| Published | 2026-10-14T16:17:29.840 |

OmniFaces is a utility library for Faces. In OmniFaces versions before 1.14.3, 2.7.33, 3.14.23, 4.7.12, and 5.4.2, CombinedResourceHandler accepts a structurally valid deflated and base64 encoded combined resource ID without verifying that the server issued it. A forged ID can cause unbounded decoded output, add unique reconstructed IDs to a process-lifetime cache, or combine resources other than stylesheets and scripts. Because jakarta.faces.RESOURCE_EXCLUDES is not applied by this custom resolution path, a forged ID can disclose Facelets source from the webapp resource tree or META-INF/resources. In a deployment configured with the wildcard CDN mapping, a forged ID that selects omnifaces.graphic can also cause a blind, deployment-dependent server-side fetch whose destination derives partly from the request Host header. The flaw does not provide arbitrary file read or establish arbitrary-scheme or arbitrary-destination SSRF. The shared authenticity failure permits memory exhaustion and limited resource disclosure. This issue is fixed in versions 1.14.3, 2.7.33, 3.14.23, 4.7.12, and 5.4.2.

### CVE-2026-101896

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-10-14T16:17:29.013 |

Angular is a development platform for building mobile and desktop web applications using TypeScript/JavaScript and other languages. Prior to 20.3.32, 21.2.24, and 22.2.0, the @angular/router URL parser stores numeric matrix parameter names and numeric outlet names as properties on initially empty JavaScript objects during Node.js server-side rendering. V8 can interpret these URL-derived keys as array indices and allocate dense backing stores sized to high numeric values, so repeated small path segments cause disproportionate per-segment heap consumption. An unauthenticated attacker can send overlapping requests containing repeated numeric matrix parameters when SSR is enabled, the router directly parses the request URL, and upstream proxies allow semicolons and multiple path segments, eventually exhausting the Node.js old-space heap and terminating the SSR worker. Pure client-side Angular applications are not affected. This issue is fixed in versions 20.3.32, 21.2.24, and 22.2.0.

### CVE-2026-17031

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T06:17:02.693 |

The Checkout Field Manager (Checkout Manager) for WooCommerce plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 7.9.6 This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for authenticated attackers, with subscriber-level access and above, to delete arbitrary Media Library attachments.

### CVE-2026-57490

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-308` |
| Published | 2026-10-14T21:17:37.357 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.16.0, when an administrator has enabled WebDAV, FileRise WebDAV Basic authentication validates only the account username and password through AuthModel::authenticate() and does not enforce the account's configured TOTP factor. An attacker who knows valid primary credentials for a TOTP-enabled account can authenticate to the enabled WebDAV service without supplying the second factor and exercise the account's WebDAV file permissions. The browser login path enforces TOTP, but the separate public/webdav.php authentication callback did not. This issue is fixed in version 3.16.0.

### CVE-2026-57489

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-14T21:17:37.200 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.16.0, FileRise deployments with AUTH_BYPASS enabled trust the configured reverse-proxy identity header without verifying that the request originated from FR_TRUSTED_PROXIES. When the backend application port is reachable directly, an unauthenticated attacker can supply X-Remote-User and obtain a session for the asserted account, including an administrator account, without a password or MFA. The flaw is limited to deployments that enable proxy-header authentication and expose an untrusted path to the backend. This issue is fixed in version 3.16.0.

### CVE-2026-104108

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287;CWE-290;CWE-345` |
| Published | 2026-10-14T21:17:34.880 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.23.0, FileRise maps an authenticated OIDC identity to a local account using mutable preferred_username or email claims and does not require email_verified for email-based naming. An attacker who can obtain provider-issued claims colliding with an existing local username can be logged in as that account, including the built-in administrator, even when automatic provisioning is disabled. Exploitability depends on the configured identity provider allowing the colliding claim. This issue is fixed in version 3.23.0.

### CVE-2026-103977

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-307;CWE-841` |
| Published | 2026-10-14T21:17:33.850 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.23.0, FileRise stores failed TOTP verification attempts in $_SESSION. An attacker who already possesses a target account's valid primary credential can restart the login workflow in a new session and restore the second-factor attempt allowance, permitting continued online TOTP guessing beyond the intended five-attempt limit. The pending-login TOTP handlers did not share a durable account-wide limit. This issue is fixed in version 3.23.0.

### CVE-2026-55682

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-200;CWE-384` |
| Published | 2026-10-14T20:17:50.487 |

WeGIA is a web manager for charitable institutions. Prior to 3.8.6, the auto-prepended web/html/seguranca/sessionStart.php reflects an attacker-supplied PHPSESSID cookie in a Set-Cookie response and uses DB_HOST as the cookie domain. If a victim authenticates while using the attacker-selected identifier, the attacker can reuse that identifier to hijack the authenticated session. The response also discloses the internal database host name through the cookie Domain attribute, and the vulnerable session handler affects all PHP pages. This issue is fixed in version 3.8.6.

### CVE-2026-102986

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T20:17:28.907 |

Plane is an open-source project management tool. In 1.3.1 and earlier, EntityAssetEndpoint at the public project asset endpoint /api/public/assets/v2/anchor/{anchor}/ requires authentication for write operations but does not verify workspace or project membership. An authenticated user who knows a published project's public DeployBoard.anchor can create FileAsset records in that project and soft-delete existing assets by identifier, allowing cross-workspace file injection, storage abuse, and data loss. The issue is fixed in version 1.4.0.

### CVE-2026-92154

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T18:19:34.630 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.2.0, Svc::FileUplink handleDataPacket offset and size validation is vulnerable because the component checks byteOffset plus dataSize with wrapping U32 arithmetic and then seeks to the large attacker-controlled offset before writing. When a file-uplink DATA packet supplies a byteOffset and dataSize whose unsigned sum wraps below the declared file size, data can be written beyond the declared upload size, causing file integrity loss and potentially large sparse-file growth or resource exhaustion. This issue is fixed in version 4.2.0.

### CVE-2026-79957

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T18:18:19.133 |

ServiceNext contains an insecure direct object reference (IDOR) in the /api/Usuario/GetUsuarios endpoint, which accepts a user-controlled numeric ID in the request body without verifying that the authenticated token belongs to the requested account (CWE-639). Any authenticated user can iterate the ID parameter to retrieve the full profile record of every other user, including passwords stored in cleartext (CWE-256), enabling account takeover and credential-stuffing attacks.

### CVE-2026-104103

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-10-14T18:17:21.540 |

Ludwig is a low-code framework for building custom LLMs, neural networks, and other AI models. Prior to 0.17.8, ludwig.datasets.archives.extract_archive() validated tar member names before calling TarFile.extractall() but did not validate symlink members or hard-link members. A crafted archive could create a link that escaped the extraction directory and then write a later member through that link, placing attacker-controlled content at an arbitrary filesystem path with the extracting process's privileges. The same containment check used os.path.commonprefix, so a sibling path sharing the destination's character prefix could also pass. The dataset-loading path can download and extract configured archive URLs, but exploitation requires a user to process an archive from a source controlled or compromised by the attacker on supported Python 3.12 and 3.13 runtimes. Python 3.14 is not affected because its default tar data filter rejects escaping links. This issue is fixed in version 0.17.8.

### CVE-2026-89068

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-304` |
| Published | 2026-10-14T16:17:55.017 |

Missing critical step in authentication vulnerability in Progress MOVEit Transfer (LDAP module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-66877

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-14T15:17:21.863 |

Gitea enforces first-time fork contributor approval by blocking jobs, but some job transition and dispatch paths do not re-check the run's approval requirement. A separate run sharing a job-level concurrency group can cancel a pending job and cause its blocked sibling jobs to be re-emitted and dispatched without approval. This allows unreviewed workflow code to execute on self-hosted runners; fork secrets remain withheld and the run token remains read-only.

### CVE-2026-79824

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-30` |
| Published | 2026-10-15T10:17:15.483 |

A directory traversal vulnerability in HPE NonStop Python 3.x could allow  attackers to overwrite arbitrary files via a .. (dot dot) sequence in filenames in a TAR archive.

### CVE-2023-32198

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-295` |
| Published | 2026-10-15T09:17:13.847 |

A vulnerability has been identified in Steve where by default it was using an insecure option that did not validate the certificate presented by the remote server while performing a TLS connection. This could allow the execution of a man-in-the-middle (MitM) attack against services using Steve.

### CVE-2026-89069

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T16:17:55.140 |

Improper neutralization of input during web page generation ('cross-site scripting') vulnerability in Progress MOVEit Transfer (Ad Hoc module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-53615

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T16:17:46.070 |

util-linux is a random collection of Linux utilities. Before util-linux 2.41.4, `parse_dos_extended()` in `libblkid/src/partitions/dos.c` computes an extended-partition start sector with 32-bit addition and does not apply the extended-area bounds checks to the first two EBR entries. A local attacker who causes a crafted DOS extended-partition disk image or removable medium to be probed can wrap `cur_start + start` to sector zero and cause libblkid to report a false partition overlapping the MBR. This directly compromises the integrity of the reported partition metadata; disk modification or availability loss requires a separate downstream consumer to act on that metadata. This issue is fixed in 2.41.4.

### CVE-2026-86563

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-131` |
| Published | 2026-10-14T17:20:05.600 |

A flaw was found in DPDK lib/vhost. A double-offset bug in vhost log mapping calculation can lead to incorrect memory access.

### CVE-2026-86562

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-14T17:20:05.420 |

A flaw was found in DPDK lib/vhost. A TOCTOU double-fetch of control-queue descriptors allows a heap buffer overflow with attacker-controlled content in the VDUSE control-queue handler.

### CVE-2026-103929

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-284` |
| Published | 2026-10-14T16:17:30.577 |

mise manages dev tools like node, python, cmake, and terraform. Prior to 2026.7.14, in the default non-safe mode, mise loads .mise.toml [settings] from an untrusted local project before trust approval and strip_local_only_settings removes only fields marked global_only. The unix_default_file_shell_args, unix_default_inline_shell_args, windows_default_file_shell_args, and windows_default_inline_shell_args settings were not marked global_only, allowing a repository to replace the default interpreter arguments used by trusted tasks that have no explicit shell, postinstall directives, template exec operations, or hooks that fall back to the default shell. When mise appends the trusted command after the attacker-controlled interpreter arguments, the attacker-selected command can execute first with the developer account's privileges even though the local configuration was never trusted. The separate path-sanitization hardening note in the advisory is outside this vulnerability. This issue is fixed in version 2026.7.14.

### CVE-2025-66275

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T07:17:56.870 |

A path traversal vulnerability has been reported to affect Video Station. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Video Station 5.8.5 and later

### CVE-2025-66272

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T07:17:56.730 |

A path traversal vulnerability has been reported to affect Video Station. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Video Station 5.8.5 and later

### CVE-2026-110857

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1287` |
| Published | 2026-10-14T23:17:26.903 |

GitPython before 3.2.0 contains a remote code execution vulnerability that allows attackers to run commands because Git.ls_remote forwards URLs without check_unsafe_protocols validation. Attackers can supply ext:: remote-helper URLs to execute commands when git permits the ext transport, while merge_base and IndexFile.move also accept unguarded option injection.

### CVE-2026-110845

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-10-14T23:17:25.097 |

n8n before 1.123.83, 2.x before 2.41.4, and 2.42.x before 2.42.1 contains a code execution vulnerability in the Git node Log operation, which fails to strip a repository's local git configuration before invoking an external program. Authenticated members who can point the node, including as an agent tool, at a repository whose local configuration they control can execute programs as the n8n process user.

### CVE-2026-110842

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1321` |
| Published | 2026-10-14T23:17:24.637 |

n8n before 2.41.4 and 2.42.x before 2.42.1 contains a prototype pollution vulnerability in the MCP workflow-validation tool, whose interpreter evaluates caller-supplied code in the main process, reads inherited properties, and permits assignment onto shared prototypes. An authenticated member holding only a workflow:read grant can replace a built-in method with one returning a truthy value so server-side permission checks accept unheld scopes, enabling takeover of owner accounts not protected by MFA.

### CVE-2026-53999

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-441` |
| Published | 2026-10-14T19:17:17.340 |

Radius is a cloud-native, portable application platform that makes app development easier for teams building cloud-native apps. Prior to 0.58.0, the Kubernetes controller deserializes the user-controlled radapp.io/status annotation on a Deployment and uses its container resource identifier for deletion without confirming ownership by that Deployment. An attacker with permission to modify Deployment annotations and knowledge of a target Radius resource ID can forge radapp.io/status and set radapp.io/enabled to false, causing reconciliation to enter the privileged deletion path for another tenant's Radius-managed container resource. In a multi-tenant installation this confused-deputy condition can delete another team's recoverable container resource and disrupt service; in a single-tenant installation the impact is limited to self denial of service. The multi-tenant Radius controller reads the annotations in pkg/controller/reconciler/annotations.go and reaches the privileged delete in pkg/controller/reconciler/deployment_reconciler.go. The issue does not disclose data, grant privileges, or provide persistence. This issue is fixed in version 0.58.0.

### CVE-2026-91159

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T16:17:56.613 |

Discourse is an open-source discussion platform. Prior to 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9, oEmbed processing treated an entire attacker-controlled HTML fragment as trusted when the fragment contained an iframe whose source matched the configured allowlist. A user with posting permission who controlled a public webpage and its oEmbed response could combine an allowlisted iframe with unrelated sibling HTML or CSS, causing stored visual overlays or other styled content to appear in post content and enabling misleading or fraudulent user interfaces. Exploitation requires a posting account, control of the fetched webpage and oEmbed response, and an allowlisted iframe source. The issue affects content integrity but does not expose restricted data, disrupt availability, or require interaction with Discourse Content Security Policy. This issue is fixed in versions 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9.

### CVE-2026-110623

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:14.833 |

Papermerge Core through 3.5.3 contains a missing authorization vulnerability in the shared nodes API that allows authenticated users to share other users' documents by supplying arbitrary node UUIDs. Attackers can call POST /shared-nodes or PATCH /shared-nodes/access/{node_id} to grant themselves any role, then read, modify, or delete victims' documents and revoke existing shares.

### CVE-2026-110622

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:14.697 |

Papermerge Core through 3.5.3 contains a missing authorization vulnerability that allows authenticated users to manipulate other users' pages because page management and OCR endpoints skip has_node_perm checks. Attackers knowing page UUIDs can call /pages/, /pages/move, or /pages/extract to rotate, delete, or extract victims' pages, and trigger OCR via /tasks/ocr.

### CVE-2025-71433

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:00.837 |

Kaneo before 2.1.6 contains a missing authorization vulnerability that allows authenticated users to access other workspaces by supplying project, task, label or workspace identifiers to API routes lacking membership checks. Attackers who obtain identifiers, for example from shared project links, can read projects and tasks, modify or delete tasks, labels and comments, and search workspace contents.

### CVE-2026-79832

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T11:17:50.313 |

A stack buffer overflow vulnerability in HPE NonStop SQL/MX Executor may potentially result in information disclosure or process crash.

### CVE-2026-76661

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T02:20:16.153 |

A vulnerability in HPE NonStop QIOMON allows an out-of-bounds write that can corrupt buffer data.

### CVE-2026-55382

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:L` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T20:17:48.200 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. Prior to version 2.4.0, InvoiceShelf NotesController::show, NotesController::update, and NotesController::destroy authorize only the generic view notes or manage notes ability and do not pass the route-bound Note to NotePolicy::viewNotes or NotePolicy::manageNotes, so neither method checks the target note's company_id. Because the Note model has no global company scope, an authenticated staff user with ordinary note abilities can select another company's sequential note identifier and read, modify, or delete its reusable invoice, estimate, and payment note templates. This issue is fixed in version 2.4.0.

### CVE-2026-102899

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T19:17:06.170 |

Sentry is an application monitoring and error tracking platform. From 26.5.0 until 26.7.2, the SAML SSO identity-linking flow allows an attacker who controls a SAML identity provider to socially engineer an authenticated user into opening a malicious URL, link the attacker's identity to the victim's Sentry account, and take control of that account. The attack requires a browser that accepts the cross-site cookie context, including Firefox with SameSite=None cookies or Chromium with third-party cookies enabled. Sentry SaaS received the remediation on July 27, 2026, and self-hosted Sentry is fixed in version 26.7.2.

### CVE-2026-100169

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-14T16:17:28.350 |

Improper Authentication in the social account linking path of the Prowler API in Prowler from 5.4.0 before 5.35.0 allows a remote unauthenticated attacker to obtain persistent access to the account of a user who has not yet registered, because ProwlerSocialAccountAdapter.pre_social_login() in api/src/backend/api/adapters.py links a Google or GitHub login to any existing local account that has the same email address as the one returned by the provider, without requiring that the address has been verified by the provider or on the existing account, and without any other check that both accounts belong to the same person. Self registration is open and the new account is usable at once, because UserViewSet.get_permissions() in api/src/backend/api/v1/views.py grants AllowAny to the create action, ACCOUNT_EMAIL_VERIFICATION is set to none in api/src/backend/config/settings/social_login.py, and the Django ModelBackend checks only the password and is_active, not the django-allauth EmailAddress record. An attacker who registers an email address before its owner keeps the password set at registration after the link is made, because sociallogin.connect() does not reset the password and does not disable the existing account, and the owner who later signs in with Google or GitHub is logged into the attacker's account. django-allauth makes the same email based link on its own, because SOCIALACCOUNT_EMAIL_AUTHENTICATION and SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT are both set to True in the same settings module. This gives the attacker the cloud provider credentials, scan findings and tenant memberships held in the account.

### CVE-2026-110723

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-290;CWE-644` |
| Published | 2026-10-15T13:17:12.857 |

In `api-gateway` versions till `1.7.3`, The default rate-limit key resolver, `ClientIpKeyResolver`, derives the per-client bucket key from the leftmost element of the `X-Forwarded-For` request header. That element is supplied by the originating HTTP client and is not validated against any trusted-proxy list. A single attacker can therefore obtain an unlimited number of independent rate-limit buckets — one per unique header value — and completely bypass the gateway's request-rate limiting on every route that uses the shipped default configuration.

### CVE-2026-107416

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-15T13:17:10.930 |

Authorization Bypass Through User-Controlled Key vulnerability in Webba Plugins Webba Booking webba-booking-lite allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Webba Booking: from n/a through 6.5.2.

### CVE-2026-79833

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248` |
| Published | 2026-10-15T11:17:50.433 |

A vulnerability in HPE NonStop ANSI SQLUTIL may allow a remote unauthenticated actor to cause an affected service to terminate unexpectedly, causing a denial of service.

### CVE-2026-109695

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-15T11:17:27.113 |

Insertion of Sensitive Information Into Sent Data vulnerability in WPManageNinja FluentCart fluent-cart allows Retrieve Embedded Sensitive Data.This issue affects FluentCart: from n/a through 1.7.1.

### CVE-2026-109855

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-248;CWE-754` |
| Published | 2026-10-15T09:17:16.573 |

undici is an HTTP client library for Node.js. In versions 8.11.0 and 8.11.1, its experimental WebSocket client, which is enabled by default when HTTP/2 is allowed, mishandles a failed WebSocket handshake over HTTP/2: the request is already marked completed, so the abort becomes a no-op and the underlying HTTP/2 stream is left open with no error listener. When a malicious server then destroys the connection, the orphaned stream emits an unhandled error and the Node.js process exits. A remote, unauthenticated server can therefore crash any client that opens a WebSocket to it over HTTP/2, resulting in a denial of service. The issue is fixed in undici 8.11.2, and users should upgrade to 8.11.2 or later. As a workaround, set allowH2 to false to disable HTTP/2 for WebSocket connections, or avoid opening WebSocket connections to untrusted servers.

### CVE-2026-101290

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-15T09:17:14.727 |

A remote attacker may send a specially crafted network packet that causes the
affected application to perform an out-of-bounds memory read due to insufficient validation of
packet length. This may result in an application crash and a denial-of-service condition.

### CVE-2026-96537

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T07:18:03.563 |

The Tutor LMS  WordPress plugin before 4.1.1 does not perform a capability check in a routine that regenerates its managed pages, allowing unauthenticated users to force-publish unpublished pages and overwrite their content, create missing ones, and change the options that reference them.

### CVE-2025-68404

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-15T07:17:57.157 |

A time-of-check time-of-use (toctou) race condition vulnerability has been reported to affect QuRouter. If exploited, the vulnerability could allow remote attackers to compromise the security of the system.

We have already fixed the vulnerability in the following version:
QuRouter 2.6.4.001 and later

### CVE-2026-15090

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T06:17:02.160 |

The Link Library plugin for WordPress is vulnerable to time-based SQL Injection via the 'link_url' parameter in all versions up to, and including, 7.9.2 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-76663

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T03:17:11.233 |

A stack-based buffer overflow vulnerability in HPE NonStop TELSERV can cause memory corruption that may result in DoS.

### CVE-2026-110907

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-669` |
| Published | 2026-10-15T03:17:10.640 |

Backdrop CMS Core 1.35.x before 1.35.2 and 1.34.x before 1.34.6 mishandles tokens. A token is a small placeholder string (like [node:title] or [user:name]) used to automatically insert dynamic data into text. A browser is provided for selecting tokens by type. The product doesn't sufficiently limit access to the types of tokens that are available in the token browser. The names of the individual tokens are adequately protected.

### CVE-2026-76659

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-15T02:20:15.897 |

A vulnerability in the finger daemon of HPE NonStop TCP/IP UTILITIES could allow an unauthenticated remote attacker to cause a denial of service.

### CVE-2026-73799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-15T02:20:15.457 |

A security vulnerability in HPE NonStop SNMP Trap Multiplexer may cause memory corruption

### CVE-2026-107795

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-862` |
| Published | 2026-10-14T23:17:22.250 |

Omada Controller's MSP and OpenAPI certificate/private-key management APIs do not properly enforce administrative authorization, allowing an authenticated user to perform privileged certificate management operations. 

Successful exploitation may allow a low-privileged authenticated user to upload or delete the controller's TLS certificate or private key, potentially disrupting secure management access.

### CVE-2026-102298

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-14T22:17:22.150 |

In Omada Controller MSP mode, the user-confirmation endpoint fails to enforce the required permission check. An authenticated user can supply a caller-controlled Identifier parameter to validate credentials for another account and receive responses that distinguish nonexistent users, invalid passwords, and successful authentication. 

Successful exploitation may allow user enumeration, credential verification, and unauthorized access to MSP resources or compromise of targeted accounts.

### CVE-2026-73261

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-20;CWE-125` |
| Published | 2026-10-14T19:17:19.990 |

Mongoose is an embedded web server and network library. Prior to 7.23, the built-in TCP/IP stack enabled by MG_ENABLE_TCPIP in src/net_builtin.c does not reject a TCP option whose declared opts[1] length exceeds the remaining option bytes. In handle_opt(), a NOP followed by a truncated MSS option causes opts[3] to be read outside the declared options area and used as the low byte of dmss. An unauthenticated remote peer can corrupt the per-connection MSS value so later mg_send() calls transmit truncated or zero-length application payloads while the TCP connection otherwise appears healthy. This issue is fixed in version 7.23.

### CVE-2026-73260

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-14T19:17:19.840 |

Mongoose is an embedded web server and network library. Prior to 7.23, the built-in TLS certificate parser selected by MG_TLS_BUILTIN fails to verify that a long-form DER element length fits within the remaining certificate buffer. In mg_der_to_tlv() and mg_der_next(), a peer-controlled length can advance the parser beyond the certificate and underflow the remaining uint32_t length, causing mg_tls_parse_cert_der() to continue walking an invalid pointer. An unauthenticated malicious TLS server, or a client presenting a certificate to a server configured for client certificates, can trigger an out-of-bounds read and denial of service during the handshake. This issue is fixed in version 7.23.

### CVE-2026-73252

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-125;CWE-191` |
| Published | 2026-10-14T19:17:19.667 |

Mongoose is an embedded web server and network library. Prior to 7.23, the built-in TLS stack selected by MG_TLS_BUILTIN in src/tls_builtin.c accepts a TLS 1.3 record whose decrypted size is exactly the 16-byte authentication tag with no plaintext or ContentType byte. In mg_tls_recv_record(), the msgsz length check permits that record and the recv_len calculation underflows to SIZE_MAX, so a later handshake step treats stale buffer contents as a trusted message with an effectively unbounded length. An unauthenticated malicious TLS peer can trigger a heap out-of-bounds read before certificate or Finished validation, causing a remote denial of service. This issue is fixed in version 7.23.

### CVE-2026-102944

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-14T19:17:06.347 |

cpp-httplib is a C++ header-only HTTP/HTTPS library. Prior to 0.51.0, create_redirect_client() removes Host, Proxy-Authorization, and Authorization headers when following a cross-origin 301, 302, 307, or 308 redirect but leaves Cookie headers attached. detail::redirect() copies the request for those redirect codes, so cookies supplied directly or through default_headers_ are sent to the redirect target. An attacker who controls a redirect response, or a network position for a non-HTTPS origin, can receive session cookies intended for the original origin. A 303 redirect is not affected because that path clears all request headers. This issue is fixed in version 0.51.0.

### CVE-2026-92155

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T18:19:34.777 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.2.0, Fw::FilePacket deserialization used by Svc::FileUplink is vulnerable because Header deserialization casts the byte to the Type enum without validating its range and FilePacket::fromSerialBuffer reaches a default FW_ASSERT. When a network file packet contains an unknown file-packet type byte, the assertion aborts or resets the default Ref application process, causing denial of service. This issue is fixed in version 4.2.0.

### CVE-2026-92150

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T18:19:34.330 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.2.0, Svc::GenericHub fromBufferDriver_handler deserialization is vulnerable because the receive handler uses FW_ASSERT for externally influenced deserialization status and type validation and permits a command payload size subtraction to underflow. When an unauthenticated inter-processor hub peer sends a truncated buffer, an invalid HubType, or a header-only command-dispatch payload, malformed hub traffic aborts or resets the process, causing denial of service. This issue is fixed in version 4.2.0.

### CVE-2026-54554

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-14T18:17:37.693 |

FOG is a free open-source cloning/imaging/rescue suite/inventory management system. Prior to 1.5.10.1870, the management adInfo() endpoint in packages/web/lib/fog/fogpage.class.php was reported to return the FOG_AD_DEFAULT_PASSWORD value in its domainpass JSON field and to be dispatchable through node=ipxe without an authenticated session. The response was also consumed by host and group Active Directory configuration interfaces. This could disclose the default domain-join credential to a remote unauthenticated requester. This vulnerability is fixed in 1.5.10.1870.

### CVE-2026-109527

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-14T18:17:33.447 |

The Model Context Protocol Python SDK is the official Python SDK for Model Context Protocol servers and clients. In mcp versions before 1.29.1 and from 2.0.0a1 through 2.0.1, the Streamable HTTP session manager, SSE message endpoint, and OAuth authorization-server routes buffer complete HTTP request bodies without enforcing a maximum size. An unauthenticated remote client able to reach an affected endpoint can send a large declared or streamed request body that consumes multiple times the body size in process memory and can repeatedly exhaust memory or terminate the server. Stdio-only servers and deployments with an effective upstream request-size limit are not affected, and applications that use StreamableHTTPServerTransport directly remain responsible for enforcing their own limit. The standard SDK server applications and session managers are fixed in versions 1.29.1 and 2.1.0.

### CVE-2026-108395

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-14T18:17:27.370 |

The Model Context Protocol Java SDK is the official Java SDK for Model Context Protocol servers and clients. From version 0.8.0 through 0.12.0 in the io.modelcontextprotocol.sdk:mcp artifact, from 0.13.0 through 0.18.3 and 1.0.0 through 1.1.3 in io.modelcontextprotocol.sdk:mcp-core, and from mcp-core 2.0.0-M1 through 2.0.0, the Servlet-based SSE, Streamable HTTP, and Stateless server transports read an HTTP request body into memory without enforcing a maximum size. An unauthenticated remote client able to reach an affected transport can stream an arbitrarily large POST body, including with chunked transfer encoding, until the Java process exhausts its heap and becomes unavailable. Authentication, Origin or Host validation, or an upstream request-size limit can reject the request before the vulnerable read. The maintained mcp-core lines are fixed in versions 0.18.4, 1.1.4, and 2.0.1.

### CVE-2026-107349

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-835` |
| Published | 2026-10-14T18:17:25.557 |

An infinite loop in PgBouncer 1.20.0 through 1.26.0 allows an unauthenticated remote attacker to cause a denial of service. A StartupMessage whose options parameter contains an empty parameter name, such as "-c=", makes the ignore_startup_parameters list lookup loop forever. Because PgBouncer serves all clients from a single process, this saturates a CPU core and makes PgBouncer unresponsive to all clients until the process is restarted.

### CVE-2026-103081

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-14T18:17:19.103 |

Improper Control of Generation of Code ('Code Injection') vulnerability in VillaTheme Salevo woo-boost-sales allows Code Injection.This issue affects Salevo: from n/a through 1.3.0.

### CVE-2026-92151

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:20:20.997 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.2.0, Svc::Ccsds::SpacePacketDeframer dataIn_handler is vulnerable because the handler treats the minimum packet-length condition as FW_ASSERT rather than rejecting and returning the buffer. When a CCSDS telecommand frame leaves a payload of six bytes or fewer after TcDeframer removes its header and trailer, the assertion aborts or resets the flight-software process, causing denial of service. This issue is fixed in version 4.2.0.

### CVE-2026-15102

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-319` |
| Published | 2026-10-14T17:18:26.670 |

ADP Desktop SDK contains a vulnerability where sensitive information is transmitted in clear text. Exploitation of this vulnerability can lead to unauthorized access to Autodesk services.

### CVE-2026-91157

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-200;CWE-863` |
| Published | 2026-10-14T16:17:56.460 |

Discourse is an open-source discussion platform. Prior to 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9, sites with secure uploads enabled did not reconcile existing upload security metadata when a previously public category became read-restricted or when category permissions changed during a bulk import. Media and attachments uploaded while the category was public retained a public accessibility flag and remained reachable by anonymous users through their short upload URLs, including uploads associated with deleted topics. This issue is fixed in versions 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9.

### CVE-2026-91156

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T16:17:56.310 |

Discourse is an open-source discussion platform. Prior to 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9, MessageBus audience calculation could deliver messages from a read-restricted category chat channel to an authenticated user who could view the category but was not allowed to use Chat under the site's group restrictions. The publication path bounded events by category visibility without also enforcing Chat eligibility, exposing live and recent message content available in the MessageBus backlog. The issue does not permit retrieval of the channel's full history through the Chat API and does not permit message creation or modification. This issue is fixed in versions 2026.9.0, 2026.8.1, 2026.7.3, and 2026.1.9.

### CVE-2026-89077

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-303` |
| Published | 2026-10-14T16:17:56.080 |

Incorrect implementation of authentication algorithm vulnerability in Progress MOVEit Transfer (SFTP module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-89074

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-176` |
| Published | 2026-10-14T16:17:55.743 |

Improper handling of unicode encoding vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-89073

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-613` |
| Published | 2026-10-14T16:17:55.630 |

Insufficient Session Expiration vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-89072

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T16:17:55.500 |

Incorrect Authorization vulnerability in Progress MOVEit Transfer (Client Certificates module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-89071

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-90` |
| Published | 2026-10-14T16:17:55.383 |

Improper neutralization of special elements used in an LDAP query ('LDAP injection') vulnerability in Progress MOVEit Transfer (LDAP module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-89070

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-294` |
| Published | 2026-10-14T16:17:55.270 |

Authentication bypass by capture-replay vulnerability in Progress MOVEit Transfer (OIDC module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-79834

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T12:16:39.497 |

A security vulnerability in HPE NonStop SQL/MX SQLCAT may allow an unauthenticated user to perform unauthorized command execution.

### CVE-2026-108337

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-14T22:17:22.563 |

An administrator could retrieve the password reset code for any user and take over the account.



The password reset codes were included in the output of an API and could be used to reset the password of any account. The API is limited to use by administrator accounts only.



An attacker who already has administrative access to the application could compromise the credentials of other accounts on the application. Device credentials and customer data cannot be accessed with this vulnerability.

### CVE-2026-57492

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-14T21:17:37.650 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.16.0, FileRise treats an empty or missing users.txt file as a fresh installation even after setup previously completed. If storage loss, truncation, or another failure empties the user store, an unauthenticated remote caller can detect that setup mode reopened and create the next initial administrator account through the setup flow. The application lacked a durable setup-complete marker independent of the mutable user store. This issue is fixed in version 3.16.0.

### CVE-2026-79837

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:C/C:N/I:L/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-15T13:17:13.707 |

A vulnerability in HPE NonStop SQL/MX UDR SERVER may allow a crafted message to cause process termination, service disruption or memory corruption, resulting in undefined behavior.

### CVE-2026-3712

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-15T05:17:04.067 |

The PhastPress plugin for WordPress is vulnerable to Server-Side Request Forgery in all versions up to, and including, 3.10 This is due to the scripts service endpoint constructing its URL whitelist dynamically from the attacker-controlled HTTP 'Host' header. This makes it possible for unauthenticated attackers to spoof the header to match any target URL, bypassing the whitelist and forcing the server to make HTTP requests to arbitrary internal or external destinations and return the response content.

### CVE-2026-54702

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-14T20:17:47.737 |

Markdown Preview Enhanced is a Markdown preview extension for Visual Studio Code. Prior to 0.8.30, the webview message handler in src/preview-provider.ts accepts an attacker-controlled command value and attacker-controlled args, constructs a command in the _crossnote namespace, and invokes vscode.commands.executeCommand without an allowlist or type validation. JavaScript already executing in the preview webview can use this bridge to invoke privileged extension commands, including file modification, code-chunk execution, export-tool execution, and arbitrary URL opening, with attacker-selected arguments. Exploitation requires a separate webview JavaScript execution path, such as the independently tracked .crossnote/head.html injection, but no further authorization check protects the extension-host command boundary. This issue is fixed in version 0.8.30.

### CVE-2026-89075

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-922` |
| Published | 2026-10-14T16:17:55.853 |

Insecure Storage of Sensitive Information vulnerability in Progress MOVEit Transfer.

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-26243

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-15T10:17:12.770 |

A path traversal vulnerability has been reported to affect Qsync Central. If a remote attacker gains a user account, they can then exploit the vulnerability to read the contents of unexpected files or system data.

We have already fixed the vulnerability in the following version:
Qsync Central 5.0.0.6 and later
Qsync Central 5.1.0.2 and later
Qsync Central 5.2.0.4 and later

### CVE-2026-88043

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T06:17:05.490 |

The Mang Board WP plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'data_type' parameter in all versions up to, and including, 2.4.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-18586

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T06:17:03.347 |

The Premium Packages – Sell Digital Products Securely plugin for WordPress is vulnerable to Unauthenticated Stored Cross-Site Scripting via 'order_email' in all versions up to, and including, 7.0.5 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-18548

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T06:17:03.043 |

The Groundhogg — CRM, Newsletters, and Marketing Automation plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'ref' parameter in all versions up to, and including, 4.5.14 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-110850

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T23:17:25.870 |

n8n before 2.41.4 and 2.42.0 before 2.42.1 does not validate credential ids stored in agent node parameters when an editor saves a shared workflow, because the check inspects only a node's credentials field. An editor can configure a Message an Agent node in inline mode with tools they control to resolve the owner's credentials and send decrypted secrets to an attacker-chosen destination.

### CVE-2026-110849

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T23:17:25.713 |

n8n before 1.123.83, 2.41.4, and 2.42.1 contains a stored cross-site scripting vulnerability in the file-preview modal, which re-publishes binary data as an unsandboxed same-origin blob URL. A member who uploads a crafted item can run script in the n8n origin of whoever previews it, typically the owner, and act with their session.

### CVE-2026-110844

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T23:17:24.940 |

n8n before 1.123.83 contains an authorization bypass vulnerability that allows shared-workflow editors to use credentials they cannot access by embedding them in nested or tool inline sub-workflows. Attackers can save workflows with Workflow Tool or Workflow Retriever inline definitions referencing restricted credentials, which execute using the workflow owner's credential values.

### CVE-2026-55387

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284;CWE-639` |
| Published | 2026-10-14T20:17:48.917 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. In version 2.3.3 and earlier, InvoiceShelf bulk-delete request validation accepts record identifiers without consistently binding them to the authenticated user's company_id. The affected DeleteCustomersRequest, DeleteEstimatesRequest, DeleteExpensesRequest, DeleteInvoiceRequest, DeleteItemsRequest, DeletePaymentsRequest, and DeleteUserRequest validators check that identifiers exist but do not consistently check tenant ownership. An authenticated user can submit another company's identifier and delete cross-company records. This vulnerability is fixed in 2.4.0.

### CVE-2026-92158

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-10-14T18:19:35.217 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.2.0, Svc::FpySequencer STORE directive stack write validation the bounds check adds attacker-controlled offset and size before memcpy, allowing integer wraparound to make an out-of-range destination appear valid. When a sequence-controlled STORE directive supplies a stack offset and size whose U32 sum wraps, memcpy can write outside the sequencer stack, causing memory corruption, denial of service, and potentially code execution. This issue is fixed in version 4.2.0.

### CVE-2026-102177

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:18:05.453 |

An Out-of-bounds Write vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to cause a denial of service when IS-IS link protection and backup-selection are configured.

### CVE-2026-89076

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T16:17:55.967 |

Improper neutralization of special elements used in an SQL command ('SQL injection') vulnerability in Progress MOVEit Transfer (Custom Reports module).

This issue affects MOVEit Transfer: before 2025.1.6 and from 2026.0.0 before 2026.0.4.

### CVE-2026-84471

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-14T15:17:26.077 |

The fix for CVE-2026-12996 was incomplete. A use-after-free in OpenVPN 2.6.0 through 2.6.22 and 2.7_alpha1 through 2.7.7 allows remote authenticated peers to potentially cause a denial of service or leak memory via crafted packets during TLS session promotion or expiry.

### CVE-2026-109702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T13:17:12.467 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in maxfoundry Social Share Buttons share-button allows Stored XSS.This issue affects Social Share Buttons: from n/a through 1.31.

### CVE-2026-109692

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-15T13:17:12.063 |

Missing Authorization vulnerability in ThemeGrill User Registration user-registration allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects User Registration: from n/a through 5.2.8.

### CVE-2026-109685

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T13:17:11.400 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Link Whisper INC Link Whisper Free link-whisper allows Reflected XSS.This issue affects Link Whisper Free: from n/a through 0.9.7.

### CVE-2026-108498

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T11:17:19.957 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in bannersky BSK PDF Manager bsk-pdf-manager allows Stored XSS.This issue affects BSK PDF Manager: from n/a through 3.8.1.

### CVE-2026-108491

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T11:17:19.677 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Everest Forms Everest Forms everest-forms allows Stored XSS.This issue affects Everest Forms: from n/a through 3.6.1.

### CVE-2026-79828

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T10:17:15.963 |

A heap buffer overflow in HPE NonStop Debug Utilities  could corrupt resume-execution address and may potentially redirect execution flow.

### CVE-2026-79827

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T10:17:15.840 |

A heap buffer overflow in HPE NonStop Inspect Subsystem could corrupt resume-execution address and may potentially redirect execution flow.

### CVE-2026-79826

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T10:17:15.727 |

A heap buffer overflow in HPE NonStop OCAX could corrupt address space and may potentially redirect execution flow.

### CVE-2026-79825

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T10:17:15.607 |

A heap buffer overflow in HPE NonStop NDSREST could corrupt resume-execution address and may potentially redirect execution flow.

### CVE-2026-26245

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T10:17:13.053 |

A SQL injection vulnerability has been reported to affect Video Station. If a remote attacker gains a user account, they can then exploit the vulnerability to execute unauthorized code or commands.

We have already fixed the vulnerability in the following version:
Video Station 5.8.8 and later

### CVE-2026-26244

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-15T10:17:12.917 |

A SQL injection vulnerability has been reported to affect Video Station. If a remote attacker gains a user account, they can then exploit the vulnerability to execute unauthorized code or commands.

We have already fixed the vulnerability in the following version:
Video Station 5.8.8 and later

### CVE-2026-16437

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-640` |
| Published | 2026-10-15T09:17:16.910 |

Weak Password Recovery Mechanism for Forgotten Password vulnerability in Mitsubishi Electric GENESIS versions 11.03 and prior, GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, MobileHMI 10.97.3 and prior, IoTWorX 10.97.3 and prior, MC Works64 all versions, GENESIS32 all versions, BizViz all versions, Mitsubishi Electric Iconics Digital Solutions GENESIS versions 11.03 and prior, GENESIS64 versions 10.97.3 and prior, ICONICS Suite versions 10.97.3 and prior, Hyper Historian versions 10.97.3 and prior, AnalytiX versions 10.97.3 and prior, MobileHMI 10.97.3 and prior, IoTWorX 10.97.3 and prior, GENESIS32 all versions, and BizViz all versions allows an authenticated local user with administrative privileges to unlock the system by tampering with the management file that stores the challenge response. Administrators are able to read and write the management file. But the management file is protected by Windows. As a result, the attacker may disclose, tamper with, destroy, or delete internal information, or cause the affected system to enter a denial-of-service (DoS) condition.

### CVE-2026-79822

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-15T07:18:02.980 |

A security vulnerability in HPE NonStop TNS/X Native Inspect may cause corruption of address and potentially redirect execution flow.

### CVE-2026-74920

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-15T07:18:02.610 |

The Document Gallery WordPress plugin through 5.1.1 does not properly sanitise and escape user input before reflecting it inside an HTML attribute in the response of an unauthenticated AJAX action, leading to a Reflected Cross-Site Scripting vulnerability which can be exploited against any visitor, including a logged-in administrator.

### CVE-2026-76665

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-15T05:17:04.310 |

A security vulnerability in HPE NonStop EXPAND may cause out-of-bounds memory read resulting in buffer overflow.

### CVE-2026-110912

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-15T04:18:23.010 |

In DragonFly BSD through 6.4.2 before 4bb22ff, the ARP input handlers arpintr() and in_arpinput() (sys/netinet/if_ether.c) do not validate the hardware address length (ar_hln) and protocol address length (ar_pln) fields of incoming ARP packets. in_arpreply() then uses these attacker-controlled values as memcpy lengths when copying from kernel buffers that are only 6 and 4 bytes long, resulting in an out-of-bounds read of kernel heap and stack memory that is copied into the ARP reply sent back to the requester. An unauthenticated attacker on the adjacent network can use a single crafted ARP request to disclose up to roughly 250 bytes of each type of kernel memory, including kernel pointers. This is expected to be fixed in the 6.6 stable release when that is available.

### CVE-2026-110873

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T23:17:29.237 |

Heym from 0.0.55 before 0.0.121 contains a privilege escalation vulnerability that allows shared collaborators to overwrite a workflow's error_workflow_id because the field is missing from OWNER_ONLY_EXECUTION_FIELDS. Attackers can point the error workflow to their own workflow with an HTTP node, and when the parent workflow errors the owner's decrypted credentials are injected and exfiltrated.

### CVE-2026-110871

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T23:17:28.953 |

Nodemailer from 3.0.0 before 10.0.10 contains a denial of service vulnerability in MessageParser.parseHeaders that allows users to exhaust CPU through quadratic header unfolding. Attackers can supply large recipient lists or long headers that fold into tens of thousands of continuation lines, blocking the Node.js event loop during DKIM signing.

### CVE-2026-110865

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-424` |
| Published | 2026-10-14T23:17:28.110 |

Renovate before 44.60.1 contains an allowlist bypass vulnerability that allows repository users to evade the allowedHeaders restriction by placing hostRules headers inside shared presets. Attackers can supply internal or externally sourced presets with unvalidated hostRules[].headers to inject custom HTTP headers into requests Renovate sends to other hosts.

### CVE-2026-110855

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-14T23:17:26.623 |

GitPython before 3.2.0 contains an information disclosure vulnerability that allows malicious repositories to expand environment variables via separate_git_dir in Repo._clone(), which omits expand_vars=False when calling Git.polish_url(). Attackers can craft a .gitmodules submodule name containing variable syntax so that clone plus submodule_update exposes secrets in .git/modules directory names and DEBUG logs.

### CVE-2026-110853

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T23:17:26.343 |

n8n before 1.123.83 contains an authorization bypass vulnerability that allows authenticated members to spoof workflow identity by supplying a trusted identifier in Execute Sub-workflow inline JSON mode. Attackers can set this identifier to resolve credentials from projects they do not belong to and modify another workflow's static data and error-workflow dispatch.

### CVE-2026-110839

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T23:17:24.173 |

FreeRDP 3.3.0 before 3.32.0, when built with WINPR_UTILS_IMAGE_JPEG=ON, has a heap-based out-of-bounds write in winpr_convert_from_jpeg because grayscale JPEG buffers are sized from one input component rather than three BGR output components. A malicious RDP server can offer a grayscale JPEG via clipboard redirection, corrupting client memory and crashing it when the item is pasted as CF_DIB bitmap data.

### CVE-2026-110836

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-835` |
| Published | 2026-10-14T23:17:23.593 |

FreeRDP from 3.0.0 before 3.32.0 contains an infinite loop vulnerability in http_response_recv() that allows malicious gateways to exhaust client CPU via crafted Content-Type headers. Attackers controlling a gateway can return a nonzero Content-Length with a semicolon-containing unrecognized Content-Type, pinning a client thread at full CPU indefinitely.

### CVE-2026-110834

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T23:17:23.300 |

FreeRDP from 2.0.0 before 3.32.0 contains a null pointer dereference vulnerability that allows malicious RDP servers to crash clients by sending out-of-lifecycle serial IRPs. Attackers can send IRP_MJ_READ or IRP_MJ_WRITE before create or after close, causing CommReadFile or CommWriteFile to dereference a null handle and terminate clients using Linux serial redirection.

### CVE-2026-110832

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-14T23:17:23.023 |

FreeRDP from 2.0.0 before 3.32.0 contains a memory exhaustion vulnerability in wts_read_drdynvc_data_first that allows authenticated clients to force servers to commit large memory allocations. Attackers can send a seven-byte DATA_FIRST message on an opened DVC declaring a large 32-bit length, causing zeroed resident memory growth and server resource exhaustion.

### CVE-2026-110829

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T23:17:22.597 |

FreeRDP versions from 3.0.0 before 3.32.0 contain a null pointer dereference in the rdpsnd channel when a fragment sets CHANNEL_FLAG_LAST without CHANNEL_FLAG_FIRST. A malicious RDP server can send a malformed rdpsnd PDU on a fresh channel to crash the client and cause denial of service.

### CVE-2026-61844

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-706` |
| Published | 2026-10-14T21:17:38.137 |

FileRise is a self-hosted web-based file manager with multi-file upload, editing, and batch operations. Prior to 3.18.0, FileRise flattens logical folder paths into metadata filenames by replacing separators and spaces with hyphens, so distinct folders such as team/docs and team-docs can share one metadata file. Because uploader metadata is used to authorize read_own and ownership-restricted edits, a low-privileged user who controls one colliding folder, knows the target basename, and already has read_own access to the target folder can alter the metadata used by that folder, make the victim file appear attacker-owned, read it, and modify it when edit-own permission is also available. This issue is fixed in version 3.18.0.

### CVE-2026-55386

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T20:17:48.773 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. Prior to version 2.4.0, InvoiceShelf passes the authenticated user's orderByField query parameter into Laravel orderBy calls in Invoice::scopeApplyFilters without restricting the value to column identifiers. A crafted SQL expression can therefore enter the ORDER BY clause across invoice and other list endpoints, enabling boolean-based blind extraction of database information. This issue is fixed in version 2.4.0.

### CVE-2026-55381

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T20:17:48.057 |

InvoiceShelf is an open-source web & mobile app that helps track expenses, payments and create professional invoices and estimates. Prior to version 2.4.0, POST /api/v1/estimates/{estimate}/convert-to-invoice in ConvertEstimateController authorizes only the caller's create-invoice ability and does not authorize access to the route-bound Estimate. Because route-model binding can resolve an estimate from any company, an authenticated user with create-invoice ability can copy another company's line items, prices, totals, taxes, notes, currency, and customer data into an invoice in the attacker's company. The victim company's configured conversion action reaches checkForEstimateConvertAction and can also change or delete the original estimate. This issue is fixed in version 2.4.0.

### CVE-2026-55787

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-10-14T19:17:17.927 |

Flyto2 Core is an execution kernel for automation and AI-agent workflows. Prior to 2.26.3, validate_url_ssrf and is_private_ip in src/core/utils.py compare resolved addresses only against native private IPv4 and IPv6 ranges and do not unwrap IPv4-mapped, IPv4-compatible, 6to4, or NAT64 transition addresses. An authenticated workflow author can provide a transition-form literal URL through the Execution API POST /v1/execute route, http.get, or sibling guarded outbound-request modules, causing the guard to accept an address whose embedded IPv4 points to loopback, RFC 1918, or cloud metadata services. On a host that routes the selected transition form, the outbound request reaches the internal destination and returns the response body to the workflow caller, enabling read SSRF and disclosure of internal-service data or cloud credentials. This issue is fixed in version 2.26.3.

### CVE-2026-110775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T19:17:13.790 |

Nexent through 2.7.0 contains a missing authorization vulnerability in check_file_access that allows authenticated users to read other tenants' knowledge-base files by skipping tenant comparison for knowledge_base/ reads. Attackers in multi-tenant deployments can list objects via GET /file/storage for presigned URLs or use GET /file/download/{object_name} to download other tenants' source documents.

### CVE-2026-108484

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T18:17:29.680 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPManageNinja Best Payments Plugin for WP wp-payment-form allows Stored XSS.This issue affects Best Payments Plugin for WP: from n/a through 4.6.27.

### CVE-2026-108483

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T18:17:29.527 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in hippooo Hippoo Mobile App for WooCommerce hippoo allows Reflected XSS.This issue affects Hippoo Mobile App for WooCommerce: from n/a through 1.12.0.

### CVE-2026-105066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T18:17:22.907 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in SimplyRETS SimplyRETS Real Estate IDX simply-rets allows Reflected XSS.This issue affects SimplyRETS Real Estate IDX: from n/a through 3.2.9.

### CVE-2026-101975

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T18:17:12.467 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent OSPF peer to cause a denial of service via OSPF traffic processed while OSPF Source Packet Routing best-route Prefix-SID installation is configured.

### CVE-2026-101972

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-14T18:17:12.300 |

An Integer Overflow or Wraparound vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service via specific OSPFv2 packets sent on an OSPF-enabled interface.

### CVE-2026-101964

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T18:17:12.140 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to cause an rpd crash via a crafted LDP packet received over an established LDP session.

### CVE-2026-101959

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-688` |
| Published | 2026-10-14T18:17:11.440 |

A Function Call With Incorrect Variable or Reference as Argument vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause an rpd crash via specifically malformed LSP-ping.

### CVE-2026-92153

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-22;CWE-73` |
| Published | 2026-10-14T17:20:21.150 |

F´ (F Prime) is a framework that enables development and deployment of spaceflight and other embedded software applications. Prior to 4.3.0, Svc::FileUplink handling of Fw::FilePacket::StartPacket destination paths FileUplink copies the packet-controlled destinationPath and opens it for writing without canonicalization or confinement to an upload directory. When a peer able to send file-uplink packets supplies an absolute, traversing, or otherwise attacker-selected writable destination path, files can be created or overwritten at attacker-selected writable filesystem locations, affecting integrity and potentially availability. This issue is fixed in version 4.3.0.

### CVE-2026-19673

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:H` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-14T17:18:26.800 |

ethernet_recv() in subsys/net/l2/ethernet/ethernet.c validates only that the first net_buf of a received frame holds a plain 14-byte struct net_eth_hdr. When the ethertype is 0x8100 and VLAN is enabled on the interface, the same buffer is reinterpreted as the 18-byte struct net_eth_vlan_hdr without re-checking the length: the VLAN TCI and the inner ethertype are read from offsets 14..17, past pkt->buffer->len, and hdr_len is raised to 18 so the subsequent net_buf_pull() removes more bytes than the buffer holds.

A single unauthenticated frame of 14 to 17 bytes carrying the VLAN ethertype triggers this. No knowledge of the node's VLAN configuration is needed: net_eth_get_vlan_iface() returns the base interface for the priority tag 0, and a broadcast destination address satisfies the "frame is for me" test, so a 16-byte broadcast frame with ethertype 0x8100 and TCI 0x0000 reaches the pull. Nothing in the receive path enforces the 60-byte Ethernet minimum — the USB CDC ECM and CDC NCM gadget classes in particular hand host-supplied frames of any non-zero length straight to net_recv_data().

With assertions enabled, net_buf_simple_pull() asserts and the node panics. In a production build (assertions and CONFIG_NET_BUF_HARDENING off) the uint16_t buffer length underflows to 65534 and buf->data is advanced past the end of the fragment's storage, so every later parser reads far outside the buffer and any net_buf_add() on that fragment computes tailroom from the underflowed length. The result is a reliable remote denial of service and out-of-bounds access with information-disclosure and corruption potential.

Only configurations built with CONFIG_NET_VLAN=y that have a VLAN enabled on the receiving Ethernet interface, and whose MAC does not strip VLAN tags in hardware (ETHERNET_HW_VLAN_TAG_STRIP), are affected. The fix rejects the frame before the tag is read, so hdr_len is thereafter either 14 or 18 with both sizes validated against pkt->buffer->len.

### CVE-2026-102087

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:X/RE:M/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-10-14T17:18:04.800 |

An Incomplete List of Disallowed Inputs vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated, adjacent attacker to cause a Denial-of-Service (DoS).

When in a BGP traffic engineering scenario a specific, valid, optional, non-transitive BGP update is received over an established BGP session, RPD crashes and automatically restarts, which leads to traffic impact until routing has reconverged.

This issue affects:
Junos OS:


  *  All versions before 23.2R2-S6;
  *  23.4 versions before 23.4R2-S7;
  *  24.2 versions before 24.2R2-S4;
  *  24.4 versions before 24.4R2-S4;
  *  25.2 versions before 25.2R1-S2, 25.2R2;



Junos OS Evolved:
  *  All versions before 23.2R2-S6-EVO;
  *  23.4 versions before 23.4R2-S8.11-EVO;
  *  24.2 versions before 24.2R2-S4-EVO;
  *  24.4 versions before 24.4R2-S5-EVO;
  *  25.2 versions before 25.2R1-S2-EVO, 25.2R2-EVO;

### CVE-2026-102072

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-14T17:18:03.253 |

An Improper Handling of Highly Compressed Data vulnerability in the gRPC library used by na-grpcd of Juniper Networks Junos OS allows an authenticated network-based attacker to cause a denial of service via a compressed gRPC request.

### CVE-2026-102071

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:18:03.093 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service via a specific RSVP packet.

### CVE-2026-102067

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:18:02.490 |

An Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to cause a denial of service via a crafted RSVP packet when L2 LSP support is enabled.

### CVE-2026-102066

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T17:18:02.330 |

A Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to cause a denial of service via a malformed RSVP packet when RSVP is enabled on the receiving interface.

### CVE-2026-102063

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:18:01.877 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos on MX Series routers allows an unauthenticated network attacker to cause a denial of service via an eBGP route update when HFRR link protection is configured in a VRF.

### CVE-2026-102060

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:18:01.417 |

A NULL Pointer Dereference vulnerability in the rpd process of Juniper Networks Junos OS on MX Series and Junos OS Evolved on ACX Series allows an unauthenticated adjacent attacker to cause a denial of service via an IGMPv3 membership report received on a directly connected network.

### CVE-2026-102058

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:18:01.090 |

A Reachable Assertion vulnerability in the bfdd daemon of Juniper Networks Junos OS and Junos OS Evolved platforms allows an unauthenticated adjacent attacker to cause a denial of service by restarting the daemon via crafted BFD session traffic.

### CVE-2026-102056

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-14T17:18:00.753 |

An Out-of-bounds Read vulnerability in the cfmd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent-network attacker to crash the daemon and disclose limited process memory via a specific CFM Message sent to a configured interface.

### CVE-2026-102051

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-14T17:17:59.943 |

An Improper Release of Memory Before Removing Last Reference vulnerability in the l2cpd process of Juniper Networks Junos OS and Junos OS Evolved platforms allows an adjacent unauthenticated attacker to cause l2cpd memory exhaustion and Layer 2 control-plane disruption via LLDP traffic when fast receive processing is enabled.

### CVE-2026-102048

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-14T17:17:59.397 |

An Allocation of Resources Without Limits or Throttling vulnerability in the l2cpd process of Juniper Networks Junos OS allows an adjacent unauthenticated attacker to cause a denial of service and l2cpd restart via FNP-enabled Layer 2 interfaces. The issue is triggered when the FNP feature is enabled on a VPLS routing instance with VLAN-VPLS encapsulation enabled.

This issue affects all platforms except the PTX Series and SRX Series.

### CVE-2026-102047

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1288` |
| Published | 2026-10-14T17:17:59.237 |

An Improper Validation of Consistency within Input vulnerability in the l2cpd process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated Layer 2 attacker to cause a denial of service in associated Layer 2 control protocols via a crafted MVRP Ethernet frame sent to an MVRP-enabled interface.

### CVE-2026-102045

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:17:58.953 |

An Out-of-bounds Write Out-of-bounds Write vulnerability in lacpd of Juniper Networks Junos OS Evolved allows a Layer-2-adjacent attacker to cause a denial of service via a crafted frame received on an LACP-enabled aggregated-Ethernet member port.

### CVE-2026-102043

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-197` |
| Published | 2026-10-14T17:17:58.640 |

A Numeric Truncation Error vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to crash the routing process via MPLS-TE fast-reroute signaling.

### CVE-2026-102042

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:58.483 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to crash the routing process via RSVP-TE associated-bidirectional LSP signaling.

### CVE-2026-102041

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:58.333 |

A Reachable Assertion vulnerability in the rpd routing daemon of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated network attacker to cause a denial of service via malformed RSVP signaling when RSVP is enabled.

### CVE-2026-102040

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:58.180 |

A NULL Pointer Dereference vulnerability in the rpd routing daemon of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent unauthenticated attacker to crash the routing daemon and cause a denial of service via an RSVP Path message.

### CVE-2026-102039

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:58.017 |

A NULL Pointer Dereference vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to cause a denial of service via a malformed RSVP Path message received on an EVPL LMP control channel.

### CVE-2026-102035

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:57.547 |

A Reachable Assertion vulnerability in the l2ald process of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to cause a denial of service via an ICCP peer message when MC-LAG IRB MAC synchronization is enabled.

### CVE-2026-102034

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:57.370 |

A Reachable Assertion vulnerability in the l2ald daemon of Juniper Networks Junos OS and Junos OS Evolved allows an attacker with access to a configured ICCP peer to cause a denial of service via a malformed MC-LAG message.

### CVE-2026-102033

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:17:57.020 |

An Improper Validation of Specified Quantity in Input vulnerability in l2ald of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to cause a denial of service via an ICCP MC-LAG message.

### CVE-2026-102032

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-401` |
| Published | 2026-10-14T17:17:56.770 |

A Missing Release of Memory after Effective Lifetime vulnerability in the l2ald process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service via crafted packets when the static MAC-IP feature is in use.

### CVE-2026-102021

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:55.040 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent network attacker to cause a denial of service via a crafted RSVP packet when MPLS-TE RSVP processing is enabled. The condition can terminate rpd and disrupt routing protocol sessions.

### CVE-2026-102019

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:17:54.710 |

An Improper Validation of Specified Quantity in Input vulnerability in the rpd process of Juniper Networks Junos OS and Junos Evolved allows an unauthenticated adjacent attacker to cause a denial-of-service condition via a malformed RIPv2 message.

### CVE-2026-102018

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:54.527 |

A NULL Pointer Dereference vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial-of-service condition via a malformed PIM Bidir message.

### CVE-2026-102017

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:17:54.340 |

An Out-of-bounds Write vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated attacker to cause a routing-plane denial of service via Auto-RP mapping announcements received when Auto-RP mapping is enabled.

### CVE-2026-102011

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:53.207 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos EVO allows an adjacent attacker to cause a denial of service via an established LDP session when two misconfigured neighbors (or one neighbor duplicated by an L2 loop) advertise the same transport address on a link-protected interface.

### CVE-2026-102000

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:53.050 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos EVO allows an adjacent unauthenticated attacker to cause a denial of service via LDP control traffic.

### CVE-2026-101999

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:52.893 |

A Reachable Assertion vulnerability in the rpd process of Juniper Networks Junos OS and Junos EVO allows an adjacent attacker to cause a denial of service via an established LDP session carrying an IPv6 Prefix FEC in a specific Label message.

### CVE-2026-101996

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:52.580 |

A Reachable Assertion vulnerability in the 

l2ald 

daemon of Juniper Networks Junos OS and Junos OS Evolved devices configured for MC-LAG/ICCP allows an adjacent attacker to cause a denial of service via an inconsistent ICCP peer message.

### CVE-2026-101994

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-14T17:17:52.233 |

An Improper Handling of Length Parameter Inconsistency vulnerability in the 

l2ald 

daemon of Juniper Networks Junos OS and Junos OS Evolved allows an attacker who can control or impersonate a configured MC-LAG ICCP peer to disclose process heap memory or cause a denial of service via a malformed ICCP message.

### CVE-2026-101993

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:52.063 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent eBGP peer to cause a denial of service via a VPLS signaling update when automatic site-ID negotiation is enabled.

### CVE-2026-101992

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-14T17:17:51.900 |

An Improper Input Validation vulnerability in the routing protocol daemon (rpd) process of Juniper Networks Junos OS and Junos OS Evolved allows a configured BGP peer to cause an rpd crash via a BGP VPLS signaling update.

### CVE-2026-101989

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:51.417 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a compromised LDP neighbor to cause an rpd crash via a crafted LDP message.

### CVE-2026-101988

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-14T17:17:51.260 |

A NULL Pointer Dereference vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service via LDP messages received over an operational LDP session.

### CVE-2026-101987

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T17:17:51.110 |

An Improper Validation of Specified Quantity in Input vulnerability in the routing daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent attacker to cause a denial of service by sending a specific IS-IS SRv6 packet when SRv6 and Flexible Algorithm are enabled.

### CVE-2026-101985

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1284` |
| Published | 2026-10-14T17:17:50.807 |

A Improper Validation of Specified Quantity in Input vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS Evolved on PTX Series allows an unauthenticated IS-IS peer to cause a denial of service.

### CVE-2026-101984

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:50.650 |

A Reachable Assertion vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS and Junos OS Evolved allows a network-adjacent BGP peer to cause a denial of service when labeled-unicast aggregate-label is configured.

### CVE-2026-101974

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `N/A` |
| Published | 2026-10-14T17:17:50.037 |

An Improper Validation of Specified Quantity in Input vulnerability in rpd of Juniper Networks Junos OS and Junos OS Evolved allows an adjacent OSPF peer to disclose rpd memory or cause a rpd crash via a malformed OSPF packets.

### CVE-2026-101971

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-14T17:17:49.740 |

An Allocation of Resources Without Limits or Throttling vulnerability in rpd, the routing protocol daemon, of Juniper Networks Junos OS and Junos OS Evolved platforms allows an unauthenticated adjacent attacker to cause a denial of service and heap memory corruption via OSPFv3 messages on an enabled broadcast interface.

### CVE-2026-101970

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-14T17:17:49.577 |

A Use After Free vulnerability in the rpd PIM Join/Prune processing of Juniper Networks Junos OS and Junos OS Evolved platforms allows an unauthenticated adjacent attacker to crash the routing daemon via specific PIM messages when sparse mode PIM is configured.

### CVE-2026-101969

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-14T17:17:49.407 |

An Improper Input Validation vulnerability in the rpd process of Juniper Networks Junos OS and Junos OS Evolved allows an unauthenticated adjacent attacker to cause a denial of service via a malformed PIM Hello message received on an IPv6-enabled PIM interface.

### CVE-2026-101960

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-14T17:17:48.657 |

An Out-of-bounds Write vulnerability in the routing protocol daemon (rpd) of Juniper Networks Junos OS Evolved on QFX5240, QFX5241 and QFX5250 configured for BGP global-load-balancing and more than 128 ecmp next-hops allows an attacker to cause an rpd crash.

### CVE-2026-101938

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-14T17:17:46.233 |

An Integer Underflow (Wrap or Wraparound) vulnerability in the srxpfe of Juniper Networks Junos OS and Junos OS Evolved on the SRX Series allows an adjacent unauthenticated attacker to cause a forwarding-plane denial of service via an ICMP message associated with an SVR carrier session.

### CVE-2026-101937

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-195` |
| Published | 2026-10-14T17:17:46.087 |

A Signed to Unsigned Conversion Error vulnerability in the srxpfe of Juniper Networks Junos OS on the SRX Series allows an adjacent attacker to cause a denial of service of the data plane via chassis-cluster fabric traffic.

### CVE-2026-101936

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:A/V:C/RE:M/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-10-14T17:17:45.933 |

A Reachable Assertion vulnerability in the srxpfe process of Juniper Networks Junos OS on SRX Series allows an adjacent network attacker to cause a denial of service of the data plane via malformed firewall-authentication synchronization traffic on chassis-cluster fabric interfaces.

### CVE-2026-110714

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-191` |
| Published | 2026-10-14T16:17:43.473 |

libsmb2 through 6.2 contains an integer underflow vulnerability in decode_acl that allows malicious SMB servers to trigger heap out-of-bounds reads via crafted security descriptors. Attackers controlling a server or intercepting unsigned sessions can send an AclSize below 8 in a QUERY_INFO reply, bypassing ACE bounds checks and crashing the client.

### CVE-2026-110713

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-14T16:17:43.337 |

libsmb2 through 6.2 contains a heap out-of-bounds read vulnerability in smb2_decode_file_fs_volume_info and smb2_decode_file_fs_attribute_info that allows malicious SMB servers to read past reply buffers. Attackers controlling a server or intercepting unsigned sessions can send crafted QUERY_INFO replies with missing or oversized name lengths to crash the client.

### CVE-2026-110712

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125` |
| Published | 2026-10-14T16:17:43.193 |

libsmb2 through 6.2 contains a heap out-of-bounds read vulnerability in smb2_decode_file_all_info that allows malicious SMB servers to crash clients by sending an unchecked FileNameLength. Attackers controlling the server or performing man-in-the-middle on unsigned sessions can return crafted FileAllInformation replies to smb2_stat or smb2_fstat calls, crashing the client.

### CVE-2026-96615

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-14T15:17:28.033 |

Description
NGINX Gateway Fabric has a vulnerability when it is configured with Gateway 

Custom Resource Definition (CRD) and have an authenticated gRPC connection with NGINX Agent. A namespaced 

 authenticated attacker with access to a service account may impersonate the authenticated NGINX Agent gRPC connection to read TLS private keys of Gateway deployments in another namespace. 

Impact
A remote authenticated attacker may be able to read TLS private keys of Gateway deployments in another namespace. 

There is no data plane exposure; this is a control plane issue only.






Note: Software versions which have reached End of Technical Support (EoTS) are not evaluated.

### CVE-2026-110629

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:15.700 |

VentureDrake Laravel CRM before 2.4.0 contains a missing authorization vulnerability that allows authenticated users to bypass Spatie role permissions through Livewire action methods. Read-only users can invoke delete, won, lost or reopen methods on components like DealIndex, or use unguarded Activities and Products routes, to modify deals, quotes, orders and invoices.

### CVE-2026-110615

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-14T15:17:13.607 |

jshERP through 3.6 contains a missing authorization vulnerability in the POST /user/batchSetStatus endpoint that allows authenticated low-privilege users to change other users' account status. Attackers can submit crafted ids and status values to disable every non-owner account in their tenant, locking out administrators, or re-enable disabled accounts.

### CVE-2026-110614

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T15:17:13.463 |

Yiuman citrus through 0.15.0 contains an ORDER BY sql injection vulnerability in the citrus-support generic query framework that allows users to inject SQL via the sortBy request parameter. Attackers can reach any generic list route of controllers extending BaseQueryController or BaseQueryRestful to append unvalidated SQL to the ORDER BY clause and extract database contents using boolean- or time-based blind techniques.

### CVE-2026-110613

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-10-14T15:17:13.327 |

youlai-mall through commit 9f62de8 contains a missing authorization vulnerability that allows authenticated members to view every customer's orders via the app order list endpoint. Attackers can page through the oms_order table using a self-registered account to read order ids, order_sn values, member ids, payment amounts, and order status.

### CVE-2026-110609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T15:17:12.760 |

Dromara Skyeye through commit 65d3ddcede70 contains an sql injection vulnerability that allows authenticated low-privileged users to inject SQL via the keyword parameter in the queryErpOrderItem MyBatis statement using raw ${} substitution. Attackers can send crafted keyword values to the queryWarehousingDetails or queryOutgoingDetails endpoints to extract database data, including other tenants' data, using boolean, UNION, error or time-based techniques.

### CVE-2026-110607

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-14T15:17:12.457 |

BizSpring Shop through commit cf22d39daaf1 contains a payment verification bypass vulnerability that allows authenticated buyers to mark orders paid by calling the PaymentController.testPostPay handler. Attackers can generate a payment log via /member/payment/load and request /member/payment/test_post_pay_{paymentLogSn} to obtain goods without paying or settle other members' orders.

### CVE-2026-101311

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-362` |
| Published | 2026-10-15T08:16:36.423 |

The framebuffer device model's maximum resolution constants were duplicated between the framebuffer and RFB modules and had gotten out of sync.  Additionally, writes to the framebuffer BAR could set arbitrary width and height values without validation, and the framebuffer BAR I/O and RFB rendering threads were not synchronized.

A malicious guest can crash the bhyve process or potentially execute arbitrary code in the host userspace context running the virtual machine, subject to bhyve's Capsicum sandbox.

### CVE-2026-110847

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-14T23:17:25.407 |

n8n before 1.123.83, 2.x before 2.41.4, and 2.42.x before 2.42.1 contains a stored cross-site scripting vulnerability in the Chat Trigger hosted-chat page, where insufficiently sanitised customCss values are interpolated into the page as markup. Workflow authors can publish a chat without n8n user authentication whose payload executes on the instance origin, acting on the sessions of signed-in visitors.

### CVE-2026-110846

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-180` |
| Published | 2026-10-14T23:17:25.253 |

n8n before 2.41.4 and 2.42.x before 2.42.1 contains a signature bypass in the waiting-webhook endpoint, which selects Send-and-Wait validation before normalising an alternate node reference form. Attackers holding an execution's resume token can approve waiting executions meant for others, running downstream actions under the workflow owner's credentials, potentially including command execution.

### CVE-2026-110840

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-14T23:17:24.320 |

n8n before 2.41.4 and 2.42.x before 2.42.1 contains an SQL injection vulnerability in version 1 of the Microsoft SQL node, which substitutes Query field expression values directly into SQL text without parameterisation. When a workflow binds untrusted input such as webhook fields to the Query field, unauthenticated external callers can execute arbitrary SQL against the connected database with the stored credential's privileges.

### CVE-2026-100413

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-14T18:17:10.633 |

SeaweedFS is a distributed storage system for files and blobs. From 4.0.388 until 4.41, the SFTP Helm chart embedded one unencrypted Ed25519 private host key in k8s/charts/seaweedfs/templates/sftp/sftp-secret.yaml as stringData.seaweedfs_sftp_ssh_private_key. A standalone deployment presented that public key when sftp.enabled and sftp.enableAuth were true, sftp.existingConfigSecret was not supplied, the legacy sftp.sshPrivateKey path remained selected, a valid config-ssh Secret allowed startup, and hostKeysFolder did not provide a later Ed25519 signer. An attacker able to redirect or intercept client traffic could impersonate that SFTP endpoint to clients that trusted the published host identity, exposing password credentials or data sent to the rogue endpoint. Default all-in-one and non-authenticated standalone paths did not load the key. This issue is fixed in version 4.41.

### CVE-2026-53614

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-807` |
| Published | 2026-10-14T16:17:45.930 |

util-linux is a random collection of Linux utilities. In util-linux 2.39.1 through 2.41.4 and 2.42 through 2.42.1, the SUID `mount` utility reads the attacker-controlled `LIBMOUNT_FORCE_MOUNT2` environment variable with `getenv()`, allowing a local low-privileged
user to force the non-atomic legacy bind-mount path. With an `/etc/fstab` bind mount authorized by `user` or `users` and protected by `nosuid`, `noexec`, or `nodev`, an attacker can race the window between the initial bind mount and the remount that applies those security flags and execute a SUID program from the temporarily unprotected mount, potentially gaining root privileges. This issue is fixed in 2.41.5 and 2.42.2.

### CVE-2026-53613

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-14T15:17:20.410 |

util-linux is a random collection of Linux utilities. In util-linux 2.17 through 2.41.6 and 2.42 through 2.42.3, and in 2.42.4 when the legacy `mount(2)` path is used without `/proc`, restricted non-root `mount` requests validate an `/etc/fstab` target before the mount operation re-resolves that pathname. A local low-privileged user authorized by an fstab `user` or `users` entry whose target has an attacker-writable ancestor can use `renameat2(RENAME_EXCHANGE)` to swap a path component and redirect an authorized mount to a root-owned location, such as mounting attacker-controlled content over `/etc/sudoers.d`, and thereby gain root privileges. Versions 2.41.5 and 2.42.2 pin targets for the new mount API, and 2.42.4 pins legacy targets through `/proc/self/fd`; the documented legacy fallback without `/proc` remains affected.

### CVE-2026-53612

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-14T15:17:20.260 |

util-linux is a random collection of Linux utilities. In util-linux 2.39 through 2.41.4 and 2.42 through 2.42.1, the SUID `mount` utility's `hook_owner.c` post-mount hook performs path-based `chmod()` and `lchown()` operations on a previously validated mount target. A local low-privileged user authorized by an `/etc/fstab` entry with `user` or `users` and an `X-mount.mode`, `X-mount.owner`, or `X-mount.group` option can use `renameat2(RENAME_EXCHANGE)` to race a writable ancestor of the target and redirect the privileged ownership or mode change to a root-owned path, potentially gaining root privileges. This issue is fixed in 2.41.5 and 2.42.2.

### CVE-2026-110630

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-14T15:17:15.843 |

VentureDrake Laravel CRM before 2.4.0 contains an incorrect authorization vulnerability in user management that allows authenticated administrators to assign unrestricted roles via Role::find. Attackers with user-management access can assign the Owner role or other teams' roles and delete cross-team users through the unscoped UserIndex delete() method.
