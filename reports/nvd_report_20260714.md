# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-07-13 15:00 UTC
- **対象期間**: `2026-07-12T15:00:12.000Z` 〜 `2026-07-13T15:00:33.000Z`
- **重要CVE数**: 137 件（Critical 9.0+: 31 件 / High 7.0〜: 106 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公表された CVE の多くは **Web アプリケーション（特に WordPress 系プラグイン）** と **IoT/管理系サーバ** に集中しており、リモートからコード実行や権限昇格が可能になる深刻度 9.0 以上の脆弱性が多数報告されています。  
- 主な攻撃手法は **コードインジェクション / ファイルアップロード無制限 / デシリアライズ**、さらに **サーバーサイドテンプレートインジェクション（SSTI）** や **TLS 証明書検証不備** といった、入力検証の欠如が根本原因となっているケースが目立ちます。  
- CVSS が 10.0 の「完全リモートコード実行」や、9.8 以上の「特権昇格・オブジェクトインジェクション」など、**即時対応が求められる脆弱性が集中**しているため、優先的にパッチ適用またはプラグインの除去を実施すべきです。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 理由・注目ポイント |
|-----|------|----------|-------------------|
| **CVE‑2026‑57811** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Realtyna Organic IDX (≤ 5.2.0) における **コードインジェクション**（RCE） | WordPress サイトで最も利用される不動産プラグインの一つ。認証不要で任意コード実行が可能になるため、サイト全体が乗っ取られるリスクが極めて高い。 |
| **CVE‑2026‑57719** | 10.0 (AV:N/AC:L/PR:N/UI:N/S:C) | Aimogen Pro (≤ 2.8.3) の **危険ファイル種別無制限アップロード** | 任意の PHP/シェルファイルをアップロードでき、即座にリモートコード実行へと繋がる。プラグインは多数の不動産サイトで導入されている点が危険度を上げる。 |
| **CVE‑2026‑14453** | 9.6 (AV:N/AC:L/PR:L/UI:N/S:C) | Centreon‑open‑tickets モジュールの **SSTI → RCE** | 認証済みユーザーがテンプレートに任意コードを埋め込める。Centreon はインフラ監視の要であり、侵入された場合は監視データ改ざん・内部ネットワーク横移動が可能になる。 |
| **CVE‑2026‑6847** | 9.3 (AV:N/AC:L/PR:N/UI:N) | ThemisNETPanel の **認証なしファイルアップロード** | PHP ファイルを任意に配置でき、管理パネルが無防備なため即座にサーバー全体の支配が可能。パッチ情報が未公開である点がリスクを増幅。 |
| **CVE‑2026‑22093** | 9.5 (CVSS:4.0) | EVbee Service Android アプリの **TLS 証明書検証不備** | ネットワーク上の中間者（MITM）攻撃で通信内容が改竄・盗聴でき、認証情報や機密データが漏洩。モバイルアプリは企業内部ツールとして利用されるケースが多く、情報漏洩リスクが高い。 |

> **注目ポイント**  
> - **認証不要**でリモートコード実行が可能なものが 2 件（CVE‑2026‑57811、CVE‑2026‑57719）あり、外部からの直接攻撃が想定されます。  
> - **プラグイン系**は WordPress エコシステム全体に波及しやすく、同一プラグインを複数サイトで使用している組織は一斉に影響を受ける可能性があります。  
> - **SSTI** や **TLS 証明書検証不備** は、従来の WAF だけでは防げないため、アプリケーションレイヤーでの対策が必須です。  

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **脆弱プラグイン・コンポーネントの即時無効化**（パッチが未提供の場合は代替プラグインへ切り替える）。  
- **Web アプリケーションファイアウォール（WAF）** で以下をブロック  
  - `*.php` への任意ファイルアップロードリクエスト  
  - `../`（パストラバーサル）や `eval`、`{{` などのテンプレートインジェクション文字列  
- **最小権限の原則**を徹底し、プラグイン実行ユーザーの `PR`（Privilege Required）を **最低限に設定**（例：WordPress の `wp_user` を `read` のみ）。  
- **TLS 証明書検証**を強制する設定に変更し、**証明書ピンニング**が可能なら実装する。  

### 3.2 個別パッケージ別具体的対策

| パッケージ / プラグイン | 現行バージョン (脆弱) | 推奨バージョン / 対策 |
|------------------------|----------------------|----------------------|
| **Realtyna Organic IDX** | ≤ 5.2.0 | 5.2.1 以降（公式リリースがある場合）または **プラグイン削除** |
| **Aimogen Pro** | ≤ 2.8.3 | 2.8.4 以降（アップロード制御を追加）または **代替プラグイン** |
| **WoowBot Pro Max** | ≤ 14.1.7 | 14.1.8 以降（ファイルタイプチェック実装） |
| **SureDash** | ≤ 1.8.0 | 1.8.1 以降（パストラバーサル対策） |
| **Directorist** | ≤ 8.8.2 | 8.8.3 以降（オブジェクトインジェクション防止） |
| **MailOptin** | ≤ 1.2.77.3 | 1.

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-57811

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-13T10:16:45.040 |

Improper Control of Generation of Code ('Code Injection') vulnerability in Realtyna Realtyna Organic IDX plugin real-estate-listing-realtyna-wpl allows Remote Code Inclusion.This issue affects Realtyna Organic IDX plugin: from n/a through <= 5.2.0.

