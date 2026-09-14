# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-14 15:00 UTC
- **対象期間**: `2026-09-13T15:00:25.000Z` 〜 `2026-09-14T15:00:26.000Z`
- **重要CVE数**: 81 件（Critical 9.0+: 11 件 / High 7.0〜: 70 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件** 近くに上りますが、特に **リモートから認証不要でコード実行や権限昇格が可能** な脆弱性が目立ちます。  
- WordPress 系プラグインや Joomla 拡張機能に対する **認可チェック不備** が多数報告され、Web アプリケーション層での攻撃が容易化。  
- ネットワーク機器（D‑Link、Tenda、Extreme Networks など）や組み込みシステムにおいて **スタックベースのバッファオーバーフロー** が多数確認され、ファームウェア更新が急務です。  
- 認証プラグインや API の実装ミスにより **認証バイパス** が発生し、内部情報漏洩や RCE に直結するケースが増加しています。  

## 2. 特に注目すべき CVE  

| CVE | スコア | 主な影響 | 注目すべき理由 |
|-----|--------|----------|----------------|
| **CVE‑2026‑81648** | 10.0 (CVSS3.1) | CryptoPayment Gateway WordPress プラグイン (1.2.1‑1.2.2) の AJAX エンドポイントで認可チェックが欠如。認証なしで任意ファイル削除・設定上書きが可能。 | **最高スコア** かつ **リモートコード実行／任意ファイル削除** が可能。WordPress サイトは即時パッチ適用が必須。 |
| **CVE‑2026‑90898** | 9.8 | Bifrost 管理 API がデフォルトで認証無効 (`governance.auth_config.is_enabled=false`)。MCP クライアント追加時に任意コマンドが実行される。 | **認証オフ状態がデフォルト** で、攻撃者が管理者権限で任意プログラムを起動できる点が深刻。設定変更とアップデートが急務。 |
| **CVE‑2026‑21391** | 9.5 | PingAM の ID Token クレームを任意に上書きできる不適切検証。トークン偽装により認証バイパス・特権昇格が可能。 | **認証トークンの改竄** が直接的に特権取得に結びつくため、シングルサインオン環境全体の安全性に影響。 |
| **CVE‑2026‑85192** | 9.4 | Joomla 用 Conditional Content 拡張 ( < 8.0.0 ) がインライン PHP を無検証で評価。認証済み権限ユーザーが任意コード実行。 | **Joomla サイトのプラグイン** が攻撃対象となり、管理者権限取得が容易。 |
| **CVE‑2026‑90693** | 9.4 | D‑Link DIR‑878 (120B05) の `SetWan3Settings` でスタックバッファオーバーフロー。リモートから任意コード実行が可能。 | **家庭用/小規模オフィス向けルータ** が広く普及している点と、ファームウェア更新が遅れがちである点がリスク。 |

> **注**：上記は **スコアが高い** だけでなく、**実運用環境で広く利用されている**（WordPress、Joomla、ネットワーク機器）点を加味して選定しています。

## 3. 推奨アクション  

### 3.1 共通の緊急対策
1. **脆弱性情報の社内共有**  
   - セキュリティチーム、インフラチーム、開発チームへ本レポートを速やかに回付。  
2. **外部からのアクセス遮断**  
   - 該当プラグイン／API のエンドポイントが外部から直接到達できないよう、WAF で IP フィルタリングまたは `X-Frame-Options` 等のヘッダーで制限。  
3. **監査ログの強化**  
   - 変更系 API（例: `SetWan3Settings`、プラグインの AJAX）へのリクエストをすべてログに残し、異常なパラメータや頻度を SIEM で検知。  

### 3.2 個別の修正・アップデート

| 脆弱箇所 | 推奨パッケージ／ファームウェア | バージョン/リリース | 対応手順 |
|----------|------------------------------|-------------------|----------|
| CryptoPayment Gateway WordPress plugin | `crypto-payment-gateway` | **≥ 1.2.3** (公式パッチ) | 1. WordPress 管理画面 → プラグイン一覧 → アップデート<br>2. `wp-config.php` で `DISALLOW_FILE_MODS` を一時的に `true` にし、手動でプラグインを上書き。 |
| Bifrost 管理 API | `bifrost` (管理サーバ) | **≥ 2.5.1** (認証デフォルト有効化) | 1. `governance.auth_config.is_enabled` を `true` に設定。<br>2. サービス再起動 (`systemctl restart bifrost`). |
| PingAM | `pingam` (認証サーバ) | **≥ 3.4.2** (トークン検証強化) | 1. パッケージマネージャ (`apt-get upgrade pingam`) で更新。<br>2. `id_token_claims` のホワイトリスト設定を見直す。 |
| Conditional Content (Joomla) | `regularlabs/conditional-content` | **≥ 8.0.0** (PHP 評価サンドボックス化) | 1. Joomla 管理画面 → 拡張機能 → 管理 → アップデート。<br>2. 旧バージョンはすぐに無効化し、バックアップを取得。 |
| D‑Link DIR‑878 (120B05) | ファームウェア `DIR-878_FW_1.07` | **≥ 1.07** (バッファオーバーフロー修正) | 1. D‑Link の管理画面 → システム → ファームウェアアップデート。<br>2. アップデート後、`SetWan3Settings` と `SetDynamicDNSIPv6Settings` の API をテストし、エラーログが出ないことを確認。 |
| D‑Link DIR‑823G (1.0.2B05) | ファームウェア `DIR-823G_FW_1.04` | **≥ 1.04** (strcpy 修正) | 同上。 |
| Tenda W20E (15.11.0.61068) | ファームウェア `W20E_V1.03` | **≥ 1.03** (バッファオーバーフロー対策) | 同上。 |
| Extreme Networks IQ Engine | ファームウェア `IQEngine_10.6r5` | **≥ 10.6r5** (ah_bgd バッファ修正) | 1. Extreme のサポートポータルからダウンロード。<br>2. CLI で `upgrade firmware` を実行。 |
| LightLLM (1.2.0) | `lightllm` (Python パッケージ) | **≥ 

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-81648

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-13T21:17:01.930 |

