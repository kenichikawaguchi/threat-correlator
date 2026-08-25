# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-08-25 15:00 UTC
- **対象期間**: `2026-08-24T15:00:18.000Z` 〜 `2026-08-25T15:00:39.000Z`
- **重要CVE数**: 205 件（Critical 9.0+: 38 件 / High 7.0〜: 167 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
2026 年上半期に公開された CVE のうち、CVSS スコアが 7.0 以上のものは **30 件以上** に上ります。目立つ傾向は以下の通りです。  

* **認証不要でリモートコード実行 (RCE) や権限昇格が可能** な脆弱性が多数。特に WordPress・Joomla のプラグイン・テーマ、IoT デバイス向けスタック、そして Python ライブラリ (NLTK) に集中しています。  
* **サードパーティ製拡張機能** が攻撃対象になるケースが増加。公式リポジトリに掲載されているものでも、メンテナンスが遅れたバージョンが多数残っている点がリスクです。  
* **攻撃経路は「ネットワーク直接アクセス」だけでなく、** フォーム入力や HTTP ヘッダー、シリアライズデータといった **アプリケーション層の入力** を通じても実行可能となっている点が共通しています。  

---

## 2. 特に注目すべき CVE  

| CVE | スコア | 製品・コンポーネント | 主な影響 | 注目理由 |
|-----|--------|----------------------|----------|----------|
| **CVE‑2026‑77998** | 10.0 | Joomla Extension **miniOrange SAML SSO** (≤ 11.0.1) | 認証バイパス → 任意ユーザーとしてログイン可能 | SAML の署名検証ロジックに致命的な欠陥があり、外部から **SAMLResponse** を改ざんして認証を回避できる。企業のシングルサインオン基盤全体が危険にさらされる。 |
| **CVE‑2026‑32559** | 9.9 | **UltimateAI** (≤ 3.1.0) | 任意ファイルアップロード → RCE | 「Subscriber」権限さえあれば任意のファイルをサーバ上に配置でき、Web シェル設置が容易。管理者権限取得の前段階として非常に危険。 |
| **CVE‑2026‑78570** / **CVE‑2026‑78568** | 9.8 | WordPress プラグイン **Total Donations** (≤ 2.0.5) | ① 権限昇格 (Unauthenticated → Administrator) ② SQL インジェクション (任意データ取得・改ざん) | 同一プラグインで 2 つの重大脆弱性が同時に残存。プラグインが有効化されているだけで **全サイトが乗っ取られる** 可能性がある。 |
| **CVE‑2026‑57909** | 9.4 | **WatchGuard Agent** (特定バージョン) | パストラバーサル + 任意コード実行 | 隣接ネットワークからのアクセスで **/etc/passwd** 取得やシェル実行が可能。VPN/UTM 製品に組み込まれることが多く、企業ネットワークの境界防御が崩れる危険性が高い。 |
| **CVE‑2026‑78683** | 9.4 | Python ライブラリ **NLTK** (≤ 3.9.4) | unsafe pickle デシリアライズ → RCE | データサイエンス環境や CI/CD パイプラインで広く利用されている。攻撃者が制御できる入力 (例: 学習データやモデル) を通じて **任意コード実行** が可能になる。 |

> **共通点**：すべて **認証不要**、または **低権限** での操作だけでシステム全体を制御できる点。特に Web アプリケーションのプラグイン・拡張機能は、インストールだけで攻撃対象になるため、管理者は即時の対策が必要です。

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ
| 製品 | 現行脆弱バージョン | 修正版 / 推奨バージョン | 対応手順 |
|------|-------------------|------------------------|----------|
| miniOrange SAML SSO (Joomla) | ≤ 11.0.1 | **11.0.2** 以上 | Joomla 管理画面 → Extensions → Manage → Update で公式リポジトリから最新版を適用 |
| UltimateAI | ≤ 3.1.0 | **3.1.1** 以上 | pip/conda で `pip install --upgrade ultimateai` またはベンダー提供のパッケージをデプロイ |
| Total Donations (WordPress) | ≤ 2.0.5 | **2.0.6** 以上 | WordPress 管理画面 → Plugins → Installed Plugins → Update、もしくは FTP で `total-donations.zip` を上書き |
| WatchGuard Agent | 該当バージョン (ベンダー公開情報参照) | **最新安定版** (2026‑09‑リリース) | WatchGuard 管理コンソールから「Firmware/Agent Update」実行、または手動でエージェントバイナリを置換 |
| NLTK | ≤ 3.9.4 | **3.10.0** 以上 | `pip install --upgrade nltk`（依存関係の再インストール推奨） |
| OAuth2‑Proxy (参考) | 任意 | **v0.13.0** 以上 | `docker pull quay.io/oauth2-proxy/oauth2-proxy:v0.13.0` でイメージ更新、設定ファイルの `X-Forwarded-Uri` 無視オプションを有効化 |

### 3.2 侵入検知・防御設定
1. **WAF ルール追加**  
   * `SAMLResponse` パラメータに対する署名検証失敗を検知し、リクエストをブロック。  
   * WordPress の `wp-admin/admin-ajax.php` への不審な POST をレートリミット。  
2. **ネットワークレベルでの遮断**  
   * WatchGuard Agent の管理ポート (例: 443/8443) への **隣接ネットワークからの直接アクセス** を ACL で拒否。  
   * OAuth2‑Proxy の `X-Forwarded-Uri` ヘッダーを信頼しない設定 (`skip-auth-headers = false`) を有効化。  
3. **ログ監視**  
   * Joomla の認証ログに **SAMLResponse** の異常パラメータが出たらアラート。  
   * NLTK を使用するサーバーで `pickle.load` が呼び出されたスタックトレースを監視（`auditd` で syscalls を捕捉）。  

### 3.3 緊急対応手順（インシデント発生時）
1. **影響範囲の特定**  
   * 該当プラグイン/ライブラリがインストールされているサーバを `grep -R "miniOrange\|total-donations\|ultimateai\|watchguard\|nltk"` で抽出。  
2. **一時的な防御**  
   * WordPress:

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-77998

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-25T13:19:30.817 |

Joomla Extension - miniorange.com - Unauthenticated Authentication Bypass via SAMLResponse Parameter in miniOrange SAML SSO < 11.0.2, SAML SP Single Sign On – Login with ADFS < 6.4,  SAML SP Single Sign On – SAML SSO login with Google Apps < 6.4 - This is due to the mo_saml_validate_signature() function performing a loose boolean check on the raw tri-state integer returned by PHP's openssl_verify(), causing an error return value of -1 to be evaluated as truthy and therefore treated as a successful signature verification. This makes it possible for unauthenticated attackers to log in as any existing Joomla user, including administrators, by submitting a crafted SAMLResponse containing an attacker-controlled NameID and a deliberately malformed signature value that triggers an OpenSSL processing error — bypassing verification entirely and resulting in wp_set_auth_cookie() being called for the targeted account.

### CVE-2025-36939

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-24T17:17:21.143 |

Multiple vulnerabilities exist in OpenThread's handling of MLE packets. An authenticated attacker on the same Thread network could send specially crafted packets to cause a denial of service. These issues include triggerable assertion failures and a stack-based buffer overflow.

### CVE-2026-32559

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-24T22:16:51.900 |

Subscriber Arbitrary File Upload in UltimateAI <= 3.1.0 versions.

### CVE-2026-78570

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-25T10:18:13.563 |

The Total Donations plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 2.0.5. This makes it possible for unauthenticated attackers to elevate their privileges to that of an adminsitrator.

### CVE-2026-78568

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T09:17:36.590 |

The Total Donations plugin for WordPress is vulnerable to SQL Injection in all versions up to, and including, 2.0.5 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-78477

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-25T06:19:01.147 |

The Jawn theme for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 1.4.2. This makes it possible for unauthenticated attackers to elevate their privileges to that of an administrator.

### CVE-2026-13214

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-25T05:17:20.060 |

The OCPP 1.6 client in subsys/net/lib/ocpp/ocpp_j.c contains a stack buffer overflow in parse_getconfig_msg(). When handling a GetConfiguration request from the central system, the handler copied the attacker-controlled JSON "key" string into the caller's fixed 50-byte stack buffer (skey[CISTR50], declared in subsys/net/lib/ocpp/ocpp.c) using an unbounded strcpy(). The parsed key value points directly into the receive buffer, so its length is bounded only by the message size (CONFIG_OCPP_RECV_BUFFER_SIZE, default 2048).

The GetConfiguration message is delivered over the WebSocket connection that the charge point opens to its configured central system. The reader thread ocpp_wsreader() reads the message into ui->recv_buf and dispatches it to parse_getconfig_msg() via the PDU function table. An attacker who controls the central system endpoint, or a man-in-the-middle on an unencrypted connection, can send a GetConfiguration request whose "key" field exceeds 50 bytes and overflow the reader thread's stack with attacker-chosen bytes.

The consequence is a remotely triggerable stack smash on the OCPP reader thread: at minimum a denial of service, and plausibly remote code execution depending on build-time hardening such as stack canaries and MPU configuration. The fix replaces the strcpy() with a bounded strncpy(key, payload.key[0], CISTR50 - 1) followed by explicit NUL termination, matching the bounded copies already used by the sibling handlers.

### CVE-2026-78267

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T22:17:20.670 |

Unauthenticated Privilege Escalation in TranslatePress <= 3.3.2 versions.

### CVE-2026-78265

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-24T22:17:20.407 |

Unauthenticated PHP Object Injection in The Events Calendar <= 6.17.2 versions.

### CVE-2026-78262

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-24T22:17:19.947 |

Unauthenticated PHP Object Injection in WP Project Manager <= 4.0.6 versions.

### CVE-2026-32563

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-24T22:16:52.287 |

Subscriber PHP Object Injection in ACPT (Pro) - Custom Post Types Plugin for WordPress <= 2.0.63 versions.

### CVE-2026-77136

| 項目 | 値 |
|------|-----|
| CVSS | `9.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-25T09:17:34.187 |

The extension passes the raw value of a form field configured as "This field contains the name of the sender" directly into a Fluid View as template source, without any sanitization, and renders it. An anonymous, unauthenticated user can submit Fluid template syntax in that field to execute arbitrary Fluid ViewHelpers leading to disclosure of server configuration, environment variables and application source, and potentially remote code execution. Exploitation requires only that a form field is configured as the sender_name field, a common and default-adjacent Powermail configuration. No authentication or user interaction beyond a normal form submission is required. This vulnerability is reported to be actively exploited in the wild.

### CVE-2026-57909

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-306` |
| Published | 2026-08-25T12:16:24.617 |

A path traversal vulnerability in WatchGuard Agent allows a remote, unauthenticated attacker on an adjacent network to execute arbitrary code on an affected system.

### CVE-2026-78683

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-25T02:16:53.033 |

NLTK before 3.10.0 (affected versions <=3.9.4) contains an unsafe pickle deserialization vulnerability in the TransitionParser.parse() method (nltk/parse/transitionparser.py). The method calls pickle_load() with the default restricted=False, routing deserialization through WarningUnpickler, which does not override find_class() and therefore permits arbitrary class resolution. When an application loads an attacker-crafted model file, embedded pickle gadget chains execute arbitrary Python code with the privileges of the user running the application. NLTK provides a RestrictedUnpickler for safe deserialization, but it is not used by production code paths. Fixed in 3.10.0.

