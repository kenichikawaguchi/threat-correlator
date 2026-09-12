# NVD 脅威インテリジェンスレポート

- **生成日時**: 2026-09-12 15:01 UTC
- **対象期間**: `2026-09-11T15:00:30.000Z` 〜 `2026-09-12T15:01:26.000Z`
- **重要CVE数**: 77 件（Critical 9.0+: 23 件 / High 7.0〜: 54 件）

---

## AI 分析サマリー

## 1. 全体サマリー  
- 直近で公開された CVE のうち **CVSS 7.0 以上** が 30 件以上報告されており、**リモートコード実行 (RCE)・任意ファイル読み書き・認証バイパス** が目立つ。  
- 特に **GitLab、Mistral Vibe、WordPress 系プラグイン、組み込み系ファームウェア** に集中しており、クラウド／オンプレミス双方で深刻な影響が想定される。  
- 多くは **入力バリデーション不備** や **権限チェックの欠如** が根本原因で、パッチ適用だけでなく、開発・運用プロセスでの「デフォルトで安全であること」の確認が重要になる。  

---

## 2. 特に注目すべき CVE  

| CVE | CVSS | 主な脆弱性種別 | 影響範囲・対象 | 注目理由 |
|-----|------|----------------|----------------|----------|
| **CVE‑2026‑85706** | 10.0 | 任意ファイル読み取り (Path Traversal) | GitLab CE/EE 18.7‑19.3 系すべて (19.1.8 未満, 19.2.6 未満, 19.3.2 未満) | 認証不要でサーバ上の任意ファイルを取得可能。機密情報漏洩だけでなく、後続の権限昇格や RCE に繋がりやすい。 |
| **CVE‑2026‑87986** (同系列: 87985‑87988) | 10.0 | 任意コード実行 (コマンドパーミッションバイパス) | Mistral Vibe 1.3.4 以降の全バージョン | 環境変数・シェル構文・ANSI‑C クオートを利用して allow‑list されたコマンドを迂回でき、リモートから任意コードが実行できる。CI/CD パイプラインや自動化スクリプトで広範に利用される可能性が高い。 |
| **CVE‑2026‑78159** / **CVE‑2026‑78006** | 9.8 | RCE (PHP のマジックメソッド・配列解析不備) | WordPress プラグイン *The Events Calendar* ≤ 6.17.4 | WordPress は最も普及している CMS の一つで、プラグイン経由の RCE はサイト全体の乗っ取りに直結。プラグインは自動更新が無効化されているケースが多く、放置リスクが大きい。 |
| **CVE‑2026‑53952** | 9.8 | 任意管理者アカウント作成 (ロジックフロー) | GetSimple CMS CE 3.3.22 以前 / 3.4.0a 以前 | 認証不要で管理者権限を取得でき、全てのコンテンツ改ざん・マルウェア埋め込みが可能。小規模サイトでも深刻な被害が想定される。 |
| **CVE‑2026‑89010** | 9.3 | OS コマンドインジェクション (root) | WAVLINK ルータ (WN535M1/M3) firmware < M35M1_V250922 | TCP 13136 の sync_server デーミオンがファイル名を直接シェルに展開。外部から root 権限で任意コマンド実行が可能で、IoT/産業ネットワークの踏み台化リスクが高い。 |

> **※同一製品・同一脆弱性クラスが複数報告されているケース（例：Mistral Vibe 系列）は、代表的な 1 件をピックアップしつつ、同系統の残りも同様に対策が必要です。**

---

## 3. 推奨アクション  

### 3.1 パッチ適用・バージョンアップ（必須）

| 製品 / パッケージ | 現行脆弱バージョン | 推奨バージョン / パッチ |
|-------------------|-------------------|--------------------------|
| **GitLab CE/EE** | 18.7‑19.3 系（19.1.8 未満、19.2.6 未満、19.3.2 未満） | **19.1.8** 以上、もしくは **19.2.6** 以上、**19.3.2** 以上にアップデート |
| **Mistral Vibe** | 1.3.4 以前（任意コード実行系） | 1.3.5 以上（公式リリースノートで「環境変数・シェル構文チェック」修正） |
| **The Events Calendar** (WordPress) | ≤ 6.17.4 | **6.17.5** 以上に更新（WordPress の自動更新が有効でない場合は手動で適用） |
| **GetSimple CMS** | CE ≤ 3.3.22、CE 3.4.0a 以前 | **3.4.0b** 以上（管理者作成ロジック修正） |
| **WAVLINK WN535M1/M3 ルータ** | firmware < M35M1_V250922 | **M35M1_V250922** 以上の公式ファームウェアに更新 |
| **ThemeREX Addons** | < 2.45.0 | **2.45.0** 以上 |
| **Everest Forms** | ≤ 3.6.0 | **3.6.1** 以上 |
| **Tutor LMS** | ≤ 4.0.7 | **4.0.8** 以上 |
| **Masteriyo – LMS** | ≤ 3.4.0 | **3.4.1** 以上 |
| **SMS Alert Order Notifications** | ≤ 3.9.9 | **3.10.0** 以上 |
| **Gato GraphQL** | ≤ 19.2.3 | **19.2.4** 以上 |
| **SPIP** | < 4.4.18 | **4.4.18** 以上 |
| **Authorizer** | < 2.2.1 | **2.2.1** 以上 |
| **stb_vorbis** | ≤ 1.22 | **1.23** 以上（整数型キャスト修正） |
| **Laci Synchroni** | < 1.2.3 | **1.2.3** 以上（OAuth2 フローのサーバ側検証追加） |

> **※パッケージマネージャ (apt, yum, dnf, apk, pip, npm など) を利用できる環境では、`apt-get update && apt-get upgrade <pkg>` 等で自動的に最新バージョンへ置き換えることを推奨します。**