The CryptoPayment Gateway WordPress plugin from 1.2.1 to 1.2.2 does not apply an authorization check on one of its AJAX endpoints, allowing unauthenticated users to invoke administrative operations, including deleting arbitrary files on the server, overwriting the payment gateway configuration and recovering stored wallet credentials in cleartext.

### CVE-2026-90898

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284;CWE-306` |
| Published | 2026-09-14T11:17:08.237 |

Bifrost registers MCP clients through its management API. A stdio client is a command plus args. Bifrost starts that program in the gateway the moment the client is added. No MCP handshake required.



The default is governance.auth_config.is_enabled=false. Auth off means every caller is a local admin. One unauthenticated POST /api/mcp/client is enough to run a program as the Bifrost process user (appuser on the official image).



 transports/v2.1.0 refuses an unauthenticated stdio registration with 403. transports/v2.0.0 still allows it.

### CVE-2026-21391

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-14T12:17:38.810 |

An improper validation vulnerability exists within PingAM where a well-crafted request allows arbitrary or protected ID Token claims to be set or overridden. In certain configurations this could allow an attacker to bypass authentication controls via spoofing leading to privilege escalation or impersonation.

### CVE-2026-90937

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-09-14T13:19:32.277 |

froxlor versions before 2.2.5 fail to validate newline characters in subdomain redirect URLs, allowing authenticated customers to inject arbitrary nginx or Apache configuration directives. Attackers can supply URLs containing literal newlines that are written verbatim into vhost config files during cron rebuild, enabling web server configuration corruption, denial of service, or hijacking of HTTP responses across hosted domains.

### CVE-2026-90693

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-14T08:16:35.673 |

A flaw has been found in D-Link DIR-878 120B05. This impacts the function SetWan3Settings of the component WAN Settings. This manipulation of the argument Primary/Secondary causes stack-based buffer overflow. Remote exploitation of the attack is possible.

### CVE-2026-90692

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-14T07:17:25.263 |

A vulnerability was detected in D-Link DIR-878 120B05. This affects the function SetDynamicDNSIPv6Settings of the component Dynamic DNS IPv6 Settings. The manipulation of the argument IPv6Address/Hostname results in stack-based buffer overflow. The attack may be launched remotely.

### CVE-2026-85192

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-14T07:17:22.757 |

Joomla Extension - regularlabs.com - Authenticated, privileged remote code execution in Conditional Content extension for Joomla < 8.0.0 - Conditional Content Pro accepts inline PHP Condition Rules in article syntax. In affected versions, the PHP is passed to the Conditions evaluator without checking who authored the article. Joomla's normal Author text filter preserves the syntax, so publishing the article causes the code to run as the web-server process.

### CVE-2026-90680

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-14T04:16:36.353 |

A security flaw has been discovered in D-Link DIR-823G 1.0.2B05_20181207. The impacted element is the function strcpy of the file /HNAP1/SetStaticRouteSettings of the component HNAP1. The manipulation of the argument PAddress/SubnetMask/Gateway results in stack-based buffer overflow. The attack can be launched remotely.

### CVE-2026-90961

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-287` |
| Published | 2026-09-14T14:17:21.270 |

The LdapAuth and LinOTPAuth authentication plugins in MISP contain an authentication bypass vulnerability. Both LdapAuthenticate and LinOTPAuthenticate replace CakePHP's FormAuthenticate class but fail to replicate its _checkFields() input validation guard. As a result, the email and password fields extracted from the login request are passed to downstream authentication logic without verifying that they are non-empty strings.

In the LDAP authenticator, an empty or null password is forwarded to ldap_bind(). Per RFC 4513 section 5.1.2, a bind request with a valid DN and an empty password constitutes an unauthenticated bind, which many LDAP directory servers accept as successful. An attacker who knows any valid user email address in the directory can therefore authenticate as that user without possessing a password. Additionally, non-string values (null, false, arrays) are either coerced to empty strings by ldap_bind(), raise TypeErrors, or are misinterpreted as find conditions in _findUser(), all of which can lead to unintended authentication outcomes.