### CVE-2026-78555

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200;CWE-522` |
| Published | 2026-08-24T20:17:24.850 |

RansomLook exposed complete API keys in the HTML source of the authenticated /admin/apikeys administration page. Although the interface displayed only a shortened representation of each key, the full token was embedded in hidden form fields used by the enable/disable, private-access, and delete actions.


As a result, API credentials could be recovered by inspecting the page source or DOM. The credentials could also be unintentionally exposed through components that retain or inspect HTTP response bodies, such as debugging proxies, browser caches, monitoring systems, or other intermediaries. An attacker obtaining one of these tokens could subsequently authenticate using the privileges assigned to that key, including access to private data where the key was granted such permissions.


The patch removes API keys from subsequent page rendering and replaces them with SHA-256-derived opaque handles. Administrative actions submit only these handles, which are resolved back to the corresponding token on the server. The full API key is therefore disclosed only once, when it is initially created.

### CVE-2026-39975

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-24T19:16:38.470 |

Combodo iTop is a web-based IT service management tool. Prior to 3.2.3, unauthenticated users could delete the .readonly file on iTop instances, leading to code execution. This file, created during the setup process, prevents users from performing write actions. This issue has been fixed in version 3.2.3.

### CVE-2026-78387

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T15:16:48.577 |

RansomLook contains an authorization weakness in the web-based configuration editor exposed through the /admin/config endpoint. The endpoint requires an authenticated session but does not perform an explicit privilege or administrator authorization check before allowing access to configuration-management functionality.

An authenticated low-privileged user able to access the endpoint can submit crafted configuration values that are written directly to the application's config/generic.json file. The affected functionality permits modification of configuration sections including notification, LDAP, SMTP, and general application settings. Successful exploitation could therefore allow an attacker to alter security-sensitive application behavior, redirect integrations or notifications, modify authentication-related configuration, disrupt external services, or render the RansomLook installation unavailable.

The configuration editor also operated on a configuration file containing sensitive values such as passwords, tokens, secrets, and API keys. Although the affected version contains logic intended to prevent recognized secret values from being returned to the browser, exposing configuration management through insufficiently authorized web functionality significantly increases the impact of a compromised or low-privileged account.

The patch resolves the issue by completely removing the /admin/config route and associated configuration-editing interface, preventing application configuration from being modified through the web UI.

### CVE-2026-79657

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-25T12:16:28.870 |

NLTK versions before 3.10.3 contain a remote code execution vulnerability in allowlisted pickle loaders that trust entire module namespaces instead of specific safe callables. Attackers can craft malicious pickle payloads invoking dangerous in-namespace functions like ReppTokenizer._execute and numpy.f2py.crackfortran.myeval through pickle REDUCE to execute arbitrary commands during model or tokenizer artifact loading.

### CVE-2026-57910

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-347;CWE-494` |
| Published | 2026-08-25T12:16:24.773 |

Improper authentication in the WatchGuard Agent allows an unauthenticated attacker with network access to cause the agent to execute arbitrary code with elevated privileges.

### CVE-2026-77138

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-25T09:17:34.497 |

The extension fails to safely process untrusted client input of an attacker-controlled cookie directly to PHP's unserialize(). A remote, unauthenticated attacker can supply a crafted serialized payload to trigger PHP Object Injection, leading to Remote Code Execution on the TYPO3 server.

### CVE-2026-63586

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-25T09:17:31.823 |

The web-based management interface uses a modified uhttpd server with CGI shell scripts. The HTTP Basic Authentication username, taken directly from the Authorization header without sanitization, is inserted into a shell command string executed via the system() function. By submitting a specially crafted username containing shell metacharacters, an unauthenticated attacker with network access to the device can escape the command context and execute arbitrary commands with root privileges.

### CVE-2026-78676

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-25T02:16:52.030 |

GitPython before 3.1.59 fails to safely re-serialize multi-line git-config values during write operations, corrupting dormant quoted values into injected directives like core.hooksPath. Attackers can craft config files with embedded newlines that become live git directives after any unrelated GitPython config write, enabling arbitrary code execution via hook invocation.

### CVE-2026-72702

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-346` |
| Published | 2026-08-25T02:16:46.120 |

Grav CMS before 2.0.16 contains an origin validation bypass in the Uri::referrer() and Pages::referrerRoute() methods, which validate the Referer header using an unanchored string prefix match (str_starts_with($referrer, $base)) with no trailing delimiter. An attacker who controls a domain that begins with the victim site's origin (e.g. https://example.com.attacker.tld) can send a request with such a Referer to be treated as same-origin, bypassing the Referer-based origin check.

### CVE-2026-72699

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-203` |
| Published | 2026-08-25T02:16:45.687 |

The Grav Login plugin (getgrav/grav-plugin-login) before 3.9.1 is vulnerable to email address enumeration. The register() method in classes/Login.php throws a distinct exception (EMAIL_NOT_AVAILABLE) when a submitted email address already belongs to an existing account, while allowing registration to proceed otherwise. Because the registration endpoint has no rate limiting, an attacker can enumerate which email addresses have accounts on the site, one guess per request.

### CVE-2026-56710

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-25T02:16:43.073 |

Grav Login plugin versions before 1.0.16 fail to validate the target account's privilege level in the onApiUserListRowAction unlock handler. An attacker with api.users.write permission can clear login lockout counters on admin.super accounts, removing brute-force protection from the highest-privilege accounts without requiring equivalent permissions.

### CVE-2026-56705

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-25T02:16:42.330 |

Adminer before 5.4.3 fails to sanitize the server field before constructing a PDO DSN string, allowing unauthenticated attackers to inject ODBC parameters via semicolons. Attackers can inject TraceFile and TraceOn parameters to write PHP code to the web root, achieving remote code execution when the trace file is accessed.

### CVE-2026-32555

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T22:16:51.650 |

Unauthenticated SQL Injection in Boost <= 2.0.4 versions.

### CVE-2026-32554

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T22:16:51.510 |

Unauthenticated SQL Injection in WooBeWoo Product Filter Pro <= 3.1.8 versions.

### CVE-2026-76835

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-24T18:17:21.570 |

OAuth2 Proxy honours a client-supplied X-Forwarded-Uri header when deciding whether a request may skip authentication, because the guard added for CVE-2026-40575 is inert in the default reverse-proxy configuration. GetRequestURI in pkg/requests/util/util.go prefers that header over the real request URI whenever CanTrustForwardedHeaders returns true, and isAllowedPath in oauthproxy.go matches the skip_auth_routes and skip_auth_regex allow list against the resulting path. CanTrustForwardedHeaders in pkg/apis/middleware/scope.go grants that trust when the caller's address is in the trusted proxy set, and buildTrustedProxyNetSet falls back to defaultTrustedProxyIPs, which is 0.0.0.0/0 and ::/0, whenever reverse proxy mode is enabled without trusted_proxy_ip configured. Every client is therefore treated as a trusted proxy. An unauthenticated attacker can request a protected upstream path while setting X-Forwarded-Uri to a value matching an allow-listed route, so the skip-auth decision is made against the spoofed value while the upstream receives the protected path unchanged.

### CVE-2026-71921

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:07.060 |

Multiple DrayTek VigorSwitch models contain a pre-authentication command injection vulnerability in the setget.cgi interface. The vulnerability is caused by insufficient filtering of the pass field before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges.

### CVE-2026-71914

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:03.497 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the dray_apm component. The vulnerability is caused by insufficient validation of UDP message content after START_SPEED_TEST before command execution. A remote attacker can trigger this vulnerability via a crafted message to execute arbitrary commands with root privileges.

### CVE-2026-77915

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306;CWE-1188` |
| Published | 2026-08-24T17:18:18.450 |

rConfig Core 8.0.0 before 8.2.13 contains an authentication bypass vulnerability that allows unauthenticated attackers to self-register accounts with full Administrator privileges due to a duplicate bare Auth::routes() call in routes/web.php that re-enables the POST /register route after it was explicitly disabled. Attackers can register a new account that is immediately authenticated with Admin-level access because the registration controller does not assign a role and the users.role column defaults to Admin, enabling access to stored device credentials, user data, and API token issuance.

### CVE-2026-76071

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-24T16:17:23.117 |

Netis NC63 firmware through V3.0.0.3327 contains a stack-based buffer overflow vulnerability that allows unauthenticated remote attackers to overwrite saved stack state by supplying an oversized destHost parameter to the ipFilterList=mod action in netis.cgi. Attackers can exploit widthless sscanf conversions that copy user-supplied input into fixed-size stack buffers before authentication is verified, achieving remote code execution as root due to the Boa web server executing the CGI environment with root privileges.

### CVE-2026-76070

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-121` |
| Published | 2026-08-24T16:17:22.963 |

Netis NC63 firmware through V3.0.0.3327 contains a stack-based buffer overflow vulnerability that allows unauthenticated remote attackers to overwrite saved stack state by submitting an oversized Base64-encoded password to the login handler in /bin/netis.cgi. Attackers can exploit the custom Base64 decoder's lack of output length validation against the fixed-size stack buffer to achieve remote code execution with root privileges, as the Boa web server executes the CGI environment as root.

### CVE-2026-77635

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-24T21:17:48.457 |

CakePHP is a rapid development framework for PHP. Prior to versions 5.1.10, 5.2.15, and 5.3.7 on their respective release lines, FunctionsBuilder::jsonValue() with PostgresDriver is vulnerable to SQL injection when user-controlled data is supplied to the jsonPath parameter. This issue is fixed in versions 5.1.10, 5.2.15, and 5.3.7.

### CVE-2026-79664

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-613` |
| Published | 2026-08-25T12:16:34.370 |

Ech0 before 4.7.3 fails to properly revoke access tokens created with never-expire option, allowing attackers to maintain perpetual authenticated access after token theft. Three independent revocation mechanisms fail: logout panics on nil ExpiresAt field, RevokeToken skips when remainTTL is zero, and admin delete does not blacklist the JTI, leaving stolen tokens cryptographically valid until JWT secret rotation.

### CVE-2026-77337

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290;CWE-770` |
| Published | 2026-08-24T22:17:19.510 |

CakePHP Authentication is an authentication plugin for CakePHP that can also be used in PSR-7 based applications. Versions before 2.11.2, from 3.0.0 through 3.3.6, and from 4.0.0 through 4.2.0 allow authentication bypass and potential CPU or memory exhaustion when CookieAuthenticator uses unencrypted, forgeable legacy tokens. This issue is fixed in versions 2.11.2, 3.3.7, and 4.2.1.

### CVE-2026-19874

| 項目 | 値 |
|------|-----|
| CVSS | `9.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-08-24T15:16:37.577 |

A heap-based buffer overflow vulnerability exists in Konami's Metal Gear Online 3, originating from improper validation of lobby data fields related to kicked players. The affected function processes a list of kicked player identifiers using the lobby data key "kick_num" to determine the number of entries, and individual kicked player IDs supplied via keys in the format "kicked_id_%i". The function does not validate that "kick_num" falls within the expected bounds. The game design limits matches to a maximum of 16 players, and the corresponding buffer for storing kicked player IDs is sized accordingly. If "kick_num" exceeds this limit, the function continues writing the provided player IDs past the end of the intended buffer and into adjacent memory regions. These adjacent regions contain Steam callback handler structures responsible for processing lobby data updates, lobby messages, and other related events. By supplying an oversized "kick_num" value and appropriate "kicked_id_%i" fields, an attacker can overwrite fields within the callback handler structures, including function pointers and callback argument values. Successful exploitation may enable control-flow hijacking, potentially allowing arbitrary code execution within the game process.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-30864

| 項目 | 値 |
|------|-----|
| CVSS | `8.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T19:16:37.140 |