### 3.2 設定・運用面での緩和策

- **GitLab**  
  - `gitlab.rb` で `gitlab_rails['gitlab_shell_ssh_port']` など

---

## 🔴 Critical（CVSS 9.0+）

### CVE-2026-85706

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-12T03:16:30.473 |

GitLab has remediated an issue in GitLab CE/EE affecting all versions from 18.7 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that, under certain conditions, an unauthenticated user could have read arbitrary files from the GitLab server due to improper path confinement and missing authentication enforcement in the repository commits API.

### CVE-2026-82617

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1333` |
| Published | 2026-09-11T18:16:59.443 |

The two built-in name-finder patterns exposed by
opennlp.tools.namefind.RegexNameFinderFactory - DEFAULT_REGEX_NAME_FINDER.EMAIL
and DEFAULT_REGEX_NAME_FINDER.URL - contain ambiguous nested quantifiers. An
application that obtains these finders through
RegexNameFinderFactory.getDefaultRegexNameFinders(...) and then applies them to
untrusted text through RegexNameFinder.find(String[]) or RegexNameFinder.find(String)
can be driven into super-linear backtracking or into unbounded matcher recursion by a
small crafted input.





For the EMAIL pattern, a long run of local-part characters that is never followed by an
@ forces the matcher to re-scan to end-of-input from every starting offset. Cost grows
quadratically with input length: an input of approximately 32 KB consumes several seconds
of CPU in a single find() call and returns no match, and each doubling of the input
multiplies the cost roughly four-fold.





For the URL pattern, the query-string sub-expression nests a capturing repetition inside
an outer repetition. The JDK matcher recurses once per query token, so an input of
approximately 4 KB containing many &-separated tokens exhausts the thread stack and
causes java.lang.StackOverflowError to propagate out of find(), terminating the
calling thread. On a thread created with a smaller stack (for example -Xss512k, typical
of server worker pools) approximately 1 KB is sufficient.





In both cases an attacker who can supply text for analysis can convert a single request
into seconds to minutes of pinned CPU, or into an abrupt thread death, denying service to
the embedding application. No authentication, special configuration, or model file is
required beyond the application having selected one of the two built-in finders.





This issue affects Apache OpenNLP: from 2.0.0 through 2.5.11; from 3.0.0-M1 through
3.0.0-M5.









Users are recommended to upgrade to version 2.5.12, or to 3.0.0-M6 for users tracking the
3.0.0 milestone line, which fix the issue.

### CVE-2026-87988

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-732` |
| Published | 2026-09-11T15:17:07.930 |

An arbitrary file access vulnerability in Mistral Vibe allows an attacker to bypass workspace restrictions through commands classified as unconditionally allowed. Missing path validation for these commands enables access to files outside the active workspace without user approval.

### CVE-2026-87987

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-15` |
| Published | 2026-09-11T15:17:07.793 |

An arbitrary code execution vulnerability in Mistral Vibe allows an attacker to bypass command permission checks using environment variable assignments preceding allowlisted commands. These assignments are excluded from inspection, enabling attacker-controlled environment variables to cause arbitrary code execution without user approval.

### CVE-2026-87986

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-228` |
| Published | 2026-09-11T15:17:07.653 |

An arbitrary code execution vulnerability in Mistral Vibe allows an attacker to bypass command permission checks using shell constructs it's parser cannot interpret. Unparsed portions are omitted from inspection, enabling embedded commands to execute on the user's system without approval.

### CVE-2026-87985

| 項目 | 値 |
|------|-----|
| CVSS | `10.0` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-184` |
| Published | 2026-09-11T15:17:07.520 |

An arbitrary code execution vulnerability in Mistral Vibe allows an attacker to bypass command permission checks using ANSI-C quoted arguments. These arguments are not properly inspected, enabling a crafted allowlisted command to execute arbitrary code on the user's system without approval.

### CVE-2026-87719

| 項目 | 値 |
|------|-----|
| CVSS | `9.9` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-12T03:16:31.477 |

GitLab has remediated an issue in GitLab EE affecting all versions from 18.3 before 19.1.8, 19.2 before 19.2.6, and 19.3 before 19.3.2 that under certain conditions could allow an authenticated user with Duo Chat access to obtain Advanced Search instance configurations and sensitive credentials using a specially crafted GraphQL subscription argument to bypass serialization and perform server object lookup.

### CVE-2026-78159

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-12T08:16:24.377 |

The The Events Calendar plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 6.17.3 via the parse_array function. This is due to insufficient validation of the widget 'classes' map, allowing a plain-array payload to bypass the is_safe_widget_instance() object check and reach the callable-invocation sink in Element_Classes::parse_array(). This makes it possible for unauthenticated attackers to execute code on the server. Exploitation requires that the targeted site has comments enabled on tribe_events posts and that at least one comment containing a crafted wp:legacy-widget block has been submitted, as the attack chain is triggered when do_blocks() processes the single-event HTML including the comment area.

### CVE-2026-78006

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-12T08:16:24.240 |

The The Events Calendar plugin for WordPress is vulnerable to Remote Code Execution in all versions up to, and including, 6.17.4 via the is_safe_widget_instance function. This is due to insufficient protection in is_safe_widget_instance, which can be bypassed because PHP fires magic methods during its pre-parse, combined with enable_rendering_widget_copied() forging a valid wp_hash integrity attribute before unserialize() is reached. This makes it possible for unauthenticated attackers to execute code on the server. This is exploitable without authentication or approval because the plugin's V2 single-event template runs do_blocks() over buffered comment HTML, and WordPress returns a moderation-hash URL that allows an unauthenticated commenter to immediately view their own pending comment, delivering the injected block markup to the vulnerable code path before any moderation occurs. This does require comments to be enabled and visible on events.

### CVE-2026-53952

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-285;CWE-306;CWE-489` |
| Published | 2026-09-11T20:17:14.060 |