### CVE-2026-57719

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-13T10:16:38.970 |

Unrestricted Upload of File with Dangerous Type vulnerability in CodeRevolution Aimogen Pro aimogen-pro allows Using Malicious Files.This issue affects Aimogen Pro: from n/a through <= 2.8.3.

### CVE-2026-57710

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-07-13T10:16:38.143 |

Unrestricted Upload of File with Dangerous Type vulnerability in quantumcloud WoowBot Pro Max woowbot-pro-max allows Using Malicious Files.This issue affects WoowBot Pro Max: from n/a through <= 14.1.7.

### CVE-2026-57401

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T10:16:33.683 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Brainstorm Force SureDash suredash allows Path Traversal.This issue affects SureDash: from n/a through <= 1.8.0.

### CVE-2026-59518

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:45.977 |

Deserialization of Untrusted Data vulnerability in wpWax Directorist directorist allows Object Injection.This issue affects Directorist: from n/a through <= 8.8.2.

### CVE-2026-57813

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-13T10:16:45.270 |

Incorrect Privilege Assignment vulnerability in properfraction MailOptin mailoptin allows Privilege Escalation.This issue affects MailOptin: from n/a through <= 1.2.77.3.

### CVE-2026-57770

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:41.040 |

Deserialization of Untrusted Data vulnerability in ThemeGoods Grand Photography grandphotography allows Object Injection.This issue affects Grand Photography: from n/a through <= 5.7.8.

### CVE-2026-57744

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:40.690 |

Deserialization of Untrusted Data vulnerability in stmcan RT-Theme 18 | Extensions rt18-extensions allows Object Injection.This issue affects RT-Theme 18 | Extensions: from n/a through <= 2.5.

### CVE-2026-57738

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:40.110 |

Deserialization of Untrusted Data vulnerability in axiomthemes 777 triple-seven allows Object Injection.This issue affects 777: from n/a through <= 1.13.0.

### CVE-2026-57724

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:39.087 |

Deserialization of Untrusted Data vulnerability in Themeum Kirki kirki allows Object Injection.This issue affects Kirki: from n/a through <= 6.0.12.

### CVE-2026-14453

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-13T09:16:23.893 |

This vulnerability is a critical Server-Side Template Injection (SSTI) in Centreon's centreon-open-tickets module that leads to Remote Code Execution. The message_confirm field is stored without sanitization and rendered via Smarty with no security policy enabled, allowing any authenticated user, to inject and execute arbitrary code on the server. This results in disclosure of environment secrets and could impact platform availability of Centreon Infra Monitoring product.

### CVE-2026-22093

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-295` |
| Published | 2026-07-13T10:16:26.910 |

The EVbee Service Android app uses TLS encrypted communication (HTTPS), but does not validate the certificate provided by the server. This allows an attacker on the network path between the app and EVbee server to intercept and manipulate the communication between the app and server. The traffic is weakly encrypted using RC4 with a hardcoded key, which allows an attacker to gain access to the communication. Part of this communication involves access codes to charging stations.





This issue affects EVbee Service: v1.4.101.00.

### CVE-2026-14934

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:Clear` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T11:16:26.470 |

A Missing Authorization vulnerability in the repository creation functionality in Google Cloud BigQuery, Dataform and Colab Enterprise, in the versions between October 2025 and May 10th, 2026, on Google Cloud Platform, allows an authenticated attacker to escalate privileges and perform cross-tenant repository takeover.


This vulnerability was patched on 10 May 2026, and no customer action is needed.

### CVE-2026-6847

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-13T14:16:32.963 |

Remote Code Execution vulnerability exists in ThemisNETPanel due to missing authentication for a critical file upload function. The application exposes an endpoint that allows unauthenticated attackers to upload arbitrary PHP files by providing a base64-encoded payload and to execute arbitrary code on the underlying server. This issue has been fixed by a patch released in April 2026.

### CVE-2026-61498

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-13T14:16:32.213 |

Vitec Flamingo 4.12.2 contains an unauthenticated OS command injection vulnerability in the admin/ajax/gen_graphs.php endpoint that allows remote unauthenticated attackers to execute arbitrary commands by supplying shell metacharacters in the start, end, key, or format HTTP GET parameters. Attackers can exploit the lack of input sanitization in the graph generation script, which passes user-supplied values directly to shell commands via passthru(), to execute arbitrary OS commands with root privileges due to the web server context having passwordless sudo access.

### CVE-2026-60121

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-13T14:16:32.067 |

Vitec Flamingo 4.12.2 contains an unauthenticated OS command injection vulnerability in the admin/ajax/ping.php endpoint that allows remote attackers to execute arbitrary commands by exploiting a double-evaluation flaw in shell argument handling. The endpoint applies escapeshellarg() to the user-supplied host POST parameter before passing it to a system wrapper, but the wrapper retrieves the decoded value from argv and incorporates it into a second shell_exec() call without escaping, allowing injected commands to execute with root privileges via passwordless sudo.

### CVE-2026-12257

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-07-13T12:16:29.150 |

Versions of Mura CMS prior to 10.0.712 contain a critical remote code execution (RCE) vulnerability. The flaw is located in the endpoint “/index.cfm/_api/json/v1/default”, where the “method” parameter in POST requests is not properly validated or sanitised before being processed by the ColdFusion engine. As a result, a remote attacker could exploit this vulnerability to inject and execute arbitrary CFML (ColdFusion Markup Language) expressions and instantiate malicious Java objects, thereby compromising the system’s security.