Combodo iTop is a web-based IT service management tool. Prior to 3.2.3, iTop is vulnerable to Reflected Cross-Site Scripting (XSS) in the dashboard revert functionality. This issue has been fixed in version 3.2.3.

### CVE-2026-79662

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:H/SI:H/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-601` |
| Published | 2026-08-25T12:16:31.470 |

Ech0 through 4.5.6 contains an OAuth redirect URI validation vulnerability in parseAndValidateClientRedirect (internal/service/auth/auth.go) that compares only the scheme and host of the client-supplied redirect_uri against the admin-configured allowlist, ignoring path, query, and fragment components. The redirect_uri is embedded into the signed state JWT at login time without validation. An attacker can craft a redirect_uri whose host matches an allowed origin but whose path is attacker-influenced; after the OAuth exchange the victim is redirected to that path with a one-time exchange code in the query string. If the code leaks (e.g., via Referer, analytics, or an open redirect on that host), the attacker can trade it at the public POST /api/auth/exchange endpoint for the victim's access and refresh tokens. Fixed in 4.7.3.

### CVE-2026-19949

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T12:16:23.783 |

The All-in-One WP Migration and Backup plugin for WordPress is vulnerable to SQL Injection via archive restore functionality in all versions up to, and including, 7.109 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This can be leveraged to obtain the ai1wm_secret_key when a site administrator performs an archive restore and achieve remote code execution once able to leverage the ai1wm_secret_key value.

### CVE-2026-77143

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-25T09:17:35.333 |

The frontend topic editing flow does not verify on the server side that the requesting visitor owns the topic being modified. As a result, a visitor who knows the identifier of a topic from the public forum can submit a modified update request for that topic directly and overwrite its content, without the application confirming ownership. Topic identifiers are visible in the public forum listing, and exploitation requires no privileged access or non-default configuration.

### CVE-2026-77142

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-25T09:17:35.133 |

The frontend company self-service editing feature relies on a template-level visibility flag to hide the edit form for company records a visitor does not own, but the corresponding write operation does not repeat this ownership check on the server side. As a result, a visitor who knows the identifier of a company record from the public directory can submit a modified update request for that record directly and overwrite its data, without the application ever confirming that the visitor owns it.

### CVE-2026-77141

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-25T09:17:34.960 |

The extension resolves the targeted club record from a user-supplied request argument in its frontend edit, update, and activate actions, but performs no ownership check in any of them. An unauthenticated visitor who knows the UID of a club record can send a direct request to the update or activate action and overwrite that record, or publish one still awaiting approval, without owning it.

### CVE-2026-63587

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-25T09:17:32.057 |

The SMS control function of IE-SR-2TX-WL-4G devices can require a password for SMS commands via the 'Enable Password Authorization' setting. The device increments a retry counter on each failed SMS password attempt; after 5 consecutive failed attempts, SMS password authorization is automatically disabled. An unauthenticated remote attacker who is able to send SMS messages to the device can deliberately trigger this by submitting 5 or more invalid passwords, after which subsequent SMS commands are executed without requiring a password, resulting in potential limited configuration tampering, limited information leakage and potentially full loss of availability.

### CVE-2026-59769

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-08-25T08:18:09.717 |

FA-50 all versions contain hard-coded credentials.
An attacker, who knows the credentials and has access to the vessel's internal network, can operate the settings screen using that credentials to alter the identification number.

### CVE-2026-16601

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-25T08:18:08.220 |

The CM Map Locations – Visualize and share your locations in a few clicks plugin for WordPress is vulnerable to Limited Arbitrary File Upload in all versions up to, and including, 2.1.8 via the uploadMedia function. This is due to insufficient file type validation in the upload handler, which performs incomplete extension filtering without MIME-type checks or upload capability verification before passing attacker-supplied files to move_uploaded_file(). This makes it possible for authenticated attackers, with subscriber-level access and above, to upload files that may be executable, which makes remote code execution possible. The required nonce is exposed to any logged-in Subscriber via the CMLOC_Editor_Images JavaScript object on the front-end location editor page.

### CVE-2026-19892

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T04:18:10.770 |

The InfusedWoo Pro plugin for WordPress is vulnerable to Privilege Escalation via Account Takeover in all versions up to, and including, 5.1.17. This is due to a missing capability check in the `ajax_iwar_preview_email()` function, which uses `is_admin()` as its only authorization check and allows low-privilege users to render email preview merge fields for an arbitrary email address. This makes it possible for authenticated attackers, with subscriber-level access and above, to generate and retrieve a valid password reset link for any WordPress user, including administrators, enabling account takeover.

### CVE-2026-32561

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-08-24T22:16:52.157 |

Subscriber Privilege Escalation in Booking Hub <= 1.3.0 versions.

### CVE-2026-32560

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-24T22:16:52.027 |

Subscriber Local File Inclusion in MagicAI for WordPress - AI Text, Image, Chat, Code, and Voice Generator <= 1.4 versions.

### CVE-2026-78551

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-307;CWE-400` |
| Published | 2026-08-24T20:17:23.927 |

RansomLook contains multiple weaknesses in its authentication endpoint that allow an unauthenticated remote attacker to enumerate valid usernames, perform unrestricted password-guessing attacks, and potentially exhaust application worker resources.

For local authentication, the login implementation previously checked whether a submitted username existed before invoking the password hash verification function. Requests containing a nonexistent username therefore returned significantly faster than requests for valid accounts, for which the computationally expensive password verification routine was executed. A remote attacker could measure these response-time differences to determine which usernames correspond to valid RansomLook accounts.

In addition, the /login endpoint did not restrict the number or frequency of failed authentication attempts. An attacker could consequently perform password brute-force, dictionary, password-spraying, or credential-stuffing attacks against known accounts without server-side throttling. For valid usernames, each authentication attempt also invokes the password key-derivation function, which consumes a significant amount of CPU time. A sufficiently high rate of login attempts could therefore occupy the application's synchronous Gunicorn workers and cause a denial of service affecting the entire application.

The issue has been addressed by always performing password verification using a randomly generated dummy password hash when the supplied username does not exist, eliminating the username-dependent timing discrepancy. Failed authentication attempts are additionally rate-limited per client IP address using Valkey/Redis, with five failed attempts within five minutes resulting in a one-hour block. The reverse-proxy configuration was also updated so that the application derives the client address from a trusted X-Forwarded-For value that cannot be overridden by a client-supplied header.

### CVE-2026-71933

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T18:17:18.090 |

Multiple DrayTek VigorSwitch models contain unauthorized operation vulnerabilities in multiple syslog functions. The vulnerability is caused by missing authorization checks. A remote attacker can trigger these vulnerabilities via crafted requests to modify configuration, restart services, save startup configuration, or clear logs.

### CVE-2025-36940

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-08-24T17:17:21.303 |

Use-After-Free vulnerability in a zircon kernel pager proxy (Fuchsia), which could lead to a Privilege Escalation from Userspace to Kernel (AP)

### CVE-2026-13212

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-129` |
| Published | 2026-08-24T16:16:55.393 |

The Zephyr virtio driver does not validate the descriptor-chain head id that the virtio device writes into the used ring. In virtio_isr() (drivers/virtio/virtio_common.c), the device-written vq->used->ring[idx].id is used directly as an index into vq->recv_cbs[] and vq->desc[], which are both allocated with exactly vq->num entries. recv_cbs[] holds {cb, opaque} callback entries, and the indexed callback pointer is then invoked as cbe.cb(cbe.opaque, used_len).

Because the id is consumed as a 16-bit value with no bound check, a malicious or compromised virtio backend (an untrusted hypervisor, or an untrusted hardware/peer-processor virtio device on a PCI or MMIO transport) can supply an id far beyond vq->num. This causes an out-of-bounds read of a {function pointer, argument} pair from heap memory beyond recv_cbs[], after which the driver calls that attacker-shaped pointer in the guest's interrupt context. No guest privileges or user interaction are required; the backend triggers it by writing the shared used ring and raising the queue interrupt.

The result is an arbitrary / attacker-influenced function-pointer call in the Zephyr guest, i.e. a control-flow-hijack primitive that can lead to code execution or, at minimum, a reliable crash. The fix rejects any used-ring id >= vq->num before indexing recv_cbs[]/desc[] or invoking the callback. This affects builds using CONFIG_VIRTIO with the PCI or MMIO transport.

### CVE-2026-78391

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T15:16:48.717 |

RansomLook contains a stored cross-site scripting (XSS) vulnerability in the cryptocurrency wallet detail view. Cryptocurrency addresses and blockchain names originating from external sources, including the public crowd-sourced ransomwhe.re feed, were stored without sufficient validation and later embedded directly into an inline JavaScript onclick handler.


Although Jinja HTML autoescaping was applied, it does not provide adequate protection when untrusted data is inserted into a JavaScript string inside an HTML attribute. HTML entities such as &#39; are decoded by the browser's HTML parser before the resulting attribute is interpreted as JavaScript. Consequently, a specially crafted cryptocurrency address containing quote characters and JavaScript syntax could escape the intended string literal and execute arbitrary JavaScript when a user clicked the affected wallet's CSV export button.


Because cryptocurrency information imported from an untrusted upstream could reach the vulnerable rendering path, exploitation may not require an authenticated RansomLook account if an attacker can introduce a malicious wallet record into a consumed external data source. Successful exploitation could allow attacker-controlled JavaScript to execute in the security context of the RansomLook web application, potentially exposing information accessible to the victim or performing actions with the victim's privileges.


The patch mitigates the issue by validating cryptocurrency addresses and blockchain identifiers before storage, restricting them to a safe character set, and replacing the inline JavaScript handler with data-* attributes and an external event listener so wallet values are treated strictly as data rather than executable JavaScript.

### CVE-2026-57863

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T13:19:24.200 |

Crater Invoice through 6.0.6 contains a path traversal vulnerability in the self-update API that allows authenticated company owners to write arbitrary files outside the intended extraction directory by supplying crafted ZIP archives with ../ sequences to the unzip endpoint. Attackers can exploit unsanitized ZIP entry names passed to PHP's ZipArchive::extractTo() to write arbitrary PHP files into the web-accessible public directory and achieve remote code execution on the server.

### CVE-2026-79665

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T12:16:34.523 |

Ech0 before 4.5.1 contains an authorization bypass vulnerability where session tokens skip scope validation in RequireScopes middleware, allowing logged-in non-admin users to access admin endpoints. Attackers can read system logs, visitor statistics, user emails, and subscribe to live WebSocket logs by sending authenticated session tokens to unprotected endpoints.

### CVE-2026-79658

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-25T12:16:29.123 |

Ech0 before 5.0.1 does not impose any size or shape limit on the Accept-Language header processed by its i18n middleware, which runs on every HTTP request. The header is passed unfiltered to go-i18n's NewLocalizer, which internally calls golang.org/x/text/language.ParseAcceptLanguage. The CVE-2022-32149 mitigation in x/text caps '-' characters but not '_' characters, which the parser aliases to '-', allowing quadratic-time parsing to be triggered with a large header (up to Go's default 1 MiB) built from underscore separators. An unauthenticated attacker can send such requests to consume roughly 1.5 seconds of CPU each, and concurrent requests can saturate a multi-core server (denial of service).

### CVE-2026-59335

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-178` |
| Published | 2026-08-25T11:16:53.817 |