GetSimple CMS is a content management system (CMS), and GetSimple CMS CE is the community edition of that CMS. A logic flaw in GetSimple CMS (v3.4.0a and below) and GetSimpleCMS-CE (v3.3.22 and below) allows unauthenticated attackers to create a new administrator account. The application features an automated security control designed to delete the sensitive `admin/setup.php` file post-installation. However, this control is neutralized by a self-exclusion bug within the deletion logic, leaving the setup script accessible for unauthorized account creation even after a legitimate installation is completed. As of time of publication, no known patched versions are available.

### CVE-2026-79395

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-11T19:17:46.367 |

An improper authentication vulnerability in the WS-Security (wsse:UsernameToken) verification routine within the Sofia IPC daemon in Xiongmai IP Camera XM530 firmware HMT.CM2005-v220608.1837 and earlier allows remote attackers to bypass authentication and execute privileged ONVIF actions (including PTZ control, stream URL retrieval, and system reboot) via a crafted SOAP request supplying the admin username with any arbitrary password when the account's stored password is empty.

### CVE-2026-62105

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-11T19:17:43.337 |

Unauthenticated PHP Object Injection in ThemeREX Addons < 2.45.0 versions.

### CVE-2026-62103

| 項目 | 値 |
|------|-----|
| CVSS | `9.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-11T19:17:43.207 |

Unauthenticated PHP Object Injection in Everest Forms <= 3.6.0 versions.

### CVE-2026-38056

| 項目 | 値 |
|------|-----|
| CVSS | `9.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-11T15:17:01.070 |

A local privilege escalation vulnerability exists in the iDirect iQ200 VSAT terminal running firmware 23.0.1.0. The iQ200 is a rackmount satellite modem deployed across oil and gas, maritime, defense, and remote infrastructure as the primary, and often sole communications link for offshore rigs, vessels, and remote sites. Important context: the device ships from the factory with a pre-configured low-privilege local user account. This account is intended for field technicians who need shell access for maintenance and diagnostics but should not have full administrative control over the device. This built-in account provides the initial access required to exploit this vulnerability. No additional credentials need to be obtained or brute-forced.

### CVE-2026-54072

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:N` |
| Weaknesses | `CWE-601` |
| Published | 2026-09-11T19:17:42.663 |

Authorizer is an open-source, self-hostable authentication and authorization server. Prior to version 2.2.1, the `/authorize` endpoint accepts any `redirect_uri` without validating it against `AllowedOrigins`. When `response_type=token` or `response_type=id_token`, the server appends `access_token`, `id_token`, and `refresh_token` as query parameters and issues a 302 redirect to the attacker-supplied URL. An unauthenticated attacker can obtain the required `client_id` from the public `/graphql?query={meta{client_id}}` endpoint. A partial fix was applied in v2.0.1 to other handlers (`oauth_login`, `verify_email`, `magic_link_login`, `forgot_password`, `invite_members`, `oauth_callback`) but `/authorize` was not included. Version 2.2.1 contains a more complete fix.

### CVE-2026-72710

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-915` |
| Published | 2026-09-11T17:18:58.907 |

SPIP before 4.4.18 contains a remote code execution vulnerability in the editer_objet action where the arg parameter resolves SQL table names without enforcing an editable columns allowlist, allowing attackers with a valid nonce to inject attacker-controlled rows into the spip_jobs table. Attackers can supply arg=job/0 with crafted fonction and args values, which are later unserialized and executed when the cron job queue is drained, resulting in arbitrary PHP function execution on the underlying system.

### CVE-2026-72709

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-11T17:18:58.760 |

SPIP before 4.4.18 contains a missing authorization vulnerability in the administrative action endpoints under ecrire/action/ that allows unauthenticated attackers to perform privileged actions by supplying a valid HMAC-SHA256 nonce without any server-side permission check via autoriser(). Attackers can obtain a valid nonce, compute it for any action as the anonymous user, and invoke the editer_auteur action directly over HTTP to reset the password of any user account, including the administrator.

### CVE-2026-89010

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-11T15:17:08.357 |

WAVLINK WN535M1 and WN535M3 routers running firmware prior to M35M1_V250922 contain an unauthenticated OS command injection vulnerability that allows remote attackers to execute arbitrary commands as root by sending crafted filenames to the sync_server daemon on TCP port 13136. The daemon interpolates attacker-controlled filename input containing shell metacharacters into a shell command string via sprintf() and passes it to system() without sanitization, enabling root-level command execution on the device.

### CVE-2026-87984

| 項目 | 値 |
|------|-----|
| CVSS | `9.3` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-11T15:17:07.383 |

An arbitrary file write vulnerability in Mistral Vibe, introduced in version 1.3.4, allows an attacker to create or overwrite files outside the active workspace without user approval. Shell redirection destinations are omitted from permission checks, enabling otherwise allowlisted commands to write to arbitrary paths accessible to the Vibe process.

### CVE-2026-90456

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-09-11T22:16:47.993 |

An example environment-configuration file for a bundled inventory-management component ships with a fixed, publicly-known administrative password. A deployment that copies this example file into active configuration without running the setup routine that regenerates credentials will expose that component's administrative interface to anyone aware of the default value.