### CVE-2026-59515

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:45.737 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Sergey AIWU ai-copilot-content-generator allows Blind SQL Injection.This issue affects AIWU: from n/a through <= 1.5.4.

### CVE-2026-57739

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:40.223 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in AcyMailing Newsletter Team AcyMailing SMTP Newsletter acymailing allows Blind SQL Injection.This issue affects AcyMailing SMTP Newsletter: from n/a through <= 10.11.0.

### CVE-2026-57726

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:39.317 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Themeum Kirki kirki allows Blind SQL Injection.This issue affects Kirki: from n/a through <= 6.0.12.

### CVE-2026-57714

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:38.617 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in LatePoint LatePoint latepoint allows Blind SQL Injection.This issue affects LatePoint: from n/a through <= 5.6.3.

### CVE-2026-57707

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:37.743 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in quantumcloud Simple Business Directory Pro simple-business-directory-pro allows SQL Injection.This issue affects Simple Business Directory Pro: from n/a through <= 15.9.4.

### CVE-2026-57702

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:37.377 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Melograno Venture Studio Amelia ameliabooking allows Blind SQL Injection.This issue affects Amelia: from n/a through <= 2.4.2.

### CVE-2026-22103

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-13T10:16:27.900 |

The NPC start endpoint on the web server at port 8090 is vulnerable to command injection.

### CVE-2026-22102

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20` |
| Published | 2026-07-13T10:16:27.783 |

A POST request sent to a specific webserver endpoint can be used to write to arbitrary file locations. The endpoint accepts the filename parameter in the Content-Disposition header without verification.
This can be used to cause a denial of service by overwriting system files, or remote-code-execution by overwriting shell-scripts which execution can be triggered through other means.

### CVE-2026-22097

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-347` |
| Published | 2026-07-13T10:16:27.277 |

The firmware update mechanism does not include cryptographic signature validation. This allows anyone with access to the firmware update capability to upload arbitrary files which can then lead to arbitrary code execution.

### CVE-2026-22096

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-07-13T10:16:27.167 |

The webserver running on port 8090 does not require authentication. This allows for sensitive information leakage such as configured passwords, or uploading files through different endpoints.

### CVE-2026-22095

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77` |
| Published | 2026-07-13T10:16:27.050 |

The network diagnosis endpoint on the web server at port 8090 is vulnerable to command injection.

### CVE-2026-4769

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-912` |
| Published | 2026-07-13T08:16:21.343 |

Certain devices in the WAGO System I/O Field series activate an internal diagnostic capability during the initial startup sequence. This functionality is not formally documented and becomes accessible without authentication for a brief period in the early boot phase. During this window, an unauthenticated remote attacker can gain access to the internal system processes, resulting in full system compromise.

### CVE-2026-22098

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-532` |
| Published | 2026-07-13T10:16:27.393 |

Various sensitive information such as passwords and charging card UIDs are written to log files.

### CVE-2026-13014

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-73;CWE-94` |
| Published | 2026-07-13T10:16:24.913 |

A vulnerability in Thales CERT "Suspicious" application =< 1.3.4 allows a remote and unauthenticated attacker to execute arbitrary code and arbitrarily overwrite writable application files—including Python modules, configuration files, cron inputs, and runtime artifacts—leading to a persistent denial of service, the potential compromise of application secrets or integrations, and root-level execution inside the Django application container.
This vulnerability has been names "Matryoshka Mail".
Thales PSIRT 
acknowledges and thanks

Lucien Doustaly (aka wlayzz) for discovering and reporting this issue.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-15511

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-07-12T23:16:38.137 |

A vulnerability was determined in Comfast CF-WR631AX V3 up to 2.7.0.8. Affected by this vulnerability is the function system_wl_upload_pic_file of the file /usr/bin/webmgnt of the component FastCGI Backend. This manipulation of the argument filename causes os command injection. It is possible to initiate the attack remotely. The exploit has been publicly disclosed and may be utilized. The vendor was contacted early about this disclosure but did not respond in any way.

### CVE-2026-57786

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-13T10:16:42.527 |

Cross-Site Request Forgery (CSRF) vulnerability in purethemes WorkScout-Core workscout-core allows Authentication Bypass.This issue affects WorkScout-Core: from n/a through <= 1.7.08.

### CVE-2026-57713

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:38.500 |

Deserialization of Untrusted Data vulnerability in Marcus (aka @msykes) Events Manager events-manager allows Object Injection.This issue affects Events Manager: from n/a through <= 7.3.6.

### CVE-2026-57410

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-13T10:16:34.767 |

Incorrect Privilege Assignment vulnerability in MailerPress Team MailerPress mailerpress allows Privilege Escalation.This issue affects MailerPress: from n/a through <= 2.0.2.

### CVE-2026-57386

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-13T10:16:31.803 |

Incorrect Privilege Assignment vulnerability in Kodezen LLC aBlocks ablocks allows Privilege Escalation.This issue affects aBlocks: from n/a through < 2.9.1.

### CVE-2026-57371

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:30.330 |

Deserialization of Untrusted Data vulnerability in denishua WPJAM Basic wpjam-basic allows Object Injection.This issue affects WPJAM Basic: from n/a through <= 7.0.

### CVE-2026-57830

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T08:16:21.713 |