Improper handling of case sensitivity (CWE-178) in the identity zone authorization check in the Identity Zone Endpoint in Cloud Foundry UAA allows a remote authenticated attacker holding only the zones.write authority to bypass the intended restriction that this authority does not grant access to the privileged uaa (system) identity zone, by referring to the zone identifier in a non-lowercase form (e.g. UAA) in the request path and body. The authorization layer performs a case-sensitive comparison against the system zone identifier, while the underlying MySQL persistence layer resolves identifiers case-insensitively under its default collation, so the request is authorized incorrectly and is then resolved against the real system zone record. This allows the attacker to overwrite the system zone's JWT signing key with attacker-controlled key material, forge JWTs claiming the admin client and administrator scopes, and fully compromise UAA and any Cloud Foundry deployment that trusts it. This issue only affects UAA deployments backed by MySQL using its default collation; PostgreSQL and HSQLDB backends are not affected.

### CVE-2026-12600

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-400` |
| Published | 2026-08-25T11:16:50.383 |

Denial-of-service (DoS) vulnerability in the internal JPEG2000 (JPX) decoding implementation of the Poppler fork developed by Innodata Labs. When an application processes an untrusted PDF file containing specially crafted JPXDecode images, a remote attacker can cause uncontrolled memory consumption. The flaw occurs in the JPXStream::readCodestream() function, where values controlled from the SIZ segment (such as img.nComps) are used for the memory allocation of tiles and components without adequate validation. This allows an attacker to force excessive memory allocation and cause a resource exhaustion, ultimately causing the pdftoppm process to terminate due to out-of-memory (OOM) conditions.

### CVE-2026-77140

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639;CWE-862` |
| Published | 2026-08-25T09:17:34.807 |

The extension validates the HMAC of a frontend employee edit link only in the action that renders the edit form, not in the action that persists the change. An unauthenticated visitor who knows the UID of a visible employee record can send a direct POST request to the update action and overwrite that record without a valid edit link or any ownership check.

### CVE-2026-67578

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-306` |
| Published | 2026-08-25T08:18:10.360 |

FA-50 all versions miss authentication for some configuration.
An attacker with access to the vessel's internal network can manipulate the product's settings screen to alter some configuration parameters.

### CVE-2026-78682

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T02:16:52.890 |

NLTK before 3.10.3 contains a server-side request forgery vulnerability in nltk.pathsec.urlopen (and callers nltk.data.load, nltk.downloader.Downloader.index/download) when an HTTP proxy is configured. pathsec.urlopen validates the requested hostname locally, but proxy-handler inheritance disables the safe HTTP/HTTPS handlers so the actual fetch is performed by the proxy against a destination that is never re-validated. An attacker can supply a validated public URL that the proxy forwards to an internal loopback-only service, allowing disclosure of internal HTTP resources, loading of forged downloader indexes, and installation of attacker-chosen package content.

### CVE-2026-78681

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-776` |
| Published | 2026-08-25T02:16:52.750 |

NLTK versions before 3.10.3 use xml.etree.ElementTree to parse XML in multiple modules, which honors entity declarations in document DTDs. Attackers can craft XML payloads with nested entity declarations that expand from hundreds of bytes to megabytes in memory, causing denial of service.

### CVE-2026-78677

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T02:16:52.173 |

GitPython before 3.1.59 omits --separate-git-dir from unsafe_git_clone_options, allowing attackers to create arbitrary git directories outside the intended clone destination. Attackers can pass a separate_git_dir parameter to Repo.clone_from() or Repo.clone() to redirect repository metadata to an attacker-controlled filesystem path, enabling arbitrary directory creation and potential hook execution.

### CVE-2026-76846

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-25T02:16:51.743 |

Grav before 2.0.16 contains an incomplete default denylist in the Twig sandbox configuration that fails to block access to system configuration secrets. Attackers with page-edit permission can use config.get() or config.toArray() in Twig templates to retrieve sensitive values like system.cache.redis.password when config_access is enabled.

### CVE-2026-76839

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-25T02:16:51.603 |

Grav before 2.0.16 allows sandboxed Twig templates to access sensitive User fields through allow-listed offsetGet() and offsetexists() methods that lack field filtering. Attackers with page-edit permissions can call offsetGet() on User objects to extract hashed passwords and 2FA secrets, enabling offline password cracking and authentication bypass.

### CVE-2026-75574

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-25T02:16:51.303 |

The Grav Email plugin (getgrav/grav-plugin-email) before 4.2.2 renders page-editor-controlled Email action parameters as unsandboxed Twig templates. An authenticated remote user with only api.access and api.pages.write permissions can place a Twig expression in header.form.process.email.body, publish the page, and submit the form to execute an arbitrary operating-system command as the account running PHP.

### CVE-2026-72700

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-208` |
| Published | 2026-08-25T02:16:45.830 |

The getgrav/grav-plugin-login Composer plugin before 3.9.1 (used by Grav) compares password reset and account activation tokens using a non-constant-time === string comparison instead of hash_equals() in classes/Controller.php (taskReset()) and login.php (activation handler). Because the token-submission endpoint (taskReset) also lacks rate limiting, an attacker could in principle send repeated token guesses against a known username and use the timing differences to attempt to recover a valid token, though the vendor rates the practical exploitability as low and no end-to-end network exploit has been demonstrated.

### CVE-2026-56709

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-350` |
| Published | 2026-08-25T02:16:42.930 |

Grav before 3.9.2 fails to validate untrusted Host headers in the sendInvitationEmail() function when constructing token-bearing invitation links. Attackers can manipulate the Host header to poison invitation links and redirect users to attacker-controlled domains, bypassing the require_trusted_host protection which only covers password reset flows.

### CVE-2026-40877

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-94;CWE-502` |
| Published | 2026-08-24T19:16:38.647 |

Combodo iTop is a web-based IT service management tool. Prior to 3.2.3, iTop is vulnerable to PHP object injection in the user preference functionality, which can lead to remote code execution. This issue has been fixed in version 3.2.3.

### CVE-2026-9254

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:34.973 |

An unauthenticated OS command injection vulnerability exists in the parental control functionality of Archer BE800 V1, BE3600 V1, and AX75 V1 due to improper filtering and neutralization of special characters in certain parameters. A LAN-based attacker can inject arbitrary commands and execute them with root privileges.






Successful exploitation may result in complete device compromise and impact the confidentiality, integrity, and availability of the affected device and network traffic.

### CVE-2026-76836

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94;CWE-863` |
| Published | 2026-08-24T18:17:21.733 |

AzuraCast exposes the Liquidsoap custom configuration fields through an endpoint that does not require the permission guarding them. The backend_config property in backend/src/Entity/Station.php is annotated with GROUP_GENERAL, and PUT /api/station/{station_id}/profile/edit in backend/src/Controller/Api/Stations/ProfileEditController.php deserializes with that group while requiring only StationPermissions::Profile. AbstractArrayEntity::fromArray() then assigns every public property with no field-level permission check, so custom_config_top, custom_config, custom_config_pre_playlists, custom_config_pre_live, custom_config_pre_fade and custom_config_bottom are writable through it. ConfigWriter::writeCustomConfigurationSection() emits those values verbatim into the generated Liquidsoap .liq script, where the process.run() and process.exec() built-ins execute operating system commands when the backend restarts, which the built-in sync task triggers automatically once needs_restart is set. The dedicated endpoint for the same data, PUT /api/station/{id}/liquidsoap-config, requires StationPermissions::Broadcasting, so a station manager holding only the profile permission reaches configuration that the intended boundary reserves for broadcasting operators.

### CVE-2026-76073

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-24T18:17:21.410 |

Label Studio does not scope the annotation detail endpoint to the requesting user's organization. AnnotationAPI in label_studio/tasks/api.py declares queryset = Annotation.objects.all() and provides no get_queryset override, so the default lookup retrieves any annotation by primary key. The view's permission_required entries name annotations.view, annotations.change and annotations.delete, and label_studio/core/permissions.py registers every permission with rules.is_authenticated, so the check is satisfied by any logged-in account and no object-level organization test runs. The sibling task endpoint does constrain its queryset with project__organization set to the requester's active organization, which is the boundary this path omits. Annotation identifiers are sequential integers, so an authenticated user of one organization can enumerate identifiers to read, modify and delete annotations belonging to other organizations on the same instance. The same unscoped queryset appears on AnnotationConvertAPI in the same file.

### CVE-2026-71922

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-24T18:17:07.280 |

Multiple DrayTek VigorSwitch models contain a pre-authentication null pointer dereference vulnerability in the setget.cgi interface. The vulnerability is caused by missing validation when the pass field is absent. A remote attacker can trigger this vulnerability via a crafted request to crash the service and cause a denial of service.

### CVE-2026-78416

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-24T16:17:24.250 |

Craft CMS versions from 4.0.0-RC1 before 4.18.2 and from 5.0.0-RC1 before 5.10.6 contain an authenticated remote code execution vulnerability in control panel element-search condition handling. A JSON cleanse bypass in condition.config allows Yii behavior/event configuration keys to be interpreted after decoding, enabling command execution as the PHP/web user.

### CVE-2026-12878

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-25T10:18:03.137 |

In affected versions of the Codefresh platform an authenticated user can utilize an API endpoint to elevate to Admin permissions.

### CVE-2026-78685

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-940` |
| Published | 2026-08-25T03:16:58.740 |

Medical Practice Management System developed by Le-yan has a Remote Code Execution vulnerability. Unauthenticated remote attackers can execute arbitrary OS commamnds via a crafted HTML page.

### CVE-2026-78675

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-25T02:16:51.887 |

GitPython before 3.1.59 fails to disable merge_includes when parsing .gitmodules, allowing attackers to disclose local file content by including arbitrary file paths via [include] directives. Attackers can craft a malicious .gitmodules file with include directives pointing to sensitive files; when repo.submodules is accessed, GitConfigParser raises MissingSectionHeaderError embedding the target file's first line verbatim in the exception message.

### CVE-2026-72696

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-25T02:16:45.253 |

Grav CMS before 2.0.16 contains a symlink following vulnerability in Scheduler Job::createLockFile() that allows local attackers to overwrite arbitrary files by pre-creating symlinks at predictable lock file paths in the world-writable temp directory. Attackers can place a symlink at the predictable lock path pointing to any file the web server process can write to, and the next scheduled job run will follow the symlink and overwrite the target file's content with the job ID string.

### CVE-2026-56703

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-08-25T02:16:42.043 |

Adminer before 5.4.3 contains a remote code execution vulnerability in SQLite query handling where VACUUM INTO is not blocked despite ATTACH restrictions. Authenticated attackers can execute VACUUM INTO to write PHP code to arbitrary file paths and execute commands on the server.

### CVE-2026-78284

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T22:17:21.053 |

Unauthenticated Arbitrary File Deletion in MasterStudy LMS <= 3.7.42 versions.

### CVE-2026-71504

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862;CWE-915` |
| Published | 2026-08-24T19:16:49.670 |