### CVE-2026-54047

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287;CWE-349;CWE-602` |
| Published | 2026-09-11T17:17:10.477 |

Laci Synchroni is a decentralized mod and appearance sync server and plugin for Dalamud. Versions of the backend prior to 1.2.3 have an improper authentication vulnerability in the application's OAuth2 login flow. The application relies on client-side state by trusting the `UID` field inside the `Authentications` object of a user's local `config.json` file. By manually editing this local file on their PC prior to logging in, a user can supply an arbitrary UID. Because the server fails to validate that the authenticated OAuth2 identity matches the requested UID, an attacker can fully impersonate any target user and perform actions on their behalf. This issue has been resolved in version 1.2.3. The patch modifies `AuthorizeOauthAsync` inside the `SecretKeyAuthenticatorService` to strictly bind the lookup of the requested User ID (`requestedUid`) to the record of the successfully authenticated identity (`primaryUid`). The server will no longer load or return session tokens for a requested UID unless it matches the verified, authenticated database record. No known workarounds are available.

### CVE-2026-3869

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-303` |
| Published | 2026-09-11T16:17:06.200 |

CWE-303 : Incorrect Implementation of Authentication Algorithm vulnerability exists that could cause loss of confidentiality, integrity and availability of the PLC provided an application project with a lower application level is running on the PLC.

### CVE-2026-87983

| 項目 | 値 |
|------|-----|
| CVSS | `9.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:H/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-11T15:17:07.240 |

An arbitrary file read vulnerability in Mistral Vibe, introduced in version 2.6.0, allows an attacker to bypass workspace restrictions using quoted absolute paths in allowlisted shell commands. Improper handling of quotation marks during path validation enables files outside the active workspace to be read without user approval.

## 🟠 High（CVSS 7.0〜9.0 未満）

### CVE-2026-90537

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-12T13:16:51.667 |

WWBN AVideo through commit c3edcc274c389816d434acadac07ee78eaf330c1 contains a missing authorization vulnerability in plugin/Scheduler/sendEmail.json.php that allows unauthenticated attackers to access scheduler email jobs by providing a site-wide daily token. Attackers can enumerate scheduler jobs, read private live titles and email addresses, and trigger email sending by supplying any valid daily token obtained from Live pages.

### CVE-2026-15451

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-269` |
| Published | 2026-09-12T13:16:50.940 |

The MemberPress Corporate Accounts plugin for WordPress is vulnerable to Privilege Escalation in versions up to, and including, 1.5.39. This is due to a mass assignment vulnerability in the 'add_sub_account_user' function that passes the raw 'userdata' array to 'wp_insert_user' without filtering dangerous keys like role or ID. This makes it possible for authenticated attackers, with subscriber-level access and above who hold a corporate account, to create new administrator accounts or hijack existing administrator accounts by overwriting their email addresses. The vulnerability was partially patched in version 1.5.39.

### CVE-2026-78175

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-12T08:16:24.507 |

The Tutor LMS – eLearning and online course solution plugin for WordPress is vulnerable to PHP Object Injection in all versions up to, and including, 4.0.7 via the `withdraw_method_field` parameter of the `tutor_save_withdraw_account` AJAX handler. This is due to the handler lacking any capability or role check, relying solely on a nonce, while also passing attacker-supplied values through `esc_sql()`, which replaces every `%` character with a 66-byte HMAC placeholder token before the data is serialized and stored via `update_user_meta()`; when the meta is later retrieved, the placeholder is collapsed back to a single `%`, leaving serialized string length declarations 65 bytes greater than the actual content, and because array keys originate from entirely unescaped POST field names, `unserialize()` over-reads into attacker-controlled bytes, allowing injection of an arbitrary serialized object stream. This makes it possible for authenticated attackers, with subscriber-level access and above, to achieve remote code execution on the server by triggering the `GuzzleHttp\Cookie\FileCookieJar` POP chain, reachable via the `spl_autoload_register` loader in `TUTOR\RestAPI` which loads the plugin's own bundled PayPal Composer autoloader, writing attacker-controlled content to an attacker-specified filename. This has an unauthenticated pathway when user registration is enabled, which is common for students and teachers to register, and it requires the monetization feature to be enabled.

### CVE-2026-89266

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-787` |
| Published | 2026-09-12T00:17:06.440 |

stb_vorbis through 1.22 contains a heap buffer overflow in start_decoder() where the codebook multiplicands allocation size is truncated from size_t to int. Attackers can craft a malicious Ogg Vorbis file with large entries and dimensions values to trigger out-of-bounds writes, causing process crashes or heap corruption.

### CVE-2026-62107

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-502` |
| Published | 2026-09-11T19:17:43.583 |

Unauthenticated PHP Object Injection in Masteriyo - LMS <= 3.4.0 versions.

### CVE-2026-62106

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-11T19:17:43.460 |

Subscriber Privilege Escalation in SMS Alert Order Notifications <= 3.9.9 versions.

### CVE-2026-62102

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-11T19:17:43.073 |

Subscriber Privilege Escalation in Gato GraphQL <= 19.2.3 versions.

### CVE-2026-89009

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-36` |
| Published | 2026-09-11T15:17:08.190 |

WAVLINK WN535M1 and WN535M3 routers running firmware prior to M35M1_V250922 contain an unauthenticated arbitrary file write vulnerability that allows remote attackers to overwrite any file on the device by sending a crafted payload to the sync_server daemon on TCP port 13136. The daemon, which runs as root and requires no authentication, accepts a 100-byte filename field in its protocol header without path canonicalization, allowing attackers to supply an absolute path and write arbitrary content to overwrite startup scripts or credential stores to achieve persistent system compromise.

### CVE-2026-78224

| 項目 | 値 |
|------|-----|
| CVSS | `8.8` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-11T15:17:04.337 |

The XSLT Transformer Step builds a bare TransformerFactory without the proper security options set, so XXE injection can allow data exfiltration and denial-of-service attacks.

### CVE-2026-90444

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-11T22:16:46.390 |

A file-transfer interface that requires valid credentials accepts attacker-controlled filenames without restricting shell metacharacters. An automated process later constructs and runs a system command using the uploaded file's name, allowing an authenticated attacker to embed and execute arbitrary operating system commands with the privileges of that process. This allows an attacker to read and modify ingested log data, and could provide a foothold for further movement within the internal network.

### CVE-2026-44715

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-285` |
| Published | 2026-09-11T22:16:37.113 |