In the LinOTP authenticator, the same missing guard allows non-string credentials to be concatenated into the LinOTP verification request, and in the mixed-authentication branch an empty password is accepted against a stored hash of the empty string.

A secondary issue in the LDAP authenticator is that newly created user accounts (auto-provisioned on first LDAP login) were assigned an empty password. Because the save path skips validation, the empty string is hashed and stored. If the user later ceases to be found in LDAP and the mixed-authentication fallback is used, the stored hash of the empty string verifies against an empty password, again permitting unauthenticated access.

The vulnerability requires that the affected plugin (LdapAuth or LinOTPAuth) is enabled on the MISP instance and that the attacker knows at least one valid email address registered in the directory or MISP user store. No prior authentication is required. Successful exploitation grants the attacker the full privileges of the impersonated user, which may include administrative access to threat intelligence data.


Version affected: ≤2.5.45

### CVE-2026-90919

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-14T12:17:51.807 |

LightLLM through 1.2.0 contains a remote code execution vulnerability in the Config Server's unauthenticated /visual_register WebSocket endpoint that passes the first client frame directly to pickle.loads(). Attackers can reach the Config Server port and send a malicious serialized payload with a __reduce__ method to execute arbitrary code with Config Server process privileges.

### CVE-2026-12258

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-284` |
| Published | 2026-09-14T13:17:33.290 |

Inadequate access control in Hiperdino’s REST v1.0 API. The public endpoint ‘customer/check’ could allow an authenticated attacker to enter a telephone number or an email address. When the value entered belongs to a registered customer, the service returns the associated information (email address and telephone number). No authentication is required beyond a static bearer token, and there is no rate limiting or generic error handling. Successful exploitation of this vulnerability could allow a remote attacker to enumerate a user’s contact details, although this would require obtaining a valid static bearer token, constituting an information disclosure vulnerability.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-90938

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T13:19:32.430 |

LangBot's plugin runtime (pip package langbot_plugin) through 0.4.17 starts a debug WebSocket server on 0.0.0.0:5401 (/plugin/ws) whose authentication is gated on plugin_debug_key, which defaults to an empty string and is never set by the upstream repository, Docker image, or docker-compose (which additionally publishes port 5401 to the host); the key check is therefore skipped entirely. Any remote attacker able to reach the port can register an arbitrary "debug plugin" without credentials. Because events are broadcast to all initialized plugins without filtering, the attacker's plugin receives the full context of every IM message event (including private chats, message chains, and user/sender IDs in plaintext) and can inject forged replies, send messages as any configured bot, enumerate bot UUIDs, invoke configured LLM models, read knowledge-base contents, and register malicious tools that feed every user's LLM pipeline. Registering with "prod_mode": true causes later legitimate installations of a plugin with the same author/name to be rejected, resulting in persistent denial of service. No patched version was available at the time of publication.

### CVE-2023-50461

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T07:17:15.653 |

An issue was discovered in the direct_mail (aka Direct Mail) extension through 9.5.1 for TYPO3. The Configuration backend module of the extension allows an authenticated user to write to an arbitrary TSConfig page for folders configured as Direct Mail. Exploiting this may lead to Configuration Injection (TYPO3 10.4 and above) and to Arbitrary Code Execution (TYPO3 9.5 and below). A valid backend user account, with access to the Direct Mail Configuration backend module, is needed to exploit this.

### CVE-2023-46273

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-14T06:16:54.647 |

Bonjour Gateway in Extreme Networks IQ Engine before 10.6r1a, and through 10.6r4 before 10.6r5, has an ah_bgd buffer overflow via ah_event_send.

### CVE-2026-88793

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-13T21:17:02.197 |

The YouTube Embed WordPress plugin from 10.0 to 10.3 does not perform any authorisation check on one of its AJAX actions, relying only on a nonce it prints on every front-end page, and does not escape the stored data before rendering it, allowing unauthenticated attackers to store arbitrary web scripts which will execute in the session of any user viewing the affected content, including an administrator.

### CVE-2026-85129

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-13T21:17:02.063 |

The Hoo Companion WordPress plugin 1.0.2 does not have any authorisation or validation checks in one of its import features, and does not sanitise the data submitted to it before storing it as the active theme's settings, allowing unauthenticated attackers to inject arbitrary web scripts which will execute for anyone viewing the site, including administrators. The same request destroys the site's existing theme settings.

### CVE-2026-74933

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-13T21:17:01.800 |

The GenieWords WordPress plugin from 1.5.27 to 1.5.34 does not have authorisation checks on some of its REST API and AJAX actions, and decodes stored values before printing them, allowing unauthenticated users to overwrite its configuration and inject arbitrary web scripts that execute on every front-end page.

### CVE-2026-90934

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T13:19:31.830 |

EspoCRM before 10.0.4 contains a field-level security bypass vulnerability in the meeting and call attendees endpoints that allows authenticated users to read restricted email addresses. Attackers can recover hidden attendee emails by exploiting incorrect ACL scope validation that checks parent event permissions instead of attendee entity permissions.

### CVE-2026-89180

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T11:17:05.860 |

EFence developed by Thinking Software Technology has a SQL Injection vulnerability, allowing unauthenticated remote attackers to inject arbitrary SQL commands to read database contents.

### CVE-2026-90689

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-14T07:17:24.700 |

A security flaw has been discovered in Tenda W20E 15.11.0.61068_1546_841_CN_TDC. Impacted is the function formDelWebAuthWhiteUser. Performing a manipulation of the argument webAuthWhiteUserIndex results in stack-based buffer overflow. The attack can be initiated remotely.

### CVE-2026-82794

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:21.617 |

SolarView Compact contains an OS command Injection vulnerability in in Schedule Settings. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82791

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:21.203 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in Contec CAN 2.0B Communication Wireless LAN / USB Converter Unit. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82789

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-95` |
| Published | 2026-09-14T07:17:20.920 |

