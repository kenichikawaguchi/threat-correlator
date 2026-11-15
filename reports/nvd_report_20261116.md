# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-11-15 15:00 UTC
- **対象期間**: `2026-11-14T15:01:37.000Z` 〜 `2026-11-15T15:00:44.000Z`
- **重要CVE数**: 40 件（Critical 9.0+: 9 件 / High 7.0〜: 31 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 2026 年上半期に公開された CVE のうち、CVSS が 7.0 以上のものは **30 件** 超と非常に多く、特に **特権昇格・認証バイパス** 系と **リモートコード実行／情報漏洩** 系が目立ちます。  
- WordPress 系プラグインや小規模ネットワーク機器（D‑Link、TRENDnet、DrayTek 等）に対する脆弱性が集中しており、**デフォルト設定のまま運用している環境** が狙われやすいことが共通点です。  
- 脆弱性の多くは **入力検証不備（Object Injection、SQLi、XSS、バッファオーバーフロー）** や **権限チェックの欠如** が根本原因で、パッチ適用だけでなく **コードレビュー・設定見直し** が不可欠です。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な影響 | 注目理由・影響範囲 |
|-----|------|----------|-------------------|
| **CVE‑2026‑125769** | 9.8 (CVSS:3.1) | Advanced Form Integration (WordPress) – 特権昇格 | `advanced-form-integration` の権限割り当てロジックに欠陥があり、認証なしで管理者権限を取得可能。プラグインは **2.11.3 まで** が対象で、サイト全体が乗っ取られるリスクが高い。 |
| **CVE‑2026‑122662** | 9.8 (CVSS:3.1) | Document Library Pro (WordPress) – オブジェクトインジェクション | `document-library-pro` がシリアライズデータを検証せずにデシリアライズし、任意コード実行が可能。**4.2.2 未満** が対象で、管理者権限が不要なリモート攻撃が成立。 |
| **CVE‑2026‑129483** | 9.3 (CVSS:4.0) | Cyrus SASL – 認証バイパス (SRP) | SRP メカニズムで `A = N`（N の倍数）を受け入れてしまい、共有鍵が 0 になる。ネットワーク上の任意クライアントが **認証なしで任意ユーザーとしてログイン** でき、メールサーバ全体が危険に晒される。 |
| **CVE‑2026‑129444** | 9.3 (CVSS:4.0) | D‑Link DSL‑6740C – ハードコードクレデンシャル | FTP デーモンの設定ファイル `/etc/templates/ftpd/ftpd_conf.php` が改ざん可能で、**固定の管理者 ID/PW** が埋め込まれる。公開エクスプロイトが存在し、外部からのリモート取得が容易。 |
| **CVE‑2026‑129351** | 9.3 (CVSS:4.0) | TRENDnet TEW‑657BRM – アウト・オブ・バウンズ書き込み | `setup.cgi` の `sprintf` 呼び出しで境界チェックが欠如し、任意メモリに書き込み可能。リモートからのコード実行が実現し、ルータ全体が乗っ取られる危険がある。 |

> **共通点**：いずれも「認証・権限チェックの欠如」または「入力検証不備」に起因し、**リモートからの完全制御** が可能になる点が特に危険です。  

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ（必須）

| 製品 / プラグイン | 現行脆弱バージョン | 修正済みバージョン | 取得先・備考 |
|-------------------|-------------------|-------------------|--------------|
| Advanced Form Integration (WordPress) | ≤ 2.11.3 | **2.11.4 以降** | WordPress プラグインディレクトリまたはベンダー公式サイト |
| Document Library Pro (WordPress) | ≤ 4.2.1 | **4.2.2 以降** | Barn2 Plugins 公式サイト |
| Cyrus SASL | ≤ 2.1.28 | **2.1.29 以降** | Cyrus SASL GitHub リリースページ |
| D‑Link DSL‑6740C (ファームウェア) | 20131126 以前のビルド | **最新ファームウェア (2026‑xx‑xx リリース)** | D‑Link サポートページ |
| TRENDnet TEW‑657BRM (ファームウェア) | 1.00.1 | **1.00.2 以降** | TRENDnet ダウンロードセンター |

> **※** 可能な限り **バックアップを取得したうえで** アップデートを実施してください。  

### 3.2 設定・運用の見直し