OpenMRS is an open source electronic medical record system platform. Prior to versions 1.23.0 and 2.10.0, an authenticated user can trigger administrative DWR services. Specifically, the `startHl7ArchiveMigration` method is accessible, which should be restricted to admin-level accounts. Versions 1.23.0 and 2.10.0 patch the issue.

### CVE-2026-72708

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T17:18:57.197 |

SPIP before 4.4.18 contains an unauthenticated blind SQL injection vulnerability in the public sitemap endpoint where the MySQL escaper spip_mysql_cite() in ecrire/req/mysql.php returns values unescaped when the target column is a date type and the supplied value matches the pattern of a word character followed by an open parenthesis. Attackers can supply a crafted value such as a time-based payload through the annee parameter in squelettes-dist/sitemap.xml.html to embed arbitrary SQL directly into the generated query, enabling time-based and boolean-based blind SQL injection that can expose arbitrary database content including the alea_ephemere secret used to sign action nonces.

### CVE-2026-89262

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-11T16:17:50.907 |

MoguBlog through 6.2 contains an authorization bypass vulnerability in the comment deletion endpoint that performs ownership checks against request-body fields instead of the authenticated principal. Attackers can delete arbitrary comments and their replies by supplying comment UIDs and author UIDs obtained from unauthenticated listing endpoints.

### CVE-2026-89260

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-11T16:17:50.560 |

MoguBlog through 6.2 contains an XML external entity injection vulnerability in the WeChat callback handler at POST /wechat/wechatCheck. The WechatRestApi.index() method passes the raw request body to SignUtil.xmlToMap(), which uses an unhardened dom4j SAXReader without DTD or external-entity restrictions. Unauthenticated remote attackers can submit DOCTYPE declarations with external parameter entities to read arbitrary local files or trigger outbound HTTP requests, with resolved entities reflected in error responses.

### CVE-2026-89013

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-11T16:17:48.853 |

Dolibarr 23.0.4 before 24.0.1 ontains an authorization bypass vulnerability that allows unauthenticated attackers to read arbitrary files through the document storage endpoints by supplying a crafted hashp parameter value. Attackers can send a request with hashp=shared to skip token validation while satisfying the authorization condition in htdocs/document.php and htdocs/viewimage.php, gaining access to application logs, uploaded business documents, database backups containing password hashes, and files belonging to other multicompany entities.

### CVE-2026-82578

| 項目 | 値 |
|------|-----|
| CVSS | `8.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-611` |
| Published | 2026-09-11T15:17:06.357 |

When XML batch processing is turned on and the XPath option is selected, the raw batch input goes through a default XPath/JAXP setup with no entity restrictions, so XXE injection can allow data exfiltration and denial-of-service attacks.

### CVE-2026-85979

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:H/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-20;CWE-78;CWE-269` |
| Published | 2026-09-11T15:17:06.807 |

Affected versions of Puppet Enterprise contain a command injection vulnerability in the handling of the java_keystore_passwd parameter. An authenticated user with Puppet administrative privileges can inject arbitrary shell commands by providing a specially crafted value for this parameter, which is passed to a shell execution context without sufficient sanitization. Because the resulting commands are executed with root privileges, successful exploitation can lead to full compromise of the affected system.

### CVE-2026-38058

| 項目 | 値 |
|------|-----|
| CVSS | `8.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-497` |
| Published | 2026-09-11T15:17:01.407 |

The endpoint on the iDirect iQ200 VSAT terminal returns the complete device configuration as JSON, including the SECURITY section which contains MD5-crypt password hashes for the root SSH and web administration accounts. Any user with valid web credentials can extract these hashes and crack them offline using commodity hardware.

### CVE-2026-90553

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-94` |
| Published | 2026-09-12T13:16:53.887 |

vLLM before 0.28.0 contains a remote code execution vulnerability in the LlavaOnevision2 processor loader that ignores the trust_remote_code parameter when loading remote processor classes. Attackers can craft a malicious model with arbitrary code in processing_llava_onevision2.py that executes with vLLM process authority even when trust_remote_code is set to False.

### CVE-2026-70341

| 項目 | 値 |
|------|-----|
| CVSS | `8.5` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-416` |
| Published | 2026-09-11T16:17:46.080 |

Use after free in Microsoft Edge (Chromium-based) allows an authorized attacker to execute code over a network.

### CVE-2026-89066

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-78;CWE-88` |
| Published | 2026-09-11T16:17:49.400 |

Improper neutralization of special elements used in an OS command in the task synthesis component in projen before 0.103.0 might allow context-dependent attackers to execute arbitrary commands on a developer workstation or continuous integration runner via shell metacharacters in project configuration values and repository file names that are interpolated into generated task definitions.



To remediate this issue, users should upgrade to version 0.103.0 and then re-synthesize the project so that .projen/tasks.json is regenerated with the corrected task definitions. Upgrading alone is not sufficient because the generated task definition file is committed to the repository.

### CVE-2026-7863

| 項目 | 値 |
|------|-----|
| CVSS | `8.4` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-11T16:17:47.490 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus Software allows OS Command Injection.

This issue affects Pardus Software: before 1.0.5.

### CVE-2026-54174