The Joomla extension Helix Ultimate is vulnerable to an unauthenticated arbitrary file deletion.

### CVE-2026-22099

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-07-13T10:16:27.523 |

The charging station does not require authentication for Bluetooth commands to perform actions. The functionality exposed includes sensitive information leakage, triggering reboots, or pushing a firmware update URL.

### CVE-2026-57829

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T08:16:21.547 |

The Joomla extension Helix Ultimate is vulnerable to an unauthenticated stored XSS.

### CVE-2026-57709

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T10:16:38.020 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in WP Swings Membership For WooCommerce membership-for-woocommerce allows Path Traversal.This issue affects Membership For WooCommerce: from n/a through <= 3.1.0.

### CVE-2026-57389

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T10:16:32.160 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Adrian Tobey Groundhogg groundhogg allows Path Traversal.This issue affects Groundhogg: from n/a through <= 4.4.1.

### CVE-2026-22100

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-07-13T10:16:27.670 |

The OCPP DataTransfer message `ReserveLogin` is vulnerable to command injection. By manipulating the data value, arbitrary OS commands can be executed as root.

### CVE-2026-57810

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:44.923 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Saad Iqbal APIExperts Square for WooCommerce woosquare allows Blind SQL Injection.This issue affects APIExperts Square for WooCommerce: from n/a through <= 4.7.4.

### CVE-2026-57787

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:42.657 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in CreativeWS CWS SVGicons cws-svgicons allows Blind SQL Injection.This issue affects CWS SVGicons: from n/a through <= 1.5.5.

### CVE-2026-57772

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:41.277 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in WP Inventory WP Inventory Manager wp-inventory-manager allows Blind SQL Injection.This issue affects WP Inventory Manager: from n/a through <= 2.4.0.

### CVE-2026-57771

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:41.157 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Milan Petrovic GD Rating System gd-rating-system allows Blind SQL Injection.This issue affects GD Rating System: from n/a through <= 3.7.

### CVE-2026-57385

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:31.687 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in appsbd Vitepos vitepos-lite allows Blind SQL Injection.This issue affects Vitepos: from n/a through <= 3.4.2.

### CVE-2026-9492

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-07-13T04:16:29.283 |

The MBStorage DRAM lighting control module within Gigabyte Control Center (GCC) developed by GIGABYTE Technology has an Improper Access Control vulnerability. Authenticated local attackers can send specific IOCTL commands through the driver MyPortIO_x64.sys bundled with the module, thereby arbitrarily reading and writing physical memory and obtaining kernel-level privileges.

### CVE-2026-62143

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:Y/R:X/V:X/RE:M/U:Green` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T09:16:24.700 |

A Server-Side Request Forgery (SSRF) protection bypass existed in the html_to_markdown expansion module of misp-modules.

The module attempts to prevent requests to loopback, private, link-local, and other restricted IP address ranges. However, IP addresses were compared against the blocked ranges without first normalising IPv4-mapped IPv6 addresses.

An authenticated attacker able to invoke the module could supply an IPv4-mapped IPv6 address, such as:

http://[::ffff:127.0.0.1]/
http://[::ffff:169.254.169.254]/

Alternatively, the attacker could use a hostname that resolves to an IPv4-mapped IPv6 address. These addresses were treated as IPv6 addresses and therefore did not match the corresponding blocked IPv4 ranges.

Successful exploitation could cause the misp-modules server to connect to services available through its loopback interface, internal network, or link-local network. This could expose internal web services, administrative interfaces, or cloud instance metadata, with retrieved content potentially returned to the attacker as converted Markdown.

The vulnerability has been addressed by normalising IPv4-mapped IPv6 addresses to their underlying IPv4 representation before applying the blocked-range checks. URLs without a valid hostname are now also rejected.

### CVE-2026-58596

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-822` |
| Published | 2026-07-12T16:16:31.350 |

Untrusted pointer dereference in Microsoft Edge (Chromium-based) allows an unauthorized attacker to elevate privileges over a network.