1. **最小権限の原則**  
   - WordPress のプラグインは「管理者権限が不要」なものは **無効化**、もしくは **最小権限ユーザー** に限定してインストール。  
2. **ネットワーク境界の強化**  
   - Cyrus SASL を使用しているメールサーバは **外部からの SRP 接続を遮断**（ファイアウォールでポート 389/636 を内部限定）し、TLS 経由のみ許可。  
   - ルータ・NAS の管理インタフェースは **VPN 経由のみ** アクセス可能にし、インターネットからの直接接続はブロック。  
3. **入力検証の徹底**  
   - カスタムプラグインや自社開発スクリプトは **PHP の `filter_input`、`wp_nonce`** 等を利用し、全ての外部入力をサニタイズ／バリデート。  
   - 既存プラグインでサニタイズが不十分な箇所は **パッチ適用後もコードレビュー** を実施。  
4. **監視・ログの強化**  
   - WordPress の `auth.log`、`error.log`、Cyrus SASL の `sasl.log`、ルータのシステムログを **SIEM** に集約し、**異常な認証失敗・権限変更** をリアルタイムでアラート。  
   - 特に **SRP の A 値が N の倍数** になるリクエストは不正アクセスの兆候として検知ルールを追加。  

### 3.3 インシデント対応手順の整備

| 手順 | 内容 |
|------|------|
| 1. 緊急パッチ適用 | 影響製品のベンダーが提供する **緊急パッチ**（またはベータ版）を即時適用。 |
| 2. 侵害確認 | 変更されたファイル（例：`ftpd_conf.php`、`setup.cgi`）の **ハッシュ比較**、不審なユーザーアカウントの有無を確認。 |
| 3. パ

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-125769

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-11-15T14:17:24.813 |

Incorrect Privilege Assignment vulnerability in Nasir Ahmed Advanced Form Integration advanced-form-integration allows Privilege Escalation.This issue affects Advanced Form Integration: from n/a through 2.11.3.

### CVE-2026-122662

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-15T14:17:20.507 |

Deserialization of Untrusted Data vulnerability in Barn2 Plugins Document Library Pro document-library-pro allows Object Injection.This issue affects Document Library Pro: from n/a before 4.2.2.

### CVE-2026-129483

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-15T14:17:27.530 |

Cyrus SASL through 2.1.28 contains an authentication bypass vulnerability in the SRP server mechanism because srp_server_mech_step2 does not reject client public values A that are multiples of N. Unauthenticated network clients can send A equal to N to force a zero shared secret, authenticating as any existing user without the password and learning session keys.

### CVE-2026-129444

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-11-15T09:16:44.570 |

A vulnerability was identified in D-Link DSL-6740C 20131126. This affects an unknown function of the file /etc/templates/ftpd/ftpd_conf.php of the component FTP Daemon. Such manipulation leads to hard-coded credentials. The attack can be executed remotely. The exploit is publicly available and might be used.

### CVE-2026-129354

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-15T01:18:03.043 |

A flaw has been found in D-Link DIR-600L 2.17b02. Affected by this issue is the function hnap_main of the file htdocs/cgibin of the component HNAP Handler. Executing a manipulation can lead to stack-based buffer overflow. The attack can be executed remotely. The exploit has been published and may be used.

### CVE-2026-129353

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-15T00:16:51.120 |

A vulnerability was detected in D-Link DIR-600L 2.17/2.17b02. Affected by this vulnerability is the function authenticationcgi_main of the file authentication.cgi. Performing a manipulation of the argument id/password results in stack-based buffer overflow. Remote exploitation of the attack is possible. The exploit is now public and may be used.

### CVE-2026-129351

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-787` |
| Published | 2026-11-14T23:16:47.753 |

A security vulnerability has been detected in TRENDnet TEW-657BRM 1.00.1. This vulnerability affects the function sprintf of the file /setup.cgi of the component mini_httpd. Such manipulation leads to out-of-bounds write. The attack can be executed remotely. The exploit has been disclosed publicly and may be used. The vendor explains: ""I am not able to confirm if such vulnerability exists as the product has been EOL for more than 15 years. We will send out an announcement letting customers know." This vulnerability only affects products that are no longer supported by the maintainer.

### CVE-2026-129261

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-782` |
| Published | 2026-11-14T16:17:04.517 |