| 項目 | 値 |
|------|-----|
| CVSS | `8.3` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:H/A:H` |
| Weaknesses | `CWE-345;CWE-354` |
| Published | 2026-09-11T21:17:11.403 |

melange allows users to build apk packages using declarative pipelines. Apko prior to version 1.2.9, corresponding to melange prior to version 0.50.4, verified the control section hash (`.PKGINFO` etc.) against the signed `APKINDEX`, but never verified the data section hash (the actual package files that get installed). An attacker who could compromise a mirror, poison a cache, or MITM a package fetch could substitute arbitrary file contents while the control hash check still passed. Apko version 1.2.9 and melange version 0.50.4 contain a fix.

### CVE-2026-90451

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-1392` |
| Published | 2026-09-11T22:16:47.343 |

An example environment-configuration file ships with a fixed, publicly-known secret value used to sign authentication cookies for a bundled packet-analysis component. A deployment that copies this example file into active configuration without running the setup routine that regenerates the value will use the known default, allowing an attacker aware of the default to forge valid authentication cookies for that component.

### CVE-2026-89090

| 項目 | 値 |
|------|-----|
| CVSS | `8.2` |
| Vector | `CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-248` |
| Published | 2026-09-11T18:17:00.097 |

An unrecovered panic in the event stream header decoder in Amazon AWS SDK for Go v2 before release-2026-03-23 might allow an unauthenticated remote actor to terminate the consuming application process via a crafted event stream response frame containing a header value type outside the valid range.



To remediate this issue, users should upgrade to release-2026-03-23 or later, and patch any forked or derivative code.

### CVE-2026-49464

| 項目 | 値 |
|------|-----|
| CVSS | `8.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-639` |
| Published | 2026-09-11T21:17:10.523 |

NL Portal Backend Libraries provide backend components for Dutch government portals that interact with residents, customers, suppliers, and partner organizations. The `nl.nl-portal:taak` package from version 1.5.0 through 3.0.0 fails to verify ownership when processing the `submitTaakV2` GraphQL mutation, allowing an authenticated user who knows or guesses another user’s task ID to read its form data, overwrite its submitted data, and mark the task as completed. Version 3.0.1 contains a patch. As a workaround, block the `submitTaakV2` mutation at the API gateway or restrict the `/graphql` endpoint to trusted networks

### CVE-2026-8303

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-266` |
| Published | 2026-09-11T15:17:09.667 |

Incorrect privilege assignment vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus-software allows Privilege Escalation.

This issue affects Pardus-software: before 1.0.5.

### CVE-2026-8301

| 項目 | 値 |
|------|-----|
| CVSS | `7.8` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` |
| Weaknesses | `CWE-78` |
| Published | 2026-09-11T15:17:09.540 |

Improper neutralization of special elements used in an OS command ('OS command injection') vulnerability in TUBITAK BILGEM Software Technologies Research Institute Pardus Boot Repair allows OS Command Injection.

This issue affects Pardus Boot Repair: before 1.0.8.

### CVE-2026-89099

| 項目 | 値 |
|------|-----|
| CVSS | `7.7` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-362` |
| Published | 2026-09-11T18:17:00.360 |

A race condition in the document value layer of MongoDB Server can allow concurrent server threads to operate on the same internal memory without synchronization, leading to memory corruption. An authenticated user holding ordinary read-write privileges on a database may be able to trigger this condition over the normal client protocol, resulting in server termination and potential corruption of process memory with user-influenced content. Successful use of this issue may impact the confidentiality, integrity, and availability of the affected server process.

### CVE-2026-90474

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-287` |
| Published | 2026-09-12T11:16:34.483 |

MCPHub before 1.0.32 contains an authentication bypass vulnerability in its embedded OAuth 2.0 authorization server where client authentication is disabled by default and PKCE enforcement is optional. Attackers who obtain an authorization code through interception can redeem it for access tokens without providing a client secret or PKCE verifier, gaining access to victim accounts and their privileges.

### CVE-2026-90460

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:L/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-863` |
| Published | 2026-09-11T22:16:48.243 |

An issue was discovered in OpenStack Keystone before 29.0.3. Tokens obtained via delegated authentication methods (EC2 credentials, application credentials, OAuth1 access tokens, and trusts) are not blocked from creating, modifying, or deleting credentials via the /v3/credentials API. EC2-derived tokens can additionally read credential blobs, exposing TOTP MFA seeds and other secrets. Also, PATCH /v3/credentials does not validate the requested post-update project_id, allowing any delegated token to move a credential to an unauthorized project. All Keystone deployments using delegated authentication are affected.

### CVE-2026-62112

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T19:17:44.113 |

Editor SQL Injection in Amelia <= 2.4.9 versions.

### CVE-2026-62109

| 項目 | 値 |
|------|-----|
| CVSS | `7.6` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:L` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T19:17:43.720 |

Editor SQL Injection in Sky Addons for Elementor <= 3.8.4 versions.

### CVE-2026-85200

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-98` |
| Published | 2026-09-12T08:16:24.810 |

The GEO my WP plugin for WordPress is vulnerable to Local File Inclusion in all versions up to, and including, 4.5.5.3 via the gmw_posts_locator_ajax_info_window_loader function. This makes it possible for unauthenticated attackers to include and execute arbitrary .php files on the server, allowing the execution of any PHP code in those files. This can be used to bypass access controls, obtain sensitive data, or achieve code execution in cases where .php file types can be uploaded and included. In environments where PEAR is installed with register_argc_argv enabled, this file inclusion can be leveraged to write and execute arbitrary PHP code, achieving full remote code execution.

### CVE-2026-16482

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-12T08:16:23.797 |

The rtMedia for WordPress, BuddyPress and bbPress plugin for WordPress is vulnerable to time-based blind SQL Injection via the 'compare' parameter in all versions up to, and including, 4.7.11 due to insufficient escaping on the user supplied parameter and lack of sufficient preparation on the existing SQL query. This makes it possible for unauthenticated attackers to append additional SQL queries into already existing queries that can be used to extract sensitive information from the database. This is exploitable on any public page containing an rtMedia shortcode (e.g., [rtmedia_gallery]) when the rtmedia_shortcode GET parameter is set, because RTMediaQuery::query() merges $_REQUEST into the internal query while only validating top-level array keys, allowing the nested 'compare' subvalue to reach the vulnerable sink without authentication.

### CVE-2026-50013

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-362;CWE-820` |
| Published | 2026-09-11T22:16:37.813 |