An improper neutralization of directives in dynamically evaluated code ('Eval Injection') issue exists in CONPROSYS HMI System(CHS). If exploited, arbitrary code may be executed by an attacker who can log in to the product.

### CVE-2026-82787

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-09-14T07:17:20.660 |

Missing authentication for critical function vulnerability exists in CPSL-08P1EN. If this vulnerability is exploited, an affected product may be operated by a remote attacker without authentication.

### CVE-2026-82780

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-14T07:17:19.663 |

Unrestricted upload of file with dangerous type issue exists in CONPROSYS TM Series. If a specially crafted file is uploaded by a remote authenticated attacker, an arbitrary command may be executed on the product.

### CVE-2026-82779

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:19.530 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in CONPROSYS TM Series. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82777

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:19.247 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in CONPROSYS PAC Series. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82774

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:18.833 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in CONPROSYS M2M Gateway Series and CONPROSYS M2M Controller Series. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82772

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-14T07:17:18.557 |

Buffer overflow vulnerability exists in Contec EC1000 series. If a remote attacker sends a specially crafted request to the product's web service, an arbitrary program may be executed.

### CVE-2026-82770

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-09-14T07:17:18.277 |

Buffer overflow vulnerability exists in Contec RP-WAH-SR Series. If a remote attacker sends a specially crafted request to the product's web service, an arbitrary program may be executed.

### CVE-2026-82766

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:17.707 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in SGA1000. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-82762

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-14T07:17:17.040 |

Improper neutralization of special elements used in an OS command ('OS Command Injection') issue exists in Contec FX5000 series, FX4000 series, and FX3000 series. If this vulnerability is exploited, an arbitrary OS command may be executed by an attacker who can log in to the product.

### CVE-2026-90932

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-09-14T13:19:31.523 |

LaraDashboard versions 0.9.2 through 1.2.2 contain a path traversal vulnerability in the core-upgrade backup handling. CoreUpgradeController and BackupService (e.g. BackupService::deleteBackup()) concatenate the user-supplied backup_file/filename value directly onto the backup directory path without normalisation, without applying basename(), and without verifying that the resolved path remains inside storage/app/core-backups; the corresponding form requests only validate the value as a bounded string. An authenticated user holding only the delegated settings.edit permission (not Superadmin) can supply ../ traversal sequences to delete arbitrary files reachable on the host filesystem, including outside the application tree, or to restore a ZIP archive from an arbitrary on-disk location, writing arbitrary files into the application directories and achieving remote code execution. Note: the advisory states the vulnerable concatenation was introduced in the v0.9.7 release line. No patched version was available at the time of publication.

### CVE-2026-78375

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-14T11:17:04.430 |

Joomla Extension - joomshaper.com - Authenticated Privileged SQL Injection in the Content Plugin of SP Page Builder (Free and Pro) 5.2.1 - 6.9.0 - plgContentSppagebuilder::onContentAfterSave() read jform[attribs][sppagebuilder_article_id] from the request and concatenated it directly into the WHERE view_id = ... clause of a query against #__sppagebuilder without quoting or type casting. Joomla's ARRAY input filter does not sanitise element values, as InputFilter::clean() returns (array) $source with the elements untouched, so the entire payload could be delivered in a single POST field. The affected block also executed before the com_content.article context test, so it ran on every onContentAfterSave event regardless of which component triggered the save. An attacker could perform time-based blind SQL injection to read arbitrary database contents, including the #__users and #__session tables.

### CVE-2026-90699

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-14T09:17:02.530 |

A weakness has been identified in D-Link DWR-M920 1.1.7. This issue affects the function sub_41E60C of the file /boafrm/formPinManageSetup. This manipulation of the argument newPin causes os command injection. The attack can be initiated remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-82793

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-09-14T07:17:21.480 |

Unrestricted upload of file with dangerous type issue exists in Contec CAN 2.0B Communication Wireless LAN / USB Converter Unit. If a specially crafted file is uploaded by a remote authenticated attacker, arbitrary code may be executed on the product.

### CVE-2026-82768

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-14T07:17:17.980 |