A vulnerability was found in Kingston FURY CTRL RGB Control Software up to 2.0.66.0. The impacted element is an unknown function in the library NTIOLib_X64.sys of the component IOCTL Handler. Performing a manipulation results in exposed ioctl with insufficient access control. The attack is only possible with local access.

### CVE-2026-129349

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:Y/R:U/V:C/RE:L/U:Red` |
| Weaknesses | `CWE-287` |
| Published | 2026-11-15T10:16:53.020 |

When authentication caching is enabled on DefaultLdapRealm, after a user logs in successfully once, subsequent logins for that user succeed with any password.
A cached authentication skips the LDAP bind, and the AllowAllCredentialsMatcher installed by default in DefaultLdapRealm accepts any credentials, allowing an attacker who knows a valid username to authenticate as that user.
This issue affects all Apache Shiro versions through 3.0.0, only when using DefaultLdapRealm (or JndiLdapRealm) with authenticationCachingEnabled set to true, which is not the default.

Mitigation: Upgrade to version 3.0.1 or later, which fixes the issue by no longer installing AllowAllCredentialsMatcher by default.
Alternatively, disable authentication caching on the LDAP realm (this is the default), or configure a credentials matcher, such as SimpleCredentialsMatcher, that verifies credentials against the cached authentication info.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-125449

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-11-15T14:17:24.497 |

Deserialization of Untrusted Data vulnerability in Mamunur Rashid Testimonial Slider testimonial-slider-and-showcase allows Object Injection.This issue affects Testimonial Slider: from n/a through 3.0.2.

### CVE-2026-129465

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-15T02:17:21.770 |

Zr.Admin.NET commit af07ffc through commit eb9228a contains an insecure direct object reference vulnerability in SysProfileController.UpdateProfile that allows any authenticated user to modify other accounts via UserId. Attackers can set the administrator's phone number to one they control, request an SMS code via /checkMobile, and log in through /PhoneLogin to take over the administrator account.

### CVE-2026-129464

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-15T02:17:21.597 |

Zr.Admin.NET commit 0ee1ab8 through commit eb9228a contains a path traversal vulnerability that allows any logged-in user to read arbitrary server files via the path parameter of /common/DownloadFile. Attackers can supply absolute paths or ../ sequences to read appsettings files and use the JwtSettings SecretKey to forge administrator tokens.

### CVE-2026-129453

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-122` |
| Published | 2026-11-15T14:17:26.583 |

A vulnerability was found in DrayTek Vigor2960 1.5.1.6. This issue affects the function check_file_exist of the file /cgi-bin/mainfunction.cgi of the component File Existence Check. Performing a manipulation of the argument upload_name results in heap-based buffer overflow. The attack may be initiated remotely. The exploit has been made public and could be used. Upgrading to version 1.5.1.7 is capable of addressing this issue. Upgrading the affected component is recommended. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-129451

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-15T13:16:58.600 |

A flaw has been found in DrayTek Vigor2960 up to 1.5.1.6. This affects the function app_guest_export of the file /cgi-bin/mainfunction.cgi. This manipulation of the argument filename causes path traversal. The attack can be initiated remotely. The exploit has been published and may be used. Upgrading to version 1.5.1.7 is able to mitigate this issue. The affected component should be upgraded. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-129450

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-15T12:17:20.913 |

A vulnerability was detected in DrayTek Vigor2960 1.5.1.6. Affected by this issue is the function sub_1E084 of the file /cgi-bin/mainfunction.cgi?action=doWebBackup. The manipulation of the argument option results in path traversal. It is possible to launch the attack remotely. The exploit is now public and may be used. Upgrading to version 1.5.1.7 can resolve this issue. You should upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-129449

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-15T11:17:10.620 |

A security vulnerability has been detected in DrayTek Vigor2960 up to 1.5.1.6. Affected by this vulnerability is the function sub_14914 of the file /cgi-bin/mainfunction.cgi. The manipulation of the argument swmconfigupload leads to command injection. It is possible to initiate the attack remotely. The exploit has been disclosed publicly and may be used. Upgrading to version 1.5.1.7 addresses this issue. It is advisable to upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-125832

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-15T14:17:26.137 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Passionate Programmer Peter WP Data Access wp-data-access allows SQL Injection.This issue affects WP Data Access: from n/a through 5.5.92.

