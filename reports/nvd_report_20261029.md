# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-10-28 15:00 UTC
- **対象期間**: `2026-10-27T15:01:29.000Z` 〜 `2026-10-28T15:00:34.000Z`
- **重要CVE数**: 241 件（Critical 9.0+: 47 件 / High 7.0〜: 194 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコア 7.0 以上のものは **30 件以上** に上り、特に **Adobe Campaign Classic** と **Dell PowerProtect Data Domain** 系列で複数の高危険度（9.8 〜 10.0）脆弱性が同時に報告されています。  
- **SQL/OS コマンドインジェクション** と **認可不備** が共通して見られ、低権限ユーザーでもリモートコード実行 (RCE) が可能になるケースが多数。  
- WordPress エコシステムでも **任意ファイルアップロード** や **認証バイパス** が続出し、プラグイン単位でのサプライチェーンリスクが顕在化。  
- インフラ系製品（Dell PowerProtect、Fireware OS、EPICS Base）では **スタックバッファオーバーフロー** や **ハードコード鍵** が報告され、ネットワーク境界からの直接攻撃が想定されます。  

> **傾向**：2026 年は「低権限からのコード実行」や「認証回避」に焦点が当たった脆弱性が集中し、特に **Web アプリケーション層** と **管理インターフェース** が狙われやすいことが分かります。

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品・コンポーネント | 主な脆弱性種別 | 影響範囲・リスク |
|-----|--------|----------------------|----------------|-------------------|
| **CVE‑2026‑105781** | 10.0 | Adobe Campaign Classic (ACC) | SQL Injection → 任意コード実行 (特権昇格不要) | 低権限ユーザーが任意の SQL を実行でき、サーバ上で任意コードを実行可能。顧客データベースやメール配信ロジックが完全に乗っ取られる危険性。 |
| **CVE‑2026‑105780** | 9.9 | Adobe Campaign Classic (ACC) | 認可不備 → 任意コード実行 | 低権限ユーザーが管理者権限相当の操作を実行できる。設定変更やスクリプト実行が可能になるため、システム全体が危殆化。 |
| **CVE‑2026‑104353** | 9.9 | Adobe Campaign Classic (ACC) | OS Command Injection | ユーザー入力がそのままシェルコマンドに渡され、任意の OS コマンドが実行可能。サーバ上でのマルウェア配置や情報窃取が即座に可能。 |
| **CVE‑2026‑115968** | 9.8 | WordPress **Ultimate Member** プラグイン (≤ 2.13.1) | オブジェクトインジェクション (デシリアライズ) | 攻撃者が任意の PHP オブジェクトを注入し、管理者権限でコード実行が可能。プラグインが広く利用されているため、影響サイト数は膨大。 |
| **CVE‑2026‑103780** | 9.8 | Dell PowerProtect Data Domain (Feature Release 7.7.1‑8.8, LTS 7.13‑8.6) | スタックバッファオーバーフロー (リモート) | 認証不要で遠隔からクラッシュさせられ、条件次第で RCE が成立。バックアップ・アーカイブ基盤全体が停止・改ざんリスクに晒される。 |

> **選定理由**  
> - **スコアが最高 (10.0) または 9.8 以上** で、**認可・入力検証の欠如** が共通。  
> - いずれも **低権限ユーザー** あるいは **認証なし** で攻撃が成立し、**被害拡大のスピードが速い**。  
> - 製品の市場シェアが大きく（Adobe Campaign、WordPress、Dell バックアップ）、**組織全体の運用・データ保護に直結** する点が重要。

---

## 3. 推奨アクション  

### 3.1 共通の緊急対策
- **脆弱性スキャンの実施**：Nessus、Qualys、OpenVAS などで上記 CVE を対象にフルスキャンを行い、未パッチのインスタンスを即座に特定。  
- **ネットワーク隔離**：管理インターフェース（ACC の管理画面、PowerProtect の Web UI）への外部アクセスを **IP アクセスコントロールリスト (ACL)** で制限し、VPN 経由のみ許可。  
- **最小権限の徹底**：ユーザーロール・権限設定を見直し、特に ACC の「低権限」ユーザーに対して **SQL 実行権限** や **シェルコマンド実行権限** が付与されていないか確認。  

### 3.2 製品別具体的パッチ適用・バージョンアップ