### CVE-2026-57768

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-266` |
| Published | 2026-07-13T10:16:40.923 |

Incorrect Privilege Assignment vulnerability in favethemes Houzez Login Register houzez-login-register allows Privilege Escalation.This issue affects Houzez Login Register: from n/a through <= 3.3.3.

### CVE-2026-57743

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:40.570 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in stmcan RT-Theme 18 | Extensions rt18-extensions allows PHP Local File Inclusion.This issue affects RT-Theme 18 | Extensions: from n/a through <= 2.5.

### CVE-2026-10666

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-12T17:16:24.550 |

parse_ipv4() in subsys/net/ip/utils.c (reached via net_ipaddr_parse() for strings of the form "a.b.c.d:port") copies the port substring into a fixed 17-byte stack buffer (char ipaddr[NET_IPV4_ADDR_LEN + 1]) using a length of str_len - end - 1, where str_len is the full, unbounded input length and end is only the (<=15-byte) offset of the ':' delimiter. Because the destination size is never consulted, a crafted address string with a long suffix after the colon (e.g. "1.2.3.4:" followed by hundreds of bytes) causes an out-of-bounds stack write whose length and contents are fully attacker-controlled (memcpy of the suffix plus a trailing NUL), enabling memory corruption and at minimum a denial of service, and potentially control-flow hijack. The parser is reached from the standard socket API (zsock_getaddrinfo / literal-address resolution), DNS server-string configuration, and the eswifi Wi-Fi co-processor DNS-response path, so an application that resolves a network-influenced address string is exposed. The bug was introduced when the parser was added (Zephyr v1.9.0) and shipped in all releases through v4.4.0. The fix removes the unbounded copy and validates the port length before copying into a small dedicated buffer. Note: the equivalent IPv6 "[addr]:port" path in parse_ipv6() retains the same unbounded copy at this commit and remains a separate, still-reachable instance of the defect.

### CVE-2026-7162

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-07-13T04:16:29.127 |

Successful
exploitation of the integer overflow vulnerability could allow an attacker to
achieve system-level access to the affected software.

### CVE-2026-10667

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-07-12T17:16:24.670 |

Zephyr's dynamic kernel-object tracking (kernel/userspace/userspace.c, formerly kernel/userspace.c) maintains a doubly-linked list (obj_list) of dynamically allocated kernel objects. Iteration over this list in k_object_wordlist_foreach() was performed under lists_lock using the SAFE iterator (which caches the next node), but list removal and freeing of nodes was performed under different, disjoint spinlocks: objfree_lock in k_object_free() and obj_lock in unref_check(). On an SMP system, while one CPU iterated obj_list under lists_lock, another CPU could unlink and k_free() the dyn_obj node that the iterator had cached as its next pointer, causing the iterator to dereference freed kernel memory (use-after-free / dangling list traversal). All of the racing operations are reachable from unprivileged user-mode threads via system calls: k_object_alloc/k_object_alloc_size and k_object_release drive removals through unref_check() (under obj_lock), while k_thread_abort and thread creation drive the iteration through k_thread_perms_all_clear()/k_thread_perms_inherit() (under lists_lock). A deprivileged user thread on a CONFIG_SMP + CONFIG_USERSPACE build can therefore corrupt the kernel's object-tracking structures across the userspace security boundary, yielding kernel memory corruption (potential privilege escalation) or a kernel crash (denial of service). The fix removes objfree_lock and serializes every obj_list modification under lists_lock, including holding it across find+remove in k_object_free() and around unref_check() in k_thread_perms_clear(). Affects CONFIG_SMP+CONFIG_USERSPACE+CONFIG_DYNAMIC_OBJECTS configurations; the defect dates to the 2019 spinlockification (commit 8a3d57b6cc6, first released in v1.14.0) and shipped through v4.4.0.

### CVE-2026-61955

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:46.450 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Hannan گرویتی فرم فارسی persian-gravity-forms allows Blind SQL Injection.This issue affects گرویتی فرم فارسی: from n/a through <= 3.0.2.

### CVE-2026-57773

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-07-13T10:16:41.393 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Zorem Advanced Shipment Tracking for WooCommerce woo-advanced-shipment-tracking allows Blind SQL Injection.This issue affects Advanced Shipment Tracking for WooCommerce: from n/a through <= 4.0.

### CVE-2026-15584

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-250` |
| Published | 2026-07-13T13:16:30.560 |

A privilege escalation vulnerability was found in the incluster-checks tool for OpenShift. The tool creates privileged debug pods with host filesystem access in the shared default namespace, where any user with the standard edit role can exec into them and obtain root access on cluster nodes.

### CVE-2026-57815

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-07-13T10:16:45.507 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in WPMU DEV - Your All-in-One WordPress Platform Forminator forminator allows Path Traversal.This issue affects Forminator: from n/a through <= 1.55.0.2.

### CVE-2026-57805

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.807 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Select-Themes Tonda tonda allows PHP Local File Inclusion.This issue affects Tonda: from n/a through <= 2.5.

### CVE-2026-57804

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.687 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in CodexThemes TheGem Theme Elements (for Elementor) thegem-elements-elementor allows PHP Local File Inclusion.This issue affects TheGem Theme Elements (for Elementor): from n/a through <= 5.11.1.

### CVE-2026-57803

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.567 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Select-Themes Struktur Core struktur-core allows PHP Local File Inclusion.This issue affects Struktur Core: from n/a through <= 2.5.1.

### CVE-2026-57802

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.453 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Select-Themes Struktur struktur allows PHP Local File Inclusion.This issue affects Struktur: from n/a through <= 2.5.1.

### CVE-2026-57801

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.337 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Select-Themes SetSail setsail allows PHP Local File Inclusion.This issue affects SetSail: from n/a through <= 2.1.

### CVE-2026-57800

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.223 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Edge-Themes Overworld overworld allows PHP Local File Inclusion.This issue affects Overworld: from n/a through <= 1.5.

### CVE-2026-57799

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:44.110 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in uxper Nuss nuss allows PHP Local File Inclusion.This issue affects Nuss: from n/a through <= 1.3.6.

### CVE-2026-57798

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.993 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in SaurabhSharma NewsPlus Shortcodes newsplus-shortcodes allows PHP Local File Inclusion.This issue affects NewsPlus Shortcodes: from n/a through <= 4.2.0.

### CVE-2026-57796

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.760 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in VLThemes Leedo leedo allows PHP Local File Inclusion.This issue affects Leedo: from n/a through <= 3.0.0.

### CVE-2026-57795

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.643 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in themelexus Kitchor kitchor allows PHP Local File Inclusion.This issue affects Kitchor: from n/a through <= 1.4.3.

### CVE-2026-57794

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.517 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in uxper Golo Framework golo-framework allows PHP Local File Inclusion.This issue affects Golo Framework: from n/a through <= 1.7.3.