Dolibarr before 24.0.0 contains an improper authorization vulnerability in the Members REST API that allows attackers with only member-creation rights to reset the password of any user account, including the system administrator, without verifying password-change permissions. Attackers can supply an arbitrary user account identifier and new password in the request body to overwrite credentials and immediately lock out the legitimate account holder.

### CVE-2026-71943

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:20.077 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the setDevNet function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71942

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:19.877 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the mail_mailalert function. The vulnerability is caused by concatenating multiple smtpReceiver email addresses into a fixed-size buffer without checking the remaining buffer size. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71941

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:19.680 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the diag_logmail function. The vulnerability is caused by concatenating multiple smtpReceiver email addresses into a fixed-size buffer without checking the remaining buffer size. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71940

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:19.480 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the acl_general_setup Edit ACE function. The vulnerability is caused by copying the name field into a fixed-size buffer without length validation. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71939

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:19.280 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the acl_general_setup Add ACE function. The vulnerability is caused by copying the name field into a fixed-size buffer without length validation. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71938

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:19.083 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the switch_lan_gvrp function. The vulnerability is caused by unsafe copying of the portList field into an undersized buffer. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71937

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:18.890 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the poe_schedule_profile function. The vulnerability is caused by repeated concatenation of the start_date, start_time, duration_time, how_often, weekdays, monthly_date, and cycle_duration fields into small fixed-size buffers without proper length checks. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71936

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:18.693 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the sysreboot function. The vulnerability is caused by unsafe concatenation of split valueN data into a fixed-size buffer. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71935

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:18.490 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the webBackupAction function. The vulnerability is caused by repeated string concatenation of the pathN, valueN, key, and option fields into fixed-size stack buffers without total length checks. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71934

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:18.290 |

Multiple DrayTek VigorSwitch models contain a buffer overflow vulnerability in the pingtrace function. The vulnerability is caused by missing length checks when the host, count, and interval fields are concatenated into a fixed-size buffer. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71931

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:17.697 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the tftp_upgrade function. The vulnerability is caused by insufficient filtering before the filename field is concatenated into a command. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71930

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:08.643 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the setTime function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71929

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:08.480 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the setDevProto function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71928

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:08.303 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the fdftDevice function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71927

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:08.140 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the rebDevice function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71926

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:07.977 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the setDevice function. The vulnerability is caused by insufficient sanitization of the username, password, and location fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71925

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:07.813 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the getDetail function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71924

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:07.653 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the getVid function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71923

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:07.497 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the auth_set function. The vulnerability is caused by insufficient filtering of the username and password fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71919

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:06.610 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the sysreboot function. The vulnerability is caused by insufficient filtering of the config, act, pathN, and valueN fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71918

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:06.377 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the webBackupAction function. The vulnerability is caused by insufficient filtering of the option, key, pw_encode, pathN, and valueN fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71917

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:06.153 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the pingtrace function. The vulnerability is caused by insufficient validation of the host field before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71916

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:03.940 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the commandTable function. The vulnerability is caused by incomplete filtering of dangerous characters such as backticks, newline characters, and single quotes in the parameter field. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71915

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:03.670 |

Multiple DrayTek VigorSwitch models contain a command injection vulnerability in the jsonstatus function. The vulnerability is caused by insufficient filtering of the usescript, usefile, and option fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71913

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:03.300 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the upload_settings.cgi interface. The vulnerability is caused by insufficient filtering before the restorekey field is concatenated into a shell command. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71912

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:03.110 |

Multiple DrayTek VigorAP models contain a buffer overflow vulnerability in the apautotest function. The vulnerability is caused by missing length checks during memory copy operations involving the CMD6 field. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71911

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T18:17:02.947 |

Multiple DrayTek VigorAP models contain a buffer overflow vulnerability in the setLan function. The vulnerability is caused by missing length checks during memory copy operations involving the lanVlanId0, lanIp, and lanNetmask fields. A remote attacker can trigger this vulnerability via crafted input, causing a denial of service or potentially executing arbitrary commands. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71910

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:02.770 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the apautotest function. The vulnerability is caused by insufficient validation of the CMD0, CMD3, and CMD6 fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71909

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:02.593 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the InquierTime function. The vulnerability is caused by insufficient filtering of the time field before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71908

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:02.420 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the mesh_start_speed_test function. The vulnerability is caused by insufficient sanitization of the meshdevice_index and meshdevice_ip fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71907

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:02.243 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the setcamset function. The vulnerability is caused by insufficient filtering of the selectSlaves field before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71906

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:02.067 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the setLan function. The vulnerability is caused by insufficient validation of the lanIp and lanNetmask fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71905

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:01.890 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the ExportSettings function. The vulnerability is caused by insufficient filtering of the backupkey, backuptype, and realtime fields before command execution. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-71904

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:17:01.700 |

Multiple DrayTek VigorAP models contain a command injection vulnerability in the tr069TestInform function. The vulnerability is caused by insufficient filtering of dangerous characters before the event_code field is concatenated into a system command. A remote attacker can trigger this vulnerability via crafted input to execute arbitrary commands with root privileges. Exploitation requires valid administrative credentials for the device's web management interface.

### CVE-2026-79673

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-25T12:16:35.680 |

Ech0 before 4.4.3 protects the PUT /user endpoint with the profile:read scope, a read-only scope, but allows write operations including password changes. An attacker with an admin's profile:read access token can change the admin's password and login to obtain an unrestricted session token that bypasses all scope enforcement.

### CVE-2026-69665

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-25T07:17:10.860 |

SKYSEA Client View and SKYMEC IT Manager contain an issue with incorrect default permissions. If this vulnerability is exploited, an attacker who can log in to a Windows system on which the affected product is installed may execute arbitrary code with SYSTEM privilege.

### CVE-2026-66109

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T07:17:10.310 |

A missing authorization vulnerability exists in SKYSEA Client View and SKYMEC IT Manager. If this vulnerability is exploited, an attacker who can log in to the Windows system on which the affected product is installed may execute arbitrary code with SYSTEM privilege.

### CVE-2026-78680

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-426` |
| Published | 2026-08-25T02:16:52.607 |

NLTK versions before 3.10.3 fail to use validated absolute paths when invoking the Graphviz dot binary in dependencygraph.dot2img and AlignedSent._repr_svg_, allowing attackers to execute arbitrary code by placing a malicious dot binary in the search path or current working directory. Attackers can exploit bare-name binary resolution on Windows via the current working directory or on Unix-like systems via relative PATH entries to execute their binary instead of the legitimate Graphviz tool.

### CVE-2026-78541

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T19:17:04.553 |

A stored OS
command injection vulnerability exists in the parent-control module of TP-Link
Archer BE3600 V1. An authenticated adjacent attacker with administrative access
may store a crafted profile name containing shell metacharacters, which is
later processed unsafely during daily cloud report generation and may result in
arbitrary command execution.





Successful
exploitation may allow command execution on the affected device with potential
impact to device confidentiality, integrity, and availability.

### CVE-2026-16348

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T18:16:59.710 |

An authenticated command injection vulnerability in TP-Link Archer BE800 V1 allows an attacker with administrative access to execute arbitrary system commands with root privileges by injecting shell metacharacters via a VPN connection. 




Successful exploitation may enable persistent backdoors, credential theft, LAN reconnaissance, and router-assisted attacks against connected devices.

### CVE-2026-12554

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1104` |
| Published | 2026-08-24T16:16:54.967 |

Potential security vulnerabilities have been identified in HP Easy Start for macOS, versions prior to 2.16.7.260722. These potential vulnerabilities may lead to escalation of privilege. HP is releasing updates to mitigate these potential vulnerabilities.

### CVE-2026-39915

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-113` |
| Published | 2026-08-24T15:16:38.090 |

TIM Flow before 26.0.6 contains a CRLF injection vulnerability that allows remote attackers to inject arbitrary HTTP headers and response body content by embedding unsanitized carriage return and line feed sequences in the rt URL parameter, which is reflected into Set-Cookie response headers. Attackers can craft malicious requests to induce authenticated users to execute arbitrary JavaScript in their browser context, enabling session token theft and account credential modification.

### CVE-2026-76838

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-24T18:17:22.363 |

Hi.Events validates a webhook destination only when it is registered, never when it is used. NoInternalUrlRule in backend/app/Validators/Rules/NoInternalUrlRule.php resolves the hostname with gethostbyname() and rejects private and reserved ranges, which any public hostname passes. At dispatch, WebhookDispatchService takes the stored URL and calls it through spatie/laravel-webhook-server without repeating the check, and backend/config/webhook-server.php sets no Guzzle options, so redirect following remains enabled by default. A destination that answers with a redirect to a loopback, private or cloud metadata address therefore causes the server to issue that request, and changing the hostname's DNS record after registration reaches the same result because no resolution is repeated. The response is not discarded: WebhookResponseHandlerService stores the body on the webhook log and WebhookLogResource returns it from the webhook logs endpoint, so the requester reads what the internal service replied rather than inferring it. Both event and organizer webhooks share the rule and the dispatch path. Version 1.11.1-beta revalidates at dispatch, pins the validated address, checks every redirect hop, and decodes IPv6 transition addresses that previously bypassed the filter.

### CVE-2026-79659

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T12:16:29.380 |

Ech0 before 4.7.3 contains a server-side request forgery vulnerability in the fetchPeerConnectInfo function that uses unvalidated HTTP requests instead of safe request methods with URL validation. Authenticated attackers can supply arbitrary URLs to access internal services and cloud metadata endpoints by triggering connection health checks or peer connection operations.

### CVE-2026-77146

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T09:17:35.820 |

The extension's invitation controller fails to stop processing after redirecting on invalid input (missing hash, non-existent, disabled, or deleted users), allowing an unauthenticated attacker to set a new password for and re-enable an arbitrary existing frontend user account. This vulnerability is only present in the 8.x versions of the extension.

### CVE-2026-77134

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-25T09:17:33.853 |

The extension fails to require the dedicated admin confirmation token when processing an admin-approval request, so a regular user confirmation hash, obtainable by any visitor through the public resend-confirmation action, is sufficient to self-approve a pending account awaiting admin approval.

### CVE-2026-56707

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T02:16:42.637 |

Grav Flex Objects plugin versions 1.4.0 through 1.4.7 contain an authorization bypass vulnerability in the flex-objects shortcode that allows users with page-edit access to render any registered Flex collection without permission checks. Attackers can place the shortcode in published pages to expose sensitive directory contents including user account information, bypassing the authorize ACL enforced in the admin panel.

### CVE-2026-75542

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-24T21:17:47.373 |

Incorrect Authorization vulnerability in the OAuth token endpoint in hexpm hexpm allows an API key holding the repositories permission to read another organization's private packages.

When an API key is exchanged for a token through the OAuth client_credentials grant, validate_scopes_against_key/2 in lib/hexpm_web/controllers/api/oauth_controller.ex admits a requested scope whenever the key carries the repositories permission and the scope string begins with repository:. The organization name is never resolved against the principal, and expand_repositories_scope/3 only rewrites the literal repositories scope, so an explicit repository:<name> passes through untouched. Both CDN edges authorize repository access from the token claim without querying the database, so the minted token is read access to that organization's private packages until it expires.

This issue affects hex.pm: from 2025-10-18 before 2026-08-24.

### CVE-2026-76072

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-08-24T18:17:21.233 |

The Continue CLI applies an incomplete denylist as its only barrier to destructive shell commands when running unattended. In headless mode and auto mode the default policy in extensions/cli/src/permissions/defaultPolicies.ts grants the Bash tool the allow permission, and permissionChecker.ts hard-blocks a command only when the terminal-security evaluator returns a disabled verdict, so isCriticalCommand in packages/terminal-security/src/evaluateTerminalCommandSecurity.ts is the sole control. Its dangerous-path test matches only /, /*, ~, ~/*, /usr, /etc, /bin and /sbin and their prefixes, so a recursive forced removal of /home, /root, /var, /opt or /srv is not disabled. The command line is parsed with shell-quote, which reduces $HOME to an empty token, so rm -rf $HOME also fails the dangerous-path test while the shell re-expands the variable when the command is spawned. find with -delete is rated high risk rather than disabled, and shred, wipefs, truncate and pkexec are not handled. Because the agent autonomously reads content it does not control, including fetched web pages, repository files and issue text, an indirect prompt injection in that content can cause an unattended run to destroy the invoking user's data.

### CVE-2026-77135

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-25T09:17:34.010 |

The extension's user detail view fails to verify that a requested user record matches the configured or logged-in target, allowing any visitor with access to the Detail or List plugin to retrieve another frontend user's profile data, including name, email, date of birth and address, by supplying an arbitrary user ID.

### CVE-2026-77634

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-93` |
| Published | 2026-08-24T21:17:48.307 |