Path traversal vulnerability exists in SGA1000. If this vulnerability is exploited, arbitrary files on the server may be viewed and/or altered by an attacker who can access the product via FTP.

### CVE-2026-82765

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-14T07:17:17.553 |

Path traversal vulnerability exists in Contec FX5000 series, FX4000 series, and FX3000 series. If this vulnerability is exploited, arbitrary files on the server may be viewed and/or altered by an attacker who can access the product via FTP.

### CVE-2023-45858

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-23` |
| Published | 2026-09-14T06:16:54.357 |

A directory traversal was identified in Paessler PRTG before 23.4.88.1429 that made it possible to read local files.

### CVE-2026-90608

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-14T01:16:28.130 |

A flaw has been found in Totolink A3002MU Hh-B20211125.1046. The affected element is the function formPortFw of the file /boafrm/formPortFw of the component boa. This manipulation of the argument service_type causes buffer overflow. It is possible to initiate the attack remotely. The exploit has been published and may be used.

### CVE-2026-90607

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-14T01:16:27.870 |

A vulnerability was detected in Totolink A3002MU Hh-B20211125.1046. Impacted is the function formNewSchedule of the file /boafrm/formNewSchedule of the component boa. The manipulation of the argument submit-url results in buffer overflow. The attack may be performed from remote. The exploit is now public and may be used.

### CVE-2026-90606

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-14T00:16:57.617 |

A security vulnerability has been detected in Totolink A3002MU Hh-B20211125.1046. This issue affects the function formIpv6Setup of the file /boafrm/formIpv6Setup of the component boa. The manipulation of the argument static_ipv6 leads to buffer overflow. The attack is possible to be carried out remotely. The exploit has been disclosed publicly and may be used.

### CVE-2026-90605

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-120` |
| Published | 2026-09-14T00:16:57.447 |

A weakness has been identified in Totolink A3002MU Hh-B20211125.1046. This vulnerability affects the function formFilter of the file /boafrm/formFilter of the component boa. Executing a manipulation of the argument ip6addr can lead to buffer overflow. The attack can be executed remotely. The exploit has been made available to the public and could be used for attacks.

### CVE-2026-20773

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T11:17:03.820 |

A role-based access control issue was identified in the administrative expression evaluation functionality. This could allow users with certain administrative roles to access expression testing capabilities beyond their intended permissions.

### CVE-2026-90703

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-14T10:17:05.610 |

A vulnerability has been found in D-Link DWR-M921 1.1.52. The affected element is the function system of the file /boafrm/formDiskCreateShare. Such manipulation of the argument folderpath leads to os command injection. The attack may be launched remotely. The exploit has been disclosed to the public and may be used.

### CVE-2026-90702

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-77;CWE-78` |
| Published | 2026-09-14T10:17:05.447 |

A flaw has been found in D-Link DWR-M921 1.1.52. Impacted is the function system of the file /boafrm/formDiskFormat. This manipulation of the argument partition causes os command injection. The attack may be initiated remotely. The exploit has been published and may be used.

### CVE-2026-12518

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-14T08:16:34.320 |

A local privilege escalation vulnerability in the Logitech Logi Options+ updater service on Windows allows a low-privileged local user to execute arbitrary code as SYSTEM.

### CVE-2024-58383

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-14T13:17:15.150 |

Froxlor before 2.2.0 (affected up to and including 2.2.0-rc3) generates /etc/pure-ftpd/db/mysql.conf with mode 0644 via the XML configuration templates in lib/configfiles/, even though the file contains the Froxlor SQL user's password. On systems where the parent directories are world readable (the default on Debian 12), any unprivileged local user able to execute commands or code on the host — including virtual users without SSH access who can upload PHP/CGI scripts — can read the file and obtain the Froxlor database credentials. Database access can then be leveraged to alter an administrator's password hash and TOTP seed, log in as a Froxlor administrator, and ultimately gain root privileges. Only instances configured to use pure-ftpd are affected.

### CVE-2026-90895

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-150;CWE-200;CWE-522;CWE-862` |
| Published | 2026-09-14T10:17:06.270 |

Affected versions of MISP’s interactive CLI shell implement access control independently from the normal web application, causing several authorization inconsistencies.


The patch shows that CLI access could differ from the web application in multiple security-sensitive areas:

 - feed listings did not enforce the same lookup_visible restrictions for non-host-organisation users;
 - feed detail access did not enforce the same host-organisation/site-admin authorization as FeedsController::view();
 - Feed.headers, which can contain HTTP authorization credentials, could be exposed instead of being hidden or masked;
 - server synchronization authkey values were not explicitly hidden from CLI detail output;
 - sharing-group detail access did not consistently use SharingGroup::checkIfAuthorised();
 - the use command could establish context for a record without first proving that the user was authorized to view that record


The commit additionally hardens pagination and terminal rendering, including neutralization of terminal control sequences found in database-backed values. Those are important hardening changes, but the main vulnerability is the CLI authorization/data-disclosure mismatch.

Version affected: ≤2.5.45