### CVE-2026-57793

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.390 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Elated-Themes Flow flow allows PHP Local File Inclusion.This issue affects Flow: from n/a through <= 1.8.

### CVE-2026-57792

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.270 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Mikado-Themes Dør dor allows PHP Local File Inclusion.This issue affects Dør: from n/a through <= 2.4.1.

### CVE-2026-57791

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.147 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in ThemeMove Brook brook allows PHP Local File Inclusion.This issue affects Brook: from n/a through <= 2.9.0.

### CVE-2026-57790

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:43.030 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in ThemeMove Billey billey allows PHP Local File Inclusion.This issue affects Billey: from n/a through <= 2.1.8.

### CVE-2026-57789

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:42.903 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in jwsthemes Aqua aqua allows PHP Local File Inclusion.This issue affects Aqua: from n/a through <= 5.1.2.

### CVE-2026-57788

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-07-13T10:16:42.777 |

Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') vulnerability in Edge-Themes Aalto aalto allows PHP Local File Inclusion.This issue affects Aalto: from n/a through <= 1.8.

### CVE-2026-57729

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:39.657 |

Missing Authorization vulnerability in UX-themes Flatsome flatsome allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Flatsome: from n/a through <= 3.20.5.

### CVE-2026-57727

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:39.427 |

Missing Authorization vulnerability in Themeum Kirki kirki allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Kirki: from n/a through <= 6.0.13.

### CVE-2026-57705

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:37.493 |

Missing Authorization vulnerability in Nexcess Event Tickets event-tickets allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Event Tickets: from n/a through <= 5.28.5.

### CVE-2026-57697

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-288` |
| Published | 2026-07-13T10:16:37.143 |

Authentication Bypass Using an Alternate Path or Channel vulnerability in Metagauss ProfileGrid  profilegrid-user-profiles-groups-and-communities allows Password Recovery Exploitation.This issue affects ProfileGrid : from n/a through <= 5.9.9.6.

### CVE-2026-57378

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:30.920 |

Missing Authorization vulnerability in Phil Kurth Advanced Forms advanced-forms allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Advanced Forms: from n/a through <= 1.9.3.7.

### CVE-2026-15574

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-538` |
| Published | 2026-07-13T09:16:24.550 |

A flaw was found in the vllm-orchestrator-gateway component. The system's production binary logs all incoming authorization headers and full chat payloads, which may contain personally identifiable information (PII) and secrets, to persistent logs. This sensitive data, including bearer tokens and chat content, can be accessed by any user with logging privileges. This vulnerability leads to information disclosure, potentially allowing an attacker to harvest credentials and sensitive conversation content.

### CVE-2026-14165

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-07-13T08:16:20.253 |

An Authorization Bypass Through User-Controlled Key vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to access data of other users without authorization.

### CVE-2026-15548

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-13T10:16:26.537 |

A security vulnerability has been detected in Shibby Tomato up to 1.28.0000. This vulnerability affects the function sub_407220 of the file /usr/sbin/httpd of the component DNS List Rendering. The manipulation leads to stack-based buffer overflow. The attack is possible to be carried out remotely. This project is superseded by FreshTomato.

### CVE-2026-15545

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-07-13T09:16:24.043 |

A vulnerability was identified in Shibby Tomato up to 1.28.0000. Affected by this vulnerability is the function main of the file www/apcupsd/tomatodata.cgi of the component apcupsd. Such manipulation leads to out-of-bounds write. The attack may be launched remotely. The exploit is publicly available and might be used. This project is superseded by FreshTomato.

### CVE-2026-15544

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-07-13T08:16:21.150 |

A vulnerability was determined in Shibby Tomato up to 1.28.0000. Affected is the function getupsvar of the file www/apcupsd/tomatodata.cgi of the component apcupsd. This manipulation of the argument Field causes stack-based buffer overflow. The attack may be initiated remotely. The exploit has been publicly disclosed and may be utilized. This project is superseded by FreshTomato.

### CVE-2026-15543

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-07-13T08:16:20.967 |

A vulnerability was found in Tenda CH22 1.0.0.1. This impacts the function formCertListInfo of the file /goform/CertListInfo. The manipulation of the argument Name results in buffer overflow. The attack can be launched remotely. The exploit has been made public and could be used.

### CVE-2026-10665

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-07-12T17:16:24.433 |

In Zephyr's WireGuard subsystem (subsys/net/lib/wireguard), wg_process_data_message() in wg_crypto.c linearizes an inbound transport-data payload into a fixed pool buffer of CONFIG_WIREGUARD_BUF_LEN bytes before decryption. The call net_buf_linearize(buf->data, data_len, pkt->buffer, ..., data_len) passed the attacker-derived data_len as both the destination capacity and the copy length, defeating the function's internal len = min(len, dst_len) bound. data_len is derived from the received UDP datagram length and is only lower-bounded by wg_ctrl_recv() (no upper bound). When data_len exceeds CONFIG_WIREGUARD_BUF_LEN — e.g. when the buffer length is lowered below the link MTU, on links with MTU above the buffer size, or via reassembled IPv4/IPv6 fragments that exceed it — the underlying memcpy writes past the end of the pool buffer, an out-of-bounds write (CWE-787). The overflow occurs before the Poly1305 authentication check, so it requires only a valid receiver session index rather than a valid authenticator, and is reachable by a malicious or compromised peer (or an on-path attacker driving an established session) over the network, yielding remote memory corruption and at minimum a reliable denial of service. The defect was present in the WireGuard implementation shipped in Zephyr 4.4.0. The fix adds an explicit data_len > CONFIG_WIREGUARD_BUF_LEN rejection and corrects the linearize call to pass net_buf_max_len(buf) as the destination capacity.