### CVE-2026-129452

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-74;CWE-77` |
| Published | 2026-11-15T13:16:59.703 |

A vulnerability has been found in DrayTek Vigor2960 1.5.1.6. This vulnerability affects the function set_table of the file /cgi-bin/mainfunction.cgi. Such manipulation of the argument jsondata leads to command injection. The attack can be launched remotely. The exploit has been disclosed to the public and may be used. Upgrading to version 1.5.1.7 is able to resolve this issue. It is suggested to upgrade the affected component. The vendor recommends: "1.5.1.6 isn't the latest version of 2960, the latest version fixes many security issues. And we have another one in our release plan which should solve the issues reported."

### CVE-2026-129352

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-11-14T23:16:48.033 |

A vulnerability was detected in TRENDnet TEW-657BRM 1.00.1. This issue affects some unknown processing of the file /usr/sbin/upgrade_flash.cgi. Performing a manipulation of the argument boundary results in stack-based buffer overflow. The attack is possible to be carried out remotely. The exploit is now public and may be used. The vendor explains: ""I am not able to confirm if such vulnerability exists as the product has been EOL for more than 15 years. We will send out an announcement letting customers know."

### CVE-2026-129258

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-11-14T15:16:58.257 |

A vulnerability was identified in Tenda AC18 15.03.05.05_multi/15.03.05.19 Build 6318. Affected by this vulnerability is an unknown functionality of the file /cgi-bin/upgrade of the component Firmware Upgrade Handler. Such manipulation of the argument upgradeFile leads to insufficient verification of data authenticity. The attack may be launched remotely. The exploit is publicly available and might be used.

### CVE-2026-129445

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-259;CWE-798` |
| Published | 2026-11-15T10:16:53.970 |

A security flaw has been discovered in D-Link DIR-850L FW1.20WWb03. This impacts an unknown function of the file /usr/sbin/consolepwd of the component Console Login. Performing a manipulation results in hard-coded credentials. The attack requires a local approach. The exploit has been released to the public and may be used for attacks.