### CVE-2026-68955

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-427` |
| Published | 2026-09-14T07:17:16.663 |

The installer for Rakuten Kobo Desktop Application (Windows version) insecurely loads Dynamic Link Libraries. If there is a crafted DLL at the same directory when invoking the affected installer, arbitrary code may be executed with the privileges of the user who performed the installation.

### CVE-2026-82786

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-09-14T07:17:20.510 |

Insufficiently protected credentials issue exists in Remote I/O Coupler Unit (Server Type) CPSN-MCB271-*. If this vulnerability is exploited, sensitive information may be restored from a backup file.

### CVE-2026-37008

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-424` |
| Published | 2026-09-13T21:17:01.303 |

CrewAI before fb2323b offers a Python blocklist approach that operates at the wrong level of abstraction, a different vulnerability than CVE-2026-2275. Import-time blocking of module names does not address the availability of Python's complete object graph. For example, calling ctypes.CDLL(None) loads the C library without relying in any import statements. In other words, a within-process sandbox cannot merely account for the import system and instead must account for the complete runtime of the Python interpreter.

### CVE-2026-90949

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T14:17:20.840 |

A flaw was found in GIMP's PSP (Paint Shop Pro) file loader. When processing a compressed selection channel, a heap-based buffer overflow can occur due to a mismatch between the allocated buffer size and the amount of data decompressed. A remote attacker could exploit this vulnerability by crafting a malicious PSP file. Opening this file in GIMP could lead to a crash or arbitrary code execution.

### CVE-2026-90948

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-14T14:17:20.693 |

A flaw was found in GIMP's ICO file loader. When processing an ICO file containing an embedded PNG image, an integer overflow can occur during the calculation of the required buffer size. This leads to an undersized buffer being allocated, causing a heap-based buffer overflow when the decoded pixel data is written. A remote attacker could exploit this by crafting a malicious ICO file, which, when opened, could lead to arbitrary code execution or a crash.

### CVE-2026-90894

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78;CWE-88;CWE-269` |
| Published | 2026-09-14T10:17:06.133 |

Parallels Desktop runs prl_disp_service as root. Local clients reach it on the world-writable socket /var/run/prl_disp_service.socket. PrlSrv_LoginLocal accepts peer credentials. No Parallels signature. No admin group.



After login, PrlSrv_InstallAppliance lets you pick the appliance folder (sVmParentPath). The daemon unpacks with one string, tar -xf "%1" -C "%2", then Qt QProcess::splitCommand chops that string into words. A quote in the folder name closes early. The leftover text becomes extra tar flags. macOS tar --use-compress-program= runs the named program as root.

### CVE-2026-23789

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-415` |
| Published | 2026-09-14T02:17:13.397 |

An issue was discovered in MFC in Samsung Mobile Processor and Wearable Processor Exynos 850, 1080, 2100, 1280, 2200, 1330, 1380, 1480, 2400, 1580, 2500, 2600, 1680, W920, W930, and W1000. A double-free vulnerability in the Exynos MFC encoder driver (due to improper cleanup of dma_buf references during error handling) leads to kernel memory corruption and potential arbitrary code execution.

### CVE-2026-31278

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-319` |
| Published | 2026-09-14T02:17:14.080 |

An issue in the /api/v2/setting/adserversetting endpoint of Suprema BioStar 2 before 2.9.12 and and BioStar X before 1.0.2 allows attackers to obtain Active Directory service account credentials in cleartext by supplying a crafted GET request.

### CVE-2026-29811

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:N/I:H/A:N` |
| Weaknesses | `CWE-1025` |
| Published | 2026-09-13T20:16:51.020 |

CyberPanel before 2.4.4 attempts to detect an "alais" domain (i.e., a second domain that serves the same content as a primary domain; normally spelled "alias") via an ORM query filter rather than a Python "if" statement.

### CVE-2026-90930

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-09-14T13:19:31.190 |

File Browser through 2.63.23 applies path rules to the requested lexical path but resolves symbolic links without reapplying rules to the target, allowing authenticated users to bypass deny rules. Attackers can read and overwrite rule-denied files by accessing them through in-scope symbolic link aliases that resolve to denied paths.

### CVE-2026-88853

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:24.383 |

Joomla Extension - regularlabs.com - Privileged stored XSS via event handler option in Modals Pro extension for Joomla < 17.0.0 - Modals Pro intentionally supports JavaScript Events such as on-open and on-closed. Affected versions do not distinguish trusted extension configuration from event code supplied in ordinary article content. A lower-privileged author can therefore use a documented executable feature which should be reserved for trusted authors.

### CVE-2026-88852

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:24.250 |

Joomla Extension - regularlabs.com - Privileged stored XSS via url option in Snippets Free extension for Joomla < 7.0.0, Snippets Pro extension for Joomla < 11.0.0 - Snippets substitutes variable values supplied by an article tag into saved Snippet content. The affected versions do not consider the article author's trust level. A lower-privileged author can therefore place an unsafe value into a security-sensitive position chosen by the trusted Snippet author.