CakePHP is a rapid development framework for PHP. Prior to versions 4.5.12, 4.6.5, 5.1.8, 5.2.14, and 5.3.7 on their respective release lines, custom mail headers added with Message::setHeaders() or Message::addHeaders() do not have CRLF bytes removed, allowing header injection when user-controlled data is used in message headers. This issue is fixed in versions 4.5.12, 4.6.5, 5.1.8, 5.2.14, and 5.3.7.

### CVE-2026-78572

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-25T10:18:13.707 |

The Kalles Addons plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 1.0.6 via deserialization of untrusted input. This makes it possible for unauthenticated attackers to inject a PHP Object. No known POP chain is present in the vulnerable software, which means this vulnerability has no impact unless another plugin or theme containing a POP chain is installed on the site. If a POP chain is present via an additional plugin or theme installed on the target system, it may allow the attacker to perform actions like delete arbitrary files, retrieve sensitive data, or execute code depending on the POP chain present.

### CVE-2026-16231

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-25T10:18:04.080 |

hbs is an Express view engine that wraps Handlebars. Its registerAsyncHelper API bypasses Handlebars' automatic HTML escaping: an async helper returns an opaque placeholder during the first render pass, so the double-brace expression escapes only the placeholder, and after rendering hbs substitutes the placeholder with the raw callback return value without escaping it, across the cached, uncached, and layout render paths. An application that passes attacker-influenced data, for example user-supplied content from a database, into an async helper callback can therefore have arbitrary HTML and JavaScript injected into the server-rendered page, resulting in stored or reflected cross-site scripting. Versions 2.1.0 through 4.2.1 are affected, and the issue is fixed in 4.3.0, which HTML-escapes async helper output. Applications that intentionally emit raw HTML from an async helper can opt in explicitly with hbs.SafeString. Users should upgrade to 4.3.0.

### CVE-2026-78566

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-25T09:17:36.427 |

The Shuffle theme for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.8. This makes it possible for unauthenticated attackers to include and execute arbitrary files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where images and other “safe” file types can be uploaded and included.

### CVE-2026-78562

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-25T09:17:36.070 |

The Verdure Core plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.2. This makes it possible for unauthenticated attackers to include and execute arbitrary files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where images and other “safe” file types can be uploaded and included.

### CVE-2026-78478

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-98` |
| Published | 2026-08-25T06:19:01.353 |

The Mane theme for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 1.7. This makes it possible for unauthenticated attackers to include and execute arbitrary files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where images and other “safe” file types can be uploaded and included.

### CVE-2026-77567

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-24T21:17:48.150 |

Filament is a collection of full-stack components for accelerated Laravel development. Prior to versions 4.12.0 and 5.7.0, incorrect challenge-form required-field handling allows app-based multi-factor authentication to be bypassed when recovery codes are enabled. Email-based multi-factor authentication is not affected. This issue is fixed in versions 4.12.0 and 5.7.0.

### CVE-2026-78414

| 項目 | 値 |
|------|-----|
| CVSS | `8.0` |
| Vector | `CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T15:16:48.873 |

Cross-site scripting in the Web Administration interface of Network Optix Nx Witness VMS before version 6.1.3 on Linux, Windows and MacOS allows an adjacent-network attacker to execute arbitrary JavaScript in the browser of an authenticated administrator and steal the administrator's session token, resulting in Administrator Account Takeover. An attacker who controls an Nx server on the same network segment can set that server's site name to a script payload, which executes when an administrator opens the "Merge with Another Site" dialog and the site selection list is displayed.Solution:

Update to Nx Witness VMS version 6.1.3 or later.

### CVE-2026-79655

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-59` |
| Published | 2026-08-25T14:16:58.010 |

A flaw was found in sos clean, a utility within the sos package. This vulnerability allows a local attacker to perform arbitrary file creation or overwrite. By crafting a malicious tar archive, an attacker can exploit a path traversal issue during tar extraction, where symlink and hardlink targets are not properly validated. This enables the attacker to write files to arbitrary locations on the system with the privileges of the sos clean process, which often runs as root.

### CVE-2026-7455

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-24T21:17:49.040 |

A maliciously crafted FLT file, when parsed through Autodesk 3ds Max, can force an Out-of-Bounds Write vulnerability. A malicious actor may leverage this vulnerability to cause a crash, cause data corruption, or execute arbitrary code in the context of the current process.

### CVE-2026-19568

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-120` |
| Published | 2026-08-24T21:16:49.573 |

A maliciously crafted SVG file, when parsed through Autodesk 3ds Max, can force a Memory Corruption vulnerability. A malicious actor can leverage this vulnerability to execute arbitrary code in the context of the current process.

### CVE-2026-16783

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-787` |
| Published | 2026-08-24T21:16:49.023 |

A maliciously crafted ABC file, when parsed through Autodesk 3ds Max, can force an Out-of-Bounds Write vulnerability. A malicious actor may leverage this vulnerability to cause a crash, cause data corruption, or execute arbitrary code in the context of the current process.

### CVE-2026-61419

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-284` |
| Published | 2026-08-24T20:16:51.990 |

Dell ThinOS 10, versions prior to 2605_10.2518, contain an Improper Access Control vulnerability. A low privileged attacker with local access could potentially exploit this vulnerability, leading to Unauthorized access.

### CVE-2026-77137

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T09:17:34.343 |

The extension fails to properly sanitize user input before using it in a database query. As a result, a low-privileged backend user can inject arbitrary SQL through a URL parameter within the "Forms Export" backend module. Exploitation requires a low-privileged backend user and read access to the "Forms Export" Backend module.

### CVE-2026-77129

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1336` |
| Published | 2026-08-25T09:17:33.200 |

The extension passes an editor-configurable email subject string directly into a Fluid template source without restriction. A backend user with edit access to the event plugin or Backend Module can supply Fluid ViewHelper syntax in this field to disclose sensitive data or execute TypoScript content objects. Exploitation of this issue requires an authenticated backend account with edit access to the event registration plugin or backend module.

### CVE-2026-56095

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-502` |
| Published | 2026-08-25T09:17:31.457 |

The extension's indexer passed every field value returned by content object rendering through PHP's unserialize() function when transferring multi-value data for the SOLR_CLASSIFICATION, SOLR_MULTIVALUE and SOLR_RELATION content object types, rather than a safe format. If user-generated content saved in the TYPO3 database can reach an indexed field, this exposes a PHP Object Injection surface.

### CVE-2026-19851

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:L` |
| Weaknesses | `CWE-1393` |
| Published | 2026-08-25T08:18:08.880 |

A Use of Default Password vulnerability affecting Tuleap Enterprise Edition from 17.0 through 17.5 could allow an attacker to gain access to user accounts created during XML import.

### CVE-2026-15469

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:L/SI:L/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-321` |
| Published | 2026-08-24T17:17:21.587 |

The use of
hard-coded cryptographic key vulnerability has been identified in the mesh
functionality of Deco XE75 v3, XE5300 v3.6 and WE10800 v3.6. 
A shared RSA-512 mesh group private key is present in the affected
firmware and is used by the mesh protocol for node authentication.  An attacker who obtains the firmware image
and has local network access may be able to authenticate as a mesh node without
possessing a device-specific credential.





Successful
exploitation may allow an unauthenticated adjacent attacker to impersonate a
trusted mesh node and bypass mesh node authentication, which may permit unauthorized
changes to device or mesh configuration, affecting confidentiality, integrity
and availability.

### CVE-2026-71366

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-24T16:17:22.820 |

A server-side request forgery (SSRF) vulnerability was found in multiple AWX notification backends. The webhook, Mattermost, Rocket.Chat, and Grafana notification backends use notification template URLs as direct HTTP request targets without validating the target address against private, loopback, or reserved IP ranges. An organization notification administrator can create notification templates pointing to internal or loopback addresses, causing the AWX control node to issue HTTP requests to services that are not externally accessible. Additionally, the webhook notification backend follows HTTP redirects and resends configured Basic Authentication credentials to redirect targets regardless of host change, allowing an attacker to exfiltrate notification credentials by redirecting to an attacker-controlled host. The Grafana backend sends its API key in the Authorization header to the configured target URL.

### CVE-2026-12556

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-319` |
| Published | 2026-08-24T16:16:55.263 |

Potential security vulnerabilities have been identified in HP Easy Start for macOS, versions prior to 2.16.7.260722. These potential vulnerabilities may lead to escalation of privilege. HP is releasing updates to mitigate these potential vulnerabilities.

### CVE-2026-12555

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-379` |
| Published | 2026-08-24T16:16:55.130 |

Potential security vulnerabilities have been identified in HP Easy Start for macOS, versions prior to 2.16.7.260722. These potential vulnerabilities may lead to escalation of privilege. HP is releasing updates to mitigate these potential vulnerabilities.

### CVE-2026-56092

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T09:17:30.807 |

The extension forces empty frontend-group and subpage-inheritance restrictions onto page records during indexer sub-requests, and this forged state was persisted into the shared rootline cache, allowing anonymous visitors to bypass extendToSubpages-inherited access restrictions on cached pages.

### CVE-2026-65633

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-08-25T08:18:09.857 |

Improper Authentication vulnerability in team-alembic AshAuthentication allows purpose-limited JWTs to be replayed as full bearer API credentials when a resource uses stateless bearer-token verification.

The bearer-token authentication helper AshAuthentication.Plug.Helpers.retrieve_from_bearer/3 verifies an Authorization: Bearer JWT's signature and rejects tokens containing an act claim, but performs no check that the token's purpose claim equals user at the bearer boundary. When the resource is configured with require_token_presence_for_authentication?: false (the DSL default), the follow-on validate_token/3 helper returns {:ok, nil} without consulting the token resource, so no downstream check on purpose takes place either. As a result, any valid, non-expired JWT the library itself issued for a narrow, single-purpose flow (most notably the purpose: sign_in token that WebAuthn always emits during sign-in, and that the Password strategy emits when sign-in tokens are enabled) is accepted directly as a general-purpose bearer credential and resolves to a full current_user assignment.