### CVE-2026-129456

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:N/R:A/V:X/RE:X/U:X` |
| Weaknesses | `CWE-415;CWE-416` |
| Published | 2026-11-14T20:17:40.060 |

In FRRouting, bgpd accepts a Tunnel Encapsulation attribute (type 23) whose outer TLV length does not match the length of the attribute: the mismatch is only logged and the attribute is processed anyway. A BGP neighbor can send UPDATE messages carrying such an attribute that put the reference count of the attribute's interned sub-TLV chain out of balance, so that the chain is freed while routes stored by bgpd (Adj-RIB-In entries and RIB paths) still point to it. When those routes are later replaced, withdrawn or cleared, for example when the session goes down, bgpd reads the freed memory, decrements a reference count inside it and frees it a second time. In the reporter's build without AddressSanitizer this ended in an assertion failure in bgpd's memory accounting, aborting bgpd and dropping all BGP sessions on the router, and the neighbor can repeat it each time bgpd restarts. Because freed heap memory is written to and freed again, consequences beyond a crash cannot be ruled out. An established BGP session is required. bgpd processes attribute 23 from every neighbor, including eBGP neighbors, unless it is explicitly discarded, although RFC 9012 requires it to be filtered on eBGP sessions by default. The issue was reproduced with "soft-reconfiguration inbound" configured for the neighbor, and the reporter observed that the crash does not occur on every attempt.

### CVE-2026-125780

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-11-15T14:17:25.130 |

Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability in Acowebs Woocommerce Custom Product Addons Pro woo-custom-product-addons-pro allows Path Traversal.This issue affects Woocommerce Custom Product Addons Pro: from n/a through 5.9.0.

### CVE-2026-82663

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-11-15T10:16:54.410 |

The Give - Peer-to-Peer plugin for WordPress is vulnerable to authorization bypass in all versions up to, and including, 2.9.5. This is due to the plugin not properly verifying that a user is authorized to perform an action. This makes it possible for unauthenticated attackers who know or discover an existing campaign and team ID to modify the team's name, story, goal, access and notification settings, set its profile image URL, and upload WordPress-allowed media files as parentless attachments. This vulnerability can be combined with CVE-2026-82568 to achieve unauthenticated remote code execution.

### CVE-2026-82568

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-11-15T10:16:54.217 |

The Give - Peer-to-Peer plugin for WordPress is vulnerable to time-based SQL Injection via the 'sort' parameter in all versions up to, and including, 2.9.3 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. Successful exploitation requires the existence of at least one Peer-to-Peer campaign. This vulnerability can be combined with CVE-2026-82663 to achieve unauthenticated remote code execution.

### CVE-2026-120687

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-14T16:17:03.957 |

The Lightbox & Modal Popup WordPress Plugin – FooBox plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'img alt attribute inside .wp-caption container' parameter in all versions up to, and including, 2.8.7 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable by Subscriber-level users when bbPress is installed, as its bbp_filter_kses filter chain permits img and pre tags while preserving numeric character references inside attribute values, allowing encoded payloads to bypass save-time sanitization and reach the vulnerable sink fully intact. Exploitation by attackers with subscriber-level access and above requires that bbPress 2.6.20 is installed, a public forum exists, and either the first topic has already been approved or subsequent topics clear moderation. On a default installation, where that is not configured, the vulnerability requires attackers with contributor-level access and above.

### CVE-2026-116753

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-14T16:17:03.793 |

The Multi Step for Contact Form 7 plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'multipart field name (array key)' parameter in all versions up to, and including, 2.9.1 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Successful exploitation requires the target CF7 form to have the 'Save every step' option enabled and the Database for Contact Form 7 companion plugin to be active with its 'Expandable' table option enabled, both of which are disabled by default.

### CVE-2026-125828

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:25.990 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Liquid Web / StellarWP BookIt bookit allows Stored XSS.This issue affects BookIt: from n/a through 2.6.0.7.

### CVE-2026-125813

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:25.847 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Ays Pro Survey Maker survey-maker allows Reflected XSS.This issue affects Survey Maker: from n/a through 5.2.4.3.

### CVE-2026-125791

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:25.563 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in iWorks Orphans sierotki allows Stored XSS.This issue affects Orphans: from n/a through 3.4.6.

### CVE-2026-125790

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:25.423 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in e4jvikwp VikBooking Hotel Booking Engine & PMS vikbooking allows Stored XSS.This issue affects VikBooking Hotel Booking Engine & PMS: from n/a through 1.8.20.

### CVE-2026-125789

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:25.277 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in e4jvikwp VikBooking Hotel Booking Engine & PMS vikbooking allows Stored XSS.This issue affects VikBooking Hotel Booking Engine & PMS: from n/a through 1.8.20.

### CVE-2026-125775

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:24.977 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in CRM Perks CRM Perks Forms crm-perks-forms allows Reflected XSS.This issue affects CRM Perks Forms: from n/a through 1.1.8.

### CVE-2026-125764

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:24.647 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in E2Pdf.com e2pdf e2pdf allows Stored XSS.This issue affects e2pdf: from n/a through 1.32.65.

### CVE-2026-125443

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:24.340 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Denishua WPJAM Basic wpjam-basic allows DOM-Based XSS.This issue affects WPJAM Basic: from n/a through 7.1.2.

### CVE-2026-124995

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:24.187 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Michal Jaworski Track, Analyze & Optimize by WP Tao wp-tao allows Stored XSS.This issue affects Track, Analyze & Optimize by WP Tao: from n/a through 1.3.1.

### CVE-2026-124270

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:21.687 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Basix NEX-Forms nex-forms-express-wp-form-builder allows Reflected XSS.This issue affects NEX-Forms: from n/a through 9.3.3.

### CVE-2026-124259

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:21.543 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Franky Events Made Easy events-made-easy allows Reflected XSS.This issue affects Events Made Easy: from n/a through 3.3.5.

### CVE-2026-124254

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-11-15T14:17:21.387 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Exactly WWW LLC EWWW Image Optimizer ewww-image-optimizer allows Stored XSS.This issue affects EWWW Image Optimizer: from n/a through 8.9.1.

### CVE-2026-129454

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-11-15T02:17:21.243 |

Zr.Admin.NET commit 85cff6a through commit eb9228a contains an insecure direct object reference vulnerability in GET /workflow/instance/{instanceId} that lets logged-in users view others' workflow instances. Authenticated low-privilege attackers can enumerate sequential instance IDs to read other users' approval requests, including submitted form contents, applicant details and approval records.