Hoverfly is an open source API simulation tool. Prior to version 1.12.8, when Hoverfly is running in Diff mode, the `AddDiff()` function writes to the shared `responsesDiff` map without any synchronization (no mutex). When multiple proxy requests are processed concurrently (the normal case for any proxy), the concurrent map writes trigger Go's built-in race detector which causes a `fatal error: concurrent map read and map write`, immediately killing the entire Hoverfly process. This is trivially exploitable by sending multiple simultaneous requests. Version 1.12.8 patches the issue.

### CVE-2026-49846

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` |
| Weaknesses | `CWE-22;CWE-697` |
| Published | 2026-09-11T22:16:37.537 |

libks provides foundational support for signalwire C products. Prior to version 2.0.11, `clean_uri()` in libks's HTTP request parser fails to reject URIs whose path has more segments than its internal canonicalization buffer can hold. The canonicalization step silently passes such URIs through with embedded ".." sequences intact, enabling path traversal in any consumer that later joins the URI with a filesystem path. Version 2.0.11 patches the issue.

### CVE-2026-54135

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-770` |
| Published | 2026-09-11T20:17:14.330 |

AirSane is a SANE frontend, and a scanner server that supports Apple's AirScan protocol. Versions prior to 0.4.12 have a vulnerability in the custom HTTP server implementation of AirSane that allows a remote unauthenticated attacker to cause a Denial of Service (DoS) via memory exhaustion (OOM). In httpserver.cpp, the HttpServer::Request::content function reads the Content-Length header and directly passes this value to std::string::resize() without any upper-bound validation or safe parsing. An attacker can send an HTTP POST request with an artificially large Content-Length value. This forces the daemon to attempt allocating gigabytes of memory, resulting in a std::bad_alloc exception and immediately crashing the AirSane process. Additionally, providing non-numeric characters in the Content-Length header leads to undefined behavior (NaN to integer conversion) due to the lack of error handling during header parsing. Version 0.4.12 patches the issue.

### CVE-2026-79393

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-122` |
| Published | 2026-09-11T19:17:46.070 |

A heap-based buffer overflow vulnerability in the WS-Addressing Action transformation function in the Sofia IPC daemon in Xiongmai IP Camera XM530 firmware HMT.CM2005-v220608.1837 and earlier allows remote unauthenticated attackers to cause a denial of service or potentially execute arbitrary code via a crafted SOAP request containing a wsa5:Action string exceeding 128 bytes.

### CVE-2026-68497

| 項目 | 値 |
|------|-----|
| CVSS | `7.5` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` |
| Weaknesses | `CWE-400;CWE-1333` |
| Published | 2026-09-11T16:17:39.610 |

jackson-databind binds a JSON string to a javax.xml.datatype.Duration or javax.xml.datatype.XMLGregorianCalendar field by passing the raw string verbatim to DatatypeFactory.newDuration(value) or newXMLGregorianCalendar(value) in CoreXMLDeserializers.Std._deserialize. These deserializers are registered by default with no opt-in, so a plain ObjectMapper or JsonMapper with no polymorphic typing and no special configuration reaches this path. The XML Schema lexical grammar permits numeric components of arbitrary length, which the JDK materializes through the native BigInteger(String) and BigDecimal(String) constructors, both quadratic in digit count. Because the digits sit inside a JSON string token rather than a JSON number token, jackson-core's StreamReadConstraints.maxNumberLength guard never applies; jackson's own NumberDeserializers call validateIntegerLength or validateFPLength before parsing a stringified number, but the XML datatype deserializer omits that pre-check. An unauthenticated attacker can therefore submit a single request of a few megabytes, such as a Duration value consisting of the letter P followed by several million digits and the letter Y, and force tens of seconds to several minutes of single-threaded CPU work; a handful of concurrent requests can saturate a server's worker threads. This affects com.fasterxml.jackson.core:jackson-databind from 2.0.0 before 2.18.10, from 2.19.0 before 2.21.6, and from 2.22.0 before 2.22.2, and tools.jackson.core:jackson-databind from 3.0.0 before 3.1.6 and from 3.2.0 before 3.2.2. Users should upgrade to 2.18.10, 2.21.6, 2.22.2, 3.1.6, or 3.2.2.

### CVE-2026-54241

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-122;CWE-190` |
| Published | 2026-09-11T22:16:38.223 |

libde265 is an open source implementation of the h.265 video codec. Versions prior to 1.1.1 use signed 32-bit arithmetic to calculate the sample adaptive offset input-buffer size, allowing a crafted HEVC stream with large dimensions and 16-bit luma samples to cause an integer overflow, an undersized allocation, and an out-of-bounds heap read that may expose heap data in decoded output or crash the decoder. Version 1.1.1 contains a patch.

### CVE-2026-54240

| 項目 | 値 |
|------|-----|
| CVSS | `7.4` |
| Vector | `CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:H` |
| Weaknesses | `CWE-190;CWE-787` |
| Published | 2026-09-11T22:16:38.083 |

libde265 is an open source implementation of the h.265 video codec. Versions prior to 1.1.1 use signed 32-bit arithmetic to calculate pixel offsets, allowing a crafted HEVC stream with large image dimensions to trigger an integer overflow and cause out-of-bounds heap reads or writes, potentially disclosing data, corrupting memory, or crashing the decoder. Version 1.1.1 contains a patch.

### CVE-2026-47773

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-131;CWE-787` |
| Published | 2026-09-11T21:17:09.940 |