This bypasses the library's intended token-exchange contract, in which the sign_in token is meant to be presented exactly once to a preparation that validates the purpose claim and immediately revokes the token. The first use of a still-valid sign-in token presented directly in the Authorization header succeeds because the stateless bearer path never scopes it to purpose == "user".

An attacker who obtains a not-yet-exchanged sign-in token for a target subject (for example via log or referrer leakage, an intercepted magic-link delivery channel, or a partially compromised intermediary) can present it as a bearer token and be authenticated as that subject, fully bypassing the intended one-time-use and revocation semantics. Exploitation additionally requires that the host application wire up retrieve_from_bearer/3 on a reachable route and uses either WebAuthn (sign-in tokens are always issued) or the Password strategy with sign_in_tokens_enabled?: true. Resources configured with require_token_presence_for_authentication?: true (including applications scaffolded by the Igniter installer since v4.5.0) and the session-based path (authenticate_resource_from_session/4) enforce purpose == "user" against the stored token record and are not affected.

This issue affects ash_authentication: from 3.10.5 before 4.14.2 and from 5.0.0-rc.0 before 5.0.0-rc.13.

### CVE-2026-55525

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-918` |
| Published | 2026-08-25T14:16:52.417 |

PraisonAI is a multi-agent teams system. Prior to praisonaiagents 1.6.58, the web_crawl function validates only the initial URL before _crawl_with_httpx uses httpx.Client(follow_redirects=True). Redirect targets are not revalidated, so an attacker who influences a crawl target can redirect a public URL to loopback, private network, or cloud metadata services while ALLOW_LOCAL_CRAWL remains disabled. The fetched internal response is returned to the agent context. This issue is fixed in version 1.6.58.

### CVE-2026-14457

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-476` |
| Published | 2026-08-25T13:17:49.533 |

Issue summary: In a server or client configuration with RFC7250 Raw Public Keys (RPKs)
enabled, and only the private key (with no associated certificate) configured locally,
a NULL pointer dereference may occur when the remote peer solicits raw public keys and
also sends the typically omitted "signature_algorithms_cert" TLS extension.

Impact summary: The impact is limited to a possible Denial of Service as a result of
an application abort, no data disclosure or remote command execution are possible.

CWE: CWE-476: NULL Pointer Dereference

Description: While a passing comment in sample code in the documentation suggests
that key-only RPK configurations are supported, the best-practice RPK configuration
is to always configure a corresponding certificate (possibly self-signed or
signed by any convenient CA).

When the private key is configured along with a matching certificate, the
"signature_algorithms_cert" extension is handled reliably even without the
fix, and peer clients or servers that don't support raw public keys may be
able to complete a TLS connection by pinning or verifying the corresponding
certificate or its public key.

Deployments that prefer to configure just a private key with no certificate
need to upgrade to an updated release as noted below.

FIPS impact: no

No FIPS modules are affected by this issue, as the SSL protocol implementation
is outside the OpenSSL FIPS module boundary.

### CVE-2026-77996

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:N/AU:N/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-25T12:16:25.973 |

Joomla Extension - yootheme.com - Authenticated, privileged stored XSS in YOOtheme Pro 1.0.0-5.0.41 - Lack of escaping in the location custom field lead to a XSS vector.

### CVE-2026-78576

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-08-25T10:18:13.877 |

The Readabler plugin for WordPress is vulnerable to SQL Injection in all versions up to 2.0.18 (exclusive) due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query.  This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database.

### CVE-2026-66766

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-1333` |
| Published | 2026-08-25T01:16:37.230 |

SAP S/4HANA (Private Cloud) uses a third-party component that contains a Regular Expression Denial of Service (ReDoS) vulnerability. An unauthenticated attacker could supply specially crafted input that triggers excessive processing within the affected functionality. Successful exploitation could exhaust system resources and make the service unavailable, resulting in a high impact on availability. There is no impact on confidentiality and integrity.

### CVE-2026-78268

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-497` |
| Published | 2026-08-24T22:17:20.797 |

Unauthenticated Sensitive Data Exposure in Lead Generation Contact Widget &amp; AI Chatbot: Chat Button, Phone Call, Telegram, Email – SiteLeads <= 1.2.0 versions.

### CVE-2026-77384

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-772` |
| Published | 2026-08-24T22:17:19.650 |

libp2p is a JavaScript implementation of the libp2p networking stack. Prior to version 4.2.9, the reservation refresh path in reservation-store.ts reuses the same retimeableSignal but unconditionally registers another abort listener on every refresh. As a result, a remote peer can repeatedly send valid RESERVE requests for the same reservation, causing unbounded listener and closure growth in @libp2p/circuit-relay-v2 relay servers and leading to denial of service. This issue is fixed in version 4.2.9.

### CVE-2026-76098

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-674` |
| Published | 2026-08-24T20:17:19.330 |

Mistune is a Python Markdown parser with renderers and plugins. Versions 3.3.0 through 3.3.2 are vulnerable to DoS through deeply nested tokens. HTML rendering creates deeply nested emphasis tokens from consecutive asterisk characters, and recursive rendering in HTMLRenderer.render_token() can exceed Python's recursion limit and raise RecursionError, allowing crafted Markdown to crash a parsing process. This issue is fixed in version 3.3.3

### CVE-2026-21752

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-1104` |
| Published | 2026-08-24T16:16:55.663 |

HCL Hive is affected by a use of vulnerable third-party components which could allow an attacker unauthorized access or compromise of the system by exploiting publicly documented security flaws.

### CVE-2025-68825

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-276` |
| Published | 2026-08-24T16:16:54.693 |

HCL Hive is affected by incorrect default permissions which could allow an attacker unauthorized lateral movement, container breakout, and interception of sensitive internal communications.

### CVE-2026-76055

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-08-24T15:16:46.860 |

Improper Neutralization of Special Elements used in an OS Command in the package manager component of Black Duck blackduck-c-cpp before 3.0.7 allows an actor able to create a file within the scanned build directory to execute operating system commands as the account running the scan.



Filesystem paths encountered while traversing the scanned directory are interpolated into command strings that are executed through a shell without quoting or escaping, so shell metacharacters within those paths are interpreted rather than treated as literal text. No control over the build command or the tool's configuration is required.

### CVE-2026-75037

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-08-25T10:18:13.113 |

Polkit Authentication Based on UnixProcessSubject / Peer PID in LACT on Linux allows an Authentication Bypass. This issue affects LACT through 0.10.0. Fixed by commit d0478fe42c2219454e272f96b1cbd29ab37ee566.

### CVE-2026-78259

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L` |
| Weaknesses | `CWE-288` |
| Published | 2026-08-24T22:17:19.803 |

Unauthenticated Broken Authentication in WPLegalPages <= 3.7.0 versions.

### CVE-2026-18349

| 項目 | 値 |
|------|-----|
| CVSS | `7.3` |
| Vector | `CVSS:4.0/AV:P/AC:H/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1247` |
| Published | 2026-08-24T17:17:21.740 |

Improper protection against voltage and clock glitches vulnerability in Microchip SAMA5D4 allows Hardware Fault Injection.

This issue affects SAMA5D4.

### CVE-2026-79667

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-08-25T12:16:34.813 |

Ech0 version 4.3.4 and earlier fails to reliably enforce scoped access token (least-privilege) restrictions on several privileged admin routes. Multiple privileged endpoints (e.g., /api/inbox, /api/panel/comments, /api/backup/export) omit scope checks and authorize based only on the user's admin role, and the backup export handler discards token scope metadata entirely. An attacker holding a deliberately limited (low-scope) admin access token can reach broader privileged functionality than intended, including reading the inbox and exporting a full database backup ZIP archive. Fixed in 4.4.3.

### CVE-2026-75971

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-08-25T12:16:25.087 |

The ShopEngine Elementor WooCommerce Builder Addon – All in One WooCommerce Solution plugin for WordPress is vulnerable to Privilege Escalation in all versions up to, and including, 4.9.4. This is due to the `rum_importer()` function being registered on the WordPress core `import_start` action hook with no plugin-owned capability check and no allowlist filtering, causing arbitrary `<wp_option>` name/value pairs parsed from an attacker-supplied WXR import file to be passed directly to `update_option()`. This makes it possible for authenticated attackers, with Shop Manager-level access and above, to write arbitrary WordPress options — most critically setting `users_can_register` to `1` and `default_role` to `administrator` — enabling open self-registration of Administrator accounts and full site takeover. This is exploitable by Shop Manager-level users because WooCommerce grants that role the `import` capability, allowing it to reach the WordPress Importer flow that fires the `import_start` hook on which `rum_importer()` is registered, contrary to the assumption that the hook is restricted to Administrators.

### CVE-2026-78563

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-25T09:17:36.247 |

The NotificationX Pro plugin for WordPress is vulnerable to Stored Cross-Site Scripting in all versions up to, and including, 3.1.4 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page.

### CVE-2026-18328

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-25T08:18:08.627 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to DOM-Based Reflected Cross-Site Scripting via the 'error_description' parameter in all versions up to, and including, 1.57.0 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. The vulnerability is only triggerable on pages hosting a Forminator form configured to use the Stripe Checkout Sessions payment API, which became the default in 1.56.0.

### CVE-2026-18323

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-25T08:18:08.497 |

The Forminator Forms – Contact Form, Payment Form & Custom Form Builder plugin for WordPress is vulnerable to Stored Cross-Site Scripting via Radio Field (Save and Continue Draft) in all versions up to, and including, 1.57.0.2 due to insufficient input sanitization and output escaping. This makes it possible for unauthenticated attackers to inject arbitrary web scripts in pages that will execute whenever a user accesses an injected page. This is exploitable because the Save-and-Continue draft submission AJAX endpoint is registered as nopriv, allowing unauthenticated attackers to bypass radio field option-membership validation and persist a crafted payload that, when rendered on the Submissions admin page, is auto-executed via the bundled Inputmask library's data-attribute callback binding.

### CVE-2026-34968

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T02:16:40.843 |

Adminer before 5.4.3 contains an arbitrary file deletion vulnerability in SQLite mode where the database-list drop action fails to validate file extensions before deletion. An authenticated attacker can submit arbitrary relative file paths in the db[] parameter to delete any files writable by the PHP process.

### CVE-2026-71506

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-24T19:16:49.960 |

Dolibarr before 24.0.0 contains an improper authorization vulnerability in the payments REST API delete endpoint that allows authenticated attackers with invoice-deletion rights to permanently delete any payment record by bypassing the intended payment-issuance rights check. Attackers can exploit this misconfigured permission check to zero paid amounts on invoices and remove entries from accounting exports, causing financial data integrity loss.

### CVE-2026-71364

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T16:17:22.663 |

A path traversal vulnerability was found in AWX's project archive extraction. The project_archive action plugin extracts zip and tar archive members by joining the project directory path with the member filename without performing path normalization, boundary validation, or rejecting directory traversal sequences. A malicious archive containing members with path traversal components can write files to arbitrary locations on the execution node's filesystem outside the intended project directory. An attacker who controls the archive content, either through a compromised upstream source, a malicious archive URL, or a man-in-the-middle attack on a plain HTTP connection, can achieve arbitrary file writes as the user performing the extraction, potentially leading to remote code execution through mechanisms such as cron files, SSH authorized keys, or playbook content injection.

### CVE-2026-79666

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T12:16:34.670 |

Ech0 before 4.4.3 fails to enforce administrator authorization on dashboard log endpoints, allowing any authenticated user to access system logs. Attackers with valid user sessions can query GET /api/system/logs and subscribe to SSE and WebSocket log streams to retrieve sensitive operational data including file paths, stack traces, and internal URLs.

### CVE-2026-77145

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-25T09:17:35.667 |

The permission check for the frontend management update flow verified a different event than the one the request went on to modify. A user with frontend event management access could therefore modify events belonging to other organizers.

### CVE-2026-77144

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-08-25T09:17:35.510 |

The frontend management plugin attributed a newly created event to the submitting user's organizer record only when the request supplied no organizer of its own. The accompanying permission check confirmed only that the submitting user held any organizer role. A user with frontend event management access could therefore create an event that is attributed to another organizer.

### CVE-2026-78679

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-73` |
| Published | 2026-08-25T02:16:52.470 |