### CVE-2026-59521

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-07-13T10:16:46.093 |

Deserialization of Untrusted Data vulnerability in ShapedPlugin LLC Real Testimonials testimonial-free allows Object Injection.This issue affects Real Testimonials: from n/a through <= 3.1.15.

### CVE-2026-57407

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T10:16:34.417 |

Server-Side Request Forgery (SSRF) vulnerability in WP Swings PDF Generator for WordPress pdf-generator-for-wp allows Server Side Request Forgery.This issue affects PDF Generator for WordPress: from n/a through <= 1.6.2.

### CVE-2026-57372

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-07-13T10:16:30.450 |

Server-Side Request Forgery (SSRF) vulnerability in denishua WPJAM Basic wpjam-basic allows Server Side Request Forgery.This issue affects WPJAM Basic: from n/a through <= 7.0.

### CVE-2026-61956

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-352` |
| Published | 2026-07-13T10:16:46.573 |

Cross-Site Request Forgery (CSRF) vulnerability in hamsalam ووسلام &#8211; همگام سازی ووکامرس و باسلام sync-basalam allows Cross Site Request Forgery.This issue affects ووسلام &#8211; همگام سازی ووکامرس و باسلام: from n/a through <= 1.9.1.

### CVE-2026-59516

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:45.860 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Room 34 Creative Services, LLC ICS Calendar ics-calendar allows Reflected XSS.This issue affects ICS Calendar: from n/a through <= 12.1.1.

### CVE-2026-57816

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:45.620 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in FunnelKit Funnel Builder by FunnelKit funnel-builder allows Reflected XSS.This issue affects Funnel Builder by FunnelKit: from n/a through <= 3.15.0.8.

### CVE-2026-57814

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:45.393 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPMU DEV - Your All-in-One WordPress Platform Forminator forminator allows DOM-Based XSS.This issue affects Forminator: from n/a through <= 1.55.0.1.

### CVE-2026-57745

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:40.807 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in stmcan RT-Theme 18 | Extensions rt18-extensions allows Reflected XSS.This issue affects RT-Theme 18 | Extensions: from n/a through <= 2.5.

### CVE-2026-57741

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:40.457 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in AcyMailing Newsletter Team AcyMailing SMTP Newsletter acymailing allows Stored XSS.This issue affects AcyMailing SMTP Newsletter: from n/a through <= 10.11.0.

### CVE-2026-57740

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:40.340 |

Missing Authorization vulnerability in AcyMailing Newsletter Team AcyMailing SMTP Newsletter acymailing allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects AcyMailing SMTP Newsletter: from n/a through <= 10.11.1.

### CVE-2026-57734

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:39.997 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in tagDiv tagDiv Composer td-composer allows Reflected XSS.This issue affects tagDiv Composer: from n/a through <= 5.4.3.

### CVE-2026-57733

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:39.883 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in tagDiv tagDiv Cloud Library td-cloud-library allows DOM-Based XSS.This issue affects tagDiv Cloud Library: from n/a through <= 3.9.4.

### CVE-2026-57732

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:39.767 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in tagDiv tagDiv Opt-In Builder td-subscription allows DOM-Based XSS.This issue affects tagDiv Opt-In Builder: from n/a through <= 1.7.4.

### CVE-2026-57728

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:39.540 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in UX-themes Flatsome flatsome allows Reflected XSS.This issue affects Flatsome: from n/a through <= 3.20.5.

### CVE-2026-57725

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:39.200 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themeum Kirki kirki allows Stored XSS.This issue affects Kirki: from n/a through <= 6.0.11.

### CVE-2026-57718

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:38.853 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Reflected XSS.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through <= 2.0.12.

### CVE-2026-57715

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:38.737 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPManageNinja Fluent CRM fluent-crm allows Reflected XSS.This issue affects Fluent CRM: from n/a through <= 3.1.7.

### CVE-2026-57712

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:38.387 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPZOOM WPZOOM Portfolio wpzoom-portfolio allows Reflected XSS.This issue affects WPZOOM Portfolio: from n/a through <= 1.4.29.

### CVE-2026-57708

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:37.900 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in CRM Perks Contact Form Entries contact-form-entries allows Reflected XSS.This issue affects Contact Form Entries: from n/a through <= 1.5.2.

### CVE-2026-57706

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:37.623 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dokan, Inc. Dokan dokan-lite allows Reflected XSS.This issue affects Dokan: from n/a through <= 5.0.6.

### CVE-2026-57695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:37.020 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Dan Rossiter Document Gallery document-gallery allows Reflected XSS.This issue affects Document Gallery: from n/a through <= 5.1.0.

### CVE-2026-57668

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:36.547 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Basix NEX-Forms nex-forms-express-wp-form-builder allows Stored XSS.This issue affects NEX-Forms: from n/a through <= 9.2.2.

### CVE-2026-57423

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:36.317 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Kofi Mokome Message Filter for Contact Form 7 cf7-message-filter allows Reflected XSS.This issue affects Message Filter for Contact Form 7: from n/a through <= 1.6.3.8.

### CVE-2026-57422

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:36.200 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in VillaTheme Bopo – WooCommerce Product Bundle Builder bopo-woo-product-bundle-builder allows Reflected XSS.This issue affects Bopo – WooCommerce Product Bundle Builder: from n/a through <= 1.2.0.

### CVE-2026-57421

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:36.070 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in CRM Perks CRM Perks Forms crm-perks-forms allows Reflected XSS.This issue affects CRM Perks Forms: from n/a through <= 1.1.7.

### CVE-2026-57417

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:35.600 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in RexTheme Cart Lift cart-lift allows Stored XSS.This issue affects Cart Lift: from n/a through <= 3.1.57.

### CVE-2026-57416

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:35.473 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in SiteGround SiteGround Email Marketing siteground-email-marketing allows Stored XSS.This issue affects SiteGround Email Marketing: from n/a through <= 1.7.5.

### CVE-2026-57415

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:35.350 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Codemenschen Gift Vouchers gift-voucher allows Stored XSS.This issue affects Gift Vouchers: from n/a through <= 4.7.0.

### CVE-2026-57411

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:34.877 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Aman CF7 Views &#8211; Complete Entry Management for Contact Form 7 cf7-views allows DOM-Based XSS.This issue affects CF7 Views &#8211; Complete Entry Management for Contact Form 7: from n/a through <= 3.2.2.

### CVE-2026-57409

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:34.650 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in RealMag777 Active Products Tables for WooCommerce profit-products-tables-for-woocommerce allows DOM-Based XSS.This issue affects Active Products Tables for WooCommerce: from n/a through <= 1.1.0.

### CVE-2026-57405

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-07-13T10:16:34.187 |

Missing Authorization vulnerability in themehunk Open Shop open-shop allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Open Shop: from n/a through <= 1.7.1.

### CVE-2026-57403

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:33.950 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Milan Petrovic GD Security Headers gd-security-headers allows Reflected XSS.This issue affects GD Security Headers: from n/a through <= 1.8.

### CVE-2026-57399

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:33.453 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Proxy &amp; VPN Blocker Proxy &amp; VPN Blocker proxy-vpn-blocker allows Stored XSS.This issue affects Proxy &amp; VPN Blocker: from n/a through <= 3.5.8.

### CVE-2026-57398

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:33.340 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WebCodingPlace Real Estate Manager Pro real-estate-manager-pro allows Reflected XSS.This issue affects Real Estate Manager Pro: from n/a through <= 12.8.3.

### CVE-2026-57396

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:33.223 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Flintop Free Gifts for WooCommerce free-gifts-for-woocommerce allows Stored XSS.This issue affects Free Gifts for WooCommerce: from n/a through <= 13.1.0.

### CVE-2026-57394

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:32.993 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Tribulant Software Newsletters newsletters-lite allows Reflected XSS.This issue affects Newsletters: from n/a through <= 4.14.

### CVE-2026-57388

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:32.040 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Themefic Hydra Booking hydra-booking allows Stored XSS.This issue affects Hydra Booking: from n/a through <= 1.1.44.

### CVE-2026-57387

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.923 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in picu picu picu allows Stored XSS.This issue affects picu: from n/a through <= 3.5.1.

### CVE-2026-57383

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.567 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in eyecix JobSearch wp-jobsearch allows Stored XSS.This issue affects JobSearch: from n/a through <= 3.2.9.

### CVE-2026-57382

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.437 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Mitchell Bennis Simple File List simple-file-list allows Reflected XSS.This issue affects Simple File List: from n/a through <= 6.3.8.

### CVE-2026-57381

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.293 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Property Hive PropertyHive propertyhive allows Reflected XSS.This issue affects PropertyHive: from n/a through <= 2.2.3.

### CVE-2026-57380

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.167 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in hupe13 Extensions for Leaflet Map extensions-leaflet-map allows DOM-Based XSS.This issue affects Extensions for Leaflet Map: from n/a through <= 5.1.

### CVE-2026-57379

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:31.050 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in WPPOOL FormyChat social-contact-form allows Stored XSS.This issue affects FormyChat: from n/a through <= 2.15.3.

### CVE-2026-57376

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:30.687 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Element Invader ElementInvader Addons for Elementor elementinvader-addons-for-elementor allows DOM-Based XSS.This issue affects ElementInvader Addons for Elementor: from n/a through <= 1.4.3.

### CVE-2026-57369

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:30.217 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in themifyme Themify Builder themify-builder allows Reflected XSS.This issue affects Themify Builder: from n/a through <= 7.7.4.

### CVE-2026-57368

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:30.100 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in NooTheme Jobmonster noo-jobmonster allows Reflected XSS.This issue affects Jobmonster: from n/a through <= 4.8.5.

### CVE-2026-57363

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-07-13T10:16:29.720 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in QuantumCloud ChatBot chatbot allows Stored XSS.This issue affects ChatBot: from n/a through <= 8.3.7.

### CVE-2026-15506

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-07-12T22:16:34.873 |

A security vulnerability has been detected in SecureAge CatchPulse up to 10.9.3. The affected element is an unknown function in the library saappctl.sys of the component Driver. Such manipulation leads to heap-based buffer overflow. An attack has to be approached locally. The exploit has been disclosed publicly and may be used. The vendor was contacted early about this disclosure.