ArduinoBLE enables Bluetooth Low Energy connectivity on certain Arduino models. Versions prior to 2.0.2 contain a missing bounds check in the ATT layer write request handler that allows a remote, unauthenticated BLE client to corrupt memory in the ATTClass global object. Devices running ArduinoBLE with one or more characteristics configured with the BLEEncryption property are affected. The fix is included starting from the 2.0.2 release.

### CVE-2026-87020

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-190` |
| Published | 2026-09-11T15:17:06.937 |

An integer overflow in a specified pitch and buffer-size computation leads to a heap out-of-bounds write when Orthanc DICOM Server decodes an attacker-supplied PNG.

### CVE-2026-82583

| 項目 | 値 |
|------|-----|
| CVSS | `7.2` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:L/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-89` |
| Published | 2026-09-11T15:17:06.510 |

NextGen Connect (Mirth Connect) versions 4.7.1 and earlier allow an authenticated user to execute arbitrary SQL through a Database Connector API, which could result in disclosure of stored credentials for connected systems, arbitrary file write, and a denial-of-service condition.

### CVE-2026-90555

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-409` |
| Published | 2026-09-12T13:16:54.180 |

vLLM versions before 0.28.0 fail to validate audio sample rate headers in the transcription endpoint, allowing authenticated clients to bypass duration checks. Attackers can submit forged FLAC headers with inflated sample rates to trigger excessive memory allocation and crash the API server process affecting all tenants.

### CVE-2026-90448

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-11T22:16:46.950 |

A deployment mode intended to expose only read access to stored data proxies a set of application programming interface routes without restricting which request methods are allowed. One such route accepts a request that creates or overwrites a stored record, including an attacker-chosen identifier, using the application's own elevated backend credentials. This allows an authenticated user on a deployment intended to be read-only to forge or overwrite stored records that should not be modifiable in that deployment mode.

### CVE-2026-90447

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-290` |
| Published | 2026-09-11T22:16:46.797 |

A routing rule selects between two different authentication mechanisms for the same downstream service based on the value of a client-supplied request header, rather than on any property the client cannot control. An authenticated user in possession of a shared service credential can set this header to route around the primary role-based authorization check and reach the alternate path's fixed, elevated role instead. This allows a low-privileged authenticated attacker who knows the shared credential to perform actions reserved for a higher-privileged role.

### CVE-2026-90445

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-22` |
| Published | 2026-09-11T22:16:46.510 |

An interface that accepts file uploads from authenticated users extracts the contents of uploaded archives without validating that extracted file paths remain within the intended destination directory. This allows an authenticated attacker to craft an archive whose entries traverse outside the destination directory, causing the extraction process to write files to arbitrary locations with the privileges of that process. This could allow an attacker to inject fabricated records into the system's stored data or tamper with application configuration.

### CVE-2026-54166

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:L` |
| Weaknesses | `CWE-918` |
| Published | 2026-09-11T21:17:11.247 |

Shelf is a platform for tracking physical assets. Prior to version 1.20.3, authenticated users with the `asset:import` permission can trigger server-side HTTP requests to attacker-controlled URLs through the Asset CSV Content Import feature. The `imageUrl` validation logic can be bypassed through multiple techniques, including image-extension suffixes, image-related path keywords, domain substring matching, and redirect chains. After validation, the server performs an unrestricted `fetch()` request to the supplied URL. This results in a Server-Side Request Forgery (SSRF) vulnerability that allows attackers to reach internal network services, cloud metadata endpoints, and arbitrary external hosts from the application's network context. Additionally, response bodies are fully buffered before size validation, creating a potential memory exhaustion vector. Version 1.20.3 patches the issue.

### CVE-2026-62089

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:H` |
| Weaknesses | `CWE-862` |
| Published | 2026-09-11T19:17:42.943 |

Missing Authorization vulnerability in Pixar Labs Master Addons for Elementor allows Privilege Abuse.

This issue affects Master Addons for Elementor: from n/a through 3.2.2.

### CVE-2026-78807

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N` |
| Weaknesses | `CWE-346` |
| Published | 2026-09-11T18:16:58.120 |

An issue in wpa_supplicant all versions before v.2.12 allows a local attacker to bypass proper network context and AKMP matching for PMKSA caching via missing validation in the driver based PMKSA selection path in wpa.c

### CVE-2026-89012

| 項目 | 値 |
|------|-----|
| CVSS | `7.1` |
| Vector | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-178` |
| Published | 2026-09-11T16:17:48.680 |

Dolibarr 24.0.0 before 24.0.1 contains a case-sensitive denylist bypass vulnerability in the sqlfilters API query parameter that allows authenticated attackers to recover protected database fields by supplying uppercase variants of denylist-protected field names. Attackers can exploit the case-insensitive database column resolution against the case-sensitive denylist check in the core library to use prefix-matching predicates as a boolean oracle and extract full password hashes for any user account, including administrators.

### CVE-2026-85083

| 項目 | 値 |
|------|-----|
| CVSS | `7.0` |
| Vector | `CVSS:4.0/AV:P/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X` |
| Weaknesses | `CWE-798` |
| Published | 2026-09-11T15:17:06.660 |

The ANJIA AJL33PC0801 IP camera uses a hard-coded credential for bootloader authentication. An attacker with physical access to the device may leverage this weakness to gain privileged bootloader access, allowing unauthorized modification of firmware and system configuration and potentially resulting in complete device compromise.