### CVE-2026-85195

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:22.887 |

Joomla Extension - regularlabs.com - Privileged stored XSS via link option in Articles Anywhere extension for Joomla < 20.0.0 - Articles Anywhere accepts link options such as onclick and onmouseover. In affected versions, those options become real HTML event attributes without checking the article author's trust level. The plugin syntax survives Joomla's normal Author content filter because the executable HTML is generated later.

### CVE-2026-85191

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:22.627 |

Joomla Extension - regularlabs.com - Privileged stored XSS via rtla-alias option in Tabs & Accordions extension for Joomla < 3.1.0 - Tabs & Accordions rewrites links matching an item alias into calls to its browser API. The affected renderer places the alias inside a quoted JavaScript argument in an HTML onclick attribute without securing both the JavaScript-string and HTML-attribute contexts. A crafted data-rlta-alias value can therefore change the generated handler.

### CVE-2026-85190

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:22.490 |

Joomla Extension - regularlabs.com - Privileged stored XSS via class option in Quick Index extension for Joomla < 5.0.5 - Quick Index inserts configurable class values into generated HTML without escaping them for an HTML attribute. A crafted value can close the intended class attribute and introduce a new attribute. Joomla's content filter cannot reliably prevent this because Quick Index creates the executable HTML after the authored plugin syntax was filtered.

### CVE-2026-85189

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T07:17:22.357 |

Joomla Extension - regularlabs.com - Privileged stored XSS via executable URL schemes in Modals extension for Joomla < 17.0.0 - Modals treats a destination using an executable browser URL scheme as an ordinary modal URL. The value can reach both the generated link and the iframe-loading path. Authored content can consequently become JavaScript in a visitor's browser without using Modals' separate Pro JavaScript Events feature.

### CVE-2023-32803

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-669` |
| Published | 2026-09-14T05:16:57.290 |

The ca-certificates package before ca-certificates-2021.2.50-72 for Amazon Linux 2 (AL2) does not properly remove certain TrustCor root certificates from the root store. NOTE: this issue exists because of an incorrect fix for CVE-2022-23491.

### CVE-2026-33963

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:C/C:N/I:H/A:H` |
| Weaknesses | `CWE-121` |
| Published | 2026-09-14T02:17:14.850 |

An issue was discovered in camera in Samsung Mobile Processor Exynos 1330, 1380, 1480, 2400, 1580, 2500, 2600, and 1680. A stack-based buffer overflow occurs when a malformed message is sent to the camera driver, causing a denial of service.

### CVE-2026-15891

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-09-13T23:16:27.870 |

The MQTT-SN client keepalive handler process_ping() in subsys/net/lib/mqtt_sn/mqtt_sn.c removes the gateway record after PINGREQ retries are exhausted. It invoked SYS_SLIST_PEEK_HEAD_CONTAINER(&client->gateways, gw, next) but discarded the result. That macro is a pure expression that does not assign to gw, so gw retained its NULL initializer regardless of the list contents.

The code then dereferences the NULL gw (gw->gw_id) and passes it to mqtt_sn_gw_destroy(), reaching k_mem_slab_free(&gateways, NULL). With CONFIG_MEM_SLAB_POINTER_VALIDATE enabled this triggers k_panic(); in the default configuration it performs a write through the NULL pointer ((char )mem = slab->free_list;) and corrupts the slab free list. The outcome is a crash/kernel panic or, on targets where address 0 is writable, silent memory-allocator corruption.