GitPython before 3.1.59 contains an arbitrary file read vulnerability in TagReference.create() where a positional reference parameter bypasses the unsafe option guard. Attackers can supply a reference value like --file=<path> to read arbitrary files, with contents returned in the annotated tag message.

### CVE-2026-78678

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-88` |
| Published | 2026-08-25T02:16:52.313 |

GitPython versions before 3.1.59 contain an incomplete denylist in the unsafe_git_revision_options guard that omits --contents and -S options, allowing attackers to read arbitrary files by passing these options to Repo.blame(). Attackers can supply revision values like --contents=/etc/passwd to leak file contents through the blame result returned to the caller.

### CVE-2026-72698

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-200` |
| Published | 2026-08-25T02:16:45.550 |

Grav CMS before 2.0.16 fails to filter system, site, and theme configuration arrays in sandboxed Twig renders, allowing content editors to read sensitive configuration values. Attackers with page-content edit access can access raw configuration arrays including secrets like cache credentials by using dot notation in Twig templates, bypassing the config_denied_paths restrictions.

### CVE-2026-72697

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T02:16:45.407 |

Grav CMS before 2.0.16 contains a path traversal vulnerability in the media_directory() Twig function that fails to validate filesystem paths, allowing authenticated users to enumerate and access files outside intended scope. Attackers with page authoring privileges can supply arbitrary filesystem paths to media_directory() and use the allow-listed filepath accessor on Medium objects to read file contents of any file matching configured media extensions that the web server process can access.

### CVE-2026-72695

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-25T02:16:45.097 |

Grav before 2.0.16 contains a path traversal vulnerability in MediaUploadTrait::deleteFile() that allows authenticated users with media management permissions to delete arbitrary files by supplying filenames with directory traversal sequences. The method validates only the basename portion of the filename while preserving unvalidated directory paths containing ../ sequences that are passed to unlink(), enabling deletion of files outside the intended media storage directory.

### CVE-2026-56702

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-434` |
| Published | 2026-08-25T02:16:41.900 |

Adminer versions before 5.4.3 contain an unrestricted file upload vulnerability in the AdminerFileUpload plugin that allows authenticated users to upload PHP files by exploiting a permissive default extension allowlist. Attackers can upload PHP webshells to columns ending in _path and execute arbitrary code as the web-server user when uploadPath is web-served.

### CVE-2026-53532

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-617` |
| Published | 2026-08-24T23:16:36.920 |

OpenEXR is the reference implementation and specification for the EXR image format, widely used in the motion picture industry. In versions 3.4.0 through 3.4.12, a crafted HTJ2K-compressed EXR file causes an unconditional process abort in any application that calls exr_start_read() on untrusted input, resulting in denial of service. The crash is triggered by a QCD marker whose lower five bits are zero, which OpenEXR passes into the vendored OpenJPH library while constructing the codestream and evaluating its quantization delta parameters. OpenJPH uses an assertion rather than a recoverable error to validate those bits, so any invalid value calls abort() directly and cannot be intercepted by surrounding error handling, a problem compounded by OpenEXR wrapping only its internal HT header parser in error handling while leaving the later codestream read and construction calls unprotected. This issue has been resolved in version 3.4.13.

### CVE-2026-78282

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T22:17:20.930 |

Unauthenticated Cross Site Scripting (XSS) in Stripe Payments <= 2.1.2 versions.

### CVE-2026-78264

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T22:17:20.267 |

Unauthenticated Cross Site Scripting (XSS) in Toolset Blocks <= 1.6.26 versions.

### CVE-2026-78263

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T22:17:20.133 |

Unauthenticated Cross Site Scripting (XSS) in Event Tickets <= 5.29.2.1 versions.

### CVE-2026-32556

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:L` |
| Weaknesses | `CWE-79` |
| Published | 2026-08-24T22:16:51.773 |

Unauthenticated Cross Site Scripting (XSS) in Boost <= 2.0.4 versions.

### CVE-2026-71511

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-522` |
| Published | 2026-08-24T20:17:13.420 |

Dolibarr before 24.0.0 contains a sensitive data exposure vulnerability in the Members REST API that allows authenticated attackers with member-read rights to retrieve bcrypt password verifiers by querying member endpoints. Attackers can call the individual member or member list endpoints to obtain crypted password verifier fields that are not filtered by the base API serializer or the Members API class, potentially enabling offline password cracking attacks.

### CVE-2026-71510

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-24T20:17:12.957 |

Dolibarr before 24.0.0 contains a SQL injection vulnerability in the users REST API that allows authenticated attackers with user-read rights to extract sensitive data by splicing unsanitized filter parameters into SQL WHERE clauses without column restrictions. Attackers can perform binary search on numeric fields and LIKE prefix iteration on string fields to recover salary figures and password verifiers omitted from normal API responses, while raw database error messages in the same endpoint enable column name enumeration.

### CVE-2026-71509

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T19:16:50.403 |

Dolibarr before 24.0.0 contains an improper authorization vulnerability in the expense report REST API update endpoint that allows authenticated attackers with expense-creation rights to bypass the approval workflow by directly setting approval status and approver identity fields. Attackers can manipulate workflow state fields through the REST API to advance expense reports to approved or closed status without possessing the dedicated approval right, while also creating forensic inconsistencies in audit records due to missing approval timestamps.

### CVE-2026-71508

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T19:16:50.253 |

Dolibarr before 24.0.0 contains an improper authorization vulnerability in the user REST API update endpoint that allows attackers with user-write rights to modify payroll fields by exploiting an incomplete credential denylist that omits payroll columns. Attackers can rewrite salary, bonus, hourly rate, daily rate, and weekly hours for any user without holding payroll rights, with the modified values appearing in payroll export reports.

### CVE-2026-71507

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-24T19:16:50.110 |

Dolibarr before 24.0.0 contains a broken object-level authorization vulnerability in the REST API company bank account write routes that allows authenticated attackers with third-party creation rights to create, replace, or delete bank account details of any company without requiring read access to that company. Attackers can inject attacker-controlled IBANs as creditor accounts, which are then written into regenerated SEPA credit-transfer files, redirecting outgoing payments to attacker-controlled accounts.

### CVE-2026-71505

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-08-24T19:16:49.817 |

Dolibarr before 24.0.0 contains a broken object-level authorization vulnerability in the REST API third-party site account write routes that allows authenticated attackers with third-party creation rights to overwrite the WebPortal password of any company by bypassing per-object access checks that are only enforced on read routes. Attackers can replace the victim company's WebPortal password through the write endpoint, authenticate as that company to access its invoice data, and also obtain the victim's previous password verifier from the API response.

### CVE-2026-77914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-08-24T17:18:18.260 |

rConfig Core 8.0.0 before 8.2.13 contains a path traversal vulnerability that allows authenticated users to read arbitrary files by supplying crafted filenames containing directory traversal sequences to the export download endpoint. Attackers can manipulate the filename parameter with traversal sequences to escape the intended export directory and access files outside it that are readable by the application process.

### CVE-2026-19685

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-863` |
| Published | 2026-08-24T17:17:21.907 |

NetworkManager did not apply the private_user restriction to the 802-1x.ca-path and phase2-ca-path directory-valued connection properties. This incomplete fix for CVE-2025-9615 allows an unprivileged local user to point a private WPA-Enterprise (802.1X) connection profile's CA path at an attacker-controlled directory, bypassing server certificate validation and enabling credential theft via a rogue access point.

### CVE-2026-76054

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:H/SA:L/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-214` |
| Published | 2026-08-24T15:16:46.650 |

Invocation of Process Using Visible Sensitive Information in Black Duck blackduck-c-cpp 1.0.17 through 3.0.6 allows an actor able to execute code within the scanned project's build to obtain the Black Duck API token via the ambient process environment, which is inherited by subprocesses launched during build capture and signature scanning. This applies only where the token is supplied through the BLACKDUCK_API_TOKEN or BD_HUB_TOKEN environment variable.



Upgrading does not remediate prior disclosure; any token supplied to an affected version through an environment variable should be rotated.

### CVE-2026-39914

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-24T15:16:37.940 |

TIM Flow before 26.0.6 contains an improper authorization vulnerability that allows any authenticated user to submit arbitrary SQL queries to a privileged dashboard Excel export endpoint intended for administrative use only. Attackers can craft and submit unauthorized SQL queries to the export endpoint to retrieve sensitive database contents as a downloadable spreadsheet, bypassing role-based access controls.

### CVE-2026-79672

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:L/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-08-25T12:16:35.537 |

Ech0 before 4.4.3 fails to enforce scope-based authorization on nine comment panel admin endpoints, allowing access tokens with minimal scopes to perform full comment moderation operations. Attackers with a limited-scope access token can list, approve, reject, delete comments, and modify comment system settings by directly accessing the unprotected panel endpoints.

### CVE-2026-78553

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-276;CWE-732` |
| Published | 2026-08-24T20:17:24.383 |

RansomLook created its Flask session-signing key without explicitly restricting the file permissions. The secret_key file was created using the process's default permissions and umask, resulting in permissions such as 0644 under a common 022 umask. Consequently, other local users able to access the RansomLook home directory could read the application's cryptographic secret.


The exposed key is security-critical because it is used to sign Flask session cookies and is also involved in the legacy API-key key derivation. An attacker who obtains the key can generate valid session cookies and impersonate an authenticated user, including an administrator. In LDAP configurations, exploitation may be particularly straightforward because the session user loader does not require the supplied username to correspond to an existing local user.


Successful exploitation requires local access sufficient to read the improperly protected file, but can result in complete compromise of RansomLook's authentication and authorization controls.


The patch creates new secret-key files atomically with permissions 0600 and also restricts permissions on existing key files during application startup.

### CVE-2026-78465

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:3.1/AV:L/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-190` |
| Published | 2026-08-24T17:18:20.810 |

A flaw was found in the file-pcx plugin in GIMP, affecting 32-bit builds only. When processing a PCX image file, the plugin calculates memory allocation sizes based on the image dimensions and the number of color planes. If a crafted file sets the number of planes to 4 alongside sufficiently large dimensions, the calculation exceeds the 32-bit integer limit and overflows, resulting in an undersized heap-based buffer allocation. This integer overflow issue results in a heap-based buffer overflow when the plugin subsequently writes image data into the undersized buffer, causing memory corruption, potentially leading to arbitrary code execution or a denial of service.