| 製品 | 現行バージョン (対象) | 推奨バージョン / パッチ | パッケージ名・取得先 |
|------|----------------------|------------------------|----------------------|
| **Adobe Campaign Classic** | 2026.0‑2026.9 系列 (全般) | **2026.10 以降** のセキュリティパッチ (ACC‑2026‑SP‑10) | Adobe Experience Cloud の **Security Update** ダウンロードページ |
| **Ultimate Member (WordPress)** | ≤ 2.13.1 | **2.13.2** 以上 | WordPress 管理画面 → 「プラグイン > 更新」または公式リポジトリ `ultimate-member` |
| **Dell PowerProtect Data Domain** | Feature Release 7.7.1‑8.8、LTS 7.13‑8.6 | **8.9.0** (Feature) または **LTS 8.7.0** 以上 | Dell Support → **PowerProtect Data Domain – Firmware Update** |
| **WordPress Contact Manager** | ≤ 9.1.2 | **9.1.3** 以上 (任意ファイルアップロード修正) | WordPress プラグインリポジトリ `contact-manager` |
| **Jackson‑databind** | 2.15.0 以前 | **2.15.2** 以上 (CVE‑2026‑110879 修正) | Maven Central `com.fasterxml.jackson.core:jackson-databind` |
| **MLflow** | 3.12.0rc0‑3.17.0 | **3.18.0** 以上 (スコアラーデシリアライズ修正) | PyPI `mlflow` |
| **EPICS Base** | 7.0.10 以前 | **7.0.11** 以上 (整数オーバーフロー

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-105781

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T17:16:56.430 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary SQL commands, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105780

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-27T17:16:56.313 |

Adobe Campaign Classic (ACC) is affected by an Incorrect Authorization vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-105489

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T17:16:56.080 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-104353

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T17:16:55.717 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-104351

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-27T17:16:55.593 |

Adobe Campaign Classic (ACC) is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-115968

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T14:16:58.013 |

Deserialization of Untrusted Data vulnerability in Ultimate Member Ultimate Member ultimate-member allows Object Injection.This issue affects Ultimate Member: from n/a through 2.13.1.

### CVE-2026-114278

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T12:17:39.773 |

The che-machine-exec service constructs a shell command by concatenating user-controlled input (the username and namespace fields from the /exec/init and /exec/config JSON endpoints) into a double-quoted sh -c "echo "..." > ..." invocation without any escaping. When che-machine-exec is run with authentication disabled (its default), any network-reachable attacker can achieve remote code execution in containers che-machine-exec is configured to access, via shell command substitution ($(...) or backticks).

### CVE-2026-103780

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T11:17:14.113 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain a Stack-based Buffer Overflow vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to command execution.

### CVE-2026-86384

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-321` |
| Published | 2026-10-28T10:17:09.433 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Use of Hard-coded Cryptographic Key vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to credential exposure. The credentials may be used to access the system with privileges of the compromised user.

### CVE-2026-86400

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-28T09:17:08.040 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Authentication vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to arbitrary command execution with root privileges. This is a critical severity vulnerability as it allows an attacker to take complete control of the system. Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-86397

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T09:17:07.663 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Authentication vulnerability. An unauthenticated attacker with remote access could potentially exploit this vulnerability, leading to privileged account creation. This is a critical severity vulnerability as it allows an attacker to take complete control of the system. Dell recommends customers to upgrade at the earliest opportunity.

### CVE-2026-109218

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T07:16:44.120 |

The Contact Manager plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 9.1.2 via the add_message function. This is due to an incomplete extension blacklist that fails to detect dangerous extensions when a trailing dot causes the extension-derivation routine to return an empty string, which sanitize_file_name() then silently removes before the file is written to disk. This makes it possible for unauthenticated attackers to upload files that may be executable, which makes remote code execution possible. Successful code execution additionally requires the server to use Apache with libapache2-mod-php (which maps .phar to PHP by default) and the attacker to retrieve the uploaded file within the brief window before it is removed by unlink() at end of request.

### CVE-2026-84999

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T03:17:16.157 |

The Pie Register Premium plugin for WordPress is vulnerable to Unrestricted File Type Upload in all versions up to, and including, 3.8.4.0 via the piereg_file_upload function. This is due to the plugin performing file type validation via wp_check_filetype and wp_check_filetype_and_ext but never checking whether those validation calls produced errors before move_uploaded_file() is called, combined with no nonce or capability check on the AJAX handler. This makes it possible for unauthenticated attackers to upload files of dangerous types (e.g. PHP scripts) that may be executable, which makes remote code execution possible. The server returns the generated destination filename in the response, giving the attacker the exact path needed to trigger the uploaded file.

### CVE-2026-106013

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-28T02:17:01.303 |

The Jupiter X Core plugin for WordPress is vulnerable to Authentication Bypass via the Twitter/X Social Login handler in all versions up to and including 4.61.0. The vulnerability exists within the verify_twitter_callback function because after exchanging the visitor's oauth_verifier for their access token, the handler never calls setOauthToken() to reassign the returned credentials to the TwitterOAuth client, causing the subsequent account/verify_credentials API call to remain signed with the site operator's stored Access Token and Access Token Secret rather than the authenticating visitor's token. This causes the X API to return the profile of the X application owner instead of the signing-in visitor, and the plugin then resolves and authenticates a WordPress account solely by matching that owner's email address via wp_set_auth_cookie(), allowing unauthenticated attackers to gain authenticated access as the WordPress user whose email corresponds to the X app owner, who is typically the site administrator.

### CVE-2026-110879

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T01:16:55.180 |

jackson-databind validates the outer class of a class-name type ID but accepts attacker-selected classes inside its generic arguments, even when those classes violate the declared type or would be rejected as direct type IDs. This bypasses the generic-argument validation added for CVE-2026-54512 (GHSA-j3rv-43j4-c7qm), of which this is an incomplete fix.



DatabindContext._resolveAndValidateGeneric() checks the outer class against the declared base type and then passes each argument from the type ID to _validateTypeParameter(), which validates the argument against the outer base type rather than enforcing its corresponding declared generic binding. It also invokes validators with arguments that have not passed the subtype check those validators expect. Under the default DefaultBaseTypeLimitingValidator this accepts an unrelated class inside a generic subtype even when the same class is rejected as a direct type ID. Where an allowIfBaseType(...) rule approves the outer type, Jackson substitutes LaissezFaireSubTypeValidator, so the configured validator no longer restricts the embedded arguments. The element type of a plain array type ID such as [Lpkg.Gadget; is likewise left unvalidated once the array's base type is approved.



Affected paths include annotation-based class-name polymorphism with a default Jackson 3.x JsonMapper, configured default typing in both Jackson 2.x and 3.x, and integrations that expose that default typing. The default-validator case requires no application-authored validator: with @JsonTypeInfo(use = Id.CLASS), a direct gadget type ID is rejected as "Not a subtype", while a type ID naming a generic wrapper around the same gadget is accepted and deserialized, including attacker-supplied bean properties. Where class-name default typing permits Map, a property declared as Map<String,String> accepts HashMap<FileSystemXmlApplicationContext,String>; map-key discovery then passes the attacker-controlled JSON property name to the selected class's one-string constructor. With Spring on the classpath and attacker-controlled XML the application can load, that constructor loads the XML and invokes ProcessBuilder.start() under the application account, giving arbitrary command execution.



This issue affects com.fasterxml.jackson.core:jackson-databind from 2.10.0 and tools.jackson.core:jackson-databind from 3.0.0. Releases before 2.10.0 are not affected, because PolymorphicTypeValidator was introduced in jackson-databind 2.10.0.

### CVE-2026-116692

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94;CWE-470` |
| Published | 2026-10-27T21:18:05.013 |

MLflow is an open source AI engineering platform for agents, large language models, and machine learning models. From 3.12.0rc0 until 3.17.0, third-party scorer deserialization in mlflow/genai/scorers/base.py accepts request-selected descendants of THIRD_PARTY_SCORER_ALLOWED_MODULES rather than requiring an exact allowed module. A caller can use MLflow artifact endpoints to place a Python module beneath a writable allowed package and submit its module and class through /ajax-api/3.0/mlflow/scorer/invoke. Scorer.model_validate_json() imports the module and constructs the class before trace processing. Authentication-disabled deployments permit this code execution without credentials, while basic-auth deployments require a principal capable of creating an experiment and run and uploading artifacts. In either configuration, the allowed scorer package must be writable by the server process. This issue is fixed in version 3.17.0.

### CVE-2026-115904

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T13:17:05.400 |

Topluyo is a social networking platform. A vulnerability exists in Topluyo Desktop for Linux prior to version 2026.9.2410 where user-controlled URLs are unsafely processed, leading to OS Command Injection via the `openExternalLinks()` routine in `utils.js`. An attacker who controls a target URL can execute arbitrary operating system commands with the privileges of the user running the application upon opening the link. Version 2026.9.2410 patches the issue.

### CVE-2026-103799

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T11:17:14.390 |

Dell PowerProtect Data Domain Management Center, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain a Missing Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to unauthorized system operation on managed systems.

### CVE-2026-103792

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T11:17:14.250 |

Dell PowerProtect Data Domain Management Center, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized access to managed systems.

### CVE-2026-48360

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-27T17:17:00.740 |

Adobe Connect is affected by an Improper Control of Generation of Code ('Code Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-116863

| 項目 | 値 |
|------|-----|
| CVSS | `9.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-27T16:17:30.543 |

Cross-Site Request Forgery (CSRF) vulnerability in Tribulant Software Newsletters newsletters-lite allows Cross Site Request Forgery.This issue affects Newsletters: from n/a through 4.18.2.

### CVE-2026-103594

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787;CWE-1284` |
| Published | 2026-10-27T16:17:28.517 |

A stack-based buffer overflow vulnerability in Fireware OS's WireGuard configuration processing allows a remote attacker that has man-in-the-middle TLS-decrypted access between the Firebox and WatchGuard Cloud to create a Denial of Service condition and potentially execute arbitrary code by tampering with a FireCloud Gateway configuration payload.

### CVE-2026-105420

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T14:16:56.230 |

Wing FTP Server does not verify user's base folder. An attacker with admin privileges can add user directories via scripts, allowing the added directories to escape the base folder. This allows the attacker to write files on the system and can lead to remote code execution with process owner privileges.Critically, since the installation guide mentions running the command with `sudo`, the files are created as “root.”




This issue was fixed in version 8.2.6.

### CVE-2026-112197

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-10-28T11:17:15.073 |

Vulnerability due to a lack of authentication in critical functions of the NoviGest Desktop App's Java RMI service. An attacker with network access to the service can invoke remote methods without authentication, obtain sensitive credentials, and execute arbitrary SQL queries on PostgreSQL. The elevated privileges of the database account allow these capabilities to be chained together to execute operating system commands on the server, compromising its confidentiality, integrity, and availability.

### CVE-2026-104383

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-28T05:16:59.533 |

Improper Control of Generation of Code in Pigeon MFA service in EagleCloud Aquila versions through 2.6.7.2 on on-premises platforms allows authenticated remote attackers to execute arbitrary code via code injection

### CVE-2026-90465

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-290;CWE-306;CWE-862` |
| Published | 2026-10-27T16:17:31.640 |

A missing authentication vulnerability in the FireCluster Sync processing allows an attacker positioned on the cluster interconnect, such as a compromised cluster peer or an on-path network attacker, to invoke privileged firewall management actions as root by sending a specially crafted request.

### CVE-2026-115607

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T13:17:04.993 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Crowd Favorite DXP ToolKit dxp-toolkit allows SQL Injection.This issue affects DXP ToolKit: from n/a through 2.0.1.

### CVE-2026-111411

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T13:17:04.167 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Aman FunnelKit Automations wp-marketing-automations allows Blind SQL Injection.This issue affects FunnelKit Automations: from n/a through 3.8.5.2.

### CVE-2026-114595

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-27T17:16:58.530 |

In EPICS Base release 7.0.10 and prior, an integer overflow in network request processing can cause memory to be allocated with an incorrect size. Subsequent handling of attacker supplied data may result in memory corruption, denial of service, or potential remote code execution.

### CVE-2026-104350

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T17:16:55.457 |

Adobe Campaign Classic (ACC) is affected by a reflected Cross-Site Scripting (XSS) vulnerability. An attacker could exploit this vulnerability to inject malicious scripts into a web page, potentially gaining elevated access or control over the victim's account or session. Exploitation of this issue requires user interaction in that a victim must visit a maliciously crafted URL or interact with a compromised web page. Scope is changed.

### CVE-2026-118375

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-28T03:17:14.077 |

llama.cpp b8841 before b11865 contains an out-of-bounds write vulnerability in the ggml-rpc RDMA transport rdma_recv() function that allows unauthenticated peers to overflow the rpc-server stack. Attackers advertising RDMA capabilities in the HELLO message can send up to 256 KiB into a 1-byte stack variable in rpc_serve_client(), crashing the server or potentially executing code.

### CVE-2026-93866

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190;CWE-288;CWE-787` |
| Published | 2026-10-27T16:17:33.013 |

An integer overflow vulnerability in the WebSocket connection handling used by WatchGuard Fireware OS's Access Portal allows a remote, unauthenticated attacker to write beyond the bounds of a heap buffer by sending a specially crafted request while the Access Portal feature is enabled.

### CVE-2026-93865

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-306;CWE-862` |
| Published | 2026-10-27T16:17:32.843 |

A missing authentication vulnerability in the Fireware OS FireCluster synchronization daemon allows a remote, unauthenticated attacker to invoke privileged system-level administrative actions by sending a specially crafted request to the FireCluster management IP when the clustering feature is enabled.

### CVE-2026-93857

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120;CWE-121;CWE-787` |
| Published | 2026-10-27T16:17:32.463 |

A stack-based buffer overflow vulnerability in Fireware OS's SIP proxy allows a remote, unauthenticated attacker to execute arbitrary code by sending a specially crafted request through a policy that uses the SIP proxy.

### CVE-2026-112710

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-131` |
| Published | 2026-10-27T16:17:30.120 |

A heap-based buffer overflow vulnerability exists in the Fireware OS authentication service allows an attacker who controls or intercepts traffic to the configured Active Directory server to create a denial of service condition and potentially execute arbitrary code by returning a specially crafted response.

### CVE-2026-112709

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-131;CWE-787` |
| Published | 2026-10-27T16:17:29.997 |

A heap-based buffer overflow vulnerability in the Fireware OS authentication service allows an attacker who controls or intercepts traffic to the configured Active Directory server to create a denial of service condition and potentially execute arbitrary code by returning a specially crafted response.

### CVE-2026-67074

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-94` |
| Published | 2026-10-28T13:17:08.463 |

HCL BigFix AEX is affected by a Remote Code Execution Vulnerability . It may allow attackers to execute code with the privileges of the affected application or service, potentially leading to unauthorized access, data exposure, or system compromise.

### CVE-2026-14571

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T10:17:08.780 |

A Blind SQL Injection vulnerability in Futurum Software’s management software, caused by a lack of adequate validation and sanitisation of user-provided inputs in queries to the private area’s database, as well as by an incorrect WAF configuration. This weakness allows the protection mechanisms to be bypassed solely by sending manipulated HTTP requests. Successful exploitation of the vulnerability could allow an unauthenticated attacker to execute arbitrary queries against the database, extract its complete structure and gain access to sensitive customer information, including personally identifiable information (PII).

### CVE-2026-90717

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:L` |
| Weaknesses | `CWE-290` |
| Published | 2026-10-28T09:17:08.297 |

Dell PowerProtect Data Domain Management Center, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Authentication Bypass by Spoofing vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges. This vulnerability could impact other managed Data Domain systems.

### CVE-2026-58256

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-10-27T23:17:06.140 |

GRR is a resource management and reservation application. Prior to the advisory-reported fixed version 4.5.0, an administrator can inject malicious PHP through LDAP connector configuration parameters such as `ldap_filter`, poisoning `/personnalisation/config_ldap.inc.php` and permitting remote code execution. The administrator must first successfully connect to an LDAP server, which can be attacker-controlled, and then submit malicious input on the subsequent connector settings page. The advisory reports this issue as fixed in version 4.5.0.

### CVE-2026-112352

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-565` |
| Published | 2026-10-27T20:17:12.997 |

Sunhillo SureLine before 9.1.5 contains an authentication bypass vulnerability that allows an unauthenticated remote attacker to impersonate any user with an active web session by forging a session cookie containing only a cleartext username with no random identifier or integrity protection. Attackers can guess default account names such as Admin or sftp_user and submit a forged username cookie to satisfy the login check in checkLogin (libwebcmn.so) and networkDiag.cgi, chaining into root command execution.

### CVE-2026-108142

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-636` |
| Published | 2026-10-27T17:16:57.553 |

A vulnerability allowing an unauthenticated attacker to bypass authorization on the CDP Coordinator Service.

### CVE-2026-108015

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-10-27T17:16:57.187 |

Private keys for eight eMudhra intermediate CA certificates have been  compromised https://emudhra.we-have-a-problem.com/ , which impacts certificate trust for outbound network request features of HCL Notes Client.  An unauthenticated network attacker could spoof server certificates to execute a man in the middle (MITM) attack, enabling them to intercept and/or modify the content of outbound TLS connections.

### CVE-2026-108014

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-327` |
| Published | 2026-10-27T17:16:57.040 |

Private keys for eight eMudhra intermediate CA certificates have been  compromised https://emudhra.we-have-a-problem.com/ , which impacts certificate trust for outbound network request features of HCL Domino Server.  An unauthenticated network attacker could spoof server certificates to execute a man in the middle (MITM) attack, enabling them to intercept and/or modify the content of outbound TLS connections.

### CVE-2026-105779

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T17:16:56.193 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in a Security feature bypass. A low-privileged attacker could leverage this vulnerability to bypass security measures and gain unauthorized read and limited write access. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-104354

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T17:16:55.837 |

Adobe Campaign Classic (ACC) is affected by an Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability that could result in arbitrary code execution in the context of the current user. An attacker with high privileges could exploit this vulnerability to execute arbitrary code. Exploitation of this issue does not require user interaction. Scope is changed.

### CVE-2026-106076

| 項目 | 値 |
|------|-----|
| CVSS | `9.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T17:16:56.553 |

A vulnerability allowing an authenticated organization-transfer peer to inject SQL into the configuration database of the source Veeam Backup for Microsoft 365 server, leading to cross-tenant read and write of configuration data and remote code execution as the PostgreSQL service account.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-59177

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-1327` |
| Published | 2026-10-28T14:17:04.747 |

ESPHome Device Builder Dashboard is a dashboard for the ESPHome home management software. Prior to 1.0.10, the `Home Assistant` add-on's trusted `ingress` site binds to `0.0.0.0` while intentionally skipping dashboard authentication because the supervisor is expected to authenticate requests upstream. Host networking, required for mDNS, also binds this no-auth site to the `Home Assistant` host's LAN interface. Any device on that local network can therefore connect directly to the `ingress` port, bypass the supervisor, and obtain the full dashboard without credentials or operator misconfiguration. Dashboard capability includes compile-time Python execution through `external_components:`, shell execution through compile and validation subprocesses, and arbitrary access to configuration and data files, compromising the mounted `Home Assistant` configuration and managed ESPHome devices. The standalone Docker dashboard and the password-gated public port 6052 are not affected. This issue is fixed in version 1.0.10.

### CVE-2026-116389

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T14:16:58.377 |

Deserialization of Untrusted Data vulnerability in crossi72 Phoenix Media Rename phoenix-media-rename allows Object Injection.This issue affects Phoenix Media Rename: from n/a through 3.13.5.

### CVE-2026-116391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T13:17:05.687 |

Deserialization of Untrusted Data vulnerability in GS Plugins GS Logo Slider gs-logo-slider allows Object Injection.This issue affects GS Logo Slider: from n/a through 3.8.9.

### CVE-2026-86378

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T11:17:26.990 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain a Stack-based Buffer Overflow vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to unauthorized access.

### CVE-2026-86385

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-273` |
| Published | 2026-10-28T10:17:09.570 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, contain an Improper Check for Dropped Privileges vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to elevation of privileges.

### CVE-2026-86398

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T09:17:07.790 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to filesystem access for attacker.

### CVE-2026-86396

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T09:17:07.540 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to command execution.

### CVE-2026-92797

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-28T08:16:30.250 |

The MemberPress plugin for WordPress is vulnerable to Cross-Site Request Forgery in versions up to, and including, 1.14.1. This is due to a bypassable nonce verification check in the save_profile_fields() function that uses an isset() condition at line 1119, allowing the security check to be completely bypassed by simply omitting the nonce parameter from the request. This makes it possible for unauthenticated attackers to change authenticated users' email addresses via a forged request granted they can trick an authenticated user into performing an action such as clicking on a link, leading to account takeover through password reset functionality.

### CVE-2026-111120

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-28T07:16:46.837 |

The VikRentCar Car Rental Management System plugin for WordPress is vulnerable to Cross-Site Request Forgery in all versions up to, and including, 1.4.8. This is due to missing or incorrect nonce validation on the condtext_update_tmpl function. This makes it possible for unauthenticated attackers to write arbitrary PHP code to the plugin's executable template files such as site/helpers/email_tmpl.php, which are later include()d by loadEmailTemplate() and loadPdfTemplate(), achieving remote code execution on the server via a forged request granted they can trick a site administrator into performing an action such as clicking on a link. The injected PHP payload bypasses sanitization because the plugin's own __PHP_OPEN__/__PHP_CLOSE__ placeholder expansion and cleanPHPSourceCode() logic explicitly reverse both sanitize_text_field filtering and saveHTML() HTML-encoding, restoring a literal <?php...?> payload to live PHP before it is written to disk. Successful exploitation additionally requires an action by an administrator — the attacker cannot trigger the vulnerability on their own.

### CVE-2026-109384

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T07:16:44.570 |

The The Innovative Form Builder – IvyForms plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 1.5.1 via the filterFiletypeAndExt function. This is due to insufficient file type validation due to the absence of a dangerous-extension denylist in the allowed-extensions sanitizer and deliberate override of WordPress's native MIME and extension defences via a registered wp_check_filetype_and_ext filter. This makes it possible for authenticated attackers, with custom-level access and above, to upload files that may be executable, which makes remote code execution possible. An authenticated attacker with the custom add_edit_forms capability must first configure a File Upload field with a dangerous extension (e.g., php) in the allowed-extensions list; once that form is published, any unauthenticated visitor can trigger the actual file upload via the publicly accessible /wp-json/ivyforms/v1/form/submission/ REST route.

### CVE-2026-1928

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T04:18:02.320 |

The Rank Math SEO – AI SEO Tools to Dominate SEO Rankings plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.0.276 via deserialization of untrusted input in the updateMeta REST API endpoint. This makes it possible forauthenticated attackers, with Contributor-level access and above, to inject a PHP Object. The additional presence of a POP chain allows attackers to achieve remote code execution by writing a webshell to the uploads directory.

### CVE-2026-58255

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269;CWE-862;CWE-915` |
| Published | 2026-10-27T23:17:05.990 |

Cronicle is a multi-server task scheduler and runner, with a web based front-end UI. Prior to 0.9.121, a non-administrator user or scoped API key with `create_events` and `run_events` privileges can inject top-level `uid` and `gid` fields through `/api/app/create_event` or `/api/app/update_event`. In `lib/api.js`, `requireValidEventData` uses `validateOptionalParams` as a partial allow-list that silently passes unknown keys, storing the injected fields verbatim. In `lib/job.js`, `launchJob` copies the whole event into the job, and a plugin `uid` overrides the event `uid` only when the plugin defines one. The default `shellplug` and `urlplug` plugins do not define a `uid`, so the event-controlled identity survives into child-process launch. On a root-daemon installation, this lets a low-privileged user run jobs as arbitrary users, including root, bypassing the otherwise administrator-only run-as-user control. This API-side event injection is distinct from the job-output `uid`/`gid` injection addressed by CVE-2026-39401. This issue is fixed in version 0.9.121.

### CVE-2026-118359

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:05.130 |

Memory corruption in V8 in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118358

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:05.017 |

Memory corruption in WebAudio in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118357

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:04.907 |

Use after free in FileSystem in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118356

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:04.750 |

Use after free in WTF in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118354

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:04.507 |

Improper input validation in Skia in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118353

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:04.380 |

Use after free in Paint in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118352

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:04.263 |

Memory corruption in Cache in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118351

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:04.157 |

Memory corruption in Skia in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118350

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:04.050 |

Use after free in Turbolev in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118349

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:03.943 |

Memory corruption in Payments in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118348

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:03.833 |

Improper input validation in Skia in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-118347

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:03.723 |

Use after free in FileSystem in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118346

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:03.613 |

Use after free in Compositing in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118345

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:03.503 |

Use after free in PDFium in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118344

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:03.393 |

Use after free in Layout in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-118343

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:03.283 |

Improper input validation in ReadingList in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118341

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:03.077 |

Use after free in Modularization in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118339

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:02.863 |

Use after free in Animation in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118338

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:02.753 |

Use after free in Animation in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Medium)

### CVE-2026-118336

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:01.907 |

Improper input validation in Headless in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118335

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:01.790 |

Improper input validation in Metrics in Google Chrome on on Mac prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118334

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:01.687 |

Use after free in ImageCapture in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118331

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:01.370 |

Improper input validation in FileAPI in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: Critical)

### CVE-2026-118330

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:17:01.267 |

Use after free in Browser in Google Chrome on on Windows prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:01.157 |

Improper input validation in ANGLE in Google Chrome on on Mac prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118328

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:01.053 |

Improper input validation in WebRTC in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118327

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:00.943 |

Memory corruption in Media in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118320

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:00.637 |

Memory corruption in V8 in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118317

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:17:00.303 |

Memory corruption in HTML in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118315

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:17:00.087 |

Improper input validation in SVG in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118314

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:16:59.970 |

Improper input validation in UI in Google Chrome on on Android prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118313

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:16:59.863 |

Use after free in Video in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118311

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-119` |
| Published | 2026-10-27T23:16:59.650 |

Memory corruption in Media in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118307

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-10-27T23:16:59.203 |

Use after free in Paint in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-118304

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-20` |
| Published | 2026-10-27T23:16:58.863 |

Improper input validation in SVG in Google Chrome prior to 156.0.8078.73 allowed a remote attacker to potentially execute arbitrary code inside the sandbox via a crafted HTML page. (Chromium security severity: High)

### CVE-2026-85898

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-27T21:19:34.117 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-83831

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-27T21:19:08.030 |

Double free in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-116676

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T18:17:35.220 |

Atlantis is a self-hosted golang application that listens for Terraform pull request events via webhooks. From version 0.4.0 until 0.47.1, Atlantis passes the pull-request-controlled workspace value from atlantis.yaml into Terraform command arguments that are joined with strings.Join(args, " ") and executed through sh -c. An authenticated contributor whose pull request is eligible for an Atlantis plan can include shell metacharacters in the workspace name, causing arbitrary commands to execute as the Atlantis service account without custom workflows, apply permission, or a malicious Terraform provider. External contributors can reach the flaw through fork pull requests only when --allow-fork-prs is enabled, while eligible same-repository branches do not require that option. The commands inherit the Atlantis process environment and can access cloud-provider, Terraform, and version-control credentials as well as files, state, and network resources available to the service. This issue is fixed in version 0.47.1.

### CVE-2026-108329

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-27T18:17:33.530 |

Tanium addressed an unauthorized code execution vulnerability in Threat Response.

### CVE-2026-108303

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-27T18:17:31.777 |

Tanium addressed an unauthorized code execution vulnerability in Certificate Manager.

### CVE-2026-116672

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-639;CWE-1188` |
| Published | 2026-10-27T17:16:59.140 |

Authlib is a Python library which builds OAuth and OpenID Connect servers. From 0.15 until 1.9.1, the documented ClientConfigurationEndpoint.authenticate_client and ClientConfigurationEndpoint.check_permission reference implementations look up a target client from request-controlled client_id data and check only whether that target is editable, without verifying that request.credential belongs to the target client. Deployments following both examples can allow a client holding any valid registration access token to read, modify, or delete another client's registration. Changing redirect_uris can enable authorization code or token interception, while deleting registrations can deny service to affected clients. This issue is fixed in version 1.9.1.

### CVE-2026-114596

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-27T17:16:58.690 |

In EPICS Base release 7.0.10 and prior, an improper validation of message length values during protocol parsing can trigger an integer overflow, resulting in an out-of-bounds memory write. Successful exploitation can cause process instability or denial of service.

### CVE-2026-92372

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-123` |
| Published | 2026-10-27T16:17:31.760 |

An out-of-bounds write vulnerability in the
screen-image decoder of TeamViewer Full Client for Linux and macOS prior to
version 15.83 allows a remote attacker to execute arbitrary code by supplying
crafted screen-image data during a remote-control session. The vulnerability
can also be exploited by persuading a user to open a specially crafted
TeamViewer session recording (.tvs). Missing destination bounds checking in the
decoder allows crafted screen-image data to cause an out-of-bounds write to the
image buffer. Exploitation requires user interaction.

### CVE-2026-111585

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-27T16:17:29.870 |

An integer overflow in the remote-control
screen processing component of TeamViewer clients (Full Client, Portable and Remote
Control App) prior to version 15.83 may allow a malicious remote host to cause
a denial of service or, depending on the platform, potentially execute
arbitrary code with the privileges of the viewer process. Exploitation requires
a user to establish a remote-control session to an attacker-controlled or
compromised host.

### CVE-2026-107672

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-77` |
| Published | 2026-10-27T16:17:29.020 |

A maliciously crafted .stack.json file can trigger a trusted Markdown injection vulnerability in Autodesk Fusion Post Processor Utility Extension. A malicious actor may exploit this vulnerability to execute arbitrary commands in the context of the current user.

### CVE-2026-116078

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-28T14:16:58.153 |

Allocation of Resources Without Limits or Throttling vulnerability in the HTTP/2 request body reader of mtrudel bandit allows an unauthenticated remote attacker to exhaust server memory via a request body sent as many 1-byte DATA frames.

do_read_data/5 in lib/bandit/http2/stream.ex keeps every DATA frame payload as its own list element until the read returns. The :length option of read_body/2 counts body bytes, not frames, so a body of 1-byte frames costs a list cell and a binary term per byte. Interleaving the frames across up to 500 concurrent streams per connection keeps each stream consuming its frames as they arrive; in the reporter's test, 100 streams held 25 to 40 MiB of stream process memory for 5 MB sent. Only routes whose Plug reads the request body are affected, which includes any route behind Plug.Parsers.

This issue affects bandit: from 0.3.1 before 1.14.1.

### CVE-2026-118477

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T12:17:40.227 |

The ei_git_repo_url parameter in the Git remote configuration endpoint of KaliFast is vulnerable to OS Command Injection. This OS Command Injection vulnerability allows an authenticated attacker (free registration available) to execute arbitrary commands on the KaliFast server with www-data privileges. Fixed in version 2026061802.

### CVE-2026-104384

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-28T05:16:59.700 |

Insufficiently Protected Credentials in tunnel gateway and provisioning interfaces in EagleCloud Aquila versions through 2.6.7.2 on on-premises platforms allows unauthenticated remote attackers to escalate privileges via authentication abuse to access the access keys, secret keys, and deployment secrets

### CVE-2026-118377

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-345` |
| Published | 2026-10-28T03:17:14.410 |

mews/pos through 2.0.0 contains an insufficient verification of data authenticity vulnerability that allows unauthenticated attackers to forge payment results by submitting unverified callbacks. GarantiPos, PayForPos and InterPos 3D Pay and 3D Host handlers skip check3DHash(), letting attackers post tampered status, amount or order ID fields to complete orders without paying.

### CVE-2014-125138

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T03:17:08.043 |

C97net qEngine CMS through 6.0.0, Kemana Directory through 1.5.6, and Cart Engine through 3.0.0 contain an unrestricted file upload vulnerability in administrative image fields. Editor-role users can upload PHP scripts via the page_image or cat_image parameters to the web-accessible /public/image directory and request them to execute code on the server.

### CVE-2026-116693

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-10-27T21:18:05.167 |

dd-trace is the Datadog APM client for Node.js. From 2.0.0 until 5.131.1 and 6.20.1, the default DD_TRACE_OBFUSCATION_QUERY_STRING_REGEXP can perform excessive backtracking on attacker-controlled URL query strings. The expression is applied synchronously while recording HTTP URL metadata, allowing a crafted request to consume excessive CPU, stall request processing, and make the instrumented application unavailable. This issue is fixed in versions 5.131.1 and 6.20.1.

### CVE-2026-112355

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-27T20:17:13.147 |

The MembershipWorks plugin for WordPress before 6.17 contains an information disclosure vulnerability that allows unauthenticated attackers to access member-only content through the WordPress REST API. Because the filter that strips protected content for non-members is only attached during normal front-end request handling and not during REST API requests, an unauthenticated attacker can retrieve the raw member-only content in a post or page’s rendered content, bypassing the plugin’s content protection.

### CVE-2026-112351

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T20:17:12.853 |

Sunhillo SureLine before 9.1.5 contains an OS command injection vulnerability in the networkDiag.cgi endpoint that allows an authenticated remote attacker with any web account to execute arbitrary commands as root by injecting shell metacharacters into the ipAddr or dnsAddr parameters. Attackers can bypass the incomplete character denylist from the prior CVE-2021-36380 fix using URL-encoded newline (%0a) or ampersand (%26) sequences that act as command separators after decoding in the ping, nslookup, or traceroute diagnostic modes, leading to full system compromise.

### CVE-2026-112350

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-27T20:17:12.693 |

Sunhillo SureLine before 9.1.5 contains a path traversal vulnerability in the radarUpdater.cgi endpoint that allows unauthenticated remote attackers to read arbitrary files with root privileges due to missing authentication checks and insufficient sanitization of the filename parameter. Attackers can use directory traversal sequences to access sensitive files such as /etc/shadow, the web user database, the root SSH private key, and the device's TLS private key, leading to full system compromise.

### CVE-2026-102814

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-27T18:17:30.157 |

An
authentication weakness exists in the TP-Link TDDP v2 service of TP-Link RE305
V3. TDDP v2 uses a fixed and derivable cryptographic key, which may allow an
unauthenticated attacker on the same local network to forge protocol packets
and access privileged TDDP operations, including functionality that can lead to
operating-system command execution when the TDDP service is running and
accessible.









Successful
exploitation may allow an unauthenticated attacker on the same local area
network to execute arbitrary system commands with root privileges.

### CVE-2026-114598

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-27T17:16:59.003 |

In EPICS Base release 7.0.10 and prior, an insufficient validation of element or length values in a network message can cause the application to read beyond the bounds of an allocated buffer. This may lead to denial of service and could expose adjacent memory contents.

### CVE-2026-114597

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-130` |
| Published | 2026-10-27T17:16:58.840 |

In EPICS Base release 7.0.10 and prior, an insufficient validation of element or length values in a network message can cause the application to read beyond the bounds of an allocated buffer. This may lead to denial of service and could expose adjacent memory contents.

### CVE-2026-93434

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-208;CWE-643` |
| Published | 2026-10-27T16:17:32.333 |

An XPath injection vulnerability in WatchGuard Fireware OS's SSH authentication process allows a remote, unauthenticated attacker with access to the management SSH interface to extract sensitive configuration data by submitting a specially crafted request.

### CVE-2026-111107

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248;CWE-476;CWE-1286` |
| Published | 2026-10-27T16:17:29.393 |

A NULL pointer dereference vulnerability in WatchGuard Fireware OS’s management interface allows a remote, unauthenticated attacker with network access to the management interface to crash the management service by sending a specially crafted login request. Repeated exploitation terminates all active administrator sessions and in-progress management operations and can prevent management of the device. Traffic processing is not affected.

### CVE-2026-117604

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-10-27T15:16:57.817 |

Grav from 1.7.53.3 before 1.7.53.6 contains an authorization bypass in Debugger::isDebuggerRequestAuthorized() that allows unauthenticated visitors to read /__clockwork/ profiler data via a loopback REMOTE_ADDR fallback. Behind a same-host reverse proxy, remote requests appear as loopback, letting attackers read stored records including administrator plaintext passwords and configuration credentials.

### CVE-2026-67073

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:L` |
| Weaknesses | `CWE-79;CWE-284;CWE-434;CWE-552` |
| Published | 2026-10-28T13:17:08.283 |

HCL BigFix AEX is affected by an Unrestricted File Upload and Improper Access Control vulnerability. This could allow an attacker to upload malicious or unauthorized files and directly access or download sensitive uploaded content, potentially leading to information disclosure, unauthorized access, or system compromise.

### CVE-2026-102790

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T12:17:39.513 |

Joomla Extension - icagenda.com -  Stored XSS via url-type event Custom Field in iCagenda 3.2.1 to 4.0.16

### CVE-2026-117607

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T03:17:12.283 |

Xerte Online Toolkits through 3.15.5 contains a remote code execution vulnerability that allows authenticated users with system permission to run PHP by importing a crafted language pack. Attackers can upload a ZIP via import_language.php containing a .inc file, then request it through the language parameter to execute code on the server.

### CVE-2015-20129

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-352` |
| Published | 2026-10-28T03:17:08.223 |

CrushFTP before 7.3.0 contains a cross-site request forgery vulnerability that allows attackers to perform administrative actions because CSRF protection is disabled by default. Attackers can lure an authenticated administrator to a malicious page that submits POST requests to commands like setUserItem, creating root-access users or changing server configuration.

### CVE-2013-20007

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T03:17:07.210 |

Linksys WAG200G through 1.01.06 contains an OS command injection vulnerability that allows authenticated attackers to execute commands by injecting backtick-delimited input into the timer_interval parameter. Attackers can send a crafted POST request to setup.cgi to start telnetd or download and run a backdoor, gaining full device control.

### CVE-2026-116682

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-59` |
| Published | 2026-10-27T18:17:36.003 |

FileBrowser Quantum is a free, self-hosted, web-based file manager. Prior to 1.5.2-stable and 2.0.1-beta, file read handling in backend/pkg/indexing/indexingFiles.go resolves symbolic links through GetRealPath without confirming that the resolved target remains inside the source root and the user's authorized scope. Download, preview, media, OnlyOffice, and public-share read flows that enable FollowSymlinks can therefore serve an out-of-scope target through a reachable in-scope symlink. An authenticated user with download access can read server-accessible files outside the assigned scope, and a holder of a public share link can do the same without an account when the shared directory exposes such a symlink. This issue is fixed in 1.5.2-stable and 2.0.1-beta.

### CVE-2026-90442

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-10-27T16:17:31.393 |

A stack-based buffer overflow vulnerability in the Fireware OS certd process allows an authenticated attacker with access to the Firebox management interface to crash the certificate management service and potentially execute arbitrary code by sending a specially crafted request.

### CVE-2026-93517

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-28T14:17:08.843 |

A heap buffer overflow in handling GLX
RenderLarge request where dataBytes exceeds cmdlen in X.org X server before 21.1.25 and XWayland before 24.1.14 that could be be triggered by an authenticated X client could cause crashes or code execution in X server context.

### CVE-2026-59185

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:N` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-10-28T14:17:05.070 |

identrail is a machine identity security platform for AWS, GitHub/OIDC, and Kubernetes. Prior to 1.0.2, the default-on `POST /v1/workspaces/:workspace_id/projects/:project_id/github/connect/complete` endpoint in `internal/api/router.go` accepts `installation_id` from the request body or `X-GitHub-Installation-ID` header without verifying the installation belongs to the caller's workspace. `CompleteGitHubConnection` in `internal/api/github_connect.go` rigorously binds `state` to the caller's tenant, workspace, and project, but checks only that the installation ID is positive before persisting it as the caller's connection. `ListInstallationRepositories` in `internal/connectors/github/repositories.go` invokes token creation through `internal/connectors/github/app.go` and `POST /app/installations/{installationId}/access_tokens`, using the application's JWT. An authenticated tenant who starts a legitimate connection can supply another customer's non-secret installation ID to read the victim organization's private repository inventory, content, and metadata or drive posture scans, provided identrail's GitHub App is installed there. The default-off V2 `CompleteGitHubConnector` path shares the installation-ownership gap and additionally matches pending `state` without rechecking caller scope. This issue is fixed in version 1.0.2.

### CVE-2026-115603

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T14:16:57.887 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in Advanced Ads GmbH Advanced Ads – Tracking advanced-ads-tracking allows Blind SQL Injection.This issue affects Advanced Ads – Tracking: from n/a before 4.0.0.

### CVE-2026-111850

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T13:17:04.303 |

Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') vulnerability in BuddyPress BuddyPress buddypress allows SQL Injection.This issue affects BuddyPress: from n/a through 14.5.2.

### CVE-2026-118378

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-28T03:17:14.570 |

Tabularis before 0.28.0 contains an SQL injection vulnerability in its SQLite driver that allows MCP clients to execute stacked statements by supplying a crafted table_name to the describe_table tool. Attackers, including AI agents steered by untrusted content, can close the quoted PRAGMA argument and append statements to read, modify, or drop SQLite data, bypassing read-only mode and write approval.

### CVE-2026-116675

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T17:16:59.617 |

TinyMCE is an open source rich text editor. From 7.9.3 until 7.9.4 and from 8.5.1 until 8.9.3, the media plugin creates elements crafted through data-mce-object in the active document before sanitization. Those elements can execute malicious scripts during processing, resulting in stored cross-site scripting for users with the media plugin enabled. This issue is fixed in versions 8.9.3 and 7.9.4.

### CVE-2026-107671

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-10-27T17:16:56.920 |

A vulnerability allowing an attacker with valid Administrator credentials to bypass multi-factor authentication by disabling it globally before completing MFA verification.

### CVE-2026-59179

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T14:17:04.907 |

OpenHop is a tool for creating interactive data-flow diagrams. Prior to 0.3.7, `@openhop/server` passes unauthenticated flow route parameters from `GET /api/flows/:id` and `DELETE /api/flows/:id` in `packages/server/src/routes.ts` to `FlowStore.filePath()` in `packages/server/src/store.ts` without an identifier allow-list. The router applies `decodeURIComponent` to the id, and `path.join()` then normalizes traversal outside the configured flow directory after appending the .yaml extension. An attacker can read accessible YAML files as YAML-parsed JSON or permanently delete accessible .yaml files outside that directory, exposing configuration or secrets and disrupting dependent services. In `packages/server/src/index.ts`, CORS `origin: true` permits any browser origin, enabling a malicious webpage to target a loopback-bound instance. Docker deployments default to `HOST=0.0.0.0` and permit direct unauthenticated network access. This issue is fixed in repository release 0.3.7.

### CVE-2026-112198

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-28T11:17:15.220 |

XML External Entity (XXE) injection vulnerability in the SAFT import feature of the NoviGest Desktop App. The application processes user-controlled XML files using a JAXB Unmarshaller without properly disabling external entity resolution. An attacker with access to this functionality could provide a manipulated XML file to read local files accessible to the application process. If the application runs with elevated privileges, sensitive system files could be exposed.

### CVE-2026-103779

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-28T11:17:13.977 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Authentication vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-106077

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-10-27T17:16:56.673 |

A vulnerability allowing a user with the Veeam Backup for Microsoft 365 Administrator role to read arbitrary files on the backup server with LocalSystem privileges.

### CVE-2026-118374

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-770` |
| Published | 2026-10-28T03:17:13.923 |

LibreSSL ocspcheck through 4.4.0 contains a memory exhaustion vulnerability that allows malicious OCSP responders to exhaust memory by sending unbounded HTTP responses. Attackers controlling the responder or intercepting plain HTTP AIA OCSP traffic can stream endless headers or body data to http_head_read() and http_body_read(), denying certificate status checks.

### CVE-2026-118370

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-28T03:17:13.293 |

libexpat through 2.9.0 contains a signed integer overflow vulnerability in storeAtts() in lib/xmlparse.c that allows attackers to trigger out-of-bounds writes via oversized attribute counts. Attackers can supply a multi-gigabyte document with a start tag carrying over 2^30 attributes to overflow attIndex and nPrefixes, crashing applications or corrupting heap memory.

### CVE-2026-117610

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-28T03:17:12.777 |

libexpat through 2.9.0 contains a NULL pointer dereference vulnerability in externalEntityInitProcessor2() in lib/xmlparse.c that mishandles the XML_TOK_NONE token from empty input. Attackers who control stream chunking can force an empty non-final first parse on an external entity subparser, causing a later parse to crash the application.

### CVE-2014-125136

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-530` |
| Published | 2026-10-28T03:17:07.707 |

C97net qEngine CMS through 6.0.0, Kemana Directory through 1.5.6, and Cart Engine through 3.0.0 contain an information disclosure vulnerability that exposes database backups in the web-accessible /admin/backup directory. Unauthenticated attackers can list the directory or guess date-based names like 'Full Backup YYYYMMDD.sql' to download dumps containing user records and administrator password hashes.

### CVE-2026-57191

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120;CWE-787` |
| Published | 2026-10-27T22:17:27.390 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, an unbounded `sscanf` in `res_pjsip_pubsub` when parsing the `MWI NOTIFY` `Message-Account` field may allow an unauthenticated attacker to send a carefully crafted packet that causes a stack buffer overflow and corrupts the underlying transport, permanently disabling all SIP functionality. An Asterisk restart is required to restore full operation. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-58205

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T23:17:05.840 |

GRR is a resource management and reservation application. Prior to version 4.5.0, `maj.php` reflects the `forcemaj` parameter without adequate escaping when installation files remain accessible. Removal of these files is not automatic. An attacker can craft a URL that executes arbitrary JavaScript in a victim's browser when the victim accesses it. This reflected cross-site scripting can enable phishing, redirection to malicious sites, cookie theft and session hijacking because the authentication cookie is not `HttpOnly`. This issue is fixed in version 4.5.0.

### CVE-2026-116688

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T20:17:14.037 |

CKEditor 5 is a modern JavaScript rich-text editor with an MVC architecture. From 45.0.0 until 47.7.4 and 48.5.1, the engine uses a vulnerable es-toolkit version whose prototype-pollution behavior can be reached while CKEditor processes incoming style attribute values. Crafted editor content can thereby cause unauthorized JavaScript execution in the browser. This issue is fixed in versions 47.7.4 and 48.5.1.

### CVE-2026-57202

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-267;CWE-1220` |
| Published | 2026-10-27T18:17:37.550 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, an authenticated Asterisk REST Interface (ARI) attacker with read-only privileges may use `setChannelVar` to execute write dialplan functions, including `FILE()` writes, even when `live_dangerously` in `asterisk.conf` is set to no. The Asterisk HTTP web server must be enabled and reachable, and the attacker must already have valid `read-only ARI credentials`. HTTP is disabled by default and binds only to 127.0.0.1 by default even when enabled. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-59176

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-28T14:17:04.593 |

Functype is a family of TypeScript functional programming libraries. Prior to 1.4.4, the `set_functype_version` MCP tool in `functype-mcp-server` accepts an unconstrained `version` string using only `z.string()` validation in `packages/mcp-server/src/index.ts` and interpolates it into `functype@<version>` for `pnpm add`. Package-alias syntaxes such as `file:`, `npm:`, URLs, or paths can cause an arbitrary local or remote package to be installed as functype. Immediately afterward, `initDocsData(true)` in `packages/mcp-server/src/lib/docs/data.ts` resolves `functype/cli` and dynamically imports the newly installed module, executing attacker-controlled JavaScript with the MCP server process's privileges. Any MCP client able to send a `tools/call` request invoking the tool can exploit the flaw; the tool is enabled by default without authentication in `stdio` mode. A connected AI assistant susceptible to indirect prompt injection can also be induced to invoke it from a malicious document or web page. In non-default `TRANSPORT_TYPE=httpStream` deployments, a network-accessible attacker does not require local access. Successful execution can read process secrets, modify files, or terminate the server. This issue is fixed in `version` 1.4.4.

### CVE-2026-59172

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-829` |
| Published | 2026-10-28T14:17:04.447 |

Joker is a small Clojure interpreter, linter and formatter written in Go. Prior to 1.8.2, `joker --lint <file>` walks upward from the linted file to locate a `.jokerd/` directory and executes matching `linter.*` files before linting. Those files contain executable Joker/Clojure code, so linting a file inside an untrusted repository can execute repository-supplied code with the linter user's privileges. Editor integrations and CI jobs that automatically lint checked-out source can trigger this behavior. The patch stops executing project-local linter customizations and loads executable customization only from the user's home directory. This issue is fixed in version 1.8.2.

### CVE-2026-88812

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-10-27T18:17:38.120 |

A double free in XKB SetGeometryin X.Org X Server before 21.1.25 and X Wayland before 24.1.14 could be used by attached clients to cause a crash or potentially code in the x server context.

### CVE-2026-108307

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T18:17:32.297 |

Tanium addressed a heap-based buffer overflow vulnerability in Index.

### CVE-2026-108306

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-27T18:17:32.163 |

Tanium addressed a local privilege escalation vulnerability in End-User Notifications.

### CVE-2026-108305

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-27T18:17:32.037 |

Tanium addressed a local privilege escalation vulnerability in End-User Notifications.

### CVE-2026-108304

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59;CWE-282` |
| Published | 2026-10-27T18:17:31.907 |

Tanium addressed a local privilege escalation vulnerability in End-User Notifications.

### CVE-2026-48379

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-27T17:17:00.870 |

Substance3D - Painter is affected by a Stack-based Buffer Overflow vulnerability that could result in arbitrary code execution in the context of the current user. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-113775

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-749` |
| Published | 2026-10-27T17:16:58.393 |

A maliciously crafted dynamic library, when loaded from an arbitrary path through the TextCommands.LoadDll command exposed by the Autodesk Fusion API, can trigger an Exposed Dangerous Function vulnerability in the Autodesk Fusion desktop application. A malicious actor may leverage this vulnerability to execute arbitrary code in the context of the current process.

### CVE-2026-92377

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-732` |
| Published | 2026-10-27T16:17:32.213 |

Improper access control in the Patch
Management update mechanism of TeamViewer Full Client and Host for Windows
prior to version 15.82 allows a local authenticated attacker with low
privileges to supply a signed executable through a forged IPC response and
cause it to load a malicious DLL from a user-writable temporary directory.
Successful exploitation results in arbitrary code execution with NT
AUTHORITY\SYSTEM privileges.

### CVE-2026-92376

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-10-27T16:17:32.103 |

Improper authentication in the
inter-process communication (IPC) mechanism of TeamViewer Remote Management
Monitoring for Windows prior to version 26.10.1 allows a local authenticated
attacker with low privileges to impersonate the IPC broker and cause the
Monitoring service to execute arbitrary code with NT AUTHORITY\SYSTEM
privileges, resulting in local privilege escalation.

### CVE-2026-92375

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-10-27T16:17:31.987 |

An improper access control vulnerability in
the IPC communication between TeamViewer Full Client or Host prior to version
15.83 and the Remote Management Monitoring component prior to version 26.10.1
allows a local authenticated attacker with low privileges to execute scripts as
SYSTEM/root.

### CVE-2026-92374

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-367` |
| Published | 2026-10-27T16:17:31.873 |

A time-of-check time-of-use (TOCTOU) race condition combined with improper symbolic link handling in the privileged helper of TeamViewer Full Client and Host prior to version 15.83 for macOS allows a local attacker with low privileges to bypass installer package verification and install a malicious package. Successful exploitation can lead to local privilege escalation to root.

### CVE-2026-57197

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-122;CWE-787` |
| Published | 2026-10-27T17:17:01.793 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, an unbounded `memcpy` of `OGG/Speex` packet data in `format_ogg_speex` can cause a heap buffer overflow and crash Asterisk when reading a file containing corrupted Speex audio. The attacker must create the file and make it available to Asterisk either through sufficiently elevated privileges or by convincing an Asterisk administrator to make it available. Asterisk must also be configured to play that file. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-86377

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-28T11:17:26.857 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Out-of-bounds Write vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Denial of service.

### CVE-2026-118040

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-295;CWE-347` |
| Published | 2026-10-28T13:17:06.877 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, improper verification of cryptographic signatures and improper certificate validation in RadPdfProcessing digital signature validation allow an unauthenticated attacker to cause signature validation to report forged content as unmodified and its signing certificate as valid via a crafted signed PDF document.

### CVE-2026-118039

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-611` |
| Published | 2026-10-28T13:17:06.753 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, an XML external entity reference vulnerability in SVG image processing allows an unauthenticated attacker to read local files on the server via a crafted SVG image with a nested embedded SVG, when the image is processed or exported to PDF.

### CVE-2026-118037

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-606;CWE-674;CWE-835;CWE-1333` |
| Published | 2026-10-28T13:17:06.490 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, uncontrolled recursion, infinite loop, unchecked loop condition and inefficient regular expression vulnerabilities in RadSpreadProcessing and RadSpreadStreamProcessing allow an unauthenticated attacker to terminate or hang the host process via a crafted XLSX or XLS workbook or formula.

### CVE-2026-118036

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-674;CWE-770;CWE-789;CWE-835` |
| Published | 2026-10-28T13:17:06.363 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, uncontrolled recursion, infinite loop, inefficient algorithmic complexity and resource allocation vulnerabilities in RadPdfProcessing and AI document summarization and question answering allow an unauthenticated attacker to terminate or hang the host process via a crafted PDF document or document text submitted for summarization or question answering.

### CVE-2026-118035

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-407;CWE-674;CWE-835` |
| Published | 2026-10-28T13:17:06.220 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, uncontrolled recursion, inefficient algorithmic complexity and infinite loop vulnerabilities in RadWordsProcessing allow an unauthenticated attacker to terminate or hang the host process via a crafted DOCX, DOC, RTF or HTML document.

### CVE-2026-116393

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T13:17:05.953 |

Missing Authorization vulnerability in iHomefinder, Inc. Optima Express optima-express allows Exploiting Incorrectly Configured Access Control Security Levels.This issue affects Optima Express: from n/a through 9.0.0.

### CVE-2026-115591

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-201` |
| Published | 2026-10-28T13:17:04.447 |

Insertion of Sensitive Information Into Sent Data vulnerability in Supsystic Contact Form by Supsystic contact-form-by-supsystic allows Retrieve Embedded Sensitive Data.This issue affects Contact Form by Supsystic: from n/a through 1.10.5.

### CVE-2026-15323

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T06:16:36.043 |

The Product Designer for WooCommerce WordPress | Lumise plugin for WordPress is vulnerable to Directory Traversal in all versions up to, and including, 2.1.2 via the process_checkout function. This makes it possible for unauthenticated attackers to read the contents of arbitrary files on the server, which can contain sensitive information. The lumise_security nonce required to reach the vulnerable /?lumise=cart endpoint is freely obtainable by any unauthenticated visitor via the /?lumise=ajax action=init handler, making this exploitable with no prior access or credentials.

### CVE-2026-116613

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T04:17:57.390 |

The Animated Text Block plugin for WordPress is vulnerable to Sensitive Information Exposure in versions up to, and including, 1.2.6 via the 'animated-text' shortcode. This is due to the atb_shortcode_handler() function fetching an arbitrary post by attacker-supplied ID and, in the 'publish' branch, calling displayContent() with no capability check and no validation that the post's post_type is the plugin's own CPT or is otherwise viewable (is_post_type_viewable()). This makes it possible for authenticated attackers, with Contributor-level access and above, to read the rendered block content of any published post, including posts of non-public custom post types (public=false, show_in_rest=false) that WordPress would otherwise hide from direct URLs and the REST API.

### CVE-2026-111255

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-10-28T04:17:56.390 |

The affiliate-toolkit – Multi-Network Affiliate & Amazon Product Display plugin for WordPress is vulnerable to Arbitrary File Upload in all versions up to, and including, 3.9.2 via the upload_image function. This is due to insufficient file type validation in upload_image due to a weak Content-Type prefix check and extension derivation from the attacker-controlled URL path, with no dangerous-extension stripping. This makes it possible for authenticated attackers, with contributor-level access and above, to upload files that may be executable, which makes remote code execution possible. Exploitation requires the "import product image" option to be enabled in the plugin settings, as this activates the image download pipeline triggered on product post save.

### CVE-2026-110747

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-28T01:16:55.017 |

ProtobufParser._readStringKey() reads the length prefix of a protobuf map entry's string key into an attacker-controlled int and then checks (_inputPtr + len) <= _inputEnd using signed arithmetic. For values near Integer.MAX_VALUE the addition overflows to a negative value and the check passes even when the input contains no key data. The parser then calls _finishShortText(len), which expands the text buffer to the declared length via TextBuffer.expandCurrentSegment and Arrays.copyOf, throwing OutOfMemoryError: Requested array size exceeds VM limit.



An 8-byte malformed message containing a map entry with a declared key length of 0x7FFFFFFF is sufficient. Configured StreamReadConstraints, including maxStringLength, maxNameLength, maxDocumentLength and maxNestingDepth, do not prevent the failure. Applications running with -XX:+ExitOnOutOfMemoryError terminate the JVM.



This is the same integer-overflow pattern addressed for other call sites in the remediation associated with CVE-2026-104016 and CVE-2026-104017; the map-key call site was corrected on the 3.x branches only, leaving the corresponding 2.x branches unguarded. Release lines 2.18, 2.19 and 2.20 do not contain _readStringKey() and are not affected by this vector. No privileges or user interaction beyond the ability to submit data for parsing are required. The 3.0 release line and 3.1.0-3.1.5 / 3.2.0-3.2.1 do not contain _readStringKey() and are therefore not affected; the method first appears in 3.1.6 and 3.2.2, mirroring its introduction at 2.21.6 on the 2.x side.

### CVE-2026-104895

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-789` |
| Published | 2026-10-28T00:17:11.357 |

The asynchronous Smile parser (NonBlockingByteArrayParser) uses a raw-binary length prefix taken from untrusted input to allocate a byte[] before the body is read, with no upper bound and no overflow check. On the raw-binary marker 0xFD, _decodeVInt() computes (value << 6) + (i & 0x3F) without the (value >>> 25) != 0 overflow guard present in the blocking SmileParser._readUnsignedVInt, and _startRawBinary then allocates the declared length immediately.



A Smile feed of roughly ten bytes can therefore force an eager allocation of approximately 2 GB, producing an OutOfMemoryError on reactive or asynchronous Smile endpoints. A VInt crafted to overflow int yields a negative length and a NegativeArraySizeException, a RuntimeException that is not a JacksonException and so escapes the parser contract. Either outcome crashes the request or processing thread.



This is the same class of issue as CVE-2020-28491 in the CBOR parser of this library, which was fixed with a LONGEST_NON_CHUNKED_BINARY guard; the asynchronous Smile parser never received the equivalent guard. No privileges or user interaction beyond the ability to submit data for parsing are required.

### CVE-2026-104016

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-28T00:17:10.530 |

ProtobufParser parses length-prefixed protobuf string and bytes fields by checking (_inputPtr + len) <= _inputEnd and then, on the fast path, calling _finishShortText(len). Both use 32-bit signed integer arithmetic. When an attacker supplies a varint decoding to a length near Integer.MAX_VALUE, _inputPtr + len overflows to a negative value, the bounds check passes, and _finishShortText(len) reaches TextBuffer.expandCurrentSegment(len), which performs Arrays.copyOf with no cap and throws OutOfMemoryError: Requested array size exceeds VM limit.



The JVM refuses arrays larger than Integer.MAX_VALUE - 8 before consulting available heap, so -Xmx tuning does not mitigate the issue. StreamReadConstraints.maxStringLength and maxDocumentLength do not gate this path: a 33-byte payload is far below any document-length cap and the string-length check does not fire before the allocation. This was confirmed empirically against shipping artifacts with maxStringLength, maxDocumentLength and maxNestingDepth all configured.



A February 2026 hardening commit added the equivalent overflow guard to the packed-array-length and message-length paths but left the string-length call sites unguarded. No privileges or user interaction beyond the ability to submit data for parsing are required.

### CVE-2026-59158

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-27T23:17:06.570 |

Nuxt Ollama integrates the official Ollama JavaScript library into Nuxt applications. Prior to 1.3.1, `src/module.ts` unconditionally merges all module options, including a configured cloud `api_key`, into `runtimeConfig.public.ollama`. Nuxt serializes this public configuration into the server-rendered HTML `window.__NUXT__` payload, exposing the API key in plaintext to any unauthenticated client that fetches a page. `src/runtime/composables/useOllama.ts` also reads the public key and sends it as an `Authorization` `Bearer` credential in browser-side Ollama requests. Following the documented cloud configuration is sufficient; the visible application template need not make an Ollama request for the secret to leak. A stolen key permits unauthorized cloud API requests at the operator's expense, quota or rate-limit exhaustion, and access to stored models or conversations if the key grants those permissions. This issue is fixed in version 1.3.1.

### CVE-2026-62765

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-843` |
| Published | 2026-10-27T22:17:29.267 |

Access of resource using incompatible type ('type confusion') in Microsoft Edge (Chromium-based) allows an unauthorized attacker to execute code over a network.

### CVE-2026-57186

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-839` |
| Published | 2026-10-27T22:17:26.990 |

Asterisk is an open source private branch exchange and telephony toolkit. From 21.0.0-pre1 until Asterisk 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 22.8-cert3, the `chan_ooh323` `Q.931 party-number parser` lacks the `CVE-2022-37325` fix because that fix was never forward-ported from Asterisk 20 to later versions. Malformed Q.931 elements in an `OOH323 request` can therefore crash Asterisk. This issue affects Asterisk versions greater than 20. The `chan_ooh323` addon channel driver must be explicitly compiled and installed, which is not the default, and its port must be publicly reachable. This issue is fixed in Asterisk 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 22.8-cert3.

### CVE-2026-57200

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22;CWE-863` |
| Published | 2026-10-27T21:18:06.843 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 22.8-cert3, an authenticated attacker with read-only permissions for the `Asterisk REST Interface (ARI)` may, under certain conditions, execute write operations through `REST-over-WebSocket`. The authorization bypass permits `arbitrary module path` loading and conditional remote code execution. The Asterisk HTTP web server must be enabled and reachable, and the attacker must already have valid `read-only ARI credentials`. HTTP is disabled by default and binds only to 127.0.0.1 by default even when enabled. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 22.8-cert3.

### CVE-2026-57195

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-10-27T21:18:06.633 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, a NULL pointer dereference in the `Asterisk Manager Interface (AMI)` may allow an unauthenticated attacker to crash Asterisk when `Digest Authentication` is used via `HTTP`. The Asterisk `HTTP` web server, AMI, and AMI access via `HTTP` must all be enabled; each is disabled by default. The attacker must be able to connect to the `HTTP` server, which binds only to `127.0.0.1` by default even when enabled. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-116690

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-27T20:17:14.340 |

MLflow is an open source AI engineering platform for agents, large language models, and machine learning models. From 3.10.0 until 3.17.0, the prompt branch in _create_model_version() accepts schemeless relative sources because path validation runs only when a source has a URL scheme, and mlflow.prompt.is_prompt is interpreted by tag presence rather than a true value. A remote caller can store a server-local path as the model version artifact location and use /api/2.0/mlflow/model-versions/get-artifact to read files accessible to the MLflow server process. Default unauthenticated servers require no privileges, while basic-auth deployments are exposed to authenticated users who can create registered models. This issue is fixed in version 3.17.0.

### CVE-2026-87086

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-690` |
| Published | 2026-10-27T18:17:38.000 |

Tanium addressed a denial of service vulnerability in Provision.

### CVE-2026-116662

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-409` |
| Published | 2026-10-27T18:17:35.100 |

Tanium addressed a compression bomb vulnerability in Enforce.

### CVE-2026-116656

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-27T18:17:34.487 |

Tanium addressed an uncontrolled resource consumption vulnerability in Enforce.

### CVE-2026-77167

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400` |
| Published | 2026-10-27T17:17:02.673 |

Abusing the federated share endpoint, an attacker can write arbitrary rows into the oc_share_external database table. These rows persist indefinitely — there is no automatic cleanup mechanism. Three distinct denial-of-service conditions follow from this write primitive, all triggered from the same unauthenticated source and all self-renewing on a 24-hour cycle for as long as the injected rows remain in the database.

### CVE-2026-57201

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-27T17:17:02.117 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, a stack buffer overflow in the H.323 `ooTrace()` trace-logging function can occur when unbounded `vsprintf` writes into a fixed `2048-byte buffer`. A remote attacker may send a carefully crafted packet that causes the Asterisk process to crash. The `chan_ooh323` addon channel driver must be explicitly compiled and installed, which is not the default, and its port must be publicly reachable. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-109090

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T17:16:57.930 |

A malicious X server could cause a heap overflow by injecting a large DEVICE_ENABLE reply when processed by libXi before 1.8.4.

### CVE-2026-109089

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-10-27T17:16:57.810 |

A buffer overflow when handling DEVICE_RESOLUTION in libXi before 1.8.4 could overflow a heap, triggered by a malicious X server.

### CVE-2026-104189

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-306;CWE-863` |
| Published | 2026-10-27T16:17:28.640 |

The 3D Viewer for Nextcloud is a comprehensive 3D model viewer application for Nextcloud that supports multiple 3D file formats. In versions 1.7.9 through 3.3.1, the app's public file endpoint performed no share authorization. Anyone who knows a share token could read the shared file's contents even when the link share was protected by a password. `PublicFileController` extended `OCP\AppFramework\Controller` and marked its routes `#[PublicPage]`. Nextcloud only enforces share passwords through `PublicShareMiddleware`, which returns early for any controller that is not an `OCP\AppFramework\PublicShareController` instance — so no password, expiry, or share-type check ran for these routes. `ShareFileService::loadLinkShare()` compounded this by treating any token that `getShareByToken()` matched as authorised. A share token is the part of the URL that people paste into chats, emails, and tickets. Password protection exists precisely for the case where holding the token should not by itself grant access, and that guarantee did not hold. Requests to `GET /ocs/v2.php/apps/threedviewer/public/file/{token}/{fileId}` returned `200` with the full file body for password-protected shares, with no password and no session. Nextcloud's own share page correctly redirected such requests to the password prompt. Scope is limited to files in the formats this app handles (STL, GLB/glTF, OBJ, STEP, IFC, and the other supported 3D types). Non-3D files in the same share are unaffected. Expired shares returned `500` rather than leaking contents. This issue is fixed in 3.3.2. `PublicFileController` now extends `PublicShareController` and implements `isValidToken()`, `isPasswordProtected()`, and `getPasswordHash()`, delegating password and token validation to the framework and gaining brute-force throttling. `ShareFileService::findValidLinkShare()` additionally rejects share types other than link and email, rejects expired shares, and treats a `ShareNotFound` from the share manager as "no share" instead of letting it surface as a 500. As a workaround, disable the 3D Viewer app (`occ app:disable threedviewer`), or avoid relying on passwords to protect link shares that contain 3D model files, until you can upgrade.

### CVE-2026-87103

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-28T11:17:27.897 |

Sensitive information disclosure and manipulation due to improper token validation. The following products are affected: Acronis Cyber Protect 17 (Linux, Windows) before build 42587.

### CVE-2026-87102

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.0/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-347` |
| Published | 2026-10-28T11:17:27.770 |

Sensitive information disclosure and manipulation due to improper token validation. The following products are affected: Acronis Cyber Protect 17 (Linux, Windows) before build 42587.

### CVE-2026-6064

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-10-28T11:17:26.707 |

Link following vulnerability in Data Shredder components in Norton Antivirus, Avast Antivirus, and AVG Internet Security prior to 26.5.10933 on Windows allows a local, low-privileged attacker to escalate privileges to SYSTEM. During a privileged shred operation, enabling arbitrary file/folder deletion that is leveraged to gain NT AUTHORITY\SYSTEM privelages.

### CVE-2026-115413

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-10-27T19:17:10.593 |

Missing token audience validation in the OAuth authentication mode of AWS API MCP Server before version 1.6.0 might allow local users to run AWS operations with the server's configured AWS credentials via an access token issued to another application by the same identity provider.



To remediate this issue, users should upgrade to version 1.6.0 and configure the expected token audience or client ID for the server.

### CVE-2026-105477

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-10-27T17:16:55.957 |

A vulnerability in Veeam Agent for Linux allows for local privilege escalation. Only installations that are managed by a Veeam Backup & Replication instance are affected.

### CVE-2026-104349

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-427` |
| Published | 2026-10-27T17:16:55.323 |

Creative Cloud Desktop is affected by an Uncontrolled Search Path Element vulnerability that could result in arbitrary code execution in the context of the current user. A low-privileged attacker could exploit this vulnerability to execute arbitrary code. Exploitation of this issue requires user interaction in that a victim must open a malicious file.

### CVE-2026-111584

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-27T16:17:29.757 |

A race condition in the installation
process of TeamViewer Remote Management - Patch Management for Windows prior to
version 26.9.1 allows a local authenticated attacker with low privileges to
execute arbitrary code with elevated privileges by replacing the service
executable in an insufficiently protected temporary directory during Patch
Management activation.

### CVE-2026-111583

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-27T16:17:29.643 |

Improper access control in the installer
staging directory used by TeamViewer Full Client and Host prior to version
15.82 for Windows during installation of Advanced Asset Management allows a
local authenticated user with low privileges to execute arbitrary commands as
SYSTEM. An attacker can place a crafted installer options file that is
processed by the Advanced Asset Management installer during service activation.

### CVE-2026-111582

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-27T16:17:29.513 |

A DLL loading vulnerability in the
TeamViewer Remote Management Monitoring installer for Windows prior to version 26.10.1
allows a local authenticated attacker with low privileges to execute arbitrary
code with elevated privileges. Exploitation requires user interaction.

### CVE-2026-116390

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T14:16:58.507 |

Deserialization of Untrusted Data vulnerability in stepasyuk Filter Everything&nbsp;— WordPress &amp; WooCommerce Filters filter-everything allows Object Injection.This issue affects Filter Everything&nbsp;— WordPress &amp; WooCommerce Filters: from n/a through 1.9.7.

### CVE-2026-115590

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T14:16:57.760 |

Deserialization of Untrusted Data vulnerability in weDevs Dokan dokan-lite allows Object Injection.This issue affects Dokan: from n/a through 5.3.1.

### CVE-2026-116392

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-10-28T13:17:05.820 |

Deserialization of Untrusted Data vulnerability in PickPlugins Accordion accordions allows Object Injection.This issue affects Accordion: from n/a through 2.3.25.

### CVE-2026-110541

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T11:17:14.937 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to command execution.

### CVE-2026-86394

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T10:17:10.990 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-86393

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-28T10:17:10.860 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Privilege Management vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Elevation of privileges.

### CVE-2026-86389

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-28T10:17:10.150 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Integer Overflow or Wraparound vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Code execution.

### CVE-2026-86380

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-10-28T10:17:09.163 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Integer Overflow or Wraparound vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Protection mechanism bypass.

### CVE-2026-86379

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T10:17:09.003 |

Dell PowerProtect Data Domain Management Center, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-86399

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T09:17:07.913 |

Dell PowerProtect Data Domain, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-86395

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-10-28T09:17:07.400 |

Dell PowerProtect Data Domain Virtual Edition, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain an Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') vulnerability. A high privileged attacker with remote access could potentially exploit this vulnerability, leading to Command execution.

### CVE-2026-111111

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T07:16:46.680 |

The Prime Slider – Hero Slider, Carousel, WooCommerce & Post Slider Elementor Addons plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'comment' parameter in all versions up to, and including, 4.7.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is possible because core wp_filter_kses leaves the submitted markup inert, but the plugin's subsequent regex fallback consumes closing quotes of allowed attribute values containing 'bdt-', promoting previously inert bytes — such as event handlers like onfocus — into real HTML attributes that are then written to the database and rendered without further sanitization.

### CVE-2026-110662

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T07:16:46.357 |

The MxChat – AI Chatbot & Content Generation for WordPress plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'feedback' parameter in all versions up to, and including, 3.2.25 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The stored payload is written by any unauthenticated visitor via a single POST to admin-ajax.php and detonates automatically when any administrator next loads the Transcripts page.

### CVE-2026-109381

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-10-28T07:16:44.423 |

The Mage Eventpress plugin for WordPress is vulnerable to privilege escalation in versions up to, and including, 5.7.8 This is due to the mep_grant_shop_manager_access() function hooking user_has_cap and unconditionally granting manage_options whenever an attacker-controllable request marker matches — most notably $_GET['page'] starting with 'mep_' or 'mpwem_', which is never validated against an actually registered EventPress screen. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to elevate their privileges to Administrator by appending ?page=mep_x to core admin URLs (options-general.

### CVE-2026-97019

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T03:17:16.317 |

The AMP for WP – Accelerated Mobile Pages plugin for WordPress is vulnerable to Stored Cross-Site Scripting via 'headline-*' Shortcode Attribute in all versions up to, and including, 1.1.17 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. A Subscriber-level user can store a malicious shortcode in their biographical info field; because WordPress core's wp_filter_kses() only strips HTML tags and not shortcode syntax, and because AMP content sanitizers run before do_shortcode() processes the archive description, the synthesized markup is never post-sanitized.

### CVE-2026-111314

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T03:17:09.817 |

The affiliate-toolkit – Multi-Network Affiliate & Amazon Product Display plugin for WordPress is vulnerable to Stored Cross-Site Scripting via the 'atkp_product_producturl' parameter in all versions up to, and including, 3.9.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation by unauthenticated attackers requires that the plugin's AJAX loading / AJAX handler option is enabled (atkp_options::get_ajax_loading_enabled() || get_ajax_handler_enabled()) and the attacker knows a product id to render. On a default installation, where that is not configured, the vulnerability requires attackers with contributor-level access and above.

### CVE-2026-109999

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T03:17:09.630 |

The AI Marketing Expert — AI Email Marketing, AI Content Generator, SEO Analyzer, AI Workflow Automation, Social Media & Ai Chatbot plugin for WordPress is vulnerable to Stored DOM-Based Cross-Site Scripting via the 'name' parameter in all versions up to, and including, 1.2.8 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. Exploitation requires only that the chatbot module is active with at least one configured bot; the attacker stores the payload via three unauthenticated REST calls, and the JavaScript widget auto-poll then delivers it to any administrator who opens wp-admin/index.php.

### CVE-2026-58257

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-27T23:17:06.280 |

GRR is a resource management and reservation application. Prior to the advisory-reported fixed version 4.5.0, the database restoration feature fails to enforce or validate file paths. A user with administrator privileges can manipulate the input to read or delete arbitrary files on the server, causing sensitive file disclosure and denial of service through file deletion. The impact is amplified when the server runs with elevated privileges. The advisory reports this issue as fixed in version 4.5.0.

### CVE-2026-93862

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-125;CWE-129;CWE-787;CWE-823` |
| Published | 2026-10-27T16:17:32.583 |

An out-of-bounds read vulnerability in the FireCluster Sync processing allows an attacker positioned on the cluster interconnect, such as a compromised cluster peer or an on-path network attacker, to repeatedly crash the firewall's cluster synchronization process by sending specially crafted network traffic, resulting in a sustained denial of service.

### CVE-2026-90464

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59;CWE-73;CWE-732` |
| Published | 2026-10-27T16:17:31.517 |

An external control of file path vulnerability in a WatchGuard Fireware OS firewall diagnostic command allows a remote, authenticated attacker with at least read-only (Device Monitor) privileges and access to the management CLI to create, truncate, or overwrite arbitrary files and modify kernel parameters with root privileges by submitting a specially crafted command. Written content is limited to numeric values.

### CVE-2026-59164

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T14:17:04.293 |

NORA is a self-hosted artifact registry and pull-through cache. Prior to 0.9.5, `nora-registry` authenticates the token-management UI but fails to require administrator authorization. `auth_middleware()` protects `/ui/tokens` and `/api/ui/tokens`, but state-changing requests are checked only with `role.can_write()`, not `role.can_admin()`. `tokens_page()` and `tokens_list()` call `store.list_all_tokens()`, exposing IDs and metadata across all users, while `tokens_revoke()` calls `store.revoke_token` using the supplied token ID without an ownership or admin check. A read bearer token can enumerate other users' token existence, owner, role, description, expiry and last-use metadata. A write bearer token or write-capable OIDC identity can additionally revoke arbitrary admin and service tokens, disrupting the registry and forcing credential recovery. Read-only identities cannot POST a revocation. This issue is fixed in version 0.9.5.

### CVE-2026-52729

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T14:17:04.137 |

Xibo is an open source digital signage platform with a web content management system and Windows display player software. Prior to 4.4.3, missing access-control checks on `PUT/DELETE /action/{id}` allow an authenticated user to modify or delete actions on any Layout. Exploitation requires the privilege to allow edits, including deletion, to all created Layouts, which is granted to non-administrators as standard. This issue concerns `Layout actions` rather than the separately reported DataSet export vulnerability. This issue is fixed in version 4.4.3.

### CVE-2026-118038

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-10-28T13:17:06.627 |

In Progress® Telerik® Document Processing Libraries prior to version 2026.3.1027, a path traversal vulnerability in the Convert and Merge AI agent tools allows an authenticated attacker with low privileges who can supply tool arguments to read files outside the configured output directory, and to overwrite such files where they are writable, via relative file paths that resolve against the process current working directory.

### CVE-2026-115612

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T13:17:05.267 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in iova.mihai SliceWP slicewp allows Stored XSS.This issue affects SliceWP: from n/a through 1.2.13.

### CVE-2026-115609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T13:17:05.130 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Stiofan GetPaid invoicing allows Stored XSS.This issue affects GetPaid: from n/a through 2.8.62.

### CVE-2026-115606

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T13:17:04.857 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Crowd Favorite DXP ToolKit dxp-toolkit allows Stored XSS.This issue affects DXP ToolKit: from n/a through 2.0.1.

### CVE-2026-115596

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T13:17:04.720 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in impleCode eCommerce Product Catalog ecommerce-product-catalog allows Reflected XSS.This issue affects eCommerce Product Catalog: from n/a through 3.6.4.

### CVE-2026-115593

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-28T13:17:04.583 |

Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') vulnerability in Unlimited Elements Unlimited Elements For Elementor (Free Widgets, Addons, Templates) unlimited-elements-for-elementor allows Reflected XSS.This issue affects Unlimited Elements For Elementor (Free Widgets, Addons, Templates): from n/a through 2.0.24.

### CVE-2026-110540

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L` |
| Weaknesses | `CWE-862` |
| Published | 2026-10-28T11:17:14.803 |

Dell PowerProtect Data Domain Management Center, Feature Release versions 7.7.1.0 through 8.8, LTS2024 release versions 7.13.1.0 through 7.13.1.80, LTS2025 release versions 8.3.1.0 through 8.3.1.40, LTS2026 release versions 8.6.1.0 through 8.6.1.20, contain a Missing Authorization vulnerability. A low privileged attacker with remote access could potentially exploit this vulnerability, leading to Unauthorized operation.

### CVE-2025-30414

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.0/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-1390` |
| Published | 2026-10-28T11:17:12.427 |

Local privilege escalation due to improper authentication. The following products are affected: Acronis Cyber Protect Cloud Agent (Windows) before build 42569, Acronis Cyber Protect 17 (Windows) before build 42587.

### CVE-2026-63286

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-326` |
| Published | 2026-10-28T07:16:48.550 |

Database backups are vulnerable to offline attacks. Backups created using a version prior to the patched version are still vulnerable. AXIS Camera Station Pro automatically creates one more such backup for recovery purpose when the update is applied. Delete all these backups and change the credentials stored in AXIS Camera Station Pro.

### CVE-2026-117609

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-10-28T03:17:12.607 |

rtl_433 through 25.12 contains a stack-based buffer overflow vulnerability in proflame2_mc() that allows nearby attackers to write past a 7-byte stack buffer by sending more than seven valid Manchester-coded words. Attackers can transmit a crafted OOK radio signal or supply a crafted signal file to crash rtl_433 and corrupt stack memory, enabling control-flow hijacking on builds without stack canaries.

### CVE-2014-125137

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-98` |
| Published | 2026-10-28T03:17:07.877 |

C97net qEngine CMS through 6.0.0, Kemana Directory through 1.5.6, and Cart Engine through 3.0.0 contain a local file inclusion vulnerability in the run parameter of admin/task.php. Authenticated administrators can supply directory traversal sequences in the run parameter to include and disclose local files readable by the web server.

### CVE-2026-116683

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-10-27T19:17:11.047 |

CTFer.io's CTFd Terraform Provider manages CTFd resources as code. From 0.1.5 until 2.8.2, ctfd_team.password is stored as a non-sensitive value in Terraform state. A local or remote user with access to that state can read the team password without an additional decryption step. This issue is fixed in 2.8.2.

### CVE-2026-57188

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-10-27T18:17:37.367 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, an authenticated attacker may cause a stack buffer overflow in `res_xmpp` `XMPP namespace prefix` handling using carefully crafted packets. The `res_xmpp` module must be loaded, an XMPP connection must be configured in `xmpp.conf`, and the attacker must have an XMPP account on the same or a federated server. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.

### CVE-2026-116649

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-1236` |
| Published | 2026-10-27T18:17:34.360 |

Tanium addressed an improper output sanitization vulnerability in Enforce.

### CVE-2026-116647

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-1236` |
| Published | 2026-10-27T18:17:34.233 |

Tanium addressed an improper output sanitization vulnerability in Comply.

### CVE-2026-102638

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T17:16:55.210 |

A maliciously crafted HTML payload in the description of an electronic library (.lbr) file, when displayed in the Library Manager after the library is imported, can trigger a Stored Cross-site Scripting (XSS) vulnerability in the Autodesk Fusion desktop application. A malicious actor may leverage this vulnerability to read local files or execute arbitrary code in the context of the current process.

### CVE-2026-102637

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T17:16:55.100 |

A maliciously crafted HTML payload in the documentName parameter of a Fusion protocol URL, when the protocol URL is invoked by a user, can trigger a Reflected Cross-site Scripting (XSS) vulnerability in the Autodesk Fusion desktop application. A malicious actor may leverage this vulnerability to read local files or execute arbitrary code in the context of the current process.

### CVE-2026-102636

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-10-27T17:16:54.957 |

A maliciously crafted HTML payload in a design name, when displayed after another user opens the manipulated design, can trigger a Stored Cross-site Scripting (XSS) vulnerability in the Autodesk Fusion desktop application. A malicious actor may leverage this vulnerability to read local files or execute arbitrary code in the context of the current process.

### CVE-2026-93864

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22;CWE-59;CWE-73;CWE-377` |
| Published | 2026-10-27T16:17:32.710 |

A link following vulnerability in WatchGuard Fireware OS’s firewall daemon allows a local attacker with code execution as a low-privileged system process to overwrite arbitrary files with root privileges, and to tamper with firewall IP set data, by planting a crafted file system object and triggering a list update. Written content is partially constrained.

### CVE-2026-103593

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121;CWE-787` |
| Published | 2026-10-27T16:17:28.353 |

A stack-based buffer overflow vulnerability in the Fireware OS logging service allows a network-adjacent attacker who can impersonate or intercept traffic to the configured log server to execute arbitrary code with root privileges by presenting a specially crafted certificate.

### CVE-2026-118485

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-24` |
| Published | 2026-10-28T12:17:40.370 |

Axel Download Accelerator 2.17.14 and earlier performs URL percent-decoding (http_decode()) on the output filename after the URL has been parsed and the filename component extracted. This allows an attacker to embed %2e%2e%2f (URL-encoded ../) sequences in the URL path. These sequences survive the URL parser intact (they contain no literal / characters) but are decoded into directory traversal sequences before the output file is opened for writing. As a result, a crafted URL can cause axel to write downloaded content to arbitrary filesystem paths relative to the current working directory.

### CVE-2013-20008

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-620` |
| Published | 2026-10-28T03:17:07.390 |

Linksys WAG200G through 1.01.06 contains a weak password change mechanism that allows attackers to change the administrator password without supplying the current password. Attackers with access to an authenticated administrator browser session can set a new password to lock out the legitimate administrator and take persistent device control.

### CVE-2026-57190

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:H/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-10-27T22:17:27.197 |

Asterisk is an open source private branch exchange and telephony toolkit. Prior to Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3, the `PostgreSQL` and `TDS/MSSQL` Channel Event Log backends `cel_pgsql` and `cel_tds` may permit arbitrary SQL execution when untrusted data is set in the CEL `eventtype` column by the `CELGenUserEvent` dialplan application. The `cel_pgsql` or `cel_tds` backend must be loaded and configured, and the administrator must call `CELGenUserEvent` in the dialplan without ensuring that only valid data is passed to the application. This issue is fixed in Asterisk 20.20.1, 21.12.3, 22.10.1, 23.4.1 and Certified Asterisk 20.7-cert11, 22.8-cert3.