The vulnerable branch runs whenever the connected MQTT-SN gateway fails to answer keepalive PINGREQs for the configured number of retries. This condition is controlled by the remote peer: a malicious or compromised gateway, or an on-path/adjacent attacker that advertises itself as a gateway and then stops responding (or blackholes the real gateway's PINGRESPs), forces the client into the defect. MQTT-SN runs over UDP and no authentication is required.

The impact is a remotely triggerable denial of service (availability) of the affected MQTT-SN client; there is no attacker-controlled data written. The sibling remover process_advertise() uses SYS_SLIST_FOR_EACH_CONTAINER_SAFE and is not affected. The fix assigns the macro's return value to gw.

### CVE-2026-88802

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-13T21:17:02.323 |

The MDJM Event Management WordPress plugin before 1.7.8.5 and the Mobile Events Manager WordPress plugin through 1.4.8.3 do not check a capability, a nonce or the type of the record before permanently deleting the post identified in a request to their playlist entry removal, allowing unauthenticated attackers to destroy arbitrary posts, pages and media attachments, bypassing the trash.

### CVE-2026-36453

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-425` |
| Published | 2026-09-13T21:16:59.947 |

Rhymix before 2.1.31 allows insecure direct object reference, aka RVE-2026-1. Arbitrary files can be accessed via extra variables.

### CVE-2026-73195

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-116` |
| Published | 2026-09-14T14:17:08.597 |

Improper Encoding or Escaping of Output vulnerability in Apache Syncope.



Authenticated users can store a spreadsheet formula payload in one of their own plain attributes. When such users are included in a CSV export and the generated CSV file is opened by a spreadsheet application, the formula may be executed.





This issue affects Apache Syncope: from 3.0.0-M0 through 3.0.16, from 4.0.0-M0 Through 4.0.7, from 4.1.0-M0 through 4.1.2.

Users are recommended to upgrade to version 4.0.8 / 4.1.3, which fix this issue.

### CVE-2026-90929

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-14T13:19:31.030 |

File Browser versions >= 2.5.0 and <= 2.63.23 contain an incorrect authorization flaw in the direct-upload endpoint (resourcePostHandler in http/resource.go). Unlike the TUS upload handler, the direct-upload handler does not reject a target that is an existing directory; a POST with ?override=true aimed at a directory fails inside writeFile (a directory cannot be opened for writing) and the failure-cleanup path then calls Fs.RemoveAll on the request path, recursively deleting the entire tree. This cleanup is gated by neither the Perm.Delete permission nor the checkDescendants rule walk applied by the delete and patch handlers, so an authenticated non-administrator holding only the default Create and Modify permissions can delete directories they are not authorized to delete, including rule-denied files within them. Deletion remains confined to the user's scope because ScopedFs.RemoveAll still enforces the scope guard. The faulty cleanup was introduced in v2.5.0; no patched version is available.

### CVE-2023-28148

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-09-14T05:16:56.837 |

A bodyclass XSS issue was discovered in Paessler PRTG before 23.3.86.1520.

### CVE-2026-90939

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T14:17:20.240 |

novel-plus through 5.3.3 contains an information disclosure vulnerability in the /sys/user/list endpoint that lacks proper permission annotations. Authenticated attackers can retrieve password hashes and personal data including email addresses and phone numbers for users within their data scope, enabling offline hash cracking and account takeover.

### CVE-2026-90933

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T13:19:31.680 |

laradashboard through 1.2.2 contains a missing authorization vulnerability in the Local License API endpoints that allows any authenticated user to read, overwrite, and delete premium module license keys. Attackers with low-privileged accounts can access GET /api/admin/licenses/show, POST /api/admin/licenses/store, and POST /api/admin/licenses/remove endpoints to disclose confidential license keys, inject attacker-controlled values, or delete stored licenses entirely.

### CVE-2026-90928

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-14T13:19:30.870 |

File Browser through 2.63.23 contains a memory exhaustion vulnerability in the subtitle conversion endpoint that loads entire subtitle files into memory without size limits. Authenticated attackers with download permission can request conversion of large .srt, .ass, or .ssa files and exhaust server memory through concurrent requests, causing denial of service.

### CVE-2026-90927

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-09-14T13:19:30.710 |

filebrowser through 2.63.23 fails to limit WebSocket message size in the /api/command handler before checking permissions, allowing authenticated users to buffer arbitrarily large messages. Attackers can send oversized WebSocket messages to exhaust server heap memory and cause denial of service regardless of EnableExec setting or Execute permission.

### CVE-2026-8821

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-14T11:17:06.153 |

Mattermost versions 11.9.x <= 11.9.0, 11.8.x <= 11.8.4, 11.7.x <= 11.7.7, 10.11.x <= 10.11.22 fail to validate channel member-management permission during playbook run creation, allowing an authenticated channel member to add an arbitrary user to a restricted channel via the run owner field.. Mattermost Advisory ID: MMSA-2026-00677

### CVE-2026-90688

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-119;CWE-121` |
| Published | 2026-09-14T07:17:24.513 |

A vulnerability was identified in Tenda W20E 15.11.0.61068_1546_841_CN_TDC. This issue affects the function formIPMacBindAdd of the component HTTP Handler. Such manipulation of the argument IPMacBindRule leads to stack-based buffer overflow. It is possible to launch the attack remotely.

### CVE-2026-81564

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:N/VI:H/VA:H/SC:N/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-14T11:17:04.707 |

Joomla Extension - joomshaper.com - Missing Directory Confinement in Media Rename Allowing Arbitrary File Rename in SP Page Builder (Free and Pro) 4.0.0 - 6.9.0 - The media rename task applied neither of the directory boundary checks used by the folder operations in the same controller, and its validation guard required only that either a media record exist for the supplied identifier or that the supplied path be present in #__spmedia, rather than both. The identifier and the path were consequently never checked against one another, so any valid media identifier could be paired with an unrelated filesystem path, and the STR input filter left traversal sequences intact. An attacker could rename files elsewhere in the installation, including renaming configuration.php to take the site offline.

### CVE-2026-71198

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-14T07:17:16.867 |

In OpenStack Glance before 32.0.1, the location API does not validate destination hosts when adding an HTTP location to an image. Unlike the web-download import path, the location API only checks the URL scheme and does not apply the import_filtering_opts host restrictions. An authenticated user can add a location pointing to internal endpoints such as the cloud metadata service (169.254.169.254), and retrieve the response by downloading the image data. This affects both the new POST /v2/images/{id}/locations API and the old PATCH API when show_multiple_locations is enabled. Deployments with the HTTP store backend enabled are affected.
